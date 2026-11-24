#!/usr/bin/env python3
"""Publish one verified short/long process film using an isolated safe core.

No action runs on import. --offline-preflight never reads credentials, creates
private state or accesses a network. Each explicit publication phase checks the
fixed channel. The six-overview metadata and private state are never modified.
Alternate audio remains a Studio capability; this uploads the MP4 and five VTTs.
"""
from __future__ import annotations
import argparse
import contextlib
import copy
import importlib.util
import json
import os
from pathlib import Path
import re
import secrets
import sys

EXPECTED_CHANNEL = 'UCXcPnnnM7btkcHwSFkVckzQ'
PLAYLISTS = {
    'short': {'title': '馬蓋先創意工程學院｜先進半導體封裝：5分鐘俯瞰導覽',
              'description': '先進封裝五分鐘俯瞰導覽與獨立工序短片。Five-minute advanced-packaging introductions and process lessons.'},
    'long': {'title': '馬蓋先創意工程學院｜先進半導體封裝：15分鐘深入工序',
             'description': '每道工程活動十五分鐘的深入課程，包含假設案例、技術取捨與證據檢查。Fifteen-minute lessons on engineering activities, worked assumptions, tradeoffs and verification evidence.'}}
STATE_FILE = 'youtube-process-state-v34.json'


def load_core(film_id):
    # A fresh module gives inherited methods their own IDS globals. This does
    # not patch the six-film module, its files, or another process job instance.
    spec = importlib.util.spec_from_file_location('isolated_youtube_' + film_id.replace('-', '_'),
                                                Path(__file__).with_name('publish-packaging-youtube-v33.py'))
    core = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(core)
    core.IDS = (film_id,)
    return core


def film_id_from(metadata):
    videos = metadata.get('videos', [])
    if len(videos) != 1 or not re.fullmatch(r'[A-Z][0-9]{2,3}(?:-long)?', videos[0].get('id', '')):
        raise ValueError('ExactlyOneProcessFilmRequired')
    return videos[0]['id']


