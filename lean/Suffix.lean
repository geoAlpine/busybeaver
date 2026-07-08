import Template

/-!
# The o4 suffix lemmas and the FULL GENERATION MAP — Lean 4 formalization

Extends `Template.lean` (machine `step`/`steps`, sweeps `B1F0`/`D1E0`, body,
prefix) to the SUFFIX layer of the certified trace-template method
(`O4_TEMPLATE_CLOSURE_2026-07-06.md` §2), and composes everything into the
full generation map `M(G, a) → M(⌊4G/3⌋ + c(G mod 3), a + δ(G mod 3))` —
the base-4/3 odometer and the a-ledger law, derived inside Lean.

Conventions (all consistent with `Template.lean`):
* filler convention: `Mcfg G a p = 0^∞ [E] 0^G (10)^a 01 0^∞`, so the Lean
  filler count `a` equals the LAB convention (`O4_TEMPLATE_CLOSURE` §4,
  a = 34, 38, 37 … on the real orbit) and equals the `o4_bouncer_macro` /
  `o4_redteam_suffix.py` Python count PLUS ONE
  (`(10)^a 01 = (10)^(a_py) 1001`, `a = a_py + 1`).
* `Z(k, g, a) = 0^∞ [E] (10)^k 1001 0^g (10)^a 01 0^∞` (head on the zone's
  leading 1, state `E`) is the suffix-entry configuration; it is literally
  `BcfgCtx k p (0^g ++ filler)`, the landing shape of `prefix_bodies`.

The three suffix classes (gap-at-meet `g ∈ {3,4,5}`, `g ≡ G−31 (mod 3)`),
Lean-filler convention:

| class | Lean theorem | steps | landing |
|---|---|---|---|
| g=3 | `suffix_g3`  (all `k`, filler `a+1 ≥ 1`) | `8k+35` | `M(2k+12, a, p−3)` |
| g=4 | `suffix_g4`  (all `k`, filler `a+1 ≥ 1`) | `8k+8a+71` | `M(2k+9, a+5, p−3)` |
| g=5 | `suffix_g5`  (all `k`, filler `b+2 ≥ 2`) | `12k+16b+164` | `M(2k+13, b+8, p−4)` |
| g=5 | `suffix_g5_small` (all `k`, filler `= 1`) | `12k+148` | `M(2k+13, 7, p−4)` |

Statement deltas vs the lab record (all sound, all machine-checked):
* the lab's validity floors (`a_py ≥ 2` at g=3) are ITERABILITY floors; the
  suffix lemmas themselves hold down to Lean filler 1 (= `a_py ≥ 0`) for
  g=3/g=4, and the g=5 small-filler case gets its own template
  (`suffix_g5_small`).  In particular `Z(41, 3, 0)_py = Zcfg 41 3 1` DOES
  land — on the degenerate milestone `M(94, 0)` (filler `01`), from which
  the NEXT generation's template fails (the lab-observed halt at 55,170
  happens downstream of this landing).
* the lab's per-`a` small-parameter templates (`a_py ≤ 4`) are absorbed:
  the sweep inductions hold for every length `≥ 0`, so one parametric
  proof per class covers them (only g=5 `a_py = 0` differs structurally).

The generation map (`gen_mod1`/`gen_mod2`/`gen_mod0`/`gen_mod0_small`,
master `generation_odometer`): for every `G ≥ 34` (all residues), every
filler `≥ 1`, `M(G, a) → M(4G/3 + c, a + δ)` with exact step counts —
`c = {G≡0: 3, G≡1: 5, G≡2: 1}`, `δ = {G≡1: −1, G≡2: +4, G≡0: +6}`.
The residual open content of the o4 decision is EXACTLY the a-ledger
conjecture (does the ledger stay ≥ 2 before every G≡1 generation?);
nothing else remains informal.  **This file decides no machine; o4 stays
`[OPEN]`.**

Dependency-free (imports only `Template`); no `sorry`, no `native_decide`.
-/

namespace Template

/-! ## §1 The suffix-entry configuration `Z(k, g, a)` and word helpers. -/

/-- `Z(k, g, a) = 0^∞ [E] (10)^k 1001 0^g (10)^a 01 0^∞`, head (state `E`)
on the zone's leading 1 at absolute position `p`.  Definitionally the
`BcfgCtx` landing shape of `prefix_bodies` with `g` leftover gap zeros. -/
def Zcfg (k g a : Nat) (p : Int) : Cfg :=
  BcfgCtx k p (List.replicate g false ++ (pow10 a ++ [false, true]))

/-- Reading `0 · (10)^j` shifted: `0 (10)^j X = (01)^j 0 X`. -/
theorem pow10_to_pow01 : ∀ (j : Nat) (X : List Bool),
    false :: (pow10 j ++ X) = pow01 j ++ (false :: X) := by
  intro j
  induction j with
  | zero => intro X; rfl
  | succ j ih =>
    intro X
    show false :: true :: (false :: (pow10 j ++ X))
        = false :: true :: (pow01 j ++ (false :: X))
    rw [ih]

/-- A leading matching cell commutes past a replicate block. -/
theorem replicate_shift (n : Nat) (b : Bool) (l : List Bool) :
    List.replicate n b ++ (b :: l) = b :: (List.replicate n b ++ l) := by
  induction n with
  | zero => rfl
  | succ n ih =>
    show b :: (List.replicate n b ++ (b :: l)) = b :: b :: (List.replicate n b ++ l)
    rw [ih]

theorem Mcfg_congr {G G' a a' : Nat} {p q : Int}
    (hG : G = G') (ha : a = a') (hp : p = q) : Mcfg G a p = Mcfg G' a' q := by
  rw [hG, ha, hp]

/-! ## §2 The third sweep: the `A1D0` leftward ERASER, arbitrary length.

From state `A` on a `1` whose left context is `(01)^j`, the 2-cycle
`A:1→0LD · D:0→0LA` marches left, ZEROING the whole block: `(01)^j` on the
left becomes `0^{2j}` on the right.  This is the sweep that converts the
old zone into the next generation's gap. -/

