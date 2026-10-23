# b335–b367 authoring and review

This set contains 33 complete Traditional Chinese/English course inputs, 330 distinct technical units and 330 executable numerical examples. The shared course builder expands each unit into four steps (1,320 steps for this range). This authoring tool writes only its assigned input files and numerical evidence; it does not change the application or shared builder.

Run from the V16 project directory:

```bash
python3 tools/rail-v16/author_track.py
python3 -I tools/rail-v16/validate_input.py tools/rail-v16/inputs/b{335..367}.json
python3 tools/rail-v16/reviews/review_track_numeric.py
```

`author_track.py` reads current titles and disciplines from `targets.json`. Its own first five records and the four `track_records_*.py` files hold the authored physics, numerical parameters, observations and failures. `track_unit_context.py`, `track_context_340_353.py`, `track_context_356.py`, or explicit fields within the records provide each unit's boundary and measurement chain. `track_metadata.py` supplies topic-specific source routing, real publication/project milestones, codes/guides, landmarks, vendors and system nodes.

Every numerical input is explicitly a hypothetical teaching value, not a claimed project specification or manufacturer setting. Formula parameters carry units. Ordinary continuous parameters use a 10% perturbation; integer counts use +1; absolute Celsius temperatures use +1 degree; the near-unity charging efficiency uses +0.01 to remain within its physical range. `track_numeric_models.json` records the exact changed input, result, boundary and measurement chain.

Independent review is in `peer_track_numeric.json` and `peer_track.json`. Its AST evaluator independently propagates arithmetic and physical dimensions without importing the generator evaluator. The final run checks all 330 baseline and sensitivity models plus generated-boundary freshness. Schema validation passes all 33 inputs. Primary-source identity and historical dates are documented in `peer_track_sources.json` and `track_additional_source_checks.json`.

Substantive review corrections include unit-specific ventilation measurements, mean-versus-spread terminology, transverse prestress bending, interval versus tangent stiffness, integer state combinations, Celsius versus Coulomb notation, energy per day, recomputation of the contact-force mean, bounded efficiency sensitivity and explicit alternative count datasets. Every misconception now contradicts that unit's own stated failure mechanism, giving a specific false proposition for the quiz. Measurement evidence is not automatically called independent evidence.

The numerical review establishes arithmetic and dimensional consistency of the stated reduced models. It does not establish site-specific physical completeness or operating approval. Public primary sources supply background, scope and dated milestones; the calculations and lesson analyses are original teaching material. No paid standard clauses or proprietary field settings were copied.
