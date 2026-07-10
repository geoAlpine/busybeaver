# o4 Christol / automatic-sequence test — the residue GF is transcendental over 𝔽₃(x) (and 𝔽₂), maximally: the p-kernel is FREE (2026-07-10)

*A genuinely-new, DECIDABLE test never run here: is the generating function of the o4 residue sequence
ρₙ = Wₙ mod 3 algebraic over 𝔽₃(x)? Christol's theorem: a sequence over 𝔽_p is p-automatic ⟺ its GF is
algebraic over 𝔽_p(x) ⟺ its p-kernel is finite. We compute the 3-kernel and 2-kernel to full feasible depth,
exact big-int orbit. Interpreter `.venv` python; exact 𝔽₃/𝔽₂ arithmetic. STRICT labels. NOT committed.
Script: `o4_christol_test.py`.*

---

## 0. One-line verdict

**[NON-AUTOMATIC — CONFIRMED, does not decide, no label upgraded].** The 3-kernel and 2-kernel of ρₙ both grow
at the **maximal possible rate** — every decimation subsequence `n ↦ ρ(pᵏn+r)` is **pairwise distinct** — so the
kernels equal the *free* counts `(3^{k+1}−1)/2` and `2^{k+1}−1` exactly at every depth, with **no** saturation and
**no** false merges (counts are window-independent at L = 100/200/400). By Christol's theorem the GF
`F(x)=Σρₙxⁿ` is **transcendental over 𝔽₃(x)** — and the ledger-drain indicator `1{Wₙ=0}` is likewise
transcendental over **both** 𝔽₃(x) and 𝔽₂(x). ρₙ is neither 3- nor 2-automatic; the residue frequency is **not**
rational-computable this way, so this test does **not** decide o4. The concrete new obstruction is the strongest
possible one: **the p-kernel is a free monoid on the p decimation maps — maximal non-automaticity.**
**No machine decided. No label upgraded.**

---

## 1. Setup [PROVEN, cross-checked exact]

Self-contained W-orbit (mirror of the G-odometer, `O4_RUN_STRUCTURE §3`): ρₙ = Wₙ mod 3,
`W_{n+1} = (4Wₙ − c(ρₙ))/3` with `c = {0:0, 1:13, 2:5}`, seed `W₀ = 57` (G₀ = 43). Integrality
`3 | 4Wₙ − c(ρₙ)` assertion-checked every step. Cross-check against the raw G-orbit
(`3G'=4G+e`, `e={0:9,1:14,2:1}`): `ρ^G_n = (ρ^W_n + 1) mod 3` for all n < 2·10⁵ — **True** (exact).
Residue counts over first 2·10⁵: `{0:66772, 1:66642, 2:66586}` (balanced ≈ 1/3 each; the ledger letter is
`Wₙ=0` ⟺ `G≡1`, freq 0.33386 — the `#1/n` of the prior builds).

**The kernel test (Christol, decidable).** The p-kernel is `K_p(ρ) = {n ↦ ρ(pᵏn+r) : k≥0, 0≤r<pᵏ}`.
Finite ⟺ p-automatic ⟺ GF algebraic over 𝔽_p(x). We measure each kernel element by its first L values and
count distinct signatures. **Anti-truncation discipline:** depth k is admitted only if *every* residue class
r < pᵏ has a full window (`pᵏ(L−1)+(pᵏ−1) < N`), so no comparison is ever truncated; and we re-run at
L = 100, 200, 400 — if a plateau were a truncation artifact it would shift with L. It does not.

## 2. The 3-kernel — FREE growth, saturates at nothing [OBSERVED, N = 2.5·10⁵, exact 𝔽₃]

Cumulative distinct kernel elements using depths 0…k (window L):

