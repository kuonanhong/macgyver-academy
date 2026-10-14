#!/usr/bin/env bash
# MacGyver V11: resumable, non-force GitHub SSH uploads. Run from any directory.
# Website source and model fragments go to separate repositories. No API token
# or model weight is ever written to the website snapshot.
set -euo pipefail
TASK_ROOT="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd -P)"
CODE_REPO=''; WEIGHTS_REPO=''; MODELS_DIR="$TASK_ROOT/models"
STATE_DIR="$(cd "$TASK_ROOT/.." && pwd -P)/MacGyver_GitHub_Upload_State"
BRANCH='main'; CHUNK_MIB=32; MAX_GIB=4; RETRIES=5
PRIVATE_CONFIRMED=0; DRY_RUN=0; RESTORE=0; RESTORE_TO=''
usage() {
  cat <<'HELP'
使用：bash upload-github-ssh.sh --repo git@github.com:OWNER/ACADEMY.git [選項]

上傳網站程式（不含權重）：
  bash upload-github-ssh.sh --repo git@github.com:OWNER/ACADEMY.git

再將本機權重分片上傳至另一個已建立的私人 repository：
  bash upload-github-ssh.sh --repo git@github.com:OWNER/ACADEMY.git \
    --weights-repo git@github.com:OWNER/PRIVATE-MODELS.git \
    --models-dir /你的模型資料夾 --weights-private-confirmed

  --repo SSH_URL           網站程式 GitHub 倉庫；不指定則只處理權重
  --weights-repo SSH_URL   獨立私人權重倉庫（不得與 --repo 相同）
  --models-dir DIRECTORY  權重來源；預設為此專案 models/
  --weights-private-confirmed  表示已親自在 GitHub 檢查權重倉庫是 Private
  --state DIRECTORY       本機續傳資料夾，預設位於專案旁；請勿在中途刪除
  --chunk-mib N           每片 MiB，1–48，預設 32；續傳時保持相同數值
  --max-gib N             權重總量 GiB 上限，1–4，預設 4
  --branch NAME           兩個新倉庫的分支名稱，預設 main
  --retries N             失敗後重試次數，1–10，預設 5
  --dry-run               本機預檢與容量估算；不分片、不連線或提交
  --restore-to DIRECTORY  只從 --weights-repo 下載、重組並驗證至此目錄

斷線後原命令重跑。已成功推送的分片保留，未完成的一批重試；
Git/SSH 不能恢復一個中斷的封包的位元組偏移。
GitHub Pages 的公開網站不能直接讀取這個私人權重倉庫。
HELP
}
die(){ printf '停止：%s\n' "$*" >&2; exit 1; }
while (($#)); do
  case "$1" in
    --repo|--weights-repo|--models-dir|--state|--chunk-mib|--max-gib|--branch|--retries|--restore-to)
      (($#>=2)) && [[ -n "$2" ]] || die "$1 缺少參數"
      case "$1" in
        --repo) CODE_REPO="$2";; --weights-repo) WEIGHTS_REPO="$2";;
        --models-dir) MODELS_DIR="$2";; --state) STATE_DIR="$2";;
        --chunk-mib) CHUNK_MIB="$2";; --max-gib) MAX_GIB="$2";;
        --branch) BRANCH="$2";; --retries) RETRIES="$2";;
        --restore-to) RESTORE=1; RESTORE_TO="$2";;
      esac; shift 2;;
    --weights-private-confirmed) PRIVATE_CONFIRMED=1; shift;;
    --dry-run) DRY_RUN=1; shift;;
    -h|--help) usage; exit 0;;
    *) die "未知參數：$1（請用 --help）";;
  esac
