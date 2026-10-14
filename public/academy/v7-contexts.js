/** V7 original teaching diagrams. Abstract interfaces, not equipment plans. */
const bi=(zh,en)=>({zh,en});
export const V7_STAGE_FAMILIES={
 b015:['site','suspensionbridge','suspensionbridge','maintenance'],
 b021:['site','tower','vibration','maintenance'],
 b103:['ground','tunnel','railinterfaces','monitoring'],
 b226:['site','lock','hydrology','maintenance'],
 a025:['backside','thinning','contact','electrical'],
 a042:['highna','lithography','lithography','metrology'],
 a211:['hvdc','transformer','electrical','monitoring'],
 a319:['consensus','consensus','software','backup'],
 c005:['aircraft','materials','electrical','maintenance'],
 c325:['webb','reflective','thermal','astrodata'],
 d036:['windfarm','ground','hvdc','maintenance'],
 d202:['pet','pettiming','petreconstruct','imageqa']
};
const defs={
 pettiming:['偵測脈衝、時間窗與符合事件','Detector pulses, time windows and coincidences','時間窗辨識候選符合，仍須處理隨機事件與散射','A timing window identifies candidates; random coincidences and scatter remain','只要脈衝接近就一定來自同一次湮滅','Nearby pulses always come from the same annihilation'],
 petreconstruct:['響應線、系統矩陣與迭代殘差','Lines of response, system matrix and iterative residuals','重建結合多條響應線、校正與模型，殘差小不自動等於真實影像','Reconstruction combines multiple lines, corrections and a model; small residuals alone do not prove truth','一次迭代或一條線就能重建全部細節','One iteration or line reconstructs every detail'],
 imageqa:['非臨床模體、偏差與重複性','Non-clinical phantom, bias and repeatability','相同模體的偏差、均勻性和重複性需要分開核對','Check phantom bias, uniformity and repeatability separately','畫面看起來平滑便證明定量數據準確','A smooth image proves quantitative accuracy'],
 astrodata:['天文觀測、校正與不確定度','Astronomical observations, calibration and uncertainty','原始讀值、校正參考檔、品質遮罩與不確定度需一起保存','Retain raw readings, calibration references, quality flags and uncertainty together','經過美化的顏色即可取代校正資料','Enhanced display colors replace calibration data'],
 tower:['高樓核心、外伸桁架與巨柱','Tall-building core, outriggers and megacolumns','樓板、核心、外伸桁架與外柱共同形成概念載荷路徑','Floors, core, outriggers and outer columns share conceptual load paths','只有阻尼球承擔全部樓層重力','The damper carries every floor’s gravity load'],
 highna:['高 NA 反射光學與視場','High-NA reflective optics and field','EUV 使用反射光學；NA 增加的解析度趨勢需連同焦深和視場判讀','EUV uses reflection; interpret NA resolution trends with depth of focus and field','EUV 可任意換成一般透明玻璃透鏡','Ordinary transparent glass can replace EUV mirrors'],
 hvdc:['AC／DC 轉換與輸電邊界','AC/DC conversion and transmission boundaries','換流器連接交流與直流系統；保護及無功條件仍需獨立驗證','Converters link AC and DC; protection and reactive-power conditions need separate validation','變壓器單獨即可把交流轉換為直流','A transformer alone converts AC to DC'],
 consensus:['多副本日誌、任期與多數','Replicated logs, terms and majority','五個投票成員的多數為三；收到任意回覆不等於日誌已提交','A five-voter majority is three; an arbitrary response does not establish commitment','任意一個副本收到寫入就表示全部提交','Any single replica receiving a write proves commitment'],
 windfarm:['風機、集電與輸出電纜','Wind turbines, collection and export cable','風能、機械能、電力與輸出介面分開核算；天氣影響不能略過','Account separately for wind, shaft power, electrical power and export interfaces, including weather','風機額定功率就是全年每一秒的實際輸出','Rated power is actual output at every second of the year'],
 webb:['分段鏡、遮陽板與觀測鏈','Segmented mirror, sunshield and observation chain','分段鏡相位、熱環境與科學儀器各需驗證；地面據點不是 L2 的位置','Segment phasing, thermal environment and science instruments need separate checks; the ground site is not L2','鏡片外觀排列好就足以證明光學相位一致','Visually arranged segments prove optical phasing'],
 pet:['符合事件、響應線與重建','Coincidence events, lines of response and reconstruction','同一符合事件給出響應線；隨機、散射、衰減和正規化需另行校正','A coincidence provides a line of response; randoms, scatter, attenuation and normalization need separate corrections','一條響應線即可唯一決定三維影像','A single line of response uniquely determines a 3D image']
};
export const V7_CONTEXT_FAMILIES=Object.fromEntries(Object.entries(defs).map(([id,d])=>[id,{scene:'v7-'+id,name:bi(d[0],d[1]),tool:bi('原創系統界面教具','Original system-interface teaching model'),metric:bi('四類教學介面核對','Four educational interface checks'),unit:' / 4',initial:0,target:4,max:4,phase:bi('需求 → 系統 → 界面 → 證據','Requirements → system → interfaces → evidence'),observation:[bi(d[2],d[3]),bi(d[4],d[5])]}]));
const C={ink:'#173f38',green:'#68987b',gold:'#d3b66d',blue:'#91b8d0',paper:'#f4f8ee',red:'#ba5b45'};
const esc=v=>String(v).replace(/[&<>"']/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
const line=(x,y,x2,y2,c=C.ink,w=2)=>`<path d="M${x} ${y}L${x2} ${y2}" stroke="${c}" stroke-width="${w}" fill="none"/>`;
const rect=(x,y,w,h,c=C.green)=>`<rect x="${x}" y="${y}" width="${w}" height="${h}" rx="3" fill="${c}" stroke="${C.ink}"/>`;
const circle=(x,y,r,c=C.paper)=>`<circle cx="${x}" cy="${y}" r="${r}" fill="${c}" stroke="${C.ink}" stroke-width="2"/>`;
const text=(x,y,t,size=11)=>`<text x="${x}" y="${y}" text-anchor="middle" font-family="system-ui,sans-serif" font-size="${size}" fill="${C.ink}">${esc(t)}</text>`;
const path=(d,fill=C.paper)=>`<path d="${d}" fill="${fill}" stroke="${C.ink}" stroke-width="2"/>`;
export function renderV7Context(scene,phase=0,lang='en'){
 if(!scene?.startsWith('v7-'))return '';
 const zh=lang==='zh', choose=(a,b)=>zh?a:b;let out='';
 if(scene==='v7-tower'){
  out=rect(176,65,48,159,C.blue)+rect(95,80,16,144)+rect(289,80,16,144);
  for(let y=90;y<220;y+=22)out+=line(103,y,297,y);
  out+=line(103,156,200,120,C.gold,5)+line(200,120,297,156,C.gold,5)+line(72,226,330,226,C.ink,4)+circle(200,99,13,C.gold)+text(200,246,choose('核心／外伸桁架／外柱','Core / outriggers / outer columns'));
 }else if(scene==='v7-highna'){
  out=rect(45,82,76,9,C.gold)+rect(266,209,92,12,C.blue)+path('M106 163 Q140 189 170 163')+path('M218 123 Q250 97 280 123')+line(85,91,138,176,C.red)+line(138,176,249,110,C.red)+line(249,110,308,210,C.red)+line(266,178,308,210,C.red)+line(344,174,308,210,C.red)+text(82,75,'MASK')+text(311,240,'WAFER')+text(190,193,choose('僅示意反射與收斂角','Reflection / convergence only'),10);
 }else if(scene==='v7-hvdc'){
  out=text(51,103,'AC')+text(350,103,'AC');
  out+=rect(77,115,62,58,C.blue)+rect(258,115,62,58,C.blue)+line(30,143,77,143)+line(139,134,258,134,C.red,3)+line(139,156,258,156,C.ink,3)+line(320,143,370,143)+text(109,139,'AC/DC')+text(289,139,'DC/AC')+text(197,113,'DC LINK')+text(200,208,choose('端站／線路／介面驗證','Terminals / link / interface checks'));
 }else if(scene==='v7-consensus'){
  const points=[[200,85],[307,125],[267,211],[133,211],[93,125]];
  for(let i=1;i<5;i++)out+=line(200,85,...points[i],i<3?C.green:C.ink,i<3?4:1);
  points.forEach(([x,y],i)=>{out+=circle(x,y,25,i<3?C.green:C.paper)+text(x,y+4,'N'+(i+1));});
  out+=text(200,154,choose('5 票中的多數 = 3','Majority of 5 = 3'))+text(200,245,choose('不表示任意 3 回覆即可提交','Not arbitrary three acknowledgements'),10);
 }else if(scene==='v7-windfarm'){
  for(const [x,y] of [[78,136],[156,118],[236,136]]){out+=line(x,y,x,211,C.ink,4)+circle(x,y,4,C.gold);for(const a of [-90,30,150]){let r=a*Math.PI/180;out+=line(x,y,x+34*Math.cos(r),y+34*Math.sin(r),C.green,5);}}
  out+=path('M40 190q20-12 40 0t40 0t40 0t40 0t40 0t40 0','none')+rect(310,174,57,34,C.gold)+line(78,218,310,218,C.red,3)+[78,156,236].map(x=>line(x,211,x,218,C.red,3)).join('')+line(310,218,340,208,C.red,3)+line(367,191,393,191,C.red,3)+text(200,244,choose('集電 → 變換 → 輸出','Collection → conversion → export'));
 }else if(scene==='v7-webb'){
  for(let row=-2;row<=2;row++)for(let col=-2;col<=2;col++){if(Math.abs(row+col)>2||(row===0&&col===0))continue;const x=155+col*24+row*12,y=126+row*21;let d='';for(let n=0;n<6;n++){const a=(n*60+30)*Math.PI/180;d+=(n?'L':'M')+(x+13*Math.cos(a)).toFixed(2)+' '+(y+13*Math.sin(a)).toFixed(2);}out+=path(d+'Z',C.gold);}
  for(let k=0;k<5;k++)out+=path(`M54 ${190+k*7}L246 ${179+k*7}L317 ${198+k*7}L114 ${211+k*7}Z`,k%2?C.blue:C.paper);
  out+=text(155,70,choose('18 片鏡段示意','18 mirror segments'))+text(281,145,choose('遮陽／热界面','Shield / thermal'),10)+text(200,250,choose('原理示意，非展開順序','Principle only; not deployment sequence'),10);
 }else if(scene==='v7-pettiming'){
  out=line(45,128,362,128)+line(45,194,362,194)+rect(175,76,54,144,C.paper);
  out+=path('M45 128H170L188 91L204 128H362','none')+path('M45 194H181L199 157L215 194H362','none')+text(69,108,'A')+text(69,174,'B')+text(204,69,choose('示意時間窗','Timing window'))+text(206,242,choose('任意時間單位，非設備設定','Arbitrary time units; not scanner settings'),10);
 }else if(scene==='v7-petreconstruct'){
  for(let y=0;y<3;y++)for(let x=0;x<3;x++)out+=rect(56+x*32,89+y*32,30,30,(x+y)%2?C.blue:C.paper);
  out+=line(43,105,165,169,C.red,3)+line(64,72,143,201,C.gold,3)+text(103,225,choose('非患者格點','Non-patient grid'));
  out+=rect(196,107,70,58,C.green)+text(231,140,'MODEL')+line(165,135,195,135)+line(267,135,300,135)+line(295,111,295,174)+line(295,174,354,174)+path('M297 115L312 139L329 154L347 162','none')+text(324,204,choose('殘差／迭代','Residual / iteration'),9);
 }else if(scene==='v7-imageqa'){
  out=rect(55,79,118,112,C.paper)+rect(226,79,118,112,C.paper)+circle(114,134,38,C.blue)+circle(285,134,38,C.blue);
  for(const x of [103,124,274,295])out+=circle(x,132,5,C.gold);
  out+=text(114,216,'REPEAT A')+text(285,216,'REPEAT B')+text(200,246,choose('同條件／偏差／重複性','Matched conditions / bias / repeatability'),10);
 }else if(scene==='v7-astrodata'){
  out=rect(34,84,92,92,C.ink);
  for(const [x,y,r] of [[56,106,2],[87,123,4],[104,99,2],[66,153,3],[111,161,2]])out+=circle(x,y,r,C.gold);
  out+=rect(164,99,78,57,C.blue)+rect(280,84,88,92,C.paper)+line(127,128,163,128,C.red)+line(243,128,279,128,C.red)+text(80,201,'RAW')+text(203,125,'CAL')+text(325,135,'DATA + σ')+text(200,241,choose('校正參考／品質標记／版本','References / quality flags / versions'),10);
 }else if(scene==='v7-pet'){
  out=circle(198,143,78,C.blue)+circle(198,143,51,C.paper);
  for(let n=0;n<16;n++){let a=n*Math.PI/8;out+=circle(198+65*Math.cos(a),143+65*Math.sin(a),6,C.gold);}
  out+=line(198-65/Math.sqrt(2),143-65/Math.sqrt(2),198+65/Math.sqrt(2),143+65/Math.sqrt(2),C.red,4)+circle(198,143,4,C.red)+text(76,81,'DETECTORS')+text(312,205,'LOR')+text(200,248,choose('非患者教學模型','Non-patient teaching model'));
 }
 return out;
}
