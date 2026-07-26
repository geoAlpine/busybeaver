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
* `Atoms T sA sB` — the six-atom interface, a `Prop`-valued structure;
* `crawlFold`, `sweep10`, `sweep01` — the three `∀`-uniform folds, derived from `Atoms`;
* `IN` — the milestone-region configuration family;
* `rung_core` / `tile` — the rung tile, `[PROVEN]` for **every** machine satisfying `Atoms`.

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

/-! ## §2 The six-atom interface. -/

/-- Position-congruence helper (all the phase arithmetic needs). -/
theorem cfgPos {S : Type} {s : S} {p q : Int} {t : Tape} (h : p = q) :
    (⟨s, p, t⟩ : Cfg S) = ⟨s, q, t⟩ := by rw [h]

/-- **The six atoms of a COMB-doubler rung.**  `sA` is the outward-sweep state, `sB` the
return-sweep state; every other state of `T` is hidden inside an atom, which is why a machine
whose graph is not a relabeling of another's can still satisfy the *same* `Atoms`.

Each field is `∀`-uniform in the tape context — that discipline is not decoration, it is the
whole reason the tile composes and the reason it transports between machines. -/
structure Atoms {S : Type} (T : S → Bool → Option (Bool × Dir × S)) (sA sB : S) : Prop where
  /-- The outward crawl: 4 steps, head `−2`, the two rewritten cells handed to the right
  verbatim.  Note the `∀ b`: the atom never reads the cell it lands on, which is what lets the
  *same* atom scan `(0 1)^u` and step over the `[1,1]` marker. -/
  crawl : ∀ (p : Int) (b : Bool) (L R : List Bool),
    steps T 4 ⟨sA, p, ⟨true :: b :: L, false, R⟩⟩
      = some ⟨sA, p - 2, ⟨L, b, true :: false :: R⟩⟩
  /-- The marker step: the outward sweep reads a `1` and keeps going, writing `0`. -/
  marker : ∀ (p : Int) (x : Bool) (L R : List Bool),
    steps T 1 ⟨sA, p, ⟨x :: L, true, R⟩⟩ = some ⟨sA, p - 1, ⟨L, x, false :: R⟩⟩
  /-- The turnaround: the outward sweep dies on the `0 0` gap and the return sweep is born,
  one cell further left, in `sB`. -/
  turnaround : ∀ (p : Int) (x : Bool) (L R : List Bool),
    steps T 1 ⟨sA, p, ⟨x :: L, false, R⟩⟩ = some ⟨sB, p - 1, ⟨L, x, true :: R⟩⟩
  /-- Return atom S1: 2 steps, head `+2`, rewrites `1 0 ↦ 0 1`.  `sB`-to-`sB`. -/
  swap10 : ∀ (p : Int) (b : Bool) (L R : List Bool),
    steps T 2 ⟨sB, p, ⟨L, true, false :: b :: R⟩⟩
      = some ⟨sB, p + 2, ⟨true :: false :: L, b, R⟩⟩
  /-- Return atom S2: 2 steps, head `+2`, rewrites `0 1 ↦ 1 0`.  `sB`-to-`sB`. -/
  swap01 : ∀ (p : Int) (b : Bool) (L R : List Bool),
    steps T 2 ⟨sB, p, ⟨L, false, true :: b :: R⟩⟩
      = some ⟨sB, p + 2, ⟨false :: true :: L, b, R⟩⟩
  /-- The turn: the return sweep hits the `0 0 0` landing pad, deposits the new `1` and settles
  back into `sA` at `+1`.  This is the rung's `+3` net head advance, and it is why `g ≥ 3` is a
  genuine hypothesis rather than slack. -/
  turn : ∀ (p : Int) (L R : List Bool),
    steps T 3 ⟨sB, p, ⟨L, false, false :: false :: R⟩⟩
      = some ⟨sA, p + 1, ⟨true :: L, false, true :: R⟩⟩

