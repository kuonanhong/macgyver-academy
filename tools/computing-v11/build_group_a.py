"""V11 original bilingual computing architecture lessons.
Reproduce: python3 tools/computing-v11/build_group_a.py (Python 3.10+).
Public primary references are linked, never copied. All workloads and numbers are
original hypothetical exercises in an owned, isolated simulator. No live scanning.
Immutable V10 stages, IDs and curriculum versions remain byte-equivalent objects.
"""
import copy, json, math, pathlib
P=pathlib.Path(__file__).resolve().parent
SNAP=json.loads((P/'group_a_snapshot.json').read_text())
CAT={c['id']:c for c in SNAP['catalog']}; OLD={c['id']:c for c in SNAP['existing']}
S={}; D={}
def source(key,title,pub,url,ref):
 zh,en=title.split('~');S[key]={'id':'v11a-'+key,'title':zh,'titleEn':en,'publisher':pub,'url':url,'category':'computing','sourceType':'primary','accessedAt':'2026-10-14','verificationRef':ref,'imageReuse':'僅連結官方文件；未重製原圖或影片。','imageReuseEn':'Official links only; no artwork or video reproduced.','scope':'支援公開架構與介面原理；課程的工作負載、圖解與數字為原創假想案例，非廠商效能保證。','scopeEn':'Supports public architecture and interface principles; workloads, diagrams and numbers are original hypothetical cases, not vendor performance guarantees.'}
source('zt','零信任架構 SP 800-207~Zero Trust Architecture SP 800-207','NIST','https://csrc.nist.gov/pubs/sp/800/207/final','turn497view0')
source('controls','安全與隱私控制 SP 800-53~Security and Privacy Controls SP 800-53','NIST','https://csrc.nist.gov/pubs/sp/800/53/r5/upd1/final','turn527view6')
source('o3','亂序 CPU 模型~Out-of-order CPU model','gem5','https://www.gem5.org/documentation/general_docs/cpu_models/O3CPU','turn495search3')
source('minor','順序 CPU 模型~In-order CPU model','gem5','https://www.gem5.org/documentation/general_docs/cpu_models/minor_cpu','turn495search30')
source('coherence','快取一致性協定~Cache coherence protocols','gem5','https://www.gem5.org/documentation/general_docs/ruby/cache-coherence-protocols/','turn493search7')
source('false','假共享的辨識~False-sharing diagnosis','Linux kernel community','https://docs.kernel.org/kernel-hacking/false-sharing.html','turn493search31')
source('cuda','CUDA 程式設計模型~CUDA programming model','NVIDIA','https://docs.nvidia.com/cuda/cuda-programming-guide/01-introduction/programming-model.html','turn493search0')
source('cudaadvanced','CUDA 進階核心設計~Advanced CUDA kernel programming','NVIDIA','https://docs.nvidia.com/cuda/cuda-programming-guide/03-advanced/advanced-kernel-programming.html','turn493search5')
source('tpu','TPU 系統架構~TPU system architecture','Google Cloud','https://docs.cloud.google.com/tpu/docs/system-architecture-tpu-vm','turn495search0')
source('bf16','TPU 的 bfloat16 選擇~TPU bfloat16 design','Google Cloud','https://cloud.google.com/blog/products/ai-machine-learning/bfloat16-the-secret-to-high-performance-on-cloud-tpus','turn495search23')
source('hls','Vitis 高階合成指南~Vitis High-Level Synthesis guide','AMD','https://docs.amd.com/r/en-US/ug1399-vitis-hls','turn493search4')
source('dataflow','資料流與相依性驗證~Dataflow and dependency verification','AMD','https://docs.amd.com/r/en-US/ug1399-vitis-hls/Verification-of-DATAFLOW-and-DEPENDENCE','turn493search6')
source('noc','片上互連網路~On-chip interconnection network','gem5','https://www.gem5.org/documentation/general_docs/ruby/interconnection-network/','turn493search1')
source('garnet','Garnet 路由器模型~Garnet router model','gem5','https://www.gem5.org/documentation/general_docs/ruby/garnet-2/','turn493search3')
source('edac','記憶體錯誤偵測與更正~Memory error detection and correction','Linux kernel community','https://cdn.kernel.org/doc/html/latest/driver-api/edac.html','turn495search4')
source('scrub','記憶體巡檢控制~Memory scrub control','Linux kernel community','https://cdn.kernel.org/doc/html/latest/edac/scrub.html','turn495search19')
source('schedule','Zephyr 排程服務~Zephyr scheduling services','Zephyr Project','https://docs.zephyrproject.org/latest/kernel/services/scheduling/index.html','turn495search5')
source('mutex','Zephyr 互斥鎖與優先權繼承~Zephyr mutexes and priority inheritance','Zephyr Project','https://docs.zephyrproject.org/latest/kernel/services/synchronization/mutexes.html','turn495search2')
source('firmware','平臺韌體韌性 SP 800-193~Platform Firmware Resiliency SP 800-193','NIST','https://csrc.nist.gov/pubs/sp/800/193/final','turn497view1')
source('verified','U-Boot 驗證啟動~U-Boot verified boot','U-Boot community','https://docs.u-boot.org/en/latest/usage/fit/verified-boot.html','turn497view2')
source('riscvboot','RISC-V 核心啟動條件~RISC-V kernel boot requirements','Linux kernel community','https://docs.kernel.org/arch/riscv/boot.html','turn497view3')
source('dt','Linux 裝置樹模型~Linux devicetree model','Linux kernel community','https://docs.kernel.org/devicetree/usage-model.html','turn497view4')
source('ipc','seL4 行程間通訊~seL4 interprocess communication','seL4 Foundation','https://docs.sel4.systems/Tutorials/ipc','turn497view5')
source('proof','seL4 證明的假設~seL4 proof assumptions','seL4 Foundation','https://sel4.systems/Verification/assumptions.html','turn499search2')
source('dma','動態 DMA 映射指南~Dynamic DMA mapping guide','Linux kernel community','https://docs.kernel.org/core-api/dma-api-howto.html','turn527view7')
source('driver','Linux 裝置模型~Linux device model','Linux kernel community','https://docs.kernel.org/driver-api/driver-model/overview.html','turn497view8')
source('ir','LLVM 語言參考~LLVM language reference','LLVM Project','https://llvm.org/docs/LangRef.html','turn521view9')
source('lexer','LLVM 詞法與前端教學~LLVM lexer and frontend tutorial','LLVM Project','https://www.llvm.org/docs/tutorial/MyFirstLanguageFrontend/LangImpl01.html','turn499search6')
source('orc','ORC JIT 架構~ORC JIT architecture','LLVM Project','https://llvm.org/docs/ORCv2.html','turn499search5')
source('hdfs','HDFS 架構~HDFS architecture','Apache Software Foundation','https://hadoop.apache.org/docs/current/hadoop-project-dist/hadoop-hdfs/HdfsDesign.html','turn506view0')
source('hdfsec','HDFS 抹除編碼~HDFS erasure coding','Apache Software Foundation','https://hadoop.apache.org/docs/current/hadoop-project-dist/hadoop-hdfs/HDFSErasureCoding.html','turn506view1')
source('object','Ceph 物件閘道~Ceph object gateway','Ceph Project','https://docs.ceph.com/en/latest/radosgw/','turn506view2')
source('ceph','Ceph 抹除編碼~Ceph erasure coding','Ceph Project','https://docs.ceph.com/en/latest/rados/operations/erasure-code/','turn506view3')
source('wal','PostgreSQL 預寫日誌~PostgreSQL write-ahead logging','PostgreSQL Global Development Group','https://www.postgresql.org/docs/current/wal-intro.html','turn506view4')
source('isolation','PostgreSQL 交易隔離~PostgreSQL transaction isolation','PostgreSQL Global Development Group','https://www.postgresql.org/docs/current/transaction-iso.html','turn506view5')
source('raft','Raft 共識原始論文~Original Raft consensus paper','Diego Ongaro and John Ousterhout','https://raft.github.io/raft.pdf','turn506view6')
source('etcd','etcd API 保證~etcd API guarantees','etcd Project','https://etcd.io/docs/v3.6/learning/api_guarantees/','turn506view7')
source('kafka','Kafka 日誌與複製設計~Kafka log and replication design','Apache Software Foundation','https://kafka.apache.org/41/design/design/','turn506view8')
source('flink','Flink 串流時間語義~Flink streaming time semantics','Apache Software Foundation','https://nightlies.apache.org/flink/flink-docs-stable/docs/concepts/time/','turn506view9')
source('k8s','Kubernetes 叢集架構~Kubernetes cluster architecture','Kubernetes Project','https://kubernetes.io/docs/concepts/architecture/','turn509view0')
source('pod','Pod 安全標準~Pod Security Standards','Kubernetes Project','https://kubernetes.io/docs/concepts/security/pod-security-standards/','turn509view1')
source('kvm','KVM API~KVM API','Linux kernel community','https://docs.kernel.org/virt/kvm/api.html','turn509view2')
source('mmu','KVM 記憶體虛擬化~KVM memory virtualization','Linux kernel community','https://docs.kernel.org/virt/kvm/x86/mmu.html','turn509view3')
source('firecracker','Firecracker 微型虛擬機~Firecracker microVMs','Firecracker maintainers','https://firecracker-microvm.github.io/','turn509view4')
source('fcdesign','Firecracker 設計~Firecracker design','Firecracker maintainers','https://github.com/firecracker-microvm/firecracker/blob/main/docs/design.md','turn509view5')
source('traffic','Istio 流量管理~Istio traffic management','Istio Project','https://istio.io/latest/docs/concepts/traffic-management/','turn509view6')
source('meshsec','Istio 安全架構~Istio security architecture','Istio Project','https://istio.io/latest/docs/concepts/security/','turn509view7')
source('traces','OpenTelemetry 追蹤~OpenTelemetry traces','OpenTelemetry Project','https://opentelemetry.io/docs/concepts/signals/traces/','turn509view8')
source('sampling','OpenTelemetry 採樣~OpenTelemetry sampling','OpenTelemetry Project','https://opentelemetry.io/docs/concepts/sampling/','turn509view9')
source('ci','GitHub Actions 安全使用~GitHub Actions secure use','GitHub','https://docs.github.com/en/actions/reference/security/secure-use','turn517view0')
source('slsa','SLSA 安全等級~SLSA security levels','OpenSSF SLSA','https://slsa.dev/spec/v1.1/levels','turn517view1')
source('repro','可重現建置定義~Reproducible-build definitions','Reproducible Builds Project','https://reproducible-builds.org/docs/definition/','turn517view2')
source('epoch','SOURCE_DATE_EPOCH~SOURCE_DATE_EPOCH','Reproducible Builds Project','https://reproducible-builds.org/docs/source-date-epoch/','turn517view3')
source('zipformat','ZIP 格式日期與時間欄位~ZIP date and time fields','PKWARE','https://pkware.cachefly.net/webdocs/casestudies/APPNOTE.TXT','turn559view0')
source('sigstore','Cosign 簽章驗證~Cosign signature verification','Sigstore Project','https://docs.sigstore.dev/cosign/verifying/verify/','turn517view4')
source('tuf','TUF 更新框架規格~TUF update-framework specification','The Update Framework','https://theupdateframework.github.io/specification/latest/','turn517view5')
source('pitr','PostgreSQL 時點復原~PostgreSQL point-in-time recovery','PostgreSQL Global Development Group','https://www.postgresql.org/docs/current/continuous-archiving.html','turn517view6')
source('availability','可用率與停機時間~Availability and downtime','Google SRE','https://sre.google/sre-book/availability-table/','turn517view7')
source('overload','服務過載處理~Service overload handling','Google SRE','https://sre.google/sre-book/handling-overload/','turn517view8')
source('ipv6','IPv6 規格 RFC 8200~IPv6 specification RFC 8200','IETF / RFC Editor','https://www.rfc-editor.org/rfc/rfc8200','turn517view9')
source('nd','IPv6 鄰居探索 RFC 4861~IPv6 neighbor discovery RFC 4861','IETF / RFC Editor','https://www.rfc-editor.org/rfc/rfc4861','turn517view10')
source('slaac','IPv6 自動配置與 DAD RFC 4862~IPv6 autoconfiguration and DAD RFC 4862','IETF / RFC Editor','https://www.rfc-editor.org/rfc/rfc4862','turn549view0')
source('virtio','Virtio 1.3 虛擬裝置規格~Virtio 1.3 virtual-device specification','OASIS','https://docs.oasis-open.org/virtio/virtio/v1.3/virtio-v1.3.html','turn549view1')
source('ovsissues','Open vSwitch 環路與設定問題~Open vSwitch loops and configuration issues','Open vSwitch Project','https://docs.openvswitch.org/en/latest/faq/issues/','turn549view2')
source('ovs','Open vSwitch 設計~Open vSwitch design','Open vSwitch Project','https://docs.openvswitch.org/en/latest/topics/design/','turn517view11')
source('ovslab','Open vSwitch 進階功能~Open vSwitch advanced features','Open vSwitch Project','https://docs.openvswitch.org/en/latest/tutorials/ovs-advanced/','turn517view12')
source('openflow','OpenFlow 1.5.1 交換器規格~OpenFlow 1.5.1 switch specification','Open Networking Foundation','https://opennetworking.org/wp-content/uploads/2014/10/openflow-switch-v1.5.1.pdf','turn517view13')
source('router','IPv4 路由器要求 RFC 1812~IPv4 router requirements RFC 1812','IETF / RFC Editor','https://www.rfc-editor.org/rfc/rfc1812','turn521view0')
source('onos','ONOS 控制器文件~ONOS controller documentation','ONOS Project','https://docs.onosproject.org/','turn521view2')
source('nvidiaaddress','NVIDIA 公開地址~NVIDIA public address','NVIDIA','https://www.nvidia.com/en-us/contact/','turn521view6')
source('amdaddress','AMD 公開辦公室~AMD public offices','AMD','https://www.amd.com/en/corporate/locations.html','turn521view7')
source('googleaddress','Google 公開辦公室~Google public offices','Google','https://about.google/company-info/locations/','turn527view1')
source('lfaddress','Linux Foundation 公開通訊地址~Linux Foundation public mailing address','Linux Foundation','https://www.linuxfoundation.org/about/contact','turn527view0')
source('stanfordaddress','史丹佛大學公開地址~Stanford University public address','Stanford University','https://www.stanford.edu/contact','turn521view5')

def add(cid,focus,stages,src,example,rows,bad,related,place='lf'):
 cid=str(cid) if cid=='cybersecurity' else 'a'+str(cid)
 units=[[x.strip().split('~',1) for x in row.split('|')]for row in rows.strip().splitlines()]
 assert len(units)==16 and all(len(u)==3 and all(len(x)==2 for x in u)for u in units),(cid,len(units))
 D[cid]={'focus':focus.split('~'),'stages':[s.split('~')for s in stages.split('|')],'src':src.split(),'example':example.split('~'),'units':units,'bad':[s.split('~')for s in bad.split('|')],'related':related,'place':place}
 assert len(D[cid]['stages'])==4 and len(D[cid]['bad'])==2

add('cybersecurity','身分、資源與復原證據~Identity, resources and recovery evidence','資產與信任邊界~Assets and trust boundaries|身分與政策執行~Identity and policy enforcement|防禦遙測與事件處理~Defensive telemetry and incidents|復原與治理驗證~Recovery and governance','zt controls',
'假設隔離樣本中有 20 件真實事件：偵測 18 件且另誤報 12 件。召回率=18/20=90%，精確率=18/(18+12)=60%；樣本並非部署成效，未包含事件基準率漂移。~Assume 20 true incidents in an isolated labeled dataset, 18 detected and 12 false alerts. Recall=18/20=90%; precision=18/(18+12)=60%. This is not deployment effectiveness and omits base-rate drift.', '''
資產身分~Asset identity|IP 可能改變，資產鍵需維持穩定。~IPs may change; asset keys must remain stable.|合併兩次假想盤點並查重。~Merge two synthetic inventories and check duplicates.
資料分級~Data classification|同一服務可包含不同保護等級資料。~One service may contain differently protected data.|標示樣本欄位的存取與保存期。~Label sample-field access and retention.
信任邊界~Trust boundaries|網段位置本身不能證明使用者權限。~Network location alone cannot establish user authority.|畫跨界資料流與授權點。~Draw boundary crossings and authorization points.
風險排序~Risk ranking|風險需同時考慮影響與暴露條件。~Risk combines impact and exposure conditions.|比較相同分數但不同損失案例。~Compare equal scores with different losses.
身分驗證~Authentication|登入驗證與資源授權是不同判斷。~Authentication and resource authorization are distinct decisions.|製作已登入但不可讀的案例。~Construct a signed-in but unreadable case.
最小權限~Least privilege|工作角色只取得必要動作與資源。~Roles receive necessary actions and resources only.|對角色矩陣加入拒絕測試。~Add denial cases to a role matrix.
政策決策~Policy decisions|政策決策點與執行點有不同失效邊界。~Decision and enforcement points fail differently.|模擬政策服務不可用的結果。~Model policy-service unavailability.
工作階段撤銷~Session revocation|權限變更後舊工作階段可能仍存活。~Old sessions may outlive permission changes.|核對撤銷時間與快取期限。~Compare revocation time and cache lifetime.
網路分段~Segmentation|允許方向與服務必須明列。~Allowed directions and services require explicit rules.|在紙上測試必要與禁止流量。~Test required and denied flows on paper.
遙測覆蓋~Telemetry coverage|缺少感測器與沒有事件不同。~Missing sensors differ from absent incidents.|將資料缺口與零值分開呈現。~Separate gaps from zero-valued events.
告警判讀~Alert interpretation|誤報率與精確率使用不同分母。~False-positive rate and precision use different denominators.|用本課混淆矩陣重算。~Recalculate from the course confusion matrix.
事件時間線~Incident timeline|時鐘偏移會顛倒跨主機事件。~Clock skew can reverse cross-host event ordering.|為假想紀錄加入時間誤差界。~Add timing-error bounds to synthetic logs.
證據保全~Evidence preservation|摘要證明位元一致，不證明內容真實。~Hashes show byte identity, not factual truth.|記錄取得時間、來源與雜湊。~Record acquisition time, source and hash.
隔離決策~Containment decisions|隔離需平衡擴散風險與服務依賴。~Containment trades spread risk against dependencies.|比較隔離資源與停整站方案。~Compare asset isolation and site shutdown.
備份復原~Backup recovery|備份成功不等於還原成功。~A successful backup need not restore successfully.|以虛構資料驗證還原及權限。~Restore fictional data and validate permissions.
控制審查~Control review|控制需可追溯至責任與證據。~Controls need accountable owners and evidence.|建立例外到期與重審清單。~Create exception expiry and review records.
''','內網登入即授權所有資源。~Internal login authorizes every resource.|高告警數必定代表高精確率。~More alerts necessarily mean higher precision.',[(310,'啟動信任與身分信任均需可信根~Boot and identity trust both need trusted roots','韌體驗證針對程式映像，網路授權針對工作階段~Firmware verification concerns images; network authorization concerns sessions'),(328,'政策與供應鏈均需驗證證據~Policy and supply chains require verified evidence','套件簽章不能替代執行時存取控制~Package signatures cannot replace runtime access control')], 'nist')

add(302,'指令相依、投機與精確提交~Instruction dependencies, speculation and precise retirement','取指與管線資源~Fetch and pipeline resources|相依與重新命名~Dependencies and renaming|分支預測與復原~Branch prediction and recovery|效能與正確性評估~Performance and correctness','o3 minor',
'假設非重疊停頓模型的基礎 CPI=1，分支佔 20%、誤預測率 5%、代價 12 cycles。ΔCPI=0.20×0.05×12=0.12，總 CPI=1.12；3 GHz 執行 10⁹ 指令約 0.373 s。忽略快取及重疊隱藏。~For a nonoverlapping-stall model, base CPI=1, branch fraction=20%, misprediction rate=5%, penalty=12 cycles. ΔCPI=0.12 and total CPI=1.12; 10⁹ instructions at 3 GHz take about 0.373 s, ignoring cache and overlap effects.', '''
ISA 與微架構~ISA and microarchitecture|相同指令集可用不同管線實作。~The same ISA permits different pipelines.|比較同一指令序列的兩種時程。~Compare two schedules for one instruction sequence.
取指頻寬~Fetch bandwidth|取指受對齊、分支及快取共同限制。~Alignment, branches and caches limit fetch.|以跨界分支追蹤取指空槽。~Trace empty fetch slots across branches.
解碼寬度~Decode width|解碼寬度不是每週期必達吞吐量。~Decode width is not guaranteed throughput.|比對可用指令與解碼槽。~Compare available instructions and decode slots.
管線深度~Pipeline depth|深管線可能提高時脈卻增加復原代價。~Deeper pipelines may raise clock and recovery cost.|固定程式比較延遲與週期數。~Compare latency and cycle counts for one program.
RAW 相依~RAW dependencies|讀取需等待先前寫入結果。~Reads wait for preceding write results.|繪製相依圖的最長路徑。~Draw the longest dependency path.
旁路網路~Forwarding network|旁路降低等待但仍受結果可用時間限制。~Forwarding remains limited by result readiness.|比較 load-use 與 ALU-use 時程。~Compare load-use and ALU-use schedules.
暫存器重新命名~Register renaming|重新命名消除名稱相依而非真資料相依。~Renaming removes name, not true data dependencies.|拆分 WAR、WAW 與 RAW。~Separate WAR, WAW and RAW cases.
重排緩衝~Reorder buffer|依序提交維持精確例外邊界。~In-order retirement preserves precise exceptions.|在假想例外點核對已提交狀態。~Check retired state at a synthetic exception.
方向預測~Direction prediction|飽和計數器保留有限分支歷史。~Saturating counters retain limited branch history.|逐次模擬 TTNT 的狀態。~Simulate counter states for TTNT.
目標預測~Target prediction|方向正確仍可能得到錯誤目標。~Correct direction may still have a wrong target.|分開記錄方向與目標命中。~Count direction and target hits separately.
歷史別名~History aliasing|不同分支可競爭同一預測表項。~Branches can compete for one predictor entry.|改變索引位數比較衝突。~Change index width and compare collisions.
投機復原~Speculation recovery|誤預測需撤銷年輕指令的狀態。~Mispredictions discard younger speculative state.|檢查重新命名檢查點復原。~Check restoration of rename checkpoints.
記憶體順序~Memory ordering|投機讀取須驗證與先前寫入相容。~Speculative loads require checks against older stores.|建立相同位址的讀寫時序。~Construct same-address load/store timing.
CPI 分解~CPI decomposition|重疊停頓不能直接重複相加。~Overlapping stalls cannot simply be added twice.|用本課非重疊假設核算。~Audit the course nonoverlap assumption.
量測基準~Measurement baseline|不同暖機與頻率使測試不可直接比較。~Warmup and frequency change comparisons.|固定輸入與暖機再比較。~Fix inputs and warmup before comparison.
架構驗收~Architecture acceptance|效能改善不能犧牲可見程式語義。~Speedups must preserve visible program semantics.|比對提交軌跡與參考結果。~Compare retirement traces with reference results.
''','重新命名也會消除真正 RAW 相依。~Renaming also removes true RAW dependencies.|寬解碼保證所有程式 CPI 同比下降。~Wider decode guarantees proportional CPI reduction.',[(303,'CPU 與一致性均需處理記憶體可見順序~CPUs and coherence both handle memory visibility','單核心投機復原不同於跨核心擁有權轉移~Single-core speculation recovery differs from intercore ownership'),(315,'投機與最佳化都需保留程式語義~Speculation and optimization preserve semantics','JIT 以軟體守衛失效復原，CPU 以硬體提交復原~JIT deoptimizes guards; CPUs recover through hardware retirement')], 'stanford')

