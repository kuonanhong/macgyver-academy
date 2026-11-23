/* Original educational narration, 2026-11-23. Technical reference links are included;
 * illustrations and flight paths are teaching reconstructions, not vendor layouts. */
(function (root) {
  'use strict';
  const languages = [
    {id:'zh-TW',label:'繁體中文',speech:'zh-TW'},
    {id:'en',label:'English',speech:'en-US'},
    {id:'ja',label:'日本語',speech:'ja-JP'},
    {id:'ko',label:'한국어',speech:'ko-KR'},
    {id:'zh-CN',label:'简体中文',speech:'zh-CN'}
  ];
  const L = (tw,en,ja,ko,cn) => ({'zh-TW':tw,en,ja,ko,'zh-CN':cn});
  const labels = {
    substrate:L('有機封裝基板','Organic substrate','有機パッケージ基板','유기 패키지 기판','有机封装基板'),
    logic:L('運算晶粒','Compute die','演算ダイ','연산 다이','计算晶粒'),
    hbm:L('HBM 堆疊記憶體','Stacked HBM memory','積層 HBM メモリー','적층 HBM 메모리','HBM 堆叠内存'),
    interposer:L('矽中介層與 TSV','Silicon interposer + TSVs','シリコンインターポーザーと TSV','실리콘 인터포저와 TSV','硅中介层与 TSV'),
    microbumps:L('微凸塊互連','Microbump interface','マイクロバンプ接続','마이크로범프 연결','微凸块互连'),
    die:L('嵌入模封的晶粒','Embedded die','封止材に埋め込まれたダイ','몰드에 내장된 다이','嵌入模封的晶粒'),
    mold:L('模封材料','Mold compound','モールド封止材','몰딩 재료','模封材料'),
    rdl:L('扇出重佈線層 RDL','Fan-out redistribution layers','ファンアウト再配線層 RDL','팬아웃 재배선층 RDL','扇出重布线层 RDL'),
    fanout:L('互連延伸至晶粒外','Connections extend beyond die','ダイの外へ広がる接続','다이 밖으로 확장된 연결','互连延伸至晶粒外'),
    'bottom-die':L('下層主動晶粒','Lower active die','下層のアクティブダイ','하부 능동 다이','下层有源晶粒'),
    bond:L('平面銅與介電層混合鍵合','Planar copper + dielectric bonds','平面の銅・絶縁層ハイブリッド接合','평면 구리·유전체 하이브리드 본딩','平面铜与介电层混合键合'),
    'top-die':L('直接鍵合的上層晶粒','Directly bonded upper die','直接接合された上層ダイ','직접 접합된 상부 다이','直接键合的上层晶粒'),
    bridge:L('局部嵌入式矽橋','Local silicon bridge','局所埋込みシリコンブリッジ','국소 내장형 실리콘 브리지','局部嵌入式硅桥'),
    dies:L('相鄰運算晶粒','Neighbouring logic dies','隣接する演算ダイ','인접한 연산 다이','相邻计算晶粒'),
    organic:L('有機基板上的其餘走線','Routing through organic substrate','有機基板を通るその他の配線','유기 기판을 지나는 나머지 배선','有机基板上的其余走线'),
    io:L('I/O 中樞晶粒','I/O hub','I/O ハブダイ','I/O 허브 다이','I/O 枢纽晶粒'),
    chiplet:L('運算小晶片','Compute chiplet','演算チップレット','연산 칩렛','计算小芯片'),
    link:L('晶粒間實體互連','Die-to-die physical links','ダイ間の物理接続','다이 간 물리 연결','晶粒间实体互连'),
    ecosystem:L('協定、封裝與驗證協作','Protocol, packaging and validation','プロトコル・パッケージ・検証の連携','프로토콜·패키징·검증 협력','协议、封装与验证协作'),
    source:L('運算與記憶體熱源','Compute and memory heat sources','演算部とメモリーの熱源','연산부와 메모리의 열원','计算与内存热源'),
    tim:L('導熱介面材料 TIM','Thermal interface material','熱界面材料 TIM','열 계면 재료 TIM','导热界面材料 TIM'),
    lid:L('均熱蓋','Heat spreader','ヒートスプレッダー','히트 스프레더','均热盖'),
    cooler:L('鰭片將熱帶入氣流','Fins move heat into airflow','フィンから気流へ放熱','핀에서 공기 흐름으로 방열','鳍片将热带入气流')
  };
  const views = ['overview','architecture','interconnect','assembly','cross-section','signal','thermal','inspection','tradeoff','roadmap'];
  const C = (title,text) => ({title,text});
  const sourceLibrary = {
    cowos:{title:'TSMC — CoWoS',url:'https://3dfabric.tsmc.com/english/dedicatedFoundry/technology/cowos.htm'},
    info:{title:'TSMC — Integrated Fan-Out',url:'https://3dfabric.tsmc.com/english/dedicatedFoundry/technology/InFO.htm'},
    soic:{title:'TSMC — SoIC',url:'https://3dfabric.tsmc.com/english/dedicatedFoundry/technology/SoIC.htm'},
    intel:{title:'Intel Foundry — Advanced Packaging',url:'https://www.intel.com/content/www/us/en/foundry/packaging.html'},
    fanout:{title:'ASE — Fan-Out Packaging',url:'https://ase.aseglobal.com/fan-out-packaging/'},
    ucie:{title:'UCIe Consortium — Specifications',url:'https://www.uciexpress.org/specifications'},
    stress:{title:'ASE — Stress and Thermal Lab',url:'https://ase.aseglobal.com/lab-services/stress-and-thermal-lab/'},
    test:{title:'ASE — Test Services',url:'https://ase.aseglobal.com/test-services/'}
  };
  const T = (id,title,summary,refs,chapters) => ({id,title,summary,duration:300,
    sources:refs.map(key=>sourceLibrary[key]),
    chapters:chapters.map((c,i)=>Object.assign(c,{id:id+'-'+(i+1),start:i*30,end:(i+1)*30,view:views[i]}))});
  const tours = [
    T('interposer',
      L('2.5D 矽中介層與 HBM','2.5D interposer & HBM','2.5D インターポーザーと HBM','2.5D 인터포저와 HBM','2.5D 硅中介层与 HBM'),
      L('把運算晶片與記憶體放在共同的精密佈線平台上，沿著資料、供電與散熱路徑看懂系統。','A shared fine-routing platform joins compute and memory. Follow data, power and heat through the package.','演算とメモリーを共通の微細配線基盤で接続し、データ・電力・熱の経路をたどります。','연산과 메모리를 미세 배선 플랫폼으로 연결하고 데이터·전력·열의 경로를 살펴봅니다.','把计算芯片与内存放在共同的精密布线平台上，沿着数据、供电与散热路径看懂系统。'),
      ['cowos','stress','test'],[
      C(L('先看整座晶片城市','Read the chip city','チップの街を見渡す','칩 도시를 내려다보기','先看整座芯片城市'),L(
        '先從上方看：中央是運算晶片，周圍是 HBM 記憶體堆疊，下方共同的平台是矽中介層。這個教學場景把微小封裝放大成一座城市；先找出「誰負責計算、誰存資料、誰把兩者連起來」，再靠近細節。',
        'Start overhead: a compute die sits beside HBM memory stacks, all supported by a silicon interposer. This teaching scene enlarges a tiny package into a city. First identify who computes, who stores data and who connects them; then descend into the details.',
        '上空から、演算ダイ、周囲の HBM メモリースタック、その下のシリコンインターポーザーを見ます。小さなパッケージを街に見立てた教材です。まず計算、記憶、接続の役割を見分けてから、細部へ近づきましょう。',
        '위에서 보면 연산 다이 옆에 HBM 메모리 스택이 있고, 아래에는 실리콘 인터포저가 있습니다. 작은 패키지를 도시처럼 확대한 교육 장면입니다. 먼저 계산, 저장, 연결을 담당하는 부분을 구분한 뒤 세부 구조로 내려갑니다.',
        '先从上方看：中央是计算芯片，周围是 HBM 内存堆叠，下方共同的平台是硅中介层。这个教学场景把微小封装放大成一座城市；先找出谁负责计算、谁存数据、谁把两者连起来，再靠近细节。')),
      C(L('三層不是同一種板','Three different levels','三つの層の役割','서로 다른 세 층','三层不是同一种板'),L(
        '鏡頭降低，分清晶粒、中介層與封裝基板。中介層承接高密度晶粒間連線；基板把訊號與電源帶往電路板。這裡講的是矽中介層型 2.5D 結構，不能把所有 CoWoS 變體都畫成同一片矽板。',
        'Lower the camera and separate the dies, interposer and package substrate. The interposer handles dense die-to-die routing; the substrate connects the assembly to the circuit board. This tour represents silicon-interposer 2.5D packaging, not every CoWoS variant, which can use different interconnect structures.',
        'ダイ、インターポーザー、パッケージ基板を分けて見ます。インターポーザーは高密度のダイ間配線、基板は回路基板への接続を担います。この映像はシリコン型 2.5D の教材であり、構造の異なる CoWoS の全方式を表すものではありません。',
        '다이, 인터포저, 패키지 기판을 구분합니다. 인터포저는 고밀도 다이 간 배선을, 기판은 회로 보드 연결을 담당합니다. 여기서는 실리콘 인터포저 기반 2.5D를 보여 줍니다. 구조가 다른 모든 CoWoS 변형을 하나의 실리콘 판으로 이해하면 안 됩니다.',
        '镜头降低，分清晶粒、中介层与封装基板。中介层承接高密度晶粒间连线；基板把信号与电源带往电路板。这里讲的是硅中介层型 2.5D 结构，不能把所有 CoWoS 变体都画成同一片硅板。')),
      C(L('短而寬的資料道路','Short, wide data routes','短く幅広いデータ経路','짧고 넓은 데이터 경로','短而宽的数据道路'),L(
        '沿著晶片邊緣飛行，注意並行連線如何跨向 HBM。高頻寬不只靠單條線變快，也靠許多通道合作。發光線代表連接關係，不是電子的真實速度；實際設計還要計算寄生效應、串擾與時序裕量。',
        'Fly along the die edges and follow parallel connections toward HBM. Bandwidth comes from many channels working together, not simply from accelerating one wire. Glowing routes show connectivity rather than electron speed. Real design also evaluates parasitics, crosstalk and timing margin.',
        'ダイの縁に沿って飛び、HBM へ向かう並列配線を追います。帯域幅は一本の高速化だけでなく、多数の経路の協調でも得られます。光は接続の表現です。実設計では寄生成分、クロストーク、タイミング余裕も評価します。',
        '다이 가장자리를 따라 HBM으로 이어지는 병렬 배선을 봅니다. 대역폭은 한 선의 속도뿐 아니라 여러 채널의 협력으로 확보됩니다. 빛은 연결 관계를 나타내며 전자의 실제 속도가 아닙니다. 기생 성분, 누화, 타이밍 여유도 검토해야 합니다.',
        '沿着芯片边缘飞行，注意并行连线如何跨向 HBM。高带宽不只靠单条线变快，也靠许多通道合作。发光线代表连接关系，不是电子的真实速度；实际设计还要计算寄生效应、串扰与时序裕量。')),
      C(L('組裝前先把風險分開','Separate assembly risks','組立前にリスクを分ける','조립 전에 위험 분리','组装前先把风险分开'),L(
        '把整體拆成待組裝的晶粒、中介層與基板。先檢查各元件，再規劃貼合、填膠與接合後測試，能避免到最後才發現昂貴的缺陷。這是概念流程；實際先後順序與材料條件必須依製程規範決定。',
        'Separate the dies, interposer and substrate before assembly. Inspect components, then plan placement, underfill and post-bond tests so defects are not discovered only after costly integration. This is a conceptual workflow: actual sequencing, materials and process conditions depend on the qualified manufacturing flow.',
        '組立前のダイ、中間層、基板を分けます。部品検査、搭載、アンダーフィル、接合後試験を計画し、高価な組立の最後まで欠陥を持ち越さないようにします。ここでは概念を示し、実際の順序や材料条件は認定工程に従います。',
        '조립 전 다이, 인터포저, 기판을 분리해 봅니다. 부품 검사와 배치, 언더필, 접합 후 시험을 계획하면 비싼 조립을 마친 뒤 결함을 발견하는 위험을 줄일 수 있습니다. 실제 순서와 재료 조건은 검증된 제조 공정에 따라 달라집니다.',
        '把整体拆成待组装的晶粒、中介层与基板。先检查各元件，再规划贴合、填胶与接合后测试，能避免到最后才发现昂贵的缺陷。这是概念流程；实际先后顺序与材料条件必须依工艺规范决定。')),
      C(L('分層間的垂直連接','Connections between layers','層間の縦方向接続','층 사이의 수직 연결','分层间的垂直连接'),L(
        '展開分層結構，辨認晶粒接點、中介層佈線與穿矽孔。不要把 HBM 內部堆疊的垂直連線，和中介層通往下方基板的連線混為一談。現在用眼睛追一遍：資料往鄰居走，供電與外部連接往基板走。',
        'In the separated layers, identify die contacts, interposer wiring and through-silicon vias. Vertical connections inside an HBM stack are not the same structures as connections through the interposer toward the substrate. Trace the distinct routes: data travels to neighboring dies, while power and external connections reach the substrate.',
        '層を分けてダイ接点、配線、シリコン貫通ビアを探します。HBM 内の積層接続と、インターポーザーから基板へ向かう接続は別の構造です。隣のダイへ向かうデータと、基板へ向かう電源・外部接続を分けて追いましょう。',
        '펼친 층에서 다이 접점, 인터포저 배선, 실리콘 관통 비아를 찾습니다. HBM 스택 내부의 수직 연결과 인터포저에서 기판으로 내려가는 연결은 서로 다릅니다. 이웃 다이로 향하는 데이터와 기판으로 이어지는 전원·외부 연결을 각각 따라가 보세요.',
        '展开分层结构，辨认晶粒接点、中介层布线与穿硅孔。不要把 HBM 内部堆叠的垂直连线，和中介层通往下方基板的连线混为一谈。现在用眼睛追一遍：数据往邻居走，供电与外部连接往基板走。')),
      C(L('頻寬要和功耗一起看','Bandwidth and energy together','帯域と電力を同時に見る','대역폭과 에너지를 함께 보기','带宽要和功耗一起看'),L(
        '資料從記憶體到運算核心，再回到記憶體。問三件事：每秒搬多少資料、每位元耗多少能量、最壞情況延遲多大。靠近可以縮短互連，但不能直接推論整個系統一定更省電；工作負載與控制器也會改變結果。',
        'Follow data from memory to compute and back. Ask three questions: how much data per second, how much energy per bit and what worst-case latency? Shorter links can help, but proximity alone does not guarantee lower system power. Workload, controllers and utilization also shape the result.',
        'メモリーから演算部へ、そして戻るデータを追います。毎秒の量、一ビットのエネルギー、最悪遅延の三点を考えます。距離短縮は有利でも、システム全体の省電力は自動的には決まりません。処理内容や制御回路も影響します。',
        '메모리에서 연산부로 갔다 돌아오는 데이터를 따라갑니다. 초당 데이터량, 비트당 에너지, 최악 지연을 함께 물어야 합니다. 짧은 연결이 도움이 되지만 가까이 배치했다고 시스템 전력이 반드시 줄지는 않습니다. 작업 부하와 제어기도 결과에 영향을 줍니다.',
        '数据从内存到计算核心，再回到内存。问三件事：每秒搬多少数据、每比特耗多少能量、最坏情况延迟多大。靠近可以缩短互连，但不能直接推论整个系统一定更省电；工作负载与控制器也会改变结果。')),
      C(L('熱也有自己的路線','Heat has a route too','熱にも経路がある','열에도 경로가 있다','热也有自己的路线'),L(
        '熱點從運算晶粒浮現，向上穿過介面材料與散熱結構。旁邊的記憶體也有溫度限制，不能只盯著中央晶片。紅色是概念熱區，不是量測溫度；真正比較散熱方案，要固定功率、環境與接觸條件。',
        'Heat leaves the compute die through interface material and cooling structures above it. Nearby memory also has temperature limits. The red region is an illustrative hotspot, not measured temperature. A fair cooling comparison holds power, ambient conditions and contact conditions constant.',
        '熱は演算ダイから界面材料を通り、上の冷却構造へ移動します。周囲のメモリーにも温度制限があります。赤色は概念上の熱点で測定値ではありません。冷却方式を比べるときは電力、周囲環境、接触条件を揃えます。',
        '연산 다이의 열은 계면 재료를 거쳐 위쪽 냉각 구조로 이동합니다. 주변 메모리의 온도 한계도 중요합니다. 붉은 영역은 개념적 열점이며 측정 온도가 아닙니다. 냉각안을 비교할 때는 전력, 주변 환경, 접촉 조건을 같게 해야 합니다.',
        '热点从计算晶粒浮现，向上穿过界面材料与散热结构。旁边的内存也有温度限制，不能只盯着中央芯片。红色是概念热区，不是测量温度；真正比较散热方案，要固定功率、环境与接触条件。')),
      C(L('看不見的接點也要驗證','Verify hidden connections','見えない接点を検証','보이지 않는 접점 검증','看不见的接点也要验证'),L(
        '鏡頭停在檢查站：外觀、接點影像與電性測試回答不同問題。漂亮的 X 光影像不等於每條訊號都正常；電性通過也不代表長期可靠。把缺陷位置、測試結果與製程批次連起來，才能找到真正的改善方向。',
        'At inspection, visual checks, joint imaging and electrical tests answer different questions. A clean X-ray image does not prove every signal works; an electrical pass does not prove lifetime reliability. Connect defect locations, test results and process lots to identify meaningful corrective actions.',
        '検査では外観、接点画像、電気試験が別々の問いに答えます。きれいな X 線像だけでは全信号の動作を証明できず、電気試験合格だけでは寿命を保証できません。位置、試験結果、製造ロットを関連付けて改善します。',
        '외관 검사, 접합부 영상, 전기 시험은 서로 다른 문제를 확인합니다. 깨끗한 X선 영상이 모든 신호의 정상 작동을 증명하지는 않습니다. 전기 시험 통과도 수명을 보장하지 않습니다. 결함 위치, 시험 결과, 공정 로트를 연결해 개선 원인을 찾습니다.',
        '镜头停在检查站：外观、接点影像与电性测试回答不同问题。漂亮的 X 光影像不等于每条信号都正常；电性通过也不代表长期可靠。把缺陷位置、测试结果与工艺批次连起来，才能找到真正的改善方向。')),
      C(L('更大不是唯一答案','Bigger is not the only answer','大きさだけが答えではない','크기만이 답은 아니다','更大不是唯一答案'),L(
        '拉高鏡頭，比較多放記憶體、縮短走線與維持可製造性的拉扯。封裝面積、翹曲、供電與散熱都會牽動成本和良率。中介層的價值在於整合適合的系統，而不是把所有空間塞滿。',
        'Rise above the package and compare more memory, shorter routes and manufacturability. Package area, warpage, power delivery and cooling interact with cost and yield. The interposer is valuable because it enables a balanced system, not because every available location is filled with silicon.',
        '上空へ戻り、メモリー増設、配線短縮、作りやすさの関係を比べます。面積、反り、給電、冷却はコストと歩留まりに影響します。空間をすべて埋めることではなく、適切なシステムを成立させることが中間層の価値です。',
        '다시 올라가 메모리 추가, 배선 단축, 제조 가능성의 균형을 봅니다. 패키지 면적, 휨, 전력 공급, 냉각은 비용과 수율에 함께 영향을 줍니다. 인터포저의 가치는 빈 공간을 모두 채우는 것이 아니라 균형 잡힌 시스템을 만드는 데 있습니다.',
        '拉高镜头，比较多放内存、缩短走线与维持可制造性的拉扯。封装面积、翘曲、供电与散热都会牵动成本和良率。中介层的价值在于整合适合的系统，而不是把所有空间塞满。')),
      C(L('帶走一條完整路線','Take away a complete route','全体の道筋を持ち帰る','완전한 경로 기억하기','带走一条完整路线'),L(
        '最後俯瞰整條技術路線：定義需求、配置運算與 HBM、設計互連和供電、安排組裝、驗證熱與可靠度。若你能指出資料從哪裡來、熱往哪裡走、哪個接點最需要證據，就已看懂這個封裝的核心。',
        'Finish with the complete route: define requirements, place compute and HBM, design interconnect and power, plan assembly, then verify thermal behavior and reliability. If you can show where data begins, where heat leaves and which connection needs evidence, you understand the core of this package.',
        '要求定義、演算と HBM の配置、配線と電源、組立計画、熱と信頼性の検証を見渡します。データの出発点、熱の出口、確認すべき接点を指せれば、このパッケージの要点を理解しています。',
        '요구 정의, 연산과 HBM 배치, 연결과 전원 설계, 조립 계획, 열·신뢰성 검증의 전체 경로를 봅니다. 데이터가 시작되는 곳, 열이 빠져나가는 곳, 검증이 필요한 접점을 짚을 수 있다면 이 패키지의 핵심을 이해한 것입니다.',
        '最后俯瞰整条技术路线：定义需求、配置计算与 HBM、设计互连和供电、安排组装、验证热与可靠性。若你能指出数据从哪里来、热往哪里走、哪个接点最需要证据，就已看懂这个封装的核心。'))
    ]),
    T('fanout',
      L('扇出封裝與重佈線層','Fan-out packaging & RDL','ファンアウトと再配線層','팬아웃 패키징과 RDL','扇出封装与重布线层'),
      L('從晶粒邊界飛向更大的連接空間，理解 RDL、模封與翹曲之間的關係。','Fly beyond the die boundary to understand RDL, molding and warpage.','ダイの外へ広がる配線をたどり、RDL、封止、反りの関係を理解します。','다이 바깥으로 펼쳐지는 배선을 따라 RDL, 몰딩, 휨을 이해합니다.','从晶粒边界飞向更大的连接空间，理解 RDL、模封与翘曲之间的关系。'),
      ['info','fanout','stress','test'],[
      C(L('把出口移到晶粒外','Move connections beyond the die','接続をダイの外へ広げる','연결을 다이 밖으로 확장','把出口移到晶粒外'),L(
        '俯瞰中央晶粒，四周留出的不是浪費空間，而是扇出連接的舞台。重佈線層把原本密集的接點重新安排到較大的範圍。先看晶粒邊界，再看連線越過邊界，你就能分辨「晶片大小」和「封裝大小」。',
        'Look down at the central die. The surrounding area is useful routing space, not empty waste. Redistribution layers relocate dense die connections across a wider region. Compare the die outline with routes extending beyond it, and distinguish the size of the silicon from the size of its package.',
        '中央のダイの周囲は無駄な空間ではなく、配線を広げる場所です。再配線層は密集した接点を広い範囲へ配置し直します。ダイの輪郭と、その外へ伸びる線を比べて、シリコンとパッケージの大きさを区別しましょう。',
        '중앙 다이 주변은 빈 낭비 공간이 아니라 배선을 펼치는 영역입니다. 재배선층은 조밀한 다이 접점을 더 넓은 범위로 옮깁니다. 다이의 경계와 그 밖으로 나가는 선을 비교하면 실리콘 크기와 패키지 크기를 구분할 수 있습니다.',
        '俯瞰中央晶粒，四周留出的不是浪费空间，而是扇出连接的舞台。重布线层把原本密集的接点重新安排到较大的范围。先看晶粒边界，再看连线越过边界，你就能分辨芯片大小和封装大小。')),
      C(L('矽、模封與銅線','Silicon, mold and copper','シリコン・封止材・銅配線','실리콘·몰드·구리 배선','硅、模封与铜线'),L(
        '下降到材質交界：硬的矽晶粒、周圍的模封材料、表面的介電層與金屬線共同形成結構。顏色用來辨認功能，不代表特定廠商配方。美感來自整齊的層次；工程難點則藏在不同材料如何一起變形。',
        'Descend to the material boundaries: silicon dies, surrounding molding compound, dielectric layers and metal traces form one structure. Colors identify function, not a vendor recipe. The ordered layers create visual clarity; the engineering challenge is how different materials deform together.',
        'シリコン、周囲の封止材、絶縁層、金属配線の境界へ降ります。色は機能を区別するためで、メーカーの材料配合ではありません。整った層が見た目を明快にし、異なる材料が一緒に変形することが技術上の課題になります。',
        '실리콘, 주변 몰딩 재료, 절연층, 금속 배선의 경계로 내려갑니다. 색은 기능 구분용이며 특정 회사의 재료 조성을 뜻하지 않습니다. 정돈된 층은 시각적 아름다움을 만들지만, 서로 다른 재료가 함께 변형되는 현상은 공학적 과제입니다.',
        '下降到材质交界：硬的硅晶粒、周围的模封材料、表面的介电层与金属线共同形成结构。颜色用来辨认功能，不代表特定厂商配方。美感来自整齐的层次；工程难点则藏在不同材料如何一起变形。')),
      C(L('RDL 是重新安排道路','RDL rearranges the roads','RDL は道を組み替える','RDL로 경로 재배치','RDL 是重新安排道路'),L(
        '沿著一個晶粒接點追到外部焊球，會遇到平面走線與跨層導孔。RDL 不是任意畫線：線寬、間距、回流路徑與絕緣都有限制。請找出哪一段在換層，哪一段在把連接位置往外展開。',
        'Follow a die contact to an external solder ball through planar traces and interlayer vias. RDL is constrained routing, not arbitrary drawing: width, spacing, return paths and insulation all matter. Identify where the route changes layer and where it moves the connection outward.',
        'ダイ接点から外部はんだボールまで、平面配線と層間ビアを追います。RDL は自由な線画ではなく、線幅、間隔、帰路、絶縁の制約を受けます。層を変える場所と、接続位置を外側へ広げる場所を探してください。',
        '다이 접점에서 외부 솔더볼까지 평면 배선과 층간 비아를 따라갑니다. RDL은 자유롭게 그리는 선이 아닙니다. 선폭, 간격, 귀환 경로, 절연 조건이 중요합니다. 층이 바뀌는 부분과 연결 위치가 바깥으로 이동하는 부분을 찾아보세요.',
        '沿着一个晶粒接点追到外部焊球，会遇到平面走线与跨层导孔。RDL 不是任意画线：线宽、间距、回流路径与绝缘都有限制。请找出哪一段在换层，哪一段在把连接位置往外展开。')),
      C(L('先放晶粒，或先做線','Die first or routing first','ダイが先か配線が先か','다이 먼저, 배선 먼저','先放晶粒，或先做线'),L(
        '畫面把兩種流程分開：晶粒先放好再形成重佈線，或先形成 RDL 再接上晶粒。兩條路都叫扇出，但良率風險出現的位置不同。不能只用成品外觀判斷製程；要知道昂貴晶粒在哪一步加入。',
        'Compare two flows: place dies before building redistribution layers, or form RDL before attaching dies. Both are fan-out approaches, but yield risks enter at different stages. The final outline alone does not reveal the process. Ask when valuable dies enter the assembly and what has already been tested.',
        'ダイを先に置いて再配線する工程と、RDL を先に作ってダイを載せる工程を比べます。どちらもファンアウトですが、歩留まりのリスクが現れる段階は異なります。完成形だけで判断せず、高価なダイをいつ投入するか確認します。',
        '다이를 먼저 놓고 RDL을 만드는 공정과 RDL을 먼저 만들고 다이를 붙이는 공정을 비교합니다. 둘 다 팬아웃이지만 수율 위험이 나타나는 단계가 다릅니다. 완성된 외형만 보지 말고 값비싼 다이를 어느 단계에서 투입하는지 확인해야 합니다.',
        '画面把两种流程分开：晶粒先放好再形成重布线，或先形成 RDL 再接上晶粒。两条路都叫扇出，但良率风险出现的位置不同。不能只用成品外观判断工艺；要知道昂贵晶粒在哪一步加入。')),
      C(L('薄層裡的立體結構','A 3D structure in thin layers','薄い層の中の立体構造','얇은 층 속 입체 구조','薄层里的立体结构'),L(
        '把薄薄的封裝拉開成分層示意，介電層隔開不同金屬層，導孔讓特定位置相通。這裡刻意放大厚度方便觀看，不能拿畫面比例當成製造尺寸。請確認相鄰的兩條線是刻意連接，還是應該保持絕緣。',
        'Open the thin package into separated layers. Dielectrics separate metal layers, while vias connect selected locations. Thickness is exaggerated for visibility and must not be read as manufacturing scale. Check whether adjacent routes should be connected or electrically isolated; that distinction is the purpose of the layer stack.',
        '薄いパッケージを層ごとに開きます。絶縁層が金属層を分け、ビアが必要な点だけを接続します。厚みは見やすく拡大しており製造寸法ではありません。隣の線をつなぐべきか、絶縁すべきかを確認します。',
        '얇은 패키지를 층별로 펼칩니다. 절연층은 금속층을 분리하고 비아는 필요한 지점만 연결합니다. 두께는 보기 쉽게 과장했으므로 제조 치수로 해석하면 안 됩니다. 인접한 배선이 연결되어야 하는지 절연되어야 하는지 확인합니다.',
        '把薄薄的封装拉开成分层示意，介电层隔开不同金属层，导孔让特定位置相通。这里刻意放大厚度方便观看，不能拿画面比例当成制造尺寸。请确认相邻的两条线是刻意连接，还是应该保持绝缘。')),
      C(L('別只追訊號，還要找回路','Follow the return path','信号の帰路も追う','신호의 귀환 경로도 보기','别只追信号，还要找回路'),L(
        '訊號線旁的參考導體同樣重要。電流必須形成回路；回流路徑中斷會改變高速訊號品質。俯瞰時看走線是否順暢，剖面時看參考層是否連續，兩種角度一起看，才能理解佈線的真正秩序。',
        'The reference conductor beside a signal is important too. Current needs a complete loop; a disrupted return path affects high-speed behavior. Use the overhead view to inspect routing and the section to inspect reference continuity. Together, the two views explain the electrical order behind the geometry.',
        '信号の近くにある基準導体も重要です。電流には閉じた経路が必要で、帰路の不連続は高速信号に影響します。上から配線を、断面から基準層の連続性を見て、形の背後にある電気的な秩序を理解します。',
        '신호 옆의 기준 도체도 중요합니다. 전류는 완전한 회로를 이루어야 하며 귀환 경로의 단절은 고속 신호에 영향을 줍니다. 위에서는 배선을, 단면에서는 기준층의 연속성을 확인하세요. 두 시점이 배선의 전기적 질서를 설명합니다.',
        '信号线旁的参考导体同样重要。电流必须形成回路；回流路径中断会改变高速信号质量。俯瞰时看走线是否顺畅，剖面时看参考层是否连续，两种角度一起看，才能理解布线的真正秩序。')),
      C(L('翹曲不是外觀小問題','Warpage is functional','反りは機能に関わる','휨은 기능에 영향을 준다','翘曲不是外观小问题'),L(
        '示意結構微微彎曲，提醒你材料熱膨脹不一致。翹曲會影響對位、接合與後續裝板，不只是看起來不平。動畫中的彎曲被誇張呈現；真正評估要使用量測、材料資料與有邊界條件的力學模型。',
        'A slight conceptual bend highlights mismatched thermal expansion. Warpage can affect alignment, joining and board assembly; it is more than a cosmetic defect. The animated bend is exaggerated. Evaluation requires measurements, material properties and a mechanical model with explicit boundary conditions.',
        '概念的な曲がりで熱膨張の違いを示します。反りは位置合わせ、接合、基板実装に影響し、外観だけの問題ではありません。映像は変形を誇張しています。評価には測定、材料特性、境界条件を定めた力学モデルが必要です。',
        '개념적인 굽힘은 재료 간 열팽창 차이를 보여 줍니다. 휨은 정렬, 접합, 보드 실장에 영향을 주므로 단순한 외관 문제가 아닙니다. 애니메이션의 변형은 과장되어 있습니다. 평가에는 측정과 재료 특성, 경계 조건을 정한 역학 모델이 필요합니다.',
        '示意结构微微弯曲，提醒你材料热膨胀不一致。翘曲会影响对位、接合与后续装板，不只是看起来不平。动画中的弯曲被夸张呈现；真正评估要使用测量、材料数据与有边界条件的力学模型。')),
      C(L('對位誤差如何變成缺陷','When alignment becomes a defect','ずれが欠陥になる瞬間','정렬 오차가 결함이 될 때','对位误差如何变成缺陷'),L(
        '停在接點附近，想像晶粒輕微偏移後，原定走線能否仍落在正確位置。檢查必須同時照顧對位、開路、短路與界面缺陷。每個異常都要回到可追溯的量測，不能只憑動畫上「看起來有接到」。',
        'Pause beside a contact and imagine the die shifting slightly. Would the intended route still land correctly? Inspection must address alignment, opens, shorts and interface defects. Each suspected issue needs traceable measurement; a visually touching animated connection is not evidence of a functional joint.',
        '接点で止まり、ダイが少しずれたら配線が正しく届くか考えます。位置、断線、短絡、界面欠陥を検査する必要があります。映像で接触して見えることは接合品質の証拠ではなく、追跡可能な測定が必要です。',
        '접점 옆에서 다이가 조금 이동하면 배선이 올바르게 닿을지 생각해 봅니다. 정렬, 단선, 단락, 계면 결함을 함께 검사해야 합니다. 화면에서 붙어 보인다는 사실은 정상 접합의 증거가 아니며 추적 가능한 측정이 필요합니다.',
        '停在接点附近，想象晶粒轻微偏移后，原定走线能否仍落在正确位置。检查必须同时照顾对位、开路、短路与界面缺陷。每个异常都要回到可追溯的测量，不能只凭动画上看起来有接到。')),
      C(L('薄型化與複雜度的交換','Thinness versus complexity','薄型化と複雑さの交換','박형화와 복잡성의 균형','薄型化与复杂度的交换'),L(
        '退後看整體，扇出可以提供靈活的接點配置與薄型整合，但更多層、更密線距或更大面積也會增加製程挑戰。不能一概說扇出一定比較便宜；比較時必須使用相同功能、測試涵蓋與合格產出。',
        'Step back: fan-out offers flexible connection placement and thin integration, while more layers, finer routing or larger area raise process demands. It is not automatically cheaper. Compare alternatives at equal function, test coverage and qualified output, rather than comparing package outlines alone.',
        '全体を見ると、ファンアウトは柔軟な接点配置と薄型化を可能にしますが、多層化、微細化、大面積化は工程を難しくします。必ず安価になるわけではありません。同じ機能、試験範囲、良品出荷を条件に比較します。',
        '전체를 보면 팬아웃은 유연한 접점 배치와 얇은 통합을 제공하지만 층수 증가, 미세 배선, 면적 확대는 공정 난도를 높입니다. 항상 더 저렴한 것은 아닙니다. 같은 기능, 시험 범위, 양품 출하량을 기준으로 비교해야 합니다.',
        '退后看整体，扇出可以提供灵活的接点配置与薄型整合，但更多层、更密线距或更大面积也会增加工艺挑战。不能一概说扇出一定比较便宜；比较时必须使用相同功能、测试覆盖与合格产出。')),
      C(L('由接點需求決定流程','Let connections guide the flow','接続要求から工程を選ぶ','연결 요구로 공정 선택','由接点需求决定流程'),L(
        '帶走這條路線：先定接點與尺寸需求，再選晶粒先行或 RDL 先行，接著規劃佈線、控制翹曲、完成電性與可靠度驗證。扇出的美感，是把擁擠的微小出口整理成有秩序、能製造也能檢查的網路。',
        'Take this route with you: define connections and size, select die-first or RDL-first integration, plan routing, manage warpage and verify electrical behavior and reliability. Fan-out turns crowded die exits into an orderly network that must be manufacturable and inspectable, not merely visually elegant.',
        '接点と寸法の要求から始め、ダイ先行か RDL 先行かを選び、配線、反り対策、電気・信頼性検証へ進みます。密集する出口を、製造でき検査できる整ったネットワークへ変えることがファンアウトの美しさです。',
        '접점과 크기 요구를 정하고, 다이 선행 또는 RDL 선행을 선택한 뒤 배선, 휨 관리, 전기·신뢰성 검증으로 이어집니다. 복잡한 다이 출구를 제조하고 검사할 수 있는 질서 있는 네트워크로 만드는 것이 팬아웃의 아름다움입니다.',
        '带走这条路线：先定接点与尺寸需求，再选晶粒先行或 RDL 先行，接着规划布线、控制翘曲、完成电性与可靠性验证。扇出的美感，是把拥挤的微小出口整理成有秩序、能制造也能检查的网络。'))
    ])
  ];
  tours.push(T('hybrid',
    L('3D 堆疊與混合鍵合','3D stacking & hybrid bonding','3D 積層とハイブリッド接合','3D 적층과 하이브리드 본딩','3D 堆叠与混合键合'),
    L('從平面街區升成立體樓層，看懂直接接合、對位、測試與熱路徑。','Turn planar districts into stacked floors, then inspect bonding, alignment, testing and heat paths.','平面の街区を立体的に重ね、接合・位置合わせ・試験・熱経路を調べます。','평면 구역을 입체로 쌓고 접합, 정렬, 시험, 열 경로를 살펴봅니다.','从平面街区升成立体楼层，看懂直接接合、对位、测试与热路径。'),
    ['soic','intel','stress','test'],[
    C(L('從向外擴張到向上堆疊','Build upward','上方向へ積み重ねる','위로 쌓아 올리기','从向外扩张到向上堆叠'),L(
      '先俯瞰，再緩緩轉成斜視：原本並排的功能可以上下堆疊，縮短某些晶粒間的路徑。這不是把完整電路板直接疊起來，而是在精密控制的界面接合晶粒。先數清有幾層，再找每一層的角色。',
      'Begin overhead, then tilt: functions can be stacked rather than placed side by side, shortening selected die-to-die routes. This is not a stack of circuit boards. Dies meet at carefully controlled interfaces. Count the layers and identify what each layer contributes before inspecting the bond.',
      '上空から斜めへ視点を変えます。機能を上下に重ねると、一部のダイ間経路を短縮できます。回路基板を積むのではなく、管理された界面でダイを接合します。層を数え、それぞれの役割を確認しましょう。',
      '위에서 본 뒤 비스듬히 내려봅니다. 기능을 나란히 놓는 대신 쌓으면 일부 다이 간 경로를 줄일 수 있습니다. 회로 보드를 쌓는 방식이 아니라 정밀하게 관리한 계면에서 다이를 접합합니다. 먼저 층수와 각 층의 역할을 확인하세요.',
      '先俯瞰，再缓缓转成斜视：原本并排的功能可以上下堆叠，缩短某些晶粒间的路径。这不是把完整电路板直接叠起来，而是在精密控制的界面接合晶粒。先数清有几层，再找每一层的角色。')),
    C(L('上層與下層如何分工','Assign the layers','上下の層の役割','상하층의 역할 배분','上层与下层如何分工'),L(
      '上層可以放運算或記憶功能，下層可以承接其他電路與連接；具體配置取決於架構。堆疊不保證每層都使用同一製程。這裡是通用教學模型，不是 SoIC 或 Foveros 特定產品的內部配置圖。',
      'Upper and lower dies can divide compute, memory and connection functions in different ways. Their process technologies need not match. This is a generic teaching model, not an internal floorplan of a particular SoIC or Foveros product. Architecture determines which functions belong together.',
      '上下のダイは演算、記憶、接続などを分担し、同じ製造プロセスとは限りません。この模型は一般的な教材で、特定の SoIC や Foveros 製品の内部配置ではありません。何を重ねるかはアーキテクチャで決めます。',
      '상하 다이는 연산, 메모리, 연결 기능을 나눌 수 있으며 같은 제조 공정을 사용할 필요는 없습니다. 이 장면은 일반 교육 모델로 특정 SoIC 또는 Foveros 제품의 내부 배치도가 아닙니다. 어떤 기능을 함께 쌓을지는 아키텍처가 결정합니다.',
      '上层可以放计算或存储功能，下层可以承接其他电路与连接；具体配置取决于架构。堆叠不保证每层都使用同一工艺。这里是通用教学模型，不是 SoIC 或 Foveros 特定产品的内部配置图。')),
    C(L('混合鍵合的兩種接合','Two bonds at one interface','一つの界面に二つの接合','한 계면의 두 가지 접합','混合键合的两种接合'),L(
      '靠近界面：銅接點建立電性連接，周圍介電表面也參與接合，這就是混合鍵合的關鍵。不要把它畫成一排大型焊球；焊料微凸塊與直接混合鍵合是不同的互連方式，適用限制也不同。',
      'Approach the interface: copper contacts provide electrical connections while surrounding dielectric surfaces also bond. That combination defines hybrid bonding. Do not picture a row of large solder balls. Solder microbumps and direct hybrid bonding are different interconnect approaches with different integration constraints.',
      '界面では銅接点が電気をつなぎ、周囲の絶縁体表面も接合します。この組合せがハイブリッド接合です。大きなはんだボールの列ではありません。微細はんだバンプと直接接合は異なる方式で、制約も違います。',
      '계면에서 구리 접점은 전기적으로 연결되고 주변 유전체 표면도 접합됩니다. 이것이 하이브리드 본딩의 핵심입니다. 큰 솔더볼의 줄로 이해하면 안 됩니다. 솔더 마이크로범프와 직접 하이브리드 본딩은 서로 다른 연결 방식이며 제약도 다릅니다.',
      '靠近界面：铜接点建立电性连接，周围介电表面也参与接合，这就是混合键合的关键。不要把它画成一排大型焊球；焊料微凸块与直接混合键合是不同的互连方式，适用限制也不同。')),
    C(L('對位之前，先準備表面','Prepare before aligning','位置合わせの前に表面を整える','정렬 전에 표면 준비','对位之前，先准备表面'),L(
      '讓兩片晶粒暫時分離，想像任何微粒或表面不平都可能留在接合界面。表面準備、潔淨度、平坦度與對位精度共同決定品質。動畫把動作放慢是為了看懂原理，不提供清洗配方或製程溫度。',
      'Separate the dies and imagine a particle or uneven surface trapped between them. Surface preparation, cleanliness, flatness and alignment work together to determine bond quality. The motion is slowed to explain the principle; it is not a cleaning recipe or a manufacturing temperature schedule.',
      'ダイを離し、粒子や凹凸が界面に残る様子を考えます。表面処理、清浄度、平坦度、位置精度が接合品質を左右します。動作を遅くして原理を示しており、洗浄レシピや工程温度を提供するものではありません。',
      '다이를 분리하고 계면에 입자나 표면 요철이 남는 상황을 생각합니다. 표면 준비, 청정도, 평탄도, 정렬 정확도가 함께 접합 품질을 좌우합니다. 느린 동작은 원리 설명용이며 세정 방법이나 공정 온도 조건을 제시하지 않습니다.',
      '让两片晶粒暂时分离，想象任何微粒或表面不平都可能留在接合界面。表面准备、洁净度、平坦度与对位精度共同决定质量。动画把动作放慢是为了看懂原理，不提供清洗配方或工艺温度。')),
    C(L('短接點與長路徑要分開','Separate contact from route','接点と全経路を分けて考える','접점과 전체 경로 구분','短接点与长路径要分开'),L(
      '分層示意中的接合距離雖短，資料仍要經過晶粒內部電路與佈線。垂直連接只解決路徑的一部分，不會讓邏輯延遲消失。找出跨越接合面的那一步，再把它放回完整的訊號鏈。',
      'The bond interface is short, but data still traverses circuits and wiring within each die. Vertical connectivity solves only part of the path; it does not remove logic delay. Identify the crossing between dies, then place that crossing back into the complete signal chain.',
      '接合界面は短くても、データは各ダイ内の回路や配線を通ります。縦方向接続が解決するのは経路の一部であり、論理遅延が消えるわけではありません。界面を越える箇所を、信号経路全体の中で見直します。',
      '접합 계면은 짧지만 데이터는 각 다이 내부 회로와 배선을 통과합니다. 수직 연결은 경로의 일부를 해결할 뿐 논리 지연을 없애지는 않습니다. 다이 사이를 건너는 지점을 찾고 전체 신호 경로 안에서 그 의미를 확인하세요.',
      '分层示意中的接合距离虽短，数据仍要经过晶粒内部电路与布线。垂直连接只解决路径的一部分，不会让逻辑延迟消失。找出跨越接合面的那一步，再把它放回完整的信号链。')),
    C(L('密集連接如何變成價值','Turn density into system value','接続密度を価値へ変える','연결 밀도를 시스템 가치로','密集连接如何变成价值'),L(
      '密集接點能讓相鄰層交換更多資訊，但架構必須真的用得上這些連接。先決定資料分工，再規劃接點與供電，不要先堆出最多接點才找用途。畫面中的流動是資訊關係示意，沒有宣稱特定速度。',
      'Dense contacts can support richer communication between layers, but the architecture must make use of them. Define the division of data and work before allocating contacts and power. More connections are not a goal by themselves. Animated movement shows information relationships, not a claimed transfer speed.',
      '高密度接点は層間通信を豊かにできますが、活用できる設計が必要です。接点や給電を決める前に、データと処理の分担を定めます。接点の多さ自体が目的ではなく、光の動きも特定の転送速度を示しません。',
      '조밀한 접점은 층간 통신을 늘릴 수 있지만 아키텍처가 이를 활용해야 합니다. 접점과 전원을 배분하기 전에 데이터와 작업 분담을 정합니다. 연결 수 자체가 목적은 아닙니다. 빛의 흐름은 정보 관계이며 특정 전송 속도를 나타내지 않습니다.',
      '密集接点能让相邻层交换更多信息，但架构必须真的用得上这些连接。先决定数据分工，再规划接点与供电，不要先堆出最多接点才找用途。画面中的流动是信息关系示意，没有宣称特定速度。')),
    C(L('被上層遮住的熱','Heat beneath the stack','積層の下にある熱','적층 아래에 갇힌 열','被上层遮住的热'),L(
      '從側面看熱往外走的路徑。不同層的發熱位置、界面熱阻與散熱器位置共同影響溫度。不能認為堆疊越高就越好；把最熱的電路放在哪裡，是一開始就要解決的架構問題。',
      'From the side, follow heat out of the stack. Heat-source location, interface resistance and cooler placement jointly affect temperature. A taller stack is not automatically better. Where the hottest circuits belong is an architectural decision to make early, not a problem to postpone until assembly.',
      '側面から熱の出口を追います。発熱位置、界面熱抵抗、冷却器の位置が温度に影響します。高く積めばよいわけではありません。最も熱い回路の配置は、組立後ではなく設計の初期に決める問題です。',
      '측면에서 열이 빠져나가는 경로를 봅니다. 발열 위치, 계면 열저항, 냉각기 위치가 온도에 영향을 줍니다. 높이 쌓을수록 좋은 것은 아닙니다. 가장 뜨거운 회로의 위치는 조립 후가 아니라 아키텍처 초기 단계에서 결정해야 합니다.',
      '从侧面看热往外走的路径。不同层的发热位置、界面热阻与散热器位置共同影响温度。不能认为堆叠越高就越好；把最热的电路放在哪里，是一开始就要解决的架构问题。')),
    C(L('埋進去之前怎麼測','Test before burying a die','埋め込む前に試験する','매립 전에 시험하기','埋进去之前怎么测'),L(
      '被其他晶粒蓋住的接點不容易再直接碰到，因此要預先設計測試存取。組裝前篩選、接合後連通檢查與系統測試各有任務。通過一次測試不是永久保證；要把涵蓋率與剩餘風險說清楚。',
      'Contacts become difficult to reach after another die covers them, so test access must be designed in advance. Pre-assembly screening, post-bond connectivity and system testing serve different purposes. One passing test is not a permanent guarantee; coverage and remaining risk must be explicit.',
      '他のダイに覆われた接点へは直接触れにくくなるため、試験経路を先に設計します。組立前の選別、接合後の導通、システム試験は役割が異なります。一度の合格は永続的保証ではなく、範囲と残るリスクを示します。',
      '다른 다이가 덮으면 접점에 직접 접근하기 어려워지므로 시험 접근 경로를 미리 설계해야 합니다. 조립 전 선별, 접합 후 연결 확인, 시스템 시험은 역할이 다릅니다. 한 번의 통과가 영구 보장은 아니므로 시험 범위와 남은 위험을 명확히 해야 합니다.',
      '被其他晶粒盖住的接点不容易再直接碰到，因此要预先设计测试访问。组装前筛选、接合后连通检查与系统测试各有任务。通过一次测试不是永久保证；要把覆盖率与剩余风险说清楚。')),
    C(L('密度、良率與可修復性','Density, yield and repair','密度・歩留まり・修復性','밀도·수율·수리 가능성','密度、良率与可修复性'),L(
      '拉開到整體視角，高密度整合會同時提高界面品質與測試規劃的重要性。已接合的晶粒未必能經濟地拆換，所以前段選別更有價值。比較方案時，要連同良品成本、熱條件與返修能力一起看。',
      'Zoom out: dense integration makes interface quality and test planning more important. Bonded dies may not be economical to replace, increasing the value of earlier screening. Compare solutions using cost per good unit, thermal conditions and repair options together, rather than connection density alone.',
      '全体を見ると、高密度化ほど界面品質と試験計画が重要です。接合後のダイ交換は経済的でない場合があり、事前選別の価値が高まります。接続密度だけでなく、良品単価、熱条件、修復性を一緒に比較します。',
      '전체로 보면 고밀도 통합일수록 계면 품질과 시험 계획이 중요합니다. 접합된 다이를 경제적으로 교체하기 어려울 수 있어 사전 선별 가치가 커집니다. 연결 밀도만 보지 말고 양품 단가, 열 조건, 수리 가능성을 함께 비교해야 합니다.',
      '拉开到整体视角，高密度集成会同时提高界面质量与测试规划的重要性。已接合的晶粒未必能经济地拆换，所以前段筛选更有价值。比较方案时，要连同良品成本、热条件与返修能力一起看。')),
    C(L('從堆疊回到系統','Return from stack to system','積層からシステムへ戻る','적층에서 시스템으로 돌아가기','从堆叠回到系统'),L(
      '最後的路線是功能分層、界面設計、表面準備、對位接合、可測試性與散熱驗證。記住：3D 的重點不是把樓蓋高，而是讓最需要溝通的功能靠近，同時讓電流、熱與測試都有可靠出口。',
      'The route is functional partitioning, interface design, surface preparation, alignment, bonding, testability and thermal verification. The aim of 3D is not merely a taller building. It is to bring communicating functions closer while preserving dependable paths for electricity, heat and testing.',
      '機能分割、界面設計、表面準備、位置合わせ、接合、試験性、熱検証が道筋です。3D の目的は高さではありません。通信する機能を近づけつつ、電流、熱、試験の確かな通り道を残すことです。',
      '기능 분할, 계면 설계, 표면 준비, 정렬·접합, 시험 접근성, 열 검증이 전체 경로입니다. 3D의 목표는 단순히 높이 쌓는 것이 아닙니다. 통신하는 기능을 가까이 두면서 전류, 열, 시험의 확실한 경로를 유지하는 것입니다.',
      '最后的路线是功能分层、界面设计、表面准备、对位接合、可测试性与散热验证。记住：3D 的重点不是把楼盖高，而是让最需要沟通的功能靠近，同时让电流、热与测试都有可靠出口。'))
  ]));
  tours.push(T('bridge',
    L('局部矽橋與異質整合','Local silicon bridges','局所シリコンブリッジ','로컬 실리콘 브리지','局部硅桥与异构集成'),
    L('只在最需要密集連接的地方架橋，辨認局部互連與整片中介層的差別。','Place dense connections where needed, and distinguish a local bridge from a full interposer.','必要な場所に高密度接続を置き、局所ブリッジと全面インターポーザーを区別します。','필요한 곳에 고밀도 연결을 배치하고 로컬 브리지와 전체 인터포저를 구분합니다.','只在最需要密集连接的地方架桥，辨认局部互连与整片中介层的差别。'),
    ['intel','cowos','stress','test'],[
    C(L('兩座晶粒之間的橋','A bridge between dies','ダイの間に橋を架ける','다이 사이에 놓인 다리','两座晶粒之间的桥'),L(
      '從高處看兩個晶粒街區，注意交界處的一小段連接區。局部矽橋把精密佈線集中在需要跨越的位置，其他區域仍由封裝基板承接。先找出「橋在哪裡」，再思考為什麼不必讓整個底面都是橋。',
      'From above, find the narrow connection zone between neighboring dies. A local silicon bridge concentrates fine routing where a crossing is needed, while the substrate serves the surrounding area. Locate the bridge first, then ask why the whole package floor does not need to become one.',
      '上空から隣り合うダイの境界にある接続部分を探します。局所シリコンブリッジは必要な場所に微細配線を集中させ、周囲は基板が支えます。橋の場所を見つけ、底面全体を橋にしなくてよい理由を考えます。',
      '위에서 이웃한 다이 사이의 좁은 연결 구역을 찾습니다. 로컬 실리콘 브리지는 건너야 하는 곳에 미세 배선을 집중하고 주변은 기판이 담당합니다. 먼저 다리의 위치를 찾은 뒤 패키지 바닥 전체가 다리일 필요가 없는 이유를 생각하세요.',
      '从高处看两个晶粒街区，注意交界处的一小段连接区。局部硅桥把精密布线集中在需要跨越的位置，其他区域仍由封装基板承接。先找出桥在哪里，再思考为什么不必让整个底面都是桥。')),
    C(L('局部橋與全面平台','Bridge versus full platform','局所ブリッジと全面基盤','로컬 브리지와 전체 플랫폼','局部桥与全面平台'),L(
      '把橋的位置高亮，就能和覆蓋較大範圍的中介層區分。兩者都能支援異質整合，但分配精密佈線的方式不同。這裡以嵌入基板的矽橋為概念，不能把所有橋接產品的結構視為完全相同。',
      'Highlight the bridge to distinguish it from a broad interposer. Both support heterogeneous integration, but distribute fine routing differently. This model explains a bridge embedded in a substrate; bridge-based products can differ in structure, so the illustration is not a universal vendor structure.',
      '橋だけを強調すると、広い面積を覆う中間層との違いが分かります。どちらも異種集積を支えますが、微細配線の配置方法が異なります。この模型は基板埋込み型の概念で、全製品に共通する構造図ではありません。',
      '브리지만 강조하면 넓은 인터포저와 구분할 수 있습니다. 두 방식 모두 이종 집적을 지원하지만 미세 배선의 배치가 다릅니다. 이 모델은 기판 내장형 브리지의 개념이며 모든 제품에 공통인 구조도는 아닙니다.',
      '把桥的位置高亮，就能和覆盖较大范围的中介层区分。两者都能支持异构集成，但分配精密布线的方式不同。这里以嵌入基板的硅桥为概念，不能把所有桥接产品的结构视为完全相同。')),
    C(L('晶粒岸線就是入口','Die edges are the shoreline','ダイの縁が橋の入口','다이 가장자리가 연결 입구','晶粒岸线就是入口'),L(
      '沿著兩個晶粒相對的邊緣飛行。橋的通道要對上晶粒的接點，不能把晶粒任意旋轉就期待連線自動成立。晶粒邊緣的可用空間、接點配置與介面方向，都是系統平面規劃的一部分。',
      'Fly along facing die edges. Bridge channels must meet the intended contacts; rotating a die arbitrarily will not make compatible wiring appear. Available die-edge length, contact placement and interface orientation belong in the system floorplan, before the bridge is treated as a finished connection.',
      '向かい合うダイの縁に沿って飛びます。橋の配線は所定の接点に合う必要があり、自由に回転させても接続は成立しません。縁の長さ、接点配置、インターフェースの向きは、システム配置計画の一部です。',
      '마주 보는 다이 가장자리를 따라갑니다. 브리지 채널은 정해진 접점과 맞아야 하므로 다이를 임의로 돌려도 연결이 자동으로 생기지 않습니다. 가장자리 길이, 접점 배치, 인터페이스 방향을 시스템 배치 계획에 포함해야 합니다.',
      '沿着两个晶粒相对的边缘飞行。桥的通道要对上晶粒的接点，不能把晶粒任意旋转就期待连线自动成立。晶粒边缘的可用空间、接点配置与接口方向，都是系统平面规划的一部分。')),
    C(L('把橋放進基板','Integrate the bridge','橋を基板に組み込む','브리지를 기판에 통합','把桥放进基板'),L(
      '鏡頭下降到基板，橋與周圍材料必須形成可組裝的平面。嵌入、對位、晶粒貼合與接點形成都有公差。這段展示的是組裝關係，不是特定設備的操作順序；真正的流程要依合格製程文件。',
      'Descend toward the substrate. The bridge and surrounding material must create an assembly-compatible surface. Embedding, alignment, die placement and contact formation all have tolerances. This sequence explains assembly relationships, not a particular machine recipe; actual work follows qualified process documentation.',
      '基板へ降ります。橋と周囲の材料は組立可能な面を作る必要があり、埋込み、位置合わせ、搭載、接点形成には公差があります。ここでは関係を示し、特定装置の手順ではありません。実作業は認定工程書に従います。',
      '기판 쪽으로 내려갑니다. 브리지와 주변 재료는 조립 가능한 표면을 형성해야 합니다. 내장, 정렬, 다이 배치, 접점 형성에는 공차가 있습니다. 이 장면은 조립 관계를 설명하며 특정 장비의 작업 순서는 검증된 공정 문서에 따라야 합니다.',
      '镜头下降到基板，桥与周围材料必须形成可组装的平面。嵌入、对位、晶粒贴合与接点形成都有公差。这段展示的是组装关系，不是特定设备的操作顺序；真正的流程要依合格工艺文件。')),
    C(L('哪些線過橋，哪些線下樓','Which routes use the bridge?','橋を渡る線と下へ向かう線','다리를 건너는 선과 아래로 가는 선','哪些线过桥，哪些线下楼'),L(
      '分層示意中先追晶粒到晶粒的連線，再追向基板的供電與外部訊號。它們不必全部經過同一座橋。不同橋接技術可能加入其他垂直結構，因此不要由這張簡化分層圖推論所有產品的供電方式。',
      'In the separated-layer view, trace die-to-die signals separately from power and external connections toward the substrate. They need not all cross the same bridge. Some bridge technologies add vertical structures, so this simplified view must not be used to infer every product’s power-delivery arrangement.',
      '分けた層からダイ間信号と、基板へ向かう電源・外部接続を分けて追います。すべてが同じ橋を渡る必要はありません。縦方向構造を加える方式もあるため、この簡略な分層図から全製品の給電方式を推測してはいけません。',
      '분리한 층에서 다이 간 신호와 기판으로 향하는 전원·외부 연결을 따로 추적합니다. 모두 같은 브리지를 지날 필요는 없습니다. 수직 구조를 추가하는 기술도 있으므로 이 단순화한 층별 보기로 모든 제품의 전력 공급 방식을 추론하면 안 됩니다.',
      '分層示意中先追晶粒到晶粒的连线，再追向基板的供电与外部信号。它们不必全部经过同一座桥。不同桥接技术可能加入其他垂直结构，因此不要由这张简化分层图推论所有产品的供电方式。')),
    C(L('橋再好，也需要共同介面','A bridge needs an interface','橋には共通の接続仕様が必要','브리지에도 공통 인터페이스 필요','桥再好，也需要共同接口'),L(
      '發光路徑表示資料能走的幾何連接，但通訊還需要兩端同意訊號與協定。橋是物理整合方式，不等於某個固定通訊標準。接下來的 UCIe 單元會把「道路怎麼造」和「車輛怎麼對話」分開說清楚。',
      'Glowing paths show geometric connectivity. Communication still requires compatible signaling and protocols at both ends. A bridge is a physical integration approach, not a single communication standard. The UCIe tour separates the question of how roads are built from how participants communicate over them.',
      '光る経路は幾何的な接続です。通信には両端の信号とプロトコルの適合が必要です。橋は物理的な集積方法で、特定の通信規格そのものではありません。UCIe 編では道路の作り方と通信ルールを分けて説明します。',
      '빛나는 경로는 기하학적 연결을 나타냅니다. 통신하려면 양쪽 신호와 프로토콜도 호환되어야 합니다. 브리지는 물리적 통합 방식이지 하나의 통신 표준이 아닙니다. UCIe 안내에서는 도로를 만드는 방식과 그 위에서 통신하는 규칙을 구분합니다.',
      '发光路径表示数据能走的几何连接，但通信还需要两端同意信号与协议。桥是物理集成方式，不等于某个固定通信标准。接下来的 UCIe 单元会把道路怎么造和车辆怎么对话分开说清楚。')),
    C(L('不同材料一起升溫','Materials heat together','異なる材料が共に温まる','서로 다른 재료의 온도 변화','不同材料一起升温'),L(
      '橋、基板與晶粒不是同一種材料。溫度改變時，它們的變形差異會把應力帶到接合區。熱與機械分析應一起看；只看橋很小，不能直接認定它不會成為可靠度風險。',
      'Bridge, substrate and dies are different materials. Temperature changes can create mismatched deformation and concentrate stress near joints. Thermal and mechanical analysis belong together. A small bridge is not automatically free of reliability risk simply because it occupies little area.',
      '橋、基板、ダイは異なる材料です。温度変化による変形の差が接合部に応力を生みます。熱と機械を一緒に解析します。面積が小さいという理由だけで、橋の信頼性リスクがないとは判断できません。',
      '브리지, 기판, 다이는 서로 다른 재료입니다. 온도 변화에 따른 변형 차이는 접합부에 응력을 집중시킬 수 있습니다. 열과 기계 해석을 함께 해야 합니다. 면적이 작다는 이유만으로 신뢰성 위험이 없다고 볼 수는 없습니다.',
      '桥、基板与晶粒不是同一种材料。温度改变时，它们的变形差异会把应力带到接合区。热与机械分析应一起看；只看桥很小，不能直接认定它不会成为可靠性风险。')),
    C(L('先確認橋，再確認系統','Test bridge and system','橋とシステムを順に確認','브리지와 시스템을 각각 검증','先确认桥，再确认系统'),L(
      '檢查通道是否開路或短路，再確認兩端晶粒能在指定條件下交換正確資料。幾何對位、電性連通與系統功能是三層不同證據。若發生錯誤，要能區分接點問題、訊號品質與協定設定。',
      'Check channels for opens and shorts, then verify that the dies exchange correct data under specified conditions. Geometric alignment, electrical continuity and system function are different evidence layers. Diagnose failures by separating joint defects, signal quality and protocol configuration.',
      '断線と短絡を調べ、指定条件で正しいデータを交換できるか確認します。幾何的な整列、電気的導通、システム機能は別々の証拠です。故障時は接点、信号品質、プロトコル設定を切り分けます。',
      '채널의 단선과 단락을 검사한 뒤 정해진 조건에서 두 다이가 올바른 데이터를 교환하는지 확인합니다. 정렬, 전기적 연결, 시스템 기능은 서로 다른 증거입니다. 오류가 나면 접점 결함, 신호 품질, 프로토콜 설정을 분리해 진단합니다.',
      '检查通道是否开路或短路，再确认两端晶粒能在指定条件下交换正确数据。几何对位、电性连通与系统功能是三层不同证据。若发生错误，要能区分接点问题、信号质量与协议设置。')),
    C(L('局部精密的取捨','Trade-offs of local precision','局所的な精密さの選択','국소 정밀 구조의 절충','局部精密的取舍'),L(
      '局部橋可以把精密資源放到真正需要的地方，但晶粒配置與基板整合也因此受到約束。不要只比較矽面積；還要計入組裝難度、供應鏈、測試與良率。選擇的依據是整個產品的需求，不是單一結構的漂亮程度。',
      'Local bridges focus precision where it is needed, but constrain floorplanning and substrate integration. Compare more than silicon area: include assembly complexity, supply chain, testing and yield. The right choice serves the complete product, rather than rewarding the most visually appealing structure.',
      '局所ブリッジは精密さを必要箇所へ集中できますが、配置と基板統合に制約も生みます。シリコン面積だけでなく、組立、供給網、試験、歩留まりを比べます。選択基準は見栄えではなく製品全体の要求です。',
      '로컬 브리지는 필요한 곳에 정밀성을 집중하지만 다이 배치와 기판 통합에 제약을 줍니다. 실리콘 면적뿐 아니라 조립 난도, 공급망, 시험, 수율도 비교해야 합니다. 선택 기준은 구조의 외관이 아니라 제품 전체의 요구입니다.',
      '局部桥可以把精密资源放到真正需要的地方，但晶粒配置与基板集成也因此受到约束。不要只比较硅面积；还要计入组装难度、供应链、测试与良率。选择的依据是整个产品的需求，不是单一结构的漂亮程度。')),
    C(L('從需求找到那座橋','Find the bridge from the need','要求から必要な橋を見つける','요구에서 필요한 다리 찾기','从需求找到那座桥'),L(
      '最後回到俯瞰：選定互通的晶粒、安排邊緣介面、配置局部橋、規劃供電散熱，再用測試證明它們能合作。這個技術的美感是節制：不把所有地方都變複雜，只在最重要的連接處投入精密。',
      'Return overhead: choose communicating dies, arrange edge interfaces, place bridges, plan power and cooling, then prove cooperation through testing. The visual idea is restraint: reserve precision for critical crossings instead of making every part of the package equally complex.',
      '通信するダイ、縁のインターフェース、橋、電源と冷却を配置し、試験で協調動作を証明します。全体を複雑にせず、重要な接続に精密さを注ぐ。その節度が、この技術の美しさです。',
      '통신할 다이와 가장자리 인터페이스, 브리지, 전원·냉각을 배치하고 시험으로 협력을 증명합니다. 모든 부분을 복잡하게 만들지 않고 중요한 연결에 정밀성을 집중하는 절제가 이 기술의 아름다움입니다.',
      '最后回到俯瞰：选定互通的晶粒、安排边缘接口、配置局部桥、规划供电散热，再用测试证明它们能合作。这个技术的美感是节制：不把所有地方都变复杂，只在最重要的连接处投入精密。'))
  ]));
  tours.push(T('chiplet',
    L('Chiplet 與 UCIe 互連','Chiplets & UCIe','チップレットと UCIe','칩렛과 UCIe','Chiplet 与 UCIe 互连'),
    L('把一個系統拆成分工清楚的晶粒，再以相容介面重組；看懂實體連接與通訊規則的差別。','Partition a system into specialized dies, then reconnect them through compatible physical and protocol interfaces.','システムを役割別のダイに分け、物理接続と通信規則を揃えて再構成します。','시스템을 역할별 다이로 나누고 호환되는 물리 연결과 통신 규칙으로 다시 연결합니다.','把一个系统拆成分工清楚的晶粒，再以兼容接口重组；看懂实体连接与通信规则的差别。'),
    ['ucie','intel','cowos','test'],[
    C(L('先畫功能地圖','Begin with a function map','まず機能の地図を描く','기능 지도부터 그리기','先画功能地图'),L(
      '俯瞰運算、記憶體控制與輸入輸出等功能街區。Chiplet 是把系統分成可整合的晶粒，不是把任意晶片放在一起就會合作。先畫出誰需要交換哪些資料，再決定哪些功能值得拆開。',
      'Look over districts for compute, memory control and input/output. Chiplets partition a system into integrable dies; placing arbitrary chips together does not make them cooperate. First map which functions exchange which data, then decide where splitting the system is worthwhile.',
      '演算、メモリー制御、入出力の街区を見渡します。チップレットは統合可能なダイへの分割であり、任意のチップを並べることではありません。まず機能間のデータ交換を描き、どこを分ける価値があるか決めます。',
      '연산, 메모리 제어, 입출력 구역을 내려다봅니다. 칩렛은 통합 가능한 다이로 시스템을 나누는 방식이지 임의의 칩을 모으는 것이 아닙니다. 먼저 어떤 기능이 어떤 데이터를 교환하는지 그린 뒤 분할할 지점을 정합니다.',
      '俯瞰计算、内存控制与输入输出等功能街区。Chiplet 是把系统分成可集成的晶粒，不是把任意芯片放在一起就会合作。先画出谁需要交换哪些数据，再决定哪些功能值得拆开。')),
    C(L('讓製程配合功能','Match process to function','機能に製造技術を合わせる','기능에 공정 맞추기','让工艺配合功能'),L(
      '不同功能未必需要相同的製程條件。拆分可以讓各晶粒採用適合的技術，也帶來介面、供電與封裝整合成本。這是一種設計選項，不是任何產品都必須改成 Chiplet；小而單純的系統可能有別的最佳解。',
      'Different functions need not use the same process technology. Partitioning can match technology to purpose, but adds interface, power and packaging costs. Chiplets are a design option, not a requirement for every product; a smaller, simpler system may favor another architecture.',
      'すべての機能が同じ製造技術を必要とするわけではありません。分割で技術を選べますが、接続、電源、パッケージのコストも増えます。チップレットは選択肢であり、単純な小規模システムでは別の構成が適する場合があります。',
      '모든 기능이 같은 공정 기술을 필요로 하지는 않습니다. 분할하면 기능에 맞는 기술을 선택할 수 있지만 인터페이스, 전원, 패키징 비용이 추가됩니다. 칩렛은 설계 선택지이며 작고 단순한 시스템에는 다른 구성이 더 적합할 수 있습니다.',
      '不同功能未必需要相同的工艺条件。拆分可以让各晶粒采用适合的技术，也带来接口、供电与封装集成成本。这是一种设计选项，不是任何产品都必须改成 Chiplet；小而单纯的系统可能有别的最佳解。')),
    C(L('UCIe 是共通的介面規則','UCIe defines interface rules','UCIe は接続の規則','UCIe는 인터페이스 규칙','UCIe 是共通的接口规则'),L(
      '現在看晶粒邊界：UCIe 針對封裝內晶粒間互連定義介面規則，涵蓋實體層與相關通訊機制。它不是某種矽橋，也不是冷卻技術。把「封裝結構」和「互連標準」分開，才能正確組合方案。',
      'At the die boundary, UCIe supplies standardized rules for on-package die-to-die connectivity, including physical and communication mechanisms. It is not a silicon bridge or a cooling technology. Separate the package structure from the interconnect standard before combining them into a system.',
      'ダイの境界で、UCIe はパッケージ内のダイ間接続に物理層や通信機構の共通規則を与えます。シリコンブリッジや冷却技術ではありません。パッケージ構造と相互接続規格を分けて理解してから組み合わせます。',
      '다이 경계에서 UCIe는 패키지 내부 다이 간 연결의 물리 계층과 통신 방식에 공통 규칙을 제공합니다. 실리콘 브리지나 냉각 기술이 아닙니다. 패키지 구조와 연결 표준을 구분한 뒤 시스템으로 조합해야 합니다.',
      '现在看晶粒边界：UCIe 针对封装内晶粒间互连定义接口规则，涵盖物理层与相关通信机制。它不是某种硅桥，也不是冷却技术。把封装结构和互连标准分开，才能正确组合方案。')),
    C(L('共同設計，不是事後拼裝','Co-design before assembly','組立前に協調設計する','조립 전에 공동 설계','共同设计，不是事后拼装'),L(
      '把晶粒放進規劃位置之前，先確認介面位置、電源需求、時脈策略與封裝能力。標準化能減少協調成本，卻不會自動解決所有相容問題。這裡的拼合動作代表經過設計的整合，不是隨插即用的保證。',
      'Before placing dies, align interface locations, power requirements, clocking strategy and package capability. Standardization can reduce coordination work, but cannot automatically solve every compatibility issue. The assembly animation represents designed integration, not a guarantee that any two components are plug-and-play.',
      '搭載前にインターフェース位置、電源、クロック、パッケージ技術の能力を揃えます。標準化は調整を減らせても、全ての相性問題を自動解決しません。模型の組合せは設計済みの統合であり、任意部品の交換可能性を保証しません。',
      '다이를 놓기 전에 인터페이스 위치, 전원 요구, 클록 전략, 패키지 능력을 맞춥니다. 표준화는 조정 비용을 줄이지만 모든 호환성 문제를 자동으로 해결하지 않습니다. 조립 장면은 설계된 통합이며 아무 부품이나 꽂아 쓸 수 있다는 보장이 아닙니다.',
      '把晶粒放进规划位置之前，先确认接口位置、电源需求、时钟策略与封装能力。标准化能减少协调成本，却不会自动解决所有兼容问题。这里的拼合动作代表经过设计的集成，不是即插即用的保证。')),
    C(L('實體層與協定各管什麼','Physical layer and protocol','物理層とプロトコルの分担','물리 계층과 프로토콜의 역할','实体层与协议各管什么'),L(
      '在剖面看金屬與接點，在上方看訊息如何交換。實體連接回答訊號能否可靠傳送，協定則規範資料如何被理解與管理。相同連線形狀不代表相同語意；系統必須核對雙方實際支援的功能。',
      'The section reveals metal and contacts; the upper view shows messages. Physical connectivity addresses reliable signaling, while protocols organize the meaning and management of data. Similar-looking connections need not carry identical semantics. Verify what functions both endpoints actually support.',
      '断面では金属と接点、上ではメッセージを見ます。物理接続は信号を確実に運べるかを扱い、プロトコルは意味と管理を定めます。同じ形でも意味は同じとは限らず、両端が対応する機能を確認します。',
      '단면에서는 금속과 접점을, 위에서는 메시지를 봅니다. 물리 연결은 신뢰할 수 있는 신호 전달을, 프로토콜은 데이터의 의미와 관리를 다룹니다. 연결 모양이 같아도 의미가 같지는 않으므로 양쪽이 실제 지원하는 기능을 확인해야 합니다.',
      '在剖面看金属与接点，在上方看消息如何交换。实体连接回答信号能否可靠传送，协议则规范数据如何被理解与管理。相同连线形状不代表相同语义；系统必须核对双方实际支持的功能。')),
    C(L('搬運資料也會花時間','Communication has a cost','通信にも時間と電力がかかる','통신에도 비용이 든다','搬运数据也会花时间'),L(
      '跟著資料從一個功能區移到另一個，留意每次跨界都需要介面工作。拆分得太細，可能增加溝通與同步負擔。路線圖要標出資料量、延遲與能量預算，不能只把每個區塊的算力加總。',
      'Follow data between functional districts. Every boundary crossing requires interface work; excessive partitioning can add communication and synchronization overhead. The roadmap must budget data volume, latency and energy instead of merely adding up the computing capability of individual blocks.',
      '機能間のデータを追うと、境界ごとにインターフェース処理が必要です。細かく分けすぎると通信と同期の負担が増えます。各ブロックの計算能力を足すだけでなく、データ量、遅延、エネルギーを配分します。',
      '기능 구역 사이의 데이터를 따라가면 경계마다 인터페이스 동작이 필요합니다. 지나친 분할은 통신과 동기화 부담을 늘릴 수 있습니다. 블록별 연산 성능만 더하지 말고 데이터량, 지연, 에너지 예산을 정해야 합니다.',
      '跟着数据从一个功能区移到另一个，留意每次跨界都需要接口工作。拆分得太细，可能增加沟通与同步负担。路线图要标出数据量、延迟与能量预算，不能只把每个区块的算力加总。')),
    C(L('一個熱點會影響鄰居','A hotspot affects its neighbors','熱点は隣にも影響する','열점은 이웃에도 영향을 준다','一个热点会影响邻居'),L(
      '把功能地圖切換成概念熱圖，觀察高負載晶粒與旁邊元件的距離。系統效能可能受最熱、最缺電或最忙的連線限制。設計應協調功率管理與散熱，不能把每個晶粒當成互不影響的孤島。',
      'Switch the function map to an illustrative heat map. Observe the distance between a busy die and its neighbors. System performance may be limited by the hottest die, weakest power path or busiest link. Coordinate power management and cooling rather than treating dies as isolated islands.',
      '機能地図を概念的な熱地図へ変えます。高負荷ダイと周囲の距離を見てください。最も熱いダイ、弱い給電、混雑したリンクが性能を制限します。独立した島と考えず、電力管理と冷却を協調させます。',
      '기능 지도를 개념적 열 지도로 바꿉니다. 부하가 큰 다이와 이웃 부품의 거리를 봅니다. 가장 뜨거운 다이, 약한 전원 경로, 혼잡한 링크가 성능을 제한할 수 있습니다. 독립된 섬처럼 다루지 말고 전력 관리와 냉각을 조율해야 합니다.',
      '把功能地图切换成概念热图，观察高负载晶粒与旁边元件的距离。系统性能可能受最热、最缺电或最忙的连线限制。设计应协调功率管理与散热，不能把每个晶粒当成互不影响的孤岛。')),
    C(L('相容性需要測試證據','Compatibility needs evidence','互換性には試験の証拠が必要','호환성에는 시험 증거가 필요','兼容性需要测试证据'),L(
      '檢查站不只問晶粒各自能否工作，也問連在一起是否符合共同條件。驗證連線啟動、錯誤處理與目標工作負載，並保留版本與設定紀錄。貼上 UCIe 名稱不等於完成所有產品層級的相容性驗證。',
      'Test not only whether dies work separately, but whether the assembled system meets shared conditions. Exercise link startup, error handling and target workloads; record versions and configurations. A UCIe label does not replace complete product-level integration and interoperability validation.',
      '個別のダイだけでなく、接続したシステムが共通条件を満たすか試験します。リンク起動、エラー処理、対象負荷を確認し、版と設定を記録します。UCIe の名称だけでは製品全体の相互運用検証を代替できません。',
      '다이가 개별적으로 작동하는지뿐 아니라 통합 시스템이 공통 조건을 만족하는지 시험합니다. 링크 시작, 오류 처리, 목표 작업 부하를 확인하고 버전과 설정을 기록합니다. UCIe라는 이름이 제품 전체의 통합·상호운용성 검증을 대신하지는 않습니다.',
      '检查站不只问晶粒各自能否工作，也问连在一起是否符合共同条件。验证连线启动、错误处理与目标工作负载，并保留版本与设置记录。贴上 UCIe 名称不等于完成所有产品层级的兼容性验证。')),
    C(L('重用的好處與整合的代價','Reuse and integration effort','再利用と統合の負担','재사용과 통합의 부담','复用的好处与集成的代价'),L(
      '重用晶粒可以讓產品組合更靈活，但也增加供應商、版本與驗證工作的協調。比較單晶片與 Chiplet 時，要看開發時間、良品成本與長期維護。沒有一種拆分方式適合所有需求，路線圖應保留取捨依據。',
      'Reusing chiplets can make product families more flexible, while adding supplier, version and validation coordination. Compare monolithic and chiplet designs using development time, cost per good unit and long-term maintenance. No partition fits every need; preserve the reasoning behind each architectural trade-off.',
      '再利用は製品展開を柔軟にしますが、供給元、版、検証の調整も増えます。一枚のチップと比較するときは開発期間、良品単価、長期保守を見ます。万能な分割はなく、選択理由を地図に残します。',
      '칩렛 재사용은 제품 구성을 유연하게 하지만 공급업체, 버전, 검증의 조정도 늘립니다. 단일 칩과 비교할 때 개발 기간, 양품 단가, 장기 유지보수를 함께 봅니다. 모든 요구에 맞는 분할은 없으므로 선택 근거를 남겨야 합니다.',
      '复用晶粒可以让产品组合更灵活，但也增加供应商、版本与验证工作的协调。比较单芯片与 Chiplet 时，要看开发时间、良品成本与长期维护。没有一种拆分方式适合所有需求，路线图应保留取舍依据。')),
    C(L('把分工重新接成系統','Reconnect the system','分担を一つのシステムへ','분담을 하나의 시스템으로','把分工重新接成系统'),L(
      '最後俯瞰功能分割、介面選擇、實體封裝、供電散熱與系統驗證。你應能分清三件事：晶粒負責什麼、封裝怎麼連、協定怎麼合作。Chiplet 的美感是有秩序的分工，而完整證據讓分工真正成立。',
      'Survey partitioning, interface selection, physical packaging, power, cooling and system validation. Distinguish three questions: what each die does, how the package connects it and how protocols coordinate behavior. Chiplet elegance comes from orderly specialization, supported by evidence that the whole system works.',
      '機能分割、接続規格、物理的なパッケージ、電源、冷却、システム検証を見渡します。ダイの役割、パッケージのつなぎ方、通信の協調という三点を区別します。秩序ある分担が美しさを生み、検証がそれを成立させます。',
      '기능 분할, 인터페이스 선택, 물리 패키징, 전원, 냉각, 시스템 검증을 내려다봅니다. 각 다이의 역할, 패키지의 연결 방식, 프로토콜의 협력을 구분하세요. 질서 있는 분담이 칩렛의 아름다움이며 전체 시스템의 작동 증거가 이를 완성합니다.',
      '最后俯瞰功能分割、接口选择、实体封装、供电散热与系统验证。你应能分清三件事：晶粒负责什么、封装怎么连、协议怎么合作。Chiplet 的美感是有秩序的分工，而完整证据让分工真正成立。'))
  ]));
  tours.push(T('thermal',
    L('散熱、測試與可靠度','Thermal, test & reliability','熱・試験・信頼性','열·시험·신뢰성','散热、测试与可靠性'),
    L('沿著熱與證據的路線飛行，從漂亮的封裝模型走向可驗證的工程系統。','Follow heat and evidence from an attractive package model to a verifiable engineering system.','熱と検証の経路をたどり、美しい模型を確かめられる工学システムへつなげます。','열과 검증의 경로를 따라 아름다운 패키지 모델을 검증 가능한 공학 시스템으로 연결합니다.','沿着热与证据的路线飞行，从漂亮的封装模型走向可验证的工程系统。'),
    ['stress','test','cowos','intel'],[
    C(L('成功不只等於接得上','Connected is not yet qualified','つながるだけでは完成しない','연결만으로는 완성이 아니다','成功不只等于接得上'),L(
      '先從上方看完整封裝：晶粒、接點、基板與散熱結構要在指定環境中長期合作。今天的路線不只看資料流，而是問「熱能否出去、缺陷能否發現、壽命是否有證據」。這些問題從設計開始就要加入。',
      'Survey the complete package: dies, joints, substrate and cooling must cooperate in a specified environment over time. Today’s route asks whether heat can escape, defects can be found and lifetime claims have evidence. These questions belong at the beginning of design, not only at final inspection.',
      'ダイ、接点、基板、冷却が所定環境で長く協調する必要があります。今日は熱の出口、欠陥の発見、寿命の根拠をたどります。これらは最終検査だけの問題ではなく、設計の最初から考える問いです。',
      '다이, 접점, 기판, 냉각 구조는 정해진 환경에서 오랫동안 함께 작동해야 합니다. 오늘은 열이 빠져나가는지, 결함을 찾을 수 있는지, 수명 주장에 증거가 있는지 살펴봅니다. 이 질문은 최종 검사뿐 아니라 설계 초기부터 포함해야 합니다.',
      '先从上方看完整封装：晶粒、接点、基板与散热结构要在指定环境中长期合作。今天的路线不只看数据流，而是问热能否出去、缺陷能否发现、寿命是否有证据。这些问题从设计开始就要加入。')),
    C(L('先列出熱從哪裡來','Locate the heat sources','熱源を先に確認する','먼저 열원 찾기','先列出热从哪里来'),L(
      '沿著各晶粒停靠，標出不同工作負載下的功率分布。總功率相同，熱點位置不同，溫度結果仍可能不同。散熱設計需要空間與時間資訊，不能只拿一個平均瓦數代表所有使用情境。',
      'Visit each die and consider power distribution under different workloads. Equal total power can produce different temperatures when hotspots move. Cooling design needs spatial and time-dependent information; one average power number cannot represent every operating condition.',
      '各ダイで負荷ごとの電力分布を考えます。総電力が同じでも熱点の位置で温度は変わります。冷却設計には場所と時間の情報が必要で、一つの平均電力だけでは全使用条件を表せません。',
      '각 다이에서 작업 부하에 따른 전력 분포를 살펴봅니다. 총전력이 같아도 열점 위치가 바뀌면 온도가 달라질 수 있습니다. 냉각 설계에는 공간과 시간 정보가 필요하며 평균 전력 하나로 모든 사용 조건을 대표할 수 없습니다.',
      '沿着各晶粒停靠，标出不同工作负载下的功率分布。总功率相同，热点位置不同，温度结果仍可能不同。散热设计需要空间与时间信息，不能只拿一个平均瓦数代表所有使用情境。')),
    C(L('界面也是熱的關卡','Interfaces resist heat flow','界面は熱の通過点','계면도 열 이동의 관문','界面也是热的关卡'),L(
      '從晶粒向上飛，穿過熱介面材料、上蓋與散熱器。每一層的厚度、接觸狀態與材料特性都可能限制熱流。不是只換一個更大的散熱器就一定有效；先找真正瓶頸在哪一段。',
      'Travel upward from the die through interface material, lid and cooler. Thickness, contact quality and material properties can each restrict heat flow. A larger cooler alone may not solve the problem. Identify the limiting part of the path before changing the hardware.',
      'ダイから界面材料、ふた、冷却器へ上がります。厚さ、接触状態、材料特性が熱流を制限します。冷却器だけを大型化しても解決しない場合があります。部品変更の前に、経路のどこが律速かを探します。',
      '다이에서 계면 재료, 덮개, 냉각기로 올라갑니다. 두께, 접촉 품질, 재료 특성은 각각 열 이동을 제한할 수 있습니다. 냉각기를 크게 바꾸는 것만으로 해결되지 않을 수 있으므로 먼저 실제 병목 구간을 찾아야 합니다.',
      '从晶粒向上飞，穿过热界面材料、上盖与散热器。每一层的厚度、接触状态与材料特性都可能限制热流。不是只换一个更大的散热器就一定有效；先找真正瓶颈在哪一段。')),
    C(L('裝配會改變散熱路徑','Assembly changes the heat path','組立が熱経路を変える','조립이 열 경로를 바꾼다','装配会改变散热路径'),L(
      '把上蓋與介面分離，觀察接觸是否均勻、材料是否連續。厚度差與空隙可能改變熱阻，機械固定也會影響接觸。這是理解品質的觀察框架，不提供可直接套用到產品的壓力或材料厚度設定。',
      'Separate lid and interface to examine uniform contact and material continuity. Thickness variation and voids can change thermal resistance, while mechanical attachment affects contact. This is an inspection framework, not a transferable prescription for clamping pressure or interface thickness on a real product.',
      'ふたと界面を分け、均一な接触と材料の連続性を見ます。厚さの差や空隙は熱抵抗を変え、固定方法も影響します。これは品質を見る枠組みで、実製品へそのまま適用できる圧力や厚さの設定ではありません。',
      '덮개와 계면을 분리해 접촉 균일성과 재료 연속성을 확인합니다. 두께 편차와 빈틈은 열저항을 바꾸고 고정 방식도 접촉에 영향을 줍니다. 이는 품질 관찰 틀이며 실제 제품에 그대로 적용할 압력이나 두께 설정값은 아닙니다.',
      '把上盖与界面分离，观察接触是否均匀、材料是否连续。厚度差与空隙可能改变热阻，机械固定也会影响接触。这是理解质量的观察框架，不提供可直接套用到产品的压力或材料厚度设置。')),
    C(L('把熱路徑看成串接網路','Read the thermal network','熱経路をネットワークで見る','열 경로를 네트워크로 보기','把热路径看成串接网络'),L(
      '分層示意讓你看到熱不只往單一方向走，也可能經基板與周圍結構分流。簡化熱阻網路可幫助初步判斷，但必須交代模型假設。動畫顏色沒有溫度刻度，不能用來讀出結溫或驗收產品。',
      'The separated-layer view shows heat can split through the substrate and surrounding structures, not only move upward. A simplified thermal-resistance network helps early reasoning if its assumptions are stated. The animation has no temperature scale and cannot provide junction-temperature readings or product acceptance results.',
      '熱は上だけでなく、基板や周囲にも分かれて流れます。仮定を明示した簡易熱抵抗網は初期検討に役立ちます。映像の色には温度目盛がなく、接合温度の読み取りや製品合否判定には使えません。',
      '열은 위로만 흐르지 않고 기판과 주변 구조로 나뉘기도 합니다. 가정을 명시한 단순 열저항망은 초기 판단에 도움이 됩니다. 애니메이션 색에는 온도 눈금이 없으므로 접합 온도를 읽거나 제품 합격을 판정할 수 없습니다.',
      '分层示意让你看到热不只往单一方向走，也可能经基板与周围结构分流。简化热阻网络可帮助初步判断，但必须交代模型假设。动画颜色没有温度刻度，不能用来读出结温或验收产品。')),
    C(L('先證明功能，再追查失效','Function and failure evidence','機能を確認して故障を追う','기능 확인과 고장 추적','先证明功能，再追查失效'),L(
      '讓示意訊號通過系統，區分元件測試、封裝後電性測試與系統級工作負載。不同測試抓到不同失效。當結果不符預期，先保存條件與症狀，再把問題縮小到供電、連線、熱或邏輯等可能來源。',
      'Follow a test signal and distinguish component tests, post-package electrical tests and system workloads. They expose different failures. When a result is unexpected, preserve conditions and symptoms before narrowing the cause to power, interconnect, temperature, logic or another subsystem.',
      '試験信号を追い、部品試験、パッケージ化後の電気試験、システム負荷を区別します。検出する故障は異なります。予想外の結果では条件と症状を保存し、電源、配線、熱、論理などへ原因を絞ります。',
      '시험 신호를 따라 부품 시험, 패키징 후 전기 시험, 시스템 작업 부하를 구분합니다. 각 시험은 다른 고장을 드러냅니다. 예상과 다르면 조건과 증상을 보존한 뒤 전원, 연결, 온도, 논리 등으로 원인을 좁힙니다.',
      '让示意信号通过系统，区分元件测试、封装后电性测试与系统级工作负载。不同测试抓到不同失效。当结果不符预期，先保存条件与症状，再把问题缩小到供电、连线、热或逻辑等可能来源。')),
    C(L('溫度循環會累積應力','Thermal cycles accumulate stress','温度サイクルと応力','온도 주기에 따른 응력 누적','温度循环会累积应力'),L(
      '觀看加熱與冷卻時的概念變形，不同材料會反覆拉扯接點與界面。可靠度關心的是時間與循環下的變化，不只是剛組裝完能否通電。實際試驗條件應依使用環境與適用規範制定，不能由示意動畫決定。',
      'Watch conceptual expansion and contraction as different materials load joints and interfaces repeatedly. Reliability concerns change over time and cycling, not merely successful power-on after assembly. Real test conditions must follow the use environment and applicable qualification requirements, never the timing of this illustration.',
      '加熱と冷却で異なる材料が接点と界面に繰り返し力を与えます。信頼性は組立直後の通電だけでなく、時間と繰返しによる変化を扱います。実試験条件は使用環境と適用要件で定め、映像の周期から決めません。',
      '가열과 냉각에서 서로 다른 재료가 접점과 계면에 반복 하중을 줍니다. 신뢰성은 조립 직후 전원이 켜지는 것뿐 아니라 시간과 반복에 따른 변화를 다룹니다. 실제 시험 조건은 사용 환경과 적용 요구사항으로 정해야 하며 영상 주기를 따라서는 안 됩니다.',
      '观看加热与冷却时的概念变形，不同材料会反复拉扯接点与界面。可靠性关心的是时间与循环下的变化，不只是刚组装完能否通电。实际试验条件应依使用环境与适用规范制定，不能由示意动画决定。')),
    C(L('多種證據交叉比對','Cross-check different evidence','異なる証拠を照合する','서로 다른 증거 교차 확인','多种证据交叉比对'),L(
      '在檢查站結合影像、電性、溫度與失效位置。單張影像能提示異常，卻不能獨自證明根因。把模型預測和量測比較，記錄誤差與不確定性；只有經過驗證的數據，才應出現在工程結論裡。',
      'Combine images, electrical results, temperatures and failure locations. One image can suggest a problem without proving its cause. Compare model predictions with measurements and record error and uncertainty. Engineering conclusions should be supported by validated data rather than the apparent realism of a visualization.',
      '画像、電気結果、温度、故障位置を照合します。一枚の画像は異常を示唆しても根因を証明できません。予測と測定を比べ、誤差と不確かさを記録します。見た目のリアルさではなく、検証済みデータで結論を支えます。',
      '영상, 전기 결과, 온도, 고장 위치를 함께 봅니다. 한 장의 영상은 이상을 시사해도 원인을 증명하지는 못합니다. 모델 예측과 측정을 비교하고 오차와 불확실성을 기록합니다. 사실적인 화면이 아니라 검증된 데이터로 공학적 결론을 뒷받침해야 합니다.',
      '在检查站结合影像、电性、温度与失效位置。单张影像能提示异常，却不能独自证明根因。把模型预测和测量比较，记录误差与不确定性；只有经过验证的数据，才应出现在工程结论里。')),
    C(L('改善要有同一個比較基準','Improve against a fair baseline','同じ基準で改善を比べる','같은 기준으로 개선 비교','改善要有同一个比较基准'),L(
      '比較兩種散熱或封裝方案時，固定工作負載、環境與量測方法，再看溫度、功耗、可靠度與成本。若同時改了太多條件，就難以判斷哪個改動有效。漂亮的下降曲線，必須能回到可重做的實驗。',
      'Compare package or cooling options under the same workload, environment and measurement method, then evaluate temperature, power, reliability and cost. Changing many conditions at once obscures causality. An attractive improvement curve must be traceable to an experiment that can be repeated.',
      '同じ負荷、環境、測定方法で温度、電力、信頼性、費用を比べます。多くの条件を同時に変えると、何が効いたか分かりません。美しい改善曲線も、再現できる実験へ戻れる必要があります。',
      '같은 작업 부하, 환경, 측정 방법으로 온도, 전력, 신뢰성, 비용을 비교합니다. 여러 조건을 동시에 바꾸면 어떤 변경이 효과가 있었는지 알기 어렵습니다. 보기 좋은 개선 곡선도 반복 가능한 실험으로 추적할 수 있어야 합니다.',
      '比较两种散热或封装方案时，固定工作负载、环境与测量方法，再看温度、功耗、可靠性与成本。若同时改了太多条件，就难以判断哪个改动有效。漂亮的下降曲线，必须能回到可重做的实验。')),
    C(L('把美感落在可驗證的秩序','Beauty in verifiable order','検証できる秩序の美しさ','검증 가능한 질서의 아름다움','把美感落在可验证的秩序'),L(
      '最後升高，看需求、熱路徑、裝配品質、測試與可靠度如何連成一圈。先進封裝的美感不只是精密層次，而是每一條資料、電力與熱的路線都有去處，每一項結論都有證據。現在你可以帶著這張地圖，回到任何一種封裝技術。',
      'Rise to see requirements, heat paths, assembly quality, testing and reliability form a feedback loop. Advanced packaging is beautiful when data, power and heat have deliberate routes and conclusions have evidence. Carry this map back to any packaging technology and ask how the complete system is verified.',
      '要求、熱経路、組立品質、試験、信頼性が循環する全体を見ます。データ、電力、熱に意図した経路があり、結論に根拠があることが美しさです。この地図を持って、どのパッケージ技術でもシステム全体の検証を問いましょう。',
      '요구사항, 열 경로, 조립 품질, 시험, 신뢰성이 피드백 고리를 이루는 전체를 봅니다. 데이터·전력·열에 의도된 경로가 있고 결론에 증거가 있을 때 첨단 패키징은 아름답습니다. 이 지도를 가지고 어떤 패키징 기술에서도 전체 시스템의 검증을 물어보세요.',
      '最后升高，看需求、热路径、装配质量、测试与可靠性如何连成一圈。先进封装的美感不只是精密层次，而是每一条数据、电力与热的路线都有去处，每一项结论都有证据。现在你可以带着这张地图，回到任何一种封装技术。'))
  ]));
  root.MACGYVER_PACKAGING_TOURS = {version:1,revision:'2026-11-23',duration:300,languages,labels,tours,sourceLibrary,
    disclaimer:L('工程教學重建｜非廠房實拍｜比例與動態為理解而調整','Educational reconstruction · not facility footage · scales and motion adjusted for clarity','工学教材の再構成・工場の実写ではありません・尺度と動きは説明用です','공학 교육용 재구성 · 실제 공장 촬영 아님 · 이해를 위해 비율과 동작 조정','工程教学重建｜非厂房实拍｜比例与动态为理解而调整')};
})(typeof window !== 'undefined' ? window : globalThis);
