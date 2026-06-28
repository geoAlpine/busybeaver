# The Nested-Collatz structural class — the BB(6) catalogue's second structural axis (2026-06-29)

*Formalizes the common structure shared by the 9 in-family-not-in-scope BB(6) Collatz machines
**{o2, o7, o8, o10-FULL, o11, o12, o13, o14, o16}** as a **named structural class** ("nested-Collatz"),
and proves **why** that structure blocks the exact single-orbit AEV reduction that puts
{Antihydra, o10-inner, o18, o15} in scope. Soundness paramount; every claim carries
`[PROVEN]`/`[CONDITIONAL]`/`[VERIFIED]`/`[OPEN]`, copied/derived from the source documents and never
upgraded. **No machine is decided; no non-halting is asserted.** All numerics this session use
`/Users/aokiyousuke/quantum-ecc/.venv/bin/python` (exact big-ints) on a simulator with bb_sim.py-identical
parse/step; scratchpad `nc_verify{,2,3}.py`.*

Sources consolidated: `REDUCE_O2_O7_O8.md`, `REDUCE_O11_O16.md`, `O10_REDUCTION.md`,
`CATALOGUE_IRREGULAR.md`, `BB6_STRUCTURAL_LIMIT_THEOREM.md` (§3, §7, §8), `MAHLER_3_2_DOMINANCE.md`.

---

## 0. Headline

> The BB(6) Collatz core has **two structural axes**, not one:
>
> - **Axis 1 (in-scope / single-orbit).** A machine's *entire* halting is one arithmetic event of one
>   inner `T_μ`-orbit — a **single-orbit AEV/Mahler equidistribution (or carry-avoidance) statement**.
>   Members: **{Antihydra, o10-inner, o18, o15}** (4).
> - **Axis 2 (nested-Collatz / outer-coupled).** A machine carries a *clean inner* `T_μ` engine, but its
>   **halt couples to an OUTER refill alignment** over **infinitely many reseeded** inner orbits, where the
>   outer refill orbit is **doubly-exponential and not eventually periodic**. Members:
>   **{o2, o7, o8, o10-FULL, o11, o12, o13, o14, o16}** (9; `μ=3/2` for the 8 of them + o10).
>
> **The Blocking Theorem `[PROVEN structural; PROVEN-instance for o10, VERIFIED-instance for the other 8]`:**
> a nested-Collatz machine's exact halt predicate **cannot** be reduced to a single-orbit equidistribution
> of its inner `T_μ`. The halt is structurally **absent from every inner epoch** and can fire **only** at a
> rare outer reconfiguration; deciding it requires an **existence/Borel-Cantelli statement over the
> doubly-exponential outer reseed sequence**, which is strictly beyond the single inner-orbit AEV statement.
> This is *the* in-family-not-in-scope barrier, made precise.

---

## 1. Definition — a nested-Collatz machine  [definitional]

> **Definition (Nested-Collatz machine).** A 6-state TM `M` is **nested-Collatz** if its blank-tape
> evolution decomposes into a two-level structure:
>
> 1. **Inner clean expanding map.** There is a milestone configuration family carrying an integer
>    "mass" `m` (a unary block / sea), and a **clean expanding map** `T_μ` with multiplier
>    `μ = 2^a/3^b`, `v_p(μ) = −1`, such that within one *epoch* the mass evolves by
>    `m → T_μ(m) (+ const)` on an **even / admissible subsequence** of head-passes. `T_μ` is the
>    in-family Collatz kernel (`BB6_STRUCTURAL_LIMIT_THEOREM.md` §4.1).
>
> 2. **Outer counter + refill.** There is a second "outer" quantity (a leading counter, or a
>    block-countdown, or a sea-countdown) that is decremented once per inner step. When the outer
>    quantity **rolls over** (underflows / empties), a **refill subroutine** fires: it re-consolidates
>    the accumulated mass into a fresh, smaller leading block and **re-seeds the inner orbit** (an epoch
>    boundary). The sequence of refill seeds `{B_e}` — the **outer refill orbit** — grows
>    **doubly-exponentially** and is **not eventually periodic**: an epoch with seed `k₀` runs
>    `≈ k₀/Δ` inner `×μ` steps, so the next seed is `≈ μ^{k₀/Δ}` (`O10_REDUCTION.md` §3,
>    `REDUCE_O11_O16.md` §4).
>
> 3. **Outer-coupled halt.** The **halt event couples to the OUTER refill alignment, not the inner
>    orbit**: the local halt mechanic (a `00`-gap collision, a parity eat-sweep, or a phase race) is
>    **structurally impossible during a normal inner epoch** and can be realized **only** at a refill /
>    boundary reconfiguration. Equivalently, the halt-precursor state is visited inside every epoch, but
>    the halt-determining cell is never the halt symbol within an epoch.

