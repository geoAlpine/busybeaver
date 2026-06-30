# One-sided (K) vs non-escape-of-mass / shrinking-target machinery — residual-candidate scout (2026-06-30)

*Scouts the TWO residual "this might already exist" candidates flagged by `RANK1_REDTEAM.md` — (i) a
Margulis-function / non-escape-of-mass argument adapted to the amenable-hyperbolic regime, and (ii) a
single-orbit shrinking-target estimate reaching a one-sided density — against the **WEAKER** true target:
the one-sided `liminf` cell-frequency bound that is `(K)` (NOT full equidistribution / `μ=`Haar). Strategic
hypothesis under test: a method giving a one-sided positive-density bound for the SPECIFIED orbit, without
pinning the whole measure, might evade the rigidity obstructions (which are about pinning `μ`). SOUNDNESS:
labels `[PROVEN]` (this program) / `[PROVEN-in-lit]` / `[HEURISTIC]` / `[OPEN]`. No claim that `(K)` is proved.
WebSearch used (US). NOT committed.*

---

## 0. Verdict

**The weakening to the one-sided target does NOT open either method. Both provably collapse — but to a
DIFFERENT wall than the rigidity no-go, and that is the one informative finding.** The rigidity engines
(`RANK1_AMENABLE_EQUIDISTRIBUTION.md`) fail because pinning the *whole* invariant measure needs rank ≥ 2 /
non-amenability; there, dropping to one-sided is at least *on the right axis*. The non-escape and
shrinking-target engines fail for an **orthogonal** reason that the one-sided relaxation does not touch:

- **Non-escape / Margulis** natively *outputs* a one-sided positive-frequency bound (proportion of time in a
  sublevel set). So on the **output axis** it is already shaped like `(K)`. Its wall is entirely on the
  **input axis**: (a) the solenoid `X` is **compact**, so non-escape is **vacuous** `[PROVEN]`; (b) the drift
  inequality it runs on is for an **averaging / random-walk operator** (annealed / a.e. starting point), not a
  single deterministic specified orbit; (c) the one genuinely *quenched* Foster–Lyapunov drift the program
  owns — `V=v₂(c−1)` — is **degree-1**, giving the **upper-bound / recurrence** direction (count of deep
  excursions `≤N`), which is **consistent with halting**, whereas `(K)` is a **second-moment lower bound** on a
  cell frequency. Relaxing the target relaxes the (already-native) output, not the (binding) compact/quenched
  input. `[PROVEN that this action has each disqualifying input feature]`
- **Shrinking-target** results are **a.e.** (full measure of *starting points*) and conclude **"infinitely
  often" / log-law**, occasionally a frequency *asymptotic* but still a.e.; the a.e. quantifier is baked into
  the Borel–Cantelli step and is **independent of one- vs two-sidedness**. The Haar-null specified seed is
  excluded at the *quantifier*, not at the conclusion strength. Moreover `(K)`'s cell `{D≥2}` has **fixed
  positive measure** — it is **not a shrinking target at all**, so the framework's native problem is the wrong
  one. `[PROVEN-in-lit that the surveyed results are a.e.]`

**Single sharpest fact established (§1):** the non-escape/Margulis machinery *natively produces* a one-sided
positive-frequency bound, so it is the only surveyed family whose **output** matches `(K)` exactly — yet it
provably cannot run here because non-escape is **vacuous on the compact solenoid** and the sole quenched
Foster–Lyapunov drift (`V=v₂(c−1)`) is **degree-1**, delivering only the **upper-bound/recurrence** direction
(a count `≤N`, `M(N)=O(log N)`) that a heavy-tailed = *halting* orbit also satisfies, while `(K)` is the
**second-moment LOWER bound** on cell frequency. The one-sided relaxation lands on the wrong axis (output, not
input). This is **recurrence ≠ frequency**, made exact.

---

## 1. Margulis-function / non-escape-of-mass analysis — the frequency-vs-recurrence gap, explicit

### 1.1 What the machinery actually delivers `[PROVEN-in-lit]`

