# The fixed-point census closed: o16 (Mahler sea) + Space Needle (×5/2, the non-(K) machine) — 2026-07-08

*Completes the closed-form fixed-point treatment for the last two frontier targets, in the exact style of
`O11_REFILL_LAW_2026-07-08.md` and `ANTIHYDRA_LEDGER_UNIFICATION_2026-07-07.md`. **o16** gets the full o11
treatment (rule-exact sea, ×3/2 branch fixed points, `run = v₂(s−x)` closed forms, W-mirror, criticality
row, the tower-sparse-gate/ledger interaction). **Space Needle** — the frontier's one non-(K) machine
(μ=5/2 ∉ 2ᵃ/3ᵇ) — is the headline: the o4/O15 fixed-point trick is shown to **transfer to ×5/2** (5 is a
2-adic unit), `run = v₂(m)` exactly; its criticality is decided by **summability**, not a drift ratio,
placing it alone on the CUMULATIVE / non-halt-leaning side. SOUNDNESS: labels
`[PROVEN]`/`[OBSERVED]`/`[MODEL]`/`[OPEN]`; the fixed-point run laws are two-line proofs + exhaustive
checks; halting stays `[OPEN]` for both. Interpreter `/Users/aokiyousuke/quantum-ecc/.venv/bin/python`.
Scripts: `o16sn_o16fixedpoint.py`, `o16sn_sn_fixedpoint.py`, `o16sn_sn_protect.py`. Not committed.*

## 0. Headline

> **o16** collapses (like o11) to one ×3/2 sea map `T(s)=⌊3s/2⌋+2` whose two branches have integer fixed
> points **x_even = −4, x_odd = −3**, giving the exact run closed forms **even-run = v₂(s+4), odd-run =
> v₂(s+3)** (`[PROVEN]`, exhaustive s≤2×10⁵). o16's residue itinerary is therefore the same v₂-depth process
> as Antihydra/o11/o4 — but its halt gate is **TOWER-SPARSE** (15 F-visits in 12M steps): the ×3/2 residue
> ledger is *read only at the doubly-exponential refills*, so o16 is the rarest-exposed rung. **Space
> Needle**: the o4/O15/Antihydra fixed-point theorem **transfers verbatim to ×5/2** — the even (v=0) branch
> is exactly `f(m)=5m/2` with fixed point **0** (m-coord) `= −4` (b-coord, `b′=⌊5b/2⌋+6`), and because **5
> is a 2-adic unit** the clean ×5/2 run length **= v₂(m) = v₂(b+4)** exactly (`[PROVEN]`, exhaustive). The
> odd branch is a **v-indexed** family `f=(2ᵛ⁺¹+3)q+2ᵛ+v−1` with no single fixed point — the transient
> carry-resolution step between ×5/2 phases (the parity break at odd b, e.g. 621→1090). SN's criticality is
> **not a ρ/β drift ratio** (no draining scalar ledger — string-ledger, o15/o18 side) but **summability**:
> per-epoch fatal prob ~2^{−width}, width cumulative ⇒ Σ<∞ ⇒ **annealed non-halt-leaning** — the o4 side,
> opposite o18's RESET. Fatal set `[PROVEN by run]` `{2ᵏ−1} ∪ {6,102,311,351,371,…}` (sporadics extended
> this session; S ⊋ all-ones). **Both `[OPEN]`.**

---

## TASK A — o16: full fixed-point treatment

o16 = `1RB0LD_1RC1RA_1LD0RB_1LE1LA_1RF0RC_---1RE`, halt = F reads 0 (an E/F rightward-alternation
`00`-vs-`11` phase race, `REDUCE_O11_O16.md` §1 `[PROVEN]`). Milestone shape `[k | 1ˢ sea | defect d]`.