theorem sweepAD : ∀ (j : Nat) (p : Int) (L R : List Bool),
    steps (2 * j) ⟨.A, p, ⟨pow01 j ++ L, true, R⟩⟩
      = some ⟨.A, p - 2 * (j : Int), ⟨L, true, List.replicate (2 * j) false ++ R⟩⟩ := by
  intro j
  induction j with
  | zero =>
    intro p L R
    exact congrArg some (cfgPos (by omega))
  | succ j ih =>
    intro p L R
    have hn : 2 * (j + 1) = 2 * j + 2 := by omega
    rw [hn]
    have h2 : steps (2 * j + 2) (⟨.A, p, ⟨pow01 (j + 1) ++ L, true, R⟩⟩ : Cfg)
        = steps (2 * j) ⟨.A, p - 1 - 1, ⟨pow01 j ++ L, true, false :: false :: R⟩⟩ := rfl
    rw [h2, ih (p - 1 - 1) L (false :: false :: R)]
    have ht : List.replicate (2 * j) false ++ (false :: false :: R)
        = List.replicate (2 * j + 2) false ++ R := by
      rw [replicate_shift, replicate_shift]; rfl
    rw [ht]
    exact congrArg some (cfgPos (by omega))

/-! ## §3 The suffix episodes (fixed bounded words, kernel-checked). -/

/-- Finisher (2 steps): `A1 · D1` — the eraser runs off the zone's left
edge onto the two turn cells, landing in state `E` on blank tape: the
milestone head position. -/
theorem fin2 (q : Int) (R : List Bool) :
    steps 2 ⟨.A, q, ⟨[true], true, R⟩⟩
      = some ⟨.E, q - 1 - 1, ⟨[], false, false :: false :: R⟩⟩ := rfl

/-- Seam drop (2 steps): `D1 · E1` — off a double-1 seam into the eraser
entry (state `A` on the second 1, first 1 re-queued right). -/
theorem ep2DA (q : Int) (L R : List Bool) :
    steps 2 ⟨.D, q, ⟨true :: true :: L, true, R⟩⟩
      = some ⟨.A, q - 1 - 1, ⟨L, true, true :: false :: R⟩⟩ := rfl

/-- Triple-1 turn (3 steps): `D1 · E1 · A1` — crosses a triple-1 seam
leftward, re-entering state `D` (g=5 mid-suffix turn). -/
theorem turn3A1 (q : Int) (L R : List Bool) :
    steps 3 ⟨.D, q, ⟨true :: true :: true :: L, true, R⟩⟩
      = some ⟨.D, q - 1 - 1 - 1, ⟨L, true, false :: true :: false :: R⟩⟩ := rfl

/-- Interior left turn (3 steps): `D1 · E1 · A0` — the filler-edge turn
(like `outro1 · intro2` but on a non-blank left context `1 0 …`). -/
theorem turnL3_int (q : Int) (L R : List Bool) :
    steps 3 ⟨.D, q, ⟨true :: false :: L, true, R⟩⟩
      = some ⟨.B, q - 1 - 1 + 1, ⟨true :: L, true, false :: R⟩⟩ := rfl

/-- Cap entry (4 steps): `B1 · F0 · B0 · C1` — crosses the `1001` cap into
the filler's leading 1, entering state `A`: the g=3 eraser hand-off. -/
theorem capEnter4 (q : Int) (L R : List Bool) :
    steps 4 ⟨.B, q, ⟨L, true, false :: false :: true :: (true :: R)⟩⟩
      = some ⟨.A, q + 1 + 1 + 1 + 1, ⟨false :: true :: false :: true :: L, true, R⟩⟩ := rfl

/-- Gap skip (5 steps): `B1 · F0 · B0 · C1 · A0` — crosses the cap plus ONE
extra gap zero onto the filler's leading 1, state `B` (g=4 filler entry). -/
theorem gapSkip5 (q : Int) (L R : List Bool) :
    steps 5 ⟨.B, q, ⟨L, true, false :: false :: true :: false :: (true :: R)⟩⟩
      = some ⟨.B, q + 1 + 1 + 1 + 1 + 1,
          ⟨true :: false :: true :: false :: true :: L, true, R⟩⟩ := rfl

/-- Gap seam (8 steps): `B1·F0·B0·C1·A0·B0·C1·A0` — crosses the cap plus
TWO extra gap zeros and the filler's first pair, state `B` on the filler's
second 1 (g=5 filler entry; note the double-1 it leaves at the meet). -/
theorem seamGap8 (q : Int) (L R : List Bool) :
    steps 8 ⟨.B, q,
        ⟨L, true, false :: false :: true :: false :: false :: (true :: false :: (true :: R))⟩⟩
      = some ⟨.B, q + 1 + 1 + 1 + 1 + 1 + 1 + 1 + 1,
          ⟨true :: false :: true :: true :: false :: true :: false :: true :: L, true, R⟩⟩ := rfl

/-! ## §4 The g = 3 suffix (`SUFFIX` class table row 1), fully parametric.

`Z(k, 3, a+1) → M(2k+12, a)` shifted −3, in exactly `8k + 35` steps, for
EVERY `k` and EVERY filler `a + 1 ≥ 1` — episodes `intro2 · seam8 ·
(outro1·intro2) · capEnter4 · fin2` glued by sweeps `B1F0(k) · D1E0(k+2) ·
B1F0(k+2) · A1D0(k+4)`.  The g=3 suffix touches the filler ONLY at its
leading 1 (consumed by the eraser): that is the whole `a′ = a − 1` ledger
mechanism, now a kernel fact. -/

