# Exit-tree re-audit — the REGEN tree re-extracted BY TRANSPORT, not by length (2026-07-17)

*Instrument audit of the probes grounding `lean/X2.lean` §5z/§5aj: `exitSteps_tree_5/6/7/8`,
`exitArity_grounds`, `exitList_grounds`. Those probes (`x2ck_regen_seg.py`, `x2dt_tree8.py`)
identify a recursive sub-call **by step count alone** — a coincidence-prone test. This document
re-extracts the whole tree by **transport identity** and reports, per level, whether the Lean
groundings survive.*

*Probes: `x2ti_tree.py` (transport re-extraction), `x2ti_parse.py` (the §5z glue parse),
`x2ti_term3.py` (the TERM(3) audit), `x2ti_canon.py` (canonicity of the reference class).
Interpreter `/Users/aokiyousuke/quantum-ecc/.venv/bin/python`, exact, ON-PATH from
`x2bd_sim.build(2)` — the one orbit; a=5 and a=6 both live there. **No Lean file was edited.**
This document decides no halting and upgrades no label.*

---

## 0. Verdict

> **The Lean groundings SURVIVE transport-based re-extraction, at every level they claim.**
> `exitSteps_tree_5/6/7/8`'s recursive REGEN calls, and `exitArity_grounds`' arities `0,1,3,6`,
> are exactly what a transport-verified re-extraction produces. **Only the METHOD was fragile.**

That is a real result and it retires a live risk. But the audit is not clean, and two findings
must be recorded precisely:

| # | finding | status |
|---|---|---|
| 1 | Every REGEN sub-call in `exitSteps_tree_5/6/7/8` is a **genuine transport**. Arities `0,1,3,6` confirmed. Sums confirmed. | **[SETTLED — groundings hold]** |
| 2 | The length test **does** admit false positives, exactly as reported: only **4/8** REGEN(7)-length windows are the transport. It happens not to corrupt `k ≤ 8`. | **[CONFIRMED]** |
| 3 | At **k=10** the length method gives arity **16**, the transport method **15**. `exitArity 10 = 15`. The defective method, extended one level past its grounding range, would have **falsely refuted** the Lean closed form. | **[CONFIRMED]** |
| 4 | §5z's `83/47/113/122/76` and the `881`: **partly artifacts.** `113`, `122`, `78`, `881`, `798`, `3944` are residues of splicing at **spurious TERM(3) boundaries** and have no transport meaning. `83/47/76` survive. | **[OBSERVED]** |
| 5 | A 24-step anchor gap — the test by which **every** `termSteps 3` in the Lean trees was claimed — is realised by **TWO distinct transports**. In `exitSteps_tree_8`, **6 of 10** `termSteps 3` terms are length coincidences. The theorems remain TRUE (they are `Nat` identities); their **docstring reading** is what is wrong. | **[OBSERVED]** |
| 6 | `881` is **not** a level-7 object. It is not a real segment at all; its transport-real counterpart `1018` recurs at k=7,8,9,10. | **[OBSERVED]** |

---

## 1. The method — and why it is EXACT, not a proxy

The task specifies: replay the candidate's IN config, match its full `(state, head, Δpos)` trace,
then TI-filter (`regen_TI_generic`: an identical trace at all orbit sites). That is the right test.
It can be made **exact and cheap** by one observation about this machine.

In `x2bd_sim.TT` every transition `(state, bit) → (write, move, next)` is a **total function of
`(state, bit)`**:

```
('A',0)→(1,+1,'B')  ('A',1)→(0,+1,'E')   ('C',0)→(0,−1,'D')  ('C',1)→(1,−1,'E')
('B',0)→(1,+1,'C')  ('B',1)→HALT         ('D',0)→(0,+1,'E')  ('D',1)→(1,−1,'D')
('E',0)→(1,+1,'F')  ('E',1)→(0,−1,'C')   ('F',0)→(0,+1,'A')  ('F',1)→(1,+1,'E')
```

Therefore the `(state, head-bit)` **symbol word** emitted over a window determines, cell for cell:
every write performed, every move — hence the entire relative position trace `pos − pos₀` — and the
next-state sequence. So

> **two windows emit the same `(st,h)` word ⟺ they are the SAME transport**

— they read and write the same local cells with the same head excursion, and differ **only** in tape
padding they never touch. That is precisely the content of the Lean `∀ L R` statements
(`regen4_transport`, `regen5_transport`, `regen_TI_generic`). Word-identity is not a proxy for the
`(state,head,Δpos)` trace test; it is **equivalent** to it, and exact. Verified directly
(`x2ti_tree.py` step [3]): at every level, all sites' `(st,h,Δpos)` traces are identical.