done
[[ -n "$CODE_REPO" || -n "$WEIGHTS_REPO" ]] || { usage; exit 2; }
ssh_url(){ [[ "$1" =~ ^git@github[.]com:[A-Za-z0-9][A-Za-z0-9_.-]*/[A-Za-z0-9][A-Za-z0-9_.-]*(\.git)?$ ]]; }
[[ -z "$CODE_REPO" ]] || ssh_url "$CODE_REPO" || die '--repo 必須是 git@github.com:OWNER/REPO.git。'
[[ -z "$WEIGHTS_REPO" ]] || ssh_url "$WEIGHTS_REPO" || die '--weights-repo 必須是 git@github.com:OWNER/REPO.git。'
[[ -z "$WEIGHTS_REPO" || "${WEIGHTS_REPO%.git}" != "${CODE_REPO%.git}" ]] || die '程式與權重須使用不同倉庫。'
[[ "$CHUNK_MIB" =~ ^[0-9]+$ && "$CHUNK_MIB" -ge 1 && "$CHUNK_MIB" -le 48 ]] || die '--chunk-mib 需為 1–48。'
[[ "$MAX_GIB" =~ ^[0-9]+$ && "$MAX_GIB" -ge 1 && "$MAX_GIB" -le 4 ]] || die '--max-gib 需為 1–4。'
[[ "$RETRIES" =~ ^[0-9]+$ && "$RETRIES" -ge 1 && "$RETRIES" -le 10 ]] || die '--retries 需為 1–10。'
command -v git >/dev/null || die '請先安裝 Git。'
command -v python3 >/dev/null || die '請先安裝 Python 3.10+。'
python3 -c 'import sys;sys.exit(sys.version_info<(3,10))' || die 'Python 版本需為 3.10+。'
git check-ref-format --branch "$BRANCH" >/dev/null || die 'Git 分支名稱不合法。'
if ((RESTORE)); then
  [[ -n "$WEIGHTS_REPO" && -z "$CODE_REPO" ]] || die '--restore-to 只可搭配 --weights-repo。'
elif [[ -n "$WEIGHTS_REPO" && "$PRIVATE_CONFIRMED" != 1 ]]; then
  die '請先建立並檢查另一個私人倉庫，再加 --weights-private-confirmed。'
fi
if [[ -n "$WEIGHTS_REPO" && "$RESTORE" == 0 ]]; then
  [[ -d "$MODELS_DIR" && ! -L "$MODELS_DIR" ]] || die '找不到實際模型資料夾或它是符號連結。'
fi

# This is an isolated state location, never a subfolder of the public project.
STATE_DIR="$(python3 - "$TASK_ROOT" "$STATE_DIR" <<'PY'
from pathlib import Path
import sys
root, target=(Path(x).resolve() for x in sys.argv[1:])
if target==root or root in target.parents or target in root.parents:
    sys.exit('續傳資料夾必須在專案之外，不能位於其上層。')
print(target)
PY
)" || die '續傳資料夾路徑無效。'

if ((DRY_RUN)); then
  if [[ -n "$CODE_REPO" ]]; then
    bash "$TASK_ROOT/publish-github.sh" --repo "$CODE_REPO" --out "$STATE_DIR/source" --dry-run > /dev/null
    echo '公開程式匯出預檢通過（模型、權重與本機會員資料排除）。'
  fi
  if [[ -n "$WEIGHTS_REPO" && "$RESTORE" == 0 ]]; then
    python3 - "$MODELS_DIR" "$CHUNK_MIB" "$MAX_GIB" <<'PY'
import os,sys
from pathlib import Path
root=Path(sys.argv[1]); size=0; selected=0; binaries=0
allowed={'.gguf','.safetensors','.onnx','.pth','.pt','.bin','.model','.tiktoken','.vocab','.merges','.json','.txt','.md'}
weight={'.gguf','.safetensors','.onnx','.pth','.pt','.bin','.model'}
for base,dirs,files in os.walk(root,followlinks=False):
    if any((Path(base)/d).is_symlink() for d in dirs):sys.exit('模型資料夾內有符號連結。')
    dirs[:]=sorted(d for d in dirs if not d.startswith('.'))
    for name in sorted(files):
        path=Path(base)/name
        if path.is_symlink():sys.exit('模型檔是符號連結。')
        if name.startswith('.') or path.suffix.lower() not in allowed:continue
        size+=path.stat().st_size;selected+=1;binaries+=path.suffix.lower() in weight
print(f'權重預估：{selected} 檔、{size/1024**3:.2f} GiB，約 {(size+int(sys.argv[2])*1024**2-1)//(int(sys.argv[2])*1024**2)} 片（實際按檔案切片）。')
if not binaries or size>int(sys.argv[3])*1024**3:sys.exit('沒有模型權重檔，或已超過指定上限。')
PY
  fi
  echo 'DRY RUN：未連線、分片、提交或上傳。';exit 0
