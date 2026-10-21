/* Original code-native educational symbols. Not dimensioned construction drawings. */
export const undergroundMotifs={
 tunnel:'<path d="M-30 30V0A30 30 0 0 1 30 0V30ZM-23 30V0A23 23 0 0 1 23 0V30M-38 30H38M-34-27L-29-31M-15-35L-13-39M15-35L13-39M34-27L29-31"/>',
 tbm:'<circle r="31"/><circle r="23"/><circle r="6"/><path d="M0-23V-6M0 6V23M-23 0H-6M6 0H23M-16-16L-4-4M4 4L16 16M16-16L4-4M-4 4L-16 16"/><circle cx="-8" cy="-17" r="2"/><circle cx="17" cy="-8" r="2"/><circle cx="8" cy="17" r="2"/>',
 immersed:'<path d="M-38-24q9-6 18 0t18 0 18 0 18 0M-38-12q9-6 18 0t18 0 18 0 18 0M-36 32H36M-32 20L-22 30H22L32 20"/><rect x="-25" y="0" width="50" height="22" rx="4"/><path d="M-19 17V6H-4V17ZM4 17V6H19V17ZM-25 0L-17-12M25 0L17-12"/>',
 cavern:'<path d="M-38 30V-18L-24-31H21L38-16V30M-26 30V0Q-26-21 0-21Q26-21 26 0V30ZM-15-20L-18-30M15-20L18-30M-26 0L-37-4M26 0L37-4M-37 30H37"/>',
 probe:'<path d="M-38-20H38M-38 0H38M-38 22H38M-18-35L18 31M-12-38L24 28M18 31L23 34L24 28M-15-30L-26-24M-5-12L-16-6M5 6L-6 12"/><circle cx="30" cy="11" r="4"/>',
 lining:'<circle r="32"/><circle r="24"/><path d="M0-32V-24M28-16L21-12M28 16L21 12M0 24V32M-28 16L-21 12M-28-16L-21-12M-38 34H38"/>',
 grout:'<circle r="31"/><circle r="22"/><path d="M0-37V-27M0 27V37M-37 0H-27M27 0H37M-3-30L0-25L3-30M27-3L24 0L27 3M-27-3L-24 0L-27 3M-3 30L0 25L3 30"/><circle cx="19" cy="19" r="2"/><circle cx="-19" cy="-19" r="2"/>',
 support:'<path d="M-27 30V0A27 27 0 0 1 27 0V30M-35 30H35M0-27V-39M-19-19L-29-29M19-19L29-29M-27 0H-39M27 0H39M-4-31H4M-25-19L-19-25M19-25L25-19"/>',
 shaft:'<path d="M-38-27H-18V32H18V-27H38M-12-27V32M12-27V32M-12-17H12M-12-3H12M-12 11H12M-26-18H-18M18-18H26M-26 0H-18M18 0H26M-26 18H-18M18 18H26M-28 32H28"/>',
 excavation:'<path d="M-38-27H-27V32M27-27V32H38M-27-12H27M-27 8H27M-27 30H27M-19-12L-14-19M19-12L14-19M-38 0H-28M28 0H38M-38 20H-28M28 20H38"/>',
 pipe:'<path d="M-38-25H38M-38 25H38M-38 6H-20V-6H-38M-20-15H30V15H-20ZM-12-15V15M0-15V15M12-15V15M30-15L38 0L30 15M-34 0H-23"/>',
 ground:'<path d="M-38-24H38M-38 4H38M-38 30H38M-25-24V30M-10-24V30M5-24V30M20-24V30M-28-16H-22M-13-8H-7M2-16H8M17-8H23M-28 12H-22M-13 22H-7M2 12H8M17 22H23"/>',
 water:'<path d="M-38-24q9-6 18 0t18 0 18 0 18 0M-38-8q9-6 18 0t18 0 18 0 18 0M-25 30V14A25 25 0 0 1 25 14V30ZM-30-2L-20 5M-25-1L-20 5L-26 5M30-2L20 5M25-1L20 5L26 5M0-10V0M-4-5L0 0L4-5"/>',
 monitoring:'<path d="M-32 31V2Q0-37 32 2V31M-22 20H22M0-22V20M-4 14L0 20L4 14M-16 16L-22 20L-16 24M16 16L22 20L16 24"/><circle cx="0" cy="-22" r="3"/><circle cx="-22" cy="20" r="3"/><circle cx="22" cy="20" r="3"/>'
};
export function undergroundComponentMotif(name,family){
 if(!undergroundMotifs[family])return '';
 const n=String(name).toLowerCase();
 for(const [pattern,key] of [[/groundwater|water|drain|pore/,'water'],[/instrument|monitor|sensor|converg/,'monitoring'],[/grout|injection/,'grout'],[/segment|lining|joint/,'lining'],[/cutter|shield|tbm/,'tbm'],[/bolt|support|rock mass/,'support'],[/shaft|hoist/,'shaft'],[/probe|borehole|core sample/,'probe'],[/soil|ground|consolid/,'ground']])if(pattern.test(n))return undergroundMotifs[key];
 return undergroundMotifs[family]||'';
}