This also lets the TI class be found **exhaustively over every offset** in the 620k-step prefix
(substring search), not just at anchors — a strictly stronger search than the grounding probes ran.

**Extent discipline.** Every head excursion and every block length in this audit is derived FROM the
tape — `min`/`max` of the real head positions, and the actual 1-cells of the simulator's own tape.
No `lo`/`hi` counter exists anywhere in these probes.

---

## 2. Canonicity — which class is the real REGEN(k)? (`x2ti_canon.py`)

For k=7 this is load-bearing: 8 windows have REGEN(7)'s length and they split **4/4** into two
transport classes. Picking the wrong one inverts every conclusion. So the choice must not rest on
"earliest" — it must rest on the **definition**.

§5z/§5y define REGEN(k) as the regeneration that **lays the fresh top block `1^{2^k−3}`** and
re-anchors `E`. That is a statement about the tape. Reading the Lean-grounded
`REGEN(5) = carry_exit_j4` OUT config at `n=7141` off the tape:

```
state E, head on 0, right tape:  0^4 1^29 0^2 1^13 0^2 1^5 0^2 1^1
                                      ^^^^ the fresh block 1^29 = 1^(2^5−3)
                                      sitting on the descending cascade 29,13,5 = 2^5−3, 2^4−3, 2^3−3
```

So the definitional test is: **at the window end, the first 1-run to the RIGHT of the head has
length `2^k−3`.** Applied to every length-candidate:

| | must lay | classes | verdict |
|---|---|---|---|
| REGEN(4) | `1^13` | 1 | class 0 lays `1^13` ✓ |
| REGEN(5) | `1^29` | 1 | class 0 lays `1^29` ✓ |
| REGEN(6) | `1^61` | 1 | class 0 lays `1^61` ✓ |
| **REGEN(7)** | `1^125` | **2** | class 0 (4 occ, first `[12709,15239]`) lays `1^125` ✓ · class 1 (4 occ, first `[55825,58355]`) lays **`1^1`** ✗ |
| REGEN(8) | `1^253` | 1 | class 0 lays `1^253` ✓ |
| REGEN(9) | `1^509` | 1 | class 0 lays `1^509` ✓ |
| REGEN(10) | `1^1021` | 1 | class 0 lays `1^1021` ✓ |

The rejected k=7 class lays `1^1` — it is not a regeneration at all. **The canonical class is
selected by the definition; "earliest" agrees with it in every case** (so the shortcut was harmless,
but the tape is the authority). The same test on the TERM blocks selects TERM(3) class 0 and
TERM(7) class 0.

Independent corroboration for k=7: `REGEN(9)` calls `REGEN(7)` (`exitList 9`), and the chosen class
is found at exactly the expected position, with the level sum closing exactly to
`exitSteps 9 = 35202`.

---

## 3. The TI classes — length vs transport (`x2ti_tree.py`)

620k steps of `build(2)`, 152 004 anchors. Every occurrence of the exact transport word:

| k | windows by LENGTH | windows by TRANSPORT | false positives |
|---|---|---|---|
| 4 | 32 | 32 | 0 |
| 5 | 16 | 16 | 0 |
| 6 | 8 | 8 | 0 |
| **7** | **8** | **4** | **4** — at `[55825,58355]`, `[155802,158332]`, `[451865,454395]`, `[552867,555397]` |
| 8 | 2 | 2 | 0 |
| 9 | 1 | 1 | 0 |
| 10 | 1 | 1 | 0 |

**The reported 4/8 at REGEN(7) is confirmed exactly.** The length test is genuinely unsound; it
simply happens to be sound at the levels the Lean file grounds.

Same audit on the TERM blocks (§4 below): TERM(3) **65/129**, TERM(7) **4/8**, all others clean.

---

## 4. Per-level verdict on the Lean groundings

`exitSteps_tree_k` re-extracted with **only transport-verified** sub-calls, compared to the literal
Lean statement:

| theorem | arithmetic sum | REGEN calls survive transport | full term-by-term parse |
|---|---|---|---|
| `exitSteps_tree_5` | **HOLDS** (218) | **HOLDS** — Lean `[]`, transport `[]` | **HOLDS** (identical) |
| `exitSteps_tree_6` | **HOLDS** (722) | **HOLDS** — Lean `[4]`, transport `[4]` | glue differs — §5 |
| `exitSteps_tree_7` | **HOLDS** (2530) | **HOLDS** — Lean `[4,5,4]`, transport `[4,5,4]` | glue differs — §5 |
| `exitSteps_tree_8` | **HOLDS** (9282) | **HOLDS** — Lean `[4,5,6,4,5,4]`, transport `[4,5,6,4,5,4]` | glue differs — §5 |

