# V12 付費會員後端：Supabase + PayPal + 綠界（站長操作手冊）

本手冊說明如何把「MacGyver 工程學院 V12」的付費學習通行證接上您自己的 Supabase 專案、PayPal 與綠界（ECPay）。網站本身仍是 GitHub Pages 靜態網站；所有金額計算、付款驗證、開通與撤銷都在 Supabase Edge Functions（伺服器端）完成。

> 一句話原則：**瀏覽器只拿公開（publishable/anon）金鑰；價格一律由伺服器計算；只有伺服器驗證過付款才開通；收款撥款帳戶只在 PayPal／綠界後台設定，程式與設定檔裡沒有任何銀行或郵局帳號。**

---

## 1. 架構總覽

```
 學員瀏覽器 (https://kuonanhong.github.io/macgyver-academy/)
   │  公開金鑰 + 學員登入後的 access token
   │
   ├─ /auth/v1/signup  (帳號 username、密碼、Email、手機 phone) ──► Supabase Auth
   │        └─ 資料庫觸發器 academy_handle_new_user 驗證並建立 profiles（重複或格式錯 → 整筆註冊失敗）
   ├─ /functions/v1/username-login  (帳號或 Email + 密碼) ──► 伺服器查 Email → Supabase Auth 密碼登入
   ├─ /rest/v1/course_content  第 0 階段公開；其他階段需有效通行證（RLS）
   ├─ /functions/v1/access          查詢自己的通行證狀態
   │
   ├─ /functions/v1/checkout-create ──► 依 pricing.json 計價、建立訂單
   │        ├─ PayPal：建立 PayPal 訂單 → 瀏覽器用 PayPal JS SDK 付款（PayPal 錢包 / 金融卡或信用卡）
   │        │      └─ /functions/v1/checkout-capture → 向 PayPal 請款並逐項核對 → 開通
   │        └─ 綠界：回傳已簽章的表單 → 瀏覽器自動送到綠界信用卡付款頁（3-D 驗證在綠界頁面）
   │
 PayPal 伺服器 ──► /functions/v1/paypal-webhook   先呼叫 PayPal 驗章，再處理付款完成／退款／撤銷
 綠界伺服器   ──► /functions/v1/ecpay-notify     驗 CheckMacValue + 伺服器端 QueryTradeInfo 查單 → 回 1|OK
 pg_cron 每週 ──► /functions/v1/fx-refresh       更新 fx_rates 匯率（需 x-cron-secret）

 Supabase Postgres：profiles、plans、fx_rates、orders、entitlements、payment_events、login_attempts、course_content
 錢的流向：買家 → PayPal／綠界 → 您在 PayPal／綠界後台綁定的本人帳戶（見第 12 節）
```

### 本版新增檔案

| 檔案 | 用途 |
|---|---|
| `supabase/002_accounts_commerce.sql` | 資料表、RLS、觸發器與開通／撤銷函式（可重複執行） |
| `supabase/functions/<名稱>/index.ts` | 7 個 Edge Functions：checkout-create、checkout-capture、paypal-webhook、ecpay-notify、username-login、fx-refresh、access |
| `supabase/functions/_shared/*.ts` | 共用邏輯（計價、綠界簽章、PayPal、CORS、處理流程），可在 Node 測試 |
| `supabase/functions/_shared/pricing-rules.ts` | 由 `public/academy/data/pricing.json` 自動產生的價格規則副本 |
| `supabase/functions/.env.example` | 秘密設定範本 |
| `supabase/config.toml` | 每個函式是否要求 Supabase JWT（verify_jwt） |
| `tools/payments-v12/sync-pricing.mjs` | 同步 pricing.json → 函式與資料庫 |
| `tools/test-payments-v12.mjs` | 自動測試（印出 `payments ok` 才算通過） |

---

## 2. 事前準備

1. Supabase 專案（已依 `docs/GITHUB_ACCOUNTS_V8_ZH.md` 建好也可以直接沿用）。
2. Supabase CLI：
   - macOS：`brew install supabase/tap/supabase`
   - Windows：`scoop bucket add supabase https://github.com/supabase/scoop-bucket.git` 然後 `scoop install supabase`
   - 任何系統也可每次用 `npx supabase@latest <指令>` 代替 `supabase <指令>`。
