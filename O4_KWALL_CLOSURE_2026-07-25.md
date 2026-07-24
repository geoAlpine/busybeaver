# o4 (K) wall — the untried routes are now EXHAUSTED, each closed by a proven mechanism (2026-07-25)

This closes the loop opened by ATTACK_CATALOG §V. Starting from the #30 premise-refutation
(margin ≠ provability), the three genuinely-untried (K) routes (#16 almost-transport,
#17 FFY/Stewart, #21 cross-orbit) were fired in parallel and **all three returned verdict (c) —
rederives the wall** — each via a *clean, independently re-verified* mechanism. The (K) frontier
of the catalog is now empirically closed. **No machine decided. No label upgraded. x2 [OPEN].**

## The object (one line)
`T(G) = (4G + e(G mod 3))/3`, `e={0:9,1:14,2:1}`, seed 43; `ρ_n = G_n mod 3`;
`φ = freq{ρ_n=1}`. Target: `φ(43) < 4/5` (measured 0.3339). This is the o4-first (K) scalar.

## The unifying fact all three routes converge on [PROVEN, re-verified]
**T is a single expanding map of multiplier 4/3 plus a locally-constant additive cocycle.**
Every branch has the identical slope 4/3; only the additive term `e(ρ)/3` is branch-dependent.
There is exactly one expanding direction. Furstenberg/Rudolph/Host rigidity — the only machinery
that would *pin* a single orbit's digit frequency — requires TWO multiplicatively-independent
maps. So pinning φ(43) ⟺ manufacturing a second multiplicatively-independent structure on the
orbit. The three routes are the three places such a structure could come from, and each is dead:

| source of a 2nd structure | route | why it fails | banked [PROVEN] fact (re-verified 10^5 steps) |
|---|---|---|---|
| **the 2-adic side** (×2) | #17 | the available 2-adic data is a *subordinate factor* of the 3-shift, not independent | `parity(G_{n+1}) = [ρ_n=1]`; `v₂(G_n)∈{0,1}`, `v₂=1 ⟺ ρ_{n−1}=1`. No 2-adic weapon can bite. |
| **algebraic symmetry** | #21 | the affine-automorphism group is **trivial**; only Koenigs self-conjugacy exists (= the map re-coordinatized) | 0 nontrivial affine automorphisms of `e={9,14,1}`; Koenigs `A(43)=49.93454575181803`, `A∘T=(4/3)A`, frequency-inert |
| **a transport target** | #16 | the only exact transport is the base-3 digit skew-shift; its target is the *full shift* (no per-point frequency) | `T(G) = 4·(G//3) + s`, `s=(3,6,3)`; `ρ_{n+1}=(G_n//3) mod 3`. (K) = digit-1 normality of the ×(4/3) orbit of 43 |

The transverse 2-adic statistic (#17: base-2 digit sum `s₂(G_n)`) is empirically independent of
ρ (χ²→2.17 as N→6·10⁴) and would itself need a base-2 normality theorem for the (4/3)ⁿ-growth
sequence — a (K)-type problem in base 2. Every escape relocates (K), never removes it.

## The sharpest restatement of o4's (K) [banked, #16]
> **o4 (K) = "is the base-3 expansion of the ×(4/3)-orbit of 43 simply normal at digit position 1?"**

A single expanding multiplier ⟹ full multifractal spectrum (every Bernoulli(f,·,·) is
T-ergodic; `dim_H{φ=f}=H(f)/log3>0`) ⟹ φ genuinely unpinned off a dimension-0 set. `φ=1` is
realized at the fixed point −14. This is the exact sibling, in T's own coordinate, of Mahler 3/2 /
AEV. No single-map tool escapes it — now demonstrated, not merely asserted, by three independent
mechanisms.

## Consequence for the program
The FEASIBILITY verdict "unconditional BB(6) is not reachable by this program" is upgraded from
an impression to a **mechanical consequence**: the (K) wall's last untried internal routes are
closed by proven no-gos (trivial automorphism group; 2-adic factor subordination; skew-shift onto
the full shift), on top of the pre-existing single-map multifractal obstruction. What remains
that could ever touch (K) is genuinely-external mathematics (a new AEV/normality theorem), which
by owner policy the program does not pursue via outside contact and cannot manufacture internally.

**The only place green theorems are still available is x2** (finite formalization; one of 17
cryptids; does not touch (K)). See `REMAINING_2026-07-24.md` / `R1_ODDSEAM_2026-07-24.md`.

## Artifacts (repo-root, committed evidence — not gitignored scratchpad)
`route16_almost_transport.py`, `route16_entropy_memory.py`, `route16_induce_ld.py`,
`route17_ffy_stewart_numerics.py`, `route21_cross_orbit.py`. All facts re-verified independently
of the subagents (skew-shift, 2-adic factor identity, trivial automorphism, Koenigs constant).

No machine decided. No label upgraded.