add(303,'一致性狀態、目錄與共享粒度~Coherence states, directories and sharing granularity','共享記憶體契約~Shared-memory contracts|一致性協定與目錄~Coherence protocols and directories|爭用與互連交通~Contention and interconnect traffic|驗證與效能診斷~Verification and diagnosis','coherence false',
'假設快取行 64 B，每秒 10⁷ 次行擁有權移轉，僅計每次 64 B 資料，交通下界=640 MB/s（十進位）。未計請求、確認、重試與互連標頭；填補不是免費。~Assume 64 B cache lines and 10⁷ ownership transfers/s. Counting 64 B payload per transfer gives a 640 MB/s decimal traffic lower bound; requests, acknowledgments, retries and headers are excluded.', '''
快取一致性與記憶體順序~Coherence and consistency|單一位址一致性不等於全域記憶體順序。~Single-address coherence is not global memory ordering.|分類單位址與雙位址測試。~Classify one- and two-address tests.
快取行粒度~Cache-line granularity|擁有權通常以行而非變數為單位。~Ownership is usually per line, not variable.|映射兩變數到快取行。~Map two variables to cache lines.
讀取共享~Shared reads|多讀者可保留乾淨共享副本。~Readers can hold clean shared copies.|畫兩核心讀取後狀態。~Draw states after two-core reads.
寫入擁有權~Write ownership|修改通常需排除其他有效副本。~Writes usually invalidate other valid copies.|追蹤一次讀後寫入。~Trace a read followed by a write.
MSI 狀態~MSI states|M、S、I 具有不同資料與擁有權語義。~M, S and I encode different ownership semantics.|列出讀寫觸發的狀態轉移。~List read/write-triggered transitions.
髒資料回寫~Dirty writeback|髒副本需將更新傳到下一層。~Dirty copies propagate updates to the next level.|檢查替換前後資料版本。~Check versions before and after eviction.
目錄追蹤~Directory tracking|目錄追蹤共享者，避免總廣播。~Directories track sharers to reduce broadcasts.|比較全位元圖與有限指標。~Compare full bitmaps and limited pointers.
暫態狀態~Transient states|等待訊息時不能當作穩態完成。~Pending messages create transient, unfinished states.|加入延遲確認的事件序列。~Introduce delayed acknowledgments in a trace.
假共享~False sharing|獨立變數共行可產生擁有權震盪。~Independent same-line variables can bounce ownership.|比較同列與分列計數器。~Compare same-line and separated counters.
真共享~True sharing|填補不能消除共同資料的寫入競爭。~Padding cannot remove genuine shared-write contention.|區分共享鎖與分離計數器。~Distinguish shared locks from separate counters.
原子操作~Atomic operations|原子更新需符合指定的記憶體順序。~Atomic updates obey their specified memory ordering.|核對 relaxed 與 acquire/release 契約。~Compare relaxed and acquire/release contracts.
NUMA 局部性~NUMA locality|一致性不代表遠端存取無延遲。~Coherence does not make remote access free.|比較本地與遠端模型延遲。~Compare modeled local and remote latency.
協定不變量~Protocol invariants|單寫者與最新資料是不同不變量。~Single-writer and latest-data are separate invariants.|對每個模擬狀態檢查兩者。~Check both invariants in each modeled state.
競態軌跡~Race traces|訊息不同到達順序可改變中間狀態。~Arrival ordering changes intermediate states.|枚舉兩請求交錯順序。~Enumerate two-request interleavings.
交通成本~Traffic costs|資料交通僅是協定總交通的下界。~Payload traffic only bounds protocol traffic below.|以本課算例加上假想標頭。~Extend the course example with assumed headers.
擴展性~Scalability|核心數增加可能先耗盡互連或目錄資源。~More cores may exhaust links or directories first.|分別掃描核心數與共享比例。~Sweep core count and sharing fraction separately.
''','一致性快取可取代所有同步原語。~Coherent caches replace all synchronization primitives.|填補變數會消除所有真共享。~Padding eliminates all true sharing.',[(302,'共用記憶體順序及停頓分析~Shared memory-order and stall analysis','跨核心協定需管理遠端訊息，CPU 管線主要管理本地指令~Coherence manages remote messages; pipelines manage local instructions'),(307,'一致性訊息經互連路由~Coherence messages traverse an interconnect','協定正確性與路由無死鎖是不同證明~Protocol correctness and routing deadlock freedom require different proofs')], 'stanford')

add(304,'SIMT 執行、資料重用與資源佔用~SIMT execution, reuse and resource occupancy','執行與索引~Execution and indexing|記憶體階層~Memory hierarchy|並行與同步~Concurrency and synchronization|效能與數值驗證~Performance and numerical validation','cuda cudaadvanced',
'假設向量加法每元素兩次 4 B 讀取、一次 4 B 寫入，共 12 B 與 1 FLOP。持續頻寬 600 GB/s 給出 50 G元素/s、50 GFLOP/s 的理想頻寬上界，未計快取、傳輸及啟動。~Assume vector addition reads two 4 B operands and writes one 4 B result: 12 B and 1 FLOP per element. Sustained 600 GB/s yields an ideal bandwidth bound of 50 Gelements/s and 50 GFLOP/s, excluding caches, transfers and launches.', '''
執行階層~Execution hierarchy|執行緒組成區塊，區塊映射到 SM。~Threads form blocks mapped to SMs.|畫 grid、block 與 SM 的對應。~Map grid, blocks and SMs.
索引覆蓋~Index coverage|索引需覆蓋資料且避免越界。~Indices must cover data without overrun.|用非整除長度檢查邊界。~Check a nondivisible input length.
Warp 分歧~Warp divergence|不同路徑可降低同時有效通道。~Divergent paths reduce active lanes.|比較相鄰與交錯條件。~Compare adjacent and alternating predicates.
區塊獨立~Block independence|一般區塊不能假設其他區塊已執行。~Ordinary blocks cannot assume others have run.|打亂區塊順序核對結果。~Shuffle block order and check results.
合併存取~Coalescing|位址分佈影響記憶體交易數。~Address distribution changes memory transaction counts.|比較連續與跨步位址圖。~Compare contiguous and strided address maps.
共享記憶體~Shared memory|區塊共享資料需配合正確同步。~Block-shared data requires synchronization.|追蹤 producer/consumer 的可見性。~Trace producer/consumer visibility.
Bank 衝突~Bank conflicts|不同位址可能映射同一 bank。~Different addresses can map to one bank.|比較轉置前後的 bank 索引。~Compare bank indices before and after transpose.
暫存器壓力~Register pressure|暫存器使用會限制駐留或引起溢出。~Register use can limit residency or cause spills.|比較每執行緒暫存器假想配置。~Compare assumed per-thread register allocations.
佔用率~Occupancy|高佔用率未必等於高有效吞吐。~High occupancy need not maximize useful throughput.|同時檢查瓶頸與有效工作量。~Inspect bottlenecks and useful work together.
屏障一致~Barrier convergence|需要參與的執行緒須遵守屏障契約。~Required threads must obey barrier participation.|核對分支內屏障的路徑。~Audit barrier paths inside branches.
原子歸約~Atomic reduction|原子正確性與競爭成本不同。~Atomic correctness differs from contention cost.|比較樹狀與集中更新。~Compare tree and centralized updates.
串流相依~Stream dependencies|重疊需避免尚未完成資料被覆寫。~Overlap must not overwrite unfinished data.|畫複製、運算與事件相依。~Draw copy, compute and event dependencies.
算術強度~Arithmetic intensity|每位元組工作量限制可達運算率。~Work per byte bounds compute throughput.|重算本課向量頻寬上界。~Recalculate the vector bandwidth bound.
時間量測~Timing measurement|非同步呼叫時間不等於核心時間。~Async call time is not kernel runtime.|分開主機提交與完成時間。~Separate host submission and completion time.
數值誤差~Numerical error|浮點歸約順序會改變捨入。~Reduction order changes rounding.|比較絕對與相對誤差。~Compare absolute and relative error.
CPU 對照~CPU reference|相同輸入與語義才能比較兩架構。~Architectures need matching inputs and semantics.|核對結果、傳輸與完整耗時。~Check results, transfers and total time.
''','佔用率最高的設定必定最快。~The highest occupancy configuration is always fastest.|原子操作會消除全部資料相依。~Atomics remove every data dependency.',[(305,'矩陣分塊與頻寬分析相通~Matrix tiling and bandwidth analysis transfer','SIMT 核心較通用，專用陣列受形狀與資料型別限制~SIMT is general; dedicated arrays constrain shapes and types'),(306,'可重用資料降低外部交通~Reuse reduces external traffic','GPU 排程執行緒，FPGA 空間配置硬體管線~GPUs schedule threads; FPGAs spatially instantiate pipelines')], 'nvidia')

add(305,'脈動陣列、混合精度與編譯映射~Systolic arrays, mixed precision and compiler mapping','矩陣工作負載~Matrix workloads|陣列資料流~Array dataflow|精度與記憶體~Precision and memory|端到端效能~End-to-end performance','tpu bf16',
'假想 128×128 MAC 陣列每週期每單元一 MAC、1 GHz，且 MAC 計兩 FLOP：峰值=128²×2×10⁹=32.768 TFLOP/s。若有效利用率 60%，為 19.661 TFLOP/s；不是任一真實 TPU 的產品規格。~A hypothetical 128×128 MAC array at one MAC/cell/cycle and 1 GHz gives 32.768 TFLOP/s counting two FLOPs/MAC; assumed 60% utilization gives 19.661 TFLOP/s. This is not a real TPU specification.', '''
張量維度~Tensor dimensions|矩陣相乘的內維度必須相容。~Matrix inner dimensions must agree.|核對 M×K 與 K×N 形狀。~Check M×K and K×N shapes.
MAC 計數~MAC counting|一乘一加常按兩 FLOP 計數。~A multiply-add commonly counts as two FLOPs.|分開 MAC/s 與 FLOP/s。~Separate MAC/s from FLOP/s.
陣列填充~Array filling|脈動資料抵達不同位置有延遲。~Systolic data arrival has position-dependent latency.|畫 4×4 陣列填充時間。~Draw fill timing for a 4×4 array.
資料平鋪~Data tiling|維度不整除會產生邊緣空槽。~Nondivisible dimensions create edge waste.|比較整齊與零補齊矩陣。~Compare aligned and padded matrices.
權重駐留~Weight stationary|權重駐留減少載入但改變累加路徑。~Stationary weights reduce loads but alter accumulation.|繪製一次 tile 的資料移動。~Draw data movement for one tile.
輸出駐留~Output stationary|局部保留部分和可降低外部寫回。~Local partial sums reduce external writes.|核對部分和的生命週期。~Audit partial-sum lifetime.
雙緩衝~Double buffering|載入與運算重疊需要足夠緩衝。~Load/compute overlap needs sufficient buffering.|比較串列與重疊時程。~Compare serial and overlapping schedules.
集體通訊~Collective communication|分散工作需支付資料交換成本。~Distributed work pays exchange costs.|比較本地運算與交換時間。~Compare local compute and exchange time.
bfloat16 格式~bfloat16 format|指數範圍與有效數位是不同特性。~Exponent range differs from significant precision.|比較 BF16 與 FP16 的位元配置。~Compare BF16 and FP16 bit allocation.
累加精度~Accumulation precision|低精度輸入可配較高精度累加。~Low-precision inputs may use wider accumulation.|追蹤長點積的捨入誤差。~Trace rounding in a long dot product.
量化比例~Quantization scales|飽和與小值消失取決於比例因子。~Scale controls saturation and lost small values.|以不同 scale 量化同一分佈。~Quantize one distribution with two scales.
HBM 頻寬~HBM bandwidth|峰值陣列算力不保證供料足夠。~Peak array compute does not ensure feeding bandwidth.|列出 tile 的讀寫位元組。~Count tile read/write bytes.
編譯映射~Compiler mapping|融合可減少交通但增加局部資源。~Fusion saves traffic but consumes local resources.|比較融合前後暫存量。~Compare temporary storage before and after fusion.
利用率~Utilization|有效利用率包含形狀及等待損失。~Useful utilization includes shape and wait losses.|重算假想陣列的有效峰值。~Recalculate hypothetical effective peak.
輸入管線~Input pipeline|預處理可能使加速器等待資料。~Preprocessing can starve an accelerator.|分離讀取、轉換與運算耗時。~Separate read, transform and compute times.
精度驗收~Accuracy acceptance|速度提升需同時核對任務品質。~Speedups require task-quality checks.|比較基準誤差與吞吐變化。~Compare reference error and throughput changes.
''','BF16 與 FP16 有相同指數和尾數配置。~BF16 and FP16 have identical exponent and mantissa layouts.|峰值 FLOP/s 可直接當作端到端訓練吞吐。~Peak FLOP/s equals end-to-end training throughput.',[(304,'分塊與記憶體重用可沿用~Tiling and memory reuse transfer','GPU 有通用執行緒模型，脈動陣列特化矩陣流~GPUs expose general threads; systolic arrays specialize matrix flows'),(306,'空間資料流與緩衝設計相近~Spatial flows and buffering are related','FPGA 管線可重配置，TPU 執行硬體支援運算~FPGA pipelines are reconfigurable; TPUs execute supported operations')], 'google')

add(306,'HLS、串流管線與有限資源映射~HLS, streaming pipelines and finite resource mapping','C 模型與硬體契約~C models and hardware contracts|管線與記憶體埠~Pipelines and memory ports|資料流與回壓~Dataflow and backpressure|共模擬與時序驗證~Cosimulation and timing','hls dataflow',
'假設時脈 200 MHz、起始間隔 II=2 cycles，穩態每週期組輸出一筆 4 B，吞吐=100 M筆/s=400 MB/s。延遲 20 cycles=100 ns；短批次另計填充及排空。~Assume 200 MHz, initiation interval II=2 cycles and one 4 B result per initiation. Steady throughput=100 Mitems/s=400 MB/s; 20-cycle latency=100 ns. Short batches also pay fill and drain.', '''
功能契約~Functional contract|C 結果正確不代表硬體時序合格。~Correct C output does not establish hardware timing.|建立輸入、輸出及完成定義。~Define input, output and completion.
位寬設計~Bit-width design|縮小位寬改變溢位及資源用量。~Narrowing changes overflow and resource use.|核對最大值與有號範圍。~Check maxima and signed ranges.
固定點~Fixed point|整數與小數位分配不同誤差風險。~Integer and fractional allocation change error risks.|比較兩種量化配置。~Compare two quantization layouts.
介面握手~Interface handshake|有效與就緒共同決定資料轉移。~Valid and ready jointly determine transfers.|枚舉暫停與連續傳輸時序。~Enumerate stalls and continuous transfers.
起始間隔~Initiation interval|II 是新工作間距，不是總延遲。~II is launch spacing, not total latency.|以本課數字計吞吐與延遲。~Calculate course throughput and latency.
循環相依~Loop dependencies|跨迭代相依可限制最小 II。~Loop-carried dependencies constrain minimum II.|畫累加器的相依距離。~Draw accumulator dependency distance.
展開迴圈~Loop unrolling|展開複製運算資源但仍受供料限制。~Unrolling duplicates compute but remains feed-limited.|比較倍增運算器與埠數。~Compare compute duplication and port count.
陣列分割~Array partitioning|分割增加平行埠但提高資源成本。~Partitioning raises parallel ports and cost.|檢查連續與交錯索引衝突。~Check contiguous and interleaved index conflicts.
任務資料流~Task dataflow|並行任務用通道傳遞中間結果。~Concurrent tasks exchange intermediate results through channels.|拆分讀取、計算與輸出。~Separate read, compute and write tasks.
FIFO 深度~FIFO depth|深度需吸收突發及相位差。~Depth absorbs bursts and phase mismatch.|追蹤每週期佔用峰值。~Trace peak cycle-by-cycle occupancy.
回壓傳播~Backpressure propagation|下游停止可向上游傳遞等待。~Downstream stalls can propagate upstream.|暫停假想 sink 並追蹤。~Pause a modeled sink and trace.
死鎖辨識~Deadlock diagnosis|循環等待可能阻止所有任務前進。~Circular waits can halt all tasks.|區分慢吞吐與零前進。~Distinguish slow throughput from no progress.
C/RTL 共模擬~C/RTL cosimulation|共模擬驗證指定輸入而非所有情境。~Cosimulation validates tested inputs, not all cases.|加入邊界長度與回壓。~Add boundary lengths and backpressure.
資源報告~Resource reports|DSP、BRAM 與暫存器限制不同。~DSP, BRAM and registers impose different limits.|建立三項獨立資源預算。~Build three separate resource budgets.
時序裕量~Timing margin|合成估計不等於佈局後時序。~Synthesis estimates differ from placed timing.|比較目標與實際 critical path。~Compare target and realized critical paths.
端到端比較~End-to-end comparison|DMA 與主機整理可能主導耗時。~DMA and host preparation can dominate runtime.|把資料傳輸納入總帳。~Include transfers in the total budget.
''','II 與每筆資料延遲必定相等。~II always equals per-item latency.|迴圈展開後記憶體埠數不再重要。~Memory ports cease to matter after loop unrolling.',[(304,'同樣需要平行供料與數值驗收~Both need parallel feeding and numerical validation','FPGA 空間硬體與 GPU 動態執行緒排程不同~Spatial FPGA hardware differs from GPU thread scheduling'),(305,'陣列與管線均利用資料重用~Arrays and pipelines exploit data reuse','HLS 可以選位寬及通道，張量加速器受既定格式限制~HLS selects widths/channels; tensor accelerators constrain formats')], 'amd')

add(307,'Flit、虛擬通道與可證明路由~Flits, virtual channels and verifiable routing','拓撲與封包化~Topology and packetization|路由與仲裁~Routing and arbitration|流量與死鎖~Traffic and deadlock|延遲與擴展評估~Latency and scaling','noc garnet',
'假設 128-bit flit、1 GHz、每週期一 flit，單向鏈路原始速率=16 GB/s。64 B 封包不計標頭需四 flit；四跳每跳 2 cycles 的空載路由延遲 8 ns，序列化另計。~A 128-bit link at 1 GHz with one flit/cycle has 16 GB/s raw one-way rate. A 64 B packet needs four payload flits. Four hops at 2 cycles/hop give 8 ns unloaded routing latency; serialization is additional.', '''
拓撲座標~Topology coordinates|網格連線決定跳數與切割頻寬。~Mesh links determine hops and bisection bandwidth.|繪製 4×4 網格並計最遠跳數。~Draw a 4×4 mesh and count farthest hops.
封包與 flit~Packets and flits|封包分成傳輸與緩衝的 flit。~Packets split into transport and buffering flits.|核對本課 64 B 的 flit 數。~Check flits for the course 64 B packet.
路由器管線~Router pipeline|路由、配置及交叉開關有不同延遲。~Routing, allocation and switching have distinct delays.|分解每跳週期預算。~Break down per-hop cycle budgets.
端點介面~Endpoint interface|端點需組包、拆包並保留語義。~Endpoints packetize and reassemble semantic messages.|核對封包與原始請求對應。~Match packets to original requests.
XY 路由~XY routing|維度順序限制允許的轉彎。~Dimension ordering restricts allowed turns.|列出來源到目的地路徑。~List source-to-destination paths.
自適應路由~Adaptive routing|選路可避壅塞但須保留無死鎖條件。~Adaptation avoids congestion but needs deadlock conditions.|比較可選轉彎及逃脫路徑。~Compare turns and escape paths.
交換仲裁~Switch arbitration|公平性與最大吞吐是不同目標。~Fairness and maximum throughput differ.|比較輪詢與固定優先權。~Compare round-robin and fixed priority.
Credit 控制~Credit control|可用 credit 代表下游緩衝容量。~Credits represent downstream buffer capacity.|核對發送與歸還的守恆。~Check send/return credit conservation.
虛擬通道~Virtual channels|共用實體鏈路可分離等待佇列。~Virtual channels separate queues on shared links.|比較阻塞前後的隊列。~Compare queues with and without blockage.
隊頭阻塞~Head-of-line blocking|首包等待可能阻止後方可行封包。~A blocked head can stall feasible followers.|構造不同目的地的佇列。~Construct queues with different destinations.
通道相依~Channel dependencies|循環相依是死鎖分析的重要結構。~Cycles matter in channel-dependency analysis.|畫通道相依圖檢查循環。~Inspect cycles in a dependency graph.
協定網路~Protocol networks|請求與回應可能需要分離資源。~Requests and responses may need separate resources.|比較路由與協定循環。~Compare routing and protocol cycles.
注入率~Injection rate|高於瓶頸服務率會積累等待。~Injection above bottleneck service builds queues.|掃描注入率及平均延遲。~Sweep injection and mean latency.
熱點流量~Hotspot traffic|平均均勻流量不能代表熱點工作量。~Uniform averages miss hotspot workloads.|比較均勻與單點目的地。~Compare uniform and single-destination traffic.
延遲分解~Latency breakdown|跳數延遲、序列化與排隊需分列。~Hop, serialization and queueing delays are separate.|擴充本課空載算例。~Extend the unloaded course example.
正確性驗收~Correctness acceptance|無丟包不代表無重複或順序正確。~No loss does not imply no duplication or correct order.|檢查序號、計數與交付順序。~Check sequences, counts and delivery order.
''','增加虛擬通道即自動證明無死鎖。~More virtual channels automatically prove deadlock freedom.|鏈路峰值可直接當作全部端點吞吐。~Peak link rate equals total endpoint throughput.',[(303,'一致性封包需要互連提供交付~Coherence packets rely on interconnect delivery','快取狀態不變量與通道相依圖不同~Cache-state invariants differ from channel graphs'),(331,'共享仲裁與壅塞分析~Arbitration and congestion analysis transfer','NoC flit/credit 機制不同於乙太框架~NoC flit/credit mechanisms differ from Ethernet frames')], 'stanford')