3. PayPal **商家（Business）帳戶**與 https://developer.paypal.com/ 開發者登入。
4. 綠界特店帳號（測試期可先用綠界公開的測試特店，見第 8 節）。
5. 本機已下載本專案，終端機切到專案根目錄。

改價格時請只改 `public/academy/data/pricing.json`，然後執行：

```bash
node tools/payments-v12/sync-pricing.mjs          # 更新函式內的價格副本
node tools/payments-v12/sync-pricing.mjs --sql    # 印出 plans 更新 SQL，貼到 SQL Editor 執行
supabase functions deploy                         # 重新部署
```

若資料庫的 `plans` 與 pricing.json 不一致，結帳會安全地拒絕（錯誤碼 `pricing_mismatch`），不會用錯價格收款。

---

## 3. 步驟一：登入 CLI、連結專案、建立資料庫

```bash
supabase login                                   # 瀏覽器會開啟授權頁
supabase link --project-ref <您的 project-ref>    # Dashboard → Project Settings → General 可看到 Reference ID
mkdir -p supabase/migrations
cp supabase/001_learning_progress.sql supabase/migrations/20261013000000_learning_progress.sql
cp supabase/002_accounts_commerce.sql supabase/migrations/20261015000000_accounts_commerce.sql
supabase db push
```

- `001` 與 `002` 都可重複執行；若 001 以前已在 SQL Editor 跑過，再推一次也沒關係。
- 不想用 CLI 推資料庫時：到 Dashboard → SQL Editor，依序貼上 `001`、`002` 的全文執行即可。
- 若專案裡**已有別的 `public.profiles` 表**（某些範本會建立），002 會停下並提示，請先把舊表改名再執行。

完成後在 Table Editor 應看到：`profiles`、`plans`（all-30、all-365）、`fx_rates`（TWD=1）、`orders`、`entitlements`、`payment_events`、`login_attempts`、`course_content`。

---

## 4. 步驟二：Auth（登入）設定

Dashboard → Authentication：

1. **Sign In / Providers → Email**：啟用 Email，開啟 **Confirm email**（學員須點驗證信才可登入；未驗證者無法購買）。
2. **密碼**：最少長度設為 **12**（網站端也會檢查 12–128 字元）。可再開啟密碼強度要求。
3. **URL Configuration**：
   - Site URL：`https://kuonanhong.github.io/macgyver-academy/`
   - Redirect URLs：加入 `https://kuonanhong.github.io/macgyver-academy/`（只加您實際的網址，不要使用萬用字元開放任意網域）
4. **SMTP**：正式上線前設定自己的 SMTP（Supabase 內建寄信額度很低，只適合測試）。
5. **Rate Limits**：保留預設即可。注意：帳號登入是由 `username-login` 函式代為呼叫 Auth，若大量學員同時登入遇到 429，可適度調高「sign-in」上限；函式本身另有「同 IP＋同帳號 15 分鐘 10 次、同帳號 15 分鐘 30 次」的限制。
6. 不需要開啟 Phone 登入：手機號碼只存在 `profiles`，檢查格式（E.164，例如 `+886912345678`）與不可重複，**不會**發簡訊驗證。

註冊規則（由資料庫觸發器強制）：

| 欄位 | 規則 |
|---|---|
| 帳號 username | `^[A-Za-z0-9_.-]{3,30}$`，不分大小寫不可重複；admin、support、macgyver 等保留字不可用 |
| 密碼 | ≥ 12 字元（Auth 設定 + 網站端） |
| Email | 由 Supabase 寄驗證信確認 |
| 手機 phone | `^\+[1-9][0-9]{7,14}$`，不可重複 |

> 因為觸發器會拒絕缺少帳號／手機的使用者，**Dashboard 的「Add user」直接建立使用者會失敗**；請一律從網站註冊。

---

## 5. 步驟三：設定 Secrets（秘密值）

```bash
cp supabase/functions/.env.example supabase/functions/.env
# 用文字編輯器填好 .env（此檔已被 .gitignore 排除，絕不要上傳 GitHub）
supabase secrets set --env-file supabase/functions/.env
supabase secrets list                            # 只會顯示名稱與雜湊，確認都在
```

