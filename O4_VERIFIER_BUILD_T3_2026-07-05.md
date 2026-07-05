# Counter-automaton verifier for o4 — build turn 3: the uniform-per-residue closure FAILS (honest negative) (2026-07-05)

*Turn 3: test whether one generation is uniform per residue class `G mod 3` (the two-counter closure that would decide
o4). **It is NOT.** Within each residue class the jump-trace phase-signatures are **all distinct**, because the number
of phases per generation **grows `~log(G)`** — the generation processes the full **base-4/3 digit string** of `G`, not
just `G mod 3`. So the two-counter `(G, a)` model is **insufficient**; o4's certificate must track the base-4/3
representation (variable-length carry). Honest negative; the verifier design must be revised. SOUNDNESS: `[OBSERVED]`;
o4 `[OPEN]` — **not decided**. No machine decided.*

## The test and its negative result `[OBSERVED]`
Using the validated accelerator, one generation (milestone→milestone) was recorded as a **jump-trace** (sequence of
accelerated-sweep phases + counts) for ~15 generations, grouped by `G mod 3`. Uniformity would require, within a class,
**one** phase-signature (with counts affine in `G`). Result:
| `G mod 3` | generations | distinct phase-signatures |
|---|---|---|
| 0 | 4 | **4** |
| 1 | 8 | **8** |
| 2 | 3 | **3** |
**Every generation has a different phase-signature** — the closure is **not** uniform per residue class.

## Why `[OBSERVED, structural]`
The number of jump-phases per generation grows `~log_{4/3}(G)` (base-4/3 digit count `4,6,7,8,…,14` as `G`
grows `7→367`). The bouncer's sweeps process the **base-4/3 digit string** of `G`, whose length is `~log G` and whose
**carry cascade has unbounded length**. So the generation's macro-structure depends on the **digits of `G`**, not just
`G mod 3`. The two-counter `(G, a)` invariant cannot capture this — o4 needs a certificate over the **base-4/3
representation** (a digit string with variable-length carry), the AFS numeration object.

## Consequence — the verifier redesign `[honest]`
- **The turn-1/2 assets survive:** the bouncer architecture, the validated sound accelerator (`o4_accel_sound.py`), and
  the halt-free structural reduction (`B` never faces `11`, `B` reads `1` only in `1010…` sweeps).
- **The turn-3 uniform-closure plan is dead:** generation complexity is `~log G`, digit-string-dependent.
- **Two viable redirections (turn 4+):** (a) a **base-4/3 digit-string certificate** — prove the AFS odometer successor
  preserves the valid-representation regular language AND `11`-freeness (a property of the variable-length carry
  cascade); or (b) a **separate local halt-freeness invariant** — prove "`B` reading `1` ⟹ right cell `0`" via a
  bounded/closed set of local `B`-contexts, which alone forbids halting and may be tractable even though the *full*
  config invariant is non-regular. (b) is the more promising: halt-freeness is a **local** property, decoupled from the
  odometer's global complexity.

## Verdict
**(c) — honest negative: the uniform-per-residue closure fails; o4 needs a digit-string (or local-halt) certificate.**
o4's generation has `~log G` phases depending on the base-4/3 digits of `G`, so the two-counter model is insufficient.
The validated accelerator and halt-free reduction survive; the decision now points to a **local halt-freeness
invariant** (the promising redirection) or a base-4/3 digit-string certificate. **o4 is not decided.** **Halting
`[OPEN]`. No machine decided. No label upgraded.**

## Reproduce
- `/tmp/o4_t3b.py` (jump-trace per generation, all signatures distinct within each `G mod 3`); phase count `~log_{4/3}G`.
  Basis: `O4_VERIFIER_BUILD_T1/T2_2026-07-05`, `o4_accel_sound.py`, AFS rational-base numeration.
