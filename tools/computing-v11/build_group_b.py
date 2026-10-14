#!/usr/bin/env python3
"""V11 group B: independently authored, bilingual defensive engineering cases.
Inputs below are course-specific technical propositions, not copied source prose.
Run this file to regenerate group_b.json; no network required during generation.
"""
import copy,json,math
from pathlib import Path
P=Path(__file__).resolve().parent
SNAP=json.loads((P/'group_b_snapshot.json').read_text())
CAT={c['id']:c for c in SNAP['catalog']}
S={}
def source(k,title,titleEn,publisher,url,note=''):
 S[k]={'id':'v11b-'+k,'title':title,'titleEn':titleEn,'publisher':publisher,'url':url,'category':'computing','sourceType':'primary','accessedAt':'2026-10-14','imageReuse':'僅連結，未重製來源圖像或影片。','imageReuseEn':'Link only; no source artwork or video reproduced.','scope':'官方標準／研究／實作文件支援技術脈絡；模型、練習及假想數字為獨立編寫。'+note,'scopeEn':'Official standard, research or implementation context; models, exercises and numerical inputs are independently authored.','retrievalStatus':'verified-primary-web-retrieval'}
source('dns','DNS 概念與設施 RFC 1034','DNS concepts and facilities RFC 1034','IETF / RFC Editor','https://www.rfc-editor.org/info/rfc1034/')
source('dnssec','DNSSEC 要求 RFC 4033','DNSSEC requirements RFC 4033','IETF / RFC Editor','https://www.rfc-editor.org/info/rfc4033/')
source('ptp','LinuxPTP ptp4l 文件','LinuxPTP ptp4l documentation','LinuxPTP Project','https://www.linuxptp.org/documentation/ptp4l/')
source('gptp','IEEE 802.1AS 時間同步','IEEE 802.1AS timing and synchronization','IEEE 802.1','https://www.ieee802.org/1/pages/802.1as.html')
source('tsn','IEEE 時間敏感網路工作組','IEEE Time-Sensitive Networking task group','IEEE 802.1','https://1.ieee802.org/tsn/')
source('wlan','高密度 WLAN 設計','High-client-density WLAN design','Cisco','https://www.cisco.com/c/en/us/td/docs/wireless/controller/technotes/8-7/b_wireless_high_client_density_design_guide.html')
source('campus','校園 LAN 與 WLAN 架構','Campus LAN and WLAN architecture','Cisco','https://www.cisco.com/c/en/us/td/docs/solutions/CVD/Campus/cisco-campus-lan-wlan-design-guide.html')
source('5g','3GPP 5G 系統架構概要','3GPP 5G architecture overview','3GPP','https://www.3gpp.org/ftp/Information/presentations/presentations_2020/Poster_2020_MWC_v6_OPTIMIZED.pdf')
source('sa2','3GPP SA2 架構與切片演進','3GPP SA2 architecture and slicing evolution','3GPP','https://www.3gpp.org/news-events/3gpp-news/sa2-artcle')
source('oran','O-RAN 開放規格','O-RAN open specifications','O-RAN ALLIANCE','https://www.o-ran.org/specifications')
source('oranres','O-RAN 白皮書與技術資源','O-RAN white papers and technical resources','O-RAN ALLIANCE','https://www.o-ran.org/o-ran-resources')
source('gpon','GPON 系統 G.984.1','GPON systems G.984.1','ITU-T','https://www.itu.int/rec/T-REC-G.984.1/en')
source('xgs','對稱 XGS-PON G.9807.1','Symmetric XGS-PON G.9807.1','ITU-T','https://www.itu.int/rec/T-REC-G.9807.1/en')
source('otn','光傳輸網路介面 G.709','Optical transport network interfaces G.709','ITU-T','https://www.itu.int/rec/T-REC-G.709/en')
source('submarine','光放大海底纜 G.977','Optically amplified submarine cables G.977','ITU-T','https://www.itu.int/rec/T-REC-G.977/en')
source('subtest','海底光纜測試 G.976','Submarine cable testing G.976','ITU-T','https://www.itu.int/rec/T-REC-G.976/en')
source('ground','ESA 地面站網路','ESA ground-station network','European Space Agency','https://www.esa.int/Enabling_Support/Operations/ESA_Ground_Stations')
source('ccsds','CCSDS 空間鏈路建議標準','CCSDS recommended space-link standards','CCSDS','https://ccsds.org/publications/bluebooks/')
source('leo','ROUTLEO 星座路由研究','ROUTLEO constellation-routing research','European Space Agency','https://resilience.esa.int/archives/projects/routleo')
source('satcom','衛星通訊軌道背景','Satellite communications and orbital context','European Space Agency','https://www.esa.int/Applications/Connectivity_and_Secure_Communications/About_Telecommunications')
source('bundle','Bundle Protocol 7 RFC 9171','Bundle Protocol 7 RFC 9171','IETF / RFC Editor','https://www.rfc-editor.org/info/rfc9171/')
source('dtn','ESA 延遲容忍網路示範','ESA delay-tolerant-network demonstration','European Space Agency','https://esoc.esa.int/extending-internet-space')
source('qnet','量子網路架構 RFC 9340','Quantum Internet architecture RFC 9340','IRTF / RFC Editor','https://www.rfc-editor.org/info/rfc9340/')
source('qnist','量子光網路研究平台','Quantum optical-network research testbeds','NIST','https://www.nist.gov/programs-projects/quantum-optical-networks')
source('zt','零信任架構 SP 800-207','Zero Trust Architecture SP 800-207','NIST','https://csrc.nist.gov/pubs/sp/800/207/final')
source('identity','數位身分 SP 800-63-4','Digital Identity Guidelines SP 800-63-4','NIST','https://pages.nist.gov/800-63-4/')
source('oauth','OAuth 安全最佳實務 RFC 9700','OAuth security best current practice RFC 9700','IETF / RFC Editor','https://www.rfc-editor.org/info/rfc9700/')
source('webauthn','WebAuthn 第 3 級建議標準','WebAuthn Level 3 Recommendation','W3C','https://www.w3.org/TR/webauthn-3/')
source('pki','X.509 PKI RFC 5280','X.509 PKI RFC 5280','IETF / RFC Editor','https://www.rfc-editor.org/info/rfc5280/')
source('acme','ACME 自動憑證 RFC 8555','ACME certificate automation RFC 8555','IETF / RFC Editor','https://www.rfc-editor.org/info/rfc8555/')
source('tls','TLS 1.3 RFC 9846','TLS 1.3 RFC 9846','IETF / RFC Editor','https://www.rfc-editor.org/info/rfc9846/','2026 年 RFC 9846 已取代 RFC 8446；部署時仍须依實作版本核對。')
source('keys','密鑰管理 SP 800-57 第 1 部第 5 版','Key management SP 800-57 Part 1 Revision 5','NIST','https://csrc.nist.gov/pubs/sp/800/57/pt1/r5/final')
source('hsm','PKCS #11 第 3.1 版','PKCS #11 Version 3.1','OASIS','https://www.oasis-open.org/standard/pkcs-11-specification-version-3-1-2/')
source('cmvp','密碼模組驗證計畫','Cryptographic Module Validation Program','NIST','https://csrc.nist.gov/projects/cryptographic-module-validation-program')
source('kem','ML-KEM FIPS 203','ML-KEM FIPS 203','NIST','https://csrc.nist.gov/pubs/fips/203/final')
source('dsa','ML-DSA FIPS 204','ML-DSA FIPS 204','NIST','https://csrc.nist.gov/pubs/fips/204/final')
source('slhdsa','SLH-DSA FIPS 205','SLH-DSA FIPS 205','NIST','https://csrc.nist.gov/pubs/fips/205/final')
source('spf','寄件政策 SPF RFC 7208','Sender Policy Framework RFC 7208','IETF / RFC Editor','https://www.rfc-editor.org/info/rfc7208/')
source('dkim','郵件簽章 DKIM RFC 6376','DKIM signatures RFC 6376','IETF / RFC Editor','https://www.rfc-editor.org/info/rfc6376/')
source('dmarc','DMARC RFC 9989','DMARC RFC 9989','IETF / RFC Editor','https://www.rfc-editor.org/info/rfc9989/','2026 年 RFC 9989 取代 RFC 7489；報告分見 9990、9991。')
source('dmarcagg','DMARC 彙總報告 RFC 9990','DMARC aggregate reporting RFC 9990','IETF / RFC Editor','https://www.rfc-editor.org/info/rfc9990/')
source('dmarcfail','DMARC 失敗報告 RFC 9991','DMARC failure reporting RFC 9991','IETF / RFC Editor','https://www.rfc-editor.org/info/rfc9991/')
source('asvs','應用安全驗證標準 ASVS','Application Security Verification Standard','OWASP Foundation','https://owasp.org/projects/asvs')
source('crs','網頁防護核心規則 CRS','Web protection Core Rule Set','OWASP Foundation','https://owasp.org/projects/crs')
source('attack','ATT&CK 防禦知識庫','ATT&CK defensive knowledge base','MITRE','https://attack.mitre.org/')
source('sysmon','Sysmon 端點事件文件','Sysmon endpoint-event documentation','Microsoft','https://learn.microsoft.com/en-us/sysinternals/downloads/sysmon')
source('logs','安全日誌管理 SP 800-92','Security log management SP 800-92','NIST','https://csrc.nist.gov/pubs/sp/800/92/final')
source('ir','事件回應 SP 800-61 第 3 版','Incident response SP 800-61 Revision 3','NIST','https://csrc.nist.gov/pubs/sp/800/61/r3/final')
source('suricata','Suricata 使用者指南','Suricata User Guide','Open Information Security Foundation','https://docs.suricata.io/en/latest/','latest 在本次檢索為開發版；練習僅分析假想事件，正式選用需固定穩定版本。')
source('ot','OT 安全 SP 800-82 第 3 版','OT security SP 800-82 Revision 3','NIST','https://csrc.nist.gov/pubs/sp/800/82/r3/final')
source('dtls','DTLS 1.3 RFC 9147','DTLS 1.3 RFC 9147','IETF / RFC Editor','https://www.rfc-editor.org/info/rfc9147/')
source('vehicle','現代車輛資安最佳實務 2022','Modern-vehicle cybersecurity best practices 2022','NHTSA','https://www.nhtsa.gov/sites/nhtsa.gov/files/2022-09/cybersecurity-best-practices-safety-modern-vehicles-2022-tag.pdf')
source('r155','UN R155 車輛資安管理','UN R155 vehicle cybersecurity management','UNECE','https://unece.org/transport/documents/2021/03/standards/un-regulation-no-155-cyber-security-and-cyber-security')
source('sev','Linux SEV 來賓介面','Linux SEV guest interface','Linux Kernel Project','https://docs.kernel.org/virt/coco/sev-guest.html')
source('rats','遠端證明架構 RFC 9334','Remote attestation architecture RFC 9334','IETF / RFC Editor','https://www.rfc-editor.org/info/rfc9334/')
D={}
def spec(n,src,focus,example,perturb,mis,units):
 pairs=lambda s:tuple(s.split('~',1))
 rows=[]
 for line in units.strip().splitlines():
  name,mechanism=line.split('|',1);rows.append((pairs(name),pairs(mechanism)))
 assert len(rows)==16,(n,len(rows))
 assert len(perturb)==4 and len(mis)==2
 D['a'+str(n)]={'src':src.split(),'focus':pairs(focus),'example':pairs(example),'perturb':[pairs(s) for s in perturb],'mis':[pairs(s) for s in mis],'units':rows}
