# WALL (B): does C3 aperiodicity advance the renewal-CLT toward the SPECIFIC orbit? (2026-06-28)

*Combines the newly proven fact **C3** (the integer Antihydra orbit's parity itinerary is NOT eventually
periodic, `WALLB_NONATOMIC.md` §2) with the **renewal-CLT** structure (`ROUTE_RENEWAL_CLT.md`): the exact
decomposition `Σ_n(-1)^{r_n} = Σ_blocks (2 - g_i)`, `g_i` = return time of the orbit to the even set. Goal:
does aperiodicity yield a CONDITIONAL or PARTIAL equidistribution for the specific orbit `c0=8`, or does the
return-time mean's convergence itself require equidistribution (the wall)? Numerics `.venv` only
(`scratchpad/renewal_aperiodic.py`). Every line labelled. Zero false proofs. NOT committed.*

---

## 0. One-line answer

**C3's aperiodicity does NOT advance the renewal-CLT toward the specific orbit.** Three independent reasons,
all confirmed:

1. **`[PROVEN, elementary]` "mean return time = 2" is NOT weaker than "even-density = 1/2" — it is the SAME
   statement.** At the specific-orbit level `mean_g · even-density ≡ 1` is an exact identity (`N = Σ g_i`).
   So Kac's lemma gives **no shortcut**: pinning the mean return time to 2 *is* proving even-density 1/2.
   Kac is a theorem only for the *invariant measure*; the specific-orbit transfer is Birkhoff genericity = the
   wall, and within the orbit the relation is a tautology with zero leverage.
2. **`[PROVEN, structural]` aperiodicity is consistent with a biased renewal mean.** The renewal-CLT needs
   quantitative *mixing / stationarity* of the gap sequence; aperiodicity is only a qualitative
   measure-zero exclusion. The **entire remaining wall** (the *aperiodic* biased orbits, `WALLB_NONATOMIC` §3)
   is aperiodic. An aperiodic-but-biased surrogate (`S4`) has `mean_gap = 2.51 ≠ 2` and `|S|/√K` growing
   linearly — aperiodicity does not pin the mean. So **"aperiodic + renewal" = "aperiodic alone"** for the mean.
3. **`[STRUCTURAL]` return-time-distribution convergence IS equidistribution.** The gap law converging to
   `Geometric(1/2)` (`P(g=k)=2^{-k}`, mean 2) is exactly the Haar cylinder-frequency statement = wall (A).
   Its convergence does not follow from aperiodicity; it is the wall.

**Net:** C3 and the renewal-CLT close *different, complementary* slices. C3 (arithmetic) kills the
**periodic** return-time patterns — the countable structured slice — *without* the renewal machinery. The
renewal-CLT needs the **aperiodic, full-complexity** gap sequence, which is exactly what aperiodicity does
NOT control. No genuine advance; no false proof.

---

## 1. What the renewal-CLT gives and what it ASSUMES `[STANDARD / TO BUILD]`

**Exact (no assumption).** Partition each block `[n_i, n_{i+1})` between successive even points: the even
point contributes `(-1)^0 = +1`, the following `g_i - 1` odd points contribute `-1` each, so the block sum is
`1 - (g_i-1) = 2 - g_i`. Hence
```
   Σ_{n<N} (-1)^{r_n}  =  Σ_{i<K} (2 - g_i)  +  O(1)        [EXACT, g_i = return time to even].
```
**What the GM-CLT would give.** If the gap sequence `(g_i)` is, under the relevant measure, a **stationary,
exponentially-mixing** sequence with **mean exactly 2**, the Gibbs–Markov / renewal CLT gives
`Σ(2-g_i) = O(√K) = o(N)` ⇒ even-density → 1/2 ⇒ Antihydra non-halt. `[STANDARD]` for the **invariant
(Gibbs/Haar) measure** and **a.e.** orbit.

**What it ASSUMES (the gap, per `ROUTE_RENEWAL_CLT` §1 (iii)).** Two inputs, neither available for `c0=8`:
- (mean) `E[g_i] = 2` — i.e. `μ(even) = 1/2` by Kac. For Haar this is the geometric law; for the *specific
  orbit* this is the very target.
- (mixing) `(g_i)` is stationary with summable correlations. This is a property of the *invariant measure /
  a.e. orbit*, **not** of the one trajectory `c0=8`. Transferring it to `c0=8` is Birkhoff genericity = the wall.

---

## 2. Does C3's aperiodicity HELP close the renewal gap? `[PROVEN: NO — confirmed]`

**Claim tested:** aperiodicity rules out the orbit being trapped in a *periodic return-time pattern* (which
would give a biased, exactly-rational `Σ(2-g_i)/K`). Does "aperiodic + renewal" give more than "aperiodic
alone"?

