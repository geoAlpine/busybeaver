# o3: the second BB(6) structural outlier, at o17's proof standard (2026-07-04)

*`CRYPTID_CLASSIFICATION_2026-07-04.md` established o3 as a **second Type-II structural outlier** beside o17 —
a tame finite-control head over a single-`0`-separated digit string with **no equidistribution kernel**, all
hardness in a Collatz-irregular halt predicate. This note brings o3 to o17's rigor (`O17_CORE_TRANSDUCER.md`):
a machine-verified normal form + finite control, a free-running length counter, and a **`[PROVEN from the
table]` halt gate**. SOUNDNESS: `[PROVEN]`/`[OBSERVED]`/`[OPEN]` labels; zero false proofs; **halting stays
`[OPEN]`**. Verifier: `o3_transducer.py` (prints `... VERIFIED: True`, 0 exceptions).*

o3 = `1RB1LD_1RC1RE_0LA1LB_0LD1LC_1RF0RA_---0RC` (blank tape; halt = state F reads 0). Table:
`A:0→1RB,1→1LD · B:0→1RC,1→1RE · C:0→0LA,1→1LB · D:0→0LD,1→1LC · E:0→1RF,1→0RA · F:0→HALT,1→0RC`.

## 1. Normal form + finite control `[OBSERVED, 2216 milestones to 12M, 0 exceptions]`

> Every milestone (head in state `A` at the left frontier) is a word in the regular language
> `𝓛 = (1|11)·( 0·(1|11) )*` — 1-blocks of length **1 or 2** (bounded digit alphabet, digit `d=len−1∈{0,1}`),
> separated by **single `0`s**, starting and ending with a block.

The milestone-to-milestone map is a **fixed finite-control head** (verifier §II): across 12M steps the head
touches the tape through only **11** boundary-crossing `(state,read,dir)` triples, **3** right-reflection and
**6** left-gate `(state,read)` pairs — no symbol beyond these fixed sets ever appears. So o3 is a finite head
bouncing over a single-`0`-separated **{0,1}-digit** string.

**Even tamer than o17.** o17's interior digits are *unbounded* (`ℓ≡2 mod3`, `d=0,2,4,…`); o3's are *bounded*
`{0,1}`, and the digit sum `S` (= number of length-2 blocks) grows only **logarithmically** (`S = 3,7,10,13` at
milestones `10,50,200,1000`). o3 is the tamest cryptid found — yet still Collatz-hard in its halt predicate (§3).

## 2. Free-running length counter + width identity `[OBSERVED, 0 exc]` (verifier §IV)

The only unbounded coordinate is the **string length** `m` (number of blocks): it is a **free-running counter**
that ticks `+1` or `+2` per milestone and **never decreases**. Exact width identity
```
        W = 2m + S + 2          (m = #blocks, S = #length-2 blocks)
```
Since `S` is logarithmic, `W = 2m + O(log)`, and each milestone costs `Θ(m)` steps (a bounce across the width),
so `step ≈ Θ(m²)` and `width ∼ step^{1/2}` — a **quadratic-time / linear-space** bouncer. This is the o17
free-running-counter mechanism (`O17_CORE_TRANSDUCER.md` §6) with a *bounded-digit* string: the `√t` growth and
the Collatz-hardness come from the length counter + carry, not from any value orbit (there is none).

## 3. The halt gate `[PROVEN from the table]` + the Collatz-hard residual

State `F` (the only halt) is entered **only** by `E,0→1RF`; then `F,0`=HALT / `F,1→0RC`. Reading straight off
the table:

> **`[PROVEN]` HALT ⟺ some step has the head in state `E` reading a `0` whose right neighbour is also `0`**
> (i.e. `E` reads the left `0` of a `00`). Equivalently: the rightward `E/F` sweep meets an **empty block**
> (a double gap) instead of a `1`-block.

This is **cleaner than o17's** parity gate — it needs no entry-invariant gadget, just F's unique predecessor.
Verified never fires (verifier §III): over **399,918** `E`-reads-`0` events the right neighbour is **always `1`**
(`E` is entering a nonempty block), so no `(0,0)` occurs — **within `𝓛`, `E` always finds a block after each
single-`0` gap, so o3 provably cannot halt while the tape stays in `𝓛`.**

> **The residual `[OPEN]`, Collatz-hard.** `𝓛` is only `[OBSERVED]`-closed: during a bounce the carry cascade
> **transiently** forms `00` defects (max interior `0`-run = 2), which are **healed by `A,0→1RB` before the
> `E/F` sweep's `F`-check reaches them** (observed 0 exceptions). So
> ```
>      o3 HALTS  ⟺  the carry cascade ever forms a 00 that the E/F sweep reads before A heals it
> ```
> — a **race / existence event over the irregular marker-carry dynamics**, the analogue of o17's
> "marker ever even". Unlike o17's clean single parity bit, o3's residual is a genuine `00`-existence event
> (not fixed by any bounded-context predictor), so it is **not** reducible below a generalized-Collatz
> reachability question. This is o3's wall.

## 4. Verdict

o3 is a **machine-verified second structural outlier** (Type II): a tame, bounded-digit, finite-control
odometer/bouncer with a free-running length counter, **no equidistribution kernel**, and a `[PROVEN from the
table]` halt gate — halting reduced to a Collatz-irregular `00`-existence race over its carry cascade, provably
impossible while the tape stays in the verified normal form `𝓛`. This matches o17's proof standard (PROVEN halt
gate + verified closure + free-running counter + localized Collatz-hard residual) and confirms `CRYPTID_
CLASSIFICATION_2026-07-04.md` §3: **o17 is not unique.** **Halting `[OPEN]`. No machine decided. No label
upgraded.**

## Reproduce
- `o3_transducer.py` — verifies (I) language closure `𝓛`, (II) fixed 11/3/6-symbol finite control, (III) the
  `[PROVEN]` halt gate (`E`-reads-`0` always has right-neighbour `1`; 0 halts), (IV) width identity `W=2m+S+2`
  and the monotone free-running length counter. Prints `O3 TRANSDUCER + HALT-GATE VERIFIED: True`.
- TM in `cryptid_census.py`. Interpreter `/opt/homebrew/bin/python3.13` (`python3` alias is broken).
