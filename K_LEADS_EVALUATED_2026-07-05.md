# (K) research — the two fresh 2026 leads evaluated, and the resource method attempted: the barrier is aperiodic carry

*Doing "both": (A) evaluate the two 2026 positive-density leads against the single-orbit-vs-a.e. and linear-vs-log
tests; (B) attempt the mixed binary–ternary resource-allocation lower bound on our orbit directly. Both converge to a
sharp conclusion: the newest method (`arXiv:2606.24972`) proves **exactly `(K)`'s shape** (linear, single-orbit,
positive digit density) **but only under rationality (periodic carry)** — and our `×3/2` orbit is precisely the
**aperiodic-carry** instance it cannot reach. This sharpens the missing input from "P1′ generational" to a concrete,
named bridge. SOUNDNESS: `[PROVEN-in-lit]`/`[OBSERVED]`/`[eval]`; `(K)` `[OPEN]`; no machine decided; no false proof.*

## A. The two leads, evaluated `[PROVEN-in-lit content, verdicts]`
- **arXiv:2606.23661 (Erdős Problem 400) — DEAD END for `(K)`.** Its "density-one lower bound" is
  `g_k(n) ≥ (3(k−1)/log12 − ε)\log n` for **all but `o(x)` integers `n`** — i.e. **(b) almost-all `n`, and only
  `log n`** (logarithmic), on a factorial-divisibility excess `g_k(n)` (not even a digit frequency). So it is **still
  `log`, still a.e.** — it does **not** breach the count→frequency barrier. (The search snippet "density-one lower
  bound" misled; "density-one" = density-one *set of `n`*, and the bound is logarithmic.)
- **arXiv:2606.24972 (Positive dyadic density) — RIGHT SHAPE, but requires rationality.** Proves
  `A_S(2X) − A_S(X) ≥ c_Q X` (a **linear, single-orbit, positive** lower density on the digit-`1` positions
  `S={n:d_n=1}`) — **exactly the shape `(K)` needs.** But the hypothesis is a **rational** `P/Q = Σ n d_n 2^{−n}`,
  and the method is "the **integral carry recurrence forced by rationality**" — i.e. it works because a rational's
  binary expansion has an **eventually periodic / deterministic carry**. The authors state it **would not extend to the
  binary digits of `3^n` or to `c↦⌊3c/2⌋`, which lack that rational carry structure.**

## B. The resource method attempted on our orbit — stops at the same place `[OBSERVED/PROVEN]`
The valuation budget gives `Σ_{odd i<n} v₂(3c_i−1) = O_n + E_n = n` (`+` boundary `v₂(c_n)`) — a **first-moment
tautology** (as in `EK2_SECOND_BUDGET`). To force `E_n ≥ n/3` one needs a **lower bound on the up-jumps**
`u_i=v₂(3c_i−1)−1`; since `u_i≥1 ⟺ c_i≡3 (mod 4)`, `(K)` reduces to a **positive frequency of the residue `c≡3 mod4`**
along the orbit (empirically `≈0.50`) — a **single-orbit equidistribution mod 4** (level-2 `(K)`). The budget yields
only the first moment; the mod-4 frequency is exactly the aperiodic-carry information it cannot supply — the **same
reason** `2606.24972` names for non-extension.

## The sharpened missing input `[the (K)-research payoff]`
> **`(K)` = the positive-dyadic-density theorem of `arXiv:2606.24972`, but for an APERIODIC (non-rational) carry** —
> the `×3/2` / base-3/2 orbit. The method that proves the *exact statement `(K)` needs* exists; it is blocked by
> exactly one hypothesis (rational ⇒ periodic carry), and our orbit is the aperiodic case. This is a **concrete,
> current bridge target**: "extend positive-dyadic-density from periodic to aperiodic carry," sharper than the generic
> "P1′." It also explains, from the newest external vantage, *why* `(K)` is hard: positive digit density is now
> provable for periodic carries, and the whole difficulty is **aperiodicity** (= non-Pisot `3/2` = non-sofic = the
> rank-1 amenable wall), consistent with our internal `CROSSING_STRATEGY`.

## Verdict
**(c)/(b) — leads evaluated (both fall short, precise reasons) + the missing input sharpened.** Erdős-400 is log+a.e.
(dead end); positive-dyadic-density is the right shape but needs rational/periodic carry; the resource method on our
orbit reproduces the first-moment tautology and reduces `(K)` to a single-orbit mod-4 frequency. **Net gain:** the
`(K)` target is now a concrete bridge — *positive-dyadic-density for aperiodic carry* — the most specific, current
formulation of the missing tool this program has. **`(K)` `[OPEN]`. No machine decided. No label upgraded.**

## Reproduce / basis
- freq(`c≡3 mod4` | odd) `≈0.50` (`/opt/homebrew/bin/python3.13`, `N=2·10⁵`). Leads: arXiv:2606.23661 (Erdős 400,
  log+a.e.), arXiv:2606.24972 (positive dyadic density, rational/periodic-carry only). Basis: `K_RESEARCH_COUNT_VS_FREQ`,
  `EK2_SECOND_BUDGET`, `CROSSING_STRATEGY_2026-07-05`, CITATIONS #10/#11.

## Addendum — attempting the aperiodic extension: the break is NON-PERIODICITY (with a self-correction) `[OBSERVED]`
Trying to carry the `2606.24972` method to our orbit, and locating the exact break:
- **Self-correction.** A first probe asked whether the 2-adic map is "non-sofic / one-bit-lookahead." It is **not**:
  `c mod 2^k` **does determine** `⌊3c/2⌋ mod 2^{k−1}` (0 ambiguous, `k=3..8`) — the downward 2-adic factor map is
  **deterministic (sofic)**. So the aperiodicity does **not** live in the factor map; my initial framing was mis-aimed.
- **The real break point.** `2606.24972`'s positive density comes from a rational's binary expansion being **eventually
  periodic** — a **finite carry recurrence** ("complete-lap mass balance," "fixed-pin confinement") that counts a fixed
  number of `1`s per period over infinitely many periods ⇒ linear density. Our observable — the parity/digit sequence
  `a_n = ` bit `0` of `c_n = ` the moving-diagonal digit of `8·3^n` — is provably **non-eventually-periodic** (it is a
  **full 2-shift**, `PARITY_FULLSHIFT_2026-07-05`; non-Pisot `3/2`). So there is **no period**, hence **no complete-lap
  count** — the density is empirically `½` but the *proof mechanism* (periodic counting) is gone.
> **Exact break: periodicity.** The positive-dyadic-density method proves the bound **by** the eventual periodicity of
> a rational expansion; `(K)`'s expansion is aperiodic (non-Pisot `3/2`), which removes the counting mechanism — not the
> density. The missing input is therefore precisely an **aperiodic analogue of the complete-lap / carry-recurrence
> count**, which does not exist in current mathematics (= the non-Pisot / rank-1-amenable wall, once more, now located
> inside the newest positive-density method).
