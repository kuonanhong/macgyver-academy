# Independent supplemental checks of course-level example sensitivity calculations.
EXAMPLES={
'b215':[('ideal strip thickened to 12m','.8*120/12',8,1e-9)],
'b216':[('nominal residence seconds','20e6/4',5000000,1e-8),('nominal residence days','20e6/4/86400',57.87,.005),('arch share after 20% stiffness reduction','50*(3000*.8)/(3000*.8+2000)',27.273,.0005)],
'b217':[('series equivalent permeability m/s','20/(10/1e-7+10/5e-8)',6.667e-8,5e-12),('flow after lower permeability doubled m3/s','1000*30/(10/1e-7+10/(2*5e-8))',.00015,1e-12)],
'b218':[('rounded original cascade MW','15*9.81*(200*.9+120*.88)/1000',42.026,.0005),('second efficiency reduced MW','15*9.81*(200*.9+120*.8)/1000',40.6134,.00005)],
'b219':[('upper storage m3/day','1.2e6-.8e6-.1e6',.3e6,1e-8),('lower storage m3/day','.8e6-.7e6-.05e6',.05e6,1e-8),('system storage m3/day','1.2e6-.1e6-.7e6-.05e6',.35e6,1e-8),('new demand m3/day','.7e6*1.2',.84e6,1e-8),('lower new storage m3/day','.8e6-.84e6-.05e6',-.09e6,1e-8),('system new storage m3/day','1.2e6-.1e6-.84e6-.05e6',.21e6,1e-8)],
'b220':[('storage with half diversion m3/day','.5e6+.15e6-.6e6-.04e6',.01e6,1e-8),('Simpson volume with midpoint10% above linear m3','2/6*(4e6+4*(4.5e6*1.1)+5e6)',9.6e6,1e-8)],
'b296':[('ten tide old-water percent','100*.95**10',59.87,.005)],
'b299':[('reduced runoff coefficient m3','500*.020*.60',6,1e-9),('runoff reduction percent','(8-6)/8*100',25,1e-9)],
'b300':[('shared bias shift m','((43/4+49)/(1/4+1))-(40/4+46)/(1/4+1)',3,1e-9)]
}
