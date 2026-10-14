"""Freeze independently authored V11 inputs. Re-run only when editing authorship.
The executable curriculum builder consumes expansion_inputs.json, not live data.
"""
import copy, json, math, pathlib
from expansion_units import UNITS
P=pathlib.Path(__file__).resolve().parent
ROOT=P.parents[1]
S=[]
def source(k,z,en,pub,url,ref=''):
    S.append({'key':k,'id':'v11x-'+k,'title':z,'titleEn':en,'publisher':pub,'url':url,'sourceType':'primary','accessedAt':'2026-10-14','category':'computing','retrievalRef':ref,'imageReuse':'僅連結；不複製原圖或影片。','imageReuseEn':'Links only; original source artwork/video not copied.','scope':'公開架構與工程背景；課程模型、圖解與假想算例由作者另行編寫，來源不提供本課假想數值。','scopeEn':'Public architecture/context; course models, diagrams and assumed exercises are independently authored, not source measurements.'})
source('qbasic','量子資訊基礎','Basics of quantum information','IBM','https://quantum.cloud.ibm.com/learning/en/courses/basics-of-quantum-information','turn540view0')
source('heron','IBM 處理器架構','IBM processor types','IBM','https://quantum.cloud.ibm.com/docs/en/guides/processor-types','turn480search5')
source('willow','Willow 系統與錯誤更正','Willow systems and error correction','Google Quantum AI','https://quantumai.google/quantumcomputer','turn481search1')
source('willowpaper','閾值以下表面碼研究','Below-threshold surface-code research','Google Quantum AI / Nature','https://pmc.ncbi.nlm.nih.gov/articles/PMC11864966/','turn481search4')
source('ankaa','Ankaa-3 公開架構','Ankaa-3 public architecture','Rigetti','https://www.rigetti.com/what-we-build','turn491search3')
source('h2','H2 QCCD 裝置指南','H2 QCCD hardware guide','Quantinuum','https://docs.quantinuum.com/systems/user_guide/hardware_user_guide/h2.html','turn480search0')
source('forte','Forte 光學位址架構','Forte optical-addressing architecture','IonQ','https://www.ionq.com/quantum-systems/forte','turn537search7')
source('iontech','離子陷阱技術原理','Trapped-ion technology','IonQ','https://www.ionq.com/technology','turn491search1')
source('aquila','Aquila 中性原子研究論文','Aquila neutral-atom paper','QuEra authors / arXiv','https://arxiv.org/abs/2306.11727','turn480academia42')
source('bloqade','中性原子哈密頓量背景','Neutral-atom Hamiltonian background','QuEra','https://www.bloqade.quera.com/vendored/bloqade-analog/background/','turn480search21')
source('fresnel','Fresnel QPU 裝置規格','Fresnel QPU specifications','Pasqal','https://docs.pasqal.com/qpu-emulators/qpus/','turn507search0')
source('auroraq','Aurora 模組光子架構','Aurora modular photonic architecture','Xanadu','https://www.xanadu.ai/blog/lighting-up-the-quantum-computing-horizon-with-aurora','turn481search5')
source('aurorapaper','Aurora 模組光子原始研究','Original Aurora modular-photonic paper','Xanadu research authors / Nature','https://www.nature.com/articles/s41586-024-08406-9','turn564view0')
source('omega','Omega 與融合式光子架構','Omega and fusion-based photonic architecture','PsiQuantum','https://www.psiquantum.com/technology','turn489search3')
source('tunnelfalls','Tunnel Falls 矽自旋研究晶片','Tunnel Falls silicon-spin research chip','Intel','https://www.intel.com/content/www/us/en/newsroom/news/quantum-computing-chip-to-advance-research.html','turn481search8')
source('advantage2','Advantage2 系統與 Zephyr 拓撲','Advantage2 and Zephyr topology','D-Wave','https://support.dwavesys.com/hc/en-us/articles/32105885880087-D-Wave-s-Advantage2-Quantum-Computer-Now-Generally-Available','turn491search0')
source('parity','InAs–Al 奇偶量測原始研究','InAs–Al parity-measurement paper','Microsoft research authors / Nature','https://www.nature.com/articles/s41586-024-08445-2','turn491search4')
source('majoranaclaim','Majorana 1 研發路線宣稱','Majorana 1 development claims','Microsoft','https://quantum.microsoft.com/en-us/insights/blogs/microsoft-unveils-majorana-1-worlds-first-quantum-processor-powered-by-topological-qubits','turn489search0')
source('jax','自動微分與有限差分核對','Autodiff and finite-difference checks','JAX authors','https://docs.jax.dev/en/latest/automatic-differentiation.html','turn540view1')
source('resnet','ResNet 原始研究','Original ResNet paper','He et al.','https://arxiv.org/abs/1512.03385','turn488search0')
source('transformer','Transformer 原始研究','Original Transformer paper','Vaswani et al.','https://arxiv.org/abs/1706.03762','turn488academia7')
source('unet','U-Net 原始研究','Original U-Net paper','Ronneberger et al.','https://arxiv.org/abs/1505.04597','turn507search3')
source('gat','圖注意力原始研究','Original graph-attention paper','Veličković et al.','https://arxiv.org/abs/1710.10903','turn516view0')
source('moe','稀疏專家混合原始研究','Original sparse mixture-of-experts paper','Shazeer et al.','https://arxiv.org/abs/1701.06538','turn507academia5')
source('cuda','CUDA 執行模型','CUDA execution model','NVIDIA','https://docs.nvidia.com/cuda/cuda-c-programming-guide/','turn540view2')
source('hopper','Hopper GPU 架構','Hopper GPU architecture','NVIDIA','https://developer.nvidia.com/blog/nvidia-hopper-architecture-in-depth/','turn513search0')
source('blackwell','Blackwell 平臺與架構','Blackwell platform and architecture','NVIDIA','https://nvidianews.nvidia.com/news/blackwell-ai-computing-platform','turn516view2')
source('tpu4','TPU v4 架構','TPU v4 architecture','Google Cloud','https://docs.cloud.google.com/tpu/docs/v4','turn513search3')
source('tpu5','TPU v5p 架構與切片','TPU v5p architecture and slices','Google Cloud','https://docs.cloud.google.com/tpu/docs/v5p','turn516view1')
source('trainium','Trainium 系統共同設計','Trainium system co-design','Amazon Web Services','https://aws.amazon.com/ai/machine-learning/trainium/','turn488search5')
source('neuron','Neuron 裝置分配與工作負載','Neuron allocation and workloads','Amazon Web Services','https://docs.aws.amazon.com/AmazonECS/latest/developerguide/ecs-inference.html','turn488search4')
source('cerebras','Wafer-Scale Cluster 架構','Wafer-Scale Cluster architecture','Cerebras','https://training-api.cerebras.ai/en/latest/wsc/Concepts/how-cerebras-works.html','turn488search3')
source('cerebrasweight','參數與運算分離','Disaggregated weights and compute','Cerebras','https://www.cerebras.ai/blog/announcing-the-cerebras-architecture-for-extreme-scale-ai','turn488search1')
source('loihi','Loihi 2 原始技術簡報','Loihi 2 technical brief','Intel','https://www.intel.com/content/dam/www/central-libraries/us/en/documents/neuromorphic-computing-loihi-2-brief.pdf','turn507search4')
source('neuromorphic','神經形態研究與 Kapoho Point','Neuromorphic research and Kapoho Point','Intel','https://www.intel.com/content/www/us/en/research/neuromorphic-computing.html','turn507search2')
source('dgx','DGX H100/H200 系統拓撲','DGX H100/H200 system topology','NVIDIA','https://docs.nvidia.com/dgx/dgxh100-user-guide/introduction-to-dgxh100.html','turn535search5')
source('gb200','GB200 NVL72 跨節點調校指南','GB200 NVL72 multi-node guide','NVIDIA','https://docs.nvidia.com/multi-node-nvlink-systems/multi-node-tuning-guide/overview.html','turn482search44')
source('elcapitan','El Capitan 節點與 APU 架構','El Capitan node and APU architecture','Lawrence Livermore National Laboratory','https://hpc.llnl.gov/documentation/user-guides/using-el-capitan-systems/hardware-overview','turn490search3')
source('alps','Alps 公開硬體指南','Alps public hardware guide','CSCS','https://docs.cscs.ch/alps/hardware/','turn490search5')
source('perlmutter','Perlmutter 節點與儲存','Perlmutter nodes and storage','NERSC','https://docs.nersc.gov/systems/perlmutter/architecture/','turn533search0')
source('leonardo','Leonardo 分區架構','Leonardo partition architecture','CINECA','https://www.hpc.cineca.it/systems/hardware/leonardo/','turn533search1')
source('jupiter','JUPITER 模組架構','JUPITER modular architecture','Jülich Supercomputing Centre','https://www.fz-juelich.de/en/jsc/jupiter/tech/','turn533search2')
source('taiwania','臺灣杉二號歷史與規格','Taiwania 2 history and specifications','National Center for High-performance Computing','https://www.nchc.org.tw/Page?itemid=2&mid=4','turn535search0')
source('ocp','OCP 伺服器正式設計清單','OCP server design inventory','Open Compute Project','https://www.opencompute.org/projects/server/','turn535search3')
source('yosemite','Yosemite V3 平臺正式規格','Yosemite V3 platform specification','Open Compute Project','https://www.opencompute.org/documents/ocp-yosemite-v3-platform-design-specification-1v16-pdf','turn535search8')
source('nrc','民用反應爐設計架構背景','Civil reactor design background','U.S. Nuclear Regulatory Commission','https://www.nrc.gov/regulations-legislation/fact-sheets-brochures/backgrounder-on-new-nuclear-plant-designs','turn483search1')
source('ap1000','AP1000 設計與審查紀錄','AP1000 design and review record','U.S. Nuclear Regulatory Commission','https://www.nrc.gov/facilities-safety/new-reactors/large-light-water-reactors/design-certification-applications-for-new-reactors/ap1000','turn483search2')
source('vogtle','Vogtle AP1000 場址與機組','Vogtle AP1000 site and units','Southern Nuclear','https://www.southernnuclear.com/our-plants/plant-vogtle.html','turn566search4')
source('barakah','Barakah 民用電廠公開架構','Barakah public civil-generation architecture','Emirates Nuclear Energy Company','https://enec.ae/barakah-plant/technology/','turn566search1')
source('esbwr','ESBWR 自然循環設計','ESBWR natural-circulation design','U.S. Nuclear Regulatory Commission','https://www.nrc.gov/facilities-safety/new-reactors/large-light-water-reactors/design-certification-applications-for-new-reactors/esbwr','turn483search3')
source('hinkley','Hinkley Point C EPR 架構','Hinkley Point C EPR architecture','EDF','https://www.edfenergy.com/energy/nuclear-new-build-projects/hinkley-point-c/reactor','turn492search4')
source('bruce','Bruce CANDU 公開導覽','Bruce CANDU public guide','Bruce Power','https://www.brucepower.com/wp-content/uploads/2020/01/160072_GuidetoBrucePowerReport_R003.pdf','turn492search7')
source('nuscale','NuScale US600 公開審查文件','NuScale US600 public review documents','U.S. Nuclear Regulatory Commission','https://www.nrc.gov/facilities-safety/new-reactors/advanced-reactors/who-were-working-with/past-licensing-activities/nuscale/application-documents-for-the-nuscale-us600-design','turn483search4')
source('bwrx','Darlington BWRX-300 工程','Darlington BWRX-300 project','Ontario Power Generation','https://www.opg.com/projects-services/projects/nuclear/smr/darlington-smr/','turn492search1')
source('smr','SMR 公開技術與階段資料','Public SMR technology and stages','International Atomic Energy Agency','https://nucleus.iaea.org/sites/nids/capacity/TM-infrastructure/TM%20Infra%202025%20Documents/Session%207%20-%20Deployment%20of%20SMRs/7.1.1%20NPTDS_Overview%20of%20SMR%20technology%20development.pdf','turn483search10')
source('htrpm','HTR-PM 工程與公開架構','HTR-PM public engineering architecture','International Atomic Energy Agency','https://conferences.iaea.org/event/150/contributions/5352/','turn492search6')
source('tokamak','Tokamak 公開原理','Tokamak principles','U.S. Department of Energy','https://www.energy.gov/science/doe-explainstokamaks','turn484search0')
source('stellarator','Stellarator 公開原理','Stellarator principles','U.S. Department of Energy','https://www.energy.gov/science/doe-explainsstellarators','turn484search1')
source('iter','ITER 工程系統','ITER engineering systems','ITER Organization','https://www.iter.org/machine','turn483search7')
source('w7x','Wendelstein 7-X 超導線圈','Wendelstein 7-X superconducting coils','Max Planck Institute for Plasma Physics','https://www.ipp.mpg.de/w7x','turn484search2')
source('jt60','JT-60SA 裝置系統','JT-60SA device systems','JT-60SA collaboration','https://www.jt60sa.org/wp/the-device/','turn484search3')
source('sparc','SPARC 研發裝置與路線','SPARC research device and roadmap','Commonwealth Fusion Systems','https://www.cfs.energy/technology/sparc/','turn484search5')
source('hts','高溫超導磁體公開研究','Public HTS magnet research','Commonwealth Fusion Systems','https://www.cfs.energy/technology/hts-magnets/','turn484search4')
source('nif','NIF 公開光學能量系統','NIF public optical-energy systems','Lawrence Livermore National Laboratory','https://lasers.llnl.gov/about/how-nif-works/injection-laser-system','turn524search0')
source('mast','MAST Upgrade 熱排出研究','MAST Upgrade heat-exhaust research','UK Atomic Energy Authority','https://www.ukaea.org/work/mast-upgrade/','turn524search2')
source('fes','DIII-D 與 NSTX-U 研究定位','DIII-D and NSTX-U research roles','U.S. Department of Energy','https://www.energy.gov/sites/default/files/2024-03/FY2025-PresidentsRequest-FES.pdf','turn484search8')
source('iea15','IEA 15 MW 原創研究模型','IEA 15 MW reference research model','IEA Wind Task 37 researchers','https://github.com/IEAWindSystems/IEA-15-240-RWT','turn485search0')
source('nrel5','NREL 5 MW 參考風機','NREL 5 MW reference turbine','National Renewable Energy Laboratory','https://www.nrel.gov/docs/fy09osti/38060.pdf','turn494search7')
source('v236','V236-15 MW 原型架構','V236-15 MW prototype architecture','Vestas','https://www.vestas.com/en/energy-solutions/offshore-wind-turbines/V236-15MW','turn485search1')
source('hornsea','Hornsea 2 工程案例','Hornsea 2 engineering case','Ørsted','https://orsted.com/en/media/news/2022/08/20220831559011','turn485search3')
source('tampen','Hywind Tampen 浮式工程','Hywind Tampen floating engineering','Equinor','https://www.equinor.com/news/20230823-hywind-tampen-officially-opened','turn485search4')
source('scotland','Hywind Scotland 浮式架構','Hywind Scotland floating architecture','Equinor','https://www.equinor.com/energy/hywind-scotland','turn494search6')
source('changhua','大彰化 1 及 2a 工程','Greater Changhua 1 and 2a engineering','Ørsted','https://orsted.tw/en/news/2024/04/chw1and2a_inaguration','turn494search0')
source('formosa','Formosa 1 場址與設計','Formosa 1 site and design','Formosa 1 Wind Power','https://formosa1windpower.com/location-c/','turn494search5')
source('hydrobasic','水力發電原理','Hydropower principles','U.S. Department of Energy','https://www.energy.gov/cmei/water/how-hydropower-works','turn540view3')
source('hoover','胡佛水壩官方工程資料','Hoover Dam official engineering data','U.S. Bureau of Reclamation','https://www.usbr.gov/projects/index.php?id=122','turn486search0')
source('coulee','大古力多目標水力工程','Grand Coulee multipurpose hydropower','U.S. Bureau of Reclamation','https://www.usbr.gov/projects/index.php?id=526','turn486search3')
source('techi','大甲溪與德基水電歷史','Dajia/Techi hydropower history','Taiwan Power Company','https://service.taipower.com.tw/Collection/2009/2025/8422/','turn537search4')
source('mingtan','日月潭與明潭抽蓄架構','Sun Moon Lake/Mingtan pumped-storage architecture','Taiwan Power Company','https://service.taipower.com.tw/tpcjournal/article/3969','turn537search0')
source('nant','Nant de Drance 地下抽蓄','Nant de Drance underground pumped storage','Nant de Drance SA','https://www.nant-de-drance.ch/en/the-power-plant','turn525search0')
source('threegorges','三峽電站官方案例','Three Gorges official plant case','China Three Gorges Corporation','https://www.ctg.com.cn/ctgenglish/news_media/news37/2025092914243383626/index.html','turn535search6')
source('geobasic','地熱原理與系統類型','Geothermal principles and system types','U.S. Department of Energy','https://www.energy.gov/hgeo/geothermal/geothermal-basics','turn540view4')
source('forge','Utah FORGE 地熱研究','Utah FORGE geothermal research','U.S. Department of Energy','https://www.energy.gov/hgeo/geothermal/forge','turn486search7')
source('krafla','Krafla 地熱站','Krafla geothermal station','Landsvirkjun','https://www.landsvirkjun.com/powerstations/krafla','turn486search8')
source('theist','Þeistareykir 與地熱系統','Þeistareykir and geothermal systems','Landsvirkjun','https://www.landsvirkjun.com/geothermal','turn486search9')
source('olkaria','Olkaria 地熱系統','Olkaria geothermal systems','KenGen','https://www.kengen.co.ke/our-business/energy-generation/geothermal/','turn525search1')
source('geysers','Geysers 乾蒸汽原理','Geysers dry-steam principles','Calpine / The Geysers','https://geysers.com/about/','turn536search0')
source('wairakei','Wairākei 雙循環更新案例','Wairākei binary-cycle replacement case','Contact Energy','https://contact.co.nz/about-us/sustainability/our-projects/geothermal/te-mihi-stage-2','turn536search3')
source('sverdrup','Johan Sverdrup 油田','Johan Sverdrup oil field','Equinor','https://www.equinor.com/energy/johan-sverdrup','turn487search0')
source('perdido','Perdido 海底設備監測案例','Perdido subsea monitoring case','Shell','https://www.shell.com/what-we-do/digitalisation/artificial-intelligence.html','turn487search4')
source('prelude','Prelude 浮式液化天然氣','Prelude floating LNG','Shell','https://www.shell.com/what-we-do/oil-and-natural-gas/liquefied-natural-gas-lng/floating-lng.html','turn487search2')
source('troll','Troll 油氣與平臺工程','Troll oil/gas and platform engineering','Equinor','https://www.equinor.com/energy/troll','turn537search6')
source('sleipner','Sleipner 油氣處理與碳封存','Sleipner processing and carbon storage','Equinor','https://www.equinor.com/energy/sleipner','turn536search4')
source('ccs','二氧化碳封存工程經驗','Carbon-storage engineering experience','Equinor','https://www.equinor.com/energy/carbon-capture-utilisation-and-storage','turn536search5')
source('gold','金礦資源與物料背景','Gold resources and material context','U.S. Geological Survey','https://www.usgs.gov/centers/national-minerals-information-center/gold-statistics-and-information','turn540view6')
source('boddington','Boddington 自動搬運礦山','Boddington automated-haulage mine','Newmont','https://operations.newmont.com/australia/boddington/','turn487search5')
source('cadia','Cadia 地下礦山','Cadia underground mine','Newmont','https://operations.newmont.com/australia/cadia/','turn487search7')
source('kibali','Kibali 大型金礦','Kibali gold mine','Barrick','https://www.barrick.com/English/operations/kibali/','turn487search9')
source('pueblo','Pueblo Viejo 礦山及尾礦管理','Pueblo Viejo mine and tailings governance','Barrick','https://www.barrick.com/English/operations/pueblo-viejo/default.aspx','turn487search10')
source('nome','Nome Creek 合法砂金與環境','Nome Creek placer access/environment','Bureau of Land Management','https://www.blm.gov/programs/recreation/recreation-activities/alaska','turn536search2')

