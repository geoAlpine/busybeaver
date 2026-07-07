# Does o4's GROWING budget escape the Antihydra no-go corpus? — route-viability assessment (2026-07-07)

*EVALUATE-BEFORE-EXECUTING pass (discipline mode A). Question: Antihydra's kernel needs a CONSTANT-threshold
one-sided density bound (even-density ≥ 1/3, zero margin); o4's ledger fails only if drain events exceed a
LINEARLY-GROWING budget (`a_n ≈ 3n`). Does the constant→growing change flip any of the proven no-gos? This is an
assessment, not a proof attempt. Labels strictly `[PROVEN]`/`[ASSESSED]`/`[OPEN]`. Numerics: sanity pass verified
inline (3000 generations exact; interpreter `/Users/aokiyousuke/quantum-ecc/.venv/bin/python`). NOT committed.*

---

## 0. One-line verdict

**No route is OPENED to a decision. Exactly ONE verdict genuinely flips under the growing budget — the
single-event/magnitude-cap comparison — and it is already banked as `[PROVEN]` (`O4_RUN_STRUCTURE_2026-07-07.md`
§2). Every structural register stays closed because the no-gos are THRESHOLD-UNIFORM: they are driven by the
existence of violating adversary orbits, which exist for every density threshold < 1 (the proven fixed point
`δ₋₁₄` has drain-density 1; the proven bijection realizes every finite pattern). What the growing budget does
change is the STRENGTH of the missing tool: from "exact-constant zero-margin quenched density" (Antihydra) to
"any effective quenched density bound below 4/5" (o4) — a strictly weaker ask in the convergent/BC-I class
(`NEW_MATH_PROGRAM.md` §8.6), same species, same wall.**

---

## 1. The exact accounting `[PROVEN, trivial algebra + verified exact 3000 gens]`

With `W_n = G_n+14`, ledger `a' = a + δ(ρ)`, `δ = {1:−1, 2:+4, 0:+6}` (`O4_LEDGER_ANALYSIS_2026-07-06.md` §1):

- **Identity:** `a_n = a₀ − #1 + 4·#2 + 6·#0` (verified exact every generation, n ≤ 3000).
- **Fatality ⟺ a level-1 density event:** `a_n ≤ 1` ⟺ `#1 − 4·#2 − 6·#0 ≥ a₀ − 1`. Since `n = #1+#2+#0`, the
  cheapest adversary (all filler ρ=2) needs **prefix density `#1/n ≥ 4/5`** (all-ρ0 filler: 6/7). And
  `#1 = #{j: 3 | W_j}` — a **level-1 cylinder frequency**, the exact mirror of Antihydra's level-1
  `freq(c_n even) ≥ 1/3`. The thresholds differ (1/3 zero-margin vs 4/5 with slack; observed freq = 0.3227),
  the species does not.
- **The free first moment (the `ΣK ≤ N` analogue) EXISTS:** the run theorem gives the exact telescope
  `Σ_{run entries} v₃(W_entry) = #{ρ=1 steps} + (v₃ boundary)`. Verified: refill-sum = 968 = #1 exactly at
  n = 3000 (boundary 0). But this identity is **the same object on both sides** (run-depth sum ≡ drain count) —
  the o4 transposition of `EK2_SECOND_BUDGET.md`'s `0=0` shape, now already at FIRST order. Its only content is
  the trivial cap `#1 ≤ n`.
- **What fatality needs vs what is free:** needed `#1 ≥ (4n + a₀−1)/5`; free `#1 ≤ n`. The gap is a **density
  CONSTANT (1 vs 4/5) at first-moment order** — not a moment-degree upgrade. The literal second-moment analogue
  `Σ_{j≤n} v₃(W_j) = Σ_runs K(K+1)/2` is NOT needed for o4 (unconditional cap: only the quadratic
  `Σ log₃W_j ≈ 0.131n²`, and it is irrelevant).

---

## 2. Route 1 — Borel–Cantelli / first-moment counting: **still closed** (sharpened, not opened)

- The Antihydra closure reason ("recurrence ≠ frequency", `EK2_TAIL_SEPARATION.md`) transposes intact: the free
  count `#1 ≤ n` cannot be narrowed to `#1 ≤ (4/5)n` by ANY unconditional counting — improving a density constant
  on a specific orbit IS the quenched-frequency species. Min-gap/separation dies identically: ρ=1 visits arrive in
  contiguous runs (countdown `v₃ ↦ v₃−1`, ×4/3 exact), min index-gap = 1, covering bounds trivial — the same wall
  as `EK2_TAIL_SEPARATION.md` §0. `[ASSESSED — mechanism transposes verbatim]`
