# V16 實景工程探索模組

`public/academy/immersive-v16.js` 與 `.css` 是無外部套件依賴的延遲載入模組。
匯入 JavaScript 本身不啟動網路請求或動畫；建立場景時才要求該場景照片。
原創 3D 教學設備以實際三維相機投影到 Canvas 2D，並用可聚焦的 DOM 按鈕作為設備標籤。

## 整合

```js
const dispose = mountImmersiveScene(container, course, {
  en: false,
  step: currentStep,
  photos: existingPhotos,
  scenePhotos: scenePhotoManifest,
  sources: curriculumSources,
  onPractice({courseId,stepId}) { /* 前往既有工作台；不代答驗收 */ },
  onExplore({courseId,equipment,kind}) { /* optional */ },
  onObservation(observation) { /* optional: add to an explicit notebook */ }
});
// 換頁、換語言、換課程或重繪時先釋放監聽器／觀察器。
dispose();
```

也可使用 `renderImmersiveScene(course,options)` 回傳安全 HTML，再呼叫
`bindImmersiveScene(container,course,options)`。所有 DOM 查詢都以容器為範圍。
`scenePhotos` 使用 `{photos,categories,courses}`：

```json
{"photos":[{"id":"example","path":"assets/photos/example.jpg","title":"…","titleEn":"…","author":"…","license":"…","licenseUrl":"https://…","sourceUrl":"https://…"}],"categories":{"rail":"example"},"courses":{"course-id":{"photoIds":["example"],"match":"representative","note":"代表性照片","noteEn":"Representative photograph"}}}
```

只有清單明列 `match: exact` 才顯示本工程照片；既有 `courseIds` 配對一律先視為代表性照片。
照片僅接受 `assets/` 下的本機相對路徑，來源與授權連結只接受 HTTPS。

`projectArchitecture(course)` 保留教材的 `architectureNodes`／`architectureEdges`，
並優先採用現有課程的 `v16Architecture` 擴充。節點可為中英配對，或含有
`id,title,titleEn,role,roleEn,sourceIds` 的物件。未提供的角色不補造；
沒有專屬節點來源時，明確標示為整門課的來源。若無架構資料，改顯示已提供的
課程階段名稱與學習順序，不把階段偽裝成真實硬體配置。
專題節點可點選並沿相連節點探索，SVG 連線會依容器與手機版重新計算。
三維暖身設備與專題關係圖分開呈現，不聲稱存在幾何或現場控制對應。

既有 app.js 在 document capture 處處理工作台鍵盤，必須對 `.immersive-v16`
加入相同的鍵盤與 focus 排除條件，避免方向鍵同時移動舊工作台零件。

## 操作與驗證

- 第一視角：較低的操作位置；第二視角：環繞相機；第三視角：全景與學徒標記。
- 拖曳變更方位／俯仰，觸控雙指縮放；聚焦畫布後滾輪可縮放。
- 方向鍵或 WASD 調整相機，`+`／`-` 縮放，`1`／`2`／`3` 切換視角，Home 重設。
- 四個設備按鈕皆可鍵盤選取；小螢幕另提供固定設備清單。
- 顯示作者、授權、原始照片連結與代表性範圍。照片失敗時保留原創模型。
- 10 個領域暖身模型涵蓋 20 分類：定減速、水力、熱 RC、直流電阻、傳輸延遲、
  軸向彈性、風洞阻力、真空光頻率、圓管層流與理想熱量平衡。
- 模型提供單位、公式、適用範圍、來源與變因挑戰；不是每項課程的完整工程模型。
- 最多五筆觀察保留於當次場景工作階段，離開前可複製；不假稱已跨裝置保存。
- 未點選或操作時不運轉持續動畫迴圈，離開可見範圍停止繪製；像素倍率上限 2。

執行 `node tools/scene-v16/test-scene.mjs` 驗證物理量、換算、相機投影、照片範圍與資料轉義。
另驗證專題節點雙語、角色／來源保留、無效連線排除及階段退回的語意。
真實瀏覽器測試由整站整合檢查執行；本檔不宣稱通過實體手機、Safari 或 Firefox 測試。

## 模型與照片邊界

參考 HEART 政策島的「全景 → 點選 → 關係與說明」探索方式；未複製其程式、圖像或文字。
照片背景與原創教學設備分層，三維位置沒有和照片中的設備做幾何配準。
本版本沒有現場感測器、數位分身校正或控制設備連線，不能宣稱是現場即時數位孿生。
顯示的假想量測與數值不作為施工、製程、行車、臨床或設備保護設定。

## Responsive browser verification (2026-10-23)

The managed preview was tested in cloud Chrome at 390 px and 820 px wrapper widths. With scrollbars, document widths were 375 px and 805 px; document scroll widths matched exactly. Photo attribution, equipment selection, all three camera modes, drag/keyboard projection, live calculation, observation table, project-stage component inspection, and navigation into the existing gated workshop passed. Changing speed from 60 to 61 km/h changed the displayed stopping distance from 190.28 to 196.39 m. No preview-origin console errors were observed. Native device multi-touch and the final new rail curriculum were outside this responsive-browser pass. Full recorded results are in `VALIDATION_SCENE_V16.json`.
