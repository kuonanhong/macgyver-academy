#!/usr/bin/env python3
"""Offline GitHub draft/public asset verification regression tests."""
import copy
import importlib.util
from pathlib import Path
import unittest

spec = importlib.util.spec_from_file_location('release_helper', Path(__file__).with_name('publish-packaging-release-v34.py'))
HELPER = importlib.util.module_from_spec(spec)
spec.loader.exec_module(HELPER)
TAG = 'packaging-tours-v33.0.3'
TOKEN = 'untagged-f4d5ebe35c0a8c75f2e1'
PREFIX = f'https://github.com/{HELPER.REPO}/releases'


def fixture():
    assets = [(Path(name + '.mp4'), {'bytes': 100 + index, 'sha256': f'{index:064x}'})
              for index, name in enumerate((*HELPER.IDS, 'C01'))]
    release = {'id': 456304747, 'tag_name': TAG, 'draft': True,
               'html_url': PREFIX + '/tag/' + TOKEN,
               'assets': [{'name': path.name, 'state': 'uploaded', 'size': record['bytes'],
                           'digest': 'sha256:' + record['sha256'],
                           'browser_download_url': f'{PREFIX}/download/{TOKEN}/{path.name}'} for path, record in assets]}
    return release, assets


class ReleaseVerificationTests(unittest.TestCase):
    def test_same_release_draft_token_allowed_for_all_seven_assets(self):
        release, assets = fixture()
        self.assertEqual(len(HELPER.verify_remote(release, assets, TAG)), 7)

    def test_canonical_urls_allowed_before_and_after_publication(self):
        release, assets = fixture()
        for asset in release['assets']:
            asset['browser_download_url'] = asset['browser_download_url'].replace(TOKEN, TAG)
        HELPER.verify_remote(release, assets, TAG)
        release.update(draft=False, html_url=PREFIX + '/tag/' + TAG)
        HELPER.verify_remote(release, assets, TAG)

    def test_published_release_must_not_keep_temporary_urls(self):
        release, assets = fixture()
        release['draft'] = False
        with self.assertRaisesRegex(ValueError, 'URL mismatch'):
            HELPER.verify_remote(release, assets, TAG)

    def test_unknown_draft_token_or_url_components_rejected(self):
        release, assets = fixture()
        original = release['assets'][0]['browser_download_url']
        for changed in (original.replace(TOKEN, 'untagged-0000'), original.replace('github.com', 'example.com'),
                        original + '?download=1', original + '#fragment', original.replace(HELPER.REPO, 'other/repo')):
            modified = copy.deepcopy(release)
            modified['assets'][0]['browser_download_url'] = changed
            with self.subTest(url=changed), self.assertRaisesRegex(ValueError, 'URL mismatch'):
                HELPER.verify_remote(modified, assets, TAG)

    def test_size_digest_and_upload_state_checks_remain_strict(self):
        release, assets = fixture()
        for field, value, reason in [('size', 1, 'size'), ('digest', 'sha256:' + 'f' * 64, 'SHA-256'), ('state', 'new', 'state')]:
            modified = copy.deepcopy(release)
            modified['assets'][0][field] = value
            with self.subTest(field=field), self.assertRaisesRegex(ValueError, reason + ' mismatch'):
                HELPER.verify_remote(modified, assets, TAG)

    def test_duplicate_remote_names_rejected(self):
        release, assets = fixture()
        release['assets'].append(copy.deepcopy(release['assets'][0]))
        with self.assertRaisesRegex(ValueError, 'Duplicate'):
            HELPER.verify_remote(release, assets, TAG)


if __name__ == '__main__':
    unittest.main()
