# V10 廠商資訊與行情資料

「從課程走進產業」把工法、供應鏈角色與公開廠商資訊連起來。每張卡片說明其業务及與課程的關聯，提供官方產品／技術頁與投資人連結；不因廠商與某領域有關就宣稱其提供課程所有製程，也不表示廠商背書本平台。

## 資料與檔案位置

| 檔案 | 用途 |
|---|---|
| `public/academy/data/vendors.json` | 可公開的廠商名稱、業務介紹、課程關聯、來源及審閱日期 |
| `tools/electronics-v10/build_vendors.py` | 廠商及課程關聯的建置原稿 |
| `public/academy/vendors.js` / `vendors.css` | 廠商卡片、點擊查詢、行情格式與來源顯示 |
| `lib/market-issuers.json` | 允許查詢的公司 ID、股票代號、交易所、幣別與投資人網址 |
| `lib/market-core.mjs` / `app/api/markets/route.ts` | Sites 的固定來源行情介接 |
| `portable/markets.py` / `portable/server.py` | Python 版同一入口的行情介接 |

關聯數會隨課程建置更新，請從實際資料及 `release.json` 核對，不把每個公司／課程關聯計為一家新公司。只有在允許清單列出的上市公司才會出現可用查詢；沒有上市代號的公司仍可提供業務及官方網站。

## 台股是每日盤後資料

本版直接查詢臺灣證券交易所 OpenAPI：

- 固定資料端點：[STOCK_DAY_ALL](https://openapi.twse.com.tw/v1/exchangeReport/STOCK_DAY_ALL)
- 官方 API 目錄：[TWSE OpenAPI](https://openapi.twse.com.tw/)
- 政府資料集說明：[上市個股日成交資訊，資料集 11549](https://data.gov.tw/dataset/11549)
- 授權說明：[政府資料開放授權條款](https://data.gov.tw/license)

使用資料中的 `Code`、`Date`、`ClosingPrice`、`Change`，比對股票身份與有效交易日期；空白或非數字價格不當作零。漲跌百分比以「漲跌金額 ÷（收盤價 − 漲跌金額）」計算；缺乏可計算欄位時保留空值。這是日資料，不是逐筆成交串流；假日或尚未更新時，交易日期可能早於今日。

台股共用一次資料抓取，伺服器最多快取 15 分鐘。畫面區分資料所屬交易日期 `asOf` 與取得時間 `retrievedAt`，按刷新並不會產生盤中價格。`isRealtime` 固定為 `false`；不把「剛抓到」表述為「剛成交」。本次開發實際讀取官方端點並驗證欄位，這不保證官方服務永不中斷。

此公開 API 不需私人 key。使用來源及授權連結應保留；官方授權範圍及條件以提供者當時公告為準。

## 海外行情預設不啟用

海外卡片使用 Twelve Data 的伺服器 `/quote` 介接，股票與交易所只能來自固定允許清單。價格、貨幣、代號、交易所與時間戳必須可驗證；供應者回傳錯誤、身份不符或價格不存在時，不顯示猜測值。

需要業主自行取得**允許你的網站對外展示**的資料方案。一般 API 存取權不等於可以在付費或公開網站展示、再散布；不同交易所、市場、即時／延遲資料可能有額外授權或費用。Twelve Data 的免費層不可直接被當作商業展示許可。請先核對你的訂閱、交易所條件及必要附加授權，再設定：

```dotenv
# 僅放私有後端環境；不要放 config.js、HTML、vendors.json 或公開 Git。
MARKET_DATA_API_KEY=你的私人金鑰
MARKET_DATA_LICENSE_ACK=true
```

`MARKET_DATA_LICENSE_ACK=true` 只是業主對已取得授權的明確設定，不會購買方案、付款或替你創造法律上的資料權利。

Python 版將以上設定放在專案根目錄私有 `.env` 或服務環境，重新啟動你的 Python 網站。Sites／Worker 部署需由擁有者在其部署環境設定伺服器秘密；本次沒有替你建立供應商帳號、加入金鑰或開通海外行情。純 GitHub Pages／雙擊 HTML 無法保守 API 秘密，須連接自行部署、具合適權限與來源限制的後端；前端未發現可用行情 API 時會保留官方連結。

海外成功回覆最多快取 60 秒，不表示其上游延遲只有 60 秒。頁面仍使用 `isRealtime:false`，並顯示來源時間；實際頻率取決於你有權使用的資料來源。不可用時回 `unconfigured` 或 `unavailable`，不以隨機數或過期示例價格補上。

官方文件（本次查閱：2026-10-14）：

- [Twelve Data 使用條款](https://twelvedata.com/terms)：訂閱用途、展示／再散布、第三方及交易所資料條件。
- [Twelve Data 方案](https://twelvedata.com/pricing)：依實際網站用途選方案，不能只看 API 次數。
- [Twelve Data API 文件](https://twelvedata.com/docs)：報價欄位、時間與市場支援。

## API 與失敗處理

```http
GET /api/markets?vendor=tsmc
```

`vendor` 是廠商允許清單的 ID，不是任意股票搜尋，也不能傳外部 URL。此讀取功能不需要學員付款或送出券商帳戶，不提供交易下單。

| 回覆欄位 | 意義 |
|---|---|
| `status` | `ok`、`unconfigured` 或 `unavailable`；未知公司為 HTTP 400 |
| `symbol` / `exchange` / `currency` | 實際核對的商品身份與計價幣別 |
| `price` / `change` / `changePercent` | 有效價格與漲跌；無可計算值時為空，不編造 |
| `asOf` | 交易日期或供應商回報的時間戳 |
| `timeZone` | 市場時區／時間標示 |
| `retrievedAt` | 伺服器取得來源資料的時間 |
| `frequency` | `end-of-day` 或 `provider-feed` |
| `source` / `sourceUrl` | 資料來源及連結；台股另有 `licenseUrl` |
| `isRealtime` | 本版固定 `false`，不宣稱即時串流 |
| `cached` | 成功快取回覆時標示；首次回覆可省略或為 false |

程式只連固定官方端點，限制逾時、回應大小並拒絕重新導向。錯誤回覆不回傳供應者原始錯誤、帶 API key 的 URL 或私人金鑰。身份錯配、無效日期、`NaN`、超大回覆及不明公司不回價格。端點並不容許使用者把它當任意 URL 代理。

## 維護及驗證

新增廠商先核對其官方業務和課程適用範圍，再更新建置原稿與 `market-issuers.json`；市場代號、交易所與幣別必須一致。不得只改前端股票名稱而保留另一公司的代號。課程關聯需有可解釋的技術理由，更新審閱日期；停牌、退市、改名、合併與 API 方案改變都可能需要維護。

`node tools/test-market-data-v10.mjs` 使用資料樣本和 mock 網路，檢查身份／交易所／幣別、曆日、漲跌計算、缺值、快取、授權閘門、固定來源、私密錯誤清理與 HTML 轉義；Python 路由在 `tests/test_commerce.py` 另以 stub 檢查。正式海外方案仍需業主的授權與憑證驗收，並未宣稱以你的付費資料帳號實測。

本區用於理解產業和資料來源，不以課程學習進度、AI 推薦或單日漲跌推導個人投資報酬；並未連接券商或執行任何買賣。
