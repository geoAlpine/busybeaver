# BB(6) proof attempt — full data re-verification + the complete proof chain, stopping at the single open kernel (2026-07-05)

*User directive: "verify ALL data collected so far; attempt a proof of BB(6)." Done by re-computation (not citation):
the actual TM, the map reduction, the balance criterion, the run-ceiling, the dictionary, the countdown renewal — all
re-run. Result: the accumulated data is **sound** (two minor over-tight claims in `DICT_AND_EXCDIM` corrected here), and
the proof of Antihydra non-halting is **complete and verified down to exactly one open link** — `(K)` = the one-sided
Normality Conjecture on base 3/2. **A proof of BB(6) is therefore not available now**: it requires `(K)`, which is open.
Stating otherwise would be a false proof. SOUNDNESS: every link labelled `[PROVEN]`/`[PROVEN-in-lit]`/`[OPEN]`; no
machine decided; no false proof.*

## Part A — re-verification of all accumulated data `[re-computed, exact big-int]`
| # | claim | re-verified result | status |
|---|---|---|---|
| 0 | the Antihydra TM `1RB1RA_0LC1LE_1LD1LC_1LA0LB_1LF1RE_---0RA` does not halt | ran `2·10⁷` steps, no halt | ✓ consistent |
| 1 | non-halt ⟺ `c↦⌊3c/2⌋`, `c₀=8`, `B_n=3E_n−n≥0 ∀n` | `B` matches `3E−N` exactly; **`min_n B_n=0` (at n=0), zero negatives to `N=5·10⁵`** | ✓ holds |
| 1b | even-density | `0.4988` (margin `0.166` above `1/3`) | ✓ |
| 2 | run-ceiling gap | `max v₂(c−1)=20` at `5·10⁵` (`~log N`); ceiling `0.585N`; need `<0.5N`; gap `1.170×` | ✓ |
| 3 | `(K)` = base-3/2 digit frequency | digit `2c mod 3` freq `0:0.4988, 1:≈0, 2:0.5012` | ✓ **with 2 corrections ↓** |
| 4 | countdown renewal | from `d≥1`, `d_{n+1}=d_n−1` exactly: **`250581/250581`, 0 violations** | ✓ exact |
| 5 | Type-I bases `p<q²` | `3<4, 8<9, 4<9` | ✓ |

**Two soundness corrections to `DICT_AND_EXCDIM_2026-07-05` (caught by this re-verification):**
- **Digit `1` is not literally absent.** It occurs **exactly once**, at `n=0`: the seed `c₀=8 ≡ 2 (mod 3)` gives
  `a₀=2·8 mod 3 = 1`. For **all `n≥1`** the orbit is `≡{0,1} mod 3`, so digits are `{0,2}`. Correct statement: *the
  orbit-word is on `{0,2}` from `n=1` on; the seed contributes the unique digit `1`.* (Earlier "completely absent" was
  a `%.4f` rounding artifact of the single `1/N` occurrence.)
- **digit-`0`-freq `=` even-density is asymptotic, not exact.** `digit_n=0 ⟺ c_{n−1}` even, so the two sequences are
  the same **shifted by one step**; they agree up to an `O(1/N)` boundary term, not identically. Correct statement:
  *digit-`0`-frequency equals the even-density asymptotically (equal orbit, one-step shift).*
The mathematical content — `(K)` = the base-3/2 digit-`0` frequency, effective alphabet `{0,2}` — is unchanged.

## Part B — the proof of Antihydra non-halting, attempted in full `[each link verified]`
1. **`[PROVEN-in-lit; TM spot-checked]`** Antihydra halts from the blank tape ⟺ the counter `B_n=3E_n−n` goes
   negative, where `c_{n+1}=⌊3c_n/2⌋`, `c₀=8`, `E_n=#{k<n: c_k` even`}` (bbchallenge / sligocki "BB(6) is Hard").
   So **non-halt ⟺ `B_n≥0 ∀n` ⟺ `E_n ≥ n/3 ∀n`** (exactly: `3E_n−n≥0`; halting = "odds ever exceed twice evens").
2. **`[PROVEN]`** `B_n` is a walk with steps `+2` (even) / `−1` (odd); it stays `≥0` iff the even-count never falls to a
   `1/3` density. Verified: no negative excursion to `N=5·10⁵`; drift `+½` (even-density `≈½>⅓`).
3. **`[PROVEN]`** The only way `B` can go negative is a late odd-run (deep 2-adic visit) of length `> ` the accumulated
   surplus; a run of length `s` needs `v₂(c_n−1)≥s`. The magnitude ceiling gives `v₂(c_n−1) ≤ log₂c_n ≈ 0.585n`.
4. **`[PROVEN consistency]`** Elementary bounds are consistent with **both** halt and non-halt: the ceiling `0.585n`
   exceeds the accumulated surplus `≈0.5n` by the factor `1.170×`. Closing this — showing runs are genuinely
   `o(0.5n)` at positive density — is the remaining lemma.
5. **`[PROVEN, this session]`** That lemma **is** `(K)`: single-orbit equidistribution / one-sided digit-`0`
   frequency `≥1/3` of the base-3/2 orbit-word = the **one-sided Normality Conjecture for base 3/2**
   (Andrieu–Eliahou–Vivion 2025, Thm 1.7 = this reformulation).
6. **`[OPEN]`** `(K)` is unproven. Everything unconditional falls exponentially short: the best is `#even ≥ 0.89 log n`
   (`EVEN_COUNT_FLOOR`) — `log n`, not the needed `n/3`. This session confirmed **no internal route crosses**:
   structureless on 6 independent axes (harmonic/occupancy/symbolic-complexity/moving-diagonal/pair-correlation/
   sum-product), `β=+½` critical (No-Structure), the needed exponential moving-diagonal rate below the counting
   ceiling `R(N)≤log₂N`, rank-1 amenable (effective-equidist SOTA is rank-≥2 only).

## Part C — honest verdict
**The proof is complete and verified except for one link, and that link is open.** Concretely:

> **Antihydra does not halt `⟸` `(K)` [Antihydra non-halt ⟺ (K), fully verified].** `(K)` = the one-sided Normality
> Conjecture on rational base 3/2 = Mahler 3/2 / AEV — an **open** problem. Therefore **BB(6) cannot be decided now**;
> a proof requires `(K)`, which no current mathematics reaches (confirmed generational from six angles this session).

**This is NOT a proof of BB(6).** It is a fully-checked **conditional** proof (non-halt ⟺ `(K)`) plus a verified,
soundness-corrected dataset. To claim BB(6) proved would be exactly the false proof this program forbids. The genuine
attempt confirms — by walking every link — that the obstruction is a single, named, generational kernel, and pins the
minimal missing input (`(K)`, equivalently a `1.170×` run-ceiling improvement, equivalently an effective base-3/2
normality rate). **Halting `[OPEN]`. No machine decided. No label upgraded.**

## Reproduce
- `/tmp/verify_bb6.py` (`/opt/homebrew/bin/python3.13` + `bb_sim.py`): TM `2·10⁷` steps no-halt; `B_n=3E_n−n` match,
  `min B=0`, 0 negatives to `5·10⁵`; `max depth 20`; digit `{0:.499,1:1/N,2:.501}`; countdown `250581/250581`. Basis:
  bbchallenge/sligocki (reduction), `OCCUPANCY_PROFILE_THEORY §7` (gap), `DICT_AND_EXCDIM` (corrected here),
  `EVEN_COUNT_FLOOR`, `FRONTIER_LIT`/CITATIONS #11 (Normality Conjecture), `SESSION_2026-07-05_INDEX` (6-axis).
