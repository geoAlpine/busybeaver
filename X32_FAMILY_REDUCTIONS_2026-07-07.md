# The ×3/2 balance family, machine by machine: o2, o7, o10 — precise reductions, one confirmation, one misclassification, three corrections (2026-07-07)

*Extends the BB(6) census with per-machine GATE / STRUCTURE / PROTECTION reductions for the three machines the
2D classification (`CRYPTID_2D_CLASSIFICATION_2026-07-05.md`) filed with Antihydra as "×3/2 balance / B1 density":
**o2, o7, o10**. Model: Antihydra's proven chain (non-halt ⟺ even-density ≥ 1/3 = `(K)`,
`BB6_FRAMEWORK_PACKAGE.md` §1–2). SOUNDNESS: every link labeled `[PROVEN]` / `[PROVEN given the automaton]` /
`[OBSERVED]` / `[OPEN]`; all numerics exact big-int (`/Users/aokiyousuke/quantum-ecc/.venv/bin/python`);
scripts `x32_gate_census.py`, `x32_o2_reduction.py`, `x32_o7_reduction.py`, `x32_o10_reduction.py`.
**No machine decided.***

## 0. Headline

| machine | value kernel (exact) | halt event (exact) | protection shape | seeded (K)-instance? |
|---|---|---|---|---|
| **o2** | `y ↦ ⌈3y/2⌉` from **y₀ = 2** (via `y=(a+4)/3`, exact conjugacy) | ledger `b = 1+3E_n−n` hits `0` at `y ≡ 3 (mod 4)` | **cumulative density ledger** — Antihydra's balance functional verbatim, PLUS a mod-4 escape hatch | **YES — literal ceiling-(K), seed 2** |
| **o7** | `x ↦ 3x/2` (x even), `x ↦ (x+1)/2` (x odd), x=a+4 — **NOT** a `⌊3c/2⌋`/`⌈3c/2⌉` orbit | some milestone has `a+3 = 2^k` (exact power of 2) | **thin-set / 2-adic exact-power avoidance** — B2 reachability, no ledger | **NO — misclassified**: not Antihydra-species |
| **o10** | `m ↦ ⌈3m/2⌉` from **m = 6, reset every epoch** | reseed orbit `B_e` hits `S_halt` (density → 1/3) | **anti-equidistribution** (generic verdict = HALT); resetting memory | **inverted** — the (K)-type statement lives in the *target*, not the protection |

The family named "×3/2 balance (Antihydra-species)" contains **one true congener (o2), one misclassified
machine (o7), and one mirror (o10)**. Three corrections to banked notes were found and raw-TM-settled (§4).

---

## 1. o2 — a second Antihydra: the ceiling-(K) instance with an escape hatch

`o2 = 1RB1RC_1LC1LE_1RA1RD_0RF0RE_1LA0LB_---1RA` (halt `F,0`).

### 1.1 Gate `[PROVEN from table]` + census `[OBSERVED]`
Unique edge into F: `D,0→0RF` ⟹ **HALT ⟺ state D reads a 0 whose right neighbour is 0**.
Census (blank, 20M steps, `x32_gate_census.py`): 4,295 trigger events, **0 firings**; distinct halt-windows
saturate at **3 (r=3) / 4 (r=4,5), last new at step 209**. All safe. The gate is never the obstruction.

### 1.2 Structure — milestone automaton and the exact value law
**Milestone** = state A at the left frontier reading 0; tape = `0 · 11 · (01)^a · 0 · 11 · (01)^b`.
Automaton (from `CRYPTID_SLOWWIDTH_2026-07-04.md` §1) `[OBSERVED, 0 mismatches: 15 consecutive raw
transitions + 103 seeded raw-TM configs covering all four branches, a=1..41, b=0..2]`:

```
a even:        D(a,b) -> D((3a+4)/2, b+2)
a odd, b>=1:   D(a,b) -> D((3a+7)/2, b-1)
a odd, b=0:    -> S(N), N=(3a+11)/2;  S(N) -> HALT if N odd, else D((3N-2)/2, 1)
```

