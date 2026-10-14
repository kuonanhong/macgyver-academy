# V10 會員、金流、課程門禁與證書

本版交付可設定的金流與課程權限程式；目前沒有建立你的綠界商家帳戶、輸入正式金鑰、開通收款或刷任何信用卡。Sites 網站保持完整的擁有者／示範版本，`/api/billing/config` 明確回報金流 disabled。正式商業站需另行部署下述 HTTPS Python 伺服器。

## 一、使用者怎麼付款？錢怎麼到你的帳戶？

1. 學員在網站註冊並登入，選擇一次性 30 天或 365 天方案，閱讀並同意你正式公布的條款。
2. 你的伺服器建立新台幣訂單；金額、方案期限都由伺服器決定，不能由瀏覽器自行傳入價格。
3. 瀏覽器以 HTML form POST 整頁前往綠界 HTTPS 收銀台。**卡號、到期日、安全碼只在綠界頁面輸入；本站不需要也不應自行收集它們。** 不以 iframe 包住付款頁。
4. 綠界進行信用卡授權／銀行驗證，再向公開 HTTPS webhook 通知結果。伺服器驗證 SHA-256 CheckMacValue、特店、訂單、金額、付款方式、交易編號；成功交易再呼叫綠界查單 API 確認一致，才在同一筆資料庫交易內建立權限。瀏覽器「返回網站」並不解鎖課程。
5. 金額由綠界依你的實際合約結算，扣除相關費用後進入你的綠界帳戶，再提領到你已驗證的銀行帳戶。銀行帳戶不是填在本站 JavaScript 中；是在綠界申請、審核及綁定。撥款日依會員類型、合約及風險審核而定，不保證固定天數。

依本次查閱的綠界一般賣家官方費率，國內信用卡 2.75% 未稅、每筆最低 NT$5，服務費另加 5% 營業稅，信用卡另有每筆 NT$1 訂單處理費。若交易額 NT$299，僅估算這些金流費約 NT$9.63；NT$2,490 約 NT$72.90。這不是最終營業利潤，也未扣你的其他稅務、主機、AI、客服或退款成本；每日結算可能有彙總四捨五入。特約、海外卡及其他支付方式費率不同，以核定合約為準。[1][2]

## 二、建議先測試的價格

| 方案 | 本版設定 | 用意 |
|---|---:|---|
| 免費試學 | 6 門完整課程 | 無需信用卡即可評估教學與操作 |
| 全學院 30 天 | NT$299，單次購買 | 降低首次嘗試門檻，沒有自動續扣 |
| 全學院 365 天 | NT$2,490，單次購買 | 適合長期跨領域學習 |

免費 ID：`semiconductor`、`packaging`、`a201`、`a242`、`a271`、`a281`。若要調整，需同步更新 `portable/commerce.py`、Sites 的 `app/api/billing/config/route.ts` 與前端示範設定。方案 `all-30`、`all-365` 的天數是固定 30 / 365 天，不是按曆月計算；再次購買會接在既有有效期限之後。尚未實作自動續訂、分期、折扣碼或企業席位購買。

上述是**可測試的起始假設**，沒有證據能保證「最多人付費」。建議先招募約 30–50 名自願試用者，觀察免費第一課完成率、7 天回訪、首次付款轉換、退款與客服時間；再做透明且一致的 NT$199／299／399 價格期間實驗。不要只以註冊數評估：要同時追蹤每名活躍學員的 AI 成本、真正完成的課程數與留存。

本次官方 Coursera Plus 頁面列出的常規參考價為 US$59／月、US$399／年，另有期間促銷；品牌、學校合作、課程規模與證書認知均不同，不代表本平台可以直接照價或宣稱同等認證。[3] 研究員／教師對算例、來源可追溯性和實作評量的回饋，比先定高價更有價值。

## 三、三種部署的能力差別

| 部署 | 課程取得方式 | 真正付費門禁 | 完成紀錄 |
|---|---|---|---|
| 雙擊 `index.html`、完整 ZIP、GitHub Pages | 完整靜態教材 | 無；下載到用戶端的教材不能靠 JavaScript 鎖住 | 本機學習聲明 |
| 現有 Sites owner/demo 網站 | 完整示範教材 | 本版未啟用金流；維持原分享對象 | 原有進度與本機聲明 |
| `COMMERCE_MODE=protected` Python + 單一 HTTPS 網域 | 伺服器按每次請求的會員權限送課程 | 有；未購回 402，直接教材／離線檔回 403 | 伺服器逐步測驗完成證書與公開驗證 |

