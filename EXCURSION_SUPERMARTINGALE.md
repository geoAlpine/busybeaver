# An a-priori excursion estimate on V = v₂(c−1)? — the Kac/supermartingale route, closed (2026-06-30)

*The one un-pre-empted route from `CORE_ORBIT_ARITHMETIC.md §5`: not a per-step drift (the feedback is
provably white), not a spectral contraction (L_ann odd-blindness), not a structure-only certificate
(No-Structure / coboundary-LP infeasible) — but a **quenched Kac return-time / Lyapunov sub-action at the
EXCURSION level** whose decrease lives in the conditional return-time law, attacked WITHOUT assuming the
D-statistics (the circularity to break). This note formalizes the Kac/excursion object, runs the
supermartingale attempt for each natural candidate W, and delivers an honest verdict. SOUNDNESS: every line
labelled [PROVEN]/[OBSERVED]/[OPEN]; no (K) claim; the one tempting loophole is caught as the §13/§14
unfaithful-model trap. Numerics `.venv`, exact big-int, orbit c₀=8 (induced o₀=27), N=10⁵. NOT committed.*

---

## 0. One-line verdict

**No a-priori excursion-level supermartingale exists.** Every candidate W's conditional excursion drift
`g(K)=E[ΔW | entry-depth K]` is **at most LINEAR in K** (measured: `g(K)≈c·K`, never `K²`), so its mean drift
`Σ_K P(K)g(K)` depends only on the **first moment E[K]** — which is the proven-free renewal count `≤N`. Such a
W is therefore negative on the **real orbit AND on a heavy-tailed E[K²]=∞ adversary alike** (verified: W1 drift
`−1.62` real vs `−3.59` adversary, same sign), so its negativity certifies **nothing** about the second
moment. The only W whose negativity *would* be equivalent to `E[K²]<∞ = (K)` must jump up by `~K²` at each
excursion start; that W is **(a)** killed by the white-jump no-go (the jumps are unpredictable — K-autocorr
≤0.012 — so no supermartingale absorbs them without a compensating drift of size `E[K²]/excursion`, finite
**iff** `E[K²]<∞`, i.e. assuming (K)), and **(b)** identically the quadratic depth potential `Q=d²`, which
telescopes `ΣK² = 2Σd−#{d≥1} = itself` **exactly** (verified, the `EK2_SECOND_BUDGET` tautology). **Sharp
no-go: an a-priori excursion estimate provably reduces to (K).** No machine decided. No label upgraded.

---

## 1. The Kac / excursion formalization [PROVEN structure; OBSERVED statistics]

`V_n := v₂(c_n−1)` (depth toward the fixed point 1; `=0` iff `c_n` even). Two [PROVEN] facts set the renewal
structure (`MINPROP_RUNS §1`, `NONATOMIC_FIXEDPOINT §1`):

- **Countdown.** If `c_n` is odd with `V_n=a≥1` then `c_{n+1}=(3c_n−1)/2` and `V_{n+1}=a−1`. So V descends
  deterministically `K,K−1,…,1`, then a step to even (`V=0`). Verified 0 exceptions.