**Contrast with the in-scope (Axis-1) machines.** An in-scope machine is the **degenerate** case where the
inner orbit is the *whole* object and the halt is a clean arithmetic event of that single orbit (no outer
reseed governs the halt): Antihydra (`c₀=8`, halt ⟺ density underflow of the one orbit), o18/o15 (one `8/3`
orbit, halt ⟺ that orbit hits the carry-alignment clopen set), o10-**inner** (the inner `⌈3m/2⌉` sub-orbit
in isolation). Nested-Collatz is **strictly richer**: the inner orbit is only the *engine*; the *halt* lives
on the outer reseed sequence.

### 1.1 The nine instances  [PROVEN mechanic + VERIFIED inner]

| machine | inner clean map (admissible subseq.) | outer refill orbit (doubly-exp) | halt mechanic (couples to outer) `[PROVEN]` |
|---|---|---|---|
| **o10-FULL** | `m→⌈3m/2⌉`, eat-length `L=2m−8` **always even** `[PROVEN]` | `B: 5→57→≈2.1·10⁸→…` (piecewise-affine, doubly-exp) | C/F eat-sweep of an **ODD** run; inner runs always even, so halt only at `b`-underflow |
| **o11** | sea `m'=⌊3m/2⌋+4` (12/12 exact) | `3,9,26,303` (`t=10,47,272,28101`), `k→k−4` | C reads a `00`-gap (left); never inside an epoch |
| **o12** | `a'=⌊3a/2⌋+(3δ−1)`, `δ∈{1,2}` | `4,10,28,370` | E reads a `00`-gap (right) |
| **o13** | a-start ratios → 3/2 | `3,6,10,64` (`t=20,51,122,3519`) | D→E eat-sweep of an **EVEN** run; inner runs always odd (o10 mirror) |
| **o14** | a-start ratios → 3/2 + accreting `4,4,2` marker | sea-countdown + marker accretion (never pure block) | C reads a `00`-gap (left) |
| **o16** | sea `s'=⌊3s/2⌋+2` | `k→k−1` doubly-exp | E/F phase race: `0` at F-phase before `1` at E-phase |
| **o2** | leading counter `5,11,65,101,155,…` (nested 3/2 over a `(10)*` sea) | `(10)*`-sea irregular collapse | D→F frontier `00`-gap (right) |
| **o7** | reset orbit `6,11,16,…,316,476,716,1076`, even-`a`: `⌊3a/2⌋+2` | 2-adic halving-cascade refill | F reads 0 ⟺ left counter empty (`00`-left) |
| **o8** | reset orbit `2,4,7,…,160,241`, even-`a`: `⌊3a/2⌋+1`; refill `a₁=⌊a/2⌋−1, b₁=a₁+5` | 2-adic halving-cascade refill | F reads 0 ⟺ left counter empty (`00`-left) |

All nine carry `μ=3/2` (`p=2`) inner content (`MAHLER_3_2_DOMINANCE.md` §1). o2/o7/o8 have a slightly
different outer mechanism (a **2-adic halving cascade** / `(10)*`-sea collapse rather than a leading-counter
countdown), but they satisfy the same three defining clauses: clean inner `3/2` on the even subsequence,
mass-reconsolidating refill, and a halt that fires only at the refill boundary. They are nested-Collatz.

---

## 2. The Blocking Theorem — why the exact reduction fails  [labels stated per clause]

