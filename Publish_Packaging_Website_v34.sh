#!/usr/bin/env bash
set -euo pipefail
PROJECT_DIR="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
SYNC_STATE="${MACGYVER_GITHUB_STATE:-$PROJECT_DIR/../MacGyver_v34_SSH_Upload_State}"
RELEASE_TAG='packaging-tours-v33.0.3'
CHECK_ONLY=0
while (($#)); do
  case "$1" in
    --state|--tag)
      (($# >= 2)) || { echo "缺少參數值 / Missing argument" >&2; exit 2; }
      if [[ "$1" == --state ]]; then SYNC_STATE="$2"; else RELEASE_TAG="$2"; fi
      shift 2 ;;
    --check-only) CHECK_ONLY=1; shift ;;
    -h|--help)
      echo 'Usage: bash Publish_Packaging_Website_v34.sh [--state SYNC_DIR] [--tag packaging-tours-v33.0.3] [--check-only]'
      echo 'Uploads the reviewed public academy and verified films to kuonanhong/macgyver-academy, then deploys Pages.'
      echo 'Requires Python 3, Git, gh authentication and existing GitHub SSH access. No YouTube upload or private model upload.'
      exit 0 ;;
    *) echo "未知參數 / Unknown argument: $1" >&2; exit 2 ;;
  esac
done
cd -- "$PROJECT_DIR"
python3 tools/publish-packaging-release-v34.py --tag "$RELEASE_TAG"
if ((CHECK_ONLY)); then
  echo '本地影片驗證完成，沒有上傳 / Local films verified; nothing uploaded.'
  exit 0
fi
if [[ -f tools/build-offline.mjs ]]; then
  node tools/build-offline.mjs
  python3 tools/check-offline.py
fi
bash Upload_MacGyver_v21_SSH.sh --state "$SYNC_STATE"
python3 tools/publish-packaging-release-v34.py --tag "$RELEASE_TAG" --publish
if [[ -f tools/build-offline.mjs ]]; then
  node tools/build-offline.mjs
  python3 tools/check-offline.py
fi
bash Upload_MacGyver_v21_SSH.sh --state "$SYNC_STATE"
python3 tools/pages-doctor-v28.py --publish --report reports/pages-packaging-v34.json
echo '完成公開網站部署 / Public website deployment completed.'
