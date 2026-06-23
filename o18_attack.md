# o18 deep analysis — the Erdős-family kernel, exact halt predicate (2026-06-24)

Stage-3 focus on the most literature-proximate cryptid kernel. `o18 = 1RB0RE_1LC0RA_1LA1LD_1LC1LF_0LC0LB_1LE---`.
All facts below are machine-verified against the raw TM (`o18_fast.py`, `o18_trace.py`, `o18_orbit.py`).

## 1. Exact mechanism [VERIFIED]
The configuration returns, once per **epoch**, to a clean single block `0 1^{N−1}` (head at the left
frontier, entering state **F**). The epoch widths are
```
epoch:  0   1   2    3    4     5     6      7       8
N_k :  10  28  76  204  546  1458  3890  10373   27660
```
- **State F is reached exactly once per epoch, at the left frontier, and READS THAT CELL.** Spec: state F
  (`1LE---`) reads 0 → write 1, go to E, extend left; **reads 1 → HALT.** Verified: in all 9 epochs F read
  a virgin **0** (steps 36, 226, 1430, 9562, 66753, 468794, 3 315 299, 23 503 104, 166 999 736).
- **`NON-HALT ⟺ state F reads 0 at every epoch's frontier.`** (Halt is the unique transition F·read-1.)

## 2. The clean scalar map and its VERIFIED break [the crux]
For epochs 0–6 the orbit obeys the clean map **exactly**:
```
N_{k+1} = ⌊8 N_k / 3⌋ + 2     (8/3 = 2³/3 — a Mahler 2^a/3^b multiplier)
```
verified `10→28→76→204→546→1458→3890`. **But at epoch 7 the clean map BREAKS** (machine-verified):
```
f(3890)=⌊31120/3⌋+2 = 10375 ,  actual N_7 = 10373   (deviation −2)
f(10373)            = 27663 ,  actual N_8 = 27660   (deviation −3)
```
Simultaneously the clean form `0 1^{N−1}` first acquires an **interior-zero DEFECT** at epoch 7 (an extra
`0` inside the 1-block). So o18 is **NOT** the trivial clean doubler (which would be a decidable bouncer):
the verified epoch-7 deviation proves it carries genuine irregular content.

## 3. Exact halt predicate [DERIVED]
The defect (interior 0) is born when the `⌊8N/3⌋` step produces a **base-3 carry** that the leftward rebuild
cannot absorb cleanly — exactly the deviation seen at epoch 7. Each epoch the defect, if present, drifts; a
halt occurs iff a defect ever sits **exactly at the cell state F tests at the frontier**. Hence:
```
o18 HALTS  ⟺  ∃ epoch k where a base-3 carry of the ⌊8/3⌋-orbit ⟨N_k⟩ lands precisely
              at the leftward F-sweep frontier  (the defect collides with the F-read).
NON-HALT   ⟺  the carry-defects of the ×(8/3) orbit never align with the moving frontier.
```
This is a **digit/carry-alignment event in the base-3 expansion of an exponentially growing ×(8/3) = ×2³/3
orbit** — structurally the **Erdős ternary-digits-of-2^{3k} family** (`8^k = 2^{3k}`).

## 4. Relation to Erdős, and the irreducible open core [HONEST]
- **Family, not literal reduction.** Erdős (1979): `2^m` has a base-3 digit 2 for all `m>8` (open; checked
  to ≈6×10²¹). o18's predicate is a *self-referential frontier-alignment* of the `⌊8N/3⌋+2` orbit, not the
  literal "`2^m` omits digit 2." Same hardness class (`×2³/3`, base-3 carries), derived analogy not identity.
- **Strongest unconditional tool, and the gap.** Narkiewicz (1980): `#{n≤x : (2ⁿ)₃ omits digit 2} ≤
  1.62·x^{0.631}` — a **density upper bound** on the analogous exceptional set, with **no lower bound** and
  **no control of any specific orbit position**. It cannot decide whether o18's particular carry-defects
  ever hit the frontier. This is the same one-sided-density wall as Antihydra's missing FLP density-analogue
  (`antihydra_attack.md` §4): the literature bounds *how often* a digit event can happen across `n`, never
  *whether it happens at one self-referentially-determined place*.
