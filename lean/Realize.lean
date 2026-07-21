import X2
import BlankNorm
import HInit
open X2

/-!
# Realize — T9 / Obligation H: ONE milestone family for ALL THREE `x2_nonhalt` hypotheses.

`x2_nonhalt` (§5, `X2.lean`) needs `M1 M6 : Nat → Cfg` with

* `h_init : ∃ n, 1 ≤ n ∧ steps n init = some (M1 1)`
* `h_low  : ∀ g, ∃ n, 1 ≤ n ∧ steps n (M1 g) = some (M6 g)`
* `h_doub : ∀ g, ∃ n, 1 ≤ n ∧ steps n (M6 g) = some (M1 (g+1))`

Before this file the state was: `h_low` PROVED (`h_low_even`/`h_low_odd`) for the §5am CANONICAL
`M1`/`M6` (pos-0, blank-trimmed), while `h_init` is **FALSE** for that family
(`HInit.h_init_neq_M1_1`) and was discharged only in REALIZED form
(`HInit.h_init_wired : … = some (realizeM1 (M1 1))`).  Two different families.  Closing that gap
is T9.

## Recommendation taken: option (a) — transport to the REALIZED family

Option (b) (re-base the canonical closed forms so `h_init` holds directly) was assessed and
REJECTED: `h_init` pins `M1 1` to the single measured config `HInit.c189`, so re-basing means
editing the §5am `def M1` — which would invalidate every `rfl` in §5ao/§5aw/§5bb that is stated
against it (`h_low_even_core`, `h_low_odd_core` and their five component transports), i.e. it
re-opens `h_low ∀g`, the one thing that is already closed.  Option (a) costs two lemmas and keeps
every existing proof.  The realized family is

    M1a a g = ⟨E, a,     ⟨[false], false, (M1 g).tape.right ++ [false]⟩⟩
    M6a a g = ⟨E, a − 5, ⟨[false], false, (M6 g).tape.right ++ [false]⟩⟩

— the canonical milestone at an arbitrary head anchor `a`, carrying the boundary blanks the machine
actually leaves.  `M1a (−25) 1 = realizeM1 (M1 1) = HInit.c189` on the nose (`M1a_one`).

The anchor is left FREE (`a : Int`) on purpose: `pos` is never read by `step`, so anchoring is pure
bookkeeping, but `x2_nonhalt` demands `Cfg` EQUALITY, so the family must be anchored consistently
with whatever per-generation drift the doubling phase turns out to have.  See §5.

## The two transport ingredients (and why `realizeM1_port` only gave `isSome`)

`BlankNorm`'s `steps_lpad`/`steps_rpad` are honest DISJUNCTIONS (pad absorbed / pad riding), so
they cannot by themselves name the target config — hence `HInit.realizeM1_port` could only extract
`.isSome`.  Both disjunctions are resolved here, each by a different device, and NEITHER is papered
over:

1. **RIGHT boundary — resolved by tail-parametricity, not by `steps_rpad` at all.**
   `h_low_even_core` is `∀ TAIL` and `h_low_odd_core` is `∀ FRAME`.  Instantiating the tail
   parameter at `(canonical tail) ++ [false]` puts the extra trailing blank INSIDE the parameter,
   so there is no disjunction to discharge: the transport holds for that tail whatever the head
   does to it.

2. **LEFT boundary — resolved by an ABSORPTION-MERGE lemma (`lmerge`), the new weapon here.**
   Within 11 steps of the `M1` entry window the head steps left off the empty `left` list, where
   `mvL ⟨[], h, r⟩ = ⟨[], false, h::r⟩ = mvL ⟨[false], h, r⟩`: the padded and the trimmed runs
   become the SAME configuration.  `lmerge` states exactly that, as an equation between the two
   `steps 11` results (kernel `rfl`, `∀ p`, `∀ Z`); `steps_of_merge` propagates it to every
   `N ≥ 11`.  That upgrades `steps_lpad`'s disjunction to an EXACT config transport on this entry
   window — the thing `realizeM1_port` could not state.  (Control: the same statement at `steps 10`
   is REJECTED by the kernel — the merge really happens at 11, not earlier.)

