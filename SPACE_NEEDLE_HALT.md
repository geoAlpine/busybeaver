# Space Needle: halt predicate PROVEN from the table + scalar reduction (2026-07-04)

*Brings the Type-III cryptid **Space Needle** to o17/o3 rigor: a `[PROVEN from the transition table]` halt gate,
plus the scalar generalized-Collatz reduction of blank-tape halting (with the earlier all-ones **correction**
folded in). SOUNDNESS: `[PROVEN]`/`[OBSERVED]`; zero false proofs; **halting stays `[OPEN]`**. Verifier:
`cryptid_halt_gates_verify.py` (`... VERIFIED: True`).*

Space Needle = `1RB1LA_1LC0RE_1LF1LD_0RB0LA_1RC1RE_---0LD` (blank tape; halt = F reads 0). Table:
`A:0→1RB,1→1LA · B:0→1LC,1→0RE · C:0→1LF,1→1LD · D:0→0RB,1→0LA · E:0→1RC,1→1RE · F:0→HALT,1→0LD`.

## 1. Milestone normal form `[OBSERVED, verified vs raw TM]`

The head returns over and over to a **single unary block**: milestone = `0^∞ 1^m 0^∞`, head on the `0`
immediately **right** of the block, in state **C** (verified: `…0 1^5 0…` = `0001111100`, head on the trailing
`0`, for m=5; `…1^9…` for m=9; etc.). The entire configuration is one scalar `m`; width `W = m + 2`.

## 2. The halt gate `[PROVEN from the table]`

State `F` (the only halt) is entered **only** by `C,0→1LF` (scanning the table for the target `F`). `C,0→1LF`
writes a `1`, moves **left**, and `F` then reads the cell to the left; `F,0`=HALT. Hence

> **`[PROVEN]` HALT ⟺ state `C` reads a `0` whose left neighbour is also `0`** (a `00`).

Same `00`-existence gate as o3/o11/o12/o14/o16. **Blank-tape audit** (`cryptid_halt_gates_verify.py`): over
`684` `C`-reads-`0` events the left neighbour is **always `1`** (0 firings) — the blank orbit never triggers it.

## 3. The scalar reduction, and the halt set `[OBSERVED, corrected]`

Because a milestone is a single scalar `m`, one epoch is a deterministic map `m ↦ f(m)` (verified against the
raw TM by constructing the config and running one epoch):
```
        f(m) = m + 3·⌊m / 2^(v+1)⌋ + v ,     v = number of trailing 1-bits of m
```
a 2-adic-digit-driven generalized-Collatz iteration (multiplier `1+3/2^{v+1}`; cubic epoch time ⇒ `W∼step^{1/3}`).
The blank orbit `m: 2,5,9,16,40,100,250,625,1094,…` is reproduced exactly.

> **The gate fires (an epoch halts) exactly for `m` in a halt set `S`.** From the true milestone config, the raw
> TM halts for `m≤255` at `S∩[1,255] = {1,3,6,7,15,31,63,102,127,255}` — i.e.
> ```
>        S = { 2^k − 1 : k ≥ 1 }  ∪  {sporadic non-all-ones},   sporadic ∩ [1,255] = {6, 102}
> ```
> **CORRECTION** (the reverse-engineering subagent claimed the clean `HALT ⟺ all-ones 2^k−1`): **FALSE** — the
> two sporadics `6=110` (`=2·3`) and `102=1100110` (`=2·3·17`) halt but are not all-ones, and `f(6)=15` predicts
> continuation where the TM in fact halts. So `S ⊋ {2^k−1}`; the sporadic set is very sparse (`2` in `255`) and
> its exact rule is a small `[OPEN]` sub-curiosity. The blank orbit `2,5,9,16,40,…` avoids all of `S`.

## 4. Net

> **`[PROVEN gate]` Space Needle halts ⟺ its `C`-reads-`00` gate ever fires ⟺ the scalar orbit
> `m, f(m), f²(m), …` (from `m₀=2`) ever reaches the halt set `S`** (with `S ⊋ {all-ones}`, a `00`-defect set).

The blank orbit `2,5,9,16,40,100,…` avoids `S` in the tested range (`orbit ∩ S = ∅`), so it is consistent with
non-halting — a **generalized-Collatz reachability** question (does a `2`-adic-driven `⌊·⌋` orbit ever hit a
sparse set), the Collatz wall (Michel; Kurtz–Simon). This matches the o17/o3 standard (a `[PROVEN from table]`
gate + the reduction to an existence event over the machine's own orbit), and folds in the soundness correction.
**Halting `[OPEN]`. No machine decided. No label upgraded.**

Together with `O17_CORE_TRANSDUCER.md`, `O3_TRANSDUCER.md`, and `MAHLER_HALT_GATES_2026-07-04.md`, **every
reverse-engineered slow-width cryptid now has a `[PROVEN from table]` halt gate**: Type II (o17, o3) decide on
their own carry cascade; Type I (o11, o12, o13, o14, o16) on a `⌊3x/2⌋` Mahler orbit; Type III (Space Needle) on
a scalar generalized-Collatz orbit.

## Reproduce
- `cryptid_halt_gates_verify.py` — the blank-tape gate audit (SN `C,0`×684, all safe, 0 firings) **and** the
  scalar-gate check (the gate fires exactly for `m∈{1,3,6,7,15,31,63}` at `m≤64`, i.e. all-ones ∪ `{6}`).
- TM in `cryptid_census.py` / `suite.py`. Interpreter `/opt/homebrew/bin/python3.13`.
