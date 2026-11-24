#!/usr/bin/env python3
"""Offline transport tests: no OAuth files, sockets or real API requests."""
import copy
import hashlib
import importlib.util
import io
import json
from pathlib import Path
import re
import stat
import tempfile
import unittest
from urllib.parse import parse_qs, urlsplit
from urllib.error import HTTPError, URLError
from urllib.request import Request

spec = importlib.util.spec_from_file_location("publisher", Path(__file__).with_name("publish-packaging-youtube-v33.py"))
m = importlib.util.module_from_spec(spec)
spec.loader.exec_module(m)
CHANNEL = "UC" + "A" * 22
PLAYLIST = "PL_offline_test_playlist"


class FakeToken:
    def access(self, force=False):
        return "offline-token-never-real"


class FakeTransport:
    def __init__(self):
        self.channel = CHANNEL
        self.playlist = None
        self.videos = {}
        self.items = []
        self.captions = {}
        self.sessions = {}
        self.requests = []
        self.mutations = []
        self.video_inits = 0
        self.caption_uploads = 0
        self.caption_order = []
        self.lose_completed_reply_once = False
        self.lose_playlist_reply_once = False
        self.caption_quota_after = None

    @staticmethod
    def reply(value, code=200, headers=None):
        return m.Reply(code, headers, json.dumps(value).encode())

    def request(self, method, url, headers=None, body=None):
        self.requests.append((method, url))
        u = urlsplit(url)
        q = parse_qs(u.query)
        route = u.path.rsplit("/", 1)[-1]
        if method != "GET" and not (method == "PUT" and (headers or {}).get("Content-Range", "").startswith("bytes */")):
            self.mutations.append((method, route))
        if route == "channels" and method == "GET":
            return self.reply({"items": [{"id": self.channel, "snippet": {"title": "Offline channel"},
                "contentDetails": {"relatedPlaylists": {"uploads": "UU_offline"}}}]})
        if route == "playlists":
            if method == "GET":
                return self.reply({"items": [self.playlist] if self.playlist else []})
            value = json.loads(body)
            self.playlist = {"id": PLAYLIST, "snippet": dict(value["snippet"], channelId=self.channel),
                             "status": value["status"]}
            if self.lose_playlist_reply_once:
                self.lose_playlist_reply_once = False
                raise m.SafeError('NetworkError')
            return self.reply(self.playlist)
        if route == "videos" and u.path.startswith("/upload/"):
            if method == "POST":
                self.video_inits += 1
                session = m.UPLOAD + "videos?uploadType=resumable&upload_id=offline-secret-" + str(self.video_inits)
                self.sessions[session] = {"metadata": json.loads(body), "total": int(headers["X-Upload-Content-Length"]), "offset": 0}
                return self.reply({}, headers={"Location": session})
            session = self.sessions[url]
            content_range = headers["Content-Range"]
            if content_range.startswith("bytes */"):
                if session.get("id"):
                    return self.reply(self.videos[session["id"]])
                return self.reply({}, 308, {"Range": "bytes=0-" + str(session["offset"]-1)} if session["offset"] else {})
            start, end, total = map(int, re.fullmatch(r"bytes (\d+)-(\d+)/(\d+)", content_range).groups())
            assert start == session["offset"] and len(body) == end-start+1 and total == session["total"]
            session["offset"] = end + 1
            if session["offset"] == total:
                vid = "vid" + str(len(self.videos) + 1).zfill(8)
                item = {"id": vid, "snippet": dict(session["metadata"]["snippet"], channelId=self.channel),
                        "status": dict(session["metadata"]["status"], uploadStatus="processed"),
                        "processingDetails": {"processingStatus": "succeeded"}}
                self.videos[vid] = item
                session["id"] = vid
                if self.lose_completed_reply_once:
                    self.lose_completed_reply_once = False
                    raise m.SafeError("NetworkError")
                return self.reply(item)
            return self.reply({}, 308, {"Range": "bytes=0-" + str(end)})
        if route == "videos" and method == "GET":
            return self.reply({"items": [self.videos[x] for x in q["id"][0].split(",") if x in self.videos]})
        if route == "playlistItems":
            if method == "GET":
                if q["playlistId"][0] == "UU_offline":
                    return self.reply({"items": [{"contentDetails": {"videoId": v}} for v in self.videos]})
                return self.reply({"items": copy.deepcopy(self.items)})
            value = json.loads(body)
            snippet = value["snippet"]
            vid = snippet["resourceId"]["videoId"]
            if method == "PUT":
                self.items = [p for p in self.items if p["id"] != value["id"]]
            item = {"id": value.get("id", "PI_" + vid), "snippet": snippet,
                    "contentDetails": {"videoId": vid}}
            self.items.insert(snippet["position"], item)
            for pos, p in enumerate(self.items):
                p["snippet"]["position"] = pos
            return self.reply(item)
        if route == "captions":
            if method == "GET":
                return self.reply({"items": copy.deepcopy(self.captions.get(q["videoId"][0], []))})
            if self.caption_quota_after is not None and self.caption_uploads >= self.caption_quota_after:
                return self.reply({"error": {"errors": [{"reason": "quotaExceeded"}]}}, 403)
            data = json.loads(body.split(b"\r\n\r\n", 1)[1].split(b"\r\n--", 1)[0])
            snippet = dict(data["snippet"], status="serving", trackKind="standard")
            self.caption_uploads += 1
            self.caption_order.append((snippet["videoId"], snippet["language"]))
            item = {"id": "caption-" + str(self.caption_uploads), "snippet": snippet}
            self.captions.setdefault(snippet["videoId"], []).append(item)
            return self.reply(item)
        raise AssertionError("Unexpected fake route: " + method + " " + route)