fi
mkdir -p "$STATE_DIR"
[[ ! -L "$STATE_DIR" ]] || die '續傳資料夾不可是符號連結。'

if [[ -n "$CODE_REPO" ]]; then
  echo '上傳網站程式：使用經審查的隔離匯出，不包含 models/。'
  attempt=1
  while :; do
    if bash "$TASK_ROOT/publish-github.sh" --repo "$CODE_REPO" --out "$STATE_DIR/source" --branch "$BRANCH" --push > "$STATE_DIR/source-last.log" 2>&1; then
      echo '程式推送完成；GitHub Pages 仍需在 Settings → Pages 選擇 GitHub Actions 並手動啟動附帶的 workflow。'
      break
    fi
    if ((attempt>=RETRIES)); then
      tail -n 12 "$STATE_DIR/source-last.log" >&2
      die '程式推送未完成。本機匯出及提交已保留；檢查網路、SSH、倉庫分支，再重跑相同命令。'
    fi
    echo "程式推送第 $attempt 次失敗；等待後重試，已完成提交保留。" >&2
    sleep $((attempt*3));attempt=$((attempt+1))
  done
fi
[[ -n "$WEIGHTS_REPO" ]] || exit 0
MODEL_GIT="$STATE_DIR/weights-repo"; NEXT_MANIFEST="$STATE_DIR/weights-next-manifest.json"
if ((RESTORE)); then
  if [[ ! -e "$MODEL_GIT" ]]; then
    git clone --depth 1 --branch "$BRANCH" "$WEIGHTS_REPO" "$MODEL_GIT"
  else
    [[ -d "$MODEL_GIT/.git" ]] || die '已有同名資料夾但不是權重續傳倉庫。'
    [[ "$(git -C "$MODEL_GIT" config --get remote.origin.url)" == "$WEIGHTS_REPO" ]] || die '續傳目錄指向不同的權重倉庫。'
    [[ -z "$(git -C "$MODEL_GIT" status --porcelain)" ]] || die '權重續傳倉庫已有本機變更，請先處理。'
    git -C "$MODEL_GIT" pull --ff-only origin "$BRANCH"
  fi
  python3 - "$MODEL_GIT" "$RESTORE_TO" <<'PY'
import hashlib,json,os,sys,tempfile
from pathlib import Path
repo=Path(sys.argv[1]);dest=Path(sys.argv[2]).expanduser().resolve();dest.mkdir(parents=True,exist_ok=True)
doc=json.loads((repo/'weights-manifest.json').read_text('utf-8'))
assert doc.get('schema')==1
def sha256_file(path):
    digest=hashlib.sha256()
    with path.open('rb') as stream:
        while data:=stream.read(1024*1024):digest.update(data)
    return digest.hexdigest()
for item in doc['files']:
    rel=Path(item['path']); assert not rel.is_absolute() and '..' not in rel.parts
    target=dest/rel;target.parent.mkdir(parents=True,exist_ok=True)
    if any(p.is_symlink() for p in [target,*target.parents] if p==dest or dest in p.parents):raise ValueError('Restoration path contains a symlink.')
    if target.exists():
        if target.stat().st_size==item['size'] and sha256_file(target)==item['sha256']:
            print('已驗證：',rel);continue
        raise ValueError('Destination already contains a different file: '+str(rel))
    whole=hashlib.sha256();total=0
    with tempfile.NamedTemporaryFile(dir=target.parent,prefix='.macgyver-',delete=False) as tmp:
        temporary=Path(tmp.name)
        try:
            for part in item['parts']:
                name=Path(part['path']);assert name.parts[:1]==('parts',) and '..' not in name.parts
                data=(repo/name).read_bytes()
                if len(data)!=part['size'] or hashlib.sha256(data).hexdigest()!=part['sha256']:raise ValueError('Chunk mismatch: '+str(name))
                tmp.write(data);whole.update(data);total+=len(data)
        except BaseException:
            temporary.unlink(missing_ok=True);raise
    if total!=item['size'] or whole.hexdigest()!=item['sha256']:
        temporary.unlink();raise ValueError('Model SHA-256 mismatch: '+str(rel))
    os.chmod(temporary,0o600);os.replace(temporary,target)
    print('已還原並驗證：',rel)