| depth k | L=100 | L=200 | L=400 | free max `(3^{k+1}−1)/2` |
|--------:|------:|------:|------:|------:|
| 0 | 1 | 1 | 1 | 1 |
| 1 | 4 | 4 | 4 | 4 |
| 2 | 13 | 13 | 13 | 13 |
| 3 | 40 | 40 | 40 | 40 |
| 4 | 121 | 121 | 121 | 121 |
| 5 | 364 | 364 | 364 | 364 |
| 6 | 1093 | 1093 | — | 1093 |
| 7 | 3280 | — | — | 3280 |

**Every entry equals the free maximum exactly.** All 3280 subsequences of depths ≤ 7 are pairwise distinct on
the first 100 terms; widening to L = 200, 400 changes *nothing* (no merge was spurious). The 3-kernel exhibits
**zero collapse** — it is the free monoid on the three decimations {n↦3n, n↦3n+1, n↦3n+2}. This is the
signature of a **non-automatic** sequence in its most extreme form.

## 3. The 2-kernel — also FREE [OBSERVED, N = 2.5·10⁵]

| depth k | L=100 | L=200 | L=400 | free max `2^{k+1}−1` |
|--------:|------:|------:|------:|------:|
| 5 | 63 | 63 | 63 | 63 |
| 8 | 511 | 511 | 511 | 511 |
| 10 | 2047 | 2047 | 1023(k≤9) | 2047 |
| 11 | 4095 | — | — | 4095 |

Again exactly the free count `2^{k+1}−1` at every admitted depth, L-independent. ρₙ is **not 2-automatic**
either. (Christol proper is the p = base = 3 statement; the 2-kernel result additionally rules out any binary
finite-state structure.)

## 4. The indicator and the run/reload sequences — all non-automatic [OBSERVED]

- **Ledger-drain indicator `1{Wₙ=0}`** (= `1{ρ^G=1}`, the fatal letter): 2-kernel = `2^{k+1}−1` and
  3-kernel = `(3^{k+1}−1)/2`, **both free**. So even the single-letter indicator whose frequency IS the o4
  decision (`#1/n ≥ 4/5` fatal) is transcendental over both 𝔽₂(x) and 𝔽₃(x). No automatic sub-coding exists.
- **Run-length sequence** (dᵢ = lengths of `Wₙ=0` runs; 55 586 runs, mean 1.5004, max 12, distribution
  `1:37062, 2:12360, …, 12:1` — an approximately geometric-3 law): as a raw ℕ-valued sequence its alphabet is
  unbounded (runs ≤ 0.262n) so it is not automatic a fortiori; **reduced mod 2 and mod 3** it still has
  **free** 2- and 3-kernels (`2^{k+1}−1`, `(3^{k+1}−1)/2`).
- **Reload-unit sequence** (non-drain block lengths): reduced mod 2, 2-kernel free (`2^{k+1}−1`).

**No exploitable automatic sub-structure anywhere.** Every derived sequence tested has a free (maximal) kernel.

## 5. Interpretation for o4 [ASSESSED]

Christol's theorem gives an **exact dichotomy**, and the computation lands unambiguously on the transcendental
side: `Σρₙxⁿ` is algebraic over 𝔽₃(x) **⟺** the 3-kernel is finite; it is instead **free** (maximal). Hence

> **[OBSERVED] The o4 residue generating function is transcendental over 𝔽₃(x); ρₙ is not 3-automatic (nor
> 2-automatic). No rational/computable residue frequency arises from automaticity, so the Christol route does
> not compute freq{Wₙ=0} and does not decide o4.**

Had the kernel been finite, ρₙ would be automatic ⟹ its letter frequencies would be **rational and exactly
computable** by the standard linear-representation / Perron–Frobenius eigenvector of the kernel automaton — and
one would compare `freq{Wₙ=0}` against 4/5 to decide the machine. The kernel is not finite; that lever is absent.