section
variable {S : Type} {T : S → Bool → Option (Bool × Dir × S)} {sA sB : S}

/-! ## §3 The three folds. -/

/-- **The crawl fold** — the outward sweep over `pow10 n`: `4n` steps, head `−2n`, tape
unchanged (the comb is handed over to the right side verbatim). -/
theorem crawlFold (h : Atoms T sA sB) : ∀ (n : Nat) (p : Int) (L R : List Bool),
    steps T (4 * n) ⟨sA, p, ⟨pow10 n ++ L, false, R⟩⟩
      = some ⟨sA, p - 2 * n, ⟨L, false, pow10 n ++ R⟩⟩ := by
  intro n
  induction n with
  | zero => intro p L R; show some _ = some _; simp [pow10]
  | succ n ih =>
    intro p L R
    rw [show 4 * (n + 1) = 4 + 4 * n from by omega, steps_add]
    show (steps T 4 ⟨sA, p, ⟨true :: false :: (pow10 n ++ L), false, R⟩⟩).bind _ = _
    rw [h.crawl p false (pow10 n ++ L) R, someBind, ih (p - 2) L (true :: false :: R),
        pow10_snoc n R]
    exact congrArg some (cfgPos (by omega))

/-- **Fold of S1** — `k+1` return atoms over a `(1 0)^{k+1}` block. -/
theorem sweep10 (h : Atoms T sA sB) : ∀ (k : Nat) (p : Int) (b : Bool) (L R : List Bool),
    steps T (2 * k + 2) ⟨sB, p, ⟨L, true, false :: (pow10 k ++ b :: R)⟩⟩
      = some ⟨sB, p + 2 * k + 2, ⟨pow10 (k + 1) ++ L, b, R⟩⟩ := by
  intro k
  induction k with
  | zero =>
    intro p b L R
    show steps T 2 ⟨sB, p, ⟨L, true, false :: b :: R⟩⟩
        = some ⟨sB, p + 2 * ((0 : Nat) : Int) + 2, ⟨true :: false :: L, b, R⟩⟩
    rw [h.swap10 p b L R]
    exact congrArg some (cfgPos (by omega))
  | succ k ih =>
    intro p b L R
    rw [show 2 * (k + 1) + 2 = 2 + (2 * k + 2) from by omega, steps_add, pow10_cons]
    rw [h.swap10 p true L (false :: (pow10 k ++ b :: R)), someBind,
        ih (p + 2) b (true :: false :: L) R, pow10_snoc (k + 1) L]
    exact congrArg some (cfgPos (by omega))

/-- **Fold of S2** — `k+1` return atoms over a `(0 1)^{k+1}` block. -/
theorem sweep01 (h : Atoms T sA sB) : ∀ (k : Nat) (p : Int) (b : Bool) (L R : List Bool),
    steps T (2 * k + 2) ⟨sB, p, ⟨L, false, true :: (pow01 k ++ b :: R)⟩⟩
      = some ⟨sB, p + 2 * k + 2, ⟨pow01 (k + 1) ++ L, b, R⟩⟩ := by
  intro k
  induction k with
  | zero =>
    intro p b L R
    show steps T 2 ⟨sB, p, ⟨L, false, true :: b :: R⟩⟩
        = some ⟨sB, p + 2 * ((0 : Nat) : Int) + 2, ⟨false :: true :: L, b, R⟩⟩
    rw [h.swap01 p b L R]
    exact congrArg some (cfgPos (by omega))
  | succ k ih =>
    intro p b L R
    rw [show 2 * (k + 1) + 2 = 2 + (2 * k + 2) from by omega, steps_add, pow01_cons]
    rw [h.swap01 p false L (true :: (pow01 k ++ b :: R)), someBind,
        ih (p + 2) b (false :: true :: L) R, pow01_snoc (k + 1) L]
    exact congrArg some (cfgPos (by omega))

/-! ## §4 The rung tile. -/

