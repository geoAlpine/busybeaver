# The integer-×2 base-2 odometer — decidability attempt (2026-07-10)

*First actual DECISION attempt on the cleanest integer-×2 candidate of the frontier:
`M = 1RB0RE_1RC---_0LD1LE_0RE1LD_1RF0LC_0RA1RE` (the `maxrun v'=2v+2` machine of
`CANDIDATE_NEW_INVESTIGATION_2026-07-10.md §1a`, flagged there as the strongest
decidability candidate, `[DECIDABLE-candidate/OPEN]`). Interpreter
`/Users/aokiyousuke/quantum-ecc/.venv/bin/python`, exact bytearray/int. Scripts:
`x2_trace.py`, `x2_local.py`, `x2_scan.py`, `x2_hist.py`, `x2_left.py`, `x2_block.py`,
`x2_transform.py`, `x2_control.py`, `x2_invariant.py`. SOUNDNESS: labels
`[PROVEN-from-table]`/`[OBSERVED]`; ZERO false proofs. Not committed.*

## 0. Verdict (headline)

**The reset-structure dichotomy is RESOLVED to the DECIDABLE side, and the halt condition
is reduced to an exact LOCAL geometric event — but a certified non-halt is NOT claimed.**

- `[PROVEN-from-table]` **Halt characterization.** `HALT ⟺ the rightward E-scanner enters
  a maximal 0-run of length EXACTLY 3` (the pattern `1 0 0 0 1`, read from the left `0` in
  state E). Positive+negative control: gap `0^L` for `L=1..6` halts **iff `L=3`**
  (`x2_control.py`).
- `[PROVEN-from-table]` **The macro-machine routes on PARITY only.** Every block-crossing
  rule (head traversing a `1^n` block) has an exit-state/side that depends **only on the
  parity of `n`**, uniform in `n` otherwise (`x2_block.py`, `n=5..31`). The head is a
  **finite-state controller over block-length parities** — a *bounded* amount of information
  per block. This is the DECIDABLE side of the task's dichotomy, and the exact structural
  OPPOSITE of o7 (oddpart/2^k couples to deep bits, reachable set fills ℤ/m) and Space
  Needle (`f` mixes all bits, **no** finite-state abstraction).
- `[OBSERVED, exact, to 3·10⁸ steps / 22,668 halt-gate exposures, 0 counterexamples]` No
  length-3 gap ever forms; state B (the halt gate) is entered 22,668× and **reads 0 every time**; the
  scanner only ever meets 0-runs of length 1, 2, or **even ≥4** (never odd ≥3).

**The machine is a finite-state-controlled base-2 (doubling) odometer — a "bouncer",
squarely in a decidable species — and is non-halt-leaning with overwhelming, exact
evidence. The one lemma that would upgrade this to a certified DECISION (`no odd 0-run of
length ≥3 is ever scanned`, equivalently the packed macro-machine closure) is reduced to a
single clean statement and structurally explained, but not formally closed here.** So:
**`[DECIDABLE-class; non-halt to 3·10⁸; NOT certified-decided]`.**

## 1. The machine and the halt gate `[PROVEN-from-table]`