**Value law `[PROVEN given the automaton — exact algebra, 0 numeric violations]`.**
`a+4 ≡ 0 (mod 3)` at every milestone, and `y := (a+4)/3` obeys **`y' = ⌈3y/2⌉` exactly on both D-branches**
(a even ⟺ y even; blank seed `D(2,1)` ⟹ `y₀ = 2`, ladder `2,3,5,8,12,18,27,41,62,…`). The b=0 escape branch
is exactly **two** ceiling steps at once. Equivalently `x = a+4` obeys `x' = 3⌈x/2⌉`.
> **Correction 1.** The banked claim (`CRYPTID_SLOWWIDTH` §1, echoed in `O2_O7_HALT.md`) that
> "`x=a+4` satisfies `x ↦ ⌊3x/2⌋`" is **false as stated** (its own ladder violates it: `9 → 15 ≠ ⌊27/2⌋ = 13`).
> The correct exact law is `x ↦ 3⌈x/2⌉`, i.e. the **ceiling map on `y = x/3`**. The ladder itself was right.

So o2's kernel is the **literal AEV Conj-1.6 ceiling map at 3/2** — the same operator as o10-inner, on the
**seed-2 orbit** (permanently disjoint from o10's seed-6 orbit: `⌈3·/2⌉` maps evens into `0 mod 3` and odds
into `2 mod 3`, hence is injective — distinct orbits never merge). Template lens: not needed — o2 is
Antihydra-like (two-counter milestone automaton, no template extraction required; the automaton IS the structure).

### 1.3 Protection — literally (K) with seed 2, plus an escape hatch
**Ledger identity `[PROVEN given the automaton]`:** `Δb = +2` iff y even, `−1` iff y odd ⟹ between escapes
> **`b_n = b_0 + 3E_n − n`**, `E_n` = # even `y` among `y_0..y_{n−1}` — **Antihydra's balance functional verbatim.**

**Halt criterion `[PROVEN given the automaton; seeded-verified]`:** b hits 0 only at odd-y steps, and
> **o2 HALTS ⟺ b = 0 at a milestone with `y ≡ 3 (mod 4)`** (`⟺ a ≡ 1 (mod 4)`; raw-TM-confirmed: seeds
> `D(a,0)` halt exactly for `a = 1,5,9,…,41`, 11/11); at `y ≡ 1 (mod 4)` the machine **escapes**
> (two ceiling steps, ledger resets to 1).