spec(335,'dns dnssec','分散式命名、快取一致性與驗證鏈~distributed naming, cache consistency and validation chains','假設 80% 查詢命中 2 ms 快取，其餘需 50 ms，平均為 0.8×2+0.2×50=11.6 ms；這不表示 p99 為 11.6 ms，也未計排隊。~Assume 80% cache hits at 2 ms and misses at 50 ms: mean latency is 11.6 ms; p99 is not 11.6 ms and queuing is excluded.', ['只改 TTL，比較更新後舊值最長保留時間。~Change only TTL and compare maximum stale-answer duration.','固定名稱，只改委派點的 NS 與 glue 內容。~Keep names fixed and change delegation NS/glue consistency.','只改簽章有效期，區分不存在與驗證失敗。~Change signature validity only; separate absence from validation failure.','固定負載，只改失去一台權威伺服器的情境。~Hold load fixed and model one authoritative-server outage.'], ['DNSSEC 會加密所有名稱查詢。~DNSSEC encrypts every name query.','縮短 TTL 必然降低所有查詢延遲。~Shorter TTL necessarily reduces every query latency.'],'''
樹狀命名空間~Hierarchical namespace|域名是標籤路徑，管理區域不必等於整個子樹。~Names are label paths; a managed zone need not cover its whole subtree.
解析器責任~Resolver responsibilities|遞迴解析器代客追查，權威伺服器提供其區域資料。~Recursive resolvers pursue answers; authoritative servers publish their zones.
資源紀錄型別~Resource-record types|A、AAAA 與 CNAME 的用途不同，別名不等於位址集合。~A, AAAA and CNAME have different semantics; aliases are not address sets.
委派與 glue~Delegation and glue|glue 協助找到委派伺服器，不能取代權威答案。~Glue locates delegated servers; it does not replace authoritative answers.
快取 TTL~Cache TTL|TTL 限制快取新鮮度；短 TTL 增加向上游查詢的機會。~TTL bounds freshness; shorter TTL increases upstream-query opportunities.
負面快取~Negative caching|名稱不存在與查詢型別無資料需要分開判讀。~Name absence and absence of the queried record type differ.
區域序號~Zone serials|序號供次要伺服器辨識更新，不是實際經過的秒數。~Serials identify updates for secondary servers, not elapsed seconds.
分割視圖~Split views|不同解析視圖可回不同答案，除錯必須記錄客戶端視圖。~Views may return different answers; diagnosis must record the client view.
DNSSEC 信任鏈~DNSSEC trust chain|DS 與 DNSKEY 連接驗證链，签章保護來源與完整性。~DS and DNSKEY connect validation; signatures protect origin and integrity.
簽章時窗~Signature windows|簽章有效性依賴時間基準，時鐘錯誤可能造成 bogus。~Signature validity depends on time; clock errors can produce bogus results.
不存在證明~Authenticated denial|帶簽章的否定證明與單純逾時不是同一種證據。~Signed denial and a timeout provide different evidence.
傳輸與截斷~Transport and truncation|截斷回應需要適當後續處理，不能當作完整答案。~Truncated responses require follow-up, not acceptance as complete answers.
冗餘權威服務~Authoritative redundancy|多台服務若共用故障域，數量增加不代表獨立可靠性。~More servers sharing one failure domain do not provide independent resilience.
容量與尾延遲~Capacity and tail latency|平均命中率不能單獨決定排隊或最慢查詢時間。~Average hit ratio alone cannot determine queues or worst-case latency.
更新回滾~Update rollback|回滾需同時考慮區域版本、簽章與仍存活的快取。~Rollback must consider zone versions, signatures and surviving caches.
證據交接~Evidence handoff|可重現查詢需保留名稱、型別、視圖、時間及驗證狀態。~Reproducible queries record name, type, view, time and validation status.
''')
spec(336,'ptp gptp','時戳、路徑不對稱與時鐘伺服~timestamps, path asymmetry and clock servos','假設 t2−t1=120 ns、t4−t3=80 ns，對稱模型估 offset=(120−80)/2=20 ns、delay=100 ns；若去程多 40 ns，不對稱造成 20 ns 偏差。~With t2−t1=120 ns and t4−t3=80 ns, the symmetric model gives offset=20 ns and delay=100 ns; 40 ns forward-path asymmetry biases offset by 20 ns.', ['改去程延遲而保留回程，辨識 offset 與 path delay 的混合。~Change forward delay only and identify offset/path-delay mixing.','比較硬體時戳與作業系統排程加入的抖動。~Compare hardware timestamps with added scheduling jitter.','固定同步週期，只改伺服器積分增益的假想響應。~Fix sync interval and compare hypothetical integral gains.','模擬 grandmaster 切換與失鎖的時間序列。~Model grandmaster transitions and loss-of-lock sequences.'], ['雙向平均延遲可以自動消除不對稱。~Averaging bidirectional delay automatically removes asymmetry.','所有 PTP profile 都具有相同消息間隔。~Every PTP profile uses identical message intervals.'],'''
時鐘域~Clock domains|時鐘域是同步邊界，不是把所有裝置時間自動合併。~A clock domain defines a synchronization boundary, not automatic universal agreement.
四時戳模型~Four-timestamp model|offset 與延遲的分離需要雙向延遲對稱假設。~Separating offset and delay requires a bidirectional symmetry assumption.
頻率與相位~Frequency and phase|頻率誤差使相位誤差隨時間累積。~Frequency error accumulates into phase error over time.
硬體時戳~Hardware timestamps|靠近媒體層的時戳減少軟體排程誤差，但仍需校準。~Near-media timestamps reduce scheduling error but still require calibration.
Ordinary clock~Ordinary clocks|單埠時鐘在選定時鐘關係內估測本地時間。~A single-port clock estimates local time within its selected clock relationship.
Boundary clock~Boundary clocks|邊界時鐘在不同埠間重新建立同步關係。~Boundary clocks reestablish synchronization relationships across ports.
Transparent clock~Transparent clocks|透明時鐘補償經過設備的 residence time，不等於重新當主時鐘。~Transparent clocks correct residence time rather than becoming a new master.
主時鐘選擇~Grandmaster selection|選擇演算法比較品質資料，優先權不能創造時鐘品質。~Selection compares quality data; priority cannot create clock quality.
E2E 與 P2P~E2E versus P2P|端對端及鄰接延遲量測所估的路徑不同。~End-to-end and peer-delay methods estimate different path segments.
雙步時戳~Two-step timestamps|Follow_Up 補送精確發送時間，需要正確關聯 Sync。~Follow_Up supplies precise send time and must match its Sync.
路徑不對稱~Path asymmetry|固定不對稱會以約一半差值偏置 offset 估計。~Fixed asymmetry biases offset by roughly half the delay difference.
伺服器控制~Servo control|伺服增益影響收斂及雜訊放大，不宜只追求最快變化。~Servo gains affect convergence and noise amplification, not only speed.
Holdover~Holdover|失去參考後依靠振盪器維持時間，誤差隨漂移增加。~After reference loss, oscillator drift grows the held-over time error.
時鐘 profile~Clock profiles|profile 限制互通選項，須逐項核對而非只看 PTP 標籤。~Profiles constrain interoperability; a PTP label alone is insufficient.
故障與告警~Faults and alarms|鎖定旗標不是所有時段的最大 offset 證明。~A lock flag does not prove the maximum offset over every interval.
時間證據預算~Time evidence budget|端到端誤差應涵蓋參考、時戳、路徑與校準不確定度。~The error budget includes reference, timestamps, path and calibration uncertainty.
''')
spec(337,'tsn gptp','排程閘門、時間同步與可界定延遲~scheduled gates, synchronization and bounded latency','假設 1 Gbit/s 上傳送 1500 byte 訊框，純內容序列化為 12 μs；1 ms 週期留 100 μs，忽略 overhead 可容納 8 框，實際須再扣 guard band 與開銷。~At 1 Gbit/s, 1500-byte payload serialization is 12 μs; a 100 μs window in a 1 ms cycle fits at most eight such payloads before overhead and guard bands.', ['只改閘門開啟時間，觀察臨界流量等待。~Change gate-open time only and observe critical-flow waiting.','固定流量，只改同步誤差對 guard band 的需求。~Fix traffic and vary synchronization error in the guard-band budget.','比較大訊框阻塞与預先中斷的理想化情境。~Compare large-frame blocking with idealized preemption.','模擬單一路徑中斷，檢查重複消除及交付延遲。~Model one path outage; check duplicate elimination and delivery latency.'], ['優先權高便保證任何負載下零延遲。~High priority guarantees zero delay at every load.','TSN 不需要知道鏈路速率或封包大小。~TSN needs neither link rate nor frame size.'],'''
流量需求合約~Traffic contracts|到達率、突發量與截止時間一起限定可接受負载。~Rate, bursts and deadlines jointly define admissible traffic.
時間基準~Time reference|跨橋排程需要共享時基及有限同步誤差。~Cross-bridge schedules need a shared timebase and bounded synchronization error.
訊框序列化~Frame serialization|序列化時間與位元數成正比、與鏈路速率成反比。~Serialization time scales with bits and inversely with link rate.
佇列映射~Queue mapping|分類將流映射至佇列；分類錯誤會破壞排程假設。~Classification maps streams to queues; mistakes break scheduling assumptions.
時間感知閘門~Time-aware gates|閘門限制何時可發送，不會讓資料瞬間穿過鏈路。~Gates constrain send times; they do not make transmission instantaneous.
Guard band~Guard bands|保護間隔避免低優先框跨越關鍵視窗。~Guard bands prevent lower-priority frames overlapping critical windows.
信用整形~Credit shaping|信用限制傳送節奏；服務保證仍受干擾流量影響。~Credit regulates transmission pacing; interference still affects service guarantees.
訊框預先中斷~Frame preemption|可中斷低優先傳送可降低阻塞，但須匹配雙端能力。~Preemption reduces blocking only with compatible peer capabilities.
流量 policing~Stream policing|入口 policing 限制不符合合約的流，維護其他流的假設。~Ingress policing constrains nonconforming streams and preserves others' assumptions.
路徑冗餘~Path redundancy|複製與消除需一致序號及不同故障域。~Replication/elimination needs consistent sequence tracking and distinct failure domains.
每跳預算~Per-hop budgets|總延遲包含每跳等待、傳送及處理，不能只加傳播。~Total delay includes waiting, serialization and processing, not propagation alone.
Admission control~Admission control|只有排程資源足夠才接受新增流。~New streams are admitted only when schedule resources suffice.
控制平面~Control plane|集中計算或分散設定都必須保持排程與流定義一致。~Centralized or distributed control must keep schedules and stream definitions consistent.
時鐘失鎖~Clock-loss behavior|同步失效時的降階策略要在服務合約中說明。~Service contracts must define degraded behavior after synchronization loss.
最差情境~Worst-case cases|平均延遲良好不代表每個截止時間都被滿足。~Good mean latency does not prove every deadline is met.
互通驗證~Interoperability evidence|採用哪些 TSN 功能應列明，不能只以支援 TSN 代替。~Enumerate adopted TSN features rather than relying on a generic support claim.
''')
spec(338,'wlan campus identity','射頻容量、漫遊與企業身分驗證~RF capacity, roaming and enterprise authentication','假想同頻域 20 台客戶端各需 2 Mbit/s，共 40 Mbit/s；有效吞吐 80 Mbit/s 的負載約 50%。此為平均容量假設，未保證碰撞、漫遊或 p99。~Twenty clients each needing 2 Mbit/s demand 40 Mbit/s; with assumed usable throughput of 80 Mbit/s, load is 50%, without guarantees for collisions, roaming or p99.', ['保留客戶數，只改同頻 AP 數，分析共享 airtime。~Keep client count and vary co-channel APs to analyze shared airtime.','固定發射功率，只改訊號衰減與 SNR。~Fix transmit power and change attenuation/SNR.','比較正常與過期伺服器憑證的假想 EAP 驗證。~Compare valid versus expired EAP server certificates.','模擬漫遊時重驗證延遲與封包中斷。~Model reauthentication latency and packet interruption during roaming.'], ['增加 AP 數一定線性增加同頻容量。~Adding APs always increases co-channel capacity linearly.','RSSI 高即證明 SNR、吞吐及驗證都合格。~High RSSI proves SNR, throughput and authentication are all acceptable.'],'''
需求與並行數~Demand and concurrency|使用者數量與同時傳输的用戶數不同。~Total users and simultaneously transmitting clients are different counts.
鏈路預算~Link budget|接收功率由發射、天線增益及路徑損耗共同決定。~Receive power combines transmit power, antenna gains and path loss.
SNR 與速率~SNR and rate|調變率受訊號與雜訊比限制，RSSI 單值不足。~Modulation depends on signal-to-noise ratio; RSSI alone is insufficient.
Airtime~Airtime|慢速客戶端可消耗較多共享空中時間。~Slow clients can consume more shared airtime per payload.
頻道重用~Channel reuse|同頻 AP 彼此爭用，重用需考慮空間隔離。~Co-channel APs contend; reuse requires spatial-separation analysis.
頻寬取捨~Channel-width tradeoffs|較寬頻道提高峰值但減少可獨立重用頻道。~Wider channels raise peak rates but reduce independently reusable channels.
AP 接回網路~AP backhaul|無線容量可能被交換器上行與 PoE 能力限制。~Wireless capacity can be limited by uplinks and PoE capability.
控制器邊界~Controller boundaries|管理集中與資料路徑集中不是同一種架構。~Centralized management and centralized data forwarding are different architectures.
企業 EAP~Enterprise EAP|企業驗證需裝置信任正確身分伺服器。~Enterprise authentication requires clients to trust the correct identity server.
憑證驗證~Certificate checks|接受任意伺服器憑證會削弱企業身分驗證。~Accepting arbitrary server certificates weakens enterprise authentication.
網路分區~Network segmentation|SSID 名稱不是獨立權限控制的證據。~An SSID name is not evidence of independent access control.
訪客生命週期~Guest lifecycle|訪客憑據應受有效期、範圍與撤銷限制。~Guest credentials need lifetime, scope and revocation limits.
漫遊決策~Roaming decisions|客戶端主導漫遊決策，AP 不能保證所有裝置同樣切換。~Clients drive roaming; APs cannot guarantee identical device transitions.
隱藏節點~Hidden nodes|無法相互聽見的客戶端仍可能在接收點碰撞。~Clients unable to hear each other may still collide at a receiver.
密度驗收~Density acceptance|必須以真實並行度及流量型態評估尾延遲。~Assess tail latency using representative concurrency and traffic patterns.
變更回滾~Change rollback|頻道與認證變更需預先保留可恢復的配置。~Channel and authentication changes need recoverable prior configurations.
''')
spec(339,'5g sa2','5G 核心服務、控制／用戶平面與狀態~5G core services, control/user planes and state','假設 10,000 用戶各平均 100 kbit/s，UPF 總量為 1 Gbit/s；加 20% 餘裕取 1.2 Gbit/s，未計封裝或尖峰，不能以此推算控制平面容量。~10,000 users averaging 100 kbit/s require 1 Gbit/s through the UPF; 20% headroom gives 1.2 Gbit/s, excluding encapsulation, peaks and control-plane capacity.', ['固定用戶數，只改 session 建立率。~Keep users fixed and vary session-setup arrival rate.','固定資料流量，只改 UPF 到應用的位置。~Fix traffic and vary UPF/application placement.','比較正常與失效的服務註冊資料。~Compare valid and stale service-registry data.','模擬 SMF 重啟後有與沒有狀態恢復。~Model SMF restart with and without state recovery.'], ['UPF 承載資料流，因此可取代所有 AMF 控制功能。~UPF data forwarding can replace all AMF control functions.','容器數量加倍必然讓有狀態核心容量加倍。~Doubling containers necessarily doubles stateful-core capacity.'],'''
控制與用戶平面~Control and user planes|控制訊息建立狀態，用戶平面承載應用資料。~Control messages establish state; the user plane carries application data.
AMF 責任~AMF responsibilities|存取與移動管理和 session 管理分開。~Access/mobility management is separate from session management.
SMF 責任~SMF responsibilities|SMF 管理 session，並控制對應 UPF 行為。~SMF manages sessions and controls corresponding UPF behavior.
UPF 責任~UPF responsibilities|UPF 將資料按規則轉送，不是身分資料庫。~UPF forwards data under rules; it is not an identity database.
服務式介面~Service-based interfaces|服務發現、授權與版本一致性一起影響互通。~Discovery, authorization and version consistency jointly affect interoperability.
NRF 登錄~NRF registration|登錄資料可能過期，服務發現需處理生命週期。~Registry entries can stale; discovery needs lifecycle handling.
訂閱與認證~Subscription and authentication|訂閱資料與認證交換是相關但不同的責任。~Subscription data and authentication exchange are related but distinct responsibilities.
政策控制~Policy control|政策將業務要求轉成可執行的 session 約束。~Policy turns service requirements into enforceable session constraints.
PDU session~PDU sessions|session 建立成功不代表端到端應用已可用。~Successful session setup does not prove end-to-end application availability.
QoS flow~QoS flows|QoS flow 與承載資源映射需同時驗證。~Verify both QoS-flow definitions and resource mappings.
邊緣 UPF~Edge UPF placement|靠近應用的 UPF 可減少路徑，但仍有無線與處理延遲。~Near-application UPFs reduce path length, not radio or processing delays.
狀態外置~Externalized state|狀態外置改變一致性與失效模式，不自動解決擴展。~External state changes consistency/failure modes; it does not solve scaling automatically.
容量模型~Capacity models|註冊率、session 率及資料吞吐要分別估計。~Estimate registration rate, session rate and data throughput separately.
容錯重試~Fault retries|重試須避免同一請求重複建立不一致狀態。~Retries must prevent duplicate inconsistent state creation.
互通矩陣~Interoperability matrix|協議版本與支援選項需形成具體矩陣。~Protocol versions and supported options need an explicit matrix.
服務驗收~Service acceptance|以合成用戶驗證狀態轉換及資料路徑後才能放行。~Accept only after synthetic users verify state transitions and data paths.
''')
spec(340,'oran oranres 5g','解耦無線元件、開放介面與閉迴路控制~disaggregated radio components, open interfaces and closed-loop control','假設 fronthaul 4 Gbit/s 的教學資料需 10% 額外封裝，鏈路需求為 4.4 Gbit/s；8 Gbit/s 假想可用速率的利用率 55%，未含突發與同步餘裕。~Assumed 4 Gbit/s fronthaul traffic with 10% encapsulation needs 4.4 Gbit/s; utilization of an assumed 8 Gbit/s usable link is 55%, excluding bursts and timing margin.', ['保留功能切分，只改 fronthaul 延遲。~Keep the split and vary fronthaul delay.','固定 xApp 輸入，只改控制更新週期。~Fix xApp inputs and vary control update interval.','比較兩供應商能力宣告重疊及缺項。~Compare overlaps and omissions in two vendor capability declarations.','模擬控制器斷線，觀察降階而非失控。~Model controller loss and verify degradation rather than uncontrolled action.'], ['開放介面保證所有供應商產品即插即用。~Open interfaces guarantee universal vendor plug-and-play.','所有 RIC 控制迴路均適合逐 OFDM 符號控制。~Every RIC loop is suitable for per-OFDM-symbol control.'],'''
解耦邊界~Disaggregation boundaries|元件解耦增加介面驗證與版本管理責任。~Disaggregation adds interface-verification and version-management responsibilities.
O-RU 與 O-DU~O-RU and O-DU|功能切分決定前傳資料型態與時限。~Functional splits determine fronthaul data formats and deadlines.
O-CU 功能~O-CU functions|較高層功能集中與無線低層時限應分開考慮。~Separate centralized higher-layer functions from low-layer radio deadlines.
前傳同步~Fronthaul synchronization|前傳資料與時基需協同，容量足夠不代表同步足夠。~Fronthaul data and timing must cooperate; capacity does not prove synchronization.
管理平面~Management plane|管理配置須與運行資料路徑的權限分離。~Management configuration needs permissions separate from runtime data paths.
Near-RT RIC~Near-real-time RIC|近即時控制仍有介面與處理延遲邊界。~Near-real-time control retains interface and processing-latency bounds.
Non-RT RIC~Non-real-time RIC|慢時間尺度政策與學習不能替代低層即時處理。~Slow-timescale policy/learning cannot replace low-layer real-time processing.
xApp/rApp~xApps and rApps|不同應用的控制目標可能競爭，需要仲裁。~Application control objectives can conflict and require arbitration.
E2 觀測~E2 observations|量測取樣與報告延遲影響控制可觀測性。~Sampling and reporting delay affect control observability.
A1 政策~A1 policies|政策意圖需要可驗證映射至可執行動作。~Policy intent needs a verifiable mapping to executable actions.
雲端資源~Cloud resources|CPU 隔離與延遲抖動是無線軟體整合要求。~CPU isolation and latency jitter matter for radio-software integration.
加速器介面~Accelerator interfaces|硬體加速需匹配資料搬移與軟體版本。~Acceleration needs compatible data movement and software versions.
安全邊界~Security boundaries|開放介面仍需相互驗證與最小權限。~Open interfaces still need mutual authentication and least privilege.
互通能力~Interoperability capabilities|支援同一規格不表示支援相同選用功能。~Sharing a specification does not imply identical optional capabilities.
閉迴路穩定~Closed-loop stability|延遲與增益會使看似良好策略震盪。~Delay and gain can destabilize an apparently good policy.
降階驗證~Fallback evidence|應用撤除時應保留可描述的基線服務。~Removing a control application should preserve a defined baseline service.
''')
spec(341,'5g sa2 zt','切片識別、资源合約與隔離證據~slice identity, resource contracts and isolation evidence','假想 1 Gbit/s 鏈路分 40%、30%、20% 給三片，共 900 Mbit/s，保留 100 Mbit/s；共享排隊與 CPU 未隔離時，分配比例不能單獨保證延遲。~A hypothetical 1 Gbit/s link allocates 40%, 30% and 20% to three slices, totaling 900 Mbit/s and leaving 100 Mbit/s; shares alone do not guarantee latency with shared queues/CPU.', ['改單一切片突發量而固定其他需求。~Vary one slice burst while fixing other demands.','比較共用與分離 UPF 的故障域。~Compare shared and separated UPF failure domains.','固定資源，只改 admission 需求。~Keep resources fixed and change admission demand.','模擬授權失效是否影響其他切片。~Model whether one authorization failure affects other slices.'], ['切片名稱不同便具有物理資源隔離。~Different slice names prove physical resource isolation.','同一切片的平均吞吐可證明所有用戶 SLA。~A slice mean throughput proves every user’s SLA.'],'''
服務合約~Service contracts|吞吐、延遲與可靠性需要分開且可測的要求。~Throughput, latency and reliability need separate measurable requirements.
切片識別~Slice identifiers|切片識別指向服務選擇，不能自行創造隔離。~Identifiers select services; they do not create isolation by themselves.
選擇與訂閱~Selection and subscription|使用者可用切片受訂閱及網路政策限制。~Available slices depend on subscriptions and network policy.
接取與核心~Access and core|端到端切片需要協調無線、傳輸與核心資源。~End-to-end slicing coordinates radio, transport and core resources.
網路功能共用~Shared network functions|共用功能降低重複成本但增加共同故障域。~Shared functions reduce duplication but add common failure domains.
資源預算~Resource budgets|資源份額必須小於可用容量並留必要餘裕。~Resource shares must fit usable capacity with required margin.
Admission control~Admission control|新增需求要通過可用資源及服務限制審查。~New demand needs available-resource and service-bound checks.
QoS 映射~QoS mapping|切片合約須轉為 flow、佇列及排程設定。~Slice contracts must map to flows, queues and schedules.
負載干擾~Load interference|單片突發可透過共享 CPU 或佇列影響其他片。~One slice burst can affect others through shared CPU or queues.
隔離層次~Isolation layers|邏輯權限、資源排程與物理隔離提供不同保證。~Logical permissions, scheduling and physical separation provide different guarantees.
生命週期~Lifecycle|建立、擴展與撤除切片需保持狀態一致。~Creation, scaling and removal must preserve consistent state.
量測可歸屬性~Metric attribution|切片指標要帶正確識別及時間範圍。~Slice metrics require correct identifiers and time windows.
策略授權~Policy authorization|管理切片的權限不應等於存取其資料權限。~Slice-management permissions should differ from data-access permissions.
故障域~Failure domains|共享資料庫故障可能超越單一切片界線。~Shared-database failures can cross slice boundaries.
SLA 尾端~SLA tails|百分位需對應樣本量，不能只用平均值代表。~Percentiles need sample-size context; means are insufficient.
解配置證據~Deprovisioning evidence|撤除後需確認路由、憑據及資源都已清理。~After removal, verify cleanup of routes, credentials and resources.
''')
spec(342,'5g oranres ptp','基地台功能切分、射頻指標與同步~base-station splits, RF metrics and synchronization','假設 20 MHz 教學頻宽與 4 bit/s/Hz 有效效率，單層吞吐 80 Mbit/s；假定四層可獨立利用為 320 Mbit/s，此為理想上界，未計協議開銷與實際通道秩。~A hypothetical 20 MHz channel at 4 bit/s/Hz yields 80 Mbit/s per layer; four independent layers imply 320 Mbit/s as an ideal upper bound, excluding overhead and actual channel rank.', ['固定頻寬，只改可用空間層數。~Fix bandwidth and vary usable spatial layers.','固定射頻訊號，只改取樣時鐘偏差。~Fix RF signals and vary sampling-clock error.','比較本地模型中不同功能切分的傳輸時限。~Compare transport deadlines for different local-model splits.','模擬一個同步源中斷後的降階。~Model degradation after one timing-source outage.'], ['天線數直接等於任何位置的可用 MIMO 層數。~Antenna count equals usable MIMO layers at every location.','平均 RF 功率合格即可省略 EVM 與頻譜品質。~Acceptable mean RF power permits skipping EVM and spectral quality.'],'''
系統功能圖~System functional map|射頻、基頻、傳輸及管理是相連但不同子系統。~RF, baseband, transport and management are connected but distinct subsystems.
功能切分~Functional splits|切分位置改變傳輸容量與時間限制。~Split placement changes transport-capacity and timing constraints.
取樣與數值格式~Sampling and formats|取樣率與位元深度共同決定原始數據率。~Sampling rate and bit depth jointly determine raw data rate.
時鐘參考~Clock reference|頻率與時間同步要求必須分别驗證。~Frequency and time synchronization requirements need separate checks.
射頻鏈路~RF chain|混頻、濾波與放大共同影響輸出品質。~Mixing, filtering and amplification jointly affect output quality.
EVM~Error-vector magnitude|EVM 描述調變偏差，不等同平均輸出功率。~EVM describes modulation error, not mean output power.
線性與峰值~Linearity and peaks|峰均比使平均功率合格仍可能發生削波。~Peak-to-average ratio allows clipping despite acceptable mean power.
MIMO 通道秩~MIMO channel rank|獨立空間層數受通道秩及訊雜比限制。~Independent spatial layers are limited by channel rank and SNR.
波束控制~Beam control|波束指向需要相位一致性與校準。~Beam pointing requires phase consistency and calibration.
傳輸網路~Transport network|前傳與回傳承載不同資料與延遲要求。~Fronthaul and backhaul carry different data and timing requirements.
基地台管理~Base-station management|配置版本須與固件及能力宣告匹配。~Configuration versions must match firmware and advertised capabilities.
干擾模型~Interference model|鄰站負載和頻率重用會改變 SINR。~Neighbor load and frequency reuse change SINR.
交遞邊界~Handover boundaries|覆蓋重疊與觸發門檻共同影響交遞中斷。~Coverage overlap and trigger thresholds jointly affect handover interruption.
熱與供電~Thermal and power budget|基頻及射頻負載會改变散熱與供電餘裕。~Baseband/RF load changes thermal and power margin.
合成驗收~Synthetic acceptance|每個功能切分要有自己的容量及時限驗收。~Each functional split needs its own capacity and deadline acceptance.
授權與版本~Authorization and versions|實際無線發射須依當地授權，本課僅離線建模。~Live RF transmission needs local authorization; this course models offline only.
''')
spec(343,'gpon xgs','住戶接取拓撲、光功率與共享容量~residential-access topology, optical power and shared capacity','假設 20 km 光纖損耗 0.25 dB/km、1:32 理想分光 15.05 dB、接頭 2 dB、餘裕 3 dB，總需 25.05 dB；須再核對實際分光器附加損耗。~Assume 20 km fiber at 0.25 dB/km, ideal 1:32 splitting at 15.05 dB, 2 dB connectors and 3 dB margin: budget=25.05 dB, before real splitter excess loss.', ['只改分光比，觀察損耗與共享容量。~Change split ratio and compare loss/shared capacity.','固定纖長，只改接頭衰減。~Fix fiber length and vary connector attenuation.','比較同步與突發住戶負載。~Compare synchronized and bursty household loads.','模擬單一 feeder 中斷的受影響住戶數。~Model households affected by one feeder outage.'], ['分光器把每個住戶都變成獨立全速鏈路。~A splitter provides an independent full-rate link to every household.','光功率高於靈敏度便保證所有上行時隙正常。~Power above sensitivity guarantees every upstream time slot works.'],'''
OLT 到 ONT~OLT-to-ONT topology|feeder、分光及 drop 段決定服務與故障範圍。~Feeder, splitting and drop segments define service/failure scope.
點對點與 PON~Point-to-point versus PON|專用纖與共享光樹具有不同容量及成本結構。~Dedicated fiber and shared trees have different capacity/cost structures.
光纖損耗~Fiber attenuation|以 dB/km 乘長度得到路徑損耗。~Attenuation in dB/km times length gives path loss.
分光损耗~Splitting loss|理想 N 路分光損耗為 10log10(N) dB。~Ideal N-way splitting loss is 10log10(N) dB.
連接點~Connection points|接頭與熔接附加損耗須獨立記帳。~Connector and splice excess losses need separate accounting.
功率窗口~Power window|接收靈敏度與過載端同時限制可用範圍。~Sensitivity and overload jointly bound usable received power.
上下行波長~Directional wavelengths|上下行波段分離支援共纖雙向傳輸。~Separated wavelength bands support bidirectional use of one fiber.
上行時分~Upstream timing|共享上行需要避免住戶突發互相重疊。~Shared upstream access must prevent overlapping subscriber bursts.
距離補償~Ranging compensation|量測傳播差異用於調整上行到達時刻。~Measured propagation differences adjust upstream arrival timing.
帶寬配置~Bandwidth allocation|需求分配影响共享流量公平性與等待時間。~Demand allocation affects fairness and waiting on shared capacity.
住戶服務映射~Subscriber mapping|實體光埠與訂閱服務須保持可追溯映射。~Physical optical ports and subscriptions need traceable mappings.
容量超售~Oversubscription|平均超售可行不代表同步尖峰可行。~Average oversubscription feasibility does not prove synchronized-peak feasibility.
備援光路~Protected paths|冗餘路徑若共用管道仍有共同故障。~Redundant paths sharing ducts retain common failures.
存量遷移~Installed-base migration|新舊波段共存需核對濾波與設備能力。~Old/new wavelength coexistence requires compatible filtering and devices.
假想量測~Hypothetical measurements|功率、錯誤率與服務可用性需分開記錄。~Record power, error rate and service availability separately.
維運交接~Operations handoff|竣工資料應連結纖路、接點及訂閱邊界。~As-built records connect fiber routes, joints and subscriber boundaries.
''')
spec(344,'gpon xgs','PON 收發機、突發模式與協議封裝~PON transceivers, burst modes and protocol framing','假設 10 Gbit/s 毛速率只有 85% 可給 payload，32 住戶均分理想值為 10×0.85/32=0.265625 Gbit/s；這不是產品額定或公平演算法保證。~With assumed 85% payload efficiency on 10 Gbit/s gross rate, equal sharing by 32 homes gives 0.265625 Gbit/s each; this is not a device rating or scheduler guarantee.', ['改單一 ONT 光功率，觀察突發動態範圍。~Vary one ONT power and observe burst dynamic range.','比較無 FEC 與有 FEC 的教學錯誤計數。~Compare synthetic error counts without/with FEC.','固定總需求，只改上行 grant 顆粒度。~Fix demand and vary upstream-grant granularity.','模擬 ONT 重新加入而不改其他訂閱。~Model ONT rejoin without changing other subscriptions.'], ['PON 接收端只需處理連續同功率資料。~PON receivers only handle continuous constant-power data.','FEC 能修正任意數量的位元錯誤。~FEC can correct any number of bit errors.'],'''
設備邊界~Equipment boundaries|OLT 與 ONT 擁有不同的發送及接收責任。~OLTs and ONTs have different transmission/reception responsibilities.
光模組規格~Optics specifications|波段、功率級及接收範圍要一同匹配。~Match wavelength, power class and receiving range together.
突發接收~Burst reception|不同 ONT 到達功率变化要求快速接收調整。~Varying ONT arrival power requires rapid receiver adjustment.
前導碼~Preambles|前導碼讓接收器取得時鐘及突發邊界。~Preambles establish clock recovery and burst boundaries.
距離量測~Ranging|不同距離的傳播時差须補償到達時隙。~Different-distance propagation delays require slot-arrival compensation.
上行 grant~Upstream grants|grant 決定允許傳送範圍，不能任意越過。~Grants define authorized transmission windows.
DBA 回饋~DBA feedback|需求回報延遲影响分配的即時性。~Demand-report delay limits allocation responsiveness.
封裝開銷~Framing overhead|毛資料率減封裝及保護開銷才是 payload 速率。~Payload rate subtracts framing/protection overhead from gross rate.
FEC 邊界~FEC limits|有限碼距限制可修正錯誤，需記錄前後錯誤率。~Finite code distance limits correction; record pre/post-FEC errors.
錯誤計數~Error counters|累積計數須搭配觀察時間及分母。~Cumulative error counts need observation time and denominators.
服務隔離~Service isolation|不同服務映射需避免住戶資料跨界。~Service mappings must prevent subscriber-data boundary crossings.
加密責任~Encryption responsibilities|鏈路加密不等於應用端到端機密性。~Link encryption is not application end-to-end confidentiality.
管理通道~Management channels|設備管理訊息與住戶 payload 的權限不同。~Management messages need permissions distinct from subscriber payload.
互通配對~Interoperability pairs|OLT/ONT 的選用功能需形成測試配對矩陣。~OLT/ONT optional features need paired interoperability tests.
故障定位~Fault localization|單一 ONT 錯誤与共享光樹故障應分開。~Separate single-ONT errors from shared-tree failures.
放行證據~Release evidence|距離、功率、負載及重啟條件須覆蓋驗收。~Acceptance must cover distance, power, load and restart conditions.
''')
spec(345,'otn submarine','相干接收、DSP 補償與光通道品質~coherent reception, DSP compensation and optical-channel quality','假設 32 GBd、DP-QPSK 共 4 bit/符號，毛速率 128 Gbit/s；20% 以毛速率為分母的開銷後 payload 為 102.4 Gbit/s。忽略成形與實際 FEC。~At assumed 32 GBd and DP-QPSK carrying four bits/symbol, gross rate=128 Gbit/s; overhead equal to 20% of gross leaves 102.4 Gbit/s, ignoring shaping and actual FEC.', ['保留調變，只改 OSNR。~Fix modulation and vary OSNR.','固定纖長，只改色散模型參數。~Fix distance and vary dispersion-model parameters.','比較不同雷射相位雜訊的假想星座。~Compare synthetic constellations at different laser phase-noise levels.','模擬降低調變階數的容量與餘裕交換。~Model capacity/margin tradeoff from lowering modulation order.'], ['相干 DSP 可無限恢復任何低功率訊號。~Coherent DSP can recover arbitrarily weak signals without limit.','提高調變階數一定提高每條實際光路容量。~Higher modulation order always raises actual path capacity.'],'''
相干量測~Coherent measurement|本地振盪光提供相位參考，不只是強度量測。~A local optical oscillator supplies phase reference, beyond intensity detection.
I/Q 訊號~I/Q signals|正交分量共同表達複數光場資訊。~Quadrature components jointly represent complex field information.
雙偏振~Dual polarization|兩個偏振可承載資料，但需補償相互混合。~Two polarizations carry data but require mixing compensation.
符號與位元~Symbols and bits|baud 與 bit/s 由調變及偏振數連接。~Baud and bit/s connect through modulation and polarization count.
OSNR~Optical signal-to-noise ratio|OSNR 需指定參考頻寬，不能無條件比較數字。~OSNR comparisons require the stated reference bandwidth.
色散補償~Dispersion compensation|色散使不同頻率成分傳播時間不同。~Dispersion gives frequency components different propagation times.
偏振解混~Polarization demultiplexing|等化器需追蹤偏振混合的變化。~Equalizers must track changes in polarization mixing.
載波回復~Carrier recovery|相位雜訊与頻率偏差要求不同回復機制。~Phase noise and frequency offset need distinct recovery treatment.
時鐘回復~Timing recovery|錯誤取樣時刻會擾動星座與等化。~Wrong sampling instants disturb constellations and equalization.
非線性代價~Nonlinear penalties|增加發送功率也會增加非線性影響。~Higher launch power can also increase nonlinear impairment.
調變取捨~Modulation tradeoffs|高階星座增加位元数亦提高品質要求。~Higher-order constellations add bits and quality requirements.
FEC 與 payload~FEC and payload|修正能力及開銷需與 net data rate 一起評估。~Assess correction capability, overhead and net rate together.
OTN 映射~OTN mapping|傳輸封裝為客戶訊號提供監測及承載邊界。~Transport framing provides monitoring and carriage boundaries for clients.
頻譜配置~Spectrum assignment|通道寬度及保護間隔限制可配置光譜。~Channel widths and guards constrain assignable spectrum.
品質餘裕~Quality margin|放行需最差路徑品質及老化餘裕。~Acceptance needs limiting-path quality and aging margin.
模式回退~Mode fallback|改變調變模式須同時核對双端及業務容量。~Mode changes require peer compatibility and service-capacity checks.
''')
spec(346,'submarine subtest otn','海底鏈路、放大器雜訊與維修可靠性~submarine links, amplifier noise and repair reliability','假想 6000 km 路線以 80 km 段切分，共 75 段；若每段損耗 16 dB，不能直接把 1200 dB 當作端到端淨損耗，因中間有放大且逐段累加雜訊。~A hypothetical 6000 km route at 80 km per span has 75 spans; 75×16=1200 dB is not net end-to-end loss when intermediate amplification restores signal and adds noise.', ['只改 span 長度，觀察段數與雜訊取捨。~Vary span length and compare span-count/noise tradeoffs.','固定通道數，只改發送功率。~Fix channels and vary launch power.','比較兩條共用岸站及分離岸站路線。~Compare routes with shared versus separate landing sites.','模擬一段停用對冗餘路由的服務影響。~Model service effects of one disabled segment under redundant routing.'], ['光放大器恢復功率便完全消除先前雜訊。~An optical amplifier restores power and removes all prior noise.','兩條海纜名稱不同便没有共同故障域。~Different cable names imply no common failure domains.'],'''
Wet plant 邊界~Wet-plant boundaries|海中纖、放大器與分支單元和岸端設備责任不同。~Submerged fibers, amplifiers and branches differ from terminal responsibilities.
纜路段數~Span counts|纜長與段長決定放大段數，不直接等於可靠性。~Length/span size determines span count, not reliability alone.
放大與雜訊~Amplification and noise|放大補功率且加入 ASE，不能視為無損。~Amplification restores power and adds ASE; it is not lossless.
通道功率~Channel powers|通道功率分配與总放大器限制須一起考慮。~Channel power allocation must respect total amplifier constraints.
非線性累積~Nonlinear accumulation|光纖非線性限制最佳發送功率。~Fiber nonlinearity constrains optimal launch power.
頻譜資源~Spectral resources|各纖對與通道提供不同容量配置邊界。~Fiber pairs and channels provide distinct allocation boundaries.
供電概念~Power-feeding concept|供電連續性是系統可靠性之一，本課不提供高壓操作。~Feed continuity affects reliability; this course provides no high-voltage procedures.
分支單元~Branching units|分支把纖路與服務拓撲連結，須追蹤配置。~Branches connect fiber routing to service topology and need tracked configuration.
岸站交接~Landing-station handoff|岸站與內陸回傳共構成服務路徑。~Landing and terrestrial backhaul jointly form the service path.
纜路多樣性~Route diversity|地理分離須考慮共同海域及岸端故障。~Geographic diversity includes shared marine regions and landing failures.
性能監測~Performance monitoring|錯誤與品質趨勢可協助辨識漸進退化。~Error/quality trends help distinguish progressive degradation.
測試邊界~Test boundaries|分段測試與端到端測試證明不同性質。~Segment and end-to-end tests establish different properties.
容量壽命~Capacity lifetime|初始容量與壽命末品質餘裕应分開评估。~Evaluate initial capacity separately from end-of-life quality margin.
維修時間~Repair times|可靠性報告須計入故障率與修復時間。~Reliability reports need both failure frequency and repair duration.
復原路由~Restoration routes|備援鏈路容量不足時只能恢復部分業務。~Insufficient backup capacity restores only part of the service.
交付證據~Delivery evidence|原始量測、纜路版本及限制需形成可追溯紀錄。~Measurements, route versions and limitations need traceable records.
''')
spec(347,'ground ccsds satcom','衛星鏈路預算、都卜勒與接收窗口~satellite link budgets, Doppler and contact windows','假設 2 GHz、1000 km 自由空間，FSPL=92.45+20log10(2)+20log10(1000)=158.47 dB；EIRP 50 dBW、接收增益 30 dBi、其他損失 2 dB，接收約 −80.47 dBW。~Assume 2 GHz over 1000 km: FSPL=158.47 dB; EIRP=50 dBW, receive gain=30 dBi and other losses=2 dB give approximately −80.47 dBW.', ['保留頻率，只改斜距與傳播損失。~Fix frequency and vary slant range/path loss.','固定距離，只改視線向相對速度。~Fix range and vary radial relative velocity.','比較不同仰角的假想遮蔽與大氣損失。~Compare synthetic blockage/atmospheric loss at different elevations.','模擬縮短接觸窗口對可傳資料量的影響。~Model reduced contact-window duration and transferable data.'], ['自由空間損失只取決於頻率，与距離無關。~Free-space loss depends only on frequency, not distance.','天線增益足夠就不需追蹤都卜勒。~Sufficient antenna gain eliminates Doppler tracking needs.'],'''
任務資料流~Mission data flows|遙測、任務資料與指令具有不同權限和時限。~Telemetry, mission data and commands have different permissions/deadlines.
軌道與可見性~Orbit and visibility|軌道幾何决定可見窗口與斜距。~Orbital geometry determines visibility windows and slant range.
自由空間損失~Free-space loss|FSPL 以距離及頻率的平方尺度增加。~FSPL increases with squared distance and frequency scales.
EIRP~Effective radiated power|EIRP 結合發射功率、損耗与天線增益。~EIRP combines transmitter power, losses and antenna gain.
接收 G/T~Receive G/T|天線增益與系統雜訊溫度共同決定接收品質。~Gain and system noise temperature jointly determine receiving quality.
指向誤差~Pointing error|窄波束提供高增益但對指向誤差更敏感。~Narrow beams offer gain but increase pointing sensitivity.
都卜勒移頻~Doppler shift|視線向相對速度使接收頻率偏移。~Radial relative velocity shifts received frequency.
取樣與同步~Sampling and synchronization|頻率、符號時鐘与框同步要分開建立。~Establish frequency, symbol timing and frame synchronization separately.
編碼與調變~Coding and modulation|碼率與調變共同影響 payload 及 Eb/N0 需求。~Code rate and modulation jointly affect payload and Eb/N0 requirements.
大氣損失~Atmospheric loss|降雨與仰角的影響依頻率與條件改變。~Rain/elevation effects vary with frequency and conditions.
接触排程~Contact schedules|可見時段不等於全段都能使用最大速率。~Visibility does not imply maximum rate throughout a contact.
緩存容量~Buffer capacity|窗口外產生資料需足够緩存或明確丟棄策略。~Out-of-contact data needs enough buffering or a defined discard policy.
地面網路~Ground network|地面回傳可成为衛星鏈路後端瓶頸。~Terrestrial backhaul may bottleneck the satellite downstream path.
指令驗證~Command authorization|通訊成功不等於指令獲授權。~Successful communication does not prove command authorization.
交接切換~Station handoff|跨站交接需連結時間、資料序列与責任。~Interstation handoff coordinates time, data sequence and responsibility.
授權邊界~Authorization boundaries|本課仅分析公開模型，不發射或操作真實衛星。~This course analyzes public models without transmitting or operating satellites.
''')
spec(348,'leo satcom ccsds','時變拓撲、交遞與星間路由~time-varying topology, handover and intersatellite routing','假想路徑四段各 1000 km 真空傳播，以 c≈300000 km/s，單向 13.33 ms；每跳處理 0.5 ms 四次加 2 ms，合為 15.33 ms，未計接取與排隊。~Four hypothetical 1000 km vacuum segments give 13.33 ms one-way at c≈300000 km/s; four 0.5 ms processing delays add 2 ms, totaling 15.33 ms before access/queuing.', ['保留星座，只改路徑代價權重。~Fix constellation and change routing-cost weights.','固定負載，只移除單一星間邊。~Fix load and remove one intersatellite edge.','比較只看當下與預先看接触變化的路由。~Compare present-only and contact-aware routing.','模擬交遞期間路由更新不一致。~Model inconsistent route updates during handover.'], ['最少跳數必然是最小延遲路徑。~Fewest hops necessarily means minimum latency.','衛星正在可見便保證所有星間鏈路存在。~Visible satellites guarantee all intersatellite links exist.'],'''
星座图~Constellation graph|節點位置與鏈路可用性都隨時間變化。~Node positions and link availability both vary over time.
星間與地面邊~Space and ground edges|星間邊與閘道邊具有不同容量及可見限制。~Intersatellite and gateway edges have different capacity/visibility constraints.
路徑代價~Path costs|跳數、距離、負載与穩定度是不同优化目標。~Hops, distance, load and stability are different optimization objectives.
傳播下限~Propagation bounds|幾何距離除光速給出傳播時間下限。~Geometric distance divided by light speed bounds propagation time.
接触預測~Contact prediction|已知軌道可預測窗口，但設備與天候仍可能偏離。~Known orbits predict windows; hardware/weather can still diverge.
交遞排程~Handover schedules|接取交遞与路由更新须協调，避免暫態黑洞。~Access handoff and route updates need coordination to avoid transient black holes.
負載分配~Load distribution|最短路徑集中可能產生排隊壅塞。~Shortest-path concentration can create queuing congestion.
分散狀態~Distributed state|過時拓撲資訊可能選到已消失的鏈路。~Stale topology can select vanished links.
路由迴圈~Routing loops|不同節點更新時間不一致可产生暫態迴圈。~Different update times can create transient loops.
壅塞控制~Congestion control|時變路徑延遲影响傳輸端的反馈判讀。~Changing path delay affects transport-feedback interpretation.
多路径取捨~Multipath tradeoffs|多路徑可分散負載但增加重排及狀態。~Multipath spreads load but adds reordering and state.
閘道多樣性~Gateway diversity|更多閘道改善選項，仍需可用地面回傳。~More gateways add options but still need available backhaul.
故障繞路~Failure detours|繞路後必须重新核對容量与延遲。~Detours require renewed capacity and latency checks.
服務優先~Service priorities|重要業務需明確資源策略，不只命名優先。~Critical services need explicit resource policies, not priority labels alone.
合成拓撲驗證~Synthetic-topology validation|固定種子及時間步可使假想路由重算。~Fixed seeds/time steps make synthetic routing reproducible.
性能報告~Performance reports|交遞丟包与穩態吞吐應分開呈現。~Report handover loss separately from steady-state throughput.
''')
spec(349,'bundle dtn ccsds','儲存攜帶轉送、接触計畫與資料壽命~store-carry-forward, contact plans and data lifetime','假設 4 Mbit/s 接触 600 s，可搬 2.4 Gbit=300 MB（十進位）；若每天產生 500 MB，且仅有一次接触，至少累積 200 MB/日，未計開銷。~A 4 Mbit/s contact lasting 600 s carries 2.4 Gbit=300 MB decimal; generating 500 MB/day with one daily contact grows backlog by at least 200 MB/day before overhead.', ['保留生成率，只改接触時長。~Fix generation rate and vary contact duration.','比較資料到期時間短於與長於無接触間隔。~Compare lifetimes shorter/longer than contact gaps.','固定接触表，只改緩存上限。~Fix contact plan and vary storage capacity.','模擬中間節點重啟後保留及丟失持久資料。~Model intermediary restart with preserved versus lost persistent data.'], ['Bundle Protocol 7 必定提供傳統 custody transfer。~Bundle Protocol 7 necessarily provides traditional custody transfer.','DTN 每一跳都必須與源端同時在線。~Every DTN hop must be online simultaneously with the source.'],'''
DTN 覆疊層~DTN overlay|DTN 跨連續與間歇網路建立儲存轉送服務。~DTN overlays continuous/intermittent networks with store-and-forward service.
Bundle 結構~Bundle structure|bundle 結合資料及跨延遲處理所需 metadata。~Bundles combine data with metadata needed across delayed handling.
端點識別~Endpoint identifiers|DTN 端點識別與當下 IP 位址不必一對一。~DTN endpoint identifiers need not map one-to-one to current IP addresses.
Convergence layer~Convergence layers|下層轉接器承載 bundle，與路由算法責任不同。~Adapters carry bundles; their responsibility differs from routing algorithms.
持久儲存~Persistent storage|轉送前保留資料需要掉電與容量假設。~Retaining data before forwarding needs power-loss and capacity assumptions.
接触計畫~Contact plans|窗口的開始、結束與速率限制可搬資料量。~Window start, end and rate bound transferable volume.
資料壽命~Data lifetime|到期後的資料不能仅因仍有儲存便視為有效。~Stored data is not valid merely because it remains after expiry.
儲存攜帶~Store-carry behavior|節點可等待未来接触，不需全路径同時存在。~Nodes can wait for future contacts without a simultaneous full path.
分片與重組~Fragmentation/reassembly|分片需保持識別与順序資訊以正确重組。~Fragments need identifying/order information for correct reassembly.
重複與重試~Duplicates and retries|重傳可能產生重複，應用要定义冪等處理。~Retransmission can duplicate data; applications need idempotent handling.
路由責任~Routing responsibilities|BPv7 定義 bundle，不指定唯一的 route computation。~BPv7 defines bundles, not a unique route-computation algorithm.
安全與應用~Security and applications|傳送可用性与授權、完整性是不同問題。~Delivery availability differs from authorization and integrity.
時基限制~Timebase limitations|壽命與年齡处理需核對時鐘可靠性。~Lifetime/age handling requires clock-reliability checks.
緩存水位~Storage occupancy|平均輸入大於平均输出時 backlog 長期增长。~Backlog grows when mean input exceeds mean output.
BP 版本差異~BP version differences|BPv7 與舊 BPv6 行為不能不經核對混用。~Do not mix BPv7 and older BPv6 behaviors without checking differences.
任務放行~Mission acceptance|需驗证中斷、到期與重啟，而非仅連續傳送。~Acceptance tests disruptions, expiry and restart, not just continuous delivery.
''')
spec(350,'qnet qnist','量子光鏈路、糾纏与古典控制平面~quantum optical links, entanglement and classical control planes','假設光损耗 20 dB，傳輸率 10^(−20/10)=0.01；每秒 10000 對、雙端偵測效率各 0.8，單臂承受此損耗的理想 coincidences=10000×0.01×0.8²=64/s，未计暗計数与死時間。~At 20 dB loss, transmission=0.01; with 10000 pairs/s and both detector efficiencies 0.8, one lossy arm gives ideal coincidences=64/s, excluding dark counts/dead time.', ['固定光源，只改單臂光損耗。~Fix source rate and vary one-arm loss.','保留損耗，只改暗計數与 coincidence 窗口。~Fix loss and vary dark counts/coincidence window.','比較有与没有古典時間標籤的資料。~Compare records with/without classical time tags.','模擬記憶保存時間短於協議等待時間。~Model memory lifetime shorter than protocol waiting time.'], ['量子位元可像古典封包任意複製重送。~Qubits can be freely copied and retransmitted like classical packets.','產生糾纏就能省略所有古典通訊。~Entanglement generation eliminates all classical communication.'],'''
量子與古典資源~Quantum/classical resources|量子狀態與古典控制資訊有不同複製限制。~Quantum states and classical control information have different copying constraints.
不可複製原理~No-cloning principle|未知量子態無法一般性完美複製。~Unknown quantum states cannot generally be copied perfectly.
單光子損耗~Single-photon loss|損耗降低成功事件率，不能靠普通光放大還原未知態。~Loss reduces success rates; ordinary amplification cannot restore unknown states.
糾纏分發~Entanglement distribution|糾纏建立需要可定義成功事件与品質。~Entanglement establishment needs defined success events and quality.
Coincidence~Coincidence measurements|時間窗口影響真實與偶然 coincidence 比例。~Timing windows affect true versus accidental coincidence ratios.
暗計數~Dark counts|没有光子的探測事件也可能污染品質估計。~Detection without photons can contaminate quality estimates.
偵測效率~Detection efficiency|雙端有效率乘積限制可觀測配對事件。~The product of endpoint efficiencies limits observed paired events.
時間標籤~Time tags|共同時基或校準关联有助配對遠端事件。~Shared/calibrated timing helps associate remote events.
古典控制~Classical control|量子協議仍需交換量測結果与成功訊息。~Quantum protocols still exchange outcomes and success messages classically.
量子記憶~Quantum memories|保存時間須涵蓋等待与協議回饋延遲。~Memory lifetime must cover waiting and protocol-feedback delay.
交換與中繼~Swapping and repeaters|糾纏交換不是一般古典封包交換。~Entanglement swapping differs from ordinary packet switching.
保真度~Fidelity|成功率高與狀態品質高是不同指標。~High success rate and high state quality are different metrics.
共纖雜訊~Coexistence noise|古典光通道可能以散射雜訊影响量子通道。~Classical optical channels can affect quantum channels through scattering noise.
QKD 與量子網~QKD versus quantum networks|密鑰分發是一種用途，不等於通用量子網路。~Key distribution is one use, not a universal quantum network.
可重現模擬~Reproducible simulation|機率事件需要樣本数与不確定度，不只一次成功。~Probabilistic events need sample counts/uncertainty, not one success.
平台驗收~Testbed acceptance|光損耗、時間误差与狀態品质須分別交付。~Report optical loss, timing error and state quality separately.
''')
spec(351,'zt identity','資源導向授權、政策決策与持續證據~resource-centric authorization, policy decisions and continuous evidence','假想撤銷同步需 30 s、授權快取最長 60 s，最差残留許可窗口可達 90 s；此为兩延遲相加的保守假設，不表示任何實作都採此值。~Assumed revocation propagation of 30 s plus 60 s authorization caching gives a conservative possible 90 s residual-access window; these are not implementation defaults.', ['固定使用者，只改裝置健康證據是否新鮮。~Fix user and vary device-health evidence freshness.','保留政策，只改資源敏感度。~Fix policy and vary resource sensitivity.','比較撤銷前後快取授權結果。~Compare cached decisions before/after revocation.','模擬政策服務不可用的 fail-closed 與受控例外。~Model unavailable policy service with fail-closed and governed exceptions.'], ['內網位址足以證明應授予存取。~An internal address is sufficient proof of access entitlement.','零信任等於每個請求都要求使用者手動再登入。~Zero trust means manual login on every request.'],'''
資源盤點~Resource inventory|先界定保護資源與動作，才有可审查的政策。~Define protected resources/actions before reviewable policy.
主體身分~Subject identities|人、服務及裝置身分需要各自生命週期。~People, services and devices need distinct identity lifecycles.
決策與執行~Decision versus enforcement|政策決策與攔截執行應分開验证。~Verify policy decision and enforcement separately.
最小權限~Least privilege|授權范围應對應特定任务而非長期全權。~Permission scope should match tasks rather than permanent total access.
裝置證據~Device evidence|健康狀態是有时效的證據，不是永遠可信標籤。~Health is time-limited evidence, not a permanent trust label.
情境條件~Context conditions|時間及風險條件應明確定義來源与限制。~Time/risk conditions need explicit sources and limitations.
網路分區~Network segmentation|分區限制可達性，但不能取代資源授權。~Segmentation restricts reachability, not resource authorization.
工作負載身分~Workload identities|服務间调用须驗证服務身分与可做動作。~Interservice calls need identity and action authorization.
政策快取~Policy caching|快取降低延遲亦延長撤銷生效窗口。~Caching lowers latency but can extend revocation windows.
持續评估~Continuous evaluation|狀態變更可觸發重评估，不等于只在登入判断。~State changes can trigger reevaluation beyond initial login.
權限撤銷~Revocation|撤銷需涵蓋既有 session、token 与快取。~Revocation covers active sessions, tokens and caches.
服務不可用~Service unavailability|失去决策服務時需要预先核准的降階政策。~Decision-service loss needs preapproved degradation policy.
例外生命週期~Exception lifecycle|例外要有範圍、期限与審批記錄。~Exceptions need scope, expiry and approval records.
审計关联~Audit correlation|决策与執行日誌需可关联同一请求。~Decision/enforcement logs must correlate the same request.
合成政策測試~Synthetic policy tests|允許与拒絕樣本都需要验证。~Validate both allowed and denied synthetic cases.
迁移验收~Migration acceptance|逐资源遷移需确认旧旁路也被关闭。~Resource-by-resource migration checks closure of old bypass paths.
''')
spec(352,'identity oauth zt','身分生命週期、聯邦與權限模型~identity lifecycle, federation and authorization models','假想 2000 人各 8 個直接權限關係共有 16000 邊；若 20 角色各 30 權限並每人 2 角色，需 600+4000=4600 邊，但角色設計仍可能過度授權。~2000 people with eight direct grants create 16000 edges; 20 roles with 30 grants plus two roles/person create 4600 edges, but role design may still overgrant.', ['固定使用者，只改角色集合。~Fix users and vary role sets.','比較正常與錯誤 audience 的假想 token。~Compare synthetic tokens with correct/incorrect audiences.','保留組織，只改離職撤銷時點。~Fix organization and vary leaver-revocation timing.','模擬身分提供者失效後的受控恢复。~Model controlled recovery after identity-provider failure.'], ['驗證成功自動授予所有資源权限。~Successful authentication automatically grants every resource.','顯示名稱可以代替不可變主體識別碼。~Display names can replace immutable subject identifiers.'],'''
身分證明~Identity proofing|聲稱身分与验证聲稱的证据需要分开。~Separate claimed identity from evidence validating that claim.
唯一識別~Stable identifiers|不可變識別碼避免改名造成權限混淆。~Immutable identifiers prevent rename-related authorization confusion.
入轉離~Joiner-mover-leaver|入職、轉調與離職都會改变授權需求。~Joining, moving and leaving all change authorization needs.
驗證与授權~Authentication/authorization|驗證回答是誰，授權回答能做什么。~Authentication identifies subjects; authorization permits actions.
角色模型~Role models|RBAC 降低重複配置，但角色组合仍需審核。~RBAC reduces repeated configuration; role combinations still need review.
屬性模型~Attribute models|ABAC 依屬性决策，属性来源必须可信且新鲜。~ABAC relies on attributes whose sources must be trusted/current.
职责分離~Separation of duties|互斥權限限制單人完成高風險鏈。~Conflicting-grant constraints limit single-person high-risk chains.
聯邦界线~Federation boundaries|聯邦断言与本地資源授權并非同一責任。~Federated assertions differ from local resource authorization.
Issuer 与 audience~Issuer and audience|token 需匹配可信簽发者与預期接收者。~Tokens must match trusted issuers and intended audiences.
OAuth 範圍~OAuth scopes|scope 限制授權範圍，不是使用者全部身份證明。~Scopes constrain delegated access, not complete identity proof.
Session 生命周期~Session lifecycle|登入 session 与 access token 有不同有效期限。~Login sessions and access tokens have different lifetimes.
服務帳號~Service accounts|非人身分也需要所有者與撤銷責任。~Nonhuman identities need owners and revocation responsibility.
權限複核~Access reviews|複核要確認必要性，而不只勾選仍存在。~Reviews check necessity, not merely continued existence.
復原邊界~Recovery boundaries|帳號復原不可成為較弱的长期登入旁路。~Recovery must not become a weaker permanent login path.
审计隐私~Audit privacy|审计應記錄必要識別而限制敏感資料。~Audit necessary identifiers while limiting sensitive information.
离职验收~Leaver acceptance|移除登入權仍需检查 token、金鑰與共享秘密。~Login removal also checks tokens, keys and shared secrets.
''')
spec(353,'identity webauthn','驗證因子、抗網釣与安全復原~authentication factors, phishing resistance and secure recovery','假設六位數等機率碼為 1000000 種，最多 5 次猜測的成功率上界 5/1000000=0.0005%；未考慮被窃取、重放或有偏分布，不能据此评估整体 MFA 安全。~A uniform six-digit code has 1000000 values; five guesses bound success at 0.0005%, excluding theft, replay and biased generation and not measuring total MFA security.', ['比較两个知识因子與不同类别因子。~Compare two knowledge factors with distinct factor categories.','固定帳號，只改 challenge 新鮮度。~Fix account and vary challenge freshness.','比較正确与错误 RP ID 的合成记录。~Compare synthetic records with correct/incorrect RP IDs.','模擬遗失驗證器的受控复原。~Model controlled recovery after authenticator loss.'], ['密码加另一个密码必定是双因素。~A password plus another password is necessarily two-factor authentication.','所有 OTP 都具备抗网钓性。~Every OTP method is phishing-resistant.'],'''
因子分類~Factor categories|知識、持有与生物特徵代表不同因子類別。~Knowledge, possession and biometrics are distinct factor categories.
因子獨立~Factor independence|兩個驗證步驟未必来自独立因子。~Two verification steps need not represent independent factors.
认证保证~Authentication assurance|所需保証应由资源风险决定。~Required assurance should follow resource risk.
一次性碼~One-time codes|一次性要求有效期、重用拒绝与猜測限制。~One-time use needs lifetime, reuse rejection and guess limits.
Challenge 新鮮度~Challenge freshness|挑战应关联当前请求并防止重放。~Challenges bind current requests and prevent replay.
WebAuthn 範圍~WebAuthn scope|公鑰凭据受 RP 範圍限制。~Public-key credentials are scoped to relying parties.
RP ID 与 origin~RP ID and origin|origin 与 RP 范围核对防止凭据跨站误用。~Origin/RP checks prevent cross-site credential misuse.
用户验证~User verification|用户在场与用户驗证是不同声明。~User presence and user verification are different claims.
同步 passkey~Synced passkeys|同步改善復原選項，也引入同步帳號邊界。~Sync improves recovery options and introduces sync-account boundaries.
装置绑定~Device binding|装置绑定与跨装置同步提供不同部署取捨。~Device-bound and synchronized credentials offer different tradeoffs.
伺服器儲存~Server storage|伺服器保存公鑰，不应取得驗證器私鑰。~Servers retain public keys, not authenticator private keys.
降阶途徑~Downgrade paths|較弱備援方式可能限制整体保护能力。~Weaker fallback methods can limit overall protection.
失落復原~Loss recovery|復原需可审查证明与告警，不只是容易操作。~Recovery needs reviewable proof and alerts, not convenience alone.
速率限制~Rate limits|限制猜測應考慮裝置、帳號与可用性。~Guess limits consider devices, accounts and availability.
可近用性~Accessibility|替代驗證应維持风险要求并支援多种需求。~Alternative methods preserve risk requirements while supporting diverse needs.
撤销验收~Revocation acceptance|移除驗證器须防止其凭据继续通过驗证。~Removing an authenticator must invalidate its continuing verification.
''')
spec(354,'pki keys tls','信任錨、憑證路徑与撤銷~trust anchors, certificate paths and revocation','假想根→中繼→葉三張憑證，驗证两个非自签链边各需 1.2 ms，合为 2.4 ms；還需名稱、用途、時間、撤销检验，不能把它当成总 TLS 握手时间。~A root→intermediate→leaf path with two non-self-signed edges at 1.2 ms verification each costs 2.4 ms, excluding name, usage, time, revocation checks and total TLS handshake time.', ['固定鏈，只改葉憑證有效時間。~Fix chain and vary leaf validity.','比較正确与错误名稱约束。~Compare correct/incorrect name constraints.','保留憑证，只改信任錨集合。~Fix certificates and vary trust-anchor sets.','模拟中繼撤销对下层叶证书的影响。~Model intermediate revocation affecting leaves.'], ['链上签章都正确便不需检查名稱與用途。~Valid signatures remove the need for name/usage checks.','自簽憑证因自簽就自动可信。~A self-signed certificate is automatically trusted.'],'''
信任锚~Trust anchors|信任锚来自策略配置，不由自簽本身建立。~Trust anchors come from policy configuration, not self-signing alone.
根与中繼~Roots and intermediates|中繼限制簽发责任并降低根鍵使用频率。~Intermediates scope issuance and reduce root-key use.
葉憑证~Leaf certificates|葉证书将主體、用途及公鑰关联。~Leaf certificates associate subjects, usages and public keys.
路徑建構~Path building|可能存在多路径，建构与验证责任不同。~Multiple paths may exist; construction and validation differ.
簽章验证~Signature validation|簽章完整性只是路径验证的一部分。~Signature integrity is only part of path validation.
名称核对~Name checks|預期服務名称须依适用规则匹配凭证标识。~Expected service names must match identifiers under applicable rules.
有效時間~Validity time|时钟錯誤会影响 NotBefore/NotAfter 判讀。~Clock errors affect NotBefore/NotAfter interpretation.
Basic constraints~Basic constraints|CA 标誌與路径长约束限制簽發鏈。~CA flags and path-length constraints limit issuance chains.
Key usage~Key usage|允许用途不应由密鑰能否運算来猜測。~Permitted usage is not inferred merely from computational capability.
名稱约束~Name constraints|上层约束应在下层路径继续生效。~Ancestor constraints remain effective down the path.
撤销资料~Revocation data|撤销状态需记录来源、新鲜度及不可用策略。~Revocation status needs source, freshness and unavailability policy.
私鍵保護~Private-key protection|憑证公开不表示关联私鍵可公开。~Public certificates do not make associated private keys public.
簽發稽核~Issuance audits|簽發请求与批准证据应关联具体版本。~Issuance requests/approvals must correlate concrete versions.
鏈更新~Chain updates|更换中繼需确认旧客戶端的信任相容。~Intermediate changes require old-client trust compatibility checks.
緊急吊銷~Emergency revocation|事故撤销需兼顾传播时间与替换部署。~Incident revocation considers propagation and replacement deployment.
驗收矩陣~Validation matrix|有效、過期、錯名与錯用途案例都要测。~Test valid, expired, wrong-name and wrong-usage cases.
''')
spec(355,'hsm cmvp keys','金鑰不可匯出、模組邊界与授權操作~nonexportable keys, module boundaries and authorized operations','假設單次簽章平均 2 ms，單串行通道理想上限 500 次/s；300 次/s 到達时利用率 60%，排队与 API 开销会使實際吞吐降低。~A hypothetical 2 ms signature averages an ideal 500/s serial channel; arrivals at 300/s imply 60% utilization before queues and API overhead.', ['固定鍵，只改调用身份的权限。~Fix keys and vary caller privileges.','比较只签章與允许匯出的对象政策。~Compare sign-only and export-enabled object policies.','固定请求率，只改 API 延迟。~Fix request rate and vary API latency.','模拟备援模組不可用及核准恢复。~Model standby-module unavailability and approved recovery.'], ['使用 HSM 會自动修复所有应用授权错误。~An HSM automatically repairs all application authorization errors.','FIPS 验证表示任意部署配置都已获验证。~FIPS validation certifies every possible deployment configuration.'],'''
模組边界~Module boundaries|安全模組邊界与应用进程边界不同。~Security-module and application-process boundaries differ.
Token 与 session~Tokens and sessions|PKCS #11 的 token 对象与 session 状态需区分。~Distinguish PKCS #11 token objects from session state.
对象属性~Object attributes|签章、解密与匯出许可是不同属性。~Signing, decryption and export permissions are distinct attributes.
鍵生成位置~Key-generation location|在模块内生成可避免明文鍵离开保护边界。~In-module generation can avoid plaintext keys leaving the boundary.
不匯出策略~Nonexportability|不可匯出降低外流路径，但不阻止被授權滥用。~Nonexportability reduces exfiltration paths, not authorized misuse.
Mechanism 配对~Mechanism matching|算法 mechanism 与键型及參數須相容。~Algorithms must match key types and parameters.
登入角色~Login roles|管理角色与应用操作角色应分離。~Administrative and application-operation roles should differ.
雙人控制~Dual control|关键管理動作可要求多名独立批准者。~Critical management actions may require independent approvers.
签章请求~Signing requests|保护键不代表任意传入资料都应签章。~Protecting a key does not authorize signing arbitrary inputs.
密钥包装~Key wrapping|包装保护搬移资料，也须明確导出策略。~Wrapping protects transported material and needs explicit export policy.
容量与排队~Capacity and queues|端到端延迟包括 API、网络及模块队列。~End-to-end delay includes API, network and module queues.
高可用~High availability|備援要保持鍵与策略一致，而非只有两台盒子。~Failover needs consistent keys/policies, not just two boxes.
备份恢復~Backup recovery|可恢复性需要独立验证批准与保管链。~Recoverability needs independently verified approvals and custody.
稽核事件~Audit events|成功操作及拒绝操作都应可关联请求。~Successful and rejected operations need request correlation.
验证状态~Validation status|模块证书范围与当前版本模式必须核对。~Check certification scope against current version/mode.
退役验证~Retirement verification|退役须確認秘密清除与备份处置。~Retirement verifies secret clearing and backup disposition.
''')
spec(356,'keys hsm','密鑰状态、期限与受控更换~key states, lifetimes and controlled rotation','假想每月新建 100 把資料鍵、每鍵 256 bit，原始鍵材每月 3200 byte；索引、包裝与审计通常更多，不能用 3.2 kB 推算完整 KMS 儲存。~Creating 100 assumed 256-bit data keys monthly produces 3200 bytes of raw key material; metadata, wrapping and audits add storage, so 3.2 kB is not total KMS storage.', ['固定资料，只改钥的 active/retired 状态。~Fix data and vary active/retired key states.','比较更换资料鍵与更换包裝鍵。~Compare rotating data keys with wrapping keys.','保留算法，只改資料保存年限。~Fix algorithms and vary data retention years.','模拟一个鍵遭撤销后的历史资料读取。~Model historical reads after one key is revoked.'], ['輪替鍵必須删除所有旧資料才能成功。~Key rotation requires deleting all old data.','加密資料有备份就代表解密金鑰可恢复。~Backing up ciphertext guarantees key recovery.'],'''
资产关联~Asset associations|每把鍵应有关联資料、用途与责任人。~Each key needs associated data, purpose and owner.
状态机~Key state machine|预启用、启用与停用的操作资格不同。~Preactive, active and deactivated keys have different operation permissions.
键类型~Key types|资料加密鍵与包裝鍵应分开管理。~Manage data-encryption and wrapping keys separately.
熵与生成~Entropy and generation|鍵材需要合适随机來源，不等于可预测编号。~Key material needs suitable randomness, not predictable identifiers.
分發通道~Distribution channels|鍵分發要維持来源与機密性。~Key distribution must preserve origin and confidentiality.
密碼期间~Cryptoperiods|使用期限依用途与风險，不能只看位元数。~Cryptoperiods depend on purpose/risk, not bit length alone.
版本識別~Version identifiers|密文需能找到正确的鍵版本。~Ciphertext must identify the correct key version.
包絡加密~Envelope encryption|包裝键保护资料鍵，建立两层生命周期。~Wrapping keys protect data keys, creating two lifecycles.
輪替范围~Rotation scope|更換包裝键与重新加密全部資料成本不同。~Rewrapping and reencrypting all data have different costs.
撤销与销毁~Revocation/destruction|禁止新用与永久销毁是不同状態。~Disallowing new use and permanent destruction are distinct states.
恢復策略~Recovery policies|解密鍵恢复需求须与数据保留相容。~Decryption-key recovery must align with data retention.
访问权限~Access permissions|取得鍵清单不应等于取得解密權。~Listing keys should not imply decryption permission.
事故范围~Incident scope|遭泄露键关联哪些资料必须可追溯。~Trace which data a compromised key protects.
備份一致性~Backup consistency|备份密文、鍵版本与包裝資料应可配對。~Backed-up ciphertext, key versions and wrappers must match.
密码敏捷~Crypto agility|算法變更需要格式、标識与相容策略。~Algorithm changes need formats, identifiers and compatibility plans.
销毁证明~Destruction evidence|删除索引不等于所有备份秘密已被清除。~Deleting an index does not clear every backed-up secret.
''')
spec(357,'acme tls pki','域名授權、憑證續期与部署一致性~domain authorization, certificate renewal and deployment consistency','假想憑证有效 90 日、到第 60 日开始续期，可用续期窗口 30 日；若每 12 h 尝试，理想有 60 次机会，不能假设这些尝试独立或都成功。~An assumed 90-day certificate renewed from day 60 leaves 30 days; attempts every 12 h give 60 nominal opportunities, not necessarily independent or successful.', ['固定域名，只改 challenge 回应是否正确。~Fix domain and vary challenge response validity.','比較已签发但未部署与已部署憑证。~Compare issued-but-undeployed versus deployed certificates.','固定有效期，只改续期服务中断时长。~Fix validity and vary renewal-service outage duration.','模拟双节点不同链版本的轮替。~Model two nodes rotating inconsistent chain versions.'], ['签发成功表示所有服务节点已更新。~Successful issuance proves every service node is updated.','取得憑证等于取得网站全部业务授权。~Obtaining a certificate grants all website business permissions.'],'''
ACME 角色~ACME roles|客户端、帐户与 CA 之间有不同对象责任。~Clients, accounts and CAs have different object responsibilities.
帐户凭據~Account credentials|ACME 帐户鍵与 TLS 服务私鍵并不相同。~ACME account keys differ from TLS service private keys.
Order 状态~Order states|order 状态记录授权与签发進度。~Order states track authorization and issuance progress.
域名授权~Domain authorization|挑战验证控制能力，不是法律所有权证明。~Challenges validate control, not legal ownership.
Challenge 类型~Challenge types|不同挑战要求不同可达性或 DNS 控制。~Different challenges need different reachability/DNS control.
CSR 与鍵~CSR and keys|CSR 请求关联公鑰；私鍵應保持受控。~CSRs associate public keys; private keys remain controlled.
名称覆盖~Name coverage|憑证的名称范围必须与部署服務一致。~Certificate names must match deployed services.
憑证鏈~Certificate chains|需要部署客户端可验证的完整中繼链。~Deploy the intermediate chain needed by verifying clients.
续期时机~Renewal timing|续期应保留故障恢复时间，不等到到期瞬间。~Renewal needs recovery margin before expiry.
Rate limits~Rate limits|重试须符合 CA 限制，不能无限密集重复。~Retries respect CA limits rather than unlimited repetition.
部署原子性~Atomic deployment|鍵与憑证需匹配且避免半更新状态。~Keys/certificates must match and avoid partial updates.
服务重載~Service reload|磁碟文件更新不保证进程已使用新鏈。~Updated files do not prove running processes use the new chain.
监测到期~Expiry monitoring|到期监测应读取实际服务的憑证。~Expiry monitoring inspects certificates actually served.
事故撤销~Incident revocation|私鍵事故需处理撤销及替代部署。~Private-key incidents need revocation and replacement deployment.
回滚边界~Rollback boundaries|回滚旧证书仍需有效、未撤销且私鍵可信。~Rollback needs valid, unrevoked certificates and trusted keys.
TLS 版本核对~TLS-version checks|2026 年 RFC 9846 已取代 8446；實作仍需逐版本核对。~RFC 9846 supersedes 8446 in 2026; implementations need version-specific checks.
''')
spec(358,'kem dsa slhdsa keys','後量子演算法角色、資產盤點与遷移~post-quantum algorithm roles, inventory and migration','ML-KEM-768 的公鑰為 1184 byte、ciphertext 為 1088 byte，合計傳輸鍵材為 2272 byte。二者通常在不同方向／協議訊息傳送，不能當成單一 IP 封包；每份鍵材本身均小於假想 1500 byte MTU，仍須逐訊息計入協議標頭並區分 MTU 與 TCP MSS。~ML-KEM-768 has a 1184-byte public key and 1088-byte ciphertext, totaling 2272 bytes of key-establishment material. They normally travel in different directions/messages, not one IP packet; each alone is below an assumed 1500-byte MTU. Evaluate actual message framing and distinguish MTU from TCP MSS.', ['固定安全目标，只改 KEM 与簽章用途。~Fix goals and compare KEM versus signature roles.','比較原有握手与加入大鍵材的傳输尺寸。~Compare legacy handshakes with larger key-material sizes.','固定算法，只改资料需保密年限。~Fix algorithms and vary required confidentiality lifetime.','模擬不支持新格式客戶端的受控遷移。~Model controlled migration for clients lacking new formats.'], ['ML-KEM 直接提供任意长度资料的数字簽章。~ML-KEM directly signs arbitrary-length data.','使用后量子演算法就自动排除實作侧信道。~Post-quantum algorithms automatically remove implementation side channels.'],'''
风险時間線~Risk timelines|长保存秘密需考虑今天收集未来解密风险。~Long-lived secrets need harvest-now/decrypt-later risk analysis.
密码盤点~Cryptographic inventory|須找出算法、协议、鍵格式与依賴。~Inventory algorithms, protocols, key formats and dependencies.
KEM 角色~KEM roles|KEM 建立共同秘密，不等于直接签署訊息。~KEM establishes shared secrets, not direct message signatures.
簽章角色~Signature roles|簽章验证来源完整性，不提供资料加密。~Signatures verify origin/integrity, not data encryption.
ML-KEM~ML-KEM|ML-KEM 是 FIPS 203 的模组格 KEM。~ML-KEM is the module-lattice KEM standardized in FIPS 203.
ML-DSA~ML-DSA|ML-DSA 是 FIPS 204 的模组格簽章。~ML-DSA is the module-lattice signature standardized in FIPS 204.
SLH-DSA~SLH-DSA|SLH-DSA 使用无状态哈希签章并有不同尺寸取捨。~SLH-DSA uses stateless hash signatures with different size tradeoffs.
安全類別~Security categories|類別与算法用途要分别核对，不能只比较名稱。~Check categories and algorithm roles separately, not names alone.
資料尺寸~Material sizes|公鑰、ciphertext 与簽章各自影响网络与储存。~Public keys, ciphertexts and signatures affect network/storage differently.
Hybrid 边界~Hybrid boundaries|组合方案须有明确协议与失败语义。~Combined schemes need explicit protocol and failure semantics.
協議互通~Protocol interoperability|演算法支持不代表握手格式相容。~Algorithm support does not prove handshake-format compatibility.
侧信道~Side channels|数学安全模型不涵盖所有实现泄漏。~Mathematical security models do not cover every implementation leak.
验证向量~Validation vectors|已知答案测试验证實作，不能证明所有路径无錯。~Known-answer tests verify implementations, not every execution path.
遷移試点~Migration pilots|試点应先定义成功、回退與不可降階条件。~Pilots define success, rollback and forbidden downgrade conditions.
长期资料~Long-lived data|資料保密期間与憑证有效期不是同一数值。~Data-confidentiality lifetime differs from certificate validity.
标准更新~Standard updates|正式部署須核對勘误与固定版本文件。~Production checks errata and pinned document versions.
''')
spec(359,'spf dkim dmarc dmarcagg dmarcfail','郵件身份、網域對齊與隔離判讀~mail identity, domain alignment and quarantine analysis','假想每日 10000 封、100 封惡意；規則偵測 90 封且誤標正常信 99 封，precision=90/(90+99)=47.62%，recall=90%。高 recall 仍可能有大量誤攔。~Of 10000 hypothetical messages, 100 malicious, detecting 90 with 99 benign false alarms gives precision=47.62% and recall=90%; high recall can coexist with many false blocks.', ['固定郵件內容，只改 envelope 與 From 網域。~Fix content and vary envelope/From domains.','比較簽章後內容被改動與未改動的合成記錄。~Compare synthetic records with/without post-signature modification.','保留規則，只改惡意比例。~Fix rules and vary malicious prevalence.','模擬隔離郵件的核准釋放與追蹤。~Model approved quarantine release and tracking.'], ['SPF 通過表示郵件所有內容必定安全。~SPF pass proves all message content safe.','DKIM 通過永遠等於與可見 From 對齊。~DKIM pass always means alignment with visible From.'],'''
Envelope 與 From~Envelope and From|傳輸寄件身分與可見 From 可能不同。~Transport sender identity can differ from visible From.
SPF 邊界~SPF boundaries|SPF 驗證網域授權發送 IP，不分析全部內容。~SPF checks domain-authorized sending IPs, not all content.
轉寄效應~Forwarding effects|轉寄可能改變來源 IP 與驗證條件。~Forwarding can change source IP and validation conditions.
DKIM 簽章~DKIM signatures|DKIM 保護選定欄位及正文雜湊。~DKIM protects selected fields and body hashes.
Canonicalization~Canonicalization|正規化規則限制哪些格式變化保持有效。~Canonicalization governs which formatting changes retain validity.
DMARC 對齊~DMARC alignment|DMARC 需要驗證通過與 From 網域對齊。~DMARC needs authentication success plus From-domain alignment.
政策階段~Policy stages|觀察、隔離與拒收是不同部署階段。~Monitoring, quarantine and rejection are distinct deployment stages.
報告資料~Reporting data|彙總与逐封失敗報告範圍不同；須最小化個資并核對来源。~Aggregate and per-message failure reports differ; minimize personal data and verify provenance.
附件分析~Attachment analysis|附件判讀與寄件網域驗證各自提供證據。~Attachment analysis and domain authentication provide separate evidence.
URL 判讀~URL analysis|顯示文字與實際目的地應分開檢查。~Check display text separately from actual destinations.
隔離生命週期~Quarantine lifecycle|隔離釋放須有批准、期限與稽核。~Quarantine release needs approval, expiry and audit.
假陽性代價~False-positive costs|攔截正常信可能破壞業務，須量化影響。~Blocking benign mail can harm operations; quantify the effect.
Precision 與 recall~Precision and recall|誤標與漏標的分母不同。~False alerts and missed detections have different denominators.
郵件流邊界~Mail-flow boundaries|內部與外部郵件應明確定義不同檢查路徑。~Define internal/external mail inspection paths explicitly.
例外到期~Exception expiry|白名單應有用途及期限，不永久放行。~Allowlists need purpose and expiry, not permanent bypass.
驗收資料集~Acceptance datasets|資料集須包含正常業務變體與合成異常。~Datasets need benign business variants and synthetic anomalies.
''')
spec(360,'asvs crs tls','應用控制、防護規則與正常流量驗證~application controls, protection rules and benign-traffic validation','假想每秒 2000 請求，每請求純檢查消耗平均 0.4 ms CPU 時間（不是含等待的經過時間），需求為 0.8 CPU-s/s；單核心理想利用率 80%，未計 TLS、排隊與多執行緒額外成本。~Assume 2000 requests/s and 0.4 ms CPU time per inspection, not elapsed time including waits: demand is 0.8 CPU-s/s, an ideal 80% single-core load before TLS, queues and additional threading costs.', ['固定規則，只改正常輸入的格式變體。~Fix rules and vary benign input formatting.','比較有與沒有來源端授權檢查的本地模型。~Compare local models with/without origin authorization.','固定流量，只改規則數量與處理成本。~Fix traffic and vary rule count/processing cost.','模擬規則更新後可審查的回滾。~Model reviewable rollback after a rule update.'], ['部署 WAF 後就不需應用端授權。~A WAF removes the need for application authorization.','增加拒絕率必然代表安全性提高。~Higher rejection rates necessarily mean greater security.'],'''
應用資產~Application assets|先界定資料與動作，才可驗證保護要求。~Define data/actions before verifying protection requirements.
信任邊界~Trust boundaries|跨邊界輸入須依格式与用途驗證。~Boundary-crossing input needs format/purpose validation.
授權責任~Authorization responsibilities|WAF 不知道所有業務物件權限。~WAFs do not know every business-object permission.
輸入格式~Input formats|正規化與解析次序可能改變檢查結果。~Normalization/parsing order can change inspection results.
規則範圍~Rule scopes|每條規則需要適用路徑與內容型別。~Each rule needs applicable paths and content types.
異常分數~Anomaly scores|分數門檻是判定策略，不是攻擊成功機率。~Score thresholds are decision policies, not attack-success probabilities.
False positive~False positives|合法變體誤攔應以業務案例重現。~Reproduce benign false blocks with business cases.
Rate limiting~Rate limiting|限制請求率需區分共享來源与單一使用者。~Request limits distinguish shared sources from individual users.
TLS 終結~TLS termination|解密位置改變可觀察性与秘密處理邊界。~Decryption placement changes visibility and secret-handling boundaries.
原站保護~Origin protection|入口防護需避免未受控旁路直達原站。~Ingress protection needs closure of uncontrolled origin bypasses.
回應資料~Response data|輸出洩漏控制與輸入檢查責任不同。~Output-leak controls differ from input inspection.
記錄遮罩~Log redaction|日誌不應保存完整密碼或敏感 token。~Logs should not retain full passwords or sensitive tokens.
檢測與封鎖~Detection versus blocking|先觀察可協助調校，但不等於已阻止流量。~Observation aids tuning but does not imply blocking.
規則版本~Rule versions|版本、例外与測試集應共同保存。~Preserve rule versions, exceptions and datasets together.
回滾決策~Rollback decisions|回滾需列明安全代價及恢復條件。~Rollback decisions specify security cost and restoration conditions.
防護驗收~Protection acceptance|正常、邊界与合成異常案例均需覆蓋。~Acceptance covers benign, boundary and synthetic anomaly cases.
''')
spec(361,'sysmon attack ir','端點事件、偵測證據與核准回應~endpoint events, detection evidence and approved response','假想 200 端點每秒 5 事件、每事件 500 byte，共 500000 byte/s=0.5 MB/s，每日 43.2 GB（十進位）；未計索引、壓縮及複本。~200 endpoints at 5 events/s each and 500 bytes/event yield 0.5 MB/s and 43.2 GB/day decimal before indexes, compression and replicas.', ['固定事件，只改程序父子關係。~Fix events and vary parent-child relationships.','比較感測器啟用與離線時的證據缺口。~Compare evidence gaps with active/offline sensors.','保留規則，只改正常管理活動比例。~Fix rules and vary benign administrative activity.','模擬核准隔離後的服務影響。~Model service impact after approved endpoint isolation.'], ['沒有告警即可證明端點沒有異常。~No alerts prove an endpoint has no anomalies.','ATT&CK 技術名稱本身就是可執行的偵測規則。~An ATT&CK technique name is itself an executable detection rule.'],'''
端點覆蓋~Endpoint coverage|感測器缺失會產生不可觀測區域。~Missing sensors create unobservable regions.
程序事件~Process events|程序名稱需搭配路徑、父節點与身分。~Process names need paths, parent processes and identities.
檔案事件~File events|檔案變化與執行證據提供不同資訊。~File changes differ from execution evidence.
網路事件~Network events|連線紀錄不一定包含應用內容。~Connection records need not contain application content.
時間排序~Time ordering|時鐘偏差會擾亂跨端點事件順序。~Clock skew disrupts cross-endpoint event order.
行為脈絡~Behavior context|同一操作在管理與異常情境可有不同意義。~The same action can mean different things in administrative/anomalous contexts.
技術映射~Technique mapping|ATT&CK 映射組織觀察，不替代具體規則。~ATT&CK mappings organize observations, not concrete rules.
規則資料需求~Rule data requirements|偵測依賴必要欄位及採樣覆蓋。~Detection depends on required fields and sampling coverage.
偵測窗口~Detection windows|窗口過短可能漏掉慢事件，過長增加誤配。~Short windows miss slow events; long windows increase false association.
證據保存~Evidence preservation|調查前後需保持來源與完整性紀錄。~Maintain provenance/integrity records throughout investigation.
告警分級~Alert severity|嚴重度需結合資產与證據可信度。~Severity combines asset impact and evidence confidence.
核准隔離~Approved isolation|隔離會影響業務，須有預先授權及恢復。~Isolation impacts operations and needs prior authorization/recovery.
感測器健康~Sensor health|事件停止可能是感測器失效而非環境正常。~Stopped events may indicate sensor failure, not normality.
隱私最小化~Privacy minimization|只收必要資料並限制調查存取。~Collect necessary data and limit investigative access.
受控回放~Controlled replay|本課用自行合成事件，不執行惡意程式。~This course uses authored synthetic events, not malware execution.
回應驗收~Response acceptance|需驗證偵測、決策、核准与恢復全鏈。~Verify detection, decision, approval and recovery end to end.
''')
spec(362,'logs ir attack','日誌正規化、事件關聯與可用性~log normalization, event correlation and availability','假想每日 100 GB 原始事件，保留 30 日得 3 TB；兩複本得 6 TB，若索引另外 20% 得 7.2 TB；未計壓縮，容量假設須逐項標示。~Assume 100 GB/day for 30 days: 3 TB raw; two replicas require 6 TB, plus 20% indexing gives 7.2 TB before compression, with all assumptions explicit.', ['固定事件，只改時區及時間偏差。~Fix events and vary timezones/clock offsets.','比較同一主體的不同名稱映射。~Compare different name mappings for one subject.','固定規則，只改匯入延遲。~Fix rules and vary ingestion delay.','模擬事件儲存中斷与緩衝回補。~Model storage outage and buffered recovery.'], ['把所有日誌集中便能自動判斷事故。~Centralizing every log automatically identifies incidents.','相同顯示名稱一定代表同一主體。~Matching display names always identify the same subject.'],'''
來源盤點~Source inventory|事件來源應有責任人、格式與健康指標。~Sources need owners, formats and health indicators.
收集通道~Collection channels|傳輸完整性与來源認證影響證據可靠性。~Transport integrity/source authentication affect evidence reliability.
欄位正規化~Field normalization|一致欄位需保留原始值与轉換規則。~Normalized fields retain originals and transformation rules.
事件時間~Event time|事件發生時間與收集時間是不同欄位，應分別記錄，數值可能恰好相同。~Event occurrence time and collection time are distinct fields and must be recorded separately.
時區與偏差~Timezone and skew|時區轉換不能消除設備本身時鐘偏差。~Timezone conversion does not remove device clock skew.
身分關聯~Identity correlation|主體關聯需穩定識別，而非僅名稱。~Correlate stable subject identifiers, not names alone.
資產脈絡~Asset context|關鍵性与所有者支援告警分級。~Criticality and ownership support alert triage.
關聯窗口~Correlation windows|時間窗口影響漏關聯与誤關聯。~Time windows affect missed/false associations.
重複事件~Duplicate events|重送會增加計數，須保留去重依據。~Resends inflate counts; preserve deduplication criteria.
資料保存~Retention|保存期限需依調查、成本与隱私需求。~Retention follows investigation, cost and privacy needs.
查詢效能~Query performance|索引加速查詢但增加儲存與寫入成本。~Indexes speed queries but add storage/write cost.
告警品質~Alert quality|規則品質需精確率、召回率及工作量。~Rule quality needs precision, recall and analyst workload.
偵測缺口~Detection gaps|來源中斷要當作健康事件處理。~Source outages need health-event handling.
事件流程~Incident workflow|告警與已確認事故不是同一狀態。~Alerts and confirmed incidents are different states.
存取稽核~Access audits|讀取敏感日誌也應有最小權限與記錄。~Sensitive-log access needs least privilege and auditing.
復原驗收~Recovery acceptance|回補須檢查遺漏、重複与原始時間。~Backfill checks missing data, duplicates and original timestamps.
''')
spec(363,'suricata attack logs','網路可觀察性、協議解碼與告警品質~network visibility, protocol decoding and alert quality','假想 100000 流中 200 異常；偵測 160、正常誤報 100，precision=160/260=61.54%、recall=80%。資料分布改變時這些比率亦改變。~Among 100000 hypothetical flows with 200 anomalies, 160 detections and 100 false positives give precision=61.54% and recall=80%; distribution shifts change these values.', ['固定事件，只改鏡像點位置。~Fix events and vary mirror placement.','比較只有流量摘要与完整合成協議記錄。~Compare flow summaries with complete synthetic protocol records.','保留規則，只改加密比例。~Fix rules and vary encrypted-traffic share.','模擬感測器丟包导致的證據缺口。~Model sensor packet loss and resulting evidence gaps.'], ['IDS 能直接讀取所有 TLS 加密內文。~An IDS directly reads every TLS-encrypted payload.','封包數沒有遺漏便保證應用解析完全正確。~Complete packet counts guarantee correct application parsing.'],'''
觀察點~Observation points|觀察位置決定看見哪些方向與流量。~Observation placement determines visible directions/traffic.
鏡像完整性~Mirror completeness|鏡像埠可能超載並丟包。~Mirror ports can overload and drop packets.
流識別~Flow identification|五元組与時間範圍一起界定流。~Five-tuples and time ranges jointly identify flows.
重組假設~Reassembly assumptions|亂序及缺包會限制可解析內容。~Reordering and missing packets limit parsable content.
協議解碼~Protocol decoding|協議辨識不能只依埠號。~Protocol identification cannot rely solely on port numbers.
加密邊界~Encryption boundaries|加密限制內文觀察，metadata 證據仍有範圍。~Encryption limits payload visibility; metadata evidence remains bounded.
規則條件~Rule conditions|規則需匹配實際可收集欄位。~Rules must match fields actually collected.
基線模型~Baseline models|正常變異應由代表性資料估計。~Estimate benign variability from representative data.
異常與事故~Anomaly versus incident|偏離基線不自動等於已確認入侵。~Baseline deviation is not automatically confirmed intrusion.
偵測門檻~Detection thresholds|低門檻可增加召回也增加誤報。~Lower thresholds can raise recall and false positives.
低基準率~Low base rates|異常稀少時少量誤報亦降低 precision。~Rare anomalies allow modest false alarms to reduce precision.
效能限制~Performance limits|解析成本與流量峰值須在容量中計入。~Capacity must include parsing cost and traffic peaks.
告警關聯~Alert correlation|告警需與身分、端點及時間證據互證。~Corroborate alerts with identity, endpoint and timing evidence.
受控資料~Controlled data|實作只使用自行生成資料或獲授權檔案。~Labs use authored synthetic data or authorized files only.
規則版本~Rule versions|固定版本及設定才能重現判斷。~Pinned versions/configurations enable reproducible decisions.
盲點報告~Blind-spot reporting|報告應列明未觀察區域而非聲稱全部防護。~Report unobserved regions rather than claiming complete protection.
''')
spec(364,'ot zt logs','OT 區域、通道与不中斷的防禦證據~OT zones, conduits and non-disruptive defensive evidence','假想 12 區原本任意雙向連通，共 12×11=132 有向關係；核准流程只需 18 關係，減少 114 個允許方向。這只衡量可達性，不能當作風險降低百分比。~Twelve fully connected zones have 132 directed relationships; approved flows need 18, removing 114 allowed directions. This measures reachability, not a percentage risk reduction.', ['固定設備，只改核准流矩陣。~Fix equipment and vary approved-flow matrices.','比較管理与程序控制通道的權限。~Compare management/process-control conduit permissions.','保留規則，只改維護例外期限。~Fix rules and vary maintenance-exception expiry.','模擬隔離失效與預先定義的安全降階。~Model isolation failure and predefined safe degradation.'], ['OT 安全可以不考慮可用性与人身安全。~OT security can ignore availability and physical safety.','VLAN 名稱不同即證明所有跨區流量已受控。~Different VLAN names prove all interzone flows are controlled.'],'''
OT 資產邊界~OT asset boundaries|控制器、感測与工程站有不同安全需求。~Controllers, sensing and engineering stations have different needs.
程序依賴~Process dependencies|網路中斷可能影響物理程序。~Network disruption can affect physical processes.
區域定義~Zone definitions|區域按功能与風險組合，不僅按樓層。~Zones group function/risk, not merely floors.
通道定義~Conduit definitions|跨區通道應對應必要業務流。~Interzone conduits should map required operational flows.
流矩陣~Flow matrices|來源、目的、方向与協議共同限定規則。~Source, destination, direction and protocol constrain rules.
IT/OT 介面~IT/OT interfaces|緩衝區降低直達性，但需明確資料交接。~DMZs reduce direct reachability but need explicit data handoffs.
遠端維護~Remote maintenance|維護需批准、限時与可歸屬身分。~Maintenance needs approval, time bounds and attributable identity.
管理通道~Management conduits|設備管理不應混用程序控制權限。~Management should not share process-control privileges indiscriminately.
被動盤點~Passive inventory|被動觀察減少干擾，但可能漏掉離線資產。~Passive observation reduces disruption but can miss offline assets.
協議限制~Protocol limitations|舊協議可能缺少身分与完整性保護。~Legacy protocols may lack identity/integrity protection.
單向資料~Unidirectional data|單向需求須檢查應用是否仍需回覆。~One-way requirements must check application reply dependencies.
變更窗口~Change windows|變更需在核准窗口与已驗證回滾下進行。~Changes need approved windows and validated rollback.
補丁取捨~Patch tradeoffs|補丁需符合設備相容与程序驗證。~Patches need equipment compatibility and process validation.
事件保存~Event preservation|日誌應記錄區域、通道与時基限制。~Logs record zones, conduits and timing limitations.
安全降階~Safe degradation|網路防禦不能替代正式程序安全設計。~Network defense does not replace formal process-safety design.
離線驗收~Offline acceptance|本課使用流矩陣模擬，不扫描真實工控設備。~This course simulates flow matrices without scanning live OT equipment.
''')
spec(365,'identity dtls keys rats','裝置根信任、佈建与憑據更新~device roots of trust, provisioning and credential renewal','假想 100000 裝置各每日驗證一次，平均 1.1574 次/s；若全於 10 min 內集中，為 166.67 次/s，平均流量不足以規劃驗證尖峰。~100000 devices authenticating once/day average 1.1574/s; concentrating them into 10 minutes gives 166.67/s, so averages do not size authentication peaks.', ['固定裝置，只改凭據是否唯一。~Fix devices and vary credential uniqueness.','比較有效與已撤銷的合成憑據。~Compare valid/revoked synthetic credentials.','保留算法，只改裝置可用時鐘品質。~Fix algorithms and vary device-clock quality.','模擬离線期間續期与受控恢復。~Model renewal during offline periods and controlled recovery.'], ['所有裝置共用一把秘密最容易稽核且無風險。~One shared fleet secret is easily audited and risk-free.','遠端證明可直接取代所有應用授權。~Remote attestation directly replaces every application authorization.'],'''
裝置識別~Device identifiers|序號是識別，不一定提供密码学验证。~Serial numbers identify devices but need not authenticate cryptographically.
唯一凭據~Unique credentials|個別憑據限制單裝置事故的擴散范围。~Per-device credentials limit the scope of one-device compromise.
根信任~Roots of trust|根信任界定最早可依據的驗證基礎。~Roots of trust define initial verifiable foundations.
安全佈建~Secure provisioning|初始身分需與實際裝置及所有者关联。~Initial identity must bind the device and owner.
秘密儲存~Secret storage|受保護儲存與應用讀取權限须分開。~Protected storage differs from application-read permissions.
共同验证~Mutual authentication|裝置与服務各自確認對方身分。~Devices and services each authenticate the peer.
DTLS 边界~DTLS boundaries|資料報安全仍需处理重排与重傳。~Datagram security still handles reordering/retransmission.
時鐘限制~Clock limitations|低品質時鐘會影響有效期判讀。~Poor clocks affect validity-window interpretation.
新鮮挑戰~Fresh challenges|挑戰回應应證明當下參與而非重播舊值。~Challenge responses prove current participation, not replayed values.
遠端證明~Remote attestation|證明報告須檢驗新鮮度及預期測量。~Attestation checks freshness and expected measurements.
佈建角色~Provisioning roles|製造、部署与維運可能由不同責任人完成。~Manufacturing, deployment and operations may have different owners.
憑据輪替~Credential rotation|更新需考慮離線裝置与雙版本過渡。~Renewal considers offline devices and dual-version transitions.
撤销傳播~Revocation propagation|離線狀態會延後裝置取得撤銷資訊。~Offline states delay device receipt of revocation data.
舰队峰值~Fleet bursts|集中開機造成驗證尖峰而非平均負載。~Synchronized boot creates authentication bursts, not average load.
退役處置~Decommissioning|轉移所有權需移除舊秘密与綁定。~Ownership transfer removes old secrets/bindings.
證據驗收~Evidence acceptance|唯一性、時效、拒絕与復原都須測試。~Test uniqueness, freshness, rejection and recovery.
''')
spec(366,'vehicle r155 logs','車載訊息、被動觀測与安全責任~vehicle messages, passive observation and safety responsibility','假想每秒 5000 訊框、每框平均含 160 bit（含教學開銷假設），在 1 Mbit/s 匯流排佔 80%；這不是所有 CAN 訊框長度，實際 bit stuffing 與仲裁需另計。~Assume 5000 frames/s at 160 bits/frame including teaching overhead: load on 1 Mbit/s bus=80%; actual CAN frame lengths, stuffing and arbitration need separate treatment.', ['固定訊框，只改時間間隔模式。~Fix frames and vary interarrival patterns.','比較正常診斷与未批准診斷的合成事件。~Compare authorized/unauthorized synthetic diagnostic events.','保留規則，只改匯流排負載。~Fix rules and vary bus load.','模擬監測器失效對告警覆蓋的影響。~Model monitor failure and alert-coverage effects.'], ['看到 CAN ID 就能證明發送裝置身分。~A CAN ID proves the transmitting device identity.','資安監測可取代全部功能安全驗證。~Cybersecurity monitoring replaces all functional-safety validation.'],'''
車載功能圖~Vehicle function maps|動力、車身与資訊娛樂具不同风险與時限。~Powertrain, body and infotainment have different risks/deadlines.
訊息識別~Message identifiers|訊息 ID 通常表示類別而非密码学發送身分。~Message IDs usually identify message classes, not cryptographic senders.
仲裁與優先~Arbitration and priority|優先規則影响等待，不等于身份授权。~Priority affects waiting, not identity authorization.
匯流排負載~Bus load|負載估計需含訊框与協議開銷。~Load estimates include frames and protocol overhead.
週期基線~Periodic baselines|正常週期會随驾驶与模式变化。~Normal periods change with driving/operational modes.
數值范围~Value ranges|超范围與不合物理变化率是不同证据。~Out-of-range values differ from implausible change rates.
跨信號关系~Cross-signal relations|相關訊號可互證但不能假定永久線性。~Related signals corroborate but need not be permanently linear.
閘道邊界~Gateway boundaries|跨域閘道應限制可轉送訊息与角色。~Domain gateways constrain forwarded messages/roles.
診斷權限~Diagnostic permissions|診斷服务有授權、时限与状态要求。~Diagnostics need authorization, timing and state constraints.
OTA 完整性~OTA integrity|更新来源与版本验证不同于下載成功。~Update origin/version verification differs from download success.
記錄與隱私~Logs and privacy|行程与识别资料需最小化与受控存取。~Minimize and control access to journey/identity data.
告警延遲~Alert latency|告警延迟應低于情境需要而非只看平均。~Alert delay should satisfy context, not only average performance.
误報處置~False-alert handling|错误阻断可能影响安全，回应须经设计审查。~False blocking can affect safety; review responses formally.
安全責任~Safety responsibilities|資安與功能安全交互但不能互相替代。~Cybersecurity and functional safety interact without replacing each other.
管理系統~Management systems|R155 管理要求不是單一感測器产品规格。~R155 management requirements are not a single-sensor specification.
合成驗收~Synthetic acceptance|本課只分析自製記錄，不連接或注入真實車輛。~This course analyzes authored records without connecting/injecting into vehicles.
''')
spec(367,'sev rats keys','記憶體保護、遠端證明与秘密釋放~memory protection, remote attestation and secret release','假想證明 15 ms、驗證 5 ms、秘密傳送 10 ms，串行初始化合 30 ms；若每秒 100 次初始作業且不可並行，每秒需 3 s 處理，單通道不足。~Assumed attestation=15 ms, verification=5 ms and secret transfer=10 ms give 30 ms serial initialization; 100 starts/s require 3 processing-seconds/s, exceeding one serial channel.', ['固定工作负载，只改预期测量值。~Fix workloads and vary expected measurements.','比较新鲜与重放的证明记录。~Compare fresh/replayed attestation records.','保留证据，只改信任策略版本。~Fix evidence and vary trust-policy version.','模拟 host 攻击面之外的应用授权缺陷。~Model application authorization flaws beyond the host-protection scope.'], ['机密運算使应用自身所有错误自动消失。~Confidential computing automatically removes every application bug.','證明報告存在便证明其测量值得信任。~The existence of an attestation report proves its measurements trusted.'],'''
威胁模型~Threat models|先定義不信任 host 的哪些能力与保護目標。~Define distrusted-host capabilities and protection goals first.
保護邊界~Protection boundaries|保護来宾記憶體不等於保護所有外部 I/O。~Protecting guest memory does not protect every external I/O path.
記憶體加密~Memory encryption|加密与完整性保護是不同性質。~Encryption and integrity protection are distinct properties.
受測工作負載~Measured workloads|測量值須代表可審查版本及配置。~Measurements represent reviewable versions/configurations.
Attester~Attesters|產生證據的角色与判断可信的角色不同。~Evidence generation differs from trust evaluation.
Verifier~Verifiers|驗證器依背書、參考值及策略評估證據。~Verifiers assess evidence using endorsements, references and policy.
Relying party~Relying parties|依賴方使用驗證結果做具体授权。~Relying parties use appraisal results for concrete authorization.
新鮮性~Freshness|nonce 或可靠时间把报告关联當前会话。~Nonces/reliable time bind reports to current sessions.
背書鏈~Endorsement chains|厂商背書链须与受支持硬体版本匹配。~Vendor endorsement chains must match supported hardware versions.
參考值~Reference values|合法測量值來自核准發行，不由報告自行宣告。~Approved releases define trusted measurements, not self-declaration.
秘密釋放~Secret release|只對满足策略且建立安全通道的工作负载释放。~Release secrets only to policy-compliant workloads over secure channels.
軟體更新~Software updates|新版本測量改變需要同步更新参考政策。~New-version measurements need reference-policy updates.
回滾限制~Rollback limits|舊版本虽曾合法，也可能因漏洞不再获准。~Once-approved old versions may later be prohibited for vulnerabilities.
I/O 邊界~I/O boundaries|資料离开保护记忆体后仍需通道與應用保护。~Data leaving protected memory still needs channel/application protection.
側信道限制~Side-channel limits|保護模型不能自动涵盖所有时间与流量泄漏。~Protection models do not automatically cover all timing/traffic leakage.
部署验收~Deployment acceptance|需測試错误測量、过期证明与授权拒绝。~Test wrong measurements, stale reports and authorization rejection.
''')
source('5gc','5GS 架構 TS 23.501 V19.8.0','5GS architecture TS 23.501 V19.8.0','3GPP / ETSI','https://www.etsi.org/deliver/etsi_ts/123500_123599/123501/19.08.00_60/ts_123501v190800p.pdf')
source('5gsec','5GS 安全 TS 33.501 V19.5.0','5GS security TS 33.501 V19.5.0','3GPP / ETSI','https://www.etsi.org/deliver/etsi_ts/133500_133599/133501/19.05.00_60/ts_133501v190500p.pdf')
source('ran','NR 架構 TS 38.300 V18.4.0','NR architecture TS 38.300 V18.4.0','3GPP / ETSI','https://www.etsi.org/deliver/etsi_ts/138300_138399/138300/18.04.00_60/ts_138300v180400p.pdf')
D['a339']['src']=['5gc','5gsec','sa2']
D['a340']['src']=['oran','oranres','5gsec','ran']
D['a341']['src']=['5gc','5gsec','zt']
D['a342']['src']=['ran','5gsec','ptp']
del S['5g']