| 名稱 | 填什麼 | 哪裡取得 |
|---|---|---|
| `SUPABASE_URL`、`SUPABASE_ANON_KEY`、`SUPABASE_SERVICE_ROLE_KEY` | 不用設定 | Supabase 會自動提供給函式 |
| `ALLOWED_ORIGINS` | `https://kuonanhong.github.io` | 只有「通訊協定＋網域」，不含 `/macgyver-academy/`；本機測試可加 `,http://localhost:埠號` |
| `SITE_URL` | `https://kuonanhong.github.io/macgyver-academy/` | 學院網址 |
| `TERMS_VERSION` | `v12-2026-10` | 必須等於網站結帳時送出的條款版本；改條款時兩邊一起改 |
| `PAYPAL_ENV` | `sandbox`（測試）或 `live`（正式） | |
| `PAYPAL_CLIENT_ID`、`PAYPAL_CLIENT_SECRET` | PayPal App 的 Client ID / Secret | 第 7 節 |
| `PAYPAL_WEBHOOK_ID` | Webhook ID | 第 7 節 |
| `ECPAY_ENV` | `sandbox` 或 `live` | |
| `ECPAY_MERCHANT_ID`、`ECPAY_HASH_KEY`、`ECPAY_HASH_IV` | 特店編號與金鑰 | 第 8 節 |
| `CRON_SECRET` | 24 字元以上亂數（例如 `openssl rand -hex 24`） | 自己產生 |

函式只記錄訂單編號與錯誤代碼，不記錄 Email、手機、密碼、token、卡號或任何金鑰。

---

## 6. 步驟四：部署函式

```bash
supabase functions deploy
```

這會部署 `supabase/functions/` 下的 7 個函式，並套用 `supabase/config.toml`：

| 函式 | verify_jwt | 驗證方式 |
|---|---|---|
| checkout-create、checkout-capture、access | true | 需要學員登入的 access token；函式內也再用 `auth.getUser` 驗證 |
| paypal-webhook | false | PayPal 簽章（verify-webhook-signature + `PAYPAL_WEBHOOK_ID`） |
| ecpay-notify | false | 綠界 CheckMacValue + 伺服器端 QueryTradeInfo |
| username-login | false | 帳密本身 + 雜湊後的頻率限制 |
| fx-refresh | false | `x-cron-secret` 標頭需等於 `CRON_SECRET` |

若您的 CLI 沒有讀到 config.toml，可個別部署：`supabase functions deploy paypal-webhook --no-verify-jwt`（ecpay-notify、username-login、fx-refresh 同理）。
若專案改用新版 JWT Signing Keys 後，checkout-create／checkout-capture／access 一直回 401「Invalid JWT」，可把這三個也改成 `verify_jwt = false` 再部署；函式內本來就會驗證使用者，安全性不變。

函式網址格式：`https://<project-ref>.supabase.co/functions/v1/<函式名稱>`。

---

## 7. 步驟五：PayPal 設定（先 Sandbox 再 Live）

### 7.1 Sandbox（測試）

1. 登入 https://developer.paypal.com/ → **Apps & Credentials** → 上方切到 **Sandbox** → **Create App**（類型選 Merchant）。
2. 複製 **Client ID** 與 **Secret** → 填入 `.env` 的 `PAYPAL_CLIENT_ID`、`PAYPAL_CLIENT_SECRET`，`PAYPAL_ENV=sandbox`。
3. 同一個 App 頁面往下找 **Webhooks → Add Webhook**：
   - Webhook URL：`https://<project-ref>.supabase.co/functions/v1/paypal-webhook`
   - 勾選事件：`Payment capture completed`、`Payment capture refunded`、`Payment capture reversed`、`Payment capture denied`、`Checkout order approved`（最後一個是保險：學員付款後若關掉分頁，伺服器仍會完成請款）。
   - 儲存後複製 **Webhook ID** → `PAYPAL_WEBHOOK_ID`。
