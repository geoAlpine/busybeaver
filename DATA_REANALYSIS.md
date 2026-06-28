# Fresh-eyes re-analysis of the accumulated Antihydra data — hunt for any unexploited lever (2026-06-28)

Adversarial re-read of all 2026-06-28 data docs (`SESSION_2026-06-28_DATA`, `QUENCHED_DATA`,
`NU_RATE_DATA`, `ANNEALED_QUENCHED_DATA`, `O18_QUENCHED_BC`, `O18_CARRYRUN`, `NONPISOT_FOURIER_CHAIN`,
`ADELIC_COUPLING`, `COMPLETE_PROOF_CAPSTONE`) **plus** new probes run this session
(`scratchpad/reanalysis.py`, exact big-int, `.venv`). Goal: find any unexploited signal/lever toward the
complete proof, or state plainly that there is none. Labels `[PROVEN]`/`[OBSERVED]`/`[OPEN]`. Zero false proofs.

**Bottom line up front.** No unexploited signal was found. Every fresh probe reproduces pure Haar/i.i.d.
behavior to the noise floor, consistent with the docs. The hunt did produce two genuinely useful *clarifying*
results (both confirming the wall, neither a crack): (a) a clean exact **potential telescoping identity** that
shows the wall extends to **every** positive constant `c`, not just `1/3`; and (b) the precise reason the
algebraic consecutive-`D` coupling is invisible. The single open frontier is unchanged: effective
single-orbit equidistribution of `{(3/2)^n}` = AEV/Mahler.

---

## 1. New probes and what they show  [OBSERVED, exact big-int, N=3·10⁵ and 1.5·10⁶]

Induced odd map `o ↦ 3^{D-1}(3o−1)/2^D`, `D=v₂(3o−1)`, `o₀=27`. All exact.

| probe | result | reading |
|---|---|---|
| `freq(D≥k)` vs Haar `2^{−(k−1)}`, k=2..11 | matches to `≤1·10⁻⁴` (dev e.g. k=2 `+1.5e−3`→k=8 `+4e−5`) | orbit Haar-generic in 2-adic cylinders out to depth 11; **no residue-class bias** |
| conditional `P(D_j=d \| D_{j−1}=d′)` − marginal | all within `~1/√n` noise (largest `D_{j−1}=5→d=1: +0.011`, n=9235, ≈1σ) | consecutive `D` independent to noise; see §3 |
| `P(D_j \| parity of D_{j−1})` | identical to 3 dp (`d=1`: 0.5004 vs 0.5021) | the `3^{D_{j−1}}` algebraic coupling leaves **no parity footprint** |
| `D=1` run-length distribution | geometric `(1/2)^{L+1}` to 3 dp; mean 1.006; **max run 19** over 1.5·10⁵ runs | runs i.i.d.-geometric, self-limiting (Countdown) |
| consecutive run-length correlation | `−0.0025` vs noise `0.0026` | runs uncorrelated → no anti-persistence to exploit |
| cross-prime `corr(D_j, v₅(3o_j−1))` | `≈0` (from ADELIC, reconfirmed) | only the forced 3-adic coupling is non-trivial |
| `v₃(o_{j+1}) = D_j − 1` | 0 exceptions | exact, but a relabel (ADELIC §1a) |

**Verdict §1.** Every distinguishing statistic that *could* separate the quenched orbit from i.i.d. sits at
the noise floor. There is **no deviation from randomness to use as a lever.** This is fully consistent with
`QUENCHED_DATA` (Weyl sums inside the i.i.d. 95% band) and `ANNEALED_QUENCHED_DATA` (autocorr ≈ 0).

---

## 2. The one genuinely new exact object: the potential telescoping identity  [PROVEN]

Let `φ(o) = v₂(o−1)`. Facts (from `MINPROP` Countdown, here recombined): `D=1 ⟺ φ≥2` and a `D=1` step does
`φ→φ−1`; `D≥2 ⟺ φ=1` and a `D≥2` step **resets** `φ` to a fresh value `φ_new = φ(o_{next})`. Telescoping
`φ` over `N` induced steps (verified exactly, both endpoints `φ=1` so the boundary terms vanish):

> **(POT) [PROVEN].**  `Σ_{i≤K} φ_new^{(i)} = N + φ_N − φ_0`, where `K = #{D≥2 steps}` and `φ_new^{(i)}` are
> the depths freshly pulled in at each `D≥2` step. Since `φ_0 = v₂(26) = 1`, the right side is `≈ N`.
> `[verified]`: at `N=3·10⁵`, `Σφ_new = N` exactly, `K=149539`, `mean φ_new = N/K = 2.006`.