# Explicit editorial normalization, kept in stdlib so rebuilding needs no service.
CHAR_PAIRS='与與 专專 业業 两兩 个個 临臨 为為 举舉 义義 书書 乱亂 争爭 于於 云雲 产產 仅僅 从從 优優 会會 传傳 伪偽 体體 偿償 关關 内內 决決 准準 凭憑 则則 删刪 别別 务務 动動 励勵 势勢 区區 协協 单單 厂廠 压壓 参參 双雙 发發 变變 叠疊 号號 后後 启啟 响響 团團 围圍 图圖 场場 块塊 声聲 处處 备備 复複 够夠 夹夾 学學 实實 审審 宽寬 对對 导導 寿壽 将將 层層 属屬 帐帳 带帶 帧幀 并並 库庫 应應 开開 异異 当當 录錄 征徵 径徑 忆憶 怀懷 态態 总總 恶惡 户戶 执執 扩擴 扫掃 护護 报報 拟擬 拥擁 拦攔 择擇 挡擋 挥揮 损損 换換 据據 摆擺 数數 断斷 无無 旧舊 时時 显顯 暂暫 机機 权權 条條 来來 构構 标標 样樣 气氣 没沒 测測 涨漲 满滿 滥濫 潜潛 点點 烟煙 爱愛 状狀 独獨 现現 电電 疗療 盐鹽 监監 盗盜 码碼 确確 碍礙 离離 种種 称稱 稳穩 窃竊 笼籠 签簽 类類 约約 级級 纽紐 线線 组組 终終 络絡 绝絕 统統 缓緩 缩縮 网網 联聯 舰艦 节節 范範 获獲 蓝藍 虑慮 虚虛 虽雖 补補 装裝 观觀 览覽 触觸 计計 认認 让讓 议議 记記 讲講 许許 设設 证證 评評 识識 译譯 该該 详詳 语語 误誤 说說 读讀 调調 负負 责責 质質 贮貯 贸貿 资資 趋趨 踪蹤 转轉 软軟 载載 较較 输輸 边邊 达達 迁遷 过過 运運 还還 这這 进進 远遠 连連 迟遲 适適 选選 邻鄰 释釋 鉴鑑 钓釣 钟鐘 钥鑰 铅鉛 链鏈 销銷 错錯 键鍵 长長 闭閉 阈閾 队隊 际際 险險 随隨 隐隱 静靜 页頁 项項 须須 预預 频頻 题題 风風 飞飛 馈饋 验驗 骤驟 鱼魚'.split()
# Ignore identities; no opaque identifiers or URLs pass through this normalizer.
TRANS={ord(p[0]):p[1] for p in CHAR_PAIRS if len(p)==2 and p[0]!=p[1]}
def T(s):
 for a,b in [('恢复','恢復'),('准确','準確'),('获准','獲准'),('获得','獲得'),('裝置艦隊','裝置群'),('舰队','裝置群'),('回應','回應'),('回复','回覆'),('复原','復原'),('复用','重用'),('响应','回應'),('固件','韌體'),('软件','軟體'),('硬件','硬體'),('消息','訊息'),('信息','資訊'),('程序','程序'),('代码','程式碼'),('舰队','裝置群'),('后续','後續'),('原始数據','原始數據')]:s=s.replace(a,b)
 return s.translate(TRANS).replace('獲準','獲准').replace('核準','核准').replace('批準','批准')
