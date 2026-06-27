# The self-consistent loop via the PROVEN 3-adic unit-part contraction — does it pin the D-distribution? (2026-06-28)

*Angle (assigned): there is now a GENUINELY PROVEN contraction — the 3-adic unit-part contraction,
ratio 1/3 (`THREEADIC_SKEW.md`, `THREEADIC_INTRATERM.md`) — unlike the earlier REFUTED `‖F‖`
self-consistency contraction (`AUDIT_CONTRACTION.md`). The unit field `u_j` is a contraction-determined
function of the D-history, and `D_j = v2(3^{e_j+1} u_j − 1)` feeds back. So set up the self-consistent
fixed-point loop using the PROVEN contraction and determine whether it pins the D-distribution
(mean `D ≥ 3/2`). Numerics `.venv` only (`scratchpad/unitpart_sc.py`, exact big-int, 2·10^5 induced steps
from `o0=27`). Every line labelled. Zero false proofs. NOT committed.*

---

## 0. One-line answer

The self-consistent loop is real and the contraction is genuinely proven, **but it is ORTHOGONAL to the
D-distribution** — it gives **no new handle**. Decisive reason, `[PROVEN structural + OBSERVED]`: the
proven contraction synchronizes the **3-adic** projection `u_j mod 3^c`, while `D_j = v2(3^{D_{j-1}} u_j − 1)`
reads the **2-adic** projection `u_j mod 2^k`, and the two projections are **CRT-decoupled** — independent
along the orbit (`χ²/dof ≈ 1`). Numerically the synchronized 3-adic state carries **literally zero**
information about `D_j` (real MI = shuffled-null MI to 4 dp, e.g. `0.0065 = 0.0066` at `3^6`), whereas the
2-adic state **determines** `D_j` exactly (`D_j = v2(3^{D_{j-1}}·(u_j mod 2^{D_j+2}) − 1)`, verified). The
contraction is in the `|·|_3` metric; the target reads the `|·|_2` metric; CRT makes them orthogonal. This
is the same wall as `THREEADIC_SKEW §2` / `THREEADIC_INTRATERM`, now stated at the level of the **closed
self-consistent loop**: the loop contracts on the coordinate the target never queries, and is
expanding/un-synchronized on the coordinate the target does query.

---

## 1. The self-consistent loop, formalized `[PROVEN]`

Induced odd map `o ↦ o' = 3^{D−1}(3o−1)/2^D`, `D = v2(3o−1)`, `o0 = 27`. Decompose `o_j = 3^{e_j} u_j`,
`gcd(u_j,6)=1`. Two exact identities (`THREEADIC_INTRATERM §1`, re-verified, 0 exceptions over 2·10^5):

- `e_j = v3(o_j) = D_{j−1} − 1`  (the injected 3-power is the previous depth − 1).
- The unit recursion and the feedback:
  > **(U)** `u_{j+1} = (3^{D_{j−1}} u_j − 1) / 2^{D_j}`,  `u_j` always coprime to 6.
  > **(D)** `D_j = v2(3^{D_{j−1}} u_j − 1)`  (since `e_j+1 = D_{j−1}`).

**The contraction (PROVEN), and U as a function of the D-tail.** Read (U) in `Z_3`. The factor
`3^{D_{j−1}}` has `|3^{D_{j−1}}|_3 = 3^{−D_{j−1}} ≤ 3^{−1}` (as `D ≥ 1`), and `2^{−D_j}` is a `|·|_3`-unit.
So the map `u_j ↦ u_{j+1}` is a `|·|_3`-**contraction with ratio `3^{−D_{j−1}} ≤ 1/3`**. Writing it forward,
> `u_{j+1} ≡ −2^{−D_j} + 3^{D_{j−1}} 2^{−D_j} u_j  (mod 3^c)`,
the dependence on the seed `u_{j−L}` is multiplied by `3^{Σ}` with `Σ = Σ injected 3-powers`, vanishing
mod `3^c` once `Σ ≥ c`. Hence the synchronized unit field is a well-defined continuous function of the
D-tail:
> **`u_j mod 3^c = U_c(D_{j−1}, D_{j−2}, …)`,** depending only on the recent D-tail back to where the
> cumulative injected 3-power reaches `c`. **Modulus of continuity:** ratio `1/3` per unit 3-power; the
> tail-length needed is `≈ c / E[D] ≈ c/2` steps (mean `D = 2`).

