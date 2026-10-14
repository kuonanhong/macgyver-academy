# V8 半導體圖像與影音核對紀錄

核對日期：2026-10-14。以下為素材使用記錄，不是原廠認證。

## 原創結構圖

`public/academy/semiconductor-visuals.js` 涵蓋半導體分類的 99 個穩定課程 ID（semiconductor、sub2nm、a003–a099）。共 36 個幾何家族，含 FinFET、CFET、反射式 EUV、MEMS 膜片及不同記憶體的子型變化。每圖含繁中／英文標籤、無障礙名稱及非比例概念圖說明。它們是理解架構的原創概念圖，不是 99 套獨立的 CAD 模型、OEM 機台圖或可製造設計。

## 新增真實照片與量測影像

24 個不同來源檔，合計 3,918,710 bytes，全部隨套件提供。每項保留作者、授權、來源、變更說明、課程對應與 SHA-256。顯微影像與 STM／螢光量測有各自限制；不宣稱每道工序有專屬現場實拍。

既有素材加上新增素材，99 門半導體課程均有明確對應的**背景／代表照片或量測影像**。這不表示有 99 個不同實拍，更不表示各步驟均有照片。新增素材本身對應 98 門；既有照片補上 sub2nm。補齊的 29 門課程在 `courseContext[courseId]` 保存繁中與英文說明，介面會優先顯示：例如 CFET 配圖明確稱為晶圓尺度背景、High-NA EUV 的塗佈顯影機明確稱為周邊製程、MRAM 配圖明確說明是金濺鍍而非磁性薄膜。這些實拍用於尺度或共用製程的比較，細部元件結構則由原創概念圖及來源說明補充。

