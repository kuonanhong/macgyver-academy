# Control, stations and maintenance curricula

Original bilingual authoring records for b368–b400. Equations use explicitly hypothetical educational inputs. Shared mathematical primitives are reused only with a distinct engineering boundary, measurement question and failure interpretation. They are not operational instructions, vendor commissioning limits or safety certification.

`generate.py` builds the 33 input files. `verify.py` independently checks the resulting arithmetic and structural requirements. Source evidence records describe precisely which public facts are supported; all numerical exercise inputs are original assumptions.

## Reproduce and review

From the repository root:

```sh
python3 tools/rail-v16/authored_control/generate.py
python3 tools/rail-v16/authored_control/verify.py
python3 tools/rail-v16/reviews/peer_control.py
```

The independent reviewer authored `reviews/peer_control.py`: 89 manually reduced baseline references and physical-dimension checks, plus all 330 generated sensitivity cases. `verify.py` additionally validates all 33 schemas, bilingual displayed numbers, probability bounds and 102 integer-count scenarios. Reusable primitives are documented separately from the 330 topic contexts. The output contains 33 courses × 10 units, expanded by the shared build into 1,320 steps.

Publication milestones refer to specific verified events: IEC editions 2002/2025, Commission Regulation (EU) 2023/1695, US DOT accessibility adoption 2006, FRA platform guidance 2022, FTA emergency-guide reprint 1991 (original 1985), ISO 2010/2015/2023 editions, and dated primary railway research. Review dates are never substituted for historical milestones. ISO 9001:2015 is explicitly historical, not asserted to be the current edition.

The ground-power overview was replaced with an official 2018 Bordeaux retrospective supporting the 2003 event; FRA crossing-human-factors publication is December 2006. Sources support bibliographic/project context and clearly scoped principles. Numeric inputs and sensitivities are original hypothetical teaching assumptions, not extracted field settings.