PL={
'yorktown':('Yorktown Heights 研究地理參照~Yorktown Heights research reference','美國~United States',41.27,-73.80,'IBM Research Yorktown Heights New York'),
'santabarbara':('Santa Barbara 研究地理參照~Santa Barbara research reference','美國~United States',34.42,-119.70,'Google Quantum AI Santa Barbara California'),
'berkeley':('Berkeley 研究地理參照~Berkeley research reference','美國~United States',37.87,-122.27,'Berkeley California'),
'broomfield':('Broomfield 機構地理參照~Broomfield institutional reference','美國~United States',39.92,-105.09,'Broomfield Colorado Quantinuum'),
'collegepark':('College Park 研究地理參照~College Park research reference','美國~United States',38.99,-76.94,'IonQ College Park Maryland'),
'boston':('Boston 機構地理參照~Boston institutional reference','美國~United States',42.36,-71.06,'QuEra Boston Massachusetts'),
'palaiseau':('Palaiseau 研究地理參照~Palaiseau research reference','法國~France',48.71,2.25,'Pasqal Palaiseau France'),
'toronto':('Toronto 機構地理參照~Toronto institutional reference','加拿大~Canada',43.65,-79.38,'Xanadu Toronto Canada'),
'paloalto':('Palo Alto 機構地理參照~Palo Alto institutional reference','美國~United States',37.44,-122.14,'Palo Alto California PsiQuantum'),
'hillsboro':('Hillsboro 研究地理參照~Hillsboro research reference','美國~United States',45.52,-122.99,'Intel Hillsboro Oregon'),
'burnaby':('Burnaby 機構地理參照~Burnaby institutional reference','加拿大~Canada',49.25,-122.95,'D-Wave Burnaby British Columbia'),
'redmond':('Redmond 機構地理參照~Redmond institutional reference','美國~United States',47.67,-122.12,'Microsoft Redmond Washington'),
'mountainview':('Mountain View 研究地理參照~Mountain View research reference','美國~United States',37.39,-122.08,'Google Mountain View California'),
'freiburg':('Freiburg 研究地理參照~Freiburg research reference','德國~Germany',48.00,7.85,'University of Freiburg Germany'),
'cambridge':('Cambridge 研究地理參照~Cambridge research reference','英國~United Kingdom',52.21,0.12,'University of Cambridge United Kingdom'),
'santaclara':('Santa Clara 機構地理參照~Santa Clara institutional reference','美國~United States',37.35,-121.97,'NVIDIA Santa Clara California'),
'seattle':('Seattle 機構地理參照~Seattle institutional reference','美國~United States',47.61,-122.33,'Amazon Seattle Washington'),
'sunnyvale':('Sunnyvale 機構地理參照~Sunnyvale institutional reference','美國~United States',37.37,-122.04,'Cerebras Sunnyvale California'),
'livermore':('Livermore 研究地理參照~Livermore research reference','美國~United States',37.68,-121.77,'Lawrence Livermore National Laboratory'),
'lugano':('Lugano 計算中心地理參照~Lugano computing reference','瑞士~Switzerland',46.00,8.96,'CSCS Lugano Switzerland'),
'bologna':('Bologna 計算中心地理參照~Bologna computing reference','義大利~Italy',44.49,11.34,'CINECA Leonardo Bologna Italy'),
'juelich':('Jülich 計算中心地理參照~Jülich computing reference','德國~Germany',50.92,6.36,'Forschungszentrum Juelich Germany'),
'hsinchu':('新竹國網中心地理參照~Hsinchu NCHC reference','臺灣~Taiwan',24.78,121.01,'National Center for High-performance Computing Hsinchu Taiwan'),
'waynesboro':('Vogtle 工程區域參照~Vogtle project-region reference','美國~United States',33.14,-81.77,'Plant Vogtle Georgia United States'),
'rockville':('Rockville 監管地理參照~Rockville regulatory reference','美國~United States',39.08,-77.15,'Nuclear Regulatory Commission Rockville Maryland'),
'barakah':('Barakah 工程區域參照~Barakah project-region reference','阿拉伯聯合大公國~United Arab Emirates',23.97,52.23,'Barakah Nuclear Power Plant UAE'),
'hinkley':('Hinkley Point 工程區域參照~Hinkley Point project-region reference','英國~United Kingdom',51.21,-3.13,'Hinkley Point C Somerset United Kingdom'),
'bruce':('Bruce 工程區域參照~Bruce project-region reference','加拿大~Canada',44.32,-81.60,'Bruce Power Ontario Canada'),
'corvallis':('Corvallis 研究地理參照~Corvallis research reference','美國~United States',44.56,-123.26,'NuScale Corvallis Oregon'),
'darlington':('Darlington 工程區域參照~Darlington project-region reference','加拿大~Canada',43.87,-78.72,'Darlington Nuclear Ontario Canada'),
'shidao':('石島灣工程區域參照~Shidao Bay project-region reference','中國~China',36.97,122.52,'Shidao Bay Nuclear Power Plant China'),
'cadarache':('Cadarache 研究區域參照~Cadarache research-region reference','法國~France',43.71,5.78,'ITER Saint Paul lez Durance France'),
'greifswald':('Greifswald 研究地理參照~Greifswald research reference','德國~Germany',54.09,13.38,'Wendelstein 7-X Greifswald Germany'),
'naka':('Naka 研究地理參照~Naka research reference','日本~Japan',36.46,140.55,'JT-60SA Naka Japan'),
'devens':('Devens 研究區域參照~Devens research-region reference','美國~United States',42.54,-71.62,'Commonwealth Fusion Systems Devens Massachusetts'),
'culham':('Culham 研究地理參照~Culham research reference','英國~United Kingdom',51.66,-1.23,'UKAEA Culham United Kingdom'),
'sandiego':('San Diego 研究地理參照~San Diego research reference','美國~United States',32.91,-117.24,'General Atomics DIII-D San Diego'),
'princeton':('Princeton 研究地理參照~Princeton research reference','美國~United States',40.35,-74.61,'Princeton Plasma Physics Laboratory'),
'golden':('Golden 研究地理參照~Golden research reference','美國~United States',39.74,-105.18,'National Renewable Energy Laboratory Golden Colorado'),
'osterild':('Østerild 測試區域參照~Østerild test-region reference','丹麥~Denmark',57.05,8.88,'Osterild wind turbine test centre Denmark'),
'hornsea':('Hornsea 海域地理參照~Hornsea offshore-region reference','英國~United Kingdom',53.92,1.63,'Hornsea 2 offshore wind farm United Kingdom'),
'tampen':('Tampen 海域地理參照~Tampen offshore-region reference','挪威~Norway',61.34,2.26,'Hywind Tampen Norway'),
'peterhead':('Peterhead 海域地理參照~Peterhead offshore-region reference','英國~United Kingdom',57.47,-1.53,'Hywind Scotland Peterhead'),
'changhua':('彰化外海地理參照~Changhua offshore-region reference','臺灣~Taiwan',24.10,120.10,'Greater Changhua offshore wind Taiwan'),
'miaoli':('苗栗外海地理參照~Miaoli offshore-region reference','臺灣~Taiwan',24.64,120.78,'Formosa 1 offshore wind Miaoli Taiwan'),
'hoover':('胡佛水壩工程區域參照~Hoover Dam project-region reference','美國~United States',36.0163,-114.7372,'Hoover Dam United States'),
'coulee':('大古力工程區域參照~Grand Coulee project-region reference','美國~United States',47.96,-118.98,'Grand Coulee Dam Washington'),
'techi':('德基工程區域參照~Techi project-region reference','臺灣~Taiwan',24.26,121.16,'Techi Dam Taichung Taiwan'),
'mingtan':('明潭工程區域參照~Mingtan project-region reference','臺灣~Taiwan',23.84,120.87,'Mingtan Power Plant Nantou Taiwan'),
'nant':('Nant de Drance 工程區域參照~Nant de Drance project-region reference','瑞士~Switzerland',46.07,6.94,'Nant de Drance Switzerland'),
'threegorges':('三峽電站工程區域參照~Three Gorges project-region reference','中國~China',30.82,111.00,'Three Gorges Dam China'),
'milford':('Milford 研究區域參照~Milford research-region reference','美國~United States',38.40,-112.89,'Utah FORGE Milford Utah'),
'krafla':('Krafla 地熱區域參照~Krafla geothermal-region reference','冰島~Iceland',65.70,-16.78,'Krafla Geothermal Station Iceland'),
'theist':('Þeistareykir 地熱區域參照~Theistareykir geothermal-region reference','冰島~Iceland',65.87,-16.97,'Theistareykir Geothermal Station Iceland'),
'olkaria':('Olkaria 地熱區域參照~Olkaria geothermal-region reference','肯亞~Kenya',-0.87,36.30,'Olkaria geothermal Kenya'),
'geysers':('Geysers 地熱區域參照~Geysers geothermal-region reference','美國~United States',38.80,-122.77,'The Geysers California'),
'wairakei':('Wairākei 地熱區域參照~Wairakei geothermal-region reference','紐西蘭~New Zealand',-38.62,176.10,'Wairakei geothermal New Zealand'),
'sverdrup':('Johan Sverdrup 海域參照~Johan Sverdrup offshore reference','挪威~Norway',58.80,2.57,'Johan Sverdrup oil field Norway'),
'perdido':('Perdido 海域地理參照~Perdido offshore-region reference','美國~United States',26.13,-94.90,'Perdido Shell Gulf of Mexico'),
'prelude':('Prelude 海域地理參照~Prelude offshore-region reference','澳洲~Australia',-13.85,123.31,'Prelude FLNG Australia'),
'troll':('Troll 海域地理參照~Troll offshore-region reference','挪威~Norway',60.65,3.72,'Troll A Norway'),
'sleipner':('Sleipner 海域地理參照~Sleipner offshore-region reference','挪威~Norway',58.37,1.91,'Sleipner Norway'),
'boddington':('Boddington 礦區地理參照~Boddington mining-region reference','澳洲~Australia',-32.75,116.34,'Newmont Boddington mine Australia'),
'cadia':('Cadia 礦區地理參照~Cadia mining-region reference','澳洲~Australia',-33.46,148.99,'Cadia East mine Australia'),
'kibali':('Kibali 礦區地理參照~Kibali mining-region reference','剛果民主共和國~Democratic Republic of the Congo',3.12,29.59,'Kibali mine Democratic Republic of Congo'),
'pueblo':('Pueblo Viejo 礦區地理參照~Pueblo Viejo mining-region reference','多明尼加~Dominican Republic',18.95,-70.15,'Pueblo Viejo mine Dominican Republic'),
'nomecreek':('Nome Creek 地理區域參照~Nome Creek geographical-region reference','美國~United States',65.34,-146.81,'Nome Creek Alaska northeast of Fairbanks'),
}

