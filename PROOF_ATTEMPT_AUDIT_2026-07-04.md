# Proof-attempt audit — we are NOT closer to a proof; the exact gap is unchanged (2026-07-04)

*An honest, rigorous test of the question "has the accumulated data brought us closer to a proof?" Method: **actually
attempt** the proof of Antihydra non-halting, locate the **exact remaining step**, and **audit every accumulated
result — including all of today's** — against it. Verdict: **NO.** The proof stalls at the identical `(K)` step (the
`0.585n → 0.5n` run-ceiling gap, factor `1.17×`), and **nothing accumulated closes it**; today's work (non-affine
unification, o10 = (K)+BC-II, thin/thick, the frontier-wide censuses, the spot-checks) is all **mapping, not
gap-closing**. SOUNDNESS: `[PROVEN]`/`[OBSERVED]` chain; the conclusion is a precise localization, not a proof.*

## The proof, set up honestly `[PROVEN chain to the gap]`
1. **Antihydra non-halt ⟺ `B_n = 3E_n − n ≥ 0` for all `n`** (`E_n=#even` steps of `c↦⌊3c/2⌋`, `c_0=8`) `[PROVEN,
   Kac / balance criterion]`.
2. `B_n` is a walk with increments `+2` (even step) / `−1` (odd step); drift `+½` iff even-density `→ ½`. Empirically
   `min_n B_n = 0` to `N=5·10⁵` (never negative — drift holds it up) `[OBSERVED]`.
3. **To prove `B_n ≥ 0` forever, exclude a late downward excursion.** A drop of size `s` needs an odd-run (deep
   2-adic visit) of length `s`; the **proven magnitude ceiling** is `run ≤ v₂(c_n−1) ≤ log₂ c_n ≈ 0.585 n`.
4. **The gap** `[PROVEN consistency, OCCUPANCY_PROFILE_THEORY §7 (W3), 2026-07-01]`: the accumulated balance is
   `≈ 0.5 n`, but the run-ceiling is `0.585 n`. Since `0.585 > 0.5`, a near-maximal late run **could** drop `B`
   below the accumulated `0.5 n` → negative. **So the elementary bounds are consistent with BOTH halt and non-halt**;
   the deficit is exactly `0.585/0.5 = 1.17×`.
5. **Closing it** requires the runs to be genuinely short (`o(0.5 n)` at positive density) = **depth-tail control =
   `(K)` = single-orbit equidistribution** — the generational wall.

## The audit — does any accumulated result close step 4→5? `[each PROVEN-negative]`
| accumulated result | closes the `0.585n → <0.5n` run-ceiling gap? |
|---|---|
| `#even ≥ 0.89 log n` (even-count floor) | **NO** — `log`, not linear; `EVEN_COUNT_FLOOR` proves it *sharp* |
| golden-ratio Cramér `θ*=log φ` | **NO** — an *annealed* exponent; quenched = `(K)` (No-Structure) |
| excursion / Kac supermartingale | **NO** — a heavy-tailed white adversary is drift-indistinguishable (`EXCURSION_SYNTHESIS`) |
| **o10 = (K)+BC-II** (today) | **NO** — o10 is *harder* than `(K)`; the mirror gives "o10 halts iff the orbit is generic", **no** bound on the run |
| **non-affine unification** (today) | **NO** — a structural *placement*; the run-ceiling is arithmetic, untouched |
| **thin/thick, o10-unique** (today) | **NO** — classifies the *target*; silent on the run-length tail |
| Stewart single-orbit effective | **NO** — bounds the *digit count* (`log`), not run-length; wrong object *and* `log` not linear |
| Fan–Fan–Ye a.e. UD | **NO** — a.e.; cannot certify the *specified* orbit (full-dim exceptional set) |

**Every accumulated result — including all of today's — fails to close the gap.**

## Honest reading
- **We are not closer to a proof.** The proof reaches the *same* `(K)` step it reached before this session; the
  remaining lemma ("late odd-runs are `o(0.5n)` at positive density") is unchanged, and no accumulated result crosses
  it.
- **What the data DID do — and its exact limit.** The accumulated work *localizes* the gap with total precision (the
  `1.17×` run-ceiling deficit; the golden-ratio annealed exponent; the seam identity; the P1′ spec) — we know
  *exactly* what is missing. **But localization ≠ closing:** the missing `1.17×` **is** `(K)`.
- **Today added zero proof progress on the gap.** The session's outputs (non-affine unification, o10 decomposition,
  thin/thick, censuses, spot-checks) are all *classificatory/structural* — none touches the run-length tail. The gap
  itself was already pinned on 2026-07-01 (`OCCUPANCY §7`); **today did not move it.**
- This is exactly what the No-Structure theorem predicts: a structure-only/mapping effort, however thorough, cannot
  close a gap that provably requires seed-specific arithmetic. The audit is a concrete confirmation, not a surprise.

## Honest verdict
**(c) — NOT closer to a proof; the gap is the unchanged `(K)`.** A rigorous proof attempt stalls at the identical
`0.585n → 0.5n` run-ceiling step (`= (K) =` quenched depth-tail `=` single-orbit equidistribution), and an audit of
every accumulated result — including all of today's — finds **none** that closes it. The data is maximally
*organized around* the gap; the gap itself is untouched. Actual proof progress needs the generational tool (`P1′`),
not more internal mapping. **Halting `[OPEN]`. No machine decided. No label upgraded.**

## Reproduce
- `scratchpad` (`/opt/homebrew/bin/python3.13`): Antihydra `B_n`, `min B_n = 0` to `5·10⁵`, `max v₂(c−1)=20`, the
  `0.585n` magnitude ceiling; the 8-result audit. Basis: `OCCUPANCY_PROFILE_THEORY.md §7` (the 1.17× gap),
  `EVEN_COUNT_FLOOR.md`, `EXCURSION_SYNTHESIS.md`, `BB6_NO_STRUCTURE_THEOREM.md`, and this session's
  `CRYPTID_NONAFFINE_UNIFICATION` / `O10_APEX` / `GRAND_SYNTHESIS`.