add(308,'DRAM 時序、排程與可辨識更正~DRAM timing, scheduling and diagnosable correction','地址與 DRAM 組織~Addressing and DRAM organization|排程與時序限制~Scheduling and timing constraints|ECC 與巡檢~ECC and scrubbing|可靠度與量測~Reliability and measurement','edac scrub',
'假設單通道 64-bit 資料匯流排、6400 MT/s：資料峰值=8 B×6.4×10⁹/s=51.2 GB/s，未含 refresh 與排程。假想 64-bit 資料加 8-bit ECC，儲存額外=8/64=12.5%；不是所有 DIMM 編碼。~A hypothetical 64-bit channel at 6400 MT/s has 51.2 GB/s payload peak, excluding refresh and scheduling. A hypothetical 64+8 ECC word has 12.5% storage overhead; not all DIMMs use this code.', '''
地址解碼~Address decoding|位址映射至通道、rank、bank 與列。~Addresses map to channel, rank, bank and row.|將假想位元欄位填入地址。~Fill assumed address bit fields.
列緩衝~Row buffer|列命中與列衝突耗時不同。~Row hits and conflicts have different costs.|比較同列與跨列請求。~Compare same-row and different-row requests.
Burst 傳輸~Burst transfers|資料傳輸率不同於命令頻率。~Transfer rate differs from command frequency.|核對 MT/s 與 MHz 的單位。~Check MT/s and MHz units.
容量組織~Capacity organization|rank、裝置寬度與容量不能混為一談。~Ranks, device widths and capacities differ.|從假想裝置數重算容量。~Recalculate capacity from assumed devices.
啟動與預充~Activate and precharge|開列與關列需遵守時序間隔。~Opening and closing rows obey timing intervals.|畫 ACT、READ、PRE 的時程。~Draw ACT, READ and PRE timing.
Bank 平行~Bank parallelism|不同 bank 可重疊部分命令工作。~Banks can overlap some command work.|比較單 bank 與交錯存取。~Compare one-bank and interleaved accesses.
Refresh 干擾~Refresh interference|刷新佔用資源並延遲正常請求。~Refresh consumes resources and delays requests.|把刷新窗口納入延遲分佈。~Include refresh windows in latency distributions.
排程公平~Scheduling fairness|列命中優先可能使其他來源久候。~Row-hit priority may starve other sources.|比較命中率與最長等待。~Compare hit rates and maximum waiting.
ECC 距離~ECC distance|碼距決定可偵測與可更正能力。~Code distance determines detection and correction.|對小碼字列出翻位結果。~Enumerate flips in a small codeword.
SECDED 邊界~SECDED limits|單錯更正雙錯偵測不等於任意錯誤復原。~SECDED does not recover arbitrary errors.|比較一位、兩位與多位案例。~Compare one-, two- and multibit cases.
Syndrome~Syndrome|症候值需配合碼的位元映射解讀。~Syndromes depend on code bit mapping.|檢查位置重排後的判讀。~Check decoding after position permutation.
巡檢頻率~Scrub frequency|巡檢間隔影響累積未修正錯誤窗口。~Scrub intervals affect accumulated-error windows.|比較兩種假想巡檢週期。~Compare two assumed scrub periods.
更正紀錄~Corrected-error records|更正事件需保留位置與時間。~Corrected events need location and timestamps.|分開總數與每 DIMM 趨勢。~Separate totals from per-DIMM trends.
不可更正~Uncorrectable errors|錯誤隔離與資料恢復是不同責任。~Error containment differs from data recovery.|核對退役頁面與備份角色。~Compare page retirement and backup roles.
頻寬驗證~Bandwidth validation|峰值匯流排速率僅是上界。~Peak bus bandwidth is an upper bound.|核算本課峰值與利用率。~Audit course peak and utilization.
證據範圍~Evidence scope|無錯誤紀錄可能代表未啟用報告。~No error logs may mean reporting is disabled.|檢查監測覆蓋而非只看零值。~Check monitoring coverage, not zeros alone.
''','ECC 可更正任何位元數的錯誤。~ECC corrects arbitrarily many bit errors.|6400 MT/s 代表每秒 6400 百萬完整記憶體命令。~6400 MT/s means 6400 million full memory commands per second.',[(303,'行粒度與資料一致性需共同考慮~Line granularity and data consistency interact','ECC 處理位元錯誤，一致性處理合法更新的可見性~ECC handles bit errors; coherence handles legal-update visibility'),(329,'更正與備份提供不同復原層~Correction and backups offer different recovery layers','ECC 不會還原誤刪或已合法寫入的壞資料~ECC does not restore deletion or validly written bad data')], 'lf')

add(309,'即時排程、同步與可界定延遲~Real-time scheduling, synchronization and bounded latency','時間契約與任務~Timing contracts and tasks|同步與中斷~Synchronization and interrupts|資源與資料交換~Resources and exchange|最差情境驗證~Worst-case validation','schedule mutex',
'假設單核心週期任務 C/T 分別 1/5 ms、2/10 ms、2/20 ms，U=0.5。三任務 RM 充分界=3(2^(1/3)−1)≈0.7798，因此在獨立、可搶佔、deadline=period 等前提可通過此充分測試；不是 Zephyr 保證。~For one core with periodic C/T=1/5, 2/10 and 2/20 ms, U=0.5. The three-task RM sufficient bound is 0.7798, under independent, preemptible tasks with deadlines equal to periods; not a Zephyr guarantee.', '''
Deadline 契約~Deadline contracts|硬 deadline 與平均延遲要求不同。~Hard deadlines differ from average latency goals.|為假想控制迴路標示到期點。~Mark deadlines for a modeled control loop.
週期與抖動~Periods and jitter|到達抖動會改變最差等待。~Arrival jitter changes worst-case waiting.|比較固定與抖動到達序列。~Compare periodic and jittered arrivals.
WCET~WCET|最慢量測未必是最差執行時間上界。~Slowest observed time need not bound WCET.|列出未測過的執行路徑。~List untested execution paths.
優先權排序~Priority ordering|較高優先權就緒任務先獲排程。~Higher-priority ready tasks are selected first.|繪製三任務時間線。~Draw a three-task timeline.
搶佔成本~Preemption cost|切換、快取與中斷增加額外時間。~Switching, cache and interrupts add overhead.|在時間線加入假想切換成本。~Add assumed switching costs to timing.
優先權反轉~Priority inversion|低優先權持鎖可阻擋高優先權任務。~Low-priority lock holders can block high priority.|畫三任務持鎖情境。~Draw a three-task lock scenario.
優先權繼承~Priority inheritance|繼承緩解特定反轉，不消除全部阻塞。~Inheritance mitigates inversion, not all blocking.|比較有無繼承的等待界。~Compare waiting bounds with inheritance.
中斷下半部~Deferred interrupts|延後工作降低 ISR 長度但增加排隊。~Deferred work shortens ISR but adds queues.|分開 IRQ 回應與工作完成。~Separate IRQ response and work completion.
訊息佇列~Message queues|有限佇列需明訂滿載策略。~Bounded queues require full-capacity policies.|比較阻塞、丟棄與回壓。~Compare blocking, dropping and backpressure.
環形緩衝~Ring buffers|讀寫索引需要一致的擁有權。~Read/write indices need consistent ownership.|檢查繞回與空滿辨識。~Check wraparound and empty/full distinction.
記憶體配置~Memory allocation|動態配置時間與碎片化可能不確定。~Dynamic allocation adds timing and fragmentation uncertainty.|比較固定池與一般 heap。~Compare fixed pools and general heaps.
計時器精度~Timer resolution|時鐘量化誤差需列入 deadline 裕量。~Clock quantization belongs in deadline margins.|比較 tick 與高解析計時。~Compare tick and high-resolution timing.
利用率測試~Utilization tests|RM 充分界失敗不等於不可排程。~Failing the RM sufficient bound is not impossibility.|以本課負載計算界限。~Calculate the course utilization bound.
回應時間~Response time|高優先權幹擾與阻塞需加入分析。~Higher-priority interference and blocking enter analysis.|逐次估算假想回應時間。~Iterate a modeled response-time estimate.
過載處理~Overload handling|超載需保護關鍵任務而非無界積壓。~Overload should protect critical tasks, not queue forever.|定義捨棄非關鍵工作政策。~Define noncritical work-shedding policy.
驗收軌跡~Acceptance traces|滿足平均值不證明全部 deadline。~Meeting averages does not prove every deadline.|核對每筆任務的完成時間。~Check completion of every task.
''','優先權繼承能消除所有阻塞時間。~Priority inheritance removes every blocking interval.|平均延遲合格即證明硬即時合格。~Passing mean latency proves hard real-time compliance.',[(312,'排程、IPC 與隔離均影響延遲~Scheduling, IPC and isolation affect latency','微核心保護域分離不保證即時期限~Microkernel protection domains do not guarantee deadlines'),(308,'兩者都需評估最差等待~Both assess worst-case waiting','DRAM 刷新可影響任務 WCET 但不是任務優先權~DRAM refresh affects WCET but is not task priority')], 'lf')

add(310,'可信根、映像驗證與可復原更新~Roots of trust, image verification and recoverable updates','可信根與啟動圖~Root of trust and boot graph|映像與簽章~Images and signatures|更新與防回退~Updates and rollback resistance|復原與證據~Recovery and evidence','firmware verified',
'假設驗證 32 MiB 映像，雜湊持續速率 400 MiB/s，僅雜湊下界=80 ms；另假定兩次簽章驗證各 5 ms，總 90 ms，未含讀取與初始化。不是任何裝置實測。~Assume a 32 MiB image hashed at sustained 400 MiB/s: hashing lower bound=80 ms. Two assumed 5 ms signature checks give 90 ms total, excluding reads and initialization; not a device measurement.', '''
信任起點~Trust anchor|驗證公鑰本身需受可信邊界保護。~Verification keys themselves need protection.|標出可寫與唯讀儲存。~Mark writable and read-only storage.
啟動序列~Boot sequence|每一載入階段可形成新的驗證邊界。~Each loading stage creates a verification boundary.|列出 ROM 到應用的關係。~List ROM-to-application relationships.
測量與驗證~Measurement and verification|測量記錄摘要不等於阻止執行。~Measurements record hashes but need not block execution.|比較紀錄與拒絕兩種策略。~Compare recording and rejection policies.
信任擴展~Trust extension|下一階段必須受前階段授權。~A stage must be authorized by its predecessor.|核對每個未受驗證的分支。~Audit every unverified branch.
摘要完整性~Digest integrity|摘要比對可偵測位元修改但需可信期望值。~Digest checks need trusted expected values.|用虛構映像更改一位元。~Flip one bit in a fictional image.
數位簽章~Digital signatures|有效簽章只在可信金鑰政策內授權。~Signatures authorize only under trusted key policy.|比較正確與錯誤測試金鑰。~Compare correct and wrong test keys.
映像範圍~Image coverage|未納入簽章的設定仍可能改變行為。~Unsigned configuration can still alter behavior.|標出映像與設定的覆蓋。~Mark image and configuration coverage.
版本繫結~Version binding|簽章需繫結適用平臺與版本。~Signatures should bind platform and version.|以錯平臺假想 manifest 判讀。~Interpret a wrong-platform manifest.
防回退~Rollback resistance|舊的合法簽章不能自行證明新版本。~Old valid signatures do not establish freshness.|比較簽章與單調版本政策。~Compare signatures and monotonic-version policy.
金鑰輪替~Key rotation|新金鑰須透過既有可信政策授權。~New keys need authorization by trusted policy.|繪製正常與撤銷輪替。~Draw normal and revoked rotations.
A/B 更新~A/B updates|備援映像需區分已寫入與已確認啟動。~Backup images need written/boot-confirmed states.|枚舉更新中斷位置。~Enumerate interrupted-update points.
斷電一致~Power-loss consistency|中途斷電不能留下半套有效狀態。~Interrupted power must not leave half-valid state.|在紙上檢查原子狀態轉換。~Audit atomic state transitions on paper.
復原可信~Recovery trust|復原路徑不能繞過原有授權。~Recovery must not bypass authorization.|比較恢復模式與主模式政策。~Compare recovery and main-mode policies.
金鑰保護~Key protection|簽章私鑰不應位於公開教材。~Signing private keys do not belong in public courseware.|區分測試金鑰與正式保管。~Separate test keys and production custody.
啟動預算~Boot budget|雜湊、讀取與驗簽成本需分列。~Hashing, reads and signature costs are separate.|重算本課 90 ms 假想案例。~Recalculate the assumed 90 ms case.
證據交接~Evidence handoff|驗證紀錄需對應實際執行映像。~Verification evidence must match the executed image.|比對映像摘要與啟動版本。~Match image digest and boot version.
''','所有簽過章的舊映像皆可安全回退。~Every signed old image is safe to roll back.|Measured boot 必定拒絕不可信映像。~Measured boot necessarily rejects untrusted images.',[(328,'簽章信任政策及新鮮度檢查相通~Signature policy and freshness checks transfer','韌體啟動涵蓋硬體可信根，套件驗證涵蓋配送及消費者政策~Boot uses hardware roots; packages use distribution and consumer policy'),(311,'核心啟動需符合平臺契約~Kernel boot obeys platform contracts','安全啟動授權映像，移植要驗證裝置與 ABI~Secure boot authorizes images; porting validates devices and ABI')], 'nist')

add(311,'啟動 ABI、平臺描述與核心基準~Boot ABI, platform description and kernel baselines','移植目標與 ABI~Port target and ABI|記憶體與平臺描述~Memory and platform descriptions|中斷與裝置啟用~Interrupts and devices|回歸與上游維護~Regression and upstream maintenance','riscvboot dt',
'假設 RV64 教學配置要求 2 MiB 對齊，實體位置 0x80200000 除以 0x200000 無餘數；0x80300000 餘 1 MiB，需調整。16 MiB 保留區佔 512 MiB RAM 的 3.125%；依選定啟動方式重查規格。~Under an assumed RV64 configuration with 2 MiB alignment, 0x80200000 is aligned; 0x80300000 leaves 1 MiB remainder. A 16 MiB reservation occupies 3.125% of 512 MiB RAM; recheck the chosen boot specification.', '''
目標架構~Target architecture|CPU ISA、ABI 與浮點配置需一致。~ISA, ABI and floating-point configuration must agree.|核對編譯目標與核心設定。~Check compiler target and kernel configuration.
交叉工具鏈~Cross toolchain|主機程式與目標程式不能混用。~Host and target binaries are not interchangeable.|檢查二進位架構 metadata。~Inspect binary architecture metadata.
核心配置~Kernel configuration|功能選項會改變依賴與初始化。~Configuration changes dependencies and initialization.|記錄可追溯配置差異。~Record traceable configuration differences.
啟動 ABI~Boot ABI|入口暫存器與 MMU 狀態由契約定義。~Contracts define entry registers and MMU state.|核對假想 bootloader 交接表。~Audit a modeled bootloader handoff.
載入對齊~Load alignment|架構及啟動方式可能規定對齊。~Architecture and boot method may require alignment.|重算本課位址的餘數。~Recalculate course address remainders.
保留記憶體~Reserved memory|韌體佔用區不能誤作一般可用 RAM。~Firmware regions must not become ordinary RAM.|畫實體區域與保留範圍。~Draw physical and reserved regions.
裝置樹節點~Devicetree nodes|裝置樹描述硬體而非驅動實作。~Devicetrees describe hardware, not driver implementations.|配對 compatible 與公開 binding。~Match compatible strings to bindings.
早期映射~Early mappings|暫時與最終映射有不同可用資源。~Early and final mappings permit different resources.|檢查配置與存取的時序。~Check allocation and access timing.
時鐘來源~Clock sources|計時來源會影響排程與延遲量測。~Time sources affect scheduling and latency measures.|核對假想頻率與換算。~Check assumed frequency conversions.
中斷路徑~Interrupt paths|中斷控制器、編號與驅動需相容。~Controllers, interrupt IDs and drivers must agree.|追蹤一個模擬中斷。~Trace one simulated interrupt.
主控臺~Console|早期輸出與完整驅動輸出路徑不同。~Early and full console paths differ.|定位最後可見啟動階段。~Locate the last visible boot phase.
SMP 啟動~SMP startup|其他核心進入時機需遵守初始化順序。~Secondary cores must obey initialization ordering.|比較單核心與多核心軌跡。~Compare single- and multicore traces.
驅動探測~Driver probing|資源未準備可能延後探測。~Missing resources can defer probing.|區分錯 binding 與依賴未就緒。~Distinguish bad bindings and unmet dependencies.
根檔案系統~Root filesystem|核心成功啟動不代表根目錄可掛載。~Kernel startup does not establish root mounting.|核對裝置、格式與必要驅動。~Check device, format and required drivers.
回歸矩陣~Regression matrix|一次成功不能覆蓋不同配置。~One success does not cover configurations.|列出啟動、SMP 與 suspend 用例。~List boot, SMP and suspend cases.
上游變更~Upstream changes|維護補丁需說明硬體需求與證據。~Maintained patches need hardware rationale and evidence.|整理最小差異與失敗復現。~Collect minimal diffs and failure reproduction.
''','裝置樹本身會實作全部裝置驅動。~The devicetree itself implements all device drivers.|一次成功啟動證明所有核心配置都正確。~One successful boot proves every kernel configuration.',[(310,'啟動序列與映像版本證據共用~Boot sequence and image-version evidence transfer','移植驗證相容性，安全啟動驗證授權~Porting validates compatibility; secure boot validates authorization'),(313,'平臺描述與驅動資源交接相連~Platform description connects to driver resources','核心移植建立全平臺，驅動聚焦特定裝置契約~Porting establishes a platform; drivers implement device contracts')], 'lf')

add(312,'能力權限、IPC 與小可信計算基~Capabilities, IPC and small trusted computing bases','保護域與可信邊界~Protection domains and trust|能力與 IPC~Capabilities and IPC|資源與驅動隔離~Resources and driver isolation|證明與量測~Proof and measurement','ipc proof',
'假設每次同步 IPC 往返消耗單核心 CPU 時間 2 µs（虛構），請求率 100,000/s，純 IPC CPU 時間佔一核心約 0.2 s/s=20%，未含服務工作與爭用。經過時間不必等於 CPU 時間。此假設不是 seL4 效能數據。~Assume a fictional synchronous IPC round trip consumes 2 µs of single-core CPU time at 100,000 requests/s: IPC alone consumes 0.2 s/s, or 20% of one core, excluding service work and contention. Elapsed time need not equal CPU time; not seL4 performance data.', '''
微核心範圍~Microkernel scope|最小核心將多數服務移到使用者域。~A minimal kernel moves many services to user domains.|畫核心與服務的邊界。~Draw kernel/service boundaries.
可信計算基~Trusted computing base|系統 TCB 不等於核心程式碼總量。~System TCB is not just kernel code size.|列出應用需信任的服務。~List services trusted by an application.
保護域~Protection domains|位址空間隔離需明確授權跨域交流。~Address isolation needs authorized cross-domain exchange.|建立兩個假想域的資源表。~Build resource tables for two domains.
核心機制~Kernel mechanisms|機制與政策可分別放在不同層。~Mechanisms and policies may reside separately.|分類排程機制與分配政策。~Separate scheduling mechanism and policy.
能力權限~Capabilities|持有能力代表對物件的特定權限。~Capabilities confer particular rights over objects.|比較讀、寫與轉授矩陣。~Compare read, write and delegation rights.
能力撤銷~Capability revocation|衍生能力的撤銷需考慮整個關係。~Revocation must consider derived capabilities.|畫授權樹並標示撤銷範圍。~Draw delegation and revocation scope.
同步 IPC~Synchronous IPC|呼叫與接收配對會形成等待。~Calls and receives pair and may wait.|檢查未有接收者的時序。~Inspect timing without a receiver.
非同步通知~Async notifications|通知訊號不同於傳送完整訊息。~Notifications differ from full-message transfer.|比較事件計數與數據交換。~Compare event counts and data exchange.
共享頁面~Shared pages|共享記憶體仍需要資料同步協定。~Shared pages still require synchronization.|核對 ring 的擁有權轉移。~Audit ring ownership transitions.
驅動隔離~Driver isolation|使用者態驅動減少核心直接介入。~User-mode drivers reduce direct kernel involvement.|畫故障影響與重啟邊界。~Draw fault and restart boundaries.
DMA 邊界~DMA boundaries|DMA 可能繞過一般 CPU MMU 隔離。~DMA may bypass ordinary CPU MMU isolation.|標示 IOMMU 與可信 DMA 假設。~Mark IOMMU and trusted-DMA assumptions.
排程預算~Scheduling budgets|隔離記憶體不能自行隔離 CPU 時間。~Memory isolation alone does not isolate CPU time.|比較失控服務的時間佔用。~Compare CPU use by an unbounded service.
形式規格~Formal specification|證明成立於規格及明示假設。~Proofs depend on specifications and assumptions.|列出硬體、啟動與 DMA 前提。~List hardware, boot and DMA premises.
證明範圍~Proof coverage|已證核心不代表所有應用皆已證。~A verified kernel does not verify every application.|區分已證與未證組件。~Separate verified and unverified components.
IPC 成本~IPC costs|訊息成本需與服務工作分離。~Messaging costs differ from service work.|重算本課每核心佔用。~Recalculate course per-core utilization.
錯誤處理~Fault handling|服務重啟需復原合法資源狀態。~Service restart must restore valid resource state.|模擬服務死亡後的客戶回應。~Model client responses after service death.
''','核心證明自動涵蓋所有驅動與應用。~Kernel proofs automatically cover all drivers and applications.|使用者態驅動無需考慮 DMA 權限。~User-mode drivers need no DMA permission analysis.',[(309,'IPC 與排程的延遲會互相影響~IPC and scheduling latencies interact','即時保證需時間分析，形式功能證明不替代它~Timing analysis is needed beyond functional proof'),(322,'硬體隔離與資源治理相近~Hardware isolation and resource governance are related','微核心隔離服務，hypervisor 隔離客體系統~Microkernels isolate services; hypervisors isolate guests')], 'lf')

