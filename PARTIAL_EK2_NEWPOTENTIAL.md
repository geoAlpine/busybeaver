# E[K²]<∞ — three genuinely-new angles: non-polynomial potential, concentration, two-input interpolation (2026-06-30)

*WEAPONS_AUDIT-style. Target (strictly WEAKER than (K)): the jump-depth second moment `E[K²]<∞`
(⟺ mean 2-adic depth bounded ⟺ `Σ_k f_k<∞` ⟹ `μ({1})=0`, no atom at the repelling fixed point
`o=1`). `K = v₂(3o−1)` = jump/entry depth = countdown-run length. The prior round closed three routes
(`EK2_SECOND_BUDGET.md`: degree-1/2 depth potentials telescope to `0=0`; `EK2_TAIL_SEPARATION.md`:
countdown forces min-gap=1; `EK2_PARTIAL_MOMENTS.md`: no fractional moment, only `ΣK≤N` free). THIS
note attacks three angles deliberately DISTINCT from that round: (1) a NON-polynomial (exponential /
geometric) potential; (2) a deterministic-concentration (Azuma/McDiarmid) bound on the empirical 2nd
moment; (3) a TWO-input interpolation combining the 2-adic budget with the 3-adic valuation. SOUNDNESS
PARAMOUNT; every line labelled; (K) NOT claimed; willing to retract. Orbit `c_{n+1}=⌊3c_n/2⌋`, `c_0=8`.
Numerics `.venv`, exact big-int, `N=10⁵`, `ek2_newpot.py`. NOT committed.*

---

## 0. One-line verdict

**All three reduce — but each with a NEW, sharper reason than the prior round, and one (the 3-adic
side) is a genuinely new structural fact.** No `E[K²]<∞`, no `E[K^{1+ε}]<∞`. (1) **Any** potential that
is a function of the current depth `d_n` — exponential `λ^{d}`, geometric `2^{-d}`, bounded, polynomial
— is an **EXACT coboundary along the deterministic countdown**: its sum over each excursion is a pure
boundary term `=0` (verified exact for `λ=2,3/2,½,3`), because an excursion is a *closed loop in
depth-space* (`d: 0→K→K−1→…→1→0`) and the sum of `Δg` around any closed loop in the state variable
vanishes identically. This is a no-go for the **entire class** of `σ(d_n)`-measurable potentials,
strictly more general than the prior "degree-2 self-closes." (2) Deterministic concentration fails
*triply*: McDiarmid's bounded-difference constant is `(max K)²`, **unbounded exactly by the giant-run
event** `E[K²]=∞` we want to exclude (circular); concentration bounds the *fluctuation* of the
empirical 2nd moment, **never its mean level** `=E[K²]`; and the requisite martingale filtration needs
the refill-digit law (mixing) `=` genericity. (3) The 3-adic side is a **symmetric copy of the same
dichotomy**: `v₃(c_n)=` current even-run length, with a FREE first-moment count `Σ_{odd}v₃≈#even≤N`
and a HARD energy `Σ_n v₃=½(ΣE²+ΣE)` — itself a *second* moment of even-run lengths (`E[E²]≈6.01 ≈
E[K²]≈5.92`), with no proven `O(N)` cap. So there is **no independent second proven input**; Hölder
among first-moment counts `+L^∞` support can only manufacture `N^{1+ε}`. **The exact gap is unchanged:
a tail-decay rate / a potential that reads the unrevealed 2-adic digits of `c_n` = single-orbit
equidistribution of `c_n mod 2^k` = the open Mahler `(3/2)^n` kernel.**

---

## 1. Angle 1 — a NON-polynomial potential: the exact-coboundary no-go [PROVEN, verified exact]