theorem suffix_g3 (k a : Nat) (p : Int) :
    steps (8 * k + 35) (Zcfg k 3 (a + 1) p)
      = some (Mcfg (2 * k + 12) a (p - 3)) := by
  have hsplit : 8 * k + 35
      = 2 + (2 * k + (8 + (2 * (k + 2) + (1 + (2 + (2 * (k + 2)
        + (4 + (2 * (k + 4) + 2)))))))) := by omega
  show steps (8 * k + 35) ⟨.E, p, ⟨[], true, pow01 k ++ ([false, false, true]
      ++ (List.replicate 3 false ++ (pow10 (a + 1) ++ [false, true])))⟩⟩ = _
  rw [hsplit, steps_add, intro2W, someBind, steps_add, sweepBF, someBind, steps_add]
  have hc : ([false, false, true]
        ++ (List.replicate 3 false ++ (pow10 (a + 1) ++ [false, true])) : List Bool)
      = false :: false :: true :: false :: false :: false
        :: (pow10 (a + 1) ++ [false, true]) := rfl
  rw [hc, seam8_ctx, someBind]
  have hL1 : false :: true :: false :: true :: (pow01 k ++ [true])
      = pow01 (k + 2) ++ [true] := rfl
  rw [hL1, steps_add, sweepDE, someBind, steps_add, outro1, someBind,
      steps_add, intro2W, someBind, steps_add]
  have hW : false :: (pow10 (k + 2) ++ (false :: true :: (pow10 (a + 1) ++ [false, true])))
      = pow01 (k + 2) ++ (false :: false :: true :: (pow10 (a + 1) ++ [false, true])) :=
    pow10_to_pow01 (k + 2) _
  rw [hW, sweepBF, someBind, steps_add]
  have hf : (false :: false :: true :: (pow10 (a + 1) ++ [false, true]) : List Bool)
      = false :: false :: true :: (true :: (false :: (pow10 a ++ [false, true]))) := rfl
  rw [hf, capEnter4, someBind]
  have hL2 : false :: true :: false :: true :: (pow01 (k + 2) ++ [true])
      = pow01 (k + 4) ++ [true] := rfl
  rw [hL2, steps_add, sweepAD, someBind, fin2]
  have htape : (false :: false :: (List.replicate (2 * (k + 4)) false
        ++ (false :: (pow10 a ++ [false, true]))) : List Bool)
      = List.replicate (2 * k + 12 - 1) false ++ (pow10 a ++ [false, true]) := by
    rw [replicate_shift, show 2 * k + 12 - 1 = 2 * (k + 4) + 3 from by omega]; rfl
  rw [htape]
  exact congrArg some (cfgPos (by omega))

/-! ### §4a sanity anchors (kernel-executed at every build) -/

-- Python `o4_redteam_suffix.py` grid point Z(19,3,4): 187 steps, M(50, 3_py).
#eval decide (steps (8 * 19 + 35) (Zcfg 19 3 5 0) = some (Mcfg 50 4 (-3)))
-- the red-team point k = 251:
#eval decide (steps (8 * 251 + 35) (Zcfg 251 3 9 0) = some (Mcfg 514 8 (-3)))
-- the Z(41,3,0)_py landing (degenerate milestone; the lab halt at 55,170 is downstream):
#eval decide (steps (8 * 41 + 35) (Zcfg 41 3 1 0) = some (Mcfg 94 0 (-3)))

/-! ## §5 The g = 4 suffix (class table row 2), fully parametric.

`Z(k, 4, a+1) → M(2k+9, a+5)` shifted −3, in exactly `8k + 8a + 71`
steps, for EVERY `k` and EVERY filler `a + 1 ≥ 1` — this class CROSSES
the filler: two `B1F0`-out/`D1E0`-back round trips over it (`gapSkip5 ·
seam8` then `turnL3_int · seam8`), each rebuilding the filler two pairs
longer, before the `A1D0` eraser converts the zone.  The lab's per-`a`
small templates (`a_py ≤ 4`) are absorbed: every sweep length is `≥ 0`
already at filler 1. -/

theorem suffix_g4 (k a : Nat) (p : Int) :
    steps (8 * k + 8 * a + 71) (Zcfg k 4 (a + 1) p)
      = some (Mcfg (2 * k + 9) (a + 5) (p - 3)) := by
  have hsplit : 8 * k + 8 * a + 71
      = 2 + (2 * k + (8 + (2 * (k + 2) + (1 + (2 + (2 * (k + 2)
        + (5 + (2 * a + (8 + (2 * (a + 2) + (3 + (2 * (a + 2)
        + (8 + (2 * (a + 4) + (2 + (2 * (k + 3) + 2)))))))))))))))) := by omega
  show steps (8 * k + 8 * a + 71) ⟨.E, p, ⟨[], true, pow01 k ++ ([false, false, true]
      ++ (List.replicate 4 false ++ (pow10 (a + 1) ++ [false, true])))⟩⟩ = _
  rw [hsplit, steps_add, intro2W, someBind, steps_add, sweepBF, someBind, steps_add]
  have hc : ([false, false, true]
        ++ (List.replicate 4 false ++ (pow10 (a + 1) ++ [false, true])) : List Bool)
      = false :: false :: true :: false :: false :: false
        :: (false :: (pow10 (a + 1) ++ [false, true])) := rfl
  rw [hc, seam8_ctx, someBind]
  have hL1 : false :: true :: false :: true :: (pow01 k ++ [true])
      = pow01 (k + 2) ++ [true] := rfl
  rw [hL1, steps_add, sweepDE, someBind, steps_add, outro1, someBind,
      steps_add, intro2W, someBind, steps_add]
  have hW : false :: (pow10 (k + 2)
        ++ (false :: true :: false :: (pow10 (a + 1) ++ [false, true])))
      = pow01 (k + 2)
        ++ (false :: false :: true :: false :: (pow10 (a + 1) ++ [false, true])) :=
    pow10_to_pow01 (k + 2) _
  rw [hW, sweepBF, someBind, steps_add]
  have hg : (false :: false :: true :: false :: (pow10 (a + 1) ++ [false, true]) : List Bool)
      = false :: false :: true :: false
        :: (true :: (false :: (pow10 a ++ [false, true]))) := rfl
  rw [hg, gapSkip5, someBind]
  have hLa : (true :: false :: true :: false :: true :: (pow01 (k + 2) ++ [true]) : List Bool)
      = true :: (pow01 (k + 4) ++ [true]) := rfl
  have hra : false :: (pow10 a ++ [false, true])
      = pow01 a ++ (false :: [false, true]) := pow10_to_pow01 a _
  rw [hLa, hra, steps_add, sweepBF, someBind, steps_add, seam8, someBind]
  have hLb : (false :: true :: false :: true
        :: (pow01 a ++ (true :: (pow01 (k + 4) ++ [true]))) : List Bool)
      = pow01 (a + 2) ++ (true :: (pow01 (k + 4) ++ [true])) := rfl
  rw [hLb, steps_add, sweepDE, someBind, steps_add]
  have hLc : (true :: (pow01 (k + 4) ++ [true]) : List Bool)
      = true :: false :: (true :: (pow01 (k + 3) ++ [true])) := rfl
  rw [hLc, turnL3_int, someBind]
  have hrb : false :: (pow10 (a + 2) ++ [false, true])
      = pow01 (a + 2) ++ (false :: [false, true]) := pow10_to_pow01 (a + 2) _
  rw [hrb, steps_add, sweepBF, someBind, steps_add, seam8, someBind]
  have hLd : (false :: true :: false :: true
        :: (pow01 (a + 2) ++ (true :: (true :: (pow01 (k + 3) ++ [true])))) : List Bool)
      = pow01 (a + 4) ++ (true :: true :: (pow01 (k + 3) ++ [true])) := rfl
  rw [hLd, steps_add, sweepDE, someBind, steps_add, ep2DA, someBind]
  have hrc : (true :: false :: (pow10 (a + 4) ++ [false, true]) : List Bool)
      = pow10 (a + 5) ++ [false, true] := rfl
  rw [hrc, steps_add, sweepAD, someBind, fin2]
  have htape : (false :: false :: (List.replicate (2 * (k + 3)) false
        ++ (pow10 (a + 5) ++ [false, true])) : List Bool)
      = List.replicate (2 * k + 9 - 1) false ++ (pow10 (a + 5) ++ [false, true]) := by
    rw [show 2 * k + 9 - 1 = 2 * (k + 3) + 2 from by omega]; rfl
  rw [htape]
  exact congrArg some (cfgPos (by omega))

