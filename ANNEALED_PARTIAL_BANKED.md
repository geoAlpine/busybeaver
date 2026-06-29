# Annealed / unconditional partial results — banked standalone note (2026-06-29)

*Consolidation of every PROVEN **unconditional** or **annealed/a.e.-tier** partial result toward the
Antihydra/BB(6) kernel. The annealed tier is exactly where the tools deliver theorems; the quenched
single-orbit statement is the open kernel. Each entry carries an exact statement, a status label, the repo
source, the literature theorem it rests on (cited from `CITATIONS.md` / the source notes — no web access used),
and the **exact quantitative gap** to the kernel H2. All orbit constants re-verified with exact big-int below
(`scratchpad/bank_verify.py`, N=10^5, <1 s). SOUNDNESS: zero false proofs; no label upgraded; no machine decided.*

---

## 0. The kernel these partials are measured against

**Kernel (K) / H2** (`WEAKEST_SUFFICIENT.md`, `WEAPONS_AUDIT_2026-06-29.md` §1): for `c0=8`, `c→⌊3c/2⌋`,
> **liminf_N (1/N) Σ_{n<N} (−1)^{c_n} ≥ −1/3**  ⟺  even-density ≥ 1/3  ⟺  mean `D=v2(3o−1) ≥ 3/2`
> ⟺  single-orbit equidistribution of `c_n mod 2^k`  ⟺  base-3/2 normality of the seed-8 orbit
> = **Mahler 3/2 / AEV Conj 1.6 (rational base)**. Status: **[OPEN]**.

Every partial below is **annealed** (i.i.d.-weight ensemble mean), **a.e.** (metric / full-measure), or
**unconditional but of the wrong order** (controls `Θ(log N)`, or support not frequency, or first moment only).
The gap column states precisely what each leaves uncovered relative to the **quenched, single-orbit,
positive-density, middle-digit** statement H2 requires.

---

## 1. Results table