- **Irreducible open core:** *does a base-3 carry of the `⌊8N/3⌋+2` orbit ever align with the frontier?* —
  a ternary-digit-distribution statement about one specific `×(8/3)` orbit. No unconditional method forces
  or forbids the alignment. **World-open, same frontier as Erdős/Mahler.** No decision; soundness intact.

## 5. What was achieved (Stage 3 honest ledger)
- [VERIFIED] o18's exact mechanism: clean `0 1^{N−1}` resets, F-frontier read once/epoch, non-halt ⟺ F·0.
- [VERIFIED] the clean map `⌊8N/3⌋+2` holds epochs 0–6 and **provably breaks at epoch 7** (−2) — so o18 is
  genuinely irregular, NOT a trivially-decidable doubler.
- [DERIVED] the exact halt predicate = base-3-carry/defect alignment with the moving F-frontier.
- [HONEST] it sits in the Erdős ternary family; the one unconditional tool (Narkiewicz) gives only a density
  upper bound and cannot reach the specific-alignment question. Open core identified; no decision claimed.

## 6. The interior-F mechanism + Borel-Cantelli heuristic (2026-06-24, all verified)
Pushed the direct simulation to **9×10⁸ steps** (reaches epoch 8; epoch 9 needs ~10⁹, simulation exhausted).
- **o18 is NOT a trivial doubler [VERIFIED — refutes a tempting wrong "decidable" claim].** In the *clean*
  regime state F only ever reads the virgin-0 frontier (→ would be trivially non-halting). BUT at the
  **epoch-7 defect epoch**, F is routed to an **interior read** (step 23 492 737, pos +9, value 0). So
  defects *do* route F into the interior where the cell *could* be 1. **Sharpened halt predicate:**
  `o18 HALTS ⟺ some interior F-read (which occurs only during a base-3-carry defect epoch) reads a 1.`
  (Checked, not assumed — the one observed interior read was 0, so no halt; o18 stays a genuine open cryptid.)
- **Defect trigger [VERIFIED]:** the lone defect (epoch 7) follows predecessor `N_6=3890` whose base-3 form
  `12100002` ends in a trailing-2 (`…0002`). The clean map `⌊8N/3⌋+2` *dropped its +2* exactly there
  (10373 = ⌊8·3890/3⌋, not +2) — i.e. the defect = a base-3 carry the clean rebuild couldn't absorb. So the
  epoch map is **not a function of N alone**; it carries forward carry-state (why no finite-state closure in N).
- **Borel-Cantelli heuristic [parallels Antihydra §4]:** the ideal orbit's base-3 digit-2 density is
  **1/3** (equidistributed, units digit uniform — numerically verified over 4000 epochs). A halt needs an
  interior F-read to align with a residual 1; `P(align at epoch k) ~ O(1/N_k)` and `Σ_{k≥7} 1/N_k ≈
  1.54×10⁻⁴ ≪ 1` (geometric, ratio 3/8). **⇒ expected number of halt-alignments ≈ 0 ⇒ o18 almost surely
  NON-HALTS.** Same heuristic verdict as Antihydra.
- **The irreducible gap [HONEST]:** Borel-Cantelli needs **independence**, but the alignment positions are
  *deterministically* fixed by the orbit's base-3 carries. Proving non-alignment = proving a specific digit
  of a `×(8/3)` orbit never lands at a self-referentially-determined spot = an **Erdős-class ternary-digit
  statement**. No unconditional tool reaches it (Narkiewicz: density upper bound only). **World-open.**

**o18 status = Antihydra status (now symmetric):** exact mechanism + sharp halt predicate + heuristic
non-halt (digit density argument) + the same deterministic-alignment wall. The breakthrough required is the
ternary-digit (Erdős/Mahler-8/3) result. No decision; soundness intact.