`exitArity_grounds` (`exitArity 5,6,7,8 = 0,1,3,6`):

| k | `exitArity k` | transport-measured arity | length-measured | verdict |
|---|---|---|---|---|
| 5 | 0 | **0** | 0 | **HOLDS** |
| 6 | 1 | **1** | 1 | **HOLDS** |
| 7 | 3 | **3** | 3 | **HOLDS** |
| 8 | 6 | **6** | 6 | **HOLDS** |

> **No Lean grounding is wrong.** Every recursive-call claim, every arity, every sum survives.
> The growing-arity conclusion — the whole `[DESIGN]` obstruction of §5z/§5aj, and the refutation of
> the bounded-arity lift — **stands on transport-verified evidence.**

### 4.1 The near-miss: k=10

Beyond the Lean grounding range, where the defect finally bites:

| k | `exitArity k` | transport arity | length arity |
|---|---|---|---|
| 9 | 10 | **10** ✓ | 10 |
| **10** | **15** | **15** ✓ | **16** ✗ |

```
transport calls(10) = [4,5,6,7,8,   4,5,6,7,  4,5,6,  4,5,  4]      (15 = exitArity 10)
length    calls(10) = [4,5,6,7,8,7, 4,5,6,7,  4,5,6,  4,5,  4]      (16 — the spurious REGEN(7))
```

The extra `7` is one of the four false-positive REGEN(7) windows. **Had anyone extended the
length-based probe to k=10, it would have reported `exitArity 10 = 16 ≠ 15` and appeared to refute
the Lean closed form.** The transport method clears it: `exitArity` is confirmed **two levels beyond
its grounding range**. This is the sharpest argument for retiring the length test outright.

---

## 5. The §5z parse verdict — `83/47/113/122/76` and `881`

**Confirmed: these are artifacts of a greedy TERM-boundary parse.** The mechanism is the *same
defect one level down*: every `termSteps 3` in the Lean trees was claimed purely because an anchor
gap equalled `termSteps(3) = 24`.

### 5.1 A 24-step anchor gap is TWO different transports (`x2ti_term3.py`)

| class | occ | first | `(st,h)` word | head excursion (from tape) | net Δpos | lays |
|---|---|---|---|---|---|---|
| **0 — the real TERM(3)** | 65 | `[90,114]` | `E0F0A0B0C0D1D1D0E1C0D1D1D1D1D1D1D0E1C0D1D0E1C0D0` | `[−9,+4]` | −8 | **`1^5`** ✓ |
| **1 — NOT TERM(3)** | 64 | `[6821,6845]` | `E0F1E1C1E1C1E1C1E1C1E1C1E1C1E1C1E1C1E1C1E1C1E1C1` | `[−19,+2]` | −20 | `1^1` ✗ |

They are not remotely the same object: class 0 is the block-final flush (an `F/A/B/C/D` descent
laying `1^5`); class 1 is a pure `E1C1` zigzag — a comb pass — that lays nothing. They collide only
in length.

### 5.2 Auditing every `termSteps 3` in the Lean trees

| theorem | `termSteps 3` terms | genuine TERM(3) | length coincidence |
|---|---|---|---|
| `exitSteps_tree_5` | 1 | **1** | 0 |
| `exitSteps_tree_6` | 3 | 2 | **1** (at `[8413,8437]`) |
| `exitSteps_tree_7` | 6 | 3 | **3** |
| `exitSteps_tree_8` | 10 | 4 | **6** |

### 5.3 What the parse really is

Re-parsed with only transport-verified TERM blocks:

```
k=5  Lean : 44 + TERM(3) + 76 + TERM(5)
     TI   : 44 + TERM(3) + 76 + TERM(5)                                    IDENTICAL

k=6  Lean : 83 + TERM(3) + 47 + REGEN(4) + 113 + TERM(3) + 122 + TERM(3) + 76 + TERM(6)
     TI   : 83 + TERM(3) + 47 + REGEN(4) + 259           + TERM(3) + 76 + TERM(6)

k=7  Lean : 170 + TERM(3) + 47 + REGEN(4) + 113 + TERM(3) + 78 + REGEN(5) + 113 + TERM(3)
            + 881 + TERM(3) + 47 + REGEN(4) + 113 + TERM(3) + 122 + TERM(3) + 76 + TERM(7)
     TI   : 170 + TERM(3) + 47 + REGEN(4) + 215 + REGEN(5) + 1018 + TERM(3)
            + 47 + REGEN(4) + 259 + TERM(3) + 76 + TERM(7)
```

The arithmetic of the fusions — each spurious TERM(3) had *manufactured two glue numbers out of one*:

```
113 + 24 + 122 = 259        113 + 24 + 78  = 215
113 + 24 + 881 = 1018       113 + 24 + 798 = 935        113 + 24 + 3944 = 4081
```