add(313,'裝置生命週期、DMA 與併發契約~Device lifecycle, DMA and concurrency contracts','資源與探測~Resources and probing|I/O 與 DMA~I/O and DMA|中斷與併發~Interrupts and concurrency|復原與移除~Recovery and removal','dma driver',
'假設 descriptor ring 有 256 格，每格 16 B，需 4096 B；每格代表一筆傳輸。在 1 M筆/s 且服務暫停 100 µs，積壓 100 格，未計既有佔用與突發，因此不能僅憑 256 格宣稱無損。~A 256-entry descriptor ring at 16 B/entry uses 4096 B. At 1 Mitems/s, a 100 µs pause adds 100 entries; existing occupancy and bursts are excluded, so 256 entries do not establish losslessness.', '''
裝置匹配~Device matching|匯流排識別與驅動匹配分開於功能探測。~Bus matching differs from functional probing.|核對虛構裝置與驅動表。~Match fictional devices and driver tables.
資源擁有~Resource ownership|記憶體、IRQ 與時鐘需有生命週期。~Memory, IRQ and clocks need lifecycles.|畫取得與釋放對稱路徑。~Draw paired acquire/release paths.
探測失敗~Probe failure|部分成功後失敗需回收既有資源。~Partial probe failure needs resource rollback.|在每個取得點插入假想失敗。~Insert modeled failures at acquisition points.
裝置模型~Device model|父子裝置與 driver 關係有不同角色。~Parent devices and drivers have distinct roles.|畫裝置樹與綁定關係。~Draw device trees and bindings.
MMIO~MMIO|裝置暫存器存取不等於一般 RAM。~Register I/O differs from ordinary RAM.|分開可讀、清除與有副作用欄位。~Separate readable, clearing and side-effect fields.
DMA 位址~DMA addresses|CPU 虛擬位址不等於裝置 DMA 位址。~CPU virtual addresses differ from DMA addresses.|標示虛擬、實體與 DMA 空間。~Mark virtual, physical and DMA spaces.
一致 DMA~Coherent DMA|一致映射仍可能需要記憶體屏障。~Coherent mapping can still require barriers.|核對 descriptor valid 之前的順序。~Audit ordering before descriptor validity.
串流 DMA~Streaming DMA|方向與同步操作需符合擁有權。~Direction and synchronization follow ownership.|畫 CPU 與裝置交接。~Draw CPU/device handoffs.
中斷上下文~Interrupt context|中斷上下文不能任意執行可睡眠工作。~Interrupt context cannot freely run sleeping work.|分類可立即與需延後的任務。~Classify immediate and deferred work.
Ring 狀態~Ring state|head/tail 與擁有位元需一致。~Head/tail and ownership bits must agree.|模擬滿、空與繞回。~Model full, empty and wraparound.
鎖粒度~Lock granularity|鎖範圍影響競爭與死鎖風險。~Lock scope affects contention and deadlock risk.|建立單向鎖順序圖。~Build a directed lock-order graph.
工作取消~Work cancellation|移除裝置前需防止回呼再取資源。~Removal must prevent callbacks reusing resources.|畫取消、同步與釋放順序。~Draw cancel, synchronize and free ordering.
錯誤復原~Error recovery|重設後軟體需重建有效裝置狀態。~Software rebuilds valid state after reset.|比對重設前後 ring 內容。~Compare ring contents across reset.
電源管理~Power management|休眠與喚醒需保留或重建必要狀態。~Suspend/resume must preserve or rebuild state.|檢查未完成 I/O 的政策。~Audit policies for unfinished I/O.
容量預算~Capacity budgets|佇列深度要含服務間隔與突發。~Queue depth includes service gaps and bursts.|擴充本課 100 格積壓例。~Extend the 100-entry backlog example.
卸載驗收~Unload acceptance|無功能錯誤不代表無資源洩漏。~Functional success does not imply no leaks.|核對反覆取得與釋放計數。~Check repeated acquire/release counts.
''','DMA 位址可直接由 CPU 指標轉型得到。~DMA addresses can be obtained by casting CPU pointers.|一致 DMA 保證所有 descriptor 更新順序。~Coherent DMA guarantees every descriptor update order.',[(311,'裝置樹與平臺資源必須銜接~Devicetrees and platform resources connect','平臺移植建立環境，驅動實作裝置生命週期~Porting establishes context; drivers implement lifecycle'),(308,'錯誤紀錄與資料完整性共同~Error records and data integrity transfer','ECC 修復儲存位元，DMA API 管理傳輸映射~ECC repairs stored bits; DMA APIs manage transfer mappings')], 'lf')

add(314,'詞法、語義與可驗證 IR~Lexing, semantics and verifiable IR','語言與剖析~Language and parsing|語義與型別~Semantics and types|SSA 與控制流~SSA and control flow|診斷與回歸~Diagnostics and regression','lexer ir',
'假想教學函式有三個基本區塊：entry、then、merge。分支在 then 定義 x1、entry 定義 x0，merge 需一個 phi（兩 incoming）。若迴圈再添加一個回邊，需依 CFG 重算而非沿用兩值。~A toy function has entry, then and merge blocks. With x1 defined in then and x0 in entry, merge needs one phi with two incoming values. Adding a loop back edge requires CFG-dependent recalculation.', '''
詞法契約~Lexer contract|字元序列被分成帶位置的 token。~Characters become location-bearing tokens.|追蹤數字、識別字與運算子。~Trace numbers, identifiers and operators.
保留字~Keywords|保留字辨識與一般名稱查找不同。~Keyword recognition differs from name lookup.|比較相近拼字 token 結果。~Compare similarly spelled token outcomes.
運算子優先~Operator precedence|同一 token 可形成不同剖析樹。~Tokens can produce different parse trees.|畫 a+b*c 與 (a+b)*c。~Draw a+b*c and (a+b)*c.
錯誤恢復~Error recovery|診斷需定位錯誤而非無限循環。~Diagnostics locate errors without endless loops.|比較缺括號與非法 token。~Compare missing brackets and illegal tokens.
AST~AST|AST 保留語義結構而非全部字面格式。~ASTs retain semantic structure, not all formatting.|比較源碼與 AST 節點。~Compare source and AST nodes.
作用域~Scopes|名稱的可見範圍依宣告位置決定。~Declarations determine name visibility.|模擬遮蔽與未宣告名稱。~Model shadowing and undeclared names.
型別檢查~Type checking|型別錯誤應在明定階段拒絕。~Type errors are rejected at defined stages.|列出可轉換與不可轉換例。~List permitted and forbidden conversions.
函式介面~Function interfaces|參數、傳回型別與呼叫契約需相容。~Parameters, returns and calling contracts agree.|核對兩個假想呼叫點。~Audit two fictional call sites.
基本區塊~Basic blocks|區塊有入口與明確終結控制。~Blocks have entries and explicit terminators.|以分支拆分小程式。~Split a toy program at branches.
CFG~CFG|控制流邊與文本先後不同。~Control-flow edges differ from textual order.|畫入口到出口的可達邊。~Draw reachable entry-to-exit edges.
SSA 定義~SSA definitions|SSA 名稱各有單一靜態定義。~SSA names have one static definition each.|重新命名重複賦值。~Rename repeated assignments.
Phi 輸入~Phi inputs|Phi 的輸入須配對 predecessor。~Phi inputs match predecessors.|重算本課合併區塊案例。~Recalculate the course merge example.
支配關係~Dominance|定義需在適用路徑支配使用。~Definitions dominate uses on relevant paths.|檢查分支內定義外部使用。~Check uses of branch-local definitions.
IR 驗證~IR verification|格式合格不保證符合原程式語義。~Valid IR format does not prove source equivalence.|分開 verifier 與 reference 比較。~Separate verifier and reference checks.
Undefined 邊界~Undefined-behavior boundaries|未定義語義不能用正常測例證明安全。~Normal tests cannot establish undefined-case safety.|明列除零與溢位語義。~Specify division-zero and overflow semantics.
回歸測試~Regression tests|正負用例需同時覆蓋語言契約。~Positive and negative cases cover language contracts.|建立 token、AST 與結果對照。~Build token, AST and result comparisons.
''','IR verifier 通過就等於原程式語義正確。~Passing the IR verifier proves source-semantic correctness.|Phi 的輸入與 CFG predecessor 無關。~Phi inputs are independent of CFG predecessors.',[(315,'IR、支配與語義驗證可直接沿用~IR, dominance and semantic validation transfer','JIT 另需執行時金鑰、守衛與程式碼生命週期~JIT also needs runtime symbols, guards and code lifetimes'),(327,'工具鏈及語義結果需要版本證據~Toolchains and semantics need version evidence','可重現建置驗證位元，不替代語言正確性~Reproducible builds verify bytes, not language correctness')], 'stanford')

add(315,'最佳化合法性、JIT 編譯與去最佳化~Optimization legality, JIT compilation and deoptimization','執行時編譯契約~Runtime compilation contracts|最佳化與分析~Optimization and analysis|程式碼生命週期~Code lifecycles|效能與語義驗收~Performance and semantic acceptance','orc ir',
'假設編譯成本 40 ms，每次執行由 1.0 ms 降至 0.6 ms，節省 0.4 ms/call，回本次數=40/0.4=100 calls。未含暖機、profiling、記憶體及去最佳化；少於 100 次可能較慢。~Assume 40 ms compilation and execution reduced from 1.0 to 0.6 ms/call. Break-even=40/0.4=100 calls, excluding warmup, profiling, memory and deoptimization; fewer calls may be slower.', '''
JIT 與 AOT~JIT and AOT|編譯時間位置與可用資訊不同。~Compilation timing and available information differ.|比較啟動與穩態成本。~Compare startup and steady costs.
符號查找~Symbol lookup|程式碼引用需解析到合法符號。~Code references resolve to valid symbols.|建立缺失與重複符號案例。~Construct missing and duplicate symbols.
編譯分層~Compilation tiers|低成本層與高最佳化層服務不同階段。~Cheap and optimized tiers serve different phases.|畫熱度觸發的轉換。~Draw hotness-triggered transitions.
Profile 資料~Profile data|過去熱門路徑不能保證未來相同。~Past hot paths do not guarantee future behavior.|比較訓練與驗收工作負載。~Compare profiling and acceptance workloads.
常數折疊~Constant folding|折疊必須遵守型別與溢位語義。~Folding obeys types and overflow semantics.|核對邊界值轉換結果。~Check boundary-value transformations.
公共子式~Common subexpressions|有副作用操作不能任意合併。~Side-effecting operations cannot be freely merged.|區分純運算與狀態讀取。~Separate pure computation and state reads.
迴圈不變~Loop invariance|搬移運算需確保依賴與例外合法。~Motion must respect dependencies and exceptions.|檢查零次迴圈的例外。~Check exceptions in zero-iteration loops.
向量化~Vectorization|資料相依與別名限制向量化合法性。~Dependencies and aliasing limit legal vectorization.|比較重疊與不重疊陣列。~Compare overlapping and disjoint arrays.
執行時守衛~Runtime guards|特化假設需有可檢查條件。~Specialization assumptions need checkable guards.|追蹤型別改變後路徑。~Trace paths after a type change.
去最佳化~Deoptimization|退出特化需重建一般執行狀態。~Leaving specialization reconstructs generic state.|核對 locals 與控制位置。~Audit locals and control position.
延遲編譯~Lazy compilation|首次呼叫成本需獨立計入。~First-call compilation costs are separate.|比較首呼叫與穩態時間。~Compare first and steady calls.
程式碼回收~Code reclamation|仍被使用的程式碼不能立即釋放。~In-use code cannot be immediately freed.|畫引用與退役的生命週期。~Draw reference and retirement lifetimes.
編譯回本~Compilation amortization|總節省需超過編譯成本。~Savings must exceed compilation cost.|核算本課 100 次回本。~Audit the 100-call break-even.
基準穩定~Benchmark stability|暖機、GC 與系統負載影響結果。~Warmup, GC and system load affect results.|保持版本與輸入並重複。~Keep versions/inputs fixed and repeat.
數值合法~Numerical legality|快速浮點假設可能改變結果。~Fast floating-point assumptions may change results.|比較 NaN 與誤差容許契約。~Compare NaN and error-tolerance contracts.
差分驗證~Differential validation|優化與未優化結果應對照相同語義。~Optimized and baseline outputs share semantics.|對邊界資料比較結果。~Compare outputs on boundary inputs.
''','測例相同就可忽略最佳化的副作用語義。~Matching tests permit ignoring side-effect semantics.|每個函式高成本最佳化必定降低總耗時。~Expensive optimization always reduces total time.',[(314,'SSA、型別與控制流是共同基礎~SSA, types and control flow are shared foundations','前端建立語義表示，JIT 還需執行時狀態復原~Frontends represent semantics; JIT must recover runtime state'),(304,'向量化與平行資料佈局相通~Vectorization and parallel layouts transfer','JIT 特化不等於自動 GPU 供料與同步~JIT specialization does not automatically solve GPU feeding/synchronization')], 'stanford')

add(316,'命名空間、區塊放置與複製復原~Namespaces, block placement and replica recovery','命名與區塊~Names and blocks|複製與放置~Replication and placement|一致性與故障~Consistency and failures|容量與復原驗證~Capacity and recovery','hdfs hdfsec',
'假設資料 1 TiB，三份完整複本需要 3 TiB；6+3 抹除編碼的理想資料成本為 1.5 TiB。未含 metadata、padding、重建暫存與保留容量；編碼與複製的修復交通不同。~Assume 1 TiB data: three replicas need 3 TiB, while ideal 6+3 erasure coding needs 1.5 TiB. Metadata, padding, rebuild scratch and headroom are omitted; repair traffic differs.', '''
命名空間~Namespace|檔案名稱與實際區塊位置分離。~File names are separate from block locations.|畫名稱到區塊的映射。~Draw name-to-block mappings.
Metadata 服務~Metadata service|控制資料與檔案內容走不同路徑。~Metadata and file content follow different paths.|區分查詢與讀資料流。~Separate lookup and data-read flows.
區塊大小~Block size|區塊大小影響 metadata 與平行粒度。~Block size changes metadata and parallel granularity.|比較小檔與大檔區塊數。~Compare block counts for small/large files.
讀寫語義~Read/write semantics|分散檔案介面不必等同所有 POSIX 語義。~Distributed interfaces may differ from POSIX semantics.|列出追加與任意覆寫需求。~List append and random-overwrite needs.
複本因子~Replication factor|複本數影響容量與容錯範圍。~Replication affects capacity and fault tolerance.|重算本課三份容量。~Recalculate the three-replica capacity.
機架感知~Rack awareness|同機架複本仍共用故障域。~Same-rack replicas share failure domains.|比較跨機架與同架配置。~Compare cross-rack and same-rack placement.
寫入管線~Write pipeline|資料傳送與確認鏈需分別追蹤。~Data and acknowledgment chains are distinct.|畫三副本的寫入確認。~Draw three-replica write acknowledgments.
抹除編碼~Erasure coding|k+m 編碼需考慮條帶與修復工作。~k+m coding needs stripe and repair analysis.|比較 6+3 的容量與重建。~Compare 6+3 capacity and rebuild.
心跳與失效~Heartbeats and failures|心跳缺失可能是網路隔離。~Missing heartbeats may indicate a partition.|區分慢節點與不可達節點。~Separate slow and unreachable nodes.
區塊報告~Block reports|存活訊號不等於完整區塊目錄。~Liveness does not establish a complete block inventory.|核對報告版本與遺失區塊。~Check report versions and missing blocks.
檢查碼~Checksums|檢查碼偵測位元損壞但不能單獨復原。~Checksums detect corruption but do not restore alone.|模擬損壞與替代副本。~Model corruption and alternate replicas.
Metadata 日誌~Metadata journal|復原需將快照與後續日誌銜接。~Recovery joins snapshots and subsequent journals.|重播虛構命名操作序列。~Replay fictional namespace operations.
復原節流~Recovery throttling|全速重建可能搶佔使用者頻寬。~Full-speed rebuild can steal user bandwidth.|比較服務與修復資源預算。~Compare serving and repair budgets.
再平衡~Rebalancing|移動區塊需維持有效複本條件。~Moving blocks preserves valid replica conditions.|核對搬移前、中、後狀態。~Audit before/during/after move states.
小檔成本~Small-file costs|少量位元組也可能耗費完整 metadata。~Tiny payloads still consume metadata.|計算每檔假想 metadata 成本。~Calculate assumed per-file metadata cost.
還原演練~Restore exercises|資料可讀與命名空間正確都需驗證。~Readable data and correct namespaces both matter.|比對完整性、權限與路徑。~Compare integrity, permissions and paths.
''','三份複本同一機架可保證機架失效存活。~Three replicas in one rack guarantee rack-failure survival.|抹除編碼省容量即代表修復沒有成本。~Erasure coding savings eliminate repair costs.',[(317,'資料放置、完整性與修復分析相通~Placement, integrity and repair analysis transfer','檔案系統有階層名稱與檔案語義，物件 API 有 key/版本語義~Filesystems have paths/file semantics; objects have keys/versions'),(319,'Metadata HA 需要共識或明示協調~Metadata HA needs consensus or explicit coordination','複製區塊資料不同於提交共識日誌~Replicating blocks differs from committing consensus logs')], 'lf')

add(317,'物件 API、版本與分佈式耐久性~Object APIs, versions and distributed durability','物件與介面~Objects and interfaces|分片與放置~Sharding and placement|版本與安全~Versioning and security|修復與成本~Repair and cost','object ceph',
'假設 100 TB 十進位資料以 8+3 編碼，理想成本=(11/8)×100=137.5 TB；保留 20% 總容量空閒需 137.5/0.8=171.875 TB。未含小物件 padding、metadata 與副本過渡。~Assume 100 decimal TB with 8+3 coding: ideal storage=137.5 TB. Keeping 20% of total capacity free requires 171.875 TB. Small-object padding, metadata and transition copies are omitted.', '''
Key 命名~Key naming|物件 key 不一定是真正的目錄。~Object keys need not represent real directories.|比較 prefix 與目錄移動需求。~Compare prefixes and directory-move needs.
API 契約~API contracts|相容 API 不代表所有語義完全相同。~API compatibility does not ensure identical semantics.|列出必要 status 與錯誤碼。~List required statuses and error codes.
物件 Metadata~Object metadata|使用者 metadata 與系統版本資訊不同。~User metadata differs from system version data.|分類假想標頭及保存需求。~Classify fictional headers and retention needs.
Multipart~Multipart|分段上傳需完整提交與殘留清理。~Multipart uploads need completion and residue cleanup.|追蹤成功與未完成上傳。~Trace complete and incomplete uploads.
分片定位~Shard placement|定位函式將物件映射至有限資源。~Placement maps objects to finite resources.|比較均勻與偏斜 key 分佈。~Compare uniform and skewed keys.
故障域~Failure domains|不同磁碟未必位於不同故障域。~Different disks need not have independent failures.|將磁碟、主機及機架分層。~Separate disk, host and rack layers.
編碼池~Coded pools|資料編碼與 metadata 策略可不同。~Data coding and metadata policy may differ.|比較資料與索引復原責任。~Compare data and index recovery roles.
讀修復~Read repair|修復必須辨識哪一版本可信。~Repair must establish the authoritative version.|用兩版本案例核對決策。~Audit decisions with two versions.
版本控制~Versioning|新版本不一定刪除舊版本。~New versions need not erase old ones.|畫版本與刪除標記生命週期。~Draw version/delete-marker lifetimes.
生命週期~Lifecycle|到期政策需考慮法律保存與還原需求。~Expiry policy accounts for retention and recovery.|比較資料與未完成段到期。~Compare object and unfinished-part expiry.
權限與租戶~Permissions and tenants|Bucket 與物件權限要符合租戶邊界。~Bucket/object rights follow tenant boundaries.|設計跨租戶拒絕用例。~Design cross-tenant denial cases.
完整性驗證~Integrity verification|ETag 不可一概當作 SHA-256。~ETags are not universally SHA-256 digests.|記錄明確 checksum 類型。~Record explicit checksum types.
容量保留~Capacity headroom|剩餘空間需吸收失效及重建。~Free space absorbs failures and rebuilds.|核算本課 20% headroom。~Audit the 20% headroom example.
小物件成本~Small-object costs|小物件的索引與編碼 overhead 可顯著。~Index/coding overhead matters for small objects.|比較 1 KiB 與 1 MiB 成本。~Compare 1 KiB and 1 MiB costs.
流量費用~Transfer costs|容量成本與 API、網路成本分開。~Storage costs differ from API/network costs.|建立假想每月成本表。~Build a fictional monthly cost table.
修復驗收~Repair acceptance|存活物件數不能替代逐物件摘要。~Live object count cannot replace per-object digests.|比較修復前後版本與摘要。~Compare versions and digests across repair.
''','ETag 永遠就是內容 SHA-256。~An ETag is always the content SHA-256.|不同磁碟自然就有獨立故障概率。~Different disks automatically have independent failures.',[(316,'複製、編碼與容量預算共用~Replication, coding and capacity budgets transfer','物件服務語義需重查，不能假設檔案 rename 或局部覆寫~Object semantics need rechecking for rename/random overwrite'),(329,'版本與備份需要不同保存責任~Versions and backups have distinct retention roles','線上版本可能同時受管理者錯誤影響~Online versions may share administrative failures')], 'lf')