for d in D.values():
 for key in ('focus','example'):d[key]=(T(d[key][0]),d[key][1])
 for key in ('perturb','mis'):d[key]=[(T(z),e) for z,e in d[key]]
 d['units']=[((T(z),e),(T(m),me)) for (z,e),(m,me) in d['units']]
for s in S.values():
 for key in ('title','scope','imageReuse'):s[key]=T(s[key])
source('nistplace','NIST 公開校區資訊','NIST public campus information','NIST','https://www.nist.gov/about-nist/visit')
source('ituplace','ITU 官方地址','ITU official address','ITU','https://www.itu.int/en/about/Pages/contact.aspx')
source('etsiplace','ETSI 官方地址','ETSI official address','ETSI','https://www.etsi.org/about/contact/')
source('ieeeplace','IEEE SA 官方地址','IEEE SA official address','IEEE SA','https://standards.ieee.org/about/contact/')
source('esaplace','ESA ESOC 官方地址','ESA ESOC official address','European Space Agency','https://www.esa.int/About_Us/ESOC/Getting_here')
source('ciscoplace','Cisco 官方地址','Cisco official address','Cisco','https://www.cisco.com/site/us/en/about/contact-cisco/index.html')
PL={
 'nist':('NIST 公開校區代表點','NIST public-campus reference','蓋瑟斯堡','Gaithersburg','美國','United States',39.1305,-77.2185,'100 Bureau Drive, Gaithersburg, MD 20899, USA','nistplace'),
 'itu':('ITU 標準機構代表點','ITU standards-institution reference','日內瓦','Geneva','瑞士','Switzerland',46.2208,6.1375,'Place des Nations, 1211 Geneva 20, Switzerland','ituplace'),
 'etsi':('ETSI 標準機構代表點','ETSI standards-institution reference','索菲亞安蒂波利斯','Sophia Antipolis','法國','France',43.6169128,7.0528493,'650 Route des Lucioles, 06560 Valbonne, France','etsiplace'),
 'ieee':('IEEE SA 標準機構代表點','IEEE SA standards-institution reference','皮斯卡特韋','Piscataway','美國','United States',40.5509,-74.4584,'445 Hoes Lane, Piscataway, NJ 08854, USA','ieeeplace'),
 'esa':('ESA ESOC 公開機構代表點','ESA ESOC institutional reference','達姆施塔特','Darmstadt','德國','Germany',49.8708,8.6222,'Robert-Bosch-Strasse 5, 64293 Darmstadt, Germany','esaplace'),
 'cisco':('Cisco 公開總部代表點','Cisco public-headquarters reference','聖荷西','San Jose','美國','United States',37.3200,-121.9494,'3098 Olsen Drive, San Jose, CA 95128, USA','ciscoplace')}