def publisher_type(core, film_id):
    class ProcessPublisher(core.Publisher):
        def __init__(self, api, state, metadata, manifest, expected_channel=EXPECTED_CHANNEL):
            if expected_channel != EXPECTED_CHANNEL:
                raise core.SafeError('UnexpectedAuthorizedChannel')
            self.api, self.state, self.manifest = api, state, manifest
            self.expected_channel, self.channel = expected_channel, None
            self.metadata = copy.deepcopy(metadata)
            self.film_id = film_id
            self.duration = 900 if film_id.endswith('-long') else 300
            self.chapter_count = self.duration // 30
            if film_id_from(metadata) != film_id:
                raise core.SafeError('ProcessIdMismatch')
            for field in ('expectedChannel', 'expectedChannelId'):
                if metadata.get(field, EXPECTED_CHANNEL) != EXPECTED_CHANNEL:
                    raise core.SafeError('MetadataChannelMismatch')
            expected = PLAYLISTS['long' if self.duration == 900 else 'short']
            declared = metadata.get('playlist', {})
            if declared.get('title', expected['title']) != expected['title']:
                raise core.SafeError('PlaylistTitleMismatch')
            self.metadata['playlist'] = {**expected, 'requireExisting': False,
                                         'creationPolicy': 'reuse-exact-title-or-create-if-absent'}
            video = self.metadata['videos'][0]
            self.validate_text(video)
            localizations = video.get('localizations', {})
            if set(localizations) != set(core.LANGUAGES):
                raise core.SafeError('FiveLocalizedMetadataLanguagesRequired')
            for value in localizations.values():
                self.validate_text(value)
            if video.get('defaultLanguage', 'zh-TW') != 'zh-TW' or video.get('defaultAudioLanguage', 'zh-TW') != 'zh-TW':
                raise core.SafeError('TraditionalChineseDefaultRequired')
            if video.get('durationSeconds', self.duration) != self.duration:
                raise core.SafeError('UnexpectedVideoDuration')
            video['durationSeconds'] = self.duration
            video['playlistPosition'] = None  # Shared series: do not move other films.
            for field in ('subtitleTracks', 'audioTracks'):
                tracks = video.get(field, [])
                if len(tracks) != 5 or {t.get('language') for t in tracks} != set(core.LANGUAGES):
                    raise core.SafeError('FiveMediaLanguagesRequired')
            for track in video['subtitleTracks']:
                track['label'] = track.get('label', track.get('name', track['language']))
            if (manifest.get('status') != 'PASS' or manifest.get('id', manifest.get('processId')) != film_id
                    or manifest.get('durationSeconds') != self.duration
                    or manifest.get('frames') != self.duration * 24
                    or (manifest.get('width'), manifest.get('height')) != (1280, 720)
                    or manifest.get('fps') != '24/1'):
                raise core.SafeError('InvalidProcessManifest')
            for field in ('subtitleLanguages', 'audioLanguages'):
                if len(manifest.get(field, [])) != 5 or set(manifest[field]) != set(core.LANGUAGES):
                    raise core.SafeError('InvalidManifestLanguages')
            chapters = manifest.get('chapters', [])
            if (len(chapters) != self.chapter_count or
                    any((c.get('startSeconds'), c.get('endSeconds')) != (i * 30, (i + 1) * 30)
                        or not c.get('title') for i, c in enumerate(chapters))):
                raise core.SafeError('InvalidManifestChapters')
            card = manifest.get('endCard', {})
            if (card.get('url') != core.LINE_URL or card.get('startSeconds') != self.duration - 10
                    or card.get('endSeconds') != self.duration or card.get('verified') is not True):
                raise core.SafeError('VerifiedLineEndCardRequired')
            verification = manifest.get('verification', {})
            if (verification.get('status') != 'PASS' or verification.get('videoPacketsByteIdentical') is not True
                    or verification.get('aacPacketsByteIdentical') is not True
                    or verification.get('subtitleTextTimingAndLineBreaks') != 'PASS'):
                raise core.SafeError('ProcessMediaVerificationRequired')
            self.videos = {film_id: video}
            self.assets = {film_id: manifest}

        @staticmethod
        def validate_text(value):
            title, description = value.get('title'), value.get('description')
            if (not isinstance(title, str) or not 1 <= len(title) <= 100
                    or not isinstance(description, str) or len(description.encode('utf-8')) > 5000
                    or any(c in title + description for c in '<>')):
                raise core.SafeError('InvalidLocalizedMetadata')

        def preflight_videos(self):
            video, asset = self.videos[film_id], self.assets[film_id]
            self.check_file(video['videoFile'], asset.get('sha256'), asset.get('bytes'), 'ManifestMismatch')
            if video.get('videoSha256') != asset['sha256'] or video.get('videoBytes') != asset['bytes']:
                raise core.SafeError('MetadataManifestMismatch')
            for track in video['audioTracks']:
                self.check_file(track['file'], track.get('sha256'), track.get('bytes'), 'AudioHashMismatch')
            spec = importlib.util.spec_from_file_location('process_vtt_validation', Path(__file__).with_name('export-bilingual-packaging-subtitles-v33.py'))
            subtitles = importlib.util.module_from_spec(spec)
            sys.modules[spec.name] = subtitles
            spec.loader.exec_module(subtitles)
            for track in video['subtitleTracks']:
                self.check_file(track['file'], track.get('sha256'), None, 'CaptionHashMismatch')
                self.check_file(track['srtFile'], track.get('srtSha256'), None, 'CaptionHashMismatch')
                try:
                    subtitles.validate_coverage(subtitles.parse_vtt(Path(track['file']).read_text('utf-8')), self.duration * 1000)
                except (ValueError, UnicodeError, OSError):
                    raise core.SafeError('CaptionTimingMismatch') from None

        @staticmethod
        def check_file(value, expected_sha, expected_size, reason):
            path = Path(value)
            if (not isinstance(expected_sha, str) or not re.fullmatch(r'[a-f0-9]{64}', expected_sha)
                    or path.is_symlink() or not path.is_file()
                    or (expected_size is not None and path.stat().st_size != expected_size)
                    or core.digest_file(path) != expected_sha):
                raise core.SafeError(reason)

        def marker(self, key):
            return 'macgyver-process-v34-' + self.state.data['job'] + '-' + key

        def ensure_playlist_item(self, key):
            self.require_channel()
            entry = self.state.data['videos'][key]
            pid, vid = self.check_playlist(), entry['id']
            items = self.api.all_items('playlistItems', {'part': 'snippet,contentDetails', 'playlistId': pid})
            matches = [p for p in items if p.get('contentDetails', {}).get('videoId') == vid]
            if len(matches) > 1:
                raise core.SafeError('DuplicatePlaylistItems')
            if matches:
                entry['playlistItemId'] = matches[0]['id']
                entry['playlistPosition'] = matches[0].get('snippet', {}).get('position')
                entry.pop('playlistPending', None)
                self.state.save()
                return
            if entry.get('playlistPending'):
                raise core.SafeError('PlaylistInsertOutcomeUnknown')
            entry['playlistPending'] = True
            self.state.save()
            # position is optional. Leave the playlist's own ordering policy in
            # control; never PUT/reorder previously published films from other jobs.
            snippet = {'playlistId': pid, 'resourceId': {'kind': 'youtube#video', 'videoId': vid}}
            try:
                item = self.api.call('POST', 'playlistItems', {'part': 'snippet'}, {'snippet': snippet})
            except core.SafeError as error:
                if not core.uncertain(error):
                    entry.pop('playlistPending', None)
                    self.state.save()
                raise
            if not item.get('id'):
                raise core.SafeError('MissingPlaylistItemId')
            entry['playlistItemId'] = item['id']
            entry['playlistPosition'] = item.get('snippet', {}).get('position')
            entry.pop('playlistPending', None)
            self.state.save()

        def verify(self):
            self.require_channel()
            pid = self.check_playlist()
            entry = self.state.data['videos'][film_id]
            if not entry.get('id'):
                raise core.SafeError('VideoNotUploaded')
            item = self.get_video(entry['id'])
            playlist = self.api.all_items('playlistItems', {'part': 'snippet,contentDetails', 'playlistId': pid})
            matches = [p for p in playlist if p.get('contentDetails', {}).get('videoId') == entry['id']]
            membership = 'PASS' if len(matches) == 1 else 'DUPLICATE' if matches else 'MISSING'
            self.state.data['playlist']['orderStatus'] = 'OWN_MEMBERSHIP_' + membership
            status = item.get('status', {})
            entry['remoteTitle'] = item.get('snippet', {}).get('title', '')
            entry['verification'] = {'privacy': status.get('privacyStatus', 'unknown'),
                'upload': status.get('uploadStatus', 'unknown'),
                'processing': item.get('processingDetails', {}).get('processingStatus', 'unknown'),
                'madeForKids': status.get('madeForKids', status.get('selfDeclaredMadeForKids')),
                'containsSyntheticMedia': status.get('containsSyntheticMedia'),
                'titleMatches': entry['remoteTitle'] == self.videos[film_id]['title'],
                'playlistMembership': membership,
                'playlistPosition': matches[0].get('snippet', {}).get('position') if len(matches) == 1 else None}
            entry['captionVerification'] = {language: 'missing' for language in core.LANGUAGES}
            observed = set()
            for caption in self.caption_items(entry['id']):
                snippet = caption.get('snippet', {})
                language = core.normalize_language(snippet.get('language'))
                if language not in core.LANGUAGES or snippet.get('trackKind') == 'ASR':
                    continue
                if language in observed:
                    entry['captionVerification'][language] = 'duplicate'
                else:
                    entry.setdefault('captions', {})[language] = {'id': caption['id'], 'status': snippet.get('status', 'unknown')}
                    entry['captionVerification'][language] = snippet.get('status', 'unknown')
                observed.add(language)
            self.state.save()

    return ProcessPublisher


