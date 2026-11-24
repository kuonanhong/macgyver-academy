#!/usr/bin/env python3
"""Publish the reviewed six-film package to YouTube, with private resumable state.

No operation runs on import. Every phase verifies the authorized channel before
any remote mutation. Uncertain mutations fail closed and are reconciled on rerun.
The client/token files and access token are never copied to state or reports.
"""
from __future__ import annotations

import argparse
import contextlib
import copy
import hashlib
import json
import os
from pathlib import Path
import re
import secrets
import stat
import sys
import tempfile
import time
from urllib.parse import urlencode, urlsplit
from urllib.error import HTTPError
from urllib.request import HTTPRedirectHandler, ProxyHandler, Request, build_opener

API = "https://www.googleapis.com/youtube/v3/"
UPLOAD = "https://www.googleapis.com/upload/youtube/v3/"
TOKEN_URL = "https://oauth2.googleapis.com/token"
IDS = ("interposer", "fanout", "hybrid", "bridge", "chiplet", "thermal")
LANGUAGES = ("zh-TW", "en", "ja", "ko", "zh-CN")
CAPTION_CODES = {"zh-TW": "zh-Hant", "en": "en", "ja": "ja", "ko": "ko", "zh-CN": "zh-Hans"}
LINE_URL = "https://line.me/R/ti/p/%40530pgchc"
CHUNK_BYTES = 8 * 1024 * 1024
QUOTA_REASONS = {"quotaExceeded", "dailyLimitExceeded", "dailyLimitExceededUnreg", "uploadLimitExceeded"}


class SafeError(Exception):
    def __init__(self, reason: str, status: int = 0):
        self.reason = reason if re.fullmatch(r"[A-Za-z][A-Za-z0-9_.-]{0,95}", reason or "") else "RemoteError"
        self.status = int(status)
        super().__init__(self.reason)

    def public(self):
        return {"status": self.status, "reason": self.reason}


class Reply:
    def __init__(self, status, headers=None, body=b""):
        self.status = int(status)
        self.headers = {str(k).lower(): str(v) for k, v in (headers or {}).items()}
        self.body = body.encode() if isinstance(body, str) else body

    def json(self):
        try:
            value = json.loads(self.body or b"{}")
            if not isinstance(value, dict):
                raise ValueError()
            return value
        except (ValueError, UnicodeError, TypeError):
            raise SafeError("InvalidJsonResponse", self.status) from None


def official_url(url):
    """Do not send credentials to redirects, userinfo, lookalike hosts or ports."""
    p = urlsplit(url)
    if p.scheme != "https" or p.username or p.password or p.port not in (None, 443) or p.fragment:
        raise SafeError("NonOfficialEndpoint")
    if url == TOKEN_URL:
        return
    if p.hostname != "www.googleapis.com":
        raise SafeError("NonOfficialEndpoint")
    if not (p.path.startswith("/youtube/v3/") or p.path.startswith("/upload/youtube/v3/")):
        raise SafeError("NonOfficialEndpoint")


def resumable_url(url):
    official_url(url)
    if urlsplit(url).path != "/upload/youtube/v3/videos":
        raise SafeError("InvalidResumableEndpoint")
    return url


class NoRedirectHandler(HTTPRedirectHandler):
    def redirect_request(self, req, fp, code, msg, headers, newurl):
        # Authorization and resumable URLs must never follow a redirect.
        return None


class StdlibTransport:
    def __init__(self, opener=None):
        # urllib does not read .netrc. Explicitly disable environment proxies;
        # its default HTTPS handler still performs certificate verification.
        self.opener = opener if opener is not None else build_opener(ProxyHandler({}), NoRedirectHandler())

    def request(self, method, url, headers=None, body=None):
        official_url(url)
        try:
            request = Request(url, data=body, headers=dict(headers or {}), method=method)
            try:
                with self.opener.open(request, timeout=180) as response:
                    return Reply(response.status, response.headers, response.read())
            except HTTPError as response:
                # urllib reports 308 and other non-2xx responses as HTTPError.
                # Preserve them for the resumable protocol and API error parser.
                with response:
                    return Reply(response.code, response.headers, response.read())
        except Exception:
            # urllib exceptions can contain the resumable URI; never expose it.
            raise SafeError("NetworkError") from None


