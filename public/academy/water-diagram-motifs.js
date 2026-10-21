// Original symbols for functional learning diagrams; not engineering drawings.
export const waterMotifs={
 'water-dam':'<path d="M-36-8H-7M-36 3H-7M-36 14H-7M-8-30H5L31 30H-8ZM-40 30H40"/><path d="M0-17L12 16H21" stroke-dasharray="4 3"/>',
 'water-gate':'<path d="M-36 30H36M-24 30V-28M24 30V-28M-24-28H24M0-28V-10M-16-10H16V22H-16ZM-36 2H-27M27 14H36M-36 12H-27"/>',
 'water-lock':'<path d="M-38-20H38M-38 20H38M-25-20V20M25-20V20M-16 0H16L10 10H-10ZM-32-32V-22M32 22V32"/><path d="M-8-20V-30H8V-20M-8 20V30H8V20"/>',
 'water-hydraulic':'<path d="M-38-26H-8L8 22H38M-38-16H-14L2 30H38M4 12Q12-4 23 12Q32 25 40 12M12 30V38M28 30V38"/>',
 'water-pipe':'<path d="M-38-8H-18V-28H18V-8H38M-38 8H-2V-12H2V8H38M-28-14V14M28-14V14"/><circle cx="0" cy="-28" r="8"/><path d="M0-33V-28L5-25"/>',
 'water-river':'<path d="M-24-34C20-12-22 12 24 34M-40-34C4-12-38 12 8 34M-34 10L-24-2-14 10M15-10L25-22 35-10"/><path d="M-8-18L0-13-8-8M-4 12L4 17-4 22"/>',
 'water-coast':'<path d="M-38-20Q-30-30-22-20T-6-20T10-20T26-20T42-20M-38-4Q-30-14-22-4T-6-4T10-4M-10 30L7 7 20 7 38 30ZM-38 30H40"/><path d="M1 22L9 17 17 23M15 8L17 15"/>',
 'water-port':'<path d="M-36 0H36M-26 0V30M-8 0V30M10 0V30M28 0V30M-20 0V-32H22M-18-30L12-8M20-32V-14M14-14H26L20-7Z"/><path d="M-36 34Q-28 26-20 34T-4 34T12 34T28 34"/>',
 'water-ecology':'<path d="M-36 22Q-26 12-16 22T4 22T24 22T44 22M-24 18V-20M-24-4Q-38-16-27-25M-24 6Q-10-6-20-14M10 18V-30M10-12Q-3-23 7-32M10 3Q25-9 15-18"/>'
};

export function waterComponentMotif(name,family){
 if(!String(family).startsWith('water-'))return '';
 const n=String(name).toLowerCase();
 if(/monitor|sensor|track|uncertainty|measurement|survey|instrument|spectr|correlat|acoustic/.test(n))return '<rect x="-32" y="-26" width="64" height="48" rx="4"/><path d="M-24 9L-15-3-6 4 4-15 14-5 24-10M0 22V32M-16 32H16"/>';
 if(/weight|buoyan|moment|torque|stress|force|bearing|hinge|uplift|sliding|stability/.test(n))return '<rect x="-18" y="-14" width="36" height="28" rx="2"/><path d="M0-36V-17M-5-23L0-17 5-23M0 36V17M-5 23L0 17 5 23M-36 0H-21M-27-5L-21 0-27 5M-28 28H28"/>';
 if(/filter|poros|permeab|seep|drainage|grouting/.test(n))return '<path d="M-32-26V26H32V-26M-38 0H-25M25 0H38M32-5L38 0 32 5"/><circle cx="-15" cy="-13" r="6"/><circle cx="1" cy="-13" r="6"/><circle cx="17" cy="-13" r="6"/><circle cx="-7" cy="10" r="7"/><circle cx="11" cy="10" r="7"/>';
 if(/hydrograph|routing|storage|balance|reservoir|retention|residence/.test(n))return '<path d="M-28-25V26H28V-25M-28 3Q-19-4-10 3T8 3T26 3M-40-14H-13M-19-19L-13-14-19-9M13 15H40M34 10L40 15 34 20"/>';
 if(/tide|surge|wave|spectrum|overtop|runup|reflection/.test(n))return '<path d="M-38-6Q-26-32-14-6T10-6T34-6M-38 14Q-26-12-14 14T10 14T34 14M-38 34H38M-28-28V-8M-33-23L-28-28-23-23"/>';
 if(/pipe|flow|discharge|velocity|drag|head loss|friction|water hammer/.test(n))return '<path d="M-38-16H-8V-28H18V-16H38M-38 16H38M-20 0H21M13-7L21 0 13 7M-29-22V22M29-22V22"/>';
 if(/gate|barrier|closure|opening|seal/.test(n))return waterMotifs['water-gate'];
 if(/lock|navigation|vessel|queue|ship/.test(n))return waterMotifs['water-lock'];
 if(/sediment|scour|erosion|bedload|grading|silt/.test(n))return '<path d="M-38-16Q-28-24-18-16T2-16T22-16T42-16M-38 10Q-14 10-8 23T10 23T38 10M-32 30H32"/><circle cx="-26" cy="2" r="3"/><circle cx="-11" cy="5" r="3"/><circle cx="8" cy="9" r="3"/><circle cx="26" cy="1" r="3"/>';
 if(/salt|salin|mixing|tracer|diffusion|concentration|quality/.test(n))return '<path d="M-26-30V29H26V-30M-26 8H26M-26-8H26M0-30V3M-5-3L0 3 5-3"/><circle cx="-14" cy="19" r="2"/><circle cx="2" cy="19" r="2"/><circle cx="17" cy="19" r="2"/><circle cx="-13" cy="-18" r="2"/><circle cx="15" cy="-18" r="2"/>';
 if(/rain|storm|catchment|runoff/.test(n))return '<path d="M-28-8C-42-22-21-34-12-23C-8-40 19-35 20-22C39-23 39-7 27-7ZM-22 4L-27 14M-5 4L-10 14M12 4L7 14M29 4L24 14M-38 30L-12 20 8 30 34 19"/>';
 if(/lift|sling|crane|placement/.test(n))return '<path d="M0-35V-22M-26 8L0-22 26 8M-26 8H26V30H-26ZM0-22V8M-34 34H34"/>';
 if(/power|pump|turbine|energy|efficien/.test(n))return '<circle r="24"/><circle r="6"/><path d="M0-6V-24M6 0H24M0 6V24M-6 0H-24M-38 0H-24M24 0H38M-12 25V33H12V25"/>';
 if(/scale|froude|similarity/.test(n))return '<path d="M-36 23V-25H-8V23ZM12 23V-1H26V23ZM-36 31H26M-3-14H22M16-19L22-14 16-9M-28-8H-16M16 11H22"/>';
 return '';
}
