import Completion
import RunStructure

/-!
# The o4 drain-run law, transported to the REAL ledger orbit

`RunStructure.lean` proves the base-4/3 odometer's run law for the **abstract** `Int` orbit
`RunStructure.orbit` of `T G = (4G + e G)/3` (`run_closed_form`, `run_cap_orbit`).
`Completion.lean` states the open o4 axiom `o4_ledger` about a **different, concrete** object:
the `Nat` milestone orbit `Completion.Gseq` (seed 43, step `G ↦ 4*G/3 + Template.cOdo G`),
whose ledger `Completion.aseq` drains by `1` exactly on the residue class `G ≡ 1 (mod 3)`.

Before this file the two were never connected — `Gseq` appeared in no module but `Completion`.
This file supplies the bridge (`Gseq_shift`, `Gseq_orbit`) and transports the run law onto the
orbit the axiom is actually about:

* `drain_run_exact` — **the drain-run starting at any drain step `n` has length exactly
  `v₃(G_n + 14)`**: the residue `G ≡ 1 (mod 3)` persists for the first `v₃(G_n + 14)` steps
  and breaks at that step.  Mechanism: on the drain branch `G ↦ 4*G/3 + 5 = (4G+14)/3` is
  affine-conjugate to `×(4/3)` about its integer fixed point `−14`, and `G ≡ 1 (mod 3)` is
  *exactly* `3 ∣ (G + 14)`; `4` is a 3-adic unit, so `v₃` drops by exactly one per drain step.
* `drain_run_cap` — the unconditional cap `3^(run) ≤ G_n + 14`, i.e. `run ≤ log₃(G_n + 14)`,
  which with `G_n = Θ((4/3)^n)` is the linear bound `run ≲ 0.262 n`.

This is the exact base-4/3 / 3-adic **mirror** of the antihydra depth `K = v₂(3c − 1)` and its
crude bound `K ≤ 0.585 n`.

**SCOPE — read before quoting.**  This does NOT close `o4_ledger`, and no label is upgraded.
The ledger drains only during drain-runs, so bounding run *length* removes the giant-run
(second-moment) failure mode; what remains is the pure first-moment statement
`limsup D(n)/n ≤ 4/5` (`D` = number of drain steps), which is `Normality43` at o4's seed and
stays `(K)`-hard.  Moreover `run = O(log n)` — the bound the numerics show — is itself
`(K)`-hard: it is `v₃(G_n + 14) = O(log n)`, a single-orbit equidistribution statement.  The
Subspace Theorem does **not** supply it: Subspace bounds digit-runs of the *clean* geometric
`⌊α(4/3)ⁿ⌋`, whereas `Gseq` is the *iterated* odometer orbit, from which the `cOdo`
perturbations accumulate.  Only the linear cap below is unconditional.

Evidence: `o4_drain_run.py` (repo root) — the identity verified with 0 mismatches over 66687
maximal drain-runs to `N = 3·10⁵`; measured cap slope 0.2625 vs `log₃(4/3) = 0.2619`.

Zero-Mathlib, core only.  No `sorry`, no `native_decide`.  No machine decided.
No label upgraded.  `o4` stays gated on `o4_ledger`.
-/

namespace O4Run

open RunStructure

/-! ## §1 The bridge: `Gseq`'s `Nat` step IS the abstract `Int` odometer map `T`. -/

/-- The three branch constants line up: `Template.cOdo` (the `Nat` landing gap) and
`RunStructure.e` (the `Int` branch offset) describe the same map,
`4*G/3 + cOdo G = (4G + e G)/3`, in all three residue classes
(`G ≡ 0`: gap 3 / `e = 9`; `G ≡ 1`: gap 5 / `e = 14`; `G ≡ 2`: gap 1 / `e = 1`). -/
theorem step_bridge (G : Nat) :
    ((4 * G / 3 + Template.cOdo G : Nat) : Int) = T (G : Int) := by
  have hmod : (G : Int) % 3 = ((G % 3 : Nat) : Int) := by omega
  rcases (by omega : G % 3 = 0 ∨ G % 3 = 1 ∨ G % 3 = 2) with h | h | h
  · have hc : Template.cOdo G = 3 := by unfold Template.cOdo; rw [if_pos h]
    have he : e (G : Int) = 9 := by unfold e; rw [if_pos (by omega)]
    rw [hc]; show ((4 * G / 3 + 3 : Nat) : Int) = (4 * (G : Int) + e (G : Int)) / 3
    rw [he]; omega
  · have hc : Template.cOdo G = 5 := by
      unfold Template.cOdo; rw [if_neg (by omega), if_pos h]
    have he : e (G : Int) = 14 := by
      unfold e; rw [if_neg (by omega), if_pos (by omega)]
    rw [hc]; show ((4 * G / 3 + 5 : Nat) : Int) = (4 * (G : Int) + e (G : Int)) / 3
    rw [he]; omega
  · have hc : Template.cOdo G = 1 := by
      unfold Template.cOdo; rw [if_neg (by omega), if_neg (by omega)]
    have he : e (G : Int) = 1 := by
      unfold e; rw [if_neg (by omega), if_neg (by omega)]
    rw [hc]; show ((4 * G / 3 + 1 : Nat) : Int) = (4 * (G : Int) + e (G : Int)) / 3
    rw [he]; omega