- **What DOES change:** the annealed conspiracy probability at scale n is `~η^{a_n} = η^{3n+O(1)}`
  (η = 0.334895, `O4_LEDGER_ANALYSIS` §3), and `Σ_n η^{3n} < ∞` (≈3×10⁻¹⁰ from the frontier) — vs Antihydra's
  divergent `Σ_n 2^{−k} = ∞` at fixed level. **The growing budget moves o4 from the divergent (K)-grade class
  into the convergent-target BC-I class** — per `NEW_MATH_PROGRAM.md` §8.6 a *strictly weaker hypothesis* than
  (K), but "blocked by the identical annealed→quenched wall": BC-I needs a measure, the orbit is one point, and
  the needed unconditional surrogate `P[deep return at j] ≲ 3^{−ℓ}` is precisely the open return-frequency bound
  (`O4_RUN_STRUCTURE` §4). **Verdict: still closed; the lever is real but it is the same missing tool at weaker
  required strength — not an escape.**

## 3. Route 2 — the excursion-supermartingale no-go: **still closed** (the closure point MOVES)

- For Antihydra the route died at the second-moment wall (every potential's drift linear in K; `K²` potentials
  telescope to `0=0`; `EXCURSION_SYNTHESIS.md` §1). For o4 the fatality functional is itself LINEAR in K, so that
  wall is moot — the route instead dies **one register earlier, at the coboundary/LP wall**: certifying
  `density(ρ=1) ≤ 4/5 − ε` is a bounded sub-action for `ψ_o4 = 1{ρ=1} − 4·1{ρ=2} − 6·1{ρ=0}`, and the ρ=1 branch
  has the **`[PROVEN]` integer fixed point x₁ = −14** (`O4_RUN_STRUCTURE` §1): `δ₋₁₄` is an invariant measure with
  `∫ψ_o4 = +1 > 0`, a positive-mean self-loop at the residue of −14 mod 3^k at EVERY level — the exact o4 image
  of Antihydra's `δ₁` obstruction (`MINPROP_COBOUNDARY_LP.md` via `BB6_NO_STRUCTURE_THEOREM.md` §3(1)).
  `[ASSESSED — fixed point PROVEN; the LP-duality kill is the proven MINPROP mechanism, not yet machine-run on
  o4's residue graph]`
- **The adversary question (does growing budget + run cap kill it?): NO.** The run cap (`run ≤ 0.262n`,
  `[PROVEN]`) kills only adversaries needing a SINGLE over-cap run. The surviving adversary is a **density-burst**
  adversary: one fatal prefix built from MANY SHALLOW runs (depth 1–2 at ~4/5 of positions — no individual run
  near the cap), then annealed-typical forever (Cesàro frequency → 1/3, first-moment matched). By the `[PROVEN]`
  bijection (`O4_LEDGER_ANALYSIS` §2) every such finite pattern is realized by an explicit seed class mod 3^n —
  indeed "fatal orbits exist for every a₀" is already `[PROVEN]` there. This adversary satisfies every proven fact
  (run cap, telescope, all residue-finite data) and is drift-indistinguishable from the real orbit for every
  candidate potential. **The growing budget forces the adversary to conspire over a positive FRACTION of the
  prefix instead of one deep event — but nothing proven excludes that, and the bijection realizes it.**

## 4. Route 3 — bijection obstruction / prefix-finite magnitude: **the one genuine flip, already banked**

- **The flip `[PROVEN, banked]`:** the archimedean smallness of the specific orbit (`W_n` a specific integer
  ≈ 57·(4/3)ⁿ) gives `v₃(W_n) ≤ log₃W_n ≈ 0.262n`, and `0.262n ≪` budget `≈ 3n` ⟹ **single-run fatality is
  impossible** past a concretely-verified horizon (`O4_RUN_STRUCTURE` §2). In Antihydra the SAME comparison
  fails: the budget there (the balance) has **no unconditional positive slope** — its positivity IS the open
  statement — so the banked cap `K ≤ 0.585n` excludes nothing (`EK2_PARTIAL_MOMENTS.md` §0,
  `NEW_MATH_PROGRAM.md` §8.3: a deep value is a near-halt). **This is exactly where "constant → growing" flips a
  verdict — and it is the content already extracted in O4_RUN_STRUCTURE, not new headroom.**