**Setup.** The depth dynamics, projected to the variable `d_n=v₂(c_n−1)`, is a deterministic
excursion process: by the **Countdown Lemma [PROVEN]** an odd term with `d=a≥1` has successor with
`d=a−1`, so each excursion runs `d: K, K−1, …, 1, 0`, and refills jump `0→K` (`K=v₂(3c'−1)`, the
Mahler core). We seek a potential `g` with a sub-coboundary inequality `ψ ≤ g∘T − g + const` for an
observable `ψ` proxying the 2nd moment (e.g. `ψ = 1{D≥2}+1{D≥3}+…`, or `K²` itself), so that
`Σψ ≤ g_N − g_0 + const·N = O(N)`. The prior round tried `g=d_n` and `g=d_n²` (self-closed) and noted
`g=2^{-d_n}` under-weights the tail. **New here:** try the full exponential family `g(c)=λ^{d_n}`
(`λ>1` over-weights deep runs — the opposite failure mode of `2^{-d}`) and ask whether ANY non-poly
`g(d)` escapes.

**The general no-go [PROVEN].** Let `g(c)=h(d_n)` for ANY function `h`. Telescoping over a single
excursion `0→K→K−1→…→1→0`:
- refill `0→K` injects `Δ = h(K) − h(0)`;
- the countdown `K→K−1→…→0` injects `Δ = [h(K−1)−h(K)] + … + [h(0)−h(1)] = h(0) − h(K)` (telescopes).

**Excursion sum `= [h(K)−h(0)] + [h(0)−h(K)] = 0`, identically, for every `h` and every `K`.** An
excursion is a *closed loop* `d=0→…→0`; the sum of exact differences of a state function around a
closed loop is zero. Hence `Σ_{n<N} Δg = g_N − g_0` (a boundary term `O(h(d_N))`), carrying **no
information about the refill magnitudes** — exactly the `0=0` tautology, now seen to hold for the
**entire class** `σ(d_n)`, not just degrees 1,2.

**Verified exact (`ek2_newpot.py`, big-int):** for `λ∈{2, 3/2, ½, 3}` the telescope total `g_N−g_0=0`
(both ends even, `d=0`), the refill sum `+X` and countdown sum `−X` **cancel exactly** (`refill +
countdown = 0`), and the predicted per-run injection `Σ_i(λ^{K_i}−1)` equals the actual refill sum
with **diff `=0`**. E.g. `λ=2`: `±1.557×10⁶`; `λ=3`: `±3.688×10⁹`. The bigger `λ`, the bigger the
(perfectly cancelling) magnitudes — `λ>1` over-weights the deep runs but the countdown removes exactly
the same amount, because the deep run *deterministically descends back through every level it injected*.

**Why the whole family is doomed (the sharp statement).** The 2nd moment `ΣK²` lives on the refill
**magnitudes** `K_i`, which are `v₂(3c'−1)` at the even-step value `c'`. At a refill the current depth
is `d=0` — so `K_i` is **NOT** a function of `d_n`; it is a function of the *hidden lower 2-adic digits*
of `c'` (the moving middle digit / Mahler vertex). Any `σ(d_n)`-measurable potential is blind to these
digits, hence is an exact coboundary, hence tautological. **A potential carrying 2nd-moment information
must be `σ(c_n mod 2^m)`-measurable for `m` beyond the revealed depth — i.e. it must read the
unrevealed digits, which is precisely the equidistribution input `=` Mahler.** The mixed
"magnitude-Lyapunov × depth" potential the ask floats inherits the magnitude-Lyapunov's known defect
(`renewal_attack`: jumps are a driftless random walk, no super-/sub-martingale; the high-`D` measures
realise the heavy tail), so it too admits the heavy-tail invariant measure and gives no one-sided bound.

**Verdict 1: REDUCES.** Non-polynomial potentials do **not** avoid the tautology; they make the no-go
*more general* (every `σ(d)`-measurable `g` is an exact coboundary). New reason vs prior round: it is
not that `p=2` is special — it is that the depth excursion is a closed loop and the 2nd moment lives on
the orthogonal (hidden-digit / refill-magnitude) coordinate.

---

## 2. Angle 2 — deterministic concentration (Azuma / McDiarmid) on `(1/R)ΣK_i²` [REDUCES, triple obstruction]

The `K_i` are deterministic, so to invoke a concentration inequality one must (a) cast `(1/R)ΣK_i²` as
a function of independent inputs with bounded differences, or (b) build a martingale on a filtration
`F_i`. Three independent obstructions, each fatal:

