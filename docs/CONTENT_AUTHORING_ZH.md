# 馬蓋先工程學院：內容編寫指南

英文站名為 **MacGyver Engineering Academy**。本指南說明如何把工程題目編成可循序跟做、具有知識點與驗收證據的教學課程。網站名稱與課程均不表示原作品、廠商或工程業主的授權／背書。

## 1. 先分清內容成熟度

| 類型 | 意義 | 必須提供 | 不應宣稱 |
| --- | --- | --- | --- |
| 題目路線圖 `roadmap` | 值得研究的工程／工藝題目 | 中英名稱、領域、研究摘要、來源範圍 | 已有完整逐步課程 |
| 逐步課程 | 人工編寫的公開原理教學 | 階段、工序、知識點、概念組合、檢核題、中英內容及來源 | 原廠建造手冊或量產製程配方 |
| 經驗證工業手冊 | 適用於指定產品、版本、場地和人員的實務文件 | 經核准圖面、材料規格、公差、合格程序、專業審查與驗證證據 | 由本網站現有教學自動取得此資格 |

目前 2,000 項是編輯選題目錄，其中包含 17 門精選逐步課程；其餘仍為路線圖。17 門不是額外加到 2,000 項之外。沒有任何路線圖可因加入 AI 回答便自動視為工業手冊。

## 2. 四層結構

固定採「**專案 → 階段 → 工序 → 知識點**」，最多四層。專案負責總體目的；階段建立合理工作順序；工序要求一個可觀察的學習產出；知識點解釋原理、假設、限制與驗收方法。

例如：ASML 微影機 → EUV 反射光學 → 理解多層膜干涉 → 界面反射的振幅與相位。課程不是把一個段落任意切成 500 個按鈕。若真正需要 500 道工序，可按模組分階段增列；每道都必須有不同的目標與驗收證據。資料結構支援大量工序，但本版沒有聲稱已編寫「2,000 × 500」道內容。

目前資料採 `stages[].steps[].knowledge[]`。前端依階段和工序的陣列順序循序解鎖，`order` 也應與陣列一致。不要把它當作已實作任意分支依賴、多人同步施工或物理正確 CAD 裝配。

## 3. 檔案與擴充流程

主要內容位於 `public/academy/data/`：

| 檔案 | 用途 |
| --- | --- |
| `catalog.json` | 完整題目目錄，包括路線圖及可開啟課程的項目 |
| `featured.json` | 已編寫的逐步課程 |
| `sources.json` | 公開來源與支援範圍 |
| `photos.json` | 真實照片的原始頁面、作者及授權 |
| `materials.json` | 使用者提供教材的檔名、頁／投影片索引及閱讀範圍 |

建議流程：

1. 先在 `catalog.json` 新增唯一且穩定的 `id`，填寫 `title`、`titleEn`、`summary`、`summaryEn`、`category`、`kind`、`status` 和 `sourceIds`。同一事物的拼字差異不能算另一項工程。
2. 查閱一次來源，記錄網址、發行機構、適用年代及它實際支持的主張。只找到領域首頁時，維持路線圖狀態。
3. 將課程物件加入 `featured.json`，並讓目錄項目的 ID 與課程一致。每個階段、工序及知識點都有唯一 ID。
4. 為每一步加入中英目標、原理、檢核與測驗；來源 ID 必須能在 `sources.json` 找到。
5. 完成原創概念圖、照片授權紀錄、來源核對及安全範圍審查後，再在目錄標為逐步課程。
6. 可攜版預設直接使用 public/academy；啟動網站檢查新課程。只有自行另建 portable/public 時才需維護副本。
7. 檢查章節排序、手機版閱讀、答案索引、來源連結、中英文及進度重開。更改既有 ID 會使舊進度無法對應，應保留 ID 或提供移轉規則。

下列為**結構示例**，只有一個工序，不能直接代表完整課程。實際來源需先登錄。`quiz.answer` 是從 0 起算的答案索引。