add(318,'ACID、MVCC 與可復原日誌~ACID, MVCC and recoverable logging','交易與隔離~Transactions and isolation|MVCC 與併發~MVCC and concurrency|WAL 與提交~WAL and commit|復原與驗收~Recovery and acceptance','wal isolation',
'假設每批 fsync=4 ms 且一次序列寫入，單筆提交理想上界 250 commits/s；每批 20 交易的 group commit 為 5000 transactions/s，上界未含日誌流量、鎖與排隊延遲。~With assumed 4 ms serial fsync, one transaction/batch has an ideal 250 commits/s bound. Twenty transactions/group yields 5000 transactions/s, excluding log bandwidth, locks and queueing.', '''
ACID 分離~ACID separation|原子性、一致性、隔離與耐久是不同屬性。~Atomicity, consistency, isolation and durability differ.|將假想失敗對應各屬性。~Map fictional failures to properties.
交易邊界~Transaction boundaries|多步操作需明定共同提交範圍。~Multi-step operations need commit boundaries.|拆分付款與庫存的假想步驟。~Split fictional payment/inventory steps.
讀取快照~Read snapshots|可見版本取決於交易隔離規則。~Visible versions follow isolation rules.|追蹤兩交易讀到的值。~Trace values observed by two transactions.
異常分類~Anomaly classification|髒讀、不可重複讀與幻讀不同。~Dirty, nonrepeatable and phantom reads differ.|用兩會話紙上時序分類。~Classify paper traces of two sessions.
MVCC 版本~MVCC versions|多版本允許讀者看到合法舊快照。~Versions permit valid older reader snapshots.|畫 tuple 版本與可見時間。~Draw tuple versions and visibility.
行鎖~Row locks|行鎖保護指定資料而非所有條件集合。~Row locks protect rows, not every predicate set.|比較行相同與條件重疊。~Compare same rows and overlapping predicates.
Serializable~Serializable|序列化失敗可能需要整個交易重試。~Serialization failures may require whole-transaction retries.|建立不重複副作用的重試。~Design retries without duplicate side effects.
死鎖~Deadlocks|相反鎖順序可形成循環等待。~Opposite lock order creates circular wait.|繪製兩交易持鎖圖。~Draw a two-transaction lock graph.
預寫順序~Write-ahead ordering|對應日誌需先於資料頁耐久。~Relevant logs become durable before data pages.|核對寫入與 flush 時序。~Audit writes and flush ordering.
提交確認~Commit acknowledgment|成功確認需符合選定耐久政策。~Acknowledgment follows selected durability policy.|比較同步與非同步承諾。~Compare synchronous/asynchronous promises.
Group commit~Group commit|共用 flush 改變吞吐與等待分佈。~Shared flush changes throughput and waiting.|核算本課批次提交上界。~Audit group-commit throughput bounds.
Checkpoint~Checkpoint|檢查點縮小復原範圍但非替代 WAL。~Checkpoints bound recovery work, not replace WAL.|追蹤檢查點後的日誌。~Trace logs after a checkpoint.
崩潰重播~Crash replay|重播需處理已提交及未完成狀態。~Replay handles committed and unfinished state.|枚舉不同崩潰位置。~Enumerate crash points.
索引一致~Index consistency|索引與資料頁需維持可復原關係。~Indexes and data maintain recoverable relationships.|比對查詢與全表結果。~Compare indexed and full-scan results.
清理版本~Version cleanup|長交易可能阻止舊版本回收。~Long transactions can delay version reclamation.|比較長快照與清理積壓。~Compare long snapshots and cleanup backlog.
不變量驗收~Invariant acceptance|資料庫提交不代表業務不變量正確。~Commit success does not establish business invariants.|核對餘額守恆與唯一約束。~Check balance conservation and uniqueness.
''','MVCC 等於所有交易均為 serializable。~MVCC makes every transaction serializable.|資料頁先耐久而日誌後寫仍符合 WAL。~Durable pages before their logs satisfy WAL.',[(319,'耐久日誌及提交證據相通~Durable logs and commit evidence transfer','本地 ACID 與跨節點共識具有不同失效模型~Local ACID and consensus have different failure models'),(329,'基底備份與日誌需銜接~Base backups and journals connect','復原保留點與日常交易延遲需求不同~Recovery targets differ from routine transaction latency')], 'lf')

add(319,'Raft 狀態、quorum 與線性化證據~Raft state, quorums and linearizability evidence','任期與選舉~Terms and elections|日誌複製與提交~Log replication and commit|讀取與重配置~Reads and reconfiguration|故障與歷史驗證~Failures and history validation','raft etcd',
'假設五個投票節點，多數=3，最多容忍兩個節點不可用；3+2 分割僅 3 節點側可在其他條件滿足時提交。30 ms 對等 RTT 只提供路徑預算，不保證 30 ms 提交，仍需持久化與排程。~With five voting nodes, majority=3 and at most two unavailable nodes are tolerated. In a 3+2 split only the three-node side may commit if other conditions hold. A 30 ms peer RTT is a path budget, not a commit guarantee.', '''
失效模型~Failure model|Raft 一般處理 crash fault 而非任意惡意節點。~Raft generally handles crashes, not arbitrary malicious nodes.|列出模型內與外的失效。~List in-model and out-of-model failures.
任期單調~Monotonic terms|任期需持久記錄並隨新任期增加。~Terms persist and increase with new terms.|追蹤重啟前後 term。~Trace terms across restart.
投票約束~Voting constraints|同任期的投票需符合協定限制。~Votes obey same-term protocol constraints.|核對重啟後是否可重投。~Check voting after restart.
選舉逾時~Election timeouts|隨機逾時降低同時競選衝突。~Random timeouts reduce concurrent candidacy.|比較同步與分散逾時。~Compare identical and spread timeouts.
日誌匹配~Log matching|索引與任期共同辨識匹配前綴。~Index and term identify matching prefixes.|比較兩份分叉日誌。~Compare diverging logs.
領導者提交~Leader commit|提交需符合目前任期的規則。~Commit follows current-term rules.|分開復制數與已提交索引。~Separate replica count and committed index.
狀態機套用~State-machine application|已提交與已套用是不同進度。~Committed and applied indices differ.|追蹤慢狀態機的積壓。~Trace backlog of a slow state machine.
重複請求~Duplicate requests|重試可能需要應用層識別去重。~Retries may need application-level deduplication.|給假想命令加 request ID。~Add request IDs to fictional commands.
線性化讀取~Linearizable reads|讀取需要確認合法最新視圖。~Reads need a legitimate current view.|比較序列化與本地舊讀。~Compare linearizable and stale local reads.
Quorum 交集~Quorum intersection|多數集合的交集支援安全性。~Majority intersection supports safety.|枚舉五節點的三節點集合。~Enumerate three-node subsets of five.
成員變更~Membership changes|改成員需遵守過渡 quorum 規則。~Membership changes obey transitional quorums.|畫舊新成員交接邊界。~Draw old/new membership transitions.
快照截斷~Snapshot truncation|快照需繫結最後包含索引與任期。~Snapshots bind included index and term.|核對快照後日誌銜接。~Audit snapshot/log continuity.
網路分割~Network partitions|失去 quorum 可保安全而失去進度。~Losing quorum preserves safety but stops progress.|分析本課 3+2 分割。~Analyze the course 3+2 partition.
時鐘假設~Clock assumptions|安全與逾時所需假設應分列。~Safety and timeout assumptions differ.|比較時鐘偏移與訊息延遲。~Compare skew and message delay.
持久化~Persistence|回應前的持久化影響重啟證據。~Pre-response persistence affects restart evidence.|枚舉寫入與確認間的崩潰。~Enumerate write/acknowledgment crashes.
歷史檢查~History checking|單次測試無法證明所有共識軌跡。~One test cannot prove all consensus histories.|檢查假想歷史的不變量。~Check invariants in fictional histories.
''','五節點 Raft 兩節點仍可單獨提交。~Two nodes alone can commit in five-node Raft.|Raft 的 crash 模型自動防止 Byzantine 節點。~Raft crash tolerance automatically prevents Byzantine nodes.',[(318,'日誌與原子提交是共同概念~Logs and atomic commit are shared concepts','交易隔離不能替代共識 quorum~Transaction isolation cannot replace consensus quorums'),(321,'叢集控制狀態常依賴一致儲存~Cluster control state relies on consistent storage','共識持久化不等於 workload 調度成功~Consensus persistence does not guarantee workload scheduling')], 'stanford')

add(320,'事件時間、分區日誌與檢查點~Event time, partition logs and checkpoints','事件與分區~Events and partitions|時間與窗口~Time and windows|狀態與重播~State and replay|背壓與語義驗證~Backpressure and semantic validation','kafka flink',
'假設每秒 50,000 筆事件、每筆 400 B：原始流量=20 MB/s。保留 24 h=1.728 TB，三份複本=5.184 TB，未計壓縮、索引、重試與編碼。晚到容許 10 s 不代表所有事件準時。~Assume 50,000 events/s at 400 B/event: 20 MB/s raw traffic, 1.728 TB over 24 h and 5.184 TB for three replicas, excluding compression, indexes, retries and encoding. A 10 s lateness allowance does not ensure timely arrivals.', '''
事件 schema~Event schema|資料格式演進需維持消費者相容。~Schema evolution preserves consumer compatibility.|比較新增選填與改型別。~Compare optional additions and type changes.
分區鍵~Partition keys|分區鍵影響順序、平行及熱點。~Keys affect ordering, parallelism and hotspots.|比較均勻與熱門 key。~Compare uniform and hot keys.
Offset~Offsets|Offset 是分區位置，不是全域時間。~Offsets are partition positions, not global time.|畫兩分區 offset 序列。~Draw offset sequences for two partitions.
消費者群組~Consumer groups|分區分配限定同群組的平行度。~Partition assignment bounds group parallelism.|比較分區與 consumer 數。~Compare partition and consumer counts.
事件時間~Event time|事件發生時間不同於處理到達時間。~Event time differs from processing arrival time.|將相同事件以兩順序送入模型。~Model two arrival orders of the same events.
Watermark~Watermarks|水位是時間進度假設，不是完成證明。~Watermarks express progress assumptions, not proof of completion.|加入晚到與閒置分區。~Add late arrivals and idle partitions.
窗口~Windows|窗口邊界決定聚合涵蓋的事件。~Window boundaries determine aggregation membership.|比較滾動與滑動窗口。~Compare tumbling and sliding windows.
晚到策略~Late-event policy|丟棄、更正與側輸出有不同語義。~Drop, correction and side output differ.|對晚到事件列出三種結果。~List three late-event outcomes.
有狀態運算~Stateful operations|key 狀態大小影響記憶體及復原。~Keyed state affects memory and recovery.|估算 key 數與每 key bytes。~Estimate key count and bytes/key.
檢查點~Checkpoints|一致檢查點需銜接來源位置與狀態。~Consistent checkpoints join source positions and state.|追蹤故障前後 offset。~Trace offsets across failure.
輸出語義~Output semantics|Exactly-once 需界定 sink 的交易協作。~Exactly-once needs defined sink transaction support.|分開處理與外部副作用。~Separate processing and external side effects.
重播去重~Replay deduplication|相同事件重播需避免重複業務效果。~Replay must avoid duplicate business effects.|用虛構 event ID 檢查。~Check fictional event IDs.
背壓~Backpressure|慢下游會改變延遲與來源積壓。~Slow downstream changes latency and backlog.|比較輸入率與服務率。~Compare arrival and service rates.
再平衡~Rebalancing|重分配需移交 partition 與狀態。~Reassignment hands over partitions and state.|核對停止與接手的重疊。~Audit stopping and takeover overlap.
保存容量~Retention capacity|保留時間需換算持續資料率。~Retention converts sustained rates into storage.|重算本課 24 h 容量。~Recalculate the 24 h storage example.
驗收歷史~Acceptance history|相同總量可能掩蓋重複與遺失。~Equal totals may hide duplicates and losses.|核對事件集合與窗口結果。~Check event sets and window outputs.
''','所有分區 offset 能建立全域事件時間。~Offsets across partitions establish global event time.|Exactly-once 處理自動保證所有外部副作用一次。~Exactly-once processing guarantees every external effect once.',[(318,'狀態提交與交易輸出可互相銜接~State commits and transactional output connect','事件時間窗口不同於資料庫單次快照~Event-time windows differ from database snapshots'),(319,'來源日誌與復原需明確提交規則~Source logs and recovery need commit rules','串流處理業務狀態不等於共識複製狀態機~Stream business state is not consensus state-machine replication')], 'lf')

add(321,'宣告式控制、排程與工作負載隔離~Declarative control, scheduling and workload isolation','控制平面與宣告~Control plane and declarations|排程與資源~Scheduling and resources|安全與網路~Security and networking|更新與故障驗證~Updates and failure validation','k8s pod',
'假設四節點各 8 CPU，每節點保留 1 CPU，allocatable 合計 28 CPU。每個不可跨節點拆分的 pod request 2 CPU，單節點只能放 floor(7/2)=3 個，四節點最多 12 個；14 個 pod 雖需合計 28 CPU，仍確定無法全部排程。拓撲、記憶體與裝置限制可能使上限更低。~Four assumed 8-CPU nodes reserve 1 CPU each, totaling 28 allocatable CPUs. Each indivisible 2-CPU-request pod fits on one node: floor(7/2)=3 pods/node and at most 12 across four nodes. Fourteen pods need 28 CPU in aggregate but definitely cannot all schedule; topology, memory or device constraints may lower the bound further.', '''
宣告狀態~Desired state|宣告期望與實際狀態會短暫不同。~Desired and observed state may temporarily differ.|畫 reconcile 的迭代。~Draw reconciliation iterations.
API 物件~API objects|物件 UID 與名稱代表不同身分。~Object UIDs and names represent different identities.|比較同名刪除重建案例。~Compare deletion/recreation under one name.
控制器~Controllers|控制器監看狀態並調整實際資源。~Controllers observe and adjust actual resources.|追蹤副本不足的補足。~Trace replacement of missing replicas.
etcd 依賴~etcd dependency|控制狀態依賴耐久一致儲存。~Control state depends on durable consistent storage.|區分 API 與 workload 存活。~Separate API and workload liveness.
Requests~Requests|排程依據 request 而非平均量測。~Scheduling uses requests, not measured averages.|核算本課 CPU 可分配量。~Audit course allocatable CPU.
Limits~Limits|Limit 執行效果取決於資源類型。~Limit behavior depends on resource type.|分開 CPU 節流與記憶體失敗。~Separate CPU throttling and memory failure.
拓撲分佈~Topology spread|分散副本減少共同故障曝露。~Spreading replicas reduces common-failure exposure.|比較同節點與跨域放置。~Compare same-node and cross-domain placement.
排程約束~Scheduling constraints|總容量足夠不保證可行放置。~Aggregate capacity does not ensure feasible placement.|加入 affinity 的反例。~Add an affinity counterexample.
Pod 隔離~Pod isolation|容器共用核心不是完整 VM 隔離。~Containers sharing a kernel differ from VMs.|標出 namespace 與 host 邊界。~Mark namespace and host boundaries.
RBAC~RBAC|API 權限與容器內權限需分開。~API rights differ from in-container rights.|建立 namespace 操作矩陣。~Build a namespace action matrix.
網路政策~Network policy|標籤及方向影響允許流量。~Labels and direction affect allowed flows.|紙上核對依賴與拒絕流。~Audit required and denied flows on paper.
Secret 處理~Secret handling|編碼儲存不等於加密與安全授權。~Encoding is not encryption or authorization.|檢查讀取範圍與輸出遮蔽。~Check reader scope and output redaction.
探針語義~Probe semantics|Ready、live 與 startup 回答不同問題。~Readiness, liveness and startup answer different questions.|比較慢啟動與失效情境。~Compare slow startup and failure cases.
滾動更新~Rolling updates|更新需考慮容量及服務就緒。~Rollouts need capacity and service readiness.|追蹤 old/new 副本時程。~Trace old/new replica timing.
排空與中止~Drain and termination|優雅中止需讓請求與狀態收斂。~Graceful shutdown drains requests and state.|核對 grace period 與最長請求。~Compare grace period and longest request.
驗收證據~Acceptance evidence|Pod running 不等於服務可用。~Running pods do not establish service availability.|從使用者路徑核對成功率。~Check success from the user path.
''','所有 running pod 都已可對使用者提供服務。~Every running pod is ready for users.|CPU 總量吻合就能忽略 affinity 排程。~Matching CPU totals permits ignoring affinity.',[(319,'控制狀態持久化需要共識~Persistent control state needs consensus','共識可用不代表節點可供排程~Consensus availability does not imply schedulable nodes'),(324,'服務流量與身份策略相連~Service traffic and identity policies connect','編排管理生命週期，mesh 管理服務間流量~Orchestration manages lifecycles; meshes manage interservice traffic')], 'lf')

add(322,'客體執行、第二層翻譯與資源界線~Guest execution, second-level translation and resource boundaries','主客體與 vCPU~Hosts, guests and vCPUs|記憶體虛擬化~Memory virtualization|裝置與隔離~Devices and isolation|遷移與效能~Migration and performance','kvm mmu virtio',
'假設 2 MiB huge page 與 4 KiB 小頁覆蓋相同 1 GiB：需要 512 個 huge pages 或 262,144 小頁，數量相差 512 倍。頁表量與 TLB 觸及非直接同倍保證，另有碎片及權限粒度成本。~For 1 GiB, 2 MiB pages need 512 pages versus 262,144 pages of 4 KiB: a 512-fold count difference. Page-table size/TLB reach do not guarantee equal gains; fragmentation and permission granularity matter.', '''
主客體邊界~Host/guest boundaries|客體核心特權受 hypervisor 控制。~Guest kernel privilege is controlled by the hypervisor.|標出 host、VMM 與 guest。~Mark host, VMM and guest.
vCPU~vCPUs|vCPU 是被排程的執行上下文。~A vCPU is a scheduled execution context.|比較 vCPU 數與實體核心。~Compare vCPU count and physical cores.
VM exit~VM exits|敏感事件可使執行返回主機。~Sensitive events can return execution to the host.|分類假想 exit 原因。~Classify modeled exit causes.
排程共享~Shared scheduling|客體延遲也受主機排程影響。~Guest latency also depends on host scheduling.|追蹤 overcommit 時間線。~Trace an overcommit timeline.
雙層位址~Two-stage addressing|客體虛擬、實體與主機實體不同。~Guest virtual/physical and host physical differ.|畫兩層轉換路徑。~Draw two-stage translations.
Shadow MMU~Shadow MMU|軟體 shadow 維持可直接用的映射。~Software shadows maintain usable translations.|比較 shadow 與硬體巢狀翻譯。~Compare shadow and hardware nested translation.
TLB 失效~TLB invalidation|修改映射需讓舊快取不再生效。~Mapping changes invalidate obsolete cached translations.|核對重映射後的存取。~Audit access after remapping.
Huge pages~Huge pages|大頁減少表項但提高分配粒度。~Huge pages reduce entries and enlarge allocation granularity.|重算本課 1 GiB 頁數。~Recalculate 1 GiB page counts.
裝置模擬~Device emulation|模擬介面需維持客體可見契約。~Emulated devices preserve guest-visible contracts.|比對暫存器與回應語義。~Compare registers and response semantics.
Virtio~Virtio|半虛擬化使用明確共享佇列契約。~Paravirtualization uses explicit shared-queue contracts.|畫 descriptor 與完成路徑。~Draw descriptor/completion paths.
裝置直通~Device passthrough|直通需要 DMA 與中斷隔離。~Passthrough needs DMA and interrupt isolation.|標出 IOMMU 與共享風險。~Mark IOMMU and sharing risks.
記憶體承諾~Memory commitments|分配、承諾與實際使用不同。~Allocation, commitment and use differ.|比較 guest RAM 與 host 壓力。~Compare guest RAM and host pressure.
Dirty tracking~Dirty tracking|追蹤寫髒頁支援遷移與快照。~Dirty tracking supports migration and snapshots.|比較前後兩輪 dirty 集合。~Compare dirty sets across two rounds.
Live migration~Live migration|收斂需複製速度超過持續寫髒。~Convergence needs copying faster than dirtying.|建立不收斂的速率案例。~Construct a nonconvergent rate case.
隔離驗收~Isolation acceptance|獨立 VM 仍可能共用硬體故障域。~Separate VMs can share hardware failure domains.|區分邏輯與實體隔離。~Separate logical and physical isolation.
效能歸因~Performance attribution|客體耗時需區分退出、I/O 與等待。~Guest time separates exits, I/O and waiting.|建立三項假想耗時帳。~Build three modeled time budgets.
''','VM 數增加就會增加實體 CPU 算力。~More VMs create more physical CPU compute.|VM 隔離自然涵蓋未受限的 DMA 直通。~VM isolation automatically covers unrestricted DMA passthrough.',[(312,'保護域與硬體資源治理共用~Protection domains and hardware governance transfer','微核心服務隔離不同於完整客體 OS 虛擬化~Service isolation differs from full guest OS virtualization'),(323,'microVM 使用虛擬化隔離執行~MicroVMs isolate execution using virtualization','Serverless 還需調度、計量與函式生命週期~Serverless adds scheduling, metering and function lifecycles')], 'lf')