-- Python grid point Z(19,4,8): 8·19+8·8+71 = 287 steps, M(47, 12_py).
#eval decide (steps (8 * 19 + 8 * 8 + 71) (Zcfg 19 4 9 0) = some (Mcfg 47 13 (-3)))
-- Python small-a point Z(21,4,0) (223+16 = 239 steps): the per-a case, absorbed.
#eval decide (steps (8 * 21 + 8 * 0 + 71) (Zcfg 21 4 1 0) = some (Mcfg 51 5 (-3)))

/-! ## §6 The g = 5 suffix (class table row 3): generic filler ≥ 2, plus
the structurally-different filler-1 template (the lab's `a_py = 0`
per-parameter case).

Generic: `Z(k, 5, b+2) → M(2k+13, b+8)` shifted −4, in exactly
`12k + 16b + 164` steps — the longest class: TWO filler sections
(`seamGap8`, then after a full return trip over the zone, `gapSkip5`),
four filler round trips total, the `turn3A1` triple-1 mid-turn, and the
`A1D0` eraser. -/

theorem suffix_g5 (k b : Nat) (p : Int) :
    steps (12 * k + 16 * b + 164) (Zcfg k 5 (b + 2) p)
      = some (Mcfg (2 * k + 13) (b + 8) (p - 4)) := by
  have hsplit : 12 * k + 16 * b + 164
      = 2 + (2 * k + (8 + (2 * (k + 2) + (1 + (2 + (2 * (k + 2) + (8
        + (2 * b + (8 + (2 * (b + 2) + (3 + (2 * (b + 2) + (8
        + (2 * (b + 4) + (3 + (2 * (k + 4) + (1 + (2 + (2 * (k + 4)
        + (5 + (2 * (b + 3) + (8 + (2 * (b + 5) + (3 + (2 * (b + 5)
        + (8 + (2 * (b + 7) + (2 + (2 * (k + 5)
        + (2)))))))))))))))))))))))))))))) := by omega
  show steps (12 * k + 16 * b + 164) ⟨.E, p, ⟨[], true, pow01 k ++ ([false, false, true]
      ++ (List.replicate 5 false ++ (pow10 (b + 2) ++ [false, true])))⟩⟩ = _
  rw [hsplit, steps_add, intro2W, someBind, steps_add, sweepBF, someBind, steps_add]
  have hc : ([false, false, true]
        ++ (List.replicate 5 false ++ (pow10 (b + 2) ++ [false, true])) : List Bool)
      = false :: false :: true :: false :: false :: false
        :: (false :: false :: (pow10 (b + 2) ++ [false, true])) := rfl
  rw [hc, seam8_ctx, someBind]
  have hL1 : false :: true :: false :: true :: (pow01 k ++ [true])
      = pow01 (k + 2) ++ [true] := rfl
  rw [hL1, steps_add, sweepDE, someBind, steps_add, outro1, someBind,
      steps_add, intro2W, someBind, steps_add]
  have hW : false :: (pow10 (k + 2)
        ++ (false :: true :: false :: false :: (pow10 (b + 2) ++ [false, true])))
      = pow01 (k + 2)
        ++ (false :: false :: true :: false :: false :: (pow10 (b + 2) ++ [false, true])) :=
    pow10_to_pow01 (k + 2) _
  rw [hW, sweepBF, someBind, steps_add]
  have hg : (false :: false :: true :: false :: false
        :: (pow10 (b + 2) ++ [false, true]) : List Bool)
      = false :: false :: true :: false :: false
        :: (true :: false :: (true :: (false :: (pow10 b ++ [false, true])))) := rfl
  rw [hg, seamGap8, someBind]
  have hra : false :: (pow10 b ++ [false, true])
      = pow01 b ++ (false :: [false, true]) := pow10_to_pow01 b _
  rw [hra, steps_add, sweepBF, someBind, steps_add, seam8, someBind]
  have hLa : (false :: true :: false :: true :: (pow01 b
        ++ (true :: false :: true :: true :: false :: true :: false :: true
          :: (pow01 (k + 2) ++ [true]))) : List Bool)
      = pow01 (b + 2) ++ (true :: false :: true :: true :: false :: true :: false :: true
          :: (pow01 (k + 2) ++ [true])) := rfl
  rw [hLa, steps_add, sweepDE, someBind, steps_add, turnL3_int, someBind]
  have hrb : false :: (pow10 (b + 2) ++ [false, true])
      = pow01 (b + 2) ++ (false :: [false, true]) := pow10_to_pow01 (b + 2) _
  rw [hrb, steps_add, sweepBF, someBind, steps_add, seam8, someBind]
  have hLb : (false :: true :: false :: true :: (pow01 (b + 2)
        ++ (true :: (true :: true :: false :: true :: false :: true
          :: (pow01 (k + 2) ++ [true])))) : List Bool)
      = pow01 (b + 4) ++ (true :: true :: true
          :: (false :: true :: false :: true :: (pow01 (k + 2) ++ [true]))) := rfl
  rw [hLb, steps_add, sweepDE, someBind, steps_add, turn3A1, someBind]
  have hLc : (false :: true :: false :: true :: (pow01 (k + 2) ++ [true]) : List Bool)
      = pow01 (k + 4) ++ [true] := rfl
  have hrc : (false :: true :: false :: (pow10 (b + 4) ++ [false, true]) : List Bool)
      = false :: (pow10 (b + 5) ++ [false, true]) := rfl
  rw [hLc, hrc, steps_add, sweepDE, someBind, steps_add, outro1, someBind,
      steps_add, intro2W, someBind, steps_add]
  have hW2 : false :: (pow10 (k + 4) ++ (false :: (pow10 (b + 5) ++ [false, true])))
      = pow01 (k + 4) ++ (false :: false :: (pow10 (b + 5) ++ [false, true])) :=
    pow10_to_pow01 (k + 4) _
  rw [hW2, sweepBF, someBind, steps_add]
  have hg2 : (false :: false :: (pow10 (b + 5) ++ [false, true]) : List Bool)
      = false :: false :: true :: false
        :: (true :: (false :: (pow10 (b + 3) ++ [false, true]))) := rfl
  rw [hg2, gapSkip5, someBind]
  have hLd : (true :: false :: true :: false :: true :: (pow01 (k + 4) ++ [true]) : List Bool)
      = true :: (pow01 (k + 6) ++ [true]) := rfl
  have hrd : false :: (pow10 (b + 3) ++ [false, true])
      = pow01 (b + 3) ++ (false :: [false, true]) := pow10_to_pow01 (b + 3) _
  rw [hLd, hrd, steps_add, sweepBF, someBind, steps_add, seam8, someBind]
  have hLe : (false :: true :: false :: true :: (pow01 (b + 3)
        ++ (true :: (pow01 (k + 6) ++ [true]))) : List Bool)
      = pow01 (b + 5) ++ (true :: (pow01 (k + 6) ++ [true])) := rfl
  rw [hLe, steps_add, sweepDE, someBind, steps_add]
  have hLf : (true :: (pow01 (k + 6) ++ [true]) : List Bool)
      = true :: false :: (true :: (pow01 (k + 5) ++ [true])) := rfl
  rw [hLf, turnL3_int, someBind]
  have hre : false :: (pow10 (b + 5) ++ [false, true])
      = pow01 (b + 5) ++ (false :: [false, true]) := pow10_to_pow01 (b + 5) _
  rw [hre, steps_add, sweepBF, someBind, steps_add, seam8, someBind]
  have hLg : (false :: true :: false :: true :: (pow01 (b + 5)
        ++ (true :: (true :: (pow01 (k + 5) ++ [true])))) : List Bool)
      = pow01 (b + 7) ++ (true :: true :: (pow01 (k + 5) ++ [true])) := rfl
  rw [hLg, steps_add, sweepDE, someBind, steps_add, ep2DA, someBind]
  have hrf : (true :: false :: (pow10 (b + 7) ++ [false, true]) : List Bool)
      = pow10 (b + 8) ++ [false, true] := rfl
  rw [hrf, steps_add, sweepAD, someBind, fin2]
  have htape : (false :: false :: (List.replicate (2 * (k + 5)) false
        ++ (pow10 (b + 8) ++ [false, true])) : List Bool)
      = List.replicate (2 * k + 13 - 1) false ++ (pow10 (b + 8) ++ [false, true]) := by
    rw [show 2 * k + 13 - 1 = 2 * (k + 5) + 2 from by omega]; rfl
  rw [htape]
  exact congrArg some (cfgPos (by omega))