/-- **The bridge, shifted form.**  Running the real milestone orbit `i` further steps from
generation `n` is the abstract orbit of `T` started at `Gseq n`.  This is what lets every
`RunStructure` run-law theorem be read as a statement about the actual o4 ledger. -/
theorem Gseq_shift (n : Nat) : ∀ i, (Completion.Gseq (n + i) : Int)
    = orbit (Completion.Gseq n : Int) i := by
  intro i
  induction i with
  | zero => rfl
  | succ i ih =>
    show (Completion.Gseq (n + i + 1) : Int) = T (orbit (Completion.Gseq n : Int) i)
    rw [← ih]
    show ((4 * Completion.Gseq (n + i) / 3
            + Template.cOdo (Completion.Gseq (n + i)) : Nat) : Int) = _
    exact step_bridge _

/-- **The bridge.**  The real o4 milestone orbit is the abstract base-4/3 odometer orbit
seeded at `43`.  (`Completion.Gseq` is the object the open axiom `o4_ledger` speaks about.) -/
theorem Gseq_orbit (n : Nat) : (Completion.Gseq n : Int) = orbit 43 n := by
  have h0 : ((Completion.Gseq 0 : Nat) : Int) = 43 := rfl
  have h := Gseq_shift 0 n
  rw [Nat.zero_add, h0] at h
  exact h

/-! ## §2 The drain branch, and the run law on the real orbit. -/

/-- `Gseq n ≥ 34 > 0`, so the run law's positivity hypothesis is always available. -/
theorem Gseq_pos (n : Nat) : (1 : Int) ≤ (Completion.Gseq n : Int) := by
  have := Completion.Gseq_ge n; omega

/-- **The drain condition IS the branch-residue condition.**  The ledger's `−1` branch
(`Template.ledgerNext` at `G ≡ 1 mod 3`) fires exactly when `(G + 14) % 3 = 0`, i.e. exactly
when `3 ∣ (G + 14)` — the orbit is on the branch of the integer fixed point `−14`.
(`14 ≡ 2 (mod 3)`, so `G ≡ 1` iff `G + 14 ≡ 0`.)  Stated in `%` form to keep the axiom audit
at `[propext, Quot.sound]`. -/
theorem drain_iff (n : Nat) :
    Completion.Gseq n % 3 = 1 ↔ (Completion.Gseq n + 14) % 3 = 0 :=
  ⟨fun h => by omega, fun h => by omega⟩

/-- On a drain step the branch offset is `e = 14`, so the run length is read at `G + 14`. -/
theorem e_drain {n : Nat} (h : Completion.Gseq n % 3 = 1) :
    e (Completion.Gseq n : Int) = 14 := by
  unfold e; rw [if_neg (by omega), if_pos (by omega)]

/-- **THEOREM 1 — the drain-run valuation identity, on the real ledger orbit.**
If generation `n` is a drain step (`G_n ≡ 1 mod 3`, the branch where `aseq` decreases),
then the maximal drain-run starting at `n` has length **exactly `v₃(G_n + 14)`**:
the drain residue persists for the first `v₃(G_n + 14)` generations and breaks at that step.

`[PROVEN]`, transported from `RunStructure.run_closed_form` across `Gseq_shift`.
Numerically cross-checked: `o4_drain_run.py`, 0 mismatches / 66687 runs to `N = 3·10⁵`. -/
theorem drain_run_exact {n : Nat} (h : Completion.Gseq n % 3 = 1) :
    (∀ i, i < v3 ((Completion.Gseq n : Int) + 14) → Completion.Gseq (n + i) % 3 = 1) ∧
      Completion.Gseq (n + v3 ((Completion.Gseq n : Int) + 14)) % 3 ≠ 1 := by
  have hpos := Gseq_pos n
  have he := e_drain h
  have hG : (Completion.Gseq n : Int) % 3 = 1 := by omega
  obtain ⟨hlow, hbrk⟩ := run_closed_form (G := (Completion.Gseq n : Int)) hpos
  rw [he] at hlow hbrk
  refine ⟨fun i hi => ?_, ?_⟩
  · have := hlow i hi
    rw [← Gseq_shift n i] at this
    omega
  · rw [← Gseq_shift n _] at hbrk
    omega

/-- **THEOREM 2 — the unconditional run cap, on the real ledger orbit.**
`3^(drain-run at n) ≤ G_n + 14`, i.e. the run is at most `log₃(G_n + 14)`.  Since
`G_n = Θ((4/3)ⁿ)` this is the linear bound `run ≲ log₃(4/3)·n ≈ 0.262 n` — the base-4/3
mirror of antihydra's crude `K ≤ 0.585 n`.  Unconditional: no normality input. -/
theorem drain_run_cap {n : Nat} (h : Completion.Gseq n % 3 = 1) :
    (3 : Int) ^ v3 ((Completion.Gseq n : Int) + 14) ≤ (Completion.Gseq n : Int) + 14 := by
  have hpos := Gseq_pos n
  have he := e_drain h
  have := run_cap_orbit (G := (Completion.Gseq n : Int)) hpos
  rw [he] at this
  exact this

