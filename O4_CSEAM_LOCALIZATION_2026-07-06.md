# o4 C-seam closed per-event (forced 14-cell template, k-uniform); cap crossing proven seam-free; the task premise "C-seams at the cap" CORRECTED; residual = arrival completeness (2026-07-06)

*Attacking the residual [OPEN] C-seam of the seam-parity lemma. **Two results: (i) a CORRECTION — the
C-seams are NOT at the right-end `1001` cap** (the prior census label `CAP` merely meant "not gap-edge");
they are **sweep-end events at the phase boundary inside the filler**, hundreds of cells from both the gap
and the cap; **(ii) every recurring C-seam event is PROVEN safe by a forced 14-cell bounded template**,
k-uniformly (locality lemma), validated step-for-step against the real machine; the cap crossing is PROVEN
k-uniform and contains **no seams at all**. The residual shrinks to ARRIVAL COMPLETENESS — which inherits
the counter-dependent wall. o4 `[OPEN]` — not decided. No machine decided.*

## The correction `[OBSERVED, 3×10⁸ exact steps, G≈24,644]`
`o4_cap_census.py`: 28 C-seams; `rel = q − rmax` grows linearly negative (−20 … −176): the C-seam is
**not** cap-local. It occurs at the **phase boundary** between the `(01)`-phase left filler and the
`(10)`-phase right filler (the previous leftward `D1E0` invert-sweep's turn-around point), with the gap
and the cap both hundreds of cells away. The prior memo's "all C-seams at the `1001` cap" traced to the
old census key `'GAP-EDGE' if (5 zeros left) else 'CAP'` — a mislabel. Everything PROVEN in the prior
memos (E-seam chain, decomposition, q+2-last-writer D) stands; only the *location gloss* was wrong.

## What a C-seam actually is `[PROVEN from the table + forced simulation]`
Every C-seam is the tail of a **sweep-end event**: the rightward `B1F0` sweep reads a `0` where the
alternation phase breaks (`B`-reads-`0`), then the continuation is FORCED by the local window:
`B:0→1RC · C:1→0RA · A:0` (template T1, seam at `x+2`) or the doubled `(B·C·A)²` (template T2, seam at
`x+5`), where `x` is the `B`-read-`0` cell. In both recurring templates the window itself contains
`tape[q+2]=0` — **the safety is decided by the 14 cells `x..x+13` alone**.

## PROVEN this session (all assertion-checked, `o4_cap_kuniform.py`, `o4_cap_macro_saturation.py`)
1. **Forced-prefix safety.** For **every** sweep-end window type observed (radius 10, saturated set),
   simulating on the window cells only: every recurring type's C-seam is forced with `q+2 = 0` read off
   the window, and every `B`-read-`1` inside has right-neighbour `0` — except, per type, the LAST
   `B`-read before the exit, whose neighbour sits at the analysis-window edge (unknown to the pure
   window analysis; resolved `0`/safe by the padded runs of item 2 for all k). One startup SINGLETON
   (`('A','000000000101000000101')`, step 221, once ever) has its seam `q+2` outside the window —
   verified safe concretely in the real run (census assertion, UNSAFE=0). `[PROVEN conditional on the window]`
2. **k-uniformity + locality.** Embedding each recurring C-seam window in period-2 padding of depth
   k = 4..12: the evolutions are **IDENTICAL** for all k, head confined to `[x, x+13]`, seam safe, exit
   rightward at `x+13` in `B1F0` sweep mode (proven read-only mode). **Locality lemma** (induction on
   steps: the read cell stays inside W): if two configs agree on W and the head never leaves W during
   0..T in one, the evolutions agree on 0..T. Hence the event is the same for **ALL k ≥ 4** — the C-seam
   event NEVER depends on the odometer once its 14-cell right context is fixed. `[PROVEN]`
3. **Real-trace identity.** Every real instance of the three recurring C-seam sweep-end types
   (T1 via `('F','…01·0101010…')` 18×; T2 via `('F','…01·0010101…')` 8×, whose second stage is the nested
   `('A','(01)^10 0')` 8×; counts consistent: 18+8 = 26 = all post-startup C-seams at G≈24,644) matches
   the standalone padded event **step-for-step**. Startup one-offs (2 seams, G∈{5,8}) verified safe
   concretely in the exhaustive run. `[PROVEN identity, OBSERVED census]`
4. **The cap crossing is seam-free and k-uniform.** The right cap has exactly ONE recurring arrival type
   — `(F, rmax−12, (01)-phase filler · 1001 · 0³)`, saturated at step **157** and frozen through
   G = 883,719-scale runs. The standalone cap event: 35 steps, span `[rmax−17, rmax+3]`, **no C-seams,
   no E-seams**, all 5 `B`-reads-`1` safe, cap extends `rmax → rmax+3` with phase flip, exit leftward in
   the proven `D1E0` invert-sweep; identical for k = 4..12 ⇒ all k ≥ 4 (locality); real-trace identity on
   all instances. `[PROVEN]` (Two crossings per generation ⇒ filler +6/generation — matches census.)
5. **Type-set saturation to G ≈ 10⁵–10⁶** (`o4_cap_macro_saturation.py`, hooked into the VALIDATED
   bouncer macro; hook soundness PROVEN: no p=2 cycle of the table contains a `B`-read-`0` — exhaustively
   checked — and no verified jump can land inside the cap region — runtime-asserted, 0 violations;
   V-check: macro type-sets AND per-type counts exactly equal concrete over 5×10⁶ steps):
   at **G = 883,719** (5.003×10¹¹ steps, 40 milestones; and at the intermediate G = 88,462 run):
   sweep-end types **frozen at 44** (radius 10) since step **4,048**; cap-arrival types **frozen at 4**
   (1 recurring + 3 startup one-offs) since step **157**; unsafe = 0, F-reads-1 = 0,
   jump-crossing violations = 0. `[OBSERVED, saturated over ~36 generations]`

## The honest residual: ARRIVAL COMPLETENESS `[OPEN — the wall, sharply restated]`
What remains is exactly: **for every G, every `B`-read-`0` window is in the saturated 44-set and every
cap arrival is the single F-type** — equivalently, the filler stays 2-periodic with only the enumerated
bounded defects at every crossing. Can it be forced from the proven sweep lemmas + milestone induction?
**No — it inherits the counter-dependent wall.** The forced-prefix exits hand off to sweeps that run into
the LEFT zone (gap edge / odometer reset), whose branch structure is the base-4/3 counter (turn-4 `0/25`;
AFS non-regularity). Concretely: the T1/T2 template *selection* sequence per generation (T2 at generations
3,7,13,16,19,22,24,26,…) is odometer data — irrelevant to safety (both templates PROVEN safe) but proof
that the completeness statement is not a finite/periodic fact. The wall now sits ENTIRELY on the left
(odometer-reset) side: the filler/cap side is proven uniform; what is unproven is that the left zone never
emits a disturbance that reaches a crossing with a window outside the saturated set.

## Small-a caveat (interface to the template-closure / a-ledger work)
The cap-crossing proof (item 4) is conditional on the recorded arrival window: **13 filler cells left of
the cap** must be clean alternation, i.e. it applies only when the filler holds ≥ 7 `(10)`-pairs
(**a ≥ 7**). For small `a` the arrival window is different by construction and NOT covered — consistent
with (and independent corroboration of) the main loop's finding that small-`a` behaviour at the cap is
where the danger lives (Z(k=41, g=3, a=0) halts). `[honest scope]`

## Verdict
**(b) — k-uniform per-arrival safety PROVEN; arrival completeness [OPEN].** Sharper than expected on two
axes: the C-seam event needed **no k at all** (it is decided by 14 fixed cells — pure forced locality,
zero odometer dependence), and the cap is seam-free (premise corrected). o4's decision now = ONE
statement: *the saturated window/type sets are complete for all G* — a base-4/3-odometer (Collatz-type)
invariant, with every LOCAL link in the chain proven. **o4 not decided.** Halting `[OPEN]`.
No machine decided. No label upgraded.

## Reproduce
- `o4_cap_census.py` (3×10⁸ exact steps: 28 C-seams — 2 recurring templates + 2 startup; sweep-end types
  34@r8 frozen since step 1,160; cap arrivals 4 frozen since 157; UNSAFE=0).
- `o4_cap_kuniform.py` (forced-prefix per type; padded k=4..12 identity; real-trace match on all
  recurring instances; cap event seam-free; assertions PASS).
- `o4_cap_macro_saturation.py` (p=2-cycle exhaustion; V-check exact vs concrete; G≈10⁵–10⁶ frozen sets).
- Basis: `O4_SEAM_PARITY_LEMMA_2026-07-06.md` (E-seam chain PROVEN — unchanged),
  `O4_WINDOW_SATURATION_2026-07-06.md`, `o4_bouncer_macro.py` (validated macro).
