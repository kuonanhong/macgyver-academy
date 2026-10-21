#!/usr/bin/env python3
"""Independent peer arithmetic ledger for b151-b175, written from the displayed models.

This is not the author's audit_support.py. Each primary result is evaluated again
in an independently specified expression, with dimensional and boundary review
notes. Input hashes bind this review to the exact content read. No design approval.
"""
import hashlib
import json
import math
import re
from pathlib import Path

HERE = Path(__file__).resolve().parent
# Ten entries per course, in unit order: expression, rounded displayed result, unit.
# Expressions use declared model assumptions, often converting to SI before evaluation.
ROWS = {
151: [
 ('.10e6*4/.15/1e6',2.67,'MPa'),('.60e6/1.20e6',.5,'1'),
 ('12-12*.18',9.84,'m3'),('25000/.025/1e6',1,'MPa'),('.012/.30',.04,'1'),
 ('15/100',.15,'m'),('200000/(pi*(.1/2)**2)/1e6',25.46,'MPa'),
 ('10e9*(.0008/4)/1e6',2,'MPa'),('(.30-.18)/30',.004,'mm/day'),('18/20',.90,'1')],
152: [
 ('18000/30000',.6,'1'),('20000*.025',500,'J'),('3e6*.10*.10**2/6/1000',.5,'kN m'),
 ('100*cos(pi/3)',50,'N'),('80*.010',.8,'J/fibre'),('5/35',.143,'1'),
 ('.5*.2',.10,'mm'),('60/sqrt(9)',20,'J'),('420/500',.84,'1'),('7/8',.875,'1')],
153: [
 ('26000*4/2/1000',52,'kN/bolt'),('314e-6*500e6/1000',157,'kN'),
 ('pi*.05*2*300000/1000',94.25,'kN'),('80000/.020/1e6',4,'MPa'),
 ('100000*2/(200e9*314e-6)*1000',3.18,'mm'),('100000/.10/1e6',1,'MPa'),
 ('(2.4-1.8)/10',.06,'mm/min'),('(100000-96000)/100000',.04,'1'),
 ('(pi*.018**2/4)/(pi*.020**2/4)',.81,'1'),('8/10',.80,'1')],
154: [
 ('80000*4*.75/1000',240,'kN'),('240000*.05/1000',12,'kN m'),
 ('pi**2*200e9*2e-6/2**2/1000',987,'kN'),('9000/.30/1000',30,'kN'),
 ('100000/.002/1e6',50,'kN/mm'),('240000/.40/1000',600,'kPa'),
 ('10e9*.10/1e6',1000,'MN'),('300000*.020/1000',6,'kN m'),
 ('1-6/8',.25,'1'),('46/50',.92,'1')],
155: [
 ('30000*3**2/8/1000',33.75,'kN m'),('pi/64*(.114**4-.102**4)',2.98e-6,'m4'),
 ('.350-.114',.236,'m'),('12-9',3,'m'),('12*tan(pi/180)',.209,'m'),
 ('pi/4*(.170**2-.114**2)*12',.150,'m3'),('10000*.005',50,'kN/m'),
 ('12-4',8,'mm'),('.002/.500',.004,'rad'),('180000/300000',.6,'1')],
156: [
 ('.012/6',.002,'1'),('80/40',2,'m2/bar'),('500e-6*600e6/1000',300,'kN'),
 ('pi*.04*4*200000/1000',100.5,'kN'),('12-7',5,'m'),('10*tan(.5*pi/180)',.0873,'m'),
 ('80000/200000',.4,'1'),('(.018-.006)/3',.004,'1'),('40*1.5',60,'m/cycle'),('15/5',3,'1')],
157: [
 ('1000*9.81*20/1000',196.2,'kPa'),('(.105-.100)/.100',.05,'1'),('1.6/2',.8,'1'),
 ('300/50',6,'N/mm'),('300000*288/293/1000',294.9,'kPa absolute'),('100/1000',.1,'1'),
 ('.005/.100',.05,'1'),('18/20',.9,'1'),('6/20',.30,'L/min'),('48/50',.96,'1')],
158: [
 ('5.30-5',.30,'m'),('24000*3/1000',72,'kPa'),('(1.1/1)**4',1.4641,'1'),
 ('360000/.60/1000',600,'kPa'),('80000*8/1000',640,'kN'),('pi*(5.3**2-5**2)*10',97.08,'m3'),
 ('1.5e6/6e6',.25,'1'),('20e9*1e-5*20/1e6',4,'MPa'),('110-70',40,'mm'),('12/6',2,'mm/cycle')],
159: [
 ('150000*4/1e6',.60,'MN/m'),('600000*.03/1000',18,'kN m/m'),('.5*400000/1000',200,'kN'),
 ('1200000/6/1000',200,'kPa'),('12/3',4,'day'),('60000/.12/1000',500,'kPa'),
 ('1000*9.81*5*10/1000',490.5,'kN'),('.004/8',.0005,'1'),('.6-.2',.4,'L/min'),('.40-.05',.35,'m')],
160: [
 ('(100e6)**2/(2*50e9)/1000',100,'kJ/m3'),('100*5**2/2/1000',1.25,'kJ'),
 ('150000*.2/1000',30,'kJ'),('.18-.10',.08,'m'),('1000*9.81*1/1000',9.81,'kJ'),
 ('5000*.002',10,'m'),('min(300,180,250)',180,'kN'),('24/6',4,'events/h'),
 ('3/20',.15,'1'),('150000*.08/1000',12,'kJ')],
161: [
 ('26000*500/3e6',4.33,'1'),('20e6*(.08-.03)/1e6',1,'MPa'),('200000*.15/1000',30,'kJ'),
 ('.20-.14',.06,'m'),('(45-30)/(6-3)',5,'mm/day'),('4*20',80,'mm circumference'),
 ('35/50',.70,'1'),('abs(48-50)/50',.04,'1'),('.02*365',7.3,'mm/year'),('5/6',.833,'1')],
162: [
 ('(.120-.100)/.100',.20,'1'),('.004/.100',.04,'1'),('25000/.005/1e6',5,'MPa'),
 ('8e6/20e6',.4,'1'),('.2*24*60',288,'L'),('.02*2',.04,'m'),('100-65',35,'mm'),
 ('.5*24',12,'mm'),('1000*9.81*3/1000',29.43,'kPa'),('9/12',.75,'1')],
163: [
 ('1000*9.81*80/1e6',.7848,'MPa'),('(900000+1000*9.81*10-150000)/1e6',.8481,'MPa'),
 ('(848100-784800)/1000',63.3,'kPa'),('1.1**3',1.331,'1'),
 ('pi*(.5**2-.05**2)*3*.10',.233,'m3'),('.20/.04',5,'1'),('(10-2)/10',.80,'1'),
 ('.002/10',.0002,'1'),('8e6/10e6',.8,'1'),('36/40',.9,'1')],
164: [
 ('80-25',55,'L/s'),('.020*.8*1000',16,'L/s'),('.07069*.075**(2/3)*sqrt(.005)/.013',.0684,'m3/s'),
 ('1000*9.81*.055*20/.70/1000',15.4,'kW'),('.055*600',33,'m3'),('2*40',80,'L/s'),
 ('(.8**2)*(.8**(2/3))',.5515,'1'),('2/.5',4,'1'),('.05*.2*3600',36,'kg/h'),('(18-21)/6',-.5,'m/month')],
165: [
 ('12-14',-2,'K difference'),('.5*24*60',720,'L/day'),('.35-.20',.15,'mm'),
 ('(.15/.20)**3',.4219,'1'),('.4/200',.002,'L/(s kPa)'),('.8/1.6',.5,'1'),
 ('1000*9.81*3/1000',29.43,'kPa'),('.1*500*24*60*60/1e6',4.32,'kg/day'),('3/4',.75,'1'),('4/20',.2,'1')],
166: [
 ('100*14*8',11200,'m3'),('.33*18000*8**2/2/1000',190.1,'kN/m'),
 ('200e9*.01*12e-6*10/1000',240,'kN'),('1000*9.81*5*100/1000',4905,'kN'),
 ('6e6/(1000*9.81*5*100)',1.223,'1'),('.004/.080',.05,'1'),('900000/6/1000',150,'kN/m'),
 ('.006/12',.0005,'rad'),('20000*2/1000',40,'kPa'),('sqrt(.01**2+.02**2+.02**2)',.03,'m standard uncertainty')],
167: [
 ('30e9*.30/20/1e6',450,'MN/m'),('(4/8)**2',.25,'1'),('3e6*.025/1000',75,'kN m'),
 ('.60-.20',.40,'m2'),('900000/.30/1e6',3,'MPa'),('18000*2/1000',36,'kPa'),
 ('1000*9.81*4/1000',39.24,'kPa'),('18-11',7,'mm'),('1000*9.81*12*100/1000',11772,'kN'),('11/12',.917,'1')],
168: [
 ('25000*2400/1000',60000,'t mass'),('60000000/1025',58536.6,'m3'),('3+8-9.5',1.5,'m'),
 ('1000*6000/60000000',.1,'m'),('500000/(1025*4000)',.122,'m'),
 ('10055*8*4**2/2/1000',643.5,'kN'),('1e-5*12*30',.0036,'m'),
 ('1025*1*200*1.5**2/2/1000',230.6,'kN'),('100000*60**2/8/1000',45000,'kN m'),('(60600-60000)/60000',.01,'1')],
169: [
 ('40*1*200',8000,'m3'),('20e6/4000/1000',5,'kPa'),('.0002*50*5',.05,'m'),
 ('.020/200',.0001,'rad'),('4000*.60',2400,'m3'),('4/.5',8,'1'),('20e6/200/1000',100,'kPa'),
 ('sqrt(.02**2+.03**2+.02**2)',.0412,'m standard uncertainty'),('1025*2**2/2',2050,'Pa'),('3800/4000',.95,'1')],
170: [
 ('30*.0005',.015,'m'),('40/100',.40,'1'),('200000*100/1e6',20,'MN'),
 ('200000*.30/1000',60,'kN/m transverse resultant'),('1e-5*200*15',.030,'m'),
 ('(.020/200)*10',.001,'m'),('1e6/.50/1e6',2,'MPa'),('12/30',.40,'L/min'),('180/240',.75,'1'),('18/20',.90,'1')],
171: [
 ('24000*(8*5-7*4)*20/1000',5760,'kN'),('25e6*.12/1e6',3,'MN'),('.15*5760000/1000',864,'kN'),
 ('50000*7**2/8/1000',306.25,'kN m per 1m strip'),('600000/2/1000',300,'kPa'),
 ('(3e6/1+(3e6*.05)/.2)/1000',3750,'kPa'),('.040/20',.002,'rad'),
 ('.005*40*20',4,'m3'),('.008/10',.0008,'rad'),('(720-600)/720',.167,'1')],
172: [
 ('250000*pi*1.5**2/4/1000',441.8,'kN'),('(.050*(1300-1100))/(2650-1100)',.00645,'m3/s added solids'),
 ('pi*1.5**2*.50/4',.8836,'m3'),('5000*pi*1.5*100/1000',2356,'kN'),('1.2e6/.30/1e6',4,'MPa'),
 ('.003*100',.30,'m'),('.03*200/.15*1200*2**2/2',96000,'Pa'),('sqrt(2*pi)*4*.003',.0301,'m2'),
 ('1000*9.81*12*1.5/1000',176.6,'kN'),('12/30',.40,'L/min')],
173: [
 ('120*8+400',1360,'kN front demand'),('8*20e6*.010/1e6',1.60,'MN'),('600*1.5',900,'kN'),
 ('.52-.40-.10',.02,'m'),('2e6*100/(30e9*.40)',.0167,'m'),('200000/.025/1e6',8,'MPa'),
 ('2*1e6*sin(2*pi/180/2)/1000',34.90,'kN'),('150000*.20/1000',30,'kN'),
 ('(1.2e6-1e6)/(.004-.002)/1e6',100,'kN/mm'),('(1.42/1.50)**2',.8962,'1')],
174: [
 ('3*sin(5*pi/180)',.2615,'m'),('100*tan(.1*pi/180)',.1745,'m'),
 ('3/(.5*pi/180)',343.8,'m'),('.30/.50',.60,'1'),('atan(.5/20)*180/pi',1.432,'degree'),
 ('200*tan((.02*.5)*pi/180)',.0349,'m'),('sqrt(.3**2+.4**2)-.1-.15',.25,'m before radii'),
 ('.020/(pi/4*(.60**2-.40**2))',.1273,'m/s'),('.40/(2*200)+20e6/200e9',.0011,'1'),
 ('sqrt(.05**2+.03**2+.04**2)',.0707,'m residual')],
175: [
 ('8000-3000-3500-1000',500,'kN net downward'),('15000*pi*10*20/1000',9425,'kN'),
 ('6e6/(pi/4*(10**2-9**2))/1000',402.1,'kPa'),('.020/10',.002,'rad'),('8/5',1.60,'1'),
 ('.0001*100*10',.10,'m'),('.10/(1/60)',6,'m/h short event'),('1000*9.81*10*pi*10**2/4/1000',7705,'kN'),
 ('2/20',.10,'1'),('12000000/(1000*9.81*1000)',1.223,'1')],
}

