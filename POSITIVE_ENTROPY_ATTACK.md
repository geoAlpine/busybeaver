# Positive 2-adic measure entropy of the Antihydra limit measure — attack & audit (2026-06-29)

*Direct assault on `h_μ(M₂) > 0` for the empirical limit measure `μ` of the single `⟨3/2⟩`-orbit `c₀=8,
c_{n+1}=⌊3c_n/2⌋` on the `(2,3)`-solenoid `X=(ℝ×ℚ₂×ℚ₃)/ℤ[1/6]`. The point of leverage: via Rudolph–Johnson,
`AIU + h_μ(M₂)>0 ⟹ μ=Haar ⟹ (K)`. We VERIFIED the orbit has FULL subword complexity (`p(ℓ)=2^ℓ`, topological
entropy `log2`); but topological entropy is a `sup` over invariant measures, so the SPECIFIC `μ` could still have
small or zero MEASURE entropy. This note asks whether `h_μ(M₂)>0` is provable, lower-boundable from PROVEN
structure, or itself (K)-hard. SOUNDNESS PARAMOUNT: every claim labelled; (K) is NOT proven; NO label upgraded.
Numerics `/Users/aokiyousuke/quantum-ecc/.venv/bin/python scratchpad/pos_entropy.py` (exact big-int, N=10⁵, <2s).
NOT committed.*

---

## 0. One-line verdict

**`h_μ(M₂)>0` is NOT provable from any PROVEN structure — it is a NECESSARY, (K)-hard sub-fact of (K).** The
measured 2-adic entropy rate is **positive and indistinguishable from `log2`** (`ĥ = 1.00 ± 0.02` bits/level
through every fully-sampled scale; the apparent decay at deep scales is a pure undersampling artifact matching
`1−e^{−N/2^k}` to ≤0.2%). As a *logical proposition* `h_μ(M₂)>0` is **strictly weaker** than (K) (a skew-Bernoulli
or maximal-entropy measure `≠`Haar could have positive entropy); but **for THIS orbit no proof of positivity is
known and none follows from proven structure**, because every proven lower bound is on the **unweighted** cell
count `p(ℓ)` (linear ⇒ topological entropy `≥0` only), whereas measure entropy needs a lower bound on the
**frequency-weighted** count `Σ−f log f` (an exponential cell-spreading = a (K)-character equidistribution fact).
**The exact gap: proven `linear unweighted count` vs unproven `exponential frequency-weighted count`.**

---

## 1. Precise definitions — topological vs measure, and which entropy RJ needs [PROVEN-in-lit / DEFINITION]

Write `r_n = c_n mod 2` (the parity / Antihydra feedback bit) and, for the limit measure `μ` (a weak-* limit of
`μ_N=(1/N)Σ_{n<N}δ_{Aⁿ8}`, `A=×(3/2)`):

- **Subword (topological) entropy.** `p(ℓ) = #{length-ℓ parity windows} = #{c_n mod 2^ℓ}` (the two counts are
  EQUAL by the PROVEN coding bijection `φ_ℓ:ℤ/2^ℓ→{0,1}^ℓ`, `LIMIT_THEOREM §3″`). `h_top = lim_ℓ (1/ℓ)log₂ p(ℓ)`.
  Observed `p(ℓ)=2^ℓ` to `ℓ=16` ⟹ `h_top = log2` (1 bit/level). This governs the **sup over invariant measures**,
  NOT `μ`. [OBSERVED full; `h_top≥0` from the linear floor is [PROVEN]; `h_top=log2 ⟺` (K)]
- **Measure entropy** `h_μ`. The exponential growth rate of the **frequency-weighted** cell count:
  `H_ℓ := −Σ_{a∈ℤ/2^ℓ} f_ℓ(a) log₂ f_ℓ(a)` (`f_ℓ(a)=` asymptotic frequency of `c_n≡a mod 2^ℓ`), and
  `h_μ = lim_ℓ (1/ℓ) H_ℓ`. The variational principle gives only `h_μ ≤ h_top` — **vacuous here** since
  `h_top=log2`. [PROVEN bound; vacuous]
