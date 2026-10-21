# V15 independent peer review — b221–b240

Status: **PASS**, reviewed on 2026-10-21 by `/root/courses_landmarks`, who did not author these 20 courses.

The review read all 200 visible models and all 200 misconception options, independently recomputed 302 displayed primary and secondary model values, and examined dimensional consistency and stated physical limits. Each misconception was checked as a false belief suitable for the wrong quiz choice. All 20 metadata records were read for factual versus hypothetical quantities, dates, source scope and institutional roles. Twenty example sensitivity comparisons were separately checked, including 61 baseline, changed or derived values.

Independent arithmetic is transcribed in `peer_landmarks_checks.py` and `peer_landmarks_sensitivity_checks.json`; it does not import the author's calculation/audit code. `peer_landmarks.json` binds each reviewed model and quiz text to its SHA-256 and records each final full input, non-unit metadata and example hash. `verify_peer_landmarks.py` uses the release gate's restricted arithmetic evaluator to check these records against the current inputs.

Resolved findings:

- Explicit freshwater density, gravity, unit weight and dimensional coefficients were added to visible models where previously implicit. This affected 34 models in 15 courses without changing numerical answers.
- b234's 2014 seepage/instrumentation publication chronology gained the official Reclamation design-standards index in its source list.
- b237 unit 10 and its corresponding fact now specify approximately linear normalization at an effective test pressure of 1 MPa, with values in L/(min·m); the mean 5.4 and median 2 are not presented as hydraulic conductivity.
- Sixteen course examples gained a fixed-condition, single-parameter sensitivity comparison. The final bilingual additions were read directly and recomputed independently; unit contents were not part of this last modification.

Examples checked include net hydrostatic force, Froude similarity, common-cause reliability, harmonic phase addition, lock equalization, caisson displacement, nonlinear multi-year exceedance, thin-arch compression, Darcy discharge, percentage-point changes in voids, steady drainage networks and Manning capacity. Boundaries distinguish ideal models from actual operating limits, contract acceptance and site design.

`peer_landmarks_sources.json` records 30 independent source cross-checks, including owner/authority project pages, official publication indexes and original publisher abstracts. It explicitly identifies indexed excerpts, access failures and abstract-level evidence. It does **not** claim that every linked PDF or paywalled paper was read in full. Course source URLs and their stated scopes were reviewed; institutional associations were not converted into unsupported contractor or securities claims. Teaching calculations remain separately stated hypothetical examples.

No material unresolved issue remains within this review scope. This review verifies educational content and arithmetic; it is not a site-specific engineering design approval.
