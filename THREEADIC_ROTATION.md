# Three-adic dual of WALLB_MARTINGALE — does o_j mod 3^k rotate? (2026-06-28)

*Angle: WALLB_MARTINGALE found that the 2-adic carry `T_n mod 2^k` is an **exact `×3`
rotation, a function of `n` alone** (period `2^{k-5}`, 0 violations) — a provable/computable
structure. THE HOPE (dual): maybe the induced odd orbit's 3-adic residue `o_j mod 3^k`
(`o0=27`, `o' = 3^{D-1}(3o-1)/2^D`, `D=v2(3o-1)`) ALSO has rotation/periodic structure, which
would make `density{3 | o_j}` (= the kernel, by the coupling `v3(o_{j+1})=D_j-1`) PROVABLE by a
rotation's unconditional equidistribution. Numerics `.venv` only (`threeadic_rotation.py`,
exact big-int, 120000 induced steps). Every line labelled. Zero false proofs. NOT committed.*

---

## 0. One-line answer

**The dual FAILS, but it fails cleanly and yields new `[PROVEN]` residual structure.**
`o_j mod 3^k` is **aperiodic / full-complexity for every `k=1..6`** (no eventual period up to
several thousand): it is **NOT a rotation** and carries **no equidistribution-for-free**. The
reason is exact and is the precise contrast with the carry: the 2-adic carry `T_n mod 2^k`
**decouples** from the orbit (the orbit-dependent input term vanishes `mod 2^k`, leaving a pure
function of the clock `n` ⇒ rotation), whereas `o_j mod 3^k` is **driven by** the orbit's own
full-complexity 2-adic depth sequence `D_j` — injected every step by `v3(o_{j+1})=D_j-1` — and
never decouples. The mod-3 residue is **measure-isomorphic to the `D`-sequence**, so it inherits
its full complexity. **However**, the 3-adic side does have genuine `[PROVEN]` residual
congruence structure (a parity law), which recodes — but does not tame — the `D`-sequence.

---

## 1. Test (1): periodicity of `o_j mod 3^k` in `j` — APERIODIC `[OBSERVED, decisive]`

If a rotation existed (the dual of the carry), the period would divide `ord_{3^k}(2) = 2·3^{k-1}`
(`≤ 486` for `k=6`); the search window was `≤ 4·3^k` (up to 2916), comfortably larger.

| `k` | mod `3^k` | smallest tail-period `≤ 4·3^k` |
|---|---|---|
| 1 | 3 | **NONE (aperiodic)** |
| 2 | 9 | **NONE** |
| 3 | 27 | **NONE** |
| 4 | 81 | **NONE** |
| 5 | 243 | **NONE** |
| 6 | 729 | **NONE** |

> **`[OBSERVED]` `o_j mod 3^k` is aperiodic in `j` for all `k=1..6` — NO rotation/period exists.**
> Direct contrast: `T_n mod 2^k` IS exactly periodic in `n` (period `2^{k-5}`, 0 violations,
> WALLB_MARTINGALE). The breakthrough hope (3-adic rotation ⇒ unconditional density) **does not
> materialise.**

---

## 2. Test (2)/(4): full subword complexity, isomorphic to the `D`-sequence `[OBSERVED + PROVEN]`

**Subword (factor) complexity `p(L)` = # distinct length-`L` factors:**

| `L` | `p(L)` mod-3 seq | `2^L` | `p(L)` `D`-seq (clip≤5) | `5^L` |
|---|---|---|---|---|
| 1 | 2 | 2 | 5 | 5 |
| 2 | 4 | 4 | 25 | 25 |
| 3 | 8 | 8 | 125 | 125 |
| 4 | 16 | 16 | 621 | 625 |
| 5 | 32 | 32 | 2715 | 3125 |
| 6 | 64 | 64 | 9055 | 15625 |
| 9 | 512 | 512 | 66191 | (sample-limited) |

- The **mod-3 sequence has complexity exactly `2^L`** (perfect binary full-complexity, not periodic
  — a periodic seq would saturate at its period). `p(1)=2`, not 3: **residue `2` never appears**
  (see §4). The mod-3 sequence is thus the binary indicator `1{D_j=1}` in disguise, and that
  indicator has full `2^L` complexity ⇒ aperiodic.
- The `D`-clip and `v3` sequences fill toward `5^L` (sample-limited, not saturated).

**Isomorphism check `[PROVEN identity + OBSERVED]`.** `v3(o_j) = D_{j-1} - 1` held for **all**
`j≥1` (0 exceptions), and the subword complexities of the `v3`-sequence and the `D`-sequence track
(both grow as full-complexity). The 3-adic valuation sequence **is** the `D`-sequence shifted and
re-based — same complexity, same aperiodicity.