- **The (K)-relevant entropy and the bijection coincidence.** RJ on the solenoid reads the archimedean place:
  `h_Haar(M₂)=log⁺|2|_∞=log2`, `h_Haar(A)=log⁺|3/2|_∞+log⁺|3/2|₂=log(3/2)+log2=log3`. The **bit/2-adic** information
  (the (K) object) is carried by the `ℚ₂`-factor, which `A` EXPANDS (`|3/2|₂=2`); its contribution to `h_μ(A)` is
  `log⁺|3/2|₂=log2`. Because the PROVEN bijection identifies the **parity time-window** (an `A`-object) with the
  **residue `c_n mod 2^ℓ`** (a `×2`/bit-object), the SAME number `H_ℓ` estimates both the `ℚ₂`-factor entropy of
  `A` and the bit-process entropy under `M₂=×2`. For Haar both equal `log2`, and on a host-invariant ergodic
  measure they **vanish together** (`LIMIT_MEASURE_ENTROPY §2(iii)`). So `lim_ℓ H_ℓ/ℓ` is the honest numeric proxy
  for the (K)-relevant 2-adic entropy. [PROVEN-in-lit, Lind–Schmidt–Ward / Yuzvinskii; bijection PROVEN]

> Crux distinction restated: `h_top = log2` (proven-modulo-(K) full **count**); `h_μ` needs the **frequency
> weights**, which the variational principle never sees. Full topological entropy does **NOT** imply `h_μ>0`.

---

## 2. Numerics — the entropy RATE is positive (≈log2), no drift to 0 in the sampled range [OBSERVED]

`scratchpad/pos_entropy.py`, exact big-int, `c_n mod 2^k`, plugin Shannon `H_k` (bits), per-bit conditional
`h_k=H_k−H_{k−1}`, Miller–Madow bias-corrected rate `H_MM/k`, fill `m/2^k` vs Poisson prediction `1−e^{−N/2^k}`:

```
 N=10⁵     k   distinct  2^k     H_k     H_k/k   h_k     H_MM/k   fill_obs  fill_pred
            8     256      256   7.998   1.000   0.999   1.000    1.0000    1.0000
           11    2048     2048  10.985   0.999   0.993   1.000    1.0000    1.0000
           13    8192     8192  12.939   0.995   0.969   1.000    1.0000    1.0000   <- last fully-filled
           16   51205    65536  15.450   0.966   0.711   0.989    0.7813    0.7826
           18   83067   262144  16.254   0.903   0.305   0.936    0.3169    0.3171
           22   98733  4194304  16.584   0.754   0.024   0.786    0.0235    0.0236
```
- **Bijection verified exactly**: `H(parity k-windows) = H(residue mod 2^k)` to `0.00e+00` (k=8,12). The
  time-shift (`A`) and bit (`×2`) block entropies are literally the same sequence `H_k`. [OBSERVED — confirms §1]
- **Per-bit entropy ≈ 1 bit = log2** through every reliably-sampled level (`h_k=0.969` at k=13, plugin;
  bias-corrected `H_MM/k=1.000`). **No deficit** — the signature of FULL / positive entropy (2-adic dimension 1).
- **The decay of `H_k/k` and `h_k` for `k≳14` is a PURE finite-sample artifact**, not an entropy deficit: the
  fill `m/2^k` matches `1−e^{−N/2^k}` (uniform sampling) to **≤0.2%** at every deep level (k=16: 0.7813 vs 0.7826;
  k=18: 0.3169 vs 0.3171). Once `2^k≳N` you cannot see more than `≈log₂N` bits; the rate must roll off for ANY
  measure, Haar included. Miller–Madow lifts the corrupted levels back toward 1.0 (k=16: 0.966→0.989).
- **Best estimate (deepest trustworthy level, N=10⁵, k=13):** `ĥ_μ(bit) = 1.00 ± 0.02` bits/level. `H_1=H(P(even))
  =1.0000` bit, `P(even)=0.5016`. The orbit's residues mod `2^k` are **statistically indistinguishable from exact
  uniform (Haar) sampling** at every level. [OBSERVED — this is the equidistribution evidence read on the entropy
  axis; it is NOT a proof: the SAMPLE rate ≈log2 does not certify the LIMIT `lim_ℓ`, and proving that limit IS (K).]

---

## 3. Does any PROVEN structure lower-bound `h_μ`? — NO; the exact obstruction [PROVEN obstruction]

