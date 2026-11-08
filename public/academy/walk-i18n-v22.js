/** V22 walk-room interface. Authored HUD dictionaries; course translation is a
 * separate, explicitly configured service. A recognized language without a
 * bundled HUD dictionary uses English; it is never labelled fully translated.
 */
import { resolveSupportedLanguage } from './locale.js';
import { EXTRA_WALK_ROWS_V25 } from './walk-extra-i18n-v25.js';

export const SUPPORTED_LANGUAGES_V22 = Object.freeze('zh-TW en zh-CN ja ko es fr de pt it nl ru uk pl cs sk sl hr sr bg ro hu el tr ar he fa ur hi bn ta te mr gu kn ml pa ne si th vi id ms fil km lo my mn kk uz az ka hy sw am ha yo ig zu af so sv no da fi is et lv lt ga cy mt sq mk bs eu gl ca eo'.split(' '));

export const UI_KEYS_V22 = Object.freeze('enter domains search role follow first overview interact approach guide task close next evidence choose complete saved exportRecord importRecord help fullscreen photos mentor move look zoom record journey home loading webglFallback modelScope language resetPosition pause resume narrate previous source machineTranslation untranslated controls objective notes saveNote shoulder recenter hideHud showHud'.split(' '));

// One ordered row per language keeps every locale's contract identical.
const rows = {
  'zh-TW': [
    '進入工程現場', '工程領域', '搜尋', '角色', '跟隨視角', '第一人稱', '總覽視角', '互動', '走近設備', '帶我前往', '任務', '關閉', '下一步', '觀察證據', '選擇', '完成', '已儲存', '匯出紀錄', '匯入紀錄', '操作說明', '全螢幕', '真實影像', 'AI 師傅', '移動', '環視', '縮放', '操作紀錄', '工程旅程', '學院首頁', '載入中…',
    '此裝置無法使用 WebGL，已切換至可行走的平面場景。',
    '可行走場景是教學模型；實拍與全景另外標示，並非量測重建。',
    '語言', '回到入口', '暫停', '繼續', '語音解說', '上一步', '來源與授權', '機器翻譯', '此內容尚未翻譯', '操作控制', '目前目標', '學習筆記', '儲存筆記',
  ],
  en: [
    'Enter the engineering world', 'Engineering domains', 'Search', 'Role', 'Follow camera', 'First person', 'Overview', 'Interact', 'Approach equipment', 'Guide me there', 'Task', 'Close', 'Next', 'Evidence', 'Choose', 'Complete', 'Saved', 'Export record', 'Import record', 'Help', 'Full screen', 'Real imagery', 'AI mentor', 'Move', 'Look around', 'Zoom', 'Activity record', 'Engineering journey', 'Academy home', 'Loading…',
    'WebGL is unavailable on this device. A walkable floor-plan scene is active.',
    'The walkable scene is a teaching model. Photos and panoramas are labelled separately; this is not a measured reconstruction.',
    'Language', 'Return to entrance', 'Pause', 'Resume', 'Narration', 'Previous', 'Sources and licenses', 'Machine translation', 'This content is not translated yet', 'Controls', 'Current objective', 'Learning notes', 'Save note',
  ],
  'zh-CN': [
    '进入工程现场', '工程领域', '搜索', '角色', '跟随视角', '第一人称', '总览视角', '互动', '走近设备', '带我前往', '任务', '关闭', '下一步', '观察证据', '选择', '完成', '已保存', '导出记录', '导入记录', '操作说明', '全屏', '真实影像', 'AI 导师', '移动', '环视', '缩放', '操作记录', '工程旅程', '学院首页', '加载中…',
    '此设备无法使用 WebGL，已切换至可行走的平面场景。',
    '可行走场景是教学模型；实拍与全景单独标示，并非测量重建。',
    '语言', '返回入口', '暂停', '继续', '语音讲解', '上一步', '来源与许可', '机器翻译', '此内容尚未翻译', '操作控制', '当前目标', '学习笔记', '保存笔记',
  ],
  ja: [
    '工学の現場に入る', '工学分野', '検索', '役割', '追従カメラ', '一人称視点', '俯瞰視点', '操作する', '設備に近づく', '案内して', '課題', '閉じる', '次へ', '観察資料', '選択', '完了', '保存済み', '記録を書き出す', '記録を読み込む', '操作説明', '全画面', '実写画像', 'AI 指導役', '移動', '見回す', 'ズーム', '操作記録', '工学の旅', '学院ホーム', '読み込み中…',
    'この端末では WebGL を利用できません。歩行可能な平面図に切り替えました。',
    '歩行空間は教材用モデルです。実写とパノラマは別途表示し、実測による再構成ではありません。',
    '言語', '入口に戻る', '一時停止', '再開', '音声解説', '前へ', '出典とライセンス', '機械翻訳', 'この内容は未翻訳です', '操作方法', '現在の目標', '学習メモ', 'メモを保存',
  ],
  ko: [
    '공학 현장 입장', '공학 분야', '검색', '역할', '추적 시점', '1인칭 시점', '전체 보기', '상호작용', '장비에 접근', '안내해 주세요', '과제', '닫기', '다음', '관찰 자료', '선택', '완료', '저장됨', '기록 내보내기', '기록 가져오기', '도움말', '전체 화면', '실제 사진', 'AI 멘토', '이동', '둘러보기', '확대 및 축소', '활동 기록', '공학 여정', '아카데미 홈', '불러오는 중…',
    '이 기기에서는 WebGL을 사용할 수 없어 이동 가능한 평면도로 전환했습니다.',
    '이동 공간은 교육용 모델입니다. 실제 사진과 파노라마는 별도로 표시하며 실측 복원 공간이 아닙니다.',
    '언어', '입구로 돌아가기', '일시 정지', '계속', '음성 해설', '이전', '출처 및 라이선스', '기계 번역', '아직 번역되지 않은 내용입니다', '조작 방법', '현재 목표', '학습 노트', '노트 저장',
  ],
  es: [
    'Entrar al mundo de ingeniería', 'Áreas de ingeniería', 'Buscar', 'Rol', 'Cámara de seguimiento', 'Primera persona', 'Vista general', 'Interactuar', 'Acercarse al equipo', 'Guíame', 'Tarea', 'Cerrar', 'Siguiente', 'Evidencias', 'Elegir', 'Completar', 'Guardado', 'Exportar registro', 'Importar registro', 'Ayuda', 'Pantalla completa', 'Imágenes reales', 'Mentor de IA', 'Moverse', 'Mirar alrededor', 'Acercar o alejar', 'Registro de actividad', 'Recorrido de ingeniería', 'Inicio de la academia', 'Cargando…',
    'Este dispositivo no admite WebGL. Se ha activado un plano transitable.',
    'El escenario transitable es un modelo educativo. Las fotos y panorámicas se identifican por separado; no es una reconstrucción medida.',
    'Idioma', 'Volver a la entrada', 'Pausar', 'Continuar', 'Narración', 'Anterior', 'Fuentes y licencias', 'Traducción automática', 'Este contenido aún no está traducido', 'Controles', 'Objetivo actual', 'Notas de aprendizaje', 'Guardar nota',
  ],
  fr: [
    'Entrer dans le monde technique', 'Domaines techniques', 'Rechercher', 'Rôle', 'Caméra de suivi', 'Vue à la première personne', 'Vue d’ensemble', 'Interagir', 'S’approcher de l’équipement', 'Me guider', 'Mission', 'Fermer', 'Suivant', 'Éléments observés', 'Choisir', 'Terminer', 'Enregistré', 'Exporter le journal', 'Importer le journal', 'Aide', 'Plein écran', 'Images réelles', 'Mentor IA', 'Se déplacer', 'Regarder autour', 'Zoomer', 'Journal d’activité', 'Parcours technique', 'Accueil de l’académie', 'Chargement…',
    'WebGL est indisponible sur cet appareil. Un plan parcourable est activé.',
    'La scène parcourable est un modèle pédagogique. Photos et panoramas sont signalés séparément ; il ne s’agit pas d’une reconstruction mesurée.',
    'Langue', 'Revenir à l’entrée', 'Pause', 'Reprendre', 'Narration', 'Précédent', 'Sources et licences', 'Traduction automatique', 'Ce contenu n’est pas encore traduit', 'Commandes', 'Objectif actuel', 'Notes d’apprentissage', 'Enregistrer la note',
  ],
  de: [
    'Technikwelt betreten', 'Ingenieurfachgebiete', 'Suchen', 'Rolle', 'Verfolgerkamera', 'Ich-Perspektive', 'Übersicht', 'Interagieren', 'Zum Gerät gehen', 'Dorthin führen', 'Aufgabe', 'Schließen', 'Weiter', 'Beobachtungsdaten', 'Auswählen', 'Abschließen', 'Gespeichert', 'Protokoll exportieren', 'Protokoll importieren', 'Hilfe', 'Vollbild', 'Echte Aufnahmen', 'KI-Mentor', 'Bewegen', 'Umschauen', 'Zoomen', 'Aktivitätsprotokoll', 'Technikreise', 'Akademie-Startseite', 'Wird geladen…',
    'WebGL ist auf diesem Gerät nicht verfügbar. Ein begehbarer Grundriss ist aktiv.',
    'Die begehbare Szene ist ein Lehrmodell. Fotos und Panoramen sind gesondert gekennzeichnet; dies ist keine vermessene Rekonstruktion.',
    'Sprache', 'Zum Eingang zurück', 'Pause', 'Fortsetzen', 'Sprachausgabe', 'Zurück', 'Quellen und Lizenzen', 'Maschinelle Übersetzung', 'Dieser Inhalt ist noch nicht übersetzt', 'Steuerung', 'Aktuelles Ziel', 'Lernnotizen', 'Notiz speichern',
  ],
  pt: [
    'Entrar no mundo da engenharia', 'Áreas de engenharia', 'Pesquisar', 'Papel', 'Câmara de acompanhamento', 'Primeira pessoa', 'Vista geral', 'Interagir', 'Aproximar-se do equipamento', 'Guiar até lá', 'Tarefa', 'Fechar', 'Seguinte', 'Evidências', 'Escolher', 'Concluir', 'Guardado', 'Exportar registo', 'Importar registo', 'Ajuda', 'Ecrã inteiro', 'Imagens reais', 'Mentor de IA', 'Mover', 'Olhar em redor', 'Ampliar ou reduzir', 'Registo de atividade', 'Percurso de engenharia', 'Início da academia', 'A carregar…',
    'O WebGL não está disponível neste dispositivo. Foi ativada uma planta navegável.',
    'O cenário navegável é um modelo educativo. Fotografias e panoramas são identificados separadamente; não é uma reconstrução por medição.',
    'Idioma', 'Voltar à entrada', 'Pausa', 'Retomar', 'Narração', 'Anterior', 'Fontes e licenças', 'Tradução automática', 'Este conteúdo ainda não foi traduzido', 'Controlos', 'Objetivo atual', 'Notas de aprendizagem', 'Guardar nota',
  ],
  it: [
    'Entra nel mondo dell’ingegneria', 'Settori di ingegneria', 'Cerca', 'Ruolo', 'Telecamera al seguito', 'Prima persona', 'Panoramica', 'Interagisci', 'Avvicinati all’attrezzatura', 'Guidami', 'Compito', 'Chiudi', 'Avanti', 'Dati osservati', 'Scegli', 'Completa', 'Salvato', 'Esporta registro', 'Importa registro', 'Aiuto', 'Schermo intero', 'Immagini reali', 'Mentore IA', 'Muoviti', 'Guarda intorno', 'Zoom', 'Registro attività', 'Percorso di ingegneria', 'Home dell’accademia', 'Caricamento…',
    'WebGL non è disponibile su questo dispositivo. È attiva una pianta percorribile.',
    'La scena percorribile è un modello didattico. Foto e panorami sono indicati separatamente; non è una ricostruzione misurata.',
    'Lingua', 'Torna all’ingresso', 'Pausa', 'Riprendi', 'Narrazione', 'Indietro', 'Fonti e licenze', 'Traduzione automatica', 'Questo contenuto non è ancora tradotto', 'Comandi', 'Obiettivo attuale', 'Appunti di studio', 'Salva appunto',
  ],
  ar: [
    'ادخل عالم الهندسة', 'المجالات الهندسية', 'بحث', 'الدور', 'كاميرا المتابعة', 'منظور الشخص الأول', 'نظرة عامة', 'تفاعل', 'اقترب من المعدات', 'أرشدني إلى هناك', 'مهمة', 'إغلاق', 'التالي', 'الأدلة المرصودة', 'اختيار', 'إكمال', 'تم الحفظ', 'تصدير السجل', 'استيراد السجل', 'مساعدة', 'ملء الشاشة', 'صور حقيقية', 'مرشد الذكاء الاصطناعي', 'تحرك', 'انظر حولك', 'تكبير وتصغير', 'سجل النشاط', 'رحلة هندسية', 'الرئيسية', 'جار التحميل…',
    'لا تتوفر WebGL على هذا الجهاز. تم تفعيل مخطط يمكن التجول فيه.',
    'المشهد القابل للتجول نموذج تعليمي. تُميز الصور والصور البانورامية بشكل منفصل؛ وليس إعادة بناء قائمة على القياس.',
    'اللغة', 'العودة إلى المدخل', 'إيقاف مؤقت', 'استئناف', 'تعليق صوتي', 'السابق', 'المصادر والتراخيص', 'ترجمة آلية', 'لم يُترجم هذا المحتوى بعد', 'عناصر التحكم', 'الهدف الحالي', 'ملاحظات التعلم', 'حفظ الملاحظة',
  ],
  hi: [
    'इंजीनियरिंग जगत में प्रवेश करें', 'इंजीनियरिंग क्षेत्र', 'खोजें', 'भूमिका', 'पीछा करने वाला कैमरा', 'प्रथम व्यक्ति दृश्य', 'समग्र दृश्य', 'इंटरैक्ट करें', 'उपकरण के पास जाएँ', 'मुझे वहाँ ले चलें', 'कार्य', 'बंद करें', 'अगला', 'अवलोकन के साक्ष्य', 'चुनें', 'पूरा करें', 'सहेजा गया', 'रिकॉर्ड निर्यात करें', 'रिकॉर्ड आयात करें', 'सहायता', 'पूरी स्क्रीन', 'वास्तविक चित्र', 'AI मार्गदर्शक', 'चलें', 'आसपास देखें', 'ज़ूम करें', 'गतिविधि रिकॉर्ड', 'इंजीनियरिंग यात्रा', 'अकादमी का मुखपृष्ठ', 'लोड हो रहा है…',
    'इस उपकरण पर WebGL उपलब्ध नहीं है। चलने योग्य समतल नक्शा सक्रिय है।',
    'चलने योग्य दृश्य एक शिक्षण मॉडल है। तस्वीरें और पैनोरमा अलग चिह्नित हैं; यह माप पर आधारित पुनर्निर्माण नहीं है।',
    'भाषा', 'प्रवेश द्वार पर लौटें', 'रोकें', 'फिर शुरू करें', 'आवाज़ में व्याख्या', 'पिछला', 'स्रोत और लाइसेंस', 'मशीनी अनुवाद', 'इस सामग्री का अभी अनुवाद नहीं हुआ है', 'नियंत्रण', 'वर्तमान लक्ष्य', 'अध्ययन के नोट्स', 'नोट सहेजें',
  ],
  vi: [
    'Vào thế giới kỹ thuật', 'Lĩnh vực kỹ thuật', 'Tìm kiếm', 'Vai trò', 'Góc nhìn theo nhân vật', 'Góc nhìn thứ nhất', 'Toàn cảnh', 'Tương tác', 'Đến gần thiết bị', 'Dẫn tôi đến đó', 'Nhiệm vụ', 'Đóng', 'Tiếp theo', 'Bằng chứng quan sát', 'Chọn', 'Hoàn thành', 'Đã lưu', 'Xuất nhật ký', 'Nhập nhật ký', 'Trợ giúp', 'Toàn màn hình', 'Hình ảnh thực tế', 'Người hướng dẫn AI', 'Di chuyển', 'Nhìn xung quanh', 'Thu phóng', 'Nhật ký hoạt động', 'Hành trình kỹ thuật', 'Trang chủ học viện', 'Đang tải…',
    'Thiết bị này không hỗ trợ WebGL. Đã chuyển sang sơ đồ mặt bằng có thể di chuyển.',
    'Không gian di chuyển là mô hình giảng dạy. Ảnh và ảnh toàn cảnh được ghi rõ riêng; đây không phải bản tái dựng từ đo đạc.',
    'Ngôn ngữ', 'Về lối vào', 'Tạm dừng', 'Tiếp tục', 'Thuyết minh', 'Trước', 'Nguồn và giấy phép', 'Dịch máy', 'Nội dung này chưa được dịch', 'Điều khiển', 'Mục tiêu hiện tại', 'Ghi chú học tập', 'Lưu ghi chú',
  ],
  id: [
    'Masuki dunia teknik', 'Bidang teknik', 'Cari', 'Peran', 'Kamera pengikut', 'Sudut pandang orang pertama', 'Tampilan keseluruhan', 'Berinteraksi', 'Dekati peralatan', 'Pandu saya ke sana', 'Tugas', 'Tutup', 'Berikutnya', 'Bukti pengamatan', 'Pilih', 'Selesaikan', 'Tersimpan', 'Ekspor catatan', 'Impor catatan', 'Bantuan', 'Layar penuh', 'Gambar nyata', 'Mentor AI', 'Bergerak', 'Lihat sekeliling', 'Perbesar atau perkecil', 'Catatan aktivitas', 'Perjalanan teknik', 'Beranda akademi', 'Memuat…',
    'WebGL tidak tersedia pada perangkat ini. Denah yang dapat dijelajahi telah diaktifkan.',
    'Ruang yang dapat dijelajahi adalah model pembelajaran. Foto dan panorama ditandai terpisah; ini bukan rekonstruksi hasil pengukuran.',
    'Bahasa', 'Kembali ke pintu masuk', 'Jeda', 'Lanjutkan', 'Narasi', 'Sebelumnya', 'Sumber dan lisensi', 'Terjemahan mesin', 'Konten ini belum diterjemahkan', 'Kontrol', 'Tujuan saat ini', 'Catatan belajar', 'Simpan catatan',
  ],
  th: [
    'เข้าสู่โลกวิศวกรรม', 'สาขาวิศวกรรม', 'ค้นหา', 'บทบาท', 'กล้องติดตามตัวละคร', 'มุมมองบุคคลที่หนึ่ง', 'มุมมองภาพรวม', 'โต้ตอบ', 'เข้าใกล้อุปกรณ์', 'พาฉันไปที่นั่น', 'ภารกิจ', 'ปิด', 'ถัดไป', 'หลักฐานที่สังเกต', 'เลือก', 'เสร็จสิ้น', 'บันทึกแล้ว', 'ส่งออกบันทึก', 'นำเข้าบันทึก', 'วิธีใช้งาน', 'เต็มหน้าจอ', 'ภาพจริง', 'ครู AI', 'เคลื่อนที่', 'มองรอบตัว', 'ซูม', 'บันทึกกิจกรรม', 'เส้นทางวิศวกรรม', 'หน้าหลักสถาบัน', 'กำลังโหลด…',
    'อุปกรณ์นี้ไม่รองรับ WebGL จึงเปลี่ยนเป็นแผนผังที่เดินสำรวจได้',
    'ฉากที่เดินสำรวจได้เป็นแบบจำลองเพื่อการเรียนรู้ ภาพถ่ายและภาพพาโนรามามีป้ายแยกต่างหาก ไม่ใช่การสร้างใหม่จากการวัด',
    'ภาษา', 'กลับไปทางเข้า', 'หยุดชั่วคราว', 'ดำเนินต่อ', 'เสียงบรรยาย', 'ก่อนหน้า', 'แหล่งที่มาและสัญญาอนุญาต', 'การแปลด้วยเครื่อง', 'เนื้อหานี้ยังไม่ได้แปล', 'การควบคุม', 'เป้าหมายปัจจุบัน', 'บันทึกการเรียนรู้', 'บันทึกโน้ต',
  ],
  tr: [
    'Mühendislik dünyasına gir', 'Mühendislik alanları', 'Ara', 'Rol', 'Takip kamerası', 'Birinci şahıs', 'Genel görünüm', 'Etkileşim', 'Ekipmana yaklaş', 'Beni oraya götür', 'Görev', 'Kapat', 'Sonraki', 'Gözlem kanıtları', 'Seç', 'Tamamla', 'Kaydedildi', 'Kaydı dışa aktar', 'Kaydı içe aktar', 'Yardım', 'Tam ekran', 'Gerçek görüntüler', 'Yapay zekâ rehberi', 'Hareket et', 'Etrafına bak', 'Yakınlaştır', 'Etkinlik kaydı', 'Mühendislik yolculuğu', 'Akademi ana sayfası', 'Yükleniyor…',
    'Bu cihazda WebGL kullanılamıyor. Gezinilebilir bir kat planı etkinleştirildi.',
    'Gezinilebilir sahne bir eğitim modelidir. Fotoğraflar ve panoramalar ayrıca işaretlenmiştir; ölçüme dayalı bir yeniden yapım değildir.',
    'Dil', 'Girişe dön', 'Duraklat', 'Sürdür', 'Sesli anlatım', 'Önceki', 'Kaynaklar ve lisanslar', 'Makine çevirisi', 'Bu içerik henüz çevrilmedi', 'Kontroller', 'Mevcut hedef', 'Öğrenme notları', 'Notu kaydet',
  ],
  ru: [
    'Войти в инженерный мир', 'Области инженерии', 'Поиск', 'Роль', 'Следящая камера', 'От первого лица', 'Общий вид', 'Взаимодействовать', 'Подойти к оборудованию', 'Провести меня', 'Задание', 'Закрыть', 'Далее', 'Данные наблюдений', 'Выбрать', 'Завершить', 'Сохранено', 'Экспорт журнала', 'Импорт журнала', 'Справка', 'Полный экран', 'Реальные изображения', 'ИИ-наставник', 'Двигаться', 'Осмотреться', 'Масштаб', 'Журнал действий', 'Инженерное путешествие', 'Главная академии', 'Загрузка…',
    'WebGL недоступен на этом устройстве. Включён план помещения с возможностью перемещения.',
    'Пространство для перемещения — учебная модель. Фото и панорамы отмечены отдельно; это не реконструкция по измерениям.',
    'Язык', 'Вернуться ко входу', 'Пауза', 'Продолжить', 'Озвучивание', 'Назад', 'Источники и лицензии', 'Машинный перевод', 'Этот материал ещё не переведён', 'Управление', 'Текущая цель', 'Учебные заметки', 'Сохранить заметку',
  ],
  uk: [
    'Увійти в інженерний світ', 'Галузі інженерії', 'Пошук', 'Роль', 'Камера стеження', 'Від першої особи', 'Загальний вигляд', 'Взаємодіяти', 'Підійти до обладнання', 'Провести мене', 'Завдання', 'Закрити', 'Далі', 'Дані спостережень', 'Вибрати', 'Завершити', 'Збережено', 'Експорт журналу', 'Імпорт журналу', 'Довідка', 'Повний екран', 'Реальні зображення', 'ШІ-наставник', 'Рухатися', 'Озирнутися', 'Масштаб', 'Журнал дій', 'Інженерна подорож', 'Головна академії', 'Завантаження…',
    'WebGL недоступний на цьому пристрої. Увімкнено план приміщення з можливістю пересування.',
    'Простір для пересування — навчальна модель. Фото й панорами позначено окремо; це не реконструкція за вимірюваннями.',
    'Мова', 'Повернутися до входу', 'Пауза', 'Продовжити', 'Озвучення', 'Назад', 'Джерела та ліцензії', 'Машинний переклад', 'Цей матеріал ще не перекладено', 'Керування', 'Поточна мета', 'Навчальні нотатки', 'Зберегти нотатку',
  ],
  pl: [
    'Wejdź do świata inżynierii', 'Dziedziny inżynierii', 'Szukaj', 'Rola', 'Kamera podążająca', 'Widok pierwszoosobowy', 'Widok ogólny', 'Interakcja', 'Podejdź do urządzenia', 'Poprowadź mnie', 'Zadanie', 'Zamknij', 'Dalej', 'Dane z obserwacji', 'Wybierz', 'Ukończ', 'Zapisano', 'Eksportuj dziennik', 'Importuj dziennik', 'Pomoc', 'Pełny ekran', 'Rzeczywiste zdjęcia', 'Mentor AI', 'Ruch', 'Rozejrzyj się', 'Powiększenie', 'Dziennik działań', 'Podróż inżynierska', 'Strona główna akademii', 'Ładowanie…',
    'WebGL jest niedostępny na tym urządzeniu. Włączono plan pomieszczenia z możliwością poruszania się.',
    'Scena do poruszania się jest modelem edukacyjnym. Zdjęcia i panoramy są oznaczone osobno; nie jest to rekonstrukcja pomiarowa.',
    'Język', 'Wróć do wejścia', 'Pauza', 'Wznów', 'Narracja', 'Wstecz', 'Źródła i licencje', 'Tłumaczenie maszynowe', 'Ta treść nie została jeszcze przetłumaczona', 'Sterowanie', 'Aktualny cel', 'Notatki z nauki', 'Zapisz notatkę',
  ],
  nl: [
    'Betreed de technische wereld', 'Technische vakgebieden', 'Zoeken', 'Rol', 'Volgcamera', 'Eerste persoon', 'Overzicht', 'Interactie', 'Nader de apparatuur', 'Breng me erheen', 'Opdracht', 'Sluiten', 'Volgende', 'Waarnemingsgegevens', 'Kiezen', 'Voltooien', 'Opgeslagen', 'Logboek exporteren', 'Logboek importeren', 'Help', 'Volledig scherm', 'Echte beelden', 'AI-mentor', 'Bewegen', 'Rondkijken', 'Zoomen', 'Activiteitenlogboek', 'Technische reis', 'Academie-startpagina', 'Laden…',
    'WebGL is niet beschikbaar op dit apparaat. Een beloopbare plattegrond is ingeschakeld.',
    'De beloopbare scène is een onderwijsmodel. Foto’s en panorama’s zijn apart gemarkeerd; dit is geen reconstructie op basis van metingen.',
    'Taal', 'Terug naar de ingang', 'Pauzeren', 'Hervatten', 'Gesproken uitleg', 'Vorige', 'Bronnen en licenties', 'Machinevertaling', 'Deze inhoud is nog niet vertaald', 'Bediening', 'Huidig doel', 'Studienotities', 'Notitie opslaan',
  ],
};