def state_type(core, film_id):
    class ProcessState(core.PrivateState):
        def __init__(self, directory, expected_channel, metadata, manifest):
            guard_state(core, directory)
            self.directory = core.secure_directory(directory)
            self.path = self.directory / STATE_FILE
            if self.path.is_symlink():
                raise core.SafeError('SymlinkStateFile')
            binding = {'jobType': 'single-process-v34', 'filmId': film_id, 'channel': expected_channel,
                       'metadataSha256': core.digest_json(metadata), 'manifestSha256': core.digest_json(manifest)}
            if self.path.exists():
                self.data = core.load_json(self.path)
                if self.data.get('version') != 2 or self.data.get('binding') != binding:
                    raise core.SafeError('StateBindingMismatch')
                os.chmod(self.path, 0o600)
            else:
                self.data = {'version': 2, 'binding': binding, 'job': secrets.token_hex(12),
                             'playlist': {}, 'videos': {film_id: {}}}
                self.save()
    return ProcessState


def guard_state(core, directory):
    if (Path(directory) / 'youtube-upload-state-v33.json').exists():
        raise core.SafeError('OverviewStateDirectoryForbidden')


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--metadata', type=Path, required=True)
    parser.add_argument('--manifest', type=Path)
    parser.add_argument('--film')
    parser.add_argument('--client', type=Path)
    parser.add_argument('--token', type=Path)
    parser.add_argument('--state', type=Path)
    parser.add_argument('--report', type=Path)
    parser.add_argument('--expected-channel', default=EXPECTED_CHANNEL)
    parser.add_argument('--phase', choices=('all', 'playlist', 'videos', 'captions', 'verify'), default='all')
    parser.add_argument('--offline-preflight', action='store_true')
    args = parser.parse_args(argv)
    core, publisher, state_directory = None, None, None
    try:
        metadata = json.loads(args.metadata.read_text('utf-8'))
        film_id = film_id_from(metadata)
        core = load_core(film_id)
        if args.film and film_id != args.film:
            raise core.SafeError('ProcessIdMismatch')
        if args.expected_channel != EXPECTED_CHANNEL:
            raise core.SafeError('UnexpectedAuthorizedChannel')
        resolved = core.resolve_metadata_paths(metadata, args.metadata)
        manifest_path = args.manifest or Path(resolved['mediaManifest'])
        if core.digest_file(manifest_path) != metadata.get('mediaManifestSha256'):
            raise core.SafeError('ManifestBindingMismatch')
        manifest = core.load_json(manifest_path)
        Publisher, State = publisher_type(core, film_id), state_type(core, film_id)
        preflight = Publisher(None, None, resolved, manifest)
        preflight.preflight_videos()
        if args.offline_preflight:
            print(json.dumps({'status': 'PASS', 'mode': 'offline-preflight', 'filmId': film_id,
                              'durationSeconds': preflight.duration, 'networkUsed': False,
                              'oauthAccessed': False, 'privateStateModified': False}))
            return 0
        if not args.client or not args.token or not args.state or not args.report:
            raise core.SafeError('ExplicitClientTokenStateAndReportRequired')
        state_directory = args.state
        guard_state(core, state_directory)
        report = args.report.absolute().resolve()
        private = state_directory.absolute().resolve()
        if args.report.is_symlink() or report == private or private in report.parents:
            raise core.SafeError('ReportMustBeOutsidePrivateState')
        with core.state_lock(state_directory):
            state = State(state_directory, EXPECTED_CHANNEL, metadata, manifest)
            publisher = Publisher(None, state, resolved, manifest)
            transport = core.StdlibTransport()
            token = core.OAuth(transport, args.client, args.token)
            publisher.api = core.GoogleAPI(transport, token)
            phases = ('playlist', 'videos', 'captions', 'verify') if args.phase == 'all' else (args.phase,)
            for phase in phases:
                publisher.run(phase)
                core.write_report(args.report, state_directory, publisher.public_report(phase + '-complete'))
                print(json.dumps({'status': 'complete', 'filmId': film_id, 'phase': phase}), flush=True)
        return 0
    except KeyboardInterrupt:
        print(json.dumps({'status': 0, 'reason': 'InterruptedResumeFromPrivateState'}), file=sys.stderr)
        return 130
    except Exception as error:
        safe = core is not None and isinstance(error, core.SafeError)
        quota = safe and error.reason in core.QUOTA_REASONS
        if publisher and state_directory and args.report:
            with contextlib.suppress(Exception):
                core.write_report(args.report, state_directory, publisher.public_report('quota-stopped' if quota else 'stopped'))
        value = error.public() if safe else {'status': 0, 'reason': 'LocalProcessJobValidationError'}
        print(json.dumps(value), file=sys.stderr)
        return 3 if quota else 2


if __name__ == '__main__':
    raise SystemExit(main())