PM={n:('ieee' if n in (336,337) else 'cisco' if n==338 else 'etsi' if 339<=n<=342 else 'itu' if 343<=n<=346 else 'esa' if 347<=n<=349 else 'nist') for n in range(335,368)}
# Every relation is within this authored group; reciprocal traversal is available.
R={335:[357,359],336:[337,342],337:[336,364],338:[352,353],339:[340,341],340:[339,342],341:[339,351],342:[340,336],343:[344,345],344:[343,345],345:[344,346],346:[345,348],347:[348,349],348:[347,349],349:[348,350],350:[349,358],351:[352,364],352:[353,351],353:[352,365],354:[357,355],355:[356,367],356:[355,358],357:[354,335],358:[354,350],359:[335,360],360:[351,363],361:[362,363],362:[361,364],363:[362,360],364:[351,366],365:[353,367],366:[364,361],367:[355,365]}
ST=[('需求、元件與基本模型','Requirements, components and baseline models'),('介面、狀態與資源配置','Interfaces, states and resource allocation'),('驗證、故障與防禦邊界','Validation, faults and defensive boundaries'),('效能、復原與證據交接','Performance, recovery and evidence handoff')]
def ids(d):return [S[k]['id'] for k in d['src']]
def ref(s):return {k:s[k] for k in ['title','titleEn','publisher','url']}
def place(n):
 p=PL[PM[n]]
 return {'name':p[0],'nameEn':p[1],'city':p[2],'cityEn':p[3],'country':p[4],'countryEn':p[5],'lat':p[6],'lng':p[7],'address':p[8],'addressEn':p[8],'mapQuery':p[8],'coordinateScope':'官方機構地址附近的近似代表點；非本課專屬設備、製造地、可進入位置或發明地。','coordinateScopeEn':'Approximate reference near an official institutional address, not course-specific hardware, a manufacturing site, an accessible facility or an invention site.'}