Transitions (`ABCDEF` × `{0,1}`):
```
A: 0->1RB  1->0RE      D: 0->0RE  1->1LD
B: 0->1RC  1->---      E: 0->1RF  1->0LC
C: 0->0LD  1->1LE      F: 0->0RA  1->1RE
```
The only halt is **`B` reads `1`**. `B` is entered ONLY from `A(0)->1RB`; `A` is entered
ONLY from `F(0)->0RA`; `F` is entered ONLY from `E(0)->1RF`. Chaining the entry conditions
gives a rightward 4-cell read window: positions `e,e+1,e+2,e+3` are read by `E,F,A,B`, and
the branch conditions force
```
tape[e]=0 (E->F),  tape[e+1]=0 (F->A),  tape[e+2]=0 (A->B),  HALT ⟺ tape[e+3]=1.
```
i.e. **`HALT ⟺ the E-scanner, aligned at the left `0` of a maximal 0-run, finds that run
has length exactly 3** (`0001`; length ≥4 ⟹ B reads 0 ⟹ turns around via C; length 1 or 2 ⟹
the scan turns before reaching B).

**Control `x2_control.py`:** planting a maximal 0-run of length `L` in the scanner's path,
`L=1,2,4,5,6 → escape (no halt)`, `L=3 → HALT in 3 steps`. Exact, matches the derivation. ∎

## 2. The tape is a base-2 odometer; 0-runs live in {1,2} `[OBSERVED, exact]`

At any rest milestone the tape is `0^∞ [1-blocks] 0^∞` with the 1-blocks the nested cascade
`1^(2^k−2) 0 1^(2^{k−1}−2) 0 …` (block `+2 = 2^k`); the super-peak `maxrun` doubles cleanly
`6,14,30,62,126,254,510,1022,2046,4094 = 2^k−2` with `steps ∝ value²` (value-×2 engine)
(`x2_macro.py`, `x2_reset.py`). Full run-length histograms across the whole tape
(`x2_hist.py`, steps 10⁶…6·10⁷):
- **0-run lengths: only `{1,2}`** — thousands of single `0` separators + a handful of `00`
  carry-markers. **Length 3 NEVER appears** (0 occurrences in every global scan).
- 1-run lengths: `1` (the low comb) plus one each of the cascade blocks `2^k−3`.

The `00` markers are the **carry digits** of the base-2 cascade; the low `1 0 1 0 1 0…` comb
is the counter's low part, which *repacks* (doubles) into the next cascade block. Block
crossings **unpack** a block into a comb and **repack** combs into blocks (`x2_transform.py`)
— the doubling mechanism.

## 3. The reset-structure dichotomy — RESOLVED to BOUNDED (decidable) `[PROVEN-from-table]`

The task's crux: does the reset/carry depend on a **bounded** amount of state (⟹ finite-state
odometer ⟹ decidable) or on **deep/unbounded bits** (⟹ (K)-base-2)?

**Answer: BOUNDED.** The full block-crossing table (`x2_block.py`, isolated `1^n`,
`n=5,6,7,8,15,16,30,31`) shows the head's exit state/side is a function of **`n mod 2`
alone**, uniform in `n`:

| enter | exit (n even) | exit (n odd) |
|---|---|---|
| B from R | B / R | F / R |
| C from R | A / R | C / R |
| D from L | A / R | C / R |
| F from L | C / R | A / R |
| A/R, B/L, C/L, D/R, E/L, E/R, F/R | (n-independent) | (same) |

So the macro-machine is a **finite-state transducer over the string of block-parities and
{0,00} gaps** — the head carries only a bounded look-back (its state + the parity of the
block it is crossing). No `oddpart`, no `⌊·/2^{v+1}⌋`, no bit-mixing: **a finite-state
abstraction EXISTS.** This is exactly the property o7 and Space Needle were PROVEN to
*lack* (`O7_DECISION_ATTEMPT`, `SPACENEEDLE_DECISION_ATTEMPT`: no mod-`M` or
bounded-parity-look-ahead automaton over-approximates their reachable set). The integer ×2
(q=1, a clean binary SHIFT that does **not** mix bits) delivers the finite-state control the
×3/2 machines cannot have.

## 4. Reduction of non-halt to one clean invariant `[the remaining lemma]`

By §1, `HALT ⟺ a maximal 0-run of length exactly 3 is scanned`. By §2–3 the only 0-runs
that ever occur are (a) stable gaps of length 1 or 2, and (b) **transient even runs ≥4** the
head momentarily opens while unpacking a block. Direct instrumentation of the halt gate
(`x2_scan.py`, to 3·10⁸ steps): **every** state-B visit sits inside a run of even length ≥4
(the count of further 0s past B is always odd ⟹ total run even), so B always reads 0.

> **Lemma (unproven-here, the whole content of a DECISION):** the E-scanner never enters a
> maximal 0-run of **odd length ≥3**. Equivalently, odd 0-runs always have length 1.

Given the finite-state parity control (§3) this is a *finite-state reachability* statement
over the packed block/gap alphabet — decidable in principle and the exact object a
bouncer/CTL decider would close. It holds with **0 counterexamples to 3·10⁸ steps**, and the
parity routing makes it structurally natural (transient runs inherit the crossed block's
even parity). But it is **not formally closed** in this session (the packed macro-machine
with context-correct block transformations was not built to closure), so **no certified
non-halt is claimed.**

## 5. Contrast with the (K)/×3/2 wall — why this one is different

| | this ×2 machine | o7 (×3/2) / Space Needle (×5/2) |
|---|---|---|
| multiplier | integer 2 (q=1), clean binary shift | p/q, q>1 (2-adic unit denom) |
| bit behavior | **does not mix bits** | `oddpart` / `⌊m/2^{v+1}⌋` mixes ALL bits |
| finite-state abstraction | **EXISTS** (parity routing) | PROVEN not to exist |
| halt condition | local geometric event (length-3 gap) | thin-set 2^k / all-ones cylinder, deep-bit |
| reachable residues mod M | (finite-state) | fill ℤ/m (equidistribute) |
| verdict | **decidable-class, non-halt-leaning** | genuine 2-adic reachability wall, `[OPEN]` |

This confirms and sharpens the CNI note: the integer-×2 species sits **outside** the
(K)/Mahler ×p/q-normality wall, and — unlike the note's cautious "could still be
(K)-base-2" — the parity-routing result shows it is **not** (K)-like: its control is
genuinely finite-state. It is the frontier's **best decidability candidate**, now with the
dichotomy resolved and only a bounded-state closure lemma between here and a first decision.

## 6. Soundness ledger
- Halt characterization: `[PROVEN-from-table]` by entry-condition chaining + positive/negative
  control `x2_control.py` (L=3 ⟺ halt, exhaustive L=1..6).
- Parity-only routing: `[PROVEN-from-table]`, `x2_block.py`, all 12 (state,side) × parities,
  `n` up to 31, uniform.
- 0-runs∈{1,2}, no length-3, B reads 0 always: `[OBSERVED exact]`, `x2_hist.py` /
  `x2_scan.py` / `x2_trace.py`, to 3·10⁸ steps, 22,668 halt-gate exposures, 0 counterexamples.
- The non-halt LEMMA (§4) is **not** proven; it is not used as a machine claim.

**No machine decided. No label upgraded.**
