from pathlib import Path
import json,html
ROOT=Path(__file__).resolve().parents[1]
DATA=ROOT/'public/academy/data'
def read(n):return json.loads((DATA/n).read_text())
def esc(v):return html.escape(str(v))
release=read('release.json');courses=[c for c in read('featured.json') if c.get('category')=='environment']
rows=''.join(f'<tr><td>{esc(c["id"])}</td><td>{esc(c["title"])}<small>{esc(c["titleEn"])}</small></td><td>{esc(c.get("subcategoryTitle",""))}</td><td>{c["stepCount"]}</td></tr>' for c in sorted(courses,key=lambda c:c['id']))
style='''*{box-sizing:border-box}body{margin:0;background:#f3f4eb;color:#203d38;font:17px/1.85 system-ui,"Noto Sans TC",sans-serif}main{max-width:1060px;margin:auto;padding:60px 28px}h1{font-size:clamp(32px,5vw,60px);line-height:1.2;letter-spacing:-.04em}h2{margin-top:60px;font-size:27px;border-top:1px solid #c3d0c2;padding-top:25px}h3{font-size:20px}.eyebrow{color:#677d59;letter-spacing:.15em;font-weight:700}.intro{font-size:21px;max-width:800px}a{color:#175f61}table{width:100%;border-collapse:collapse;font-size:15px}td,th{text-align:left;padding:14px 10px;border-bottom:1px solid #c7d4c9;vertical-align:top}th{background:#dfebdc}small{display:block;color:#65736c;font-size:12px}.box{background:#fff;border:1px solid #cfdbcb;border-radius:16px;padding:24px;margin:24px 0}.steps{counter-reset:step;list-style:none;padding:0}.steps li{counter-increment:step;padding:18px 0 18px 60px;position:relative;border-bottom:1px solid #d8dfd3}.steps li:before{content:counter(step,decimal-leading-zero);position:absolute;left:0;color:#6b895d;font-size:26px;font-weight:700}code,pre{font-family:ui-monospace,monospace}pre{background:#183d38;color:#f1f4d9;padding:20px;border-radius:12px;overflow:auto;font-size:14px}nav{display:flex;gap:20px;flex-wrap:wrap}.table-wrap{overflow:auto}@media(max-width:600px){main{padding:30px 18px}td,th{padding:10px 6px}.box{padding:18px}}@media print{body{background:white}main{padding:10px}h2{break-after:avoid}tr{break-inside:avoid}}'''
page=f'''<!doctype html><html lang="zh-Hant"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>MacGyver V17｜設計分析與使用說明</title><style>{style}</style><main>
<div class="eyebrow">MACGYVER ENGINEERING ACADEMY · V17 · 2026.10.23</div>
<h1>從看見工程，<br>走到親手理解。</h1><p class="intro">把工程地圖、真實影像、可點選設備和逐步輔助接成一條學習路徑。本次集中完成 100 門環境與城市課程的深度擴充。</p>
<nav><a href="#play">開始操作</a><a href="#design">參考作品分析</a><a href="#scope">實作與範圍</a><a href="#upload">一鍵上傳</a><a href="#courses">100門目錄</a></nav>
<div class="box"><b>交付數量</b><p>全站 {release.get('guidedCourses')} 門逐步課程、{release.get('allSteps'):,} 道工序。環境與城市 100 門，各新增 10 個技術單元 × 4 道工序，共新增 4,000 道；原有新加坡新生水 12 道保留，因此該課合計 52 道。全站既有內容保留。</p><p>20 專科場景、156 項授權實景影像（149 普通照片＋7 真實全景）、18 類場景暖身計算模型。每個新增技術單元另有可編輯算式、基準比較與筆記記錄。</p></div>
<h2 id="play">第一次玩：一條完整操作路徑</h2>
<ol class="steps"><li><b>開啟網站。</b>解壓完整包或四包合併後，電腦執行 <code>bash run-local.sh</code>，依終端機顯示的本機網址進入。純離線可直接開 <code>public/academy/index.html</code>；API、登入和模型功能須使用相應服務。</li>
<li><b>選工程領域，再選任務。</b>首頁工程島點「環境與城市」，先挑一門感興趣的工程；卡片會顯示課名與可進入的場景。白天／夜晚僅影響顯示，不代表即時日照模擬。</li>
<li><b>觀察實景、切換視角。</b>第一視角在固定位置觀察；第二視角檢視設備，可拖曳與縮放；第三視角查看教學配置。選取真正全景才能環顧拍攝點四周；普通照片保持平面呈現。</li>
<li><b>點設備看用途。</b>場景上的設備與下方設備清單共用選取狀態，右側提供用途、量測與判讀。課程流程節點連結本專題的工程程序，並明示與參考照片的區別。</li>
<li><b>逐階段動手。</b>按任務提示觀察、選設備、改參數、記錄。場景的「輔助」每按一次處理目前一個階段；最後保存觀察，仍可修改參數重做。</li>
<li><b>進入工序工作台。</b>「師傅帶我完成這一步」依序示範、套用教學參數、完成操作證據、解說答案，僅完成目前工序並留下輔助紀錄。可中途停止；完成後由你按下一步。既有登入、會員及驗收條件仍適用。</li>
<li><b>算例、驗證與反思。</b>新增課程的算例可改數字再計算，比較基準值與差值，寫入工程筆記。按檢核提示提出測量與故障假設；算出數值不等於證明真實設備安全或合格。</li></ol>
<h2 id="design">參考作品：觀察 → 教學原則 → 本次改造</h2>
<p><a href="https://puma.taipei/heart-island">HEART 政策島</a>公開頁面呈現 14 主題、94 細項及 20 協作關係，並有清單、搜尋、時間、鳥瞰與導覽控制。以下教學原則是本次設計推論；本瀏覽器的 WebGL 初始化失敗，因此未聲稱已完整玩過其 3D 動畫流程。</p>
<div class="table-wrap"><table><thead><tr><th>順序</th><th>從參考介面得到的原則</th><th>工程學院的原創實作</th></tr></thead><tbody>
<tr><td>1</td><td>先給可辨認的入口</td><td>20 個領域地圖格，每格顯示名稱、課程數和推薦任務；鍵盤與觸控皆能操作。</td></tr>
<tr><td>2</td><td>由整體走到細節</td><td>領域 → 專題 → 實景 → 設備 → 工序；同時保留搜尋與完整目錄。</td></tr>
<tr><td>3</td><td>用關係幫助理解系統</td><td>課程程序節點、相關技能及跨工程比較；畫面線條只表示教學關係，不偽稱實測管線。</td></tr>
<tr><td>4</td><td>把時間與狀態變得可見</td><td>任務階段、參數讀值、觀察紀錄與完成進度；日夜外觀提供探索氣氛。</td></tr>
<tr><td>5</td><td>降低第一次操作門檻</td><td>短任務提示和單階段輔助；詳解按需展開，初學者不用先學全部按鍵。</td></tr>
<tr><td>6</td><td>保留退出與替代路線</td><td>可取消、重設、手動重做；無 WebGL 時仍可完成設備選取、計算、記錄與工序。</td></tr></tbody></table></div>
<h3>Taichi：輔助必須有清楚的開始與結束</h3><p>已檢查使用者提供的 SmartAction Taichi v4.1 與 <a href="https://github.com/kuonanhong/taichi">taichi 專案</a>。其輔助會逐步靠近目前動作目標，保存 assisted 標記，步驟或 session 改變便停止。V17 移植的是「單次只幫目前一步、能取消、保留紀錄」的互動原則；工程參數採各工序的示範資料，不宣稱使用相同的運動學求解器。</p>
<h3>AERO：寫實感應來自可說明的資料層</h3><p>已讀取 AERO Explorer v6 ZIP、RealWorld HTML 和寫實模擬 PDF，並對照 <a href="https://github.com/kuonanhong/AERO_Explorer">AERO 專案</a>。其地理資料、地形與程序幾何讓人理解位置關係；V17 採取同樣的分層觀念，把照片、全景、教學幾何與模擬數據分別標示。未複製商業街景或限制再散布的地圖影像。</p>
<h2 id="scope">交付範圍與尚未具備的能力</h2>
<div class="table-wrap"><table><tr><th>項目</th><th>本版實際狀態</th></tr>
<tr><td>真實影像</td><td>156 項皆有來源、作者、授權及本地檔案。7 張是固定拍攝點的等距柱狀 360° 全景，其中工業全景附 4K 預設圖和 8K 原檔；公園全景為 1280×640，放大細節有限。工業照片是參考環境，並非正在運作的專科實驗室。</td></tr>
<tr><td>物件360與數位孿生</td><td>設備可用原創教學模型從不同方向檢視；未從一張照片推造未知背面。尚無每門課的實測 BIM、攝影測量、即時感測與現場校準，不能視作完整工程數位孿生。</td></tr>
<tr><td>每專科差異</td><td>20 類設備配置與代表影像，各課保留自身流程節點及文字。場景暖身採合適的共享領域模型；新增環境課程的技術單元另附自己的定量算例。</td></tr>
<tr><td>語言</td><td>核心內容及新增課程完整繁體中文／英文。保留 79 語言選項，依瀏覽器語言偏好自動選擇，不要求定位權限。其他語言使用既有字典、已載入本機模型或配置的翻譯服務；未宣稱 79 語課程都已人工完整翻譯。</td></tr>
<tr><td>平台</td><td>響應式網頁支援滑鼠、鍵盤與觸控；Bash 用於 macOS、Linux、Windows Git Bash／WSL。手機／平板使用網站；上傳腳本通常在電腦執行。真球面全景需要可用 WebGL，否則顯示明確標記的平面全景檢視。</td></tr>
<tr><td>生成式 AI</td><td>保留瀏覽器本機、Ollama、llama.cpp、Gemini 和 OpenAI 相容後端路線。權重、執行器、服務配額與 API key 需自行配置；壓縮包不內含大型權重。未設定時顯示課程知識模式，不冒稱生成式回答。單純推 GitHub Pages 不會啟動 Python 或雲端模型。</td></tr>
<tr><td>內容驗收</td><td>公式經程式重算，附教學假設、單位及適用邊界；來源支持原理和工程背景，不代表來源機構核准所有原創教案。輔助完成是學習紀錄，不是獨立操作資格。</td></tr></table></div>
<p>影像署名見 <code>public/academy/assets/scenes-v17/ATTRIBUTION.txt</code>；完整索引見 <code>data/scene-assets-v17.json</code>。Poly Haven 的本次素材採 <a href="https://polyhaven.com/license">CC0 授權</a>；其他影像依各檔 CC BY、CC BY-SA 或公共領域記錄保留條件。</p>
<h2 id="upload">一個命令：合併、驗證、增量上傳</h2>
<p>把獨立上傳腳本與完整 ZIP 放同一資料夾；若完整包下載不順，放齊 Alternative 1–4 四個 ZIP。不要先拼接二進位分卷；它們是可獨立解壓的標準 ZIP。</p>
<pre>bash Install_and_Upload_MacGyver_v17.sh --with-assets</pre>
<p>此命令核對本次檔案、解壓並執行網站增量更新；<code>--with-assets</code> 同時處理已有的本地文件／模型權重。詳細資產目錄與首次 SSH 設定見包內上傳說明。上傳工具不下載未有的權重，也不把私有模型推進公開網站分支。若只更新網站，移除 <code>--with-assets</code>。</p>
<p>已解壓並更新本地內容後，可在專案根目錄執行：</p><pre>bash Upload_MacGyver_v17_SSH.sh --with-assets</pre>
<p>目的地固定為 <a href="https://github.com/kuonanhong/macgyver-academy">kuonanhong/macgyver-academy</a>。首次需具備 Git、Python、SSH 及可存取該儲存庫的 SSH 金鑰；若首次連線要求確認主機指紋，依 GitHub 官方指紋核對。程式不替你產生帳號憑證、不強制推送，也不刪除遠端額外檔案。私有資產沿用既有私人儲存庫／遠端設定。</p>
<p>網站原始碼與離線教材完整提供。若公開 GitHub 儲存庫包含完整教材，原始檔本身仍可被下載；頁面上的會員檢查不能把公開原始碼變成保密內容。正式付費內容應採受保護後端部署。</p>
<h2 id="courses">環境與城市：100門完整目錄</h2><p>每個新單元依序安排原理、計算、驗證與故障診斷。完整來源、歷史位置、量測練習與雙語內容皆包含在課程檔案。</p>
<div class="table-wrap"><table><thead><tr><th>編號</th><th>課程</th><th>分支</th><th>工序</th></tr></thead><tbody>{rows}</tbody></table></div>
<p class="eyebrow" style="margin-top:50px">LEARN BY OBSERVING · CALCULATING · VERIFYING</p></main></html>'''
(ROOT/'docs/V17_Design_and_Quickstart_ZH.html').write_text(page,encoding='utf-8')
print('Generated docs/V17_Design_and_Quickstart_ZH.html')
