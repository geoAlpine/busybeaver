# Wall (B) bilinear angle: does the JOINT cross-correlation cancel where the marginals can't? (2026-06-28)

Target of the angle: the cross-correlation
```
   C_N = (1/N) Σ_{n<N} (−1)^{a_n} (−1)^{b_n},   a_n = bit_n(8·3ⁿ),  b_n = bit_n(Tₙ).
```
The two MARGINAL sums `Σ(−1)^{a_n}` and `Σ(−1)^{b_n}` are each lacunary `(3/2)ⁿ`
exponential sums and resist van der Corput ([CLOSED], `ATTACK_VDC.md`: the obstruction
is `(3/2)^{b−a}=O(1)` failing). The hypothesis tested here: the product
`(−1)^{a_n+b_n}` is a DIFFERENCE of two `(3/2)`-driven phases, and Weyl/vdC-style
difference structure ("A-process", type-I/II philosophy) might cancel the fast mode and
leave a slower, tractable residual.

Script: `wallb_bilinear.py` (exact big-int, `.venv`). **Zero false proofs.**

---

## 1. The cross-correlation as an exponential sum  [PROVEN identity]

Both signs are EXACT half-wave functions of an explicit phase:
```
   (−1)^{a_n} = g({φ_a(n)}),   φ_a(n) = 4(3/2)ⁿ = (8·3ⁿ)/2^{n+1}
   (−1)^{b_n} = g({φ_b(n)}),   φ_b(n) = Tₙ/2^{n+1} = (1/4) Σ_{j} e_{n−1−j}(3/2)ʲ
```
with `g(t)=+1` on `[0,½)`, `−1` on `[½,1)`, the square wave `g(t)=Σ_{k odd} ĝ_k e(kt)`,
leading modes `e(±t)`. So the product's Fourier expansion is the BILINEAR sum
```
   (−1)^{a_n}(−1)^{b_n} = Σ_{k,l odd} ĝ_k ĝ_l · e( k·φ_a(n) + l·φ_b(n) ).
```
The `(3/2)ⁿ` "velocity" of the `(k,l)` mode is the coefficient of `(3/2)ⁿ` in
`k·φ_a + l·φ_b`.

---

## 2. The crux: the fast `(3/2)ⁿ` mode CANCELS EXACTLY in the difference  [PROVEN, exact]

There is an exact integer identity (codebase-confirmed, re-verified here over n<40000,
0 mismatches; `Tₙ ≡ 8·3ⁿ mod 2ⁿ`, the low n bits cancel):
```
   8·3ⁿ = 2ⁿ·cₙ + Tₙ ,     cₙ = ⌊3cₙ₋₁/2⌋ = real Antihydra orbit  (c₀=8).
```
Divide by `2^{n+1}`:
```
   φ_a(n) − φ_b(n) = (8·3ⁿ − Tₙ)/2^{n+1} = cₙ/2   (mod 1)   ≡  rₙ/2 ∈ {0, ½}.
                                                                 ^^^^^^^^^^^^^^^
```
**VERIFIED EXACTLY** (`phi_a − phi_b` takes only the values `{0.0: 19963, 0.5: 20037}`
over n<40000 — never anything else).

Reading of the bilinear modes:
- **DIFF / diagonal modes `l = −k`:** `k·φ_a + l·φ_b = k(φ_a−φ_b) = k·cₙ/2`.
  The `(3/2)ⁿ` coefficient is `4(k+l) = 0`. **The fast mode is annihilated.** Both
  phases share their ENTIRE fast part `4(3/2)ⁿ`; they are PHASE-LOCKED, differing only
  by the bounded parity `cₙ/2`.
- **SUM / off-diagonal modes `k+l ≠ 0`:** `(3/2)ⁿ` coefficient `4(k+l) ≠ 0` — still
  lacunary, still `(3/2)ⁿ`, still [CLOSED] by `ATTACK_VDC.md`.

So the bilinear hypothesis is **TRUE in the strongest possible form**: the fast mode does
not merely partially cancel, it cancels *exactly and totally* in the difference channel.

---

## 3. …but the residual it leaves is the open kernel itself  [PROVEN — why the cancellation does not help]

The diagonal residual is `e(k·cₙ/2)`. For `k` odd, `e(k cₙ/2) = ((−1)^{cₙ})^k = (−1)^{rₙ}`.
Summing the diagonal coefficients (`Σ_{k odd} ĝ_k ĝ_{−k} = ⟨g²⟩ = 1`, Parseval) gives:
```
   (−1)^{a_n}(−1)^{b_n} = (−1)^{rₙ}     EXACTLY   (verified all n<40000),
```
which is just the XOR identity `a_n ⊕ b_n = rₙ` (the real orbit parity). Hence
```
   C_N = (1/N) Σ (−1)^{rₙ} = W_N / N   IDENTICALLY.
```
**The cross-correlation IS the marginal parity kernel `W_N`** — the same open object
(`PROOF_STATUS.md` (K), Mahler/AEV). Numerically the `C_N` and `W_N` columns are
bit-identical (slope −0.420, see §4).

**Why van der Corput cannot use the cancelled residual.** The "slow tractable residual"
the hypothesis hoped for would be a smooth, slowly-varying phase with bounded but nonzero
derivatives (where the k-th-derivative test bites). Instead the residual is `cₙ/2 (mod 1)`,
a **two-valued step `{0,½}` = the parity bit itself**. It has:
- bounded velocity (no `(3/2)ⁿ` blow-up) — so it ESCAPES the §1-obstruction of
  `ATTACK_VDC.md`, **but**