```json
{
  "id": "optics-learning",
  "title": "反射光學教學",
  "titleEn": "Reflective Optics Learning",
  "category": "photonics",
  "summary": "從公開原理理解 EUV 光路。",
  "summaryEn": "Understand EUV optical paths from public principles.",
  "scope": "原創概念示意，非製造圖面。",
  "scopeEn": "Original conceptual illustration, not manufacturing drawings.",
  "contentStatus": "reviewable-educational-curriculum",
  "sourceIds": ["asml-optics"],
  "depth": 4,
  "stepCount": 1,
  "estimatedMinutes": 15,
  "diagram": {
    "type": "lithography",
    "labels": ["光源", "反射光學", "晶圓"],
    "labelsEn": ["Source", "Reflective optics", "Wafer"],
    "original": true,
    "notToScale": true
  },
  "stages": [{
    "id": "optics-learning-s01",
    "order": 1,
    "title": "光路選擇",
    "titleEn": "Optical-path selection",
    "steps": [{
      "id": "optics-learning-s01-01",
      "order": 1,
      "title": "辨識反射式投影",
      "titleEn": "Identify reflective projection",
      "objective": "指出 EUV 不沿用一般透射透鏡的主要原因。",
      "objectiveEn": "Identify why EUV does not use ordinary transmissive lenses.",
      "knowledge": [{
        "id": "optics-learning-s01-01-k1",
        "title": "材料吸收",
        "titleEn": "Material absorption",
        "text": "EUV 在材料中強烈吸收，微影系統使用真空中的多層膜反射光學。",
        "textEn": "EUV is strongly absorbed by materials, so lithography uses multilayer reflective optics in vacuum."
      }],
      "check": "在示意圖標出反射元件及真空光路。",
      "checkEn": "Mark reflective elements and the vacuum optical path.",
      "sourceIds": ["asml-optics"],
      "simulationOnly": true,
      "quiz": {
        "question": "EUV 投影光學為何採用反射鏡？",
        "questionEn": "Why do EUV projection optics use mirrors?",
        "options": ["材料對 EUV 強烈吸收", "EUV 沒有波長", "所有鏡面都完全不吸收"],
        "optionsEn": ["Materials strongly absorb EUV", "EUV has no wavelength", "Every mirror has zero absorption"],
        "answer": 0,
        "explanation": "反射光學避免透射光路的強吸收；反射鏡仍有損耗。",
        "explanationEn": "Reflective optics avoid strong transmission absorption; mirrors still have losses."
      }
    }]
  }]
}
```

`diagram.type` 必須使用前端已支援的圖型；新字串不會自動產生新的三維模型。`estimatedMinutes` 是編輯估計，不能宣稱為實測完成時間。要列出更細的複習內容，新增同層知識點；不要超過四層。

## 4. 光學課程的正確分流範例

「鏡頭如何不散色」應改成「如何控制色差」。透明材料的折射率隨波長而變，不同波長可能聚焦在不同位置。一般折射光學可透過材料配對、多元件設計、窄頻照明與系統匹配降低色差；這不等於任何系統都能完全消除色差。ZEISS 的顯微鏡說明亦指出，物鏡與管鏡的色差校正可能共同設計，跨廠混搭可能破壞校正。[2]

| 教學工序 | 知識點 | 學徒產出 | 驗收 |
| --- | --- | --- | --- |
| 畫出兩個波長的折射光路 | 色散與焦點位移；色差和球差不同 | 原創光線示意圖 | 正確標出不同焦點，沒有把所有像差混為一談 |
| 比較單片與組合透鏡概念 | 元件與材料可以互相補償部分色差 | 比較表與殘餘誤差說明 | 註明工作波段及模型假設 |
| 比較 DUV 與 EUV | 微影工作波長改變會改變可用材料與光學架構 | 兩條不同的概念光路 | EUV 沒有被畫成一般透射鏡頭串接 |
| 展開 EUV 反射模組 | 多層膜反射、波前、粗糙度、真空及污染 | 功能方塊與待驗證項目 | 把反射率、面形與污染分成不同指標 |

ASML 說明 DUV 微影採用透鏡，而 EUV 系統使用真空中的多層膜反射鏡，因為材料對 EUV 的吸收很強。[1] 因此不應把「可見光消色差雙合透鏡」直接當作「EUV 曝光機鏡頭製造」。EUV 鏡組也不是天然沒有所有像差；面形、波前、鍍膜反射及系統對位仍需工程控制。ZEISS 將 DUV、EUV 與 High-NA EUV 分列為不同光學技術領域。[3]

