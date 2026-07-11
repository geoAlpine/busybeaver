# The doubling-phase symbolic composition on the integer-×2 machine — the episode chain, the per-block lemma mechanized, and the exact remaining gap (2026-07-11)

*Continuation of `X2_CARRY_CALCULUS_2026-07-11.md`. Goal: close the doubling-phase
transport `M6(g) →* M1(g+1)` SYMBOLICALLY for arbitrary g (not just the machine-checked
g=2..6), mirroring the o4/o3 body-lemma composition discipline (`lean/Suffix.lean`,
`lean/O3.lean`). Interpreter `/Users/aokiyousuke/quantum-ecc/.venv/bin/python`; certified
symbolic executor `x2cc_symb.py` + prover `x2cc_faith.py`. Scripts `x2co_*.py`.
SOUNDNESS: `[PROVEN]` = machine-checked symbolic derivation; `[OBSERVED]` = exact
measurement. ZERO false proofs. Not committed.*

## 0. Verdict

**NO certified decision.** The doubling-phase episode chain is now extracted precisely
and shown UNIFORM across g (§1); its per-block inductive step is newly **mechanized as a
parametric lemma** (§2, `x2co_compose.py`: chew-fold ∀k,r and the full per-block cascade
step ∀k,r,s, both 0 gap≥3). But the composition does **not** close symbolically for
arbitrary g: three glue points remain open, and the deepest one is a genuine wall, not
engineering volume. Concretely (§3):

* **G1 — the cascade FOLD.** The per-block step must be composed over the cascade's
  `K−2 = g+6` blocks, whose lengths `2^j−3` are all DIFFERENT. This is an induction over
  a variable-length list of non-uniform blocks. The `x2cc` executor represents a
  configuration as a FIXED-length list of runs with AFFINE counts; it can represent
  neither a symbolic block count nor an exponential block length. The prover's loop
  acceleration needs a uniform `config(p)→config(p−1)` shift, which provably does **not**
  exist across the cascade (block sizes 61,29,13,5,1,… — `x2co_fold.py`). So the fold is
  not expressible in the available tool.
* **G2 — the boundary/repack episodes** (entry M6→first-block, the `10^10`-marked
  big-block R/L sweep, the comb repack) are demonstrated per-g only (g=2..6), not proven
  as parametric lemmas.
* **G3 — the register-rebuild + doubling arithmetic.** Reconstructing the exact `M1(g+1)`
  template requires equating the accumulated comb-total (≈ `2^K`) to the next big block
  `2^(K+1)−3` and re-writing `U^g` + the parity tail. This couples the exponential
  high-part value to the transport — precisely the task-flagged "register-rebuild couples
  to the high part" failure mode, and it is unrepresentable in the affine executor.

The prior session's optimistic framing ("what remains is engineering volume, not a
conceptual wall") is **corrected**: G1 and G3 are conceptual/representational walls in
the current infrastructure. The honest open core is now sharply located.

## 1. The T7 episode chain (extracted, uniform across g) `[OBSERVED exact g=2..6; structure identical]`

From `x2co_episodes.py`/`x2co_trace.py` (executor traces of `M6(g)→M1(g+1)`; g=3 and g=4
compared cell-for-cell, differing only in the register count `1111100^{g±?}` and the
block values): the doubling phase is, in order,

1. **ENTRY** (fixed, bounded): `M6(g) = (10)^4 1^9 0^2 (1^5 0^2)^j C · 1^big · casc`
   → a short `1^9` chew, then hand-off into the register.
2. **REGISTER CHEW** (uniform fold over `(1^5 0^2)^j`): each register unit is one C1
   chew-body (`1^5→1^3`) + one C2 separator-crossing. All units EQUAL length → this is a
   uniform loop (accelerable in principle).
3. **BIG-BLOCK SWEEP** (`10^10`-marked R/L loop): `[D] 0^3 (10)^10 1^(2v+1) 0^2 · tail`,
   `v→v−1` per 8-op R/L cycle, left comb `(10)^k` accumulating, tail untouched. Runs
   ≈ big/2 times (~2^(K−1)). A uniform single-parameter loop, distinct from the C1/C2
   chew.
4. **CASCADE FOLD** (`g+6` non-uniform blocks): for each cascade block `1^(2^j−3)`, a
   C1 chew-fold down to `1^3` then a C2 separator-crossing into the next block. The
   marker is *not* present here — cascade blocks are plain `[D] 0^3 1^(2v+1) 0^2`
   (`x2co_cross.py`). This is exactly C1/C2 (`x2cc_prove.py` obligations 3,4).
5. **REPACK**: the accumulated comb `(01)^K` is R-cycled (`try_R_cycle`, `E@(01)^n→1^2n`)
   into the new big block — the ×2.
6. **REGISTER-REBUILD**: `U^g` and the parity tail are re-written, yielding `M1(g+1)`.

Safety: the executor's halt-gate (E meets gap-3) never fires anywhere in the doubling
phase; the phase emits ONLY gaps of length 1 and 2 (`[OBSERVED exact g=2..6]`,
`x2cc_gencheck.py`; the ≥3 gaps {6,10,18} all live in the PROVEN low phase). So
doubling-phase safety-through-composition = the transport completes, i.e. every episode
lemma closes and the glue holds.

## 2. The per-block lemma — mechanized `[PROVEN ∀ parameters]`