> **Theorem (Nested-Collatz Blocking).** Let `M` be a nested-Collatz machine. Then `M`'s exact halt
> predicate is **NOT** equivalent to a single-orbit equidistribution / carry-avoidance statement about its
> inner `T_μ` (the form that decides the Axis-1 cryptids). Precisely:
>
> **(i) [PROVEN, definitional]** The halt does not occur within any inner epoch. By Definition clause 3 the
> halt mechanic is structurally impossible while the inner orbit runs; the inner map alone therefore has
> **no halt site**, so no statement about the single inner orbit (its density, its parity, its
> mod-`2^k` equidistribution, or its avoidance of a clopen set) can be equivalent to "M halts".
>
> **(ii) [PROVEN structural]** The object the halt predicate quantifies over is the **outer reseed family**
> `{O_e}_{e≥0}` of inner orbits, where `O_e` starts at the doubly-exponential refill seed `B_e`, **not** a
> single inner orbit. `M` halts `⟺ ∃ e :` the `e`-th reseeded inner orbit produces the lethal outer
> alignment at its underflow/boundary. This is an **existence statement over infinitely many restarting
> orbits**, a strictly larger logical object than "the single inner orbit `O_0` equidistributes".
>
> **(iii) [PROVEN-instance for o10; VERIFIED-instance for the other 8]** For o10 the exact predicate is
> *derived* (`O10_REDUCTION.md`): halt `⟺ ∃ epoch whose b-countdown lands on b=0 at odd m`, and the inner
> eat-length `L=2m−8` is **provably always even** (so the inner orbit provably never halts) — the blocking
> is `[PROVEN]`. For o2,o7,o8,o11,o12,o13,o14,o16 the halt **mechanic** is `[PROVEN, unit-tested]` and the
> **inner-never-triggers** fact is `[VERIFIED]` (the halt-determining cell is never the halt symbol across
> millions of inner-epoch visits, §4), but the exact closed-form predicate is **`[OPEN]`** — the outer
> reseed map is not fully modelled. The blocking is `[CONDITIONAL]` on the verified structural model for
> these eight.

**What the exact predicate WOULD require (the excess over the inner AEV statement).** Decomposing `M`'s halt
into ingredients (`O10_REDUCTION.md` §4, `REDUCE_O11_O16.md` §5):

1. **The inner AEV statement** — single-orbit equidistribution of `⌊μⁿ x⌋ mod p`, governing the **parity /
   carry phase of the inner orbit at the underflow index** of each epoch. This is exactly the Axis-1
   object.  **PLUS**
2. **The outer refill map** `B_{e+1} = R(terminal config of epoch e)` — TM-derived, piecewise-affine within
   residue classes, with `B_{e+1} ≈ μ^{(epoch length)}` so `{B_e}` is **doubly-exponential** and not
   eventually periodic.  **PLUS**
3. **An existence / Borel-Cantelli analysis over the reseeds** — whether, for the **deterministic,
   doubly-exponentially-sparse** sequence `{B_e}`, the inner-orbit phase **ever** realizes the lethal
   alignment at a reseeded underflow index. Because each reseed restarts a *fresh* inner orbit, this is a
   hitting/avoidance event evaluated at a **dynamically-determined sparse set of indices across infinitely
   many orbits** — a **Borel-Cantelli-type existence statement over restarts**, requiring **effective**
   equidistribution (a rate beating a summable target), strictly stronger than the **qualitative**
   single-orbit AEV statement that suffices on Axis 1.

> **Slogan.** Axis-1 (in-scope) halt `=` *AEV (single orbit, qualitative density/avoidance)*.
> Nested-Collatz halt `=` *AEV (parity-at-underflow, per epoch) ⊗ outer refill map ⊗ Borel-Cantelli over
> doubly-exp reseeds*. The first factor is the Axis-1 object; the last two are the irreducible excess that
> blocks the reduction.

---

## 3. Sharp classification — the catalogue's second structural axis  [PROVEN organizational]

| | **Axis 1 — single-orbit (in-scope)** | **Axis 2 — nested-Collatz (in-family, not in-scope)** |
|---|---|---|
| **count** | 4 | 9 |
| **members** | Antihydra, o10-inner, o18, o15 | o2, o7, o8, o10-FULL, o11, o12, o13, o14, o16 |
| **what halts** | the whole machine **is** one inner-orbit event | a refill alignment over **∞ reseeded** inner orbits |
| **halt object** | single orbit `O_0` of `T_μ` | reseed family `{O_e}`, `B_e` doubly-exp |
| **exact predicate** | **derived** (`[PROVEN]` reduction) | o10 derived `[PROVEN]`; other 8 `[OPEN]` (mechanic `[PROVEN]`, inner-never `[VERIFIED]`) |
| **logical form** | density (Π⁰₂) **or** single Π⁰₁ avoidance, of ONE orbit | Π⁰₁ avoidance (∀e ∀step) over a doubly-exp **family** = existence/Borel-Cantelli over restarts |
| **needs** | qualitative AEV (Antihydra: weak one-sided `k=2` fragment over-implied) | qualitative AEV ⊗ outer map ⊗ **effective**-rate existence over reseeds |
| **proven barrier** | Antihydra `β>0` density `[PROVEN]`; o10-inner `[CONDITIONAL]` | none on the density axis (existence facet, no `β`); blocked by doubly-exp outer (§2) |
| **generic direction** | non-halt (Antihydra density floor) | **opposite**: genericity tends to make it **halt** (∞ reseeds, each w.p. >0) — but per-epoch prob extractable only for o10; direction `[OPEN]` for all 9 |

