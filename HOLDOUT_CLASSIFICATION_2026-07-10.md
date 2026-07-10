# Species classification sweep of the 1104 BB(6) holdouts — landscape + the collapse obstruction

*The [C]-frontier dig of 2026-07-10: an automated species census over all 1104 BB(6) holdouts, to test whether the
"1087 un-catalogued" collapse to the known ~5 engines (⟹ the complete proof's [C] is a small conjecture set) or form
a long tail, and to decide any that fall to certified tools. HONEST OUTCOME: the landscape is fully mapped and the
collapse-by-coarse-probe is proven impossible for a structural reason; no machine decided. Scripts: `hc_sim.py`,
`hc_classify.py`, `hc_census.py`, `hc_decide.py`. Every multiplier here is `[OBSERVED, width-ratio proxy]`, not a
certified Type-I assignment. No machine decided. No label upgraded.*

## 1. The species census (all 1104, per-machine sim to 3·10⁵ steps, fork-parallel)

**Growth-exponent band** (width ~ t^a): sqrt-t **663**, sub-sqrt **387**, bounded~cycler **47**, intermediate **7**.
→ Every holdout is a **slow polynomial-width counter** (0 halt-in-cap, 0 exponential-width), confirming
`HOLDOUT_SWEEP_FEASIBILITY` / `BB6_FRONTIER_CENSUS` at full 1104 granularity.

**Block structure:** digit-string **924**, bounded-digit **498**, unary/scalar **19**, mixed **18** (overlapping tags).

**Multiplier extraction (width-ratio probe):** clean width-multiplier on only **8 / 1104** (×7/6:5, ×4/3:2 [known
engine], ×6/5:1); **924** are digit-string with the multiplier *hidden from tape width*; **171** width-grows but
noisy/unmatched.

## 2. The collapse obstruction `[the load-bearing finding]`

**A coarse automated probe CANNOT collapse the 1087 to the ~5 named engines — for a structural reason, not a compute
limit.** The ×p/q multiplier of a Type-I machine is visible in the tape *width* only when the counter is **unary**
(width ∝ value). But **924 of the 1104 are digit-string machines**, where the value is encoded as a digit-string and
the width stays ≈ constant while the *value* grows ×(p/q) — **exactly o4's own structure** (o4's ×4/3 lives in the
base-4/3 odometer digit-string; its tape width does NOT reveal 4/3). So the width-ratio proxy is blind to the engine
of the digit-string majority. Extracting the engine of such a machine requires the **per-machine milestone analysis**
that each of the 17 named cryptids received by hand (find the milestone form, read off the value map, match the
fixed-point/reload structure). Doing that for 924 machines is not a coarse sweep — it is either 924× hand-analyses or
an automated milestone-extractor of Coq-BB5-scale sophistication.

## 3. Decision yield `[confirmed 0]`

The 47 bounded~cycler machines (the highest-yield sample — those that *look* bounded to 3·10⁵ steps) were run through
the trusted certified suite (`suite.verdict`, sim 2·10⁶ + halt-unreachable + translated-cycler + 3 bouncer variants +
halt-segment + FAR): **47 / 47 HOLDOUT, 0 decided.** They are not genuine cyclers (those were already removed by the
community); they are slow counters with long transients that survive our suite exactly as C1's 0/10 and the historical
0/300 predicted — our certified tools ARE (a subset of) the community decider class that produced this residual.

## 4. Honest verdict for the complete proof's [C]

- **What advanced:** the full 1104 landscape is now quantified (all slow polynomial-width counters; 924 digit-string),
  and the reason a coarse collapse is impossible is pinned structurally (the multiplier is in the digit-string, invisible
  to width — the o4 phenomenon at scale).
- **What did NOT collapse:** the 1087 un-catalogued holdouts do **not** reduce to the ~5 engines by any coarse probe;
  each digit-string machine needs deep per-machine analysis. [C] therefore remains **community-scale**, as C1 concluded
  — now with the structural reason, not just an empirical 0/10.
- **Contrast with the achieved [A] collapse:** the 17 *named* conjectures DID collapse to 3 meta-schemas
  (`Completion.lean`, `MINIMAL_CONJECTURE_SET`), because those 17 had already received the deep per-machine analysis.
  The 1087 have not, and automating that analysis is the genuine remaining engineering — the honest boundary between
  what internal work reaches ([A] done, [C] mapped-but-not-collapsed) and what needs the full formal pipeline.

**Net:** no machine decided; the [C] frontier is mapped and its collapse-obstruction identified, sharpening (not
crossing) the community-scale boundary of the complete proof. No machine decided. No label upgraded.