D=[]
def add(slug, title, group, family, discipline, src, focus, place, anchors, *, existing=None, history=None, units=None, nodes=None, example=None):
    az=[s.strip() for s in anchors.split('|')]
    assert len(az)==6 and all('~' in s for s in az),(slug,az)
    D.append({'slug':slug,'id':existing or 'v11-'+slug,'title':title,'group':group,'family':family,'discipline':discipline,'sources':src.split(),'focus':focus,'placeKey':place,'anchors':az,'history':history,'units':units or [f'{group}{i}' for i in range(1,7)],'architectureNodes':nodes,'example':example})

# Quantum routes: public research systems, not manufacturer assembly instructions.
add('ibm-heron','IBM Heron 超導量子處理器~IBM Heron superconducting quantum processor','sc','quantum','quantum-superconducting','heron qbasic','可調耦合、耦合圖與量子控制~Tunable coupling, coupling graphs and quantum control','yorktown','transmon 能階~Transmon levels|Heron 耦合圖~Heron coupling graph|微波控制線~Microwave control lines|色散讀出鏈~Dispersive readout chain|多溫層熱路~Multistage heat paths|邏輯錯誤證據~Logical-error evidence')
add('google-willow','Google Willow 表面碼系統~Google Willow surface-code system','sc','quantum','quantum-superconducting','willow willowpaper','碼距、每循環邏輯錯誤與完整系統指標~Code distance, logical error per cycle and system metrics','santabarbara','Willow 非諧能階~Willow anharmonic levels|表面碼鄰接圖~Surface-code adjacency|同時閘串擾~Concurrent-gate crosstalk|反覆量測與重置~Repeated measurement and reset|冷卻與訊號預算~Cooling and signal budgets|跨碼距閾值比較~Cross-distance threshold comparison')
add('rigetti-ankaa','Rigetti Ankaa-3 方格量子架構~Rigetti Ankaa-3 square-lattice architecture','sc','quantum','quantum-superconducting','ankaa qbasic','方格連通、可調耦合與原生閘編譯~Square connectivity, tunable coupling and native-gate compilation','berkeley','Ankaa 接面與能階~Ankaa junctions and levels|方格耦合路由~Square-lattice routing|fSim 與iSWAP控制~fSim and iSWAP controls|量測指派矩陣~Readout assignment matrix|熱化與環境屏蔽~Thermalization and shielding|閘誤差與邏輯證據~Gate errors and logical evidence')
add('quantinuum-h2','Quantinuum H2 QCCD 離子架構~Quantinuum H2 QCCD ion architecture','ion','quantum','quantum-ion','h2 qbasic','跑道陷阱、分區搬運及中途量測~Racetrack traps, zoned transport and mid-circuit readout','broomfield','Yb離子與集體模態~Yb ions and collective modes|光學地址與通道~Optical addressing and channels|運動介導雙位元閘~Motion-mediated gates|運算區排程~Gate-zone scheduling|跑道QCCD搬運~Racetrack QCCD transport|中途螢光量測~Mid-circuit fluorescence')
add('ionq-forte','IonQ Forte 光學位址量子核心~IonQ Forte optically addressed quantum core','ion','quantum','quantum-ion','forte iontech','聲光偏轉選址與線性離子鏈~Acousto-optic addressing and linear ion chains','collegepark','Forte離子鏈模態~Forte ion-chain modes|AOD光束選址~AOD beam addressing|激光糾纏與閉合軌跡~Laser entanglement and closed paths|全連通與共享光路~Connectivity and shared optics|重排與通道邊界~Rearrangement and channel boundaries|螢光與樣本分佈~Fluorescence and sample distributions')
add('quera-aquila','QuEra Aquila 中性原子類比機~QuEra Aquila neutral-atom analog machine','neutral','quantum','quantum-neutral','aquila bloqade','可重排幾何與 Rydberg 多體類比模擬~Reconfigurable geometry and Rydberg many-body simulation','boston','Aquila光鑷佔位~Aquila tweezer occupancy|Rydberg距離耦合~Rydberg distance coupling|類比驅動與失諧~Analog drive and detuning|Aquila通道約束~Aquila channel constraints|原子損失標記~Atom-loss labels|多體空間關聯~Many-body spatial correlations')
add('pasqal-fresnel','Pasqal Fresnel 光鑷 QPU~Pasqal Fresnel optical-tweezer QPU','neutral','quantum','quantum-neutral','fresnel bloqade','公開裝置約束、原子佈局及脈衝驗證~Device constraints, atom layouts and pulse validation','palaiseau','Fresnel光學register~Fresnel optical register|二體距離圖~Pair-distance graph|時間相依哈密頓量~Time-dependent Hamiltonian|Pulser序列約束~Pulser sequence constraints|前後佔位判讀~Before/after occupancy|有限樣本關聯函數~Finite-shot correlators')
add('xanadu-aurora','Xanadu Aurora 模組光子量子系統~Xanadu Aurora modular photonic quantum system','photon','quantum','quantum-photon','auroraq qbasic','光子來源、多工、叢集態與即時解碼~Sources, multiplexing, cluster states and real-time decoding','toronto','光子與時間模式~Photons and time modes|來源多工模組~Source multiplexing modules|光纖與芯片損耗~Fiber and chip loss|叢集態量測架構~Cluster-state measurement architecture|低溫光子偵測~Cryogenic photon detection|跨機架回饋期限~Interrack feedforward deadlines')
add('psiquantum-omega','PsiQuantum Omega 融合式光子架構~PsiQuantum Omega fusion-based photonic architecture','photon','quantum','quantum-photon','omega qbasic','光子來源、融合量測與可製造模組~Sources, fusion measurements and manufacturable modules','paloalto','單光子編碼~Single-photon encoding|機率性來源與多工~Probabilistic sources and multiplexing|封裝與光纖損耗~Package and fiber loss|融合量測資源圖~Fusion-measurement resource graph|光子偵測器~Photon detectors|模組互連與解碼~Module links and decoding',history='Omega 公開架構連結晶片、封裝與機櫃；容錯及百萬位元為研發目標，課程不將路線圖當成已完成系統。~Omega connects chips, packages and racks; fault tolerance and million-qubit scale are development goals, not treated as completed systems here.')
add('intel-tunnel-falls','Intel Tunnel Falls 矽自旋研究晶片~Intel Tunnel Falls silicon-spin research chip','spin','quantum','quantum-spin','tunnelfalls qbasic','量子點、交換、自旋讀出與晶圓變異~Quantum dots, exchange, spin readout and wafer variability','hillsboro','閘定義量子點~Gate-defined dots|鄰點交換~Neighbor exchange|自旋共振選擇~Spin-resonance selectivity|自旋轉電荷讀出~Spin-to-charge readout|跨點參數變異~Across-dot variability|低溫控制熱預算~Cryogenic-controller heat budget')
add('dwave-advantage2','D-Wave Advantage2 量子退火器~D-Wave Advantage2 quantum annealer','anneal','quantum','quantum-annealing','advantage2 qbasic','QUBO、Zephyr 圖嵌入與端到端公平比較~QUBO, Zephyr embeddings and fair end-to-end comparison','burnaby','QUBO與Ising符號~QUBO and Ising signs|Zephyr物理圖~Zephyr physical graph|成本差與能量尺度~Cost gaps and energy scale|退火樣本分佈~Annealing sample distributions|鏈斷裂解碼~Broken-chain decoding|完整服務時間~Full service elapsed time')
add('majorana-parity','Majorana 1 研發與奇偶量測證據~Majorana 1 research and parity-measurement evidence','topo','quantum','quantum-qec','parity majoranaclaim','近接材料、奇偶讀出及拓撲宣稱審查~Proximity materials, parity readout and review of topological claims','redmond','InAs–Al近接結構~InAs-Al proximity structures|電容與奇偶干涉~Capacitance and parity interference|指派分佈~Assignment distributions|平庸態競爭假說~Trivial-state competing hypotheses|受保護操作證據~Protected-operation evidence|論文與路線圖邊界~Paper/roadmap boundaries',history='原始奇偶量測論文討論平庸與非平庸解釋；Microsoft 的拓撲位元及擴充宣稱需另行檢驗。本課以證據判讀為核心，不將裝置訊號當成已完成容錯運算。~The parity paper discusses trivial and nontrivial interpretations; Microsoft’s topological/scaling claims require separate examination. Device signals are not treated as completed fault-tolerant computation.')

# Neural architectures and accelerator schools.
add('resnet','ResNet 殘差視覺網路~ResNet residual vision network','nn','ai','ai-neural','resnet jax','殘差跳接、梯度路徑與影像表徵~Residual skips, gradient paths and visual representations','redmond','卷積stem與shape~Convolutional stem and shapes|F(x)+x殘差連接~F(x)+x residual connection|跨層梯度路徑~Cross-layer gradient paths|feature map記憶~Feature-map memory|羣組分割與資料洩漏~Grouped splits and leakage|類別與移轉失效~Class and transfer failures')
add('transformer','Transformer 注意力編解碼器~Transformer attention encoder-decoder','nn','ai','ai-neural','transformer jax','QKV、遮罩、位置與平行序列運算~QKV, masks, position and parallel sequence computation','mountainview','token與位置張量~Token and position tensors|softmax(QKᵀ/√d)V~softmax(QKᵀ/sqrt(d))V|殘差與層歸一化~Residuals and layer normalization|L平方attention記憶~Quadratic attention memory|時間與來源切分~Temporal/source splits|長序列與分佈移轉~Long-sequence distribution shift')
add('unet','U-Net 多尺度分割網路~U-Net multiscale segmentation network','nn','ai','ai-neural','unet jax','收縮、擴張、跳接與像素級驗收~Contraction, expansion, skips and pixel-level validation','freiburg','影像與像素標籤~Images and pixel labels|多尺度編碼解碼~Multiscale encoding/decoding|跳接與邊界梯度~Skips and boundary gradients|skip feature緩存~Skip-feature buffers|患者羣組切分~Subject-group splits|Dice與小目標誤差~Dice and small-object errors')
add('graph-attention','GAT 圖注意力網路~GAT graph attention network','nn','ai','ai-neural','gat jax','鄰域遮罩、注意力權重與歸納圖學習~Neighborhood masks, attention weights and inductive graph learning','cambridge','節點與邊張量~Node and edge tensors|鄰域masked attention~Neighborhood masked attention|聚合與梯度路徑~Aggregation and gradients|節點邊數的成本~Node/edge-count cost|未見圖與資料隔離~Unseen-graph isolation|度數偏差與解釋~Degree bias and interpretation')
add('sparse-moe','稀疏 Mixture-of-Experts 網路~Sparse mixture-of-experts network','nn','ai','ai-neural','moe jax','閘控路由、專家容量與負載平衡~Gated routing, expert capacity and load balancing','mountainview','輸入與專家張量~Inputs and expert tensors|top-k門控route~Top-k gated routing|稀疏梯度路徑~Sparse gradient paths|activated與total參數~Activated versus total parameters|路由與來源切分~Routing/source splits|專家負載與overflow~Expert load and overflow')
add('nvidia-hopper','NVIDIA Hopper GPU 架構~NVIDIA Hopper GPU architecture','gpu','ai','ai-gpu','hopper cuda','SIMT、Transformer Engine 與非同步記憶體~SIMT, Transformer Engine and asynchronous memory','santaclara','Hopper warp與SM~Hopper warps and SMs|FP8矩陣核心~FP8 matrix cores|HBM3與L2重用~HBM3 and L2 reuse|TMA與barrier~TMA and barriers|NVLink層級~NVLink hierarchy|工作能耗與精度~Job energy and precision')
add('nvidia-blackwell','NVIDIA Blackwell 多晶粒 GPU~NVIDIA Blackwell multi-die GPU','gpu','ai','ai-gpu','blackwell cuda','多晶粒互連、低精度矩陣與機架擴充~Die interconnects, low-precision matrices and rack scaling','santaclara','Blackwell SM與調度~Blackwell SMs and scheduling|低精度Tensor路徑~Low-precision Tensor paths|HBM與data reuse~HBM and data reuse|異步數據依賴~Async data dependencies|die與rack界面~Die and rack interfaces|精度等質能量比較~Equal-quality energy comparison')
add('google-tpu-v4','Google TPU v4 張量超級電腦~Google TPU v4 tensor supercomputer','tpu','ai','ai-tpu','tpu4 jax','矩陣陣列與可重組三維互連~Matrix arrays and reconfigurable 3D interconnects','mountainview','v4 MXU張量shape~v4 MXU tensor shapes|vector/scalar單元~Vector/scalar units|XLA與sharding~XLA and sharding|v4 mesh與torus~v4 mesh and torus|梯度collective~Gradient collectives|Pod與slice尺寸~Pod and slice dimensions')
add('google-tpu-v5p','Google TPU v5p 與 SparseCore~Google TPU v5p and SparseCore','tpu','ai','ai-tpu','tpu5 jax','矩陣、稀疏嵌入與大工作切片~Matrices, sparse embeddings and large job slices','mountainview','v5p TensorCore~v5p TensorCore|SparseCore embedding~SparseCore embeddings|張量佈局與分片~Tensor layout and sharding|3D torus與ICI~3D torus and ICI|跨slice集體傳輸~Cross-slice collectives|Pod與單作業上限~Pod and per-job limits')
add('aws-trainium','AWS Trainium 與 Neuron 系統~AWS Trainium and Neuron system','tpu','ai','ai-tpu','trainium neuron','專用核心、編譯器及叢集共同設計~Specialized cores, compilers and cluster co-design','seattle','NeuronCore算術路徑~NeuronCore arithmetic paths|vector與稀疏算子~Vector/sparse operators|Neuron圖編譯~Neuron graph compilation|NeuronLink與EFA~NeuronLink and EFA|集體傳輸與並行~Collectives and parallelism|EC2資源與device分配~EC2 resources and allocation',units=['gpu2','tpu2','tpu3','server2','tpu5','server6'])
add('cerebras-cs3','Cerebras CS-3 晶圓尺度叢集~Cerebras CS-3 wafer-scale cluster','wafer','ai','ai-wafer','cerebras cerebrasweight','本地 SRAM、權重串流與晶圓尺度通信~Local SRAM, weight streaming and wafer-scale communication','sunnyvale','WSE本地core與SRAM~WSE local cores and SRAM|MemoryX參數流~MemoryX parameter streaming|稀疏計算mapping~Sparse compute mapping|晶圓冗餘繞路~Wafer redundancy and rerouting|多CS系統梯度~Multi-CS system gradients|晶圓與設施散熱~Wafer/facility cooling')
add('intel-loihi2','Intel Loihi 2 脈衝計算平臺~Intel Loihi 2 spiking-compute platform','neuro','ai','ai-neuromorphic','loihi neuromorphic','非同步事件、可程式神經元及本地突觸~Asynchronous events, programmable neurons and local synapses','hillsboro','graded spike事件~Graded-spike events|膜狀態微碼~Membrane-state microcode|local synapse與學習~Local synapses and learning|NoC事件突發~NoC event bursts|可程式模型映射~Programmable model mapping|Lava端到端比較~Lava end-to-end comparison')

