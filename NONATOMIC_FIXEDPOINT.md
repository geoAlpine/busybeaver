# No atom at the fixed point o=1 — the bottom rung, reduced to a first-vs-second-moment gap (2026-06-29)

*Attack on the bottom rung of the ENT ladder `{orbit avoids periodic}[PROVEN] ⊊ {μ non-atomic}[OPEN] ⊊ ENT ⊊ (K)`:
does the orbit limit measure `μ` have an atom at the fixed point `o=1`? Consolidated by the main loop after the three
sub-agents died on API connection errors mid-run (their numeric scripts survived; the decisive computation was re-run here:
`scratchpad/nonatomic_decide.py`, exact big-int, N up to 2·10⁵). SOUNDNESS: every claim labelled; the reduction is verified;
the verdict is honest (no free partial). NOT committed by default.*

---

## 0. One-line verdict

`μ({1})=0` (no atom at the fixed point) is **[OPEN], not a free unconditional partial**, BUT it now has a clean **[PROVEN]
reduction** to a single sharp statement: **the second moment of the jump-depths is finite** (equivalently mean 2-adic depth
bounded, equivalently the residue-1 occupancy `f_k` is summable). The proven valuation budget controls the **first** moment
of jump-depths but not the **second**; that first-vs-second-moment gap is the exact, (K)-adjacent obstruction. Numerics
strongly support `μ({1})=0` (mean depth ≈ 0.99, `f_k ≈ 2^{-k}`, max depth ≈ log₂N) but do not prove it.

---

## 1. The reduction [PROVEN, verified]

Let `d_n := v₂(c_n − 1)` (the 2-adic depth; `=0` when `c_n` is even). An `A`-invariant measure's atoms sit on periodic
orbits, and `μ({1}) = inf_k f_k` where
> `f_k := limsup_N (1/N) #{ n<N : c_n ≡ 1 (mod 2^k) } = limsup_N (1/N)#{n: d_n ≥ k}`  (occupancy of residue 1 mod 2^k).

`f_k` is non-increasing in `k`, so `μ({1}) = lim_k f_k`. Hence **`μ({1}) = 0 ⟺ f_k → 0`.**

**Countdown structure [PROVEN, verified 0 exceptions].** For odd `c_n` with `d_n=k≥1`: write `c_n−1=2^k u` (`u` odd);
then `c_{n+1}=(3c_n−1)/2` has `c_{n+1}−1 = 3·2^{k−1}u`, so `d_{n+1}=k−1`. The depth decrements by exactly 1 each step until
`d=1`, whose successor is **even** (`d=0`). So the orbit visits residue 1 mod 2^k only in **contiguous countdown runs**:
an excursion that jumps to entry-depth `K` occupies depths `K, K−1, …, 1` (one step each), then an even step.

**Mean-depth identity [PROVEN].** Summing the countdown, an excursion of entry-depth `K` contributes `Σ_{j=1}^{K} 1` to
`#{d≥1}` and exactly **one** step to each level `{d≥j}, j≤K`. Therefore, with `K_i` the entry-depths,
> `(1/N) Σ_{n<N} d_n = Σ_{k≥1} f_k^{(N)} = E[K(K+1)/2] / E[K+1]`  (renewal–reward; `K`=jump/entry-depth).

So **mean depth = Σ_k f_k**, and:
> **Sufficient condition [PROVEN implication]:** mean depth bounded `⟺ Σ_k f_k < ∞ ⟹ f_k → 0 ⟹ μ({1}) = 0.`
And by renewal–reward, **mean depth bounded `⟺ E[K²] < ∞`** (second moment of jump-depths finite).

---

## 2. Where the proof stops — the first-vs-second-moment gap [the exact obstruction]

- **First moment of `K` is controlled [PROVEN].** The valuation budget `Σ_{odd i<n} v₂(3c_i−1) = n + v₂(c_n) − v₂(c_0)`
  (`VALUATION_BUDGET.md`) and the renewal identity give `E[K] = ` mean gap `= total steps / #renewals ≈ 2` — a first-moment
  tautology.