/-! ## §3 What this does and does not do.

The ledger `aseq` decreases **only** on drain steps, so a drain-run of length `L` costs the
ledger exactly `L`.  §2 therefore bounds every single downward excursion of `aseq`
unconditionally by `log₃(G_n + 14)`.  That removes the *giant-run* (second-moment) failure
mode from `o4_ledger` — the mode that, on antihydra's critical `×3/2` rung, is provably
indistinguishable from the true orbit by any drift/telescoping argument.

What is left is **first-moment only**: `aseq n = 18 + 6n − 7D(n) − 2T(n) ≥ 18 + 4n − 5D(n)`
(`D`,`T` = counts of `G ≡ 1`, `G ≡ 2`), so `o4_ledger` follows from `limsup D(n)/n ≤ 4/5`.
That is a single-orbit base-4/3 digit-frequency statement = `Normality43` at o4's seed, and it
is `(K)`-hard for the standard reason: the feasible-measure set of the residue subshift reaches
drain-frequency `1 > 4/5`, so no structure-only functional can certify the bound (the 2.4
margin is irrelevant — the obstruction is the *undetermined* frequency, not the distance to the
threshold).  See `SYNTHESIS_2026-07-26.md` §3–§4 and `BB6_NO_STRUCTURE_THEOREM.md`.

So: `o4_ledger` remains `[OPEN]`, `o4` remains gated, and this file upgrades no label.  Its
content is that o4's residual difficulty is now pinned to the first moment *alone*. -/

/-! ## §4 Anti-vacuity anchors (kernel-checked at every build).

`drain_run_exact` is conditional on `Gseq n % 3 = 1`.  These anchors certify that the
hypothesis is **actually met on the real orbit** (so the theorem is not vacuous), and that the
predicted run length is the *observed* one at three separate generations with three different
lengths.  Each anchor is a kernel `decide` on the genuine `Completion.Gseq` recurrence.
Cross-checked cell-for-cell against `o4_drain_run.py`. -/

/-- Anchor 0 — the hypothesis is met at the seed: `G₀ = 43 ≡ 1 (mod 3)`.  The theorem is
therefore non-vacuous already at `n = 0`. -/
theorem anchor_drain_0 : Completion.Gseq 0 % 3 = 1 := by decide

/-- Anchor 1 — run of length exactly **1** at `n = 0` (`G₀ = 43`, `43 + 14 = 57 = 3·19`).
The residue holds at `n = 0` and breaks at `n = 1`. -/
theorem anchor_run1 : Completion.Gseq 0 % 3 = 1 ∧ Completion.Gseq 1 % 3 ≠ 1 := by decide

/-- Anchor 2 — run of length exactly **2** at `n = 21` (`G₂₁ = 20983`, `+14 = 20997 = 3²·2333`). -/
theorem anchor_run2 :
    Completion.Gseq 21 % 3 = 1 ∧ Completion.Gseq 22 % 3 = 1 ∧ Completion.Gseq 23 % 3 ≠ 1 := by
  decide

/-- Anchor 3 — run of length exactly **3** at `n = 46` (`G₄₆ = 27898627`, `+14 = 3³·1033283`).
This is the first length-3 drain-run on the orbit.  The final conjunct is the **control that
must fail** for the identity to be exact: if the run were longer, `Gseq 49 % 3` would be `1`. -/
theorem anchor_run3 :
    Completion.Gseq 46 % 3 = 1 ∧ Completion.Gseq 47 % 3 = 1 ∧ Completion.Gseq 48 % 3 = 1
      ∧ Completion.Gseq 49 % 3 ≠ 1 := by decide

/-- Anchor 4 — the concrete milestone values the anchors above rest on, pinned by `decide`
so that a drift in `Gseq`/`cOdo` would break the build rather than silently invalidate them. -/
theorem anchor_values :
    Completion.Gseq 0 = 43 ∧ Completion.Gseq 21 = 20983 ∧ Completion.Gseq 46 = 27898627 := by
  decide

-- The predicted run lengths, evaluated (`v3` is well-founded, so `#eval` not `decide`):
-- each must equal the observed run length in the anchors above (1, 2, 3).
#eval v3 ((Completion.Gseq 0 : Int) + 14)   -- 1
#eval v3 ((Completion.Gseq 21 : Int) + 14)  -- 2
#eval v3 ((Completion.Gseq 46 : Int) + 14)  -- 3

-- AXIOM AUDIT — must be `[propext, Quot.sound]` (no `sorryAx`, no new axiom).
#print axioms step_bridge
#print axioms Gseq_shift
#print axioms Gseq_orbit
#print axioms drain_iff
#print axioms drain_run_exact
#print axioms drain_run_cap
#print axioms anchor_run3
#print axioms anchor_values

end O4Run
