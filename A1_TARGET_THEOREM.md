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

## Open sub-questions (the next counterexample searches / proof targets)
- **Q-a [largely settled empirically]** rational seed not → Haar? — only if eventually-periodic or singular
  (verified, no other). *Sharpen:* prove that a non-periodic rational orbit cannot remain biased (the
  shadowing-is-transient lemma made rigorous).
- **Q-b [settled empirically]** integer seed biased? — none (all → Haar; shadowers recover). *Prove:* an integer
  orbit's empirical measure → Haar (the actual theorem).
- **Q-c [open, structural]** what is the exact Diophantine condition, and is it removable?
- **Q-d [settled in catalogue]** non-Haar factors beyond periodic shadowing? — singularity capture and
  non-Haar-Bernoulli-generic irrationals; both excluded for integer/rational-non-periodic seeds.
- **Q-e [the proof, = the hard core]** *prove* the conjecture for one integer seed — this is the rank-1
  single-orbit effective-equidistribution tool itself (the multi-year object; the wall named in `MEETING_BRIEF`).

## Status
A **conjecture shaped by counterexample**, with hypotheses (i),(ii) forced by dense rational counterexamples and
no surviving aperiodic-non-singular counterexample. It is the correct *target* statement for the new programme;
proving it (Q-e) is the new mathematics. Not a theorem — labelled as a conjecture throughout. 0 false proofs.
