import DCascade

set_option maxRecDepth 40000000
set_option maxHeartbeats 4000000

/-!
# `D`'s entry segment — blank tape to the first in-family milestone, kernel-verified

`D_SPEC_2026-07-26.md` §7 records the entry as `blank → M1(4) = 291,168 steps` and estimates
"~3–4 kernel-`rfl` chunks".  It is one of the items `D`'s non-halting proof needs, listed
separately from the epoch law.  This file closes it, in one chunk.

```
steps dT 291168 init = some (M1 0)          -- `M1 0` is `M1(4)`, indexed `k = j + 4`
```

The fit is exact, with no padding: measured from the raw orbit, at `t = 291168` the head is at
`pos = −32` **and that is its leftmost point so far** (so `Tape.left` is literally `[]`), and the
rightmost cell it has ever visited is `+861`, which is also the position of the last `1` (so
`Tape.right` carries no trailing `false`s and is exactly `Dcascade 0`, 893 cells).  Neither of
those is automatic — a one-cell overshoot on either side would force `zeros` padding and
`TapeCalc.steps_runpad_zeros` — so the anchor is a genuine check of `Dcascade`, not a restatement.

**This is also the first Lean fact that connects `M1`/`Dcascade` to the machine at all.**  Before
it, `lean/DCascade.lean` pinned the words against measurement but nothing tied them to `dT`.

`D` remains `[OPEN]`: the entry is one segment, and the epoch law (`DCascade.EpochLaw`) is still
unproven.  Zero-Mathlib, core only.  No `sorry`, no `native_decide`.

**Build cost.**  291,168 kernel steps in three chunks, roughly 2 minutes, which is why this
lives in its own file and not in `DCascade.lean`.
-/

namespace DEntry

open TapeCalc RungCalc DMachine DCascade

/-! ## The three chunks.

291,168 steps in one `rfl` overflows the kernel stack, so the run is cut at two intermediate
configurations.  Both cut points were generated from the raw orbit, not transcribed by hand, and
both happen to be compactly expressible in the `zeros`/`pow10`/`ones` vocabulary — 10 and 14
terms — which is the only reason chunking here is cheap.  (`Tape.left` is nearest-first and runs
down to the leftmost cell ever visited, `−31` at both cuts; `Tape.right` runs up to the rightmost
ever visited.  Those bounds are what make the literals below exact.) -/

/-- The configuration at `t = 110000`. -/
def C1 : Cfg St :=
  ⟨.B, 260, ⟨pow10 65 ++ zeros 1 ++ ones 37 ++ zeros 1 ++ pow10 36 ++ ones 2 ++ zeros 1
              ++ pow10 13 ++ zeros 1 ++ ones 20,
             true, zeros 1 ++ pow10 51 ++ zeros 1 ++ pow10 71 ++ ones 1⟩⟩

/-- The configuration at `t = 230000`. -/
def C2 : Cfg St :=
  ⟨.B, 290, ⟨zeros 1 ++ pow10 5 ++ ones 2 ++ zeros 1 ++ pow10 30 ++ zeros 1 ++ ones 123
              ++ zeros 1 ++ pow10 36 ++ ones 2 ++ zeros 1 ++ pow10 13 ++ zeros 1 ++ ones 20,
             false, pow10 237 ++ ones 1⟩⟩

theorem chunk1 : steps dT 110000 init = some C1 := by rfl
theorem chunk2 : steps dT 120000 C1 = some C2 := by rfl
theorem chunk3 : steps dT 61168 C2 = some (M1 0) := by rfl

/-- **The entry segment, `[PROVEN]` by the kernel.**  The blank tape reaches `M1(4)` — state `A`
at `pos −32`, left side blank, right side `Dcascade 0` — in exactly 291,168 steps. -/
theorem entry : steps dT 291168 init = some (M1 0) := by
  rw [show 291168 = 110000 + (120000 + 61168) from by omega, steps_add, chunk1, someBind,
      steps_add, chunk2, someBind, chunk3]

/-- Spelled out, so the statement can be read without unfolding `M1`/`Dcascade`. -/
theorem entry_explicit :
    steps dT 291168 init
      = some ⟨.A, -32, ⟨[], false,
          zeros 33 ++ pow10 66 ++ zeros 111 ++ pow10 308 ++ [true]⟩⟩ := by
  rw [entry]
  show some (M1 0) = _
  rw [show M1 0 = (⟨.A, -32, ⟨[], false, Dcascade 0⟩⟩ : Cfg St) from rfl, cascade4]

/-- The milestone is a genuine *left-frontier record*: one step earlier the head is not yet at
`−32`.  This is what makes `Tape.left = []` a structural fact rather than a coincidence. -/
theorem entry_is_record :
    (steps dT 291167 init).map (fun c => c.pos) = some (-31 : Int) := by
  rw [show 291167 = 110000 + (120000 + 61167) from by omega, steps_add, chunk1, someBind,
      steps_add, chunk2, someBind]
  rfl

-- AXIOM AUDIT
#print axioms chunk1
#print axioms chunk3
#print axioms entry
#print axioms entry_explicit
#print axioms entry_is_record

end DEntry