const cameraControls = {
  'zh-TW': ['肩後視角', '鏡頭回正', '收合工具', '顯示工具'],
  en: ['Over the shoulder', 'Recenter camera', 'Hide controls', 'Show controls'],
  'zh-CN': ['肩后视角', '镜头回正', '隐藏工具', '显示工具'],
  ja: ['肩越し視点', 'カメラを正面に戻す', '操作パネルを隠す', '操作パネルを表示'],
  ko: ['어깨너머 시점', '카메라 중앙 정렬', '조작 도구 숨기기', '조작 도구 표시'],
  es: ['Vista sobre el hombro', 'Recentrar cámara', 'Ocultar controles', 'Mostrar controles'],
  fr: ['Vue par-dessus l’épaule', 'Recentrer la caméra', 'Masquer les commandes', 'Afficher les commandes'],
  de: ['Schulterperspektive', 'Kamera zentrieren', 'Steuerung ausblenden', 'Steuerung einblenden'],
  pt: ['Vista por cima do ombro', 'Recentrar a câmara', 'Ocultar controlos', 'Mostrar controlos'],
  it: ['Visuale da dietro la spalla', 'Ricentra la telecamera', 'Nascondi i comandi', 'Mostra i comandi'],
  ar: ['منظور فوق الكتف', 'إعادة توسيط الكاميرا', 'إخفاء عناصر التحكم', 'إظهار عناصر التحكم'],
  hi: ['कंधे के ऊपर से दृश्य', 'कैमरा केंद्रित करें', 'नियंत्रण छिपाएँ', 'नियंत्रण दिखाएँ'],
  vi: ['Góc nhìn qua vai', 'Đưa máy quay về giữa', 'Ẩn điều khiển', 'Hiện điều khiển'],
  id: ['Tampilan dari balik bahu', 'Pusatkan kamera', 'Sembunyikan kontrol', 'Tampilkan kontrol'],
  th: ['มุมมองข้ามไหล่', 'จัดกล้องให้อยู่กึ่งกลาง', 'ซ่อนตัวควบคุม', 'แสดงตัวควบคุม'],
  tr: ['Omuz üstü görünüm', 'Kamerayı ortala', 'Kontrolleri gizle', 'Kontrolleri göster'],
  ru: ['Вид из-за плеча', 'Центрировать камеру', 'Скрыть управление', 'Показать управление'],
  uk: ['Вид з-за плеча', 'Відцентрувати камеру', 'Приховати керування', 'Показати керування'],
  pl: ['Widok znad ramienia', 'Wyśrodkuj kamerę', 'Ukryj sterowanie', 'Pokaż sterowanie'],
  nl: ['Over de schouder', 'Camera centreren', 'Bediening verbergen', 'Bediening tonen'],
};

