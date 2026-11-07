/* Original, bounded teaching models. All values are synthetic and require independent engineering validation. */
(function (root) {
  'use strict';

  const MU = 398600.435507; // km³/s², Earth GM (JPL DE440)
  const EARTH_RADIUS = 6378.1363; // km, reference equatorial radius
  const G0 = 9.80665; // m/s²
  const SIGMA = 5.670374419e-8; // W/(m² K⁴)
  const C = 299792458; // m/s
  const K = 1.380649e-23; // W/(Hz K)
  const TAU = 2 * Math.PI;
  const SUN_AT_EARTH = 1361; // W/m², nominal teaching value at 1 AU

  const input = (key, zh, en, unit, value, min, max, step, integer = false) => ({key, label:[zh,en], unit, value, min, max, step, integer});
  const output = (key, zh, en, unit) => ({key, label:[zh,en], unit});
  const period = radius => TAU * Math.sqrt(radius ** 3 / MU);
  const speed = radius => Math.sqrt(MU / radius);
  const apsisSpeed = (radius, semiMajor) => Math.sqrt(MU * (2 / radius - 1 / semiMajor));
  const sources = {
    jpl:['JPL · Astrodynamic Parameters','https://ssd.jpl.nasa.gov/astro_par.html'],
    trajectories:['NASA · Basics of Space Flight, Trajectories','https://science.nasa.gov/learn/basics-of-space-flight/chapter4-1/'],
    mechanics:['NASA · Basics of Space Flight, Gravity & Mechanics','https://science.nasa.gov/learn/basics-of-space-flight/chapter3-3/'],
    rocket:['NASA Glenn · Ideal Rocket Equation','https://www1.grc.nasa.gov/beginners-guide-to-aeronautics/ideal-rocket-equation/'],
    radio:['ITU-R P.525-5 · Free-space attenuation','https://www.itu.int/rec/R-REC-P.525-5-202411-I/en'],
    power:['NASA Small Spacecraft Technology · Power','https://www.nasa.gov/smallsat-institute/sst-soa/power-subsystems/'],
    irradiance:['NASA Goddard · Solar Irradiance Science','https://earth.gsfc.nasa.gov/climate/projects/solar-irradiance/science'],
    thermal:['NASA NTRS · Thermal Management in Space','https://ntrs.nasa.gov/api/citations/19930007716/downloads/19930007716.pdf'],
    gnc:['NASA Small Spacecraft Technology · Guidance, Navigation and Control','https://www.nasa.gov/smallsat-institute/sst-soa/guidance-navigation-and-control/'],
    gsd:['U.S. Bureau of Land Management · Photogrammetric Technology, p. 30','https://www.blm.gov/sites/default/files/documents/files/Library_BLMTechnicalNote428_0.pdf'],
    landsat:['USGS · EO-1 sensor sample distances','https://www.usgs.gov/centers/eros/eo-1-sensors']
  };

  const models = [
    {
      id:'circular-orbit', group:['軌道力學','Orbital mechanics'], title:['圓軌道速度與週期','Circular orbit speed and period'],
      formula:'r = R⊕ + h   |   v = √(μ/r)   |   T = 2π√(r³/μ)',
      assumption:['地球採球對稱、二體圓軌道；高度以固定參考半徑計算，省略大氣阻力、地球扁率及攝動。','Spherical Earth and a two-body circular orbit. Altitude uses a fixed reference radius. Drag, oblateness and perturbations are omitted.'],
      prompt:['從 550 km 提高到 1,100 km，軌道速度與週期各往哪個方向變化？比較相同高度下的圓軌道與逃逸速度。','Raise altitude from 550 km to 1,100 km. Which direction do speed and period move? Compare circular and escape speed at the same altitude.'],
      references:[sources.jpl,sources.mechanics],
      inputs:[input('altitude','軌道高度','Altitude','km',550,150,45000,10)],
      outputs:[output('period','公轉週期','Orbital period','min'),output('speed','圓軌道速度','Circular speed','km/s'),output('escape','當地逃逸速度','Local escape speed','km/s')],
      run(p) { const r = EARTH_RADIUS + p.altitude; return {period:period(r)/60,speed:speed(r),escape:Math.sqrt(2)*speed(r)}; }
    },
    {
      id:'hohmann', group:['軌道力學','Orbital mechanics'], title:['霍曼轉移與兩次脈衝','Hohmann transfer and two burns'],
      formula:'aₜ = (r₁+r₂)/2   |   vₜ(r) = √[μ(2/r−1/aₜ)]   |   tₜ = π√(aₜ³/μ)',
      assumption:['兩端皆為同向、同平面圓軌道。脈衝視為瞬時切向施加；正號代表順行，負號代表逆行。高度相同時無需轉移。','Both endpoints are co-prograde, coplanar circular orbits. Burns are instantaneous and tangential. Positive is prograde, negative retrograde. Equal altitudes require no transfer.'],
      prompt:['先做升軌，再對調兩個高度。比較有號 Δv、總脈衝需求及轉移時間。','Raise the orbit, then swap the endpoints. Compare signed burns, total Δv and transfer time.'],
      references:[sources.trajectories,sources.jpl],
      inputs:[input('from','起始圓軌道高度','Initial circular altitude','km',500,150,45000,10),input('to','目標圓軌道高度','Target circular altitude','km',35786,150,45000,10)],
      outputs:[output('deltaV','總脈衝需求','Total Δv','m/s'),output('first','第一脈衝','First burn','m/s'),output('second','第二脈衝','Second burn','m/s'),output('time','轉移飛行時間','Transfer coast time','min')],
      sweep:'to',
      run(p) {
        const r1 = EARTH_RADIUS+p.from, r2 = EARTH_RADIUS+p.to, a = (r1+r2)/2;
        const first = r1 === r2 ? 0 : 1000*(apsisSpeed(r1,a)-speed(r1));
        const second = r1 === r2 ? 0 : 1000*(speed(r2)-apsisSpeed(r2,a));
        return {deltaV:Math.abs(first)+Math.abs(second),first,second,time:r1===r2 ? 0 : period(a)/120};
      }
    },
    {
      id:'rocket-equation', group:['推進','Propulsion'], title:['火箭方程式與推進劑裕度','Rocket equation and propellant margin'],
      formula:'Δv = g₀ Iₛₚ ln(m₀/mf)   |   m_used = m₀(1−exp(−Δv_req/(g₀ Iₛₚ)))',
      assumption:['單段理想燃燒，比衝固定。終態質量含保留推進劑與有效載荷。省略重力、氣動、轉向與有限燃燒時間損失。','A single ideal burn at constant specific impulse. Final mass includes reserved propellant and payload. Gravity, drag, steering and finite-burn losses are omitted.'],
      prompt:['固定初始與終態質量，提高比衝。若需求裕度為負，先區分質量限制與額外飛行損失。','Hold initial and final mass fixed and increase specific impulse. If margin is negative, separate the mass constraint from any additional flight losses.'],
      references:[sources.rocket],
      inputs:[input('initial','初始質量','Initial mass','kg',150,1,100000,1),input('final','終態質量','Final mass','kg',112,1,100000,1),input('isp','真空比衝','Vacuum specific impulse','s',220,50,5000,5),input('requested','任務 Δv 需求','Required Δv','m/s',550,0,20000,10)],
      outputs:[output('deltaV','可用理想 Δv','Available ideal Δv','m/s'),output('margin','需求裕度','Margin against requirement','m/s'),output('used','達標的理想推進劑需求','Ideal propellant needed','kg')],
      sweep:'isp',
      run(p) {
        if (p.final > p.initial) throw new RangeError('mass-order');
        const exhaust = G0*p.isp, deltaV = exhaust*Math.log(p.initial/p.final);
        return {deltaV,margin:deltaV-p.requested,used:-p.initial*Math.expm1(-p.requested/exhaust)};
      }
    },
    {
      id:'radio-link', group:['通訊','Communications'], title:['下行鏈路與 Eb/N₀ 裕度','Downlink and Eb/N₀ margin'],
      formula:'Lfs = 20 log₁₀(4πdf/c)   |   Pr = Pt+Gt+Gr−Lfs−Lother   |   Eb/N₀ = Pr−10 log₁₀(kT)−10 log₁₀(Rb)',
      assumption:['自由空間傳播，距離為斜距。將饋線、偏振、指向、大氣及實作損耗併入其他損失。溫度是等效系統雜訊溫度；門檻取決於實際調變、編碼與誤碼率目標。','Free-space propagation using slant range. Include feeder, polarization, pointing, atmospheric and implementation losses in other loss. Use equivalent system noise temperature. Required threshold depends on modulation, coding and the target error rate.'],
      prompt:['將斜距或位元率加倍。比較兩者各損失幾 dB，並判斷是否還達到門檻。','Double slant range or bit rate. Compare the dB lost in each case and check whether the threshold is still met.'],
      references:[sources.radio],
      inputs:[input('distance','斜距','Slant range','km',1200,100,500000,50),input('frequency','載波頻率','Carrier frequency','GHz',2.25,.1,40,.05),input('power','發射端功率','Transmit power','dBW',3,-30,60,.5),input('tx','發射天線增益','Transmit antenna gain','dBi',5,-10,80,.5),input('rx','接收天線增益','Receive antenna gain','dBi',26,-10,90,.5),input('loss','其他鏈路損失','Other link loss','dB',4,0,90,.5),input('temperature','系統雜訊溫度','System noise temperature','K',500,25,5000,25),input('bitrate','資訊位元率','Information bit rate','Mbit/s',1,.01,500,.01),input('required','所需 Eb/N₀','Required Eb/N₀','dB',8,-10,35,.5)],
      outputs:[output('margin','鏈路裕度','Link margin','dB'),output('pathLoss','自由空間衰減','Free-space path loss','dB'),output('receive','接收功率','Received power','dBW'),output('cn0','載波對雜訊密度','Carrier-to-noise density','dB-Hz'),output('ebn0','每位元能量對雜訊密度','Eb/N₀','dB')],
      run(p) {
        const pathLoss = 20*Math.log10(4*Math.PI*p.distance*1e3*p.frequency*1e9/C);
        const receive = p.power+p.tx+p.rx-pathLoss-p.loss;
        const cn0 = receive-10*Math.log10(K*p.temperature), ebn0 = cn0-10*Math.log10(p.bitrate*1e6);
        return {margin:ebn0-p.required,pathLoss,receive,cn0,ebn0};
      }
    },
    {
      id:'power-eclipse', group:['電力與能源','Electrical power'], title:['食期電池與日照回充','Eclipse battery and sunlight recharge'],
      formula:'E_load = Pₑtₑ   |   E_bat,min = E_load/(ηdis·DoD)   |   P_day,min = P_dayload + E_load/(ηdis·ηch·t_day)',
      assumption:['兩段負載皆為常數。計入充放電效率及最大放電深度，未計電池老化、溫度、轉換器瞬態、陣列衰退或營運裕度。','Each phase uses a constant load. Includes charge/discharge efficiency and maximum depth of discharge. Battery aging, temperature, converter transients, array degradation and operational reserves are omitted.'],
      prompt:['將食期拉長 10 分鐘，並同步縮短日照 10 分鐘。比較電池容量與日照功率兩個結果，說明哪項變化更陡。','Add 10 minutes of eclipse while removing 10 minutes of sunlight. Compare the change in battery capacity and daylight power.'],
      references:[sources.power],
      inputs:[input('eclipseLoad','食期負載','Eclipse load','W',36,0,5000,1),input('eclipse','食期時間','Eclipse duration','min',35,0,120,1),input('sunLoad','日照負載','Sunlight load','W',48,0,5000,1),input('sunTime','日照時間','Sunlight duration','min',62,1,1440,1),input('dod','允許放電深度','Allowed depth of discharge','%',30,5,100,1),input('discharge','放電效率','Discharge efficiency','%',95,20,100,1),input('charge','回充效率','Charge efficiency','%',92,20,100,1)],
      outputs:[output('capacity','最小電池標稱能量','Minimum nominal battery energy','Wh'),output('dayPower','最低日照供電能力','Minimum daylight supply','W'),output('eclipseEnergy','食期負載用電','Eclipse load energy','Wh')],
      sweep:'eclipse',
      run(p) {
        const eclipseEnergy = p.eclipseLoad*p.eclipse/60, storage = eclipseEnergy/(p.discharge/100);
        return {capacity:storage/(p.dod/100),dayPower:p.sunLoad+storage/(p.charge/100)/(p.sunTime/60),eclipseEnergy};
      }
    },
    {
      id:'radiator', group:['熱控','Thermal control'], title:['散熱器面積與熱沉','Radiator area and sink temperature'],
      formula:'q_net = εσ(T⁴−T_sink⁴)−q_abs   |   A = Q/q_net   (q_net > 0)',
      assumption:['單一等溫輻射面、灰體、穩態。熱沉為等效輻射溫度，另以每單位面積吸收通量代表尚未計入的外部熱源。面積為有效輻射面積。','Steady, isothermal, gray radiating surface. Use effective radiative sink temperature and include separately only external absorbed flux not already represented by the sink. The output is effective radiating area.'],
      prompt:['將等效熱沉升溫或提高外部吸收通量，找出淨放熱接近零的位置。若淨值小於等於零，增加面積也無法解決。','Increase sink temperature or external absorbed flux until net rejection approaches zero. If net rejection is nonpositive, increasing area cannot solve the problem.'],
      references:[sources.thermal],
      inputs:[input('heat','需排出的內部熱量','Internal heat to reject','W',85,1,50000,1),input('temperature','散熱面溫度','Radiator surface temperature','K',300,100,600,1),input('sink','等效熱沉溫度','Effective sink temperature','K',190,2,600,1),input('emissivity','紅外放射率','IR emissivity','1',.85,.05,1,.01),input('absorbed','外部吸收熱通量','External absorbed heat flux','W/m²',65,0,2000,1)],
      outputs:[output('area','最小有效散熱面積','Minimum effective radiating area','m²'),output('flux','淨散熱通量','Net heat rejection flux','W/m²')],
      sweep:'temperature',
      run(p) {
        const flux = p.emissivity*SIGMA*(p.temperature**4-p.sink**4)-p.absorbed;
        if (flux <= 0) throw new RangeError('no-thermal-sink');
        return {area:p.heat/flux,flux};
      }
    },
    {
      id:'reaction-wheel', group:['姿態控制','Attitude control'], title:['反作用輪動量飽和','Reaction-wheel momentum saturation'],
      formula:'H_end = H₀ + |τd|t   |   t_sat = (H_max−H₀)/|τd|   |   ω_end = H_end/Jw',
      assumption:['單軸等效輪。初始輪動量與擾動同向，持續抵銷常值外擾且無卸載。理論終態超容量時，實際輪速會受限。快速轉向峰值扭矩、反向週期擾動與輪陣配置需另算。','Single equivalent wheel axis. Initial wheel momentum and disturbance have the same sign, with constant rejection and no unloading. Wheel speed is constrained in practice when theoretical demand exceeds capacity. Slew torque, cyclic reversal and wheel geometry require separate analysis.'],
      prompt:['先把連續精指向時間加倍，再把擾動加倍。尋找動量裕度跨過零的條件。','Double the uninterrupted fine-pointing interval, then double disturbance. Find when momentum margin crosses zero.'],
      references:[sources.gnc],
      inputs:[input('disturbance','常值擾動扭矩大小','Constant disturbance torque magnitude','mN·m',.08,.001,100,.001),input('duration','指向持續時間','Pointing duration','min',20,0,1440,1),input('initial','初始輪動量','Initial wheel momentum','N·m·s',.02,0,100,.001),input('capacity','輪動量容量','Wheel momentum capacity','N·m·s',.15,.001,100,.001),input('inertia','轉子轉動慣量','Rotor moment of inertia','kg·m²',.00024,.00001,1,.00001)],
      outputs:[output('margin','剩餘動量裕度','Remaining momentum margin','N·m·s'),output('demand','期末理論輪動量','Theoretical final wheel momentum','N·m·s'),output('saturation','起始至飽和時間','Time to saturation from start','min'),output('rpm','理論需求輪速','Theoretical required wheel speed','rpm')],
      sweep:'duration',
      run(p) {
        if (p.initial>p.capacity) throw new RangeError('wheel-initial');
        const torque = p.disturbance/1000, demand = p.initial+torque*p.duration*60;
        return {margin:p.capacity-demand,demand,saturation:(p.capacity-p.initial)/torque/60,rpm:demand/p.inertia*60/TAU};
      }
    },
    {
      id:'phasing', group:['軌道力學','Orbital mechanics'], title:['同軌會合的相位調整','Orbital phasing for same-orbit rendezvous'],
      formula:'Tₚ = T₀[1−φ/(2πN)]   |   aₚ = [μ(Tₚ/2π)²]⅓   |   r_opp = 2aₚ−r₀',
      assumption:['追蹤器與目標最初同一圓軌道、同方向。正相位代表目標在前方，追蹤器降低另一側拱點以追上目標。回到出發拱點後立即圓化。最低高度檢查只是本教學模型的 150 km 下界；未模擬交會走廊、碰撞風險或近接控制。','Chaser and target start on the same co-prograde circular orbit. A positive angle means the target is ahead, so the chaser lowers the opposite apsis. It circularizes on returning to the departure apsis. The 150 km floor is a teaching constraint. Approach corridors, collision risk and proximity control are omitted.'],
      prompt:['選擇目標超前 20°，比較 1 圈和 5 圈的等待時間及脈衝需求。若拱點高度太低，增加圈數後重算。','With the target 20° ahead, compare wait time and Δv for one and five laps. If opposite apsis is too low, increase lap count and recalculate.'],
      references:[sources.mechanics,sources.gnc],
      inputs:[input('altitude','共同圓軌道高度','Shared circular altitude','km',550,150,45000,10),input('angle','目標超前相位','Target lead angle','°',20,-180,180,1),input('laps','追蹤器相位軌道圈數','Chaser phasing laps','laps',3,1,30,1,true)],
      outputs:[output('deltaV','總脈衝需求','Total Δv','m/s'),output('time','相位等待時間','Phasing coast time','min'),output('oppositeAltitude','另一側拱點高度','Opposite apsis altitude','km'),output('first','第一脈衝','First burn','m/s')],
      sweep:'angle',
      run(p) {
        const r = EARTH_RADIUS+p.altitude, phasingPeriod = period(r)*(1-p.angle/(360*p.laps));
        const a = Math.cbrt(MU*(phasingPeriod/TAU)**2), oppositeAltitude = p.angle===0 ? p.altitude : 2*a-r-EARTH_RADIUS;
        if (oppositeAltitude < 150-1e-8) throw new RangeError('phasing-altitude');
        const first = p.angle===0 ? 0 : 1000*(apsisSpeed(r,a)-speed(r));
        return {deltaV:2*Math.abs(first),time:p.angle===0 ? 0 : phasingPeriod*p.laps/60,oppositeAltitude,first};
      }
    },
    {
      id:'imaging-gsd', group:['光學酬載','Optical payloads'], title:['地面取樣距離與動態拖影','Ground sample distance and motion smear'],
      formula:'GSD = hp/f   |   W ≈ Npx·GSD   |   smear = v_ground·t_exp / GSD',
      assumption:['平坦地面、近軸天底取像、方形像素。速度為地表投影速度。未含光學繞射、姿態抖動、大氣、地形、電子補償與非天底畸變；像素取樣間距與實際可辨能力應分開驗證。','Flat ground, paraxial nadir imaging and square pixels. Use projected ground speed. Diffraction, jitter, atmosphere, terrain, electronic compensation and off-nadir distortions are omitted. Validate pixel spacing and resolvable detail separately.'],
      prompt:['把曝光時間減半，地面取樣間距是否改變？再延長焦距，觀察取樣、幅寬及拖影像素數的取捨。','Halve exposure time. Does GSD change? Then extend focal length and compare sampling, swath and smear in pixels.'],
      references:[sources.gsd,sources.landsat],
      inputs:[input('altitude','感測器離地高度','Sensor height above ground','km',525,100,45000,5),input('pitch','像素間距','Pixel pitch','µm',5.5,1,50,.1),input('focal','有效焦距','Effective focal length','mm',900,10,20000,5),input('pixels','橫軌有效像素數','Active cross-track pixels','px',4096,1,50000,1,true),input('groundSpeed','地表投影速度','Projected ground speed','km/s',7.2,0,15,.1),input('exposure','曝光時間','Exposure duration','ms',.2,.001,100,.001)],
      outputs:[output('gsd','地面取樣距離','Ground sample distance','m/px'),output('swath','近似橫軌幅寬','Approximate cross-track swath','km'),output('smear','沿軌拖影','Along-track smear','px')],
      sweep:'focal',
      run(p) {
        const gsd = p.altitude*p.pitch/p.focal;
        return {gsd,swath:p.pixels*gsd/1000,smear:p.groundSpeed*p.exposure/gsd};
      }
    },
    {
      id:'solar-array', group:['電力與能源','Electrical power'], title:['太陽能陣列壽終供電','Solar-array end-of-life output'],
      formula:'S(d) = 1361/d_AU²   |   P_EOL = S(d)·A·η·k_EOL·ηpath·cos θ',
      assumption:['以 1 AU、1361 W/m² 為教學基準。假設平面陣列均勻受光，θ 自陣列法線量起。壽終係數涵蓋本例指定的老化與溫度折減，未含遮蔭、部分電池失效或非線性電路效應。','Uses a nominal teaching irradiance of 1361 W/m² at 1 AU. A flat array is uniformly lit and θ is measured from the array normal. EOL factor represents the example’s aging and temperature derating. Shadowing, partial cell failure and nonlinear circuit effects are omitted.'],
      prompt:['將太陽距離由 1 AU 改為 1.52 AU，並比較正對與傾斜 45°。檢查是否需要增加面積。','Change solar distance from 1 AU to 1.52 AU and compare normal incidence with a 45° tilt. Check whether more array area is needed.'],
      references:[sources.power,sources.irradiance],
      inputs:[input('distance','日距','Distance from Sun','AU',1,.1,20,.01),input('area','有效電池片面積','Active cell area','m²',.68,.001,1000,.001),input('efficiency','電池片效率','Cell conversion efficiency','%',29,1,65,1),input('degrade','壽終保留比例','EOL retention','%',80,5,100,1),input('path','電力路徑效率','Power-path efficiency','%',94,5,100,1),input('angle','與陣列法線夾角','Angle from array normal','°',20,0,89,1),input('required','日照負載需求','Required sunlight power','W',140,0,50000,1)],
      outputs:[output('power','壽終日照端可供功率','EOL sunlight power','W'),output('margin','需求裕度','Margin against requirement','W'),output('requiredArea','達標最小有效面積','Minimum active area to meet load','m²')],
      run(p) {
        const density = SUN_AT_EARTH/p.distance**2*(p.efficiency/100)*(p.degrade/100)*(p.path/100)*Math.cos(p.angle*Math.PI/180);
        const power = density*p.area;
        return {power,margin:power-p.required,requiredArea:p.required/density};
      }
    }
  ];

  function modelFor(id) { return models.find(model=>model.id===id); }
  function defaults(id) {
    const model = modelFor(id);
    if (!model) throw new RangeError('unknown-model');
    return Object.fromEntries(model.inputs.map(field=>[field.key,field.value]));
  }
  function calculate(id, inputs) {
    const model = modelFor(id);
    if (!model) throw new RangeError('unknown-model');
    const params = {};
    for (const field of model.inputs) {
      const value = inputs?.[field.key];
      if (typeof value !== 'number' || !Number.isFinite(value) || value<field.min || value>field.max || (field.integer&&!Number.isInteger(value))) {
        const error = new RangeError('invalid-input');
        error.field = field.key;
        throw error;
      }
      params[field.key] = value;
    }
    const result = model.run(params);
    if (model.outputs.some(field=>!Number.isFinite(result[field.key]))) throw new RangeError('non-finite');
    return result;
  }

  root.MG_SPACE_LAB_V23 = Object.freeze({models,defaults,calculate});
})(typeof window==='undefined' ? globalThis : window);