PY
  exit 0
fi

if [[ ! -d "$MODEL_GIT/.git" ]]; then
  [[ ! -e "$MODEL_GIT" ]] || die '權重續傳資料夾已存在且不是本工具建立的 Git 倉庫。'
  mkdir -p "$MODEL_GIT"; git -C "$MODEL_GIT" init -q
  git -C "$MODEL_GIT" symbolic-ref HEAD "refs/heads/$BRANCH"
  git -C "$MODEL_GIT" remote add origin "$WEIGHTS_REPO"
else
  [[ "$(git -C "$MODEL_GIT" config --get remote.origin.url)" == "$WEIGHTS_REPO" ]] || die '權重續傳資料夾指向不同倉庫。'
  [[ "$(git -C "$MODEL_GIT" symbolic-ref --short HEAD)" == "$BRANCH" ]] || die '續傳分支不同。'
fi
git -C "$MODEL_GIT" ls-remote origin HEAD >/dev/null || die 'SSH 無法連上權重倉庫，請檢查已建立的 repo 和 SSH key。'
remote_tip="$(git -C "$MODEL_GIT" ls-remote --heads origin "refs/heads/$BRANCH" | cut -f 1)" || die '無法確認權重倉庫分支。'
if ! git -C "$MODEL_GIT" rev-parse --verify HEAD >/dev/null 2>&1 && [[ -n "$remote_tip" ]]; then
  die '權重倉庫已有提交，但本機沒有相符的續傳歷史；請使用原續傳資料夾或另建空白私人倉庫。'
fi
for value in user.name user.email; do
  [[ -n "$(git -C "$MODEL_GIT" config --get "$value" || true)" ]] || die "請先設定 git config --global $value。"
done
retry_model_push(){
  local attempt=1 remote_head local_head
  local_head="$(git -C "$MODEL_GIT" rev-parse HEAD)"
  while :; do
    remote_head="$(git -C "$MODEL_GIT" ls-remote --heads origin "refs/heads/$BRANCH" | cut -f 1)" || die '無法確認遠端分支；未強推。'
    if [[ -n "$remote_head" && "$remote_head" != "$local_head" ]]; then
      git -C "$MODEL_GIT" cat-file -e "$remote_head^{commit}" 2>/dev/null &&
        git -C "$MODEL_GIT" merge-base --is-ancestor "$remote_head" "$local_head" || die '遠端已有不同提交，請人工處理，未強推。'
    fi
    [[ "$remote_head" != "$local_head" ]] || return 0
    if git -C "$MODEL_GIT" push --set-upstream origin "HEAD:refs/heads/$BRANCH"; then return 0; fi
    if ((attempt>=RETRIES)); then die '本批權重上傳失敗。本機提交完整保留，斷線後重跑相同命令。'; fi
    echo "本批權重第 $attempt 次中斷；等待後重試。" >&2
    sleep $((attempt*3));attempt=$((attempt+1))
  done
}
if git -C "$MODEL_GIT" rev-parse --verify HEAD >/dev/null 2>&1; then retry_model_push; fi

# BEGIN MODEL CHUNKER
python3 - "$MODELS_DIR" "$MODEL_GIT" "$NEXT_MANIFEST" "$CHUNK_MIB" "$MAX_GIB" "$STATE_DIR" <<'PY'
import hashlib,json,os,sys,tempfile
from pathlib import Path
source,repo,manifest,chunk_mib,max_gib,state=Path(sys.argv[1]),Path(sys.argv[2]),Path(sys.argv[3]),int(sys.argv[4]),int(sys.argv[5]),Path(sys.argv[6])
allowed={'.gguf','.safetensors','.onnx','.pth','.pt','.bin','.model','.tiktoken','.vocab','.merges','.json','.txt','.md'}
weight={'.gguf','.safetensors','.onnx','.pth','.pt','.bin','.model'}
files=[]
for base,dirs,names in os.walk(source,followlinks=False):
    if any((Path(base)/d).is_symlink() for d in dirs):raise ValueError('模型子目錄含符號連結，停止。')
    dirs[:]=sorted(d for d in dirs if not d.startswith('.'))
    for name in sorted(names):
        p=Path(base)/name
        if p.is_symlink():raise ValueError('模型檔含符號連結，停止。')
        if name.startswith('.') or p.suffix.lower() not in allowed:continue
        if p.is_file():files.append(p)