4. 重新 `supabase secrets set --env-file supabase/functions/.env`。
5. **Testing Tools → Sandbox Accounts** 有預設的 Personal（買家）測試帳號，可用來測 PayPal 錢包付款；**Testing Tools → Card Testing / Credit Card Generator** 可產生測試卡號，用來測「Debit or Credit Card」訪客刷卡。

### 7.2 網站端（給前端整合者）

PayPal JS SDK 只需要公開的 Client ID：
`https://www.paypal.com/sdk/js?client-id=<PAYPAL_CLIENT_ID>&currency=<實際收費幣別>&intent=capture&components=buttons`。
`currency` 必須等於 checkout-create 回傳的 `currency`（例如要求 KRW 會改用 USD）。PayPal 錢包與「Debit or Credit Card」按鈕都由 PayPal 顯示與處理，卡號不經過本站。

### 7.3 Live（正式）

1. Developer 網站切到 **Live** → 建立 Live App（需已通過認證的 PayPal 商家帳戶）。
2. 在 Live App 重新新增同樣的 Webhook（Live 與 Sandbox 的 Webhook ID 不同）。
3. `.env` 改 `PAYPAL_ENV=live`、填 Live 的 Client ID／Secret／Webhook ID → `supabase secrets set ...` → `supabase functions deploy`。
4. 網站的 PayPal SDK client-id 也要換成 Live 的 Client ID。

> 台灣 PayPal 帳戶對「台灣買家付款給台灣賣家」的國內交易有限制，台灣學員建議引導使用綠界；請以 PayPal 台灣客服或使用條款確認您帳戶的實際適用規則。

---

## 8. 步驟六：綠界 ECPay 設定

### 8.1 測試環境

`.env.example` 已預填綠界公開測試特店（`ECPAY_ENV=sandbox`、特店 `3002607`、HashKey `pwFHCqoQZGmho4w6`、HashIV `EkRm7iFT261dpevs`），付款頁為 `payment-stage.ecpay.com.tw`，不會真的扣款。
測試信用卡（依綠界技術文件，若有更新以綠界為準）：卡號 `4311-9522-2222-2222`、安全碼 `222`、有效期限填未來日期；3-D 驗證簡訊碼通常為 `1234`。

### 8.2 申請正式特店

1. 到綠界官網註冊會員，申請成為特約會員（個人賣家或公司），開通「信用卡」收款，等待審核。
2. 登入**廠商管理後台 → 系統開發管理 → 系統介接設定**，取得正式的 **特店編號（MerchantID）、HashKey、HashIV**。
3. `.env` 改成 `ECPAY_ENV=live` 與正式值 → `supabase secrets set ...` → `supabase functions deploy`。
   （`live` 模式若仍填公開測試特店編號，函式會拒絕啟用。）

### 8.3 ReturnURL（付款結果通知）

本系統每筆訂單都會自動帶入 ReturnURL：
`https://<project-ref>.supabase.co/functions/v1/ecpay-notify`
綠界伺服器會在付款後 POST 到這個網址，函式驗證通過才回 `1|OK`；沒有收到 `1|OK` 時綠界會重送。學員付款完成後按「返回商店」會回到 `SITE_URL?payment=ecpay&order=MG...`，網站再向伺服器查詢狀態。

- 綠界後台的「模擬付款」只送出 `SimulatePaid=1` 的連線測試通知，本系統**刻意不開通**，請用測試卡實際走一次付款流程。
- 綠界只收新台幣（TWD），一律以 pricing.json 的台幣價格收費。

---

## 9. 3-D Secure（3D 驗證）說明

- **綠界**：學員在綠界的信用卡付款頁輸入卡號，由綠界與發卡銀行依規則觸發 3-D 驗證（OTP 簡訊等）；本站伺服器只收到付款結果，從不接觸卡號。
- **PayPal**：無論是 PayPal 錢包或「Debit or Credit Card」訪客刷卡，卡片驗證與需要時的 3-D Secure 都由 PayPal 在其視窗內處理。
- 本系統開通的條件只看伺服器端驗證結果（PayPal：請款回應 `COMPLETED` 且金額、幣別、`custom_id` 全部相符；綠界：簽章正確 + `RtnCode=1` + 金額相符 + QueryTradeInfo `TradeStatus=1`），瀏覽器回報的「成功」不會直接開通。

