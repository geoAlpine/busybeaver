# R3 + tail — MEASURED (2026-07-23)

Labels: `[MEASURED]` = reproduced on the real orbit with the bounds-checked wide-tape
instrument (`x2r2_sim.py`, anchors M1(1..3) exact). `[PREDICTED→CONFIRMED]` = stated
before the measurement that tested it. Nothing here is proven; no label is upgraded.

Anchors used (M1(4), M1(5) are NEW, first member of each milestone cluster):

| g | 1 | 2 | 3 | 4 | 5 |
|---|---|---|---|---|---|
| M1(g) | 188 099 | 732 733 | 2 852 091 | 11 329 301 | 44 986 995 |

---

## 1. `topEntry(g)` — the descent's ENTRY is PARITY-SPLIT `[MEASURED, 2 points each side]`

| g | parity | entry level | K(g)=g+8 | K−1 | M1(g) → entry | marker head after the comb |
|---|---|---|---|---|---|---|
| 1 | odd | `descIn 7` | 9 | 8 | 12 318 | `1^20` then `0010101010…` |
| 2 | even | `descIn 9` | 10 | 9 | 2 026 | `001001010100101010010101…` |
| 3 | odd | `descIn 9` | 11 | 10 | 48 904 | `1^20` then `0010101010…` |
| 4 | even | `descIn 11` | 12 | 11 | 6 740 | `001001010100101010010101…` |

- **even g: entry = `descIn (K−1)`.** Confirmed at g=2 and g=4.
- **odd g: entry = `descIn (K−2)`.** Confirmed at g=1 and g=3 — one level LOWER than
  the even family, and the whole approach costs ~6× more.
- **The comb is exact at every entry**: `(01)^{2^{k−1}}` — 64/256/256/1024 at k=7/9/9/11.
  `descIn` is the right cut; `headLaw` applies verbatim once the entry is reached.
- **The odd decoration is visible in the marker**: odd g's marker begins with a run of
  exactly **twenty 1s** at BOTH g=1 and g=3; even g's begins with the nested comb prefix
  `001001010100101010010101`, which extends by one layer from g=2 to g=4 (as the ladder
  nesting predicts). This is the same phenomenon that forced `h_low_even`/`h_low_odd`.

**Consequence for R3.** `topEntry` must be stated per parity, exactly as `h_low` was. The
even branch looks like the tractable one (uniform marker prefix, entry at `K−1`). No closed
form for the cost yet — 2 026 / 6 740 (even) and 12 318 / 48 904 (odd) are only two points
each. **R3 stays `[OPEN]`.**

---

## 2. `tail(g)` — the tail is a FRAME-DIGIT ODOMETER plus a fixed 110-step end `[MEASURED, 4 generations]`

The design doc recorded 211 / 184\* / 265 at g=2/3/4 with g=3 flagged "does not land
cleanly". The irregularity was **the cut, not the machine** (METHODS M2). At the right cut:

```
tail(g)  =  <entry: parity-dependent>  ∘  (g−1) × frameDigit(27 steps)  ∘  fixedEnd(110)
```

`frameDigit` count, measured: g=1 → **0**, g=2 → **1**, g=3 → **2**, g=4 → **3**. Count = `g−1`.

`[PREDICTED → CONFIRMED]` The `g−1` reading was stated from g=1,2,3 and then tested at
g=4 *before* looking: predicted 3 stages, measured exactly 3
(44 986 804 → 831 → 858 → 885, three `+27`s).

**`fixedEnd` is bit-for-bit the same at all four generations** — `+35, +6, +6, +6, +6, +51`
= 110 steps, with the identical comb progression 5→6→7→8→9 and the identical local shapes
`0^1 1^8 0^8 …` → `0^1 1^6 …` → `0^1 1^4 …` → `0^1 1^2 …` → `0^9 1^1 …` → `M1(g+1)`.

**The entry is where the parity lives:**

| g | ladder-top shape | into the odometer |
|---|---|---|
| 1 (odd) | `0^13 1^1021 0^2 1^509 …` — **not** a canonical `cascadeReg` | directly (`+35` to `fixedEnd`) |
| 2 (even) | `cascadeReg 11` = `0^3 1^2045 0^2 1^1021 …` | 74-step block chew, then `+29` to the `0^7 1^1` config |
| 3 (odd) | `0^13 1^4093 0^2 1^2045 …` — **not** a canonical `cascadeReg` | directly |
| 4 (even) | `cascadeReg 13`-shaped `0^3 1^8189 …` | block chew, then `+29` to `0^7 1^1` |

So **`ladderToCascade`'s OUT presents the tail's IN only at EVEN g.** At odd g the top
carries `0^13` where `cascadeReg` has `0^3` — ten extra zeros. That is why no
`cascadeReg 12` exists before M1(4): there is no canonical `cascadeReg` at odd g at all.

Totals at the uniform cut: `tail = 27(g−1) + 110`, i.e. 110 / 137 / 164 / 191 for g=1..4,
plus the parity-dependent entry (0 for odd; 74 + 29 = 103 for even at g=2 — hence the
recorded 211 = 103 + 27 + 110 ✓).

---

## 3. What this changes

- **The tail is no longer "no closed form".** It is an odometer over the milestone frame's
  digits (`0^21 1 0^6 1 0^6 1 …` — one `1` per generation) with a fixed ending. That is a
  `∀g` fold of the same species as `ladderFold`, and it should be provable by the same
  tile+fold+strong-induction toolkit (METHODS M3).
- **The parity split is now MEASURED at both ends of the phase** (entry level and marker at
  the head; ladder-top shape at the tail), with two data points on each side. It is the same
  odd decoration `h_low_odd` already handles.
- **R3 is the remaining unknown.** Both branches' costs lack a closed form. This is now the
  single largest open piece of `h_doub ∀g`.

## 4. Honest limits

- Two generations per parity class. The `g−1` frame-digit law has four points but the
  parity claims have two each; g=5 (M1(5) = 44 986 995 → M1(6)) is untested.
- The odd-g ladder top is characterised only by its RLE prefix; its Lean-level shape is
  not yet defined.
- The `+29` even-entry step and the 74-step chew at g=2 are measured at g=2 only in detail.
- No machine decided. No label upgraded. `x2` remains `[OPEN]`.