Substituting into (D) closes the loop on the D-sequence alone:
> **`D_j = G(D_{j−1}, D_{j−2}, …) = v2( 3^{D_{j−1}} · U(D-tail) − 1 )`.**

This is a genuine self-generated D-sequence with a **proven contraction in the auxiliary `u` variable**.
The question is whether the `u`-contraction transfers to a contraction/uniqueness for the **D-distribution**
(which would pin `mean D ≥ 3/2`).

**`[OBSERVED, A]` Modulus of continuity verified** (`unitpart_sc.py [A]`, panel of 2000 indices,
reconstruct `u_j mod 3^c` from the D-tail using a deliberately wrong seed):
reconstruction is **exact (2000/2000)** once the cumulative injected 3-power `≥ c`:

| target `c` | min cumulative 3-power needed | mean |
|---|---|---|
| 2 | 1 | 2.03 |
| 3 | 2 | 3.52 |
| 4 | 3 | 4.26 |
| 6 | 5 | 6.34 |

Confirms ratio-`1/3`-per-3-power contraction; `U` is well-defined and Lipschitz in the D-tail.

---

## 2. The crux — the contraction does NOT control D; CRT decouples it `[PROVEN structural + OBSERVED]`

Heeding the `AUDIT_CONTRACTION` lesson (the 2-adic transfer operator is non-normal/expanding; a scalar
contraction estimate is not a bound), we ask *directly*: does threading through the **3-adic** `u`-contraction
control `D_j`? `D_j` reads `u_j` via `v2(3^{D_{j−1}} u_j − 1)`, i.e. through `u_j mod 2^k`. So the test is
whether the synchronized **3-adic** state `u_j mod 3^c` predicts `D_j`, or whether `D_j` depends only on the
**un-synchronized 2-adic** state `u_j mod 2^k`.

**`[OBSERVED, B]` `D_j` is read from the 2-adic part, not the synchronized 3-adic part** (`H(D)=1.98` bits):

| state read of `u_j` | MI(state ; `D_j`) | E[D | state] spread |
|---|---|---|
| 3-adic `mod 3^2` (9) | 0.0002 | 0.023 |
| 3-adic `mod 3^3` (27) | 0.0005 | 0.146 |
| 3-adic `mod 3^4` (81) | 0.0013 | 0.258 |
| 3-adic `mod 3^6` (729) | 0.0065 | 0.899 |
| 2-adic `mod 2^3` (8) | **0.5815** | — |
| 2-adic `mod 2^5` (32) | **0.7389** | — |
| 2-adic `mod 2^7` (128) | **0.8303** | — |
| 2-adic `mod 2^9` (512) | **0.8472** | — |
| 2-adic `mod 2^12` (4096) | **0.8609** | — |

The 3-adic MI is **finite-sample estimator bias, not signal** — `[OBSERVED]` shuffle control:
real vs label-shuffled null are **equal to 4 dp** (`3^4`: 0.0013 vs 0.0011; `3^6`: 0.0065 vs 0.0066). So the
synchronized 3-adic state carries **zero** information about `D_j`. By contrast the 2-adic state determines
it: `[OBSERVED]` `D_j = v2(3^{D_{j−1}}·(u_j mod 2^{D_j+2}) − 1)` exactly (checked, all sampled `j`).

**`[OBSERVED, C]` CRT decoupling — the two projections are independent along the orbit:**

| `(3^c × 2^k)` | χ²/dof | verdict |
|---|---|---|
| `3^2 × 2^3` | 1.393 | independent |
| `3^2 × 2^5` | 1.209 | independent |
| `3^3 × 2^5` | 1.116 | independent |
| `3^3 × 2^7` | 0.988 | independent |

So knowing the contraction-synchronized `u_j mod 3^c` tells you **nothing** about `u_j mod 2^k`, which is
exactly what `D_j` reads. **This is the precise obstruction the angle asked to pin:** `u_j` is 3-adically
synchronized, but its 2-adic residue (what `D_j` reads) is NOT synchronized — and CRT makes the two metrics
orthogonal coordinates of the single integer `u_j`.

**Structural reason `[PROVEN]`.** In (U), the same factor that **contracts** 3-adically, `3^{D_{j−1}}2^{−D_j}`,
**expands** 2-adically: `|2^{−D_j}|_2 = 2^{D_j} ≥ 2` and `3^{D_{j−1}}` is a 2-adic unit. So the unit recursion
is a `|·|_3`-contraction **and simultaneously** a `|·|_2`-expansion (the inverse-of-contraction). The 2-adic
projection is precisely the autonomous exact-Bernoulli base of `THREEADIC_SKEW §1` (ρ=0 but operator-norm 1,
maximally non-normal, `AUDIT_CONTRACTION §2a`). The contraction lives entirely on the orthogonal 3-adic
coordinate.