1. **Bounded-difference constant is unbounded — and unbounded by exactly the event we want to
   exclude.** McDiarmid bounds `|empirical − mean| ≲ (range of one coordinate)·√(#coords)/#coords`.
   Changing one refill `K_i` changes `ΣK_i²` by up to `(max K)² ≈ (0.585N)²` (proven support bound,
   `VALUATION_BUDGET`). The bounded-difference hypothesis `c_i = O(1)` is **logically equivalent to
   "no giant run,"** i.e. to `E[K²]<∞` itself. **Circular:** the concentration hypothesis IS the
   conclusion. A single deep run of length `≈0.585N` (consistent with every proven identity) moves the
   empirical 2nd moment by `Ω(N)` — McDiarmid does not apply, and *should* not.
2. **Concentration controls the FLUCTUATION, not the LEVEL.** Even granted a bounded-difference
   martingale, Azuma gives `(1/R)ΣK_i² ≈ μ̄ ± O(1/√R)` for `μ̄ =` the conditional mean. But `μ̄` IS
   `E[K²]` — the very number whose finiteness is open. Concentration says the empirical 2nd moment is
   *close to its own mean*; it can never decide whether that mean is finite. (Same shape as
   `M4_P2_RESULT`: an identity relating quantities bounds neither.)
3. **The only non-circular filtration needs mixing = genericity.** With no exogenous randomness,
   `E[K_i | F_{i−1}]` is either `K_i` itself (martingale differences `=0`, no concentration) or requires
   *positing the refill-digit law* (Haar `P(K=k)=2^{-k}`). Positing it is single-orbit equidistribution
   of `c_n mod 2^k` — the open Mahler kernel. The "carry automaton" (2-adic odometer) does generate the
   next digit deterministically, but quantitative bounded-differences from it needs a spectral gap /
   mixing rate, which is exactly the equidistribution rate.

**Verdict 2: REDUCES.** Deterministic concentration is structurally the wrong tool *and* circular: its
hypothesis (bounded differences) equals the conclusion (`E[K²]<∞`), and even if granted it bounds the
fluctuation around `E[K²]`, never `E[K²]` itself. New reason vs prior round: the prior never tried
concentration; the finding is that the heavy-tail giant-run event is *precisely* the McDiarmid
hypothesis violation, making the route self-referential.

---

## 3. Angle 3 — two-input interpolation, incl. the 3-adic valuation [REDUCES; new 3-adic fact]

The free PROVEN facts are: (i) the 2-adic budget `Σ_{odd i<N} v₂(3c_i−1)=N+v₂(c_N)−v₂(c_0)`, i.e.
`ΣK_i ≤ N+O(log N)` (a first-moment **count**, `L¹`); (ii) the support bound `K_i ≤ ⌊log₂c_i⌋≈0.585i`
(`L^∞`); (iii) the foothold `≈0.85 log N` and `M(N)≈log₂N` (the latter only OBSERVED). The prior round
showed Hölder between `L¹` and `L^∞` gives only `ΣK^{1+ε} ≤ (max K)^ε·ΣK = O(N^{1+ε})` — loose by `N^ε`
(re-verified: `ε=1` gives crude `9.97` vs actual `1.48`; the proven `max K≤0.585N` makes it `≈0.29·N^ε`).

**The new candidate second input: the 3-adic valuation `v₃(c_n)`.** [PROVEN, verified 0 violations.]
On the orbit, `v₃` has a clean telescope DUAL to the 2-adic one: on an **even** step `c_{n+1}=3c_n/2`
so `v₃(c_{n+1})=v₃(c_n)+1`; on an **odd** step `3c_n−1≡−1 (mod 3)` so `v₃(c_{n+1})=0` (reset). Hence
**`v₃(c_n) = length of the current even-run`** (the holding time at depth `0`), the 3-adic mirror of
`d_n=v₂(c_n−1)=` position within the current odd-run. Two consequences, both verified:

- **A FREE 3-adic first-moment count.** Telescoping `Δv₃`: `+1` on even steps, `−v₃(c_n)` on odd steps,
  summing to `v₃(c_N)−v₃(c_0) = #even − Σ_{odd}v₃(c_n)`, i.e. `Σ_{odd}v₃(c_n) ≈ #even ≤ N`. This is a
  genuine second proven input — **but it is again a first-moment count `≤N`** (the 3-adic mirror of
  `ΣK≤N`), carrying no tail.
- **The 3-adic ENERGY is itself an open second moment.** `Σ_n v₃(c_n) = ½(Σ_j E_j² + Σ_j E_j)` where
  `E_j` are the even-run lengths (triangle sum, the exact mirror of `Σd_n=½(ΣK²+ΣK)`). Verified:
  `Σv₃=100327`, `½(ΣE²+ΣE)=100328` (off by 1 = mid-run truncation boundary). Numerically
  `E[E]=2.004`, `E[E²]=6.014`, `max E=15` — **the even-run 2nd moment is the same magnitude and the
  same difficulty as the depth 2nd moment** `E[K²]=5.918`. So the 3-adic side has **no `O(N)` cap on
  its energy either**; it is a co-equal open second moment, not a fresh handle.

**Why two inputs still cannot reach `E[K²]`.** All proven inputs are either first-moment **counts**
(`ΣK≤N`, `Σ_{odd}v₃≈#even`) or the `L^∞` **support** (`0.585n`). Hölder/Cauchy–Schwarz can only bound a
moment by *higher* moments (`(ΣK)² ≤ R·ΣK²` runs the *wrong way*; bounding `ΣK²` needs an `L^p`, `p>2`,
which is *harder*). Combining two first-moment counts stays first-moment; adding `L^∞` support only
buys the `N^ε`-loose envelope. There is **no proven `L^p` with `p>1`** (other than the trivial support),
so no interpolation produces `L²`. The 3-adic energy that *would* be a second input is itself open and
numerically identical to the target.

**Verdict 3: REDUCES.** New reason vs prior round: the 3-adic valuation does give a second exact
telescope, but it splits into the *same* free-count / open-energy dichotomy (mirror-symmetric to the
2-adic depth), so it is not an independent input — the even-run 2nd moment is as hard as `E[K²]`. Two
first-moment counts + `L^∞` cannot interpolate to `L²` without an `L^{p>1}` tail bound.

---

## 4. Does any angle give `E[K²]<∞` or a fractional moment `E[K^{1+ε}]<∞`? — NO.

| angle | new attempt | outcome | new precise reason |
|---|---|---|---|
| 1 non-poly potential | `g=λ^{d_n}` (`λ>1,<1`), any `g(d)` | **REDUCES** | every `σ(d_n)` potential is an EXACT coboundary (closed-loop excursion ⇒ sum `=0`); 2nd moment lives on hidden refill digits = Mahler |
| 2 concentration | Azuma/McDiarmid on `(1/R)ΣK²` | **REDUCES** | bounded-diff constant `=(max K)²` unbounded ⟺ giant run ⟺ `E[K²]=∞` (circular); bounds fluctuation not the mean level `E[K²]`; needs mixing = genericity |
| 3 two-input | 2-adic budget × 3-adic `v₃` | **REDUCES** | 3-adic side = mirror dichotomy (free count `Σ_{odd}v₃≈#even`; open energy `Σv₃=½(ΣE²+ΣE)`, `E[E²]≈E[K²]`); Hölder among counts+`L^∞` can't make `L²` |

No `E[K²]<∞`, no `E[K^{1+ε}]<∞` for any `ε>0`, no reduction to a *new* proven input. All three bottom
out at the identical wall as the prior round and `NONATOMIC_FIXEDPOINT.md`.

---

## 5. The exact gap (one sentence)

> **A tail-decay rate `P(K≥k)=O(k^{-(1+ε)})`, equivalently a potential `σ(c_n mod 2^k)`-measurable
> beyond the revealed depth that reads the refill-generating digits.** Angle 1 shows no `σ(d_n)`
> potential supplies it (exact coboundary); angle 2 shows concentration cannot decide a mean level and
> its hypothesis is the conclusion; angle 3 shows the 3-adic mirror only reproduces the same
> free-count/open-energy split. The missing object is the single-orbit equidistribution of `c_n mod 2^k`
> — the open Mahler `(3/2)^n` kernel. First moment (count) is free on BOTH the 2-adic and 3-adic sides;
> the second moment (energy) is open on both, mirror-symmetrically.