- **What remains beyond the banked cap: nothing unconditional.** Fatality at time n is a union of explicit seed
  classes mod 3ⁿ (bijection); deciding whether 43 lies in them for ALL n is running the machine — verification,
  not a theorem. "G_n is a specific integer of size (4/3)ⁿ ≪ 3^{3n}" adds nothing: smallness reads ONE
  generation's depth (the banked cap), while fatality is a FREQUENCY across j ≤ n; summed, the magnitude gives
  only `Σ v₃(W_j) ≤ 0.131n²` — quadratically too weak against a linear-density requirement, and predicting
  `W_n mod 3^{3n}` in closed form is the equidistribution of `4ⁿ`-weighted digit sums = the wall itself.
  `[ASSESSED]`

## 5. Route 4 — the rest of the corpus: **threshold-uniformly closed**

The meta-point that settles all remaining registers: **(C1)/(C2)/(C3) of `BB6_NO_STRUCTURE_THEOREM.md` are
adversary-existence arguments, and the violating set is nonempty for EVERY threshold < 1** — `δ₋₁₄` realizes
drain-density 1, and the bijection (o4's specification analogue) realizes every intermediate density on a seed
class. A growing budget only moves the threshold (1/3 zero-margin → 4/5 with slack); no threshold below 1 is
reachable structurally. Consequently `[ASSESSED]`:
- **(C2)/(C3):** fatal seeds exist for every a₀ (`[PROVEN]`, `O4_LEDGER_ANALYSIS` §2) — no all-orbits certificate;
  the annealed verdict is now even stronger (summable ruin) but remains measure-level, and the orbit is one
  μ-null point.
- **Adelic/magnitude-aware sub-actions:** the per-step adelic increment is depth-independent (each branch is
  ×4/3 + O(1) archimedean), so it charges only the free count — the clustering-indifference of
  `EXCURSION_SYNTHESIS.md` §1 transposes; the threshold/conditional escape fails because `v₃(W)` is unbounded at
  arbitrarily large W inside the −14 residue classes (mirror of `D` unbounded at large `o`,
  `BB6_NO_STRUCTURE_THEOREM.md` §4-update).
- **EK2-style moment identities:** moot in the strong sense — o4 does not even need a second moment (§1); the
  needed first-moment-constant improvement self-closes as `refill-sum ≡ drain-count` (`0=0` at first order).

---

## 6. The route-viability map

| route | Antihydra verdict | o4 (growing budget) verdict |
|---|---|---|
| single-event / magnitude cap | NOT excluded (cap 0.585n vs no proven budget slope) | **FLIPPED: excluded `[PROVEN, banked]`** (0.262n ≪ 3n) |
| BC-I / first-moment counting | closed (divergent, recurrence≠frequency) | **still closed**; now convergent-class (weaker ask), same annealed→quenched wall |
| excursion supermartingale | closed at 2nd-moment tautology | **still closed**, at the earlier coboundary/LP wall (`δ₋₁₄`, ∫ψ_o4 = +1) |
| heavy-tail adversary | survives (first-moment matched) | **survives as density-burst adversary** (shallow multi-run, bijection-realized) |
| bijection / prefix-finite | — | **still closed** beyond the banked cap (frequency ≠ one-generation smallness) |
| (C1)/(C2)/(C3) structural | closed (δ₁, specification, a.e.) | **still closed, threshold-uniformly** (δ₋₁₄, bijection, a.e.) |

**Minimal deciding statement (the sharpened `[OPEN]` core, unchanged in species):** an effective quenched bound
`freq_{j≤n}{3 | G_j+14} ≤ 4/5 − ε` (weighted form: every prefix `#1 − 4#2 − 6#0 ≤ a₀ − 2`) for the specific
seed — any effective rate suffices (convergent class), vs Antihydra's exact-constant zero-margin form. Margin is
invisible to every closed register; it is usable only by a tool that reads the seed's arithmetic — the
`NEW_MATH_PROGRAM.md` §3 spec verbatim, at its easiest instance (the margin-ladder staging claim, confirmed).

**Housekeeping candidate for a later pass (not a decision lever, do NOT attempt here):** machine-run the
coboundary LP on o4's residue graphs mod 3^k (expected infeasible via the −14 self-loop at every level), which
would upgrade §3's `[ASSESSED]` transposition to `[PROVEN]` and complete the o4 No-Structure mirror.

**No machine decided. No label upgraded.**