此範例只教授公開物理原理，不補造廠商膜厚、加工公差、污染允收值或可量產配方。引用沒有支持某個數字時，刪去數字或標為清楚的示意假設。

## 5. 引用與授權

- **項目級來源**須直接支持該工程名稱、技術主張或工序；**領域級來源**只提供研究入口。不能將 NASA／ASML／NIST 首頁掛到每個工序便聲稱已逐項查證。
- 編寫時記錄主張、來源、位置、查閱日期與適用條件；網站摘要應使用自己的文字。與版本、日期或法規有關的資料需更新核對。
- 論文中的數值應保留單位、條件、圖表位置與不確定度。原創模擬結果需附方法及程式；不要把示意數值寫成實驗資料。
- 真實照片須逐張記錄作品頁、作者、授權版本、授權網址及修改情形。優先使用可核實的公有領域或允許再利用作品；來源是 Wikimedia 或 NASA 並不免除逐張檢查。
- 官方網站可供閱讀，不等於可任意轉載照片。沒有授權便只提供來源連結。已下載素材的授權見 `assets/photos/LICENSES.txt`；不要移除署名。
- 使用者上傳的教材可以支援本次分析與索引；本次提供檔案不自動等於同意公開散布完整教材。公開站點宜保留來源索引與自行編寫摘要。
- 原創架構圖標示「概念示意／非比例」。若重畫特定原圖的獨特表達或直接使用資料圖，仍需檢查引用及再利用條件。

## 6. 內容安全與品質

經國號、阿帕契及潛艦以公開史料、非武器結構、安全、材料與品質管理為範圍，不編寫武器建造、攻擊性能改良、作戰瞄準或武裝整合程序。資安課程採授權環境、防禦與模擬。壓力、燃燒、高壓、化學或大型結構題目使用概念模型與合格程序辨識，不以頁面通關替代實務資格。

每道檢核題必須測量該工序真正的核心能力。選項不能靠長短、重複句型或固定答案位置猜出。將模型輸出的答案視為待審內容，工程術語與公式需人工核對；第三語言機器翻譯亦同。

## 參考來源

1. ASML, **Lenses & mirrors**：[官方說明](https://www.asml.com/en/technology/lithography-principles/lenses-and-mirrors)。支持 DUV 透鏡與 EUV 真空反射架構的區分；不提供完整製造配方。
2. ZEISS, **Basic Principles of Infinity Optical Systems**：[官方說明](https://www.zeiss.com/microscopy/en/resources/insights-hub/foundational-knowledge/basic-principles-of-infinity-optical-systems.html)。支持物鏡／管鏡共同校正與不相容混搭的說明；不是半導體曝光機設計手冊。
3. ZEISS SMT, **Lithography Optics**：[官方技術入口](https://www.zeiss.com/semiconductor-manufacturing-technology/products/lithography-optics.html)。支持各光學技術領域的分類。

本文件引用核對日期：2026-10-12。


## V2 新欄位與打包

完整課程只存 featured.json；catalog.json 的逐步課程項目保留 stepCount，不複製 stages。網頁啟動後依 id 合併，減少傳输量。每個新增工序應有 instruction/En、observation/En、failure/En、photoId、photoNote/En。photoEvidence 表明代表照片，不能因已有圖片就宣稱該步實拍。stage.route/routeEn 說明製程分支，description/descriptionEn 說明原理；course.flowDiagram 指向原創 SVG。

兩門重點課程的原創中英操作表與生成器位於 tools/curriculum/。修改後執行 `bash rebuild-curriculum.sh` 可重建兩門課程、來源對應、代表照片及 slim catalog。生成器提供共用模組脈絡；每道操作、判據及診斷由不同原創條目組成，不宣稱全部段落互不共用。直接改 featured.json 也可，但再次重建會以操作表取代這兩門課的直接修改，請選一種方式管理。

`python3 tools/validate-data.py` 檢查課程數量、雙語、來源、照片、唯一工序及前置關係無循環；內容數量改變時須合理更新發行規格，不得只改斷言來隱藏缺漏。`node tools/test-frontend.mjs` 檢查實際事件與大量步驟导航，`node tools/test-engineering-labs.mjs` 驗證算例公式與單位。