| # | Statement (exact) | Status | Source (repo / literature) | Gap to H2 |
|---|---|---|---|---|
| 1 | 3/2 is non-Pisot, non-Salem (rational, not an algebraic integer) ⇒ `ν_{2/3}` is **Rajchman**: `|ν̂_{2/3}(ξ)|→0` as `|ξ|→∞`. | [PROVEN-in-lit] | `NONPISOT_FOURIER_CHAIN.md` Link A; Erdős (1939)/Salem (1944) dichotomy; survey Li–Sahlsten arXiv:1910.03463 | Qualitative `→0` only; controls the **annealed mean**, not the quenched derivative `‖F‖`. |
| 2 | Effective decay rate of `ν_{2/3}`: **≥ logarithmic** in `|ξ|`, and **sharp** (∃ subsequence with only log decay). | [PROVEN-in-lit] | `NU_RATE_DATA.md` §5; **Varjú–Yu** arXiv:2004.09358 (ratios powers of λ, 1/λ algebraic non-Pisot non-Salem); **Kershner (1936)** for rational λ | Log-in-ξ. Power rate (`a≈1.71` observed) is **[OPEN]** = Mahler; no citable theorem gives power decay for 2/3. |
| 3 | Annealed carry product `Φ(N)=Π_{k≤N}|cos(π{(3/2)^k/4})| → 0` (i.i.d.-weight carry balance ⇒ annealed even-density = 1/2). | [PROVEN] | `NONPISOT_FOURIER_CHAIN.md` Link B; `ATTACK_RENORMALIZATION.md`; rests on item 1 via the exact identity below | Annealed (ensemble) only. The quenched orbit's own correlated weights do not factor (= Mahler). |
| 4 | Exact identity `|ν̂_{2/3}((3/2)^N/8)| = Φ(N)·C`, `C = √2·ν̂_{2/3}(1/8) = Π_{m≥1}cos((π/4)(2/3)^m) = 0.774846171700205…` | [PROVEN] | `ATTACK_RENORMALIZATION.md` §1 (60-digit), `NU_RATE_DATA.md` §2 | An identity (tautology); relocates the rate, does not produce it. Provable floor `Φ(N) ≲ N^{−a}`; observed `2^{−N}` is Mahler. |
| 5 | **Top-digit equidistribution**: the top `Θ(log N)` binary digits of `c_n` equidistribute; at CF convergents `N=q_m` of `α=log₂3` the leading-mantissa discrepancy is `≪ 1/N`; uniformly the top `(1/(μ−1)−ε)log₂N` digits. | [PROVEN] | `EFFECTIVE_TOPDIGIT.md` (a),(b); Weyl + Erdős–Turán + finite irrationality measure `μ(log₂3)` | Reaches **depth `Θ(log N)`**; the parity/halting bit is the **diagonal** `bit_{n+3}(3^n)` at depth `Θ(n)`. Gap `Θ(n)−Θ(log N)=Θ(n)`. |
| 6 | **Salem–Zygmund**: for a.e. ξ, `|Σ_{n<N} e(ξ(3/2)^n)| = O(√(N log log N))`. | [PROVEN-in-lit] | `NONPISOT_FOURIER_CHAIN.md`, `ONECHAR_CANCELLATION.md` §3b, `THERMO_FORMALISM.md`; Salem–Zygmund LIL | **a.e. ξ — not specializable** to the single ξ that the seed-8 orbit reads. |
| 7 | **Vaaler L¹ minorant ceiling**: H2 needs only `J=5` circle frequencies; at J=5 the minorant has `m̂(0)=1/3` exactly (genuine `o(N)` on those 5); a uniform crude bound needs `|S_N(h)|/N ≤ θ* ≤ 1/6` (rigorous ceiling), LP-optimal `θ*≈0.043` ⇒ **≥96% per-frequency cancellation**. | [PROVEN] | `ONECHAR_CANCELLATION.md` §2–3, `H2_ONESIDED_CANCELLATION.md`; Vaaler/Beurling–Selberg extremal minorant | Reduces the **frequency count** to finite; the per-frequency demand is still single-orbit `√N→o(N)` cancellation = (K). |
| 8 | **FLP spread**: `Ω(3/2) = limsup{ξ(3/2)^n} − liminf ≥ 1/3` for all ξ>0. | [PROVEN-in-lit] | `ONECHAR_CANCELLATION.md` §3b; **Flatto–Lagarias–Pollington**, Acta Arith. 70 (1995) 125–147 | **Support/range only**, says nothing about frequency (Cesàro Dirac-mass vs limsup–liminf closure). |
| 9 | **Zudilin/Padé**: `‖(3/2)^n‖ > 0.5803^n` for `n ≥ K` (K effective), via hypergeometric/Padé (not Baker). | [PROVEN-in-lit] | `BAKER_LINFORMS.md` §2C; **Zudilin**, J. Théor. Nombres Bordeaux 19 (2007) 311–323 (`0.5803 = 2^{−0.78513}`) | **Pointwise single-term** lower bound, no density / no frequency. |
| 10 | **Longest run** `L(8·3^n) = o(n)` (subspace theorem). | [PROVEN-in-lit] | `WEAPONS_AUDIT_2026-06-29.md` §2B; arXiv:2501.00850 | Horizontal/two-sided `→0`; bounds the longest single odd-run, not the even-density. |
| 11 | **Tightest unconditional density-ish result**: `#even(n) ≥ c·log n`, `c ≈ 0.89 = 1/log₂2.17`. | [PROVEN] | `EVEN_DENSITY_PARTIAL.md`; from orbit growth `bitlen(c_p)=0.585p+O(1)` ⇒ `p_{j+1} ≤ 2.17p_j` | `c·log n` vs the needed `εn`: **the entire wall is the `log n → n` factor.** Marginally consistent with even-density→0. |
| 12 | **Adelic 2↔3 coupling** `v3(o_{j+1}) = v2(3o_j−1) − 1` exactly (since `3o−1 ≡ −1 mod 3`); product formula ⇒ first-moment identity `log o_n ≈ (Σ D_j)log(3/2)` only. | [PROVEN] | `ADELIC_COUPLING.md` §1a; fundamental theorem of arithmetic + product formula | An **isomorphism of the obstruction** (2-adic density ⇔ 3-adic density), not a reduction; first moment only, shape free. |
| 13 | **Renewal spectral gap**: the low-bit 2-adic Markov chain has gap `1−|λ₂| ≈ 0.99`; self-consistency operator contracts to `(E,ρ)=(½,0)`. | [PROVEN] (operator) / annealed | `antihydra_renewal_attack.md` §2,§12 | Annealed/Haar self-consistency; the incoming high bits that would close it are the orbit's own high bits = (K). |
| 14 | **Transfer-operator a.e. tier**: twisted RPF gap `ρ(L_t)<1` ⇒ annealed decay (= Rajchman) + **quenched CLT for a.e. sequence**. | [PROVEN-in-lit] (a.e.) | `THERMO_FORMALISM.md` §2.2; twisted Gibbs–Markov / Aaronson–Denker–Gouëzel | a.e. realisation — the seed-8 orbit is one Haar-null point; the a.e.→specified upgrade is the wall. |
| 15 | **Ergodic / structural floors** (durable core): induced map exact Bernoulli (`D_j` iid geom, mean 2); valuation budget `Σ v2(3c_i−1)=n+v2(c_n)−v2(c_0)`; subword complexity `p(ℓ)≥1.71ℓ`. | [PROVEN] | `BB6_STRUCTURAL_LIMIT_THEOREM.md` §4.2, `VALUATION_BUDGET.md`, `LIMIT_THEOREM.md` §3″; Dubickas (2009) for the slope | First moment / a.e.-Haar / linear-complexity; all far below the normality (full equidistribution) H2 needs. |