class PublisherTests(unittest.TestCase):
    def setUp(self):
        tmp_parent = "/private/tmp" if Path("/private/tmp").is_dir() else None
        self.tmp = tempfile.TemporaryDirectory(dir=tmp_parent)
        self.root = Path(self.tmp.name)
        self.metadata = {"playlist": {"title": "Reviewed offline playlist", "description": "Review copy"}, "videos": []}
        self.manifest = {"status": "PASS", "endCard": {"url": m.LINE_URL, "startSeconds": 290, "endSeconds": 300, "verified": True}, "videos": []}
        for i, key in enumerate(m.IDS):
            content = (key + "-offline-media-fixture").encode()
            video = self.root / (key + ".mp4")
            video.write_bytes(content)
            tracks = []
            for lang in m.LANGUAGES:
                f = self.root / (key + "." + lang + ".vtt")
                data = ("WEBVTT\n\n00:00:00.000 --> 00:00:30.000\n" + lang + "\n").encode()
                f.write_bytes(data)
                tracks.append({"file": str(f), "language": lang, "label": lang, "sha256": hashlib.sha256(data).hexdigest()})
            self.metadata["videos"].append({"id": key, "title": "Reviewed " + key, "description": "Reviewed description",
                "playlistPosition": i, "durationSeconds": 300, "videoFile": str(video), "subtitleTracks": tracks})
            self.manifest["videos"].append({"id": key, "bytes": len(content), "sha256": hashlib.sha256(content).hexdigest(),
                "duration": 300, "chapters": 10, "subtitleLanguages": list(m.LANGUAGES)})
        self.transport = FakeTransport()
        self.api = m.GoogleAPI(self.transport, FakeToken())
        self.state = m.PrivateState(self.root / "private-state", CHANNEL, self.metadata, self.manifest)
        self.publisher = m.Publisher(self.api, self.state, self.metadata, self.manifest, CHANNEL, require_qr=True)

    def tearDown(self):
        self.tmp.cleanup()

    def ready_videos(self):
        self.publisher.run("playlist")
        self.publisher.run("videos")

    def test_completed_upload_response_lost_then_resume_does_not_duplicate(self):
        self.publisher.run("playlist")
        self.transport.lose_completed_reply_once = True
        with self.assertRaisesRegex(m.SafeError, "NetworkError"):
            self.publisher.run("videos")
        self.assertEqual(1, len(self.transport.videos))
        self.assertIn("session", self.state.data["videos"]["interposer"])
        # New process-equivalent state object uses the saved resumable URI.
        restored = m.PrivateState(self.state.directory, CHANNEL, self.metadata, self.manifest)
        publisher = m.Publisher(self.api, restored, self.metadata, self.manifest, CHANNEL)
        publisher.run("videos")
        publisher.run("videos")
        self.assertEqual(6, self.transport.video_inits)
        self.assertEqual(6, len(self.transport.videos))
        self.assertEqual(6, len(self.transport.items))
        self.assertEqual(6, len({p["contentDetails"]["videoId"] for p in self.transport.items}))

    def test_channel_mismatch_all_phases_have_zero_mutations(self):
        self.transport.channel = "UC" + "B" * 22
        for phase in ("playlist", "videos", "captions", "verify"):
            with self.subTest(phase=phase), self.assertRaisesRegex(m.SafeError, "ChannelMismatch"):
                self.publisher.run(phase)
        self.assertEqual([], self.transport.mutations)

    def test_required_existing_playlist_is_reused_and_never_recreated(self):
        metadata = copy.deepcopy(self.metadata)
        metadata['playlist']['requireExisting'] = True
        state = m.PrivateState(self.root / 'existing-playlist-state', CHANNEL, metadata, self.manifest)
        publisher = m.Publisher(self.api, state, metadata, self.manifest, CHANNEL)
        with self.assertRaisesRegex(m.SafeError, 'ExistingPlaylistNotFound'):
            publisher.run('playlist')
        self.assertEqual([], self.transport.mutations)
        self.transport.playlist = {'id': PLAYLIST, 'snippet': {'channelId': CHANNEL, 'title': metadata['playlist']['title']},
                                   'status': {'privacyStatus': 'public'}}
        publisher.run('playlist')
        self.assertEqual(state.data['playlist']['id'], PLAYLIST)
        self.assertEqual([], self.transport.mutations)

    def test_uncertain_playlist_creation_reconciles_without_duplicate(self):
        self.transport.lose_playlist_reply_once = True
        with self.assertRaisesRegex(m.SafeError, 'NetworkError'):
            self.publisher.run('playlist')
        self.assertTrue(self.state.data['playlist']['pending'])
        restored = m.PrivateState(self.state.directory, CHANNEL, self.metadata, self.manifest)
        publisher = m.Publisher(self.api, restored, self.metadata, self.manifest, CHANNEL)
        publisher.run('playlist')
        self.assertEqual(restored.data['playlist']['id'], PLAYLIST)
        self.assertEqual(self.transport.mutations.count(('POST', 'playlists')), 1)

    def test_portable_metadata_paths_resolve_against_json_not_working_directory(self):
        metadata = copy.deepcopy(self.metadata)
        metadata['pathResolutionMode'] = 'metadata-relative'
        folder = self.root / 'docs'
        folder.mkdir()
        for video in metadata['videos']:
            video['videoFile'] = '../' + Path(video['videoFile']).name
            for track in video['subtitleTracks']:
                track['file'] = '../' + Path(track['file']).name
        before = copy.deepcopy(metadata)
        resolved = m.resolve_metadata_paths(metadata, folder / 'job.json')
        self.assertEqual(metadata, before)
        publisher = m.Publisher(self.api, self.state, resolved, self.manifest, CHANNEL)
        publisher.preflight_videos()
        self.assertEqual([], self.transport.requests)

    def test_manifest_mismatch_prevents_all_video_uploads(self):
        self.publisher.run("playlist")
        Path(self.metadata["videos"][-1]["videoFile"]).write_bytes(b"changed after review")
        before = len(self.transport.mutations)
        with self.assertRaisesRegex(m.SafeError, "ManifestMismatch"):
            self.publisher.run("videos")
        self.assertEqual(0, self.transport.video_inits)
        self.assertEqual(before, len(self.transport.mutations))

    def test_description_limit_counts_utf8_bytes_for_non_ascii_text(self):
        metadata = copy.deepcopy(self.metadata)
        metadata["videos"][0]["description"] = "封" * 1666 + "ab"
        self.assertEqual(5000, len(metadata["videos"][0]["description"].encode("utf-8")))
        m.Publisher(self.api, self.state, metadata, self.manifest, CHANNEL)
        metadata["videos"][0]["description"] += "c"
        self.assertLess(len(metadata["videos"][0]["description"]), 5000)
        with self.assertRaisesRegex(m.SafeError, "InvalidVideoMetadata"):
            m.Publisher(self.api, self.state, metadata, self.manifest, CHANNEL)
        self.assertEqual([], self.transport.requests)

    def test_existing_manual_caption_aliases_are_not_uploaded_again(self):
        self.ready_videos()
        for key in m.IDS:
            vid = self.state.data["videos"][key]["id"]
            self.transport.captions[vid] = [{"id": key + "-" + lang,
                "snippet": {"videoId": vid, "language": m.CAPTION_CODES[lang], "status": "serving", "trackKind": "standard"}}
                for lang in m.LANGUAGES]
        self.publisher.run("captions")
        self.publisher.run("captions")
        self.assertEqual(0, self.transport.caption_uploads)
        self.assertTrue(all(len(v["captions"]) == 5 for v in self.state.data["videos"].values()))

    def test_localizations_are_validated_and_included_in_upload_request(self):
        metadata = copy.deepcopy(self.metadata)
        for video in metadata["videos"]:
            video["defaultLanguage"] = "zh-TW"
            video["localizations"] = {language: {"title": language + " 標題", "description": "封" * 1666 + "ab"}
                                      for language in m.LANGUAGES}
        state = m.PrivateState(self.root / "localized-state", CHANNEL, metadata, self.manifest)
        publisher = m.Publisher(self.api, state, metadata, self.manifest, CHANNEL)
        publisher.run("playlist")
        publisher.run("videos")
        for session in self.transport.sessions.values():
            self.assertEqual(set(session["metadata"]["localizations"]), set(m.LANGUAGES))
        starts = [url for method, url in self.transport.requests if method == "POST" and "/upload/youtube/v3/videos?" in url]
        self.assertEqual(len(starts), 6)
        self.assertTrue(all("localizations" in parse_qs(urlsplit(url).query)["part"][0] for url in starts))
        metadata["videos"][0]["localizations"]["ja"]["description"] += "c"
        before = len(self.transport.requests)
        with self.assertRaisesRegex(m.SafeError, "InvalidLocalizedMetadata"):
            m.Publisher(self.api, state, metadata, self.manifest, CHANNEL)
        self.assertEqual(before, len(self.transport.requests))

    def test_quota_stops_then_retry_preserves_language_first_progress(self):
        self.ready_videos()
        self.transport.caption_quota_after = 2
        with self.assertRaisesRegex(m.SafeError, "quotaExceeded"):
            self.publisher.run("captions")
        self.assertEqual(2, self.transport.caption_uploads)
        self.assertNotIn("zh-TW", self.state.data["videos"]["hybrid"]["captions"])
        self.transport.caption_quota_after = None
        self.publisher.run("captions")
        self.assertEqual(30, self.transport.caption_uploads)
        self.assertEqual([m.CAPTION_CODES[l] for l in m.LANGUAGES for _ in m.IDS],
                         [language for _, language in self.transport.caption_order])

    def test_verification_does_not_erase_uncertain_caption_guard(self):
        self.ready_videos()
        self.state.data["videos"]["interposer"]["captions"] = {"zh-TW": {"pending": True}}
        self.state.save()
        self.publisher.run("verify")
        self.assertTrue(self.state.data["videos"]["interposer"]["captions"]["zh-TW"]["pending"])
        with self.assertRaisesRegex(m.SafeError, "CaptionUploadOutcomeUnknown"):
            self.publisher.run("captions")
        self.assertEqual(0, self.transport.caption_uploads)

    def test_private_permissions_and_report_allowlist(self):
        self.publisher.run("playlist")
        self.state.data["videos"]["interposer"]["session"] = m.UPLOAD + "videos?upload_id=private-secret"
        self.state.save()
        self.assertEqual(0o700, stat.S_IMODE(self.state.directory.stat().st_mode))
        self.assertEqual(0o600, stat.S_IMODE(self.state.path.stat().st_mode))
        report = self.publisher.public_report()
        text = json.dumps(report)
        for forbidden in ("upload_id", "private-secret", "session", "refresh_token", "client_secret", "Authorization"):
            self.assertNotIn(forbidden, text)
        self.assertEqual({"id", "url", "title", "status", "captionlangs"}, set(report["videos"][0]))

    def test_non_official_endpoint_is_rejected_before_transport(self):
        with self.assertRaisesRegex(m.SafeError, "NonOfficialEndpoint"):
            self.api.request("PUT", "https://www.googleapis.com.evil.invalid/upload/youtube/v3/videos")
        self.assertEqual([], self.transport.requests)

    def test_stdlib_transport_preserves_resumable_308_with_fake_opener(self):
        observed = []

        class FakeOpener:
            def open(self, request, timeout):
                observed.append((request.get_method(), request.data, timeout))
                raise HTTPError(request.full_url, 308, "Resume Incomplete",
                                {"Range": "bytes=0-1023"}, io.BytesIO(b""))

        transport = m.StdlibTransport(opener=FakeOpener())
        reply = transport.request("PUT", m.UPLOAD + "videos?upload_id=offline-secret",
            {"Content-Range": "bytes */2048", "Content-Length": "0"}, b"")
        self.assertEqual(308, reply.status)
        self.assertEqual("bytes=0-1023", reply.headers["range"])
        self.assertEqual([( "PUT", b"", 180)], observed)

    def test_stdlib_transport_disables_redirect_and_sanitizes_network_error(self):
        handler = m.NoRedirectHandler()
        request = Request(m.API + "channels")
        self.assertIsNone(handler.redirect_request(request, None, 302, "Found", {},
                                                  "https://untrusted.invalid/collect"))
        opener = m.StdlibTransport().opener
        self.assertTrue(any(isinstance(h, m.NoRedirectHandler) for h in opener.handlers))
        self.assertFalse(any(getattr(h, "proxies", {}) for h in opener.handlers))

        class FakeOpener:
            def open(self, request, timeout):
                raise URLError("upload_id=private-secret Authorization=private-token")

        with self.assertRaises(m.SafeError) as caught:
            m.StdlibTransport(opener=FakeOpener()).request("GET", m.API + "channels")
        self.assertEqual({"status": 0, "reason": "NetworkError"}, caught.exception.public())
        self.assertNotIn("private", str(caught.exception))


if __name__ == "__main__":
    unittest.main(verbosity=2)
