# o12 / o13 / o14: halt predicates PROVEN from the table (2026-07-04)

*Brings the halt predicates of the three Type-I Mahler-3/2 cryptids o12, o13, o14 to o17/o3 rigor: each halt
state has a **unique predecessor transition**, so the halt condition is `[PROVEN from the transition table]` a
single bounded-context tape event, and that event is machine-verified to **never fire** from the blank tape.
Non-halting is thus exactly "the gate is never triggered" — an existence/parity event over each machine's `×3/2`
Mahler orbit (`CRYPTID_CLASSIFICATION_2026-07-04.md` Type I = the (K) wall). SOUNDNESS: `[PROVEN]`/`[OBSERVED]`;
zero false proofs; **halting stays `[OPEN]`**. Verifier: `cryptid_halt_gates_verify.py` (`... VERIFIED: True`).*

## The three gates `[PROVEN from the table]`

For each machine the halt state is reachable by exactly one transition (checked by scanning the table for the
halt-state target), so halting reduces to that transition landing on a `0`:

| machine | halt | unique predecessor | ⇒ **HALT ⟺** |
|---|---|---|---|
| **o12** `1RB0RE_1LC1LD_0RA0LD_1LB0LA_1RF1RA_---1LB` | `F,0` | `E,0→1RF` (only edge into F) | state `E` reads a `0` whose **right** neighbour is also `0` (an `E`-phase `00`) |
| **o13** `1RB0LC_0LC0RF_1RD1LC_0RA1LE_---0LD_1LF1LA` | `E,0` | `D,1→1LE` (only edge into E) | a `D,1→1LE` step lands the head on a `0` — i.e. `D` reads a `1` whose **left** neighbour is `0` |
| **o14** `1RB0LC_1LC0RD_1LF1LA_1LB1RE_1RB1LE_---0LE` | `F,0` | `C,0→1LF` (only edge into F) | state `C` reads a `0` whose **left** neighbour is also `0` (a `00`) |

o12 and o14 are **`00`-existence** gates (the sweep meets an empty block), exactly like o3/o11/o16; o13 is a
**parity** gate (the erase-sweep exits in `E` onto a `0` iff a block it crosses has the wrong parity), like o17.

## Machine-verified safety `[OBSERVED, blank tape to 15M, 0 exceptions]`

Every trigger event is **safe** — the neighbour that would have to be `0` for a halt is always `1`
(`cryptid_halt_gates_verify.py`):

| machine | trigger `(state,read)` events | of which safe (neighbour = 1) | gate fires (= halts) |
|---|---|---|---|
| o12 | `E,0` : 5880 | 5880 | **0** |
| o13 | `D,1` : 4067 | 4067 | **0** |
| o14 | `C,0` : 3240 | 3240 | **0** |

So within each machine's normal form the sweep always finds the safe neighbour (a nonempty block / even block),
and the gate never fires.

## Net

Each of o12, o13, o14 halts **⟺ its `[PROVEN]` gate is ever triggered** — a `00`-existence (o12, o14) or parity
(o13) event. Because the tape content is a `×3/2` Mahler orbit (Type I; exact maps `V'=⌊3V/2⌋+c` (o12),
`a'=⌊3a/2⌋+c` (o13), `A'=⌊3A/2⌋+6` (o14), `CRYPTID_CLASSIFICATION_2026-07-04.md`), deciding whether the gate ever
fires = a parity/alignment question along a `⌊3x/2⌋` orbit = the **(K)/Mahler-3/2 (Erdős) equidistribution wall**.
This upgrades the agents' `[OBSERVED]` halt descriptions to a `[PROVEN from table]` gate + `[OBSERVED]` safety,
matching the o17/o3 standard. **Halting `[OPEN]` for all three. No machine decided. No label upgraded.**

## Reproduce
- `cryptid_halt_gates_verify.py` — audits each gate (unique halt-predecessor from the table) and its trigger
  events from the blank tape: 0 firings, every trigger safe. Prints `HALT-GATES VERIFIED ... : True`.
- Maps/normal forms: `CRYPTID_CLASSIFICATION_2026-07-04.md` §2. TMs: `cryptid_census.py`. Interpreter
  `/opt/homebrew/bin/python3.13`.