| candidate PROVEN structure | what it proves | does it force `h_μ>0`? | why / exact obstruction |
|---|---|---|---|
| complexity floor `p(ℓ)≥1.71ℓ` (`LIMIT_THEOREM §3″`) | linear **unweighted count** | **NO** | even if those `1.71ℓ` cells were equi-weighted, `H_ℓ ≥ log₂(1.71ℓ) ⟹ H_ℓ/ℓ ≥ (log₂ℓ)/ℓ → 0`. A linear count lower-bounds `h_top≥0` only; it gives `h_μ≥0`, nothing more. **This is the exact obstruction.** |
| orbit growth rate `≈0.585n` (`log₂c_n≈n·log₂(3/2)`) | the **support**: `≈0.585n` significant bits / `≥min(N,·)` distinct residues by time `n` | **NO** | bounds the number of cells the orbit can touch (a topological/support quantity), not how the FREQUENCY mass spreads. A deterministic low-complexity sequence grows at the same rate with zero measure entropy. |
| annealed transducer gap `½`, unique uniform fixed point (`NEWMATH_DIAGONAL_RENORM §3.1`) | the i.i.d.-carry SURROGATE contracts to Bernoulli(½), entropy `log2` | **NO (for the orbit)** | positive entropy holds for the **annealed** (Bernoulli-carry) model *by construction*; the quenched orbit uses its OWN deterministic carry `γ_n^{(k)}`. "Quenched inherits annealed" = R-GEN = (K). The gap between proven annealed positivity and the orbit is the Mahler wall. |
| non-Pisot no-atom spectrum `|3/2|₂=2>1` (`DIAGONAL_RENORM §3.2`) | no atomic/Pisot/sofic `A`-fixed point | **NO** | rules out the **zero-dimensional** (atomic) extreme, i.e. excludes `h=0` *via concentration on a finite orbit*; it does NOT exclude positive-but-fractal or `0<dim<1` measures, and gives no positive lower bound on `H_ℓ/ℓ`. |
| H₂ even-density floor / `liminf(1/N)Σ(−1)^{c_n}≥−1/3` | — | **NO (and it is (K) itself)** | the `≥1/3` even-density bound IS (K) (`WEAPONS_AUDIT §1`), not a proven input; even granted, it bounds only `H_1`, not the rate. |

> **Net [PROVEN].** Proven structure forces `h_μ ≥ 0` only. The honest obstruction is sharp: all proven lower
> bounds control the **unweighted** residue count `p(ℓ)` (linear ⇒ rate 0 even if equi-weighted), while `h_μ>0`
> requires an **exponential lower bound on the frequency-weighted count** `Σ−f_ℓ log f_ℓ` — equivalently a positive
> lower bound on the per-bit conditional entropy `h_k` that SURVIVES `k→∞`. No such bound is proven; the numerics
> show `h_k≈1` only where `2^k≪N`, i.e. exactly where the statement degenerates to a finite-sample observation.

---

## 4. `h_μ(M₂)>0` vs (K): strictly weaker proposition, but (K)-hard for THIS orbit [PROVEN logic]

- **(K) ⟹ `h_μ(M₂)>0`.** (K) `⟺ μ=`Haar, and `h_Haar(M₂)=log2>0`. So positive entropy is **NECESSARY** for (K).
  [PROVEN]
- **`h_μ(M₂)>0` ⟹̸ (K) (strictly weaker as a proposition).** Positive entropy `≠` Haar. The orbit-closure subshift
  has `h_top=log2`; its **measure of maximal entropy** (or any skew-Bernoulli`(p)`, `p≠½`, with entropy `H(p)>0`)
  is a positive-entropy invariant measure that is **not** Haar. Nothing in `h_μ>0` alone pins `μ=`Haar. So as a
  standalone logical statement `h_μ(M₂)>0` is **strictly weaker** than (K). [PROVEN — counterexample class]
- **But it closes (K) with one more open input, via the PROVEN RJ.** `μ` is `A`-invariant [PROVEN, Krylov–
  Bogolyubov] and non-atomic [PROVEN, 2-adic repulsion]. Then **`AIU + h_μ(M₂)>0` ⟹ (Rudolph–Johnson) μ=Haar ⟹
  (K)**. So `{AIU ∧ h_μ>0}` is *sufficient* for (K) (and (K) implies both): the pair is **(K)-equivalent**, even
  though each conjunct alone is weaker. [PROVEN reduction, modulo the two OPEN inputs]
- **For the SPECIFIC orbit, positivity is not known to be easier than (K).** To PROVE the empirical `μ`'s entropy
  is positive you must lower-bound the frequency-weighted cell spreading exponentially (§3) — an equidistribution
  statement of the SAME character as (K), with **no proven shortcut**. And `h_μ=0` would itself **refute** (K)
  (`μ≠`Haar). So positivity is sandwiched: weaker than (K) logically, but a necessary, (K)-hard sub-fact in
  practice, with no proven separation in difficulty. [PROVEN that necessary & that zero refutes (K); positivity OPEN]

