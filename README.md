# MacGyver Engineering Academy V22

全畫面工程行走版：20 個領域、290 條既有故事路線，共 1,740 個製程站。人物可連續行走，鏡頭跟隨；走近設備後閱讀證據與操作。支援鍵盤、觸控搖桿、第一人稱／跟隨／總覽；無 WebGL 時使用連續行走的 2D 模式。

- 網站入口：`public/academy/experience.html`
- 本機啟動：`bash run-local.sh`（Windows：`run-local.bat`）
- 安裝／增量上傳：`bash Install_and_Upload_MacGyver_v22.sh --with-assets`
- 詳細指南：`docs/V22_WALKING_WORLDS_ZH.html`

工程空間是原創教學模型，照片維持原作者與授權，並非實測數位孿生。新控制介面內建 20 種語言；79 種語言目標的完整故事翻譯需配置翻譯服務。生成式 AI 需本機模型或後端 API；未附大型權重。公開分支維持首節試讀，完整教材與後端隨下載包提供。

---

# MacGyver Engineering Academy V21

This branch serves the public first-stage preview. The downloadable owner/source ZIP contains the complete bilingual curricula and local backend.

Run the **Publish static MacGyver Academy** GitHub Actions workflow to deploy Pages. Full member lessons require a separately configured authenticated content backend; GitHub Pages has no server-side account verification.

V21 uploads replace public files and remove recognized legacy generated member payloads/authoring inputs. They preserve unrelated repository files and do not erase earlier Git history.
