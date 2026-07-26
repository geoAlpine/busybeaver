import TapeCalc

set_option maxRecDepth 4000000
set_option maxHeartbeats 1000000

/-!
# `RungCalc` — the COMB-doubler rung tile as a **machine-independent** library

A second machine-independent layer above `TapeCalc`, in the same spirit: `TapeCalc` knows
nothing about which machine it moves, and `RungCalc` knows nothing about which machine's rung
it tiles.

## Why this file exists

`D`'s rung tile was first proven inside `lean/DMachine.lean` as a nine-phase composition of six
atoms.  Only **two** state names occur in those six atom *interfaces* — the outward-sweep state
`sA` and the return-sweep state `sB`.  Every other state the machine passes through is hidden
*inside* an atom.  So the tile cannot see the machine's transition graph at all; it sees six
local rewrite facts.

That prediction was then tested (`h_vs_d_tile.py`, `h_tile_fire.py`) and it held in a strong
form.  `H = 1RB0RE_0RC0RA_1LD1RE_1LA0LD_1RA0LF_1LD---` has a transition graph that is **not** a
relabeling of `D`'s — a full search over state permutations in both orientations returns zero
isomorphisms — and yet `D`'s rung tile fires on `H` verbatim: same span `6(u+m)+15`, same
`+3` head advance, same `IN(u,m,c,g) → IN(u+2,m−1,c+1,g−3)`, on the same 23040-point grid, from
`H`'s state `D`.  The two itineraries are the same word:

```
D^R : ABED ABED ABED A ABED ABED ABED A  BC AE·… →  ABEDABEDABEDAABEDABEDABEDABCBEBEBEBCBCBCBCBCD
H   : DAEF DAEF DAEF D DAEF DAEF DAEF D  AB  …  →  DAEFDAEFDAEFDDAEFDAEFDAEFDABAEAEAEABABABABABC
```

`H` *splits* one of `D`'s states in two: `Dᴿ`'s `D` is entered both from `E` (inside the crawl)
and from `C` (inside the turn), and `H` uses two different states (`F` and `C`) for those two
roles.  The graphs differ; the atoms do not.  So the tile is an invariant of the machine
**modulo merging states that behave identically within an atom** — which is exactly what
`Atoms` below records.

## Contents

* `pow10`/`pow01`/`ones` and the four word identities the seams need;
* `Atoms T sA sB cr mk ta s10 s01 tu` — the six-atom interface (a `Prop`-valued structure),
  each atom carrying its own step count, since those are not part of the mechanism;
* `span` — the rung's step count as a linear function of the six;
* `crawlFold`, `sweep10`, `sweep01`, `markerFold` — the four `∀`-uniform folds, from `Atoms`;
* `sweep10At` — the S1 fold at an **arbitrary anchor state**, needing only the `swap10` atom;
  `D` runs one at state `D` (`D1→0RF, F0→1RD`) in its epoch-entry turn;