Consequence, worth stating because it is forced and not a matter of taste: the low phase ABSORBS
the left boundary blank and CARRIES the right one, so `M6a`'s `left` is `M6`'s own `[false]` — NOT
`M6`'s `left ++ [false]`.  `realizeM1` is therefore NOT the right realization on the `M6` side.

## The `g = 0` slot (a genuine gap in the literal `∀ g`, closed honestly)

`h_low`/`h_doub` are quantified over ALL `g : Nat`, but `h_low_even`/`h_low_odd` cover only `g ≥ 2`
(`g = 2k+2` / `g = 2k+3`); `g = 1` is covered by NEITHER and is discharged here separately
(`h_low_g1_a`, kernel `rfl`, 343 steps on the full milestone tapes).  Generation `0` is not a
generation at all: a `#eval` search finds NO `n < 700` with `steps n (M1 0) = some (M6 0)`
(contrast `g = 1`, which returns `[343]`).  Rather than weaken `x2_nonhalt`'s `Prop` (forbidden),
the family's index-`0` slot is filled with the orbit's genuine PRE-HISTORY: `M1d A 0 = init`,
`M6d A 0 = init` after one step.  Then `h_low` at `0` is `init → (1 step)` and `h_doub` at `0` is
the remaining `188 098` steps of `HInit.h_init_reached`.  Both are true, nonempty, halt-free
segments of the real orbit — nothing here is vacuous or weakened.

## What remains OPEN

Exactly one obligation: `DoubCanon A` (§5) — the doubling phase in the CANONICAL frame, with the
boundary conventions this family fixes.  `x2_nonhalt_of_DoubCanon` shows it is the ONLY input still
missing.
-/

set_option maxRecDepth 20000

namespace Realize

/-! ## §1 The merge weapon: an EXACT (non-disjunctive) left-boundary transport. -/

