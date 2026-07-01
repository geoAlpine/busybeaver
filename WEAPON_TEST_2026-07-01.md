# Adversarial weapon-test of the 2026-06-30/07-01 session results (2026-07-01)

*Adversarial audit: for each significant result accumulated this session, TRY HARD to weaponize it — (a) prove a
partial toward the kernel `(K)` = Mahler 3/2 / AEV, (b) decide (halt / non-halt) any BB(6) machine, or (c) produce a
strictly-NEW unconditional bound — then rule honestly. SOUNDNESS: verdicts labelled WEAPON / DESCRIPTIVE /
NEGATIVE-BARRIER. Independent numerics re-run (`scratchpad/verify.py`, exact big-int, `N=3·10⁵`,
`/Users/aokiyousuke/quantum-ecc/.venv/bin/python`). NOT committed.*

---

## 0. Independent numerical re-verification (this audit's own run)

Confirmed, exact big-int, seed `c₀=8` → induced `o₀=27`, `N=3·10⁵` base steps (150 194 induced steps):

- **T5 Cramér:** `x=1/φ` gives `x³−2x+1 = 0.0` exactly; `θ*=log φ=0.481212`; `E[e^{−θ*X}]=1.0` (`X=2D−3`). ✓ exact.
- **T1 identity:** `#even = Σ(D_j−1) = 149 806`, `mean D = 1.99742`. ✓ (boundary `O(1)`, matches the doc's 149 805).
- **T4 balance walk:** running-min `B_n = 0` (attained only at `n=0`; never negative on the run), final drift
  `≈ +0.995`/induced step `= 2·meanD−3`. Max drawdown from running peak `= 27`. ✓ supercritical, empirically.
- **Drawdown ratio:** `P(draw=s)/P(s−1) ≈ 0.618 = 1/φ` for `s=1..11` (0.62±0.02). ✓ matches golden-ratio LDP.
- **hyp-C (50/50):** after a `D=1` step, continue `37 571` / stop `37 564`, ratio `0.50005`. ✓ ½-mixing.
- **Depth tail:** `P(D≥k) = 2^{1−k}` to 3–4 digits, `k=1..9`. ✓ geometric.

Every descriptive claim checks out. The audit below concerns whether any of it *weaponizes*.

---

## 1. Per-result weapon table

| Result | Best-case weaponization attempt | Works? | Honest reason |
|---|---|---|---|
| **T1 occupancy identity** `#even=Σ(D_j−1)=Σ_{k≥2}N_k` | Reformulate `(K)` as cumulative 2-adic-cylinder occupancy; hope the exact identity yields a floor | **DESCRIPTIVE** | Exact but a *reformulation* (valuation budget). A lower bound on `ΣN_k` = cylinder-visit **frequency** control = `(K)` (EVEN_COUNT_FLOOR §2–3). Tautology, not a bound. |
| **T2 RG / fixed-point line** | Use the relevant eigenvalue `1/(1−a)` / critical point `a=2/3` to force the orbit's tail rate | **DESCRIPTIVE** | RG acts on **depth-law space** (annealed measures), not on the single orbit. The orbit's actual `a` is quenched = `(K)`. Structural picture only. |
| **T3 family-wide RG** | Cross-machine leverage (hyp 5) | **DESCRIPTIVE** | Ports the annealed structure across `{v_p(μ)=−1}`; the halt-threshold and the quenched core stay **per-machine** (independent `(K)`'s). |
| **T4 balance-walk drift** `2−3/meanD`, zero at `3/2` | Prove drift `>0` unconditionally ⇒ even-density bounded below ⇒ non-halt | **DESCRIPTIVE / =(K)** | Drift-formula is exact algebra; but `drift>0 ⟺ liminf meanD>3/2` is **itself `(K)`** (Rmk 4.2). Elementary run-ceiling `0.585·idx` > a.e. drift `0.5·idx` (deficit `1.17×`), consistent with both halting and non-halting. |
| **T5 golden-ratio Cramér** `θ*=log φ` | Deterministic Lundberg supermartingale `e^{−θ*Sₙ}` ⇒ pathwise ruin bound (hyp 1) | **NEGATIVE-BARRIER** | Exact NEW algebraic *fact* (verified), but the martingale is an **annealed** (i.i.d.-expectation) object. A pathwise/deterministic realization is exactly a bounded sub-action `ψ≤g∘T−g` — the **(C1) coboundary proven infeasible** by No-Structure (`δ₁` maximizer `∫ψ=+½>0`). |
| **T5.2 two-parameter `(p,m)` Cramér family** `(p−1)xᵐ−px+1=0` | Cross-machine constraint via shared algebraic constants (hyp 5) | **DESCRIPTIVE** | Elegant unification of annealed constants ((m−1)-bonacci); carries no quenched/orbit information between machines. |
| **T6 / GOF quenched match** (χ²=0.43, indep=0.44, moments) | Use "passes all i.i.d. tests" as proof evidence (hyp 6) | **DESCRIPTIVE / HEURISTIC** | Finite-`N` empirical match. By No-Structure a perfect annealed/statistical match **cannot select** the orbit from a violating orbit; is *precisely* single-realization genericity `=(K)`. (Runs-test `z` overflowed int64 — caveat, not result.) |
| **EVEN_COUNT_FLOOR** (`Θ(log n)` sharp; no rung to `(K)`) | Extract a super-log unconditional `#even` bound | **NEGATIVE-BARRIER** | *Proves the opposite*: `0.89 log₂n` (prior, magnitude-ceiling) is sharp; any `ω(log n)` improvement = cylinder frequency = `(K)`. `[ARGUED]` (reduction, not meta-theorem). No new bound; ladder collapses to 2 levels. |
| **SINGLE_REALIZATION_WALL** (linkage ½-mixing) | Deterministic linkage `D_{j+1}=f(o_j)` imposes a quenched rigidity i.i.d. lacks | **NEGATIVE-BARRIER** | At the decisive `D=1` transition the next residue is `50/50` (verified `0.50005`): the linkage is ½-mixing, **no rigidity**. Wall stands `=(K)`. |
| **BB6_NO_STRUCTURE_THEOREM** (C1/C2/C3 + magnitude/adelic) | — (it is the barrier) | **NEGATIVE-BARRIER** `[PROVEN]` | The master obstruction: no measure/all-orbits/coboundary certificate (bounded or magnitude-aware/adelic) selects `o₀`. This is *why* every row above stops. |
| **RANK1_AMENABLE (Coverage No-Go)** | Point an existing effective-equidistribution framework at `T(d)` | **NEGATIVE-BARRIER** (Tier-1 `[PROVEN]`, intersection `[SURVEY ~85%]`) | Every named framework's *hypothesis* fails (rank-1, amenable, hyperbolic, degree-1, growing height, endogenous carry). Positioning, not a proof; `T(d)⟹(K)`. |
| **DECIDER_PREEMPTION** | Run bbchallenge MITM-WFA / any decider | **NEGATIVE-BARRIER** (Kind R `[PROVEN]`, Kind W `[ARGUED]`) | Regular deciders → (C2) (safe set `3E≥O` non-regular, full complexity); weighted → (C1) sub-action (infeasible). No decider class escapes; residual gaps = taxonomy-completeness + MITM-WFA closure semantics. |
| **o17 exact-linear off 3ℤ** (`H(k)` closed form, `k≢0 mod 3`) | Decide o17 via the linear regime (hyp 4) | **DESCRIPTIVE** | These are **HALTERS** in bounded time `O(k)` for an *embedded probe family* `0A01^k`, not the machine's actual start; a bounded halt is trivially decidable by simulation and is **not** a non-halting result. |
| **o17 no 1-D reduction** (multi-digit odometer) | — | **NEGATIVE-BARRIER** | Honest negative: o17's kernel is a base-3 string/carry dynamics, no scalar-Collatz reduction; different, harder obstruction type. Open. |
| **DEPTH_REACH / NEW_METHODS_SWEEP** (log-vs-linear gap) | Combine #1 Diophantine + #2 adaptive Oseledets (hyp 7) | **NEGATIVE-BARRIER** | Localizes the wall as a `Θ(n/log n)` depth-reach gap; the one untried combination is `[PROVEN-backed]` collapsed on that same gap (HAIRLINE_CRACK_PROBE). |

---

## 2. The seven weaponization hypotheses, stress-tested

**H1 — Quenched golden-ratio LDP / deterministic Lundberg supermartingale?**
*Steelman.* `E[e^{−θ*X}]=1` (verified exactly) makes `Mₙ=e^{−θ*Sₙ}` a martingale in the i.i.d. model; optional
stopping gives the annealed ruin bound `P(dip to −a) ≤ e^{−θ*a}` — the source of the "halts w.p. `10^{−2439…}`"
heuristic. If `Mₙ` were a **pathwise supermartingale** (`E`-free), the seed orbit's non-halting would follow.
*Ruling.* **NO WEAPON — NEGATIVE-BARRIER (annealed-not-quenched).** A pathwise/deterministic supermartingale is
exactly a bounded sub-action `ψ ≤ g∘T − g`, which is register **(C1)**, `[PROVEN]` infeasible: the halting fixed
point `δ₁` (`T(1)=1`, `ψ=+½`) is an ergodic-optimization maximizer with `∫ψ dδ₁=+½>0`, so no such `g` exists at any
level (exact `Fraction` LP, `k=3..12`), and the magnitude-aware/adelic extension is closed by sign tension + product
formula. The paper (§7) itself concedes "the Lundberg supermartingale has no exact deterministic (coboundary)
realization." The martingale is genuinely new and exact **as an annealed fact**; it is not a quenched bound.

**H2 — Balance-walk criticality ⇒ drift>0 unconditionally?**
*Steelman.* Drift `= 2−3/meanD` (verified: `+0.995`/induced step for the orbit); if some elementary argument forced
`meanD>3/2`, non-halting would follow, and criticality-at-`3/2` looks like a phase-transition handle.
*Ruling.* **NO WEAPON — DESCRIPTIVE, `= (K)`.** `drift>0 ⟺ liminf meanD>3/2 ⟺ liminf even-density >1/3`, which is
`(K)` (indeed a hair stronger). The only unconditional handle on `meanD` is the magnitude/run ceiling `0.585·idx`,
which exceeds the a.e. drift `0.5·idx` (deficit `1.17×`) — consistent with **both** outcomes. Drift-positivity for
the specific orbit is the kernel itself, not a lever on it.

**H3 — Occupancy identity / RG line ⇒ new unconditional `#even` floor beyond `0.89 log n`?**
*Steelman.* `#even = Σ_{k≥2}N_k` is exact; the RG fixed-point line pins the annealed profile; maybe the structure
forces cumulative occupancy above `log`.
*Ruling.* **NO WEAPON — NEGATIVE-BARRIER.** EVEN_COUNT_FLOOR `[PROVEN]`+`[ARGUED]`: `0.89 log₂n` (which is *prior*,
from the magnitude ceiling, not new this session) is **sharp**; any `ω(log n)` improvement is a super-log lower bound
on cylinder-visit **frequency** = quenched 2-adic occupancy = `(K)`, and a large depth is a *near-halt*, so bounding
the tail **is** proving non-halting. No unconditional rung lives between `Θ(log n)` and `(K)`. The RG line is an
annealed object and adds no orbit floor. (This is a valuable *negative* meta-result — it deflates the optimistic
ladder — but it is not a new bound and not `[PROVEN]` as a meta-theorem over all proofs.)

**H4 — o17 exact-linear off 3ℤ ⇒ decide o17?**
*Steelman.* Two-thirds of the embedded seeds (`k≢0 mod 3`) halt with a closed-form `H(k)`; if o17's real start sat
in that regime, o17 would be decided (HALT).
*Ruling.* **NO WEAPON — DESCRIPTIVE (bounded-halt-not-non-halt; probe-family-not-start).** The linear formulas are
**halters in bounded time `O(k)`** for the *probe family* `0A01^k`, not the machine's actual initial configuration; a
bounded halt is trivially decidable by direct simulation and proves nothing about non-halting. o17's genuine kernel
lives on the `k≡0 mod 3` sublattice, is Collatz-hard / undecidable-by-cap (the `k=21` slow-halter caveat), and
`[OBSERVED]` has **no 1-D Collatz reduction** (multi-digit base-3 odometer). Nothing decided; obstruction is a
different, harder type than the Mahler family.

**H5 — Family-wide / two-parameter Cramér ⇒ cross-machine argument?**
*Steelman.* T3 (family-wide RG) and T5.2 (`(p,m)` Cramér, (m−1)-bonacci constants) unify the cryptids; maybe one
machine's data constrains another.
*Ruling.* **NO WEAPON — DESCRIPTIVE.** The unification is entirely at the **annealed/structural** level (same RG,
analogous algebraic constants). T3 states the halt-criticality threshold is **per-machine**, and each machine's
quenched core is its own independent single-orbit equidistribution. There is no shared quenched fact for a
cross-machine transfer to exploit — the quenched cores are precisely the separate, mutually independent `(K)`'s.

**H6 — Quenched i.i.d.-match (GOF passing) usable in a proof?**
*Steelman.* The depth sequence passes χ²-GOF (`p=0.43`), independence (`p=0.44`), autocorrelation, and all moment
tests — "statistically indistinguishable from i.i.d. geometric." Strong evidence for non-halting.
*Ruling.* **NO WEAPON — DESCRIPTIVE / HEURISTIC.** GOF passing is a finite-`N` empirical statement; it is *exactly*
the single-realization genericity that constitutes `(K)`. By No-Structure, an annealed/statistical match cannot
distinguish the seed orbit from a violating orbit and so cannot enter a proof of orbit selection. (Caveat: the
runs-test `z` overflowed int64 — a numerical artifact, not evidence.) Consistent with non-halting; provably not a
handle.

**H7 — Latent combination weapon?**
*Steelman.* Perhaps T1 (identity) + T4 (drift) + T5 (LDP) + T6 (GOF) + linkage together prove what none does alone.
*Ruling.* **NO WEAPON.** Each ingredient is either (i) exact-algebra/structural about the **annealed** model, or
(ii) a finite-`N` empirical match. Composing annealed/structural facts cannot manufacture a quenched selection — the
missing step is always the same one, and it is `(K)`. The one genuinely untried cross-tool combination in the program
(#1 Diophantine top-digit data + #2 adaptive Oseledets certificate) was already probed and `[PROVEN-backed]`
collapses on the log-vs-linear depth-reach gap (`Θ(n/log n)` short): #1 reaches only `Θ(log N)` depth and is
mutual-information-independent (`~10⁻⁵` bits) of the depth/parity bit #2 needs at depth `Θ(n)`. No latent weapon.

---

## 3. Is anything genuinely NEW and unconditional? (skeptical check)

- **`θ*=log φ` (T5)** and the **`(p,m)` Cramér family (T5.2)** are genuinely new, exact, proven identities. But they
  are facts about the **i.i.d./annealed model**, not unconditional statements about any orbit; they decide no machine
  and bound no orbit quantity. New mathematics, zero weapon value.
- **`#even = Σ(D_j−1)` (T1)** is exact and proven but a reformulation, not a bound.
- **`0.89 log₂ n`** is *not* new this session (prior, LIMIT_THEOREM). What is new is the `[ARGUED]` proof that it is
  **sharp** — a negative meta-result, not a bound.
- No result produces a strictly-new **unconditional** bound on `#even(n)`, subword complexity, depth, or any orbit
  statistic. No machine (Antihydra, o17, or family) is decided.

---

## 4. Overall verdict

> **USABLE WEAPON: NO.** Every result this session is either **DESCRIPTIVE** (an exact algebraic/structural fact
> about the annealed Haar/i.i.d. model, or a finite-`N` empirical match) or a **NEGATIVE-BARRIER** (No-Structure,
> the sharp-`Θ(log n)` floor-collapse, the Coverage No-Go, decider-preemption, the o17 halt-not-non-halt / no-1-D
> finding, the log-vs-linear localization). None proves a partial toward `(K)`, decides any BB(6) machine, or
> establishes a strictly-new unconditional bound.

**The single unifying reason.** Every result stops precisely at the **annealed↔quenched boundary**. Each lives in
one of the registers the `[PROVEN]` No-Structure-Only-Selection theorem rules out — the invariant measure (Haar/
i.i.d./LDP/GOF: register C3), all-orbits/topological structure (RG line, family unification, regular deciders: C2),
or a finite coboundary/sub-action (deterministic Lundberg, weighted deciders: C1) — plus exact identities whose
weaponized use requires quenched single-orbit **frequency** control. That quenched step — that the deterministic
seed-27 orbit *attains* the annealed statistics it exhibits, equivalently that its balance walk's quenched minimum
stays `≥0` — cannot be reached from any of those registers, because none reads data separating `o₀` from the halting
fixed point `δ₁` (an ergodic-optimization maximizer with `∫ψ dδ₁=+½>0`). That separating step **is** `(K)` = Mahler
3/2 / AEV. The session's value is architectural and cartographic (the cleanest structure the eventual quenched tool
must inhabit, and the sharpest map of why every tool stops), not a weapon.

**No machine decided. No label upgraded.** `(K)` remains `[OPEN]` = Mahler 3/2 / AEV.
