#!/usr/bin/env python3
"""Fake-transport process publishing tests: no credentials or network."""
import copy
import hashlib
import importlib.util
import json
from pathlib import Path
import tempfile
import unittest
from urllib.parse import urlsplit


def module(name, file):
    spec = importlib.util.spec_from_file_location(name, Path(__file__).with_name(file))
    value = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(value)
    return value


ADAPTER = module('process_adapter_tests', 'publish-process-youtube-v34.py')
FAKES = module('shared_youtube_fakes', 'test-publish-packaging-youtube-v33.py')


class Transport(FAKES.FakeTransport):
    def __init__(self):
        super().__init__()
        self.channel = ADAPTER.EXPECTED_CHANNEL
        self.lose_insert_once = False
        self.original_insert_bodies = []

    def request(self, method, url, headers=None, body=None):
        insertion = method == 'POST' and urlsplit(url).path.endswith('/playlistItems')
        if insertion:
            value = json.loads(body)
            self.original_insert_bodies.append(copy.deepcopy(value))
            value['snippet'].setdefault('position', len(self.items))
            body = json.dumps(value).encode()
        result = super().request(method, url, headers, body)
        if insertion and self.lose_insert_once:
            self.lose_insert_once = False
            raise FAKES.m.SafeError('NetworkError')
        return result