# Additional results, not counted as extra unit coverage. The corrected GM is a
# derived cross-check linking b168 units 3-4; the other 30 results are displayed.
SECONDARY = [
 ('b151',1,'.10e6*4/1e6',.40,'MN/m'),('b151',2,'.60/.80',.75,'1'),
 ('b151',5,'.30-.012',.288,'m3'),('b151',8,'.0008/4',.0002,'1'),
 ('b153',1,'26*4',104,'kN'),('b153',4,'80000/.01/1e6',8,'MPa'),
 ('b153',8,'20e6*.005/1000',100,'kN'),('b154',7,'200e9*.003/1e6',600,'MN'),
 ('b158',8,'1e-5*20',.0002,'1'),('b161',1,'26000*500/1e6',13,'MPa'),
 ('b165',5,'.6/300',.002,'L/(s kPa)'),('b168',3,'3+8-9.5-.1',1.4,'m corrected GM'),
 ('b170',6,'.020/200',.0001,'rad'),('b171',1,'8*5-7*4',12,'m2'),
 ('b171',6,'3000*.05',150,'kN m'),('b171',8,'40*20',800,'m3'),
 ('b171',10,'720-600',120,'min'),('b172',2,'(1300-1100)/(2650-1100)',.1290,'1'),
 ('b173',1,'180*8',1440,'kN rear friction'),('b173',2,'7*20e6*.010/1e6',1.40,'MN'),
 ('b174',6,'.02*.5',.010,'degree'),('b174',7,'sqrt(.3**2+.4**2)',.50,'m'),
 ('b174',8,'pi/4*(.6**2-.4**2)',.1571,'m2'),('b174',9,'.4/(2*200)',.001,'1'),
 ('b174',9,'20e6/200e9',.0001,'1'),('b175',3,'pi/4*(100-81)',14.92,'m2'),
 ('b175',5,'(2.65-1)/(1+.65)',1,'1'),('b175',7,'.12/.50',.24,'m/h'),
 ('b175',8,'pi*10**2/4',78.54,'m2'),('b175',8,'24*2*pi*10**2/4',3770,'kN'),
 ('b175',10,'1000*9.81*1000/1000',9810,'kN')]