The Margulis-function method (Eskin–Mozes *Margulis functions and their applications*; Eskin–Margulis–Mozes
quantitative Oppenheim; Eskin–Margulis quantitative recurrence; Benoist–Quint; Athreya–Margulis) runs on:

> a **proper** function `u` on a **non-compact** homogeneous space `G/Γ` (`u(x)→∞` as `x→cusp`) satisfying a
> **drift inequality** for an **averaging operator** `A` (a spherical average over the acting group, or a
> random-walk step `E_{g∼μ}[u(g·x)]`): `A u ≤ c·u + b` with `c<1`, `b<∞`.

Its two outputs:
1. **Non-escape of mass** (tightness): empirical measures do not leak into the cusp. `[PROVEN-in-lit]`
2. **Quantitative recurrence = a one-sided frequency bound for a sublevel set.** Iterating the drift gives
   `limsup_N (1/N)Σ_{n<N} u(x_n) ≤ b/(1−c)`, so by Markov
   `liminf_N (1/N)#{n<N : u(x_n) ≤ M} ≥ 1 − b/((1−c)M)`. `[PROVEN-in-lit]`

Output (2) is, in shape, **exactly a one-sided `liminf` positive-density bound** — the very form `(K)` is. So
this is the **one** surveyed family whose *conclusion* is the weaker one-sided target rather than full `μ=`Haar.
That is why the red-team flagged it, and it is a genuine point in its favour.

### 1.2 Why it nonetheless cannot apply — three input failures, each `[PROVEN]` for this action

**(a) Compactness ⇒ non-escape is vacuous.** `X=(ℝ×ℚ₂×ℚ₃)/ℤ[1/6]` is a **compact** solenoid (already noted
`NEW_ENGINE.md` §"constraints", line 13). There is no cusp; every proper `u` is bounded; for `M` past
`sup u` the sublevel set `{u≤M}` is **all of `X`**. Output (2) then reads "the orbit spends `≥1−ε` of its time
in `X`" — content-free. The `(K)` cell `{D≥2}` is a **clopen, fixed-positive-measure** set, not the complement
of a cusp neighbourhood, and there is no height function on compact `X` whose sublevel set is its complement
under a drift inequality. `[PROVEN: X compact]`

**(b) Averaged / annealed operator, not a deterministic single orbit.** The drift `A u ≤ cu+b` is for the
**averaging** operator `A` (spherical average / random-walk step). The recurrence conclusion is for the
**random walk**, the **stationary measure**, or **a.e. starting point** (Benoist–Quint and Eskin–Margulis are
*random-walk* recurrence theorems; EMM averages over an `SO(2,1)`-orbit). It is **not** a statement about the
single **deterministic** orbit `{Aⁿx₀}` of a **specified** `x₀`. Passing averaged → quenched-single-orbit is
exactly the a.e.→specified descent that is the whole wall (`BB6_NO_STRUCTURE_THEOREM`; package §3). `[PROVEN: the
acting group `Γ=ℤ[1/6]⋊⟨3/2⟩` is amenable/cyclic, so there is no random-walk spectral gap to drive an averaged
drift, and the orbit is a single deterministic trajectory]`

