# V11 課程與技能地圖

這張地圖以工程門派與技能關係整理全部課程。它與原有「世界工程地圖」分工：課程與技能地圖呈現學習、概念準備與衍生比較，世界工程地圖呈現工程所在地、地理環境與 Google Maps。

## 使用方式

1. 選擇工程門派，例如量子電腦、神經網路與 AI、伺服器與 HPC、防禦資安、通訊、能源或資源工程。
2. 使用中英文關鍵字與專業分支縮小範圍。搜尋採不分大小寫、多詞 AND 比對，保留完整目錄；分頁不改變教材的存在與存取權限。
3. 在卡片按工程名稱進入既有 `#project/<id>` 專案頁。
4. 按「準備、衍生與比較」查看概念準備、目前項目與下一個比較。課程順序是編輯的概念建議，不是正式先修資格或工業作業程序。
5. 「逐步課程」「研究選題」與「需解鎖」分開標示。研究選題尚未包含專屬完整工序；付款與解鎖仍由既有會員與伺服器權限處理。

共有 17 個門派與 35 個預設分支，另保留各課作者定義的子領域。量子門派包含超導、囚禁離子、中性原子、光子、自旋、退火、錯誤校正與拓樸。拓樸分支是研究與證據界線；分類不表示已證實拓樸性、非阿貝爾操作或容錯運算。AI 分支包含神經網路、GPU、TPU、晶圓級加速器、FPGA／可重組資料流、類神經與資料／模型服務。能源分支包含核電、SMR、融合、風力、水力、地熱、儲能與其他轉換；資源分支包含油氣、淘金與採礦。實際項目依目錄動態出現，分支本身不代表課程已完成。

## 整合 API

檔案：`public/academy/learning-map.js` 與 `learning-map.css`。模組只依賴既有的 `project-identity.js` 圖示，不連線、不要求位置、不讀寫會員或付費資料。

```js
import { renderLearningMap, mountLearningMap } from './learning-map.js';

// 首次渲染；language 可為 'zh-TW'、'en'，或布林 zh。
main.innerHTML = renderLearningMap(catalog, featured, language);

// 掛載會再次依目前資料渲染並啟用元件內事件。
const map = mountLearningMap(main, {
  catalog,
  featured,
  language,
  // 可省略：由既有全站 hashchange 處理 #project/id。
  onOpenCourse(id) { location.hash = '#project/' + encodeURIComponent(id); },
  onRendered() { /* 可在此使用既有頁面語言處理 */ }
});

// 切換帳號／重新取得課程存取權後，傳入當下資料。
map.update({ catalog, featured, language });

// 離開路由前移除元件事件。
map.dispose();
```

純函式輸出包括 `buildLearningMapIndex`、`classifyLearningCourse`、`filterLearningMapCourses`、`resolveLearningRoute`、`learningCoursePath`。`LEARNING_TRACKS`、`LEARNING_SUBDISCIPLINES`、`LEARNING_ROUTES` 是可讀取的編輯資料。

`renderLearningMap(catalog, featured, language, options)` 的可選 `options`：`query`、`track`、`subdiscipline`、`maturity`（`guided`／`research`／`locked`）、`page`（從 0 起算）、`pageSize`（6–60，預設 18）、`selectedId`、`routes`。掛載初始狀態由 `state` 提供。`update({state:{...}})` 可調整目前篩選。

## 目錄標記

新選題可加入以下欄位，舊資料仍能以標題分類：

```json
{
  "learningTrack": "quantum",
  "learningSubdiscipline": "quantum-ion",
  "learningTags": ["QPU", "trapped ion", "囚禁離子"],
  "learningPrerequisites": ["確實存在的課程 ID"],
  "learningDerivatives": ["確實存在的課程 ID"]
}
```

門派列舉：`quantum`、`ai`、`servers`、`cyber`、`networks`、`foundation`、`energy`、`resources`、`semiconductor`、`packaging`、`electronics`、`civil`、`mobility`、`materials`、`science`、`process`、`other`。

來源目錄中的 `locked:true` 不會被較舊 featured 資料覆蓋成未鎖定。這只是介面標記，真正的教材保護仍由後端門禁執行。不存在的準備或衍生課程 ID 不生成連結。量子硬體與核能類型等並列門派標為比較分支，不編造必須按序建造的依賴。

## 驗證與限制

執行 `node tools/test-learning-map-v11.mjs`。檢查完整中英分頁、100 個既有資訊／資安 ID 保留、量子／能源／資源分支、有效專案連結、鎖定與研究標示、HTML 字元逃逸、元件篩選與清理、資料更新後清除已移除的項目。

若 `tools/computing-v11/expansion.json` 存在，另核對 80 項擴充課程的門派／分支宣告與地圖分類一致。獨立編輯檢查核對了 66 個新 ID、14 個既有研究選題升級，沒有覆寫既有逐步課程；80 組地理欄位標為公開場址或機構的近似代表點，160 個延伸連結均指向同批已存在項目。80 組原創假想算例的 129 項數值與單位換算已重算，包含獨立錯誤事件機率、光路透過率與 dB、自旋／Rydberg 尺度、roofline、Amdahl、熱電與脈衝能量界線；此核對不驗證產品性能，也不替代真實量測。

介面使用語意化原生按鈕、表單、欄位標籤與 `aria-live` 結果數，具響應式欄數、深色主題與 reduced-motion 規則。這些程式檢查不取代實體手機、平板、桌機與真實瀏覽器的視覺／輔助技術驗收。