add(323,'函式生命週期、microVM 與彈性成本~Function lifecycles, microVMs and elasticity costs','函式與執行契約~Functions and execution contracts|隔離與啟動~Isolation and startup|調度與擴展~Dispatch and scaling|狀態與成本驗收~State and cost acceptance','firecracker fcdesign',
'假設請求率 200/s，每請求服務 100 ms，不含排隊，Little 法則所需平均在途量 L=λW=20。若每實例一請求，需至少平均 20 活躍槽；不是 20 實例就能保證 p99 或突發 SLO。~At assumed 200 requests/s and 100 ms service time without queueing, Little’s law gives average in-flight L=20. One request/instance needs at least 20 mean active slots, not a p99 or burst SLO guarantee.', '''
執行契約~Execution contracts|函式介面需定義輸入、輸出及逾時。~Function interfaces define input, output and timeout.|核對正常與失敗回應。~Check normal and failed responses.
無狀態邊界~Stateless boundaries|短命執行不代表所有業務無狀態。~Short execution does not make business state disappear.|畫函式與外部狀態。~Draw functions and external state.
MicroVM~MicroVMs|縮小裝置模型降低界面與管理成本。~Smaller device models reduce interfaces and overhead.|比較通用 VM 與精簡裝置圖。~Compare general VM and reduced-device diagrams.
多租戶隔離~Multitenant isolation|隔離需管理記憶體、網路與 CPU。~Isolation governs memory, networks and CPU.|建立租戶資源矩陣。~Build a tenant-resource matrix.
冷啟動~Cold starts|啟動包括映像、環境與應用初始化。~Startup includes image, environment and application setup.|分解三階段啟動假設。~Break down three assumed startup phases.
Warm pool~Warm pools|預暖降低延遲但佔用閒置資源。~Prewarming saves latency but reserves idle resources.|比較預暖比例與成本。~Compare prewarm fraction and cost.
快照啟動~Snapshot startup|還原需考慮時間、隨機性及秘密狀態。~Restore considers clocks, randomness and secret state.|列出不可盲目複用的資料。~List state unsuitable for blind reuse.
映像版本~Image versions|執行證據需繫結指定映像版本。~Execution evidence binds a specific image version.|比對 deployment 與 runtime 摘要。~Compare deployment/runtime digests.
並行槽~Concurrency slots|在途量與到達率、服務時間相關。~In-flight demand depends on arrivals and service time.|核算本課平均 20 槽。~Audit the mean 20-slot example.
擴展延遲~Scaling delay|增加容量有延遲而非瞬間完成。~Capacity growth takes time.|加入突發與擴展準備窗口。~Add burst and scaling-readiness windows.
排隊與拒絕~Queueing and rejection|無界排隊可讓延遲及成本失控。~Unbounded queues inflate latency and cost.|比較排隊上限與拒絕政策。~Compare queue bounds and rejection policies.
公平計量~Fair metering|計量邊界需包含實際計費資源。~Metering boundaries define billed resources.|分開啟動、執行與外部 I/O。~Separate startup, execution and external I/O.
重試去重~Retry deduplication|事件重送需防重複業務副作用。~Redelivery needs duplicate-effect prevention.|建立虛構 idempotency key。~Construct a fictional idempotency key.
外部服務~External services|函式彈性可能壓垮固定容量資料庫。~Elastic functions can overload fixed-capacity databases.|比較函式與 DB 連線上限。~Compare function and DB connection limits.
成本模型~Cost model|每請求與保留資源成本需分列。~Request and reserved-resource costs differ.|建立假想量價表。~Build an assumed usage-price table.
SLO 驗收~SLO acceptance|平均並行不足以證明尾端延遲。~Mean concurrency does not prove tail latency.|對突發工作負載看分位數。~Inspect percentiles for burst workloads.
''','Serverless 代表伺服器與維運成本不存在。~Serverless means servers and operational costs do not exist.|Little 法則平均量可保證 p99 延遲。~Little’s-law averages guarantee p99 latency.',[(322,'客體隔離與映像生命週期相通~Guest isolation and image lifecycles transfer','microVM 還需函式服務調度與計費~MicroVM-based functions add dispatch and metering'),(330,'排隊、擴容與 SLO 可互相銜接~Queues, scaling and SLOs connect','短函式與持續網站服務的冷啟動成本不同~Short functions and persistent web services have different cold-start costs')], 'lf')

add(324,'服務身分、路由政策與韌性控制~Service identities, routing policies and resilience','流量架構與發現~Traffic architecture and discovery|路由與韌性~Routing and resilience|身分與政策~Identity and policy|觀測與驗收~Observation and acceptance','traffic meshsec',
'假設原始 1000 requests/s，每個最多重試兩次，最差請求嘗試量可達 3000/s（首次加兩次），不表示全部成功。若每次 timeout 200 ms 且順序重試，總預算需至少 600 ms 外加 backoff。~At 1000 original requests/s with at most two retries, attempts may reach 3000/s including first attempts. Sequential 200 ms timeouts need at least 600 ms plus backoff, without guaranteeing success.', '''
服務發現~Service discovery|邏輯服務需對應目前可用端點。~Logical services resolve to current endpoints.|畫端點新增與移除時序。~Draw endpoint addition/removal timing.
資料與控制~Data and control|控制政策與資料轉送有不同失效。~Policy control and forwarding fail differently.|比較控制失聯與端點失效。~Compare control disconnection and endpoint failure.
代理邊界~Proxy boundaries|代理加入觀察點也加入資源成本。~Proxies add observation and resource costs.|標出請求經過的代理。~Mark proxies crossed by requests.
流量分流~Traffic splitting|百分比分流需在足夠樣本解讀。~Weighted routing needs adequate samples.|比較十筆與萬筆結果。~Compare ten and ten-thousand requests.
Timeout 預算~Timeout budgets|各 hop 逾時須符合整體 deadline。~Per-hop timeouts fit total deadlines.|建立三服務的時間預算。~Build a three-service time budget.
Retry 預算~Retry budgets|重試會放大負載且需檢查冪等。~Retries amplify load and require idempotency.|核算本課三倍嘗試量。~Audit the threefold attempt count.
Circuit breaker~Circuit breakers|限制連線與排隊保護有限資源。~Connection/queue limits protect finite resources.|比較拒絕與無界等待。~Compare rejection and unbounded waiting.
離群偵測~Outlier detection|局部錯誤資料不一定代表全域故障。~Local errors need not imply global failures.|比較單端點與共同依賴失效。~Compare endpoint and shared-dependency failures.
工作身分~Workload identities|服務身分不同於來源 IP。~Service identity differs from source IP.|比較位址變化與身份變化。~Compare address and identity changes.
mTLS~mTLS|加密驗證連線不自動授權資源。~Authenticated encryption does not authorize resources.|建立已驗證但拒絕的請求。~Build authenticated but denied requests.
憑證輪替~Certificate rotation|輪替需銜接到期與信任更新。~Rotation connects expiry and trust changes.|畫舊新憑證相容窗口。~Draw old/new certificate windows.
授權政策~Authorization policy|政策需明確 subject、action 與資源。~Policy specifies subjects, actions and resources.|核對必要與禁止服務呼叫。~Check required and forbidden service calls.
Trace 傳遞~Trace propagation|跨服務關聯需保留合法 trace context。~Cross-service correlation preserves valid context.|比較有無 context 的鏈結。~Compare chains with/without context.
故障演練~Failure exercises|隔離模擬需預先限定影響範圍。~Isolated simulation bounds impact in advance.|用虛構延遲檢查 fallback。~Use fictional delays to check fallback.
政策推出~Policy rollout|改政策需觀察拒絕與相容性。~Policy rollout checks denial and compatibility.|比較乾跑與正式規則模型。~Compare dry-run and enforced-rule models.
驗收與歸因~Acceptance and attribution|Mesh metrics 需與使用者結果對照。~Mesh metrics correlate with user outcomes.|檢查成功率與末端延遲。~Check success rate and end-user latency.
''','mTLS 已完成所有業務授權。~mTLS completes every business authorization check.|增加重試次數必定提升整體可用率。~More retries necessarily improve overall availability.',[(321,'工作負載、標籤與政策共同~Workloads, labels and policies are shared','mesh 政策執行不替代編排的資源與 rollout 控制~Mesh policies do not replace orchestration resource/rollout control'),(325,'Context 傳遞與觀測資料相通~Context propagation and telemetry transfer','流量控制改行為，追蹤主要收集證據~Traffic control changes behavior; tracing mainly gathers evidence')], 'lf')

add(325,'遙測語義、context 與可靠採樣~Telemetry semantics, context and reliable sampling','訊號與量測契約~Signals and measurement contracts|追蹤與因果~Tracing and causality|採樣與收集~Sampling and collection|SLO 與隱私驗收~SLO and privacy acceptance','traces sampling',
'假設 10,000 traces/s、每 trace 8 spans、每 span 500 B：原始=40 MB/s，頭部 10% 採樣理想為 4 MB/s，未含批次與標頭。低機率錯誤可能被漏採，不可宣稱保留全部錯誤。~Assume 10,000 traces/s, 8 spans/trace and 500 B/span: 40 MB/s raw; ideal 10% head sampling gives 4 MB/s, excluding batches and headers. Rare errors may be missed; this does not retain every error.', '''
三類訊號~Signal types|Metrics、logs 與 traces 回答不同問題。~Metrics, logs and traces answer different questions.|將問題配對適當訊號。~Match questions to signals.
量測語義~Measurement semantics|單位、起止點與成功定義需一致。~Units, boundaries and success definitions agree.|建立延遲與成功率定義。~Define latency and success rate.
屬性基數~Attribute cardinality|高基數維度增加儲存及查詢成本。~High-cardinality dimensions raise storage/query cost.|比較用戶 ID 與服務類別。~Compare user IDs and service classes.
Histogram~Histograms|桶與分位數估計受到邊界影響。~Buckets and quantiles depend on boundaries.|比較兩組桶界與 p99。~Compare bucket boundaries and p99.
Trace ID~Trace IDs|相同 trace ID 關聯同一追蹤範圍。~One trace ID correlates a trace scope.|配對三服務的 span。~Match spans across three services.
父子關係~Parent-child relationships|span 關係描述呼叫而非絕對時間保證。~Span relations describe calls, not absolute timing guarantees.|核對非同步子任務。~Audit asynchronous child tasks.
Context 傳播~Context propagation|跨邊界需明確傳遞與驗證 context。~Context crosses boundaries through explicit validation/propagation.|比較遺失與有效標頭。~Compare missing and valid headers.
時鐘偏差~Clock skew|跨主機絕對時間可有偏差。~Cross-host wall clocks may disagree.|給時間線加偏差範圍。~Add skew bounds to timelines.
Head sampling~Head sampling|起點採樣未看到後續全部結果。~Head decisions lack future outcomes.|比較隨機與錯誤策略需求。~Compare random and error-policy needs.
Tail sampling~Tail sampling|尾部採樣需等待與緩衝 trace。~Tail decisions require trace waits/buffers.|估算延遲 trace 的儲存。~Estimate delayed-trace storage.
採樣權重~Sampling weights|採樣統計需保留選取概率。~Sampled statistics need selection probabilities.|比較無權與加權估計。~Compare unweighted and weighted estimates.
批次與回壓~Batching and backpressure|Collector 可能丟棄或積壓資料。~Collectors may drop or backlog data.|核對緩衝滿載行為。~Audit full-buffer behavior.
資料容量~Data volume|span 數與大小共同決定原始量。~Span count and size determine raw volume.|重算本課 40 MB/s。~Recalculate the 40 MB/s example.
SLO 錯誤預算~SLO error budgets|預算需繫結指定時間與有效事件。~Budgets bind windows and eligible events.|對假想 SLI 重算消耗。~Recalculate consumption from fictional SLIs.
隱私與保存~Privacy and retention|紀錄不能無限制收集敏感輸入。~Telemetry must not freely collect sensitive inputs.|分類敏感欄位與保存期。~Classify sensitive fields and retention.
根因證據~Causal evidence|關聯不等於獨立因果證明。~Correlation does not establish independent causality.|列出兩個可反駁假說。~List two falsifiable hypotheses.
''','頭部採樣可以預先保證留下所有未來錯誤。~Head sampling guarantees retaining every future error.|Trace 時間相近就證明唯一根因。~Nearby trace times prove a unique root cause.',[(324,'代理可提供服務呼叫證據~Proxies supply service-call evidence','觀測結果不自動改變流量與授權政策~Telemetry does not automatically change traffic/authorization policy'),(330,'使用者成功率與錯誤預算相通~User success and error budgets transfer','網站可用率定義不能只看 collector 存活~Website availability is not collector liveness')], 'lf')

add(326,'隔離建置、證據與受控部署~Isolated builds, evidence and controlled deployment','原始碼與觸發~Sources and triggers|建置與驗證~Build and validation|身分與發布~Identity and release|部署與回復~Deployment and rollback','ci slsa',
'假設串列工作 2、8、6、4 min，總 20 min；若 8 與 6 min 可獨立平行，關鍵路徑=2+max(8,6)+4=14 min。兩工作不得共享可變 workspace；runner 成本仍約 20 worker-min。~Assume serial jobs of 2, 8, 6 and 4 min: 20 min. Independent parallel 8/6 min jobs give a 14 min critical path. They must not share mutable workspaces; total worker time remains about 20 worker-min.', '''
觸發邊界~Trigger boundaries|外部 PR 代碼與發佈信任等級不同。~External PR code and releases have different trust levels.|分類事件可取用的權限。~Classify permissions available to events.
原始碼繫結~Source binding|建置應繫結不可變的原始碼版本。~Builds bind immutable source versions.|核對 commit 與 artifact metadata。~Match commits and artifact metadata.
依賴鎖定~Dependency locking|可變標籤可能改變依賴內容。~Mutable tags can change dependency content.|比較完整版本與移動標籤。~Compare pinned revisions and moving tags.
乾淨環境~Clean environments|上一次工作殘留可影響下一次產物。~Prior-job residue can affect artifacts.|比較乾淨與汙染假想環境。~Compare clean and contaminated environments.
DAG 工作圖~Job DAG|獨立工作才能安全平行。~Only independent jobs safely parallelize.|重算本課 14 min 關鍵路徑。~Recalculate the 14 min critical path.
測試分層~Test layers|單元與整合測試涵蓋不同邊界。~Unit/integration tests cover different boundaries.|建立功能與系統契約對應。~Map functions to system contracts.
快取政策~Cache policy|快取需繫結依賴版本及信任範圍。~Caches bind dependencies and trust scope.|比較受信與外部工作緩存。~Compare trusted and external-job caches.
產物完整性~Artifact integrity|驗收的產物應等於發布的產物。~Accepted artifacts must equal released artifacts.|比對測試與發佈摘要。~Compare test and release digests.
短效身分~Short-lived identity|短效憑證仍需限制 audience 與權限。~Short-lived credentials still need audience/privilege limits.|列出 job 可申請的操作。~List job-authorized operations.
最小權限~Least privilege|建置與部署不必具有相同權限。~Build and deployment need different privileges.|畫只讀與發布權限矩陣。~Draw read-only/release rights matrices.
秘密遮蔽~Secret redaction|文字遮蔽不保證所有變形秘密被遮蔽。~Text masking may miss transformed secrets.|核對假想 base64 與拆分輸出。~Audit fictional base64/split outputs.
發布證據~Release evidence|Provenance 記錄來源與建置流程。~Provenance records source and build process.|核對主張與可驗證證據。~Compare claims and verifiable evidence.
部署批准~Deployment approval|批准需繫結審核過的確定產物。~Approval binds a reviewed artifact.|建立批准後產物變更反例。~Construct post-approval artifact-change cases.
Canary~Canary|少量流量測試需明訂回退條件。~Limited traffic tests need rollback criteria.|對錯誤率設定假想停止條件。~Set modeled error-based stop criteria.
Rollback~Rollback|回退程式仍需相容資料 schema。~Code rollback still needs schema compatibility.|比較前後版本資料契約。~Compare old/new data contracts.
證據保存~Evidence retention|紀錄需保存來源、結果與責任人。~Records retain sources, results and owners.|建立從 PR 到部署的索引。~Index PR-to-deployment evidence.
''','秘密遮蔽會可靠移除所有編碼變形。~Secret masking reliably removes every encoded transformation.|快取命中就可略過依賴與來源驗證。~Cache hits permit skipping dependency/source verification.',[(327,'不可變工具鏈及輸入繫結共用~Immutable toolchains and input binding transfer','CI 通過不等於跨環境位元可重現~Passing CI does not establish cross-environment reproducibility'),(328,'產物身分與發布證據相連~Artifact identity connects to release evidence','Provenance 與簽章消費者驗證是不同步驟~Provenance and consumer signature validation are distinct')], 'lf')

add(327,'確定輸入、位元重現與差異診斷~Defined inputs, byte reproducibility and difference diagnosis','建置輸入契約~Build-input contracts|非確定性來源~Nondeterminism sources|隔離與比對~Isolation and comparison|來源與重現證據~Source and reproduction evidence','repro epoch zipformat',
'ZIP 基本 DOS 時間欄位只有 2 s 精度：同分鐘 0 s 與 1 s 可能編碼相同，0 s 與 2 s 才改變該欄位；額外時間欄位可有不同精度。必須比較實際編碼的 metadata，不能宣稱邏輯時間差 1 s 必然改變包摘要。固定檔案清單、順序、工具版本與正規化時間後比較位元。128 MiB 在假設 256 MiB/s 下雜湊約 0.5 s。~ZIP basic DOS time fields have 2 s precision: seconds 0 and 1 in one minute may encode identically, whereas 0 and 2 change that field; extra timestamp fields may use other precision. Compare encoded metadata rather than claiming every logical 1 s change alters the archive digest. Match manifests, order, tool versions and normalized times for byte comparison. Hashing 128 MiB at assumed 256 MiB/s takes 0.5 s.', '''
重現定義~Reproduction definition|相同程式行為不等於相同位元。~Equivalent behavior differs from byte identity.|比較語義與位元驗收。~Compare semantic and byte acceptance.
輸入清單~Input manifests|原始碼以外的工具與設定也是輸入。~Tools/settings are inputs beyond source code.|列出所有顯式和隱含輸入。~List explicit and implicit inputs.
版本固定~Version pinning|版本名稱應繫結不可變內容。~Version labels bind immutable content.|核對套件版本與摘要。~Match package versions and digests.
建置規格~Build specifications|環境資訊需足以重建而非只說明 OS。~Environment records must enable rebuilding, not just name an OS.|建立最小可重現環境表。~Build a minimal reproduction environment table.
時間戳~Timestamps|目前時間可進入壓縮包與二進位。~Current time can enter archives/binaries.|追蹤 timestamp 傳入產物。~Trace timestamp entry into artifacts.
SOURCE_DATE_EPOCH~SOURCE_DATE_EPOCH|固定來源時間需被工具正確採用。~Tools must actually honor the fixed source time.|比較支持與忽略該值的模型。~Compare honoring/ignoring tools.
路徑汙染~Path contamination|絕對路徑可能嵌入除錯資訊。~Absolute paths may enter debug information.|比較兩個假想工作根目錄。~Compare two modeled workspace roots.
Locale~Locale|語系改變排序、格式與字元處理。~Locales change ordering, formatting and characters.|比較明確與默認 locale。~Compare explicit/default locales.
檔案順序~File order|檔案列舉順序可能不是固定。~File enumeration order may be unstable.|重排輸入再核對輸出。~Shuffle inputs and compare outputs.
亂數種子~Random seeds|固定種子需涵蓋實際亂數來源。~Seeds must cover actual randomness sources.|列出沒有固定的 generator。~List unpinned generators.
平行排程~Parallel schedules|競爭完成順序可影響產物排列。~Completion races can affect artifact order.|比較不同 worker 數。~Compare different worker counts.
網路輸入~Network inputs|建置期即時下載可能引入變更。~Build-time downloads can introduce changes.|改用已驗證的離線清單模型。~Model verified offline manifests.
獨立建置~Independent builds|獨立環境增加對非確定性檢驗。~Independent environments test nondeterminism.|比較兩環境原始摘要。~Compare raw digests across two environments.
差異定位~Difference diagnosis|整包不同需展開找最小差異。~Bundle mismatch needs minimal-difference diagnosis.|區分內容、metadata 與壓縮差異。~Separate content, metadata and compression differences.
雜湊時間~Hashing time|雜湊核對成本與包大小相關。~Hashing cost scales with bundle size.|重算本課 0.5 s 模型。~Recalculate the 0.5 s model.
證據邊界~Evidence boundaries|重現不能證明原始碼沒有惡意。~Reproducibility does not prove benign source code.|分開內容審查與位元證據。~Separate source review and byte evidence.
''','兩包可重現就可證明原始碼無惡意。~Reproducible bundles prove the source is benign.|相同原始碼即可忽略工具鏈和時間差異。~Identical source makes toolchain/time differences irrelevant.',[(326,'版本與產物摘要可串接 CI 證據~Versions/digests connect to CI evidence','可重現要求跨建置位元一致，CI 可只有單次測試~Reproduction needs byte equality across builds; CI may test once'),(328,'雜湊身分與可信來源可互補~Digest identity and source trust complement','重現證明一致，簽章證明指定身分授權~Reproduction proves equality; signatures prove identity authorization')], 'lf')

add(328,'簽章政策、provenance 與安全更新~Signature policy, provenance and secure updates','內容與信任政策~Content and trust policy|身分與證據~Identity and evidence|更新與新鮮度~Updates and freshness|消費者驗收~Consumer acceptance','sigstore tuf',
'假想更新 metadata 門檻為 2-of-3 金鑰，單一有效簽章不滿足政策；三把中的任兩把才滿足門檻。若 metadata 到期 24 h，即使簽章正確，過期後仍需依政策拒絕，不是永久信任。~For fictional 2-of-3 metadata keys, one valid signature fails policy and any two satisfy the threshold. With 24 h expiry, valid signatures do not establish freshness after expiry.', '''
內容摘要~Content digests|摘要識別特定位元而非作者身分。~Digests identify bytes, not author identity.|核對來源聲明與摘要差別。~Compare origin claims and digests.
簽章契約~Signature contracts|簽章需驗證算法、內容與信任金鑰。~Verification checks algorithm, bytes and trusted key.|用測試金鑰核對不同內容。~Check different content with test keys.
消費者政策~Consumer policy|有效簽章不等於所有消費者接受。~Valid signatures need not satisfy all consumer policies.|比較不同 signer allowlist。~Compare signer allowlists.
Artifact 繫結~Artifact binding|簽章應繫結完整指定產物。~Signatures bind the exact artifact.|檢查 tag 移動後的摘要。~Check digest after tag movement.
Keyless 身分~Keyless identity|無長期金鑰仍需 issuer 與身分驗證。~Keyless flows still verify issuers and identities.|核對虛構 issuer/subject 組合。~Audit fictional issuer/subject combinations.
透明紀錄~Transparency logs|紀錄提供可查證 inclusion，不替代授權。~Logs establish inclusion, not authorization.|分開 inclusion 與 trust 判斷。~Separate inclusion and trust decisions.
Provenance~Provenance|建置證據需對應產物及 builder。~Build evidence binds artifact and builder.|核對來源、參數與產物。~Check source, parameters and artifacts.
SBOM~SBOM|成分清單不等於漏洞全已排除。~Component lists do not establish absence of vulnerabilities.|比較成分完整與風險審查。~Compare inventory completeness and risk review.
角色分離~Role separation|Root、targets 與時間角色責任不同。~Root, target and timestamp roles differ.|畫更新 metadata 的權限圖。~Draw update-metadata authority graphs.
簽章門檻~Signature thresholds|接受門檻需由可信政策指定。~Trusted policy defines acceptance thresholds.|核算本課 2-of-3 案例。~Audit the 2-of-3 example.
Metadata 新鮮~Metadata freshness|有效簽章不能消除過期與凍結風險。~Valid signatures do not remove expiry/freeze risks.|比較未到期與過期 metadata。~Compare fresh/expired metadata.
回退抵抗~Rollback resistance|新版本應抵抗低版本合法資料替換。~Updates resist replacement by valid older metadata.|模擬低版本回退判讀。~Model lower-version rollback decisions.
金鑰輪替~Key rotation|輪替需由舊信任授權新信任。~Old trust authorizes new trust during rotation.|核對舊新門檻交接。~Audit old/new threshold handoff.
離線驗證~Offline verification|離線包需帶足合法驗證證據。~Offline bundles need sufficient valid evidence.|列出簽章、chain 與政策。~List signatures, chains and policy.
拒絕用例~Rejection cases|驗證需測錯身分與修改內容。~Verification tests wrong identity and changed content.|製作全部虛構負向用例。~Create fictional negative cases.
發布追溯~Release traceability|發布證據需可回溯到來源審查。~Release evidence traces back to source review.|建立 digest 到 review 的索引。~Index digests to reviews.
''','透明日誌的存在就代表網站授權該 signer。~A transparency entry means the site authorized the signer.|有效簽章讓 metadata 永遠不會過期。~Valid signatures make metadata never expire.',[(310,'信任根、回退與更新驗證共用~Trust roots, rollback and update checks transfer','套件配送可信不等於硬體啟動鏈可信~Trusted package delivery differs from trusted hardware boot'),(327,'可重現產物與簽章摘要相連~Reproducible artifacts connect to signed digests','簽章不要求建置可重現，重現不證明發布授權~Signatures need not imply reproducibility; reproduction does not prove release authority')], 'lf')