- **Excursion = renewal cycle.** Mark an **entry** at index `n₀` where `V_{n₀}≥1` and `V_{n₀−1}=0` (came from
  even); the **entry-depth** `K=V_{n₀}` is the moving-middle-digit `K=v₂(3c'−1)` of the even predecessor `c'`
  (the Mahler core, the orbit's **only** randomness). The cycle entry→next-entry has **return time**
  `R = K + (even-run length)`.

**Kac/renewal identity [PROVEN, verified].** Over `N` steps with `M` cycles, `N=Σ R_i`, so the renewal rate is
`M/N = 1/E[R]`, and
> **even-density `= E[even-run]/E[R]`,  `E[R] = E[K] + E[even-run]`.   (Kac)**

Numerics (N=10⁵): even-density `0.50159`, `E[R]=3.996`, `E[K]=1.992`, `E[even-run]=2.004`, `1/E[R]=0.250`.
The induced first-return map `F` to the even set has return time `R`; `K_i` are the entry-depths (iid-geometric
`P(K≥k)≈2^{−(k−1)}` under Haar — measured ratio 0.95–1.00 through k=9, §3 table).

**The sharpening Kac gives, and where it stops [PROVEN].** Return-time **finiteness** is the **first moment**:
`E[R]<∞ ⟺ E[K]<∞`, and `E[K]≤ N/M` is a count, **free** (`VALUATION_BUDGET`, `EK2_SECOND_BUDGET §1`). But
`(K)` = `μ({1})=0` = mean depth bounded = `E[K²]<∞` is the **return-time energy / second moment**, NOT its
finiteness. **Kac controls E[R]; (K) needs E[R²]-type control. The renewal identity is silent on the second
moment** — the exact gap.

---

## 2. The supermartingale attempt — what an a-priori excursion estimate would have to be

We seek `W(c)` (NOT a function of V alone — `EK2_SECOND_BUDGET` proved every σ(d_n) potential telescopes to
itself; `MINPROP_COBOUNDARY_LP` proved every bounded residue potential is infeasible at the o=1 fixed point)
with a **provably negative conditional excursion drift** `E[ΔW | excursion start] ≤ −ε` derived from **proven
orbit arithmetic only** (countdown, archimedean growth `log c_{n+1}=log c_n+log(3/2)+o(1)` [PROVEN], white
feedback, first-moment budget), **without** assuming the K-law.

The diagnostic is the **conditional drift profile** `g(K)=E[ΔW | entry-depth K]`. The mean drift is
`Σ_K P(K)g(K)`. For W to bound `E[K²]` (= prove (K)), the **negativity of the drift must be EQUIVALENT to
`E[K²]<∞`** — which forces `g(K) ~ K²` (so the sum `Σ P(K)K²` is what must converge). If instead `g(K)` grows
slower than `K²`, the drift converges under a strictly larger class of K-laws (including `E[K²]=∞`), so its
negativity is **too weak** to certify (K).

---

## 3. Candidate W's, conditional excursion drift, and the adversary control [OBSERVED]

`excursion_supermartingale.py` (N=10⁵, M=25024 excursions). Drift = `W(c_{next entry})−W(c_{entry})`.

| candidate W | overall mean drift | profile `g(K)` | reads which moment |
|---|---|---|---|
| **W1 = α·log c + V** (α=−1, magnitude-aware) | **−1.62** | `g(K)≈−1.3·K` (LINEAR; `g/K²→0`) | **E[K] only** |
| **W2 = log·oddpart(c−1)** (3-adic/adelic; oddpart ×3 per step, `REPELLER §1`) | **+1.62** | `g(K)≈+K·log(3/2···)` (LINEAR, positive) | **E[K] only** |
| **W3 = h(c mod 2¹⁰)+V** (bounded residue + depth) | **≈0.000** | `g(K)≈0` until K>10, then `−(K−10)` | nothing (coboundary) |

The **tail-tilt** in W1/W2 (`g(K)/K` drifting from 1.0 to 1.3 as K grows) is the deterministic countdown
length feeding the `log c` / oddpart terms — strictly **O(K)**, never `O(K²)`. So for all three,
**mean drift = Σ_K P(K)·O(K) = O(E[K])** = a function of the **first moment alone**.

**Adversary control (the decisive test).** Build a synthetic excursion stream with **iid heavy-tailed**
`K_adv`, `P(K≥k)=k^{−1.2}` (so `E[K]≈` finite but **`E[K²]=∞`**; measured `E[K²]=5.8·10⁵`, maxK=3.3·10⁵), same
white per-step feedback, same matched even-run. Recompute each W's drift from the structure each W can
a-priori see:

| W | real-orbit drift | adversary drift (E[K²]=∞) | separates? |
|---|---|---|---|
| W1 = α log c + V | **−1.62** | **−3.59** (same sign, *more* negative) | **NO** |
| W2 = log oddpart(c−1) | +1.62 | +7.53 (same sign) | NO |
| W3 bounded+V | 0.000 | 0.000 | NO |

**No candidate separates the real orbit from the E[K²]=∞ adversary.** W1 is negative on *both* — its
negativity is genuine but certifies only `E[K]<∞` (free), exactly as `REPELLER_ESCAPE §4` / `MINPROP §5`
predicted for the magnitude-aware α<0 Lyapunov (it couples to the size-drift `D·log(3/2)`, a per-step
deterministic quantity, not to the excursion-height tail). The adversary satisfies **every proven fact**
(countdown, log-growth, white jumps, first-moment budget) yet has `E[K²]=∞`; hence **no argument using only
those proven facts can prove `E[K²]<∞`.** This is the rigorous form of `EK2_SECOND_BUDGET`'s "one `K≈0.585n`
run is permitted by every proven identity."

---

## 4. The §13/§14 unfaithful-model trap, caught [SOUNDNESS]

`exc_predictability.py` produces a **tempting false loophole**: the entry-depth K is *highly predictable*
from the pre-jump residue, `R²(K | c' mod 2^m) = 0.94, 0.98, 0.994, 0.998` for `m=6,8,10,12`. One could read
this as "K is foreseeable, so a state-dependent W can pre-load the `+K²` up-jump and BE a supermartingale."

**This is an artifact, rejected.** `K = v₂(3c'−1)` is by definition a **deterministic readout of the low
~K+1 bits** of the value; "predicting" K from `c' mod 2^m` is just reading the bits that *are* K — it adds no
foresight. The hard content is in two facts the R² hides:
1. A **level-m** residue W reads K only up to `K≤m`; the **tail** `K>m` (which alone drives `E[K²]`) is
   **invisible** to it — confirmed by W3's `g(K)=0` until K>10. The well-populated buckets (m=8, n≥30) show
   `E[K|res]` deviating from `E[K]` by up to 5.98 — i.e. the residue *names* small K but the large-K mass
   escapes any fixed level.
2. An **all-levels** W that reads K exactly is precisely the quadratic depth potential `Q=d²`, whose telescope
   (`EK2_SECOND_BUDGET §2`) is verified here **exactly**: `ΣK² = 148101 = 2·Σd − #{d≥1} = 148101`, and
   `Σd = ½(ΣK²+ΣK)` (`98971 = 98971`). It **closes on itself**: the `+K²` up-jumps are paid for by the
   `−(2d−1)` countdown decrements summing to the *same* `ΣK²`. Net information beyond the first moment: **zero**.

So the high R² is the unfaithful-model trap (a deterministic identity masquerading as predictability); the
white-jump no-go (K-autocorr ≤0.012, §3) is the faithful statement, and the iid adversary is the faithful
model. **No survivor.**

---

## 5. Why the route closes — the precise circular reduction [PROVEN reduction]

Assemble the three independent reasons, each [PROVEN] at its level:

- **(linear-drift / moment-mismatch).** Every W built from proven arithmetic has `g(K)=O(K)`; its mean drift
  reads `E[K]` (free), not `E[K²]`. To make negativity ⟺ `E[K²]<∞` you need `g(K)~K²`.
- **(white-jump no-go).** A W with `g(K)~K²` jumps up by `~K²` at each excursion start. The jumps are white
  (autocorr ≤0.012; `I(β;state)=3·10⁻⁵` bits, `CORE_CARRY_LEVER §2.2`), so a supermartingale must offset them
  by a **predictable** down-drift of size `E[K²]` per excursion. That drift is finite **iff `E[K²]<∞`** — the
  conclusion. Circular.
- **(telescoping no-go).** The unique `g(K)=K²` potential is `Q=d²`, which telescopes `ΣK²` to `2Σd−#{d≥1} =`
  itself (exact, §4). No second-moment information is created.

All three land on the same point: the missing quantity is the **conditional refill law** — `E_deep ≤ 2`
(`MINPROP_RUNS §3`), equivalently `Σ_k k·P(K≥k) < ∞`, equivalently the moving-middle-digit
`K=v₂(3c'−1)` equidistributes single-orbit. **That law IS the D-statistics IS (K).** The Kac identity gives
its first moment for free and is structurally silent on its second. **An a-priori excursion estimate is
impossible because the only object that would carry it (the refill/return-time law beyond first moment) is
exactly (K).**

---

## 6. Verdict (the prompt's asks)

| ask | answer | label |
|---|---|---|
| Kac/excursion formalization | even-density `=E[even-run]/E[R]`, `E[R]=E[K]+E[even-run]`; induced first-return map F, entry-depths `K_i` iid-geom under Haar; **Kac = first-moment (free), (K) = second-moment (open)** | [PROVEN] |
| Does an a-priori excursion supermartingale W exist (not assuming the K-law)? | **NO.** All candidates (W1 magnitude-aware, W2 adelic/3-adic, W3 bounded residue) have `g(K)=O(K)` → drift reads E[K] only → negative on the E[K²]=∞ adversary too → cannot certify (K) | [PROVEN reduction] |
| Any W surviving a shuffle/adversary control? | **None.** Heavy-tailed iid-K adversary (E[K²]=∞, white, first-moment-matched) gives the same drift sign as the real orbit for every W; satisfies all proven facts | [OBSERVED + PROVEN] |
| Precise reason it reduces to (K) | three [PROVEN] no-gos (linear-drift moment-mismatch / white-jump unpredictability / `Q=d²` telescopes to itself); all bottom out at the conditional refill law `E_deep≤2` = D-statistics | [PROVEN] |
| Exact missing input | `Σ_k k·P(K≥k)<∞` (`E[K²]<∞`), i.e. single-orbit equidistribution of `K=v₂(3c'−1)` = (K) = Mahler 3/2 / AEV Conj 1.6 | [OPEN] |

**Honest landing.** This closes the last un-pre-empted route named in `CORE_ORBIT_ARITHMETIC.md §5` with a
sharp no-go, not a breakthrough: the quenched Kac/excursion argument **provably reduces to (K)**. The reduction
is itself the deliverable — it pins *why* an a-priori excursion estimate cannot exist (the proven facts are
consistent with a heavy-tailed K, and the second moment is the conclusion, not a usable input). Consistent with
`EK2_SECOND_BUDGET` (count vs energy), `MINPROP_RUNS` (no one-sided margin), `MINPROP_COBOUNDARY_LP` (o=1
atom), `REPELLER_ESCAPE` (α<0 reintroduces genericity), `NONATOMIC_FIXEDPOINT` (first-vs-second-moment gap).

---

## 7. Sources

- **Repo [PROVEN/OBSERVED inputs]:** `CORE_ORBIT_ARITHMETIC.md §5` (the un-pre-empted shape); `CORE_CARRY_LEVER.md §2.2`
  (feedback white, I(β;state)=3·10⁻⁵); `NONATOMIC_FIXEDPOINT.md` (μ({1})=0 ⟺ E[K²]<∞); `EK2_SECOND_BUDGET.md`
  (Q=d² telescopes to itself; count vs energy); `MINPROP_RUNS.md` (countdown lemma, `freq(D=1)=1−1/E_deep`,
  no margin); `MINPROP_COBOUNDARY_LP.md` (bounded coboundary infeasible at o=1); `REPELLER_ESCAPE.md`
  (dual-repulsion, α<0 reintroduces genericity, adelic height degenerate); `VALUATION_BUDGET.md` (first-moment
  budget = count ≤ N).
- **Literature [repo knowledge]:** Kac return-time lemma; Mahler (1968, open); Andrieu–Eliahou–Vivion
  arXiv:2510.11723 (Conj 1.6 at α=8); Erdős/Salem (Rajchman ⟺ non-Pisot).
- **Numerics:** `excursion_supermartingale.py` (Kac identity; tail; conditional drift `g(K)` for W1/W2/W3;
  heavy-tailed adversary separation), `exc_predictability.py` (K-autocorr; the R²(K|res) trap; Q=d² telescope
  exact). Exact big-int, c₀=8/o₀=27, N=10⁵.

**No machine decided. No label upgraded.**