- **no derivatives at all** (it is not a smooth phase; it is a `{0,½}` indicator). The vdC
  derivative tests are *vacuous* on it. There is no nontrivial-but-slow phase to exploit —
  the residual is the raw parity sequence, carrying 100% of the original difficulty.

This is a genuinely SHARPER closure than the marginal: the marginal is closed because vdC
hits a lacunary phase; the cross-correlation is closed because its bilinear structure
**collapses by an exact identity straight back to the open parity kernel** — there is no
new cancellation channel to open.

---

## 4. Numerics  (`wallb_bilinear.py`, exact big-int, orbit c₀=8)

EXACT identities (n<40000, 0 mismatches):
| identity | holds |
|---|---|
| `rₙ == a_n XOR b_n` | True |
| `cₙ == (8·3ⁿ−Tₙ)/2ⁿ == real orbit hₙ` | True |
| `Tₙ == 8·3ⁿ (mod 2ⁿ)` (low n bits cancel) | True |
| **`φ_a − φ_b == cₙ/2 (mod 1) == rₙ/2`** (fast mode cancels) | **True** |
| `(−1)^{a_n}(−1)^{b_n} == (−1)^{rₙ}` | True |

Phase velocities `|d/dn| mod 1` (a fast/equidistributed phase ⇒ mean ≈ 0.25):
| phase | mean | median | values |
|---|---|---|---|
| marginal `φ_a` (fast `(3/2)ⁿ`) | 0.2505 | 0.2502 | continuous on (0,½) |
| SUM mode `φ_a+φ_b` (fast, doubled) | 0.2517 | 0.2530 | continuous on (0,½) |
| **DIFF residual `φ_a−φ_b`** | 0.2504 | 0.5000 | **only `{0, ½}`** (19963 / 20037) |

→ marginal and sum modes are lacunary-fast; the diff residual collapses to the
two-valued parity (bounded velocity, non-smooth).

Decay `|·|/N` (slope ≈ −0.5 = √-cancellation), N up to 2·10⁵:
| sum | 1e3 | 1e4 | 3e4 | 1e5 | 2e5 | slope |
|---|---|---|---|---|---|---|
| `A_a` (marg a) | .030 | .0098 | .0021 | .0029 | .0027 | **−0.418** |
| `A_b` (marg b) | .032 | .0022 | .0071 | .0034 | .0041 | **−0.418** |
| `C_N` (a·b)    | .002 | .0092 | .00033 | .0032 | .00037 | **−0.420** |
| `W_N` (parity) | .002 | .0092 | .00033 | .0032 | .00037 | **−0.420** |

`C_N` and `W_N` are identical columns (the XOR identity). All four decay near √N
empirically; none is provable by vdC (`ATTACK_VDC.md` §1–2).

---

## 5. Verdict (the asks)

1. **Cross-correlation exponential sum:** `C_N = (1/N)Σ_{k,l odd} ĝ_k ĝ_l Σ_n e(k φ_a + l φ_b)`,
   `φ_a=4(3/2)ⁿ`, `φ_b=Tₙ/2^{n+1}`. **[PROVEN form]**

2. **Do the fast `(3/2)ⁿ` modes cancel in the product?** **YES — exactly and totally**, in
   the difference (diagonal `l=−k`) channel, by the exact identity
   `φ_a − φ_b = cₙ/2 (mod 1)`. The two phases are **phase-locked** (share their whole fast
   part `4(3/2)ⁿ`). The sum (`k+l≠0`) channel keeps the fast mode and stays lacunary
   ([CLOSED]). **[PROVEN, exact]**

3. **Partial van der Corput bound on the joint?** **None obtainable.** The cancelled
   residual is not a tractable slow phase: it is `cₙ/2 ∈ {0,½}` = the orbit parity `rₙ`
   itself, so `C_N ≡ W_N/N` *identically*. The cross-correlation is **not a new, easier
   object** — by an exact algebraic collapse it equals the original open kernel
   (Mahler/AEV, `PROOF_STATUS.md` (K)). vdC's derivative tests are vacuous on a two-valued
   step. **[CLOSED — precise reason: bilinear difference collapses to the open parity
   kernel by `(−1)^{a}(−1)^{b}=(−1)^{a⊕b}=(−1)^{r}`.]**

4. **Numerics:** §4. Fast-mode cancellation verified exactly (residual `{0,½}` only);
   `C_N≡W_N`; empirical √N decay (slope −0.42) on all sums; vdC provable bound is the
   trivial `O(N)` on every channel.

**Bottom line.** The bilinear/difference angle does NOT open a new cancellation channel.
It produces the cleanest possible structural fact — the explicit digit phase `4(3/2)ⁿ` and
the self-generated carry phase `Tₙ/2^{n+1}` are **phase-locked, differing only by the
bounded parity `cₙ/2`** — but precisely because of that lock, the cross term collapses by
an exact identity to the open parity kernel `W_N`. The earlier "decorrelation" of the bits
(`Pearson ≈ 0`, `WALL_B_WHICH_PART.md`) coexists with **rigid phase-locking** of the
underlying phases; the bilinear product exploits the lock and returns nothing new. This is
a new, sharper [CLOSED] for the joint angle, complementary to the marginal lacunary
obstruction in `ATTACK_VDC.md`. The kernel (5) = Mahler/AEV remains **[OPEN]**.

*(Asset for future angles: the exact phase-lock `φ_a − φ_b = cₙ/2` and `8·3ⁿ = 2ⁿcₙ + Tₙ`
say the joint object has NO extra degree of freedom beyond the single orbit parity — any
proof must act on `rₙ` directly; splitting into a/b marginals provably cannot help, since
their product re-fuses exactly. This rules OUT the bilinear/type-II route specifically.)*