add(329,'RPO、RTO 與獨立還原證據~RPO, RTO and independent restore evidence','業務目標與範圍~Business goals and scope|備份與日誌~Backups and logs|還原與切換~Restore and failover|演練與治理~Exercises and governance','pitr controls',
'假設 2 TB 十進位基底以持續 400 MB/s 還原，純資料搬移下界=5000 s≈83.3 min；需重播 120 GB 日誌、200 MB/s 約 10 min，串列合計至少 93.3 min，未含驗證、配置及索引。~Restoring assumed 2 decimal TB at sustained 400 MB/s takes at least 5000 s≈83.3 min. Replaying 120 GB logs at 200 MB/s adds 10 min serially, for at least 93.3 min excluding checks, setup and indexes.', '''
RPO~RPO|可容忍資料損失需用時間或事件界定。~Tolerable loss needs time/event boundaries.|標出最後可恢復提交點。~Mark the last recoverable commit.
RTO~RTO|恢復時間需包含驗收與服務重啟。~Recovery time includes validation and restart.|列出完整恢復路徑。~List the full recovery path.
業務優先~Business priorities|依賴服務的恢復順序影響可用性。~Dependency recovery order affects availability.|畫 DNS、身分與資料依賴。~Draw DNS, identity and data dependencies.
故障範圍~Failure scope|磁碟、帳號與區域失效不同。~Disk, account and regional failures differ.|建立三類演練情境。~Build three exercise scenarios.
基底備份~Base backups|一致基底須與後續日誌相容。~Consistent bases must match later logs.|核對快照與 WAL 起點。~Match snapshots and WAL starting points.
日誌保存~Log retention|缺少一段日誌可破壞 PITR 鏈。~Missing logs can break PITR continuity.|比較完整與缺段序列。~Compare complete and incomplete log sequences.
獨立副本~Independent copies|同帳號線上副本可共用管理失誤。~Same-account copies can share administrative mistakes.|標示不同信任與故障域。~Mark distinct trust/failure domains.
加密金鑰~Encryption keys|有備份但失去金鑰仍不能還原。~Backups without keys may be unrestorable.|演練虛構金鑰取得政策。~Model fictional key-access policies.
還原環境~Restore environment|演練需避免覆寫生產資料。~Exercises avoid overwriting production data.|使用虛構資料與隔離名稱。~Use fictional data and isolated names.
時點選擇~Target time|復原目標需在壞操作前且業務一致。~Targets precede bad operations and preserve business consistency.|比較兩個假想提交時點。~Compare two fictional commit points.
日誌重播~Log replay|資料重播需核對 timeline 與順序。~Replay checks timelines and ordering.|列出可用與不可接續段。~List continuous/discontinuous segments.
完整性驗收~Integrity acceptance|檔案可開啟不代表業務資料完整。~Openable files do not establish business integrity.|比對筆數、摘要與不變量。~Compare counts, digests and invariants.
搬移成本~Transfer costs|可持續速率而非峰值決定下界。~Sustained rates determine lower bounds.|核算本課 93.3 min 下界。~Audit the 93.3 min lower bound.
切換授權~Failover authorization|服務切換需避免雙主寫入。~Failover avoids concurrent writable primaries.|畫停止、fencing 與接手。~Draw stop, fencing and takeover.
演練紀錄~Exercise records|RTO 實測要保留各階段時間。~Measured RTO retains stage times.|記錄準備、恢復與驗收。~Record setup, recovery and acceptance.
修正閉環~Remediation loop|演練缺口需責任、期限及再測。~Gaps need owners, deadlines and retests.|建立假想問題追蹤表。~Build a modeled issue tracker.
''','備份工作成功就證明 RTO 已達成。~Successful backup jobs prove RTO compliance.|資料有副本就不需保存解密金鑰。~Data replicas remove the need to retain decryption keys.',[(318,'WAL 與交易不變量提供還原依據~WAL and transaction invariants support restoration','交易正常提交不等於跨區還原可用~Normal commits do not establish cross-region restorability'),(330,'切換與故障域分析相通~Failover and failure-domain analysis transfer','高可用服務副本不能替代獨立歷史備份~HA service replicas do not replace independent historical backups')], 'nist')

add(330,'SLO、失效域與有限容量網站~SLOs, failure domains and finite-capacity websites','服務與失效契約~Service and failure contracts|容量與過載~Capacity and overload|冗餘與切換~Redundancy and failover|驗收與成本~Acceptance and cost','availability overload',
'30 天共 43,200 min，99.9% 可用率的時間型錯誤預算=43.2 min。假設兩元件獨立且皆 99.9%，串列 A=0.999²=99.8001%；備援才可用 1−(1−A)²，獨立假設常不成立。~Thirty days contain 43,200 min; 99.9% time availability permits 43.2 min. Two independent 99.9% components in series yield 99.8001%; redundancy uses 1−(1−A)² only when independence assumptions apply.', '''
使用者路徑~User paths|首頁存活不代表所有關鍵操作成功。~A live homepage does not establish critical-operation success.|畫登入、讀取與寫入路徑。~Draw login, read and write paths.
SLI~SLIs|有效事件與成功定義需明列。~Eligible events and success definitions are explicit.|比較時間型與請求型 SLI。~Compare time-based/request-based SLIs.
SLO~SLOs|目標需指定期間與服務範圍。~Objectives specify windows and scope.|定義假想 30 天目標。~Define a fictional 30-day target.
故障域~Failure domains|副本若共用電源或控制則可能共同失效。~Replicas sharing power/control can fail together.|標出共用依賴與獨立部分。~Mark shared and independent dependencies.
排隊模型~Queueing models|接近滿載時排隊延遲會上升。~Queueing grows as utilization approaches saturation.|比較兩種假想負載率。~Compare two assumed utilization levels.
負載均衡~Load balancing|分配需考慮端點容量與就緒。~Distribution considers endpoint capacity/readiness.|比較輪詢與容量加權。~Compare round-robin and capacity weights.
快取策略~Cache policies|快取命中需符合資料新鮮度契約。~Cache hits must meet freshness contracts.|列出允許舊值與需最新值。~List stale-allowed and fresh-required data.
負載卸除~Load shedding|及早拒絕可保護核心成功率。~Early rejection can protect core success rates.|比較限流與無限排隊。~Compare limits and unbounded queues.
多區副本~Multizone replicas|跨區部署仍可共用資料或身分瓶頸。~Zones may still share data/identity bottlenecks.|畫整體依賴而非只畫網頁。~Draw full dependencies, not only frontends.
健康檢查~Health checks|檢查需關聯真正服務能力。~Checks relate to actual service capability.|比較淺層與完整請求檢查。~Compare shallow/full-request checks.
狀態共享~Shared state|無狀態 frontend 仍需外部可靠狀態。~Stateless frontends still need reliable external state.|標出 session 與資料所有權。~Mark session and data ownership.
Failover~Failover|接手容量應可承受剩餘全部工作量。~Takeover capacity carries surviving workload.|檢查 N−1 模型的容量。~Check capacity under an N−1 model.
可用率組合~Availability composition|串列與備援需要不同公式與假設。~Series/redundancy use different formulas and assumptions.|核算本課串列 99.8001%。~Audit the 99.8001% series case.
錯誤預算~Error budgets|預算消耗可由不同失敗方式造成。~Different failure modes consume the budget.|重算本課 43.2 min。~Recalculate the 43.2 min budget.
演練停止~Exercise stop criteria|隔離演練需有固定停止與復原條件。~Isolated exercises have stop/restore criteria.|用虛構流量檢查容量下降。~Check modeled capacity loss with fictional traffic.
成本審查~Cost review|額外副本需比較價值與共同失效限制。~Replicas trade cost against common-failure limits.|比較兩種架構的預算與 SLO。~Compare budgets/SLOs of two architectures.
''','兩個 99.9% 元件串列仍是 99.9%。~Two 99.9% components in series still yield 99.9%.|不同可用區自動排除所有共同失效。~Different zones remove every common failure.',[(329,'故障域、接手與驗收相通~Failure domains, takeover and acceptance transfer','HA 減少中斷，備份恢復歷史資料~HA reduces outages; backups recover history'),(325,'SLI 與使用者結果需可觀測~SLIs and user outcomes require observation','採樣追蹤不能自動當作全量可用率統計~Sampled traces do not automatically represent full availability statistics')], 'google')

add(331,'L2 學習、VLAN 與有限交換容量~L2 learning, VLANs and finite switching capacity','框架與學習~Frames and learning|隔離與環路~Isolation and loops|佇列與交換~Queues and switching|可觀測與驗收~Observation and acceptance','ovs ovslab ovsissues',
'假設 10 Gb/s Ethernet 最小框架 64 B，另計 8 B preamble/SFD 與 12 B IFG，每框架線路佔用 84 B，理想為 10¹⁰/(84×8)≈14.881 Mframes/s；VLAN 與不同框架長度需重算。~At assumed 10 Gb/s, a 64 B minimum frame plus 8 B preamble/SFD and 12 B IFG occupies 84 B: about 14.881 Mframes/s ideal. VLAN and other frame sizes need recalculation.', '''
框架欄位~Frame fields|來源與目的 MAC 屬於框架而非 IP 路由。~Source/destination MACs belong to frames, not IP routes.|分類 L2 與 L3 位址。~Classify L2 and L3 addresses.
FCS~FCS|框架檢查碼偵測傳輸錯誤而非授權。~Frame checks detect errors, not authorization.|區分損壞與未授權框架。~Separate damaged/unauthorized frames.
MAC 學習~MAC learning|交換器以來源位址更新轉送表。~Switches learn forwarding entries from source addresses.|模擬三框架表格更新。~Model table updates for three frames.
Unknown flooding~Unknown flooding|未知單播可在允許域內泛洪。~Unknown unicast may flood within permitted domains.|核對 ingress 與其他 port。~Check ingress and other ports.
VLAN 分域~VLAN domains|VLAN 分離廣播域但不是完整授權。~VLANs separate broadcasts, not complete authorization.|畫兩 VLAN 的流量邊界。~Draw two-VLAN traffic boundaries.
Tagged trunk~Tagged trunks|標籤與埠規則需一致解讀。~Tags and port rules require consistent interpretation.|比較 access 與 trunk 模型。~Compare access and trunk models.
環路風險~Loop risks|L2 環路可持續複製泛洪框架。~L2 loops can keep replicating flooded frames.|紙上追蹤三交換器環路。~Trace a three-switch loop on paper.
Spanning tree~Spanning trees|阻擋部分路徑避免活動拓撲成環。~Blocking paths prevents active topology cycles.|比較物理圖與轉送樹。~Compare physical topology and forwarding tree.
交換容量~Switching capacity|埠速率和內部容量都可能限制吞吐。~Ports and internal fabric both limit throughput.|核對全雙工計數定義。~Check full-duplex counting conventions.
隊頭阻塞~Head-of-line blocking|單一隊頭可能阻擋其他可送框架。~One head may block other feasible frames.|比較單隊列與目的地隊列。~Compare single and destination queues.
Buffer 預算~Buffer budgets|緩衝吸收突發而非創造持續頻寬。~Buffers absorb bursts, not create bandwidth.|計算不同突發累積量。~Calculate burst backlog volumes.
QoS 排程~QoS scheduling|優先權可降低特定延遲卻可能飢餓他流。~Priority reduces selected latency but may starve others.|比較嚴格優先與加權。~Compare strict priority and weights.
最小框架率~Minimum-frame rates|小框架耗用固定線路 overhead。~Small frames pay fixed wire overhead.|重算本課 14.881 Mframes/s。~Recalculate 14.881 Mframes/s.
Port 計數~Port counters|byte、frame 與 drop 定義需核對。~Byte/frame/drop counters need defined scope.|配對發送、接收與丟棄。~Match transmitted, received and dropped counts.
Link 聚合~Link aggregation|單一流未必用滿多條鏈路。~One flow may not fill all aggregated links.|比較多流與單流 hash。~Compare single/multiflow hashing.
隔離驗收~Isolation acceptance|正向可通與負向拒絕均需測試。~Allowed and denied paths both need testing.|用虛構框架檢查 VLAN 規則。~Check VLAN rules with fictional frames.
''','VLAN 是所有應用授權的充分證據。~VLAN membership proves all application authorization.|緩衝增加就能長期突破出口頻寬。~More buffers permanently exceed egress bandwidth.',[(332,'有限 buffer、轉送表與線路成本相通~Buffers, tables and wire costs transfer','交換器學 MAC，路由器以最長前綴選 IP 下一跳~Switches learn MACs; routers choose IP next hops by prefix'),(333,'交換政策可由控制器下發~Controllers can install switching policies','L2 學習與 OpenFlow 明確規則是不同控制機制~L2 learning and explicit OpenFlow rules differ')], 'lf')

add(332,'最長前綴、轉送管線與流量計量~Longest prefixes, forwarding pipelines and traffic accounting','封包與查表~Packets and lookup|處理管線與佇列~Pipelines and queues|控制與一致更新~Control and consistent updates|性能與正確性~Performance and correctness','router ovs',
'假設路由有 10.0.0.0/8 → A、10.1.0.0/16 → B、10.1.2.0/24 → C；10.1.2.3 選 C（最長前綴），不是 metric 最小跨所有前綴。1 Gb/s 發送 1500 B 封包的純 serialization 為 12 µs，未含 L2 overhead。~Routes 10.0.0.0/8→A, 10.1.0.0/16→B and 10.1.2.0/24→C send 10.1.2.3 to C by longest prefix, not a global metric minimum. Serializing 1500 B at 1 Gb/s takes 12 µs excluding L2 overhead.', '''
RIB 與 FIB~RIB and FIB|控制路由資料與實際轉送表不同。~Control routes differ from actual forwarding tables.|核對路由選擇到 FIB 安裝。~Audit route selection to FIB installation.
Prefix 選擇~Prefix selection|最長匹配前綴優先於較短前綴。~Longest matching prefixes precede shorter ones.|重算本課三個前綴。~Recalculate the three-prefix example.
Parser~Parsers|封包解析必須檢查長度與格式。~Parsing checks packet lengths and format.|分類完整與截斷虛構封包。~Classify complete/truncated fictional packets.
本地遞送~Local delivery|目的本機與需要轉送是不同路徑。~Local delivery differs from forwarding.|畫兩條目的地處理路徑。~Draw two destination-processing paths.
TTL~TTL|轉送需更新存活限制並處理到期。~Forwarding updates lifetime and handles expiry.|模擬 TTL=1 與 TTL=2。~Model TTL=1 and TTL=2.
標頭檢查~Header checks|修改 IPv4 標頭需維持 checksum 一致。~Changed IPv4 headers need consistent checksums.|核對更新前後標頭欄位。~Audit fields before/after changes.
MTU~MTUs|出口 MTU 可能小於輸入封包。~Egress MTU may be smaller than input packets.|比較允許片段與禁止片段。~Compare fragmentable/nonfragmentable cases.
Neighbor 解決~Neighbor resolution|下一跳 IP 需對應可用鏈路資訊。~Next-hop IP needs usable link information.|比較路由存在但鄰居未知。~Model a route with an unknown neighbor.
Fast path~Fast paths|常見轉送與例外慢路徑需分離。~Common forwarding and exceptions differ.|分類 TTL 到期與正常轉送。~Classify expired/normal forwarding.
ECMP~ECMP|等價下一跳通常按流分配。~Equal-cost next hops commonly hash flows.|比較單流與多流分佈。~Compare single/multiflow distribution.
ACL 順序~ACL ordering|重疊規則的優先權會改變結果。~Overlapping-rule priority changes outcomes.|核對接受與拒絕順序。~Audit accept/deny ordering.
Queue 管理~Queue management|出口壅塞造成排隊或丟棄。~Congested egress creates queues or drops.|比較入出口持續數據率。~Compare sustained ingress/egress rates.
表格更新~Table updates|更新期間需避免不一致的部分狀態。~Updates avoid inconsistent partial state.|畫兩路由一起更新的時程。~Draw timing for two-route updates.
線速預算~Line-rate budgets|封包大小影響每秒封包與處理預算。~Size affects packet rate and processing budgets.|核算本課 12 µs serialization。~Audit the 12 µs serialization.
Counter 範圍~Counter scope|成功查表不等於成功線路輸出。~Successful lookup does not prove wire delivery.|配對查表、丟棄與傳送數。~Match lookup, drop and transmit counts.
驗收向量~Acceptance vectors|查表邊界、錯格式與禁止流都需檢查。~Prefix edges, malformed and denied flows need checks.|建立純離線封包向量。~Build offline-only packet vectors.
''','路由選擇在所有匹配前綴中只看最小 metric。~Routing chooses only the smallest metric across matching prefixes.|查表成功證明封包已送到最終目的地。~Lookup success proves delivery to the final destination.',[(331,'封包緩衝與轉送證據共用~Buffering and forwarding evidence transfer','路由改 IP 層存活限制，L2 交換不執行同一查表契約~Routing updates IP lifetimes; L2 switching has a different lookup contract'),(334,'下一跳與 MTU 判讀可沿用~Next-hop and MTU analysis transfer','IPv6 標頭、鄰居探索及片段規則需另查~IPv6 headers, discovery and fragmentation require rechecking')], 'lf')

add(333,'控制平面、流表與分散政策一致性~Control planes, flow tables and distributed policy consistency','控制圖與南向介面~Control graph and southbound interfaces|規則與政策編譯~Rules and policy compilation|分散更新與故障~Distributed updates and failures|驗收與防禦治理~Acceptance and defensive governance','openflow onos',
'假設 100 個交換器、每個 2000 個規則，總 200,000 entries。若更新 5% 且每 rule message 假想 120 B，純更新 payload=1.2 MB，未含 TLS、確認及回報；table 容量仍需逐設備驗證。~Assume 100 switches with 2000 rules each: 200,000 entries. Updating 5% with fictional 120 B/rule messages gives 1.2 MB payload, excluding TLS, acknowledgments and reports; capacity needs per-device checks.', '''
平面分離~Plane separation|控制決策與封包轉送執行可分離。~Control decisions and packet execution can be separated.|畫管理、控制與資料三層。~Draw management/control/data layers.
南向契約~Southbound contracts|控制器與裝置須同意協定及能力。~Controllers/devices agree on protocols/capabilities.|核對版本與可用功能。~Check versions and capabilities.
拓撲證據~Topology evidence|觀測到的鏈路需記錄時效與來源。~Observed links record freshness and source.|比較過期與最新拓撲。~Compare stale and fresh topology.
控制身分~Control identity|南向授權需限制可改動哪些裝置。~Southbound authority limits devices/actions.|建立裝置與控制角色矩陣。~Build device/control-role matrices.
Match/action~Match/action|欄位匹配後依序套用合法動作。~Matches select ordered valid actions.|用虛構框架追蹤動作。~Trace actions on fictional frames.
規則優先~Rule priority|重疊規則需明定優先及 fallback。~Overlaps need priority and fallback.|比較特定與一般規則。~Compare specific/general rules.
Table pipeline~Table pipelines|跨表 goto 與 metadata 形成資料管線。~Goto/metadata create cross-table pipelines.|畫三表的封包狀態。~Draw packet state across three tables.
Miss 政策~Miss policy|未命中處理影響負載與拒絕行為。~Miss handling affects load and denial behavior.|比較丟棄與控制器處理。~Compare drop/controller handling.
意圖轉換~Intent compilation|高階意圖需轉為可驗證裝置規則。~Intents compile to verifiable device rules.|核對意圖與具體允許路徑。~Match intent and permitted paths.
多裝置更新~Multidevice updates|單裝置成功不代表全網一致。~Single-device success does not establish network consistency.|枚舉更新順序與暫態路徑。~Enumerate update order/transient paths.
Barrier~Barriers|順序屏障與多交換器原子性不同。~Ordering barriers differ from multiswitch atomicity.|區分單連線與全網證據。~Separate connection/network evidence.
規則期限~Rule lifetimes|Idle/hard timeout 有不同清除時機。~Idle/hard timeouts expire differently.|模擬持續與閒置流量。~Model active and idle traffic.
控制器 HA~Controller HA|多實例仍需一致狀態與裝置擁有權。~Replicas need consistent state/device ownership.|畫主控切換與重複命令。~Draw takeover and duplicate commands.
失聯政策~Disconnection policy|控制失聯時需明定留存與拒絕。~Disconnection defines retention/denial behavior.|比較 fail-safe 與既有規則。~Compare fail-safe and retained-rule behavior.
更新量~Update volume|設備與規則數決定控制交通下界。~Device/rule counts bound control traffic below.|核算本課 1.2 MB payload。~Audit the 1.2 MB payload example.
離線驗收~Offline acceptance|需檢查可達、禁止與無環路條件。~Tests check reachability, denial and loop freedom.|用虛構 topology 做政策判讀。~Review policy on fictional topology.
''','Barrier 可讓全部交換器同時原子更新。~Barriers make every switch update atomically together.|多控制器自動保證狀態與裝置擁有權一致。~Multiple controllers automatically ensure state/ownership consistency.',[(331,'流表與框架動作對應交換行為~Flow rules and frame actions map to switching','控制器政策不同於自動 MAC 學習~Controller policy differs from automatic MAC learning'),(319,'分散控制狀態需要一致性~Distributed control state needs consistency','共識日誌提交不證明設備已安裝規則~Consensus log commit does not prove device rule installation')], 'lf')