* `IN` — the milestone-region configuration family;
* `rung_prefix` — phases 1–7, which never read the right context;
* `rung_core` / `tile` — the rung tile, `[PROVEN]` for **every** machine satisfying `Atoms`;
* `rung_core2` / `IN2` / `tile2` — the **rightward turn phase** (`RF-4`), the same law with the
  return sweep crossing a `(1 0)^w` comb before the landing pad.  `IN` is the `w = 0` case, so one
  law covers both, and a turn phase's output is again an `IN` — at `u'=0, m'=w, c'=1`;
* `rung0` / `descend` — the two pieces of the **leftward** turn phase: the rung with an exhausted
  comb, and the descent `crawlFold ; crawl ; markerFold ; crawl`.

Zero-Mathlib, core only.  No `sorry`, no `native_decide`, no `decide`.
No machine is decided here and no label is upgraded: this file proves a *conditional*
statement, and supplying its hypotheses for a given machine is what the client files do.
-/

namespace RungCalc

open TapeCalc

/-! ## §1 Word vocabulary. -/

/-- `(1 0)` repeated `j` times. -/
def pow10 : Nat → List Bool
  | 0 => []
  | j + 1 => true :: false :: pow10 j

/-- `(0 1)` repeated `k` times. -/
def pow01 : Nat → List Bool
  | 0 => []
  | k + 1 => false :: true :: pow01 k

/-- `n` `true`s. -/
def ones : Nat → List Bool
  | 0 => []
  | n + 1 => true :: ones n

theorem pow10_add : ∀ (a b : Nat), pow10 (a + b) = pow10 a ++ pow10 b := by
  intro a
  induction a with
  | zero => intro b; rw [Nat.zero_add]; rfl
  | succ a ih =>
    intro b
    rw [show a + 1 + b = (a + b) + 1 from by omega]
    show true :: false :: pow10 (a + b) = pow10 (a + 1) ++ pow10 b
    rw [ih]; rfl

/-- `pow10` absorbs a `1 0` handed to it from the right — the identity the crawl fold needs
(each crawl moves one `(1 0)` unit across the head, front to back). -/
theorem pow10_snoc : ∀ (n : Nat) (R : List Bool),
    pow10 n ++ true :: false :: R = pow10 (n + 1) ++ R := by
  intro n
  induction n with
  | zero => intro R; rfl
  | succ n ih =>
    intro R
    show true :: false :: (pow10 n ++ true :: false :: R)
        = true :: false :: (pow10 (n + 1) ++ R)
    rw [ih]

/-- Mirror of `pow10_snoc`, for the return sweep's `(0 1)` deposit. -/
theorem pow01_snoc : ∀ (n : Nat) (R : List Bool),
    pow01 n ++ false :: true :: R = pow01 (n + 1) ++ R := by
  intro n
  induction n with
  | zero => intro R; rfl
  | succ n ih =>
    intro R
    show false :: true :: (pow01 n ++ false :: true :: R)
        = false :: true :: (pow01 (n + 1) ++ R)
    rw [ih]

/-- Head-peel, as a `rw`-able equation (both sides are definitionally equal). -/
theorem pow10_cons (n : Nat) (X : List Bool) :
    pow10 (n + 1) ++ X = true :: false :: (pow10 n ++ X) := rfl

theorem pow01_cons (n : Nat) (X : List Bool) :
    pow01 (n + 1) ++ X = false :: true :: (pow01 n ++ X) := rfl

/-- **Re-phasing.**  A `(1 0)`-comb followed by a `1` is a `1` followed by a `(0 1)`-comb.
This is what lets the *return* sweep read as `(0 1)` exactly the block the *outward* sweep
wrote as `(1 0)`; it is used twice, once on the tape and once on the target word. -/
theorem pow10_true : ∀ (n : Nat) (R : List Bool),
    pow10 n ++ true :: R = true :: (pow01 n ++ R) := by
  intro n
  induction n with
  | zero => intro R; rfl
  | succ n ih =>
    intro R
    show true :: false :: (pow10 n ++ true :: R) = true :: (false :: true :: (pow01 n ++ R))
    rw [ih]

/-- **The comb re-reading.**  Once the `[1,1]` marker has been consumed, the left context
`1 · (0 1)^n · 0 0 · Z` — which is how `IN` writes it — is literally `(1 0)^{n+1} · 0 · Z`,
which is what `crawlFold` consumes.  This is the one identity that makes the second outward
sweep a *single* fold instead of an ad-hoc phase. -/
theorem pow01_shift : ∀ (n : Nat) (Z : List Bool),
    true :: (pow01 n ++ false :: false :: Z) = pow10 (n + 1) ++ false :: Z := by
  intro n
  induction n with
  | zero => intro Z; rfl
  | succ n ih =>
    intro Z
    show true :: false :: (true :: (pow01 n ++ false :: false :: Z))
        = true :: false :: (pow10 (n + 1) ++ false :: Z)
    rw [ih]

/-- `zeros` absorbs a `0` handed to it from the right (mirror of `pow10_snoc`). -/
theorem zerosSnoc : ∀ (n : Nat) (R : List Bool),
    zeros n ++ false :: R = zeros (n + 1) ++ R := by
  intro n
  induction n with
  | zero => intro R; rfl
  | succ n ih =>
    intro R
    show false :: (zeros n ++ false :: R) = false :: (zeros (n + 1) ++ R)
    rw [ih]

/-- Mirror of `pow01_shift`, for reading a turn phase's output back as an `IN` word:
a `0` in front of a `(1 0)`-comb is a `(0 1)`-comb in front of a `0`. -/
theorem pow10_shift : ∀ (n : Nat) (Y : List Bool),
    false :: (pow10 n ++ Y) = pow01 n ++ (false :: Y) := by
  intro n
  induction n with
  | zero => intro Y; rfl
  | succ n ih =>
    intro Y
    show false :: true :: false :: (pow10 n ++ Y) = false :: true :: (pow01 n ++ (false :: Y))
    rw [ih]

/-! ## §2 The six-atom interface. -/

/-- Position-congruence helper (all the phase arithmetic needs). -/
theorem cfgPos {S : Type} {s : S} {p q : Int} {t : Tape} (h : p = q) :
    (⟨s, p, t⟩ : Cfg S) = ⟨s, q, t⟩ := by rw [h]

/-- **The six atoms of a COMB-doubler rung.**  `sA` is the outward-sweep state, `sB` the
return-sweep state; every other state of `T` is hidden inside an atom, which is why a machine
whose graph is not a relabeling of another's can still satisfy the *same* `Atoms`.

Each field is `∀`-uniform in the tape context — that discipline is not decoration, it is the
whole reason the tile composes and the reason it transports between machines. -/
structure Atoms {S : Type} (T : S → Bool → Option (Bool × Dir × S)) (sA sB : S)
    (cr mk ta s10 s01 tu : Nat) : Prop where
  /-- The outward crawl: 4 steps, head `−2`, the two rewritten cells handed to the right
  verbatim.  Note the `∀ b`: the atom never reads the cell it lands on, which is what lets the
  *same* atom scan `(0 1)^u` and step over the `[1,1]` marker. -/
  crawl : ∀ (p : Int) (b : Bool) (L R : List Bool),
    steps T cr ⟨sA, p, ⟨true :: b :: L, false, R⟩⟩
      = some ⟨sA, p - 2, ⟨L, b, true :: false :: R⟩⟩
  /-- The marker step: the outward sweep reads a `1` and keeps going, writing `0`. -/
  marker : ∀ (p : Int) (x : Bool) (L R : List Bool),
    steps T mk ⟨sA, p, ⟨x :: L, true, R⟩⟩ = some ⟨sA, p - 1, ⟨L, x, false :: R⟩⟩
  /-- The turnaround: the outward sweep dies on the `0 0` gap and the return sweep is born,
  one cell further left, in `sB`. -/
  turnaround : ∀ (p : Int) (x : Bool) (L R : List Bool),
    steps T ta ⟨sA, p, ⟨x :: L, false, R⟩⟩ = some ⟨sB, p - 1, ⟨L, x, true :: R⟩⟩
  /-- Return atom S1: 2 steps, head `+2`, rewrites `1 0 ↦ 0 1`.  `sB`-to-`sB`. -/
  swap10 : ∀ (p : Int) (b : Bool) (L R : List Bool),
    steps T s10 ⟨sB, p, ⟨L, true, false :: b :: R⟩⟩
      = some ⟨sB, p + 2, ⟨true :: false :: L, b, R⟩⟩
  /-- Return atom S2: 2 steps, head `+2`, rewrites `0 1 ↦ 1 0`.  `sB`-to-`sB`. -/
  swap01 : ∀ (p : Int) (b : Bool) (L R : List Bool),
    steps T s01 ⟨sB, p, ⟨L, false, true :: b :: R⟩⟩
      = some ⟨sB, p + 2, ⟨false :: true :: L, b, R⟩⟩
  /-- The turn: the return sweep hits the `0 0 0` landing pad, deposits the new `1` and settles
  back into `sA` at `+1`.  This is the rung's `+3` net head advance, and it is why `g ≥ 3` is a
  genuine hypothesis rather than slack. -/
  turn : ∀ (p : Int) (L R : List Bool),
    steps T tu ⟨sB, p, ⟨L, false, false :: false :: R⟩⟩
      = some ⟨sA, p + 1, ⟨true :: L, false, true :: R⟩⟩

section
variable {S : Type} {T : S → Bool → Option (Bool × Dir × S)} {sA sB : S}
    {cr mk ta s10 s01 tu : Nat}

/-! ## §3 The three folds. -/

/-- **The crawl fold** — the outward sweep over `pow10 n`: `4n` steps, head `−2n`, tape
unchanged (the comb is handed over to the right side verbatim). -/
theorem crawlFold (h : Atoms T sA sB cr mk ta s10 s01 tu) : ∀ (n : Nat) (p : Int) (L R : List Bool),
    steps T (cr * n) ⟨sA, p, ⟨pow10 n ++ L, false, R⟩⟩
      = some ⟨sA, p - 2 * n, ⟨L, false, pow10 n ++ R⟩⟩ := by
  intro n
  induction n with
  | zero =>
    intro p L R
    rw [show cr * 0 = 0 from by omega]
    show some _ = some _
    simp [pow10]
  | succ n ih =>
    intro p L R
    rw [show cr * (n + 1) = cr + cr * n from by rw [Nat.mul_succ]; omega, steps_add]
    show (steps T cr ⟨sA, p, ⟨true :: false :: (pow10 n ++ L), false, R⟩⟩).bind _ = _
    rw [h.crawl p false (pow10 n ++ L) R, someBind, ih (p - 2) L (true :: false :: R),
        pow10_snoc n R]
    exact congrArg some (cfgPos (by omega))

/-- **Fold of S1, at ANY anchor.**  The fold needs only the `swap10` atom, not the whole
interface, and not `sB` in particular.  That matters: `D`'s epoch-entry turn runs a `swap10`
sweep anchored at state `D` (`D1→0RF, F0→1RD`) rather than at `sB = B`, so the same fold serves
both (`d_rf4_epochs.py`). -/
theorem sweep10At {S : Type} {T : S → Bool → Option (Bool × Dir × S)} {s : S} {n : Nat}
    (hs : ∀ (p : Int) (b : Bool) (L R : List Bool),
      steps T n ⟨s, p, ⟨L, true, false :: b :: R⟩⟩
        = some ⟨s, p + 2, ⟨true :: false :: L, b, R⟩⟩) :
    ∀ (k : Nat) (p : Int) (b : Bool) (L R : List Bool),
    steps T (n * (k + 1)) ⟨s, p, ⟨L, true, false :: (pow10 k ++ b :: R)⟩⟩
      = some ⟨s, p + 2 * k + 2, ⟨pow10 (k + 1) ++ L, b, R⟩⟩ := by
  intro k
  induction k with
  | zero =>
    intro p b L R
    rw [show n * (0 + 1) = n from by omega]
    show steps T n ⟨s, p, ⟨L, true, false :: b :: R⟩⟩
        = some ⟨s, p + 2 * ((0 : Nat) : Int) + 2, ⟨true :: false :: L, b, R⟩⟩
    rw [hs p b L R]
    exact congrArg some (cfgPos (by omega))
  | succ k ih =>
    intro p b L R
    rw [show n * (k + 1 + 1) = n + n * (k + 1) from by rw [Nat.mul_succ]; omega,
        steps_add, pow10_cons]
    rw [hs p true L (false :: (pow10 k ++ b :: R)), someBind,
        ih (p + 2) b (true :: false :: L) R, pow10_snoc (k + 1) L]
    exact congrArg some (cfgPos (by omega))

/-- **Fold of S1** — `k+1` return atoms over a `(1 0)^{k+1}` block. -/
theorem sweep10 (h : Atoms T sA sB cr mk ta s10 s01 tu) : ∀ (k : Nat) (p : Int) (b : Bool) (L R : List Bool),
    steps T (s10 * (k + 1)) ⟨sB, p, ⟨L, true, false :: (pow10 k ++ b :: R)⟩⟩
      = some ⟨sB, p + 2 * k + 2, ⟨pow10 (k + 1) ++ L, b, R⟩⟩ :=
  sweep10At h.swap10

/-- **Fold of S2** — `k+1` return atoms over a `(0 1)^{k+1}` block. -/
theorem sweep01 (h : Atoms T sA sB cr mk ta s10 s01 tu) : ∀ (k : Nat) (p : Int) (b : Bool) (L R : List Bool),
    steps T (s01 * (k + 1)) ⟨sB, p, ⟨L, false, true :: (pow01 k ++ b :: R)⟩⟩
      = some ⟨sB, p + 2 * k + 2, ⟨pow01 (k + 1) ++ L, b, R⟩⟩ := by
  intro k
  induction k with
  | zero =>
    intro p b L R
    rw [show s01 * (0 + 1) = s01 from by omega]
    show steps T s01 ⟨sB, p, ⟨L, false, true :: b :: R⟩⟩
        = some ⟨sB, p + 2 * ((0 : Nat) : Int) + 2, ⟨false :: true :: L, b, R⟩⟩
    rw [h.swap01 p b L R]
    exact congrArg some (cfgPos (by omega))
  | succ k ih =>
    intro p b L R
    rw [show s01 * (k + 1 + 1) = s01 + s01 * (k + 1) from by rw [Nat.mul_succ]; omega,
        steps_add, pow01_cons]
    rw [h.swap01 p false L (true :: (pow01 k ++ b :: R)), someBind,
        ih (p + 2) b (false :: true :: L) R, pow01_snoc (k + 1) L]
    exact congrArg some (cfgPos (by omega))

/-- **Fold of `marker`** — the outward sweep crossing a `1`-run leftwards, erasing it.
`marker` leaves the head scanning `true` again whenever the cell it lands on is a `1`, so it
folds exactly like the crawl does.  This is the `(A)^n` run that dominates `D`'s **leftward**
(coming-back-down) turn phases; the rightward ones are `rung_core2`. -/
theorem markerFold (h : Atoms T sA sB cr mk ta s10 s01 tu) :
    ∀ (n : Nat) (p : Int) (x : Bool) (L R : List Bool),
    steps T (mk * (n + 1)) ⟨sA, p, ⟨ones n ++ (x :: L), true, R⟩⟩
      = some ⟨sA, p - (n + 1), ⟨L, x, zeros (n + 1) ++ R⟩⟩ := by
  intro n
  induction n with
  | zero =>
    intro p x L R
    rw [show mk * (0 + 1) = mk from by omega]
    show steps T mk ⟨sA, p, ⟨x :: L, true, R⟩⟩ = _
    rw [h.marker p x L R]
    exact congrArg some (cfgPos (by omega))
  | succ n ih =>
    intro p x L R
    rw [show mk * (n + 1 + 1) = mk + mk * (n + 1) from by rw [Nat.mul_succ]; omega, steps_add]
    show (steps T mk ⟨sA, p, ⟨true :: (ones n ++ (x :: L)), true, R⟩⟩).bind _ = _
    rw [h.marker p true (ones n ++ (x :: L)) R, someBind, ih (p - 1) x L (false :: R)]
    rw [zerosSnoc (n + 1) R]
    exact congrArg some (cfgPos (by omega))

/-! ## §4 The rung tile. -/

/-- The rung's span, as a linear function of the six atom step counts.

The nine phases fire `u+m+2` crawls, `u+3` `swap01`s, `m+1` `swap10`s, and one each of `marker`,
`turnaround` and `turn`.  The step counts are **not** part of the mechanism: `D`'s
`(cr,mk,ta,s10,s01,tu) = (4,1,1,2,2,3)` gives `6(u+m)+21`, and the residual also contains a
machine whose turn takes **five** steps instead of three — reaching the identical output
configuration — for which `(4,1,1,2,2,5)` gives `6(u+m)+23`
(`1RB0RF_0LC0RA_1LE1RD_0RC---_1LA0LE_1RA0LC`, `sA = E`; see `atoms_flex_scan.py`). -/
def span (cr mk ta s10 s01 tu u m : Nat) : Nat :=
  cr * (u + m + 2) + s01 * (u + 3) + s10 * (m + 1) + mk + ta + tu

/-! ### The rung, with its two frozen contexts abstracted.

`W` is everything at or left of the `1^c` counter, `Z` everything right of the `1 0 0 0` landing
pad.  Neither is read — the visited window is `[p − 2(u+m) − 6, p + 4]` in *these* variables —
which is what makes the tile composable under
`TapeCalc.steps_lpad_dich` / `steps_rpad_dich`.

The nine phases, in order (total `6(u+m)+21` at `D`'s step counts):

| # | steps | atom | what it does |
|---|---|---|---|
| 1 | `4u` | `crawlFold u` | outward over `(0 1)^u` |
| 2 | `4` | `crawl _ true` | outward over the first `1` of `[1,1]` |
| 3 | `1` | `marker` | the second `1` |
| 4 | `4(m+1)` | `crawlFold (m+1)` | outward over the comb, re-read by `pow01_shift` |
| 5 | `1` | `turnaround` | the `0 0` gap |
| 6 | `2` | `swap01` | first return atom |
| 7 | `2(m+1)` | `sweep10 m` | return over the comb |
| 8 | `2(u+2)` | `sweep01 (u+1)` | return over the deposit, re-phased by `pow10_true` |
| 9 | `3` | `turn` | land in `sA` at `+3`
-/

/-- **Phases 1–7 alone.**  These never read the right context — every atom is `∀ R` — so `Rt` is
completely arbitrary here.  That is what lets the *same* prefix serve both the rung tile
(`Rt = 1 0 0 0 …`, the return sweep turns immediately) and the **turn phase**
(`Rt = 1 (1 0)^{w+1} 0 0 0 …`, the return sweep first crosses a comb).  See `rung_core2`. -/
theorem rung_prefix (h : Atoms T sA sB cr mk ta s10 s01 tu) (u m : Nat) (p : Int)
    (W Rt : List Bool) :
    steps T (cr * (u + m + 2) + mk + ta + s01 + s10 * (m + 1))
        ⟨sA, p, ⟨pow10 u ++ (true :: true :: (pow01 (m + 1) ++ (false :: false :: W))),
                 false, Rt⟩⟩
      = some ⟨sB, p - 2 * u - 2,
          ⟨pow10 (m + 1) ++ (false :: true :: W), false, pow10 (u + 1) ++ Rt⟩⟩ := by
  rw [show cr * (u + m + 2) + mk + ta + s01 + s10 * (m + 1)
        = cr * u + (cr + (mk + (cr * (m + 1) + (ta + (s01 + s10 * (m + 1))))))
      from by simp only [Nat.mul_add, Nat.mul_succ]; omega]
  -- 1 ── outward crawl over `(0 1)^u`
  rw [steps_add, crawlFold h u p (true :: true :: (pow01 (m + 1) ++ (false :: false :: W))) Rt,
      someBind]
  -- 2 ── the same atom carries the head over the first `1` of the `[1,1]` marker
  rw [steps_add, h.crawl _ true (pow01 (m + 1) ++ (false :: false :: W)) (pow10 u ++ Rt), someBind]
  -- 3 ── the marker step
  rw [pow01_cons, steps_add, h.marker _ false (true :: (pow01 m ++ (false :: false :: W))) _,
      someBind]
  -- the comb now re-reads as `(1 0)^(m+1) 0`
  rw [pow01_shift m W]
  -- 4 ── outward crawl over the comb
  rw [steps_add, crawlFold h (m + 1) _ (false :: W) _, someBind]
  -- 5 ── the turnaround on the `0 0` gap
  rw [steps_add, h.turnaround _ false W _, someBind]
  -- 6 ── the first return atom
  rw [pow10_cons, steps_add, h.swap01 _ true W _, someBind]
  -- 7 ── the return sweep over the comb (the last piece: no further `steps_add`)
  rw [sweep10 h m _ false (false :: true :: W) _, ← pow10_cons u Rt]
  exact congrArg some (cfgPos (by omega))

theorem rung_core (h : Atoms T sA sB cr mk ta s10 s01 tu) (u m : Nat) (p : Int) (W Z : List Bool) :
    steps T (span cr mk ta s10 s01 tu u m)
        ⟨sA, p, ⟨pow10 u ++ (true :: true :: (pow01 (m + 1) ++ (false :: false :: W))),
                 false, true :: false :: false :: false :: Z⟩⟩
      = some ⟨sA, p + 3,
          ⟨pow10 (u + 2) ++ (true :: true :: (pow01 m ++ (false :: false :: true :: W))),
           false, true :: Z⟩⟩ := by
  rw [show span cr mk ta s10 s01 tu u m
        = (cr * (u + m + 2) + mk + ta + s01 + s10 * (m + 1)) + ((s01 * (u + 1 + 1)) + tu)
      from by simp only [span, Nat.mul_add, Nat.mul_succ]; omega]
  rw [steps_add, rung_prefix h u m p W (true :: false :: false :: false :: Z), someBind]
  -- the deposit re-phases from `(1 0)` to `(0 1)`
  rw [pow10_true (u + 1) (false :: false :: false :: Z)]
  -- 8 ── the return sweep over the deposit
  rw [steps_add, sweep01 h (u + 1) _ false (pow10 (m + 1) ++ (false :: true :: W)) _, someBind]
  -- 9 ── the turn
  rw [h.turn _ (pow01 (u + 2) ++ (pow10 (m + 1) ++ (false :: true :: W))) Z]
  -- the target word, read back through the same two identities
  rw [pow01_shift m (true :: W), pow10_true (u + 2) (pow10 (m + 1) ++ (false :: true :: W))]
  exact congrArg some (cfgPos (by omega))

/-! ### §4.1 The **turn phase** — the same law with a longer return sweep.

`D_SPEC_2026-07-26.md` §5 (RF-4) recorded the inter-segment turn phases as `≈2 steps/cell` with
additive constants that "are not a closed function of `k` alone", and §8 called each one "a
separate small lemma".  Measurement says otherwise (`d_rf4_turns.py`, `d_rf4_law.py`): the
rightward turn phase is **this same rung**, with the return sweep crossing a `(1 0)`-comb before
it reaches the landing pad.  A turn happens exactly when the gap `g` is exhausted, so the return
sweep meets a comb instead of `0 0 0`; it crosses with `w+1` more `swap10` atoms and turns beyond.

Two spot checks against `D`'s real orbit, epoch `M1(4) → M1(5)`:

| turn | `u` | `m` | comb crossed | predicted span | measured |
|---|---:|---:|---:|---:|---:|
| `t = 291698` | 9 | 2 | 66 | `6·11+15+2·66 = 213` | **213** |
| `t = 310271` | 72 | 29 | 309 | `6·101+15+2·309 = 1239` | **1239** |

and in both cases the next ladder segment starts at `IN(0, w, 1, g)` — which `IN2_is_IN` below
proves in general.  The rung tile is the `w = 0` case of the same statement, so this is **one**
law rather than two (`d_rf4_law.py §3`, 144/144). -/
theorem rung_core2 (h : Atoms T sA sB cr mk ta s10 s01 tu) (u m w : Nat) (p : Int)
    (W Z : List Bool) :
    steps T (span cr mk ta s10 s01 tu u m + s10 * (w + 1))
        ⟨sA, p, ⟨pow10 u ++ (true :: true :: (pow01 (m + 1) ++ (false :: false :: W))),
                 false, true :: (pow10 (w + 1) ++ (false :: false :: false :: Z))⟩⟩
      = some ⟨sA, p + 3 + 2 * (w + 1),
          ⟨true :: (pow10 (w + 1) ++ (pow01 (u + 2) ++ (pow10 (m + 1) ++ (false :: true :: W)))),
           false, true :: Z⟩⟩ := by
  rw [show span cr mk ta s10 s01 tu u m + s10 * (w + 1)
        = (cr * (u + m + 2) + mk + ta + s01 + s10 * (m + 1))
            + ((s01 * (u + 1 + 1)) + ((s10 * (w + 1)) + tu))
      from by simp only [span, Nat.mul_add, Nat.mul_succ]; omega]
  rw [steps_add,
      rung_prefix h u m p W (true :: (pow10 (w + 1) ++ (false :: false :: false :: Z))), someBind]
  -- the deposit re-phases from `(1 0)` to `(0 1)`
  rw [pow10_true (u + 1) (pow10 (w + 1) ++ (false :: false :: false :: Z))]
  -- 8 ── the return sweep over the deposit; it now lands on a `1`, not on the pad
  rw [pow10_cons w (false :: false :: false :: Z), steps_add,
      sweep01 h (u + 1) _ true (pow10 (m + 1) ++ (false :: true :: W)) _, someBind]
  -- 8b ── the EXTRA sweep: `w+1` more `swap10` atoms across the comb
  rw [steps_add, sweep10 h w _ false (pow01 (u + 2) ++ (pow10 (m + 1) ++ (false :: true :: W))) _,
      someBind]
  -- 9 ── the turn, on the pad beyond the comb
  rw [h.turn _ (pow10 (w + 1) ++ (pow01 (u + 2) ++ (pow10 (m + 1) ++ (false :: true :: W)))) Z]
  exact congrArg some (cfgPos (by omega))

/-! ### §4.2 The **leftward** turn phase — two more laws from the same atoms.

`d_rf4_left.py` reads `D`'s leftward (coming-back-down) turn phases as two pieces, and the head
trajectory confirms the split (the first advances `+3`, i.e. it is a rung; the second is a pure
descent):

```
t = 1194806 (1371 steps):  (ABED)^128 A A (BC)^130 D   ++   (ABED)^131 (A)^66 (ABED)
                           \________ rung0, u=127 ______/      \____ descend, q=130, r=65 ___/
                                    777 steps                          594 steps
