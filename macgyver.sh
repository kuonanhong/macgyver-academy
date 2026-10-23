#!/usr/bin/env bash
# V16 entry point. The previous advanced CLI is preserved separately.
set -euo pipefail
TASK_ROOT="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd -P)"
TASK_COMMAND="${1:-upload}"
case "$TASK_COMMAND" in
  -h|--help|help)
    cat <<'HELP'
Usage: bash macgyver.sh [upload|deploy|all] [uploader options]
       bash macgyver.sh compare [uploader options]
       bash macgyver.sh serve [server options]

Default: V16 incremental SSH upload; no rebuild, delete or model download.
Website: git@github.com:kuonanhong/macgyver-academy.git
Existing models/documents: git@github.com:kuonanhong/PRIVATE-MODELS.git
compare adds --dry-run and never pushes.
Uploader options: bash Upload_MacGyver_v16_SSH.sh --help

Legacy advanced commands: doctor, config, models, models-compare,
restore-models, stocks, schedule, unschedule.
These use V15 settings and behavior; models may download weights.
Use Bash (not sh). Python 3.10+ is required for upload or serve.
HELP
    exit 0 ;;
  upload|deploy|all)
    if (($#)); then shift; fi
    exec bash "$TASK_ROOT/Upload_MacGyver_v16_SSH.sh" "$@" ;;
  compare)
    shift
    exec bash "$TASK_ROOT/Upload_MacGyver_v16_SSH.sh" --dry-run "$@" ;;
  serve)
    shift
    exec bash "$TASK_ROOT/run-local.sh" "$@" ;;
  doctor|config|models|models-compare|restore-models|stocks|schedule|unschedule)
    printf '%s\n' 'Legacy V15 advanced command: uses the old settings and behavior; models may download weights, stocks may push, schedule may install a task.' >&2
    exec bash "$TASK_ROOT/macgyver-legacy-v15.sh" "$@" ;;
  --*)
    exec bash "$TASK_ROOT/Upload_MacGyver_v16_SSH.sh" "$@" ;;
  *)
    printf 'Unknown command: %s. Run: bash macgyver.sh --help\n' "$TASK_COMMAND" >&2
    exit 2 ;;
esac