-- Python grid point Z(23,5,8): 12·23+16·7+164 = 552 steps, M(59, 14_py).
#eval decide (steps (12 * 23 + 16 * 7 + 164) (Zcfg 23 5 9 0) = some (Mcfg 59 15 (-4)))

/-! ### §6a the g = 5 filler-1 template (the lab's genuine per-parameter
case: at `a_py = 0` the first filler section degenerates and the skeleton
changes).  Two fixed episode words (38 and 58 steps, kernel-checked with
symbolic left context) + the SAME four zone sweeps. -/

/-- Position-anchored run lifted to an arbitrary base position. -/
theorem steps_at {n : Nat} {s s' : St} {d : Int} {t t' : Tape}
    (h : steps n ⟨s, 0, t⟩ = some ⟨s', d, t'⟩) (q : Int) :
    steps n ⟨s, q, t⟩ = some ⟨s', d + q, t'⟩ := by
  have h0 : (⟨s, q, t⟩ : Cfg) = ⟨s, (0 : Int) + q, t⟩ := cfgPos (by omega)
  rw [h0, steps_shift q n s 0 t, h]
  rfl

set_option maxRecDepth 8000 in
set_option maxHeartbeats 2000000 in
/-- g=5 filler-1, first filler section (38 fixed steps): from the zone
seam over gap `0^5` and filler `1001`, back to the zone's right edge in
state `D` — leaves `(01)^2` above the untouched left context `L` and the
filler area recoded as `(01)^4 001`. -/
theorem epi38_base (L : List Bool) :
    steps 38 ⟨.B, 0, ⟨L, true,
        [false, false, true, false, false, true, false, false, true]⟩⟩
      = some ⟨.D, 4, ⟨false :: true :: false :: true :: L, true,
          [false, true, false, true, false, true, false, true, false, false, true]⟩⟩ := rfl