**Answer: NO.** Aperiodicity excludes only the **eventually-periodic** gap sequences. But:
- A biased renewal mean does **not** require periodicity. A Birkhoff-generic point of a *non-Haar* ergodic
  measure has an **aperiodic** itinerary and a biased gap mean. This is precisely the *unstructured/aperiodic
  half* of the exceptional set (`WALLB_NONATOMIC` §3), which is full-dimensional and non-sofic.
- The renewal-CLT's missing input is *quantitative mixing*, not *non-periodicity*. Aperiodicity gives no
  decay-of-correlation, no stationarity, no mean. It is a measure-zero qualitative exclusion; the CLT needs a
  positive-measure quantitative ergodic input.

**Numerical confirmation** (`renewal_aperiodic.py`, surrogate `S4` = biased coin `p_odd=0.6`, length `10^6`):
genuinely **aperiodic** (no period ≤ 2000 in the tail window) yet `mean_gap = 2.506 ≠ 2`,
`S = Σ(2-g) = -201747`, `|S|/√K = 319` — i.e. `S` grows **linearly**, NOT `O(√K)`. Aperiodicity coexists with
a biased renewal mean and a non-CLT (linear) parity sum. (`S2`, a near-rational Sturmian density-1/3, also
gives `mean_gap = 1.5`, `|S|/√K = 408`; its tiny irrational perturbation registers as period-3 over the 20k
window — a clean *genuinely aperiodic* biased witness is `S4`.)

> `[PROVEN, structural]` Aperiodicity does NOT pin the renewal mean to 2. The renewal-CLT requires mixing of
> the aperiodic gap sequence; that is the open ingredient and aperiodicity provides none of it.
> **"Aperiodic + renewal" = "aperiodic alone"** for the renewal mean. C3 closes the periodic slice (which the
> renewal machinery does not even need); the renewal route is bottlenecked precisely on the aperiodic slice.

---

## 3. Kac / mean-return-time: is even-density 1/2 obtainable by an argument WEAKER than equidistribution?
`[PROVEN, elementary: NO — it is a tautology at the orbit level]`

Kac's lemma: for an ergodic m.p.s. the mean return time to `A` equals `1/μ(A)` (w.r.t. the induced measure on
`A`). So `μ(even) = 1/2 ⟺ mean return = 2`. **Hope:** pin the mean to 2 by an arithmetic/renewal argument
using aperiodicity, even if the full distribution stays open.

**This hope fails, identically.** At the **specific-orbit** level the relation is an *exact identity*, not a
theorem:
```
   Σ_{i<K} g_i  =  (span covered)  =  N + O(1)            [the gaps tile the time axis]
   ⇒  mean_g  =  N/K  =  1 / (empirical even-density)      [EXACT, no dynamics]
   ⇒  mean_g · even-density  ≡  1.
```
Confirmed numerically: real orbit `c0=8`, `N=4·10^5`, `mean_g = 2.003687`, `even-density = 0.499080`,
`mean_g · even-density = 1.0000000000`. **Pinning `mean_g → 2` is *literally* proving `even-density → 1/2`** —
not one step weaker. Kac as a *theorem* lives on the invariant measure; the transfer to `c0=8` is exactly the
Birkhoff-genericity wall, and *within* the orbit Kac degenerates to the identity above and yields nothing.

**Does the return-time *distribution's* convergence require equidistribution?** Yes. The gap law converging to
`Geometric(1/2)` (`P(g=k)=2^{-k}`) is the Haar cylinder-frequency statement: the gap `g` is a deterministic
function of the low 2-adic bits of `c` at the even point, so `g`'s distribution = the orbit's cylinder
frequencies = equidistribution = wall (A). Convergence of even the **first moment** is the target; convergence
of the **distribution** is strictly the wall. There is no weaker handle here.

---

## 4. Numerics — return-time structure of the specific orbit `[OBSERVED]`

`renewal_aperiodic.py`, exact big-int for the real orbit `c0=8`, `N=4·10^5` (`K=199631` blocks).

| quantity | real orbit `c0=8` | target (Haar) |
|---|---|---|
| mean return time `mean_g` | **2.003687** | 2 |
| even-density over span | 0.499080 | 0.5 |
| `mean_g · even-density` | **1.0000000000** (exact identity) | 1 |
| `Σ(2-g_i)` (parity sum) | `-736` | `o(N)` |
| `|Σ(2-g_i)|/√K` | **1.647** (`O(1)`) | bounded ⇒ CLT |
| gap autocorrelation lag 1..20 | all `≤ 0.0034` (null `≈ 0.0022`) | 0 ⇒ no memory / mixing |
| stationarity (mean per quarter) | 1.994, 2.005, 2.009, 2.007 | 2 (stationary) |

