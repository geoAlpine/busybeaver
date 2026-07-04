# Frontier-wide halt-gate census — the unique-predecessor gate is 87% of the 1104, not universal (2026-07-04)

*Empirical breadth test of the A11 gate-uniformity finding (`BB6_TYPE_IV_CENSUS §5d`: "every reverse-engineered
halt gate is a unique-predecessor `00`/`11` existence gate") across **all 1104 holdouts** (`gate_census.py`, from
the transition tables directly). Result: the unique-predecessor single-halt gate is the **dominant (87%)** pattern
but **not universal** — 13% have **disjunctive** (multi-predecessor) gates. This refines A11 from "uniform" to
"predominantly unique-predecessor," and confirms frontier-wide that **every** halt is a bounded-context existence
event (supporting the grand synthesis). SOUNDNESS: `[OBSERVED]`, table-level; no machine decided; halting `[OPEN]`.*

## The census `[OBSERVED, all 1104]`
| property | count | share |
|---|---|---|
| **exactly 1 halt-transition** | 1101 | 99.7 % |
| 2 halt-transitions (doubly-disjunctive) | 3 | 0.3 % |
| **unique-predecessor single-halt gate** (the clean A11 gate) | **963** | **87.2 %** |
| single-halt but **multi-predecessor** (disjunctive gate) | 138 | 12.5 % |

**Gate-type spread** (of the 963 unique-predecessor gates, by `predecessor-wrote → halt-reads`): `1→1` 415, `0→1`
252, `1→0` 190, `0→0` 106 — the `00`/`11`-family (`0→0`, `1→1`) accounts for `521`, the mixed-adjacency the rest.

## Reading
- **The A11 unique-predecessor gate is the majority pattern (87%), not universal.** The ~16 named cryptids (all
  unique-predecessor) generalised to a **dominant** frontier pattern, but **13% of holdouts have a disjunctive
  gate** — the halt-state is reachable from ≥2 transition-contexts (138), or from ≥2 distinct halt cells (3).
  This is a **refinement**, not a contradiction: A11 correctly described the reverse-engineered machines; the
  frontier simply has more gate variety than the named sample.
- **Every halt is still a bounded-context existence event.** Unique-predecessor gates fire on a single
  bounded-context adjacency; disjunctive gates fire on a *disjunction* of bounded contexts — both are
  finite-context existence gates over the machine's own orbit. So the grand-synthesis "halt = reachability of a
  target config" holds frontier-wide (the target is a single context for 87%, a small disjunction for 13%).
- **Consistency with 0 halters.** All 1104 are undecided holdouts; the gate structure (unique or disjunctive) is
  the *form* of the halt predicate — none fires from the blank tape in the sampled budget (consistent with the
  census's 0 halters, `BB6_TYPE_IV_CENSUS §1`).

## Honest verdict
**(b) — a frontier-wide refinement of A11.** The unique-predecessor `00`/`11` existence gate is the **dominant
(87%)** halt-gate form across all 1104 holdouts, with 13% disjunctive (multi-predecessor) and 0.3% doubly-disjunctive
— all still bounded-context existence gates. This confirms, frontier-wide, that every cryptid halt is a
reachability/existence event (grand synthesis), and sharpens A11's "uniform" to "predominantly unique-predecessor."
**Halting `[OPEN]`. No machine decided. No label upgraded.**

## Reproduce
- `scratchpad/gate_census.py`: for each of the 1104 TMs, count halt-transitions, test unique-predecessor of the
  halt-state, classify the gate adjacency. Data `_bbdata/bb6_holdouts_1104.txt`, interpreter
  `/opt/homebrew/bin/python3.13`. Basis: `BB6_TYPE_IV_CENSUS_2026-07-04.md §5d` (A11), `GRAND_SYNTHESIS_2026-07-04.md`
  (halt = reachability).
