# GitHub Pages 的個人帳號與跨裝置學習紀錄

GitHub Pages 負責公開 HTML／CSS／JavaScript；登入、驗證信與個人資料庫由您設定的 Supabase 提供。本版已附真實 Auth REST 與資料庫介接，但沒有替您開設 Supabase 專案，也沒有內建帳密。未設定時清楚顯示本機學習檔案：姓名／信箱只在目前瀏覽器，不驗證信箱、不使用密碼、不能當作保密帳號；清除瀏覽器資料會失去它，請定期匯出。

## 站長一次設定

1. 在 https://supabase.com/ 建立您自己的專案。在 SQL Editor 執行套件中的 `supabase/001_learning_progress.sql`。它建立 `academy_progress`、每名學員只能讀寫自己資料的 RLS 政策，以及以版本比對避免覆寫的 `academy_save_progress` 函式。
2. Authentication → Providers 啟用 Email，開啟 **Confirm email**。設好正式 SMTP，設定密碼至少 12 字元、登入／郵件速率限制。若要啟用 CAPTCHA，須先另接入對應前端驗證元件；本版未附 CAPTCHA widget，不能只啟用後端要求。正式大量對外使用前，依 Supabase 的最新額度、備份與安全設定檢查自己的部署。
3. Authentication → URL Configuration：Site URL 填完整正式網址，例如 `https://kuonanhong.github.io/macgyver-academy/`。Redirect URLs 加入實際學院路徑，使用本套件 Pages workflow 時就是 `https://kuonanhong.github.io/macgyver-academy/`；若自行改成子目錄部署，才填對應的 `/academy/` 或 `/public/academy/`。查看瀏覽器地址列，使用精確路徑；不要開放任意網域。
4. Settings → API Keys 複製 Project URL 與 **publishable key**（`sb_publishable_...`）。舊專案的 `anon` JWT 也可以。**不要複製 secret／service_role key 到前端**。
5. 修改 `public/academy/config.js`：

   ```js
   supabaseUrl: 'https://YOUR_PROJECT.supabase.co',
   supabasePublishableKey: 'sb_publishable_YOUR_PUBLIC_KEY',
   siteMode: 'auto',
   ```

6. 執行 `bash build-offline.sh`，再依 `docs/GITHUB_UPLOAD_ZH.md` 推送與執行 Pages workflow。GitHub Pages 的學院介面會出現雲端註冊／登入。自訂靜態網域可設定 `siteMode: 'static'`；原 ChatGPT Sites 與 Python 同源帳號仍使用原後端。
7. 用兩個不同信箱實測：A 註冊、收信驗證、登入、完成一步並寫筆記；另一瀏覽器登入 A 應看到紀錄；登入 B 必須看不到 A 的紀錄。同時在兩個視窗改筆記，應合併或提示衝突而不是靜默覆蓋。只有此站長實測通過後，才算您的雲端服務部署完成。

## 學員流程

使用姓名、信箱、12–128 字元密碼註冊，依驗證信完成驗證後登入。下次在另一台裝置登入同一信箱即可讀取同步完成的工序、概念組合狀態與筆記。原來的本機學習檔案不會偷偷轉交雲端；可自行匯出後，在登入雲端帳號時匯入。

忘記密碼時按「重設密碼」，從郵件連回**同一正式網址**後設定新密碼。驗證／重設連結的授權片段會從地址列移除，再向 Supabase 驗證。共用電腦請登出；瀏覽器會保存可更新的登入 session，並以每名使用者 ID 分開保存裝置備份。

連線中斷時保留裝置備份，介面顯示尚未同步；不要把「裝置已保存」視為雲端保存。瀏覽器私人模式、儲存額度不足、撤銷權限均可能影響保存。直接雙擊 `index.html` 的 `file://` 頁面適合本機檔案，郵件驗證應使用 HTTPS 網站。

## 資料範圍與管理

姓名／信箱在 Supabase Auth；學習表保存專案 ID、完成步驟、組合步驟、筆記與版本戳。密碼不寫進 GitHub、HTML 或本機設定。刪除 Auth 使用者時，外鍵會一併刪除其雲端學習紀錄；站長可從 Supabase Dashboard 管理。刪除雲端帳號不會替學員刪除已匯出的檔案或裝置備份。

RLS 以 `auth.uid()` 及 `security invoker` 判斷資料所有者；公開 key 不是權限控制。版本為單調遞增的毫秒整數；比較失敗會回傳衝突，前端保存雙方筆記。不要移除 RLS，也不要把 service-role key 放在瀏覽器。現有單元測試驗證 API 轉接、身份切換與衝突處理；沒有連入您的實際 Supabase，因此不冒稱已完成跨裝置實測。

官方依據（2026-10-13 查閱）：
- https://supabase.com/docs/guides/auth/passwords
- https://supabase.com/docs/guides/database/postgres/row-level-security
- https://supabase.com/docs/guides/database/functions
- https://supabase.com/docs/guides/auth/managing-user-data
- https://docs.github.com/en/pages/getting-started-with-github-pages/what-is-github-pages