```

`rung0` is the rung with an **exhausted comb** (`m_literal = 0`): the crawl run between `marker`
and `turnaround` is empty, which is exactly the boundary case the `IN` family excludes (`IN`
needs `m ≥ 1`).  `descend` is `crawlFold ; crawl ; markerFold ; crawl`.  Both are built from the
same four folds; neither needs a new atom.  Measured 6144/0 and 2304/0 (`d_rf4_left_law.py`). -/

/-- **The rung with an exhausted comb** (`m_literal = 0`).  Span `cr(u+1) + mk + ta + s01(u+3) + tu`
(`= 6u+15` at `D`'s counts), head `+3` — the same advance as the tile. -/
theorem rung0 (h : Atoms T sA sB cr mk ta s10 s01 tu) (u : Nat) (p : Int) (W Z : List Bool) :
    steps T (cr * (u + 1) + mk + ta + s01 * (u + 3) + tu)
        ⟨sA, p, ⟨pow10 u ++ (true :: true :: (false :: false :: W)),
                 false, true :: false :: false :: false :: Z⟩⟩
      = some ⟨sA, p + 3,
          ⟨true :: (pow01 (u + 2) ++ (false :: true :: W)), false, true :: Z⟩⟩ := by
  rw [show cr * (u + 1) + mk + ta + s01 * (u + 3) + tu
        = cr * u + (cr + (mk + (ta + (s01 + ((s01 * (u + 1 + 1)) + tu)))))
      from by simp only [Nat.mul_succ]; omega]
  rw [steps_add, crawlFold h u p (true :: true :: (false :: false :: W))
        (true :: false :: false :: false :: Z), someBind]
  rw [steps_add, h.crawl _ true (false :: false :: W)
        (pow10 u ++ (true :: false :: false :: false :: Z)), someBind]
  rw [steps_add, h.marker _ false (false :: W) _, someBind]
  rw [steps_add, h.turnaround _ false W _, someBind]
  rw [steps_add, h.swap01 _ false W _, someBind]
  rw [← pow10_cons u (true :: false :: false :: false :: Z),
      pow10_true (u + 1) (false :: false :: false :: Z)]
  rw [steps_add, sweep01 h (u + 1) _ false (false :: true :: W) _, someBind]
  rw [h.turn _ (pow01 (u + 2) ++ (false :: true :: W)) Z]
  exact congrArg some (cfgPos (by omega))

/-- **The descent** — `crawlFold q ; crawl ; markerFold r ; crawl`: the head walks left over a
`(1 0)^q` comb, steps onto a `1`-run, erases it with `markerFold`, and takes one more crawl.
Span `cr(q+2) + mk(r+1)`, head `−2(q+1) − (r+1) − 2`. -/
theorem descend (h : Atoms T sA sB cr mk ta s10 s01 tu) (q r : Nat) (p : Int) (b : Bool)
    (L R : List Bool) :
    steps T (cr * (q + 2) + mk * (r + 1))
        ⟨sA, p, ⟨pow10 q ++ (true :: true :: (ones r ++ (false :: true :: b :: L))), false, R⟩⟩
      = some ⟨sA, p - 2 * (q + 1) - (r + 1) - 2,
          ⟨L, b, true :: false :: (zeros (r + 1) ++ (true :: false :: (pow10 q ++ R)))⟩⟩ := by
  rw [show cr * (q + 2) + mk * (r + 1) = cr * q + (cr + (mk * (r + 1) + cr))
      from by simp only [Nat.mul_succ]; omega]
  rw [steps_add, crawlFold h q p (true :: true :: (ones r ++ (false :: true :: b :: L))) R,
      someBind]
  rw [steps_add, h.crawl _ true (ones r ++ (false :: true :: b :: L)) (pow10 q ++ R), someBind]
  rw [steps_add, markerFold h r _ false (true :: b :: L) _, someBind]
  rw [h.crawl _ b L _]
  exact congrArg some (cfgPos (by omega))

end

/-- The rung-tile configuration family.  In tape order the neighbourhood reads
`… TAILᴿ 1^c 0 0 (1 0)^m 1 1 (0 1)^u [head=0] 1 0^g REST …`. -/
def IN {S : Type} (sA : S) (u m c g : Nat) (p : Int) (TAIL REST : List Bool) : Cfg S :=
  ⟨sA, p, ⟨pow10 u ++ [true, true] ++ pow01 m ++ [false, false] ++ ones c ++ TAIL,
           false,
           true :: (zeros g ++ REST)⟩⟩

/-- Right-associated normal form of `IN`'s left word — the shape the atoms consume. -/
theorem IN_norm {S : Type} (sA : S) (u m c g : Nat) (p : Int) (TAIL REST : List Bool) :
    IN sA u m c g p TAIL REST
      = ⟨sA, p, ⟨pow10 u ++ (true :: true :: (pow01 m ++ (false :: false :: (ones c ++ TAIL)))),
                 false, true :: (zeros g ++ REST)⟩⟩ := by
  show (⟨sA, p, ⟨pow10 u ++ [true, true] ++ pow01 m ++ [false, false] ++ ones c ++ TAIL,
                 false, true :: (zeros g ++ REST)⟩⟩ : Cfg S) = _
  rw [List.append_assoc, List.append_assoc, List.append_assoc, List.append_assoc]
  rfl

/-- **The rung tile, `[PROVEN]` for every machine satisfying `Atoms`.**

In `IN`'s own arguments this reads `steps (6(u+m)+15) IN(u,m,c,g) = IN(u+2, m−1, c+1, g−3)` at
`pos+3`, for `m ≥ 1`, `g ≥ 3`, **any `c ≥ 0`** (the counter is never read: the outward sweep
dies on the `0 0` gap one cell short of it) and arbitrary `TAIL`/`REST`. -/
theorem tile {S : Type} {T : S → Bool → Option (Bool × Dir × S)} {sA sB : S}
    {cr mk ta s10 s01 tu : Nat} (h : Atoms T sA sB cr mk ta s10 s01 tu)
    (u m c g : Nat) (p : Int) (TAIL REST : List Bool) :
    steps T (span cr mk ta s10 s01 tu u m) (IN sA u (m + 1) c (g + 3) p TAIL REST)
      = some (IN sA (u + 2) m (c + 1) g (p + 3) TAIL REST) := by
  rw [IN_norm, IN_norm]
  exact rung_core h u m p (ones c ++ TAIL) (zeros g ++ REST)

/-- The tile as a single `Prop`, for clients that want to name it. -/
def Tile {S : Type} (T : S → Bool → Option (Bool × Dir × S)) (sA : S)
    (sp : Nat → Nat → Nat) : Prop :=
  ∀ (u m c g : Nat) (p : Int) (TAIL REST : List Bool),
    steps T (sp u m) (IN sA u (m + 1) c (g + 3) p TAIL REST)
      = some (IN sA (u + 2) m (c + 1) g (p + 3) TAIL REST)

theorem tile_holds {S : Type} {T : S → Bool → Option (Bool × Dir × S)} {sA sB : S}
    {cr mk ta s10 s01 tu : Nat} (h : Atoms T sA sB cr mk ta s10 s01 tu) :
    Tile T sA (span cr mk ta s10 s01 tu) := tile h

/-! ## §6 The turn phase as a configuration law.

`IN2` is `IN` with the landing pad pushed `2w` cells further right by a `(1 0)`-comb.  `IN` is
literally the `w = 0` case (`pow10 0 = []`), so the rung tile and the turn phase are two
instances of ONE law -- which is what `d_rf4_law.py §3` measures (144/144 at `w = 0`). -/

/-- The turn-phase configuration family: `IN` with a `(1 0)^w` comb before the landing pad.
In tape order the neighbourhood reads
`… TAILᴿ 1^c 0 0 (1 0)^m 1 1 (0 1)^u [head=0] 1 (1 0)^w 0^g REST …`. -/
def IN2 {S : Type} (sA : S) (u m c w g : Nat) (p : Int) (TAIL REST : List Bool) : Cfg S :=
  ⟨sA, p, ⟨pow10 u ++ [true, true] ++ pow01 m ++ [false, false] ++ ones c ++ TAIL,
           false,
           true :: (pow10 w ++ (zeros g ++ REST))⟩⟩

theorem IN2_norm {S : Type} (sA : S) (u m c w g : Nat) (p : Int) (TAIL REST : List Bool) :
    IN2 sA u m c w g p TAIL REST
      = ⟨sA, p, ⟨pow10 u ++ (true :: true :: (pow01 m ++ (false :: false :: (ones c ++ TAIL)))),
                 false, true :: (pow10 w ++ (zeros g ++ REST))⟩⟩ := by
  show (⟨sA, p, ⟨pow10 u ++ [true, true] ++ pow01 m ++ [false, false] ++ ones c ++ TAIL,
                 false, true :: (pow10 w ++ (zeros g ++ REST))⟩⟩ : Cfg S) = _
  rw [List.append_assoc, List.append_assoc, List.append_assoc, List.append_assoc]
  rfl

/-- The word identity that lets a turn phase's output be read back as an `IN` word: the new
register is `1 1 (0 1)^w 0 0 1 …`, i.e. `IN` at `u' = 0`, `m' = w`, `c' = 1`. -/
theorem turn_out_word (u m w : Nat) (W : List Bool) :
    pow10 0 ++ (true :: true :: (pow01 w ++ (false :: false ::
        (ones 1 ++ (pow01 (u + 1) ++ (pow10 (m + 1) ++ (false :: true :: W)))))))
      = true :: (pow10 (w + 1) ++ (pow01 (u + 2) ++ (pow10 (m + 1) ++ (false :: true :: W)))) := by
  show true :: true :: (pow01 w ++ (false :: false ::
          (true :: (pow01 (u + 1) ++ (pow10 (m + 1) ++ (false :: true :: W))))))
      = true :: true :: false ::
          (pow10 w ++ (pow01 (u + 2) ++ (pow10 (m + 1) ++ (false :: true :: W))))
  rw [← pow01_cons (u + 1) (pow10 (m + 1) ++ (false :: true :: W)),
      ← pow10_shift w (pow01 (u + 2) ++ (pow10 (m + 1) ++ (false :: true :: W)))]