# Specific servers: a392--a396 are preserved for the separate IT100 authoring team.
add('dgx-h100','NVIDIA DGX H100 八 GPU 伺服器~NVIDIA DGX H100 eight-GPU server','server','servers','servers-server-design','dgx cuda','雙 CPU、NVSwitch 與計算／儲存網路分層~Dual CPUs, NVSwitch and compute/storage fabric layers','santaclara','H100與主記憶拓撲~H100 and host-memory topology|NVSwitch與外部NIC~NVSwitch and external NICs|八GPU工作切分~Eight-GPU work partition|NVMe與檢查點~NVMe and checkpoints|PSU冗餘與風冷~PSU redundancy and air cooling|BMC與作業復原~BMC and job recovery')
add('gb200-nvl72','NVIDIA GB200 NVL72 機架系統~NVIDIA GB200 NVL72 rack system','server','servers','servers-server-design','gb200 blackwell','Grace–Blackwell、機架 NVLink 與液冷~Grace-Blackwell, rack NVLink and liquid cooling','santaclara','Grace與Blackwell記憶~Grace/Blackwell memory|72GPU NVLink域~72-GPU NVLink domain|機架模型分割~Rack-scale model partition|存儲與checkpoint~Storage and checkpoints|液冷與機架供電~Liquid cooling and rack power|服務邊界與復原~Service boundaries and recovery')
add('el-capitan','El Capitan MI300A 超級電腦~El Capitan MI300A supercomputer','server','servers','servers-hpc','elcapitan perlmutter','APU 共享 HBM 與 Slingshot 系統架構~APU shared HBM and Slingshot systems','livermore','MI300A共享HBM~MI300A shared HBM|APU與Slingshot網絡~APU and Slingshot fabrics|NUMA工作分佈~NUMA work distribution|Lustre與近端存儲~Lustre and near-node storage|液冷與設施功率~Liquid cooling and facility power|節點排程與一致性~Node scheduling and consistency')
add('alps','Alps Grace–Hopper 超級電腦~Alps Grace-Hopper supercomputer','server','servers','servers-hpc','alps perlmutter','異質節點分區及 CPU–GPU 相干互連~Heterogeneous partitions and coherent CPU-GPU links','lugano','GH200相干記憶~GH200 coherent memory|node內與Slingshot~Intranode and Slingshot|異質partition選擇~Heterogeneous partition choice|scratch與archive~Scratch and archive|機櫃冷卻預算~Cabinet cooling budget|分區作業復原~Partition job recovery')
add('perlmutter','Perlmutter GPU 與 CPU 雙分區~Perlmutter GPU and CPU partitions','server','servers','servers-hpc','perlmutter cuda','雙分區、Dragonfly 網路與全快閃暫存~Dual partitions, Dragonfly and all-flash scratch','berkeley','A100與EPYC拓撲~A100/EPYC topology|Dragonfly光銅連線~Dragonfly optical/copper links|CPU/GPU分工~CPU/GPU partitioning|all-flash與metadata~All-flash and metadata|機櫃與節點能量~Cabinet/node energy|排程與檢查點重啟~Scheduling/checkpoint restart')
add('leonardo','Leonardo Booster 與資料分區~Leonardo Booster and data-centric partitions','server','servers','servers-hpc','leonardo perlmutter','GPU Booster 與通用節點的工作流分工~GPU Booster and general-node workflow division','bologna','Booster GPU與主機~Booster GPU and host|InfiniBand層級~InfiniBand hierarchy|partition工作流~Partition workflows|高效與容量存儲~Fast/capacity storage|計算分區能耗~Compute-partition energy|跨分區排程~Cross-partition scheduling')
add('jupiter','JUPITER 模組超算系統~JUPITER modular supercomputing system','server','servers','servers-hpc','jupiter alps','Booster、Cluster 與多層儲存協作~Booster, Cluster and tiered-storage cooperation','juelich','GH200與CPU模塊~GH200 and CPU modules|DragonFly+網絡~DragonFly+ fabric|模塊化工作分割~Modular workload partition|ExaFLASH/STORE/TAPE~ExaFLASH/STORE/TAPE|溫水冷卻邊界~Warm-water cooling boundary|模塊排程與故障恢復~Module scheduling/recovery')
add('taiwania2','臺灣杉二號歷史架構~Taiwania 2 historical architecture','server','servers','servers-hpc','taiwania perlmutter','V100 節點、AI 平臺與溫水冷卻~V100 nodes, AI platforms and warm-water cooling','hsinchu','雙Xeon與八V100~Dual Xeon and eight V100|EDR InfiniBand~EDR InfiniBand|AI節點工作分割~AI-node workload partition|Ceph與GPFS層級~Ceph and GPFS hierarchy|溫水冷卻與PUE~Warm-water cooling and PUE|Slurm與Kubernetes~Slurm and Kubernetes',history='國網中心公開資料標示臺灣杉二號於2026年8月31日下架；本課研究2018年建置架構與系統整合，不主張目前仍可申請此主機。~NCHC marks Taiwania 2 decommissioned on 31 August 2026. This course studies its 2018 architecture/integration and does not claim current access.')
add('ocp-yosemite-v3','OCP Yosemite V3 模組伺服器~OCP Yosemite V3 modular server','server','servers','servers-server-design','yosemite ocp','開放模組、共用服務與硬體介面~Open modules, shared services and hardware interfaces','santaclara','sled與主機拓撲~Sled/host topology|平臺接口與I/O~Platform interfaces and I/O|多sled工作分割~Multisled workload partition|boot與數據存儲~Boot/data storage|共用供電與冷卻~Shared power/cooling|維護邊界與隔離~Maintenance boundaries and isolation')
add('ocp-grand-teton','OCP Grand Teton AI 平臺~OCP Grand Teton AI platform','server','servers','servers-server-design','ocp dgx','開放 AI 託盤、CPU 與交換介面~Open AI trays, CPUs and switching interfaces','santaclara','CPU與加速器tray~CPU/accelerator trays|switch tray與fabric~Switch trays and fabrics|AI工作與資源配置~AI work/resource allocation|存儲與主機接口~Storage/host interfaces|模塊供電與thermal~Module power and thermals|托盤維護與可追溯~Tray maintenance/traceability')

# Peaceful civilian power: thermal-cycle and system safety concepts only.
add('ap1000','AP1000 壓水式發電架構~AP1000 pressurized-water generation architecture','nuclear','energy','energy-nuclear','ap1000 nrc','主次迴路、被動排熱與民用電廠證據~Primary/secondary loops, passive heat removal and civil evidence','waynesboro','壓水熱源與蒸汽發生器~PWR heat source/steam generators|汽輪島淨電~Turbine-island net power|餘熱與熱容~Residual heat/capacitance|自然循環支持~Natural-circulation support|核島與共用系統~Nuclear-island shared systems|公開設計與建造驗證~Public design/build evidence')
add('esbwr','ESBWR 自然循環沸水架構~ESBWR natural-circulation boiling-water architecture','nuclear','energy','energy-nuclear','esbwr nrc','直接蒸汽路徑及自然循環邊界~Direct steam paths and natural-circulation boundaries','rockville','沸水與直接蒸汽路~BWR/direct steam paths|汽輪轉換與輔機~Turbine conversion/auxiliaries|餘熱概念預算~Residual-heat concept budget|自然循環與重力路徑~Natural circulation/gravity|系統共因依賴~Shared-system dependencies|設計認證與廠址區別~Design certification versus sites')
add('barakah-apr1400','Barakah APR1400 汽輪機與安全架構~Barakah APR1400 turbine and safety architecture','nuclear','energy','energy-nuclear','nrc smr','大型壓水式電廠的熱電與支援邊界~Thermal/electrical/support boundaries of large PWR plants','barakah','APR1400主次邊界~APR1400 loop boundaries|汽輪與發電機島~Turbine/generator island|停機餘熱~Post-shutdown heat|主動與被動支援~Active/passive support|多機組共用界面~Multiplant shared interfaces|工程QA與運行證據~Engineering QA/operation evidence',existing='d050')
add('hinkley-epr','Hinkley Point C EPR 民用工程~Hinkley Point C EPR civil engineering','nuclear','energy','energy-nuclear','hinkley nrc','複製設計、分離安全支援與工程驗證~Design replication, separated safety support and validation','hinkley','EPR核島與蒸汽迴路~EPR nuclear/steam loops|常規島熱電效率~Conventional-island conversion|餘熱移除功能~Residual-heat removal function|分離支援架構~Separated support architecture|複製與廠址界面~Replication/site interfaces|設計施工階段追溯~Design/construction traceability')
add('bruce-candu','Bruce CANDU 重水發電架構~Bruce CANDU heavy-water generation architecture','nuclear','energy','energy-nuclear','bruce nrc','壓力管、蒸汽產生與大型更新工程~Pressure tubes, steam generation and major refurbishment','bruce','壓力管與熱傳邊界~Pressure-tube heat-transfer boundary|蒸汽與汽輪發電~Steam/turbine generation|餘熱與持續支持~Residual heat/support|熱流與支援路徑~Heat/support paths|多機組與更新界面~Units/refurbishment interfaces|生命週期更新證據~Lifecycle refurbishment evidence')
add('nuscale-us600','NuScale US600 模組設計研究~NuScale US600 modular design study','nuclear','energy','energy-smr','nuscale nrc','整合式壓水模組與共用水池~Integral PWR modules and a shared pool','corvallis','整合模組熱流體邊界~Integral-module fluid boundaries|模組與淨髮電~Modules/net generation|池內餘熱路徑~Pool residual-heat paths|自然循環概念~Natural-circulation concepts|多個模塊共用池~Shared multimodule pool|US600文檔審查界面~US600 document-review boundary',history='US600 是有公開審查文件的模組設計；本課不把設計覈准等同某一商轉電廠，也不混用後續較大模組的產品數字。~US600 is a modular design with public review documents; approval is not an operating plant, and later larger-module values are not mixed into this case.')
add('darlington-bwrx300','Darlington BWRX-300 SMR 工程~Darlington BWRX-300 SMR engineering','nuclear','energy','energy-smr','bwrx smr','小型沸水模組、自然循環與施工階段~Small BWR modules, natural circulation and construction stages','darlington','小型BWR蒸汽邊界~Small-BWR steam boundaries|模塊與汽輪轉換~Module/turbine conversion|餘熱與熱容量~Residual heat/capacity|自然循環熱路~Natural-circulation heat paths|模塊共用基礎設施~Shared module infrastructure|許可與建造階段~Licensing/build stages',history='Darlington 公開資料區分施工許可與運轉許可；此案例研究 BWRX-300 的模組化與工程界面，不將建造階段標成已商轉。~Darlington sources distinguish construction/operating permissions. The case studies BWRX-300 modular interfaces without calling construction commercial operation.')
add('htr-pm','HTR-PM 高溫氣冷發電系統~HTR-PM high-temperature gas-cooled generation','nuclear','energy','energy-smr','htrpm smr','氦熱傳、雙模組與共同汽輪機~Helium heat transfer, twin modules and a shared turbine','shidao','氦熱路與蒸汽邊界~Helium/steam boundaries|共用汽輪島~Shared turbine island|餘熱與熱容概念~Residual heat/capacitance|傳熱與支持依賴~Heat-transfer/support dependencies|雙模組接口~Twin-module interfaces|公開架構與階段證據~Public architecture/stage evidence')