theorem epi38 (q : Int) (L : List Bool) :
    steps 38 ⟨.B, q, ⟨L, true,
        [false, false, true, false, false, true, false, false, true]⟩⟩
      = some ⟨.D, 4 + q, ⟨false :: true :: false :: true :: L, true,
          [false, true, false, true, false, true, false, true, false, false, true]⟩⟩ :=
  steps_at (epi38_base L) q

set_option maxRecDepth 8000 in
set_option maxHeartbeats 2000000 in
/-- g=5 filler-1, second filler section (58 fixed steps): builds the final
filler `(10)^7 01` and hands off to the `A1D0` eraser (state `A`, a `01`
pair above the untouched left context). -/
theorem epi58_base (L : List Bool) :
    steps 58 ⟨.B, 0, ⟨L, true,
        [false, false, true, false, true, false, true, false, true, false, false, true]⟩⟩
      = some ⟨.A, 2, ⟨false :: true :: L, true,
          [true, false, true, false, true, false, true, false, true, false, true, false,
           true, false, false, true]⟩⟩ := rfl

theorem epi58 (q : Int) (L : List Bool) :
    steps 58 ⟨.B, q, ⟨L, true,
        [false, false, true, false, true, false, true, false, true, false, false, true]⟩⟩
      = some ⟨.A, 2 + q, ⟨false :: true :: L, true,
          [true, false, true, false, true, false, true, false, true, false, true, false,
           true, false, false, true]⟩⟩ :=
  steps_at (epi58_base L) q

/-- The g = 5 suffix at filler 1 (`a_py = 0`): `Z(k, 5, 1) → M(2k+13, 7)`
shifted −4, in exactly `12k + 148` steps, for EVERY `k`. -/
theorem suffix_g5_small (k : Nat) (p : Int) :
    steps (12 * k + 148) (Zcfg k 5 1 p)
      = some (Mcfg (2 * k + 13) 7 (p - 4)) := by
  have hsplit : 12 * k + 148
      = 2 + (2 * k + (8 + (2 * (k + 2) + (1 + (2 + (2 * (k + 2)
        + (38 + (2 * (k + 4) + (1 + (2 + (2 * (k + 4)
        + (58 + (2 * (k + 5) + 2))))))))))))) := by omega
  show steps (12 * k + 148) ⟨.E, p, ⟨[], true, pow01 k ++ ([false, false, true]
      ++ (List.replicate 5 false ++ (pow10 1 ++ [false, true])))⟩⟩ = _
  rw [hsplit, steps_add, intro2W, someBind, steps_add, sweepBF, someBind, steps_add]
  have hc : ([false, false, true]
        ++ (List.replicate 5 false ++ (pow10 1 ++ [false, true])) : List Bool)
      = false :: false :: true :: false :: false :: false
        :: ([false, false, true, false, false, true] : List Bool) := rfl
  rw [hc, seam8_ctx, someBind]
  have hL1 : false :: true :: false :: true :: (pow01 k ++ [true])
      = pow01 (k + 2) ++ [true] := rfl
  rw [hL1, steps_add, sweepDE, someBind, steps_add, outro1, someBind,
      steps_add, intro2W, someBind, steps_add]
  have hW : false :: (pow10 (k + 2)
        ++ (false :: true :: ([false, false, true, false, false, true] : List Bool)))
      = pow01 (k + 2)
        ++ (false :: false :: true :: ([false, false, true, false, false, true] : List Bool)) :=
    pow10_to_pow01 (k + 2) _
  rw [hW, sweepBF, someBind, steps_add, epi38, someBind, steps_add]
  have hL2 : (false :: true :: false :: true :: (pow01 (k + 2) ++ [true]) : List Bool)
      = pow01 (k + 4) ++ [true] := rfl
  rw [hL2, sweepDE, someBind, steps_add, outro1, someBind, steps_add,
      intro2W, someBind, steps_add]
  have hW2 : false :: (pow10 (k + 4)
        ++ ([false, true, false, true, false, true, false, true, false, false, true] : List Bool))
      = pow01 (k + 4) ++ (false
          :: ([false, true, false, true, false, true, false, true, false, false, true]
            : List Bool)) :=
    pow10_to_pow01 (k + 4) _
  rw [hW2, sweepBF, someBind, steps_add, epi58, someBind, steps_add]
  have hL3 : (false :: true :: (pow01 (k + 4) ++ [true]) : List Bool)
      = pow01 (k + 5) ++ [true] := rfl
  rw [hL3, sweepAD, someBind, fin2]
  have htape : (false :: false :: (List.replicate (2 * (k + 5)) false
        ++ ([true, false, true, false, true, false, true, false, true, false, true, false,
             true, false, false, true] : List Bool)) : List Bool)
      = List.replicate (2 * k + 13 - 1) false ++ (pow10 7 ++ [false, true]) := by
    rw [show 2 * k + 13 - 1 = 2 * (k + 5) + 2 from by omega]; rfl
  rw [htape]
  exact congrArg some (cfgPos (by omega))

-- Python point Z(19,5,0): 376 steps, M(51, 6_py) — the per-a case, now parametric in k.
#eval decide (steps (12 * 19 + 148) (Zcfg 19 5 1 0) = some (Mcfg 51 7 (-4)))

/-! ## §7 THE GENERATION MAP (S4): `prefix471 · body^s · suffix_g`
composed — `M(G, a) → M(G', a')` with exact step counts, for every
`G ≥ 34` and every filler `≥ 1` (all three residue classes; the leftover
gap `G − 31 − 3s ∈ {3,4,5}` selects the suffix class).  The base-4/3
odometer and the a-ledger law fall out below (`generation_odometer`). -/