| 素材 | 作者／授權 | 來源 |
|---|---|---|
| 12 吋矽晶圓表面 | 2x910 / CC BY-SA 4.0 | [v8-wafer](https://commons.wikimedia.org/wiki/File:Si_wafer.jpg) |
| UC Davis 奈微製造無塵室 | Lucy Knowles / UC Davis College of Engineering / CC BY 2.0 | [v8-cleanroom](https://commons.wikimedia.org/wiki/File:UC_Davis_Cleanroom_(45490130562).jpg) |
| Los Alamos 原子層沉積設備 | Center for Integrated Nanotechnologies - Los Alamos National Laboratory / Public domain | [v8-ald](https://commons.wikimedia.org/wiki/File:Aomic-layer-deposition-system.jpg) |
| Alabama Huntsville 反應式離子蝕刻設備 | AlabamaUSA / CC BY-SA 3.0 | [v8-rie](https://commons.wikimedia.org/wiki/File:Reactive_Ion_Etcher.JPG) |
| DRIE 鈍化不足與蝕刻失敗顯微影像 | Mgerlt / CC BY 4.0 | [v8-drie-failure](https://commons.wikimedia.org/wiki/File:DRIE_etch_fail.jpg) |
| 不同開口深寬比的矽蝕刻深度 | Mgerlt / CC BY-SA 4.0 | [v8-etch-depth](https://commons.wikimedia.org/wiki/File:Etch_depth.jpg) |
| 深蝕刻微柱與側壁波紋 | Mgerlt / CC BY 4.0 | [v8-micro-pillars](https://commons.wikimedia.org/wiki/File:Micro-Pillar.jpg) |
| 矽深蝕刻後懸出的銅互連 | Dave Kopp / Public domain | [v8-copper-undercut](https://commons.wikimedia.org/wiki/File:QP_2.jpg) |
| 金濺鍍腔中的電漿輝光 | GcG(jawp) / Public domain | [v8-sputter-plasma](https://commons.wikimedia.org/wiki/File:Au_sputtering_light.JPG) |
| 薄膜橢圓偏光量測設備 | AlabamaUSA / CC BY-SA 3.0 | [v8-ellipsometer](https://commons.wikimedia.org/wiki/File:Ellipsometer.JPG) |
| 晶圓測試探針卡 | Ajoones / CC BY 3.0 | [v8-probe-card](https://commons.wikimedia.org/wiki/File:Probe_card.JPG) |
| 移除測試頭後的晶圓探測機 | Ixnayonthetimmay / CC BY-SA 3.0 | [v8-wafer-prober](https://commons.wikimedia.org/wiki/File:Wafer_prober_service_configuration.jpg) |
| LAAS-CNRS 離子佈植機前端 | Guillaume Paumier (user:guillom) / CC BY-SA 3.0 | [v8-implant](https://commons.wikimedia.org/wiki/File:Ion_implantation_machine_at_LAAS_0521.jpg) |
| 4 吋旋轉塗佈設備 | Junny97008 / CC BY-SA 4.0 | [v8-spin-coater](https://commons.wikimedia.org/wiki/File:Spin_Coater.jpg) |
| LAAS-CNRS 擴散與熱氧化爐 | Guillaume Paumier (user:guillom) / CC BY-SA 3.0 | [v8-furnace](https://commons.wikimedia.org/wiki/File:Centrotherm_diffusion_furnace_at_LAAS_0493.jpg) |
| CMOS 影像感測器晶片尺寸封裝 | Phiarc / CC BY-SA 4.0 | [v8-cmos-sensor](https://commons.wikimedia.org/wiki/File:CMOS_image_sensor_chip-scale_package_top.jpg) |
| LAAS-CNRS 光阻塗佈顯影設備 | Guillaume Paumier (user:guillom) / CC BY-SA 3.0 | [v8-resist-track](https://commons.wikimedia.org/wiki/File:EVG_120_resist_coater-developer_at_LAAS_0434.jpg) |
| 兩片六吋碳化矽晶圓 | FDominec / CC BY-SA 4.0 | [v8-sic-wafers](https://commons.wikimedia.org/wiki/File:SiC_wafers_6inch.jpg) |
| LAAS-CNRS 光罩對準曝光設備 | Guillaume Paumier (user:guillom) / CC BY-SA 3.0 | [v8-mask-aligner](https://commons.wikimedia.org/wiki/File:MA-6_%26_MJB-3_steppers_at_LAAS_0455.jpg) |
| Sandia 分子束磊晶研究設備 | ENERGY.GOV / Public domain | [v8-mbe](https://commons.wikimedia.org/wiki/File:Molecular_beam_epitaxy_system.jpg) |
| HBM DRAM 晶粒顯微照片 | FritzchensFritz / CC0 | [v8-hbm-die](https://commons.wikimedia.org/wiki/File:AMD@14nm@GCN_5th_gen@Vega10@Radeon_RX_Vega_64@HBM_DRAM_Die@_Stack-DSC08838-DSC08973_-_ZS-retouched.jpg) |
| SiC 上磊晶石墨烯的 STM 缺陷影像 | Nathan Guisinger, EMMD Group, Argonne National Laboratory / CC BY-SA 2.0 | [v8-graphene-stm](https://commons.wikimedia.org/wiki/File:Graphene-epitaxial.jpg) |
| NIST 微機電致動器與螢光定位 | National Institute of Standards and Technology / Public domain | [v8-mems-actuator](https://commons.wikimedia.org/wiki/File:Scratch_Drive_Actuator_(8097296709).jpg) |
| 靜電微夾具夾持矽奈米線的 SEM 影像 | Kristian Mølhave (SEM image); Erik Bakkers (nanowire sample) / CC BY 2.5 | [v8-microgripper](https://commons.wikimedia.org/wiki/File:Microgripper_holding_silicon_nanowires.jpg) |

## 授權判讀

- `Graphene-epitaxial.jpg` 的來源頁同時有不一致的 public domain 摘要及明確 CC BY-SA 2.0 與 Flickr 授權複核；本站採較明確的 **CC BY-SA 2.0**，不援引模糊的 public-domain 描述。
- `Microgripper holding silicon nanowires.jpg` 的 API author 欄空白，依完整來源頁補上 Kristian Mølhave、Erik Bakkers，並致謝 Opensource Handbook of Nanoscience and Nanotechnology。
- UC Davis 圖像補上來源說明中的攝影者 Lucy Knowles。
- 曾檢查 NIST 的 Scanning Electron Microscope with Spin Polarization Analysis 照片；頁面內另有第三方攝影著作權及用途限制，與公共領域標籤衝突，因此**未收入**。
- CC BY-SA 照片仍適用其原授權；專案程式碼的授權不會取代第三方照片授權。

## 新增官方影片

6 個不同官方影片 ID，配置到適合的課程並附觀看前、觀看中與觀看後的教學問題。此數字不把同片在不同課程的引用重複計算。

- [ASML 光學元件製造：加工、拋光與對準](https://www.youtube.com/watch?v=_5TSeXkX5Js) — ASML；[原始來源](https://www.youtube.com/watch?v=_5TSeXkX5Js)。
- [High-NA EUV 晶圓平台：上片、對準、整平與掃描](https://www.youtube.com/watch?v=v9Pg92cdJa4) — ASML；[原始來源](https://www.youtube.com/watch?v=v9Pg92cdJa4)。
- [ASML High-NA EUV：系統導入、驗證與協作](https://www.youtube.com/watch?v=UAWu1O1UuQc) — ASML；[原始來源](https://www.youtube.com/watch?v=UAWu1O1UuQc)。
- [從平面到 FinFET、GAA 與 CFET：電晶體架構演進](https://www.youtube.com/watch?v=ST_1krgYni4) — Lam Research；[原始來源](https://newsroom.lamresearch.com/gate-all-around-and-logic-scaling)。
- [Micron Idaho 無塵室建置與潔淨度準備](https://www.youtube.com/watch?v=l6o7VH8lJk4) — Micron Technology；[原始來源](https://www.micron.com/us-expansion/id)。
- [Micron 1α DRAM 製程的跨領域整合](https://www.youtube.com/watch?v=GlwtS_Vq9aE) — Micron Technology；[原始來源](https://in.micron.com/about/blog/memory/dram/inside-1a-the-worlds-most-advanced-dram-process-technology)。

YouTube oEmbed 已返回對應標題與官方頻道（ASML、Lam Research、Micron Technology）。這只驗證公開影片中介資料與嵌入程式可取得，**未完成各地區、瀏覽器與未登入狀態的實際播放測試**。影片不下載、不重託管，不繞過 YouTube 的登入／年齡／地區限制。外部影片應由使用者點擊後才載入。新增 ID 必須同步到既有公開播放器白名單；主站帳號／權限不應為此改成公開。

## 驗證

`node tools/test-semiconductor-visuals.mjs` 檢查 99 ID 覆蓋、36 家族、47 種英文幾何／標註結果、396 份雙語與兩種顯示模式 SVG 的 XML、安全輸出、24 照片檔案與 SHA-256、99 門課程的背景照片實際呈現、6 個影片中介資料及課程對應。`node tools/test-learning-media.mjs` 另驗證兩種本地照片路徑、拒絕外部追蹤與目錄跳脫、雙語課程情境圖說及既有影片行為。
另以 Inkscape 查看所有幾何家族及 24 照片聯絡表；此環境缺少繁中系統字型，因此圖形版面以英文檢查，繁中採字串與 XML 驗證。未宣稱實機瀏覽器 QA。
