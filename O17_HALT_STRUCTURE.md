# o17 halt-time structure: exact-linear off the 3-sublattice, Collatz-hard on it (2026-07-01)

*New structural finding on o17 — the one BB(6) Collatz-core cryptid that is NOT in the Mahler/occupancy family (it is a
base-3 carrying odometer whose hardness is its halt predicate, `o17_attack.md`, `CRYPTID_KERNEL.md`). Simulating the
embedded left-frontier family `0 A 0 1^k` on the raw TM (`scratchpad/o17.py`, cap `3·10⁶`) sharpens the obstruction to
the `k≡0 (mod 3)` sublattice and gives the complement an EXACT linear halt-time formula. SOUNDNESS: halt times are
`[OBSERVED]` exact TM simulation; the linear formulas are `[OBSERVED, k≤48]` (an elementary proof looks accessible but is
not written); `k≡0` classification is `[OBSERVED, cap-limited]` — some "no-halt<cap" entries are slow halters (see the
k=21 caveat). No non-halt claimed. NOT committed by default.*

---

## 1. Off the 3-sublattice: exact-linear halt time `[OBSERVED, k≤48]`

For `k≢0 (mod 3)` the family `0A01^k` **always halts, in time linear in `k`**, split into four arithmetic progressions
by `k \bmod 6`:

| `k \bmod 6` | halt time `H(k)` | first values |
|---|---|---|
| 1 | `7 + 16(k-1)/6` | `k=1,7,13,19,\dots \to 7,23,39,55,\dots` (step 16) |
| 4 | `35 + 32(k-4)/6` | `k=4,10,16,22,\dots \to 35,67,99,131,\dots` (step 32) |
| 2 | `33 + 32(k-2)/6` | `k=2,8,14,20,\dots \to 33,65,97,129,\dots` (step 32) |
| 5 | `21 + 16(k-5)/6` | `k=5,11,17,23,\dots \to 21,37,53,69,\dots` (step 16) |

All verified `k\le48`, zero exceptions. So on `\{k: 3\nmid k\}` (two-thirds of the seeds) o17's left-frontier family is
**exactly decided with a closed-form halt time** — a bouncer-like linear régime.

## 2. On the 3-sublattice: the Collatz-hard core `[OBSERVED, cap-limited]`

For `k≡0 (mod 3)` (write `j=k/3`) the behaviour is Collatz-irregular:
- **Halters (within `3·10⁶`):** `k=6,12,15,24,30,36,45` (i.e. `j=2,4,5,8,10,12,15`), halt times
  `206, 394, 794964, 3690, 7262, 13810, 45688` — **wildly non-monotone** in `k` (e.g. `k=15\to795\text{k}` but
  `k=45\to46\text{k}`).
- **No halt `<3·10⁶`:** `k=3,9,18,21,27,33,39,42,48` (`j=1,3,6,7,9,11,13,14,16`).
- **CAVEAT (Collatz signature):** `k=21` is listed no-halt here only because it halts at `\approx4.24\cdot10^{6}`, beyond
  this run's `3\cdot10^{6}` cap (`o17_attack.md`). So the "no-halt<cap" set **mixes true non-halters with slow halters**,
  and the halt/no-halt split on `3\mid k` is not decidable by any fixed cap — the concrete Collatz-undecidability
  signature. (The proven halters `k=6,12,15` remain proven.)

## 3. Reading

o17's hardness is **precisely localized to the `k≡0 (mod 3)` sublattice**. This matches the odometer picture: a settled
base-3 digit is a block of length `ℓ≡2 (mod 3)` (digit `d=(ℓ-2)/3`); an initial block `k≡0 (mod 3)` is *off* the
settled-digit lattice, so it triggers the deep leftward carry cascade whose overflow-past-MSB is the halt
(`o17_attack.md` §CORRECTION). The `k≢0` seeds settle immediately into the linear régime; only `k≡0` enters the
Collatz-irregular carry dynamics. This **sharpens `o17_attack.md`'s "Collatz-hard"** from "the family is irregular" to
"the family is *exactly linear off `3ℤ` and Collatz-hard on `3ℤ`*," concentrating the open kernel on the `j=k/3`
dynamics. Extracting the explicit Collatz-type map on `j` (the analogue of the Antihydra `(K)` reduction) is the natural
next step and remains open.