**不要把完整 ZIP、public 資料夾或 GitHub 公開原始碼作為付費站的下載附件。** 本次完整原始碼是給你作為擁有者管理、研究與部署；若同時把同一份教材放在公開 Pages，該公開副本自然仍可取得。門禁不能撤回學員先前已合法讀到、下載或截圖的內容，也不是 DRM。

目前 Python 帳號由信箱／密碼建立，密碼為 PBKDF2 雜湊，session 是 HttpOnly cookie。它與 ChatGPT Sites／Supabase 帳號是不同身分系統；不要假稱自動共用。尚未內建寄信驗證與忘記密碼流程，正式營運需先補齊其服務及客服處理方式。本版以單機 SQLite 與標準函式庫 HTTP 伺服器作為可檢查的起點，沒有宣稱通過大規模商業流量或安全稽核。

## 四、正式站安裝順序

1. 準備自己的網域、HTTPS 憑證與可執行 Python 3.10+ 的 Linux 主機；Mac、Windows 可用於本機測試。`pip install python` 不會升級 Python，請用官方安裝器／作業系統套件工具安裝。
2. 解壓縮完整專案。不要用 Nginx `root` / `alias` / `try_files` 或 CDN 對外直接發布 `public/academy`。所有 URL 都需走 Python，範本見 `examples/commerce-nginx.conf`；反向代理只通往 `127.0.0.1:8010`。
3. 將 `examples/commerce.env.example` 的適用設定放入專案根目錄的私有 `.env`。先用 `COMMERCE_MODE=protected`、`BILLING_MODE=disabled`，設定精確 `SITE_ORIGIN=https://你的網域`。資料庫與 `.env` 必須放在靜態根目錄外。Unix 可設 `chmod 600 .env`。
4. 在專案目錄執行 `bash run-commerce.sh --port 8010`。程式只使用 Python 標準函式庫；此指令不會替你申請商家、不會自動裝金流金鑰、不會收費。背景常駐、重啟與備份請交由你主機的服務管理器。
5. 先在**獨立網域、獨立資料庫**使用 `BILLING_MODE=sandbox`。測試 MerchantID / HashKey / HashIV 從綠界官方測試頁取得，不將真實卡片填入沙盒。沙盒 entitlement、測驗紀錄及證書均帶 sandbox；切換 live 不會接受它們。`SimulatePaid=1` 連在沙盒也只是連線測試，不發權限。[4]
6. 核對公開 `https://你的網域/api/billing/ecpay/notify` 可讓綠界從外網 POST，不能要求先登入、不放 Cloudflare Access／Sites owner wall；不得把外網任何路徑直接交給 Python 以外的檔案伺服器。對外用 443；不把 8010 填進綠界 ReturnURL。[4][5]
7. 完成綠界商家申請、審核、銀行綁定、必要發票／稅務安排。修改 `public/academy/commerce-terms.html`：經營者名稱與客服、付款方案、退款條件、資料保留與刪除窗口都要填妥。文件目前清楚標示為尚未完成的範本，不能當作正式審核過的契約。
8. 完成會員資料備份／回復、測試付款／失敗付款／重送通知／到期／退款對帳／權限撤銷測試後，才以正式金鑰設定 `BILLING_MODE=live`、`ECPAY_LIVE_CONFIRMED=1`、`COMMERCE_LEGAL_READY=1`。一般測試特店 ID 會被 live 模式拒絕。**本次沒有代你設定或執行這一步。** 首次正式交易與退款需由你以自己核准的商家環境驗證。

套件有進度匯出及更新上傳腳本；**不要**把會員資料庫、付款資料、金流 `.env` 或備份推到公開 Git。付費資料庫另做加密、存取受控的備份。部署新程式前，停止服務或用 SQLite backup API 做一致備份；不要只拷貝正在寫入的 SQLite 主檔而漏掉 WAL。

## 五、付款狀態與管理

```bash
# 在專案根目錄；預設讀取私有 .env 和 portable/data/macgyver.sqlite3
python3 -m portable.commerce_admin status
python3 -m portable.commerce_admin orders --limit 20

# 只有在確認某訂單通知遺失時手動查綠界；不修改價格、不使用瀏覽器付款旗標
python3 -m portable.commerce_admin reconcile MGXXXXXXXXXXXXXXXXXX

# 先到綠界依退款程序處理並對帳，再撤銷本站權限與相應證書
python3 -m portable.commerce_admin revoke MGXXXXXXXXXXXXXXXXXX --reason '已在綠界核對退款完成'
```

