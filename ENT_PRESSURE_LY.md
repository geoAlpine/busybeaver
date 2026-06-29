# ENT via pressure / large-deviation / Ledrappier–Young — lower-bounding `h_μ` (2026-06-29)

*WEAPONS_AUDIT style. Target: an UNCONDITIONAL positive lower bound `h_μ(M₂) ≥ c > 0` for the empirical limit
measure `μ` of the single `⟨3/2⟩`-orbit `c₀=8, c_{n+1}=⌊3c_n/2⌋` on the `(2,3)`-solenoid
`X=(ℝ×ℚ₂×ℚ₃)/ℤ[1/6]`, via (1) Ledrappier–Young with the explicit Lyapunov exponents, (2) pressure /
large-deviation, (3) the proven Gibbs–Markov renewal. SOUNDNESS PARAMOUNT: every claim labelled; (K) NOT
claimed; distinguish TOPOLOGICAL entropy (sup over measures) from the MEASURE entropy of the SPECIFIC `μ`;
no label upgraded. Numerics `/Users/aokiyousuke/quantum-ecc/.venv/bin/python scratchpad/ent_pressure_ly.py`
(exact big-int, N≤10⁵, <5s). NOT committed.*

---

## 0. One-line verdict

**Verdict (b): only ANNEALED / TOPOLOGICAL lower bounds exist; an unconditional positive lower bound
`h_μ(M₂) ≥ c > 0` is NOT provable from any proven structure, and the target is (K)-hard.** Ledrappier–Young
pins ENT to a single conditional-dimension number that is `> 0`; pressure gives only the (vacuous) UPPER bound
`h_μ ≤ h_top = log2`; large-deviation and the proven Gibbs–Markov renewal both deliver positivity **only for
Haar/SRB-typical points** — never the specified Haar-null seed `8`. Every proven structural input
(`p(ℓ)≥1.71ℓ`, growth `0.585n`, foothold depth `~log₂N`, even global non-atomicity) controls an **unweighted /
support / annealed** quantity, all of which yield measure-entropy rate `≥0` and **nothing more**. The exact
obstruction is unchanged and sharp: **unweighted/annealed count (proven) vs frequency-weighted/quenched count
(unproven = equidistribution = (K)).** No machine decided. No label upgraded.

---

## 1. Ledrappier–Young on the solenoid — exact formula + PROVEN Lyapunov exponents [PROVEN-in-lit]

`A=×(3/2)=M₃M₂^{-1}` is an **affine automorphism** of `X`, so its derivative is constant and the Lyapunov
exponents are the logs of the place-wise dilations — **explicit, measure-independent, PROVEN**:

| map | `λ_∞` (ℝ) | `λ_2` (ℚ₂) | `λ_3` (ℚ₃) | Σ positive = `h_Haar` |
|---|---|---|---|---|
| `A=×(3/2)` | `log(3/2)≈0.405` (expand) | `log\|3/2\|_2=log2≈0.693` (expand) | `log\|3/2\|_3=−log3` (contract) | `log(3/2)+log2 = log3` |
| `M₂=×2` | `log2` (expand) | `−log2` (contract) | `log\|2\|_3=0` (**neutral**) | `log2` |

`|3/2|_2=|3|_2/|2|_2=1/(½)=2`; `|3/2|_3=|3|_3=1/3`; `|2|_3=1`. [PROVEN — `p`-adic valuations]

**Ledrappier–Young** (smooth: Ledrappier–Young 1985; algebraic solenoid/adelic form via Einsiedler–Lindenstrauss
leafwise measures): order the positive exponents decreasingly and let `γ_i∈[0,1]` be the **partial (transverse)
dimension** of `μ`'s conditional on the `i`-th coarse-unstable leaf. Then

```
  A :  h_μ(A) = log2 · γ_2 + log(3/2) · γ_∞ ,      γ_2,γ_∞ ∈ [0,1]   (γ along ℚ₂, ℝ)
  M₂:  h_μ(M₂) = log2 · γ_∞^{(2)} ,                γ_∞^{(2)} ∈ [0,1] (γ along the ℝ-unstable of ×2)
```