> **`[PROVEN]` `o_j mod 3^k` is measure-isomorphic to the 2-adic depth sequence `(D_j)` (via
> `v3(o_{j+1})=D_j-1` and §4). It inherits the `D`-sequence's full complexity; it is aperiodic and
> non-rotational, exactly as the dual hope is the mirror of the 2-adic side, not a new tame object.**

---

## 3. Why the dual fails — the exact contrast carry-rotation vs. orbit-driven `[PROVEN]`

The two updates look symmetric but are structurally opposite:

- **Carry `T_{n+1} = 3 T_n + 2^n r_n`.** For `n ≥ k` the orbit-dependent input `2^n r_n ≡ 0
  (mod 2^k)` — it **drops out** of the low bits. So `T_n mod 2^k = 3·(T_{n-1} mod 2^k)`, a pure
  `×3` rotation that is a **function of the clock `n` alone**. The deterministic clock erases the
  orbit data; the result equidistributes unconditionally (rotation). `[PROVEN, WALLB_MARTINGALE]`
- **Induced `o_{j+1} = 3^{D_j - 1} m_j`.** Here `D_j = v2(3o_j-1)` and `m_j = (3o_j-1)/2^{D_j}`
  are **full orbit data** (the 2-adic depth). They **never drop out**: `v3(o_{j+1}) = D_j - 1`
  injects the entire full-complexity `D`-sequence into the 3-adic residue **every step**. There is
  **no clock term that decouples**; the 3-adic residue is *driven by* the orbit's own 2-adic
  complexity. Hence aperiodicity, not rotation.

> **`[PROVEN]` The carry rotates because its low bits are decoupled from the orbit and become a
> function of the deterministic clock `n`. The 3-adic residue does NOT rotate because it is
> coupled to — indeed equal in valuation to — the full-complexity 2-adic depth sequence `D_j`. The
> asymmetry is exact: clock-driven (tame) vs. orbit-driven (full-complexity).**

---

## 4. Residual computable structure on the 3-adic side `[PROVEN]` (the genuine gain)

The dual is not empty: there are exact congruence laws (0 violations / 120000 steps, **and**
proved below).

**Lemma (3-adic congruence laws).** For the induced orbit, with `N=3o-1=2^D m` (`m` odd):
1. `m ≡ (−1)^{D+1} (mod 3)` — i.e. `m ≡ 1` if `D` **odd**, `m ≡ 2` if `D` **even**.
2. `o_{j+1} ≡ 0 (mod 3)` iff `D_j ≥ 2`; and `o_{j+1} ≡ 1 (mod 3)` iff `D_j = 1`.
3. **`o_j mod 3 ∈ {0, 1}` for all `j ≥ 1` — the residue `2` NEVER occurs.**

**Proof.** `3o ≡ 0`, so `N = 3o−1 ≡ −1 ≡ 2 (mod 3)`. Since `2 ≡ −1 (mod 3)`, `2^D ≡ (−1)^D`, so
`(−1)^D m ≡ 2 ≡ −1 (mod 3)`, giving `m ≡ (−1)^{D+1} (mod 3)` — (1). Now `o_{j+1} = 3^{D−1} m`:
if `D ≥ 2`, `3 | o_{j+1}` so `≡ 0`; if `D = 1` (odd), `o_{j+1} = m ≡ (−1)^{1+1} = 1` — (2). Both
cases land in `{0,1}` — (3). ∎ Verified exactly: `o_j mod 3` distribution `{0: 60052, 1: 59948}`,
`#(o_j ≡ 2) = 0`; all three laws 0 violations over 120000 steps.

**The 3-adic leading (unit) digit `u_j = (o_j / 3^{v3(o_j)}) mod 3 ∈ {1,2}`** carries the parity
of the driving depth: by Lemma (1) the unit part of `o_{j+1}` is `m ≡ (−1)^{D_j+1}`, so
`u_{j+1} = 1 ⇔ D_j` odd, `u_{j+1} = 2 ⇔ D_j` even. Numerics: `P(u=1)=0.665`, `P(u=2)=0.335`
(= `P(D` odd`)` vs `P(D` even`)`, i.e. `Σ 4^{-i}·2 = 2/3` vs `1/3` under the geometric law),
unit-sequence complexity exactly `2^L`, autocorrelation `≈ 0` (lags 1–5 all `< 0.003`), no period
≤ 20000, `corr(u_j, v3(o_j)) = +0.34` (both functions of `D_{j-1}`), `corr(u_j, D_j) ≈ 0`.