def error_from_reply(reply):
    reason = "HttpError"
    try:
        error = reply.json().get("error", {})
        if isinstance(error, str):
            reason = error
        elif isinstance(error, dict):
            entries = error.get("errors") or []
            reason = (entries[0].get("reason") if entries else error.get("status")) or reason
    except SafeError:
        pass
    return SafeError(reason, reply.status)


def load_json(path):
    try:
        value = json.loads(Path(path).read_text(encoding="utf-8"))
        if not isinstance(value, dict):
            raise ValueError()
        return value
    except (OSError, ValueError, UnicodeError):
        raise SafeError("InvalidLocalJson") from None


def digest_file(path):
    h = hashlib.sha256()
    try:
        with Path(path).open("rb") as f:
            for chunk in iter(lambda: f.read(1024 * 1024), b""):
                h.update(chunk)
        return h.hexdigest()
    except OSError:
        raise SafeError("AssetReadFailed") from None


def digest_json(value):
    return hashlib.sha256(json.dumps(value, sort_keys=True, ensure_ascii=False,
                                     separators=(",", ":")).encode()).hexdigest()


def resolve_metadata_paths(metadata, metadata_path):
    """Resolve asset paths relative to the job file, without changing its binding."""
    result = copy.deepcopy(metadata)
    # Historical schema-1 jobs used the caller's project directory. Preserve
    # that interpretation for existing bound V33 state; V34 opts into portability.
    portable = metadata.get("pathResolutionMode") == "metadata-relative" or metadata.get("schemaVersion", 1) >= 2
    base = Path(metadata_path).absolute().resolve().parent if portable else Path.cwd().resolve()
    def resolve(value):
        if not isinstance(value, str) or not value:
            raise SafeError("InvalidAssetPath")
        path = Path(value)
        return str(path if path.is_absolute() else (base / path).resolve())
    if result.get("mediaManifest"):
        result["mediaManifest"] = resolve(result["mediaManifest"])
    for video in result.get("videos", []):
        video["videoFile"] = resolve(video.get("videoFile"))
        for track in video.get("subtitleTracks", []):
            track["file"] = resolve(track.get("file"))
            if track.get("srtFile"):
                track["srtFile"] = resolve(track["srtFile"])
        for track in video.get("audioTracks", []):
            track["file"] = resolve(track.get("file"))
    return result


class OAuth:
    def __init__(self, transport, client_path, token_path):
        # Loaded only on explicit CLI execution, never by tests or import.
        installed = load_json(client_path).get("installed", {})
        token = load_json(token_path)
        if not isinstance(installed, dict):
            raise SafeError("InstalledOAuthClientRequired")
        self.client_id = installed.get("client_id")
        self.client_secret = installed.get("client_secret")
        self.refresh_token = token.get("refresh_token")
        if not all(isinstance(v, str) and v for v in (self.client_id, self.client_secret, self.refresh_token)):
            raise SafeError("OAuthCredentialsIncomplete")
        if installed.get("token_uri", TOKEN_URL) != TOKEN_URL:
            raise SafeError("NonOfficialTokenEndpoint")
        scope = token.get("scope", "")
        scopes = set(scope.split() if isinstance(scope, str) else scope if isinstance(scope, list) else [])
        if not scopes.intersection({"https://www.googleapis.com/auth/youtube",
                                    "https://www.googleapis.com/auth/youtube.force-ssl"}):
            raise SafeError("YouTubeWriteScopeRequired")
        self.transport, self.access_token, self.expires = transport, None, 0

    def access(self, force=False):
        if force or not self.access_token or time.monotonic() >= self.expires:
            data = urlencode({"client_id": self.client_id, "client_secret": self.client_secret,
                              "refresh_token": self.refresh_token, "grant_type": "refresh_token"}).encode()
            r = self.transport.request("POST", TOKEN_URL,
                {"Content-Type": "application/x-www-form-urlencoded"}, data)
            if r.status != 200:
                raise error_from_reply(r)
            result = r.json()
            access = result.get("access_token")
            if not isinstance(access, str) or not access:
                raise SafeError("MissingAccessToken")
            self.access_token = access
            self.expires = time.monotonic() + max(1, int(result.get("expires_in", 3600)) - 60)
        return self.access_token


