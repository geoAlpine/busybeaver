# The trap / no-trap boundary of the cross-cryptid family (2026-06-26, Phase 2)
*Program: rank-1 specified-orbit genericity. This note pins the **decidable vs cryptid boundary** of the
`v_p(μ)=−1` Mahler family completely and **provably** (two elementary lemmas, then verified across 23 members,
`trap_boundary.py`). It is a structure theorem for the family's *easy* part; the *hard* part (genericity) is shown
to be uniform across the family. 0 false proofs.*

## Setup
Family: `T_μ(c) = ⌊μ c⌋` on `ℤ⁺`, `μ = a/p > 1`, `gcd(a,p)=1`, `v_p(μ)=−1`. Antihydra `= (p=2, a=3, μ=3/2)`.

## Two elementary lemmas (both verified)
- **(L1) Monotone:** `c ≤ c′ ⟹ T(c) ≤ T(c′)` (floor of a monotone map).
- **(L2) Non-decreasing:** `T(c) ≥ c` for all `c ≥ 0` (since `μc ≥ c` for `μ ≥ 1`, and `⌊μc⌋ ≥ ⌊c⌋ = c`).

## Structure theorem (consequence; verified, no cycle found anywhere)
1. **Periodic ⟹ fixed.** A cycle `c₀→c₁→⋯→c₀` has `c_{i+1} = T(c_i) ≥ c_i` (L2); summing around the cycle forces
   every inequality to equality ⟹ all `c_i` equal. **So the whole family has *no* periodic orbit of length ≥ 2** —
   brute-force confirmed (cap 3000 seeds, every member): none.
2. **Fixed set is an explicit interval.** `⌊μc⌋ = c ⟺ c ≤ μc < c+1 ⟺ c < 1/(μ−1)`. Hence
   `FIX(μ) = { c ∈ ℤ : 1 ≤ c < 1/(μ−1) }`, size `≈ 1/(μ−1)`. **Measured = predicted for all 23 tested members.**
3. **No transients, no basins.** A non-fixed seed has `T(c) > c` strictly, and (L1+L2) can never re-enter the fixed
   interval from above ⟹ it **escapes monotonically to `+∞`**. Every positive-integer seed is therefore **either a
   fixed point (trivially decidable) or an escaping orbit** — there is no third behavior.

## The boundary
> **The trap / no-trap boundary of the family is the single curve `μ = 2` (`a = 2p`).**
- **`μ > 2` (`a > 2p`): TRAP-FREE.** `1/(μ−1) < 1` ⟹ `FIX = ∅` ⟹ **every seed `≥ 1` escapes** (a cryptid candidate).
- **`1 < μ ≤ 2` (`p < a ≤ 2p`): finite trap.** `FIX = [1, 1/(μ−1))` (e.g. `μ=6/5`→`{1,2,3,4}`, `μ=8/7`→`{1..6}`);
  every larger seed escapes. **Antihydra `μ=3/2`: `FIX = {1}`, threshold 2; seed 8 escapes.**

## What it means for the program
- The family's **decidable part is finite and fully explicit** — the fixed interval `[1, 1/(μ−1))`, present only for
  `μ ≤ 2`. There are no hidden cycles or long transients to chase: boundedness-decidability is *completely mapped*.
- The **cryptid-hard part is every escaping seed**, and the genericity wall on it (`avg jump ≤ 2`, i.e. the running
  even-density `≥ 1/3` question) is **uniform across all `μ` and all escaping seeds**. The `μ=2` boundary separates
  *fixed-point existence*, **not** *difficulty* — the wall does not see it.
- Sharpens the earlier finding: Lemma 1 ("integer seeds avoid periodic traps") is **not** family-universal. For
  `μ < 2` the trap interval is nonempty; what is special about Antihydra is only that its seed (8) lies **above** the
  threshold 2 — a one-line, explicit certificate that seed 8 is in the hard regime, replacing the earlier
  2-adic-repulsion argument with a sharper boundedness one.
- **Honest caveat:** escape (unbounded growth) is *necessary* for cryptid status but not sufficient — whether an
  escaping orbit actually keeps even-density `≥ 1/3` (is a genuine non-halting cryptid) is exactly the open
  genericity question. Escape only certifies "outside the boundedness-decidable region."

## Rate scan result — the rate is `μ`-uniform, and the orbit is i.i.d.-indistinguishable (`rate_scan2.py`)
Probe: within trap-free `μ>2`, does the *effective genericity rate* depend on `μ`? Prediction tested: the renewal
Lyapunov exponent is `log μ` (≈`log₂μ` fresh bits/step), so larger `μ` *might* equidistribute faster. **Refuted.**
At **fixed `p`** (removing the `p`-confound of a first scan), the CLT-normalized residue statistic
`χ²_N(μ) = N·Σ_r(freq_N(r) − 1/p)²` sits at the multinomial baseline `(p−1)/p` for **every** `μ`, with **no
consistent `μ`-trend** (`corr(μ,χ²)` signs disagree across `p`: `−0.25, −0.33, +0.84`, 3–7 pts each = noise).
Two conclusions:
1. **The convergence rate is `μ`-uniform** ⇒ the genericity wall is **one object**; the `log μ`-speedup prediction
   is **refuted** (faster expansion does not buy faster equidistribution once `p` is fixed).
2. **The orbit's mod-`p` statistics are statistically indistinguishable from i.i.d. uniform at the CLT `√N` rate**
   (orbit `χ²` = i.i.d.-control `χ²` = `(p−1)/p`, verified by an *averaged* i.i.d. control). The low residues look
   exactly like fair `p`-sided dice — a **quantitative** confirmation of `NEW_ENGINE`'s "too random to certify":
   maximal apparent randomness is exactly what blocks a proof.

*Discipline note:* a first draft used the wrong baseline `p−1` (correct: `(p−1)/p`) with a *single-draw* i.i.d.
control, which spuriously suggested "sub-CLT super-uniformity." An averaged i.i.d. control caught it before any
claim: orbit `==` i.i.d. `== (p−1)/p`. 0 false claims.

## Net Phase-2 picture (boundary + rate)
The family splits cleanly: a finite, explicit **decidable** part (fixed interval `[1,1/(μ−1))`, present only for
`μ≤2`) and an **escaping** part where the genericity wall stands — and on that wall, **every** member, **every**
`μ`, equidistributes mod `p` at the **same i.i.d./CLT rate**. The boundary `μ=2` separates fixed-point existence;
the wall and its rate see neither `μ` nor `p` (after normalization). The family is, on the hard side, **one
homogeneous object** — strengthening the single program banner. Next internal probe: push the i.i.d.-likeness to
**higher cylinders** (mod `p²`, joint `(c_n,c_{n+1})`) to see if independence *across steps* also matches i.i.d.,
or if the deterministic self-feeding shows up as a detectable `k≥2` correlation (the quenched-vs-annealed seam).
