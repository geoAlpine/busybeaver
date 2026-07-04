# (K) as a base-3/2 digit frequency (verified), and the exceptional-set foothold RETRACTED (2026-07-05)

*Two follow-ups to `FRONTIER_LIT_2026-07-05.md`: (1) verify the exact dictionary between Antihydra and the base-3/2
number system; (2) numerically test the "`p<q²` softens the exceptional set for 3/2" foothold. **(2) verifies `(K)` is
literally a base-3/2 digit frequency — a Normality-Conjecture sibling.** **(1) RETRACTS the foothold** by a red-team
numerical check: `p<q²` only thins the (already-thin) confinement set; the equidistribution-exceptional set that
certifying seed 8 actually needs is full-dimension regardless. SOUNDNESS: `[OBSERVED]`/`[PROVEN]` labelled; a foothold
withdrawn; `(K)` `[OPEN]`; no machine decided.*

## Task 2 — `(K)` IS a base-3/2 digit frequency `[OBSERVED, exact, N=4·10⁴]`
AFS base-`3/2` digit of an integer `c` is `a₀(c) = 2c mod 3` (successor `c↦⌊2c/3⌋`). Reading `a₀` **along the Antihydra
orbit** `c_{n+1}=⌊3c_n/2⌋`, `c₀=8`:
- **Digit frequencies: `0 → 0.4991`, `1 → ≈0`, `2 → 0.5009`.** Digit `1` occurs **exactly once** (see correction).
- **Reason `[PROVEN]`:** `c_{n+1}=⌊3c_n/2⌋ ≡ 0 (mod 3)` if `c_n` even, `≡ 1 (mod 3)` if `c_n` odd — so for **all `n≥1`**
  the orbit is `≡{0,1} mod 3`, and `a₀=2c mod 3 ∈ {0,2}` (digit `1 ⟺ c≡2 mod 3`). Alphabet `{0,2}` from `n=1`.
- **`a₀=0 ⟺ c≡0 mod 3 ⟺` previous step even; `a₀=2 ⟺` previous step odd.** So **digit-`0` frequency `=` the `(K)`
  even-density asymptotically** (same orbit, one-step shift; `O(1/N)` boundary).

> **CORRECTIONS (2026-07-05, re-verification `BB6_PROOF_ATTEMPT_CAPSTONE_2026-07-05.md`):** (i) digit `1` is **not
> literally absent** — the **seed `c₀=8 ≡ 2 mod 3`** gives the unique digit `1` at `n=0` (earlier "`0.0000`" was a
> `%.4f` rounding of the single `1/N`); the `{0,2}` alphabet holds for `n≥1`. (ii) digit-`0`-freq `=` even-density is
> **asymptotic, not exact** — `digit_n=0 ⟺ c_{n−1}` even, a one-step shift, agreeing up to `O(1/N)`. The mathematical
> content (`(K)` = base-3/2 digit-`0` frequency, effective alphabet `{0,2}`) is unchanged.
> **`(K)` = "the base-3/2 last-digit sequence of the Antihydra orbit (alphabet `{0,2}`) has digit-`0` frequency
> `≥ 1/3`" — literally a base-3/2 digit-frequency / normality-type statement.** Confirms `(K)` is in the
> Normality-Conjecture family (`arXiv:2510.11723`) concretely. **Caveat:** the orbit-digit alphabet `{0,2}` is
> *neither* the minimal word `{0,1}` *nor* the maximal word `{1,2}` of Conjecture 1.3 — so `(K)` is a **sibling**
> (a distinct distinguished sequence in the same base-3/2 digit-frequency family), **not literally** Conj 1.3's word.

*(Aside: the recursive orbit parity agrees only `~0.50` with the non-recursive `⌊8(3/2)ⁿ⌋` half-itinerary — floor
errors fully decorrelate the two sequences pointwise, though both carry even-density `≈0.499`. `(K)` is about the
recursive orbit.)*

## Task 1 — the `p<q²` foothold RETRACTED `[OBSERVED + PROVEN reasoning; a red-team self-correction]`
Box-dimension of the confinement set `E_α = {ξ : frac((3/2)ⁿξ) ∈ [0,α) ∀ 1≤n≤N}` by exact interval tracking, `N≤26`:

| `α` | last `K` (intervals) | measure | box-dim (tail) | reading |
|---|---|---|---|---|
| **0.5** (Z-number type) | 1 (collapsed) | `1.3e−5` | `≈0.585` then collapse | **thin** — matches Flatto `dim ≤ log₂(3/2)=0.585` |
| 0.6 | 2 | `2.5e−5` | ~0.1 (collapsed) | thin |
| 0.75 | 387 | `3.2e−3` | **0.576** | intermediate |
| 0.9 | 13504 | `1.3e−1` | **0.909** | large |
| →1 | — | — | **→ 1** | full-dimension |

**The dimension rises monotonically to `1` as the constraint weakens (`α→1`).** Now the correction: `p<q²` excludes
Akiyama's Cantor-set *confinement* construction — but the confinement set was **already** thin (Flatto: `dim≤0.585`,
confirmed above by the `α=0.5` collapse). **The set that actually blocks certifying seed 8 is the
*equidistribution-exceptional* set** (`ξ` where `{ξ(3/2)ⁿ}` fails to equidistribute), which is **weaker than any fixed-`α`
confinement** (it contains `E_α` for every `α<1`, plus every persistently-biased `ξ`), so its dimension is
**`≥ sup_α dim(E_α) = 1` — FULL-dimension.** `[PROVEN reasoning + OBSERVED trend]`
> **The `p<q²` observation targets the wrong (already-thin) set. The equidistribution-exceptional set is full-dimension
> for 3/2 too, so the Fan–Fan–Ye a.e. wall is NOT softened. Foothold WITHDRAWN.** (`FRONTIER_LIT §5` is retracted.)

## Verdict
**One connection verified, one foothold honestly killed.** `(K)` is literally a base-3/2 digit-`0` frequency of the
Antihydra orbit (alphabet `{0,2}`, digit `1` arithmetically forbidden), even-density `=` digit-`0`-freq exactly — a
concrete Normality-Conjecture **sibling** (not its minimal/maximal word). The hoped `p<q²` softening is **retracted**:
it thins only the already-thin confinement set, while the relevant equidistribution-exceptional set stays
full-dimension, so a.e.-to-seed-8 remains as blocked for 3/2 as in general. **`(K)` `[OPEN]`. No machine decided. No
label upgraded.**

## Reproduce
- `scratchpad/dict_check.py`, `scratchpad/exc_dim.py` (`/opt/homebrew/bin/python3.13`, exact int / interval): orbit
  digit `2c mod 3 ∈{0,2}`, digit-`0`-freq `=` even-density; confinement box-dim `α=0.5→0.585`, `α→1→1`. Basis:
  `FRONTIER_LIT_2026-07-05.md` (§5 retracted), CITATIONS #8 (Fan–Fan–Ye a.e. full-dim), #11 (Normality Conjecture),
  Flatto 1992 (`dim ≤ log₂(3/2)`).
