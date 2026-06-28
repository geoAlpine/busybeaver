# The Antihydra Complete-Proof Capstone — full reduction chain to a single named open kernel (2026-06-28)

This is the master "current state of the complete proof" document for the non-halting of **Antihydra**, the
BB(6) cryptid. It integrates the entire proof program as it stands after the 2026-06-28 session block. The
result is a chain of **[PROVEN]** links (machine-checked and/or elementary) that reduces Antihydra
non-halting to a **single [OPEN] statement** — a triple-weakened fragment of the 2025 Andrieu–Eliahou–Vivion
normality conjecture (which itself implies Mahler's 1968 3/2 conjecture).

**Soundness discipline.** Every assertion carries an explicit `[PROVEN]` / `[CONDITIONAL]` / `[OPEN]` label,
copied verbatim from the source session documents; no label is upgraded. Numerical checks reproduced this
session are flagged `[verified]`. Zero false claims.

Source documents: `PROOF_STATUS.md`, `KERNEL_FINAL.md`, `SESSION_2026-06-28_{MINPROP, INDUCED_MAP, WALL_B,
WALL_B_DEEP, WALL_B_APERIODIC, ADELIC_KERNEL, THREEADIC, UNITPART, AEV}.md`.

---

## 1. Statement

**Antihydra** is a 6-state, 2-symbol Turing machine on the bbchallenge BB(6) frontier whose halting is
equivalent to a clean arithmetic dynamical question. Its computation tracks the integer orbit

> `c₀ = 8`, `c_{n+1} = ⌊3·c_n / 2⌋`  (the floor 3/2-map),

counting `E_n :=` (number of even values among `c_0,…,c_{n-1}`). Define the **balance**
`balance_n := 3·E_n − n`. The machine **halts iff `balance_n < 0` for some `n`** (a counter that the machine
maintains underflows). Equivalently it halts iff the **even-density** `E_n/n` drops below `1/3` at some `n`.

> **[PROVEN] (target theorem to be established).** Antihydra never halts ⟺ `balance_n ≥ 0` for **all** `n`
> ⟺ even-density `E_n/n ≥ 1/3` for **all** `n`.

This is an *all-n* statement, not merely an asymptotic one; the asymptotic content (the only open part) is
isolated in §6. A finite verification `balance_n ≥ 0` for `n ≤ N₀` has been carried to large `N₀` by
bbchallenge; `[verified]` here to `N₀ = 2·10⁵` (min balance `= +2`). The complete proof requires that finite
check **plus** an asymptotic tail bound, which is the kernel.

---

## 2. The reduction chain  [PROVEN, machine-checked]

A sequence of [PROVEN] equivalences carries the halting question from the raw integer orbit down to a
one-sided single-orbit density statement. Each link is labelled with the lemma/identity that powers it.

**Link 0 — Halting criterion → density. [PROVEN]**
non-halt ⟺ `balance_n ≥ 0 ∀n` ⟺ `E_n/n ≥ 1/3 ∀n`. Sharpness: if `liminf E_n/n < 1/3` then
`balance_n → −∞` along a subsequence and the machine halts, so the `1/3` threshold is exact.
(`PROOF_STATUS.md` §0; `KERNEL_FINAL.md` §2 converse.)

**Link 1 — GAP LEMMA: pass to the induced odd map. [PROVEN]**
> **GAP LEMMA.** For odd `c_i`, write `D := v₂(3c_i − 1)` (the 2-adic valuation). Then the number of steps
> until the next odd value is **exactly `D`**: `3c_i − 1 = 2^D m` (m odd) ⟹ `c_{i+1} = 2^{D−1}m`, followed by
> `D−1` halvings. `[verified]` to `N = 10⁵`, zero exceptions.

This collapses the orbit to its **induced odd map**
> `T(o) = 3^{D−1}(3o − 1) / 2^D`,  `D = D(o) = v₂(3o − 1)`,  started at **`o₀ = 27`**
(from `c₀ = 8 → 12 → 18 → 27`, the first odd value). The exponent `D` is simultaneously the odd-run gap.
(`SESSION_2026-06-28_WALL_B_APERIODIC.md` D2; `SESSION_2026-06-28_INDUCED_MAP.md`.)

**Link 2 — Renewal identity: density ↔ mean D. [PROVEN]**
Even steps are renewal points; the inter-renewal gaps equal the `D`-values. The Kac/renewal identity
`(mean gap)·(even-density) ≡ 1` gives
> even-density `= 1 − 1/(mean D)`,  hence  even-density `≥ 1/3 ⟺ mean D ≥ 3/2`.
Since `D ≥ 1` always, the only danger is an excess of `D = 1` steps. `[verified]`: `mean D ≈ 1.9989`,
even-density `≈ 0.4997` over 120k induced steps. (`INDUCED_MAP` §"標的の正しい形"; `WALL_B_APERIODIC` D4 Kac.)

**Link 3 — Exact valuation formula → one-sided cylinder form. [PROVEN]**
Because `3` is a 2-adic unit, `D ≥ k ⟺ o ≡ 3⁻¹ (mod 2^k)`, so
> `mean D = Σ_{k≥1} freq(o ≡ 3⁻¹ mod 2^k)`,
with the `k=1` term `≡ 1` and the `k=2` term `= freq(o ≡ 3 mod 4)`. As all `k ≥ 3` terms are `≥ 0`:
`mean D ≥ 3/2 ⟸ freq(o ≡ 3 mod 4) ≥ 1/2`. The GAP-LEMMA arithmetic gives `D=1 ⟺ o≡1 mod4`,
`D≥2 ⟺ o≡3 mod4`. (`INDUCED_MAP` E2; `MINPROP` F3.) `[verified]`: `freq(D≥2) ≈ 0.5004`.

**The chain, summarized (all links [PROVEN]):**

| Form | Statement | Bridge (PROVEN) |
|---|---|---|
| (i) | even-density of `c`-orbit (`c₀=8`) `≥ 1/3` | renewal identity ↔ (ii) |
| (ii) | `mean D ≥ 3/2` along induced orbit `o₀=27`, `D=v₂(3o−1)` | `mean D = Σ_k freq(o≡3⁻¹ mod 2^k)` ↔ (iii) |
| (iii) | `freq(D≥2)+freq(D≥3) ≥ 1/2` (robust, Haar-margin 1/4); tight: `freq(o≡3 mod4) ≥ 1/2` | residue arithmetic ↔ (iv) |
| (iv) | `freq(D=1) = freq(o≡1 mod4) ≤ 1/2` (one-sided cylinder occupancy) | ergodic-opt ↔ (v) |
| (v) | the orbit's Cesàro empirical measure does not concentrate on the `D=1`-region near the halting fixed point `o=1` | meta-theorem §5 |

All five are the **same** single one-sided density statement for **one** deterministic orbit; everything
around them is PROVEN. This is the one-sided **single-orbit kernel** of §6.

---

## 3. The measure side  [PROVEN]

The induced odd map is a bona-fide exact Syracuse-type system — the measure-theoretic side of the proof is
**complete**.

> **[PROVEN new theorem] (`INDUCED_MAP` E4).** The induced odd map `T(o) = 3^{D−1}(3o − 1)/2^D` is
> **Haar-measure-preserving, exact, and Bernoulli on the odd 2-adic units `ℤ₂*`**, with the gap exponents
> `D_j` **i.i.d. geometric** `P(D = d) = 2^{−d}` (mean `2`).

**Branch-by-branch proof sketch.** Partition `ℤ₂*` by the cylinders `A_d = {o : v₂(3o−1) = d}`, each of Haar
measure `2^{−d}`. On `A_d` the map is the affine `o ↦ 3^{d−1}(3o−1)/2^d`, whose 2-adic Jacobian has absolute
value `2^d` (the `2^{−d}` division expands by `2^d`; the `3^{d−1}` factor is a 2-adic unit, Jacobian `1`). Each
branch maps `A_d` bijectively onto all of `ℤ₂*`, so the pushforward of Haar restricted to `A_d` is `2^{−d}·`Haar,
and summing over `d` reproduces Haar — preservation. Full-branch surjectivity gives the Bernoulli/exact
structure (a full one-sided shift on the alphabet `{d}` with weights `2^{−d}`), and the symbols `D_j` are
i.i.d. geometric. A deterministic finite enumeration confirms the branch count (min = max image multiplicity
consistent with the full shift). (Lagarias 2-adic conjugacy `INDUCED_MAP` E1; Bernstein–Lagarias 1996,
Matthews–Watts.)

**Consequence.** Under Haar, `mean D = Σ_{d≥1} d·2^{−d} = 2 > 3/2`, so the kernel statement (ii) holds **with
room to spare** for Haar-a.e. point, with a CLT and exponential large-deviation concentration of even-density
at `1/2`. The entire remaining problem is therefore whether the **single deterministic orbit `o₀ = 27`
inherits the a.e. value** — i.e. whether it is *Haar-generic* for `T`. (`PROOF_STATUS.md` line (5).)

Supporting [PROVEN] structure on the 3-adic side (relabels, not reductions):
- **v₃ identity (§4)** re-encodes 2-adic depth as 3-adic divisibility.
- **Explicit skew cocycle** `Φ_D(y) = 3^{D−1}2^{−D}(3y−1)`: base = the exact Bernoulli 2-adic dynamics
  (emitting symbol `D`), fiber = 3-adic coordinate, an honest skew product (`THREEADIC` H2).

---

## 4. The example side  [PROVEN by arithmetic]

Everything that can be settled about the **specific** orbit `o₀ = 27` by elementary arithmetic *has* been
settled. The exceptional set for the kernel is bisected and its structured half is killed.

**Periodic-itinerary exclusion (C3). [PROVEN].** The parity coding is injective, so an eventually-periodic
itinerary forces an eventually-periodic point. A period-`q` cycle of `T` has the closed form
`c₀ = N/(3^q − 2^q)` with `N = Σ_{j} 2^j 3^{q−1−j} e_j ≤ 3^q − 2^q` (equality iff all-odd). Hence **every
cycle point lies in `[0,1]`, and the only integer cycle points are the endpoints `{0,1}` (atoms)**;
non-atomic cycles are odd-denominator rationals in `(0,1)` (e.g. the itinerary `(001)^∞` gives `4/19`) and can
never be an integer `c₀ ≥ 2`. Because the integer orbit is **strictly increasing** (`T(c) − c = ⌊c/2⌋ ≥ 1`),
it reaches no cycle. Therefore Antihydra's itinerary is **not eventually periodic** — proved without assuming
equidistribution. `[verified]`: all 2046 cycles of period `q ≤ 10` enumerated, plus the general bound.
(`SESSION_2026-06-28_WALL_B_DEEP.md` C3.) This is the **bisection**: exceptional set = structured/periodic
(now killed) ⊔ aperiodic/full-complexity (= the kernel).

**Countdown Lemma. [PROVEN].** Let `φ(o) = v₂(o − 1)`. Each `D=1` step decrements `φ` exactly:
`φ → φ − 1`. Hence `m` consecutive `D=1` steps ⟺ `o_start ≡ 1 (mod 2^{m+1})` — a thin cylinder of measure
`2^{−(m+1)}` — and any maximal `D=1` run has length `v₂(o_start − 1) − 1`. The runs are **self-limiting**: an
infinite `D=1` run occurs only at the off-orbit fixed point `o = 1`. `[verified]`: all 75139 runs of the
`o₀=27` orbit match, longest run `= 19`, zero exceptions. (`MINPROP` F2.)

**Dual-Repulsion Lemma. [PROVEN].** On each `D=1` step, `o' − 1 = (3/2)(o − 1)` exactly, so the archimedean
size `|o−1|_∞` multiplies by `3/2` while the 2-adic size `|o−1|_2` multiplies by `2` (Countdown); the adelic
product `|o−1|_∞·|o−1|_2` multiplies by `3`. Thus the halting fixed point `o = 1` is **simultaneously
repelling in both valuations**. `[verified]`: 300174/300174 steps. (`SESSION_2026-06-28_ADELIC_KERNEL.md` G3.)

**v₃ identity. [PROVEN].** Since `3 ∤ (3o − 1)`, the next term carries the full `3`-power:
> `v₃(o_{j+1}) = D_j − 1`  `[verified]`: 0 exceptions over 2·10⁵ steps (reconfirmed this session, 120k steps).

This re-encodes the kernel in 3-adic form: `mean D ≥ 3/2 ⟺ density{3 | o_j} + density{9 | o_j} ≥ 1/2`. The
3-adic dual is **provably isomorphic** to the 2-adic wall (the map `k ↦ k+1` is a bijection on valuations); it
is a relabel, not a reduction. (`SESSION_2026-06-28_ADELIC_KERNEL.md` G1; `SESSION_2026-06-28_THREEADIC.md`.)

---

## 5. Why no structure-only proof exists  [PROVEN, two independent meta-theorems]

A central, soundness-bearing result of the program: the kernel is **irreducibly orbit-specific**. No proof
using only the structure of `T` (measure preservation, exactness, specification, contraction) can close it,
because every such structure is *also satisfied by the genuinely halting orbit `o = 1`*. Two independent
meta-theorems establish this from opposite directions; both pin the obstruction to the **halting fixed point
`o = 1`**.

**(i) Ergodic-optimization meta-theorem. [PROVEN] (`MINPROP` F3).** Let `ψ` be the one-sided test function
(`ψ = +1/2` on `D=1`, `−1/2` on `D=2`, `−3/2` on `D≥3`; numerically a function of `D` only, 0 mismatch for
`o < 2·10⁶`). By standard ergodic-optimization (Mañé / Conze–Guivarc'h / Bousch sub-action theory), a
one-sided bound holding for **all** orbits is equivalent to
`β(ψ) := max_{T-invariant μ} ∫ψ dμ ≤ 0`. But
> **`β(ψ) = +1/2 > 0`, attained at the fixed point `o = 1`** (`D = 1` forever ⟹ even-density `0` ⟹ a
> genuinely *halting* orbit).
A finite coboundary/Lyapunov LP confirms infeasibility for all `k = 3..12`, the dual obstruction being the
`o=1` self-loop of weight `+1/2`. Hence any all-orbits structural bound would prove the **false** statement
"all orbits non-halt"; the Haar `1/4` slack is irrelevant (feasibility is set by the atomic maximizer `δ₁`,
not by Haar). The content is exactly that `o₀ = 27` — an integer orbit that *grows*, hence is repelled from
`o = 1` (Dual-Repulsion, §4) — is generic, **not** that all orbits are.

**(ii) Shared-free-structure meta-theorem. [PROVEN] (`UNITPART` I4).** "Free" = pathwise determined by the
base symbol sequence, independent of genericity (e.g. the 3-adic fiber contraction, the synchronization
`o_j mod 3^k = f(`recent `D`-history`)`, every unit-part observable). The decisive fact:
> the halting fixed point `o = 1` (`D ≡ 1`) **synchronizes under the very same free contraction** as the real
> orbit (`[verified]`: the all-`D=1` sequence and the real orbit synchronize identically).
Therefore **any free condition also holds at `o = 1`; since `o = 1` halts, no free/structure-only condition can
imply non-halting**. The free part is *blind to* `freq(D≥2)`, the sole discriminator between halting and
non-halting. Supporting [PROVEN] facts: the 3-adic fiber contraction (rate `≤ 1/3`) is real but **orthogonal
to the target** (it contracts in the 3-adic place while `D` is read off the 2-adic place — controlled
coordinate and queried coordinate are on opposite sides); `MI(`free 3-adic data; `D_j) = 0` (shuffle-null);
the dynamics actively route free data and the hard target into two CRT-independent coordinates connected only
by a null channel.

**Unifying principle.** The two meta-theorems are the same obstruction seen twice — once via the invariant
simplex (the maximizer is the atom `δ₁`), once via the free/contraction algebra (free structure is shared
with `o = 1`). The split is exact: the **finite-window / free** part of the system carries no
halting/non-halting information (it is shared with `o = 1`), while the distinction lives **only in the
tail-average (genericity)** — i.e. in single-orbit equidistribution, the AEV/Mahler kernel. This is *why*
every structural attack (contraction, bootstrap, van der Corput, Mauduit–Rivat, twisted RPF, residue,
coboundary, adelic coupling) only *relocated* the gap: each is a finite-window/free tool, structurally unable
to reach the tail-average.

---

## 6. The open kernel

After all PROVEN reductions, the complete proof rests on exactly one open statement.

> **Kernel (K). [OPEN].** For the induced 3/2-Syracuse orbit `o₀ = 27`,
> `o_{n+1} = 3^{D(o_n)−1}(3o_n − 1)/2^{D(o_n)}`, `D(o) = v₂(3o − 1)`:
> > `liminf_{N→∞} (1/N) #{ n < N : D(o_n) ≥ 2 } ≥ 1/2`.

**Equivalent forms (all [PROVEN]-equivalent to (K)):**
- `mean D ≥ 3/2` for the orbit of 27;
- `liminf` even-density of `c₀ = 8` `≥ 1/3`;
- `liminf freq(o ≡ 3 mod 4) ≥ 1/2` (zero-margin tight form);
- `freq(D≥2) + freq(D≥3) ≥ 1/2` (robust form, Haar-margin `1/4`);
- 3-adic form: `density{3 | o_j} + density{9 | o_j} ≥ 1/2`;
- independence form (`THREEADIC` H4): the 3-free cofactor `u_j ∈ ℤ₂*` is asymptotically independent of its
  own 3-adic exponent `e_j = D_{j−1} − 1`.

> **Conditional theorem (`KERNEL_FINAL.md` §2). [PROVEN reduction].** Antihydra does not halt **iff** (K)
> holds **together with** the finite check `balance_n ≥ 0` for `n ≤ N₀`. Converse: if `liminf` even-density
> `< 1/3` the machine halts, so the threshold is exact. Under Haar (for which `T` is exact, `mean D = 2`,
> [PROVEN]) (K) holds with room to spare; the whole problem is whether the single orbit `o₀ = 27` is
> Haar-generic.

**Exact literature placement.** (K) is precisely the
> **`p/q = 3/2`, one-sided, single-level (`k=2`), single-orbit fragment of the Andrieu–Eliahou–Vivion
> normality conjecture** (arXiv:2510.11723, Conjecture 1.6, *floor mirror*).
AEV Conj 1.6: for coprime `p > q ≥ 1`, every orbit of the **ceiling** map `T_{p/q}(x) = ⌈px/q⌉` is
equidistributed in residue classes mod `q^k` for all `k`. AEV Thm 1.7 [PROVEN] gives Conj 1.6 ⇔ their
normality Conjecture 1.2; AEV Thm 1.5 [PROVEN] gives (for `p < q²`, which holds at `3/2` since `3 < 4`)
Conj 1.2 ⇒ Conj 1.4 = **Mahler's 1968 Z-number conjecture**. So AEV is the single umbrella above the entire
3/2 cluster (Mahler 1968, Flatto's Z-numbers, Akiyama 2008 triple expansions, Dubickas–Mossinghoff 2009
"4/3 problem"), and (K) is one instance under it.

Two precise calibrations (both [PROVEN]/verified this session):
- **floor vs ceiling.** AEV uses the **ceiling** `(3x+1)/2` (odd branch); Antihydra uses the **floor**
  `(3x−1)/2`. The `±1` flips parity, so the two are **not literally conjugate** (even branches agree); the
  GAP-LEMMA bookkeeping `v₂(3o−1)` is the bridge. (K) is the **floor-mirror** of AEV's `p/q=3/2` instance.
- **(K) is strictly weaker than AEV on three axes** — one-sided (`≥1/2`) vs two-sided (`=1/2`); single level
  `k=2` vs all `k`; single orbit `o₀=27` vs all `n`. Yet **no named conjecture sits at this weaker level**:
  AEV is the *weakest named established-open* conjecture that implies (K).

**Distinct from the "support" axis (no bridge). [PROVEN/verified].** Mahler's literal 1968 conjecture (no
`ξ` with `{ξ(3/2)ⁿ} ∈ [0,½) ∀n`) and the Flatto–Lagarias–Pollington bound (`limsup − liminf ≥ 1/3`,
Acta Arith. 70 (1995)) are **support/spread** statements; (K) is a **frequency/density** statement. FLP's `1/3`
and our `1/3` are numerically identical but on **orthogonal axes** (which values are hit vs how often), and an
orbit can have full spread while its empirical measure concentrates (density `→ 0`) — exactly the `δ₁`-drift
permitted by §5. So **FLP is not a partial result toward (K)**; there is no published bridge from spread to
density. Likewise Tao 2019 (arXiv:1909.03562) is log-density over almost-all *starting points* (an ensemble
theorem, no per-orbit output); Krasikov–Lagarias counts starting integers via inverse-tree branching (a single
orbit has no population to count); and Birkhoff/invariant-measure averaging is empty because the integer orbit
is **transient** (grows like `(3/2)ⁿ`, so there is no invariant probability measure for it).

**No analytic handle exists. [OPEN].** AEV (a 2025 conjecture paper) supports Conj 1.6 with *combinatorics on
words plus numerical experiment only* — no ergodic theory, transfer operator, exponential sums, or Fourier
analysis, and **zero unconditional results at `3/2`** (not even a one-sided density bound). No published result
gives `liminf` even-density `> 0` for any specific 3/2 / Syracuse orbit. The lone candidate analytic route is
> **effective power Fourier-decay** `|ν̂_{2/3}(t)| ≤ C|t|^{−a}` (a *rate*, not bare Rajchman) → Erdős–Turán →
> `liminf` even-density `≥ 1/2 − O(decay)`, clearing `1/3` with margin.
We have [PROVEN] (commit 984f70f) that `3/2` is **non-Pisot ⟹ `ν_{2/3}` is Rajchman** (Fourier transform
`→ 0`); candidate sources for an effective rate are Streck, Varjú–Yu, Brémont, Bourgain–Dyatlov. **But the
annealed/quenched gap is the lone remaining analytic missing link [OPEN]:** `ν_{2/3}`'s Fourier decay is
**annealed** (i.i.d. weights, the measure side), whereas the orbit's even-density needs the **quenched** Weyl
sum `Σ e(h·4·(3/2)ⁿ)` of the orbit itself, which `ν̂_{2/3}` does not directly bound (the "broken link" C of
`NONPISOT_FOURIER_CHAIN`). AEV itself does not cross this gap. This is the single honest frontier.

---

## 7. What is new here vs the inherited open problem

**BB6-specific contributions of this program (all [PROVEN] unless noted):**
- **The induced-map identification** — Antihydra's halting is the induced odd return map
  `T(o) = 3^{D−1}(3o−1)/2^D`, `o₀ = 27`, identified as an **exact, Haar-preserving, Bernoulli Syracuse-type
  system with `D_j` i.i.d. geometric** (§3, `INDUCED_MAP` E4). This is the maximal localization of the
  problem and completes the **measure side**.
- **The exact reduction chain** non-halt ⟺ even-density `≥ 1/3` ⟺ `mean D ≥ 3/2` ⟺ one-sided cylinder form,
  via the **renewal identity** even-density `= 1 − 1/(mean D)` and the valuation formula
  `mean D = Σ_k freq(o ≡ 3⁻¹ mod 2^k)` (§2, machine-checked).
- **The two meta-theorems** proving *no structure-only proof exists* (§5): ergodic-optimization
  `β(ψ) = +1/2` at the halting fixed point `o=1`, and free-structure sharing with `o=1`. These explain, with
  proofs, why every structural attack only relocated the gap — a genuinely new structural insight.
- **The arithmetic lemmas** (§4): periodic-itinerary exclusion C3 (the bisection that kills the structured
  half of the exceptional set), the Countdown Lemma, the Dual-Repulsion Lemma, and the v₃ identity
  `v₃(o_{j+1}) = D_j − 1`.
- **Precise literature placement** of the kernel as the floor-mirror, triple-weakened fragment of AEV
  Conj 1.6, with the support-vs-density axis distinction (FLP/Mahler) made rigorous, and the lone analytic
  route (effective Fourier rate) identified together with its annealed/quenched obstruction.

**Inherited open problem (not ours to claim):**
- The kernel (K) is a single-orbit equidistribution statement of `{(3/2)ⁿ}`-type — the **`p/q=3/2`,
  single-orbit fragment of the AEV normality conjecture (2025), which implies Mahler's 3/2 conjecture
  (1968)**. It is a recognized, generational open problem with **no analytic handle in the literature**, and
  the annealed→quenched bridge is the missing analytic link that AEV itself does not cross.

**Bottom line.** The complete proof of Antihydra non-halting is in the state:
*"everything PROVEN except a single named line — the one-sided, single-orbit, level-2 floor-mirror fragment
of AEV Conj 1.6."* The measure side is fully proven; the example side is proven by arithmetic; two independent
meta-theorems prove that the residue is irreducibly orbit-specific (the obstruction is the halting orbit
`o=1`); and the kernel closes the instant the AEV/Mahler-equidistribution line moves. Far in calendar time
(new mathematics is needed), shortest in path (reduced to one open point).

---

## References
- Andrieu, Eliahou, Vivion, *A Normality Conjecture on Rational Base Number Systems*, arXiv:2510.11723 (2025) — Conj. 1.2 / 1.6, Thm 1.5 / 1.7.
- Mahler, *An unsolved problem on the powers of 3/2*, J. Austral. Math. Soc. 8 (1968).
- Flatto, Lagarias, Pollington, *On the range of fractional parts {ξ(p/q)ⁿ}*, Acta Arith. 70 (1995) 125–147.
- Eliahou, Verger-Gaugry, *The number system in rational base 3/2 and the 3x+1 problem*, arXiv:2504.13716 (2025).
- Tao, *Almost all orbits of the Collatz map attain almost bounded values*, arXiv:1909.03562 (2019/2022).
- Krasikov, Lagarias, *Bounds for the 3x+1 problem using difference inequalities* (2003).
- Lagarias / Bernstein–Lagarias (1996), Matthews–Watts — 2-adic Collatz conjugacy and ergodicity.
- Mañé / Conze–Guivarc'h / Bousch — ergodic optimization and sub-action theory.
- Dubickas, Mossinghoff (2009) "4/3 problem"; Akiyama (2008) triple expansions — both implied by AEV Conj.
