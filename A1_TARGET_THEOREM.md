# A1 — target theorem: rank-1 single-orbit effective equidistribution (2026-06-25)
*The foundational document of the reframed programme: not "solve Antihydra" but **"build rank-1 single-orbit
effective equidistribution."** Step 1 (per the plan) is to write the correct theorem statement and refine it by
**hunting counterexamples**, not by proving. Everything below is machine-tested; the statement is a CONJECTURE
shaped by the hunt, not a theorem. `A1_counterexample_hunt.py`.*

## The target statement (current best form, refined by counterexample)
> **Conjecture A1.** Let `μ = a/p` in lowest terms with `p` prime and `p ∤ a` (so `v_p(μ) = −1`), and let
> `T_μ(x) = ⌊μx⌋` act on `ℤ_p` (the clean `p`-to-1 exact endomorphism — *classification theorem*,
> `CRYPTID_KERNEL.md`). Suppose `log_p a` satisfies a Diophantine condition (finite irrationality measure;
> **hypothesis — see §Diophantine**). Then for every seed `x ∈ ℤ_p` that is
> - **(i) not eventually periodic** under `T_μ`, and
> - **(ii) not a preimage of the singular point** `s_μ` (the point with `v_p(a·x−1)=∞`, where the renewal jump
>   diverges; `s = 1/3` for Antihydra's `μ=3/2`),
>
> the **empirical measures** `(1/n)Σ_{k<n} δ_{T_μ^k x}` converge weak-* to **Haar measure** on `ℤ_p`.
>
> **Corollary (the BB(6) target).** Every nonzero **integer** seed is automatically non-periodic and
> non-singular (an integer orbit stays integral, so it can never equal the rational `s_μ`), hence equidistributes
> — in particular Antihydra's seed `8`. So **A1 ⇒ Antihydra non-halts**, and likewise for the whole
> `v_p(μ)=−1` family (`CRYPTID_KERNEL.md`).

## Why exactly hypotheses (i),(ii) — the counterexamples that forced them (verified)
The hunt found the obstructions to equidistribution, and they are **exactly** two dense rational families:
- **(i) Eventually-periodic seeds — must be excluded.** The fixed points `x_D=(p^D… )` realize **every** value
  of `avg jump = D` (`D=0,1,2,3,…`): e.g. for `μ=3/2`, `x_1=1/5` (period-1, `avg jump=1`), `x_2=5/19`
  (`avg jump=2`), `x_3=19/65` (`avg jump=3`), … and period-2 cycles `2/19, 3/19` (`D=0,1,0,1,…`, `avg jump=½`).
  Periodic points are **dense** in `ℤ_p` (full-branch map), all rational, none equidistribute.
- **(ii) Singularity preimages — must be excluded.** Rational seeds whose orbit hits `s_μ=1/3` (where
  `3x−1=0`) terminate; this is the "halting" analogue. A dense rational tree.
- **No third obstruction found.** Over a sweep of rationals `a/b` (`a≤15`, `b≤33` odd): **181 → Haar
  (aperiodic), 10 biased-but-periodic, 4 singularity, and 0 aperiodic-non-singular counterexamples.** Integer
  seeds (`8, 12345, 7^13, 10^18+7, …`): all `→ Haar` (`avg jump≈1`, `P(D=0)≈0.5`). Integer seeds that *shadow*
  a periodic point (`≡ 1/5 mod 2^m`) **recover** to Haar once the finite shadow is exhausted (transient).
**So the conjecture survives the hunt: the only seeds that fail are eventually-periodic or singularity-preimages,
both excluded by (i),(ii), and both impossible for integer seeds.**

## The Diophantine condition — status (honest)
`log_p a` (e.g. `log_2 3`) is a fixed transcendental for each `μ`; the hunt cannot vary it, so it does **not**
test whether the condition is *necessary*. The condition is kept as the expected **proof tool** (a single-orbit
equidistribution proof would use that `log_p a` is not too-well approximable — the same input that makes
`{(3/2)^n}` equidistribute heuristically), not as a counterexample-excluder. For `μ=3/2`, `log_2 3` is known
non-Liouville (finite irrationality measure), so the hypothesis holds for Antihydra. **Open:** is it removable,
or genuinely needed? (No rational `μ` is available to violate it, so this is a structural, not empirical, question.)

## The non-Haar factors, catalogued (the answer to "what biases an orbit")
1. **Periodicity** — orbit trapped on a finite cycle (the fixed points + cycles; `avg jump =` the cycle mean).
2. **Singularity capture** — orbit reaches `s_μ` (terminates).
3. **Transient shadowing** — an orbit can *approach* a periodic point and be biased on a finite window, but for
   non-periodic seeds this is transient and washes out (verified for the `1/5`-shadowers).
4. **(adversarial) non-Haar-Bernoulli-generic points** — irrational `ℤ_p` points generic for a non-Haar
   measure (our §A2/Q9b constructions). These are **never rational/integer** (a ν-generic point for `ν≠`Haar is
   "random"), so restricting the seed to ℚ∩ℤ_p or ℤ excludes them — consistent with the hunt finding none.
This catalogue is the content: *the only obstructions are arithmetic-special seeds (periodic / singular), and
integer seeds avoid all of them.*

## Lemma 1 — Shadows are transient; periodic points are 2-adically repelling [PROVEN]
*Firms up hypothesis (i): the exclusion "not eventually periodic" is **tight** — there is no asymptotically-
periodic-but-aperiodic orbit. (`shadow_transient.py`; the period-1 case is verified sharp.)*

**Setup.** `F` is full-branch piecewise-affine on `ℤ_2`; on the branch `{v2(3x−1)=D}` it is affine with 2-adic
slope `(3/2)^{D+1}`, so `|F(x)−F(y)|_2 = 2^{D+1}|x−y|_2` for `x,y` on the same branch (**expansion** by `≥ 2`).

> **Lemma 1.** Let `p` be a fixed point of `F` on branch `D` (e.g. `p=5/19`, `D=2`). For any seed `x` with
> `v2(x−p)=m ≥ D+1`,
> ` v2(F^t(x) − p) = m − t(D+1) ` strictly decreasing, so the orbit **leaves `p`'s branch within
> `t* ≤ m/(D+1) ≤ m` steps**. Hence every shadowing episode of `p` has length `≤ m` = the depth of approach,
> and **no orbit converges to (is permanently trapped near) `p` unless it is eventually equal to `p`.**

**Proof.** While `x_t:=F^t(x)` is on `p`'s branch, `v2(3x_t−1)=D`, so `F(x_t)−p = F(x_t)−F(p) =
(3/2)^{D+1}(x_t−p)`, giving `v2(x_{t+1}−p) = v2(x_t−p) − (D+1)`. Inducting from `v2(x_0−p)=m`, the orbit stays
on `p`'s branch while `v2(x_t−p) ≥ D+1` (i.e. `x_t ≡ p mod 2^{D+1}`); since `v2` drops by `D+1 ≥ 1` each step,
this fails after `≤ m/(D+1)` steps, at which point `x_t`,`p` lie on different branches and decouple. ∎
*(Verified sharp: integer seeds `≡ 5/19 mod 2^m` shadow for exactly `m/3` steps — `10,16,23,30` for
`m=30,50,70,90` — with `v2(x_t−p)` decrementing by exactly `D+1=3` per step.)*

**General period-`τ` cycle.** Apply the same to `F^τ`, affine near `p` with multiplier `σ = ∏_{i<τ}(3/2)^{D_i+1}`,
`|σ|_2 = 2^{Σ(D_i+1)} > 1`; a shadow entered at depth `m` lasts `≤ τm/Σ(D_i+1) ≤ τm` steps.

**Corollary (hypothesis (i) is tight).** The only orbits asymptotic to a periodic cycle are the eventually-
periodic ones. So Conjecture A1's exclusion of eventually-periodic seeds removes **exactly** the permanently-
trapped seeds — there is no grey zone.

**Scope (honest).** Lemma 1 bounds each *single* episode by its approach depth and kills the "trapped forever"
failure mode. It does **not** bound the *total* shadow time `Σ(episode lengths)` over infinitely many re-
approaches — that needs control of how often the orbit re-approaches periodic points, which is itself
equidistribution-flavored (the remaining gap, Q-b/Q-e). What is rigorously gained: a fixed non-periodic seed's
first shadow contributes only **finitely many** biased steps; permanent trapping is **impossible**.

## Lemma 2 — the singularity-preimage class (ii), characterized [PROVEN]
> **Lemma 2.** The singularity-preimage set `S = ⋃_{d≥0} F^{−d}({1/3})` consists of **rationals with
> denominators that are powers of 3**; it is countable, dense in `ℤ_2`, **Haar-measure-zero**, and contains
> **no integer**. Hence hypothesis (ii) excludes a measure-zero rational set, **automatic for every integer seed**.

**Proof.** `F(y)=1/3` on branch `D` solves to `y_D=(2^{D+1}/3+3^D−2^D)/3^{D+1}` (verified: `F(y_D)=1/3`, on branch
`D`, `∈ℤ_2`): `2/9, 7/27, 23/81, 73/243,…` — denominators `3^{D+1}`, never integer. `S` = countable union of
finite preimage-sets ⇒ countable, dense (full-branch), Haar-null. An integer orbit stays integral and `1/3∉ℤ`,
so no integer reaches the singularity. ∎

**Corollary (hypotheses complete).** Lemmas 1–2: both excluded classes — (i) eventually-periodic and (ii)
singularity-preimages — are **measure-zero rational sets disjoint from `ℤ`** (bar trivial fixed points). So
**every integer seed satisfies (i),(ii) for free**; the corollary `A1 ⇒ Antihydra` needs no extra hypothesis.

## Proposition 3 — a 2↔3 duality of the jump [PROVEN, new]
> **Proposition 3.** For every `j`, ` D_j := v2(3c'_j − 1) = v3(2c'_{j+1} − 1) ` (verified `49999/49999`).

**Proof.** The renewal recurrence gives `2c'_{j+1}−1 = 3^{D_j} u_j`, `u_j=(3c'_j−1)/2^{D_j}`. `u_j` is a unit at
both 2 and 3: `v2(u_j)=0` (def of `D_j`) and `v3(u_j)=v3(3c'_j−1)=0` since `3c'_j−1≡−1 (mod 3)`. Hence
`v3(2c'_{j+1}−1)=v3(3^{D_j})+v3(u_j)=D_j`. ∎

**Consequences (a new 3-adic attack surface).**
- **3-adic avatar:** `avg jump = (1/J)Σ_j v3(2c'_{j+1}−1)`, so non-halt `⟺` the 3-adic valuations
  `v3(2c'_{j+1}−1)` average `≤ 2` — the whole even-density problem read 3-adically.
- **2↔3 / 1/3↔1/2 symmetry:** `avg jump` = avg 2-adic proximity of `c'_j` to `1/3` = avg 3-adic proximity of
  `c'_{j+1}` to `1/2`.
- **Locked expansions:** `2c'_{j+1}−1 = 3^{D_j}·(2,3-unit)` ⇒ the orbit is `3`-power-rich; consecutive states'
  2-adic and 3-adic expansions are **locked**. This **links the 2-adic Antihydra problem to the 3-adic `(p=3)`
  cryptid family** (o18/o15, `μ=8/3`, kernel = 3-adic equidistribution): the two cryptid primes meet on one orbit.
- **Honest status:** the two sides are *equal* — a new structural symmetry, not yet a proof tool — but it opens a
  3-adic surface absent before (next probe: does a tool on the 3-adic side, e.g. the Erdős/ternary machinery of
  the `8/3` family, bound `v3(2c'_{j+1}−1)` where the 2-adic side resisted?).

## Proposition 4 — the dual carry identity & the Erdős connection [PROVEN, new]
> **Proposition 4.** With `b_j = 2c'_j − 1` and `M_j = Σ_{i<j}(D_i+1)` (the step-index of the `j`-th renewal),
> ` 2^{M_J} b_J = 3^{M_J} b_0 + T_J ,  T_J = Σ_{j<J} 2^{M_j} 3^{M_J−1−M_j} ` (verified `199/199`). This is the
> **exact 3-adic dual** of the 2-adic identity `2^n c_n = 8·3^n − S_n`, `S_n = Σ_{j<n,e_j=1} 2^j 3^{n−1−j}`.
> Moreover `v3(b_J) = v3(T_J) = D_{J−1}` (verified): the orbit's **3-adic depth is governed by the carry `T_J`**.

**Proof.** The recurrence `2^{D_j+1} b_{j+1} = 3^{D_j+1} b_j + 3^{D_j}` (from `F`) telescopes against
`2^{M_j}/3^{M_j}`: setting `W_j = 2^{M_j}b_j/3^{M_j}`, `W_{j+1}−W_j = 2^{M_j}/3^{M_j+1}`, so
`W_J = b_0 + Σ_{j<J}2^{M_j}/3^{M_j+1}`; clearing denominators gives the identity. `v3(2^{M_J}b_J)=v3(b_J)` and
`v3(3^{M_J}b_0)=M_J` huge, so `v3(b_J)=v3(T_J)`; the lowest term (`j=J−1`) has 3-exponent `M_J−1−M_{J−1}=D_{J−1}`,
matching Prop 3. ∎

**The Erdős connection (the new toolset).** `S_n` (2-adic) is `Σ 2^j 3^{n−1−j}` over *odd* steps; `T_J` (3-adic)
is `Σ 2^{M_j} 3^{M_J−1−M_j}` over *renewal* (even) steps — a perfect `2↔3` dual. `v3(T_J) ≤ 2` on average
(= non-halt) is a statement about **sums of `2^{M_j} 3^{·} mod 3^k`**, i.e. about **powers of 2 mod 3^k** — the
**Erdős ternary-digit regime** (the kernel of the `8/3`/o18 family). Since `2` has order `2·3^{k−1}` mod `3^k`,
`2^{M_j} mod 3^k` depends on `M_j mod 2·3^{k−1}` = the **renewal times mod a 3-power** — a *different* object from
the 2-adic `⌊(3/2)^n⌋ mod 2` (where van der Corput is closed). **This is a genuinely new attack surface**: the
3-adic depth is controlled by powers-of-2-mod-3^k / renewal-times-mod-3^k, where sum-product / digit-distribution
tools live, rather than the 2-adic moving diagonal. *(Honest: still the same number; but a different toolset now
applies — actively probing whether it bounds where the 2-adic side resisted.)*

## Open sub-questions (the next counterexample searches / proof targets)
- **Q-a [PARTIALLY PROVEN — Lemma 1]** the *permanent-trapping* failure mode is now ruled out rigorously
  (no orbit is asymptotically periodic unless eventually periodic; each shadow episode `≤` its approach depth).
  *Remaining:* bound the *total* shadow time over re-approaches (= Q-b/Q-e, equidistribution-flavored).
- **Q-b [settled empirically; the *total* is CIRCULAR — feasibility-checked]** integer seed biased? — none
  (all → Haar; shadowers recover). The remaining "total shadow time = o(n)" is **not a non-circular target**:
  it equals `Σ_j v2(c'_j − 1/3) = avg jump·J` (the singularity's total weighted shadow), and the frequency of
  depth-`≥k` approach to any periodic point `p` is exactly the visit count to `p`'s `2^{−k}` cylinder = the
  equidistribution quantity (verified). So *proving* Q-b for an integer seed = proving equidistribution = the
  wall. **Lemma 1 (each single episode finite) was the maximal non-circular extract; the total is Q-e.**
- **Q-c [open, structural]** what is the exact Diophantine condition, and is it removable?
- **Q-d [settled in catalogue]** non-Haar factors beyond periodic shadowing? — singularity capture and
  non-Haar-Bernoulli-generic irrationals; both excluded for integer/rational-non-periodic seeds.
- **Q-e [the proof, = the hard core]** *prove* the conjecture for one integer seed — this is the rank-1
  single-orbit effective-equidistribution tool itself (the multi-year object; the wall named in `MEETING_BRIEF`).

## Status
A **conjecture shaped by counterexample**, with hypotheses (i),(ii) forced by dense rational counterexamples and
no surviving aperiodic-non-singular counterexample. It is the correct *target* statement for the new programme;
proving it (Q-e) is the new mathematics. Not a theorem — labelled as a conjecture throughout. 0 false proofs.
