# Data gather for attacking P1 / (K) — the comprehensive empirical dataset (2026-07-01)

*Directive: "go after P1/P1′, gather as much data as possible." This note collects the decision-relevant empirical
data on the kernel `(K)` = Mahler 3/2 / AEV, at the largest feasible exact-arithmetic scales, to inform building the
missing quenched-equidistribution tool (P1′). SOUNDNESS: all `[OBSERVED]` exact big-int; nothing proved; no orbit
selected. Scripts in `scratchpad/gather1.py`, `scratchpad/gather_big.py`.*

---

## 1. Orbit master statistics `[OBSERVED, N=3·10⁵]`

- even-density `= 0.499360`; **worst running even-density (n≥50) `= 0.479675` at `n=122`; margin over the halting
  threshold `1/3` is `+0.1463`.**
- induced map: mean `D = 1.995187`; `freq(D≥2) = 0.498463`; `max D = 22`; `#odd = 3·10⁵`.
- **worst running mean `D` (j≥50) `= 1.888889` at `j=62`; margin over `3/2` is `+0.3889`.**

The two margins (`+0.146` on even-density above `1/3`; `+0.389` on mean-`D` above `3/2`) are the empirical "distance
to halting." The whole question P1 is whether these `liminf` margins stay `> 0` forever. (Large-N trend: §4.)

## 2. The exogenous kernel — moving diagonal of `3ⁿ` `[OBSERVED, n<2·10⁵]`

`(K)` splits as `β_n = bit_k(c_n) = bit_{n+k}(8·3ⁿ) ⊕ (carry)`. The exogenous part is the binary digit of `3ⁿ` on
the **moving diagonal** at position `n+k`:
- `k=2`: diagonal-bit density `= 0.501965`
- `k=3`: `0.501390`
- `k=5`: `0.498420`

All `≈ 1/2` (consistent with normality). **This is the hardest object:** no unconditional positive-density bound
for a moving diagonal of `3ⁿ` exists (AEV prove none); this density being `≥` anything `>0` unconditionally is at
the P1 frontier.

## 3. The foothold-governing constant `[OBSERVED]`

`log₂3 = 1.5849625007…`, continued fraction `[1,1,1,2,2,3,1,5,2,23,2,2,1,1,55,1,4,3,1,1,…]`. The **large partial
quotients** (`a_9=23`, `a_14=55`) are where the unconditional top-digit foothold depth-reach (`≈0.85·log₂N`) dips
and recovers — the archimedean Diophantine input that reaches `Θ(log N)` depth (the log side of the log-vs-linear
gap). The finite irrationality measure of `log₂3` is what powers the foothold; crossing to linear depth is P1′.

## 4. Large-N margin trend `[OBSERVED, N=1.5·10⁶ / J=7.5·10⁵]` — the margins are CONSTANT

`scratchpad/gather_big.py`, exact big-int:

| `N` (base) | even-density | worst running (n≥50) | margin over `1/3` |
|---|---|---|---|
| `10³` | 0.499000 | **0.479675 @ n=122** | +0.14634 |
| `10⁵` | 0.501590 | **0.479675 @ n=122** | +0.14634 |
| `10⁶` | 0.499501 | **0.479675 @ n=122** | +0.14634 |
| `1.5·10⁶` | 0.499307 | **0.479675 @ n=122** | +0.14634 |

| `J` (induced) | mean `D` | worst running (j≥50) | margin over `3/2` |
|---|---|---|---|
| `500` | 1.992 | **1.888889 @ j=62** | +0.38889 |
| `50 000` | 2.006 | **1.888889 @ j=62** | +0.38889 |
| `750 000` | 1.997 | **1.888889 @ j=62** | +0.38889 |

> **Decisive empirical fact:** the worst running dip is achieved in the **transient** (even-density at `n=122`,
> mean-`D` at `j=62`) and is **never approached again** over `1.5·10⁶` steps — both margins are **exactly constant**
> (`+0.146`, `+0.389`). The `liminf` is not merely `> 1/3` (resp. `> 3/2`); its empirical infimum is attained early
> and the orbit is monotone-safe thereafter (matching the balance-walk running-min `= 17` constant). Antihydra is
> **decisively non-halting empirically**, with a large, stable margin.

Implication for P1′: the tool needs only a **weak** bound (`liminf` even-density `≥ 1/3`, vs. observed `≈ 0.48`) —
the difficulty is entirely qualitative (unconditional positivity of a moving-`3ⁿ`-diagonal density), not
quantitative. A finite check handles the transient; the asymptotic `liminf` is the (K)-hard part.

## 5. What this data says for P1′ (the tool)

