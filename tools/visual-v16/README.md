# V16 圖示與真實照片

這個目錄保存可重建的視覺素材來源、明確的主題對應、照片來源證據及驗證程式。瀏覽器只讀取產出的 SVG／JPEG 與按需載入的資料，不需要 Python 或繪圖套件。

## 已提供的範圍

- 20 個首頁分類各有不同幾何結構的彩色 SVG。
- 全部 2,066 個專題皆有固定路徑的 SVG。既有逐步課程與鐵道專題合計 1,003 個，其幾何結構全部不同；檢查時移除文字、標題、ID、顏色、透明度與繪圖順序差異。尚未展開為逐步課程的部分候選專題可以共用主題構圖，沒有宣稱這些候選專題也全部不同。
- 圖示由主題圖形及課程中的工程元件組合而成。123 個原創元件圖形在 `glyphs.py`；100 個鐵道專題及兩個資訊專題有人工撰寫的對應覆寫。沒有用流水號、隨機邊框或雜湊值改變幾何圖形。
- 原有 118 張授權照片，加上本版 11 張有原始來源證據的新照片，共 129 張；全部保存在安裝包內，可離線讀取。新增 JPEG 共 2,442,829 bytes。20 個分類及全部 2,066 個專題皆有明確的照片對應。
- 11 個專題使用與具名工程／設備相符的照片，其餘 2,055 個專題使用已標示的同領域代表照片。不同專題可重用照片；這不是每個課程、每個步驟各自獨立拍攝的影像。照片與示意模型並不構成現場校準、即時更新的數位孿生。

## 瀏覽器介面

```text
assets/icons-v16/categories/<category>.svg
assets/icons-v16/projects/<course-id>.svg
data/icon-manifest-v16.json
data/scene-photos-v16.json
data/photos.json
```

首頁及課程卡片可直接由分類／專題 ID 建立圖示路徑，配合 `loading="lazy"`、`decoding="async"`，不需要先下載完整圖示對照表。圖示名稱來自課程標題，英文短標籤只作識別輔助；可存取名稱應使用介面目前語言的課程標題。

`scene-photos-v16.json` 的 `categories`／`courses` 記錄 `photoId`、`photoIds`、`match`、`note`、`noteEn`；`photos` 包含實際拍攝對象、作者、授權、來源與本地檔案路徑。`match: exact` 只表示照片所拍攝的具名設備／工程相符，並不表示這是課程模型所描述時間或狀態的現場紀錄。場景畫面應保留這些說明及作者／授權／來源連結。

## 離線重建與驗證

需要 Python 3.9+；照片處理和驗證另需 Pillow。正式網頁執行不需要這些開發依賴。

```bash
python3 -m venv .venv-visuals
. .venv-visuals/bin/activate
python3 -m pip install Pillow
python3 tools/visual-v16/build_icons.py
python3 tools/visual-v16/build_photo_manifest.py
python3 tools/visual-v16/validate_visuals.py
```

請先完成 `catalog.json` 的課程修改，再重建圖示與照片對應，最後執行專案的離線資料建置程序。`build_icons.py` 會更新 SVG、圖示對照表與重複檢查報告；`build_photo_manifest.py` 會更新 `photos.json`、場景對應與照片署名文件。若新增逐步課程發生幾何重複，應根據真實課程內容修改 `icon-overrides.json`，加入不同且相關的工程元件，直到驗證通過。

`validate_visuals.py` 不匯入產生器，獨立檢查全部 SVG 是否只包含本地安全向量元素、檔案 SHA-256、所有必要圖示的幾何唯一性、照片解碼與尺寸、課程／分類對應，以及新增照片的 Commons 原始來源證據。結果寫入 `VALIDATION_VISUALS_V16.json`。

## 需要重新取得照片時

```bash
python3 tools/visual-v16/fetch_photos.py
python3 tools/visual-v16/build_photo_manifest.py
python3 tools/visual-v16/validate_visuals.py
```

下載清單是人工審查的 `photo-selection.json`。程式只從 Wikimedia Commons API 取得明確選定的照片與授權資料，將 API 證據保存於 `provenance/`，並記錄原檔 SHA-1 與實際交付 JPEG 的 SHA-256。變更照片選項時，程式會檢查快取來源檔名，避免同一 ID 留下舊照片或舊授權資料。已存在且來源不變的本地 JPEG 不會重複下載；需要重新壓縮時可先移除對應 JPEG。

## 授權與修改

- 原創圖示與工程元件以 CC0-1.0 提供。部分主題主圖形保留 Tabler 的 MIT 與 Material Design Icons 的 Apache-2.0 授權；完整授權文字位於 `public/academy/assets/icons-v16/LICENSES.md`。主圖形來源逐一記錄於 `icon-manifest-v16.json`，不能將第三方圖形改稱為 CC0。
- 每張照片依其個別授權使用；作者、授權連結、來源、縮圖／JPEG 重壓縮說明均在 `photos.json`。完整署名表位於 `public/academy/assets/photos-v16/ATTRIBUTION.md`。CC BY-SA 照片的本地重壓縮版本仍依原照片的相同授權提供。獨立的介面模型與可點選提示不宣稱是原照片內容。
- 新照片已檢查 Commons 檔案說明與 API 授權欄位，並逐張查看交付的影像。繼承照片保留 V15 的原作者及授權資料；本版新增其本地檔案完整性與尺寸檢查。這不代表重新確認了所有舊照片來源在今天的權利狀態。

## 視覺檢查紀錄

2026-10-23：以 CairoSVG 實際渲染全部 20 個分類及 27 個代表專題，共 47 個圖示，檢查構圖、彩色筆畫、文字及元件是否可見；並檢視全部 11 張新增照片。Python、CairoSVG 與 Pillow 僅供開發驗證，沒有加入網頁的必要執行依賴。

## English scope note

Every catalog topic has an SVG path. All 1,003 guided/railway topics and all 20 categories have distinct geometry independent of color, text, IDs and drawing order. Some unexpanded backlog topics share compositions. Licensed real photographs are bundled and mapped to all topics; most are explicitly labeled representative references. They are not unique photos of every lesson, live imagery, or evidence of a site-calibrated digital twin. Preserve each photograph's attribution and license, and retain MIT/Apache notices for the corresponding source glyphs.