class GoogleAPI:
    def __init__(self, transport, token_provider):
        self.transport, self.token_provider = transport, token_provider

    def request(self, method, url, *, headers=None, body=None, json_body=None, ok=(200,)):
        official_url(url)
        outgoing = dict(headers or {})
        if json_body is not None:
            outgoing["Content-Type"] = "application/json; charset=UTF-8"
            body = json.dumps(json_body, ensure_ascii=False).encode()
        for attempt in range(2):
            outgoing["Authorization"] = "Bearer " + self.token_provider.access(force=bool(attempt))
            r = self.transport.request(method, url, outgoing, body)
            if r.status != 401 or attempt:
                break
        if r.status not in ok:
            raise error_from_reply(r)
        return r

    def call(self, method, resource, params=None, body=None):
        url = API + resource + ("?" + urlencode(params) if params else "")
        return self.request(method, url, json_body=body, ok=(200, 201)).json()

    def all_items(self, resource, params):
        result, page, seen = [], None, set()
        for _ in range(1000):
            query = dict(params, maxResults=50)
            if page:
                query["pageToken"] = page
            data = self.call("GET", resource, query)
            result.extend(data.get("items", []))
            page = data.get("nextPageToken")
            if not page:
                return result
            if page in seen:
                break
            seen.add(page)
        raise SafeError("IncompletePagination")


def secure_directory(path):
    p = Path(path).absolute()
    if any(parent.is_symlink() for parent in (p, *p.parents)):
        raise SafeError("SymlinkStateDirectory")
    p.mkdir(mode=0o700, parents=True, exist_ok=True)
    if not p.is_dir():
        raise SafeError("InvalidStateDirectory")
    os.chmod(p, 0o700)
    return p


class PrivateState:
    def __init__(self, directory, expected_channel, metadata, manifest):
        self.directory = secure_directory(directory)
        self.path = self.directory / "youtube-upload-state-v33.json"
        if self.path.is_symlink():
            raise SafeError("SymlinkStateFile")
        binding = {"channel": expected_channel, "metadataSha256": digest_json(metadata),
                   "manifestSha256": digest_json(manifest)}
        if self.path.exists():
            os.chmod(self.path, 0o600)
            self.data = load_json(self.path)
            if self.data.get("binding") != binding or self.data.get("version") != 1:
                raise SafeError("StateBindingMismatch")
        else:
            self.data = {"version": 1, "binding": binding, "job": secrets.token_hex(12),
                         "playlist": {}, "videos": {key: {} for key in IDS}}
            self.save()

    def save(self):
        fd, name = tempfile.mkstemp(prefix=".youtube-state-", suffix=".json", dir=self.directory)
        try:
            os.fchmod(fd, 0o600)
            with os.fdopen(fd, "w", encoding="utf-8") as f:
                json.dump(self.data, f, ensure_ascii=False, indent=2)
                f.write("\n")
                f.flush()
                os.fsync(f.fileno())
            os.replace(name, self.path)
            os.chmod(self.path, 0o600)
        finally:
            with contextlib.suppress(FileNotFoundError):
                os.unlink(name)


@contextlib.contextmanager
def state_lock(directory):
    p = secure_directory(directory) / ".publisher.lock"
    try:
        fd = os.open(p, os.O_CREAT | os.O_EXCL | os.O_WRONLY, 0o600)
    except FileExistsError:
        raise SafeError("PublisherLocked") from None
    try:
        with os.fdopen(fd, "w") as f:
            f.write(str(os.getpid()))
        yield
    finally:
        with contextlib.suppress(FileNotFoundError):
            p.unlink()


def normalize_language(value):
    return {"zh-Hant": "zh-TW", "zh-Hant-TW": "zh-TW", "zh-TW": "zh-TW",
            "zh-Hans": "zh-CN", "zh-Hans-CN": "zh-CN", "zh-CN": "zh-CN",
            "en-US": "en", "en-GB": "en", "ja-JP": "ja", "ko-KR": "ko"}.get(value, value)


def uncertain(error):
    return error.status == 0 or error.status >= 500


