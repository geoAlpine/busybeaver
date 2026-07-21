# D9 probe — lacunarity of the deep-return time set (2026-07-22)

*Numerical probe of `BB6_PROOF_HANDLES_2026-07-22.md` §D9, the only new idea in that document.
Everything below is `[OBSERVED]` — measurement, not proof. No label upgraded, no machine decided.*

**Verdict: PREMISE FALSE.** D9's forcing step ("a divergent second moment forces the deep-return
time set to be near-lacunary") is not merely unproven — it is **backwards**, and refuted three
independent ways below. A secondary, independent obstruction (§5) would kill the proposal even if
the premise held. Recommended action: **add to the trap list** (`§2` of the handles document).

Scripts: `d9_orbit.py` (orbit + budget identity), `d9_analyze.py` (T_L geometry + restricted sums),
`d9_adversary.py` (the decisive premise test), `d9_compare.py` (real-vs-surrogate percentiles).
Data: `d9_orbit.npz`, log `d9_analyze.out`.

---

## 1. Instrument check — the budget identity is EXACT `[OBSERVED, exact]`

Orbit `c₀ = 8`, `c → ⌊3c/2⌋`, run to **n = 2,500,000 c-steps** (c has 1,462,414 bits), giving
**J = 1,250,979 induced odd steps**, `max D = 22`.

The identity verifies **exactly** at 177 geometrically-spaced checkpoints, with the clean uniform
definition `D_i := v₂(3c_i − 1)` at *every* c-step (this is automatically 0 on even `c_i`, since
`3c−1` is odd there):

> `Σ_{i<n} D_i = n + v₂(c_n) − v₂(c₀)`   — 177/177 exact, 0 failures.

Final: `n = 2500000`, `Σ D = 2499997 = 2500000 + 0 − 3`. ✓
(Telescoping proof: `v₂(c_{i+1}) − v₂(c_i) = D_i − 1` at every step.)

Independent instrument checks also passed: the modular tracker `u ← (3u − parity)·2⁻¹ mod m` matches
direct big-int reduction on all odd visits (100k-step cross-check), and the depth law matches
`P(D=d) = 2^{−d}` to 3 digits out to `d = 15` (`mean D = 1.998432`, Haar value 2).

**The instrument is sound. The budget is real. The inference drawn from it is not.**

---

## 2. Refutation A (arithmetic) — the budget caps density HARMONICALLY, nowhere near lacunary

From `Σ_{j<J} D_j = 2J + o(J)` and `D_j ≥ L` on `T_L`, all the first moment can give is

> `|T_L ∩ [1,J]| ≤ 2J / L`   — density `≤ 2/L`.

That is a **harmonic** cap. Lacunary means density 0 with `|T_L ∩ [1,J]| = O(log J)`. The gap is not
a constant factor, it is a change of order:

| L | observed density | budget cap `2/L` | cap/observed |
|---|---|---|---|
| 3 | 2.494e-01 | 6.667e-01 | 2.7× |
| 7 | 1.564e-02 | 2.857e-01 | 18.3× |
| 10 | 1.982e-03 | 2.000e-01 | 100.9× |
| 13 | 2.486e-04 | 1.538e-01 | 618.8× |

Two things follow, both fatal:

1. **The budget is loose, not binding.** It permits 600× more deep returns than actually occur. The
   observed sparsity is produced by the *depth law's geometric tail*, which is exactly the `(K)`-side
   fact one is trying to prove. **The budget contributes nothing to the sparsity.**
2. **Positive density ⇒ never lacunary, for any fixed `L`.** `T_L` has density `≈ 2^{−(L−1)} > 0`;
   lacunary sets have density 0. At `J = 1,250,979` a genuinely lacunary set admits at most
   **20** elements (ratio 2), **147** (ratio 1.1), or **1411** (ratio 1.01). Observed `|T_3| = 311,976`;
   even `|T_13| = 311`. Measured `min ratio t_{i+1}/t_i` is `1.000001`–`1.000003` for every `L ≤ 13`;
   `median ratio ≤ 1.0049`. **Nothing here is remotely lacunary at any threshold.**

---

## 3. Refutation B (decisive) — E[K²]=∞ makes the time set DENSER, not sparser