# Fusion research machines: no target recipes, reactor operation or fuel handling.
add('iter','ITER 國際磁約束研究工程~ITER international magnetic-confinement engineering','fusion','energy','energy-fusion','iter tokamak','大型 tokamak 系統、低溫磁體與熱排出~Large tokamak systems, cryogenic magnets and heat exhaust','cadarache','tokamak真空與磁場~Tokamak vacuum/magnetic fields|plasma與設施Q邊界~Plasma/facility Q boundaries|超導coil公差~Superconducting-coil tolerances|divertor熱負載~Divertor heat loads|診斷與反演~Diagnostics/reconstruction|研究裝置與電廠差距~Research/plant gaps',history='ITER 是研究 burning-plasma 與系統整合的國際實驗工程，不是已供電的商用電廠。課程只分析公開架構、熱路與證據。~ITER is an international burning-plasma/system-integration experiment, not a commercially generating plant. This course analyzes public architectures, heat paths and evidence.')
add('wendelstein7x','Wendelstein 7-X 三維仿星器~Wendelstein 7-X three-dimensional stellarator','fusion','energy','energy-fusion','w7x stellarator','非平面超導線圈與長脈衝熱管理~Nonplanar superconducting coils and long-pulse heat management','greifswald','三維stellarator約束~3D stellarator confinement|輸入與plasma熱量~Input/plasma energy|非平面coil幾何~Nonplanar coil geometry|長pulse熱排出~Long-pulse heat exhaust|三維診斷反演~3D diagnostic reconstruction|穩態研究與發電差距~Steady-state research/plant gaps')
add('jt60sa','JT-60SA 超導 tokamak~JT-60SA superconducting tokamak','fusion','energy','energy-fusion','jt60 tokamak','超導磁體、低溫屏蔽與支援系統~Superconducting magnets, thermal shielding and support systems','naka','tokamak磁體與vacuum~Tokamak magnets/vacuum|加熱與能量邊界~Heating/energy boundaries|cryostat與thermal shield~Cryostat/thermal shield|壁面與冷卻熱流~Wall/cooling heat flow|公開diagnostics~Public diagnostics|實驗與電廠整合差距~Experiment/plant integration gaps')
add('sparc','SPARC 高場 tokamak 研究~SPARC high-field tokamak research','fusion','energy','energy-fusion','sparc hts','高溫超導磁體與緊湊裝置能量邊界~HTS magnets and compact-device energy boundaries','devens','緊湊tokamak幾何~Compact tokamak geometry|預期Q與設施邊界~Projected Q/facility boundaries|HTS磁體負載~HTS magnet loads|緊湊壁面熱通量~Compact-device surface flux|診斷與仿真驗證~Diagnostics/simulation validation|目標與已證明能力~Goals/demonstrated capabilities',history='SPARC 官方路線描述未來研究目標。課程分開設計預測、磁體示範與仍需驗證的整體裝置能力，不宣稱已供電。~SPARC sources describe research goals. The course separates design predictions, magnet demonstrations and remaining integrated validation without claiming power delivery.')
add('nif-energy-systems','NIF 慣性融合能量邊界~NIF inertial-fusion energy boundaries','fusion','energy','energy-fusion','nif tokamak','高能雷射、增益定義與設施能量~High-energy lasers, gain definitions and facility energy','livermore','慣性約束系統邊界~Inertial-confinement boundaries|target與wallplug增益~Target/wall-plug gain|公開光學timing精度~Public optical timing precision|脈衝與冷卻負載~Pulse/cooling loads|能量計量與誤差~Energy metrology/errors|重複率與發電差距~Repetition/plant gaps',history='NIF 是高能密度與融合研究設施。target 能量增益不等於全設施淨發電；本課不提供靶設計、脈衝優化配方或燃料操作。~NIF is a high-energy-density/fusion research facility. Target gain is not facility net power; this course provides no target designs, pulse-optimization recipes or fuel operations.')
add('mast-upgrade','MAST Upgrade 球形 tokamak~MAST Upgrade spherical tokamak','fusion','energy','energy-fusion','mast tokamak','低長寬比與 Super-X 排熱研究~Low aspect ratio and Super-X exhaust research','culham','球形tokamak約束~Spherical tokamak confinement|加熱與gain定義~Heating/gain definitions|低aspect ratio場形~Low-aspect-ratio fields|Super-X熱排出~Super-X exhaust|plasma診斷與估計~Plasma diagnostics/estimates|排熱研究與電廠需求~Exhaust research/plant needs')
add('diii-d','DIII-D 可重組 tokamak 研究~DIII-D configurable tokamak research','fusion','energy','energy-fusion','fes tokamak','磁形、診斷與核心邊緣整合~Magnetic shaping, diagnostics and core-edge integration','sandiego','可重組場形約束~Configurable magnetic shaping|加熱及能量預算~Heating/energy budgets|三角形與field誤差~Triangularity/field errors|core-edge熱通量~Core-edge heat flux|多diagnostic證據~Multiple-diagnostic evidence|研究方案與可用率~Research regimes/availability')
add('nstx-u','NSTX-U 球形電漿研究~NSTX-U spherical-plasma research','fusion','energy','energy-fusion','fes tokamak','球形幾何、診斷及可擴充物理~Spherical geometry, diagnostics and scalable physics','princeton','低aspect ratio約束~Low-aspect-ratio confinement|輸入與儲能budget~Input/stored-energy budget|球形磁場幾何~Spherical field geometry|表面power loading~Surface power loading|模型與量測分離~Models versus measurements|研究結果外推邊界~Research extrapolation boundaries')

add('iea15mw','IEA 15 MW 參考風機~IEA 15 MW reference wind turbine','wind','energy','energy-wind','iea15 nrel5','開放氣彈性模型與大型風輪設計~Open aeroelastic models and large-rotor design','golden','15MW風速功率包絡~15-MW wind/power envelope|參考blade氣動~Reference-blade aerodynamics|參考傳動與generator~Reference drivetrain/generator|固定浮式support模型~Fixed/floating support models|陣列與export cable概念~Array/export cable concepts|OpenFAST負載驗證~OpenFAST load validation')
add('nrel5mw','NREL 5 MW 基準風機~NREL 5 MW benchmark wind turbine','wind','energy','energy-wind','nrel5 iea15','三葉片基準、變速與變槳~Three-blade reference, variable speed and pitch','golden','5MW假想功率曲線~5-MW assumed power curve|參考chord與twist~Reference chord/twist|變速軸扭矩~Variable-speed shaft torque|基準支撐模態~Benchmark support modes|風場損失分解~Farm-loss decomposition|控制與疲勞記錄~Control/fatigue records')
add('vestas-v236','Vestas V236-15 MW 風輪工程~Vestas V236-15 MW rotor engineering','wind','energy','energy-wind','v236 nrel5','大型葉片、中速傳動與全功率轉換~Large blades, medium-speed drivetrain and full converters','osterild','V236風速包絡~V236 wind envelope|大型blade載荷~Large-blade loads|中速gear與converter~Medium-speed gear/converter|測試塔與support動態~Test-tower/support dynamics|單機與陣列差異~Turbine/array differences|原型與壽命證據~Prototype/lifetime evidence')
add('hornsea2','Hornsea 2 離岸風場工程~Hornsea 2 offshore wind engineering','wind','energy','energy-wind','hornsea nrel5','大陣列尾流、出口海纜與海上維護~Large-array wakes, export cables and offshore service','hornsea','Hornsea2風資源~Hornsea-2 wind resources|陣列blade載荷~Array blade loads|風機與海上集電~Turbines/offshore collection|基礎與海況模態~Foundations/sea-state modes|尾流與出口海纜~Wakes/export cables|海上可達窗口~Offshore access windows',existing='d035')
add('hywind-tampen','Hywind Tampen 浮式風電~Hywind Tampen floating wind','wind','energy','energy-wind','tampen nrel5','浮式混凝土支撐與油氣平臺供電~Floating concrete supports and platform electricity','tampen','Tampen風資源~Tampen wind resources|浮式葉片載荷~Floating-rotor loads|轉矩與平臺供電~Torque/platform power|繫泊與浮體模態~Mooring/floater modes|動態海纜與陣列~Dynamic cables/array|海況與供電可用率~Sea states/power availability')
add('hywind-scotland','Hywind Scotland 浮式風場~Hywind Scotland floating wind farm','wind','energy','energy-wind','scotland nrel5','spar 支撐、繫泊與浮式經驗遷移~Spar supports, mooring and floating-design transfer','peterhead','Scotland風分佈~Scotland wind distribution|海上rotor載荷~Offshore rotor loads|風機電能轉換~Turbine electrical conversion|spar與mooring~Spar/mooring|動態cable與陣列~Dynamic cable/array|長期capacity與availability~Long-term capacity/availability',existing='d039')
add('greater-changhua','大彰化 1 與 2a 離岸工程~Greater Changhua 1 and 2a offshore engineering','wind','energy','energy-wind','changhua nrel5','遠岸直驅陣列、颱風環境與供應鏈~Farshore direct-drive arrays, typhoons and supply chains','changhua','彰化風資源與typhoon~Changhua resources/typhoons|大型rotor與載荷~Large rotors/loads|直驅與集電~Direct drive/collection|支撐與海況~Supports/sea states|海纜與岸上互連~Cables/onshore interconnection|臺灣O&M與窗口~Taiwan O&M/windows',existing='d038')
add('formosa1','Formosa 1 近岸風電工程~Formosa 1 nearshore wind engineering','wind','energy','energy-wind','formosa nrel5','分期示範、近岸基礎與集電~Phased demonstration, nearshore foundations and collection','miaoli','苗栗近岸資源~Miaoli nearshore resources|不同機型blade~Different turbine blades|分期電力轉換~Phased power conversion|近岸基礎與海況~Nearshore foundations/sea states|集電與export路由~Collection/export routing|示範至商業證據~Demonstration/commercial evidence',existing='d037')

add('hoover-hydro','胡佛水壩水力系統~Hoover Dam hydropower system','hydro','energy','energy-hydro','hoover hydrobasic','厚拱壩、水頭變動與多目標水庫~Thick-arch dams, variable head and multipurpose reservoirs','hoover','Hoover有效水頭~Hoover effective head|水輪工況map~Turbine operating maps|壓力水路暫態~Penstock transients|厚拱壩載荷路徑~Thick-arch load paths|供水與發電調度~Water/power scheduling|水庫與泥砂邊界~Reservoir/sediment boundaries',existing='d003')
add('grand-coulee','大古力多電廠水力工程~Grand Coulee multi-powerhouse engineering','hydro','energy','energy-hydro','coulee hydrobasic','多機組、水庫、灌溉與抽水協作~Multiple units, reservoir, irrigation and pumping','coulee','Coulee流量水頭~Coulee flow/head|多電廠機組工況~Multiple-powerhouse units|水路與spillway暫態~Waterway/spillway transients|forebay與壩體載荷~Forebay/dam loads|灌溉泵發協作~Irrigation pump/generation|生態與泥砂指標~Ecology/sediment metrics',existing='d004')
add('techi-hydro','德基水庫與級聯水電~Techi reservoir and cascade hydropower','hydro','energy','energy-hydro','techi hydrobasic','薄拱壩與大甲溪級聯能量~Thin-arch dams and Dajia cascade energy','techi','德基有效水頭~Techi effective head|山區水輪工況~Mountain turbine envelopes|引水隧道暫態~Headrace transients|薄拱壩與基礎~Thin-arch dam/foundation|上游下游級聯~Upstream/downstream cascade|泥砂與集水區~Sediment/catchment',existing='d016')
add('mingtan-storage','明潭抽蓄與日月潭系統~Mingtan storage and Sun Moon Lake system','hydro','energy','energy-hydro','mingtan hydrobasic','上下池、可逆機組與往返效率~Upper/lower pools, reversible units and round-trip efficiency','mingtan','上下池淨水頭~Pool net head|可逆水輪pump~Reversible turbine/pump|切換水路暫態~Transition transients|地下powerhouse界面~Underground powerhouse interfaces|抽蓄能量循環~Pumped energy cycle|水位與環境監測~Level/environment monitoring',existing='d017')
add('nant-storage','Nant de Drance 地下抽蓄~Nant de Drance underground pumped storage','hydro','energy','energy-hydro','nant hydrobasic','地下洞室、可逆機組及電網彈性~Underground caverns, reversible units and grid flexibility','nant','上下庫能量~Reservoir energy|pump turbine工況~Pump-turbine envelopes|水路壓力暫態~Waterway pressure transients|深埋洞室支撐~Deep-cavern supports|往返效率與電網~Round-trip efficiency/grid|水位與長期性能~Levels/long-term performance',existing='d021')
add('three-gorges-station','三峽巨型水輪發電站~Three Gorges large hydroelectric station','hydro','energy','energy-hydro','threegorges hydrobasic','巨型機組、聯合水庫與水沙平衡~Large units, coordinated reservoirs and water/sediment balance','threegorges','長江flow與head~Yangtze flow/head|巨型水輪工況~Large-turbine envelopes|水道與機組暫態~Waterway/unit transients|壩體與發電洞室~Dam/powerhouse|多目標水庫調度~Multipurpose scheduling|水沙與生態證據~Water/sediment/ecology',existing='d001')

add('utah-forge','Utah FORGE 增強型地熱研究~Utah FORGE enhanced-geothermal research','geo','energy','energy-geothermal','forge geobasic','公開儲層觀測、井筒與熱循環~Public reservoir observations, wells and heat cycles','milford','EGS熱與連通~EGS heat/connectivity|研究井完整性~Research-well integrity|假想發電循環選擇~Assumed-cycle choice|換熱與礦物證據~Transfer/mineral evidence|示蹤與thermal return~Tracer/thermal return|公開microseismic目錄~Public microseismic catalogs')
add('krafla-geothermal','Krafla 地熱與回注系統~Krafla geothermal and reinjection system','geo','energy','energy-geothermal','krafla geobasic','火山儲層、蒸汽利用與回注~Volcanic resources, steam utilization and reinjection','krafla','Krafla儲層觀測~Krafla reservoir observations|高溫井與完整性~High-temperature well integrity|高低壓steam循環~High/low-pressure steam|結垢與材料~Scaling/materials|回注與溫度變化~Reinjection/temperature|環境與微震證據~Environment/seismic evidence')
add('theistareykir','Þeistareykir 地熱工程~Theistareykir geothermal engineering','geo','energy','energy-geothermal','theist geobasic','火山熱源、分期機組與環境整合~Volcanic heat, phased units and environmental integration','theist','Theistareykir熱源~Theistareykir heat source|井羣與採樣~Wellfields/sampling|分期steam機組~Phased steam units|管路熱傳與corrosion~Piping heat/corrosion|回注質量熱量~Reinjection mass/heat|自然環境證據~Natural-environment evidence')
add('olkaria-geothermal','Olkaria 地熱與井口發電~Olkaria geothermal and wellhead generation','geo','energy','energy-geothermal','olkaria geobasic','兩相資源、閃蒸及分期井口電力~Two-phase resources, flash and phased wellhead generation','olkaria','Olkaria兩相資源~Olkaria two-phase resources|井羣與完整性~Wellfield integrity|flash與井口機組~Flash/wellhead units|分離與熱傳~Separation/heat transfer|回注與補給~Reinjection/recharge|公園生態與證據~Park ecology/evidence',existing='d025')
add('geysers-geothermal','Geysers 乾蒸汽與再生水系統~Geysers dry-steam and reclaimed-water system','geo','energy','energy-geothermal','geysers geobasic','乾蒸汽、冷凝與資源補水~Dry steam, condensation and resource replenishment','geysers','Geysers蒸汽儲層~Geysers steam reservoir|產汽井與管線~Steam wells/pipelines|dry steam turbine~Dry-steam turbines|冷凝與熱傳~Condensation/heat transfer|再生水與質量平衡~Reclaimed-water mass balance|環境及微震monitor~Environmental/seismic monitoring',existing='d024')
add('wairakei-geothermal','Wairākei 地熱現代化~Wairakei geothermal modernization','geo','energy','energy-geothermal','wairakei geobasic','既有蒸汽田與雙循環更新~Existing steamfields and binary-cycle renewal','wairakei','Wairakei資源與歷史~Wairakei resources/history|舊井與完整性~Existing-well integrity|steam至binary邊界~Steam/binary boundaries|換熱效率與結垢~Transfer efficiency/scaling|回注與長期溫度~Reinjection/long-term temperature|更新環境與階段證據~Renewal environment/stages',existing='d026',history='Contact 的公開更新計畫描述 Te Mihi Stage 2 雙循環新機組及 Wairākei 分期退役；本課比較熱循環，不把預計商轉日期當成已達成。~Contact’s plan describes Te Mihi Stage 2 binary units and staged Wairākei retirement; projected dates are not treated as completed commissioning.')

