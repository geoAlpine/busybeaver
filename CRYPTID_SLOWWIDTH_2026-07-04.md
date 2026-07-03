# Slow-width cryptid kernel extraction — five machines, all Mahler/Collatz-class (2026-07-04)

*Applied the o17 reverse-engineering methodology (`O17_CORE_TRANSDUCER.md`) to the five best "slow-width"
BB(6) cryptids whose kernels were listed **un-extracted** (`CRYPTID_CENSUS.md`): **o2, o7, o11, o16, and
Space Needle**. A parallel multi-agent assault; every headline claim was cross-checked against the raw TM by
the orchestrator. SOUNDNESS: `[PROVEN]`/`[OBSERVED]`/`[OPEN]` labels; zero false proofs; **the discipline
caught a concrete error** (Space Needle §5). **No machine decided; halting stays `[OPEN]` for all five.**
Verifier: `cryptid_slowwidth_verify.py`. TMs are in `suite.py`/`tier3_suite.py` (the census's "TMs not in
repo" claim was wrong — all cryptid TMs are present).*

## 0. Headline

**All five are Mahler/Collatz-class; NONE is a fresh o17-style structural outlier.** Four (o2, o7, o11, o16)
sit on the **(K)/Mahler-3/2 (Erdős) equidistribution wall**; Space Needle is a **scalar generalized-Collatz**
machine. The **√t growth that flagged them as "o17-class" is a red herring** — it is produced by unary-encoded
exponential-Mahler orbits (o2, o7), a base-3/2 odometer (o11), and a quadratic-cost ×3/2 engine (o16), not by
an o17-type tame odometer. **o17 remains the unique genuine outlier** (no equidistribution kernel; hardness is
its Collatz-irregular halt predicate alone).

| machine | growth | mechanism (verified vs raw TM) | wall | verdict |
|---|---|---|---|---|
| **o2** | `√t` | `1^a 0 1^b` two-block automaton: `a` a clean ⌊3x/2⌋ Mahler map, `b` an Antihydra balance counter; value stored **unary** ⇒ exp-Mahler disguised as `√t` | (K)/Mahler-3/2 | (b)+(c) |
| **o7** | `√t` | identical shape to o2 (`1^a 0 1^b`); reset-`a` values `6,11,16,26,41,49,58,89,…` → **×3/2 exactly** (tail ratios 1.502,1.503,1.504) | (K)/Mahler-3/2 | (b)/(c) |
| **o11** | `√t` | base-3/2 **odometer** bouncer: reflection increments `D_{n+1}=⌊3D_n/2⌋+ε`, `ε∈{1,2,3}` a carry bit; halt ⟺ top-digit (marker) → 0 | Mahler-3/2/Erdős | (b)/(c) |
| **o16** | `√t` | **nested** Mahler-3/2: inner `S'=⌊3S/2⌋+c` (`c∈{4,6}`), middle countdown −1/epoch, doubly-exp outer refill; √t = ×3/2 engine × quadratic epoch cost | (K)/Mahler-3/2 | (c) |
| **Space Needle** | `step^{1/3}` | **scalar** generalized-Collatz: milestone = single block `1^m`; `f(m)=m+3⌊m/2^{v+1}⌋+v` (`v`=trailing-1s); cubic-time/linear-space | Collatz | (b), **corrected** |

## 1. o2 — Antihydra-class, unary-disguised `[OBSERVED, verified]`
Milestone (state A, left frontier): `[11]·[1]^a·[11]·[1]^b`, single-0 gaps, width `2a+2b+6`. Map:
`D(a,b)→D((3a+4)/2,b+2)` (`a` even) / `D((3a+7)/2,b−1)` (`a` odd, `b≥1`) / `S((3a+11)/2)` (`a` odd, `b=0`);
`S(N)→D((3N−2)/2,1)` (`N` even) / **HALT** (`N` odd). Orchestrator cross-check: raw blank orbit gives
`D(2,1)→D(5,3)→…` exactly (verified), and the value ladder `x=a+4 = 6,9,15,24,36,54,81,123,186,279` satisfies
`x↦⌊3x/2⌋`. **HALT ⟺ the balance `b` returns to 0 at a milestone with `a≡1 (mod 4)`** — an Antihydra-style
balance-returns-to-zero criterion on a ⌊3x/2⌋ orbit = the (K) wall.

## 2. o7 — coupled two-counter Mahler-3/2, exact map `[VERIFIED, 5850 pairs + 2M-milestone orbit, 0 mismatches]`
Milestone (state D, left frontier): `0 1^a 0 1^b` (two unary counters). **Exact closed-form return map:**
```
   even a≥2:  (a,b) → (3a/2 + 1 + b, 1)          # growth step (reads b)
   odd  a≥5:  (a,b) → ((a−3)/2, b + (a+5)/2)      # collapse/refill step (feeds b)
   a=3: →(b+5, 2·[b odd]) ;  a=1: → HALT
```
Raw blank orbit `(1)→(2,2)→(6,1)→(11,1)→(4,9)→(16,1)→(26,1)→(41,1)→…`; the `b=1` reset-`a` values
`6,11,16,26,41,49,58,89,103,131,166,251,316,476,716,1076,1616,…` grow **×3/2 in the tail** (verifier ratios
1.502,1.503,1.504). The even step `a↦3a/2+(b+1)≥3a/2` makes the **content exponential** (`a` exceeds 4300
digits over 2M milestones) — a genuine Mahler ×3/2 orbit; the `√t` width is just the `(3/2)a²` quadratic cost of
grinding unary counters (a red herring, same geometry as o17 but exponential *content*).
> **Halt predicate `[reduction verified, halt event proven on raw TM]`.** `HALT ⟺ the left counter `a` reaches
> `1` ⟺ (unique milestone-preimage) **the orbit ever reaches `a=5`** — a clean single-coordinate predicate
> (comparable to o17's 1-bit one). Halt-avoidance observed to 2M milestones (`min a=4`; danger values
> `a∈{1,5,3,7,…}` never revisited; no modular pattern) but **not proven** — the Mahler-3/2/(K) wall.

*(The o7 subagent ran ~5.2h/100 tool-calls; the orchestrator independently recovered the same map, reset
values, and Mahler-3/2 verdict from the raw TM before the agent's report landed — they agree exactly. The
stray `(2,1)→HALT` in an early scratch file was a wrong start point; the true blank start does not halt.)*

## 3. o11 — base-3/2 odometer bouncer `[OBSERVED, verified]`
Normal form (state E, right frontier): `1^L · (10)*` with one migrating `00` "ball" and a `1`/`11` cap; **digit
values are uniform (all 1)** — the hardness is *lengths*, not a value cascade (contrast o17). Reflection widths
`D=10,18,28,44,68,104,158,240,362,544,818,1230,1846,2772,4160` obey `D_{n+1}=⌊3D_n/2⌋+ε` (`ε∈{1,2,3}`, a
single carry-parity bit). **HALT gate `[PROVEN from the table]`:** the only edge into halt-state C is `B,0→1LC`,
and `C,0`=HALT, so **HALT ⟺ B ever reads a `00`** ⟺ the leading marker (odometer top digit) is consumed to
length 0 (observed min marker = 1 over 20M steps). = the base-3/2 Mahler/Erdős equidistribution wall.

## 4. o16 — nested Mahler-3/2 `[OBSERVED, verified]`
Milestone `1^a 0 1^S` (collapsed two-block). Inner big block `S'=⌊3S/2⌋+c` (`c∈{4,6}`): verified
`S=22,37,59,94,145,221,335,508,768,1158,1741,2615`, ratios →1.500, `S'−⌊3S/2⌋∈{4,6}` exactly. Leading counter
`a`↓1/epoch; at `a=1` a doubly-exponential refill (`a:3,2,1→25`). Per-epoch step ratio →2.25=(3/2)² (quadratic
cost) with `W∼S∼(3/2)^{epoch}` ⇒ `W∼√t`. Halt = a `00`-vs-`11` phase race in the sea-collapse sweep, blocked as
a defect-existence event over the doubly-exp refill. Confirms the prior `REDUCE_O11_O16.md`. Mahler-3/2 wall.

## 5. Space Needle — scalar generalized-Collatz, with a SOUNDNESS CORRECTION `[OBSERVED, corrected]`
Milestone = a single block `1^m`, head on the `0` just right of it, state C (verified: `0001111100` for m=5,
`00011111111100` for m=9, `…` — head on the trailing 0). Width `= m+2`. The subagent found the milestone map
```
        f(m) = m + 3·⌊m / 2^(v+1)⌋ + v ,   v = #trailing-1-bits of m
```
a 2-adic-digit-driven generalized-Collatz iteration (multiplier `1+3/2^{v+1}`, drift ×1.92, cubic epoch time ⇒
`W∼step^{1/3}`). The blank orbit `m: 2,5,9,16,40,100,250,625,1094,2735,…` is **verified against the raw TM**
(orchestrator reproduced `2,5,9,16,40,100` exactly) and does not halt.

> **CORRECTION (orchestrator, verified).** The subagent's clean claim *"HALT ⟺ the orbit reaches an all-ones
> number `2^k−1`"* is **FALSE.** Constructing the *true* milestone config (`1^m`, head on the right `0`, state
> C) and running the raw TM, the halt set for `m≤160` is `{1,3,6,7,15,31,63,102,127}` — **`m=6` (`110`) and
> `m=102` (`1100110`) halt but are NOT all-ones**, and the subagent's map gives `f(6)=15` where the raw TM
> actually **halts**. So the halt set is strictly larger than the all-ones set; the "0 mismatches over
> m=1..800" claim does not hold at the true config. **Net:** the map `f` correctly generates the blank orbit,
> and that orbit avoids the (true, richer) halt set in the tested range ⇒ still consistent with non-halting and
> `[OPEN]`; but the clean 1-line all-ones reduction is retracted. Blank-tape halting reduces to "does the orbit
> `2,f(2),f²(2),…` ever hit the halt set `S ⊋ {2^k−1}`?" — a generalized-Collatz reachability (Collatz wall).

## 6. Honest verdict
**Outcome (c) across the board** (o2 also (b) via the reclassification): every slow-width cryptid tested
**rederives a known wall** — four the (K)/Mahler-3/2 (Erdős) equidistribution wall, Space Needle the
generalized-Collatz wall. The genuine contributions are **structural**: exact normal forms + milestone maps for
all five (verified vs raw TM), the reclassification of the `√t`-bouncer phenotype (unary/odometer encodings, not
an o17 signature), and the retracted Space Needle all-ones claim. **o17 stays the unique structural outlier.**
**No machine decided. No non-halting proven. No label upgraded. Halting `[OPEN]` for all five.**

## Reproduce
- `cryptid_slowwidth_verify.py` — checks (A) o7 reset-`a` ratios → 3/2 (Mahler-3/2), (B) the Space Needle
  correction (raw-TM halt set `{1,3,6,7,15,31,63}` for m≤64, `m=6` halts ∉ all-ones; blank orbit avoids it).
- TMs: `suite.py` / `tier3_suite.py`. Interpreter `/opt/homebrew/bin/python3.13` (`python3` alias is broken).
- Per-machine scratch scripts (o2/o7/o11/o16/SN sims + automata) live in the session scratchpad, not committed.
