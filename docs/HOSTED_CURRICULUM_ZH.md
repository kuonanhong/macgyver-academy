# 課程分段與網站建構

`public/academy/data/featured.json` 是完整、按順序排列的課程原始資料，供編輯工具、Python 後端、測試和完整下載包使用。不要手動刪除它，也不要直接編輯生成的分段檔。

執行 `bash build-offline.sh` 時，`tools/build-offline.mjs` 同時產生兩套等價資料：

- 離線用 `offline-data-XX.js`：由一般 script 標籤依序載入，直接開啟 `index.html` 不需 fetch 或本地伺服器。
- 網站用 `data/course-parts/index.json` 與 `part-0001-<內容雜湊>.json`：各部分不超過 7 MiB；清單列出順序、課程 ID、位元組數及 SHA-256。

網站的 `curriculum-loader.js` 先檢查已載入的 `MG_DATA`；HTTP(S) 模式則取得不使用舊快取的清單，最多同時載入兩個部分，再依原始順序合併。它拒絕不安全的路徑、重複 ID、缺少檔案、錯誤順序、數量不符及超過大小限制的內容。HTTPS／localhost 可用 Web Crypto 時，亦核對完整 SHA-256；一般 HTTP 仍核對大小、數量、ID 和檔名內容雜湊格式。

目前仍在啟動時載入全部逐步課程，分段解決的是單檔大小與並行載入的限制，並不是逐課按需載入。清單總資料上限為 256 MiB；若未來達到此界限，需先改成逐課載入，再提高課程總量。

`pnpm build` 經由 `tools/build-hosted.mjs` 執行：

1. 必要時重新生成離線 bundle 和兩套分段資料。
2. 呼叫原有 `scripts/run-framework.mjs build`，原樣傳遞額外建構參數。
3. 執行 `tools/prepare-hosted-curriculum.mjs`，逐一比對建構後分段與完整來源，確認內容、順序和雜湊。
4. 只移除 `dist/client/academy/data/featured.json` 的部署副本，保留來源及下載包中的完整 JSON；檢查其餘所有部署資產不超過 25 MiB。

Sites 的標準 build helper 呼叫相同的 package build 指令，無需修改 Sites 插件。直接執行低階 `vinext build` 而略過 wrapper 時，請在部署前另執行 `node tools/prepare-hosted-curriculum.mjs`。

驗證指令：

```bash
node tools/build-offline.mjs --check
node tools/test-curriculum-loader.mjs
node tools/test-offline.mjs
```

測試包含網站／離線資料一致性、載入失敗與毀損檢查、並行數限制、部署資料驗證、保留原始 JSON，以及建構參數傳遞和失敗時停止。這些是程式／資料測試，不等同實機瀏覽器和手機測試。