/-- Generation, class `G ≡ 1 (mod 3)` (`G = 34 + 3s`, suffix g=3):
`M(G, a+1) → M(50+4s, a)` shifted `−14−s`.  The LEDGER DRAIN class:
filler count drops by exactly 1. -/
theorem gen_mod1 (s a : Nat) (p : Int) :
    steps ((471 + bodyTime s 19) + (8 * (19 + 2 * s) + 35))
        (Mcfg (34 + 3 * s) (a + 1) p)
      = some (Mcfg (50 + 4 * s) a (p - 14 - (s : Int))) := by
  rw [steps_add, prefix_bodies (34 + 3 * s) (a + 1) s p (by omega), someBind]
  rw [show 34 + 3 * s - 31 - 3 * s = 3 from by omega]
  rw [show BcfgCtx (19 + 2 * s) (p - 11 - (s : Int))
        (List.replicate 3 false ++ (pow10 (a + 1) ++ [false, true]))
      = Zcfg (19 + 2 * s) 3 (a + 1) (p - 11 - (s : Int)) from rfl]
  rw [suffix_g3]
  exact congrArg some (Mcfg_congr (by omega) rfl (by omega))

/-- Generation, class `G ≡ 2 (mod 3)` (`G = 35 + 3s`, suffix g=4):
`M(G, a+1) → M(47+4s, a+6)` shifted `−14−s` — ledger `+4`
(Lean filler `a+1 ↦ (a+1)+4 = a+5`). -/
theorem gen_mod2 (s a : Nat) (p : Int) :
    steps ((471 + bodyTime s 19) + (8 * (19 + 2 * s) + 8 * a + 71))
        (Mcfg (35 + 3 * s) (a + 1) p)
      = some (Mcfg (47 + 4 * s) (a + 5) (p - 14 - (s : Int))) := by
  rw [steps_add, prefix_bodies (35 + 3 * s) (a + 1) s p (by omega), someBind]
  rw [show 35 + 3 * s - 31 - 3 * s = 4 from by omega]
  rw [show BcfgCtx (19 + 2 * s) (p - 11 - (s : Int))
        (List.replicate 4 false ++ (pow10 (a + 1) ++ [false, true]))
      = Zcfg (19 + 2 * s) 4 (a + 1) (p - 11 - (s : Int)) from rfl]
  rw [suffix_g4]
  exact congrArg some (Mcfg_congr (by omega) rfl (by omega))

/-- Generation, class `G ≡ 0 (mod 3)` (`G = 36 + 3s`, suffix g=5),
generic filler `≥ 2`: `M(G, b+2) → M(51+4s, b+8)` shifted `−15−s` —
ledger `+6`. -/
theorem gen_mod0 (s b : Nat) (p : Int) :
    steps ((471 + bodyTime s 19) + (12 * (19 + 2 * s) + 16 * b + 164))
        (Mcfg (36 + 3 * s) (b + 2) p)
      = some (Mcfg (51 + 4 * s) (b + 8) (p - 15 - (s : Int))) := by
  rw [steps_add, prefix_bodies (36 + 3 * s) (b + 2) s p (by omega), someBind]
  rw [show 36 + 3 * s - 31 - 3 * s = 5 from by omega]
  rw [show BcfgCtx (19 + 2 * s) (p - 11 - (s : Int))
        (List.replicate 5 false ++ (pow10 (b + 2) ++ [false, true]))
      = Zcfg (19 + 2 * s) 5 (b + 2) (p - 11 - (s : Int)) from rfl]
  rw [suffix_g5]
  exact congrArg some (Mcfg_congr (by omega) rfl (by omega))

/-- Generation, class `G ≡ 0 (mod 3)` at filler 1 (the per-parameter
template): `M(G, 1) → M(51+4s, 7)` shifted `−15−s` — ledger `+6`. -/
theorem gen_mod0_small (s : Nat) (p : Int) :
    steps ((471 + bodyTime s 19) + (12 * (19 + 2 * s) + 148))
        (Mcfg (36 + 3 * s) 1 p)
      = some (Mcfg (51 + 4 * s) 7 (p - 15 - (s : Int))) := by
  rw [steps_add, prefix_bodies (36 + 3 * s) 1 s p (by omega), someBind]
  rw [show 36 + 3 * s - 31 - 3 * s = 5 from by omega]
  rw [show BcfgCtx (19 + 2 * s) (p - 11 - (s : Int))
        (List.replicate 5 false ++ (pow10 1 ++ [false, true]))
      = Zcfg (19 + 2 * s) 5 1 (p - 11 - (s : Int)) from rfl]
  rw [suffix_g5_small]
  exact congrArg some (Mcfg_congr (by omega) rfl (by omega))

/-! ### §7a the odometer and the ledger law (`O4_TEMPLATE_CLOSURE` §3–4),
DERIVED. -/

/-- `c(G mod 3)`: the odometer constant `{0 → 3, 1 → 5, 2 → 1}`. -/
def cOdo (G : Nat) : Nat := if G % 3 = 0 then 3 else if G % 3 = 1 then 5 else 1

/-- The a-ledger update `a ↦ a + δ(G mod 3)`, `δ = {1 → −1, 2 → +4, 0 → +6}`. -/
def ledgerNext (G a : Nat) : Nat :=
  if G % 3 = 1 then a - 1 else if G % 3 = 2 then a + 4 else a + 6

/-- The odometer law as pure arithmetic: the three landing gaps of the
generation map are exactly `⌊4G/3⌋ + c(G mod 3)`. -/
theorem odometer_arith (s : Nat) :
    50 + 4 * s = 4 * (34 + 3 * s) / 3 + 5
      ∧ 47 + 4 * s = 4 * (35 + 3 * s) / 3 + 1
      ∧ 51 + 4 * s = 4 * (36 + 3 * s) / 3 + 3 := by
  refine ⟨by omega, by omega, by omega⟩