### A1. The sea rule, exact on grids `[PROVEN on defect-4 pairs]`
Clean sea law (defect = 4 milestones): **`T(s) = ⌊3s/2⌋ + 2`** — re-verified on the real orbit
(`o16sn_o16fixedpoint.py`, 12M steps): the clean chain `73 → 111 → 168` and 7/12 consecutive defect-4 pairs
satisfy `s′=T(s)` exactly (the other 5 cross a refill boundary — the classification's "5 clean, rest
boundary jumps"). Matches `REDUCE_O11_O16.md` (`73,111,168`) and `MAHLER_SEA_CLASSIFICATION` §2.

### A2. Branch fixed points and run closed forms `[PROVEN]`
Two affine branches, integer fixed points from `x = T(x)`:

| branch | map | fixed point | run closed form |
|---|---|---|---|
| s even | `s′ = 3s/2 + 2` | **x_e = −4** | maximal even-run = **v₂(s+4)** |
| s odd  | `s′ = (3s+3)/2` | **x_o = −3** | maximal odd-run  = **v₂(s+3)** |

*Proof:* distance to the branch fixed point multiplies by exactly 3/2 on a same-branch step
(`s′+4 = (3/2)(s+4)` even; `s′+3 = (3/2)(s+3)` odd), and branch membership is 2-divisibility of that
distance (`s even ⟺ 2|s+4`; `s odd ⟺ 2|s+3`). Since 3 is a 2-adic unit each same-branch step lowers v₂ of
the distance by exactly 1, so the run length is v₂ of the entry distance. ∎ **Exhaustive: 200000/200000**
(s=1..2×10⁵); on-orbit at the clean seeds {73,111,168} 3/3.

- **mod-4 dictionary** (what the phase race reads): `s≡0(4) ⟺ v₂(s+4)≥2`, `s≡2(4) ⟺ v₂(s+4)=1`,
  `s≡1(4) ⟺ v₂(s+3)≥2`, `s≡3(4) ⟺ v₂(s+3)=1` — **200000/200000 exact**.
- **W-mirror coords:** `W = s+4` makes even steps EXACTLY ×3/2 (`W′=(3/2)W`); `U = s+3` makes odd steps
  exactly ×3/2. Exact on s<5000. So **o16's residue itinerary is the v₂-depth process of a ×3/2 orbit** —
  the same object as Antihydra (v₂/×3/2), o11 ((2,3) at x=−8/−7), o4 (v₃/×4/3), o15 (v₃/×8/3). The mirror
  ladder's o16 rung sits at Antihydra's own (p,q)=(2,3), offset by (−4,−3) instead of o11's (−8,−7).
- **Run cap:** `run(s) ≤ log₂(s+4)`; on-orbit `s_i ~ C(3/2)ⁱ` ⇒ run ≤ `i·log₂(3/2)+O(1) ≈ 0.585 i`.

### A3. Criticality row + the tower-sparse-gate / ledger interaction
o16's criticality row: **run-cap slope `log₂(3/2)=0.585`** `[PROVEN depth process]`; **budget = leading
block k, RESETTING** (each refill re-seeds the sea), **drained at the constant rate −1 per sea step**
(`k→k−1`, catalogue "o11 with step −1"; contrast o11's −4), giving self-determined terminal index
**`e(k)=k`** (o11 has `e=⌊k/4⌋`). The drain does **not** couple to the residue itinerary, so the ρ/β ratio
criterion is **inapplicable in-epoch** (no halt branch mid-epoch); all fatality sits at the terminal phase
race — **one exposure per epoch**.

**Fatal probe + memory class `[OBSERVED]`.** o16's fatal set is `[PROVEN nonempty]` in the standalone
family (`msea_fatal.py`: `[k,0²,1ᵐ,d]` mutants, `[1,1,4]` halts @160, 162/250 dense), while the blank orbit
is safe at all 15 gate exposures — protection is seed-specific, and the **ledger-memory class is RESETTING**
(each doubly-exp refill re-seeds the sea; epoch residue is a fresh draw), o15/o18's side of the axis.

**The distinguishing costume — gate sparsity ⋈ ledger.** o16's halt gate is entered **only** during the
doubly-exponential refill reconfiguration: **15 F-state visits in 12M steps** `[OBSERVED]` (vs o11's
collapse, which fires every epoch). So o16's ×3/2 residue *ledger is READ only at the refill index* — a
strictly sparser exposure than any other sea machine. Combined with the **RESETTING** memory (each refill
wipes the sea to a fresh seed), o16's protection is: *the sea residue, sampled at the doubly-exp refill
ladder and re-seeded between reads, never lands at the F-phase-lethal residue*. Gate sparsity does not
change the residue process — it changes how often it is *sampled*: o16 is the residue-ledger machine with
the rarest ledger read in the frontier.

---

## TASK B — Space Needle (μ = 5/2, the non-(K) machine)

SN = `1RB1LA_1LC0RE_1LF1LD_0RB0LA_1RC1RE_---0LD`; halt gate `[PROVEN from table]`: **state C reads a 0
whose left neighbour is 0** (`SPACE_NEEDLE_HALT.md`).

### B1. Exact rule system `[PROVEN from table, re-verified vs raw TM]`
Single-block milestone `0^∞ 1ᵐ 0^∞`, head on the 0 right of the block, state C. One epoch is the
2-adic-digit-driven map
> **`f(m) = m + 3·⌊m / 2^{v+1}⌋ + v`,  `v` = number of trailing 1-bits of m.**

Re-verified against the raw TM by running one full epoch per seed: **58/58 exact** (m=2..59, halts
counted consistent). Two-block reset counter **`b = m − 4`** (the `[1,0,1ᵇ]` milestone); mid-epoch 3-block
milestones **`[1, b, b/2+2]`** appear on even b (verified: (12,8),(36,20),(96,50),(246,125) exact; the
first *odd* b breaks the shape — the 5th observed 3-block is `[1,308,470]`, `470 ≠ 156`).

### B2. Fixed-point closed forms for ×5/2 — the trick TRANSFERS `[PROVEN]`

| branch | map | fixed point | run closed form |
|---|---|---|---|
| **v=0 (m even)** | `f(m) = m+3(m/2) = 5m/2` | **x = 0** (m) `= −4` (b) | **clean ×5/2 run = v₂(m) = v₂(b+4)** |
| v≥1 (m odd) | `f = (2^{v+1}+3)q + 2ᵛ+v−1`, `q=⌊m/2^{v+1}⌋` | **none** (v-indexed multiplier) | transient carry step |

- **The even branch is exactly ×5/2** (`f(m)=5m/2` on all evens 2..2×10⁵, exact). Solving `x=5x/2+c` gives
  `x=−2c/3`; in b-coordinates `b′=⌊5b/2⌋+6` (c=6) ⇒ **x=−4**, and `b′ = f(b+4)−4` exactly (evens, exact).
  The m-coordinate fixed point is 0.
- **The fixed-point trick works for ×5/2** because the numerator **5 is a 2-adic unit** (just like the 3
  in ×3/2): distance to the fixed point multiplies by 5/2, so v₂ of the distance drops by exactly 1 per
  even step, and **the maximal even-run (= clean ×5/2 phase length) = v₂(m) = v₂(b+4)** exactly. **Verified
  exhaustively on all evens 2..2×10⁵** and on-orbit (`b=12→36→96→246`: v₂(16)=4, exactly 4 clean resets
  before the odd break at 621=⌊5·246/2⌋+6). So `runs = v₂(value − x)` is a genuine ×5/2 closed form — the
  first non-(K) member of the mirror ladder.
- **The odd branch has no single fixed point.** For odd m with v trailing ones, `f = (2^{v+1}+3)q + 2ᵛ+v−1`
  — multiplier `1 + 3/2^{v+1}` is **v-dependent** (exact on all odds 2..2×10⁵). It is the transient
  carry-resolution step *between* ×5/2 phases; the clean scalar chain is exactly the maximal even-run and
  **breaks at the first odd value** — the observed parity-branching (621→1090, not ⌊5·621/2⌋+6=1558).

### B3. Criticality — summability, not a drift ratio; SN's ladder position
**Run-cap slope ρ = log₂(5/2) = 1.3219** (the ×5/2 depth expansion). But SN has **no draining scalar
ledger**: the value m is **CUMULATIVE** (grows; per-gen log-growth ≈ 0.933 `[OBSERVED]`) and halt is a
base-2 **cylinder avoidance** (string-ledger). So the family ρ/β criterion is **inapplicable** — exactly as
for o15/o18 ("string-valued, no scalar slope"). What replaces it is **SUMMABILITY**: the per-epoch fatal
probability is ~`2^{−width}` with `width_n ~ (growth)·n` growing, so **Σ 2^{−width_n} < ∞** (measured ≈0.50
over 400 epochs, converging) ⇒ **annealed E[# fatal hits] finite ⇒ non-halt-leaning** (Borel–Cantelli I).

> **Ladder position `[MODEL]`.** SN is the frontier's one **CUMULATIVE, non-(K) string-ledger**. On the
> annealed memory axis it lands on the **o4 side** (Σ finite ⇒ non-halt-lean), the *opposite* side from the
> five RESETTING sea machines (o11,o12,o13,o14,o16 — constant per-refill prob ⇒ Σ=∞ ⇒ annealed
> halt-leaning) and from o18 (RESET word). Its non-halt lean is the **strongest in the six** — but this is
> the memory axis, not a decision. SN is thus **the annealed-easiest** target, yet **not decidable by
> growth alone**: the actual content — does the specific ×5/2 orbit ever enter the all-ones ∪ sporadic
> cylinder — is generalized-Collatz reachability (the Collatz wall), and 5/2 ∉ 2ᵃ/3ᵇ means it does not even
> reduce to the (K) residue-equidistribution program. **Genuinely different, not genuinely easier.**

### B4. Protection statement + fatal cylinder (base-2 digit condition)
**Halt set `[PROVEN by run]`** (raw-TM epoch census, `o16sn_sn_protect.py`):
> `S ∩ [1,599] = {1,3,6,7,15,31,63,102,127,255,311,351,371,511}` `= {2ᵏ−1 : k≥1} ∪ {6,102,311,351,371,…}`.

Every all-ones `2ᵏ−1 ≤ 599` is fatal; the sporadic 00-defect alignments **{6,102,311,351,371}** extend the
documented `{6,102}` (new this session) and confirm **S ⊋ {all-ones}** (the sporadic rule stays `[OPEN]`).

> **PROTECTION STATEMENT `[OPEN]`.** SN does not halt ⟺ the milestone orbit `m₀=2, m_{n+1}=f(m_n)` never
> enters S. **Is the fatal cylinder a base-2 digit condition on the ×5/2 orbit? — YES for the dominant
> part:** `m = 2ᵏ−1 ⟺ every bit of m is 1` (a full-width 1-cylinder in base 2), plus a measure-thin
> sporadic 00-defect correction. **Fatal set** = all-ones cylinder ∪ sporadics. **Margin** = #zero-bits(m):
> halt needs **0** zero-bits; the blank orbit stays at **≥ 1** zero-bit at every tested generation, and
> because m grows ~×5/2 the all-ones target is `2^{−width}`-thin and recedes geometrically — the summable,
> non-halt-leaning picture of B3. Blank-orbit ∩ S = ∅ on the tested range; **blank-tape reachability is NOT
> claimed** — it is exactly the open protection.

---

## Soundness ledger

- **o16**: sea law `[PROVEN on defect-4 pairs]`; the branch fixed points and `run=v₂(s+4)/v₂(s+3)` closed
  forms `[PROVEN]` (two-line proof + 200000/200000 exhaustive + on-orbit); gate-sparsity 15/12M
  `[OBSERVED]`; criticality row is a re-coordinatization, no non-halting claim.
- **Space Needle**: f-map `[PROVEN from table]` (re-verified 58/58 vs raw TM); ×5/2 even-branch fixed point
  and `run=v₂(m)=v₂(b+4)` `[PROVEN]` (exhaustive evens + b-coord identity + odd-branch v-indexed form);
  fatal set `[PROVEN nonempty by run]` (sporadics {6,102,311,351,371} new); criticality/annealed lean
  `[MODEL]`; protection `[OPEN]`.
- No margin, no simulation, and no annealed lean is ever a machine claim. Both machines `[OPEN]`.

**No machine decided. No label upgraded.**

## Reproduce
`o16sn_o16fixedpoint.py [MMAX N]` (o16 fixed points, mod-4 dict, W-mirror; real-orbit sea law + gate
sparsity) · `o16sn_sn_fixedpoint.py [MMAX]` (SN rule system vs raw TM; ×5/2 fixed point + run law +
b-coord + odd branch; growth/summability) · `o16sn_sn_protect.py [HI]` (SN fatal-set census, base-2 view,
orbit margin). Basis: `O11_REFILL_LAW_2026-07-08.md`, `MAHLER_SEA_CLASSIFICATION_2026-07-07.md`,
`ANTIHYDRA_LEDGER_UNIFICATION_2026-07-07.md`, `SPACE_NEEDLE_HALT.md`, `SPACE_NEEDLE_5_2.md`,
`REDUCE_O11_O16.md`, `msea_*.py`.

**No machine decided. No label upgraded.**