- The orbit is **comfortably supercritical empirically** (margins `+0.146` / `+0.389`), so P1′ needs only to
  convert this observed margin into a proof — i.e. control the `liminf`, not improve the mean.
- The obstruction is **entirely on the moving-diagonal-of-`3ⁿ` density** (§2), which no tool bounds unconditionally.
- The available Diophantine input (`log₂3` CF, §3) reaches `Θ(log N)` depth; P1′ must reach `Θ(n)`.
- Every internal statistic matches i.i.d. (prior sessions), so P1′ cannot come from a statistical distinguishing
  feature — it must be a genuinely new quenched-equidistribution / effective-Diophantine mechanism.

## 6. Weapon-build attempt from the data → the explicit conditional certificate (2026-07-01)

Built the magnitude-aware Lyapunov `g(o)=α\log o + h(o\bmod 2^k)` (the one variant No-Structure left ajar). Sub-action
`ψ(o) ≤ α·D·\log(3/2) + h(To)-h(o)`. LP (`scratchpad/build_cert.py`): **feasible with `α<0` when (i) the `δ_1` fixed
point `o=1` is excluded and (ii) `D` is capped at `k`** (`k=3` `α≈-0.62`, `k=6` `-0.62`, `k=8` `-0.52`, `k=9` `-0.21`).
This confirms No-Structure's "conditional-above-a-threshold" statement — but skeptical re-examination shows the
feasibility is **an artifact of the two exclusions, both of which are exactly `(K)`-content**:
- **Deep-cylinder cap `[the real flaw]`:** for true (uncapped) `D`, the constraint needs `h(To)-h(o) ≥ |α|D\log(3/2)`,
  **unbounded in `D`**, but `h` is bounded. The orbit's depth is unbounded (`D ≤ \log_2 o ≈ 0.585n`; observed
  `\max D=22` and growing), so capping `D<k` silently ignores the deep cylinders where the certificate fails.
  Removing the cap = controlling the depth tail = `(K)`.
- **`δ_1` exclusion:** `o=1` is the ergodic-optimization maximizer (`ψ=+½`); excluding it = the orbit avoiding the
  `δ_1` density = `freq(D≥2)` control = `(K)`.

**Honest result:** the magnitude-aware conditional certificate is explicitly constructible and feasible *only under*
depth-tail-boundedness + `δ_1`-avoidance — **two residuals, both `(K)`-grade**. Unconditionally it reduces to `(K)`.
The discipline caught the LP "feasible" as a `D`-cap artifact, not a weapon.

## 7. The last thread verified — CDT / effective-irrationality methods do NOT reach the depth gap (2026-07-01)

The lit check (`LIT_CHECK_2026-07.md`) flagged **Calegari–Dimitrov–Tang (arXiv:2510.04156)** — a new arithmetic-holonomy
route to **effective irrationality measures** — as the one building block worth shelving for a future depth-gap
attack. Verified: **it does not connect.** `[OBSERVED + analysis]`
- **The foothold is `Θ(log N)`, and no irrationality-measure improvement changes the order** (`scratchpad/foothold.py`):
  the leading-digit reach `k(N)` of `{n\log_2 3 \bmod 1}` is `≈ 0.75$–$0.90·\log_2 N`. Improving the irrationality
  measure `μ` of `log_2 3` improves only the **constant** `c` in `k ≈ c\log N`; by pigeonhole (N points resolve only
  `~\log_2 N` leading binary digits) it can **never** reach linear depth.
- **The gap is the wrong kind of object for CDT.** CDT controls the **archimedean (and specific `p`-adic)
  approximation of FIXED constants** (algebraic roots, `L(2,χ_{-3})`, 2-adic `ζ(5)`) → the **`Θ(log N)` archimedean
  foothold** only. The kernel bit `bit_{n+k}(8·3ⁿ)` lives at **2-adic depth `Θ(n)` (linear)** and is the **2-adic
  digit distribution of the geometric sequence `3ⁿ`** = `(K)` — **not** a fixed-constant irrationality measure. CDT's
  `p`-adic component is likewise about fixed constants, not geometric-orbit equidistribution; and `3ⁿ`'s digits are
  not in CDT's `G`-function/period class.

**Verdict `[OBSERVED + reasoned]`:** the last identified constructive thread is **closed**. Effective-irrationality
machinery — CDT included, the newest available — controls only the log-depth archimedean foothold; the depth gap is
geometric-sequence 2-adic equidistribution `= (K)`, a fundamentally different object no such method addresses. There is
now **no internal weapon, no literature weapon, and no shelvable building block that connects.** The genuinely-remaining
path is entirely new mathematics (P1′) that no current tool — internal, or the 2024–26 literature — provides.

**No machine decided. No label upgraded.** `(K)` remains `[OPEN]` = Mahler 3/2 / AEV.