---

## 10. 匯率自動更新（非台幣 PayPal 付款需要）

非 TWD 的價格 = 台幣價格 × `fx_rates.per_twd`，**無條件進位**到該幣別最小單位（JPY、HUF、TWD 等為整數，其餘到 0.01）。匯率超過 10 天（pricing.json `fxMaxAgeDays`）未更新時，該幣別會暫停結帳並提示改用台幣。

手動更新一次：

```bash
curl -X POST -H "x-cron-secret: <CRON_SECRET>" https://<project-ref>.supabase.co/functions/v1/fx-refresh
```

每週自動更新：在 Dashboard → Database → Extensions 啟用 `pg_cron` 與 `pg_net`，再依 `002_accounts_commerce.sql` 最後的註解範例，把同一個 CRON_SECRET 存進 Vault 並建立排程。
匯率來源為 open.er-api.com（ExchangeRate-API 免費端點，約每日更新）；網站若顯示換算價格，請依其使用條款加註「Rates By Exchange Rate API」與連結 https://www.exchangerate-api.com 。

---

## 11. 付費課程內容

- `course_content(course_id, stage_index, revision, payload)`：`stage_index = 0`（每門課第一節）任何人可讀；其他階段只有有效通行證的學員讀得到（資料庫 RLS 強制）。
- 內容由站長／整合工具用 service role 寫入（SQL Editor 或伺服器端腳本），瀏覽器不能寫入。
- **重要**：付費階段若仍放在 GitHub Pages 的公開 JSON／JS 檔裡，任何人都能直接下載。上線前請確認公開網站只保留第 0 階段（及目錄資訊），其餘階段只存在 `course_content`。

---

## 12. 收款撥款到郵局帳戶

撥款（把營收轉進您的存款帳戶）**只在 PayPal 與綠界的後台設定**，本專案的程式、資料庫與設定檔都不需要、也不應該出現任何銀行或郵局帳號。

### 12.1 綠界 → 銀行帳戶

依綠界客服中心說明（https://support.ecpay.com.tw/4784/ ，2026-10-15 查閱）：

- 綠界帳戶餘額可提領到**會員本人或公司名稱**的銀行帳戶，不能新增非本人帳戶；分行資訊需與存摺一致，戶名不符會提領失敗。
- 申請提領後約 **2–3 個工作日**到帳（自動提領同樣時程）。
- 提領銀行**非永豐銀行**時，每次提領另收跨行轉帳手續費 **NT$15**（固定金額自動提領時會從入帳金額扣除，例如 NT$10,000 實收 NT$9,985）；以永豐帳戶為預設提領帳戶可免手續費。
- 每月提領上限依賣家類型與服務而定；長期（365 天）未提領另有規定。
- **郵局（中華郵政）帳戶**：該頁未提及。是否可設定郵局帳戶為提領帳戶，請直接向綠界客服確認；若不行，可先提領到本人銀行帳戶再自行轉入郵局。

### 12.2 PayPal → 台灣帳戶

- 台灣的 PayPal 帳戶提領新台幣，目前是透過**玉山銀行（E.SUN）的 PayPal 提領服務**；玉山帳戶戶名需與 PayPal 帳戶登記的姓名或公司名稱完全相符，且 PayPal 帳戶需為台灣註冊。
- 依 MrMad 2024-02-04 整理（https://mrmad.com.tw/paypal-withdrawal-tutorial ）：新台幣餘額提領到玉山新台幣帳戶免手續費；最低提領 NT$100；約 3–5 個工作日入帳；文中另提及以其他幣別提領的費用（2.5%）與換匯規則。費率與流程可能變動，請以 PayPal 與玉山官方頁面為準（玉山 PayPal 服務頁：https://www.esunbank.com.tw/bank/digital/ecommerce/cross-border/paypal ，本次未能直接開啟核對）。
- 款項進入玉山帳戶後，再由您**自行轉帳到郵局帳戶**。

---

## 13. 退款與撤銷