The two axes are **orthogonal**: Axis 1 distinguishes *the halt is a single-orbit event*; Axis 2 is the
**outer-reseed composite** structure. o10 is the pivot: its **inner** sub-orbit is the cleanest Axis-1
object (literal AEV ceiling `⌈3m/2⌉`), while its **full** machine is the canonical Axis-2 object — the same
machine sits on both axes at different granularities, which is exactly why it is the template.

---

## 4. Where nested-Collatz sits relative to the in-scope cryptids  [characterized honestly]

Nested-Collatz is **strictly above** the in-scope cryptids in the relevant hierarchy — it is a **composite**
of the in-scope object with an extra existence layer:

- **It contains the Axis-1 object as a sub-factor.** Ingredient 1 of §2 *is* a single-orbit AEV statement
  (per-epoch parity-at-underflow). So nested-Collatz is **not less** than the in-scope cryptids; resolving
  it requires (at least) resolving the same inner equidistribution that the in-scope cryptids need.
- **Plus a Borel-Cantelli / effective-rate layer over restarts** (ingredients 2–3). The in-scope cryptids
  reduce to a statement about **one** orbit; nested-Collatz adds an **existence quantifier over a
  doubly-exponential family** of orbits and demands an **effective** equidistribution rate (to control a
  summable hitting target over the reseeds). In the `BB6_STRUCTURAL_LIMIT_THEOREM.md` §7.1 two-facet
  language this is the **existence facet** (`invariant SET` / over-approximation top), evaluated not once
  but over a doubly-exp index family — so on the certificate axis it lies at the **`[OPEN]`
  over-approximation top** (no finite-state / semilinear / 2-automatic over-approximation closes: all nine
  are FAR/CEGAR HOLDOUT, `REDUCE_O11_O16.md` §0).
- **Direction is reversed from Antihydra (the Borel-Cantelli signature).** On Axis 1, Antihydra's density
  floor pushes toward **non-halt**. On Axis 2, a heuristic Borel-Cantelli reads the opposite way: if each
  reseed independently realizes the lethal alignment with probability `p>0`, then over **infinitely many**
  reseeds the machine halts with probability `→1` (o10's `[OBSERVED]` `≈1/3` per epoch ⇒ likely a **delayed
  halter**). This is the honest "genericity ⇒ halt" reading. **But** unlike o10, the per-epoch halt
  probability is **not cleanly extractable** for the other eight (the outer reconfiguration is
  `δ`-coupled / marker-accreting / phase-dependent), so **no direction is claimed** — `[OPEN]` for all
  nine, and the all-odd (o13) / `00`-avoiding (o11/o12/o14) / exit-wins (o16) observations lean *non-halt*,
  the **opposite** of o10's lean, underscoring that the direction is genuinely undetermined.

> **Net placement.** Nested-Collatz `=` in-scope single-orbit AEV object **+** a doubly-exponential outer
> reseed map **+** a Borel-Cantelli-over-restarts existence test. It is a strict super-structure of the
> in-scope cryptids on the equidistribution side and sits at the over-approximation `[OPEN]` top on the
> certificate side. It is the precise formal content of "in-family-by-multiplier, not-in-scope-by-proof."

---

## 5. Numerical verification (this session, bb_sim-faithful, exact big-ints)  [VERIFIED]

Representative machines o10, o11, o13 (+ o8 non-halt). Scripts `nc_verify{,2,3}.py`; all use bb_sim.py's
exact parse/step.