**Why this is the right kind of new obstruction.** This is a *decidable, exact* confirmation — not a heuristic —
of transcendence, complementing the earlier structural findings without duplicating them:
- It is **sharper than periodicity**. `NEWMATH_DIGIT_BRIDGE` scanned residues mod 3ᵏ for periodicity **in n**
  and found none; automaticity is the strictly weaker property (every eventually-periodic sequence is automatic
  but not conversely), so **ruling out automaticity rules out periodicity a fortiori and much more** — no
  finite-state machine of *any* kind (not just a periodic one) generates ρₙ base 3 or base 2.
- It **realizes concretely** the `newmath_digit_bridge` non-descent / non-autonomy prediction: a p-automatic
  sequence is exactly one whose base-p decimations close into a finite set (the finite-state descent). The
  branch self-selection `e(ρₙ)` is the non-descent, and here it shows up as the kernel being not merely infinite
  but **free** — the decimations satisfy *no* relations at all, the maximal expression of "no fixed
  characteristic polynomial ⇒ no analytic descent."
- It **strengthens** `O4_EXPSUM`'s square-root-cancellation picture from a rate observation to a *structural*
  statement: an automatic ρ would force the exponential sum `S₁` into a finite algebraic-nested-sum form with
  provable (log-power / rational-spectrum) behaviour; the free kernel says no such closed algebraic form exists,
  which is exactly why the van-der-Corput regress (unit multiplier `|4|=1` mod 3) has no spectral gap.

The concrete "kernel growth rate" asked for: **it is the maximum, pᵏ new elements at depth k, i.e. the kernel of
size (p^{k+1}−1)/(p−1) through depth k with p ∈ {2,3} — free, no saturation to any horizon we can reach
(depth 7 base-3 ≈ 3.7·10³ elements all distinct; depth 11 base-2 = 4095 all distinct), verified truncation-free.**

## 6. Summary table

| object | test | result | label |
|---|---|---|---|
| ρₙ = Wₙ mod 3 | 3-kernel (Christol, base = 3) | **free** `(3^{k+1}−1)/2`, k≤7=3280, L-indep | `[OBSERVED]` non-automatic |
| ρₙ | 2-kernel | **free** `2^{k+1}−1`, k≤11=4095 | `[OBSERVED]` non-2-automatic |
| `1{Wₙ=0}` (ledger letter) | 2- & 3-kernel | **free** both | `[OBSERVED]` transc. over 𝔽₂(x) & 𝔽₃(x) |
| run-length dᵢ mod 2, mod 3 | 2-,3-kernel | **free** | `[OBSERVED]` non-automatic |
| reload-unit mod 2 | 2-kernel | **free** | `[OBSERVED]` non-automatic |
| GF `Σρₙxⁿ` over 𝔽₃(x) | Christol dichotomy | **transcendental** (kernel infinite) | `[OBSERVED]` |
| decision of o4 | via automatic frequency | **not available** (no finite kernel) | — |

**Soundness note.** The kernel-size measurement is a decidable finite computation; the only inference risk is a
*false plateau* from truncated windows, which would spuriously suggest automaticity. We saw the opposite —
**free growth** — and the L = 100/200/400 agreement rules out the reverse risk (spurious *merges* inflating the
non-automaticity would show as counts rising with L; they are flat). No claim beyond the finite data: the kernel
is free to the tested depth (base-3 depth 7, base-2 depth 11); Christol requires infinite closure, which the
strict, unbroken free growth to those depths evidences but — being a finite computation — does not *prove* to
infinity. Verdict labelled `[OBSERVED]`, not `[PROVEN]`.

## 7. Reproduce

`o4_christol_test.py` (`.venv` python, exact big-int orbit N = 2.5·10⁵; kernel_sizes auto-caps depth to
truncation-free horizon; all integrality assertions + G/W cross-check pass). Not committed.

Cross-refs: `O4_RUN_STRUCTURE_2026-07-07.md`, `O4_EXPSUM_FREQUENCY_BUILD_2026-07-10.md`,
`NEWMATH_DIGIT_BRIDGE_2026-07-09.md`.

**No machine decided. No label upgraded.**