**Honest scope.** This decides nothing new unconditionally (the `k≢0` linear régime is a bounded-time halt, not a
non-halting result; the `k≡0` core is Collatz-hard and undecidable-by-cap). It is a structural sharpening: o17's
obstruction lives entirely on `3ℤ`, and the complement is exactly linear. o17 remains a genuinely *different* obstruction
type from the Mahler/occupancy family — a halt-predicate (odometer-overflow) hardness, not an equidistribution kernel.
**No machine decided. No label upgraded.** o17 non-halting stays `[OPEN]` (a Collatz-type statement).

## 4. Addendum — o17 does NOT reduce to a 1-D Collatz map; its kernel is a base-3 string dynamics (2026-07-01)

Attempting the analogue of the Antihydra `→(K)` reduction (extract an explicit scalar map `j→j'` on `j=k/3`), we
instrumented the raw TM to record the tape at each recurring canonical config (state `A` at the left frontier) for
`k≡0 (mod 3)` seeds (`scratchpad/o17_map.py`). Result: the milestone states are **growing multi-digit base-3 strings**,
not a scalar iterate. E.g. for `k=15` (a halter) the left-frontier-`A` block-length patterns are
`(3,2,2,2,2,2) → (3,8,2,2,20) → (3,14,2,2,14,44) → (5,2,2,\dots,14,236)`; the settled blocks (`ℓ≡2\bmod3`) decode to
base-3 digits `d=(ℓ-2)/3` (`2,8,14,20,50,170,236 → 0,2,4,6,16,56,78`), i.e. the tape encodes a **growing multi-digit
base-3 number** with nontrivial carry dynamics between milestones.

**Honest verdict `[OBSERVED]`.** Unlike Antihydra (whose kernel is the *scalar* 1-D map `c\mapsto⌊3c/2⌋`), o17's kernel
is a genuine **multi-digit odometer / base-3 string dynamics** — it does **not** collapse to a single-integer Collatz
iterate at these milestones. This is precisely *why* o17 is a **different, structurally harder-to-place obstruction
type**: there is no 1-D Mahler-style reduction to exhibit. Placing o17's kernel would require analyzing the full
string/carry dynamics (higher-dimensional), which this pass does not achieve. The finding is the honest negative that
**the 1-D reduction does not exist for o17**, sharpening its classification (odometer-string, not scalar-Collatz).
**No machine decided. No label upgraded.** o17 non-halting stays `[OPEN]`.

## 5. Addendum 2 — the carry cascade + extended hard-core data (2026-07-01)

**(5a) The `k≡0` cascade is an explicit multi-digit base-3 carry `[OBSERVED]`** (`scratchpad/o17_value.py`). Off-lattice
seeds `k≡0 (mod3)` trigger a leftward carry: the left block length decreases by `3` per step while spawning a
length-`2` (digit-`0`) block rightward, e.g. `k=12`: `(11)→(11,2)→(8,2,2)→(5,2,2,2)→(2,2,2,2,2)`; `k=9`:
`(8)→(8,2)→(5,2,2)→(2,2,2,2)`. This is a genuine base-3 carry cascade — but the decoded value sequence does **not**
form a clean scalar odometer (it jumps `0,3,-3,3,-1,1,…` under any tried decoding), confirming §4: the state is an
irreducibly multi-digit base-3 string.

**(5b) Extended hard-core map `[OBSERVED, cap 6·10⁶]`** (`scratchpad/o17_core.py`). For `j=k/3`, `j≤22`:
- **HALT** `j = 2,4,5,7,8,10,12,15,17,19,21` (times `206,394,794964,4240985,3690,7262,13810,45688,52932,117160,232604`
  — wildly non-monotone: `j=5→795\text{k}`, `j=7→4.24\text{M}`, `j=8→3690`).