**Return-time distribution** vs `Geometric(1/2)` — near-perfect:
`P(g=1..5) = 0.4984, 0.2505, 0.1249, 0.0631, 0.0312` vs `0.5, 0.25, 0.125, 0.0625, 0.03125`. The depth
`v2(c)` at even points follows `P(v2=k) ≈ 2^{-k}` (k≥1), the 2-adic source of the geometric gap law.

**Aperiodicity-respecting surrogates** (length `10^6`) — the decisive contrast:

| surrogate | aperiodic? | even-dens | mean_gap | `|Σ(2-g)|/√K` |
|---|---|---|---|---|
| `S1` Sturmian density~1/2 (unbiased) | yes | 0.4999 | 2.0005 | 0.33 (`O(1)`) |
| `S3` fair coin (Geometric) | yes | 0.5006 | 1.9977 | 1.61 (`O(1)`) |
| **`S2` Sturmian density~1/3 (BIASED)** | (near-rational) | 0.6667 | 1.5000 | **408** |
| **`S4` biased coin `p_odd=0.6` (BIASED)** | **yes** | 0.3991 | 2.5055 | **319** |

`[OBSERVED]` The real orbit is **statistically indistinguishable from a fair coin / Geometric return times**
(mean → 2, CLT scaling, null autocorrelation, stationary, geometric distribution). The **aperiodic-and-biased**
surrogate `S4` shows that **aperiodicity alone permits `mean_gap ≠ 2` with a linearly-growing parity sum** —
so the real orbit's observed mean-2 behavior is an *empirical* fact about `c0=8`, NOT a consequence of its
proven aperiodicity. (Finite `N` proves nothing about the limit; `E` is exactly the set invisible to finite
tests.)

---

## 5. Verdict

| question | answer | label |
|---|---|---|
| Does C3 aperiodicity advance the renewal-CLT toward the specific orbit? | **No.** It excludes only periodic gap patterns (the countable slice C3 already kills arithmetically, *without* renewal). The renewal-CLT is bottlenecked on the *aperiodic* gap sequence, where aperiodicity gives no mixing/mean. | `[PROVEN: no gain]` |
| Does Kac / mean-return-time give even-density 1/2 by an argument weaker than equidistribution? | **No.** `mean_g · even-density ≡ 1` is an exact identity at the orbit level; "mean return = 2" *is* "even-density = 1/2", not weaker. Kac-as-theorem lives on the invariant measure; the transfer is the Birkhoff wall. | `[PROVEN: tautology]` |
| Does the return-time distribution's convergence require equidistribution? | **Yes.** The gap law = orbit cylinder frequencies; `Geometric(1/2)` convergence = Haar = wall (A). Even first-moment convergence is the target. | `[STRUCTURAL]` |
| Numerics on the specific orbit | mean → 2.004, CLT scaling `O(1)`, null autocorrelation, stationary, `Geometric(1/2)` distribution — fair-coin behavior. Aperiodic-biased surrogate `S4` (mean 2.51, linear `S`) proves aperiodicity ≠ mean-pinning. | `[OBSERVED]` |

**Bankable (zero false proofs).** C3's aperiodicity is a real `[PROVEN]` exclusion of the **periodic** part of
the exceptional set, but it is **orthogonal** to the renewal-CLT's needs: the renewal route requires
quantitative mixing/stationarity of the *aperiodic* return-time sequence, and aperiodicity supplies none of it.
The Kac/mean-return-time hope collapses to an exact identity (`mean_g · even-density ≡ 1`), so it offers no
sub-equidistribution shortcut to even-density 1/2. The specific orbit *empirically* behaves like a fair coin
(mean-2 geometric returns, CLT scaling), but this is `[OBSERVED]`, not derivable from aperiodicity — the
aperiodic-biased surrogate is the explicit counterexample to any such derivation. **The renewal wall is the
mixing/genericity of the aperiodic gap sequence — i.e. wall (A) / Mahler — unchanged by C3.**

### Live next angle
The renewal route's only remaining input is *relative mixing of the gap sequence over the rotation base*
(`ROUTE_RENEWAL_CLT` §2–3). C3 does not supply it, but the **conditional/innovation form**
`E[(2 - g_i) | F_{i-1}] = o(1)` (martingale-difference of the gap increments over the carry filtration,
`SESSION_2026-06-28_WALL_B_DEEP` C1) is the matching weakest target: a *single conditional first moment* of the
gap, strictly weaker than full mixing. Whether the proven aperiodicity plus the 2-adic depth law constrains
that conditional mean is the next probe — but note it terminates on the same `(3/2)^j` Mahler phase.