**(c) The one quenched drift the program owns is degree-1 ⇒ recurrence, not frequency.** The program's
`V=v₂(c−1)` **is** a genuine deterministic Foster–Lyapunov / Margulis-type function on the *non-compact
odd-integer model* (`V→∞` as `c→1` 2-adically, i.e. toward the halting fixed point `o=1`): drift exactly **`−1`
per `D=1` step**, jump **`+K`** at a refill. It **does** give recurrence — `ΣΔV` telescopes, so the number of
deep excursions and the count `ΣK` are `O(N)`, and `M(N)=max depth =O(log N)` `[OBSERVED + the count `ΣK≤N` is
PROVEN]`. **But this is the UPPER-bound / non-escape direction** ("the orbit cannot run away to the fixed
point"), and it is **consistent with both `(K)` and halting**.

`(K)` needs the **opposite sign and a higher moment**: even-density `=1−1/avgD`, so `(K)` (`ed≥1/3`) `⟺`
`avgD≥3/2` — a **LOWER bound on the earning frequency**, governed by the **refill-jump tail** (the second
moment `E[K²]`), not by the first-moment count the drift controls. `EXCURSION_SYNTHESIS.md` proves `[PROVEN
no-go for this whole class]`: every drift one can build on `V` has conditional excursion drift **linear in `K`**
(reads `E[K]` only); the degree-2 potential that would read `E[K²]` telescopes to the `0=0` tautology; and a
**heavy-tailed adversary** (`E[K²]=∞`, white, first-moment-matched — i.e. a giant run = an **atom at `o=1` =
HALTING**) satisfies **every** such drift inequality and is drift-indistinguishable from the real orbit.

**The exact gap.** In the *standard* (non-compact) Margulis setting recurrence *does* equal a frequency bound,
because the target (the compact set) **is** the sublevel set `{u≤M}` of the *same* `u` whose drift is
controlled. Here that coincidence breaks twice: the target `{D≥2}` is **not** a sublevel set of the controlled
function `V` (`V` tracks distance to the fixed point / even-run depth; `{D≥2}` is the orthogonal "earning"
cell), **and** even if it were, a non-escape drift is an **upper** bound (degree-1, first moment) while the
cell-frequency `(K)` is a **lower** bound that is a **second-moment** functional of the same excursions. So:

> **Non-escape / Margulis here gives RECURRENCE (count `ΣK≤N`, `M(N)=O(log N)`, orbit returns to bounded-`V`
> region) — already known, and consistent with halting — but NEVER FREQUENCY of the `(K)` cell, because the
> frequency is a second-moment LOWER bound that a heavy-tailed (halting) excursion law satisfies.** `[PROVEN]`

---

## 2. Shrinking-target / quantitative-recurrence literature — per-result a.e.-vs-specified, frequency-vs-i.o.

All surveyed shrinking-target results need a **non-compact** target (cusp neighbourhood with measure `→0`) and
a **reference measure** (Haar / Gibbs); their conclusions are **a.e. in the starting point**. Per result:

| Result `[PROVEN-in-lit]` | Quantifier | Conclusion type | Disqualifier for `(K)` |
|---|---|---|---|
| **Kelmer–Yu**, *Shrinking targets for ... flows on homogeneous spaces*, Trans. AMS 371 (2019); Ghosh–Kelmer *Shrinking targets for semisimple groups* | **a.e.** point (full Haar measure of starts) | **i.o.** + log-laws for cusp excursions (settles Athreya–Margulis); a counting asymptotic but a.e. | a.e. excludes the **Haar-null specified seed**; target is a **shrinking cusp nbhd**, our cell has **fixed** positive measure |
| **Kleinbock–Margulis** (log laws 1999; strong-BC / Schmidt condition) | **a.e.** | **strongly Borel–Cantelli**: hit-count `S_N(x)/E_N→1` — a frequency *asymptotic*, but a.e. | needs **exponential decay of correlations** (annealed mixing); a.e. excludes the seed; cusp target |
| **Maucourant** (log laws, geodesic/diagonal flows) | **a.e.** | **i.o.** / log-law | a.e.; cusp target; diagonal flow on non-compact space |
| **Athreya / Athreya–Margulis** (quantitative recurrence, non-escape, large deviations) | **a.e.** or **averaged** | non-escape + quantitative recurrence | averaged-not-quenched; cusp; same as §1 |
| **Dynamical Borel–Cantelli** (Chernov–Kleinbock; Gibbs-measure & Lipschitz-twist versions, e.g. arXiv:2205.12366; Gibbs-measure BC) | **a.e.** w.r.t. an invariant Gibbs measure | **i.o.**; the quasi-independent (strong) form gives frequency `∼` expected count, **a.e.** only | a.e.-w.r.t.-Gibbs excludes the seed (it is in the null exceptional set the BC argument cannot name) |
| **Eventually-always-hitting / zero-one laws** (arXiv:1904.08584, rapidly mixing systems) | **a.e.** | zero-one law (i.o./eventually) | a.e.; needs rapid mixing (annealed) |

**Net `[PROVEN-in-lit]`:** **no** surveyed shrinking-target result gives a **single specified** orbit (every one
is a.e. / full measure of starts), and the typical conclusion is **i.o.** or a **log-law**; the strong-BC
variants give a frequency asymptotic but still **a.e.** and still requiring **decay of correlations / mixing**
of the system against a **reference measure** (an annealed input). Two structural mismatches compound this:
(i) the a.e. quantifier's exceptional null set is **exactly** where a Haar-null point like the seed could sit —
the method **cannot certify any named point** is outside it (same gap as Birkhoff genericity); (ii) `(K)`'s cell
`{D≥2}` has **fixed positive measure**, so it is **not a shrinking target** — the framework's native problem
(how fast may a target shrink and still be hit i.o.) is **not** `(K)`'s problem (positive-frequency of a fixed
cell). The "single-orbit shrinking-target estimate reaching a one-sided density" the red-team worried about
**does not exist in the surveyed literature**: the closest objects are a.e. + i.o., one or two quantifiers
short on both axes.