add(334,'位址規劃、鄰居探索與雙棧驗收~Address planning, neighbor discovery and dual-stack acceptance','位址與範圍~Addresses and scope|鄰居與自動配置~Neighbors and autoconfiguration|路由與 MTU~Routing and MTU|防禦與雙棧驗收~Defense and dual-stack acceptance','ipv6 nd slaac',
'假設分配 /48，每子網 /64，可有 2^(64−48)=65,536 個 /64 子網；不是主機數。單一 /64 理論含 2^64 個位址，但可用與配置受保留、介面及政策限制。IPv6 最小鏈路 MTU=1280 B，不能與 TCP payload 混同。~A /48 split into /64 yields 65,536 subnets, not hosts. A /64 contains 2^64 theoretical addresses, with use constrained by reservations/interfaces/policy. IPv6 minimum link MTU is 1280 B, not TCP payload.', '''
位址長度~Address length|IPv6 位址為 128-bit 且前綴定義網路。~IPv6 addresses have 128 bits and network prefixes.|展開壓縮表示並核對位數。~Expand compressed notation and check width.
位址範圍~Address scopes|Link-local 與 global 有不同可達邊界。~Link-local/global scopes differ in reachability.|標示跨鏈路可用性。~Mark cross-link usability.
前綴規劃~Prefix planning|父子前綴需避免非預期重疊。~Parent/child prefixes avoid unintended overlap.|核算本課 /48 到 /64。~Audit /48-to-/64 allocation.
介面識別~Interface identifiers|介面 ID 政策與 MAC 綁定不是唯一選擇。~Interface IDs need not always bind MACs.|比較穩定與暫時識別。~Compare stable/temporary identifiers.
Router discovery~Router discovery|路由器通告傳遞配置資訊與期限。~Advertisements convey configuration and lifetimes.|核對 prefix 與 default router。~Check prefixes and default routers.
SLAAC~SLAAC|自動配置依賴有效前綴與本地政策。~Autoconfiguration uses valid prefixes/local policy.|追蹤地址建立與到期。~Trace creation and expiry.
DAD~DAD|重複位址偵測需解讀鏈路上的回應。~Duplicate detection interprets link responses.|比較重複與無回應模型。~Compare duplicates/no-response models.
鄰居快取~Neighbor caches|鄰居狀態不同於路由表存在。~Neighbor state differs from route existence.|畫 reachable 到 stale 的轉移。~Draw reachable-to-stale transitions.
ICMPv6~ICMPv6|必要控制訊息不能一概全部拒絕。~Necessary control messages cannot all be indiscriminately denied.|分類錯誤與探索訊息。~Classify error/discovery messages.
Path MTU~Path MTU|端點依路徑資訊選擇合適大小。~Endpoints size packets from path information.|比較正常與遺失 too-big 回應。~Compare valid/lost too-big responses.
Fragmentation~Fragmentation|IPv6 路由器不進行一般 IPv4 式分片。~IPv6 routers do not perform ordinary IPv4-style fragmentation.|區分來源與路由器角色。~Separate source/router roles.
Extension headers~Extension headers|擴充標頭需按規格與政策處理。~Extension headers follow specifications/policy.|檢查長度與鏈結合法性。~Check length/chain validity.
雙棧政策~Dual-stack policies|IPv4 防禦規則不自動涵蓋 IPv6。~IPv4 defenses do not automatically cover IPv6.|建立兩棧一致允許矩陣。~Build a two-stack permission matrix.
DNS 與連線~DNS and connections|AAAA 存在不保證端到端可達。~AAAA records do not guarantee reachability.|比較解析成功與連接成功。~Compare resolution/connection success.
前綴變更~Renumbering|新舊位址期限需銜接既有連線。~Renumbering lifetimes connect to existing sessions.|畫 preferred 與 valid 期限。~Draw preferred/valid lifetimes.
驗收矩陣~Acceptance matrix|位址、MTU、政策及失效需分項檢查。~Addresses, MTUs, policies and failures need separate checks.|用純離線範例建立測試表。~Build checks from offline-only examples.
''','IPv4 ACL 自動覆蓋相同服務的 IPv6。~IPv4 ACLs automatically cover the same IPv6 services.|/48 分成 /64 的 65,536 數字是主機數。~65,536 from /48-to-/64 subdivision counts hosts.',[(332,'查表、下一跳與 MTU 分析相通~Lookup, next hops and MTU analysis transfer','IPv6 無基底標頭 checksum 且鄰居機制不同~IPv6 has no base-header checksum and different discovery'),('cybersecurity','雙棧政策與資產盤點需要一致~Dual-stack policies and asset inventory need consistency','IPv6 配置成功不等於身份授權與防禦完整~Working IPv6 does not establish complete identity/defense')], 'lf')

PLACES={
 'nist':{'name':'NIST 蓋瑟斯堡校區','nameEn':'NIST Gaithersburg campus','city':'蓋瑟斯堡','cityEn':'Gaithersburg','lat':39.133,'lng':-77.220,'address':'100 Bureau Drive, Gaithersburg, MD 20899, USA','source':'zt','kind':'官方標準機構的代表校區，非本課現場實驗室','kindEn':'Representative standards-institution campus, not this course’s onsite laboratory'},
 'nvidia':{'name':'NVIDIA 公開總部','nameEn':'NVIDIA public headquarters','city':'聖塔克拉拉','cityEn':'Santa Clara','lat':37.370,'lng':-121.965,'address':'2788 San Tomas Expressway, Santa Clara, CA 95051, USA','source':'nvidiaaddress','kind':'官方企業總部代表點，非晶片製造廠','kindEn':'Official headquarters reference, not a chip factory'},
 'amd':{'name':'AMD 公開辦公室代表點','nameEn':'AMD public office reference','city':'聖塔克拉拉','cityEn':'Santa Clara','lat':37.383,'lng':-121.971,'address':'2485 Augustine Drive, Santa Clara, CA 95054, USA','source':'amdaddress','kind':'公開企業地址代表點，非本課 FPGA 實驗現場','kindEn':'Public corporate address reference, not this course’s FPGA lab'},
 'google':{'name':'Googleplex 公開地址代表點','nameEn':'Googleplex public-address reference','city':'山景城','cityEn':'Mountain View','lat':37.422,'lng':-122.084,'address':'1600 Amphitheatre Parkway, Mountain View, CA 94043, USA','source':'googleaddress','kind':'官方辦公室代表點，非公開可進入 TPU 機房','kindEn':'Official office reference, not a publicly accessible TPU facility'},
 'stanford':{'name':'史丹佛大學公開校區代表點','nameEn':'Stanford public campus reference','city':'史丹佛','cityEn':'Stanford','lat':37.4275,'lng':-122.1697,'address':'450 Jane Stanford Way, Stanford, CA 94305, USA','source':'stanfordaddress','kind':'電腦研究與開放教材的代表校區；不是每項技術發明地或該校授權課程','kindEn':'Representative computing-research/open-education campus; not every technology’s birthplace or a university-authorized course'},
 'lf':{'name':'Linux Foundation 公開通訊地址所在城市','nameEn':'Linux Foundation public mailing-address city','city':'威明頓','cityEn':'Wilmington','lat':39.771,'lng':-75.540,'address':'2810 N Church St, PMB 57274, Wilmington, Delaware 19802-4447, USA','source':'lfaddress','kind':'官方公開通訊地址的城市代表點，不代表專案在此開發或可參觀實驗室','kindEn':'City reference for an official mailing address; no claim of project development or visitable laboratories here'}
}

def source_ids(keys): return list(dict.fromkeys(S[k]['id'] for k in keys))
def ref(key):return {k:S[key][k]for k in ['title','titleEn','publisher','url']}
def place_for(cid):
 pl=copy.deepcopy(PLACES[D[cid]['place']]);kind=pl.pop('kind');kindEn=pl.pop('kindEn');pl.pop('source')
 pl.update({'country':'美國','countryEn':'United States','addressEn':pl['address'],'mapQuery':pl['address'],'coordinateScope':kind+'。座標為近似代表點，請以官方地址及地圖查詢為準。','coordinateScopeEn':kindEn+'. Coordinates are approximate references; consult official addresses and map queries.'})
 return pl

def step(cid,d,index,offset,previous):
 unit=d['units'][index//2];(zh,en),(mechanism,mechanismEn),(test,testEn)=unit
 model=index%2==0;sid=f'{cid}-v11-{index+1:02d}';number=offset+index+1
 objective=f'以「{zh}」建立可檢查的架構、原理與驗證依據。' if model else f'用「{test}」檢查「{zh}」的假設、結果及失效邊界。'
 objectiveEn=f'Establish reviewable architecture, principles and evidence for {en.lower()}.' if model else f'Validate assumptions, outcomes and failure boundaries for {en.lower()} using the specified experiment.'
 instruction=(f'先觀看師傅示意，辨識「{zh}」的資料、控制與時間關係。{mechanism} 在離線工作臺畫出元件／資料流，列出輸入、輸出、保存狀態與合法轉移；建立基準與擾動兩種假想情境，寫下可被反駁的預測。以「{test}」設計下一步驗證。記錄版本、單位、未知參數與模型外的行為。' if model else f'重播師傅對「{zh}」的示範，在自己的隔離模型或試算表執行：{test} 核對「{mechanism}」是否成立；保留輸入、預期、實際結果與差異。至少提出兩個競爭原因，選擇一項能區分它們的新增觀察。依事前定義的語義、容量或延遲條件判斷通過／保留，未執行的真實平臺項目不得標為實測。')
 instructionEn=(f'Watch the mentor and identify data, control and timing relationships for {en.lower()}. {mechanismEn} Draw components/data flows offline; specify inputs, outputs, retained state and legal transitions. Build baseline and perturbed hypothetical cases and make a falsifiable prediction. Plan validation using: {testEn} Record versions, units, unknowns and out-of-model behavior.' if model else f'Replay the mentor for {en.lower()} and execute in your own isolated model or worksheet: {testEn} Check the principle: {mechanismEn} Preserve input, expected output, observed output and differences. Propose two competing causes and a discriminating observation. Apply predefined semantic, capacity or latency criteria and mark untested real-platform claims unresolved.')
 correct=mechanism if model else test;correctEn=mechanismEn if model else testEn
 wrong=[x[0]for x in d['bad']];wrongEn=[x[1]for x in d['bad']];answer=index%3
 options=wrong.copy();optionsEn=wrongEn.copy();options.insert(answer,correct);optionsEn.insert(answer,correctEn)
 knowledge=[{'id':sid+'-k1','title':zh+'的原理與邊界','titleEn':en+' principle and boundaries','text':mechanism,'textEn':mechanismEn,'sourceIds':source_ids(d['src'])},{'id':sid+'-k2','title':zh+'的驗證設計','titleEn':en+' validation design','text':test+' 保留基準與擾動的完整輸入／輸出，以語義、容量或時間條件檢查，並明列假想模型未涵蓋的現實因素。','textEn':testEn+' Retain complete inputs/outputs for baseline and perturbation, check semantic/capacity/timing criteria and state real-world factors omitted from the hypothetical model.','sourceIds':source_ids(d['src'])}]
 if index in (0,1,30,31):knowledge.append({'id':sid+'-k3','title':'本課原創量化算例','titleEn':'Original course worked example','text':d['example'][0],'textEn':d['example'][1],'sourceIds':source_ids(d['src']),'authorship':'original-hypothetical-exercise'})
 return {'id':sid,'order':number,'sequence':number,'estimatedMinutes':35,'simulationOnly':True,'sourceIds':source_ids(d['src']),'prerequisiteIds':[previous]if previous else [],'title':zh+('：原理與架構'if model else '：實驗與驗證'),'titleEn':en+(': principles and architecture'if model else ': experiment and validation'),'objective':objective,'objectiveEn':objectiveEn,'instruction':instruction,'instructionEn':instructionEn,'observation':test,'observationEn':testEn,'failure':'常見誤判：'+wrong[index//2%2]+' 本步需分開功能正確、資源上界與證據範圍，不可把假想結果當作真實平臺保證。','failureEn':'Common mistake: '+wrongEn[index//2%2]+' Separate correctness, resource bounds and evidence scope; hypothetical results are not real-platform guarantees.','check':f'提交「{zh}」的'+('兩情境架構／狀態圖、參數表與可反駁預測；標出哪些資料支援「'+mechanism+'」。'if model else '輸入與結果對照、競爭原因、接受／保留理由；逐項說明「'+test+'」的證據與尚未驗證範圍。'),'checkEn':f'Submit {en.lower()} '+('two-case architecture/state diagrams, parameter table and falsifiable prediction; identify evidence supporting the principle.'if model else 'input/output comparisons, competing causes and pass/hold rationale; state evidence and untested scope for the experiment.'),'knowledge':knowledge,'quiz':{'question':f'本步審查「{zh}」與整體「{CAT[cid]["title"]}」時，哪項陳述或驗證有依據？','questionEn':f'When reviewing {en.lower()} within {CAT[cid]["titleEn"].lower()}, which statement or check is supported?','options':options,'optionsEn':optionsEn,'answer':answer,'explanation':mechanism+' '+test+' 其餘選項混淆不同架構或證據的適用邊界。','explanationEn':mechanismEn+' '+testEn+' The alternatives confuse architectural or evidence boundaries.'}}

def build():
 assert set(D)==set(CAT),(set(CAT)-set(D),set(D)-set(CAT))
 courses=[];places=[];related=[]
 for cid in CAT:
  d=D[cid];c=copy.deepcopy(OLD.get(cid,CAT[cid]));original=copy.deepcopy(c.get('stages',[]));oldsteps=[s for st in original for s in st['steps']];offset=len(oldsteps);previous=oldsteps[-1]['id']if oldsteps else None
  extra=[]
  for si,(title,titleEn)in enumerate(d['stages']):
   steps=[]
   for j in range(8):
    s=step(cid,d,si*8+j,offset,previous);steps.append(s);previous=s['id']
   extra.append({'id':f'{cid}-v11-stage{si+1:02d}','order':len(original)+si+1,'title':title,'titleEn':titleEn,'description':f'四個技術單元以原理／架構與實驗／驗證兩步完成「{title}」；每步獨立保存進度與知識測驗。','descriptionEn':f'Four technical units develop {titleEn.lower()} through separate principle/architecture and experiment/validation tasks with saved progress and knowledge checks.','steps':steps})
  c.update({'kind':'course','status':'guided','contentStatus':'reviewable-educational-curriculum','depth':4,'stepCount':offset+32,'estimatedMinutes':sum(s.get('estimatedMinutes',35)for s in oldsteps)+1120,'simulationOnly':True,'languageCoverage':['zh-TW','en'],'stages':original+extra,'sourceIds':list(dict.fromkeys(c.get('sourceIds',[])+source_ids(d['src']))),'summary':f'以{d["focus"][0]}連結 16 個技術單元，新增 32 步原理、架構、假想算例、實驗設計與失效驗證。'+(' 原有步驟及進度識別完整保留。'if offset else ''),'summaryEn':f'Sixteen technical units connect {d["focus"][1].lower()} through 32 new tasks covering principles, architecture, assumed calculations, experiment design and failure validation.'+(' Existing steps and progress identities are preserved.'if offset else ''),'scope':'公開原理的雙語工程教育；工作臺是概念模擬，不是特定廠商產品的完整模擬器。數值為自行設定的教學假設。實驗僅限離線模型、自己的隔離環境或明確授權的測試資料；不掃描或改動真實第三方系統，未測平臺保留未決。','scopeEn':'Bilingual engineering education from public principles; the workbench is a conceptual simulation, not a complete simulator of any vendor product. Inputs are original teaching assumptions. Experiments use offline models, owned isolated environments or explicitly authorized test data, never scan/modify third-party systems and leave untested platforms unresolved.','workedExample':{'title':'原創可重算假想案例','titleEn':'Original reproducible hypothetical case','text':d['example'][0],'textEn':d['example'][1],'assumptions':'使用算例明列的單位、邊界與理想化前提；改變版本、工作負載、故障模型或資源條件後重算。','assumptionsEn':'Use the stated units, boundaries and idealizations; recalculate after version, workload, fault-model or resource changes.','sourceScope':'作者原創算例；官方來源支援原理與背景，不是這組數字的實測來源。','sourceScopeEn':'Original assumed example; official sources support principles/context, not measurements of these numbers.'}})
  if offset:c['enrichmentVersion']=11
  else:c['curriculumVersion']=11
  c['diagram']={'type':'network','labels':[x[0]for x in d['stages']],'labelsEn':[x[1]for x in d['stages']],'original':True,'notToScale':True}
  courses.append(c)
  pk=PLACES[d['place']]['source'];references=[ref(k)for k in list(dict.fromkeys(d['src']+[pk]))];p=place_for(cid)
  places.append({'courseId':cid,'place':p,'summary':f'本課從{d["focus"][0]}比較公開原理與大型系統交接。地圖為供應商、標準機構或研究／開放技術的代表點；不宣稱課程由該機構授課或所有實作在此完成。','summaryEn':f'The course connects public principles and large-system handoffs through {d["focus"][1].lower()}. Maps identify representative vendors, standards institutions or research/open-technology references; no institutional teaching or universal implementation-site claim is made.','connection':f'從「{d["units"][0][0][0]}」到「{d["units"][-1][0][0]}」逐項檢查架構、介面與證據。','connectionEn':f'Connect {d["units"][0][0][1].lower()} to {d["units"][-1][0][1].lower()} and audit architecture, interfaces and evidence.','history':[{'year':'公開技術脈絡 / Public technical context','title':d['stages'][0][0],'titleEn':d['stages'][0][1],'text':f'官方公開資料「{S[d["src"][0]]["title"]}」提供架構脈絡；本課先由「{d["units"][0][0][0]}」及「{d["units"][1][0][0]}」建立邊界，再進入實驗判讀。這是原創教材的學習順序，不是宣稱技術發明年代。','textEn':f'The primary reference {S[d["src"][0]]["titleEn"]} supplies architectural context. These original lessons start with {d["units"][0][0][1].lower()} and {d["units"][1][0][1].lower()} before experiments; this is a learning sequence, not an invention-date claim.','sourceIds':source_ids([d['src'][0]])},{'year':'代表機構 / Representative institution','title':p['name'],'titleEn':p['nameEn'],'text':p['coordinateScope'],'textEn':p['coordinateScopeEn'],'sourceIds':source_ids([pk])}],'references':references,'sourceIds':source_ids(d['src']+[pk])})
  comparisons=[]
  for target,why,difference in d['related']:
   tid=target if target=='cybersecurity'else 'a'+str(target);t=CAT[tid];why,whyEn=why.split('~');difference,differenceEn=difference.split('~')
   comparisons.append({'id':tid,'title':t['title'],'titleEn':t['titleEn'],'why':why,'whyEn':whyEn,'transfer':why,'transferEn':whyEn,'difference':difference,'differenceEn':differenceEn,'practice':[f'由「{d["units"][0][0][0]}」畫出兩課共用與需要重定義的資料、控制及時間邊界。',f'針對「{difference}」各指定一個能辨識差異的實驗；只使用虛構資料或明確授權隔離環境。','將本課算例移植到衍生課：逐項重查方程適用條件、單位、版本、故障假設，標示不能沿用的數字。'],'practiceEn':[f'From {d["units"][0][0][1].lower()}, map shared and redefined data, control and timing boundaries.',f'For "{differenceEn}", specify a discriminating experiment for each course using fictional data or an explicitly authorized isolated environment.','Transfer the worked example: recheck equation scope, units, versions and fault assumptions; mark values that cannot carry over.'],'place':place_for(tid),'referenceUrls':[S[k]['url']for k in d['src']]})
  related.append({'courseId':cid,'overview':f'由{d["focus"][0]}延伸；共用概念不代表可原封不動搬移全部規格或程式。','overviewEn':f'Extend {d["focus"][1].lower()}; shared concepts do not imply unchanged specifications or code.','related':comparisons,'references':references})
  assert len(comparisons)==2 and all(x['id']in CAT and x['id']!=cid for x in comparisons)
  if offset:
   assert c['stages'][:len(original)]==OLD[cid]['stages']
   assert c.get('curriculumVersion')==OLD[cid].get('curriculumVersion')
  assert c['title']==CAT[cid]['title']and c['titleEn']==CAT[cid]['titleEn']and c['category']=='computing'
  newsteps=[s for st in extra for s in st['steps']];assert len(newsteps)==32
  for st in newsteps:
   assert len(st['knowledge'])>=2 and st['quiz']['answer']in range(3)
   assert len(st['quiz']['options'])==len(set(st['quiz']['options']))==3
  assert len(c['sourceIds'])>=2
 out={'version':11,'scope':'Original bilingual offline/local authorized architecture and defensive experiments; immutable existing steps retained. Public primary references linked, no copied source media.','courses':courses,'sources':list(S.values()),'places':places,'related':related}
 (P/'group_a.json').write_text(json.dumps(out,ensure_ascii=False,indent=2)+'\n')
 stats={'courses':len(courses),'newCourses':len(courses)-len(OLD),'enrichedCourses':len(OLD),'technicalUnits':len(D)*16,'addedSteps':len(D)*32,'totalSteps':sum(c['stepCount']for c in courses),'knowledgeRecords':sum(len(s.get('knowledge',[]))for c in courses for st in c['stages']for s in st['steps']),'primarySources':len(S),'places':len(places),'relatedComparisons':sum(len(r['related'])for r in related)}
 print(json.dumps(stats,ensure_ascii=False));return out
if __name__=='__main__':build()
