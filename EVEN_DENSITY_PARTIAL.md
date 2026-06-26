# Attacking even-density ≥ ε via one-sided shrinking-target — a genuine unconditional partial + the wall (2026-06-26)
*The realistic short-term partial (expert option E, direction corrected). Result: a small but genuine
**unconditional** rate `#even(n) ≥ c·log n`; positive *density* (`even-density ≥ ε`) is out of reach of the growth
argument (it is marginally consistent with `even-density → 0`) and funnels to a shrinking-target / Borel–Cantelli
wall — true heuristically, unprovable unconditionally for the specified seed. `H_lowmoduli.py`/inline-verified.*

## The reduction [PROVEN]
`even-density ≥ ε ⟺ N_3/O ≥ ε` (a positive fraction of odd values are `≡3 mod 4`, i.e. `D=v2(3c−1)≥2`), equivalently
`avgD_odd ≥ 1+ε`. Also `even-density ≥ 1/(1+avgL)` exactly (verified), where `avgL` = average odd-run length;
`even-density → 0 ⟺ avgL → ∞ ⟺ o(n) runs covering ~n odd steps`.

## The genuine unconditional partial [PROVEN]: `#even(n) ≥ c·log n`
The orbit grows `c_p ~ A(3/2)^p`, so `bit-length(c_p) = 0.585 p + O(1)`. Two consequences (both from `v2 ≤
bit-length`):
- an **odd-run** of length `L_j` starting at position `p_j` needs `c_{p_j} ≡ 1 mod 2^{L_j}`, so `L_j ≤ 0.585 p_j + O(1)`;
- an **even-run** of length `M_j` from `c` even needs `M_j = v2(c) ≤ 0.585 p_j + O(1)`.
Hence one full cycle (odd-run + even-run) advances the position by `L_j + M_j ≤ 1.17 p_j + O(1)`, so
`p_{j+1} ≤ 2.17 p_j + O(1)`. To reach position `n` therefore takes
> `#cycles ≥ log_{2.17}(n) − O(1) ≈ 0.89·log₂ n`,  and `#even(n) ≥ #cycles ≥ c·log n` (`c≈0.89`), **unconditional.**
This upgrades the trivial floor ("infinitely many even steps", from "the only all-odd orbit is the fixed point 1")
to an explicit **rate**. (Tiny — the truth is `#even ~ n/2` — but it is a genuine unconditional statement about the
*specified* orbit, of the kind the literature says is otherwise only an FLP-type *range* bound.)

## Why positive *density* is out of reach of growth [rigorous negative]
The natural hope — that the growth constraint `L_j ≤ 0.585 p_j` forbids `even-density → 0` — **fails, marginally.**
The maximal geometric scenario `L_j = 0.585 p_j` with minimal even-runs gives `p_{j+1} = 1.585 p_j`, so
`O(log n)` runs of geometrically-growing length, and `Σ L_j → n` exactly **at the boundary** (computed: `n=10⁹` ⇒
43 runs, `Σ L_j = 0.99999n`, `even-density → 0`). So `even-density → 0` is **consistent** with the growth
constraint; growth alone cannot prove positive density.

## The wall (where it funnels) — Borel–Cantelli: true but unprovable for the specified seed
`even-density → 0` requires the orbit to hit the **shrinking targets** `{c_p ≡ 1 mod 2^{≈0.585 p}}` (near-maximal
runs) at a positive density of scales. The Borel–Cantelli sum converges: `Σ_p 2^{−0.585 p} = 2.0 < ∞`, so a
*generic* orbit hits near-maximal runs only **finitely often** ⟹ `even-density ↛ 0` (in fact `→ 1/2`). The actual
seed-8 orbit confirms this empirically — max run length `20` at `N=3·10⁵` (vs the maximal `≈175500`, ratio
`10^{−4}`), mean run length `2.001` — runs are `O(log n)`, **nowhere near maximal.** But converting the
Borel–Cantelli heuristic into an unconditional statement for the **specified** seed is exactly the
shrinking-target / single-orbit-equidistruction wall (no current tool; positive density for a specified orbit is
open per the literature, beyond FLP's range bound).

## Verdict
- **Achieved (unconditional, new):** `#even(n) ≥ c·log n` — a rate, beating "infinitely many", from the growth
  constraint alone. This is a genuine first-of-its-kind quantitative fact about the specified orbit, modest but
  honest.
- **Out of reach (rigorously, via growth):** `even-density ≥ ε` — the maximal geometric scenario marginally
  realizes `even-density → 0`, so growth cannot prove positive density; it funnels to a one-sided shrinking-target
  bound = Borel–Cantelli-true / unconditionally-open. The factor between what growth gives (`log n`) and what we
  want (`εn`) is the whole wall.
- **Honest next:** any unconditional `even-density ≥ ε` needs an effective shrinking-target / Borel–Cantelli input
  for the deterministic orbit — i.e. exactly the effective-`log₂3` / single-orbit genericity tool (the frontier).
  The cheap remaining lever is **(B-Theorem) push the top foothold one scale** — a bounded sub-goal independent of
  this wall.
