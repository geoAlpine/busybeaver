# o17 core is a SKEW PRODUCT — a finite 5-state leading-block automaton over an unbounded carry fiber (2026-07-04)

*New structural characterization of the o17 core (P6, the non-Mahler cryptid), complementing the "unbounded
interior digits" emphasis of `O17_CORE_TRANSDUCER.md` / `O17_HALT_STRUCTURE.md`. Finding: while the interior
base-3 digit string grows unboundedly, the **leading/marker block stays in a FIXED FINITE SET `{2,3,5,8,14}`**
(never exceeds 14), so the core is a **skew product**: a finite-state leading-block automaton (the base, carrying
the halt predicate) driven by the unbounded interior carry cascade (the fiber, carrying the Collatz-hardness).
SOUNDNESS: `[OBSERVED]` (robust to `j≤60`, 40 M steps) + `[PROVEN §7(I)]` links; **halting `[OPEN]`; no machine
decided.** o17 TM `1RB1LD_1RC0LE_1LA1RE_0LF1LA_1RB0RB_---0LB`; script `scratchpad/o17_lead.py`.

## 0. Headline
- **The leading/marker block of the o17 core takes values in the FIXED finite set `{2,3,5,8,14}` — never above
  14** — for every tested seed `C(3j)`, `j=1..60`, over 40 M-step runs, **while the tape width grows to thousands**
  (the interior digit string is unbounded). `[OBSERVED, robust]`.
- **So the o17 core is a SKEW PRODUCT:** a **finite 5-state base automaton** (the leading block) over an
  **unbounded fiber** (the interior carry cascade). The **halt predicate lives entirely on the finite base**
  (`[PROVEN §7(I)]` halt ⟺ leading block ever even — here refined to: reach the even subset `{2,8,14}` in the
  halt-gate state), while **all the Collatz-hardness lives in the fiber** (which base-edge fires, and whether the
  gate aligns, is driven by the unbounded interior).

## 1. The bounded base `[OBSERVED, j≤60, 40 M steps]`
Simulating from the embedded seeds `C(3j)` (marker `1^3`, then `j` zero-digits) and recording the leading 1-block
length at every left-frontier visit:

| `j` (`k=3j`) | status | width_max | leading-value set |
|---|---|---|---|
| 3 (9) | run | 5397 | `{2,3,5,8,14}` |
| 5 (15) | HALT | 1408 | `{3,5,8,14}` |
| 9 (27) | run | 5292 | `{3,8,14}` |
| 20,30 | run | ~5500 | `{3,8}` |
| 40,50,60 | run | ~5500 | `{3}` |

**Union over all runs: `{2,3,5,8,14}`, max 14.** The leading block is bounded by a constant while the interior is
unbounded — the defining signature of a skew product (finite base, infinite fiber).

## 2. The base automaton (extracted) `[OBSERVED]`
Transition graph of the leading value (fiber-driven), edge counts over `j=1..40`:

```
     3 ──►5 (13)     3 ──►8 (8)          3 = transient SOURCE (start marker; never re-entered)
     5 ──►2 (7)      5 ──►8 (11)         recurrent core = {2,5,8,14}
     2 ──►5 (2)      2 ──►8 (2)          even / halt-eligible = {2,8,14}
     8 ──►5 (1)      8 ──►14 (3)         odd = {3,5}
    14 ──►5 (2)
```

- **`3` is a pure source** (out-degree only) — once the start marker leaves `3` it never returns; the recurrent
  dynamics live on **`{2,5,8,14}`**.
- **`5` is the hub** (target of `2,3,8,14`; source to `2,8`).
- **The even states `{2,8,14}`** are the halt-eligible ones (`[PROVEN §7(I)]`: halt requires an even leading
  block). Reaching them is **necessary but not sufficient** — a run can sit at an even value without halting
  (e.g. `j=9` reaches `14` and does **not** halt), because halting additionally needs the even block read in the
  **halt-gate state** (the "no-jump" alignment, `O17_CORE_TRANSDUCER §7.2`, fiber-driven).

## 3. The skew-product picture `[the characterization]`
> **o17 core `=` (finite base automaton on `{2,3,5,8,14}`) `⋉` (unbounded interior base-3 carry cascade).**
> The base carries the **halt predicate** (finite-state: reach `{2,8,14}` in the gate); the fiber carries the
> **Collatz-hardness** (unbounded digits, no scalar reduction, `O17_CORE_TRANSDUCER §3`). Each base transition is
> triggered by a **carry arriving from the fiber**, so the *sequence* of base states is a factor of the fiber
> dynamics — and *which* even-state visit (if any) aligns with the gate is exactly the undecidable part.

This **refines** the prior results without contradicting them:
- `O17_CORE_TRANSDUCER §1` (finite CONTROL, unbounded digit VALUES) is the machine-level statement; **§2 here is
  the configuration-level statement**: not only the head-control but the **leading digit** is finite-state; the
  unboundedness is confined to the interior.
- `§7(I)` (halt ⟺ leading block ever even) is sharpened to **"the leading block is a 5-state automaton and halt =
  reaching its even subset `{2,8,14}` in the gate"** — a much smaller object than the full digit string.