/-- **Run-splitting from a MERGE.**  If two configs have the same `steps n0` image, any `N ≥ n0`
transport of one is a transport of the other, with the SAME target config.  This is what turns
`BlankNorm`'s disjunctive `steps_lpad` into an exact statement, once a merge is exhibited. -/
theorem steps_of_merge {n0 N : Nat} {c c' d : Cfg} (hle : n0 ≤ N)
    (hm : steps n0 c' = steps n0 c) (h : steps N c = some d) : steps N c' = some d := by
  obtain ⟨m, rfl⟩ : ∃ m, N = n0 + m := ⟨N - n0, by omega⟩
  rw [steps_add] at h ⊢
  rw [hm]; exact h

/-- **THE LEFT-BOUNDARY ABSORPTION MERGE.**  At the `M1` entry window (`[E] 0 0^4 …`) the head dips
to `pos −1` off an empty `left`, absorbing one leading blank: after exactly `11` steps the
blank-padded and the blank-trimmed runs are LITERALLY the same `Option Cfg`.  Kernel `rfl`, for
EVERY head anchor `p` and EVERY continuation `Z`.  (Control: the same claim at `10` steps is
rejected by the kernel.) -/
theorem lmerge (p : Int) (Z : List Bool) :
    steps 11 ⟨.E, p, ⟨[false], false, false::false::false::false::false::Z⟩⟩
      = steps 11 ⟨.E, p, ⟨[], false, false::false::false::false::false::Z⟩⟩ := rfl

/-- **EXACT left-pad transport at an `M1`-shaped entry.**  Any `≥ 11`-step transport out of the
canonical (`left = []`) `M1`-shaped config is a transport out of the one-leading-blank config, to
the very SAME target — no disjunction, no `isSome` weakening. -/
theorem lpad_M1entry {N : Nat} (hle : 11 ≤ N) (p : Int) (Y : List Bool) {d : Cfg}
    (h : steps N ⟨.E, p, ⟨[], false, zeros 21 ++ Y⟩⟩ = some d) :
    steps N ⟨.E, p, ⟨[false], false, zeros 21 ++ Y⟩⟩ = some d := by
  refine steps_of_merge hle ?_ h
  show steps 11 ⟨.E, p, ⟨[false], false, false::false::false::false::false::(zeros 16 ++ Y)⟩⟩
      = steps 11 ⟨.E, p, ⟨[], false, false::false::false::false::false::(zeros 16 ++ Y)⟩⟩
  exact lmerge p (zeros 16 ++ Y)

#print axioms steps_of_merge
#print axioms lmerge
#print axioms lpad_M1entry

/-! ## §2 The realized milestone families, at a FREE head anchor. -/

/-- **The realized generation-start milestone at anchor `a`.** -/
def M1a (a : Int) (g : Nat) : Cfg :=
  ⟨.E, a, ⟨[false], false, (M1 g).tape.right ++ [false]⟩⟩

/-- **The realized mid-generation milestone at anchor `a`.**  Its own anchor is `a − 5`: the low
phase's head displacement, `−5`, is PROVED for every `g` (§5ao/§5aw), so this is forced. -/
def M6a (a : Int) (g : Nat) : Cfg :=
  ⟨.E, a - 5, ⟨[false], false, (M6 g).tape.right ++ [false]⟩⟩

/-- `M1a (−25) 1` IS `realizeM1 (M1 1)`, hence (`HInit.realizeM1_bridge`) the config `c189` the
orbit actually occupies at step 188 099. -/
theorem M1a_one : M1a (-25) 1 = HInit.realizeM1 (M1 1) := rfl

#print axioms M1a_one

/-! ## §3 `h_low` for the realized family, at every anchor, `∀ g ≥ 1`. -/

set_option maxHeartbeats 4000000 in
/-- **`h_low` realized, `∀` EVEN `g ≥ 2`, `∀` anchor.**  Ported from `h_low_even_core` by
(i) tail-parametricity at `TAIL ++ [false]` (the right blank rides inside the tail parameter),
(ii) `lpad_M1entry` (the left blank is absorbed), (iii) `steps_pos_shift` (the anchor). -/
theorem h_low_even_a (a : Int) (k : Nat) :
    steps (267 + 38*(2*k+2)) (M1a a (2*k+2)) = some (M6a a (2*k+2)) := by
  have hmod : (2*k+2) % 2 = 0 := by omega
  have hM1 : M1a a (2*k+2) = ⟨.E, (0:Int) + a, ⟨[false], false,
      zeros 21 ++ (uUnits (2*k+1) ++ (true :: (zeros 10 ++
        ((ones (2^(2*k+2+8)-3) ++ m1casc (2*k+2+6) (2*k+2+7) []) ++ [false]))))⟩⟩ := by
    unfold M1a M1
    rw [hmod]
    simp only [reduceIte, show 2*k+2-1 = 2*k+1 from by omega]
    simp only [List.append_assoc, List.cons_append]
    exact cfgPos (by omega)
  have hM6 : M6a a (2*k+2) = ⟨.E, (-5:Int) + a, ⟨[false], false,
      false :: pow10 4 ++ ones 9 ++ false::false:: (rUnits (2*k+3) ++
        (true::false::false:: ((ones (2^(2*k+2+8)-3) ++ m1casc (2*k+2+6) (2*k+2+7) []) ++ [false])))⟩⟩ := by
    unfold M6a M6
    rw [hmod]
    simp only [reduceIte, show 2*k+2+1 = 2*k+3 from by omega]
    simp only [List.append_assoc, List.cons_append]
    exact cfgPos (by omega)
  rw [hM1, hM6]
  exact steps_pos_shift (d := a)
    (lpad_M1entry (by omega) 0 _
      (h_low_even_core k ((ones (2^(2*k+2+8)-3) ++ m1casc (2*k+2+6) (2*k+2+7) []) ++ [false])))

set_option maxHeartbeats 4000000 in
/-- **`h_low` realized, `∀` ODD `g ≥ 3`, `∀` anchor.**  Same three devices, from `h_low_odd_core`
(the block-edge `−4` trim rides inside the `FRAME` parameter). -/
theorem h_low_odd_a (a : Int) (k : Nat) :
    steps (419 + 76*k) (M1a a (2*k+3)) = some (M6a a (2*k+3)) := by
  have hsub : 2*k+3-1 = 2*k+2 := by omega
  have e1 : (2:Nat)^(2*k+3+8) = 2^(2*k+3) * 256 := by rw [Nat.pow_add]
  have e2 : 4 ≤ (2:Nat)^(2*k+3) := by
    have := four_le_two_pow (2*k+1); rwa [show 2*k+1+2 = 2*k+3 from by omega] at this
  have hpow : (2:Nat)^(2*k+3+8) - 9 = 4 + (2^(2*k+3+8) - 13) := by rw [e1]; omega
  have hM1 : M1a a (2*k+3) = ⟨.E, (0:Int) + a, ⟨[false], false,
      zeros 21 ++ (uUnits (2*k+2) ++ (true :: (zeros 4 ++ (pow10 6 ++
        (ones 4 ++ ((ones (2^(2*k+3+8)-13) ++ m1casc (2*k+3+6) (2*k+3+7) []) ++ [false]))))))⟩⟩ := by
    unfold M1a M1
    rw [hsub]
    simp only [if_neg (show ¬ ((2*k+3) % 2 = 0) from by omega)]
    rw [show (2:Nat)^(2*k+3+8)-9 = 4 + (2^(2*k+3+8)-13) from hpow, ones_add]
    simp only [List.append_assoc, List.cons_append]
    exact cfgPos (by omega)
  have hM6 : M6a a (2*k+3) = ⟨.E, (-5:Int) + a, ⟨[false], false,
      false :: pow10 4 ++ ones 9 ++ false::false:: (rUnits (2*k+3) ++
        (pow10 10 ++ ((ones (2^(2*k+3+8)-13) ++ m1casc (2*k+3+6) (2*k+3+7) []) ++ [false])))⟩⟩ := by
    unfold M6a M6
    simp only [if_neg (show ¬ ((2*k+3) % 2 = 0) from by omega)]
    simp only [List.append_assoc, List.cons_append]
    exact cfgPos (by omega)
  rw [hM1, hM6]
  exact steps_pos_shift (d := a)
    (lpad_M1entry (by omega) 0 _
      (h_low_odd_core k ((ones (2^(2*k+3+8)-13) ++ m1casc (2*k+3+6) (2*k+3+7) []) ++ [false])))

set_option maxHeartbeats 4000000 in
/-- **`h_low` realized at `g = 1`, `∀` anchor.**  `g = 1` falls outside BOTH `h_low_even`
(`g = 2k+2`) and `h_low_odd` (`g = 2k+3`), so it is a genuine extra obligation.  Kernel `rfl` at
anchor `0` on the FULL untruncated milestone tapes (343 steps — the left-blank absorption and the
riding right blank are both witnessed directly by the kernel here), then `steps_pos_shift`. -/
theorem h_low_g1_a (a : Int) : steps 343 (M1a a 1) = some (M6a a 1) := by
  have h : steps 343 ⟨.E, (0:Int), ⟨[false], false, (M1 1).tape.right ++ [false]⟩⟩
      = some ⟨.E, (-5:Int), ⟨[false], false, (M6 1).tape.right ++ [false]⟩⟩ := rfl
  have h2 := steps_pos_shift (d := a) h
  show steps 343 ⟨.E, a, ⟨[false], false, (M1 1).tape.right ++ [false]⟩⟩
      = some ⟨.E, a - 5, ⟨[false], false, (M6 1).tape.right ++ [false]⟩⟩
  rw [cfgPos (s := St.E) (t := ⟨[false], false, (M1 1).tape.right ++ [false]⟩)
        (show a = 0 + a from by omega),
      cfgPos (s := St.E) (t := ⟨[false], false, (M6 1).tape.right ++ [false]⟩)
        (show a - 5 = -5 + a from by omega)]
  exact h2

/-- **`h_low` realized, `∀ g ≥ 1`, `∀` anchor** — the three cases assembled. -/
theorem h_low_a (a : Int) (g : Nat) (hg : 1 ≤ g) :
    ∃ n, 1 ≤ n ∧ steps n (M1a a g) = some (M6a a g) := by
  obtain ⟨k, hk | hk | hk⟩ : ∃ k, g = 1 ∨ g = 2*k+2 ∨ g = 2*k+3 := ⟨g/2 - 1, by omega⟩
  · rw [hk]; exact ⟨343, by omega, h_low_g1_a a⟩
  · rw [hk]; exact ⟨267 + 38*(2*k+2), by omega, h_low_even_a a k⟩
  · rw [hk]; exact ⟨419 + 76*k, by omega, h_low_odd_a a k⟩

#print axioms h_low_even_a
#print axioms h_low_odd_a
#print axioms h_low_g1_a
#print axioms h_low_a

/-! ## §4 The family fed to `x2_nonhalt`, indexed by a per-generation ANCHOR `A`. -/

/-- **The generation-start family.**  Index `0` is the orbit's pre-history (`init`); index `g ≥ 1`
is the realized milestone anchored at `A g`. -/
def M1d (A : Nat → Int) (g : Nat) : Cfg := if g = 0 then init else M1a (A g) g

/-- **The mid-generation family.**  Index `0` is `init` after one step. -/
def M6d (A : Nat → Int) (g : Nat) : Cfg :=
  if g = 0 then ⟨.B, 1, ⟨[true], false, []⟩⟩ else M6a (A g) g

/-- **`h_init` DISCHARGED** for `M1d A`, for any anchor function with `A 1 = −25` (the measured
arrival anchor).  188 099 steps, from `HInit.h_init_reached`. -/
theorem h_init_d (A : Nat → Int) (hA : A 1 = -25) :
    ∃ n, 1 ≤ n ∧ steps n init = some (M1d A 1) := by
  refine ⟨188099, by omega, ?_⟩
  show steps 188099 init = some (M1a (A 1) 1)
  rw [hA, M1a_one, HInit.realizeM1_bridge]
  exact HInit.h_init_reached

/-- **`h_low` DISCHARGED `∀ g`** for `M1d A`/`M6d A`, for EVERY anchor function.  The index-`0`
slot is the orbit's first step; `g ≥ 1` is `h_low_a`. -/
theorem h_low_d (A : Nat → Int) (g : Nat) :
    ∃ n, 1 ≤ n ∧ steps n (M1d A g) = some (M6d A g) := by
  by_cases hg : g = 0
  · subst hg; exact ⟨1, by omega, rfl⟩
  · unfold M1d M6d
    rw [if_neg hg, if_neg hg]
    exact h_low_a (A g) g (by omega)

#print axioms h_init_d
#print axioms h_low_d

/-! ## §5 `h_doub`: the EXACT remaining obligation (T7's target), and the reduction. -/

/-- **THE ONE REMAINING OBLIGATION, in the CANONICAL frame** (a `Prop`, NOT an axiom — the
`x2_nonhalt` style).  For every real generation `g ≥ 1` the doubling phase must carry

    `[E @ −5]`, `left = [false]`, `right = (M6 g).tape.right ++ [false]`
      ⟶  `[E @ A(g+1) − A g]`, `left = [false]`, `right = (M1 (g+1)).tape.right ++ [false]`

in `n ≥ 1` steps.  Four things are load-bearing and must not be tacitly dropped:

* **the target's `left` is `[false]`, not `[]`.**  The §5am canonical `M1 (g+1)` is blank-TRIMMED
  (`left = []`); the real machine leaves one boundary blank there, as `HInit.c189` measures at
  `g = 1`.  A doubling proof aimed at canonical `left = []` proves the WRONG statement for this
  family.  If the measurement instead shows `left = zeros j` with `j ≠ 1` at some generation, this
  family is NOT closed as defined and must be re-anchored past the absorption point (`lmerge` shows
  every left-blank surplus is absorbed within 11 steps of the NEXT low phase, so re-anchoring
  `M1d`/`M6d` at `+11` steps repairs it) — flagging this rather than assuming `j = 1` is the point
  of stating the obligation exactly.
* **one extra trailing blank on both sides.**  Free if the doubling is proved tail-parametrically:
  see `doubCanon_of_tailparam`, the recommended shape.
* **the head displacement is `A(g+1) − A g`, whatever the measurement says.**  `A` is a free
  parameter precisely so a `g`-GROWING doubling drift does not falsify the obligation: measure the
  drift `δ g`, take `A 1 = −25` and `A (g+1) = A g − 5 + δ g`, and this `Prop` is the right target.
  A CONSTANT anchor (`A = fun _ => −25`) forces displacement exactly `+5` for every `g`, which is
  an ASSUMPTION about the orbit, not a theorem — do not build T7 around it without measuring.
* **`n ≥ 1`** — a nonempty segment; `n = 0` would prove nothing. -/
def DoubCanon (A : Nat → Int) : Prop := ∀ g, 1 ≤ g → ∃ n, 1 ≤ n ∧
  steps n ⟨.E, -5, ⟨[false], false, (M6 g).tape.right ++ [false]⟩⟩
    = some ⟨.E, A (g+1) - A g, ⟨[false], false, (M1 (g+1)).tape.right ++ [false]⟩⟩

/-- **The recommended shape for the doubling proof.**  If `M6 g`'s right tape splits as `P ++ T`
and `M1 (g+1)`'s as `Q ++ T`, and the transport is proved `∀ X` on the shared tail, then the
`DoubCanon` obligation at `g` follows with the trailing blank handled for free (it rides inside
`X`).  This is exactly the shape of `h_low_even_core`/`h_low_odd_core`, and the reason their port
to the realized family cost nothing on the right boundary. -/
theorem doubCanon_of_tailparam (A : Nat → Int) (g n : Nat) (hn : 1 ≤ n) (P Q T : List Bool)
    (hP : (M6 g).tape.right = P ++ T) (hQ : (M1 (g+1)).tape.right = Q ++ T)
    (hrun : ∀ X, steps n ⟨.E, -5, ⟨[false], false, P ++ X⟩⟩
        = some ⟨.E, A (g+1) - A g, ⟨[false], false, Q ++ X⟩⟩) :
    ∃ n, 1 ≤ n ∧ steps n ⟨.E, -5, ⟨[false], false, (M6 g).tape.right ++ [false]⟩⟩
      = some ⟨.E, A (g+1) - A g, ⟨[false], false, (M1 (g+1)).tape.right ++ [false]⟩⟩ := by
  refine ⟨n, hn, ?_⟩
  rw [hP, hQ, List.append_assoc, List.append_assoc]
  exact hrun (T ++ [false])

/-- `h_doub` at the index-`0` slot: the orbit's pre-history, the `188 098` steps of
`HInit.h_init_reached` after the first one.  A real halt-free segment of the real orbit. -/
theorem h_doub_d_zero (A : Nat → Int) (hA : A 1 = -25) :
    ∃ n, 1 ≤ n ∧ steps n (M6d A 0) = some (M1d A 1) := by
  refine ⟨188098, by omega, ?_⟩
  have h : steps 188099 init = some (M1d A 1) := by
    show steps 188099 init = some (M1a (A 1) 1)
    rw [hA, M1a_one, HInit.realizeM1_bridge]
    exact HInit.h_init_reached
  rw [show (188099 : Nat) = 1 + 188098 from rfl, steps_add,
      show steps 1 init = some (⟨.B, 1, ⟨[true], false, []⟩⟩ : Cfg) from rfl, someBind] at h
  exact h

/-- **`h_doub` for the assembled family, REDUCED to `DoubCanon A`** (`steps_pos_shift` at the
anchor, plus the index-`0` pre-history slot). -/
theorem h_doub_d (A : Nat → Int) (hA : A 1 = -25) (hd : DoubCanon A) (g : Nat) :
    ∃ n, 1 ≤ n ∧ steps n (M6d A g) = some (M1d A (g+1)) := by
  by_cases hg : g = 0
  · subst hg; exact h_doub_d_zero A hA
  · obtain ⟨n, hn, hrun⟩ := hd g (by omega)
    refine ⟨n, hn, ?_⟩
    unfold M6d M1d M6a M1a
    rw [if_neg hg, if_neg (show ¬ (g+1 = 0) from by omega),
        cfgPos (s := St.E) (t := ⟨[false], false, (M6 g).tape.right ++ [false]⟩)
          (show A g - 5 = -5 + A g from by omega),
        cfgPos (s := St.E) (t := ⟨[false], false, (M1 (g+1)).tape.right ++ [false]⟩)
          (show A (g+1) = (A (g+1) - A g) + A g from by omega)]
    exact steps_pos_shift (d := A g) hrun

/-- **THE ASSEMBLY.**  `x2` never halts from the blank tape, PROVIDED `DoubCanon A` for some anchor
function with `A 1 = −25`.  `h_init` and `h_low ∀g` are now THEOREMS for the SAME family
(`M1d A`/`M6d A`) — obligation H (T9) is closed on those two axes, and `DoubCanon` is the single
remaining input. -/
theorem x2_nonhalt_of_DoubCanon (A : Nat → Int) (hA : A 1 = -25) (hd : DoubCanon A) :
    ∀ N, steps N init ≠ none :=
  x2_nonhalt (M1d A) (M6d A) (h_init_d A hA) (h_low_d A) (h_doub_d A hA hd)

#print axioms doubCanon_of_tailparam
#print axioms h_doub_d_zero
#print axioms h_doub_d
#print axioms x2_nonhalt_of_DoubCanon

/-! ## §6 CONTROLS — statements that MUST fail, each verified rejected by the kernel in a scratch
probe (kept as comments; uncommenting any of them breaks the build, which is the point).

* `lmerge` one step earlier — REJECTED (`Type mismatch`), so the absorption really lands at 11:
    `steps 10 ⟨.E,p,⟨[false],false,0^5++Z⟩⟩ = steps 10 ⟨.E,p,⟨[],false,0^5++Z⟩⟩ := rfl`
* `h_low_g1_a` with the left blank RIDING instead of absorbed (target `left = [false,false]`) —
  REJECTED, confirming `M6a`'s `left = [false]` is measured, not chosen:
    `steps 343 (M1a (-25) 1) = some ⟨.E,-30,⟨[false,false],false,(M6 1).tape.right ++ [false]⟩⟩`
* the low-phase displacement off by one (`−4` instead of the proved `−5`) — REJECTED:
    `steps 343 (M1a (-25) 1) = some ⟨.E,-29,⟨[false],false,(M6 1).tape.right ++ [false]⟩⟩`
* `h_low` at `g = 0` for the §5am families — the `#eval` below returns `[]`: there is NO
  `n < 700` with `steps n (M1 0) = some (M6 0)`.  Hence the index-`0` pre-history slot. -/

-- Live `#eval` audits (kernel-executed at every build):
#eval decide (M1a (-25) 1 = HInit.c189)                                          -- true
#eval decide (steps 343 (M1a (-25) 1) = some (M6a (-25) 1))                      -- true
#eval ((List.range 700).filter (fun n => decide (steps n (M1 1) = some (M6 1)))) -- [343]
#eval ((List.range 700).filter (fun n => decide (steps n (M1 0) = some (M6 0)))) -- []  (g=0 is no generation)

end Realize