---

## 6. Numerics [OBSERVED, exact big-int, `N=10⁵`, `ek2_newpot.py`]

- **Exponential potential cancellation (angle 1):** telescope total `g_N−g_0=0` exactly for
  `λ∈{2,3/2,½,3}`; refill sum `= −`countdown sum exactly (`refill+countdown=0`); predicted per-run
  `Σ_i(λ^{K_i}−1)` matches actual refill with **diff `=0`** (`λ=2`: `±1.557×10⁶`; `λ=3`: `±3.688×10⁹`).
  Confirms the closed-loop coboundary identity for the whole exponential family.
- **3-adic structure (angle 3):** "increment on even / reset on odd" violations `=0`; `Σ_n v₃=100327`,
  `½(ΣE²+ΣE)=100328` (Δ1 = boundary); `#even=50159`, `Σ_{odd}v₃≈#even` (free count); even-runs:
  `#=25026`, `E[E]=2.004`, `E[E²]=6.014`, `max E=15`. Depth side: `#runs=25025`, `E[K]=1.992`,
  `E[K²]=5.918`, `max K=20`; `ΣK/N=0.498` (count, `≤1` PROVEN), `ΣK²/N=1.481` (energy, OBSERVED
  bounded). The even-run and odd-run energies are numerically twins (`6.01 ≈ 5.92`) — the symmetry.
- **Hölder looseness (angle 3):** `ε=0.5`: actual `ΣK^{1.5}/N=0.817` vs crude `max^{0.5}·ΣK/N=2.23`;
  `ε=1`: actual `1.481` vs crude `9.97` — and with the proven `max K≤0.585N` the crude bound carries the
  `N^ε` factor, never `O(N)`. All consistent with `E[K²]<∞` but **evidence, not proof** (the
  equidistribution-flavoured finite-`N` data cannot upgrade).

Runtime `≈5s`, `N=10⁵`.

---

## Sources

- `NONATOMIC_FIXEDPOINT.md` — PROVEN reduction `μ({1})=0 ⟺ f_k→0 ⟸ Σf_k<∞ ⟺ E[K²]<∞`; first-vs-second-moment gap; Countdown Lemma; mean-depth identity.
- `EK2_SECOND_BUDGET.md` — prior round: degree-1/2 depth potentials telescope `ΣK^p` to itself (`0=0`); `p=1` free count, `p=2` `(K)`-hard; `g=2^{-d}` under-weights tail. (Angle 1 here generalises this to ALL `σ(d)` potentials.)
- `EK2_TAIL_SEPARATION.md` — prior round: countdown forces min index-gap `=1`; separation/BC cannot bound `Σf_k`; reduces to refill-law genericity.
- `EK2_PARTIAL_MOMENTS.md` — prior round: no proven fractional moment `E[K^{1+ε}]`; only `ΣK≤N` free; Hölder `L¹×L^∞` gives `N^{1+ε}`; longest-run literature doesn't apply (iterated-floor orbit ≠ standalone power).
- `VALUATION_BUDGET.md` — PROVEN 2-adic budget `Σ_{odd}v₂(3c_i−1)=n+v₂(c_n)−v₂(c_0)`; support `K_i≤0.585n`.
- `REPELLER_ESCAPE.md` / `MINPROP_RUNS.md` — Countdown Lemma `[PROVEN]`; refill law `freq(D=1)=1−1/E_deep`, no one-sided margin.
- `antihydra_renewal_attack.md` — jump random walk has no super-/sub-martingale (kills the magnitude-Lyapunov mixed potential of angle 1).
- `LIMIT_THEOREM.md §3″` — single-orbit equidistribution `=` Mahler `(3/2)^n` kernel = the exact gap.
- Numerics: `scratchpad/ek2_newpot.py` (exact big-int; exponential-potential cancellation, 3-adic telescope, even-run energy, Hölder looseness; `N=10⁵`).

No machine decided. No label upgraded.