## 4. What it does and does not buy `[honest]`
- **Does:** a clean, minimal structural placement — o17's halt is a **finite-state event on a bounded base**, so
  the "hardness" is precisely localized to (a) which fiber-carry drives each base edge and (b) the gate alignment.
  The halt predicate is *not* itself unbounded-state; the earlier "irreducibly multi-digit" obstruction is about
  the **fiber**, not the halt condition.
- **Does NOT:** give decidability. The base is finite but its **input (the fiber carry sequence) is the undecidable
  object**; reaching an even state is necessary-not-sufficient (the gate); and the halt set `{j: halts}` stays
  **Collatz-irregular** (`j=2,4,5,7,8,10,12,15,17,…` halt; `1,3,6,9,11,13,14,16,…` not — no clean residue rule,
  cap-sensitive). A skew product with an undecidable fiber is undecidable.

## 4b. The gate condition, in skew-product language `[OBSERVED]`
Refining §2's "reaching an even state is necessary-not-sufficient": all three halting seeds tested (`j=2,4,5`) halt
with the **identical configuration** `(state F, read 0, leading value 8)`, and the trigger is the head **entering
the leading block in state `A` while it is even** (value 8): `leadval=8` is touched on its leftmost `1` in state
`A`, which runs `A→…→F` reading `0` = HALT. Non-halting seeds (`j=3,9`) **never present an even leading block to
state `A`** in-window (they touch the leading block only in states `D,E,B`).

> **Gate = a base–fiber COINCIDENCE.** `halt ⟺` **(base) the leading value is even** `{2,8,14}` (obs. `8`) **AND
> (fiber) the interior delivers the head to it in the gate-state `A`.** The base-parity is the finite-state part;
> **which approach-state the head is in is fiber-determined** (the interior carry cascade routes the head), so the
> gate is a *cocycle condition on the fiber over the even base states*. The **no-jump lemma** (`O17_CORE_TRANSDUCER
> §7.2`) is exactly the statement that this approach is **local** (the marker shifts ≤1 base-3 step), which is what
> makes "approach-state" well-defined and the gate a finite check — the core-hard residual is *whether the
> fiber ever routes an even base state into state `A`*, a quenched property of the unbounded carry.

## 4c. Skew product is o17-SPECIFIC — o3 and Space Needle differ `[OBSERVED, cross-check]`
Testing the skew signature (bounded leading block over an unbounded fiber) on the other reverse-engineered
digit-string / scalar cryptids (`skew_test.py`, block-length trajectories):

| machine | type | max block length | #blocks | structure |
|---|---|---|---|---|
| **o17** | II | **unbounded** (interior/right → 4466) but **leading bounded (≤5)** | 8–500 | **SKEW PRODUCT** (bounded base × unbounded-value fiber) |
| **o3** | II | **bounded (≤6)** — *every* block | grows 13→1516 | **uniform bounded-alphabet odometer** (NOT skew: fiber also bounded; a subshift over `{1,11}` of growing length) |
| **Space Needle** | III | **unbounded** (single block → 310+) | **3** (scalar) | **NOT skew** (one growing scalar block; no base/fiber split) |

So the three non-Type-I structures are genuinely distinct: **o17 = skew product** (bounded leading, unbounded
interior values), **o3 = bounded-alphabet odometer** (all blocks bounded, unbounded *length*), **Space Needle =
scalar** (one unbounded block). This **splits the census's "Type II" band structurally**: the o3-type
(uniform-bounded odometer) and the o17-type (skew product with unbounded interior) are different objects — only
o17 has the finite-base / unbounded-fiber decomposition. The skew-product characterization is therefore a **feature
of o17's specific "unbounded interior digit values," not of Type II in general.**

## 5. Honest verdict
**(b) — a new structural characterization: the o17 core is a skew product of a finite 5-state leading-block
automaton `{2,3,5,8,14}` (halt-eligible even subset `{2,8,14}`) over an unbounded interior carry fiber.** It
localizes the halt predicate to a bounded finite-state base and confines all Collatz-hardness to the fiber,
sharpening `§7(I)` and complementing the "unbounded interior" obstruction. **The gate** (§4b) is a base–fiber
coincidence — halt ⟺ an even base state met by the head in the gate-state `A`, the approach-state being
fiber-determined, and the no-jump lemma = the approach is local. **Cross-check** (§4c): the skew product is
**o17-specific** — o3 is a uniform bounded-alphabet odometer (all blocks ≤6), Space Needle is a scalar (one growing
block); this splits the "Type II" band structurally. No decidability gain (fiber undecidable); the halt set stays
Collatz-irregular. **Halting `[OPEN]`. No machine decided. No label upgraded.**

## Reproduce
- `scratchpad/o17_lead.py` (+ inline scans): leading-block value set `⊆{2,3,5,8,14}` for `j≤60` over 40 M steps;
  base-automaton edges `3→{5,8}, 5→{2,8}, 2→{5,8}, 8→{5,14}, 14→5`. o17 TM
  `1RB1LD_1RC0LE_1LA1RE_0LF1LA_1RB0RB_---0LB`, interpreter `/opt/homebrew/bin/python3.13`. Basis:
  `O17_CORE_TRANSDUCER.md` (§1 normal form, §3 no-scalar, §7 parity halt), `O17_HALT_STRUCTURE.md` (halt set),
  `PROBLEM_LIST.md` P6/P11.