| 情況 | 退錢在哪裡做 | 通行證怎麼撤銷 |
|---|---|---|
| PayPal 退款 | PayPal 後台 → Activity → 該筆交易 → Refund | 自動：Webhook `PAYMENT.CAPTURE.REFUNDED` |
| PayPal 爭議／撤銷 | PayPal Resolution Center | 自動：`PAYMENT.CAPTURE.REVERSED` |
| 綠界退刷 | 綠界廠商後台 → 信用卡收單 → 交易查詢 → 退刷 | **手動**（綠界不會通知 ReturnURL）：見下方 SQL |
| 不退錢只取消權限 | — | 手動 SQL |

```sql
-- 以訂單編號撤銷（SQL Editor 以站長身分執行；reason 以 refund 開頭 → 狀態 refunded）
select public.academy_revoke_entitlement('MG0123456789ABCDEF01', 'refund: ECPay 退刷 2026-10-20');
```

- 任何退款（含部分退款）都會撤銷該筆通行證；撤銷後排在後面的通行證會自動往前補齊，學員只失去被退款的那一段時間。
- 撤銷是冪等的，重複執行不會出錯；撤銷後即使收到遲到的付款通知也不會再開通。
- 查詢：`select id, status, provider, currency, amount, paid_at, revoked_at, revoke_reason from public.orders order by created_at desc limit 50;`
- 狀態 `review` 代表付款資料與訂單不符（金額、幣別、訂單編號或交易序號），系統不會自動開通；請到 PayPal／綠界後台核對，確認無誤可執行 `select public.academy_grant_entitlement('MG...');`，否則退款。

---

## 14. Sandbox 測試清單

- [ ] `node tools/test-payments-v12.mjs` 印出 `payments ok`。
- [ ] 註冊：帳號、密碼 ≥12、Email、手機都必填；重複帳號（大小寫不同也算）與重複手機會被拒；收到驗證信並能點開。
- [ ] 登入：用帳號、用 Email 都能登入；密碼錯誤只顯示一般錯誤訊息；同一 IP＋帳號 15 分鐘第 11 次被擋（429）。
- [ ] 未登入／未購買：只看得到每門課第 0 階段。
- [ ] PayPal 錢包（Sandbox Personal 帳號）付款 → 狀態 paid → `access` 顯示 active → 看得到其他階段。
- [ ] PayPal「Debit or Credit Card」以測試卡付款成功。
- [ ] 再買一次：到期日從上一張的到期日往後延。
- [ ] Sandbox 後台對該筆退款 → 幾分鐘內訂單變 refunded、權限消失。
- [ ] 綠界測試卡付款 → `payment_events` 有一筆 result=paid、訂單 paid。
- [ ] 綠界後台「模擬付款」→ 不開通（result=simulated-ignored）。
- [ ] 手動呼叫 fx-refresh（錯誤 secret → 401；正確 → `fx_rates` 更新）。
- [ ] 函式 Logs（Dashboard → Edge Functions → Logs）沒有 Email、密碼、卡號或金鑰。

## 15. 上線清單

- [ ] PayPal 已切 Live（Client ID／Secret／Webhook ID 都是 Live；網站 SDK 也用 Live Client ID）。
- [ ] 綠界已換正式特店編號、HashKey、HashIV，`ECPAY_ENV=live`。
- [ ] `ALLOWED_ORIGINS`、`SITE_URL` 只有正式網址；`TERMS_VERSION` 與網站條款頁一致，條款含退款與數位內容說明。
- [ ] Auth：Confirm email 開啟、密碼最少 12、正式 SMTP、Site URL／Redirect URLs 正確。
- [ ] `pricing.json`、`pricing-rules.ts`、`plans` 三者一致（`node tools/payments-v12/sync-pricing.mjs --check`）。
- [ ] 匯率排程已建立，`fx_rates` 在 10 天內。
- [ ] 清除測試期開通的權限：
      `select public.academy_revoke_entitlement(id, 'sandbox cleanup') from public.orders where env = 'sandbox' and status = 'paid';`
- [ ] 公開網站已移除付費階段內容（第 11 節）。
- [ ] 用真卡小額買一次、確認開通，再於後台退款確認撤銷。
- [ ] 在 PayPal／綠界後台確認撥款帳戶（第 12 節），程式內不放任何帳號。

---

## 16. 給前端整合者：API 摘要

