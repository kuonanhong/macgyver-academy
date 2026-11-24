#!/usr/bin/env bash
set -euo pipefail
umask 077

# Explicit invocation only. No scheduler, automatic quota retry, or credential
# discovery. Every phase verifies the fixed authorized YouTube channel.
SCRIPT_DIR="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
if [[ -f "$SCRIPT_DIR/tools/publish-packaging-youtube-v33.py" ]]; then
  PROJECT_DIR="$SCRIPT_DIR"
else
  PROJECT_DIR="${SCRIPT_DIR}/../../MacGyver_Engineering_Academy_v32"
fi
PACKAGE_DIR="${MACGYVER_NARRATED_DIR:-$PROJECT_DIR/../delivery/narrated-v33}"
PACKAGE_EXPLICIT=0
PYTHON_BIN="${PYTHON_BIN:-python3}"
EXPECTED_CHANNEL='UCXcPnnnM7btkcHwSFkVckzQ'
EXPECTED_PLAYLIST_TITLE='馬蓋先創意工程學院｜先進半導體封裝：5分鐘俯瞰導覽'
CLIENT_JSON="${MACGYVER_YOUTUBE_CLIENT_JSON:-}"
TOKEN_JSON="${MACGYVER_YOUTUBE_TOKEN_JSON:-}"
PRIVATE_STATE="${MACGYVER_YOUTUBE_STATE_DIR:-${XDG_STATE_HOME:-$HOME/.local/state}/macgyver-youtube/narrated-v34}"
PHASE='all'
METADATA=''
MANIFEST=''
REPORT=''

usage() {
  printf '%s\n' 'Usage: bash Upload_Narrated_V34.sh --client CLIENT.json --token TOKEN.json [--package NARRATED_DIR] [--state PRIVATE_DIR] [--phase all|playlist|videos|captions|verify]'
  printf '%s\n' 'Optional relocated files: --metadata PATH --manifest PATH --report PATH. Rebuild the reviewed job when media paths change.'
  printf '%s\n' 'Run only after the channel upload/quota limits have reset and the local films have been reviewed.'
  printf '%s\n' 'The verified channel reuses one exact-title playlist, creates only after an exhaustive zero-match result, and stops on ambiguity or uncertain prior creation.'
  printf '%s\n' 'No unconfirmed playlist/video IDs are assumed. Installed source metadata is preferred unless --package or --metadata is supplied.'
}
while (($#)); do
  case "$1" in
    --client|--token|--state|--phase|--package|--metadata|--manifest|--report)
      (($# >= 2)) || { usage >&2; exit 2; }
      case "$1" in
        --client) CLIENT_JSON="$2" ;;
        --token) TOKEN_JSON="$2" ;;
        --state) PRIVATE_STATE="$2" ;;
        --phase) PHASE="$2" ;;
        --package) PACKAGE_DIR="$2"; PACKAGE_EXPLICIT=1 ;;
        --metadata) METADATA="$2" ;;
        --manifest) MANIFEST="$2" ;;
        --report) REPORT="$2" ;;
      esac
      shift 2 ;;
    -h|--help) usage; exit 0 ;;
    *) usage >&2; exit 2 ;;
  esac
done
case "$PHASE" in all|playlist|videos|captions|verify) ;; *) usage >&2; exit 2 ;; esac
[[ -n "$CLIENT_JSON" && -n "$TOKEN_JSON" ]] || { usage >&2; exit 2; }
if [[ -z "$METADATA" && "$PACKAGE_EXPLICIT" == 0 && -f "$PROJECT_DIR/docs/PACKAGING_YOUTUBE_METADATA_V34.json" ]]; then
  METADATA="$PROJECT_DIR/docs/PACKAGING_YOUTUBE_METADATA_V34.json"
  MANIFEST="${MANIFEST:-$PROJECT_DIR/public/academy/assets/packaging-tour-v33/videos/manifest.json}"
  REPORT="${REPORT:-$PROJECT_DIR/reports/YOUTUBE_PUBLICATION_V34.json}"
else
  METADATA="${METADATA:-$PACKAGE_DIR/youtube-job-v34/metadata.json}"
  MANIFEST="${MANIFEST:-$PACKAGE_DIR/manifest.json}"
  REPORT="${REPORT:-$PACKAGE_DIR/youtube-job-v34/publication-report.json}"
fi

# This check reads only the prepared public metadata, never credential files.
"$PYTHON_BIN" - "$METADATA" "$EXPECTED_PLAYLIST_TITLE" <<'PY'
import json, sys
from pathlib import Path
job = json.loads(Path(sys.argv[1]).read_text(encoding='utf-8'))
if job.get('jobCompleteness') != 'complete-six-video-job':
    raise SystemExit('The complete six-video V34 job is required.')
if job.get('playlist', {}).get('title') != sys.argv[2]:
    raise SystemExit('The prepared job does not target the authorized existing playlist title.')
if job.get('playlist', {}).get('creationPolicy') != 'reuse-exact-title-or-create-if-absent' or job.get('playlist', {}).get('requireExisting') is not False:
    raise SystemExit('This V34 job must use exact-title reuse or authorized creation only when no match exists.')
PY

if [[ "$PHASE" == all ]]; then
  PHASES=(playlist videos captions verify)
else
  PHASES=("$PHASE")
fi
for current_phase in "${PHASES[@]}"; do
  "$PYTHON_BIN" "$PROJECT_DIR/tools/publish-packaging-youtube-v33.py" \
    --client "$CLIENT_JSON" --token "$TOKEN_JSON" \
    --metadata "$METADATA" --manifest "$MANIFEST" --state "$PRIVATE_STATE" \
    --expected-channel "$EXPECTED_CHANNEL" --phase "$current_phase" \
    --report "$REPORT" --require-qr
done
printf 'Publication phase completed. Safe public report: %s\n' "$REPORT"