This is the crux and it needs no orbit data. D9 asserts that within the budget-legal class, a
*divergent* second moment *forces* sparsity of `T_L`. Constructed directly (`d9_adversary.py`): iid
`P(D=d) ∝ d^{−s}` with `s = 2.478483`, giving `E[D] = 2.000000` (budget-matched) and
`E[D²] = ζ(s−2)/ζ(s) = ∞` (verified drifting: `E[D²]` over the first 200k / 500k / 1M / 2M samples =
148.5 / 171.7 / 219.4 / 293.2 — no stabilisation ✓). Its tail is `P(D ≥ L) ~ L^{−1.478}`.

`T_L` density, same J = 2,000,000, cap-legal adversary vs the Haar/geometric law:

| L | E[D²]=∞ adversary | geometric `2^{−(L−1)}` | adversary / geometric |
|---|---|---|---|
| 6 | 3.975e-02 | 3.125e-02 | 1.3× |
| 9 | 2.100e-02 | 3.893e-03 | 5.4× |
| 12 | 1.349e-02 | 4.935e-04 | **27×** |
| 100 | 5.800e-04 | ~1e-30 | astronomically denser |

`min ratio = 1.000001` and `median ratio ≤ 1.0013` for the adversary at every `L` up to 100.

> **The implication runs the wrong way.** Sparsity of the deep-return time set is a consequence of a
> *light* (geometric) tail. A divergent second moment is precisely the statement that the tail is
> *heavy*, i.e. that deep returns are **more** frequent at every threshold. The surviving adversary
> class is the *least* lacunary member of the budget-legal family, not the most. D9's forcing step
> conflates "deep excursions are individually expensive" (true — the run-cap) with "deep excursions
> are collectively rare" (false under E[K²]=∞, which is the whole point of that adversary).

This kills D9 independently of any Antihydra data.

---

## 4. Refutation C (empirical) — the real orbit's T_L is statistically indistinguishable from iid

The crux test the task specified. `d9_compare.py`: percentile of each real statistic within 200
matched iid-geometric surrogate draws (50 = dead centre of the null; <2.5 or >97.5 = distinguishable).
Statistics: `|T_L|`, `min ratio`, `median ratio`, `max gap`, count-dispersion (variance/mean over
1000 blocks; 1.0 = Poisson).

```
  L      count       rmin       rmed     maxgap       disp
  3        7.0        3.5       30.5       74.5       73.0
  4        2.5       64.5       36.5       79.0       78.0
  5       24.0       75.0       20.0       72.5       97.5
  6       54.5       82.5       61.0        2.0       82.5
  7       58.0       95.5       45.5       22.0       87.0
  8       65.0       57.5       63.0       50.5        3.0
  9       80.0       20.5       12.5       55.0       10.0
 10       74.5       68.0       61.0       61.0       51.5
 11       91.5       79.0       75.0       19.0       18.0
 12       72.0       41.5       26.0       20.0       56.5
 13       64.5       14.5       21.0       26.0       80.0
```

55 tests, percentiles uniform on [0,100]; 4 land outside [2.5, 97.5], against ~2.75 expected by
chance. **No signal.** Gap-law KS statistics against `Geom(2^{−(L−1)})` likewise sit at the
discreteness floor (`KS·√n → 0.5–0.7` for `L ≥ 8`), matching surrogates. Dispersion `≈ 1.0` — the
deep-return times are Poisson-like, neither clustered nor repelling.

> The observed sparsity of the deep-return set on the real Antihydra orbit is **exactly
> geometric-tail sparsity**. It is not budget-forced, and it carries no geometry beyond what an iid
> coin flip produces. Per the task's own criterion, **the forcing premise is false**.

The one genuinely lacunary-looking set is the **record-depth times**:
`j = 0, 24, 170, 173, 1826, 3553, 147466, 267697` (`D = 4, 8, 9, 11, 15, 16, 17, 22`), `min ratio 1.018`.
But that set has `O(log J)` elements by construction — see §5.

---

## 5. Independent obstruction — restriction DESTROYS cancellation; and the sparse set is useless to D1/D2

Even granting the premise, the proposed payoff does not exist.

**(a) Measured: no excess cancellation on `T_L`.** Additive characters `e(a·c_j/m)` for
`m ∈ {5,7,11,13,17,19,23}`, `a = 1`, shifts 0 and 1 (shift 1 probes the real dependence
`o_{j+1} = 3^{D_j−1}(3o_j−1)/2^{D_j}`, where the residue genuinely does depend on `D_j`).
112 tests, restricted `|S|/√n` vs a matched-size random-subset null (20 draws each):

- mean `z = 0.002`, sd `z = 1.077`, `max|z| = 2.37`, `frac |z|>2 = 0.071` (null 0.046), `frac |z|>3 = 0`
- mean restricted `|S|/√n = 0.865` vs null mean `0.867`