add('johan-sverdrup','Johan Sverdrup 海上油田~Johan Sverdrup offshore oilfield','oil','resources','resources-oil','sverdrup troll','岸電、平臺整合與海底接回~Shore power, platform integration and subsea tiebacks','sverdrup','油藏物料與壓力~Reservoir material/pressure|公開井筒屏障概念~Public well-barrier concepts|油氣水多相界面~Oil/gas/water interfaces|海底tieback與平臺~Subsea tiebacks/platforms|岸電與排放邊界~Shore power/emissions|維修與狀態複覈~Maintenance/state review')
add('shell-perdido','Shell Perdido 深水監測~Shell Perdido deepwater monitoring','oil','resources','resources-oil','perdido sverdrup','海底泵、多相流與遠端狀態辨識~Subsea pumps, multiphase flow and remote diagnosis','perdido','深水reservoir假說~Deepwater-reservoir hypotheses|井筒與壓力containment~Well/pressure containment|海底多相pump~Subsea multiphase pumps|浮平臺與riser界面~Floating-platform/riser interfaces|處理與digital能量~Processing/digital energy|AI診斷與獨立證據~AI diagnosis/independent evidence')
add('prelude-flng','Prelude FLNG 海上處理工程~Prelude FLNG offshore processing engineering','oil','resources','resources-oil','prelude troll','海上氣體處理、液化及儲運邊界~Offshore gas treatment, liquefaction and storage/transfer boundaries','prelude','天然氣資源與庫存~Gas resources/inventory|海底與上部containment~Subsea/topside containment|氣體與液化相態~Gas/liquefaction phases|浮式平臺與transfer~Floating-platform transfer|冷卻能耗與邊界~Cooling energy/boundaries|可用率與事件證據~Availability/event evidence')
add('troll-field','Troll 海上油氣平臺~Troll offshore oil/gas platforms','oil','resources','resources-oil','troll sverdrup','重力基礎、岸電與壓縮支援~Gravity bases, shore power and compression support','troll','Troll油氣與壓力~Troll oil/gas pressure|井羣與屏障~Wellfield barriers|氣體compression界面~Gas-compression interfaces|Condeep與管路~Condeep/piping|岸電與壓縮能耗~Shore-power/compression energy|平臺系統與恢復~Platform systems/recovery')
add('sleipner-ccs','Sleipner 油氣與碳封存~Sleipner oil/gas and carbon storage','oil','resources','resources-oil','sleipner ccs','分離、壓縮與封存監測邊界~Separation, compression and storage-monitoring boundaries','sleipner','油氣與CO2物料~Hydrocarbon/CO2 balance|井筒完整性概念~Well-integrity concepts|分離與輸送相態~Separation/transport phases|處理與儲層界面~Processing/reservoir interfaces|capture能耗與減排~Capture energy/abatement|封存monitoring與不確定度~Storage monitoring/uncertainty')

add('boddington-mine','Boddington 自動化金銅礦~Boddington automated gold/copper mine','mine','resources','resources-mining','boddington gold','露天礦、自治搬運與物料回收~Surface mining, autonomous haulage and material recovery','boddington','金銅grade分佈~Gold/copper grades|露天autonomous haulage~Surface autonomous haulage|粒度與解離~Size/liberation|給料與精礦balance~Feed/concentrate balance|通信與人員隔離~Communications/people separation|礦水尾礦與覆育~Mine water/tailings/rehabilitation')
add('cadia-mine','Cadia 地下金銅礦~Cadia underground gold/copper mine','mine','resources','resources-mining','cadia gold','panel caving、地下支援與長期礦水~Panel caving, underground support and long-term mine water','cadia','地下grade與取樣~Underground grades/sampling|panel caving物料路徑~Panel-caving material paths|碎礦與磨礦能量~Comminution energy|銅金回收balance~Copper/gold recovery balance|地下ventilation供電~Underground ventilation/power|尾礦與長期水管理~Tailings/long-term water')
add('kibali-mine','Kibali 大型金礦工程~Kibali large gold-mining engineering','mine','resources','resources-gold','kibali gold','多路徑採礦、支援電力與回收證據~Multiple mining routes, support power and recovery evidence','kibali','Kibali資源grade~Kibali resource grades|露天地下path區別~Surface/underground paths|碎磨與能量~Comminution/energy|金回收與產率~Gold recovery/yield|礦山支援與電力~Mine support/electricity|尾礦水與生命週期~Tailings/water/lifecycle')
add('pueblo-viejo','Pueblo Viejo 礦山與尾礦~Pueblo Viejo mine and tailings','mine','resources','resources-gold','pueblo gold','回收物料、尾礦與社區生命週期~Recovery materials, tailings and community lifecycle','pueblo','品位與區域sample~Grade/regional samples|礦石與廢石路徑~Ore/waste paths|粒度與能耗tradeoff~Size/energy tradeoff|金屬balance與回收~Metal balance/recovery|採礦支援邊界~Mine-support boundaries|尾礦設施與覆育~Tailings facilities/rehabilitation')
add('nome-creek-placer','Nome Creek 砂金與重力選別~Nome Creek placer gold and gravity separation','mine','resources','resources-gold','nome gold','密度分離、代表取樣與河川環境~Density separation, representative samples and river environments','nomecreek','砂金grade與取樣~Placer grades/sampling|允許區域與搬運~Permitted regions/handling|粒徑與形狀~Size/shape|重力選別balance~Gravity-separation balance|模擬數據與支援~Simulated data/support|溪流沉砂與覆育~Stream sediment/rehabilitation',history='BLM 指定的 Nome Creek 位於 Fairbanks 東北方，不是 Nome 市海灘。課程採假想顆粒資料做密度與質量收支，不提供未許可採礦或化學浸出作業。~BLM’s Nome Creek is northeast of Fairbanks, not Nome city beaches. The course uses assumed particles for density/material balances without unpermitted mining or chemical-leaching operations.')

# Fill additional neural schools without counting closely overlapping catalog cases twice.
D[:]=[r for r in D if r['slug'] not in ['nrel5mw','ocp-grand-teton','pueblo-viejo']]
source('autoencoder','深度自動編碼器原始研究','Original deep-autoencoder research','Hinton and Salakhutdinov','https://www.cs.toronto.edu/~hinton/papers.html','turn552search5')
source('lstm','LSTM 原始研究','Original LSTM paper','Hochreiter and Schmidhuber / MIT Press','https://doi.org/10.1162/neco.1997.9.8.1735','turn552search2')
source('ddpm','DDPM 原始研究','Original DDPM paper','Ho, Jain and Abbeel','https://arxiv.org/abs/2006.11239','turn552academia8')
add('mlp-autoencoder','深度 MLP 與自動編碼器~Deep MLP and autoencoder','nn','ai','ai-neural','autoencoder jax','全連接層、非線性與潛在瓶頸重建~Dense layers, nonlinearities and latent-bottleneck reconstruction','toronto','MLP weight與bias~MLP weights/biases|非線性與latent瓶頸~Nonlinearity/latent bottleneck|encoder-decoder梯度~Encoder-decoder gradients|全連接參數與activation~Dense parameters/activations|樣本與重建切分~Sample/reconstruction splits|潛在維度與失效~Latent dimensions/failure',example='假設MLP架構32→8→32，每層含bias：encoder有32×8+8=264參數，decoder有8×32+32=288，總552。線性瓶頸最多秩8；非線性增加表達能力但不保證泛化，重建loss不能代替任務驗證。~Assume MLP 32→8→32 with bias: encoder 264 parameters, decoder 288, total 552. A linear bottleneck has rank at most 8; nonlinear expression does not guarantee generalization, and reconstruction loss does not replace task validation.')
add('lstm-recurrent','LSTM 循環時序網路~LSTM recurrent sequence network','nn','ai','ai-neural','lstm jax','閘控記憶、共享權重與長時序梯度~Gated memory, shared weights and long-sequence gradients','lugano','input與hidden state~Input/hidden states|input forget output gates~Input/forget/output gates|cell state與梯度流~Cell state/gradient flow|時間展開與共享參數~Unrolling/shared parameters|時間切分與lookahead~Temporal splits/lookahead|long-horizon失效~Long-horizon failures',example='假設帶bias的標準四組LSTM矩陣，輸入d=6、hidden h=10，參數=4h(d+h+1)=680。若簡化記憶路徑forget固定0.95且忽略其他項，20步導數因子0.95²⁰≈0.358486；不是完整LSTM梯度或產品表現。~Assume four standard biased LSTM matrices with input d=6 and hidden h=10: 4h(d+h+1)=680 parameters. On a simplified memory path with fixed forget=0.95 and other terms omitted, a 20-step derivative factor is 0.358486, not the full LSTM gradient/performance.')
add('ddpm-diffusion','DDPM 擴散生成網路~DDPM diffusion-generation network','nn','ai','ai-neural','ddpm unet','前向加噪、時間條件去噪與反向採樣~Forward noising, time-conditioned denoising and reverse sampling','berkeley','clean sample與noise~Clean samples/noise|time-conditioned U-Net~Time-conditioned U-Net|noise prediction gradient~Noise-prediction gradients|sampling步數與記憶~Sampling steps/memory|來源與權利切分~Source/rights splits|生成品質與失效~Generation quality/failures',example='假設q(x_t|x_0)中ᾱ_t=0.81，x_0=2、ε=−1，x_t=√0.81×2+√0.19×(−1)=1.364110。這是單一前向加噪例；noise prediction loss與反向生成品質不同，非特定模型權重結果。~Assume alpha_bar=0.81, x0=2 and epsilon=−1: xt=sqrt(0.81)*2−sqrt(0.19)=1.364110. This is one forward-noising example; noise loss differs from reverse-generation quality and is not an output from model weights.')
assert len(D)==80, len(D)

NODES={
'sc':['微波控制器~Microwave controller','超導QPU~Superconducting QPU','讀出共振器~Readout resonator','經典解碼器~Classical decoder','低溫熱路~Cryogenic heat path'],
'ion':['位址雷射~Addressing lasers','離子與陷阱~Ions and trap','螢光讀出~Fluorescence readout','經典控制器~Classical controller','運動模態~Motional modes'],
'neutral':['光鑷與驅動~Tweezers and drive','原子陣列~Atom array','狀態讀出~State readout','經典控制器~Classical controller','Rydberg耦合~Rydberg coupling'],
'photon':['光子來源~Photon sources','多工與開關~Multiplexing and switches','糾纏資源~Entangled resources','光子偵測器~Photon detectors','經典回饋~Classical feedforward'],
'spin':['電壓與共振控制~Voltage/resonance control','矽量子點~Silicon quantum dots','電荷感測器~Charge sensors','經典控制器~Classical controller','低溫支援~Cryogenic support'],
'anneal':['問題編碼器~Problem encoder','耦合自旋QPU~Coupled-spin QPU','樣本讀出~Sample readout','經典解碼器~Classical decoder','低溫支援~Cryogenic support'],
'topo':['近接材料裝置~Proximity-material device','奇偶干涉計~Parity interferometer','電容讀出~Capacitance readout','推論模型~Inference models','證據比較~Evidence comparison'],
'nn':['輸入張量~Input tensors','表徵算子~Representation operators','輸出層~Output layer','損失函數~Loss function','梯度更新~Gradient update'],
'gpu':['主機控制~Host control','SM與矩陣核心~SMs and matrix cores','HBM記憶體~HBM memory','GPU互連~GPU interconnect','冷卻與供電~Cooling and power'],
'tpu':['主機與編譯~Host and compilation','張量計算核心~Tensor compute cores','HBM與嵌入~HBM and embeddings','晶片互連~Interchip links','叢集控制~Cluster control'],
'wafer':['本地SRAM核心~Local-SRAM cores','晶圓網格~Wafer mesh','參數記憶體~Parameter memory','梯度聚合~Gradient aggregation','供電與冷卻~Power and cooling'],
'neuro':['事件編碼器~Event encoder','可程式神經元~Programmable neurons','本地突觸~Local synapses','事件NoC~Event NoC','輸出解碼器~Output decoder'],
'server':['計算節點~Compute nodes','本地記憶體~Local memory','叢集網路~Cluster fabric','儲存階層~Storage tiers','供電與冷卻~Power and cooling'],
'nuclear':['民用熱源~Civil heat source','熱傳與蒸汽~Heat transfer and steam','汽輪發電機~Turbine-generator','冷凝排熱~Condensation/heat removal','支援與監測~Support and monitoring'],
'fusion':['磁體或雷射~Magnets or lasers','研究電漿~Research plasma','熱排出~Heat exhaust','診斷系統~Diagnostics','經典控制~Classical control'],
'wind':['風輪葉片~Rotor blades','傳動與發電機~Drivetrain/generator','功率轉換~Power conversion','支撐或繫泊~Supports/mooring','陣列與海纜~Array/cables'],
'hydro':['水庫與取水口~Reservoir/intake','水路~Waterways','水輪發電機~Turbine-generator','尾水與下池~Tailwater/lower pool','土建與監測~Civil works/monitoring'],
'geo':['熱儲層~Thermal reservoir','井羣~Wellfield','蒸汽或換熱器~Steam/heat exchangers','汽輪發電機~Turbine-generator','回注與監測~Reinjection/monitoring'],
'oil':['儲層~Reservoir','井筒與海底連接~Wells/subsea links','處理平臺~Processing platform','儲運介面~Storage/transfer','支援與監測~Support/monitoring'],
'mine':['礦體與樣本~Orebody/samples','物料搬運~Material handling','解離與選別~Liberation/separation','回收物料~Recovered materials','礦水尾礦管理~Water/tailings management'],
}

