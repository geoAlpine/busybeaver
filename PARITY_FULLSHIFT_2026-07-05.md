# The Antihydra parity / base-3/2 digit word is a FULL 2-shift — no de Bruijn/complexity foothold (2026-07-05)

*Continuation probe: measure the subword complexity / de Bruijn structure of the Antihydra parity word (= the `(K)`
base-3/2 digit word, `DICT_AND_EXCDIM_2026-07-05.md`) — a literature-tied angle (arXiv:1811.02254 "De Bruijn graphs and
powers of 3/2") never run on this exact object. Result: **maximal complexity `p(ℓ)=2^ℓ`, entropy 1, complete de Bruijn
graph, no genuine forbidden words (iid-control-confirmed) — a full 2-shift.** Extends the "structureless/random face"
to the symbolic-complexity axis; no combinatorial foothold. SOUNDNESS: `[OBSERVED]`, iid control run; `(K)` `[OPEN]`;
no machine decided.*

## Measurement `[OBSERVED, N=6·10⁴ recursive orbit]`
Subword complexity of the parity word `p_n=c_n mod 2` (`c₀=8, c→⌊3c/2⌋`): **`p(ℓ)=2^ℓ` exactly for `ℓ=1..12`** (every
binary word appears), `log₂p(18)/18 = 0.873`. Apparent "forbidden words" from `ℓ=13` (`11` missing at `ℓ=13`, `476` at
`ℓ=14`, …) are **finite-size sampling artifacts**: an iid Bernoulli(½) word of the same length has essentially the same
counts (`ℓ=13`: `11` vs `6` vs Poisson `5.4`; `ℓ=15`: `5397` vs `5251` vs `5253`; `ℓ=16–18`: within `<1%`). So no
genuine forbidden factor exists up to the sampling horizon `ℓ≈log₂N`.

## Reading
- **The parity/base-3/2-digit word is (empirically) a FULL 2-shift** — maximal subword complexity, topological entropy
  `1`, **complete de Bruijn graph** (every edge present), **non-sofic** (no finite forbidden set → no finite automaton).
  Statistically indistinguishable from iid fair coin at the *symbolic-complexity* level, not just the harmonic level.
- **No de Bruijn / low-complexity / soficity foothold** for `(K)`. The literature's de Bruijn-graph angle gives nothing
  exploitable for *our* sequence: the graph is complete, so it carries no forbidden-pattern constraint to leverage.
- This is the **third independent axis** confirming the "structureless" face of the wall (after harmonic statistics
  `BLIND_HARMONIC` and occupancy/countdown `BLIND_EFFECTIVENESS`): now **symbolic complexity** is maximal too. The
  `(K)` word is deterministic (single orbit) yet full-entropy — exactly the rank-1 amenable "deterministic-but-random"
  regime with no structure for a proof to grip. (Minor: a mild `ℓ=13–14` excess over iid, `11` vs `6`, is within
  two-sample fluctuation and not pursued.)

## Verdict
**(c) — rederives the wall on a new axis; no foothold.** The Antihydra parity / base-3/2 digit word is a full 2-shift
(maximal complexity, complete de Bruijn graph, non-sofic), closing the combinatorial/complexity route. Extends the
duality's random face to symbolic complexity. **`(K)` `[OPEN]`. No machine decided. No label upgraded.**

## Reproduce
- `scratchpad/parity_complexity.py`, `scratchpad/parity_control.py` (`/opt/homebrew/bin/python3.13`, exact int, N=6·10⁴):
  `p(ℓ)=2^ℓ` to `ℓ=12`; "forbidden" counts match iid control + Poisson. Basis: `DICT_AND_EXCDIM_2026-07-05.md` (the word),
  `BLIND_HARMONIC_2026-07-05.md`/`BLIND_EFFECTIVENESS_2026-07-05.md` (the other random-face axes), arXiv:1811.02254.
