from pathlib import Path
import json
HERE=Path(__file__).resolve().parent
# Each row describes actual engineering study subjects. The row order has no
# geometric effect; no numeric ID or hash is rendered as a distinguishing mark.
rows='''
b301|railside|track pantograph signal bridge|High-speed rolling stock with track, overhead collection, train protection and civil interfaces.
b302|traincar|wheel signal viaduct control|Automated elevated metro with guide wheels, train control, viaduct and automation.
b303|rail|station pantograph brake tunnel|Metro station interfaces, traction supply, braking and underground alignment.
b304|rail|station ground signal voltage|Urban metro stations, underground conditions, signaling and traction supply.
b305|railside|aircraft station clock network|Airport railway connecting air-terminal access, stations, travel time and service coordination.
b306|railside|track pantograph spring signal|High-speed running, current collection, dynamic response and train protection.
b307|railside|tunnel vent fire track|High-speed railway with tunnel ventilation, fire strategy and track interfaces.
b308|railside|cool heat pantograph signal|Cold-weather high-speed railway, snow/ice response, contact collection and protection.
b309|railside|force brake tunnel motor|Mountain high-speed alignment, grades, braking, tunnels and traction.
b310|railside|switch track transformer clock|High-speed line interfaces: turnouts, track, traction conversion and service timing.
b311|railside|signal network station clock|International high-speed interoperability, signaling, communications and timetable interfaces.
b312|railside|tunnel station shield signal|High-speed tunnel and terminal interfaces with protection and operational safety.
b313|railside|map heat pantograph track|Long-distance high-speed alignment, thermal exposure, supply and track geometry.
b314|railside|viaduct station clock grid|Large high-speed corridor with viaducts, stations, capacity and network interfaces.
b315|railside|bridge tunnel flow signal|High-speed corridor civil structures, tunnels, drainage and train protection.
b316|track|cool ground heat sensor|Permafrost track support, freezing/thawing, thermal balance and condition monitoring.
b317|railside|tunnel viaduct motor signal|High-speed vehicle/traction interfaces across tunnels and viaducts.
b318|railside|heat filter station pantograph|Desert high-speed operation, dust filtration, stations and overhead supply.
b319|railside|map voltage station clock|High-speed corridor integration, power supply, stations and service timing.
b320|railside|tunnel spring viaduct sensor|High-speed civil and dynamic interfaces with tunnel/viaduct condition monitoring.
b321|traincar|tunnel station signal clock|Cross-city railway linking tunnels, platforms, train control and timetable capacity.
b322|traincar|station force network clock|Dense commuter services: platform loads, network interfaces and timetable capacity.
b323|traincar|aircraft station shield clock|Airport express terminal integration, passenger movement, safety and timing.
b324|traincar|tunnel signal control voltage|Automated underground metro with signaling, automation and traction supply.
b325|traincar|viaduct heat control station|Elevated automated metro with climate exposure and station interfaces.
b326|traincar|tunnel ring station signal|Circular underground metro: ring-route connectivity, stations and protection.
b327|traincar|tunnel viaduct control signal|Automated metro integrating underground and elevated sections.
b328|traincar|aircraft bridge tunnel station|Airport-linked metro through bridge, tunnel and station interfaces.
b329|rail|tunnel ground station vent|Urban subway construction, ground support, stations and ventilation.
b330|traincar|tunnel network switch station|Urban light-rail connection, junctions and station integration.
b331|traincar|tunnel waves station control|Coastal urban metro interfaces, underground structures and automation.
b332|traincar|grid heat station voltage|Multiline metro integration with climate, station and power interfaces.
b333|traincar|tunnel heat control network|Automated metro in a hot climate with tunnels and network integration.
b334|tunnel|traincar station ground vent|Metro tunnel project linking railway systems, stations, ground and ventilation.
b335|traincar|force signal pantograph network|Freight railway with axle loading, train protection, collection and logistics.
b336|track|map survey force chart|Horizontal/vertical route geometry, surveying, load and geometric checks.
b337|track|wheel force spring survey|Cant balances wheel loads, lateral forces, dynamics and geometry.
b338|track|concrete foundation ground check|Slab-track concrete, foundations, subgrade and acceptance checks.
b339|track|alignment survey concrete bond|Precast slab alignment, survey references, concrete and interface attachment.
b340|track|heat strain force sensor|Continuously welded rail thermal stress, strain, restraint and monitoring.
b341|track|current heat force bond|Flash-butt welding combines electrical heating, upsetting force and joint formation.
b342|track|sample heat material bond|Aluminothermic welding uses reaction heat, filler metal and rail-joint formation.
b343|track|gear ground alignment survey|Ballast tamping, granular support, alignment and survey verification.
b344|track|filter ground leaf gear|Ballast screening, granular materials, reuse and cleaning machinery.
b345|track|spring bond force wheel|Resilient fasteners transfer wheel loads through elastic rail attachments.
b346|track|concrete spring wave ground|Floating slabs separate structural mass from ground through resilient isolation.
b347|track|gear wave probe material|Grinding treats rail corrugation using tools, profile measurement and material removal.
b348|track|survey sensor spring chart|Moving geometry inspection combines survey references, sensors, dynamics and data.
b349|track|wave probe crack check|Ultrasonic probes, wave responses, internal flaws and verification.
b350|track|concrete force test crack|Sleeper load tests connect material durability, force and crack evidence.
b351|switch|track alignment wheel check|Turnout assembly depends on rail geometry, wheel passage and inspection.
b352|switch|track control alignment sensor|Movable crossings need actuation, alignment and position detection.
b353|switch|heat cool voltage sensor|Turnout heating balances snow/ice conditions, electrical supply and sensing.
b354|track|ground foundation spring force|Subgrade transitions combine changing support stiffness and dynamic loads.
b355|embankment|track cool heat ground|Rail embankments over frozen ground require thermal and soil assessment.
b356|track|force spring ground sensor|Heavy-haul support modulus connects axle force, stiffness and monitored ground response.
b357|traincar|track wheel spring force|Vehicle–track coupling links wheel contact, suspension and dynamic force.
b358|bridge|track heat strain force|Rail–bridge coupling considers thermal movement, strain and restraint force.
b359|track|ground sensor shield signal|Trackside geohazard detection links ground observation to protective warning.
b360|pantograph|cable spring survey voltage|Contact-line suspension integrates wire geometry, tension, alignment and power.
b361|pantograph|sensor wave current check|Current-collection verification measures contact behavior, current and dynamic response.
b362|transformer|voltage current switch shield|Traction substations combine conversion, feeders, switching and protection.
b363|track|voltage current shield bond|Third-rail supply requires conductive rail, return interfaces and protective isolation.
b364|current|track ground probe shield|Return-current paths, soil leakage, measurement and corrosion control.
b365|wheel|droplet pressure strain sensor|Wheel–rail friction and lubrication depend on film, pressure, contact strain and observation.
b366|battery|voltage transformer clock track|Wayside storage exchanges traction energy through converters over duty cycles.
b367|signal|brake sensor shield track|Automatic protection supervises position, braking limits and safe movement.
b368|traincar|control brake clock signal|Automatic train operation commands traction/braking under timetable and protection constraints.
b369|network|traincar clock chart signal|Supervision coordinates fleet position, timetables, performance and signals.
b370|signal|antenna identity clock traincar|Communications-based train control uses radio identity, timing and moving trains.
b371|signal|map network shield traincar|European train-control integration combines interoperable route data and protection.
b372|switch|code shield check signal|Electronic interlocking verifies logic, mutual exclusion and signal safety.
b373|track|current sensor traincar shield|Track circuits infer occupancy through electrical track response and safe logic.
b374|wheel|sensor current traincar check|Axle counters sense wheel passages and reconcile entry/exit counts.
b375|switch|motor gear alignment sensor|Point machines link drive, transmission, mechanical alignment and detection.
b376|traincar|sensor wheel map clock|Train-position fusion combines odometry, location references and time.
b377|clock|network traincar switch chart|Timetable conflicts involve trains, junction resources and schedule analysis.
b378|control|identity network signal check|Operations-center interfaces support operators, network status, signaling and checks.
b379|shield|signal crack code check|Fail-safe signaling connects faults, logic and verified safe states.
b380|signal|car traincar clock shield|Grade-crossing coordination separates road/rail movement using timing and protection.
b381|door|station alignment sensor traincar|Platform-screen doors synchronize stopping position and detected vehicle state.
b382|station|flow identity map chart|Passenger flow connects demand, people, station layout and simulation results.
b383|station|tower identity force clock|Vertical circulation considers lifts/escalators, passengers, loading and waiting time.
b384|station|identity alignment door check|Accessible boarding links people, gap/height alignment, door access and inspection.
b385|station|fire vent pressure shield|Station smoke control combines fire scenarios, ventilation, pressure and safe routes.
b386|tunnel|traincar vent pressure flow|Piston winds couple train motion, tunnel flow, pressure and ventilation.
b387|tunnel|identity door fire shield|Tunnel evacuation walkways connect people, exits, fire and protected routes.
b388|station|gear traincar clock check|Depot workflow coordinates equipment, rolling stock, task scheduling and verification.
b389|wheel|gear force alignment traincar|Bogie exchange combines lifting load, machine positioning and rolling-stock interfaces.
b390|wheel|gear probe material track|Underfloor lathes restore wheel profiles through cutting, measurement and retained track support.
b391|traincar|droplet filter pump leaf|Train washing combines water, filtration, pumping and environmental management.
b392|track|brake sensor force control|Hump-yard retarders control wagon gravity motion using sensing and braking.
b393|traincar|layers force gear network|Intermodal containers require stacking, lifting loads, handling equipment and logistics.
b394|track|strain heat sensor chart|Welded-rail strain monitoring combines thermal state, sensors and recorded trends.
b395|track|car traincar wheel map|Grooved street rails share an urban corridor with road users and guided wheels.
b396|traincar|battery voltage station control|Catenary-free light rail uses stored energy, stop charging and control.
b397|beam|traincar wheel force alignment|Straddle monorail beams guide load-bearing wheels and constrain alignment.
b398|traincar|beam switch motor alignment|Suspended monorail switches transfer hanging vehicles through movable guideway elements.
b399|railside|magnet survey sensor alignment|Maglev guideway precision connects levitation, surveying and monitored alignment.
b400|traincar|network check signal clock|System integration testing verifies interfaces, signaling and trial-run sequences.
a327|code|layers clock check shield|Reproducible builds fix input layers, time-dependent variation and verification boundaries.
a399|code|network identity check lock|Collaborative Linux engineering connects contributors, interfaces, reviews and access control.
'''
result={}
for line in rows.strip().splitlines():
 ident,main,features,rationale=line.split('|');result[ident]={'main':main,'features':features.split(),'rationale':rationale}
(HERE/'icon-overrides.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n')