`x2co_compose.py` closes, in the certified prover (raw TM + certified R/L/D closed forms
+ exhaustive splits + certified loop induction):

* **L0 — within-block chew fold** (uniform in `r`):
  `(01)^(k+1) [D] 0^3 1^(2r+5) 0^2 T →* (01)^(k+r+2) [D] 0^3 1^3 0^2 T`, for ALL `k,r`,
  with `T` an opaque tail never read; **0 gap events**, by certified loop induction
  (`INV(r+1,J)→*INV(r,J+1)`). `[PROVEN]`
* **L1 — full per-block cascade step** (chew-fold ⋯ then C2 separator-cross):
  `(01)^(k+1) [D] 0^3 1^(2r+5) 0^2 1^(2s+5) 0^2 T →* (01)^(k+r+4) 0^2 1 [D] 0^3 1^(2s+3) 0^2 T`,
  for ALL `k,r,s`, `T` opaque; **0 gap≥3**. `[PROVEN]`

L1 is EXACTLY the inductive step of the cascade fold: its postcondition (state D at
`0^3 1^(2s+3) 0^2`, comb grown, tail intact) matches the precondition of the next
per-block step with the next block as the new current block. The glue between consecutive
blocks is therefore proven — the missing piece is the FOLD that iterates it.

## 3. Why the composition does not close — the exact gaps

**G1 (cascade fold).** L1 is proven for one block with an *opaque* tail. To conclude for
the whole cascade one needs `cascade_cross([L_1,…,L_m])` by induction on `m`, `L_i=2^{i}−3`
distinct — the o4/o3 analogue is `prefix_bodies`/`body_iter`, but those were mechanized in
**Lean** over `List Nat`. In `x2cc_symb`, a `Config` is a fixed-length list of `(pattern,
affine-count)` runs: it can hold neither a symbolic number of runs (`m` symbolic) nor an
exponential count (`2^j−3`). And the prover's only inductive engine — d=1 loop
acceleration — requires a uniform `config(p)→config(p−1)` shift; `x2co_fold.py`
demonstrates that across the cascade the block-entry lengths are `61,29,13,5,1` (all
distinct), so no such shift exists. Hence the fold is **not expressible** in the current
tool. (It IS a standard list induction whose STEP (L1) is machine-proven; closing it needs
either a Lean port of the x2 machine or a `Config` generalization to variable-length
symbolic run-lists. Neither exists.)

**G2 (boundary/repack).** The ENTRY, the `10^10`-marked BIG-BLOCK sweep, and the REPACK
are bounded/uniform episodes of the same provable kind, but are here only machine-checked
per-g (g=2..6, `x2cc_gencheck.py`), not lifted to parametric lemmas. The big-block sweep
in particular is a *distinct* loop from C1/C2 (it carries the `(10)^10` marker) and was not
proven parametrically this session.

**G3 (register-rebuild + doubling arithmetic) — the deepest wall.** `M1(g+1)` has big
block `2^(K+1)−3` and `U^g` register with parity tail. The repack turns the comb of total
length `K_total = Σ_i (per-block comb contributions)` into `1^(2·K_total)`; for the result
to equal the template one must PROVE `2·K_total + (rebuild corrections) = 2^(K+1)−3` — an
identity between the accumulated cascade-fold output and the exponential high part. This
couples the register rebuild to the exponential value `2^K` (the "high part"), which the
affine executor cannot represent, so the reconstruction cannot be verified symbolically —
only per-g. This realizes exactly the failure mode the task flagged.

## 4. Cross-checks

* `x2cc_prove.py`: 4/4 obligations (low-phase ∀g both parities; C1 ∀k,r; C2 ∀k,s) — re-run
  green.
* `x2cc_gencheck.py 2 6`: `M1(g+1)` template EXACT and gap ledger exact for g=2..6.
* `x2co_compose.py`: L0, L1 PROVEN (0 gap≥3), certified loop induction.
* `x2co_fold.py`: register fold uniform (loop detected); cascade fold non-uniform
  (distinct block sizes) — no uniform shift.
* Accelerated simulator halt-free to `8·10^11` (`x2cc_fast`, step-exact to `10^8`),
  carried from the prior session; not re-extended (a decision was not reached).

## 5. Soundness ledger

* Episode chain, uniform across g: `[OBSERVED exact g=2..6; structure identical g=3,4]`.
* L0 chew-fold ∀k,r; L1 per-block step ∀k,r,s: `[PROVEN, certified loop induction, 0 gap≥3]`.
* Low phase ∀g; C1 ∀k,r; C2 ∀k,s: `[PROVEN]` (prior, re-verified).
* Doubling full transport g=2..6: `[MACHINE-CHECKED exact per generation]`.
* Cascade fold over g+6 non-uniform blocks: **OPEN** (G1, tool-representational wall).
* Big-block marked sweep / entry / repack as parametric lemmas: **OPEN** (G2, per-g only).
* Register-rebuild + doubling reconstruction of M1(g+1): **OPEN** (G3, couples to 2^K).

**No machine decided. No label upgraded.** The advance is: the doubling episode chain is
precisely mapped and its per-block inductive step mechanized; the residual open core is now
three sharply-stated glue points, of which G1 and G3 are representational walls requiring a
Lean-style formalization (as the o4/o3 folds required), not further executor runs.
