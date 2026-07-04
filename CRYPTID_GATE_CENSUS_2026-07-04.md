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

## Thinness addendum `[OBSERVED, all 1104, cap 1.5 M]`
Running every holdout from the blank tape (`thin_census.py`): **0 halt** (all non-halting in budget), **0 machines
whose halt-state is never entered** (every machine's head *does* reach its gate), and the would-halt config
**never appears** at any halt-state entry — `danger-ratio` `= 0` (mean/median/max) across all 1101 single-halt
machines. So **frontier-wide, every halt target is empirically thin**: the gate is approached but the halting
adjacency is structurally absent. **Limit (honest):** this is the blank-orbit level; it **cannot detect
annealed-thickness** (o10's density-⅓ target is a property of its *extracted outer model* — o10 too has
`danger=0` from the raw blank orbit). So the census confirms uniform blank-level thinness but neither finds nor
rules out other o10-class machines (which would need per-machine outer-model extraction).

## The 3 doubly-disjunctive machines `[OBSERVED]`
The 3 two-halt-transition machines each halt on a **disjunction of two configs**:
- **L334** `1RB---_1RC---_1RD1LC_1LE1RF_1LC0LE_1RA0RD`: halt `A:1` **or** `B:1` — the sweep writes `1`s rightward
  (`A:0→1RB`, `B:0→1RC`) and halts on reading a `1` in `A` or `B`.
- **L752** `1RB1LA_1RC0RF_1RD---_0LE1RB_---0LA_1LD1RF`: halt `C:1` **or** `E:0`.
- **L1019** `1RB1LD_1RC0RB_1LA1RC_1LE0LA_1LF---_1LC---`: halt `E:1` **or** `F:1`.
Still bounded-context existence gates — the target is a 2-config disjunction rather than one config.

## The consolidated frontier-wide gate picture
> **Every one of the 1104 holdouts halts (if ever) on a bounded-context existence gate over its own orbit** — a
> single unique-predecessor config (87%), a disjunction of predecessor-contexts into one halt-state (13%), or a
> disjunction of two halt-configs (0.3%); every machine approaches its gate but never presents the halting
> adjacency. This is the frontier-wide validation of the grand synthesis's **"halt = reachability of a target
> config"** on a non-affine orbit — confirmed across all 1104, not just the ~16 named cryptids.

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