class Publisher:
    def __init__(self, api, state, metadata, manifest, expected_channel, require_qr=False):
        self.api, self.state, self.metadata, self.manifest = api, state, metadata, manifest
        self.expected_channel, self.channel = expected_channel, None
        items = metadata.get("videos", [])
        assets = manifest.get("videos", [])
        if [v.get("id") for v in items] != list(IDS) or len(assets) != 6 or {v.get("id") for v in assets} != set(IDS):
            raise SafeError("ExactlySixKnownVideosRequired")
        self.videos = {v["id"]: v for v in items}
        self.assets = {v["id"]: v for v in assets}
        for i, v in enumerate(items):
            if v.get("playlistPosition") != i or not isinstance(v.get("title"), str) or not 1 <= len(v["title"]) <= 100:
                raise SafeError("InvalidVideoMetadata")
            if not isinstance(v.get("description"), str) or len(v["description"].encode("utf-8")) > 5000:
                raise SafeError("InvalidVideoMetadata")
            if "localizations" in v:
                localized = v["localizations"]
                if not isinstance(localized, dict) or not localized or not v.get("defaultLanguage"):
                    raise SafeError("InvalidLocalizedMetadata")
                for language, value in localized.items():
                    if language not in LANGUAGES or not isinstance(value, dict):
                        raise SafeError("InvalidLocalizedMetadata")
                    title, description = value.get("title"), value.get("description")
                    if (not isinstance(title, str) or not 1 <= len(title) <= 100
                            or not isinstance(description, str) or len(description.encode("utf-8")) > 5000
                            or any(c in title + description for c in "<>")):
                        raise SafeError("InvalidLocalizedMetadata")
            if v.get("durationSeconds") != 300:
                raise SafeError("UnexpectedVideoDuration")
            tracks = v.get("subtitleTracks", [])
            if len(tracks) != 5 or {t.get("language") for t in tracks} != set(LANGUAGES):
                raise SafeError("FiveCaptionLanguagesRequired")
        playlist = metadata.get("playlist", {})
        if not isinstance(playlist.get("title"), str) or not playlist["title"] or not isinstance(playlist.get("description"), str):
            raise SafeError("InvalidPlaylistMetadata")
        if manifest.get("status") != "PASS":
            raise SafeError("ManifestNotValidated")
        if require_qr:
            card = manifest.get("endCard", {})
            if card.get("url") != LINE_URL or card.get("startSeconds") != 290 or card.get("endSeconds") != 300 or card.get("verified") is not True:
                raise SafeError("VerifiedLineEndCardRequired")

    def verify_channel(self):
        result = self.api.call("GET", "channels", {"part": "id,snippet,contentDetails", "mine": "true"})
        items = result.get("items", [])
        if len(items) != 1 or items[0].get("id") != self.expected_channel:
            raise SafeError("ChannelMismatch")
        self.channel = items[0]

    def require_channel(self):
        if not self.channel or self.channel.get("id") != self.expected_channel:
            raise SafeError("ChannelNotVerified")

    def preflight_videos(self):
        for key in IDS:
            asset, video = self.assets[key], self.videos[key]
            sha, size = asset.get("sha256"), asset.get("bytes")
            if not isinstance(sha, str) or not re.fullmatch(r"[a-f0-9]{64}", sha) or not isinstance(size, int) or size <= 0:
                raise SafeError("InvalidManifestHash")
            p = Path(video["videoFile"])
            try:
                good_size = p.is_file() and not p.is_symlink() and p.stat().st_size == size
            except OSError:
                good_size = False
            if not good_size or digest_file(p) != sha:
                raise SafeError("ManifestMismatch")
            if float(asset.get("duration", 0)) != 300 or asset.get("chapters") != 10:
                raise SafeError("InvalidManifestTiming")
            if set(asset.get("subtitleLanguages", [])) != set(LANGUAGES):
                raise SafeError("InvalidManifestLanguages")

    def playlist(self):
        self.require_channel()
        saved = self.state.data["playlist"]
        title = self.metadata["playlist"]["title"]
        if saved.get("id"):
            self.check_playlist()
            return
        matches = [p for p in self.api.all_items("playlists", {"part": "snippet,status", "mine": "true"})
                   if p.get("snippet", {}).get("title") == title]
        if len(matches) > 1:
            raise SafeError("AmbiguousPlaylistTitle")
        if matches:
            self._remember_playlist(matches[0])
            return
        if self.metadata["playlist"].get("requireExisting") is True:
            raise SafeError("ExistingPlaylistNotFound")
        if saved.get("pending"):
            raise SafeError("PlaylistCreateOutcomeUnknown")
        saved["pending"] = True
        self.state.save()
        try:
            item = self.api.call("POST", "playlists", {"part": "snippet,status"},
                {"snippet": {"title": title, "description": self.metadata["playlist"]["description"]},
                 "status": {"privacyStatus": "public"}})
        except SafeError as e:
            if not uncertain(e):
                saved.pop("pending", None)
                self.state.save()
            raise
        self._remember_playlist(item)

    def _remember_playlist(self, item):
        if not item.get("id") or item.get("snippet", {}).get("channelId") != self.expected_channel:
            raise SafeError("PlaylistOwnerMismatch")
        if item.get("status", {}).get("privacyStatus") != "public":
            raise SafeError("ExistingPlaylistNotPublic")
        self.state.data["playlist"] = {"id": item["id"], "title": item["snippet"]["title"], "status": "public"}
        self.state.save()

    def check_playlist(self):
        self.require_channel()
        pid = self.state.data["playlist"].get("id")
        if not pid:
            raise SafeError("RunPlaylistPhaseFirst")
        data = self.api.call("GET", "playlists", {"part": "snippet,status", "id": pid})
        items = data.get("items", [])
        if len(items) != 1 or items[0].get("snippet", {}).get("channelId") != self.expected_channel:
            raise SafeError("PlaylistOwnerMismatch")
        if items[0].get("status", {}).get("privacyStatus") != "public":
            raise SafeError("ExistingPlaylistNotPublic")
        if items[0].get("snippet", {}).get("title") != self.metadata["playlist"]["title"]:
            raise SafeError("PlaylistTitleMismatch")
        return pid

    def marker(self, key):
        return "macgyver-v33-" + self.state.data["job"] + "-" + key

    def get_video(self, vid):
        result = self.api.call("GET", "videos", {"part": "snippet,status,processingDetails", "id": vid})
        items = result.get("items", [])
        if len(items) != 1 or items[0].get("snippet", {}).get("channelId") != self.expected_channel:
            raise SafeError("VideoMissingOrWrongOwner")
        return items[0]

    def recover_video(self, key):
        uploads = self.channel.get("contentDetails", {}).get("relatedPlaylists", {}).get("uploads")
        if not uploads:
            raise SafeError("MissingUploadsPlaylist")
        items = self.api.all_items("playlistItems", {"part": "contentDetails", "playlistId": uploads})
        ids = [p.get("contentDetails", {}).get("videoId") for p in items]
        matches = []
        for offset in range(0, len(ids), 50):
            batch = [v for v in ids[offset:offset+50] if v]
            if not batch:
                continue
            data = self.api.call("GET", "videos", {"part": "snippet,status", "id": ",".join(batch)})
            matches.extend(v for v in data.get("items", [])
                           if v.get("snippet", {}).get("channelId") == self.expected_channel
                           and self.marker(key) in v.get("snippet", {}).get("tags", []))
        if len(matches) > 1:
            raise SafeError("DuplicateRecoveryMarker")
        if matches:
            self._complete_video(key, matches[0])
            return True
        return False

    def _complete_video(self, key, item):
        vid = item.get("id")
        if not isinstance(vid, str) or not re.fullmatch(r"[A-Za-z0-9_-]{11}", vid):
            raise SafeError("InvalidUploadedVideoId")
        entry = self.state.data["videos"][key]
        entry.update({"id": vid, "title": self.videos[key]["title"], "uploadStatus": "uploaded"})
        entry.pop("session", None)
        entry.pop("offset", None)
        self.state.save()

    def videos_phase(self):
        self.require_channel()
        self.preflight_videos()  # All six pass before ANY upload begins.
        self.check_playlist()
        for key in IDS:
            self.upload_video(key)
            self.ensure_playlist_item(key)

    def upload_video(self, key):
        self.require_channel()
        entry = self.state.data["videos"][key]
        if entry.get("id"):
            self.get_video(entry["id"])
            return
        video, asset = self.videos[key], self.assets[key]
        total = asset["bytes"]
        if entry.get("session"):
            session = resumable_url(entry["session"])
            r = self.api.request("PUT", session,
                headers={"Content-Length": "0", "Content-Range": "bytes */" + str(total)},
                body=b"", ok=(200, 201, 308, 404, 410))
            if r.status in (200, 201):
                self._complete_video(key, r.json())
                return
            if r.status in (404, 410):
                if self.recover_video(key):
                    return
                raise SafeError("ExpiredSessionOutcomeUnknown", r.status)
            offset = self.upload_offset(r, total)
        else:
            body = {"snippet": {"title": video["title"], "description": video["description"],
                    "categoryId": "27", "defaultLanguage": video.get("defaultLanguage", "zh-TW"),
                    "tags": ["MacGyver Engineering Academy", "Advanced Packaging", self.marker(key)]},
                    "status": {"privacyStatus": "public", "selfDeclaredMadeForKids": False,
                               "containsSyntheticMedia": True}}
            parts = "snippet,status"
            if video.get("localizations"):
                body["localizations"] = video["localizations"]
                parts += ",localizations"
            url = UPLOAD + "videos?" + urlencode({"uploadType": "resumable", "part": parts,
                                                  "notifySubscribers": "false"})
            r = self.api.request("POST", url, json_body=body,
                headers={"X-Upload-Content-Length": str(total), "X-Upload-Content-Type": "video/mp4"},
                ok=(200, 201))
            session = resumable_url(r.headers.get("location", ""))
            offset = 0
            entry.update({"session": session, "offset": 0, "sha256": asset["sha256"], "bytes": total})
            self.state.save()
        if entry.get("sha256") != asset["sha256"] or entry.get("bytes") != total:
            raise SafeError("ResumableAssetMismatch")
        if offset >= total:
            raise SafeError("UploadCompletionPending")
        with Path(video["videoFile"]).open("rb") as f:
            f.seek(offset)
            while offset < total:
                chunk = f.read(min(CHUNK_BYTES, total-offset))
                if not chunk:
                    raise SafeError("AssetChangedDuringUpload")
                end = offset + len(chunk) - 1
                r = self.api.request("PUT", session,
                    headers={"Content-Length": str(len(chunk)), "Content-Type": "video/mp4",
                             "Content-Range": f"bytes {offset}-{end}/{total}"}, body=chunk,
                    ok=(200, 201, 308))
                if r.status in (200, 201):
                    self._complete_video(key, r.json())
                    return
                acknowledged = self.upload_offset(r, total)
                if acknowledged <= offset or acknowledged > end+1:
                    raise SafeError("UnexpectedUploadProgress")
                offset = acknowledged
                entry["offset"] = offset
                self.state.save()
                f.seek(offset)
        raise SafeError("UploadCompletionPending")

    @staticmethod
    def upload_offset(reply, total):
        value = reply.headers.get("range")
        if value is None:
            return 0
        match = re.fullmatch(r"bytes=0-(\d+)", value)
        if not match or int(match[1]) >= total:
            raise SafeError("InvalidResumableRange")
        return int(match[1]) + 1

    def ensure_playlist_item(self, key):
        entry = self.state.data["videos"][key]
        pid = self.state.data["playlist"]["id"]
        vid, position = entry["id"], self.videos[key]["playlistPosition"]
        all_items = self.api.all_items("playlistItems", {"part": "snippet,contentDetails", "playlistId": pid})
        known = {v.get("id") for v in self.state.data["videos"].values() if v.get("id")}
        if any(p.get("contentDetails", {}).get("videoId") not in known for p in all_items):
            raise SafeError("PlaylistContainsUnrelatedVideos")
        matches = [p for p in all_items if p.get("contentDetails", {}).get("videoId") == vid]
        if len(matches) > 1:
            raise SafeError("DuplicatePlaylistItems")
        snippet = {"playlistId": pid, "position": position,
                   "resourceId": {"kind": "youtube#video", "videoId": vid}}
        if matches:
            found = matches[0]
            if found.get("snippet", {}).get("position") != position:
                self.api.call("PUT", "playlistItems", {"part": "snippet"}, {"id": found["id"], "snippet": snippet})
            entry["playlistItemId"] = found["id"]
            entry.pop("playlistPending", None)
            self.state.save()
            return
        if entry.get("playlistPending"):
            raise SafeError("PlaylistInsertOutcomeUnknown")
        entry["playlistPending"] = True
        self.state.save()
        try:
            item = self.api.call("POST", "playlistItems", {"part": "snippet"}, {"snippet": snippet})
        except SafeError as e:
            if not uncertain(e):
                entry.pop("playlistPending", None)
                self.state.save()
            raise
        if not item.get("id"):
            raise SafeError("MissingPlaylistItemId")
        entry["playlistItemId"] = item["id"]
        entry.pop("playlistPending", None)
        self.state.save()

    def caption_items(self, vid):
        return self.api.call("GET", "captions", {"part": "snippet", "videoId": vid}).get("items", [])

    def captions_phase(self):
        self.require_channel()
        self.check_playlist()
        # Validate ALL original subtitle bytes before uploading any caption.
        for video in self.videos.values():
            for track in video["subtitleTracks"]:
                p = Path(track["file"])
                if not re.fullmatch(r"[a-f0-9]{64}", track.get("sha256", "")) or digest_file(p) != track["sha256"]:
                    raise SafeError("CaptionHashMismatch")
                if not p.read_bytes().lstrip(b"\xef\xbb\xbf").startswith(b"WEBVTT"):
                    raise SafeError("WebVttRequired")
        listed = {}
        for key in IDS:
            vid = self.state.data["videos"][key].get("id")
            if not vid:
                raise SafeError("UploadAllVideosBeforeCaptions")
            self.get_video(vid)
            listed[key] = self.caption_items(vid)
        # Language first: all six Traditional Chinese tracks, then English, etc.
        for language in LANGUAGES:
            for key in IDS:
                self.upload_caption(key, language, listed[key])

    def upload_caption(self, key, language, existing):
        entry = self.state.data["videos"][key]
        entry.pop("captionVerification", None)
        captions = entry.setdefault("captions", {})
        matches = [c for c in existing if normalize_language(c.get("snippet", {}).get("language")) == language
                   and c.get("snippet", {}).get("trackKind") != "ASR"]
        if len(matches) > 1:
            raise SafeError("DuplicateCaptionLanguage")
        if matches:
            c = matches[0]
            captions[language] = {"id": c["id"], "status": c.get("snippet", {}).get("status", "unknown")}
            self.state.save()
            if captions[language]["status"] == "failed":
                raise SafeError("CaptionProcessingFailed")
            return
        previous = captions.get(language, {})
        if previous.get("pending") or previous.get("id"):
            raise SafeError("CaptionUploadOutcomeUnknown")
        track = next(t for t in self.videos[key]["subtitleTracks"] if t["language"] == language)
        content = Path(track["file"]).read_bytes()
        boundary = "macgyver_" + secrets.token_hex(20)
        info = {"snippet": {"videoId": entry["id"], "language": CAPTION_CODES[language],
                            "name": track.get("label", language) + " · MacGyver v33", "isDraft": False}}
        payload = (f"--{boundary}\r\nContent-Type: application/json; charset=UTF-8\r\n\r\n".encode()
                   + json.dumps(info, ensure_ascii=False).encode()
                   + f"\r\n--{boundary}\r\nContent-Type: text/vtt; charset=UTF-8\r\n\r\n".encode()
                   + content + f"\r\n--{boundary}--\r\n".encode())
        captions[language] = {"pending": True}
        self.state.save()
        try:
            item = self.api.request("POST", UPLOAD + "captions?uploadType=multipart&part=snippet",
                headers={"Content-Type": "multipart/related; boundary=" + boundary}, body=payload,
                ok=(200, 201)).json()
        except SafeError as e:
            if not uncertain(e):
                captions.pop(language, None)
                self.state.save()
            raise
        if not item.get("id"):
            raise SafeError("MissingCaptionId")
        captions[language] = {"id": item["id"], "status": item.get("snippet", {}).get("status", "syncing")}
        existing.append(item)
        self.state.save()

    def verify(self):
        self.require_channel()
        pid = self.check_playlist()
        playlist = self.api.all_items("playlistItems", {"part": "snippet,contentDetails", "playlistId": pid})
        ordered = [p.get("contentDetails", {}).get("videoId") for p in
                   sorted(playlist, key=lambda p: p.get("snippet", {}).get("position", -1))]
        desired = [self.state.data["videos"][k].get("id") for k in IDS]
        self.state.data["playlist"]["orderStatus"] = "PASS" if ordered == desired and all(desired) else "MISMATCH"
        for key in IDS:
            entry = self.state.data["videos"][key]
            if not entry.get("id"):
                continue
            item = self.get_video(entry["id"])
            entry["remoteTitle"] = item.get("snippet", {}).get("title", "")
            status = item.get("status", {})
            entry["verification"] = {"privacy": status.get("privacyStatus", "unknown"),
                "upload": status.get("uploadStatus", "unknown"),
                "processing": item.get("processingDetails", {}).get("processingStatus", "unknown"),
                "madeForKids": status.get("madeForKids", status.get("selfDeclaredMadeForKids")),
                "containsSyntheticMedia": status.get("containsSyntheticMedia"),
                "playlistPosition": ordered.index(entry["id"]) if entry["id"] in ordered else None,
                "expectedPlaylistPosition": self.videos[key]["playlistPosition"]}
            # Keep unresolved upload intent: a read-only verification must never
            # erase the guard against repeating an uncertain caption mutation.
            entry["captionVerification"] = {language: "missing" for language in LANGUAGES}
            observed = set()
            for c in self.caption_items(entry["id"]):
                snippet = c.get("snippet", {})
                language = normalize_language(snippet.get("language"))
                if language in LANGUAGES and snippet.get("trackKind") != "ASR":
                    if language in observed:
                        entry["captionVerification"][language] = "duplicate"
                    else:
                        status = snippet.get("status", "unknown")
                        entry.setdefault("captions", {})[language] = {"id": c["id"], "status": status}
                        entry["captionVerification"][language] = status
                    observed.add(language)
            self.state.save()
        self.state.save()

    def run(self, phase):
        self.verify_channel()
        {"playlist": self.playlist, "videos": self.videos_phase,
         "captions": self.captions_phase, "verify": self.verify}[phase]()

    def public_report(self, status="saved"):
        p = self.state.data["playlist"]
        result = {"status": status, "playlist": {"id": p.get("id"),
                  "url": "https://www.youtube.com/playlist?list=" + p["id"] if p.get("id") else None,
                  "title": p.get("title", self.metadata["playlist"]["title"]),
                  "status": {"privacy": p.get("status", "not-created"), "order": p.get("orderStatus", "not-verified")}},
                  "videos": []}
        for key in IDS:
            e = self.state.data["videos"][key]
            result["videos"].append({"id": e.get("id"),
                "url": "https://www.youtube.com/watch?v=" + e["id"] if e.get("id") else None,
                "title": e.get("remoteTitle", self.videos[key]["title"]),
                "status": e.get("verification", {"upload": e.get("uploadStatus", "not-uploaded")}),
                "captionlangs": e.get("captionVerification", {l: e.get("captions", {}).get(l, {}).get("status", "pending" if e.get("captions", {}).get(l, {}).get("pending") else "missing") for l in LANGUAGES})})
        return result


