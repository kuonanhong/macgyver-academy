#!/usr/bin/env python3
"""V17 public incremental sync using the existing no-force Git transport.

Keep the reviewed V16 transport intact. Extend its public snapshot policy for
all weight formats and explicitly selected private folders before invoking it.
"""
from pathlib import Path
import argparse
import importlib.util
import sys

ROOT = Path(__file__).resolve().parents[2]


def load_sync(excluded=()):
    spec = importlib.util.spec_from_file_location('macgyver_v17_public_transport', ROOT / 'tools/sync-v12/sync_github.py')
    sync = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(sync)
    exporter = sync.export_github
    original_candidate = exporter.candidate
    forbidden = {'.model', '.h5', '.hdf5', '.pb', '.npy', '.npz', '.pkl', '.pickle', '.keras'}
    exporter.BLOCK_SUFFIXES.update(forbidden)
    exporter.ROOT_FILES.add('RELEASE_FILES_V17.json')
    exporter.EXTRA_IGNORE += '\n# V17 additional private model formats\n' + ''.join('*' + suffix + '\n' for suffix in sorted(forbidden))
    private_paths = [Path(path).expanduser().resolve() for path in excluded]
    blocked_names = {'credentials.json', 'tokens.json', 'token.json', 'cookies.txt', 'cookies.json', 'accounts.json', 'users.json', 'owner.json', '.gitconfig', 'id_ecdsa', 'id_dsa'}

    def candidate(relative):
        parts = tuple(part.casefold() for part in relative.parts)
        name = relative.name.casefold()
        if any(part in exporter.BLOCK_DIRS for part in parts):
            return False
        if name in blocked_names or name.startswith(('owner-bootstrap', 'owner_bootstrap')):
            return False
        if parts[:2] == ('portable', 'data'):
            return False
        absolute = ROOT.joinpath(relative).resolve()
        if any(absolute == directory or directory in absolute.parents for directory in private_paths):
            return False
        return original_candidate(relative)

    exporter.candidate = candidate
    return sync


def main():
    parser = argparse.ArgumentParser(add_help=False)
    parser.add_argument('--exclude-private', action='append', default=[])
    args, rest = parser.parse_known_args()
    sync = load_sync(args.exclude_private)
    sys.argv = [sys.argv[0], *rest]
    return sync.main()


if __name__ == '__main__':
    try:
        sys.exit(main())
    except (ValueError, OSError) as error:
        print('停止：' + str(error), file=sys.stderr)
        sys.exit(1)