**(A) Inner clean expanding map on the admissible subsequence.**
- **o10** `[VERIFIED, consistent with O10_REDUCTION.md PROVEN]`: 16 completed C/F eat-sweeps in 2·10⁶ steps,
  lengths `4,10,20,34, 4,10,20,34,56,88,136,208,316,478,722,1088` — **all EVEN, zero odd**. The reset to
  `4,10,20,34,…` at the 5th eat is the outer **refill re-seeding** the inner orbit (epoch boundary). The
  inner mass orbit `m→⌈3m/2⌉` from `m=6` is `6,9,14,21,32,48,72,108,162,243,365,548,822`, eat-length
  `L=2m−8 ∈ {4,10,20,34,56,…}` all even — so by the (HALT-MECHANIC) "halt ⟺ odd eat" the inner loop
  **provably never halts**.
- **o11** `[VERIFIED]`: documented sea `2,7,14,25,41,65,101,155,236,358,541,815,1226` satisfies
  `m'=⌊3m/2⌋+4` **12/12 exact**; ratios `→1.5043`.

**(B) Outer refill orbit is doubly-exponential.** Tracking pure single-1-block reconsolidation peaks:
- **o13** `[VERIFIED]`: growing epoch-seed peaks reach `k=64` at step `3326` (matching the documented refill
  `3,6,10,64`, `t≈3519`); the next seed lies `≈μ^{64/Δ}` further — astronomically far.
- **o11** `[VERIFIED]`: reaches `k=201` at step `12088`, then `k=582` at step `56237` — the per-epoch
  runtime `≈k/4` inner steps gives next-seed `≈(3/2)^{k/4}`, the doubly-exponential jump (`26→303` is ×11.6
  documented).

**(C) Halt couples to OUTER, not inner.** Generic halt-precursor instrumentation (the unique state with a
HALT transition), 2·10⁶ steps:

| machine | halt-precursor (state,read) | precursor visits in 2M | halt fired? |
|---|---|---|---|
| o10 | `(F,0)` | **1614** | **NO** |
| o11 | `(C,0)` | **1498** | **NO** |
| o13 | `(E,0)` | **1474** | **NO** |

The halt-precursor state is entered ~1500 times **per machine within inner epochs**, yet the halt
transition **never fires** — the halt-determining cell is never the halt symbol during an epoch. This is the
operational confirmation of Definition clause 3 / Blocking Theorem (i): the halt is **structurally absent
from every inner epoch** and can only be reached at an outer reconfiguration. (Cross-check: o2/o7/o8/o12/o14
/o16 all `[VERIFIED]` non-halting and inner-never-triggering in `REDUCE_O2_O7_O8.md` §2 and
`REDUCE_O11_O16.md` §3, with 2330/2330, 3516/3516, 1996/1996, 7214/7214 inner visits all non-lethal.)

All four representatives `[VERIFIED]` non-halting to 2·10⁶ steps (o10 1418 ones, o11 2047, o13 1448, o8 812),
consistent with the documented 10M–120M holdouts.

---

## 6. Soundness summary (labels enforced, none upgraded)

- **Definition** of nested-Collatz: `[definitional]`, with 9 instances, the three clauses each backed by
  `[PROVEN]` (halt mechanic) + `[VERIFIED]` (inner map, inner-never-triggers) facts from the source docs and
  re-confirmed here.
- **Blocking Theorem**: clauses (i)–(ii) `[PROVEN structural]`; clause (iii) `[PROVEN]` for **o10**
  (exact criterion derived + inner provably always-even), `[CONDITIONAL]`/`[VERIFIED]` for the other **8**
  (mechanic proven, inner-never-triggers verified, exact predicate `[OPEN]`).
- **The exact nested-Collatz predicate** = single-orbit AEV (parity-at-underflow, per epoch) ⊗ outer refill
  map (doubly-exp) ⊗ **Borel-Cantelli existence over reseeds** (effective rate). Strictly beyond the
  single inner-orbit AEV statement. `[PROVEN structural]`.
- **Classification**: Axis 1 (single-orbit, 4 machines) vs Axis 2 (nested-Collatz, 9 machines) is a
  `[PROVEN organizational]` second structural axis; the scope set
  {Antihydra, o10-inner, o18, o15} of `BB6_STRUCTURAL_LIMIT_THEOREM.md` is **unchanged**.
- **No machine is decided; no non-halting is asserted; no direction is claimed** (o10 leans halt; the other
  8 lean non-halt; all `[OPEN]`). Numerics exact-bigint, bb_sim-faithful.