BOUNDARIES = {
151:'Closed-ring membrane estimate is conditional on contact; voids induce bending. Early-age strength, rebound, bond, thickness minima and strain-zero/temperature history are separate evidence.',
152:'Panel energy and residual ratios remain test-geometry dependent; bending resistance uses the rectangular elastic section modulus. No conversion of panel energy to tunnel-system energy.',
153:'Two equal vertical bolts require symmetric load sharing. Steel, bond and plate bearing capacities are distinct; pull test reaction and local interface do not certify a whole wedge.',
154:'N=pRs is the complete uniform-pressure ring idealization. Euler uses effective elastic straight-column length, not proof of curved-rib capacity. Joints and lateral restraint remain independent.',
155:'Pipe umbrella needs forward ground and rear support. Simple-span moment, intact-tube inertia and local Winkler line support are comparison models; joint rotation must distinguish local chord slope from two-sided relative rotation.',
156:'Tributary area is geometrical, not uniform bar-force allocation. Bond maturity, retained embedment and three-dimensional deviation govern reinforcement continuity.',
157:'Membrane blocks flow but does not replace lining pressure resistance. P/T requires absolute pressure/temperature and fixed gas volume/mass. Completeness percentages are not reliability.',
158:'Hydrostatic fresh-concrete pressure is a reference envelope. L^4 scaling holds fixed line load, EI and supports; full-restraint thermal stress ignores creep/slip and is an ideal upper comparison.',
159:'N=pR assumes a closed ring; not an open invert. Coulomb resistance is an isolated assumed interface. Uniform head-area uplift is separate from bearing, early-age wheel loads and leaking-head changes.',
160:'Stored elastic, projectile, drop-weight and component work are different energies. Static serial-force minimum does not predict dynamic system energy; remaining constant-force work requires verified residual travel.',
161:'Stress-strength ratio is screening, not a squeeze prediction. Installation displacement changes support engagement. Summed sliding-joint shortening is circumferential, not diametral closure. Calibration does not prove parameter identifiability.',
162:'Free swelling and constrained swelling pressure cannot be proportionally converted. Strain-times-thickness is a uniform layer idealization. Drawdown effective-stress increment isolates the pore-pressure component.',
163:'Pressure datum/elevation, fluid density and flowing line losses are distinct. Parallel-plate cubic law needs laminar fixed-gradient assumptions; connected void volume is not a grout-take instruction.',
164:'Storage balance assumes steady storage. Manning needs hydraulic slope and compatible geometry; D^(8/3) requires geometrically similar effective circular passages. Pump redundancy may share failure modes.',
165:'Condensation, structural opening, water head and flow-path diversion are separate. Conductance comparisons need matched flow law; chloride mass is exposure, not predicted corrosion penetration.',
166:'Construction stages change both load path and flotation resistance. Raw weight/uplift ratio is not a code factor. Settlement slope, rigid tilt, distortion and standard survey uncertainty must not be conflated.',
167:'Early slab stiffness and column effective length use construction states. Drawdown increases effective stress only as an isolated pore-pressure change; excavation unloading must be superposed separately.',
168:'Tonnes are mass. Displacement balance is not stability; GM requires free-surface correction. Hydrostatic bulkhead resultant uses the stated triangular pressure geometry. Drag excludes wave/acceleration dynamics; land simple-span bending is not a floating beam model.',
169:'Foundation pressure uses net downward force after buoyancy. Long-term compressibility and partial bed contact differ. One-element chord tilt becomes joint relative rotation only with an explicit adjacent orientation.',
170:'Seal compression and clearance are geometric and do not establish contact force or water tightness. p times span is transverse resultant, not membrane tension. Relative rotation needs both adjacent orientations.',
171:'Rectangular box is a staged frame. A one-metre simple strip is not the entire box; force eccentricity uses stated A and Z. Settlement slope is neither a track-twist acceptance rule nor a damage criterion.',
172:'Density mixture estimates incremental solids relative to specified carrier. Pipe friction is a specified equivalent-Newtonian Darcy model. Gaussian settlement area is per metre and not equal to instantaneous spoil imbalance.',
173:'Intermediate stations require a closed reaction path; front and rear demands are staged, not simultaneously applied to every joint. Uniform axial shortening excludes nonlinear joint compression. Curvature resultant assumes equal axial forces on both sides.',
174:'Projection and radius depend on angle units and segment definitions. Heading drift example is geometrical amplification of a stated angle, not a time-integrated path. Utility radii remain to be deducted. Steel strain example does not transfer to plastics.',
175:'Static force imbalance cannot predict sinking speed. Upward flow reduces effective stress; critical gradient is ideal saturated granular soil, not undrained clay uplift. Plug self-weight alone does not establish wall transfer or permanent flotation safety.',
}