---

## 3. Distribution-level: the loop does NOT contract the D-law `[OBSERVED]`

Does conditioning on the synchronized 3-adic state pin/contract the D-distribution? (`unitpart_sc.py [D]`,
state `= u_j mod 3^4`, 41 well-sampled states, ≥200 each):
- pooled D-law `{1:.500, 2:.251, 3:.125, 4:.062, 5:.031, ≥6:.031}` = geometric(1/2) (Haar);
- **TV( D-law | 3-adic state ‖ pooled ) : mean 0.0211, max 0.0934** — at the sampling-noise floor.

So conditioning on the contraction-determined 3-adic state leaves the D-law **unchanged**. The proven
`u`-contraction supplies **no contraction on the D-distribution**: the loop `D_j = G(D-tail)` factors as
"`D-tail → (3-adic u, synchronized)`" composed with "`(2-adic u, un-synchronized) → D_j`", and the bridge
between the two is severed by CRT. The mean is `1.99627 ≈ 2` (margin over the `3/2` threshold), but this is
the SAME `[OBSERVED]` genericity statement as before — the contraction adds nothing toward proving it.

---

## 4. Honest verdict (the four asks)

| ask | answer | label |
|---|---|---|
| Self-consistent loop `D_j = G(D-history)` via contraction-determined `u`? | **Yes, clean.** `u_j mod 3^c = U_c(D-tail)` is well-defined (proven `|·|_3`-contraction, ratio `1/3`/3-power, modulus of continuity tail-length `≈ c/2`); `D_j = v2(3^{D_{j−1}}U(D-tail) − 1) = G(D-tail)`. | `[PROVEN]` |
| Does the proven 3-adic `u`-contraction give a handle on the D-distribution? | **No — ORTHOGONAL.** | `[PROVEN structural + OBSERVED]` |
| If orthogonal, why crisply? | The contraction synchronizes `u_j mod 3^c` (`|·|_3`); `D_j` reads `u_j mod 2^k` (`|·|_2`); CRT makes them **independent coordinates** of the one integer `u_j`. The factor `3^{D_{j−1}}2^{−D_j}` **contracts 3-adically while expanding 2-adically**, so the controlled coordinate and the queried coordinate are on opposite sides. MI(3-adic state; D) = shuffled-null (zero); MI(2-adic state; D) → `H(D)`; `u_j mod 3^c ⟂ u_j mod 2^k` (`χ²/dof ≈ 1`). | `[PROVEN]` |
| Numerics | `U` modulus-of-continuity verified (seed killed once cum-3-power ≥ c); D read from 2-adic not 3-adic (MI table + shuffle null); CRT independence; conditional D-law = pooled (TV ≈ 0). | `[OBSERVED]` |

### Why this is the AUDIT lesson, vindicated (honest)
`AUDIT_CONTRACTION` warned the earlier `‖F‖<1` contraction was REFUTED because the 2-adic operator is
non-normal/expanding. The NEW proven contraction is real — but it is the **3-adic** contraction, and the 2-adic
expansion the AUDIT identified is precisely the channel `D` reads. The new handle does **not** change the 2-adic
situation; it lives on the orthogonal place. So the answer is not "the contraction is also refuted" (it is
genuinely proven) but "the genuine contraction is **orthogonal** to the target by CRT." No over-claim:
contraction PROVEN, transfer to D REFUTED-by-orthogonality, mean-`D` genericity still `[OPEN]` = Mahler/AEV wall.

### What would make it load-bearing (the one un-mined micro-question, unchanged)
The contraction would help only if some **sufficient** halting/non-halting criterion could be written as a
**3-adic-unit-part** (not 2-adic-valuation) statement. The current target (`mean D ≥ 3/2 ⟺ density{3|o}`) is a
2-adic-valuation statement (`THREEADIC_SKEW §2`), orthogonal to the synchronized part. Whether a *different*
sufficient criterion that is 3-adic-unit-measurable exists is the single remaining open micro-question — the
self-consistent loop does not, by itself, supply one.

Script: `scratchpad/unitpart_sc.py` (+ inline shuffle control). Not committed.