**Species placement.** o2's protection is **literally a seeded `(K)`-instance**: non-halt **⟸**
`3E_n − n ≥ 0 ∀n` = one-sided even-density ≥ 1/3 for the **ceiling** orbit from seed 2 (the AEV side — where
Antihydra's `(K)` is the floor-mirror from seed 8). Note the implication is one-way: o2's halt event is a
**strict sub-event** of ledger-underflow (underflow at `y≡1 mod 4` survives). o2 is *more* protected than
Antihydra — same critical density, plus a parity hatch at every zero-touch.

**LEDGER-MEMORY axis: CUMULATIVE** (Antihydra-type). On the blank orbit the ledger never resets:
**0 escapes** in 100,000 exact ceiling steps. Contingent resets exist in the automaton but are unexercised.

**Margins `[OBSERVED]`** (abstract exact iteration, 100k steps): even-density `0.50002` (Haar ½; checkpoints
0.508 / 0.494 / 0.498 / 0.50002 at 10³/10⁴/5·10⁴/10⁵); `b ≈ n/2` (b = 50,007 at n = 10⁵); **worst prefix
`3E_n − n = 0` at n = 3** (i.e. b touched 1 — one unit from the zero-touch, which would then still have needed
`y ≡ 3 mod 4`); min b at odd-y entries = 1. Same critical zero-margin *early* profile as Antihydra (min
balance +2), same +1/2 drift *asymptotically*.

### 1.4 Reduction theorem (the Antihydra-style chain)
> **non-halt ⟺ the ledger process `(y_n, b_n)` from `(2, 1)` never reaches `b=0 ∧ y ≡ 3 (mod 4)`**
> **⟸ liminf even-density of the `⌈3y/2⌉`-orbit of 2 ≥ 1/3** (with the finite check `3E_n−n ≥ 0`, verified n ≤ 10⁵).

Links: gate `[PROVEN from table]` → milestone automaton `[OBSERVED, 0-mismatch raw + seeded]` → conjugacy +
ledger identity + halt criterion `[PROVEN given the automaton]` → density sufficiency `[PROVEN, elementary]` →
**the density itself = ceiling-(K), seed 2 `[OPEN]`**. The one unproven link is exactly the `(K)`-shaped one.
*(The automaton link is the analogue of Antihydra's Link 0, which there is `[PROVEN]`; here it rests on
0-mismatch verification over 15 raw transitions + 103 seeded branch checks, not a certified induction — the
honest gap between `[PROVEN]` and `[OBSERVED]` for o2.)*

**Verdict: o2 IS Antihydra-species** — the census's second genuine one-sided ×3/2 density ledger, and the
first on the **ceiling/AEV side**. The B1-density call of `CRYPTID_2D_CLASSIFICATION` **survives, sharpened**.

---

## 2. o7 — NOT Antihydra-species: a 2-adic exact-power (thin-set) machine

`o7 = 1RB0RB_1LC1RE_1LF0LD_1RA1LD_1RC1RB_---1LC` (halt `F,0`).

### 2.1 Gate `[PROVEN from table]` + census `[OBSERVED]`
Unique edge into F: `C,0→1LF` ⟹ **HALT ⟺ state C reads a 0 whose left neighbour is 0**.
Census (20M steps): 3,601 triggers, **0 firings**, windows saturate at **3/3/4 (r=3/4/5), last new step 224**.

### 2.2 Structure — coupled two-counter map; the value orbit is NOT ×3/2
**Milestone** = state D at left frontier reading the 0 adjacent to the first block; tape = `0 1^a 0 1^b`.
Map `[OBSERVED, 0 mismatches: 29 consecutive raw transitions + 124 seeded one-step configs (a=1..31, b=1..4)
after one correction]`:

```
a even >= 2: (a,b) -> (3a/2 + 1 + b, 1)
a odd  >= 5: (a,b) -> ((a-3)/2, b + (a+5)/2)
a = 3:       (a,b) -> (b+5, 1 + [b odd])      <- CORRECTED (see §4)
a = 1:       HALT
```

**The value map is not Mahler `[PROVEN given the automaton]`.** On `x = a+4`: even x → `3x/2`, **odd x →
`(x+1)/2`** — a *halving*, where `⌊3x/2⌋`/`⌈3x/2⌉` have `(3x±1)/2`. No shift conjugacy `c = x+k` can repair
both branches (even branch forces `3k/2 = k` ⟹ k=0; k=0 fails the odd branch). The ×3/2 seen in the banked
reset ratios is only the even-branch chain; **the "counter law is `c → ⌊3c/2⌋`-like" premise fails**.
The growth is carried by mass conservation through `b` (odd steps: `a+b → a+b+1`; even steps re-absorb b).

**Cascade law `[PROVEN given the automaton; 0 raw violations]`:** on odd steps `u := a+3` **halves exactly**
(`u' = u/2`). A cascade entered at odd `a` runs exactly `v₂(a+3)` milestones and exits at
`a_end = oddpart(a+3) − 3` (or hits the `a=3` branch iff `oddpart(a+3) = 3`).

### 2.3 Protection — thin-set avoidance, no ledger, no density
`b ≥ 1` is invariant; **no branch of the automaton tests b against 0** — there is **no balance-returns-to-zero
event in o7 at all**. The halt is `a = 1`, and by the cascade law:

> **o7 HALTS ⟺ some milestone value satisfies `a + 3 = 2^k` (k ≥ 2), i.e. `oddpart(a+3) = 1`.**
> `[PROVEN given the automaton]`; raw-TM-confirmed on a seeded grid (12 decided multi-step seeds, 0 mismatches;
> confirmed halting seeds include `(2,1),(5,·),(13,·),(9,1),(18,·)` — each hits `a+3 ∈ {8,16,32}`).

This is **one fatal point per dyadic scale** — a thin (exponentially shrinking relative measure) target, hit
by *reachability*, not by an accumulated density. The natural species kin is **o15's cylinder avoidance**
(string-ledger: "the 2-adic tail of `a+3` is never all-zeros"), not Antihydra's Cesàro density.

**Margins `[OBSERVED]`** (500k exact milestones): min `a = 2` (at start); 124,914 cascade entries; depth
statistic `v₂(a+3)` matches the geometric law `2^{−d}` to d = 16 (freq 0.4996, 0.2504, 0.1261, … vs 0.5,
0.25, 0.125); **max depth 22** vs the ≈100,650 bits fatality would need; **min `oddpart(a+3)` at entries = 7**
(fatality needs 1; the value 3 — the `a=3` branch — is also never hit on the blank orbit).

### 2.4 Reduction theorem
> **non-halt ⟺ the coupled orbit `(a_n, b_n)` from `(2,2)` never has `a_n + 3` a power of 2**
> — a Π⁰₁ **reachability/avoidance** statement over the exact coupled map. No density statement is equivalent
> to it: the event is not a Birkhoff average of the parity sequence.

Links: gate `[PROVEN from table]` → automaton `[OBSERVED 0-mismatch + seeded, incl. one corrected branch]` →
cascade law + fatal-set characterization `[PROVEN given the automaton]` → avoidance on the blank orbit
`[OBSERVED to 500k milestones]` → **the avoidance forever `[OPEN]`** — a generalized-Collatz reachability wall
(B2), *not* `(K)`.

**Verdict: o7 is MISCLASSIFIED in the 2D map.** `CRYPTID_2D_CLASSIFICATION`'s row "o2, o7 … B1 density
[verified] … b is a balance/refill counter returning to 0" is **wrong for o7** on both counts: b never
returns to 0 (b ≥ 1 invariant) and the wall is B2 reachability. (`O2_O7_HALT.md`'s own o7 line — "halts ⟺ a
reaches 1", a value-hitting — was already inconsistent with the row; `REDUCE_O2_O7_O8.md`'s "existence, not
density" facet call is confirmed and sharpened to the exact-power criterion.) In the species frame o7's
protection is a **string/cylinder shape** (2-adic tail of `a+3`), sitting with o15, away from Antihydra/o2.

---

## 3. o10 — the mirror, re-verified, with one banked row corrected

`o10 = 1RB1RA_0RC1RC_1LD0LF_0LE1LE_1RA0LB_---0LC` (halt `F,0`).

### 3.1 Gate `[PROVEN from table]` + census `[OBSERVED]`
Unique edge into F: `C,1→0LF` ⟹ **HALT ⟺ state C reads a 1 whose left neighbour is 0** (⟺ a C/F eat-sweep
consumes an odd-length 1-run). Census (20M steps): 5,507 triggers, **0 firings**, windows saturate at
**7/10/13 (r=3/4/5), last new step 2,660**. Largest window census of the three, still tiny and safe.

### 3.2 Structure — epoch model, raw-verified 16/16
**Clean config** = state E at left frontier, tape `0* 1 0^{2m−8} 1^b 0 1` → `(m, b)`; blank orbit
`(6,5)@52 → (9,4) → (14,2) → (21,1) → (6,57)@2621 → …`. Macro-step `[OBSERVED, 0 mismatches over 18 blank
transitions to 20M steps]`:
> `dec = 1 + [m odd]`; `b −= dec`; `m → ⌈3m/2⌉` — the **literal AEV ceiling map, seed 6, reset every epoch**;
> overshoot (`b<0`) ⟹ refill `B' = 3(m−2)`; landing (`b=0`) ⟹ HALT if new m odd, else refill `B' = 3m−7`.

**Seeded epoch cross-check `[OBSERVED]`: B = 1..16 all match the raw TM** (halts at B = 1, 4, 11, 13; refills
`21, 35, 57, 89, 137, 209, 317, 479, 723, 1089, 1637, 2459`).
> **Correction 3 (§4): the previously unverified row B=16** — `O10_HALTER.md` recorded "B=16:
> predicted-halt (>3M cap, timeout)". The raw TM (40M-step cap) **REFILLS at B=16 with B' = 2459**, matching
> this model. The banked prediction was wrong; every row of the epoch model is now raw-verified.

### 3.3 Protection — the inverted species
`[PROVEN given the epoch model]`: the m-orbit is epoch-independent, so with `C_t` = cumulative dec,
**epoch(B) halts ⟺ B ∈ S_halt := {C_t : m_{t+1} odd}** = `{1, 4, 11, 13, 17, 20, 22, 24, 29, 32, 34, 42, …}`.
`[OBSERVED]`: density(S_halt) = 0.329 / 0.334 / 0.332 at N = 10³/10⁴/10⁵ → **1/3**, because the m-orbit's
odd-density is 0.49744 ≈ ½ (the **(K)-TYPE statement — but about the *target*, not the protection**) and C
grows at rate 3/2. Reseed orbit (exact): `B₁ = 5, B₂ = 57, B₃ = 210,273,201`, doubly exponential; epochs 1–2
**refill** (raw/exact-verified); epoch 3 needs ~1.4·10⁸ ceiling steps on ~10^(2.5·10⁷)-digit integers
(~10¹⁵ digit-ops) — infeasible here, `[OPEN]`.

**Species axes:** LEDGER-MEMORY = **RESETTING** (m and b restart each epoch; no cumulative functional
survives a refill). Margin = **zero/inverted**: the generic verdict is HALT (each epoch hits a density-⅓
target); non-halt requires the specific doubly-exponential `B_e` to avoid a *positive-density* set forever —
**anti-equidistribution**, strictly stronger than the genericity `(K)` asks for (`O10_APEX_2026-07-04.md`,
confirmed).

### 3.4 Reduction theorem
> **non-halt ⟺ ∀e: B_e ∉ S_halt** — links: gate `[PROVEN from table]` → epoch model `[OBSERVED, 16/16 raw +
> 18 blank transitions]` → S_halt equivalence `[PROVEN given the model]` → target density 1/3 `[OBSERVED;
> proving it = a seed-6 ceiling-(K)-type statement]` → avoidance forever `[OPEN]`.

**Verdict:** o10 shares the family's gate shape and the ceiling-3/2 kernel (same operator as o2's, different
seed, resetting), but its **protection is the inverse of a (K)-instance**: the (K)-shaped quantity defines the
*halt target's density*; the open conjecture is avoidance of a thick set. "B1 density apex" survives only in
that refined sense.

---

## 4. Corrections to banked notes (all raw-TM-settled this session)

1. **`CRYPTID_SLOWWIDTH_2026-07-04.md` §1 / `O2_O7_HALT.md` (o2 value law).** "`x = a+4` satisfies
   `x ↦ ⌊3x/2⌋`" is false (`9 → 15 ≠ 13`); the exact law is `x ↦ 3⌈x/2⌉`, i.e. **`y = (a+4)/3 ↦ ⌈3y/2⌉`**
   (ceiling, not floor — o2 sits on the AEV side, not Antihydra's floor-mirror side).
2. **`CRYPTID_SLOWWIDTH_2026-07-04.md` §2 (o7 a=3 branch).** `(3,b) → (b+5, 2·[b odd])` is wrong for even b:
   seeded raw TM gives `(3,2) → (7,1)` and `(3,4) → (9,1)`, so the branch is `(b+5, 1+[b odd])` — in
   particular **b = 0 never occurs**, removing the last balance-like artifact from o7's automaton.
3. **`O10_HALTER.md` §1 (B=16 row).** "predicted-halt" is wrong: the raw TM refills at B=16 with `B' = 2459`
   (40M-step run), as the re-derived epoch model predicts. All 16 rows now raw-verified, 0 mismatches.
4. **`CRYPTID_2D_CLASSIFICATION_2026-07-05.md` (the o2/o7 row).** The joint call "o2, o7 = B1 density
   [verified]" splits: **o2 confirmed B1** (sharpened to the exact ledger + escape hatch); **o7 reclassified
   B2 reachability** (thin-set / 2-adic exact-power avoidance; no ledger exists). The 2D map's claim "B1 is
   confined to the ×3/2 balance machines" tightens further: genuine cumulative-density B1 = **Antihydra + o2**.

## 5. The family picture after this census

- **Ceiling vs floor:** the census's `(K)`-species now has *named seeds on both sides* of AEV 1.6(3/2):
  floor seed 8 (Antihydra) — ceiling seed 2 (o2) — ceiling seed 6, resetting (o10-inner). The ⌈3·/2⌉ map is
  injective (evens → 0 mod 3, odds → 2 mod 3), so the seed-2 and seed-6 ceiling orbits never merge: **three
  permanently distinct single-orbit instances of the same open equidistribution problem.**
- **Protection taxonomy within the "family":** cumulative density ledger (Antihydra, o2 — o2 with an extra
  mod-4 hatch), thin-set 2-adic reachability (o7 → sits with o15's cylinder species), anti-equidistribution
  against a thick Mahler-defined target (o10, unique). The multiplier alone was never the species.
- **Margins:** o2's ledger drifts +1/2 per step (b ≈ n/2, worst early prefix 0 — critical like Antihydra);
  o7's exposure is doubly protected (needs a geometric-tail event of depth ≈ bitlength, observed max 22 of
  ~10⁵ bits); o10 has no margin at all (generic side says HALT; two epochs decided, both refill, third
  infeasible).

## Reproduce
- `x32_gate_census.py` — gates from table + 20M-step window censuses (o2: 4 windows r=5, 0/4295 fires;
  o7: 4, 0/3601; o10: 13, 0/5507).
- `x32_o2_reduction.py` — automaton 0-mismatch (raw + 103 seeds), ceiling conjugacy, ledger identity, halt
  seeds `a ≡ 1 mod 4` (11/11), 100k-step margins.
- `x32_o7_reduction.py` — automaton 0-mismatch (raw + 124 seeds; a=3 branch corrected), cascade law, halt
  grid (0 mismatches), 500k-step margins with `v₂` histogram.
- `x32_o10_reduction.py` — clean-config model 0-mismatch (blank), seeded epochs B=1..16 (0 mismatches,
  B=16 settled), S_halt density, exact `B₃`.

**Halting stays `[OPEN]` for o2, o7, o10. No machine decided. No label upgraded.**
