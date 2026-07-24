# x2 — the remaining work, itemized (2026-07-24 close)

After today the doubling phase `h_doub ∀g` is reduced to a finite list of **register/seam
identities over already-proven theorems** — no unmapped dynamics remain. This is the precise
to-do list. Everything cited as GREEN is `[propext, Quot.sound]` in the 57/57 `lake build`.
**No machine decided. No label upgraded. `x2` remains `[OPEN]`.**

## The proven machines (nothing here is open)

* head descent `descLaw`/`headLaw` (∀k, parity-free)
* ladder `ladderToCascade`; top rung `RegenLawGen`/`topRung`/`topRungToMilestone` (∀U)
* seam `seam74` (∀X); tail `frameFold`/`turn`/`fixedEnd`/`tailLaw` (∀j)
* even topEntry `topEntryEven`/`topEntryEvenLT` and even phase `doubPhaseEven` (M6→M1-frame)
* odd topEntry `carry46`/`carryFold46`/`cross17`/`crossCarry`/`odTurn`/`topEntryOddFull`
* low phase `h_low_even`/`h_low_odd`; padded `hlow_padded`/`hlow_to_phase`; bound `hlow_j_ge`

## The remaining items (all measured; each is one seam/register identity)

1. **`oddTopRungSeam`** — the odd analogue of `topRungSeam`.  Measured: odd `cReg11` (g+8) is
   canonical `cascadeReg 11 1 p (001::U) R` with `U = 0 · frameL(g−1) · turnWord · endWord · L`,
   right `= 0^3 1^2045 …` identical to even.  `topRung` (∀U) fires; the composition
   `topRung ∘ seam74 ∘ tailLaw` needs the odd 1-cell seam `0` where even hard-codes the 9-cell
   `001010100`.  E3-scale re-derivation.  Output: odd `topRungToMilestone`.

2. **`oddSpine`** — `headToLadder` (∀marker', parity-free) ∘ `oddTopRungSeam`.  `descIn(2h+9) →
   M1(g+1)-frame` for odd g.  Mechanical once (1) is done.

3. **`doubPhaseOdd`** — `topEntryOddFull ∘ oddSpine`.  Mirror of `doubPhaseEven`, M8 assembly.
   Anti-vacuity: M6(3)→M1(4) = 8 476 791 (measured).

4. **H upper bound** — pin `j = 10` in `hlow_padded` (lower bound `hlow_j_ge` ≥ 10 done, and
   `∃ j ≤ 16` done).  Either (a) a `steps_left` upper-edge lemma using the measured pos-invariance
   (padded OUT pos ≡ −5 for all pad), or (b) `++ LL` restatements of the five low-phase lemmas
   (`lowEntry` etc., head reaches −3..−6 so `zeros 6 ++ LL` is inert; `p1tLL`-style mechanical
   port).  Then padded `h_low` at both parities.

5. **Obligation-H assembly** — `hlow16 ∘ doubPhase{Even,Odd}` = `M1(g) → M1(g+1)` realized,
   both parities, threading the `[false] ++ zeros 10 = zeros 11` boundary.

6. **F** — `exact x2_nonhalt …` with the §5am families reconciled to the realized configs; cold
   full build; `#print axioms` audit; red-team.  Label discussion only after this.

## Honest scale

Items 1–3 are the odd-branch mirror of what E1/E2/E3 did for even (each ~a session).  Item 4 is
one BlankNorm lemma or one mechanical port.  Items 5–6 are assembly + audit.  None require new
mechanism — the last genuine discovery was the odd carry fold (`carryFold46`), now GREEN.

x2 remains one of the 17 named BB(6) cryptids; closing it decides ONE machine and validates the
template method for the carry-transparent island (~5–8 more).  BB(6) itself stays behind the
(K) wall (14 machines = external normality mathematics), untouched by any of this.

---

## O4 item 1 refined (2026-07-24) — the odd seam is a DISTINCT episode, not `seam74`

Attacking `oddTopRungSeam` under M8/M7, the marker algebra is now exact:

* The odd `cReg11` marker is `0 0 · frameL 2 X`, which IS `0 0 1 · U` with
  `U = 0 1 0 1 0 0 · frameL 1 X` (Lean `rfl`).  So **`topRung` (∀U) fires on the odd cReg11
  directly** — the top-grind rung is shared with the even branch verbatim.
* But `seam74` requires the post-`topRung` left to be `0 1 · U` with
  `U = 0 0 1 0 1 0 1 0 0 · X` (its 9-cell seam).  The odd `U = 0 1 0 1 0 0 · frameL 1 X`
  begins `0 1`, not `0 0` — **`seam74` does NOT fire on the odd register.**

So the odd top→tail seam is a *different* fixed episode than the even 74-step `seam74`.  It
must be measured on its own (its endpoints bracket the odd `topRung` OUT and the odd
`frameFold` tail-IN) and built by M3′, then composed `topRung ∘ oddSeam ∘ tailLaw` into
`oddTopRungToMilestone`.  `topRung` and `tailLaw` are reused; only `oddSeam` is new — a
single fixed episode, the odd counterpart of `seam74`.

**Net:** item 1 splits into `oddSeam` (measure + M3′, ~`seam74`-scale) then a 3-line
composition.  Still no new *fold* or *mechanism* — the odd branch's only Θ-scale novelty
(`carryFold46`) remains done.  The residue is one more fixed episode plus assembly.