def assumed_example(r,i):
    family=r['family'];group=r['group']
    if family=='quantum':
        if group=='photon':
            n=4+(i%4);t=.90-.01*(i%3);p=t**n
            return f'假設 {n} 段光路各透過率 {t:.2f}，獨立串接成功率為 {t:.2f}^{n}={p:.6f}；總損耗 {-10*math.log10(p):.4f} dB。未含光源、偵測器及糾纏閘失敗，不能當作容錯閾值。~Assume {n} segments each transmit {t:.2f}: cascaded success {t:.2f}^{n}={p:.6f}, loss {-10*math.log10(p):.4f} dB. Sources, detectors and entangling-gate failure are excluded; this is not a fault-tolerance threshold.'
        if group=='neutral':
            ratio=1.05+.01*(i%3);factor=ratio**-6
            return f'假設兩原子交互作用能移服從 U=C6/r⁶，距離增為 {ratio:.2f} 倍且 C6 固定，U 比率={ratio:.2f}⁻⁶={factor:.6f}。這是兩體尺度比較，未含驅動、多體及讀出，非裝置控制設定。~Assume U=C6/r^6 for a pair. Increasing separation by {ratio:.2f} at fixed C6 changes U by {ratio:.2f}^-6={factor:.6f}. This omits drive, many-body effects and readout and is not a device setting.'
        if group=='anneal':
            return '假設二元目標 E(x1,x2)=2x1+2x2−3x1x2，四組成本依(00,01,10,11)為(0,2,2,1)，最小解00。以 x=(s+1)/2 重算等價 Ising，再比較常數偏移與最小解。這不是量子優勢證據。~For assumed E=2x1+2x2−3x1x2, (00,01,10,11) cost (0,2,2,1), minimum 00. Convert using x=(s+1)/2 and check constants/minima. This is not evidence of quantum advantage.'
        if group=='topo':
            return '假想讀出1000次，兩標籤各500次，錯分各5次與10次：兩類錯分率1%與2%，均衡錯分率1.5%。這只能量化該假想讀出，不能證明拓撲性、非阿貝爾操作或受保護邏輯位元。~Assume 1000 readouts with 500 per label and 5/10 misassignments: class errors 1%/2%, balanced error 1.5%. This quantifies assumed readout only, not topology, non-Abelian operations or protected logical qubits.'
        n=30+i*3;p=.001+.0001*(i%4);v=(1-p)**n
        return f'假設 {n} 個獨立且相同錯誤率 p={p:.4f} 的事件，無錯誤機率 (1−p)^{n}={v:.6f}。此簡化不含相干、相關、洩漏與讀出錯誤，不能預測完整量子電路或邏輯精度。~Assume {n} independent events with equal p={p:.4f}: no-error probability (1−p)^{n}={v:.6f}. Coherent, correlated, leakage and readout errors are omitted; this does not predict full-circuit/logical fidelity.'
    if family=='ai':
        if group=='nn':
            m=64+(i%4)*16;d=32;n=48;ops=2*m*d*n;bytes_=4*(m*d+d*n+m*n)
            return f'假設一次 FP32 矩陣乘法 A({m}×{d})B({d}×{n})，以乘加計2 FLOP，成本={ops} FLOP。只讀A、B及寫C一次最低流量={bytes_} byte，算術強度={ops/bytes_:.4f} FLOP/byte；未含反傳、快取與模型其他層。~Assume one FP32 product A({m}x{d})B({d}x{n}), counting multiply-add as 2 FLOP: {ops} FLOP. Single reads/writes need at least {bytes_} bytes, intensity {ops/bytes_:.4f} FLOP/byte; backward pass, caches and other layers are excluded.'
        if group=='neuro':
            return '假設1000個神經元各平均10次/s，每事件成本20 nJ，核心事件能量率為1000×10×20 nJ/s=0.2 mW。未含閒置、輸入編碼、讀出與供電；不能當成Loihi實測或端到端功率。~Assume 1000 neurons at 10 events/s with 20 nJ/event: event power is 0.2 mW. Idle, encoding, readout and supply are excluded; this is neither Loihi measurement nor end-to-end power.'
        intensity=2+i%6;bw=.8+.1*(i%3);peak=20+i
        return f'假設算術強度 I={intensity} FLOP/byte、頻寬 B={bw:.1f} TB/s、計算峯值 {peak} TFLOP/s，理想 roofline=min({peak},I×B)={min(peak,intensity*bw):.1f} TFLOP/s。皆非產品規格，未含同步、精度轉換或工作形狀損失。~Assume I={intensity} FLOP/byte, B={bw:.1f} TB/s and compute peak {peak} TFLOP/s: ideal roofline min({peak},I×B)={min(peak,intensity*bw):.1f} TFLOP/s. These are not product specifications; synchronization, precision conversion and shape inefficiency are omitted.'
    if family=='servers':
        f=.02+.005*(i%4);n=8+(i%4)*8;v=1/(f+(1-f)/n)
        return f'假設固定工作量有串行比例 {f:.3f}，使用 {n} 個理想同速工作者，Amdahl 上限 S=1/[f+(1−f)/N]={v:.4f}。通信、負載不均及I/O尚未計入，實效不得用此上限當實測。~Assume serial fraction {f:.3f} and {n} ideal equal workers: Amdahl upper bound S={v:.4f}. Communication, imbalance and I/O are omitted; this bound is not measured performance.'
    if r['group']=='nuclear':
        q=400+(i%4)*100;eta=.30+.01*(i%3);aux=8+(i%5);out=q*eta-aux
        return f'假設民用熱源 {q} MWth、熱電效率 {eta:.2f}、輔機 {aux} MWe，淨電={q}×{eta:.2f}−{aux}={out:.1f} MWe；循環排熱約{q*(1-eta):.1f} MW。僅熱平衡，不含反應性、燃料製造或操作整定。~Assume civil heat input {q} MWth, efficiency {eta:.2f} and auxiliaries {aux} MWe: net power {out:.1f} MWe; cycle rejection about {q*(1-eta):.1f} MW. This is heat balance only, without reactivity, fuel manufacture or operating settings.'
    if r['group']=='fusion':
        return '假設融合輸出100 MW、指定等離子體加熱20 MW，Qplasma=5；若驅動電效率40%、熱電效率35%、其他輔機10 MW，假想淨電=100×0.35−20/0.40−10=−25 MW。忽略其他回收熱，說明Q>1不自動等於淨發電。~Assume fusion output 100 MW and specified plasma heating 20 MW: Qplasma=5. With driver efficiency 40%, conversion 35% and auxiliaries 10 MW, assumed net=35−50−10=−25 MW. Other recovered heat is omitted; Q>1 does not ensure net electricity.'
    if r['group']=='wind':
        a=80+(i%4)*10;v=8+(i%3);cp=.40;power=.5*1.225*a*v**3*cp
        return f'教學小型風輪假設ρ=1.225 kg/m³、面積{a} m²、風速{v} m/s、Cp=0.40，P=0.5ρAv³Cp={power/1000:.4f} kW。未含傳動電損、尾流、額定限值與風速分佈，不是本工程產品數值。~Assume a teaching rotor with rho=1.225 kg/m³, A={a} m², v={v} m/s and Cp=0.40: P={power/1000:.4f} kW. Drivetrain/electrical loss, wakes, ratings and wind distributions are excluded; these are not project specifications.'
    if r['group']=='hydro':
        h=30+(i%4)*10;q=5+(i%3);eta=.88;out=1000*9.81*q*h*eta
        return f'假設淨水頭{h} m、流量{q} m³/s、效率0.88，P=1000×9.81×{q}×{h}×0.88={out/1e6:.6f} MW。另若抽蓄上下流程效率均0.88，往返效率0.7744；高程、流量皆是假想，非場站規格。~Assume net head {h} m, flow {q} m³/s and efficiency 0.88: P={out/1e6:.6f} MW. Two pumped-cycle legs at 0.88 yield round-trip efficiency 0.7744. Inputs are assumed, not plant specifications.'
    if r['group']=='geo':
        md=12+(i%3)*3;dh=250+(i%4)*20;q=md*dh;eta=.12;aux=.1
        return f'假設流體{md} kg/s、比焓降{dh} kJ/kg，熱量率={q} kW；轉換效率0.12、輔機100 kW，淨電={q*.12-100:.1f} kW。未含儲層可持續性、相變細節與回注冷卻，非鑽井或現場設定。~Assume flow {md} kg/s and enthalpy drop {dh} kJ/kg: heat rate {q} kW. At conversion 0.12 and auxiliaries 100 kW, net={q*.12-100:.1f} kW. Reservoir sustainability, phase details and reinjection cooling are omitted; no field settings are given.'
    if r['group']=='oil':
        return '假想一日液體進料1000 t，油700 t、水280 t、未判明20 t。質量閉合=98%，未判明2%須保留；不能把全部差額直接當洩漏，需核對取樣、庫存與量測。無實際井壓、鑽進或井控操作。~Assume daily liquid feed 1000 t, oil 700 t, water 280 t and unassigned 20 t: closure 98%, unresolved 2%. Do not call the entire residual leakage; check samples, inventory and measurements. No well-pressure, drilling or well-control operations are provided.'
    mass=800+(i%4)*100;grade=1.5+.1*(i%3);recovery=.85;metal=mass*grade*recovery
    return f'假設乾給料{mass} t、品位{grade:.1f} g/t、金屬回收率0.85，可回收金屬={metal:.1f} g={metal/1000:.4f} kg。回收率不同於精礦品位；未含礦物解離、處理成本或任何浸出配方，非礦場實測。~Assume dry feed {mass} t, grade {grade:.1f} g/t and metal recovery 0.85: recovered metal {metal:.1f} g={metal/1000:.4f} kg. Recovery differs from concentrate grade; liberation/costs and all leaching recipes are excluded; this is not a mine measurement.'

DISC={
'quantum-superconducting':'超導量子系統~Superconducting quantum systems','quantum-ion':'離子陷阱量子系統~Trapped-ion quantum systems','quantum-neutral':'中性原子量子系統~Neutral-atom quantum systems','quantum-photon':'光子量子系統~Photonic quantum systems','quantum-spin':'半導體自旋量子系統~Semiconductor-spin quantum systems','quantum-annealing':'量子退火~Quantum annealing','quantum-qec':'量子證據與錯誤更正~Quantum evidence and error correction','quantum-topological':'拓撲量子研究與證據~Topological quantum research and evidence','ai-neural':'神經網路架構~Neural-network architectures','ai-gpu':'GPU與平行架構~GPU and parallel architectures','ai-tpu':'TPU與專用加速器~TPU and specialized accelerators','ai-wafer':'晶圓尺度計算~Wafer-scale compute','ai-neuromorphic':'神經形態計算~Neuromorphic compute','server-design':'伺服器平臺工程~Server-platform engineering','servers-hpc':'大型計算系統~Large computing systems','energy-nuclear':'民用核能發電~Civil nuclear generation','energy-smr':'小型模組發電~Small modular generation','energy-fusion':'和平融合研究工程~Peaceful fusion research','energy-wind':'風輪與風電工程~Rotors and wind engineering','energy-hydro':'水力與抽蓄工程~Hydro and pumped-storage engineering','energy-geothermal':'地熱儲層與電力~Geothermal resources and power','resources-oil':'油氣與海上資源~Oil/gas and offshore resources','resources-gold':'金礦與砂金工程~Gold and placer engineering','resources-mining':'礦業物料與系統~Mining materials and systems'}
SCOPES={
'quantum':'依公開研究與裝置資料編寫的離線模型、編譯及證據判讀。不是實機組裝、雷射或低溫作業SOP；假想算例不代表廠商精度、量子優勢或容錯能力。研發宣稱與已驗證觀測分開標示。~Offline models, compilation and evidence interpretation from public research/device sources. Not hardware assembly, laser/cryogenic SOPs; assumed examples are not vendor fidelity, advantage or fault tolerance. Development claims and demonstrated observations remain distinct.',
'ai':'原創張量、運算成本及失效分析。架構圖是功能教學示意，非晶片floorplan或專有電路；數字為假想，需依精度、shape、資料分佈與系統邊界重算。~Original tensor, compute-cost and failure analysis. Functional diagrams are not chip floorplans/proprietary circuits; assumed values need recalculation for precision, shape, data and boundaries.',
'servers':'公開伺服器與超算架構的離線工作流、通信、儲存及能量模型；非機櫃接線、供電施工或實體維護SOP，也不表示學員取得廠商／研究中心設備存取。~Offline workflow, fabric, storage and energy models of public servers/HPC. No rack-wiring, power-installation or physical-maintenance SOP and no vendor/research-center hardware access is implied.',
'energy':'和平民用發電與融合研究的公開熱循環、功能架構及工程證據。核能不包含燃料製備、濃縮、武器、反應性整定或反應爐操作；地熱、風電及水力不提供未經場址驗證的施工／操作參數。算例皆是假想，實機由合格專業團隊依規範負責。~Public thermal cycles, functional architecture and engineering evidence for peaceful generation/fusion research. Nuclear content excludes fuel production, enrichment, weapons, reactivity settings and reactor operations. Geothermal/wind/hydro supply no unverified construction/operation settings. Examples are hypothetical; qualified professionals govern actual equipment.',
'resources':'公開資源工程的離線質量、能量及環境證據判讀；不提供鑽井、井控、採掘、爆破或危險化學浸出SOP。採礦權、許可、地質完整性與現場規範需由合格團隊另行確認，課程完成不是操作資格。~Offline public resource-engineering material/energy/environmental analysis; no drilling, well-control, excavation, blasting or hazardous-leaching SOP. Qualified teams separately establish rights, permits, integrity and field requirements; completion is not operating qualification.'}
TRANSFER={
'quantum':'可遷移量子狀態、控制、量測及不確定度模型；實體編碼與硬體限制需重設。~Quantum states, control, measurement and uncertainty transfer, while physical encodings/hardware constraints must be respecified.',
'ai':'可遷移張量、數值誤差及計算／記憶體收支；算子、精度與資料歸納假設需重設。~Tensor, numerical-error and compute/memory accounting transfer while operators, precision and data assumptions must be respecified.',
'servers':'可遷移節點、互連、I/O及復原的分層分析；拓撲、資源配置與工作流不同。~Layered node, fabric, I/O and recovery analysis transfers, with different topology, resources and workflows.',
'energy':'可遷移能量守恆、熱路、載荷與驗證證據；熱源、工作流體及安全邊界不同。~Energy conservation, heat paths, loads and validation evidence transfer, with different heat sources, fluids and safety boundaries.',
'resources':'可遷移物料守恆、代表取樣及環境證據；物相、搬運路徑與回收方法需重設。~Material balance, representative sampling and environmental evidence transfer while phases, handling paths and recovery methods must be respecified.'}