`reconcile` 會呼叫固定綠界 API，驗證回覆簽章與已儲存訂單。付款後暫未查得成功會維持未解鎖；依綠界建議稍後重查，不要高頻輪詢。[6] `revoke` **只撤銷本站權限，不會退錢**；沒有假裝完成銀行退款的按鈕。已退款／撤銷訂單收到舊通知也不會重新發權限。續購期限獨立按訂單記錄；若退掉前一段但希望後一段提前，需要管理者依實際合約調整時段，勿直接改付款證據。

## 六、證書代表什麼？

- 前端的 localStorage、匯入 JSON、`PUT /api/progress` 只能保存學習進度，不能當成發證依據。
- 付費伺服器另外記錄每一步測驗答案，檢查課程 SHA-256 版本、正確答案、先後順序、帳號、課程權限；每帳號每小時最多 240 次測驗提交。
- 完成所有步驟後可要求證書。驗證網址的高熵 ID 對应伺服器資料；顯示課名、步驟數、課程 hash、時間與撤銷狀態。瀏覽器打開驗證頁可列印／另存 PDF；JSON API 保留給程式驗證。
- 預設顯示 `Learner`；學員另外勾選同意才公開帳號姓名。驗證頁不輸出 email、內部帳號 ID、訂單號或付款資料。
- **這是本平台課程測驗完成紀錄**。題目是開卷、沒有真人監考與實物考核；不能證明由本人獨立作答、不可宣稱是學位、工程師資格或已驗證的工廠實作能力。實際工藝技能與高價專業證書需要另設人工評審、作品、量測資料與身份驗證。
- 教材改版產生新 hash，舊證書仍記載舊版本，新的課程版本需新的測驗紀錄；不會把先前證書偷偷換成新課。

## 七、API 契約

| 方法與路徑 | 用途／主要欄位 |
|---|---|
| `GET /api/billing/config` | mode、protected、checkoutAvailable、freeCourseIds、plans、termsVersion、legalUrls |
| `GET /api/billing/me` | 本人的 orders、entitlements、active；所有時間為 Unix 秒 |
| `POST /api/billing/checkout` | `{planId,requestId,termsAccepted:true,termsVersion}` → `{action,fields,orderId,mode}`；requestId 16–80 位英數／`_`／`-`，重送同一 checkout 要沿用 |
| `POST /api/billing/ecpay/notify` | 只有綠界 form-encoded 通知，成功接收回純文字 `1\|OK` |
| `GET /api/curriculum` | 課程陣列；未購的課只回簡介、`locked:true`、`stages:[]` |
| `GET /api/courses/:id` | 完整課；無有效權限 402 |
| `GET /api/learning/:courseId` | `{revision,completed:[stepId],total,mode}` |
| `POST /api/learning/evidence` | `{courseId,revision,stepId,answer}` → `{passed,completed:數量,total}` |
| `POST /api/certificates` | `{courseId,publishName:false}` → 證書物件 |
| `GET /api/certificates` | 本人證書清單 |
| `GET /api/certificates/:id` | 公開驗證 JSON；`Accept:text/html` 回可列印雙語證書 |

除公開 config、公開免費課、證書驗證及綠界 webhook，其餘會員操作需原有 session cookie；寫入還需同 Origin。伺服器不信任 `oai-authenticated-*` 或前端自稱 user ID。照片、官方來源與原創觀看提示可公開作課程介紹，私有文件索引只提供有效付費會員的 AI 檢索。

## 八、測試範圍與來源

`python3 -m unittest discover -s tests -p test_commerce.py -v`：使用本機測試 HTTP 與 mock 綠界回覆，檢驗官方 CheckMacValue 範例、未設定金流、live 啟用條件、價格所有權、重複 checkout、篡改、金額、特店、重複欄位、模擬付款、獨立查單、重複通知、跨帳號、到期、撤銷、靜態檔旁路、付費進度寫入、CSRF、證書順序／版本／隱私／列印頁。沒有刷卡、建立商家、呼叫真實綠界 API或做真實金流驗收。

本次查閱日期：2026-10-14。實際合約、費率及產品規格可能更動，上線前再核對：

1. 綠界官方費率：https://www.ecpay.com.tw/Business/payment_fees
2. 綠界結算與撥款：https://support.ecpay.com.tw/4809/
3. Coursera Plus 官方：https://www.coursera.org/courseraplus/
4. 綠界測試介接：https://developers.ecpay.com.tw/2856/
5. 建單／回呼／檢查碼：https://developers.ecpay.com.tw/2862/ 、https://developers.ecpay.com.tw/2878/ 、https://developers.ecpay.com.tw/2902/
6. 查詢訂單：https://developers.ecpay.com.tw/2890/

技術實作是依公開協定自行撰寫，未複製供應商網站版面、教材或第三方 SDK 原始碼；列出的官方測試向量僅用於互通驗證。
