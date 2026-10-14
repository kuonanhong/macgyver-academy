# V11 資訊與資安原創架構與本機算例

本模組對應課程地圖原有的「資訊與資安」100 個主題：`cybersecurity` 與 `a302`–`a400`。圖稿由教材作者以 SVG 程式繪製；沒有追描廠商架構圖、採用廠商商標，或將原始碼圖示當作真實設備照片。

## 交付與閱讀方式

- 100 組雙語課程架構（200 個 SVG 檔案），位於 `public/academy/assets/diagrams/computing-v11/`。
- 100 個課程專用組合圖示，位於 `public/academy/assets/icons/computing-v11/`。
- 100 個無文字時仍可區別的架構圖；100 個去除文字、標籤屬性後仍可區別的組合圖示。
- 225 個元件語義名稱，依功能共用適當的原創符號。這不表示 225 個廠商設備或實際硬體 CAD。
- 16 種可調參數的算例，對應 90 門適合用算例討論的課程；另外 10 門不硬套不相干數學模型。

資料流、控制流與信任關係以箭頭及界面區域表現。圖的拓樸依課題區別，涵蓋 CPU 管線、快取一致性、GPU 分派、張量乘加、容器控制平面、Raft 多數、副本抹除碼、零信任、PKI、海纜、DNS 階層、分散式訓練與科學 HPC。圖是功能關聯概念，並非可直接投產的設計。

英文字元與繁體中文使用系統字型。SVG 可縮放，所有圖片含 `title`、`desc` 與 `aria-label`；不能將顏色單獨作為判讀依據。四個節點可隨目前步驟突出顯示，但突出位置是導覽重點，不是量測結果。

## 模組介面

`public/academy/computing-visuals.js`：

```js
COMPUTING_SUBJECTS
computingGlyph(kind)
computingGeometry(courseId, { zh: true, labels: true, focus: -1 })
computingVisualFamily(courseId)
renderComputingVisual(courseId, { zh: true, mode: 'full', focus: -1 })
renderComputingIcon(courseId, { en: false })
searchComputingSubjects(query, { limit: 100, zh: true })
COMPUTING_LABS
COMPUTING_COURSE_LABS
computingLabKind(course, step)
calculateComputingLab(kind, values)
computingLabDetail(kind, values, zh)
```

圖稿 `viewBox` 為 `600 370`，與既有電機課程功能圖相同。計算模型資料結構與 `engineering-labs.js` 既有介面一致，含 `title`、`formula`、`unit`、`params`、`note`、`question`、`source`。`calculateComputingLab` 對未知模型回傳 `null`；對缺值、非數值、無窮大或超界輸入回傳 `NaN`。離散參數在計算前就近取整，連續趨勢圖也可以繪製門檻變化。

## 算例及邊界

| 算例 | 產生的數量 | 主要限制 |
|---|---|---|
| 分支失誤 CPI | cycles/instruction | 固定指令組合、未模擬亂序重疊 |
| 快取 AMAT | ns | 單層阻塞快取、額外 miss penalty |
| GPU Roofline | TFLOP/s 上界 | 同一精度、相同記憶體層，並非跑分 |
| 稠密矩陣乘法 | GFLOP 工作量 | 一乘加計兩運算，並非執行時間 |
| Raft 多數門檻 | 投票節點 | 固定成員、非拜占庭，不是 MPC 容錯門檻 |
| 理想抹除碼 | 容量倍數 | 等長 MDS 片段，不含修復與共同失效 |
| 30 日錯誤預算 | 分鐘 | 時間型 SLI，不等同請求成功率 |
| 合成 M/M/1 p99 | ms | Poisson 到達、獨立指數服務、單伺服器 |
| ML-KEM-768 payload | ms 序列傳輸尺度 | 1184-byte 公鑰與 1088-byte 密文，非完整 TLS |
| 單筆 DNS 更新率 | queries/min | 自訂 Poisson 更新模型，非 RFC 流量公式 |
| 警報基率效應 | precision % | 合成固定標籤，並非產品偵測率 |
| Laplace 噪音尺度 | query units | 不抽樣、不讀個資；須核定敏感度及組合 |
| LLM KV 容量 | GiB | 使用 KV 頭數，不含權重、碎片與啟用值 |
| Amdahl 強擴展 | 加速倍數上界 | 固定問題大小，無通訊負擔 |
| payload 序列化 | µs | 無傳播、佇列、重傳或 headers |
| 獨立副本可用性 | % | 任一可服務且完全獨立，非 SLA |

所有輸入均為教學假設。本模組沒有 `fetch`、WebSocket、網路掃描、攻擊測試、shell 指令、外部流量、真正控制硬體或真實個資處理。老師與學徒的組合工作台仍是既有教學任務；架構圖與算例不能稱為真實伺服器的已校準數位分身。

## 主要公式核對來源

以下使用一次資料與官方文件核對，內容為原創解釋，沒有轉貼教材篇章或廠商圖：

- Cornell CS3410 Caches（AMAT）：https://www.cs.cornell.edu/courses/cs3410/2026sp/notes/caches.html
- NERSC Roofline： https://docs.nersc.gov/tools/performance/roofline/
- NVIDIA Matrix Multiplication Background（2MNK）：https://docs.nvidia.com/deeplearning/performance/dl-performance-matrix-multiplication/index.html
- Ongaro 與 Ousterhout，Raft 原論文（固定成員多數）：https://raft.github.io/raft.pdf
- NIST FIPS 203（ML-KEM 格式）：https://csrc.nist.gov/pubs/fips/203/final
- RFC 1035（DNS TTL；更新率模型由本教材另行建立）：https://www.rfc-editor.org/rfc/rfc1035.html
- Dwork 與 Roth，The Algorithmic Foundations of Differential Privacy（Laplace）：https://www.cis.upenn.edu/~aaroth/Papers/privacybook.pdf
- NVIDIA LLM Inference Optimization（KV 容量）：https://developer.nvidia.com/blog/mastering-llm-techniques-inference-optimization/
- LLNL Introduction to Parallel Computing（Amdahl）：https://hpc.llnl.gov/documentation/tutorials/introduction-parallel-computing-tutorial
- AWS Availability Zone Independence（共同失效需要另外評估）：https://docs.aws.amazon.com/whitepapers/latest/advanced-multi-az-resilience-patterns/availability-zone-independence.html

其餘工作量、單位換算、Bayes 基率、容量與理想概率式屬本教材明確列出的數學假設；不宣稱對具名設備的現行性能提供保證。

## 重建及驗證

```bash
node tools/build-computing-visuals-v11.mjs
node tools/build-computing-visuals-v11.mjs --check
node tools/test-computing-v11-visuals.mjs
```

JavaScript 模組本身是版本控制中的原始教材；建置程式讀取模組，僅重建兩個本模組素材目錄，不會覆寫模型參數。`--check` 會逐檔比對原始模組渲染結果並拒絕過期素材，不寫入檔案。結果是確定性的。`manifest.json` 列出課題映射與每個 SVG 的 SHA-256、位元組數，供完整性檢查。

測試涵蓋 100 個既有課程 ID、雙語名稱、元件覆蓋、300 個 XML 圖檔、幾何與圖示區別、搜尋與非法字元、16 組獨立數值算例、各參數上下界及超界拒絕、素材雜湊一致性。這些是程式與靜態圖稿檢查，沒有完成真實瀏覽器與每種手機/桌機裝置操作驗收。

本組原創 SVG 採 CC BY 4.0，署名 `MacGyver Engineering Academy`。課程引用來源維持其原授權；引用文獻連結不表示可重製來源整篇文章或影片。