- **no-halt `<6·10⁶`** `j = 1,3,6,9,11,13,14,16,18,20,22`.
- Weak tendency for `j≥15` (odd `j=15,17,19,21` halt; even `j=14,16,18,20,22` don't; `j=13` an exception), but for
  small `j` the split is fully mixed, and base-3 / mod patterns give **no clean rule** — the Collatz-irregularity is
  confirmed with more data, not resolved.

**(5c) Other cryptids `[status]`.** The kernel-unresolved "slow-width" cryptids (o2,o3,o4,o7,o11–o14,o16, Space
Needle, Lucy's Moonlight) have catalogue notes (`CATALOGUE_IRREGULAR.md`, `CATALOGUE_O2_O5.md`, `CATALOGUE_O7_O12.md`,
`CATALOGUE_O13_SN.md`, `CRYPTID_CENSUS.md`; TMs in `cryptid_map.py`) but their kernels remain **un-extracted**
(`CRYPTID_KERNEL.md` census) — extraction is a substantial per-machine reverse-engineering, not done here.

**Net.** o17's `k≡0` core is a genuine multi-digit base-3 carry cascade, Collatz-irregular with no clean rule
(confirmed to `j=22`), and irreducible to a scalar map. It stays `[OPEN]`, structurally the hardest-to-place BB(6)
Collatz-core cryptid. **No machine decided. No label upgraded.**

## 6. Addendum 3 — o17 is NOT even a clean base-3 odometer: interior "digits" are unbounded (2026-07-01)

Tracing the canonical (state-`A`-at-left-frontier) config sequence to derive an exact transition rule
(`scratchpad/o17_cascade.py`), a sharper obstruction surfaces:
```
k=6 : (3,2,2) → (5,2,8) → (8,14) → HALT@206
k=9 : (3,2,2,2) → (3,8,14) → (3,14,8,20) → (5,2,2,2,2,14,8,2,2,26) → ...
k=12: (3,2,2,2,2) → (5,8,14) → (8,2,2,20) → HALT@394
```
The interior **settled** blocks (`ℓ≡2 \bmod 3`, so "digit" `d=(ℓ-2)/3`) include `ℓ=14` (`d=4`) and `ℓ=20` (`d=6`)
— i.e. `d>2`. So:

> **o17 is NOT a clean base-3 odometer `[OBSERVED]`.** The `o17_attack.md` reading "settled block `↔` base-3 digit
> `d=(ℓ-2)/3`" is an *approximation*: the interior digits are **unbounded** (`d=4,6,\dots` observed as genuine
> interior settled blocks), so the state is not a base-3 (or any fixed-base) number. o17 is a general **carrying
> counter with unbounded digits**; halting is a left-frontier overflow (`F` reads a double-blank), but the path to it
> runs through unbounded-digit carries with **no clean base, no scalar, and not even a fixed-radix reduction**.

**Task A note (Lucy's Moonlight, blocked).** Attempting to extract a kernel for the width-ratio-`3/2` candidate
"Lucy's Moonlight" is blocked: its TM is **not in the repo** (`cryptid_map.py` holds only Antihydra and a distinct
halting "Lucy"; the 19-cryptid slow-width roster's TMs are not stored locally — `CRYPTID_CENSUS.md`), and obtaining it
requires an external (bbchallenge) lookup, out of scope here.

**Net (deepened).** o17's obstruction is now pinned as sharply as this pass allows: not merely "multi-digit," but a
**carrying counter with unbounded digits**, off any fixed radix — the structural reason no odometer/base/scalar kernel
extraction succeeds. This is the honest end of the o17 line for now: `[OPEN]`, the hardest-to-place BB(6) cryptid.
**No machine decided. No label upgraded.**