def freeze():
    # Re-authoring retains the initial V10 identities even after root integration.
    frozen=P/'expansion_inputs.json'
    catalog=json.loads(frozen.read_text())['catalogSnapshot'] if frozen.exists() else json.loads((ROOT/'public/academy/data/catalog.json').read_text())
    cat={c['id']:c for c in catalog};selected=[]
    family_members={f:[r for r in D if r['family']==f] for f in SCOPES}
    groups={g:[r for r in D if r['group']==g] for g in {x['group'] for x in D}}
    neural_nodes={
    'resnet':['影像輸入~Image input','卷積stem~Convolutional stem','殘差blocks~Residual blocks','全域pooling~Global pooling','分類器~Classifier'],
    'transformer':['Token與位置~Tokens/positions','QKV投影~QKV projections','遮罩注意力~Masked attention','前饋層~Feed-forward layers','序列輸出~Sequence output'],
    'unet':['影像輸入~Image input','收縮encoder~Contracting encoder','瓶頸~Bottleneck','擴張decoder~Expanding decoder','像素輸出~Pixel output'],
    'graph-attention':['節點特徵~Node features','圖鄰域遮罩~Graph-neighborhood mask','注意力聚合~Attention aggregation','節點輸出~Node outputs','任務損失~Task loss'],
    'sparse-moe':['輸入特徵~Input features','門控router~Gating router','專家網路~Expert networks','加權聚合~Weighted aggregation','輸出~Output'],
    'mlp-autoencoder':['輸入向量~Input vector','全連接encoder~Dense encoder','潛在瓶頸~Latent bottleneck','全連接decoder~Dense decoder','重建向量~Reconstructed vector'],
    'lstm-recurrent':['時序輸入~Sequence input','LSTM閘控cell~LSTM gated cell','Hidden state~Hidden state','Cell state~Cell state','輸出投影~Output projection'],
    'ddpm-diffusion':['資料與噪聲排程~Data/noise schedule','帶噪x_t~Noisy x_t','時間條件U-Net~Time-conditioned U-Net','去噪loss~Denoising loss','反向採樣~Reverse sampling']}
    curated_related={
    'ibm-heron':['google-willow','rigetti-ankaa'],'google-willow':['ibm-heron','quantinuum-h2'],'rigetti-ankaa':['ibm-heron','google-willow'],
    'quantinuum-h2':['ionq-forte','quera-aquila'],'ionq-forte':['quantinuum-h2','pasqal-fresnel'],'quera-aquila':['pasqal-fresnel','quantinuum-h2'],'pasqal-fresnel':['quera-aquila','ionq-forte'],
    'xanadu-aurora':['psiquantum-omega','google-willow'],'psiquantum-omega':['xanadu-aurora','intel-tunnel-falls'],'intel-tunnel-falls':['ibm-heron','majorana-parity'],'dwave-advantage2':['quera-aquila','ibm-heron'],'majorana-parity':['intel-tunnel-falls','google-willow'],
    'resnet':['unet','mlp-autoencoder'],'transformer':['lstm-recurrent','graph-attention'],'unet':['resnet','ddpm-diffusion'],'graph-attention':['transformer','mlp-autoencoder'],'sparse-moe':['transformer','cerebras-cs3'],'mlp-autoencoder':['resnet','lstm-recurrent'],'lstm-recurrent':['transformer','intel-loihi2'],'ddpm-diffusion':['unet','transformer'],
    'nvidia-hopper':['nvidia-blackwell','dgx-h100'],'nvidia-blackwell':['nvidia-hopper','gb200-nvl72'],'google-tpu-v4':['google-tpu-v5p','aws-trainium'],'google-tpu-v5p':['google-tpu-v4','cerebras-cs3'],'aws-trainium':['google-tpu-v5p','dgx-h100'],'cerebras-cs3':['google-tpu-v5p','gb200-nvl72'],'intel-loihi2':['lstm-recurrent','cerebras-cs3']}
    for i,r in enumerate(D):
        special={'resnet':'resnetspecial','transformer':'transformerspecial','unet':'unetspecial','graph-attention':'gatspecial','sparse-moe':'moespecial','mlp-autoencoder':'autospecial','lstm-recurrent':'lstmspecial','ddpm-diffusion':'diffusionspecial'}.get(r['slug'])
        if special:r['units']=[special+str(j) for j in range(1,4)]+['nn4','nn5','nn6']
        if r['slug']=='ionq-forte':r['units'][4]='fortespecial1'
        if r['slug']=='nome-creek-placer':r['units'][4]='placerspecial1'
        if r['slug']=='ap1000':r['sources']=['ap1000','nrc','vogtle']
        if r['slug']=='barakah-apr1400':r['sources']=['barakah','nrc','smr']
        if r['slug']=='xanadu-aurora':
            r['units']=['photon1','auroraspecial1','photon3','auroraspecial2','auroraspecial3','photon6']
            r['sources']=['auroraq','aurorapaper','qbasic']
            r['anchors'][1]='擠壓態與PNR條件資源~Squeezed states/PNR-heralded resources'
            r['anchors'][4]='PNR與homodyne量測~PNR/homodyne measurement'
        if r['discipline'] in ('server-design','servers-server-design'):r['discipline']='server-design'
        if r['slug']=='majorana-parity':r['discipline']='quantum-topological'
        if r['slug']=='google-willow':
            r['discipline']='quantum-qec';r['extraLearningTags']=['quantum-superconducting']
            r['scopeExtra']='特定表面碼記憶實驗的閾值以下結果，不等同完整容錯通用電腦或任意工作負載上的量子優勢。~Below-threshold results from particular surface-code memory experiments do not establish a complete fault-tolerant universal computer or advantage on arbitrary workloads.'
        if r['slug']=='nif-energy-systems':
            r['example']='假想單次脈衝：到target的雷射能量2 MJ、融合輸出3 MJ，Qtarget=1.5。若wall-plug雷射效率2%，電網驅動需100 MJ；僅回收融合熱且熱電效率35%，輸出1.05 MJ；另有5 MJ輔助輸入，淨能量=1.05−100−5=−103.95 MJ。未回收雷射熱，皆為假想而非NIF實測；target gain不等於電廠淨電。~Assume one pulse with laser energy 2 MJ at the target and fusion output 3 MJ: Qtarget=1.5. At assumed wall-plug laser efficiency 2%, driver input is 100 MJ. Recovering only fusion heat at 35% gives 1.05 MJ; auxiliaries consume 5 MJ, so net=1.05−100−5=−103.95 MJ. Laser-heat recovery is omitted; values are hypothetical, not NIF measurements. Target gain is not plant net electricity.'
        if r['id'] in cat:
            old=cat[r['id']];assert old.get('status')!='guided'
            r['title']=old['title']+'~'+old['titleEn'];selected.append(copy.deepcopy(old))
        track=r['family'];r['track']=track
        r['category']='computing' if track in ['quantum','ai','servers'] else 'energy' if track=='energy' else 'materials'
        # Track 'energy' contains multiple unit groups; examples use group dispatch.
        g=r['group'];nodes=r['architectureNodes'] or neural_nodes.get(r['slug']) or NODES[g]
        if r['slug']=='utah-forge':nodes=['研究熱儲層~Research thermal reservoir','研究井群~Research wellfield','壓力與流量量測~Pressure/flow measurements','後續熱循環假想模型~Prospective hypothetical-cycle model','研究回注與監測~Research reinjection/monitoring']
        if r['slug']=='xanadu-aurora':nodes=['擠壓光源~Squeezed-light sources','PNR條件資源~PNR-heralded resources','多工與refinery~Multiplexing/refinery','叢集態與homodyne~Cluster states/homodyne','經典解碼回饋~Classical decode/feedforward']
        if r['slug']=='nif-energy-systems':nodes=['雷射能量系統~Laser-energy system','研究target與plasma~Research target/plasma','假想能量帳本~Hypothetical energy balance','能量診斷~Energy diagnostics','研究資料分析~Research-data analysis']
        if r['slug'] in ['mingtan-storage','nant-storage']:nodes=['上池水庫~Upper reservoir','壓力水路~Pressure waterways','可逆泵水輪機與電機~Reversible pump-turbine/motor-generator','下池水庫~Lower reservoir','土建與監測~Civil works/monitoring']
        if r['slug'] in ['esbwr','darlington-bwrx300']:nodes=['沸水熱源與容器~Boiling-water heat source/vessel','蒸汽分離路徑~Steam-separation path','汽輪發電機~Turbine-generator','冷凝與給水~Condensation/feedwater','支援與監測~Support/monitoring']
        r['architectureNodes']=[s.split('~',1) for s in nodes]
        r['architectureFamily']={'quantum':'qpu','ai':'ai','servers':'server'}.get(track,{'nuclear':'thermal','fusion':'fusion','wind':'wind','hydro':'hydro','geo':'geothermal','oil':'oil','mine':'mining'}.get(g))
        if r['slug']=='lstm-recurrent':r['architectureEdges']=[[0,1],[1,2],[1,3],[2,1],[3,1],[2,4]]
        elif r['slug']=='xanadu-aurora':r['architectureEdges']=[[0,1],[1,2],[2,3],[3,4],[4,2],[4,3]]
        elif r['slug']=='graph-attention':r['architectureEdges']=[[0,2],[1,2],[2,3],[3,4]]
        elif r['slug']=='sparse-moe':r['architectureEdges']=[[0,1],[0,2],[1,2],[2,3],[3,4]]
        elif r['slug']=='unet':r['architectureEdges']=[[0,1],[1,2],[2,3],[1,3],[3,4]]
        elif r['slug']=='ddpm-diffusion':r['architectureEdges']=[[0,1],[0,2],[1,2],[2,3],[2,4]]
        elif r['slug']=='utah-forge':r['architectureEdges']=[[0,1],[1,2],[2,3],[1,4],[4,0]]
        elif r['slug']=='nif-energy-systems':r['architectureEdges']=[[0,1],[0,3],[1,3],[3,4],[1,2]]
        elif r['slug'] in ['mingtan-storage','nant-storage']:r['architectureEdges']=[[0,1],[1,2],[2,3],[3,2],[2,1],[1,0],[4,1],[4,2]]
        elif r['slug'] in ['esbwr','darlington-bwrx300']:r['architectureEdges']=[[0,1],[1,2],[2,3],[3,0],[4,0],[4,3]]
        elif g=='gpu':r['architectureEdges']=[[0,1],[1,2],[2,1],[1,3],[3,1],[4,1],[4,2]]
        elif g=='tpu':r['architectureEdges']=[[0,1],[1,2],[2,1],[1,3],[3,1],[4,0],[4,3]]
        elif g=='wafer':r['architectureEdges']=[[2,0],[0,3],[3,2],[1,0],[0,1],[4,0]]
        elif g=='neuro':r['architectureEdges']=[[0,1],[1,2],[2,1],[1,3],[3,1],[3,4]]
        elif g=='mine':r['architectureEdges']=[[0,1],[1,2],[2,3],[2,4]]
        elif g=='oil':r['architectureEdges']=[[0,1],[1,2],[2,3],[4,1],[4,2]]
        elif g in ['photon','nn','topo']:
            r['architectureEdges']=[[0,1],[1,2],[2,3],[3,4]]
        elif g in ['sc','ion','neutral','spin','anneal']:
            r['architectureEdges']=[[0,1],[1,2],[2,3],[3,0],[4,1]]
        elif g=='server':r['architectureEdges']=[[0,1],[0,2],[2,3],[4,0]]
        elif g=='nuclear':r['architectureEdges']=[[0,1],[1,2],[2,3],[3,1],[4,0],[4,3]]
        elif g=='fusion':r['architectureEdges']=[[0,1],[1,2],[1,3],[3,4],[4,0]]
        elif g=='wind':r['architectureEdges']=[[0,1],[1,2],[2,4],[3,0],[3,1]]
        elif g=='hydro':r['architectureEdges']=[[0,1],[1,2],[2,3],[4,0],[4,1]]
        elif g=='geo':r['architectureEdges']=[[0,1],[1,2],[2,3],[2,4],[4,0]]
        else:r['architectureEdges']=[[0,1],[1,2],[2,3],[3,4]]
        r['diagram']='optics' if g in ['photon','ion','neutral'] else 'power' if track in ['energy','resources'] else 'network'
        pl=PL[r['placeKey']];r['place']={'name':pl[0],'country':pl[1],'lat':pl[2],'lng':pl[3],'query':pl[4]}
        if not r['history']:
            z,en=r['title'].split('~',1);f,fe=r['focus'].split('~',1)
            r['history']=f'{z}的公開資料展示{f}的工程脈絡；本課以不同功能層與可驗證輸出重建教學案例，不宣稱取得任何專有製造流程。~Public sources for {en} illustrate {fe.lower()}. The course reconstructs functional layers and verifiable outputs educationally without proprietary manufacturing access.'
        r['example']=r['example'] or assumed_example(r,i)
        choices=groups[g]
        # Modalities with one member compare with two physically different quantum schools.
        if len(choices)<3:choices=family_members[track]
        at=choices.index(r)
        r['related']=[choices[(at+1)%len(choices)]['id'],choices[(at+2)%len(choices)]['id']]
        if r['slug'] in curated_related:
            by_slug={item['slug']:item for item in D}
            r['related']=[by_slug[slug]['id'] for slug in curated_related[r['slug']]]
        assert len(r['sources'])>=2
    out={'version':11,'stageTitles':['系統邊界與基本原理~System boundaries and principles','功能架構與量化模型~Functional architecture and quantitative models','獨立驗證與工程交接~Independent validation and engineering handoff'],'sources':S,'catalogSnapshot':selected,'units':UNITS,'projects':D,'disciplineNames':DISC,'scopes':SCOPES,'transfers':TRANSFER,'coverage':{'quantum':12,'neuralAndAccelerators':15,'servers':9,'civilNuclearAndSMR':8,'fusionResearch':8,'wind':7,'hydroStorage':6,'geothermal':6,'oilGas':5,'miningGold':4},'enrichmentRequests':[{'courseId':cid,'preserveGuidedSteps':True,'sourceKeys':keys,'reason':'由資訊100教材先整合；此清單不覆寫原步驟。','reasonEn':'Integrate through IT100 first; this list does not overwrite existing tasks.'} for cid,keys in [('a392',['perlmutter']),('a393',['alps']),('a394',['dgx']),('a395',['elcapitan']),('a396',['jupiter'])]]}
    (P/'expansion_inputs.json').write_text(json.dumps(out,ensure_ascii=False,indent=2)+'\n')
    print(json.dumps({'projects':len(D),'existingRoadmaps':len(selected),'sources':len(S),'authoredTechnicalUnits':len(UNITS)},ensure_ascii=False))

if __name__=='__main__':freeze()