---

## 5. Honest ledger

| item | label |
|---|---|
| `h_top(parity subshift)=log2` (full count `p(ℓ)=2^ℓ`); `h_top≥0` from linear floor | [OBSERVED full; `≥0` PROVEN; `=log2 ⟺`(K)] |
| `h_μ ≤ h_top`, vacuous here (`=log2`); variational principle cannot deliver `h_μ` | [PROVEN] |
| bijection: `H(parity k-windows)=H(c_n mod 2^k)` (the `A`- and `×2`-block entropies coincide) | [PROVEN coding bijection; OBSERVED diff 0] |
| measured 2-adic entropy rate `ĥ=1.00±0.02` bits = `log2`; per-bit `h_k≈1`; deep-`k` decay = `1−e^{−N/2^k}` ≤0.2% | [OBSERVED — equidistribution evidence, not proof] |
| PROVEN structure forces `h_μ≥0` ONLY; exact obstruction = unweighted-linear vs weighted-exponential count | **[PROVEN obstruction]** |
| `h_μ(M₂)>0` is NECESSARY for (K) (`h_Haar(M₂)=log2`) | [PROVEN] |
| `h_μ(M₂)>0` is STRICTLY WEAKER than (K) as a proposition (max-entropy/skew-Bernoulli `≠`Haar) | [PROVEN] |
| `AIU ∧ h_μ(M₂)>0 ⟹ (K)` via PROVEN Rudolph–Johnson; the pair is (K)-equivalent | [PROVEN reduction, modulo 2 OPEN inputs] |
| `h_μ(M₂)=0 ⟹ μ≠Haar ⟹ (K) false` (zero entropy not provable without refuting (K)) | [PROVEN] |
| `h_μ(M₂)>0` for THIS orbit (positivity) | **[OPEN / (K)-hard]** |
| (K) itself | **[OPEN]** = Mahler 3/2 / AEV Conj 1.6 at α=8 |

**Make-or-break disposition.** `h_μ(M₂)>0` is the correctly-stated live target (it buys the *proven* RJ given AIU),
the data places it firmly positive (≈log2), and it is a NECESSARY consequence of (K). But it is **not provable from
proven structure**: the only proven cell-count lower bounds are unweighted and linear, yielding measure-entropy
rate `≥0` and nothing more, while positivity demands an exponential frequency-weighted spreading bound of (K)
strength. It is strictly weaker than (K) as a proposition yet (K)-hard to establish for the specific orbit. The
exact gap is **unweighted-count (proven linear) vs frequency-weighted-count (unproven exponential)** — equivalently
a per-bit conditional entropy bounded below uniformly in `k`, which the literature provides for the annealed
surrogate but not the quenched orbit.

---

## Sources
- Rudolph, *×2 ×3 invariant measures and entropy*, ETDS (1990); Johnson (1992); solenoid form arXiv:2101.11120.
  [PROVEN-in-lit] — positive-entropy ergodic `⟨×2,×3⟩`-invariant ⟹ Haar.
- Lind–Schmidt–Ward, entropy of solenoid/`ℤ^d` automorphisms `h(×u)=Σ_v log⁺|u|_v`. [PROVEN-in-lit]
- Furstenberg (1967) `×2,×3` conjecture (zero-entropy case). [OPEN]
- Walters, *Ergodic Theory* (variational principle `h_top=sup_ν h_ν`). [PROVEN-in-lit]
- Repo: `LIMIT_MEASURE_ENTROPY.md` (the sign correction: full complexity, zero entropy = (K)-false regime),
  `NEWMATH_SYNTHESIS.md`, `NEWMATH_DIAGONAL_RENORM.md` (annealed gap ½, non-Pisot no-atom), `LIMIT_THEOREM.md §3″`
  (coding bijection + `p(ℓ)≥1.71ℓ` floor), `WEAPONS_AUDIT_2026-06-29.md` (kernel funnel, H₂ floor = (K)).
- Numerics: `scratchpad/pos_entropy.py` (exact big-int, N=10⁵, <2s): bijection diff 0; per-bit `h_k≈1`,
  `H_MM/k=1.000` through last fully-filled level k=13; deep-`k` rolloff matches `1−e^{−N/2^k}` to ≤0.2%;
  `ĥ=1.00±0.02` bits = `log2`.

No machine decided. No label upgraded.