This re-expresses the kernel cleanly:

> **`freq(D≥2) = K/N = 1 / mean(φ_new)`** — even-density `≥ 1/3 ⟺ mean(φ_new) ≤ 2`, where `φ_new` is the
> "fresh 2-adic depth pulled in at each return to the `D≥2` boundary."

**Why (POT) is a clarifier, not a crack.** The *total* budget `Σφ_new = N + φ_N − φ_0 ≈ N` is **fixed by the
identity** regardless of how the orbit behaves. The only freedom is how that budget is distributed among the
`K` cycles. A bound `freq(D≥2) ≥ c` needs `mean(φ_new) ≤ 1/c`, i.e. the budget spread over `≥ cN` cycles. But
a single long `D=1` run (one giant `φ_new`) can absorb an `Ω(N)` share of the budget, collapsing `K`. The
only unconditional cap is `φ_new ≤ log₂(o−1) ≤ log₂ o_N ≈ 1.17·N` (integrality), which is far above any useful
threshold — exactly the o18 phenomenon ("trivial bound lands on the threshold, residual gap = the halt
event"). So **(POT) makes precise that the wall is the average size of the fresh depth, and that integrality
gives no nontrivial cap on it.**

---

## 3. Question 2 — is there a third encoding / combined (2,3)-adic invariant?  [answer: NO new one]

- **Conserved quantity:** none exists. The induced map is exact/Bernoulli on `ℤ₂*` (`INDUCED_MAP` E4,
  `[PROVEN]`), hence ergodic — no non-constant invariant function. Dead end by structure.
- **The actual third structural fact** (made explicit here): writing `o_j = 3^{D_{j−1}−1} m_{j−1}` with
  `m` odd and coprime to 3, the depth recursion is **`D_j = v₂(3^{D_{j−1}} m_{j−1} − 1)`**. Because `3` has
  multiplicative order `2^{k−2}` mod `2^k`, `3^{D_{j−1}} mod 2^k` genuinely depends on `D_{j−1} mod 2^{k−2}`,
  so there *is* an algebraic channel from `D_{j−1}` into `D_j`. **But** multiplying a Haar-random unit `m` by
  the fixed unit `3^{D_{j−1}}` returns a Haar-random unit, so the channel is invisible **iff `m_{j−1}`
  equidistributes** — which is the same genericity wall. The data (§1: conditional table and parity table at
  noise floor) confirms the channel is washed out. So `D_j ⊥ D_{j−1} ⟺ m_{j−1}` equidistributes: a clean
  reformulation, **not a weaker statement.**
- **(2,3) coupling `v₃(o_{j+1})=D_j−1`** is exact (ADELIC §1a) but a relabel: `freq(D≥2) = density{3∣o_j}`,
  same wall in `ℤ₃`. Cross-prime `v₅,v₇` correlations are `0`. **No missed invariant.**

---

## 4. Question 3 — is any unconditional `liminf even-density ≥ c > 0` reachable for o₀=27?  [answer: NO]

This is the most important question and the answer is a firm **no — the same wall blocks every `c>0`**, with a
sharp boundary:

- **`[PROVEN]` (the one unconditional positive fact):** `D≥2` happens **infinitely often**. Each `D=1` run is
  finite (Countdown: length `= φ(start)−1 < ∞` for any integer orbit `≠ 1`), the orbit is infinite, hence
  infinitely many runs end, hence infinitely many `D≥2` steps. **This gives `liminf even-density ≥ 0` only
  (`c=0`).**
- **`[PROVEN]` no `c>0` from elementary means:** by (POT), `c>0` requires `mean(φ_new)` bounded, i.e. an
  unconditional cap on the *average* fresh depth. The per-step cap is `φ_new ≤ log₂ o_N = Θ(N)` — a single run
  may be `Ω(N)` long, so `K` may be `O(1)` and `freq(D≥2)→0`. Integrality bounds each run finite but **not
  bounded-on-average.**
- **Why this is structural, not lack of effort:** the obstruction is precisely the halting fixed point
  `δ₁` (`o=1`, `D≡1`) identified by meta-theorem (i) (`MINPROP` F3): `min over T-invariant μ of freq(D≥2) = 0`,
  attained at `δ₁`. So an all-measures (structure-only) lower bound `freq(D≥2) ≥ c` is **false** for *every*
  `c>0`. A single-orbit `c>0` therefore requires ruling out the empirical measure of `o₀=27` drifting
  (2-adically) onto `δ₁` — and that drift is approached through **long `D=1` runs** (2-adic proximity to 1),
  *not* archimedean proximity, so the orbit's growth/Dual-Repulsion (an archimedean fact) does **not** exclude
  it. Effective exclusion = single-orbit equidistribution = the open kernel.
- **No finite-computation-plus-effective-tail:** the required "tail" is exactly an effective bound on how
  often the orbit enters `o≡1 mod 2^k` for large `k` (the long-run depths) — i.e. an effective equidistribution
  tail, which is the missing object. There is none.

> **Result.** Even the weakest positive lower bound `liminf even-density ≥ c > 0` is **not reachable** for the
> specific orbit by any current tool; `c=0` ("D≥2 infinitely often") is the exact boundary of the
> unconditional. The wall is not specific to the threshold `1/3` — it is the `δ₁` obstruction, which sits at
> `c=0`.

---

## 5. Question 4 — a different reduction to a solved problem?  [answer: NO]

Re-scanned the equivalent forms. None connect to a solved problem:
- `mean D ≥ 3/2`, `freq(o≡3 mod4) ≥ 1/2`, `freq(D≥2)+freq(D≥3) ≥ 1/2`, 3-adic `density{3∣o}+density{9∣o}≥1/2`,
  independence form (`u_j ⊥ e_j`), and now `mean(φ_new) ≤ 2` (§2) — all are the **same** single-orbit
  equidistribution.
- **Explicit conjugacy view:** the Lagarias 2-adic conjugacy sends the kernel to "the explicit 2-adic point
  `Q(27)` is normal for the Bernoulli shift" — a hard *unsolved* instance (the analogue of "is π normal?"),
  with no solved cousin to borrow from.
- **Second-moment / large-sieve route** (bound `Σ_h|S_N(h)|²` to get smallness for a.e. `h`, then specialise):
  fails for the same reason — the difference set `(3/2)^n−(3/2)^m` is not equidistributed because `3/2` is not
  an integer base; this is the structural obstruction `NONPISOT` Link C names, and it kills the variance method.

---

## 6. Honest ledger — real leads vs dead ends

**Genuine (already-known) frontier — the ONLY live analytic lead:**
- Effective `o(N)` (ideally `N^{1−ε}`) bound on the **quenched** Weyl sum `Σ_{n<N} e(h·4·(3/2)^n)` for the
  single orbit = effective `{(3/2)^n}` equidistribution = AEV Conj 1.6 floor-mirror fragment / Mahler. This is
  unchanged and is the real next computation/lemma (a van der Corput / Vinogradov treatment of `(3/2)^n`,
  whose lacunary obstruction is known). `[OPEN]`

**Clarifying assets banked this session (confirm the wall, not cracks):**
- **(POT)** `Σφ_new = N + φ_N − φ_0`, giving `freq(D≥2) = 1/mean(φ_new)` and the proof that **the wall extends
  to every `c>0`** (§2, §4). `[PROVEN]`
- The depth recursion `D_j = v₂(3^{D_{j−1}} m_{j−1} − 1)` and the exact statement
  `D_j ⊥ D_{j−1} ⟺ m_{j−1}` equidistributes (§3). `[PROVEN]` reformulation.

**Dead ends (checked and closed this pass):**
- Conditional/parity dependence of consecutive `D`: at noise floor — no lever (§1, §3).
- Run-length anti-persistence: uncorrelated — no averaging lever (§1).
- Residue-class bias / special-epoch non-genericity (Antihydra has no o18-style carry-defect epochs in the
  relevant coordinate): none found (§1).
- Conserved (2,3)-adic invariant / third encoding: none (ergodicity; coupling is a relabel) (§3).
- Unconditional `c>0` via integrality / growth / finite-plus-tail: blocked by `δ₁` (§4).
- Reduction to a solved problem; second-moment method: fail (§5).

**One-line verdict.** The fresh-eyes pass found **no unexploited signal**. The data is maximally
pro-non-halting and statistically identical to i.i.d.; the new potential identity sharpens *why* — the wall is
the average fresh 2-adic depth, blocked by `δ₁` for every positive `c`, and reachable only by the open
effective single-orbit equidistribution (AEV/Mahler). Soundness intact; zero claims upgraded.
