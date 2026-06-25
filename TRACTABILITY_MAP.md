# Tractability map: why the cousins of Antihydra are solvable and 3/2 is not (2026-06-26)
*A change of tactic (the new programme): instead of re-attacking seed 8 (every direct angle is the wall), map the
**tractable cousin models** where single-orbit equidistribution IS provable, identify the **specific structure**
each uses, and pin **exactly what `3/2` lacks** — so the multi-year tool has a precise target: supply a substitute
for one of those structures. All facts machine-verified (`tractability_map.py`).*

## The three tractable cousins and their structures
| cousin model | orbit behaviour | **why it is provable** (the structure) | status |
|---|---|---|---|
| **Odometer** `x ↦ x+1` on `ℤ_p` (≈ o17's base object) | every digit equidistributes | **unique ergodicity** — the only invariant measure is Haar, so *every* orbit equidistributes, for free | classical |
| **Linear** `{nα}` (`α` irrational) | equidistributes (Weyl) | **linearity** — van der Corput differencing drops the degree to 0; the exponential sum `Σe(nα)` is a geometric series | Weyl 1916 |
| **Pisot** `{β^n}` (`β` Pisot, e.g. `φ`) | `→ 0/1` (structured) | **archimedean conjugate decay** — `β^n + (conjugates)^n = trace ∈ ℤ`, conjugates `|·|<1` so `β^n` is archimedean-close to an integer | classical |

Verified: `{φ^n} → 1` with gap `|ψ^n| = 0.0081, 5e−7, 3e−13, 1e−21` for `n=10,30,60,100` (`ψ=−0.618`); `{(3/2)^n}`
stays generic (`0.665, 0.059, 0.933, 0.397`), no decay.

## What `3/2` lacks — all three (verified)
- **No unique ergodicity.** The induced map `F` on `ℤ_2` is full-branch expanding with a **continuum of invariant
  measures** (every Bernoulli measure on the branch-coding; §A2/Q9b). So "every orbit equidistributes" is false —
  seed 8 must be pinned individually.
- **No linearity.** `(3/2)^n` is exponential; **van der Corput is closed** (verified, `vdc_closed.py`):
  differencing returns `t'(3/2)^n`, the same family, no degree drop.
- **No archimedean conjugate decay.** `3/2` is rational with **no archimedean conjugate `<1`**; `(3/2)^n` is *not*
  archimedean-close to any integer (verified: distance-to-nearest-integer `= 0.33, 0.059, 0.067` for `n=10,30,60`,
  generic, not `→0`).

## The adelic-Pisot probe — the most promising substitute, and where it stops
`3/2` *does* have a contracting "conjugate", but at a **non-archimedean place**: `|3/2|_3 = 1/3`, so
`|(3/2)^n|_3 = 3^{−n} → 0` — a genuine 3-adic contraction, structurally like a Pisot conjugate (this is the
`2↔3` duality, Prop 3, in adelic dress; product formula `|3/2|_2·|3/2|_3·|3/2|_∞ = 2·⅓·1.5 = 1`).
- **Naive form fails (verified):** 3-adic smallness does *not* imply archimedean closeness-to-an-integer — they are
  different topologies — so the Pisot mechanism (`{β^n}→0`) does **not** transfer.
- **Sophisticated form = the real target, and the wall:** the right framing is **equidistribution on an
  `S`-arithmetic homogeneous space** (`ℝ × ℚ_3`, or the adele class group), where the prime `3` supplies a
  *contracting direction* and `2`,`∞` *expanding* ones — the natural home for a Pisot-type argument across places.
  But the acting element is `(3/2)` generating a **rank-1** (cyclic) group, and rank-1 diagonal actions have **no
  Ratner/measure rigidity** — the same single-orbit wall, now in `S`-arithmetic clothing.

## Route 3 — resolved [the cleanest dynamical home for the wall] (2026-06-26, `route3_adelic.py`)
Attacking the adelic route concretely **corrects the earlier "Pisot/wrong-place" framing** to a sharper, more
positive one:
- **`×(3/2)` is a HYPERBOLIC automorphism of the S-arithmetic solenoid** `X = (ℝ×ℚ_2×ℚ_3)/ℤ[1/6]` (`3/2∈ℤ[1/6]^*`
  so it descends to an automorphism). Dilations: `|3/2|_∞=3/2` and `|3/2|_2=2` **expanding**, `|3/2|_3=1/3`
  **contracting** (the *stable manifold*). No neutral direction ⇒ **hyperbolic** (product formula `3/2·2·⅓=1`,
  verified). **The 3-adic contraction is not "at the wrong place" — it is the stable direction that makes the
  system hyperbolic**, exactly the structure the cousins exploit.
- **[PROVABLE, a.e.]** hyperbolic ⇒ ergodic + mixing ⇒ **`a.e.` orbit equidistributes** (Birkhoff; the
  `S`-arithmetic analogue of a hyperbolic toral automorphism / Cat map). So equidistribution is *rigorously true
  for almost every seed* — the contraction delivers this.
- **[WALL]** seed 8 is the orbit of the *single specified* point `1` (resp. `8`); a **single orbit** of a
  hyperbolic automorphism need not equidistribute (periodic points don't). This is the **a.e.→specific** wall
  again — now in its **cleanest dynamical form**: *single-orbit equidistribution of a hyperbolic `S`-arithmetic
  automorphism.*
- **Why Pisot was the wrong analog:** `ℚ` has no Galois conjugates, so there is no "trace `∈ℤ`" making `(3/2)^n`
  close to an integer (the product formula gives a *product* `=1`, not a sum). The correct mechanism is
  **hyperbolic mixing**, which gives `a.e.`, not the single orbit.
- **The named target:** this places Antihydra in **homogeneous dynamics** — the home of Einsiedler–Lindenstrauss
  measure rigidity. Their rigidity is for **rank ≥ 2** actions (`⟨×2,×3⟩`); our action is the **rank-1** cyclic
  `⟨×(3/2)⟩`, with no rigidity — so the open frontier is precisely **rank-1 single-orbit equidistribution on a
  hyperbolic `S`-arithmetic solenoid.** A genuine, named, well-populated battlefield (not "solve Mahler"), with
  the rank-1 gap as the explicit obstruction.

## Literature anchor for Route 3 (2026-06-26 triage, homogeneous dynamics) — the frontier coincides with our wall
A focused homogeneous-dynamics consultation **independently confirms the Route 3 placement and the rank-1 gap**:
- **Closest result — Koksma (1935):** for Lebesgue-a.e. `θ>1`, `{θ^n}` equidistributes mod 1. *Right shape (our
  map, our orbit) but `a.e.`* — says nothing about the named `θ=3/2`.
- **Single-orbit on the torus exists only at rank ≥ 2:** Bourgain–Furman–Lindenstrauss–Mozes (JAMS 2011) get
  individual-orbit equidistribution, but require a **non-abelian / large semigroup**, not a cyclic `⟨A⟩`.
- **Rank-1 has no rigidity (explicit):** Einsiedler–Lindenstrauss (JMD 2008) — a single diagonalizable/hyperbolic
  element has a rich family of invariant measures and **invariant Cantor sets**; Furstenberg/Rudolph/Lindenstrauss
  rigidity needs multiplicatively-independent `p,q` (rank 2).
- **Effective equidistribution (Lindenstrauss–Mohammadi 2022, arXiv:2202.11815, and successors):** for
  **unipotent / higher-rank** orbits only — none covers a single cyclic hyperbolic orbit.
- **Verdict (the field's own frontier):** **homogeneous dynamics currently offers NO single-orbit (non-`a.e.`)
  tool for a rank-1 hyperbolic action.** Every positive single-orbit theorem needs rank ≥ 2, a non-elementary
  acting group, or unipotent structure. The exact gap — *remove "almost every" to reach the named cyclic orbit of
  `×(3/2)`* — **is** the open Mahler-3/2 / Antihydra problem. So Route 3 does not breach the wall, but it places
  it on the **most-developed equidistribution battlefield**, with the obstruction named precisely
  (`rank-1 single-orbit`) and anchored to specific theorems and their precise deficiency.

## The deliverable: what the new tool must supply
The new single-orbit tool for `3/2` must provide a **substitute for one of the three tractability structures**:
1. a **rank-1 unique-ergodicity-type input** that pins one specified orbit (the dynamical face, A1/Q1); or
2. a **degree-reduction beyond van der Corput** for the exponential phase (the analytic face, Q3 / middle-digit); or
3. an **effective adelic / `S`-arithmetic equidistribution** using the 3-adic contraction as a Pisot-conjugate
   substitute (the *most structurally-promising* route — it is the only one with a genuine extra structure
   (`|3/2|_3<1`) that the classical cousins exploit) — **conditional on a rank-1 `S`-arithmetic equidistribution**,
   which is the precise open frontier.

**Net:** the cousins prove the problem is *not* hopeless in general — three nearby systems are solvable — and they
pinpoint that `3/2` sits exactly at the intersection of "no unique ergodicity ∧ exponential ∧ no archimedean
conjugate." Route 3 (adelic, exploiting `|3/2|_3<1`) is the one new structural asset the cousins suggest is worth
years; it converts the problem to **rank-1 `S`-arithmetic equidistribution**, a named (open) target rather than
"solve Mahler." 0 false proofs; the rank-1 obstruction in Route 3 is stated, not hidden.
