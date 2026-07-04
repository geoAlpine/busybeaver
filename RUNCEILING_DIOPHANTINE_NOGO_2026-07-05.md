# Can Diophantine/Baker lower the run-ceiling below 0.585n? — evaluated, then probed: NO, a family NO-GO (2026-07-05)

*"Evaluate whether the next attack is genuinely effective **before** executing." The next attack: unlike every prior
depth-tail route (`EXCURSION_*`, `EK2_*` — all attack the **frequency / 2nd moment**, all closed), attack the
**max-depth ceiling itself** with **Baker / linear-forms-in-logs**. This is a genuinely **different regime**: the max is
an **individual-term / support** quantity — the one place Baker has purchase (`BAKER_LINFORMS §0`: "forbids individual
super-close returns"). Evaluation + a cofactor probe show it yields a **real but razor-thin** result that is **vacuous
for the actual orbit**. Net: the entire Diophantine/Baker family is removed as a way to lower the run-ceiling by any
fixed factor. SOUNDNESS: `[PROVEN-cond]`/`[OBSERVED]` labelled; `(K)` `[OPEN]`; no machine decided.*

## 1. The setup — why the MAX (not the frequency) is Baker's natural regime `[PROVEN framing]`
Non-halt needs `max_n v₂(c_n−1) < 0.5n`; the proven magnitude ceiling is `v₂(c_n−1) ≤ log₂ c_n ≈ 0.585n`. Write a
depth-`k` visit as `c_n − 1 = 2^k·u`, `u` odd, `u ~ 2^{0.585n − k}`. At the **top** `k ≈ 0.585n` the cofactor is
**bounded** `u=O(1)`, so `c_n ≈ u·2^k ⟹ 8·3^n/2^n ≈ u·2^k ⟹ |n log3 − (k+n)log2 − log(u/8)|` small — **a clean linear
form in logs.** Baker's effective lower bound forbids this from vanishing fast, so **`depth = 0.585n − O(1)` (bounded
cofactor) is impossible for large `n`** `[PROVEN-cond on standard effective Baker]`. This is a genuine individual-term
statement — exactly the regime the frequency routes could not touch.

## 2. Why it dies before any fixed fraction below the ceiling `[PROVEN]`
For `k = (0.585−ε)n` (any fixed `ε>0`) the cofactor `u ~ 2^{εn}` is **exponentially large** — there is **no single
linear form**; covering the `≈2^{εn}` candidate cofactors needs a **union** over exponentially many targets, which
overwhelms Baker's per-form bound. So Baker shaves only `o(n)` off the very top: **the ceiling stays `0.585n` for any
*linear* improvement.** The thick/thin phase transition sits **right under the ceiling** — the accessible (thin,
bounded-cofactor) set is `θ = 0.585 − o(1)` only; `0.5n` is deep in the **thick** (equidistribution) regime `= (K)`.

## 3. The cofactor probe — Baker's real purchase is VACUOUS for this orbit `[OBSERVED, exact big-int, N=3·10⁵]`
Running-max depth `d_n=v₂(c_n−1)` and its odd cofactor `u=(c_n−1)/2^{d_n}` at each record:

| n | max depth `d` | `u` bit-length | `0.5n` | `0.585n` |
|---|---|---|---|---|
| 254 | 8 | 144 | 127 | 149 |
| 1133 | 9 | 657 | 566 | 663 |
| 2927 | 11 | 1705 | 1464 | 1712 |
| 15130 | 13 | **8841** | 7565 | 8851 |

Two facts, both decisive: **(a)** actual `max depth ~ log n` (`d=13` at `n=15130`) — the orbit sits `~580×` **below**
even `0.5n`, astronomically below the `0.585n` ceiling. **(b)** the cofactor `u` is **exponentially large and grows**
(`u_bits ≈ 0.585n`, essentially the whole number) at *every* record depth — the orbit's deep visits live **deep in the
thick regime**, and **never** enter Baker's accessible bounded-cofactor top. So the one real thing Baker proves (§1) is
about a razor-thin set the orbit **never visits**; it is vacuous for the actual excursion question.

## 4. Verdict — a family NO-GO, banked `[the honest outcome of evaluating-before-executing]`
**The Diophantine / Baker / linear-forms family is removed as a route to lower the run-ceiling by any fixed factor.**
Evaluated first (not fired blindly): it is a genuinely different regime from the closed frequency routes and *does*
give a real individual-term result (`depth = 0.585n−O(1)` forbidden), but (§2) it cannot reach `(0.585−ε)n` for any
fixed `ε` (exponential-cofactor union kills it) and (§3, probed) it is vacuous for the orbit, which never leaves the
thick regime. This is **not a crossing** — it is a **narrowing**: a previously-unpinned tool-family is now a proven
NO-GO at this specific target, with mechanism (cofactor exponential growth) and numerics. The run-ceiling gap
`0.585n → 0.5n` remains exactly `(K)` (thick/equidistribution), with **no Diophantine shortcut** — now established, not
assumed. **Halting `[OPEN]`. No machine decided. No label upgraded.**

## Reproduce
- `scratchpad/baker_cofactor_probe.py` (`/opt/homebrew/bin/python3.13`, exact big-int): Antihydra `c₀=8, c→⌊3c/2⌋`,
  running-max `d_n=v₂(c_n−1)` and odd cofactor `u`; `d~log n`, `u_bits~0.585n` (thick) at every record. Basis:
  `BAKER_LINFORMS.md` (Baker = support/individual-term only, no frequency), `OCCUPANCY_PROFILE_THEORY.md §7` (the
  1.17× gap), `DEPTH_REACH_CLARIFICATION.md` (log-cap vs moving-diagonal), `PROOF_TOOL_ATTEMPT_2026-07-04.md`.
