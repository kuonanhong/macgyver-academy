# V16 b368–b400 content review

Reviewed 2026-10-23. This date records editorial verification only.

All 33 input files meet the bilingual schema: 330 distinct unit titles within their courses, each with mechanism, computable model, stated applicability, measurement chain, causal failure explanation, false misconception and parameter experiment. The shared course builder expands each unit to four steps; this authoring batch supplies 1,320 steps.

The control author reviewed b391–b400 independently from the agent who wrote their topic briefs. The parent additionally reviewed all tail contexts. The scene reviewer independently reviewed b368–b390, source dates, and all numerical primitives; its record is `tools/rail-v16/reviews/peer_control.json`. This division prevents the tail author's own prose review from being represented as independent.

Substantive corrections made before freeze:

- Boolean-variable count is distinguished from the exponential state count. Observed axles, cases, alarms and other discrete sensitivity inputs increase by one whole count, while continuous parameters increase by ten percent. Fluid queue expectation may be fractional and is explicitly identified as an average-flow approximation.
- Pressure sampling is temporal (milliseconds); pressure uncertainty is in pascals. Pedestrian trajectory samples use a hypothetical walking speed. Elevator and maintenance cycles use direct stage definitions and trips/hour or jobs/hour, rather than crane terminology.
- Rail strain uncertainty uses microstrain. Wheel scanning uses circumferential surface speed. Coupled point actuators, suspended switch mechanisms and container lifting have appropriate geometry and failure wording.
- Repeated actuator heating is a duty-averaged steady model, not a transient heat-capacity model. Small battery examples cover monitoring/control or lighting, not whole-plant motive power or traction range.
- Static air-gap magnetic pressure is explicitly a comparison model and is not presented as superconducting electrodynamic suspension. Natural-frequency calculations exclude damping and do not claim ride-response amplitudes.
- Grooved-rail error budget is not actual groove clearance; runoff demand is not drain capacity; DC feeder losses do not reproduce ground-power segment logic.
- Dated public sources distinguish US DOT transportation accessibility standards (2006) from DOJ general-facility standards. FTA 1991 is a reprint of the 1985 guide. FRA crossing human factors is 2006, and the EU 2023 control milestone has an actual EUR-Lex regulation source.

For b391–b400 the model/context review covered wash-water mass balance and hydraulic brush-arm limits; hump potential/kinetic-energy boundaries and offline timing; container load sharing and pendulum sway; CWR thermal sign, restraint and compensated strain; street groove/drainage interfaces; ground power versus storage; straddle-beam bending/torsion; suspended-switch position versus retention; maglev spatial/temporal excitation; and integration requirements, timebases and finite-sample evidence.

Independent numerical evidence comprises 89 reference-value and SI-dimension checks and 330 sensitivity cases. `authored_control/verify.py` checks schema, rendered bilingual numbers and parameter bounds. These are educational computations, not operational settings, site acceptance criteria or certifications. Reference locations are approximate orientation points; vendor/institution entries identify public roles without asserting unverified procurement relationships.
