import DCascade

set_option maxRecDepth 40000000
set_option maxHeartbeats 4000000

/-!
# `EpochLaw` at `j = 0` — the first proven instance

`DCascade.EpochLaw` is `D`'s single open obligation and `lean/DReduce.lean` shows it implies `D`'s
non-halting.  Until now nothing in Lean showed the statement is even **satisfiable**: `Dcascade`
was pinned against measurement and `DEntry` reached `M1 0`, but no epoch had been closed.

This file closes the first one:

```
steps dT 905244 (M1 0) = some (M1 1)          -- k = 4 → k = 5
```

by the kernel, in nine chunks (one `rfl` overflows the stack), at eight intermediate
configurations generated from the orbit — **using `TapeCalc`'s own list semantics, not an
infinite-array model**.  That distinction is not cosmetic: the first attempt reconstructed each
cut from an array of cells and the two chunks touching `M1 0` and `M1 1` failed, because
`Tape.right` grows only when `mvL` pushes a cell back onto it, so its extent is not "every cell
visited".  Regenerating with `mvL`/`mvR` as `TapeCalc` defines them, and round-tripping every cut
word through the `zeros`/`pow10`/`ones` vocabulary, fixed it.

## What this is and is not

It is an **anti-vacuity anchor**: `EpochLaw` now has an instance, and `Dcascade 0 → Dcascade 1`
is verified end-to-end against `dT` rather than against a Python measurement.

It is **not** progress on `EpochLaw` itself, which is `∀ j`.  That route is being built in
`lean/DOpening.lean` (the opening, at every level) and `RungCalc` (`tileIter`, `tile2`, `rung0`,
`descend`) — a chain of prefix-local `∀`-laws under a `k → k+2` induction.  One measured
observation for it: the prefix-local decomposition **absorbs** the stretches the law-based
decomposition gets stuck on — at `k = 4`, `openEven`'s 13219 steps already cover two of the
three stuck stretches.

**Build cost ≈ 10 minutes**, which is why this lives in its own file.
`D` remains `[OPEN]`.  Zero-Mathlib, core only.  No `sorry`, no `native_decide`.
-/

namespace DEpoch

open TapeCalc RungCalc DMachine DCascade

/-- The configuration 110000 steps into the epoch. -/
def E110000 : Cfg St :=
  ⟨.B, 884, ⟨zeros 1 ++ pow10 32 ++ ones 2 ++ zeros 1 ++ pow10 263 ++ zeros 1 ++ ones 46 ++ zeros 1
      ++ pow10 72 ++ ones 2 ++ zeros 1 ++ pow10 28 ++ zeros 1 ++ ones 38 ++ zeros 1
      ++ pow10 9 ++ ones 2 ++ zeros 1 ++ pow10 1 ++ zeros 1 ++ ones 7 ++ zeros 1 ++ ones 2
      ++ zeros 2 ++ ones 2,
    false,
    pow10 56 ++ ones 1⟩⟩

/-- The configuration 220000 steps into the epoch. -/
def E220000 : Cfg St :=
  ⟨.D, 778, ⟨zeros 1 ++ pow10 3 ++ ones 2 ++ zeros 1 ++ pow10 215 ++ zeros 1 ++ ones 94 ++ zeros 1
      ++ pow10 72 ++ ones 2 ++ zeros 1 ++ pow10 28 ++ zeros 1 ++ ones 38 ++ zeros 1
      ++ pow10 9 ++ ones 2 ++ zeros 1 ++ pow10 1 ++ zeros 1 ++ ones 7 ++ zeros 1 ++ ones 2
      ++ zeros 2 ++ ones 2,
    false,
    zeros 1 ++ pow10 182 ++ ones 1⟩⟩

/-- The configuration 330000 steps into the epoch. -/
def E330000 : Cfg St :=
  ⟨.B, 666, ⟨zeros 1 ++ pow10 142 ++ zeros 1 ++ ones 137 ++ zeros 1 ++ pow10 72 ++ ones 2 ++ zeros 1
      ++ pow10 28 ++ zeros 1 ++ ones 38 ++ zeros 1 ++ pow10 9 ++ ones 2 ++ zeros 1
      ++ pow10 1 ++ zeros 1 ++ ones 7 ++ zeros 1 ++ ones 2 ++ zeros 2 ++ ones 2,
    true,
    ones 2 ++ zeros 1 ++ pow10 28 ++ zeros 1 ++ pow10 273 ++ ones 1⟩⟩

/-- The configuration 440000 steps into the epoch. -/
def E440000 : Cfg St :=
  ⟨.C, 764, ⟨pow10 38 ++ ones 2 ++ zeros 1 ++ pow10 132 ++ zeros 1 ++ ones 177 ++ zeros 1 ++ pow10 72
      ++ ones 2 ++ zeros 1 ++ pow10 28 ++ zeros 1 ++ ones 38 ++ zeros 1 ++ pow10 9 ++ ones 2
      ++ zeros 1 ++ pow10 1 ++ zeros 1 ++ ones 7 ++ zeros 1 ++ ones 2 ++ zeros 2 ++ ones 2,
    true,
    zeros 1 ++ pow10 312 ++ ones 1⟩⟩