def fixture(folder, film, core):
    duration = 900 if film.endswith('-long') else 300
    folder.mkdir(parents=True, exist_ok=True)
    movie = folder / (film + '.mp4')
    movie.write_bytes((film + '-fake-video').encode())
    video = {'id': film, 'title': 'Reviewed ' + film, 'description': 'Offline fixture only',
             'defaultLanguage': 'zh-TW', 'defaultAudioLanguage': 'zh-TW', 'durationSeconds': duration,
             'videoFile': str(movie), 'videoBytes': movie.stat().st_size, 'videoSha256': core.digest_file(movie),
             'localizations': {lang: {'title': 'Reviewed ' + lang, 'description': 'Offline fixture'} for lang in core.LANGUAGES},
             'audioTracks': [], 'subtitleTracks': []}
    for language in core.LANGUAGES:
        audio = folder / (film + '.' + language + '.m4a')
        audio.write_bytes(('fake-audio-' + language).encode())
        vtt, srt = folder / (film + '.' + language + '.vtt'), folder / (film + '.' + language + '.srt')
        end = f'00:{duration // 60:02}:00.000'
        vtt.write_text('WEBVTT\n\n00:00:00.000 --> ' + end + '\n' + language + '\n', 'utf-8')
        srt.write_text('1\n00:00:00,000 --> ' + end.replace('.', ',') + '\n' + language + '\n', 'utf-8')
        video['audioTracks'].append({'language': language, 'file': str(audio), 'bytes': audio.stat().st_size, 'sha256': core.digest_file(audio)})
        video['subtitleTracks'].append({'language': language, 'file': str(vtt), 'sha256': core.digest_file(vtt),
                                         'srtFile': str(srt), 'srtSha256': core.digest_file(srt)})
    metadata = {'schemaVersion': 2, 'expectedChannel': ADAPTER.EXPECTED_CHANNEL, 'videos': [video]}
    manifest = {'status': 'PASS', 'id': film, 'durationSeconds': duration, 'frames': duration * 24,
                'fps': '24/1', 'width': 1280, 'height': 720, 'bytes': video['videoBytes'], 'sha256': video['videoSha256'],
                'audioLanguages': list(core.LANGUAGES), 'subtitleLanguages': list(core.LANGUAGES),
                'chapters': [{'startSeconds': i * 30, 'endSeconds': (i + 1) * 30, 'title': f'Chapter {i+1}'} for i in range(duration // 30)],
                'endCard': {'url': core.LINE_URL, 'verified': True, 'startSeconds': duration - 10, 'endSeconds': duration},
                'verification': {'status': 'PASS', 'videoPacketsByteIdentical': True,
                                 'aacPacketsByteIdentical': True, 'subtitleTextTimingAndLineBreaks': 'PASS'}}
    return metadata, manifest


class ProcessPublisherTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory(dir='/private/tmp' if Path('/private/tmp').is_dir() else None)
        self.root = Path(self.tmp.name)
        self.core = ADAPTER.load_core('C01')
        FAKES.m = self.core
        self.metadata, self.manifest = fixture(self.root / 'assets', 'C01', self.core)
        self.transport = Transport()
        self.api = self.core.GoogleAPI(self.transport, FAKES.FakeToken())
        self.State = ADAPTER.state_type(self.core, 'C01')
        self.Publisher = ADAPTER.publisher_type(self.core, 'C01')
        self.state = self.State(self.root / 'private', ADAPTER.EXPECTED_CHANNEL, self.metadata, self.manifest)
        self.publisher = self.Publisher(self.api, self.state, self.metadata, self.manifest)

    def tearDown(self):
        self.tmp.cleanup()

    def ready(self):
        self.publisher.run('playlist')
        self.publisher.run('videos')

    def test_resume_completed_movie_and_captions_without_duplicates_or_reordering(self):
        self.publisher.run('playlist')
        previous = {'id': 'PI_previous', 'snippet': {'position': 0}, 'contentDetails': {'videoId': 'prior000001'}}
        self.transport.items.append(copy.deepcopy(previous))
        self.publisher.run('videos')
        self.publisher.run('captions')
        self.publisher.run('videos')
        self.publisher.run('captions')
        self.publisher.run('verify')
        self.assertEqual(self.transport.video_inits, 1)
        self.assertEqual(self.transport.caption_uploads, 5)
        self.assertEqual(self.transport.items[0], previous)
        self.assertEqual(len(self.transport.items), 2)
        self.assertNotIn(('PUT', 'playlistItems'), self.transport.mutations)
        self.assertNotIn('position', self.transport.original_insert_bodies[0]['snippet'])
        self.assertEqual(self.state.data['playlist']['orderStatus'], 'OWN_MEMBERSHIP_PASS')

    def test_lost_upload_completion_resumes_existing_video(self):
        self.publisher.run('playlist')
        self.transport.lose_completed_reply_once = True
        with self.assertRaisesRegex(self.core.SafeError, 'NetworkError'):
            self.publisher.run('videos')
        state = self.State(self.root / 'private', ADAPTER.EXPECTED_CHANNEL, self.metadata, self.manifest)
        self.Publisher(self.api, state, self.metadata, self.manifest).run('videos')
        self.assertEqual(self.transport.video_inits, 1)
        self.assertEqual(len(self.transport.items), 1)

    def test_lost_playlist_insertion_reconciles_without_duplicate(self):
        self.publisher.run('playlist')
        self.transport.lose_insert_once = True
        with self.assertRaisesRegex(self.core.SafeError, 'NetworkError'):
            self.publisher.run('videos')
        self.assertTrue(self.state.data['videos']['C01']['playlistPending'])
        self.publisher.run('videos')
        self.assertEqual(len(self.transport.items), 1)
        self.assertNotIn('playlistPending', self.state.data['videos']['C01'])

    def test_channel_mismatch_all_phases_have_zero_mutations(self):
        self.transport.channel = 'UC' + 'X' * 22
        for phase in ('playlist', 'videos', 'captions', 'verify'):
            with self.subTest(phase=phase), self.assertRaisesRegex(self.core.SafeError, 'ChannelMismatch'):
                self.publisher.run(phase)
        self.assertEqual(self.transport.mutations, [])

    def test_changed_movie_prevents_upload(self):
        self.publisher.run('playlist')
        self.transport.mutations.clear()
        Path(self.metadata['videos'][0]['videoFile']).write_bytes(b'changed')
        with self.assertRaisesRegex(self.core.SafeError, 'ManifestMismatch'):
            self.publisher.run('videos')
        self.assertEqual(self.transport.mutations, [])
        self.assertEqual(self.transport.video_inits, 0)

    def test_caption_quota_stops_and_resume_skips_completed_tracks(self):
        self.ready()
        self.transport.caption_quota_after = 2
        with self.assertRaisesRegex(self.core.SafeError, 'quotaExceeded'):
            self.publisher.run('captions')
        self.assertEqual(self.transport.caption_uploads, 2)
        self.transport.caption_quota_after = None
        self.publisher.run('captions')
        self.assertEqual(self.transport.caption_uploads, 5)
        self.assertEqual(len(set(self.transport.caption_order)), 5)

    def test_900_second_process_isolated_from_short_and_overview_core(self):
        other = ADAPTER.load_core('C01-long')
        meta, manifest = fixture(self.root / 'long-assets', 'C01-long', other)
        publisher = ADAPTER.publisher_type(other, 'C01-long')(None, None, meta, manifest)
        publisher.preflight_videos()
        self.assertEqual(publisher.duration, 900)
        self.assertEqual(publisher.chapter_count, 30)
        self.assertEqual(self.core.IDS, ('C01',))
        self.assertEqual(other.IDS, ('C01-long',))
        untouched = module('untouched_six_core', 'publish-packaging-youtube-v33.py')
        self.assertEqual(len(untouched.IDS), 6)
        manifest['endCard']['startSeconds'] = 290
        with self.assertRaisesRegex(other.SafeError, 'VerifiedLineEndCardRequired'):
            ADAPTER.publisher_type(other, 'C01-long')(None, None, meta, manifest)

    def test_old_overview_state_is_never_modified(self):
        folder = self.root / 'old-state'
        folder.mkdir()
        file = folder / 'youtube-upload-state-v33.json'
        file.write_bytes(b'old-private-state-unchanged')
        before = list(folder.iterdir())
        with self.assertRaisesRegex(self.core.SafeError, 'OverviewStateDirectoryForbidden'):
            self.State(folder, ADAPTER.EXPECTED_CHANNEL, self.metadata, self.manifest)
        self.assertEqual(file.read_bytes(), b'old-private-state-unchanged')
        self.assertEqual(list(folder.iterdir()), before)

    def test_localized_utf8_limits_and_private_report_allowlist(self):
        metadata = copy.deepcopy(self.metadata)
        metadata['videos'][0]['localizations']['ja']['description'] = '界' * 1667
        with self.assertRaisesRegex(self.core.SafeError, 'InvalidLocalizedMetadata'):
            self.Publisher(None, self.state, metadata, self.manifest)
        self.state.data['videos']['C01']['session'] = 'https://www.googleapis.com/upload/youtube/v3/videos?upload_id=private'
        self.state.data['videos']['C01']['captions'] = {'ja': {'pending': True}}
        text = json.dumps(self.publisher.public_report())
        self.assertNotIn('upload_id', text)
        self.assertNotIn('session', text)
        self.assertEqual(self.state.path.stat().st_mode & 0o777, 0o600)
        self.assertEqual(self.state.directory.stat().st_mode & 0o777, 0o700)


if __name__ == '__main__':
    unittest.main()
