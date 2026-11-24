#!/usr/bin/env bash
# Use an existing OAuth grant. Credentials and private resumable state stay outside this package.
set -euo pipefail
TASK_ROOT="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd -P)"
cd "$TASK_ROOT"
TASK_PHASE="${1:-}"
case "$TASK_PHASE" in playlist|videos|captions|verify) shift;; *)
  printf '%s\n' 'Usage: bash Upload_Packaging_YouTube_v33.sh playlist|videos|captions|verify --client CLIENT.json --token TOKEN.json --state PRIVATE_DIR --expected-channel CHANNEL_ID --report REPORT.json'
  exit 2;;
esac
exec "${MACGYVER_PYTHON:-python3}" tools/publish-packaging-youtube-v33.py \
  --metadata docs/PACKAGING_YOUTUBE_METADATA_V33.json \
  --manifest public/academy/assets/packaging-tour-v33/videos/manifest.json \
  --require-qr --phase "$TASK_PHASE" "$@"