def evaluate(expression):
    namespace = {name:getattr(math,name) for name in ('pi','sqrt','sin','cos','tan','atan')}
    namespace.update({'abs':abs,'min':min})
    return eval(expression, {'__builtins__':{}}, namespace)

def numeric_check(expression, displayed):
    actual = evaluate(expression)
    # All differences are displayed rounding; tolerance is deliberately <0.4%.
    ok = math.isclose(actual, displayed, rel_tol=.004, abs_tol=1e-12)
    assert ok, (expression, actual, displayed)
    return actual

def main():
    checks=[]; hashes={}; bilingual=0
    for cid, rows in sorted(ROWS.items()):
        assert len(rows)==10
        path=HERE/'inputs'/f'b{cid}.json'
        raw=path.read_bytes(); data=json.loads(raw)
        hashes[path.name]=hashlib.sha256(raw).hexdigest()
        assert len(data['units'])==10
        for index,(expression,displayed,unit) in enumerate(rows,1):
            zh,en=data['units'][index-1]['model'].split('~')
            tokens=lambda s: re.findall(r'(?<![a-zA-Z])[+-]?\d+(?:\.\d+)?(?:e[+-]?\d+)?',s)
            assert tokens(zh)==tokens(en),(cid,index,'bilingual numeric mismatch')
            bilingual+=1
            checks.append(dict(course=f'b{cid}',unit=index,
                expression=expression,recalculated=numeric_check(expression,displayed),
                displayed=displayed,outputUnit=unit,result='pass',
                modelSha256=hashlib.sha256(data['units'][index-1]['model'].encode()).hexdigest()))
    secondary=[dict(course=c,unit=u,expression=e,recalculated=numeric_check(e,v),expected=v,outputUnit=q,result='pass',
                   resultType='derived cross-check' if (c,u)==('b168',3) else 'additional displayed result')
               for c,u,e,v,q in SECONDARY]
    findings_path=HERE/'review_support_by_ground_findings.json'
    findings=json.loads(findings_path.read_text()) if findings_path.exists() else []
    report=dict(reviewed='2026-10-21',reviewer='courses_ground; independent course-author peer reviewer',
        scope=dict(courses=25,models=250,primaryArithmeticChecks=250,additionalArithmeticChecks=len(secondary),
            ids='b151-b175; units 1-10 each',
            method='Read all 250 displayed models; separately recalculate every primary result in SI or compatible declared units; inspect mechanism/verification text for physical interpretation and all flagged cases.',
            limits='Educational arithmetic, dimensional and physical-boundary review. Not source-project data validation, code compliance, equipment operating authorization, site design verification or professional certification.'),
        roundingToleranceRelative=.004,bilingualNumericTokenChecks=bilingual,
        findingSummary=dict(observations=len(findings),closed=sum(f['status']=='closed' for f in findings),
                            open=sum(f['status']!='closed' for f in findings),arithmeticErrors=0),
        inputSha256=hashes,checks=checks,secondaryChecks=secondary,
        courseBoundaryReview={f'b{k}':v for k,v in BOUNDARIES.items()},findings=findings,
        additionalReferences=[dict(url='https://www.fhwa.dot.gov/publications/research/infrastructure/structures/bridge/15080/002.cfm',
            ref='turn117view0',scope='FHWA bridge terminology also uses differential settlement/span as angular distortion; the peer finding requests definition clarity in building/rail contexts, not a claim that the ratio is arithmetically wrong.')])
    (HERE/'review_support_by_ground.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
    print(f'{len(checks)} primary + {len(secondary)} additional calculations PASS; {len(hashes)} input hashes recorded.')

if __name__=='__main__':main()