---

## 3. Does dropping to the one-sided target open anything?

**No — and the reason is sharper than for the rigidity no-go.** The decisive observation is *which axis* the
weakening sits on for each method:

- **Rigidity engines** (Ratner / E–L / Rudolph–Johnson / BFLM): their conclusion *is* pinning the whole measure
  `μ=`Haar, and their input (rank ≥ 2 / non-amenable / unipotent) is what manufactures that. Dropping to the
  one-sided liminf is **on the conclusion axis they care about**, so it is at least the *right kind* of
  relaxation — yet `RANK1_AMENABLE_EQUIDISTRIBUTION.md` `[PROVEN]` shows the hypotheses still fail for the
  action regardless of output strength. (Recorded there; not re-litigated here.)

- **Non-escape / Margulis**: its conclusion is **already** a one-sided positive-frequency bound (§1.1). So the
  one-sided relaxation costs **nothing** and gains **nothing** — the method's wall is entirely on the **input**
  side (compactness ⇒ vacuous; averaged-not-quenched; degree-1 wrong-sign drift). Weakening the target relaxes
  the *output*, which was never the binding constraint. `[PROVEN: the three input features hold for this action]`

- **Shrinking-target**: the **a.e.** quantifier is produced by the Borel–Cantelli step and is **invariant under
  one- vs two-sidedness** of the target. The Haar-null seed is excluded at the **quantifier**, upstream of any
  statement about conclusion strength. So again the relaxation is on the wrong axis. `[PROVEN-in-lit]`

**Crisp verdict.** Dropping "`μ=`Haar" to "one-sided positive density" is a relaxation on the **output** axis.
The non-escape and shrinking-target methods are blocked on the **input** axis (compact phase space, averaged/
a.e. driving data). Output-axis relaxation cannot move an input-axis wall. Therefore the one-sided target opens
**no new route** through these two candidates; it collapses to a wall — but, importantly, **not the same wall**
as rigidity. It is the **"annealed/a.e./non-compact input"** wall (the program's recurring a.e.→specified and
count→frequency seam), reached here from the recurrence side. `[PROVEN for the input features; SURVEY-VERDICT
that no variant in the literature evades them]`

A residual honest caveat (the door this scout does **not** close): the *abstract* possibility of a **bespoke,
deterministic, quenched** Foster–Lyapunov function — not the averaging-operator kind — whose **drift itself
encodes a second-moment / earning quantity** is exactly the object `EXCURSION_SYNTHESIS.md` proves cannot be
built on `V` (degree-1 ceiling; heavy-tailed adversary survives). That no-go is **specific to the `σ(d)`-
measurable / depth-potential class**; a genuinely new height function reading the orbit's *magnitudes* in a
non-telescoping way is not excluded — but it would no longer be a "non-escape" argument (the input wall), it
would be the generational object of `NEW_MATH_PROGRAM.md`. The candidate, as a *non-escape* method, is closed.

---

## 4. Net