---

## 2. Numerics-verification table (recorded vs recomputed, exact big-int, N=10^5)

| Constant | Recorded (source) | Recomputed (N=10^5) | Match? |
|---|---|---|---|
| even-density | 0.50018 (N=2·10^5, `quick_anchor.py`) | 0.50159 | ✓ (both ½ ± O(1/√N)) |
| worst running avg `(1/N)Σ(−1)^{c_n}`, n≥50 | −0.0407 at n=122, margin +0.293 over −1/3 (`WEAPONS_AUDIT` §0) | −0.0407 at n=122, margin +0.293 | ✓ exact |
| mean `D=v2(3o−1)` | 1.998 (N=5·10^6, `ANNEALED_QUENCHED_DATA` §6) | 2.00638 (49 841 odd steps) | ✓ (→2, within 1/√n) |
| freq(D≥2) | ≈0.500 (Haar ½) | 0.50210 | ✓ |
| Φ(N) decay slope `−lnΦ/N` | →ln2 = 0.6931 (0.687 at N=32768, `ATTACK_RENORMALIZATION`) | 0.6868 (N=3·10^4, exact phase) | ✓ |
| Φ exponent `a = slope/ln(3/2)` | 1.7095 = log2/log(3/2) (`NU_RATE_DATA` §3) | 1.694 (N=3·10^4) → 1.7095 | ✓ |
| `C = √2·ν̂_{2/3}(1/8)` | 0.774846171700205 (`ATTACK_RENORMALIZATION` §1) | 0.7748461717 (both products) | ✓ exact |
| top-digit foothold depth `k=log₂(1/D*)` | `Θ(log N)`, k/log₂N→1 at convergents (`EFFECTIVE_TOPDIGIT`) | k/log₂N = 0.78–0.87 (generic N) | ✓ (k = Θ(log N)) |
| max odd-run length | 20 at N=3·10^5 (`EVEN_DENSITY_PARTIAL`) | 20 at N=10^5 | ✓ |
| Zudilin `‖(3/2)^n‖ > 0.5803^n` | holds for `n ≥ K` (`BAKER_LINFORMS`) | holds all n in 5..1999; only n=1,2,4 below (sub-threshold) | ✓ (asymptotic bound; small-n exceptions expected) |
| Vaaler ceiling `θ* ≤ 1/6`; J=5 surplus 0 | θ*≤1/6, LP-opt 0.043 (`ONECHAR_CANCELLATION`) | `m̂(0)=1/2−1/6=1/3` exact; 1/6 ceiling | ✓ analytic |

**Soundness note (no incident).** One discrepancy surfaced and was traced to *my own* verifier, not the
recorded data: a naïve `mpmath dps=300` Φ(5000) returned slope 0.383 because `(3/2)^5000` needs ~880 decimal
digits. Recomputing with **exact integer phase** `{(3/2)^k/4}=(3^k mod 2^{k+2})/2^{k+2}` restored the recorded
slope (0.6868→ln2, a→1.7095). No recorded constant failed to reproduce.

---

## 3. Honest summary

Every banked partial is real, proven, and **lands strictly inside the annealed / a.e. / wrong-order tier**:
the non-Pisot ⇒ Rajchman ⇒ annealed carry-balance chain (items 1–4) controls the **ensemble mean** and gives a
clean polynomial-in-N floor `Φ(N)≲N^{−a}` whose observed exponential truth `2^{−N}` is exactly Mahler; the
top-digit theorem (5) is unconditional but reaches only depth `Θ(log N)` against a diagonal bit at depth
`Θ(n)`; Salem–Zygmund, transfer-operator CLT (6,14) are a.e. and non-specializable; Vaaler (7) compresses the
demand to 5 frequencies but cannot soften the per-frequency `≈96%` single-orbit cancellation; FLP and Zudilin
(8,9) are support/pointwise, never frequency; the adelic coupling and renewal gap (12,13) are exact but
first-moment / annealed isomorphisms of the same obstruction. The **single tightest unconditional density-style
statement is item 11, `#even(n) ≥ c·log n` with `c≈0.89`** — the only result that says something quantitative
about the *count* of even terms of the *specified* seed-8 orbit, yet it is a `log n` floor against a needed
`εn`, and is marginally consistent with even-density→0. All eleven re-verified orbit constants reproduce under
exact big-int; the lone numeric wobble was an mpmath-precision artifact in the fresh verifier, corrected by
exact integer phase reduction, leaving the recorded values intact.

**No machine decided. No label upgraded.**
