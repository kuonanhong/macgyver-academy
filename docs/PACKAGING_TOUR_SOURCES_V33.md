# 先進半導體封裝俯瞰導覽：內容與資料依據

編寫及查核日期：2026-11-23。內容檔：`public/academy/packaging-tour-content-v33.js`。

這是原創工程解說與教學重建，不是廠房空拍、企業提供的產品動畫、量產製程規格或實測模擬。晶粒、封裝厚度、接點、光流、熱區與變形按可理解性調整；不應從畫面推算尺寸、速度、溫度、良率或壽命。商標只用於指出公開參考技術，不表示廠商背書。

## 導覽規格

六項各 300 秒，每項十段連續的 30 秒章節，共 30 分鐘。每段具獨立學習重點、鏡頭閱讀提示與五語完整文字：繁體中文、英文、日文、韓文、簡體中文，共 300 段在地化解說；不是以英文回退冒充完整譯文。語音若啟用，實際可用聲音與讀速依使用者裝置；五分鐘是視覺導覽時間，並非承諾每語語音不間斷朗讀五分鐘。

| 內容 ID | 主題 | 十段教學進程 |
| --- | --- | --- |
| interposer | 2.5D 矽中介層與 HBM | 整體配置、三層角色、並行互連、組裝風險、垂直連接、頻寬與能量、熱路徑、檢查證據、整合取捨、完整路線 |
| fanout | 扇出封裝與 RDL | 晶粒外連接、材料、RDL、晶粒先行與 RDL 先行、分層、回流路徑、翹曲、對位、成本與複雜度、設計流程 |
| hybrid | 3D 堆疊與混合鍵合 | 立體整合、分層功能、金屬與介電接合、表面與對位、完整訊號鏈、架構價值、熱路徑、測試存取、良率與返修、系統路線 |
| bridge | 局部矽橋 | 局部連接、與全面中介層比較、晶粒岸線、基板整合、不同路徑、實體與協定、熱機械、三種驗證、整體成本、需求到設計 |
| chiplet | Chiplet 與 UCIe | 功能分割、製程分工、介面標準、協同設計、物理與協定、通訊成本、熱與負載、相容驗證、重用取捨、系統重組 |
| thermal | 散熱、測試與可靠度 | 任務需求、熱源、界面熱阻、裝配品質、分流熱路徑、不同測試、循環應力、多證據、比較基準、驗證回饋 |

鏡頭語意固定依序為 `overview`, `architecture`, `interconnect`, `assembly`, `cross-section`, `signal`, `thermal`, `inspection`, `tradeoff`, `roadmap`。`cross-section` 是程式的階段名稱，視覺以分層與半透明材料解釋內部關係；不是以真正切割的幾何宣稱量測剖面。

## 官方技術來源

- [TSMC：CoWoS](https://3dfabric.tsmc.com/english/dedicatedFoundry/technology/cowos.htm)：核對邏輯與 HBM 整合，以及 CoWoS-S、R、L 的互連材料／架構差別。導覽第一項只用矽中介層作通用概念，不將所有 CoWoS 變體等同一片矽。
- [TSMC：Integrated Fan-Out](https://3dfabric.tsmc.com/english/dedicatedFoundry/technology/InFO.htm)：核對 InFO、RDL 與多種整合選項；不把 InFO 等同所有扇出封裝。
- [TSMC：SoIC](https://3dfabric.tsmc.com/english/dedicatedFoundry/technology/SoIC.htm)：核對 3D 堆疊的整合定位；不採用官網產品節點、接點尺寸、量產年份作動畫規格。
- [Intel Foundry：Advanced Packaging](https://www.intel.com/content/www/us/en/foundry/packaging.html)：核對嵌入基板的局部矽橋，以及 Foveros Direct 的混合鍵合。EMIB、EMIB-T 等變體不可共用一張簡圖推論供電路徑；導覽已保留此區別。
- [ASE：Fan-Out Packaging](https://ase.aseglobal.com/fan-out-packaging/)：核對 chip-first 與 RDL-first／chip-last 的流程差別與製程挑戰。未提供材料配方、操作溫度或宣稱任一方式無缺陷。
- [UCIe Consortium：Specifications](https://www.uciexpress.org/specifications)：核對 UCIe 是封裝內晶粒互連規格，區分物理介面、協定與互通驗證。內容避免鎖定規格版本或最新速度數字，並未宣稱符合標準等於任意晶粒可直接互換。
- [ASE：Stress and Thermal Lab](https://ase.aseglobal.com/lab-services/stress-and-thermal-lab/)：核對熱、機械、材料、模型與量測需一併考量的工程範疇。導覽熱區是概念提示，沒有標示假造的測量溫度。
- [ASE：Test Services](https://ase.aseglobal.com/test-services/)：核對元件／晶圓、封裝電性與系統級測試的分層範疇，以及可靠度與失效分析的不同任務。

上述連結是技術名詞與架構核對來源。鏡頭、街區比喻、閱讀提示、比較問題與教學路線為本專案原創編排；沒有擷取廠商影片、照片或長篇文章。工程推理，例如固定條件再比較、區分相關與根因、記錄量測不確定性，屬教學方法而不是特定產品宣稱。

## 內容檢查

- 六項導覽、六十個章節、五語標題／摘要／解說皆存在且非空。
- 每項第一段從 0 秒開始，十段無缺口／重疊地覆蓋至 300 秒。
- 每項有官方來源連結；品牌名稱與教學重建的界線在文字中說明。
- 所有五語文字為完整提供的初稿，未宣稱經過母語工程師或原廠審核。
- 用於影像呈現的宣稱要與實作一致；幾何、字幕、操作與匯出由主實作流程另外驗證。
