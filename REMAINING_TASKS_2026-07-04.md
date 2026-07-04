# Remaining tasks — organized inventory (2026-07-04)

*Task map after the 2026-07-03/04 cryptid campaign. Supersedes nothing in `PROBLEM_LIST.md` (P0–P13); it
records what is **DONE**, what is **ACTIONABLE**, and what is **GENERATIONAL** (no internal route). SOUNDNESS:
nothing here is claimed solved.*

## DONE (this campaign) ✅

- **o17 core** — full `[PROVEN]`-level characterization: finite-control base-3 digit-string transducer; the
  unbounded-digits + polynomial-growth obstruction unified as a free-running LSB counter; **halt predicate
  `[PROVEN]`-reduced to one parity bit** (leading block ever even); the no-jump residual dissected and shown
  **core-hard**. (`O17_CORE_TRANSDUCER.md`.)
- **o3** — brought to o17's standard; the **second Type-II structural outlier** (bounded `{0,1}` digits, PROVEN
  halt gate, carry cascade dissected to the no-jump analogue). (`O3_TRANSDUCER.md`.)
- **9 slow-width cryptids reverse-engineered & classified** into a machine-verified **trichotomy** (Type I
  Mahler-3/2 ×11; Type II outliers o17, o3; Type III scalar-Collatz Space Needle). `√t` shown non-diagnostic.
  (`CRYPTID_CLASSIFICATION_2026-07-04.md`, `CRYPTID_SLOWWIDTH_2026-07-04.md`.)
- **All 9 halt predicates `[PROVEN from table]`** (unique-predecessor gates, blank never-fire verified).
  (`MAHLER_HALT_GATES_2026-07-04.md`, `SPACE_NEEDLE_HALT.md`, `O2_O7_HALT.md`, `o3_transducer.py`.)
- **(K) fresh-angle probe** — verdict (c): the two-counter/reachability framing gives **no new handle**.
- **Soundness audit** — VERDICT **SOUND**; 2 in-session errors (Space Needle all-ones; o7 coordinate) caught &
  corrected. (`CRYPTID_AUDIT_2026-07-04.md`.)

## ACTIONABLE — status

- **A1. Space Needle halt-set `S`** ✅ DONE. `S = {2^k−1} ∪ {sporadic}`; `sporadic∩[1,255]={6,102}` (`6=2·3`,
  `102=2·3·17`), very sparse. Blank orbit avoids all of `S`. Exact sporadic rule = small `[OPEN]` sub-curiosity.
  (`SPACE_NEEDLE_HALT.md` §3.)
- **A2. 1104-holdout frontier census** ✅ DONE. Structurally homogeneous: 1104 slow polynomial counters (√t 665,
  sub-√t 399; 0 halt, 0 exp-width); bounded-digit (o3-class) ~522 (~half; proxy split ~183 kernel-less / ~176
  odometer); sound suite 0/15. (`BB6_FRONTIER_CENSUS_2026-07-04.md`, `holdout_census*.py`.)
- **A3. External packaging** ✅ DONE. `BB6_CRYPTID_PACKAGE.md` — trichotomy + 9 PROVEN halt gates + Type-II
  dissections + census + the two walls, shareable alongside `BB6_FRAMEWORK_PACKAGE.md`.
- **A4. o4 TM** ✅ DONE (found in repo, not missing): `o4 = 1RB0LD_1RC1RF_1LA0RA_0LA0LE_1LD1LA_0RB---`
  (`cryptid_map.py`). Not yet reverse-engineered (a follow-up if wanted).

### Follow-ups
- **A5. Reverse-engineer o4** ✅ DONE (`O4_HALT.md`, `o4_transducer.py`). **Type I with a NEW ratio `μ=4/3`
  (`v₃=−1`, kernel prime 3)** — exact closed base-4/3 odometer `G'=⌊4G/3⌋+c(G mod3)` (residual 0, ratio→1.33338),
  `[PROVEN]` **11-existence** halt gate (dual to o3's 00; 0 firings/15M). Adds a third census ratio (3/2, 8/3,
  4/3) and flips o3's "4/3=envelope" to "genuine value". Now **15 named cryptids** classified.
- **A6. Type-I/II proxy split of the ~522 bounded-digit band** ✅ DONE (`holdout_band_split.py`): ~234
  Type-II-like (o3-class, incl. 79 binary-exact) / ~190 bounded-radix odometers / ~100 ambiguous — the o3-class
  is ~21% of the frontier. A clean per-machine split still needs reverse-engineering (open).

## Frontier structure — the classification is a TETRACHOTOMY `[2026-07-04, done]`

Trichotomy-extension test (5 un-analyzed holdouts, `BB6_TRICHOTOMY_EXTENSION_2026-07-04.md`): confirmed Type I
(H1), Type II (H2, H3, H4), and found a **NEW Type IV** (H5, fixed-arity nested-counter bouncer). Growth-rate is
**fully orthogonal to type**; the census A6 Type-I proxy was optimistic (H4 refutes it). B1-side attack
(`BB6_TWO_WALLS`): B1/B2 are provably-distinct objects (entropy/spectral separation), o4 the bridge — no crack.

