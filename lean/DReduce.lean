import DEntry

/-!
# `D`'s non-halting, reduced to ONE obligation

This is the `M5` pattern of `lean/Completion.lean`, applied to `D`: state the whole result
conditionally and isolate what is unproven into a single named `Prop`, so that progress is
measurable (every axiom-to-theorem upgrade is visible) and so that nothing unproven can hide.

```
DCascade.EpochLaw  →  ∀ N, steps dT N init ≠ none
```

The two ingredients are both `[PROVEN]`:

* `DEntry.entry` — the blank tape reaches `M1(4)` in exactly 291,168 kernel-checked steps;
* `TapeCalc.nonhalt_of_invariant` — the machine-independent assembly lemma.

So `D`'s non-halting now rests on exactly one open statement, `EpochLaw`: that every milestone
`M1(j)` reaches `M1(j+1)` in some positive number of steps.  Measured for `j = 0..4`
(i.e. `k = 4..8`); the four `RungCalc` laws account for 99.98% of each epoch's steps
(`d_rf4_epochs.py`), but the **seams** — each law's output configuration being the next law's
input on `Dcascade` — are unproven, which is precisely the content of `EpochLaw`.

**`D` remains `[OPEN]`.**  This file proves an implication, not the machine.
Zero-Mathlib, core only.  No `sorry`, no `native_decide`.
-/

namespace DReduce

open TapeCalc DMachine DCascade

/-- The milestone family, as an invariant predicate. -/
def AtMilestone (c : Cfg St) : Prop := ∃ j, c = M1 j

/-- **`EpochLaw` ⟹ `D` never halts.** -/
theorem nonhalt_of_EpochLaw (h : EpochLaw) : ∀ N : Nat, steps dT N init ≠ none := by
  have hM : ∀ M : Nat, steps dT M (M1 0) ≠ none := by
    refine nonhalt_of_invariant dT AtMilestone ?_ (M1 0) ⟨0, rfl⟩
    rintro c ⟨j, rfl⟩
    obtain ⟨n, hn, hrun⟩ := h j
    exact ⟨n, hn, M1 (j + 1), ⟨j + 1, rfl⟩, hrun⟩
  intro N
  by_cases hle : N ≤ 291168
  · exact steps_prefix_ne_none DEntry.entry hle
  · rw [show N = 291168 + (N - 291168) from by omega, steps_add, DEntry.entry, someBind]
    exact hM (N - 291168)

-- AXIOM AUDIT
#print axioms nonhalt_of_EpochLaw

end DReduce