for (const [lang, values] of Object.entries(EXTRA_WALK_ROWS_V25)) {
  if (values.length !== UI_KEYS_V22.length) throw new Error(`Incomplete V25 HUD dictionary: ${lang}`);
  rows[lang] = values.slice(0, 45);
  cameraControls[lang] = values.slice(45);
}

export const UI_LANGUAGES_V22 = Object.freeze(Object.fromEntries(Object.entries(rows).map(([lang, row]) => {
  const values = [...row, ...cameraControls[lang]];
  if (values.length !== UI_KEYS_V22.length) throw new Error(`Incomplete V22 HUD dictionary: ${lang}`);
  return [lang, Object.freeze(Object.fromEntries(UI_KEYS_V22.map((key, i) => [key, values[i]])))];
})));

/** Resolve saved choice first, then browser languages in priority order. */
export function resolveLanguage(preference = 'auto', navigatorLanguages) {
  return resolveSupportedLanguage(preference, navigatorLanguages, SUPPORTED_LANGUAGES_V22);
}

/** Labels for the 79 recognized choices, with native names when Intl supports them. */
export function languageChoices(displayLanguage = null) {
  return SUPPORTED_LANGUAGES_V22.map(code => {
    let label = code;
    try { label = new Intl.DisplayNames([displayLanguage || code], { type: 'language' }).of(code) || code; } catch { /* old browsers retain the language code */ }
    return { code, value: code, label, bundled: Object.hasOwn(UI_LANGUAGES_V22, code) };
  });
}

/** English fallback is explicit and deterministic; unknown keys remain visible. */
export function uiText(language, key) {
  const code = resolveLanguage(language, []);
  return UI_LANGUAGES_V22[code]?.[key] ?? UI_LANGUAGES_V22.en[key] ?? String(key);
}