files.sort(key=lambda p:p.relative_to(source).as_posix())
total=sum(p.stat().st_size for p in files)
if not any(p.suffix.lower() in weight for p in files) or total>max_gib*1024**3:raise ValueError('沒有模型權重檔，或總量超過上限；請分不同私人倉庫。')
chunk_bytes=chunk_mib*1024**2;state.joinpath('tmp').mkdir(exist_ok=True)
entries=[]
for p in files:
    before=p.stat();whole=hashlib.sha256();parts=[];relative=p.relative_to(source).as_posix()
    with p.open('rb') as fh:
        while data:=fh.read(chunk_bytes):
            whole.update(data);digest=hashlib.sha256(data).hexdigest()
            part='parts/'+digest[:2]+'/'+digest+'.part';target=repo/part
            target.parent.mkdir(parents=True,exist_ok=True)
            if target.exists():
                if target.is_symlink() or target.stat().st_size!=len(data) or hashlib.sha256(target.read_bytes()).hexdigest()!=digest:
                    raise ValueError('本機分片與雜湊不符；請保留續傳目錄並人工排查：'+part)
            else:
                with tempfile.NamedTemporaryFile(dir=state/'tmp',delete=False) as tmp:
                    tmp.write(data);temporary=Path(tmp.name)
                os.replace(temporary,target)
            parts.append({'path':part,'size':len(data),'sha256':digest})
    after=p.stat()
    if (before.st_size,before.st_mtime_ns)!=(after.st_size,after.st_mtime_ns):raise ValueError('讀取期間來源模型變動：'+relative)
    entries.append({'path':relative,'size':before.st_size,'sha256':whole.hexdigest(),'parts':parts})
document={'schema':1,'chunk_bytes':chunk_bytes,'files':entries}
manifest.write_text(json.dumps(document,ensure_ascii=False,indent=2)+'\n','utf-8')
print(f'準備完成：{len(entries)} 檔、{total/1024**3:.2f} GiB、{sum(len(x["parts"]) for x in entries)} 個引用分片。')
PY
# END MODEL CHUNKER
commit_batch(){
  if ! git -C "$MODEL_GIT" diff --cached --quiet; then
    git -C "$MODEL_GIT" commit -m "$1" >/dev/null
    retry_model_push
  fi
}
batch=0
while IFS= read -r -d '' part; do
  git -C "$MODEL_GIT" add -- "$part";batch=$((batch+1))
  if ((batch>=4)); then commit_batch 'Upload verified model fragments';batch=0; fi
done < <(python3 - "$NEXT_MANIFEST" <<'PY'
import json,sys
x=json.load(open(sys.argv[1],encoding='utf-8'))
for part in sorted({p['path'] for f in x['files'] for p in f['parts']}):sys.stdout.buffer.write(part.encode()+b'\0')
PY
)
commit_batch 'Upload verified model fragments'
cp "$NEXT_MANIFEST" "$MODEL_GIT/weights-manifest.json"
git -C "$MODEL_GIT" add -- weights-manifest.json
# Only remove old content-addressed fragments when the replacement manifest is
# committed in the same final transaction; old readers never see missing parts.
while IFS= read -r -d '' part; do git -C "$MODEL_GIT" rm -q -- "$part"; done < <(python3 - "$MODEL_GIT" "$NEXT_MANIFEST" <<'PY'
import json,subprocess,sys
repo,manifest=sys.argv[1:];doc=json.load(open(manifest,encoding='utf-8'))
needed={p['path'] for f in doc['files'] for p in f['parts']}
for raw in subprocess.check_output(['git','-C',repo,'ls-files','-z','--','parts']).split(b'\0'):
    if raw and raw.decode() not in needed:sys.stdout.buffer.write(raw+b'\0')
PY
)
commit_batch 'Publish verified model manifest'
echo '權重分片與 SHA-256 manifest 已推送。新電腦可用 --weights-repo SSH_URL --restore-to DIRECTORY 還原。'