def make_step(cid,d,ui,phase,prev):
 (zh,en),(m,me)=d['units'][ui];(nz,ne),(nm,nme)=d['units'][(ui+1)%16]
 p,pe=d['perturb'][ui//4];model=phase==0;seq=ui*2+phase+1;sid=f'{cid}-v11-{seq:02d}';qidx=ui%3
 instructions=(f'觀看師傅的功能示意後，以「{zh}」為中心標出輸入、輸出、信任或資源邊界，並在學徒工作台排列資料流或元件。原理是：{m} 使用自行編寫的兩組小型資料或試算表，建立基準與一次只改一項的對照：{p} 先寫出可被反駁的預測；把「{nz}」視為相鄰問題，說明它如何影響模型而不能混同。數值只採本課假想算例或自訂並列明單位；本步保存架構圖、假設表與預測。' if model else f'重播本單元示意，讀取自製的基準與擾動紀錄，不接觸未授權目標。對照「{m}」，執行下列紙上或本地合成資料試驗：{p} 分開記錄預測、觀察與不確定度，再提出至少兩個可能原因；利用「{nz}」的獨立證據排除一個原因。若結果只來自模型，標記為模擬，不能當作真實設備量測。最後說明目前應接受、保留或拒絕哪一項要求，並保存可重算資料。')
 instructionsEn=(f'After the mentor functional diagram, mark inputs, outputs and trust/resource boundaries around {en.lower()}, then arrange components or data flows in the apprentice workspace. Principle: {me} Create two small authored datasets or spreadsheet cases: a baseline and a one-variable change. {pe} Predict a falsifiable outcome before evaluating it. Treat {ne.lower()} as a neighboring issue and explain its influence without conflating them. Use only the stated hypothetical case or declared assumed inputs/units. Save the architecture, assumptions and prediction.' if model else f'Replay the unit diagram and inspect your authored baseline/perturbed records without accessing unauthorized targets. Evaluate the principle: {me} Conduct this paper or local synthetic-data experiment: {pe} Record prediction, observation and uncertainty separately, propose two competing causes and use independent evidence from {ne.lower()} to exclude one. Model outputs must remain labeled simulation, not physical measurements. Explain which requirement to accept, hold or reject and retain recomputable records.')
 question=f'針對「{zh}」的原理與可觀測性，哪項最直接成立？';questionEn=f'Which statement most directly explains the principle/observability of {en.lower()}?'
 wrong1=d['mis'][ui%2];wrong2=(f'只檢查「{nz}」，便可取代「{zh}」的專屬驗證。',f'Checking {ne.lower()} alone replaces verification specific to {en.lower()}.')
 opts=[wrong1[0],wrong2[0]];optsEn=[wrong1[1],wrong2[1]];opts.insert(qidx,m);optsEn.insert(qidx,me)
 k=[{'id':sid+'-k1','title':'原理、架構與適用邊界','titleEn':'Principle, architecture and applicability','text':m,'textEn':me,'sourceIds':ids(d)},{'id':sid+'-k2','title':'相鄰機制與不可混同處','titleEn':'Neighboring mechanism and separation','text':f'相鄰的「{nz}」：{nm} 必須另列其證據，不能把這項機制的通過當作「{zh}」已通過。','textEn':f'Neighboring {ne.lower()}: {nme} Record its evidence separately; its success does not prove {en.lower()} passes.','sourceIds':ids(d)},{'id':sid+'-k3','title':'受控對照與證據品質','titleEn':'Controlled comparison and evidence quality','text':p+' 只變一個條件，保留相同資料格式、時間範圍及分母；模型估计與實測證據要分別標記。','textEn':pe+' Change one condition and retain comparable formats, intervals and denominators; label estimates separately from measured evidence.','sourceIds':ids(d)}]
 if ui in (0,7,15):k.append({'id':sid+'-k4','title':'可重算的原創假想例','titleEn':'Recomputable original hypothetical case','text':d['example'][0],'textEn':d['example'][1],'sourceIds':ids(d),'authorship':'original-hypothetical-exercise'})
 return {'id':sid,'order':seq,'sequence':seq,'estimatedMinutes':30 if model else 40,'simulationOnly':True,'sourceIds':ids(d),'prerequisiteIds':[prev] if prev else [],'title':zh+('：架構與原理' if model else '：對照試驗與證據'),'titleEn':en+(': architecture and principle' if model else ': controlled experiment and evidence'),'objective':f'針對「{zh}」'+('建立有邊界、可反駁的系統模型。' if model else '完成含競爭原因及不確定度的驗收紀錄。'),'objectiveEn':f'For {en.lower()}, '+('construct a bounded falsifiable system model.' if model else 'complete acceptance evidence with competing causes and uncertainty.'),'instruction':instructions,'instructionEn':instructionsEn,'observation':p+f' 比較「{zh}」與「{nz}」的證據是否支持相同推論。','observationEn':pe+f' Compare whether evidence for {en.lower()} and {ne.lower()} supports the same inference.','failure':wrong1[0]+' 這是本課要排除的誤判；先核對模型邊界、來源版本及缺失證據。','failureEn':wrong1[1]+' This is a misconception to reject; check boundaries, source versions and missing evidence.','check':f'提交「{zh}」的功能草圖、基準／擾動表、單位或欄位定義、可反駁預測及接受／保留理由。需能重算本課假想例，並說明相鄰機制不可取代的驗證。','checkEn':f'Submit a functional sketch, baseline/perturbation table, unit/field definitions, falsifiable prediction and accept/hold rationale for {en.lower()}. Recompute the course case and explain verification that the neighboring mechanism cannot replace.','knowledge':k,'quiz':{'question':question,'questionEn':questionEn,'options':opts,'optionsEn':optsEn,'answer':qidx,'explanation':m+f' 相鄰的「{nz}」有不同責任：{nm}因此不能用該項通過或課內誤判取代本單元證據。','explanationEn':me+f' Neighboring {ne.lower()} has a different role: {nme} Its success or the stated misconception cannot replace unit-specific evidence.'}}
def numerical_review():
 """Recompute 33 course cases independently of presentation strings."""
 q={
 335:(0.8*2+0.2*50,11.6,'ms'),336:((120-80)/2,20,'ns offset'),
 337:(1500*8/1e9*1e6,12,'microseconds payload serialization'),
 338:(20*2/80,0.5,'offered/assumed-usable throughput'),
 339:(10000*100e3/1e9*1.2,1.2,'Gbit/s with assumed headroom'),
 340:(4*1.1/8*100,55,'percent utilization'),341:(1e3*(.4+.3+.2),900,'Mbit/s assigned'),
 342:(20*4*4,320,'Mbit/s ideal four-layer rate'),
 343:(20*.25+10*math.log10(32)+2+3,25.05149978319906,'dB budget'),
 344:(10*.85/32,.265625,'Gbit/s equal payload share'),345:(32*4*.8,102.4,'Gbit/s assumed payload'),
 346:(6000/80,75,'spans, not net loss'),
 347:(92.45+20*math.log10(2)+20*math.log10(1000),158.47059991327963,'dB FSPL'),
 348:(4000/300000*1e3+4*.5,15.333333333333334,'ms propagation and processing'),
 349:(4e6*600/8/1e6,300,'decimal MB/contact'),350:(10000*10**(-20/10)*.8**2,64,'ideal paired detections/s'),
 351:(30+60,90,'s conservative residual window'),352:(20*30+2000*2,4600,'grant edges'),
 353:(5/1e6*100,.0005,'percent bounded uniform guessing'),354:(2*1.2,2.4,'ms two chain signatures only'),
 355:(1/.002,500,'operations/s ideal serial service'),356:(100*256/8,3200,'raw key-material bytes/month'),
 357:((90-60)*24/12,60,'nominal renewal opportunities'),358:(1184+1088,2272,'bytes ML-KEM-768 public key+ciphertext'),
 359:(90/(90+99)*100,47.61904761904761,'percent precision'),360:(2000*.0004,.8,'CPU seconds/second'),
 361:(200*5*500*86400/1e9,43.2,'decimal GB/day raw events'),362:(100*30/1000*2*1.2,7.2,'decimal TB with replicas/index assumption'),
 363:(160/(160+100)*100,61.53846153846154,'percent precision'),364:(12*11-18,114,'removed directed reachability relations'),
 365:(100000/(10*60),166.66666666666666,'authentications/s concentrated boot'),
 366:(5000*160/1e6*100,80,'percent assumed bus load'),367:(100*(15+5+10)/1000,3,'serial processing seconds/second')}
 assert len(q)==33
 for cid,(actual,expected,unit) in q.items():assert math.isclose(actual,expected,rel_tol=1e-10,abs_tol=1e-10),(cid,actual,expected)
 return {f'a{k}':{'computed':v[0],'unit':v[2],'verified':True} for k,v in q.items()}

def build():
 numerical=numerical_review()
 courses=[];places=[];related=[]
 assert set(D)==set(CAT)=={f'a{i}' for i in range(335,368)}
 for cid,d in D.items():
  n=int(cid[1:]);c=copy.deepcopy(CAT[cid]);prev=None;stages=[]
  for si,(z,e) in enumerate(ST):
   steps=[]
   for ui in range(si*4,(si+1)*4):
    for phase in range(2):s=make_step(cid,d,ui,phase,prev);steps.append(s);prev=s['id']
   stages.append({'id':cid+f'-v11-stage{si+1:02d}','order':si+1,'title':z,'titleEn':e,'description':'四個領域技術單元各完成原理建模與對照證據，共八項可個別保存的作業。','descriptionEn':'Four domain units each pair principle modeling with controlled evidence, producing eight separately saved tasks.','steps':steps})
  c.update({'kind':'course','status':'guided','contentStatus':'reviewable-educational-curriculum','curriculumVersion':11,'depth':4,'stepCount':32,'estimatedMinutes':1120,'simulationOnly':True,'languageCoverage':['zh-TW','en'],'stages':stages,'sourceIds':ids(d),'summary':f'以{d["focus"][0]}串連 16 個領域技術單元、32 個保存步驟；分析架構、原理、介面、故障、量化案例與防禦證據。','summaryEn':f'Sixteen domain-specific technical units and 32 saved steps connect {d["focus"][1].lower()} through architecture, principles, interfaces, faults, quantitative cases and defensive evidence.','scope':'公開原理的離線／本地合成資料工程教育。只使用自行生成資料或明確獲授權的測試環境；不提供真實目標掃描、漏洞利用、惡意程式、車輛／工控注入或實際射頻發射程序。數值為原創假設，非供應商保證或現場驗收標準。','scopeEn':'Offline/local synthetic-data engineering education from public principles. Use authored data or explicitly authorized test environments only. No real-target scanning, exploitation, malware, vehicle/OT injection or live RF procedures. Numerical cases are original assumptions, not supplier guarantees or field acceptance criteria.','workedExample':{'title':'原創假想量化例與限制','titleEn':'Original hypothetical quantitative case and limits','text':d['example'][0],'textEn':d['example'][1],'assumptions':'只採算例中明列的教學條件；效能與安全估計須依拓撲、分布、開銷、版本與不確定度重算。','assumptionsEn':'Use only the stated teaching assumptions; recalculate for topology, distribution, overhead, versions and uncertainty.','sourceScope':'作者自行設定的教學數值；官方來源支援原理與尺寸規格，未聲稱量測此假想平台。','sourceScopeEn':'Independently chosen teaching inputs; official sources support principles and specified material sizes, not measurements of this hypothetical platform.'},'diagram':{'type':'network','labels':[u[0][0] for u in d['units'][::4]],'labelsEn':[u[0][1] for u in d['units'][::4]],'original':True,'notToScale':True}})
  courses.append(c);p=place(n);refs=[ref(S[k]) for k in d['src']+[PL[PM[n]][9]]]
  places.append({'courseId':cid,'place':p,'summary':f'{c["title"]}以{d["focus"][0]}連結元件與系統。地圖顯示相關標準、研究或供應鏈機構的公開代表位置。','summaryEn':f'{c["titleEn"]} links components and systems through {d["focus"][1].lower()}. The map marks a public standards, research or supply-chain reference.','connection':f'從「{d["units"][0][0][0]}」走到「{d["units"][-1][0][0]}」，比較原理與防禦驗證責任。','connectionEn':f'Connect {d["units"][0][0][1].lower()} to {d["units"][-1][0][1].lower()} and compare principle/defensive-validation responsibilities.','history':[{'year':'公開技術脈絡 / Public technical context','title':S[d['src'][0]]['title'],'titleEn':S[d['src'][0]]['titleEn'],'text':f'本課的公開資料脈絡包括「{S[d["src"][0]]["title"]}」與「{S[d["src"][1]]["title"]}」。課程把介面和原理改寫為自行設定的對照練習，沒有重製文章、圖像或來源算例。','textEn':f'Public context includes {S[d["src"][0]]["titleEn"]} and {S[d["src"][1]]["titleEn"]}. The course turns interfaces/principles into independently assumed comparisons without reproducing articles, artwork or source examples.','sourceIds':ids(d)},{'year':'機構與工程角色 / Institution and role','title':'全球標準、研究與實作的交會','titleEn':'Standards, research and implementation','text':f'{p["name"]}提供地理參照，不代表本課所有設備在此製造，也不主張該機構授課或推薦本站。訪問與地址以官方文件為準。','textEn':f'{p["nameEn"]} provides geographic context, not a claim that all equipment is manufactured here or that the institution teaches/endorses this site. Visits/addresses follow official information.','sourceIds':[S[PL[PM[n]][9]]['id']]}],'references':refs,'sourceIds':ids(d)+[S[PL[PM[n]][9]]['id']]})
  rr=[]
  for target in R[n]:
   tid=f'a{target}';td=D[tid];tc=CAT[tid];tp=place(target);shared=set(d['src'])&set(td['src'])
   transfer=(f'可移植「{d["units"][0][0][0]}」的邊界辨識、對照資料與證據方法；兩課都需要可追溯的{("介面與版本" if n<351 else "身分與授權")}。',f'Transfer boundary identification, controlled records and evidence methods from {d["units"][0][0][1].lower()}; both require traceable '+('interfaces/versions.' if n<351 else 'identities/permissions.'))
   diff=(f'本課主要處理{d["focus"][0]}；「{tc["title"]}」主要處理{td["focus"][0]}，其驗收指標及信任／物理邊界需重定義。',f'This course emphasizes {d["focus"][1].lower()}; {tc["titleEn"]} emphasizes {td["focus"][1].lower()}. Redefine acceptance metrics and trust/physical boundaries.')
   rr.append({'id':tid,'title':tc['title'],'titleEn':tc['titleEn'],'why':transfer[0],'whyEn':transfer[1],'transfer':transfer[0],'transferEn':transfer[1],'difference':diff[0],'differenceEn':diff[1],'practice':[f'並排畫出「{c["title"]}」與「{tc["title"]}」的資料／元件流程，圈出可共用及不可共用的邊界。',f'移植本課「{d["units"][4][0][0]}」的對照方法至「{td["units"][4][0][0]}」，重新指定輸入、單位與可觀測量。','重算两課假想例，列出哪些參數無法直接沿用，並各寫一項拒絕與一項放行證據。'],'practiceEn':[f'Draw {c["titleEn"]} and {tc["titleEn"]} flows side by side and mark transferable/nontransferable boundaries.',f'Transfer the comparison method from {d["units"][4][0][1].lower()} to {td["units"][4][0][1].lower()}, redefining inputs, units and observations.','Recompute both hypothetical cases, identify parameters that cannot transfer and write one rejection/acceptance record per case.'],'place':tp,'referenceUrls':list(dict.fromkeys(S[k]['url'] for k in d['src']+td['src']))})
  related.append({'courseId':cid,'overview':f'由{d["focus"][0]}連結兩個已編寫的相鄰專業；相似方法不表示性能數值、權限或介面可以直接沿用。','overviewEn':f'Connect {d["focus"][1].lower()} to two authored neighboring domains; shared methods do not make metrics, permissions or interfaces interchangeable.','related':rr,'references':refs})
 out={'version':11,'scope':'Original bilingual, local synthetic-data educational engineering; no offensive or live operational procedures.','courses':courses,'sources':list(S.values()),'places':places,'related':related}
 # Normalize Chinese editorial fields only. English, URLs, IDs remain byte-for-byte unchanged.
 english_keys={'titleEn','textEn','instructionEn','objectiveEn','observationEn','failureEn','checkEn','summaryEn','scopeEn','whyEn','transferEn','differenceEn','overviewEn','descriptionEn','connectionEn','nameEn','cityEn','countryEn','addressEn','coordinateScopeEn','assumptionsEn','sourceScopeEn','explanationEn','questionEn','practiceEn','optionsEn','labelsEn','url','referenceUrls','sourceIds','id','courseId','prerequisiteIds','publisher','address','mapQuery','languageCoverage'}
 def norm(x,key=''):
  if key in english_keys:return x
  if isinstance(x,dict):return {k:norm(v,k) for k,v in x.items()}
  if isinstance(x,list):return [norm(v,key) for v in x]
  if isinstance(x,str):return T(x)
  return x
 out=norm(out)
 for c in out['courses']:
  assert c['title']==CAT[c['id']]['title'] and c['titleEn']==CAT[c['id']]['titleEn']
  assert len(c['stages'])==4 and all(len(s['steps'])==8 for s in c['stages'])
  assert len(c['sourceIds'])>=2
  for st in c['stages']:
   for s in st['steps']:
    assert len(s['knowledge'])>=2 and all(s[k] and s[k+'En'] for k in ['objective','instruction','observation','failure','check'])
    assert len(set(s['quiz']['options']))==3 and len(set(s['quiz']['optionsEn']))==3
 (P/'group_b.json').write_text(json.dumps(out,ensure_ascii=False,indent=2)+'\n')
 stats={'courses':len(courses),'technicalUnits':528,'steps':1056,'knowledgeRecords':sum(len(s['knowledge']) for c in courses for st in c['stages'] for s in st['steps']),'sources':len(S),'places':len(places),'relatedComparisons':sum(len(r['related']) for r in related),'minimumPrimarySourcesPerCourse':min(len(c['sourceIds']) for c in courses),'bilingual':'zh-TW/en','defensiveOnly':True,'quantitativeChecks':numerical,'reviewedQuantitativeCases':len(numerical)}
 (P/'group_b_review.json').write_text(json.dumps(stats,ensure_ascii=False,indent=2)+'\n')
 print(json.dumps({k:v for k,v in stats.items() if k!="quantitativeChecks"},ensure_ascii=False));return out
if __name__=='__main__':build()
