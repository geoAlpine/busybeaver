# Counter-automaton verifier for o4 — build turn 4: local halt-freeness is ALSO non-regular; o4 needs a base-4/3 digit-string verifier (2026-07-05)

*Turn 4: try the local halt-freeness invariant (redirect (b)) via the **sound** `far_dfa.verify()` on observed
`m`-gram gram-sets at larger orders. **HOLDOUT through `m=26`.** So even *halt-freeness alone* has **no regular (sofic
`m`-gram) certificate** — closure of any regular over-approximation re-admits halting/escaping configs, because keeping
the orbit halt-free requires the **big-gap counting** the sofic language cannot express. Both redirections converge:
o4's decision needs a **base-4/3 digit-string certificate + a sound verifier for that class** — genuine new,
must-be-validated tooling. SOUNDNESS: `[VERIFIED negative]`; o4 `[OPEN]` — **not decided**. No machine decided.*

## The test and result `[VERIFIED via sound verify()]`
`far_dfa.prove` builds `m`-gram gram-sets from sampled reachable configs and runs the **sound** abstract-closure
`verify()` (start-in-L, halt-exclusion, closure over all moves). Ran at `m = 10,14,18,22,26`, samples up to `3·10⁴`:
**HOLDOUT — no verified invariant.** Combined with the earlier `m≤16` HOLDOUT, **no `m`-gram invariant up to order 26
is closed and halt-free.**

## Why local halt-freeness is still non-regular `[reasoning]`
Halting is `B` reading a `1` with right-neighbour `1`. A regular (sofic) over-approximation `S ⊇ reachable` that is
**closed** must contain the successors of everything it admits; because the sofic language cannot track the **big-gap
length** (`base-4/3` counter), any `S` coarse enough to be regular and contain the reachable orbit also contains
configs whose successors **halt or escape** — so `verify()` finds a witness. The transient `[2]` (`11`) blocks exist,
and excluding "`B` on the left `1` of a `[2]`" **for all time** needs the odometer timing, which is non-regular.
Halt-freeness is *locally checkable* but *not locally provable* — its **invariance** is global (counting).

## Where the multi-turn build stands `[honest ledger]`
- **T1** ✓ architecture: bouncer over a base-4/3 counter; halt-freeness reduced to a structural fact.
- **T2** ✓ a **validated** sound period-`p` accelerator (`o4_accel_sound.py`, exact-match incl. tape to 2·10⁶).
- **T3** ✗ uniform-per-residue closure fails — generation has `~log G` phases (base-4/3 **digit-string** dependent).
- **T4** ✗ local halt-freeness has no regular certificate either (m-gram HOLDOUT to `m=26`).
**Converged conclusion:** o4 is Fork-A (invariant exists, explicit `0^G(10)^a1001`) but its certificate is
**irreducibly non-regular** — it must model the **base-4/3 odometer's variable-length carry (digit string)**. Deciding
o4 requires a **sound base-4/3-odometer closure verifier** (checks the AFS successor preserves the valid-representation
language + `11`-freeness) — **new tooling that must itself be validated** before any decision it emits is trustworthy.
Producing a decision from unvalidated tooling would be a false proof; not done.

## Verdict
**(c) — turn 4 honest negative; the whole regular-tool avenue is now closed for o4.** No `m`-gram (`≤26`) certifies o4,
even for halt-freeness alone — its invariant is irreducibly non-regular (base-4/3 counter). o4 stands as **Fork-A with
an explicit non-regular invariant and a validated accelerator**, but a rigorous decision needs a **validated
base-4/3-odometer verifier** (substantial new tooling). **o4 is not decided.** **Halting `[OPEN]`. No machine decided.
No label upgraded.**

## Reproduce
- `far_dfa.prove(o4, ms=(10,14,18,22,26))` = HOLDOUT (sound `verify()`). Basis: `O4_VERIFIER_BUILD_T1/T2/T3_2026-07-05`,
  `O4_FAR_VERIFICATION_2026-07-05` (non-regularity), `o4_accel_sound.py`.