1. **Non-escape / Margulis is the only surveyed family whose OUTPUT already matches `(K)`** (a one-sided liminf
   frequency for a sublevel set). That genuine merit is why the red-team flagged it. `[PROVEN-in-lit]`
2. **But its INPUT fails three ways for this action, each `[PROVEN]`:** the solenoid is **compact** (non-escape
   vacuous, `NEW_ENGINE.md` §constraints); the drift is for an **averaging/random-walk** operator (annealed /
   a.e.), not a deterministic specified orbit; and the only **quenched** Foster–Lyapunov drift available
   (`V=v₂(c−1)`) is **degree-1**, giving the **recurrence / upper-bound** direction (`ΣK≤N`, `M(N)=O(log N)`),
   which a **heavy-tailed = halting** orbit also satisfies. `(K)` is the **second-moment LOWER bound** on cell
   frequency — recurrence ≠ frequency, exactly (`EXCURSION_SYNTHESIS.md`).
3. **Shrinking-target literature is uniformly a.e. + i.o.** (Kelmer–Yu, Kleinbock–Margulis, Maucourant,
   Athreya, dynamical Borel–Cantelli); the strong-BC variants reach a frequency asymptotic but stay a.e. and
   require decay-of-correlations against a reference measure. None is single-specified-orbit; and `(K)`'s
   **fixed-positive-measure** cell is **not a shrinking target**. `[PROVEN-in-lit]`
4. **The one-sided weakening opens nothing here** because for these two methods the relaxation is on the
   **output** axis while the wall is on the **input** (compact / averaged / a.e.) axis — a *different* wall from
   the rigidity no-go, but a wall. `[PROVEN input features; SURVEY-VERDICT no literature variant evades them]`
5. **No label upgraded. `(K)` remains `[OPEN]` = Mahler 3/2 / AEV Conj 1.6.** The residual open door is a
   bespoke quenched magnitude-reading height function — which is the `NEW_MATH_PROGRAM.md` object, **not** a
   non-escape argument.

---

## Sources

- A. Eskin, S. Mozes, *Margulis Functions and their Applications* (lecture notes). https://www.math.uchicago.edu/~eskin/margulis-functions.pdf
- A. Eskin, G. Margulis, S. Mozes, *Upper bounds and asymptotics in a quantitative version of the Oppenheim conjecture*, Ann. of Math. 147 (1998).
- A. Eskin, G. Margulis, *Recurrence properties of random walks on finite volume homogeneous manifolds* (2004).
- Y. Benoist, J.-F. Quint, *Random walks on reductive groups* / recurrence on homogeneous spaces.
- J. Athreya, G. Margulis, *Logarithm laws for unipotent flows*, arXiv:1105.5325.
- D. Kelmer, S. Yu (and M. Ghosh, D. Kelmer), *Shrinking targets problems for flows on homogeneous spaces*, Trans. AMS 372 (2019); *Shrinking targets for semisimple groups*, arXiv:1512.05848.
- D. Kleinbock, G. Margulis, *Logarithm laws for flows on homogeneous spaces*, Invent. Math. 138 (1999).
- *Dynamical Borel–Cantelli lemma for recurrence under Lipschitz twists*, arXiv:2205.12366; Gibbs-measure dynamical Borel–Cantelli.
- *Zero-one laws for eventually always hitting points in rapidly mixing systems*, arXiv:1904.08584.
- *An avoidance principle and Margulis functions for expanding translates of unipotent orbits*, arXiv:2206.12019.
- (repo) `EXCURSION_SYNTHESIS.md`, `EXCURSION_SUPERMARTINGALE.md`, `RANK1_AMENABLE_EQUIDISTRIBUTION.md`, `EMPTY_TOOLBOX_QUESTION.md`, `NEW_ENGINE.md` §constraints, `BB6_NO_STRUCTURE_THEOREM.md`, `NEW_MATH_PROGRAM.md`, `PARTIAL_POSITIVE_EVENDENSITY.md`.

*No machine decided beyond cited repo numerics. No label upgraded. `(K)` remains `[OPEN]`. Not committed.*