/-- **The rung tile with its two frozen contexts abstracted.**  `W` is everything at or left of
the `1^c` counter, `Z` everything right of the `1 0 0 0` landing pad.  Neither is read — the
visited window is `[p − 2(u+m) − 6, p + 4]` in *these* variables — which is what makes the tile
composable under `TapeCalc.steps_lpad_dich` / `steps_rpad_dich`.

The nine phases, in order (total `6(u+m)+21`):

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
| 9 | `3` | `turn` | land in `sA` at `+3` -/
theorem rung_core (h : Atoms T sA sB) (u m : Nat) (p : Int) (W Z : List Bool) :
    steps T (6 * (u + m) + 21)
        ⟨sA, p, ⟨pow10 u ++ (true :: true :: (pow01 (m + 1) ++ (false :: false :: W))),
                 false, true :: false :: false :: false :: Z⟩⟩
      = some ⟨sA, p + 3,
          ⟨pow10 (u + 2) ++ (true :: true :: (pow01 m ++ (false :: false :: true :: W))),
           false, true :: Z⟩⟩ := by
  rw [show 6 * (u + m) + 21
        = 4 * u + (4 + (1 + (4 * (m + 1) + (1 + (2 + ((2 * m + 2) + ((2 * (u + 1) + 2) + 3)))))))
      from by omega]
  -- 1 ── outward crawl over `(0 1)^u`
  rw [steps_add, crawlFold h u p (true :: true :: (pow01 (m + 1) ++ (false :: false :: W)))
        (true :: false :: false :: false :: Z), someBind]
  -- 2 ── the same atom carries the head over the first `1` of the `[1,1]` marker
  rw [steps_add, h.crawl _ true (pow01 (m + 1) ++ (false :: false :: W))
        (pow10 u ++ (true :: false :: false :: false :: Z)), someBind]
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
  -- 7 ── the return sweep over the comb
  rw [steps_add, sweep10 h m _ false (false :: true :: W) _, someBind]
  -- the deposit re-phases from `(1 0)` to `(0 1)`
  rw [← pow10_cons u (true :: false :: false :: false :: Z),
      pow10_true (u + 1) (false :: false :: false :: Z)]
  -- 8 ── the return sweep over the deposit
  rw [steps_add, sweep01 h (u + 1) _ false (pow10 (m + 1) ++ (false :: true :: W)) _, someBind]
  -- 9 ── the turn
  rw [h.turn _ (pow01 (u + 2) ++ (pow10 (m + 1) ++ (false :: true :: W))) Z]
  -- the target word, read back through the same two identities
  rw [pow01_shift m (true :: W), pow10_true (u + 2) (pow10 (m + 1) ++ (false :: true :: W))]
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
    (h : Atoms T sA sB) (u m c g : Nat) (p : Int) (TAIL REST : List Bool) :
    steps T (6 * (u + m) + 21) (IN sA u (m + 1) c (g + 3) p TAIL REST)
      = some (IN sA (u + 2) m (c + 1) g (p + 3) TAIL REST) := by
  rw [IN_norm, IN_norm]
  exact rung_core h u m p (ones c ++ TAIL) (zeros g ++ REST)

/-- The tile as a single `Prop`, for clients that want to name it. -/
def Tile {S : Type} (T : S → Bool → Option (Bool × Dir × S)) (sA : S) : Prop :=
  ∀ (u m c g : Nat) (p : Int) (TAIL REST : List Bool),
    steps T (6 * (u + m) + 21) (IN sA u (m + 1) c (g + 3) p TAIL REST)
      = some (IN sA (u + 2) m (c + 1) g (p + 3) TAIL REST)

theorem tile_holds {S : Type} {T : S → Bool → Option (Bool × Dir × S)} {sA sB : S}
    (h : Atoms T sA sB) : Tile T sA := tile h

-- AXIOM AUDIT
#print axioms crawlFold
#print axioms sweep10
#print axioms sweep01
#print axioms rung_core
#print axioms tile
#print axioms tile_holds

end RungCalc