### Follow-ups
- **A7. Characterize Type IV** ✅ DONE (`BB6_TYPE_IV_CENSUS_2026-07-04.md`). Type IV is a distinct PHENOTYPE
  (bounded-arity counter bouncer), now POPULATED beyond H5 (L997 = −2 countdown; inner map varies), but **NOT a
  distinct wall** — halt = generalized-Collatz counter-machine reachability = the **B2 wall** shared with II/III;
  decidability `[OPEN]`, Collatz-class. Durable: the 4-way phenotype tetrachotomy **projects onto a 2-way WALL
  dichotomy** {I→B1=(K)/Mahler, II/III/IV→B2=gen-Collatz}.
- **A8. Larger extension sample** ✅ DONE (`BB6_TYPE_IV_CENSUS_2026-07-04.md`). **Global fingerprint of all 1104
  holdouts**: **NO 5th type** (tetrachotomy stable at 4; within-type inner-map is a continuous parameter, not a new
  type). Census: **80 % Type II** growing-digit cascades, **0 halters** in 300 K, bounded-arity band a MIX
  (over-counts I/IV). **Bonus: 2 new ratio-verified Type-I Mahler ×3/2 cryptids** (L373, L921).

### Follow-ups
- **A9. Halt gates for the 2 new Type-I (L373, L921)** ✅ DONE (`BB6_TYPE_IV_CENSUS_2026-07-04.md` §5b). Both
  carry the identical `00`-existence gate as the named `00`-family: halt = F/D read 0, unique predecessor C read 0
  (write 1, move L) ⇒ `HALT ⟺ C reads 0 with left-neighbour 0`; `[PROVEN from table]`. Blank-orbit invariant
  `[OBSERVED, 100 M]`: C:0 events all have left-neighbour 1 (7645 / 7333 firings, never 00). Reduction: `HALT ⟺`
  the `×3/2` orbit ever aligns the leading counter to the outer 0 = `(K)`-class, like the family. Non-halt `[OPEN]`.
- **A10. Clean per-machine Type-II/IV split** ✅ DONE — **negative/(b)** (`BB6_TYPE_IV_CENSUS_2026-07-04.md` §5c). A
  clean per-machine split is **`(K)`-hard**, proven by discriminator-dependence (max-block-value → IV 29; snapshot
  `#blocks`-trend → IV 27/II 8/I 5); phenotypes form a continuum (active leading counter + settled digits). Clean
  cases split (II ≈ 8, I ≈ 5, IV ≈ several); the I↔IV boundary = detecting positive entropy of the driver =
  `(K)`-adjacent. Empirically confirms the B1/B2-probe theoretical result.

- **A11. Halt gates for the clean-IV (H5-class) machines** ✅ DONE (`BB6_TYPE_IV_CENSUS_2026-07-04.md` §5d). RE'd 7
  clean-IV gates to `[PROVEN from table]`: all unique-predecessor adjacency-existence gates (5 `00`, 2 `11` incl.
  H5), blank never fires (30 M, read-on-entry histogram uniform-safe; H5 210 641 entries all safe, one machine
  3.75 M all safe). **The halt-gate mechanism is UNIFORM across the whole tetrachotomy** — same `00`/`11`
  existence family as I/II/III; only the *substrate* the existence runs over selects the wall (Mahler orbit → B1;
  cascade/counter → B2). Non-halt `[OPEN]` for all.

### Follow-ups (still open)
- *(none pressing internally — the frontier map, phenotype/wall classification, halt gates, and both walls are
  characterized; remaining progress is generational (B1/B2) or external.)*

## GENERATIONAL — no internal route (documented, not action items)

- **B1. (K) / P1 — the Mahler-3/2 kernel.** Unlocks **all 11 Type-I cryptids at once** (Antihydra, o2, o7, o10,
  o11, o12, o13, o14, o15, o16, o18) — each Type-I halt gate reduces to single-orbit equidistribution of a
  `⌊3x/2⌋` (or `⌊8x/3⌋`) orbit. Proven internal barriers (No-Structure, Coverage No-Go, decider-preemption,
  even-count floor); needs generational new math (`PROBLEM_LIST.md` P1/P1′) or external movement on AEV/Mahler.
- **B2. Generalized-Collatz for Type II/III.** o17, o3 (Type II) and Space Needle (Type III) reduce to
  generalized-Collatz reachability over their own carry cascade / scalar orbit — a Collatz-type statement with
  **no bounded predictor** (verified core-hard). Distinct from (K); each needs a Collatz-class breakthrough.

## CLOSED / not-independent

- **P8–P13** (`PROBLEM_LIST.md`): proven `(K)`-hard/equivalent (`#even`, drift>0, quenched Cramér) or dead ends
  (independence question). Not separate handles.

## Suggested next (highest leverage among ACTIONABLE)

**A2 (1104-holdout census)** maps the real BB(6) frontier and is genuinely new; **A3 (packaging)** is the
memory's stated priority and banks the durable contribution; **A1 (Space Needle `S`)** is the quick clean win.
B1/B2 remain the walls — external, generational.