For Haar all `γ=1`: `h_Haar(A)=log3`, `h_Haar(M₂)=log2`. ✓ **Therefore**

> **ENT ⟺ `h_μ(M₂)>0` ⟺ `γ_∞^{(2)}>0` ⟺ the conditional measures of `μ` on the ℝ-unstable foliation of `×2`
> are positive-dimensional (non-atomic).** Equivalently (via `h_μ(A)=h_μ(A^{-1})`, AIU_JOININGS §3.1) the
> `A`-stable `ℚ₃`-leaf conditionals are positive-dimensional. **L–Y collapses ENT to ONE number `γ>0`.**
> [PROVEN reduction; the value of `γ` is OPEN]

This is the precise statement L–Y buys: it does **not** lower-bound `γ`; it only identifies *which* conditional
dimension `h_μ(M₂)>0` is equivalent to. The positive Lyapunov exponent `log2` is a constant prefactor that
**cannot** rescue a vanishing `γ`.

---

## 2. Pressure / large-deviation / Gibbs–Markov — three lower-bound attempts, three precise obstructions

| route | what it would give | what it actually gives | exact obstruction |
|---|---|---|---|
| **(A) Pressure / variational** `P(0)=h_top=sup_ν h_ν=log2` | a lower bound if `μ` were the equilibrium state (MME) | only `h_μ ≤ h_top=log2` (**UPPER**, vacuous since `=log2`) | **No selection principle forces a single orbit's empirical `μ` to be the MME.** The orbit-closure subshift has `h_top=log2` but ALSO carries zero-entropy invariant measures (every positive-entropy subshift does); the variational *sup* sees them all. Pressure bounds entropy from ABOVE, never below, for a named measure. [PROVEN obstruction] |
| **(B) Large deviation (level-2 LDP)** | under Haar/SRB, `{x : h(emp. meas.)<log2−ε}` is exponentially rare (rate `= log2−h`) | a Haar-**a.e.** positivity statement | **The seed `8` is a single Haar-NULL point.** An LDP bounds the *measure* of the exceptional set; it says nothing about membership of one specified point. This is the a.e.-vs-specified-seed wall (Tao-2019 / COCYCLE §3) read on the entropy axis. [PROVEN obstruction] |
| **(C) Gibbs–Markov renewal transfer** | the induced first-return-to-even map `F` is a full-branch piecewise-affine EXPANDING (Gibbs–Markov) endomorphism of `ℤ₂` (`CRYPTID_KERNEL`, `renewal_attack §8`); w.r.t. its a.c.i.m.=Haar the jump heights `D_j=v2(3c'_j−1)` are geometric(½), entropy `2` bits — **positive ANNEALED entropy** | positivity for the SRB/Haar measure of `F` only | **The Gibbs–Markov gap is a property of the SRB/Haar measure, not the orbit.** "The single orbit's empirical `D`-law = geometric(½)" ⟺ "`c'_j` equidistributes mod `2^k`" = **(K)**. The spectral gap gives CLT/LDP for `F`-typical points (annealed) — same wall as (B). The renewal centered sums `Σ(D_j−1)` random-walk like `√N` (no supermartingale; `renewal §8`), so no drift converts annealed→quenched. [PROVEN obstruction — annealed≠quenched] |

> **Net.** All three positive-entropy engines deliver `h>0` for a *typical* point of a *reference* (Haar/SRB)
> measure, or an UPPER bound on the sup; none touches the specified Haar-null orbit. The frequency weights that
> distinguish `h_μ` (a property of the SPECIFIC `μ`) from `h_top` (the sup) are exactly what these tools cannot
> pin for one named seed. [PROVEN]

---

## 3. Does ANY proven structure force `h_μ ≥ c>0`? — NO; the frequency-weighting obstruction [PROVEN]

