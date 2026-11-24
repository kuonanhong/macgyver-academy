#!/usr/bin/env bash
set -euo pipefail
umask 077
PROJECT_DIR="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
PYTHON_BIN="${PYTHON_BIN:-python3}"
FILM='C01'
METADATA=''
MANIFEST=''
CLIENT_JSON="${MACGYVER_YOUTUBE_CLIENT_JSON:-}"
TOKEN_JSON="${MACGYVER_YOUTUBE_TOKEN_JSON:-}"
PRIVATE_STATE=''
REPORT=''
PHASE='all'
OFFLINE=0
usage() {
  printf '%s\n' 'Usage: bash Upload_Process_V34.sh --film C01|C01-long --client CLIENT.json --token TOKEN.json [--phase all|playlist|videos|captions|verify]'
  printf '%s\n' 'Offline check: bash Upload_Process_V34.sh --film C01 --offline-preflight'
  printf '%s\n' 'Other reviewed process films: --film ID --metadata JOB.json. Optional: --manifest PATH --state PRIVATE_DIR --report PATH.'
  printf '%s\n' 'Run publishing only after channel limits reset. No scheduled or automatic quota retry. Each film has independent private progress.'
  printf '%s\n' 'Checks fixed channel and exact series playlist; reuses it or creates only if none exists. Existing playlist items are never reordered.'
  printf '%s\n' 'Uploads the main MP4 and five caption tracks. Alternate audio publication still depends on YouTube Studio support.'
}
while (($#)); do
  case "$1" in
    --film|--metadata|--manifest|--client|--token|--state|--report|--phase)
      (($# >= 2)) || { usage >&2; exit 2; }
      case "$1" in
        --film) FILM="$2" ;; --metadata) METADATA="$2" ;; --manifest) MANIFEST="$2" ;;
        --client) CLIENT_JSON="$2" ;; --token) TOKEN_JSON="$2" ;; --state) PRIVATE_STATE="$2" ;;
        --report) REPORT="$2" ;; --phase) PHASE="$2" ;;
      esac
      shift 2 ;;
    --offline-preflight) OFFLINE=1; shift ;;
    -h|--help) usage; exit 0 ;;
    *) usage >&2; exit 2 ;;
  esac
done
[[ "$FILM" =~ ^[A-Z][0-9]{2,3}(-long)?$ ]] || { usage >&2; exit 2; }
case "$PHASE" in all|playlist|videos|captions|verify) ;; *) usage >&2; exit 2 ;; esac
if [[ -z "$METADATA" ]]; then
  if [[ "$FILM" == C01 ]]; then
    METADATA="$PROJECT_DIR/docs/PACKAGING_PROCESS_C01_YOUTUBE_METADATA_V34.json"
  elif [[ "$FILM" == *-long ]]; then
    METADATA="$PROJECT_DIR/../delivery/process-long-v34/$FILM/youtube-metadata.long-v34.json"
  else
    printf '%s\n' 'Supply --metadata for this reviewed process film.' >&2
    exit 2
  fi
fi
PRIVATE_STATE="${PRIVATE_STATE:-${XDG_STATE_HOME:-$HOME/.local/state}/macgyver-youtube/process-v34/$FILM}"
REPORT="${REPORT:-$PROJECT_DIR/reports/YOUTUBE_PROCESS_${FILM}_V34.json}"
ARGS=(--film "$FILM" --metadata "$METADATA" --expected-channel 'UCXcPnnnM7btkcHwSFkVckzQ' --phase "$PHASE")
[[ -z "$MANIFEST" ]] || ARGS+=(--manifest "$MANIFEST")
if [[ "$OFFLINE" == 1 ]]; then
  ARGS+=(--offline-preflight)
else
  [[ -n "$CLIENT_JSON" && -n "$TOKEN_JSON" ]] || { usage >&2; exit 2; }
  ARGS+=(--client "$CLIENT_JSON" --token "$TOKEN_JSON" --state "$PRIVATE_STATE" --report "$REPORT")
fi
exec "$PYTHON_BIN" "$PROJECT_DIR/tools/publish-process-youtube-v34.py" "${ARGS[@]}"
