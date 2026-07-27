import DCascade
import TapeExt

set_option maxRecDepth 40000000
set_option maxHeartbeats 4000000

/-!
# The epoch's opening move, `∀`-uniform in the tail

`DCascade.EpochLaw` is `D`'s single open obligation (`lean/DReduce.lean`).  This file proves the
first stretch of it, and — unlike everything before it — for **every** `j`, not at measured levels.

## The structural fact this rests on

An epoch's behaviour from `M1(j)` is a function of the cascade word's **prefix**, and nothing
else.  Measured: two epochs of the same parity run **identically — same itinerary and same head
trajectory — until the head first reaches a cell where their cascade words differ**:

| pair | words share | diverge at step | head then at |
|---|---:|---:|---:|
| `k=4` vs `k=6` | 243 cells | 13221 | `+245` |
| `k=5` vs `k=7` | 513 cells | 50141 | `+515` |
| `k=6` vs `k=8` | 1047 cells | 185421 | `+1049` |

So the epoch decomposes along the cascade word, and the induction for `EpochLaw` should run
`k → k+2` over the **prefix**, with tail-independence supplied by `TapeCalc.steps_rext`.

## How these are proven

Not by `rfl` on a symbolic tail — measured, a 2000-step `rfl` with a free `X` does not finish in
ten minutes, and a symbolic `p` makes the kernel accumulate one `± 1` per step in the position.
Instead: run on the **concrete** prefix at `p = 0` (fast), then

* `TapeCalc.steps_rext` to extend the right context by an arbitrary `X` — legitimate because the
  run ends with the head on the prefix's last cell and an empty right list, so the frontier
  `right.length + pos` is unchanged and the run provably never read past the prefix;
* `TapeCalc.steps_pos_shift` to move it to any `p`.

Both openings are **maximal**: one more step reads the first cell beyond the prefix.

`D` remains `[OPEN]`.  Zero-Mathlib, core only.  No `sorry`, no `native_decide`.
-/

namespace DOpening

open TapeCalc RungCalc DMachine DCascade

/-! ## §1 Even `k`. -/

/-- The 243-cell prefix shared by every even-`k` cascade word. -/
def evenPre : List Bool := zeros 33 ++ pow10 66 ++ zeros 78

/-- The left deposit the even opening leaves behind. -/
def evenOut : List Bool :=
  pow10 51 ++ ones 2 ++ zeros 1 ++ pow10 39 ++ zeros 1 ++ ones 27 ++ zeros 1
    ++ pow10 9 ++ ones 2 ++ zeros 1 ++ pow10 1 ++ zeros 1 ++ ones 7 ++ zeros 1
    ++ ones 2 ++ zeros 2 ++ ones 2

theorem evenPre_length : evenPre.length = 243 := by rfl

/-- The concrete even run: 13219 steps, ending on the prefix's **last** cell with an empty right
list — so the frontier never advanced and the run never read past the prefix. -/
theorem openEvenCore :
    steps dT 13219 ⟨.A, 0, ⟨[], false, evenPre⟩⟩ = some ⟨.C, 243, ⟨evenOut, true, []⟩⟩ := by rfl

/-- **Even-`k` opening**, `∀ p X`. -/
theorem openEven (p : Int) (X : List Bool) :
    steps dT 13219 ⟨.A, p, ⟨[], false, evenPre ++ X⟩⟩
      = some ⟨.C, p + 243, ⟨evenOut, true, X⟩⟩ := by
  have hx := steps_rext dT 13219 .A 0 [] false evenPre X openEvenCore
    (by rw [evenPre_length]; rfl)
  rw [show ([] : List Bool) ++ X = X from rfl] at hx
  have h := steps_pos_shift (d := p) hx
  rw [show (0 : Int) + p = p from by omega, show (243 : Int) + p = p + 243 from by omega] at h
  exact h

/-! ## §2 Odd `k`. -/

/-- The 513-cell prefix shared by every odd-`k` cascade word. -/
def oddPre : List Bool :=
  zeros 2 ++ pow10 4 ++ zeros 5 ++ pow10 15 ++ zeros 60 ++ pow10 132 ++ zeros 144

