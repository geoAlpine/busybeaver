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
