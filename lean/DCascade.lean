import DMachine

set_option maxRecDepth 4000000
set_option maxHeartbeats 1000000

/-!
# `D`'s milestone word family, in Lean

The four laws of `RungCalc` (`tile`, `tile2`, `rung0`, `descend`) chain over 99.98% of `D`'s
epochs (`d_rf4_epochs.py`, epochs `k = 4` and `k = 5`).  What they do **not** give is the epoch
itself: chaining them needs each law's *output* configuration to be the next law's *input* on the
real tape, and that is a statement about `D`'s cascade word.  So the word family has to exist in
Lean before the seam induction can be attempted.  This file is that prerequisite, and nothing
more.

## What is pinned here

`D_SPEC_2026-07-26.md` §2 gives the family in closed form and calls it `[MEASURED, k = 4..9]`.
Per this project's discipline that claim was **re-derived from the raw orbit** before being
encoded (`d_cascade_measure.py`), which confirmed, for every `k = 4..9`:

* the milestone time and position (`t = 291168, 1196412, 4846662, 19488198, 78148404, 312959448`
  at `pos = −8k`), state `A`, head cell `0`, and **the entire left side blank**;
* the explicit right words of §2's table;
* the closed forms `a(k) = 39·2^{k−1} − 4`, `G(k) = 57·2^{k−3} − 3k + 9`,
  `w(k) = 117·2^{k−1} + 3k − 55`;
* the block construction (`§5` of the instrument) reproducing every milestone `k ≥ 4`.

**One correction to `D_SPEC` §2.**  Its prefix-stability sentence says `M1(k) → M1(k+2)` appends
"two new blocks".  It appends **one**: keep every block but the last, rewrite the last
`(G(k), a(k)) → (33·2^{k−3}+12, 66·2^{k−2})`, then append a single `(G(k+2), a(k+2))`.  Measured
for `k = 4,5,6,7` (`d_cascade_measure.py §4`).

## What this file does NOT do