def write_report(path, private_directory, report):
    target = Path(path).absolute()
    private = Path(private_directory).resolve()
    if target.is_symlink() or target.resolve() == private or private in target.resolve().parents:
        raise SafeError("ReportMustBeOutsidePrivateState")
    target.parent.mkdir(parents=True, exist_ok=True)
    # Report is constructed from an explicit allowlist, never a redacted state copy.
    target.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    for name in ("client", "token", "metadata", "manifest", "state", "expected-channel", "report"):
        parser.add_argument("--" + name, required=True)
    parser.add_argument("--phase", choices=("playlist", "videos", "captions", "verify"), required=True)
    parser.add_argument("--require-qr", action="store_true", help="Require the verified 290–300 second official LINE end card in the manifest")
    args = parser.parse_args(argv)
    publisher = None
    try:
        if not re.fullmatch(r"UC[A-Za-z0-9_-]{22}", args.expected_channel):
            raise SafeError("InvalidExpectedChannel")
        metadata, manifest = load_json(args.metadata), load_json(args.manifest)
        with state_lock(args.state):
            state = PrivateState(args.state, args.expected_channel, metadata, manifest)
            # Validate local assets and QR claims before credentials are read.
            # Bind private progress to the portable JSON bytes/values; resolve
            # only the execution copy so relocating a job keeps its identity.
            resolved_metadata = resolve_metadata_paths(metadata, args.metadata)
            publisher = Publisher(None, state, resolved_metadata, manifest, args.expected_channel, args.require_qr)
            if args.phase == "videos":
                publisher.preflight_videos()
            report_target = Path(args.report).absolute().resolve()
            private = Path(args.state).absolute().resolve()
            if report_target == private or private in report_target.parents:
                raise SafeError("ReportMustBeOutsidePrivateState")
            transport = StdlibTransport()
            provider = OAuth(transport, args.client, args.token)
            publisher.api = GoogleAPI(transport, provider)
            publisher.run(args.phase)
            write_report(args.report, args.state, publisher.public_report(args.phase + "-complete"))
            print(json.dumps({"status": "complete", "phase": args.phase}, ensure_ascii=False))
        return 0
    except SafeError as error:
        if publisher:
            with contextlib.suppress(Exception):
                write_report(args.report, args.state, publisher.public_report("quota-stopped" if error.reason in QUOTA_REASONS else "stopped"))
        print(json.dumps(error.public()), file=sys.stderr)
        return 3 if error.reason in QUOTA_REASONS else 2
    except KeyboardInterrupt:
        print(json.dumps({"status": 0, "reason": "InterruptedResumeFromPrivateState"}), file=sys.stderr)
        return 130
    except Exception:
        # Never print traceback, local credential paths, request headers or URIs.
        print(json.dumps({"status": 0, "reason": "LocalExecutionError"}), file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