def oddOut : List Bool :=
  pow10 95 ++ ones 2 ++ zeros 1 ++ pow10 83 ++ zeros 1 ++ ones 49 ++ zeros 1
    ++ pow10 28 ++ ones 2 ++ zeros 1 ++ pow10 17 ++ zeros 1 ++ ones 16

theorem oddPre_length : oddPre.length = 513 := by rfl

theorem openOddCore :
    steps dT 50139 ⟨.A, 0, ⟨[], false, oddPre⟩⟩ = some ⟨.C, 513, ⟨oddOut, true, []⟩⟩ := by rfl

/-- **Odd-`k` opening**, `∀ p X`. -/
theorem openOdd (p : Int) (X : List Bool) :
    steps dT 50139 ⟨.A, p, ⟨[], false, oddPre ++ X⟩⟩
      = some ⟨.C, p + 513, ⟨oddOut, true, X⟩⟩ := by
  have hx := steps_rext dT 50139 .A 0 [] false oddPre X openOddCore
    (by rw [oddPre_length]; rfl)
  rw [show ([] : List Bool) ++ X = X from rfl] at hx
  have h := steps_pos_shift (d := p) hx
  rw [show (0 : Int) + p = p from by omega, show (513 : Int) + p = p + 513 from by omega] at h
  exact h

/-! ## §3 The prefixes really are prefixes of `Dcascade`.

At the measured levels, by `rfl`.  The `∀ j` version needs an "unfold `midBlocks` from the front"
lemma (the definition recurses on its *last* block), which is the next step. -/

theorem prefix_even_0 : Dcascade 0 = evenPre ++ (zeros 33 ++ pow10 308 ++ [true]) := by rfl
theorem prefix_even_2 :
    Dcascade 2 = evenPre ++ (pow10 264 ++ zeros 447 ++ pow10 1244 ++ [true]) := by rfl
theorem prefix_even_4 :
    Dcascade 4 = evenPre ++ (pow10 264 ++ zeros 276 ++ pow10 1056 ++ zeros 1809 ++ pow10 4988
                              ++ [true]) := by rfl
theorem prefix_odd_1 : Dcascade 1 = oddPre ++ (zeros 78 ++ pow10 620 ++ [true]) := by rfl
theorem prefix_odd_3 :
    Dcascade 3 = oddPre ++ (pow10 528 ++ zeros 900 ++ pow10 2492 ++ [true]) := by rfl
theorem prefix_odd_5 :
    Dcascade 5 = oddPre ++ (pow10 528 ++ zeros 540 ++ pow10 2112 ++ zeros 3630 ++ pow10 9980
                              ++ [true]) := by rfl

/-! ## §4 The openings on the real milestones. -/

theorem open_M1_0 :
    steps dT 13219 (M1 0)
      = some ⟨.C, -32 + 243, ⟨evenOut, true, zeros 33 ++ pow10 308 ++ [true]⟩⟩ := by
  show steps dT 13219 (⟨.A, -32, ⟨[], false, Dcascade 0⟩⟩ : Cfg St) = _
  rw [prefix_even_0]
  exact openEven (-32) _

theorem open_M1_1 :
    steps dT 50139 (M1 1)
      = some ⟨.C, -40 + 513, ⟨oddOut, true, zeros 78 ++ pow10 620 ++ [true]⟩⟩ := by
  show steps dT 50139 (⟨.A, -40, ⟨[], false, Dcascade 1⟩⟩ : Cfg St) = _
  rw [prefix_odd_1]
  exact openOdd (-40) _

/-- The same opening fires at `k = 8`, whose epoch is 234,811,044 steps and which no `rfl` could
reach.  This is what tail-uniformity buys. -/
theorem open_M1_4 :
    steps dT 13219 (M1 4)
      = some ⟨.C, -64 + 243, ⟨evenOut, true,
          pow10 264 ++ zeros 276 ++ pow10 1056 ++ zeros 1809 ++ pow10 4988 ++ [true]⟩⟩ := by
  show steps dT 13219 (⟨.A, -64, ⟨[], false, Dcascade 4⟩⟩ : Cfg St) = _
  rw [prefix_even_4]
  exact openEven (-64) _

-- AXIOM AUDIT
#print axioms openEvenCore
#print axioms openEven
#print axioms openOdd
#print axioms open_M1_0
#print axioms open_M1_4

end DOpening