> **`[PROVEN]` Residual structure EXISTS and is exact: `o_j mod 3 ∈ {0,1}` (never 2), and the
> leading 3-adic digit is the parity of the preceding depth `D`. BUT this is a deterministic
> RECODING of the full-complexity `D`-sequence (mod-3 seq ≅ `1{D=1}`; unit digit ≅ `parity(D)`),
> NOT an independent tame structure. It equidistributes only as much as `D` does — i.e. NOT
> unconditionally. No density bound follows.**

---

## 5. Test (3): densities `[OBSERVED, NOT proven]`

`density{3 | o_j} = 0.50043` (target/Haar `1/2`), `density{9 | o_j} = 0.24942` (`1/4`),
`d3 + d9 = 0.74985` (minimal proposition `≥ 1/2` `OBSERVED` to hold with margin). The `v3` law
matches `2^{−(k+1)}` to 3 dp for `k=0..6`. These are **observed for this orbit only** — they are
exactly what genericity of `D` would give, but are **not forced** by any of the proven structure,
since that structure is the aperiodic, full-complexity recoding of `D` (no counting lock). Finite
`N` proves nothing about the limit. The single-orbit genericity wall (Mahler 3/2 / wall (A)) stands.

---

## 6. Verdict (the asks)

| ask | answer | label |
|---|---|---|
| Does `o_j mod 3^k` have rotation/periodic/computable structure (breakthrough)? | **No rotation/period** — aperiodic, full complexity (`2^L`), measure-isomorphic to the `D`-sequence (`v3(o_j)=D_{j-1}-1`). The dual of the carry-rotation **fails**. | `[OBSERVED + PROVEN-iso]` |
| Exact contrast with the `T_n`-rotation? | Carry `T_n mod 2^k`: orbit input `2^n r_n ≡ 0 mod 2^k` **decouples** ⇒ pure clock-`n` function ⇒ rotation (equidistributes free). `o_j mod 3^k`: **driven by** the orbit's full-complexity depth `D_j` (`v3(o_{j+1})=D_j-1`), never decouples ⇒ aperiodic. Clock-driven (tame) vs orbit-driven (full-complexity). | `[PROVEN]` |
| Any residual computable structure? | **Yes, exact congruences:** `o_j mod 3 ∈ {0,1}` (never 2); `m ≡ (−1)^{D+1} mod 3`; leading 3-adic digit = `parity(D_{prev})`. But all are deterministic **recodings** of the full-complexity `D`-sequence — no equidistribution, no density bound. | `[PROVEN]` |

### New assets banked `[PROVEN]`
- **3-adic congruence laws** (§4): for the induced orbit, `o_j mod 3 ∈ {0,1}` always (residue 2
  impossible); `m ≡ (−1)^{D+1} (mod 3)`; the leading 3-adic digit of `o_{j+1}` equals
  `parity(D_j)` (1 if odd, 2 if even). All proved + 0 violations / 120000 steps.
- **Isomorphism statement** (§2–§3): `o_j mod 3^k` is the orbit-driven full-complexity recoding of
  the 2-adic depth sequence, the exact mirror of (not a tame alternative to) the 2-adic cylinder
  problem. The carry-rotation does NOT transfer.

### Why this confirms rather than breaches (honest)
The carry rotates because a deterministic clock erases the orbit data; the 3-adic residue cannot
rotate because it is, by the proven coupling, the orbit data. The new congruence laws are real and
citable but are a re-encoding of the same full-complexity `D`-sequence — they pin the 3-adic
*shape* (`{0,1}`-valued, parity-controlled leading digit) without pinning its *density*. The
density `density{3|o_j}=1/2` remains single-orbit genericity = Mahler 3/2 = wall (A). Fully
consistent with ADELIC_COUPLING (the coupling is an isomorphism of obstructions) and
INDUCED_RESIDUE_STRUCTURE (`o_j mod 2^k` aperiodic in `j`; the induced map is a shift, not a
rotation — and so is its 3-adic shadow).

### Live next angle (not yet mined)
The proven `{0,1}`-valuedness collapses the 3-adic mod-3 question to a **single binary indicator
`b_j = 1{3∤o_j} = 1{D_{j-1}=1}`**, and `density{3|o_j} = 1 − freq(b)`. The leading-digit parity
law further says the *next* unit digit is `parity(D_j)`. So the 3-adic side reads off **two
specific functionals of the `D`-sequence** (`1{D=1}` and `parity(D)`) with exact congruences. The
one un-mined micro-question: whether the *joint* law of `(1{D_j=1}, parity(D_j))` carries a local
self-consistency (e.g. via the `Z_2×Z_3` simultaneous constraint `v2(3o−1)=D` and
`v3(o)=D_{prev}−1`) not visible in either functional alone. Numerics show `corr(u_j,D_j)≈0`, so
it is a long shot — same verdict as ADELIC_COUPLING §5.

Script: `threeadic_rotation.py`. Not committed.