| proven structure | controls | forces `h_μ>0`? | why not |
|---|---|---|---|
| `p(ℓ)≥1.71ℓ` (LIMIT_THEOREM §3″) | **unweighted** residue count | **NO** | even equi-weighted: `H_ℓ≥log₂(1.71ℓ)` ⇒ rate `(log₂ℓ)/ℓ→0`. Linear count ⇒ `h_top≥0` only ⇒ `h_μ≥0` only. |
| growth `log₂c_n≈0.585n` | the **support** (#cells touched ≤ min(N,2^k)) | **NO** | a support/topological quantity; a low-complexity deterministic sequence grows identically with `h_μ=0`. |
| foothold / max depth `~log₂N` (renewal §7) | depth reached `~log₂N` **total** bits | **NO** | `log₂N` bits across the whole orbit ⇒ rate `→0`; it is a support-depth, not a per-scale frequency spread. |
| **global** non-atomicity of `μ` (PROVEN, 2-adic repulsion) | no atoms in `μ` | **NO** | **decisive honest point:** global non-atomicity does NOT imply non-atomic CONDITIONALS (`γ>0`). `μ` can be globally non-atomic while its ℝ/ℚ₃-leaf conditionals are atomic (mass spread atomically per leaf, leaves varying continuously). So proven non-atomicity gives `h_μ≥0`, **not** ENT. |
| renewal `D_j` geometric(½) | **annealed** entropy `2` bits | **NO** | annealed (Haar/SRB) property; transfer to the quenched orbit = (K) (§2C). |

> **Exact obstruction (sharp, unchanged).** Every proven lower bound controls an **unweighted / support /
> annealed** quantity, all of which give measure-entropy rate `≥0`. ENT needs a positive lower bound on the
> **frequency-weighted, quenched** count `H_ℓ=−Σ_a f_ℓ(a)log f_ℓ(a)` surviving `ℓ→∞` — an exponential
> cell-spreading that **is** the (K)-character equidistribution of `c_n mod 2^ℓ`. There is **no proven `c>0`**,
> and not even a non-explicit proof of `h_μ>0` (that proposition IS ENT). [PROVEN obstruction]

---

## 4. Numerics — the conditional dimension `γ` reads `1`, and the deficit is pure undersampling [OBSERVED]

`scratchpad/ent_pressure_ly.py`: residues `c_n mod 2^k`, plugin Shannon `H_k`, per-bit `h_k=H_k−H_{k−1}`,
Miller–Madow rate `H_MM/k`, fill `m/2^k` vs Poisson `1−e^{−N/2^k}`. **Error bars = fixed-level rate vs N:**

```
 per-bit rate at the last fully-filled level k=13 (the conditional-dimension proxy γ̂):
   N=10⁴ :  H_13/13 = 0.9486   H_MM/13 = 0.9811
   N=3·10⁴: H_13/13 = 0.9832   H_MM/13 = 0.9979
   N=10⁵ :  H_13/13 = 0.9953   H_MM/13 = 0.9999      ← γ̂ → 1 as sampling completes
 deep-k rolloff is undersampling, not deficit:  k=16 fill 0.7813 vs pred 0.7826 ; k=18 0.3169 vs 0.3171 (≤0.2%)
 renewal jumps (N=10⁵): #=50159, E[D]=0.9937 (≈1), H(D)=1.9934 bits (geometric(½): E=1, H=2) — matches annealed
 parity blocks: H_L/L = 0.9998 (L=8), 0.9975 (L=12) — full per-symbol entropy where resolvable
```

- **Conditional-dimension estimate `γ̂(M₂)=1.00`.** At every level the sample resolves, per-bit entropy is
  `1 bit = log2`, and the fixed-level rate `H_MM/13` **rises to `0.9999` as `N→10⁵`** (the smaller-`N` deficit
  is sampling, not entropy). Read through L–Y (§1): `γ_∞^{(2)}≈1`, i.e. ℝ-conditional dimension `1`, i.e.
  `μ₂≈`Haar on `ℤ₂` (2-adic local dimension `1`). [OBSERVED]
- **This is equidistribution evidence, NOT a proof.** The sample rate `≈log2` certifies `h_k` only where
  `2^k≪N`; it does not certify `lim_{k→∞}`, and certifying that limit IS (K). The renewal `H(D)≈2` likewise
  confirms the ANNEALED geometric law, the very transfer §2C cannot make rigorous.

---

## 5. Honest verdict

| disposition | status |
|---|---|
| **(a)** explicit unconditional `h_μ(M₂) ≥ c>0` proven [major partial] | **NO** — no proven `c>0`; no proven `h_μ>0` at all |
| **(b)** only annealed / topological bounds; `h_μ>0` OPEN with a precise obstruction | **YES — this is the verdict** |
| **(c)** reduces to (K) | **YES, in difficulty** — `h_μ>0` is strictly weaker than (K) as a proposition (max-entropy/skew-Bernoulli ≠ Haar) but (K)-hard for THIS orbit, with no proven shortcut; `h_μ=0` would *refute* (K) |

**Make-or-break.** L–Y is genuinely useful: it converts ENT into a single conditional-dimension number `γ_∞^{(2)}`
with an explicit proven prefactor `log2`, and the numerics read `γ̂≈1`. But the prefactor cannot manufacture
positivity, and **no proven structure lower-bounds `γ`**. Pressure gives the wrong-direction (upper) bound;
large-deviation and the proven Gibbs–Markov renewal give positivity only for Haar/SRB-typical points, never the
named seed. The gap is exactly **frequency-weighted/quenched (= equidistribution = (K)) vs
unweighted/support/annealed (proven, rate ≥0)** — equivalently the a.e.-vs-specified-seed wall. ENT stays
**[OPEN / (K)-hard]**; (K) stays **[OPEN]** = Mahler 3/2 / AEV Conj 1.6 at α=8.

---

## Sources
- Ledrappier, Young, *The metric entropy of diffeomorphisms* I/II, Ann. Math. **122** (1985) — `h=Σλ_iγ_i`.
  [PROVEN-in-lit]
- Lind–Schmidt–Ward / Yuzvinskii, solenoid automorphism entropy `h(×u)=Σ_v log⁺|u|_v`. [PROVEN-in-lit]
- Rudolph (ETDS 1990); Johnson (1992); Einsiedler–Lindenstrauss, arXiv:2101.11120 (solenoid RJ + leafwise
  measures). [PROVEN-in-lit]
- Aaronson–Denker / Gibbs–Markov maps; large-deviation for Gibbs measures (Kifer, Young). [PROVEN-in-lit, annealed]
- Tao, *(3/2)ⁿ mod 1…*, arXiv:1909.03562 (log-density-1, not one seed). [PROVEN-in-lit, the a.e. wall]
- Repo: `POSITIVE_ENTROPY_ATTACK.md` (frequency-weighting obstruction), `LIMIT_MEASURE_ENTROPY.md` (ENT
  necessary, (K)-hard; topological≠measure sign correction), `AIU_JOININGS.md` (ENT ⟺ non-atomic conditionals;
  neutral-direction obstruction), `antihydra_renewal_attack.md` §7–§12 (Gibbs–Markov renewal, annealed geometric
  `D_j`, random-walk centered sums), `LIMIT_THEOREM.md` §3″ (`p(ℓ)≥1.71ℓ`), `CRYPTID_KERNEL.md`.
- Numerics: `scratchpad/ent_pressure_ly.py` (exact big-int, N≤10⁵): `γ̂(M₂)→1` (`H_MM/13`: 0.981→0.998→0.9999
  as N=10⁴→3·10⁴→10⁵); deep-k rolloff = `1−e^{−N/2^k}` to ≤0.2%; renewal `E[D]=0.994`, `H(D)=1.993` (≈ geom ½).

No machine decided. No label upgraded.