It defines the word and pins it against the measurement.  It does **not** prove
`steps dT (T(k+1) − T(k)) (M1 k) = some (M1 (k+1))` — that is the seam induction, still open, and
stated below only as a `Prop` (this project's `[DESIGN]` idiom), never as a `sorry`.
`D` remains `[OPEN]`.

Zero-Mathlib, core only.  No `sorry`, no `native_decide`.
-/

namespace DCascade

open TapeCalc RungCalc DMachine

/-! ## §1 Blocks and closed forms. -/

/-- One cascade block, in tape order: a `0`-gap then a `(1 0)`-comb. -/
def block (g a : Nat) : List Bool := zeros g ++ pow10 a

/-- The last comb's length, `a(k) = 39·2^{k−1} − 4`, indexed by `j` with `k = j + 4` so the
exponent needs no truncated subtraction. -/
def aLast (j : Nat) : Nat := 39 * 2 ^ (j + 3) - 4

/-- The gap before the last comb, `G(k) = 57·2^{k−3} − 3k + 9`, at `k = j + 4`. -/
def gLast (j : Nat) : Nat := 57 * 2 ^ (j + 1) - 3 * j - 3

/-- A middle block, by its exponent `e = k − 2j`.  `e = 0` and `e = 1` are the two bottoms; from
`e ≥ 2` the shape is uniform. -/
def blockE (e : Nat) : List Bool :=
  match e with
  | 0 => block 33 66
  | 1 => block 60 132
  | e + 2 => block (33 * 2 ^ (e + 1) + 12) (66 * 2 ^ (e + 2))

/-- The middle blocks for parity `p ∈ {0,1}`: `n` of them, at exponents `p, p+2, …, p+2(n−1)`,
in tape order (the `D_SPEC` loop runs `j = jmax … 2`, i.e. `e` increasing). -/
def midBlocks (p : Nat) : Nat → List Bool
  | 0 => []
  | n + 1 => midBlocks p n ++ blockE (p + 2 * n)

/-- **`D`'s milestone word** — everything right of the head at `M1(k)`, `k ≥ 4`.
Written `Dcascade j` with `k = j + 4`. -/
def Dcascade (j : Nat) : List Bool :=
  (if (j + 4) % 2 = 1 then block 2 4 ++ block 5 15 else [])
    ++ midBlocks ((j + 4) % 2) ((j + 4) / 2 - 1)
    ++ block (gLast j) (aLast j)
    ++ [true]

/-- The milestone configuration.  The left field is literally `[]` — a genuine structural fact
(`M1(k)` is a *fresh left-frontier record*), re-measured for `k = 4..9`. -/
def M1 (j : Nat) : Cfg St := ⟨.A, -8 * ((j : Int) + 4), ⟨[], false, Dcascade j⟩⟩

/-! ## §2 The definition, pinned against the measured words.

Each of these is a closed `rfl` against the block decomposition measured from the raw orbit
(`d_cascade_measure.py §2`, which re-derived `D_SPEC` §2's table rather than trusting it).  If
the recursion in §1 drifted, these would stop holding. -/

/-- `k = 4`: `0^33 (10)^66 0^111 (10)^308 1`. -/
theorem cascade4 :
    Dcascade 0 = zeros 33 ++ pow10 66 ++ zeros 111 ++ pow10 308 ++ [true] := by rfl

/-- `k = 5`: `0^2 (10)^4 0^5 (10)^15 0^60 (10)^132 0^222 (10)^620 1`. -/
theorem cascade5 :
    Dcascade 1 = zeros 2 ++ pow10 4 ++ zeros 5 ++ pow10 15 ++ zeros 60 ++ pow10 132
                 ++ zeros 222 ++ pow10 620 ++ [true] := by rfl

/-- `k = 6`: `0^33 (10)^66 0^78 (10)^264 0^447 (10)^1244 1`. -/
theorem cascade6 :
    Dcascade 2 = zeros 33 ++ pow10 66 ++ zeros 78 ++ pow10 264 ++ zeros 447 ++ pow10 1244
                 ++ [true] := by rfl

/-- `k = 7`: `0^2 (10)^4 0^5 (10)^15 0^60 (10)^132 0^144 (10)^528 0^900 (10)^2492 1`. -/
theorem cascade7 :
    Dcascade 3 = zeros 2 ++ pow10 4 ++ zeros 5 ++ pow10 15 ++ zeros 60 ++ pow10 132
                 ++ zeros 144 ++ pow10 528 ++ zeros 900 ++ pow10 2492 ++ [true] := by rfl

/-- `k = 8`: `0^33 (10)^66 0^78 (10)^264 0^276 (10)^1056 0^1809 (10)^4988 1`. -/
theorem cascade8 :
    Dcascade 4 = zeros 33 ++ pow10 66 ++ zeros 78 ++ pow10 264 ++ zeros 276 ++ pow10 1056
                 ++ zeros 1809 ++ pow10 4988 ++ [true] := by rfl

/-- `k = 9`: the six-block word. -/
theorem cascade9 :
    Dcascade 5 = zeros 2 ++ pow10 4 ++ zeros 5 ++ pow10 15 ++ zeros 60 ++ pow10 132
                 ++ zeros 144 ++ pow10 528 ++ zeros 540 ++ pow10 2112
                 ++ zeros 3630 ++ pow10 9980 ++ [true] := by rfl

/-! ### §2.1 Widths — an independent check of the same definition.

`w(k) = 117·2^{k−1} + 3k − 55`, measured as the exact length of the right word. -/

theorem width4 : (Dcascade 0).length = 893 := by rfl
theorem width5 : (Dcascade 1).length = 1832 := by rfl
theorem width6 : (Dcascade 2).length = 3707 := by rfl
theorem width7 : (Dcascade 3).length = 7454 := by rfl
theorem width8 : (Dcascade 4).length = 14945 := by rfl
theorem width9 : (Dcascade 5).length = 29924 := by rfl

/-- The closed forms themselves, at the measured levels. -/
theorem lasts :
    (aLast 0, gLast 0) = (308, 111) ∧ (aLast 1, gLast 1) = (620, 222)
      ∧ (aLast 2, gLast 2) = (1244, 447) ∧ (aLast 3, gLast 3) = (2492, 900)
      ∧ (aLast 4, gLast 4) = (4988, 1809) ∧ (aLast 5, gLast 5) = (9980, 3630) := by
  refine ⟨rfl, rfl, rfl, rfl, rfl, rfl⟩

/-! ## §3 Prefix stability, as measured.

`D_SPEC` §2 says `M1(k) → M1(k+2)` keeps every block but the last, rewrites that one, and appends
**two** new blocks.  The measurement says **one** (`d_cascade_measure.py §4`, `k = 4,5,6,7`).
Here is the corrected statement at the measured levels, as `rfl` on the words. -/

/-- `k = 4 → 6`: the `(33,66)` prefix survives, `(111,308)` is rewritten to `(78,264)`, and a
single new block `(447,1244)` is appended. -/
theorem prefix46 :
    Dcascade 2 = zeros 33 ++ pow10 66 ++ (zeros 78 ++ pow10 264) ++ (zeros 447 ++ pow10 1244)
                 ++ [true] := by rfl

/-- `k = 5 → 7`: the three-block prefix survives, `(222,620)` becomes `(144,528)`, one new block
`(900,2492)` is appended. -/
theorem prefix57 :
    Dcascade 3 = (zeros 2 ++ pow10 4 ++ zeros 5 ++ pow10 15 ++ zeros 60 ++ pow10 132)
                 ++ (zeros 144 ++ pow10 528) ++ (zeros 900 ++ pow10 2492) ++ [true] := by rfl

/-! ## §4 The epoch obligation — stated, NOT proven.

This is the seam induction.  It is the honest remaining gap for `D`: the four `RungCalc` laws
account for 99.98% of an epoch's steps, but chaining them into `M1(j) → M1(j+1)` requires each
law's output configuration to be the next one's input *on this word*, which is exactly what is
unproven.  Stated as a `def … : Prop` with the measured step counts, never as a `sorry`, so
nothing here can leak into an axiom audit. -/

/-- Measured epoch spans `T(k+1) − T(k)` for `k = 4..8`, from the milestone times
`291168, 1196412, 4846662, 19488198, 78148404, 312959448`.  A **data table**, not a closed form:
no closed form for the span is measured beyond `k = 8`, which is exactly why `EpochLaw` below is
stated existentially rather than with this function. -/
def epochSpan : Nat → Nat
  | 0 => 905244
  | 1 => 3650250
  | 2 => 14641536
  | 3 => 58660206
  | 4 => 234811044
  | _ + 5 => 0

/-- **The epoch law — `[MEASURED for k = 4..8; NOT PROVEN]`.**

Stated existentially, and deliberately so.  An earlier revision of this file wrote it as
`∀ j, steps dT (epochSpan j) (M1 j) = some (M1 (j+1))`, which is **false**: `epochSpan` is a
five-entry measured table and returns `0` for `j ≥ 5`, so that statement asserted
`M1 j = M1 (j+1)`.  The existential form is also exactly the shape
`TapeCalc.nonhalt_of_invariant` consumes — see `lean/DReduce.lean`, where `D`'s non-halting is
reduced to this single obligation. -/
def EpochLaw : Prop := ∀ j, ∃ n, 1 ≤ n ∧ steps dT n (M1 j) = some (M1 (j + 1))

/-- Anti-vacuity for the *statement*: the spans really are the measured differences. -/
theorem epochSpan_measured :
    epochSpan 0 = 1196412 - 291168 ∧ epochSpan 1 = 4846662 - 1196412
      ∧ epochSpan 2 = 19488198 - 4846662 ∧ epochSpan 3 = 78148404 - 19488198
      ∧ epochSpan 4 = 312959448 - 78148404 := by
  refine ⟨rfl, rfl, rfl, rfl, rfl⟩

-- AXIOM AUDIT
#print axioms cascade4
#print axioms cascade9
#print axioms width9
#print axioms prefix46
#print axioms epochSpan_measured

end DCascade