/-- **The turn phase, `[PROVEN]` for every machine satisfying `Atoms`.**

`steps (span + s10·(w+1)) IN2(u, m+1, c, w+1, g+3) = IN(0, w, 1, g)` at `pos + 3 + 2(w+1)`.

The output is itself a member of the `IN` family -- at `u' = 0`, `m' = w`, `c' = 1` -- so a turn
phase feeds straight back into the rung tile, which is exactly what `D`'s epoch does: ladder
segment, turn, ladder segment.  Measured on `D`'s real orbit at `t = 291698` (`w = 66`, next
segment `IN(0,65,1,·)`) and `t = 310271` (`w = 309`, next `IN(0,308,1,·)`). -/
theorem tile2 {S : Type} {T : S → Bool → Option (Bool × Dir × S)} {sA sB : S}
    {cr mk ta s10 s01 tu : Nat} (h : Atoms T sA sB cr mk ta s10 s01 tu)
    (u m c w g : Nat) (p : Int) (TAIL REST : List Bool) :
    steps T (span cr mk ta s10 s01 tu u m + s10 * (w + 1))
        (IN2 sA u (m + 1) c (w + 1) (g + 3) p TAIL REST)
      = some (IN sA 0 w 1 g (p + 3 + 2 * (w + 1))
          (pow01 (u + 1) ++ (pow10 (m + 1) ++ (false :: true :: (ones c ++ TAIL)))) REST) := by
  rw [IN2_norm, IN_norm, turn_out_word u m w (ones c ++ TAIL)]
  exact rung_core2 h u m w p (ones c ++ TAIL) (zeros g ++ REST)

-- AXIOM AUDIT
#print axioms crawlFold
#print axioms sweep10At
#print axioms sweep10
#print axioms sweep01
#print axioms markerFold
#print axioms rung_prefix
#print axioms rung_core
#print axioms rung_core2
#print axioms rung0
#print axioms descend
#print axioms tile
#print axioms tile_holds
#print axioms tile2

end RungCalc