所有錯誤皆為 JSON：`{"error": "<代碼>", "message": "<說明>", ...}`；429 會附 `Retry-After`。函式網址前綴 `https://<ref>.supabase.co/functions/v1/`。

| 呼叫 | 請求 | 成功回應 |
|---|---|---|
| RPC `academy_check_available`（`POST /rest/v1/rpc/academy_check_available`，anon key） | `{"p_username":"Alice_01","p_phone":"+886912345678"}` | `{"usernameAvailable":true,"phoneAvailable":true}`（格式錯 → false；傳 null → null） |
| `/auth/v1/signup` | `{"email","password","data":{"name","username","phone"}}` | Supabase 原生回應；觸發器拒絕時為 500「Database error saving new user」 |
| `username-login`（POST） | `{"login":"帳號或Email","password":"..."}` | Supabase Auth session JSON（access_token、refresh_token、expires_in、expires_at、user…） |
| `access`（GET/POST，Bearer） | — | `{"active":true,"expiresAt":"2026-11-14T08:00:00+00:00","planId":"all-30","serverTime":"..."}` |
| `checkout-create`（POST，Bearer） | `{"planId":"all-30","currency":"USD","provider":"paypal","termsAccepted":true,"termsVersion":"v12-2026-10"}` | PayPal：`{"orderId","provider":"paypal","amount":"9.33","currency":"USD","paypalOrderId","planId","durationDays"}`；綠界：`{"orderId","provider":"ecpay","action","fields":{...},"amount":"299","currency":"TWD","planId","durationDays"}` |
| `checkout-capture`（POST，Bearer） | `{"orderId":"MG..."}` | 200 `{"status":"paid","orderId","expiresAt"}`；202 `{"status":"pending"}`；402 `{"status":"declined","restart":true}`；409 `review`／`refunded`／`not_approved`。綠界訂單只回報狀態（供付款後輪詢） |
| 課程內容（`GET /rest/v1/course_content?select=course_id,stage_index,revision,payload&course_id=eq.<id>&order=stage_index`） | apikey；已登入再加 `Authorization: Bearer <access_token>` | 未購買只會回第 0 階段的列；有效通行證回全部 |

主要錯誤代碼：`auth_required`(401)、`email_not_confirmed`(403/400)、`origin_not_allowed`(403)、`invalid_plan`／`invalid_provider`／`invalid_currency`／`terms_required`(400)、`terms_outdated`(409，附 `termsVersion`)、`fx_unavailable`(503，附 `fallbackCurrency:"TWD"`)、`pricing_mismatch`／`not_configured`(503)、`too_many_orders`／`rate_limited`(429)、`invalid_credentials`(400)、`provider_error`(502)。

---

## 17. 疑難排解

- **註冊一直出現「Database error saving new user」**：帳號或手機格式錯、保留字或已被使用。網站應先呼叫 `academy_check_available`。
- **checkout-create 回 503 not_configured**：查看函式 Logs 中 `not_configured` 的 `problems` 欄位（只列出缺少的設定名稱）。
- **綠界一直重送通知**：查看 ecpay-notify Logs 的 `code`：`bad_mac`（金鑰錯）、`order_mismatch`（金額或環境不符）、`query_not_paid`（綠界查單尚未成功）。
- **PayPal Webhook 400 bad_signature**：`PAYPAL_WEBHOOK_ID` 與實際 App 不符，或 Sandbox／Live 混用。

## 18. 參考資料

- 綠界提領說明：https://support.ecpay.com.tw/4784/ （2026-10-15 查閱）
- PayPal 提領教學（MrMad）：https://mrmad.com.tw/paypal-withdrawal-tutorial （2026-10-15 查閱；內容日期 2024-02-04）
- 玉山銀行 PayPal 服務：https://www.esunbank.com.tw/bank/digital/ecommerce/cross-border/paypal
- Supabase Edge Functions、PayPal Orders v2／Webhooks、綠界 AIO 全方位金流 V5 與 QueryTradeInfo 請參閱各自官方開發文件。綠界 CheckMacValue 演算法已由自動測試與既有 `portable/commerce.py` 及綠界文件範例值逐位元比對。