**So of §5z's `83/47/113/122/76`:** `83`, `47`, `76` are real glue segments; **`113` and `122` are
not** — they are the two halves of the single segment `259`, split by a comb pass mistaken for a
block flush. Likewise `78`, `798`, `3944`, and `881`.

### 5.4 `881` is not a level-7 object

§5z presents `881` as *"the level-dependent CORE `sweepEF` build-up in REGEN(7)"*. Two things are
wrong with that. First, `881` is not a segment at all — it is `1018` minus a spurious split. Second,
the TI-verified glue multisets show the real segment `1018` is **not level-7-specific**:

```
REGEN(5)  : [44, 76]
REGEN(6)  : [83, 47, 259, 76]
REGEN(7)  : [170, 47, 215, 1018, 47, 259, 76]
REGEN(8)  : [353, 47, 215, 935, 4081, 47, 215, 1018, 47, 259, 76]
REGEN(9)  : [728, 47, 215, 935, 3911, 16360, 47, 215, 935, 4081, 47, 215, 1018, 47, 259, 76]
REGEN(10) : [1487, 47, 215, 935, 3911, 16007, 65503, 47, 215, 935, 3911, 16360, ...,
             47, 215, 935, 4081, 47, 215, 1018, 47, 259, 76]
```

`1018` appears at k=7, 8, 9 **and** 10. (`881` appears in *no* TI-verified parse at any level, and
in Lean at both k=7 and k=8 — so it was never level-7-only even on the old reading.)

The multisets also expose a structure the greedy parse obscured: **REGEN(k)'s glue tail is exactly
REGEN(k−1)'s glue list**, with one new head segment and one new ascending run per level — the
`exitList(k) = range(4,k−1) ++ exitList(k−1)` shape, visible in the glue as well as the calls. That
is a cleaner statement of the growing-arity tree than §5z's numbers, and it is transport-verified.

---

## 6. What this means for `lean/X2.lean`

**Nothing in the Lean file is false, and nothing needs retracting.** Precisely:

- `exitSteps_tree_5/6/7/8` are pure `Nat` identities discharged by `decide`. They **cannot** be
  false, and their sums re-check. ✓
- Their **load-bearing content** — which strictly-lower `REGEN` calls occur, and how many — is
  transport-verified at every level. ✓
- `exitArity_grounds`, `exitArity_exceeds_four`, and the growing-arity `[DESIGN]` conclusion are
  **sound**, and `exitArity` now additionally checks out at k=9 and k=10. ✓
- What is **wrong is a docstring reading**: `exitSteps_tree_6/7/8`'s prose describes the trees as
  *"interleaved with `TERM(3)`s and glue"*, and §5z's narrative attributes meaning to `881`/`113`/
  `122`. Some of those `termSteps 3` terms are a *different* 24-step transport, and those glue
  numbers are parse residues, not orbit structure.

**Recommended (for the `lean/X2.lean` owner — this agent edited no Lean):** the `termSteps 3` terms
in `exitSteps_tree_6/7/8` are arithmetically fine but semantically over-claimed. Either re-state
those trees in the TI-verified form (§5.3), which is *shorter* and has *fewer* free numbers, or
weaken the docstrings to say the `24`s are anchor gaps of length `termSteps 3`, not TERM(3) blocks.
The REGEN calls and the arities need no change.

---

## 7. Method note — what generalizes

1. **The defect was never "length is a bad heuristic"; it was that a coincidence-prone test was
   used where an exact one was available at the same cost.** Word-identity is *equivalent* to the
   trace test here, and is a substring search. There was no reason to test by length.
2. **A grounding can be right for the wrong reason.** `k ≤ 8` survived because the false positives
   happen to live at k=7 *outside* the windows the trees parse, and because REGEN(8) does not call
   REGEN(7). That is luck. k=10 is where the luck runs out — and it would have run out as an
   apparent *refutation* of a correct Lean definition.
3. **The same defect recurs at every level of a hierarchy — audit all of them.** The REGEN audit was
   the reported one; the identical fault sat untouched one level down in the TERM blocks, and *that*
   is the one that actually corrupted the published numbers.
4. **Canonicity must come from the definition, not from convenience.** "Earliest window" happened to
   be right at every level, but nothing made it right. Reading the block off the tape does.

---

*Probes: `x2ti_tree.py`, `x2ti_parse.py`, `x2ti_term3.py`, `x2ti_canon.py`. All results
`[OBSERVED, exact, ON-PATH from build(2), 620k-step prefix]` except the Lean sums, which are
`[PROVEN]` in the file itself. No Lean file was edited.*

**No machine decided. No label upgraded.**
