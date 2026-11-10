/* V30 full-screen real-world engineering scene.
 * A character walks on the terrain and imagery of a real site; the camera and the
 * loaded ground follow the footsteps. Six fixed wide-angle looks (front, back,
 * left, right, up, down), credited photographs, fixed-position 360° panoramas and
 * engineering workstations are available in all 20 domains.
 * Online layers (satellite imagery, elevation, Wikimedia Commons) are optional,
 * loaded at view time and credited on screen; without a connection the scene uses
 * the credited local media only. No uncaptured surface is fabricated as real.
 */
(function(){'use strict';
const D=window.MG_REALWORLD_V30,R=window.MG_RESOURCE_V31,SC=window.MG_SCENES_V31,T=window.THREE,$=id=>document.getElementById(id);
const loading=$('rw-loading');
if(!D||!Array.isArray(D.domains)||!T){if(loading)loading.textContent='場景資料或 3D 引擎未載入，請重新整理。 Scene data or the 3D engine failed to load; reload this page.';return;}
if(D&&window.MG_RESOURCE_MEDIA_V31){const ids=new Set((D.assets.materials||[]).map(m=>m.id));D.assets.materials=[...window.MG_RESOURCE_MEDIA_V31.filter(m=>!ids.has(m.id)),...(D.assets.materials||[])];}
if(R&&D){const resources=D.domains.find(d=>d.id==='materials');if(resources){resources.t='材料／石油、天然氣與採礦';resources.e='Materials / oil, gas & mining';}const ids=new Set((D.sites.materials||[]).map(s=>s.id));D.sites.materials=[...(R.sites||[]).filter(s=>!ids.has(s.id)),...(D.sites.materials||[])];}
const CFG=Object.assign({online:false,imagery:'https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}',imageryCredit:'Imagery © Esri, Maxar, Earthstar Geographics and the GIS User Community',elevation:'https://s3.amazonaws.com/elevation-tiles-prod/terrarium/{z}/{x}/{y}.png',elevationCredit:'Elevation: Terrain Tiles (Mapzen / AWS Open Data)',commons:'https://commons.wikimedia.org/w/api.php',imageryZoom:16,elevationZoom:13,photoLimit:12},(window.MG_CONFIG||{}).realworld||{});
const KEYS=['domain','site','online','offline','full','help','follow','shoulder','first','over','front','back','left','right','up','down','wide','pace','recenter','act','close','compute','result','inputs','correct','wrong','openCourse','exitPano','station','photo','pano','challenge','loading','onlineOk','onlineFail','approx','progress','source','teaching'];
const WORDS={
'zh-TW':['領域','場址','線上實景','離線場景','全螢幕','說明','跟隨','肩後','第一人稱','俯瞰','前','後','左','右','上','下','廣角','步速','回正','處理','關閉','計算','結果','輸入','正確','再想想','開啟完整課程 ↗','離開全景','工程工作站','實拍照片','360° 全景','把 {v} 增加 10%，結果會是多少？','正在載入地形與影像…','已載入線上衛星影像與地形','無法連線，改用離線場景','代表座標為近似位置','已完成 {n} / {m} 個工作站','來源','數值為公開標稱值或教學假設'],
'zh-CN':['领域','场址','在线实景','离线场景','全屏','说明','跟随','肩后','第一人称','俯瞰','前','后','左','右','上','下','广角','步速','回正','处理','关闭','计算','结果','输入','正确','再想想','打开完整课程 ↗','离开全景','工程工作站','实拍照片','360° 全景','把 {v} 增加 10%，结果会是多少？','正在加载地形与影像…','已加载在线卫星影像与地形','无法连接，改用离线场景','代表坐标为近似位置','已完成 {n} / {m} 个工作站','来源','数值为公开标称值或教学假设'],
'en':['Domain','Site','Live imagery','Offline scene','Full screen','Help','Follow','Shoulder','First person','Overview','Front','Back','Left','Right','Up','Down','Wide angle','Pace','Recentre','Engage','Close','Compute','Result','Inputs','Correct','Try again','Open the full course ↗','Leave panorama','Engineering workstation','Photograph','360° panorama','Raise {v} by 10%: what is the result?','Loading terrain and imagery…','Live satellite imagery and terrain loaded','No connection; using the offline scene','Coordinates are approximate','{n} of {m} workstations completed','Source','Values are public nominal figures or teaching assumptions'],
'ja':['分野','サイト','オンライン実景','オフライン','全画面','ヘルプ','追従','肩越し','一人称','俯瞰','前','後','左','右','上','下','広角','速度','正面に戻す','対応する','閉じる','計算','結果','入力','正解','もう一度','講座を開く ↗','パノラマを出る','工学ワークステーション','実写真','360° パノラマ','{v} を 10% 増やすと結果はいくつ？','地形と画像を読み込み中…','オンラインの衛星画像と地形を読み込みました','接続できません。オフライン表示です','座標はおおよその位置です','{m} か所中 {n} か所完了','出典','数値は公称値または教材上の仮定です'],
'ko':['분야','현장','온라인 실경','오프라인','전체 화면','도움말','따라가기','어깨 뒤','1인칭','조감','앞','뒤','왼쪽','오른쪽','위','아래','광각','속도','정면 복귀','처리','닫기','계산','결과','입력','정답','다시 생각','전체 강좌 열기 ↗','파노라마 나가기','공학 워크스테이션','실제 사진','360° 파노라마','{v} 을(를) 10% 늘리면 결과는?','지형과 영상을 불러오는 중…','온라인 위성 영상과 지형을 불러왔습니다','연결할 수 없어 오프라인 장면을 사용합니다','좌표는 근사 위치입니다','워크스테이션 {m}개 중 {n}개 완료','출처','수치는 공칭값 또는 교육용 가정입니다'],
'es':['Dominio','Sitio','Imágenes en línea','Escena sin conexión','Pantalla completa','Ayuda','Seguir','Hombro','Primera persona','Vista general','Frente','Atrás','Izquierda','Derecha','Arriba','Abajo','Gran angular','Ritmo','Recentrar','Atender','Cerrar','Calcular','Resultado','Entradas','Correcto','Inténtalo de nuevo','Abrir el curso completo ↗','Salir del panorama','Estación de ingeniería','Fotografía','Panorama 360°','Aumenta {v} un 10 %: ¿cuál es el resultado?','Cargando terreno e imágenes…','Imágenes satelitales y terreno cargados','Sin conexión; se usa la escena local','Las coordenadas son aproximadas','{n} de {m} estaciones completadas','Fuente','Valores nominales públicos o supuestos didácticos'],
'fr':['Domaine','Site','Imagerie en ligne','Scène hors ligne','Plein écran','Aide','Suivre','Épaule','Première personne','Vue d’ensemble','Avant','Arrière','Gauche','Droite','Haut','Bas','Grand angle','Allure','Recentrer','Traiter','Fermer','Calculer','Résultat','Entrées','Correct','Réessayez','Ouvrir le cours complet ↗','Quitter le panorama','Poste d’ingénierie','Photographie','Panorama 360°','Augmentez {v} de 10 % : quel est le résultat ?','Chargement du terrain et des images…','Imagerie satellite et relief chargés','Pas de connexion ; scène hors ligne','Coordonnées approximatives','{n} postes terminés sur {m}','Source','Valeurs nominales publiques ou hypothèses pédagogiques'],
'de':['Fachgebiet','Standort','Live-Bilder','Offline-Szene','Vollbild','Hilfe','Folgen','Schulter','Ich-Perspektive','Übersicht','Vorne','Hinten','Links','Rechts','Oben','Unten','Weitwinkel','Tempo','Zentrieren','Bearbeiten','Schließen','Berechnen','Ergebnis','Eingaben','Richtig','Noch einmal','Vollständigen Kurs öffnen ↗','Panorama verlassen','Ingenieur-Arbeitsstation','Foto','360°-Panorama','{v} um 10 % erhöhen: Wie lautet das Ergebnis?','Gelände und Bilder werden geladen…','Satellitenbilder und Gelände geladen','Keine Verbindung; Offline-Szene','Koordinaten sind Näherungen','{n} von {m} Stationen erledigt','Quelle','Öffentliche Nennwerte oder Lehrannahmen'],
'pt':['Domínio','Local','Imagens online','Cena offline','Tela cheia','Ajuda','Seguir','Ombro','Primeira pessoa','Visão geral','Frente','Trás','Esquerda','Direita','Cima','Baixo','Grande angular','Ritmo','Recentrar','Resolver','Fechar','Calcular','Resultado','Entradas','Correto','Tente de novo','Abrir o curso completo ↗','Sair do panorama','Estação de engenharia','Fotografia','Panorama 360°','Aumente {v} em 10%: qual é o resultado?','Carregando terreno e imagens…','Imagens de satélite e relevo carregados','Sem conexão; usando a cena offline','As coordenadas são aproximadas','{n} de {m} estações concluídas','Fonte','Valores nominais públicos ou hipóteses didáticas'],
'ru':['Область','Объект','Онлайн-снимки','Офлайн-сцена','Во весь экран','Справка','Следовать','Из-за плеча','От первого лица','Обзор','Вперёд','Назад','Влево','Вправо','Вверх','Вниз','Широкий угол','Темп','Центрировать','Решить','Закрыть','Вычислить','Результат','Входные данные','Верно','Попробуйте ещё','Открыть полный курс ↗','Выйти из панорамы','Инженерная станция','Фотография','Панорама 360°','Увеличьте {v} на 10 %: каков результат?','Загрузка рельефа и снимков…','Спутниковые снимки и рельеф загружены','Нет связи; используется офлайн-сцена','Координаты приблизительные','Выполнено станций: {n} из {m}','Источник','Значения — публичные номиналы или учебные допущения'],
'ar':['المجال','الموقع','صور مباشرة','مشهد دون اتصال','ملء الشاشة','مساعدة','متابعة','فوق الكتف','منظور أول','نظرة عامة','أمام','خلف','يسار','يمين','أعلى','أسفل','زاوية واسعة','السرعة','إعادة التوسيط','معالجة','إغلاق','احسب','النتيجة','المدخلات','صحيح','حاول مجددًا','افتح الدورة الكاملة ↗','غادر البانوراما','محطة عمل هندسية','صورة فوتوغرافية','بانوراما 360°','ارفع {v} بنسبة 10٪: ما النتيجة؟','جارٍ تحميل التضاريس والصور…','تم تحميل صور الأقمار والتضاريس','لا يوجد اتصال؛ يُستخدم المشهد المحلي','الإحداثيات تقريبية','اكتملت {n} من {m} محطات','المصدر','القيم اسمية منشورة أو افتراضات تعليمية'],
'hi':['क्षेत्र','स्थल','ऑनलाइन चित्र','ऑफ़लाइन दृश्य','पूर्ण स्क्रीन','सहायता','अनुसरण','कंधे से','प्रथम पुरुष','ऊपर से','आगे','पीछे','बाएँ','दाएँ','ऊपर','नीचे','वाइड एंगल','गति','केंद्र में लाएँ','हल करें','बंद करें','गणना','परिणाम','इनपुट','सही','फिर सोचें','पूरा पाठ्यक्रम खोलें ↗','पैनोरमा छोड़ें','इंजीनियरिंग वर्कस्टेशन','तस्वीर','360° पैनोरमा','{v} को 10% बढ़ाएँ: परिणाम क्या होगा?','भू-आकृति और चित्र लोड हो रहे हैं…','उपग्रह चित्र और भू-आकृति लोड हुई','कनेक्शन नहीं; ऑफ़लाइन दृश्य','निर्देशांक अनुमानित हैं','{m} में से {n} वर्कस्टेशन पूरे','स्रोत','मान सार्वजनिक नाममात्र या शिक्षण मान्यताएँ हैं'],
'id':['Bidang','Lokasi','Citra daring','Adegan luring','Layar penuh','Bantuan','Ikuti','Bahu','Orang pertama','Tinjauan','Depan','Belakang','Kiri','Kanan','Atas','Bawah','Sudut lebar','Laju','Pusatkan','Tangani','Tutup','Hitung','Hasil','Masukan','Benar','Coba lagi','Buka kursus lengkap ↗','Keluar panorama','Stasiun kerja teknik','Foto','Panorama 360°','Naikkan {v} 10%: berapa hasilnya?','Memuat medan dan citra…','Citra satelit dan medan dimuat','Tidak ada koneksi; memakai adegan luring','Koordinat bersifat perkiraan','{n} dari {m} stasiun selesai','Sumber','Nilai nominal publik atau asumsi pengajaran'],
'vi':['Lĩnh vực','Địa điểm','Ảnh trực tuyến','Cảnh ngoại tuyến','Toàn màn hình','Trợ giúp','Theo sau','Qua vai','Góc nhìn thứ nhất','Toàn cảnh','Trước','Sau','Trái','Phải','Lên','Xuống','Góc rộng','Tốc độ','Căn giữa','Xử lý','Đóng','Tính','Kết quả','Đầu vào','Đúng','Thử lại','Mở khóa học đầy đủ ↗','Rời ảnh toàn cảnh','Trạm kỹ thuật','Ảnh chụp','Toàn cảnh 360°','Tăng {v} thêm 10%: kết quả là bao nhiêu?','Đang tải địa hình và ảnh…','Đã tải ảnh vệ tinh và địa hình','Không có kết nối; dùng cảnh ngoại tuyến','Tọa độ là gần đúng','Hoàn thành {n} / {m} trạm','Nguồn','Giá trị là số danh định công khai hoặc giả định giảng dạy']};
const NAMES={'zh-TW':'繁體中文','zh-CN':'简体中文','en':'English','ja':'日本語','ko':'한국어','es':'Español','fr':'Français','de':'Deutsch','pt':'Português','ru':'Русский','ar':'العربية','hi':'हिन्दी','id':'Bahasa Indonesia','vi':'Tiếng Việt'};
const HELP={
'zh-TW':'場景中的設備與道路是可行走的教學模型，不是現場三維掃描。照片館與全景則使用逐張標明來源的實拍素材。移動：WASD 或方向鍵（←→ 轉向），或左下搖桿；Shift 加速。環視：在畫面上拖曳；滾輪或「廣角」滑桿調整視角。前後左右上下六個按鈕會切到第一人稱並固定朝該方向廣角觀看。走近發光的工作站、照片或全景球，按 E 或畫面上的按鈕。線上實景會向第三方服務載入衛星影像、高程與 Wikimedia Commons 照片，並逐一標示來源；離線時只使用本機已授權的照片與全景。固定拍攝點的全景不能產生未拍攝的步行視差。',
'zh-CN':'移动：WASD 或方向键（←→ 转向），或左下摇杆；Shift 加速。环视：在画面上拖动；滚轮或“广角”滑杆调整视角。前后左右上下六个按钮会切到第一人称并固定朝该方向广角观看。走近发光的工作站、照片或全景球，按 E 或画面上的按钮。在线实景会向第三方服务加载卫星影像、高程与 Wikimedia Commons 照片并逐一标示来源；离线时只使用本机已授权的照片与全景。',
'en':'Equipment and roads are walkable teaching models, not surveyed reconstructions. The gallery and panoramas use credited real photographs. Move with WASD or the arrow keys (←→ turn) or the joystick at lower left; hold Shift to go faster. Look around by dragging on the scene; use the wheel or the wide-angle slider to change the field of view. The six buttons front, back, left, right, up and down switch to first person and hold a wide-angle look in that direction. Walk up to a glowing workstation, photograph or panorama sphere and press E or the on-screen button. Live imagery loads satellite imagery, elevation and Wikimedia Commons photographs from third-party services and credits each one; offline, only the credited local photographs and panoramas are used. A fixed-position panorama cannot supply walking parallax that was never captured.',
'ja':'移動：WASD または矢印キー（←→ で旋回）、左下のジョイスティック。Shift で加速。画面をドラッグして見回し、ホイールまたは「広角」スライダーで画角を調整します。前・後・左・右・上・下の6ボタンは一人称視点でその方向を広角で表示します。光るワークステーション、写真、パノラマ球に近づいて E または画面のボタンを押します。オンライン実景は第三者サービスから衛星画像・標高・Wikimedia Commons の写真を読み込み、出典を表示します。',
'ko':'이동: WASD 또는 방향키(←→ 회전), 왼쪽 아래 조이스틱. Shift로 가속. 화면을 끌어 둘러보고, 휠이나 “광각” 슬라이더로 시야각을 조절합니다. 앞·뒤·왼쪽·오른쪽·위·아래 여섯 버튼은 1인칭으로 해당 방향을 광각으로 고정합니다. 빛나는 워크스테이션, 사진, 파노라마 구에 다가가 E 또는 화면 버튼을 누르세요. 온라인 실경은 제3자 서비스에서 위성 영상, 고도, Wikimedia Commons 사진을 불러오며 출처를 표시합니다.',
'es':'Muévete con WASD o las flechas (←→ giran) o con el joystick inferior izquierdo; Mayús acelera. Arrastra sobre la escena para mirar; la rueda o el control «Gran angular» cambian el campo de visión. Los seis botones frente, atrás, izquierda, derecha, arriba y abajo pasan a primera persona con vista gran angular fija. Acércate a una estación, fotografía o esfera panorámica luminosa y pulsa E o el botón en pantalla. Las imágenes en línea cargan satélite, elevación y fotos de Wikimedia Commons de servicios de terceros y acreditan cada una.'};
const RTL=new Set(['ar']);
const params=new URLSearchParams(location.search);
const store={get(k){try{return localStorage.getItem(k)}catch{return null}},set(k,v){try{localStorage.setItem(k,v)}catch{}}};
function pickLanguage(){
  const wanted=[params.get('lang'),store.get('mg-rw-lang'),...(navigator.languages||[navigator.language||''])].filter(Boolean);
  for(const raw of wanted){const code=String(raw);if(WORDS[code])return code;const low=code.toLowerCase();
    if(low.startsWith('zh'))return /cn|sg|hans/.test(low)?'zh-CN':'zh-TW';
    const base=low.split('-')[0];if(WORDS[base])return base;}
  return 'en';
}
let lang=pickLanguage();
const zhLike=()=>lang==='zh-TW'||lang==='zh-CN';
const tr=(key,vars)=>{let s=(WORDS[lang]||WORDS.en)[KEYS.indexOf(key)]||WORDS.en[KEYS.indexOf(key)]||key;if(vars)for(const [k,v] of Object.entries(vars))s=s.replace('{'+k+'}',v);return s;};
const pick=(zh,en)=>zhLike()?zh:(en||zh);
const I18N=window.MG_SCENE_I18N_V31;
const ui=key=>{const i=I18N?.keys.indexOf(key);return (I18N?.ui[lang]||I18N?.ui.en||[])[i]||key;};
const domainName=d=>(I18N?.domains[lang]||I18N?.domains.en||[])[I18N?.ids.indexOf(d.id)]||pick(d.t,d.e);
const el=(tag,cls,text)=>{const e=document.createElement(tag);if(cls)e.className=cls;if(text!==undefined)e.textContent=text;return e;};
const clamp=(v,a,b)=>Math.max(a,Math.min(b,v));
const reduced=window.matchMedia?window.matchMedia('(prefers-reduced-motion: reduce)'):{matches:false};
const compact=Math.min(innerWidth,innerHeight)<560;

/* ---------- bounded arithmetic: numbers, names, + - * / **, parentheses, a few functions ---------- */
const FUNCTIONS={sqrt:Math.sqrt,sin:Math.sin,cos:Math.cos,tan:Math.tan,log:Math.log,log10:Math.log10,log2:Math.log2,exp:Math.exp,radians:x=>x*Math.PI/180,ceil:Math.ceil,floor:Math.floor,min:Math.min,max:Math.max,abs:Math.abs};
function calc(expression,variables){
  const src=String(expression);if(src.length>400)throw Error('expression too long');
  const tokens=src.match(/\s+|\d+\.?\d*(?:[eE][+-]?\d+)?|\.\d+|\*\*|[-+*/(),]|[^\s\d+\-*/(),.][^\s+\-*/(),]*/gu)||[];
  if(tokens.join('')!==src)throw Error('bad expression');
  const list=tokens.filter(t=>!/^\s+$/.test(t));let i=0,depth=0;
  const peek=()=>list[i],next=()=>list[i++];
  function primary(){
    if(++depth>40)throw Error('too deep');
    const t=next();let value;
    if(t===undefined)throw Error('unexpected end');
    if(t==='('){value=sum();if(next()!==')')throw Error('missing )');}
    else if(/^[\d.]/.test(t))value=Number(t);
    else if(t==='-')value=-power();
    else if(t==='+')value=power();
    else if(peek()==='('){const f=Object.hasOwn(FUNCTIONS,t)?FUNCTIONS[t]:null;if(!f)throw Error('unknown function');next();const args=[sum()];while(peek()===','){next();args.push(sum());}if(next()!==')')throw Error('missing )');value=f(...args);}
    else if(t==='pi')value=Math.PI;
    else if(Object.hasOwn(variables,t))value=Number(variables[t]);
    else throw Error('unknown name '+t);
    depth--;return value;
  }
  function power(){const base=primary();if(peek()==='**'){next();const sign=peek()==='-'?(next(),-1):1;return Math.pow(base,sign*power());}return base;}
  function product(){let v=power();while(peek()==='*'||peek()==='/'){const op=next(),r=power();v=op==='*'?v*r:v/r;}return v;}
  function sum(){let v=product();while(peek()==='+'||peek()==='-'){const op=next(),r=product();v=op==='+'?v+r:v-r;}return v;}
  const result=sum();if(i!==list.length||!Number.isFinite(result))throw Error('bad result');
  return result;
}
function show(value){const a=Math.abs(value);if(a===0)return '0';if(a>=1e6||a<1e-3)return value.toExponential(3);return value.toLocaleString('en-US',{maximumSignificantDigits:4});}

/* ---------- geography ---------- */
const EARTH=40075016.686,rad=d=>d*Math.PI/180;
const lonTile=(lng,z)=>(lng+180)/360*2**z;
const latTile=(lat,z)=>(1-Math.log(Math.tan(rad(lat))+1/Math.cos(rad(lat)))/Math.PI)/2*2**z;
const tileMetres=(lat,z)=>EARTH*Math.cos(rad(lat))/2**z;
const metresPerLat=111320,metresPerLng=lat=>111320*Math.cos(rad(lat));
function tileUrl(template,z,x,y){const n=2**z;return template.replace('{z}',z).replace('{x}',((x%n)+n)%n).replace('{y}',clamp(y,0,n-1));}
function loadImage(url,timeout=9000){return new Promise((resolve,reject)=>{const image=new Image();image.crossOrigin='anonymous';image.referrerPolicy='strict-origin-when-cross-origin';const timer=setTimeout(()=>{image.src='';reject(Error('timeout'))},timeout);image.onload=()=>{clearTimeout(timer);resolve(image)};image.onerror=()=>{clearTimeout(timer);reject(Error('image failed'))};image.src=url;});}

/* ---------- renderer and world ---------- */
const stage=$('rw-stage');
let renderer;
try{if(params.get('renderer')==='canvas')throw Error('requested compatibility mode');renderer=new T.WebGLRenderer({antialias:!compact,powerPreference:'high-performance'});}catch(error){if(!SC){loading.textContent='3D unavailable';return;}renderer=SC.canvasRenderer(T);document.body.classList.add('rw-software');}
renderer.setPixelRatio(Math.min(devicePixelRatio||1,compact?1.25:1.75));
if('outputColorSpace' in renderer)renderer.outputColorSpace=T.SRGBColorSpace;
stage.append(renderer.domElement);
const scene=new T.Scene();scene.background=new T.Color(0x9cc4dd);scene.fog=new T.Fog(0x9cc4dd,500,2600);
const camera=new T.PerspectiveCamera(62,1,.25,6000);
scene.add(new T.HemisphereLight(0xdcefff,0x4a5a44,1.25));
const sun=new T.DirectionalLight(0xfff2d8,1.6);sun.position.set(-300,520,260);scene.add(sun);
const world=new T.Group();scene.add(world);
const under=new T.Mesh(new T.PlaneGeometry(9000,9000),new T.MeshBasicMaterial({color:0x2b3a33}));under.userData.softwareIgnore=true;under.rotation.x=-Math.PI/2;under.position.y=-60;scene.add(under);
let ground=null,field=null,groundSize=1800,groundOffset={x:0,z:0};
const colorTexture=texture=>{if('colorSpace' in texture)texture.colorSpace=T.SRGBColorSpace;texture.anisotropy=Math.min(8,renderer.capabilities.getMaxAnisotropy());return texture;};
function heightAt(x,z){
  if(!field)return 0;
  const u=clamp((x-groundOffset.x)/groundSize+.5,0,1)*(field.n-1),v=clamp((z-groundOffset.z)/groundSize+.5,0,1)*(field.n-1);
  const x0=Math.floor(u),z0=Math.floor(v),x1=Math.min(field.n-1,x0+1),z1=Math.min(field.n-1,z0+1),fx=u-x0,fz=v-z0,h=field.h,n=field.n;
  return (h[z0*n+x0]*(1-fx)+h[z0*n+x1]*fx)*(1-fz)+(h[z1*n+x0]*(1-fx)+h[z1*n+x1]*fx)*fz;
}
function proceduralCanvas(domainIndex){
  const c=document.createElement('canvas');c.width=c.height=1024;const g=c.getContext('2d');
  const hue=(domainIndex*47+150)%360;g.fillStyle=`hsl(${hue} 18% 42%)`;g.fillRect(0,0,1024,1024);
  g.strokeStyle='rgba(255,255,255,.16)';g.lineWidth=1;for(let i=0;i<=1024;i+=32){g.beginPath();g.moveTo(i,0);g.lineTo(i,1024);g.moveTo(0,i);g.lineTo(1024,i);g.stroke();}
  g.strokeStyle='rgba(255,255,255,.4)';g.lineWidth=2;for(let r=80;r<=480;r+=80){g.beginPath();g.arc(512,512,r,0,Math.PI*2);g.stroke();}
  g.fillStyle='rgba(255,255,255,.8)';g.font='700 34px system-ui';g.textAlign='center';g.fillText('N',512,60);g.fillText('S',512,1004);g.fillText('E',992,524);g.fillText('W',32,524);
  return c;
}
let buildToken=0;
async function buildGround(origin,domainIndex,online){
  const token=++buildToken,segments=renderer.isSoftware?10:compact?48:88,n=segments+1,heights=new Float32Array(n*n);
  let canvas=null,size=1800,offset={x:0,z:0},live=false;
  if(online){
    try{
      const z=CFG.imageryZoom,tx=lonTile(origin.lng,z),ty=latTile(origin.lat,z),cx=Math.floor(tx),cy=Math.floor(ty),metres=tileMetres(origin.lat,z);
      const images=await Promise.all([-1,0,1].flatMap(dy=>[-1,0,1].map(dx=>loadImage(tileUrl(CFG.imagery,z,cx+dx,cy+dy)))));
      canvas=document.createElement('canvas');canvas.width=canvas.height=768;const g=canvas.getContext('2d');
      images.forEach((image,i)=>g.drawImage(image,(i%3)*256,Math.floor(i/3)*256,256,256));
      g.getImageData(0,0,1,1);
      size=metres*3;offset={x:-(tx-(cx+.5))*metres,z:-(ty-(cy+.5))*metres};live=true;
      try{
        const ez=CFG.elevationZoom,ex=lonTile(origin.lng,ez),ey=latTile(origin.lat,ez),tile=await loadImage(tileUrl(CFG.elevation,ez,Math.floor(ex),Math.floor(ey)));
        const ec=document.createElement('canvas');ec.width=ec.height=256;const eg=ec.getContext('2d',{willReadFrequently:true});eg.drawImage(tile,0,0,256,256);
        const px=eg.getImageData(0,0,256,256).data,em=tileMetres(origin.lat,ez);
        const sample=(u,v)=>{u=clamp(u,0,255);v=clamp(v,0,255);const x0=Math.floor(u),y0=Math.floor(v),x1=Math.min(255,x0+1),y1=Math.min(255,y0+1),fx=u-x0,fy=v-y0,at=(x,y)=>{const i=(y*256+x)*4;return px[i]*256+px[i+1]+px[i+2]/256-32768;};return (at(x0,y0)*(1-fx)+at(x1,y0)*fx)*(1-fy)+(at(x0,y1)*(1-fx)+at(x1,y1)*fx)*fy;};
        const u0=(ex-Math.floor(ex))*256,v0=(ey-Math.floor(ey))*256,base=sample(u0,v0);
        for(let j=0;j<n;j++)for(let i=0;i<n;i++){const wx=offset.x+(i/segments-.5)*size,wz=offset.z+(j/segments-.5)*size;heights[j*n+i]=clamp(sample(u0+wx/em*256,v0+wz/em*256)-base,-900,900);}
      }catch{/* flat ground with live imagery */}
    }catch{canvas=null;live=false;}
  }
  if(token!==buildToken)return null;
  if(!canvas){canvas=proceduralCanvas(domainIndex);size=1800;offset={x:0,z:0};heights.fill(0);}
  const geometry=new T.PlaneGeometry(size,size,segments,segments);geometry.rotateX(-Math.PI/2);
  const position=geometry.attributes.position;for(let k=0;k<position.count;k++)position.setY(k,heights[k]);
  position.needsUpdate=true;geometry.computeVertexNormals();
  const mesh=new T.Mesh(geometry,new T.MeshLambertMaterial({map:colorTexture(new T.CanvasTexture(canvas))}));mesh.position.set(offset.x,0,offset.z);
  if(ground){scene.remove(ground);ground.geometry.dispose();ground.material.map?.dispose();ground.material.dispose();}
  mesh.userData.softwareIgnore=true;ground=mesh;scene.add(mesh);field={n,h:heights};groundSize=size;groundOffset=offset;
  return {live};
}

/* ---------- avatar ---------- */
function makeAvatar(){
  const group=new T.Group(),suit=new T.MeshLambertMaterial({color:0x285e69}),vest=new T.MeshLambertMaterial({color:0xf3b954}),skin=new T.MeshLambertMaterial({color:0xe2b48c}),helmet=new T.MeshLambertMaterial({color:0xf0c859});
  const torso=new T.Mesh(new T.BoxGeometry(.52,.66,.3),vest);torso.position.y=1.12;group.add(torso);
  const head=new T.Mesh(new T.SphereGeometry(.17,16,12),skin);head.position.y=1.62;group.add(head);
  const hat=new T.Mesh(new T.SphereGeometry(.2,16,8,0,Math.PI*2,0,Math.PI/2),helmet);hat.position.y=1.66;group.add(hat);
  const limbs=[];
  for(const side of [-1,1]){
    const leg=new T.Group();leg.position.set(side*.14,.8,0);const shin=new T.Mesh(new T.BoxGeometry(.19,.8,.22),suit);shin.position.y=-.4;leg.add(shin);group.add(leg);
    const arm=new T.Group();arm.position.set(side*.34,1.4,0);const fore=new T.Mesh(new T.BoxGeometry(.14,.62,.16),suit);fore.position.y=-.31;arm.add(fore);group.add(arm);
    limbs.push({leg,arm,side});
  }
  return {group,limbs,torso,head};
}
const avatar=makeAvatar();scene.add(avatar.group);

/* ---------- state ---------- */
const VIEWS={follow:[.36,11,0],shoulder:[.17,5.2,1.25],first:[0,0,0],over:[1.1,95,0]};
const PACES=[3,6,15];
const state={sixFov:0,domain:null,site:null,origin:{lat:0,lng:0},online:false,live:false,view:'follow',yaw:0,pitch:.32,dist:14,fov:62,pace:0,pos:new T.Vector3(),heading:0,walk:0,manualUntil:0,objects:[],near:null,done:new Set(),pano:null,generation:0};
const keys=new Set(),joy={x:0,z:0};
let decor=null,route=[],routeLabel='',lastTelemetry=0,fullPhoto=null;
const PHOTO_FULL={'zh-TW':'全畫面照片','zh-CN':'全画面照片',en:'Full-window photo',ja:'写真を全画面表示',ko:'사진 전체 화면',es:'Foto a pantalla completa',fr:'Photo plein écran',de:'Foto im Vollbild',pt:'Foto em tela cheia',ru:'Фото на весь экран',ar:'صورة بملء الشاشة',hi:'पूर्ण स्क्रीन तस्वीर',id:'Foto layar penuh',vi:'Ảnh toàn màn hình'};
function closeFullPhoto(){if(!fullPhoto)return;fullPhoto.remove();fullPhoto=null;document.body.classList.remove('rw-photo-full');panel.querySelector('.rw-photo-full-button')?.focus();}
function openFullPhoto(media){closeFullPhoto();fullPhoto=el('section','rw-full-photo');fullPhoto.setAttribute('role','dialog');fullPhoto.setAttribute('aria-modal','true');fullPhoto.setAttribute('aria-label',pick(media.t,media.e));const bar=el('header'),name=el('h2','',pick(media.t,media.e)),close=el('button','',tr('close')+' ×');close.onclick=closeFullPhoto;bar.append(name,close);const image=el('img');image.src=media.src;image.alt=pick(media.t,media.e);image.referrerPolicy='strict-origin-when-cross-origin';const foot=el('footer');foot.append(creditLine(media));fullPhoto.append(bar,image,foot);document.body.append(fullPhoto);document.body.classList.add('rw-photo-full');close.focus();}

const EXTRA={
'zh-TW':['工作站','照片館','教學模型 · 非實地重建','3D 相容模式','行走到工作站','開啟工作站','WASD 移動 · 拖曳環視','停止導覽','請先計算，再回答下方問題。','輸入已變更，請重新計算。','請輸入有效數值。','實拍參考'],
'zh-CN':['工作站','照片馆','教学模型 · 非实地重建','3D 兼容模式','走到工作站','打开工作站','WASD 移动 · 拖动环视','停止导航','请先计算，再回答下方问题。','输入已变更，请重新计算。','请输入有效数值。','实拍参考'],
'en':['Stations','Photo gallery','Teaching model · not a site reconstruction','3D compatibility mode','Walk to station','Open workstation','WASD move · drag to look','Stop guide','Compute first, then answer the question below.','Inputs changed. Compute again.','Enter valid numbers.','Real photographs'],
'ja':['作業台','写真集','教材モデル・現地再現ではありません','3D互換モード','作業台へ歩く','作業台を開く','WASD 移動・ドラッグで見回す','案内を停止','計算してから解答してください。','入力が変わりました。再計算してください。','有効な数値を入力してください。','実写真'],
'ko':['작업대','사진 갤러리','교육 모형 · 현장 재구성 아님','3D 호환 모드','작업대로 이동','작업대 열기','WASD 이동 · 끌어서 보기','안내 중지','먼저 계산한 뒤 답하세요.','입력 변경. 다시 계산하세요.','유효한 숫자를 입력하세요.','실제 사진'],
'es':['Estaciones','Fotografías','Modelo didáctico · no reconstrucción','Modo 3D compatible','Caminar a la estación','Abrir estación','WASD mover · arrastrar para mirar','Detener guía','Calcula y responde abajo.','Datos cambiados. Calcula de nuevo.','Introduce números válidos.','Fotos reales'],
'fr':['Postes','Photographies','Maquette pédagogique · pas une reconstruction','Mode 3D compatible','Marcher vers le poste','Ouvrir le poste','WASD déplacer · glisser pour regarder','Arrêter le guide','Calculez puis répondez.','Entrées modifiées. Recalculez.','Saisissez des nombres valides.','Photos réelles'],
'de':['Stationen','Fotogalerie','Lehrmodell · keine Standortrekonstruktion','3D-Kompatibilitätsmodus','Zur Station gehen','Station öffnen','WASD bewegen · Ziehen zum Umsehen','Führung stoppen','Erst berechnen, dann antworten.','Eingaben geändert. Neu berechnen.','Gültige Zahlen eingeben.','Echte Fotos'],
'pt':['Estações','Fotografias','Modelo didático · sem reconstrução local','Modo 3D compatível','Caminhar à estação','Abrir estação','WASD mover · arrastar para olhar','Parar guia','Calcule e responda abaixo.','Entradas alteradas. Recalcule.','Insira números válidos.','Fotos reais'],
'ru':['Станции','Фотографии','Учебная модель · не реконструкция','Режим совместимости 3D','Идти к станции','Открыть станцию','WASD — ходьба · тянуть — обзор','Остановить маршрут','Сначала вычислите, затем ответьте.','Данные изменены. Пересчитайте.','Введите допустимые числа.','Реальные фотографии'],
'ar':['محطات','معرض الصور','نموذج تعليمي · ليس إعادة بناء للموقع','وضع توافق ثلاثي الأبعاد','المشي إلى المحطة','افتح المحطة','WASD حركة · اسحب للنظر','أوقف الدليل','احسب أولاً ثم أجب أدناه.','تغيرت المدخلات. أعد الحساب.','أدخل أرقامًا صالحة.','صور حقيقية'],
'hi':['स्टेशन','फ़ोटो संग्रह','शिक्षण मॉडल · स्थल का पुनर्निर्माण नहीं','3D संगत मोड','स्टेशन तक चलें','स्टेशन खोलें','WASD चलें · खींचकर देखें','मार्गदर्शन रोकें','पहले गणना करें, फिर उत्तर दें।','इनपुट बदले। फिर गणना करें।','सही संख्याएँ दर्ज करें।','वास्तविक तस्वीरें'],
'id':['Stasiun','Galeri foto','Model pengajaran · bukan rekonstruksi lokasi','Mode kompatibel 3D','Berjalan ke stasiun','Buka stasiun','WASD bergerak · tarik untuk melihat','Hentikan panduan','Hitung dahulu, lalu jawab.','Masukan berubah. Hitung ulang.','Masukkan angka valid.','Foto nyata'],
'vi':['Trạm','Ảnh chụp','Mô hình giảng dạy · không tái dựng địa điểm','Chế độ tương thích 3D','Đi tới trạm','Mở trạm','WASD di chuyển · kéo để nhìn','Dừng hướng dẫn','Tính trước, rồi trả lời.','Đầu vào thay đổi. Hãy tính lại.','Nhập số hợp lệ.','Ảnh thật']};
const tx=i=>(EXTRA[lang]||EXTRA.en)[i];
function clearDecor(){if(!decor)return;world.remove(decor.group);const materials=new Set();decor.group.traverse(n=>{n.geometry?.dispose();if(n.material)materials.add(n.material)});for(const m of materials)m.dispose();decor=null;}
function buildDecor(){clearDecor();if(!SC)return;decor=SC.create(T,state.domain.id,state.site.scene);decor.group.position.y=heightAt(0,0)+.12;world.add(decor.group);}
function resetRoute(){route=[];routeLabel='';}
function walkTo(o){route=[{x:0,z:state.pos.z},{x:0,z:o.z+3.2},{x:o.x,z:o.z+3.2}];routeLabel=pick(o.data.t,o.data.e);closePanel();setView('follow');}
function openStations(){const r=openPanel(tx(0));r.append(el('p','',tx(6)));for(const o of state.objects.filter(o=>o.kind==='station')){const row=el('section','rw-station-card');row.append(el('h3','',(state.done.has(o.key)?'✓ ':'')+pick(o.data.t,o.data.e)));const go=el('button','',tx(4)),open=el('button','',tx(5));go.onclick=()=>walkTo(o);open.onclick=()=>openStation(o);row.append(go,open);r.append(row);}}
function openGallery(){const r=openPanel(tx(1)),grid=el('div','rw-gallery');r.append(el('p','',ui('photoNote')));for(const m of D.assets[state.domain.id]||[]){const b=el('button','rw-thumb'),im=el('img');im.src=m.src;im.alt=pick(m.t,m.e);im.loading='lazy';b.append(im,el('span','',(m.p?'360° · ':'')+pick(m.t,m.e)));b.onclick=()=>m.p?enterPano(m):openPhoto(m);grid.append(b);}r.append(grid);}

const labelSprite=(text,color='#f3c75a',scale=7)=>{
  const c=document.createElement('canvas');c.width=512;c.height=128;const g=c.getContext('2d');g.fillStyle='rgba(8,20,28,.82)';g.beginPath();g.roundRect?g.roundRect(4,24,504,80,22):g.rect(4,24,504,80);g.fill();
  g.fillStyle=color;g.font='700 40px system-ui, "Noto Sans TC", sans-serif';g.textAlign='center';g.textBaseline='middle';let s=String(text);while(g.measureText(s).width>480&&s.length>4)s=s.slice(0,-2);if(s!==String(text))s+='…';g.fillText(s,256,65);
  const sprite=new T.Sprite(new T.SpriteMaterial({map:colorTexture(new T.CanvasTexture(c)),depthTest:false,transparent:true}));sprite.scale.set(scale,scale/4,1);sprite.renderOrder=5;return sprite;
};
function clearObjects(){for(const o of state.objects){world.remove(o.group);o.group.traverse(node=>{node.geometry?.dispose();if(node.material){node.material.map?.dispose();node.material.dispose();}});}state.objects=[];state.near=null;}
function place(group,x,z,lift=0){group.position.set(x,heightAt(x,z)+lift,z);}
function addObject(kind,group,x,z,data,radius){place(group,x,z);world.add(group);const object={kind,group,x,z,data,radius};state.objects.push(object);return object;}
function addStation(index,x,z,problem){
  const group=new T.Group(),base=new T.Mesh(new T.CylinderGeometry(.9,1.1,1.1,20),new T.MeshLambertMaterial({color:0x33464f}));base.position.y=.55;group.add(base);
  const screen=new T.Mesh(new T.BoxGeometry(1.5,1,.12),new T.MeshLambertMaterial({color:0x10242e,emissive:0x1d6f86,emissiveIntensity:.7}));screen.position.y=1.75;group.add(screen);
  const beacon=new T.Mesh(new T.SphereGeometry(.32,16,12),new T.MeshLambertMaterial({color:0xe8c26d,emissive:0x7a5a10,emissiveIntensity:.8}));beacon.position.y=2.7;group.add(beacon);
  const label=labelSprite(`${index+1} · ${pick(problem.t,problem.e)}`);label.position.y=3.7;group.add(label);
  const object=addObject('station',group,x,z,problem,4.2);if(decor)decor.obstacles.push({x,z,w:1.8,d:1.8});object.beacon=beacon;object.key=`${state.site.id}:${index}`;if(state.done.has(object.key))beacon.material.color.set(0x83e8ae);
  group.rotation.y=Math.atan2(-x,-z);return object;
}
function addPhoto(media,x,z,remote){
  const group=new T.Group(),width=11,height=7.4;
  const post=new T.Mesh(new T.BoxGeometry(.3,2.2,.3),new T.MeshLambertMaterial({color:0x2a3a42}));post.position.y=1.1;group.add(post);
  const frame=new T.Mesh(new T.BoxGeometry(width+.5,height+.5,.3),new T.MeshLambertMaterial({color:0x16262e}));frame.position.y=2.2+height/2;group.add(frame);
  const material=new T.MeshBasicMaterial({color:0x6d7f88}),picture=new T.Mesh(new T.PlaneGeometry(width,height),material);picture.position.set(0,2.2+height/2,.17);group.add(picture);
  const back=picture.clone();back.rotation.y=Math.PI;back.position.z=-.17;group.add(back);
  const loader=new T.TextureLoader();loader.setCrossOrigin('anonymous');const generation=state.generation;
  loader.load(media.src,texture=>{if(generation!==state.generation){texture.dispose();return;}colorTexture(texture);material.map=texture;material.color.set(0xffffff);material.needsUpdate=true;const ratio=texture.image.width/texture.image.height||1.5,w=Math.min(width,height*ratio),h=w/ratio;picture.scale.set(w/width,h/height,1);back.scale.copy(picture.scale);},undefined,()=>{});
  const label=labelSprite(pick(media.t,media.e),remote?'#bfe6ff':'#ffffff',9);label.position.y=2.2+height+1.5;group.add(label);
  const object=addObject('photo',group,x,z,media,9);group.rotation.y=Math.atan2(-x,-z);return object;
}
function addPano(media,x,z){
  const group=new T.Group(),ball=new T.Mesh(new T.SphereGeometry(1.9,24,16),new T.MeshLambertMaterial({color:0x8fd3ff,emissive:0x2a7fb0,emissiveIntensity:.9,transparent:true,opacity:.86}));ball.position.y=2.6;group.add(ball);
  const label=labelSprite('360° · '+pick(media.t,media.e),'#bfe6ff',9);label.position.y=5.6;group.add(label);
  return addObject('pano',group,x,z,media,5);
}
function problemsFor(site){
  if(R?.problems?.[site.id])return R.problems[site.id].map(p=>({...p,course:site}));
  if(state.domain.id==='energy'){
    const list=D.sites.energy,start=Math.max(0,list.findIndex(s=>s.id===site.id)),rows=[];
    for(let k=0;k<list.length&&rows.length<4;k++){const other=list[(start+k)%list.length];for(const p of D.problems.energy[other.id]||[]){if(rows.length<4)rows.push({...p,course:other});}}
    return rows;
  }
  return (D.problems.generic[state.domain.id]||[]).map(p=>({...p,course:site.c?site:null}));
}
function populate(remotePhotos){
  clearObjects();buildDecor();
  const marker=new T.Group(),beam=new T.Mesh(new T.CylinderGeometry(.08,.08,8,8),new T.MeshBasicMaterial({color:0xf3c75a,transparent:true,opacity:.75}));beam.position.y=4;marker.add(beam);
  const name=labelSprite(pick(state.site.t,state.site.e),'#ffffff',16);name.position.y=10;marker.add(name);addObject('marker',marker,0,-61,null,0);
  const problems=problemsFor(state.site);
  problems.forEach((p,i)=>{addStation(i,i%2===0?-4.6:4.6,-4-Math.floor(i/2)*13,p);});
  const media=D.assets[state.domain.id]||[],flats=media.filter(m=>!m.p).slice(0,compact?6:10),panos=media.filter(m=>m.p).slice(0,3);
  flats.forEach((m,i)=>{const a=Math.PI/2+(i-(flats.length-1)/2)*(Math.PI*1.3/Math.max(1,flats.length)),r=44+(i%2)*9;addPhoto(m,Math.cos(a)*r,Math.sin(a)*r,false);});
  panos.forEach((m,i)=>{const a=Math.PI+(i-(panos.length-1)/2)*.5;addPano(m,Math.cos(a)*26,Math.sin(a)*26);});
  (remotePhotos||[]).forEach((m,i)=>{
    let x,z;const limit=groundSize*.4;
    if(Number.isFinite(m.lat)&&Number.isFinite(m.lng)){x=(m.lng-state.origin.lng)*metresPerLng(state.origin.lat);z=-(m.lat-state.origin.lat)*metresPerLat;}
    if(!Number.isFinite(x)||Math.hypot(x,z)>limit||Math.hypot(x,z)<20){const a=i/Math.max(1,remotePhotos.length)*Math.PI*2,r=78+(i%3)*10;x=Math.cos(a)*r;z=Math.sin(a)*r;}
    addPhoto(m,x,z,true);
  });
  updateProgress();$('rw-stations').textContent=tx(0)+' · '+problems.length;$('rw-gallery-open').textContent=tx(1)+' · '+media.length;
}

/* ---------- Wikimedia Commons (credited, optional) ---------- */
const plain=html=>{const d=new DOMParser().parseFromString('<p>'+String(html||'')+'</p>','text/html');return (d.body.textContent||'').replace(/\s+/g,' ').trim().slice(0,160);};
async function commonsPhotos(site){
  const collect=async query=>{
    const url=CFG.commons+'?action=query&format=json&origin=*&prop=imageinfo%7Ccoordinates&iiprop=url%7Cextmetadata%7Cmime&iiurlwidth=960&coprop=type&colimit=50&'+query;
    const controller=new AbortController(),timer=setTimeout(()=>controller.abort(),9000);
    try{const response=await fetch(url,{signal:controller.signal,credentials:'omit',referrerPolicy:'strict-origin-when-cross-origin'});if(!response.ok)return [];const pages=Object.values((await response.json())?.query?.pages||{});
      return pages.map(page=>{const info=page.imageinfo?.[0],meta=info?.extmetadata||{},thumb=info?.thumburl||'',page_url=info?.descriptionurl||'';
        if(!/^image\/(jpeg|png)$/.test(info?.mime||'')||!/^https:\/\/upload\.wikimedia\.org\//.test(thumb)||!/^https:\/\/commons\.wikimedia\.org\//.test(page_url))return null;
        const license=plain(meta.LicenseShortName?.value);if(!license)return null;const title=String(page.title||'').replace(/^File:/,'').replace(/\.[a-z0-9]+$/i,'').replace(/_/g,' ').slice(0,120);
        return {id:'commons-'+page.pageid,src:thumb,p:0,t:title,e:title,by:plain(meta.Artist?.value)||'Wikimedia Commons contributor',lic:license,licUrl:/^https:\/\//.test(meta.LicenseUrl?.value||'')?meta.LicenseUrl.value:'',url:page_url,lat:page.coordinates?.[0]?.lat,lng:page.coordinates?.[0]?.lon,remote:true};}).filter(Boolean);
    }catch{return [];}finally{clearTimeout(timer);}
  };
  const lists=await Promise.all([site.q?collect('generator=categorymembers&gcmtype=file&gcmlimit=12&gcmtitle='+encodeURIComponent('Category:'+site.q)):Promise.resolve([]),collect(`generator=geosearch&ggsnamespace=6&ggsradius=10000&ggslimit=24&ggscoord=${site.lat}%7C${site.lng}`)]);
  const seen=new Set(),out=[];for(const item of lists.flat()){if(!seen.has(item.id)&&out.length<CFG.photoLimit){seen.add(item.id);out.push(item);}}
  return out;
}

/* ---------- site loading ---------- */
function updateProgress(){const stations=state.objects.filter(o=>o.kind==='station');$('rw-progress').textContent=stations.length?tr('progress',{n:stations.filter(o=>state.done.has(o.key)).length,m:stations.length}):'';}
function credit(){const parts=[];if(state.live)parts.push(CFG.imageryCredit,CFG.elevationCredit,ui('commonsCredits'));parts.push(ui('photoCredits'),tr('approx'));$('rw-credit').textContent=parts.join(' · ');}
async function loadSite(site,origin){
  resetRoute();const generation=++state.generation;state.site=site;state.origin=origin||{lat:site.lat,lng:site.lng};
  if(!origin){state.pos.set(0,0,10);state.heading=0;state.yaw=0;}
  $('rw-title').textContent=pick(site.t,site.e);
  $('rw-coords').textContent=`${state.origin.lat.toFixed(4)}°, ${state.origin.lng.toFixed(4)}° · ${tr('approx')}`;
  $('rw-status').textContent=state.online?tr('loading'):tr('offline');
  const link=$('rw-course');if(site.c){link.hidden=false;link.href='index.html#project/'+encodeURIComponent(site.c);link.textContent=pick(site.ct,site.ce)+' · '+tr('openCourse');}else link.hidden=true;
  const query=new URLSearchParams({domain:state.domain.id,site:site.id,lang});if(!state.online)query.set('online','0');try{history.replaceState(null,'',location.pathname+'?'+query);}catch{}
  const built=await buildGround(state.origin,D.domains.indexOf(state.domain),state.online);
  if(!built||generation!==state.generation)return;
  state.live=built.live;$('rw-status').textContent=state.online?(built.live?tr('onlineOk'):tr('onlineFail')):tr('offline');
  populate([]);credit();loading.hidden=true;
  if(built.live){const photos=await commonsPhotos({...site,lat:state.origin.lat,lng:state.origin.lng});if(generation===state.generation&&photos.length)populate(photos);}
}
function fillSites(){const select=$('rw-site');select.replaceChildren();for(const site of D.sites[state.domain.id]){const o=el('option','',pick(site.t,site.e));o.value=site.id;select.append(o);}}
function setDomain(id,siteId){
  state.domain=D.domains.find(d=>d.id===id)||D.domains.find(d=>d.id==='energy')||D.domains[0];$('rw-domain').value=state.domain.id;fillSites();
  const sites=D.sites[state.domain.id],site=sites.find(s=>s.id===siteId)||sites[0];$('rw-site').value=site.id;closePanel();loadSite(site);
}

/* ---------- panels ---------- */
const panel=$('rw-panel');
function closePanel(){document.body.classList.remove('rw-panel-open');panel.hidden=true;panel.replaceChildren();if(state.pano)leavePano();stage.focus({preventScroll:true});}
function openPanel(title){panel.replaceChildren();const close=el('button','rw-close','×');close.type='button';close.setAttribute('aria-label',tr('close'));close.onclick=closePanel;const heading=el('h2','',title);heading.id='rw-panel-title';panel.append(close,heading);panel.hidden=false;document.body.classList.add('rw-panel-open');close.focus({preventScroll:true});return panel;}
function creditLine(media){const p=el('p');p.append(el('small','',(media.by||'')+' · '));if(/^https:\/\//.test(media.licUrl||'')){const l=el('a','',media.lic||'Licence');l.href=media.licUrl;l.target='_blank';l.rel='noopener noreferrer';p.append(l);}else p.append(el('small','',media.lic||''));if(/^https:\/\//.test(media.url||'')){const a=el('a','',tr('source')+' ↗');a.href=media.url;a.target='_blank';a.rel='noopener noreferrer';p.append(document.createTextNode(' · '),a);}return p;}

function openPhoto(media){const root=openPanel(pick(media.t,media.e));const image=el('img');image.alt=pick(media.t,media.e);image.referrerPolicy='strict-origin-when-cross-origin';image.src=media.src;const full=el('button','rw-photo-full-button',PHOTO_FULL[lang]||PHOTO_FULL.en);full.onclick=()=>openFullPhoto(media);root.append(el('h3','',tr('photo')),image,full,creditLine(media));if(!media.remote)root.append(el('p','',ui('photoNote')));}
function openStation(object){
  const p=object.data,root=openPanel(pick(p.t,p.e));
  if(p.course)root.append(el('p','',pick(p.course.ct||p.course.t,p.course.ce||p.course.e)));
  root.append(el('h3','',tr('station')),el('p','rw-formula',p.f),el('p','',pick(p.m,p.me)),el('h3','',tr('inputs')));
  const recordKey='mg-rw31-inputs:'+object.key;let saved={};try{saved=JSON.parse(store.get(recordKey)||'{}')}catch{}
  const table=el('table'),inputs={};for(const [name,value] of Object.entries(p.v)){const row=el('tr'),cell=el('td'),input=el('input');input.type='number';input.step='any';input.value=String(Number.isFinite(saved[name])?saved[name]:value);input.setAttribute('aria-label',name);const b=p.bounds?.[name];if(b){if(Number.isFinite(b.min))input.min=String(b.min);if(Number.isFinite(b.max))input.max=String(b.max);if(b.integer)input.step='1';input.title=name+': '+(Number.isFinite(b.min)?(b.exclusiveMin?'> ':'≥ ')+b.min:'')+(Number.isFinite(b.max)?' · ≤ '+b.max:'');}inputs[name]=input;cell.append(input);if(b){const limits=(Number.isFinite(b.min)?String(b.min)+(b.exclusiveMin?' < ':' ≤ '):'')+name+(Number.isFinite(b.max)?' ≤ '+b.max:'')+(b.integer?' ∈ ℤ':'');cell.append(el('small','rw-bound',limits));}row.append(el('td','',name),cell,el('td','',(p.s?.[name]||'').replace(/^[-+\d.,eE\s]+/,'').replace(/\b(fraction|dimensionless)\b/g,'1')));table.append(row);}root.append(table);
  const unit=String(p.u||'').split('~')[zhLike()?0:1]??String(p.u||'').split('~')[0],result=el('p','rw-result',tx(8)),compute=el('button','rw-primary',tr('compute')),challenge=el('div','rw-challenge');let computed=false;compute.type='button';root.append(compute,result,challenge);
  const invalidate=()=>{computed=false;state.done.delete(object.key);store.set('mg-rw-done',JSON.stringify([...state.done]));object.beacon.material.color.set(0xe8c26d);object.beacon.material.emissive.set(0x7a5a10);result.textContent=tx(9);challenge.replaceChildren();updateProgress();};for(const i of Object.values(inputs))i.addEventListener('input',invalidate);
  compute.onclick=()=>{invalidate();try{const values={};for(const [k,i] of Object.entries(inputs)){if(!i.value.trim()||!Number.isFinite(Number(i.value)))throw Error('number');values[k]=Number(i.value);}if(SC&&!SC.validInputs(values,p.bounds))throw Error('bounds');const base=calc(p.x,values),changed={...values,[p.y]:values[p.y]*1.1};if(SC&&!SC.validInputs(changed,p.bounds)){result.textContent=`${tr('result')}: ${show(base)} ${unit}`;challenge.append(el('p','rw-bad',ui('sensitivityRange')));return;}const bumped=calc(p.x,changed);if(Math.abs(bumped-base)<1e-12*Math.max(1,Math.abs(base)))throw Error('degenerate');computed=true;store.set(recordKey,JSON.stringify(values));result.textContent=`${tr('result')}: ${show(base)} ${unit}`;challenge.append(el('h3','',tr('challenge',{v:p.y})));let options=[bumped,base,base+2*(bumped-base)];if(new Set(options.map(show)).size!==3)options=[bumped,bumped*1.1+1,bumped*.8-1];const box=el('div','rw-options'),feedback=el('p');feedback.setAttribute('role','status');for(const k of [1,2,0]){const b=el('button','',`${show(options[k])} ${unit}`);b.type='button';b.onclick=()=>{if(!computed)return;if(k===0){feedback.className='rw-ok';feedback.textContent=`${tr('correct')} · ${p.y} ×1.1 → ${show(bumped)} ${unit}`;state.done.add(object.key);object.beacon.material.color.set(0x83e8ae);object.beacon.material.emissive.set(0x2c7a4a);store.set('mg-rw-done',JSON.stringify([...state.done].slice(-1200)));updateProgress();}else{feedback.className='rw-bad';feedback.textContent=tr('wrong');}};box.append(b);}challenge.append(box,feedback);}catch(error){computed=false;result.textContent=error.message==='bounds'?ui('modelRange'):tx(10);}};
  root.append(el('p','rw-small',tr('teaching')+(zhLike()?'。':'.')));if(p.course?.c||p.course?.id){const a=el('a','',tr('openCourse'));a.href='index.html#project/'+encodeURIComponent(p.course.c||p.course.id);root.append(a);}
}

function enterPano(media){
  const root=openPanel('360° · '+pick(media.t,media.e));const leave=el('button','',tr('exitPano'));leave.type='button';leave.onclick=closePanel;root.append(creditLine(media),el('p','',ui('panoNote')),leave);
  const sphere=new T.Mesh(new T.SphereGeometry(400,48,32),new T.MeshBasicMaterial({color:0x223038,side:T.BackSide}));sphere.scale.x=-1;scene.add(sphere);
  state.pano={sphere,view:state.view};state.view='first';state.pitch=0;world.visible=false;under.visible=false;avatar.group.visible=false;if(ground)ground.visible=false;document.body.classList.add('rw-pano');panel.classList.add('rw-compact');
  new T.TextureLoader().load(media.src,texture=>{if(!state.pano||state.pano.sphere!==sphere){texture.dispose();return;}colorTexture(texture);sphere.material.map=texture;sphere.material.color.set(0xffffff);sphere.material.needsUpdate=true;},undefined,()=>{});
  refreshButtons();
}
function leavePano(){const p=state.pano;if(!p)return;scene.remove(p.sphere);p.sphere.geometry.dispose();p.sphere.material.map?.dispose();p.sphere.material.dispose();state.pano=null;world.visible=true;under.visible=true;if(ground)ground.visible=true;document.body.classList.remove('rw-pano');panel.classList.remove('rw-compact');setView(p.view==='first'?'follow':p.view);}
function interact(){const o=state.near;if(!o)return;if(o.kind==='station')openStation(o);else if(o.kind==='photo')openPhoto(o.data);else if(o.kind==='pano')enterPano(o.data);}

/* ---------- camera and controls ---------- */
function setView(view){if(!VIEWS[view])return;if(state.sixFov){setFov(state.sixFov);state.sixFov=0;}state.view=view;[state.pitch,state.dist]=VIEWS[view];if(view!=='first')state.yaw=state.heading;avatar.group.visible=view!=='first'&&!state.pano;refreshButtons();}
function lookSix(direction){
  state.view='first';avatar.group.visible=false;const turns={front:0,back:Math.PI,left:Math.PI/2,right:-Math.PI/2};
  if(direction in turns){state.yaw=state.heading+turns[direction];state.pitch=0;}else state.pitch=direction==='up'?1.35:-1.35;
  if(state.fov<96){state.sixFov=state.sixFov||state.fov;setFov(96);}state.manualUntil=performance.now()+60000;refreshButtons(direction);
}
function setFov(value){state.fov=clamp(Number(value)||62,40,120);$('rw-fov').value=String(Math.round(state.fov));$('rw-fov-out').textContent=Math.round(state.fov)+'°';}
function refreshButtons(six){document.querySelectorAll('[data-view]').forEach(b=>b.setAttribute('aria-pressed',String(b.dataset.view===state.view&&!six)));document.querySelectorAll('[data-six]').forEach(b=>b.setAttribute('aria-pressed',String(b.dataset.six===six)));}
function buildControls(){
  const views=$('rw-view-buttons'),six=$('rw-six');views.replaceChildren();six.replaceChildren();
  for(const v of ['follow','shoulder','first','over']){const b=el('button','',tr(v));b.type='button';b.dataset.view=v;b.onclick=()=>{state.manualUntil=0;setView(v)};views.append(b);}
  for(const d of ['front','back','left','right','up','down']){const b=el('button','',tr(d));b.type='button';b.dataset.six=d;b.onclick=()=>lookSix(d);six.append(b);}
  document.querySelectorAll('[data-rw]').forEach(e=>{e.textContent=tr(e.dataset.rw)});
  $('rw-online').textContent=tr('online');$('rw-online').setAttribute('aria-pressed',String(state.online));$('rw-full').textContent=tr('full');$('rw-help').textContent=tr('help');
  $('rw-cam').textContent=tr('wide')+' ▾';$('rw-stations').textContent=tx(0);$('rw-gallery-open').textContent=tx(1);$('rw-mode').textContent=tx(2)+(renderer.isSoftware?' · '+tx(3):'');$('rw-guide-stop').textContent=tx(7);$('rw-pace').textContent=`${tr('pace')} ${PACES[state.pace]} m/s`;$('rw-recenter').textContent=tr('recenter');$('rw-act').textContent=tr('act');
  const domains=$('rw-domain');domains.replaceChildren();for(const d of D.domains){const o=el('option','',domainName(d));o.value=d.id;domains.append(o);}if(state.domain)domains.value=state.domain.id;
  document.querySelector('.rw-skip').textContent=ui('skip');$('rw-stage').setAttribute('aria-label',ui('stage'));$('rw-joy').setAttribute('aria-label',ui('joystick'));$('rw-views').setAttribute('aria-label',ui('camera'));$('rw-info-toggle').setAttribute('aria-label',ui('toggleInfo'));$('rw-lang').setAttribute('aria-label',ui('language'));$('rw-lang').previousElementSibling.textContent=ui('language');loading.textContent=ui('loading');document.title=ui('stage')+' · MacGyver V31';
  document.documentElement.lang=lang==='zh-TW'?'zh-Hant':lang==='zh-CN'?'zh-Hans':lang;document.documentElement.dir=RTL.has(lang)?'rtl':'ltr';
  refreshButtons();
}
const languages=$('rw-lang');for(const [code,name] of Object.entries(NAMES)){const o=el('option','',name);o.value=code;languages.append(o);}languages.value=lang;
languages.onchange=()=>{lang=languages.value;store.set('mg-rw-lang',lang);buildControls();fillSites();if(state.site){$('rw-site').value=state.site.id;const site=state.site;closePanel();loadSite(site,state.origin);}};
$('rw-domain').onchange=event=>setDomain(event.target.value);
$('rw-stations').onclick=openStations;$('rw-gallery-open').onclick=openGallery;$('rw-guide-stop').onclick=resetRoute;
$('rw-info-toggle').onclick=()=>{const b=$('rw-info-toggle'),on=document.body.classList.toggle('rw-info-hidden');b.setAttribute('aria-pressed',String(on));};
$('rw-site').onchange=event=>{const site=D.sites[state.domain.id].find(s=>s.id===event.target.value);if(site){closePanel();loadSite(site);}};
$('rw-online').onclick=()=>{state.online=!state.online;store.set('mg-rw-online',state.online?'1':'0');buildControls();loadSite(state.site,state.origin);};
$('rw-full').onclick=()=>{const root=document.documentElement;if(document.fullscreenElement)document.exitFullscreen?.();else (root.requestFullscreen||root.webkitRequestFullscreen)?.call(root)?.catch?.(()=>{});};
$('rw-help').onclick=()=>{const root=openPanel(tr('help'));root.append(el('p','',ui('help')),el('p','',ui('modelScope')),el('p','',ui('languageScope')));};
$('rw-fov').oninput=event=>setFov(event.target.value);
$('rw-pace').onclick=()=>{state.pace=(state.pace+1)%PACES.length;buildControls();};
$('rw-recenter').onclick=()=>{state.manualUntil=0;state.yaw=state.heading;if(state.view==='first')state.pitch=0;else [state.pitch,state.dist]=VIEWS[state.view];setFov(62);refreshButtons();};
$('rw-act').onclick=interact;
$('rw-cam').onclick=()=>{const open=document.body.classList.toggle('rw-cam-open');$('rw-cam').setAttribute('aria-expanded',String(open));};
const MOVE={KeyW:[0,1],ArrowUp:[0,1],KeyS:[0,-1],ArrowDown:[0,-1],KeyA:[-1,0],KeyD:[1,0]};
addEventListener('keydown',event=>{if(fullPhoto){if(event.code==='Escape'){closeFullPhoto();event.preventDefault();}else if(event.code==='Tab'){const items=[...fullPhoto.querySelectorAll('button,a')];if(event.shiftKey&&event.target===items[0]){event.preventDefault();items.at(-1).focus();}else if(!event.shiftKey&&event.target===items.at(-1)){event.preventDefault();items[0].focus();}}return;}if(event.code==='Escape'){closePanel();document.body.classList.remove('rw-cam-open');$('rw-cam').setAttribute('aria-expanded','false');return;}if(event.code==='Tab'&&!panel.hidden){const items=[...panel.querySelectorAll('button,a,input,select,textarea')].filter(e=>!e.disabled&&!e.hidden);if(items.length){if(event.shiftKey&&event.target===items[0]){event.preventDefault();items.at(-1).focus();}else if(!event.shiftKey&&event.target===items.at(-1)){event.preventDefault();items[0].focus();}}return;}if(/^(INPUT|SELECT|TEXTAREA)$/.test(event.target.tagName))return;if(event.code==='KeyE'||event.code==='Enter'&&event.target===stage){interact();return;}if(MOVE[event.code]||event.code==='ArrowLeft'||event.code==='ArrowRight'||event.code==='ShiftLeft'||event.code==='ShiftRight'){keys.add(event.code);event.preventDefault();}});
addEventListener('keyup',event=>keys.delete(event.code));addEventListener('blur',()=>keys.clear());
let drag=null;
stage.addEventListener('pointerdown',event=>{drag={id:event.pointerId,x:event.clientX,y:event.clientY};stage.setPointerCapture?.(event.pointerId);});
stage.addEventListener('pointermove',event=>{if(!drag||drag.id!==event.pointerId)return;const dx=event.clientX-drag.x,dy=event.clientY-drag.y;drag.x=event.clientX;drag.y=event.clientY;state.yaw-=dx*.0052;state.pitch=clamp(state.pitch+(state.view==='first'?-1:1)*dy*.004,state.view==='first'?-1.45:.04,state.view==='first'?1.45:1.45);state.manualUntil=performance.now()+2500;refreshButtons();});
const endDrag=event=>{if(drag&&drag.id===event.pointerId)drag=null;};stage.addEventListener('pointerup',endDrag);stage.addEventListener('pointercancel',endDrag);
stage.addEventListener('wheel',event=>{event.preventDefault();if(state.view==='first'||state.pano)setFov(state.fov+Math.sign(event.deltaY)*4);else state.dist=clamp(state.dist*(1+Math.sign(event.deltaY)*.12),3,900);},{passive:false});
const pad=$('rw-joy'),stick=$('rw-stick');let padId=null;
const movePad=event=>{const r=pad.getBoundingClientRect(),x=(event.clientX-r.left-r.width/2)/(r.width/2),y=(event.clientY-r.top-r.height/2)/(r.height/2),m=Math.hypot(x,y),k=m>1?1/m:1;joy.x=x*k;joy.z=-y*k;stick.style.transform=`translate(${joy.x*30}px,${-joy.z*30}px)`;};
pad.addEventListener('pointerdown',event=>{padId=event.pointerId;pad.setPointerCapture?.(padId);movePad(event);event.preventDefault();});
pad.addEventListener('pointermove',event=>{if(event.pointerId===padId)movePad(event);});
const endPad=event=>{if(event.pointerId===padId){padId=null;joy.x=joy.z=0;stick.style.transform='';}};pad.addEventListener('pointerup',endPad);pad.addEventListener('pointercancel',endPad);
function resize(){const w=stage.clientWidth||innerWidth,h=stage.clientHeight||innerHeight;renderer.setSize(w,h,false);camera.aspect=w/h;camera.updateProjectionMatrix();}
addEventListener('resize',resize);addEventListener('orientationchange',resize);
function fitHud(){document.documentElement.style.setProperty('--rw-top-h',Math.ceil($('rw-top').getBoundingClientRect().height)+'px');}if(window.ResizeObserver)new ResizeObserver(fitHud).observe($('rw-top'));addEventListener('resize',fitHud);fitHud();

/* ---------- frame loop: the ground and the camera follow the footsteps ---------- */
let frames=0;
const clock=new T.Clock(),wanted=new T.Vector3(),aim=new T.Vector3(),look=new T.Vector3();let snap=true,lastNear='',recentering=false;
async function recentre(){
  if(recentering||!state.online||!state.live)return;recentering=true;
  const shiftX=state.pos.x,shiftZ=state.pos.z,origin={lat:state.origin.lat-shiftZ/metresPerLat,lng:state.origin.lng+shiftX/metresPerLng(state.origin.lat)};
  const built=await buildGround(origin,D.domains.indexOf(state.domain),true);
  if(built){state.origin=origin;state.live=built.live;state.pos.x-=shiftX;state.pos.z-=shiftZ;for(const o of state.objects){o.x-=shiftX;o.z-=shiftZ;place(o.group,o.x,o.z);}camera.position.x-=shiftX;camera.position.z-=shiftZ;aim.x-=shiftX;aim.z-=shiftZ;
    if(decor){decor.group.position.x-=shiftX;decor.group.position.z-=shiftZ;for(const b of decor.obstacles){b.x-=shiftX;b.z-=shiftZ;}}for(const p of route){p.x-=shiftX;p.z-=shiftZ;}
    $('rw-coords').textContent=`${origin.lat.toFixed(4)}°, ${origin.lng.toFixed(4)}° · ${tr('approx')}`;}
  recentering=false;
}
function frame(){
  requestAnimationFrame(frame);frames++;
  const dt=Math.min(clock.getDelta(),.35),now=performance.now();if(fullPhoto||document.hidden)return;
  if(keys.has('ArrowLeft')){state.yaw+=dt*1.9;state.manualUntil=now+900;}if(keys.has('ArrowRight')){state.yaw-=dt*1.9;state.manualUntil=now+900;}
  let ix=joy.x,iz=joy.z;for(const code of keys){const m=MOVE[code];if(m){ix+=m[0];iz+=m[1];}}
  if(Math.hypot(ix,iz)>.05)resetRoute();
  if(route.length&&!state.pano&&panel.hidden){const target=route[0],dx=target.x-state.pos.x,dz=target.z-state.pos.z,d=Math.hypot(dx,dz);if(d<.35)route.shift();else{state.yaw=Math.atan2(-dx,-dz);ix=0;iz=Math.min(1,d/(PACES[state.pace]*dt));}}
  const magnitude=Math.hypot(ix,iz);let moved=0;
  if(magnitude>.05&&!state.pano&&panel.hidden){
    const k=Math.min(1,magnitude)/magnitude,fx=-Math.sin(state.yaw),fz=-Math.cos(state.yaw),rx=Math.cos(state.yaw),rz=-Math.sin(state.yaw);
    const dx=(fx*iz+rx*ix)*k,dz=(fz*iz+rz*ix)*k,speed=PACES[state.pace]*(keys.has('ShiftLeft')||keys.has('ShiftRight')?2.2:1),limit=groundSize*.47;
    const next=SC?SC.move(state.pos.x,state.pos.z,dx*speed*dt,dz*speed*dt,decor?.obstacles||[]):{x:state.pos.x+dx*speed*dt,z:state.pos.z+dz*speed*dt};state.pos.x=clamp(next.x,groundOffset.x-limit,groundOffset.x+limit);state.pos.z=clamp(next.z,groundOffset.z-limit,groundOffset.z+limit);
    moved=speed*dt;const target=Math.atan2(-dx,-dz);let delta=target-state.heading;delta=Math.atan2(Math.sin(delta),Math.cos(delta));state.heading+=delta*(1-Math.exp(-dt*10));
    state.walk+=dt*(5+speed*.35);
    if(state.view!=='first'&&now>state.manualUntil){let follow=state.heading-state.yaw;follow=Math.atan2(Math.sin(follow),Math.cos(follow));if(Math.abs(follow)<2.6)state.yaw+=follow*(1-Math.exp(-dt*1.6));}
    if(Math.hypot(state.pos.x-groundOffset.x,state.pos.z-groundOffset.z)>groundSize*.3)recentre();
  }
  state.pos.y=heightAt(state.pos.x,state.pos.z);
  const swing=moved>0&&!reduced.matches?Math.sin(state.walk):0,bob=moved>0&&!reduced.matches?Math.abs(Math.sin(state.walk))*.07:0;
  avatar.group.position.set(state.pos.x,state.pos.y+bob,state.pos.z);avatar.group.rotation.y=state.heading;
  for(const l of avatar.limbs){l.leg.rotation.x=T.MathUtils.lerp(l.leg.rotation.x,swing*.62*l.side,.3);l.arm.rotation.x=T.MathUtils.lerp(l.arm.rotation.x,-swing*.5*l.side,.3);}
  avatar.torso.rotation.x=T.MathUtils.lerp(avatar.torso.rotation.x,moved>0?.07:0,.2);
  if(Math.abs(camera.fov-state.fov)>.05){camera.fov=T.MathUtils.lerp(camera.fov,state.fov,1-Math.exp(-dt*14));camera.updateProjectionMatrix();}
  const eye=state.pos.y+1.68;
  if(state.view==='first'||state.pano){
    camera.position.set(state.pos.x,eye+(state.pano?0:bob*.6),state.pos.z);if(state.pano)state.pano.sphere.position.copy(camera.position);
    look.set(-Math.sin(state.yaw)*Math.cos(state.pitch),Math.sin(state.pitch),-Math.cos(state.yaw)*Math.cos(state.pitch));aim.copy(camera.position).add(look);camera.up.set(0,1,0);if(Math.abs(state.pitch)>1.3)camera.up.set(-Math.sin(state.yaw),0,-Math.cos(state.yaw)).multiplyScalar(state.pitch>0?-1:1);camera.lookAt(aim);
  }else{
    const side=VIEWS[state.view][2];camera.up.set(0,1,0);
    wanted.set(state.pos.x+Math.sin(state.yaw)*state.dist*Math.cos(state.pitch)+Math.cos(state.yaw)*side,eye+Math.sin(state.pitch)*state.dist,state.pos.z+Math.cos(state.yaw)*state.dist*Math.cos(state.pitch)-Math.sin(state.yaw)*side);
    wanted.y=Math.max(wanted.y,heightAt(wanted.x,wanted.z)+1.2);
    const ease=snap||reduced.matches?1:1-Math.exp(-dt*9);camera.position.lerp(wanted,ease);aim.lerp(look.set(state.pos.x,eye-.3,state.pos.z),snap?1:1-Math.exp(-dt*12));camera.lookAt(aim);
  }
  snap=false;
  let near=null,best=Infinity;if(!state.pano)for(const o of state.objects){if(!o.radius)continue;const d=Math.hypot(o.x-state.pos.x,o.z-state.pos.z);if(d<o.radius&&d<best){best=d;near=o;}}
  state.near=near;const id=near?near.kind+near.x:'';
  if(id!==lastNear){lastNear=id;const prompt=$('rw-prompt'),act=$('rw-act');prompt.hidden=act.hidden=!near;if(near)prompt.textContent=`E · ${tr(near.kind==='station'?'station':near.kind)} — ${pick(near.data.t,near.data.e)}`;}
  for(const o of state.objects)if(o.kind==='pano')o.group.children[0].rotation.y+=dt*.6;
  if(decor&&!reduced.matches&&!state.pano)for(const a of decor.animations){if(a.sway)a.group.rotation[a.axis]=Math.sin(now/1400)*.15;else a.group.rotation[a.axis]+=a.speed*dt;}
  if(now-lastTelemetry>400){lastTelemetry=now;stage.dataset.renderer=renderer.isSoftware?'canvas':'webgl';stage.dataset.renderMs=String(Math.round(renderer.lastStats?.milliseconds||0));stage.dataset.renderFaces=String(renderer.lastStats?.faces||0);const heading=((state.yaw*180/Math.PI)%360+360)%360;$('rw-bearing').textContent=Math.round(heading)+'° · '+Math.round(state.pos.x)+' / '+Math.round(-state.pos.z)+' m';$('rw-guide-stop').hidden=!route.length;$('rw-guide-label').textContent=route.length?'→ '+routeLabel:tx(6);}
  renderer.render(scene,camera);
}

/* ---------- start ---------- */
try{for(const key of JSON.parse(store.get('mg-rw-done')||'[]'))if(typeof key==='string')state.done.add(key);}catch{}
state.online=params.get('online')==='0'?false:params.get('online')==='1'?true:store.get('mg-rw-online')==='0'?false:store.get('mg-rw-online')==='1'?true:!!CFG.online;
state.domain=D.domains[0];buildControls();resize();setFov(62);setView('follow');snap=true;
setDomain(params.get('domain')||(R?'materials':'energy'),params.get('site')||params.get('course')||'');
requestAnimationFrame(frame);
window.MG_RW_V30={state:()=>({renderer:renderer.isSoftware?'canvas':'webgl',renderStats:renderer.lastStats,decor:decor?.profile.name,route:route.length,completed:state.done.size,frames,domain:state.domain.id,site:state.site?.id,view:state.view,fov:Math.round(camera.fov),x:state.pos.x,z:state.pos.z,y:state.pos.y,yaw:state.yaw,pitch:state.pitch,heading:state.heading,online:state.online,live:state.live,objects:state.objects.map(o=>({kind:o.kind,x:o.x,z:o.z,remote:!!o.data?.remote})),near:state.near?.kind||null,pano:!!state.pano,origin:state.origin,groundSize,lang}),teleport:(x,z)=>{state.pos.x=x;state.pos.z=z;snap=true;},calc,interact,lookSix,setView,openStations,openGallery};window.MG_RW_V31=window.MG_RW_V30;
})();