- **Second moment `E[K²]` is NOT controlled [OPEN].** `μ({1})=0` needs `E[K²]<∞` (mean depth bounded), a statement about
  the **tail** of the jump-depth distribution `P(K≥k)`. The proven first-moment budget says nothing about it. The
  per-visit dual-repulsion (`REPELLER_ESCAPE.md`) proves the orbit *escapes* each deep cylinder (countdown), giving
  per-visit length control — but **not** the visit *frequency* `f_k`, which is exactly the occupancy/tail. The crude proven
  bound `K_i ≤ 0.585n` permits (without contradiction) a heavy tail / a single run of length `≈0.585N`, which would give
  `E[K²]=∞` and an atom `μ({1})≥0.585`. So the gap is precisely **first-moment (proven) vs second-moment (open)** of the
  jump-depths; the second moment is single-orbit jump-tail control = (K)-adjacent.

This is strictly weaker than (K) (which fixes `f_k = 2^{−k}` for *every* residue, not just residue 1, exactly) but is not
reachable from the proven first-moment structure.

---

## 3. Numerics [OBSERVED, decisive support, `nonatomic_decide.py`, exact big-int]

| N | mean depth `Σd_n/N` | max depth `M(N)` | `M(N)/log₂N` |
|---|---|---|---|
| 2·10⁴ | 1.0037 | 13 | 0.91 |
| 5·10⁴ | 0.9952 | 14 | 0.90 |
| 10⁵ | 0.9897 | 20 | 1.20 |
| 2·10⁵ | 0.9940 | 20 | 1.14 |

Mean depth is **stable ≈ 0.99 (bounded)**; max depth `M(N) ≈ log₂N` (logarithmic). Occupancy `f_k` (N=2·10⁵):
`f_1..f_{10} = 0.500, 0.250, 0.124, 0.061, 0.030, 0.0146, 0.0071, 0.0035, 0.0018, 0.0009` — **geometric `≈2^{−k} → 0`**,
ratio `f_k/f_{k−1} ≈ 0.49`. All consistent with `E[K²]<∞`, mean depth bounded, and `μ({1})=0`. **Evidence, not proof** —
the same equidistribution-flavoured data that finite N can never upgrade.

---

## 4. The other two rungs (sub-agents died; status from this analysis)

- **Max-depth `M(N)` (intended `MAX_DEPTH_BOUND.md`).** Clarification: `M(N)=o(N)` is **not** what controls the atom — the
  atom mass is `inf_k f_k` (fixed-`k` occupancy tail), and `M(N)` (max over `n` at fixed `N`) does not bound `f_k`. The
  relevant quantity is the jump-depth second moment, not the max. (`M(N)≈log₂N` observed, but it is a side fact here.)
- **Global non-atomicity (intended `NONATOMIC_GLOBAL.md`).** Periodic points are the countably many rationals
  `p/(3^q−2^q)` (`WALLB_NONATOMIC.md`); `μ` non-atomic ⟺ every one has zero mass ⟺ the analogous occupancy `f_k^{(q)}→0`
  for each period `q`. The fixed point `o=1` (`q=1`) is the analysed case; higher `q` need the same per-residue occupancy
  decay, uniformly in `q` — no uniform proven bound exists, so global non-atomicity is at least as hard as the `o=1` case
  and shares the second-moment gap.

---

## 5. Net

The bottom rung sharpens but does not fall: **`μ({1})=0` ⟺ `f_k→0` ⟸ mean depth bounded ⟺ `E[K²]<∞`**, with the **first
moment proven and the second moment open** — a clean, quotable characterization of why even the weakest non-atomicity
precursor resists. Confirms `ENT_NONATOMIC.md` (open, with the giant-run obstruction) and pins the obstruction to the
jump-depth second moment. **No machine decided. No label upgraded.** (K) remains [OPEN].