/-- **THE GENERATION THEOREM, odometer + ledger form.**  For every
milestone `M(G, a)` with `G ≥ 34` and filler `a ≥ 1` (Lean convention;
`= a_py ≥ 0`), o4 reaches `M(⌊4G/3⌋ + c(G mod 3), a + δ(G mod 3))` —
the base-4/3 odometer and the prefix-sum a-ledger, machine-checked.
Everything about o4's generation dynamics is now formal; what is NOT
proved (and remains THE open core) is that the ledger keeps the filler
`≥ 1` (resp. `≥ 2` before `G ≡ 1` drains) along the orbit — the a-ledger
conjecture.  o4 stays `[OPEN]`. -/
theorem generation_odometer (G a : Nat) (p : Int) (hG : 34 ≤ G) (ha : 1 ≤ a) :
    ∃ (N : Nat) (q : Int),
      steps N (Mcfg G a p) = some (Mcfg (4 * G / 3 + cOdo G) (ledgerNext G a) q) := by
  have hm : G % 3 = 0 ∨ G % 3 = 1 ∨ G % 3 = 2 := by omega
  cases hm with
  | inl h0 =>
    obtain ⟨s, hs⟩ : ∃ s, G = 36 + 3 * s := ⟨(G - 36) / 3, by omega⟩
    subst hs
    have hc : cOdo (36 + 3 * s) = 3 := by
      unfold cOdo; rw [show (36 + 3 * s) % 3 = 0 from by omega]; rfl
    cases Nat.lt_or_ge a 2 with
    | inl ha1 =>
      have ha' : a = 1 := by omega
      subst ha'
      have hl : ledgerNext (36 + 3 * s) 1 = 7 := by
        unfold ledgerNext; rw [show (36 + 3 * s) % 3 = 0 from by omega]; rfl
      exact ⟨(471 + bodyTime s 19) + (12 * (19 + 2 * s) + 148), p - 15 - (s : Int), by
        rw [hc, hl, gen_mod0_small]
        exact congrArg some (Mcfg_congr (by omega) rfl rfl)⟩
    | inr ha2 =>
      obtain ⟨b, hb⟩ : ∃ b, a = b + 2 := ⟨a - 2, by omega⟩
      subst hb
      have hl : ledgerNext (36 + 3 * s) (b + 2) = b + 8 := by
        unfold ledgerNext; rw [show (36 + 3 * s) % 3 = 0 from by omega]; rfl
      exact ⟨(471 + bodyTime s 19) + (12 * (19 + 2 * s) + 16 * b + 164),
          p - 15 - (s : Int), by
        rw [hc, hl, gen_mod0]
        exact congrArg some (Mcfg_congr (by omega) rfl rfl)⟩
  | inr h12 =>
    cases h12 with
    | inl h1 =>
      obtain ⟨s, hs⟩ : ∃ s, G = 34 + 3 * s := ⟨(G - 34) / 3, by omega⟩
      subst hs
      obtain ⟨a', ha'⟩ : ∃ a', a = a' + 1 := ⟨a - 1, by omega⟩
      subst ha'
      have hc : cOdo (34 + 3 * s) = 5 := by
        unfold cOdo; rw [show (34 + 3 * s) % 3 = 1 from by omega]; rfl
      have hl : ledgerNext (34 + 3 * s) (a' + 1) = a' := by
        unfold ledgerNext; rw [show (34 + 3 * s) % 3 = 1 from by omega]; rfl
      exact ⟨(471 + bodyTime s 19) + (8 * (19 + 2 * s) + 35), p - 14 - (s : Int), by
        rw [hc, hl, gen_mod1]
        exact congrArg some (Mcfg_congr (by omega) rfl rfl)⟩
    | inr h2 =>
      obtain ⟨s, hs⟩ : ∃ s, G = 35 + 3 * s := ⟨(G - 35) / 3, by omega⟩
      subst hs
      obtain ⟨a', ha'⟩ : ∃ a', a = a' + 1 := ⟨a - 1, by omega⟩
      subst ha'
      have hc : cOdo (35 + 3 * s) = 1 := by
        unfold cOdo; rw [show (35 + 3 * s) % 3 = 2 from by omega]; rfl
      have hl : ledgerNext (35 + 3 * s) (a' + 1) = a' + 5 := by
        unfold ledgerNext; rw [show (35 + 3 * s) % 3 = 2 from by omega]; rfl
      exact ⟨(471 + bodyTime s 19) + (8 * (19 + 2 * s) + 8 * a' + 71),
          p - 14 - (s : Int), by
        rw [hc, hl, gen_mod2]
        exact congrArg some (Mcfg_congr (by omega) rfl rfl)⟩

/-! ### §7b real-orbit anchor: the generation 43 → 62 end-to-end. -/

/-- Blank tape → step 2551 = `M(62, 17)` at −59: `real_milestone` (step
1548 = `M(43, 18)`) composed with `gen_mod1` (s = 3, ledger 18 → 17) —
matching the instrumented run's milestone dump (gap 62, `a_py` 16 at step
2551).  `1548 + 471 + (91+99+107) + 235 = 2551`. -/
theorem real_next_milestone :
    steps (1548 + ((471 + bodyTime 3 19) + (8 * (19 + 2 * 3) + 35))) init
      = some (Mcfg 62 17 (-59)) := by
  rw [steps_add, real_milestone, someBind,
      show (Mcfg 43 18 (-42) : Cfg) = Mcfg (34 + 3 * 3) (17 + 1) (-42) from rfl,
      gen_mod1]
  exact congrArg some (Mcfg_congr (by omega) rfl (by omega))

-- the composed step count is the real orbit's 2551:
#eval (1548 + ((471 + bodyTime 3 19) + (8 * (19 + 2 * 3) + 35)))
-- generation grid anchor (G=100 ≡ 1: M(100,9) → M(⌊400/3⌋+5, 8) = M(138,8)):
#eval decide (steps ((471 + bodyTime 22 19) + (8 * (19 + 2 * 22) + 35)) (Mcfg 100 9 0)
      = some (Mcfg 138 8 (-36)))

/-! ## §8 Axiom audit (printed at every build). -/

#print axioms sweepAD
#print axioms suffix_g3
#print axioms suffix_g4
#print axioms suffix_g5
#print axioms suffix_g5_small
#print axioms gen_mod1
#print axioms gen_mod2
#print axioms gen_mod0
#print axioms gen_mod0_small
#print axioms generation_odometer
#print axioms odometer_arith
#print axioms real_next_milestone

end Template
