# o2 / o7: halt predicates PROVEN from the table + counter reduction (2026-07-04)

*Brings the two Antihydra-class two-counter cryptids **o2, o7** (Type I, `1^a 0 1^b`) to o17/o3 rigor: a
`[PROVEN from the transition table]` halt gate, verified never to fire from the blank tape, plus the
milestone-level reduction of halting to a balance/counter event over the machine's `⌊3x/2⌋` orbit (the (K)
wall). Unlike the sea machines (o11–o16) the gate is **not vacuous** — o2/o7 DO halt for constructed seeds; the
blank orbit merely avoids them. SOUNDNESS: `[PROVEN]`/`[OBSERVED]`; zero false proofs; **halting `[OPEN]`**.
Verifier: `cryptid_halt_gates_verify.py`.*

## The gates `[PROVEN from the table]`

Each halt state has a unique predecessor (table scan for the halt-state target):

| machine | halt | unique predecessor | ⇒ **HALT ⟺** |
|---|---|---|---|
| **o2** `1RB1RC_1LC1LE_1RA1RD_0RF0RE_1LA0LB_---1RA` | `F,0` | `D,0→0RF` (only edge into F) | state `D` reads a `0` whose **right** neighbour is also `0` (a `00`) |
| **o7** `1RB0RB_1LC1RE_1LF0LD_1RA1LD_1RC1RB_---1LC` | `F,0` | `C,0→1LF` (only edge into F) | state `C` reads a `0` whose **left** neighbour is also `0` (a `00`) |

Both are `00`-existence gates. **Blank-tape audit** (`cryptid_halt_gates_verify.py`): o2 `D,0`×3834 all safe,
o7 `C,0`×3199 all safe — **0 firings** from blank.

## Non-vacuous — the gate DOES fire, over the two-counter orbit `[OBSERVED, verified]`

Unlike o11–o16 (whose gate is `[PROVEN]` unreachable *within* the normal form), o2/o7 genuinely halt for some
milestone seeds; the blank orbit avoids them. On the `1^a 0 1^b` milestone automaton
(`CRYPTID_SLOWWIDTH_2026-07-04.md`, `CRYPTID_CLASSIFICATION_2026-07-04.md` §2):

- **o7** — verified: from the milestone config `0 1^a 0 1^b` (head at the frontier, state D), `a=1 → HALT`
  (6 steps), `a=5 → HALT` (31 steps, via `a=5→1`), while `a=2,6 → run`. So
  > **o7 HALTS ⟺ the left counter `a` reaches `1`** (`a=1`'s unique milestone-preimage is `a=5`), where `a`
  > follows the coupled two-counter map `even a:(a,b)→(3a/2+1+b,1)`, `odd a:→((a−3)/2, b+(a+5)/2)`. Blank orbit
  > `(1)→(2,2)→(6,1)→…` keeps `a≥4` (min a=4 over 2M milestones) ⇒ avoids the gate. *(Caveat: the exact halting
  > coordinate has a config-convention discrepancy across agents; the robust, verified facts are the PROVEN
  > `C`-reads-`00` gate, the ×3/2 map, and that the blank orbit avoids the small danger values.)*
- **o2** — the balance counter `b` is an Antihydra-style cocycle over the parities of the `a↦⌊3a/2⌋` orbit
  (`x=a+4↦⌊3x/2⌋`, verified). The single-marker state `S(N)` with `N` odd halts; its preimage is `D(a,0)` with
  `a≡1 (mod 4)`. So
  > **o2 HALTS ⟺ the balance `b` returns to `0` at a milestone with `a≡1 (mod 4)`** — a balance-returns-to-zero
  > criterion, exactly the Antihydra shape. Blank orbit: `b` drifts up (`+0.502`/milestone) and never returns
  > to `0` after the start ⇒ avoids the gate.

## Net

Each of o2, o7 halts **⟺ its `[PROVEN]` `00`-gate ever fires ⟺** (milestone level) a **counter/balance event on
its `⌊3x/2⌋` Mahler orbit** — `a` reaching `1` (o7) / `b` returning to `0` at `a≡1 mod4` (o2). Deciding whether
the blank orbit ever hits that event = single-orbit equidistribution of the `⌊3x/2⌋` parities = the
**(K)/Mahler-3/2 (Erdős) wall**. This matches the o17/o3 standard (`[PROVEN from table]` gate + reduction to an
event over the machine's own orbit) and completes the halt-predicate treatment of **all nine reverse-engineered
slow-width cryptids** (Type II o17/o3; Type I o2/o7/o11/o12/o13/o14/o16; Type III Space Needle). **Halting
`[OPEN]` for all. No machine decided. No label upgraded.**

## Reproduce
- `cryptid_halt_gates_verify.py` — blank-tape gate audit (o2 `D,0`×3834, o7 `C,0`×3199, all safe, 0 firings)
  plus the o7 non-vacuous check (`a=1,5 → HALT`; `a=2,6 → run`). TMs: `suite.py`/`cryptid_map.py`. Interpreter
  `/opt/homebrew/bin/python3.13`.
