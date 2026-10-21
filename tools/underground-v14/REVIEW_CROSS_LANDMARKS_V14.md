# Independent cross-review by the landmark author

Reviewed 2026-10-21. This supplemental review covers all 50 displayed models in b171–b175, authored by another agent, with 68 independently re-expressed intermediate and final results. `audit_cross_landmarks.py` imports none of the support author functions; it compares its own arithmetic against both language halves at half the last displayed digit. All 68 results pass. Exact input-file hashes and quantities are in `audit_cross_landmarks.json`.

| Course | Coverage | Representative independent result |
|---|---:|---|
| b171 box jacking | 10 models | Box weight 5760 kN; strip moment 306.25 kN·m; eccentric elastic stress 3750 kPa |
| b172 microtunnelling | 10 models | Face resultant 441.7865 kN; equivalent-Newtonian pressure drop 96000 Pa |
| b173 intermediate stations | 10 models | Radial force 34.9048 kN; elastic shortening 0.0166667 m |
| b174 HDD guidance | 10 models | Curvature radius 343.7747 m; magnetic heading bias 1.43210 degrees |
| b175 caissons | 10 models | Plug uplift 7704.7560 kN; raw weight/uplift ratio 1.22324 |

The mechanism and failure fields were checked for the following application boundaries:

- b171: roof-strip moments are not substituted for frame corner moments; elastic eccentric stress requires uncracked section properties; overbreak volume is not a particular building settlement.
- b172: return slurry solids are not all new excavation; Darcy loss is explicitly an equivalent-Newtonian scale check; integrated trough area is volume per unit length, not total volume.
- b173: intermediate stations retain a reaction path, and leading/rear loads are stage-dependent; curved-pipe radial resultant describes one node, not total curved-drive friction.
- b174: bounded centerline separation still requires both external radii to be deducted; elastic steel strain is not transferred to thermoplastic products. The 0.0349 m gyro example projects the final angle across the entire length and is not an integrated guidance-path error.
- b175: the granular critical-gradient comparison is distinguished from undrained clay heave; base-plug self-weight does not establish wall transfer; nominal seal strain does not prove water tightness; raw weight ratio is not a code safety factor.

Final support-freeze input hashes were refreshed after rereading the clarified model labels and boundaries; the same 68 displayed results still pass. No arithmetic correction was needed in this final snapshot. This review checks the displayed base examples and selected physical boundaries. It does not claim full sensitivity recalculation, regulatory compliance, or design adequacy. The separate landmark audit covers all 250 own-course base examples and all 250 sensitivities.