/-- The configuration 550000 steps into the epoch. -/
def E550000 : Cfg St :=
  ⟨.E, 1248, ⟨zeros 2 ++ pow10 297 ++ ones 2 ++ zeros 1 ++ pow10 96 ++ zeros 1 ++ ones 213 ++ zeros 1
      ++ pow10 72 ++ ones 2 ++ zeros 1 ++ pow10 28 ++ zeros 1 ++ ones 38 ++ zeros 1
      ++ pow10 9 ++ ones 2 ++ zeros 1 ++ pow10 1 ++ zeros 1 ++ ones 7 ++ zeros 1 ++ ones 2
      ++ zeros 2 ++ ones 2,
    true,
    pow10 126 ++ ones 1⟩⟩

/-- The configuration 660000 steps into the epoch. -/
def E660000 : Cfg St :=
  ⟨.E, 1328, ⟨zeros 2 ++ pow10 354 ++ ones 2 ++ zeros 1 ++ pow10 62 ++ zeros 1 ++ ones 247 ++ zeros 1
      ++ pow10 72 ++ ones 2 ++ zeros 1 ++ pow10 28 ++ zeros 1 ++ ones 38 ++ zeros 1
      ++ pow10 9 ++ ones 2 ++ zeros 1 ++ pow10 1 ++ zeros 1 ++ ones 7 ++ zeros 1 ++ ones 2
      ++ zeros 2 ++ ones 2,
    true,
    pow10 137 ++ ones 1⟩⟩

/-- The configuration 770000 steps into the epoch. -/
def E770000 : Cfg St :=
  ⟨.E, 1336, ⟨zeros 2 ++ pow10 374 ++ ones 2 ++ zeros 1 ++ pow10 30 ++ zeros 1 ++ ones 279 ++ zeros 1
      ++ pow10 72 ++ ones 2 ++ zeros 1 ++ pow10 28 ++ zeros 1 ++ ones 38 ++ zeros 1
      ++ pow10 9 ++ ones 2 ++ zeros 1 ++ pow10 1 ++ zeros 1 ++ ones 7 ++ zeros 1 ++ ones 2
      ++ zeros 2 ++ ones 2,
    true,
    pow10 181 ++ ones 1⟩⟩

/-- The configuration 860000 steps into the epoch. -/
def E860000 : Cfg St :=
  ⟨.D, 1448, ⟨zeros 1 ++ pow10 443 ++ ones 2 ++ zeros 1 ++ pow10 5 ++ zeros 1 ++ ones 304 ++ zeros 1
      ++ pow10 72 ++ ones 2 ++ zeros 1 ++ pow10 28 ++ zeros 1 ++ ones 38 ++ zeros 1
      ++ pow10 9 ++ ones 2 ++ zeros 1 ++ pow10 1 ++ zeros 1 ++ ones 7 ++ zeros 1 ++ ones 2
      ++ zeros 2 ++ ones 2,
    false,
    zeros 1 ++ pow10 162 ++ ones 1⟩⟩

theorem ec1 : steps dT 110000 (M1 0) = some E110000 := by rfl
theorem ec2 : steps dT 110000 E110000 = some E220000 := by rfl
theorem ec3 : steps dT 110000 E220000 = some E330000 := by rfl
theorem ec4 : steps dT 110000 E330000 = some E440000 := by rfl
theorem ec5 : steps dT 110000 E440000 = some E550000 := by rfl
theorem ec6 : steps dT 110000 E550000 = some E660000 := by rfl
theorem ec7 : steps dT 110000 E660000 = some E770000 := by rfl
theorem ec8 : steps dT 90000 E770000 = some E860000 := by rfl
theorem ec9 : steps dT 45244 E860000 = some (M1 1) := by rfl

/-- **The `k = 4` epoch, `[PROVEN]` by the kernel.** -/
theorem epoch0 : steps dT 905244 (M1 0) = some (M1 1) := by
  rw [show 905244 = 110000 + (110000 + (110000 + (110000 + (110000 + (110000 + (110000
        + (90000 + 45244))))))) from by omega,
      steps_add, ec1, someBind, steps_add, ec2, someBind, steps_add, ec3, someBind,
      steps_add, ec4, someBind, steps_add, ec5, someBind, steps_add, ec6, someBind,
      steps_add, ec7, someBind, steps_add, ec8, someBind, ec9]

/-- `EpochLaw` is satisfiable: it holds at `j = 0`, with `905244 ≥ 1`. -/
theorem epochLaw_at_zero : ∃ n, 1 ≤ n ∧ steps dT n (M1 0) = some (M1 1) :=
  ⟨905244, by omega, epoch0⟩

-- AXIOM AUDIT
#print axioms ec1
#print axioms ec9
#print axioms epoch0
#print axioms epochLaw_at_zero

end DEpoch