**Zero effect**, at either shift. (`m = 3` excluded: `c ≡ 0 mod 3` from step 1 onward — degenerate.)

**(b) Restriction is strictly counterproductive.** The FULL sums over all `J = 1,250,979` induced
steps already exhibit cancellation far beyond square-root:

| m | `\|S_full\|` | `\|S\|/√J` | `\|S\|/J` |
|---|---|---|---|
| 5 | 84.9 | **0.076** | 6.8e-05 |
| 23 | 413.0 | 0.369 | 3.3e-04 |
| 13 | 696.2 | 0.623 | 5.6e-04 |

Restricted sums sit at the square-root barrier (`≈ 0.87`). So the restriction **throws away** the
cancellation the full sum already has. Whatever mechanism produces `|S_full|/J ~ 10⁻⁴` is not
localised on the deep-return set.

**(c) Structural: the sparse-set route cannot reach D1 or D2 even in principle.** Theorem E (D1)
requires a bound on the **full** sum `|Σ_{i<N} ψ(c_i)| ≤ C·N^{1−δ}`. A bound on a sparse subset `S`
gives nothing about the complement. The only decomposition available is
`Σ_full = Σ_L Σ_{j: D_j = L}`, and **every** piece has positive density — one is back at the original
problem with extra bookkeeping. Conversely the one set that *is* near-lacunary (record times) has
`|S| = O(log J)`, for which `|Σ_S| ≤ |S| = O(log J)` is trivially true and controls nothing.
Salem–Zygmund-class tools need the lacunary set to *carry* the sum; here it carries a
`log J / J` fraction of it.

---

## 6. Verdict and trap-list entry

**PREMISE FALSE + independently non-transferable.** D9 is closed.

Proposed trap-list wording for `BB6_PROOF_HANDLES_2026-07-22.md §2`:

> **Lacunary restriction of the character sums to the deep-return time set (D9, probed & closed
> 2026-07-22, `D9_LACUNARY_PROBE_2026-07-22.md`).** Three independent failures. (i) The first-moment
> budget `Σ_{i<n} D_i = n + v₂(c_n) − v₂(c₀)` (re-verified exact to n = 2.5×10⁶) caps the depth-`L`
> return density only *harmonically*, at `2/L` — 600× looser than observed at L=13, and a cap
> incompatible in order with lacunarity (`O(log J)` counting). (ii) The forcing implication is
> **inverted**: a budget-legal `E[K²]=∞` law (`P(D=d) ∝ d^{−2.478}`) has `T_L` density `~ L^{−1.478}`,
> up to 27× *denser* than geometric at L=12 — the surviving adversary is the *least* sparse
> budget-legal law, not the most. Sparsity comes from a light tail, i.e. from `(K)` itself.
> (iii) The real orbit's `T_L` is statistically indistinguishable from an iid-geometric surrogate on
> count / min-ratio / median-ratio / max-gap / dispersion (55 percentile tests, uniform), and
> restricted character sums show no excess cancellation (112 tests, mean `z = 0.002`, sd 1.08) —
> indeed restriction *destroys* the beyond-square-root cancellation the full sums already exhibit
> (`|S|/J ~ 10⁻⁴` at m=5). This is the same failure mode as the **adelic-budget no-go**
> (budget-counting is clustering-indifferent) — the honest risk (i) named in D9's own text — now
> confirmed numerically: the time-set geometry contains no information the budget sum did not.

**What survives.** Nothing of the mechanism. Two byproducts worth keeping:
- The clean uniform form of the budget identity, `D_i := v₂(3c_i − 1)` at *every* c-step with the
  one-line telescoping proof, verified exact to `n = 2.5×10⁶` (was previously stated only at the
  induced level).
- The unexplained **beyond-square-root cancellation of the full low-modulus sums**
  (`|S|/J ≈ 6.8×10⁻⁵` at m=5 over 1.25M terms). This is the D1/Theorem-E quantity itself, observed
  with enormous margin — it belongs with the other measured-margin observations (D1/D2/D3), not with
  D9. It is *not* evidence for D9; if anything it is evidence against, since the cancellation lives
  on the full sum and vanishes under restriction.

**Honest limits of this probe.** J = 1.25×10⁶ induced steps, `max D = 22`, thresholds `L ≤ 13`,
low moduli only, additive characters only. A finite computation cannot exclude structure at depth
scales beyond those reached. But refutations A and B (§2, §3) are *not* finite-data arguments: they
are order-of-magnitude/definitional and hold for all J.
