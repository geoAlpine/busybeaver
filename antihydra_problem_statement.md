# Antihydra (BB(6) Turing machine) — non-halting as a number-theory problem: state of the attack, and a request for new ideas

*（ChatGPT 等に貼る用の自己完結した説明。下記はすべて機械検証済み（[VERIFIED]）か、文献で確立（[KNOWN]）か、発見的（[HEURISTIC]）かを明記。新しい角度を求めています。既に潰した死に道（§DEAD ENDS）は再走しないでください。）*

## 0. Goal
Decide whether the "Antihydra" Busy-Beaver-6 Turing machine halts. It is equivalent to a clean
number-theory statement (below). We want a **proof** of non-halting, or a genuinely new angle of attack.

## 1. The object [VERIFIED — these are exact, machine-checked]
Integer orbit, the **iterated floor map**:
> `c_0 = 8`,  `c_{n+1} = floor(3·c_n / 2)`  →  `8, 12, 18, 27, 40, 60, 90, 135, 202, 303, 454, …`

(NB: `c_n` is **NOT** `floor(8·(3/2)^n)`; they agree only for `n ≤ 5` and diverge at `n=6`: `90` vs `91`.
The iterated floor loses one low bit per step. Growth is still `c_n ~ A·(3/2)^n` with a *different*
constant `A = 8 − κ = 7.864177262…`, `κ = (1/3)·Σ_{k: c_k odd}(2/3)^k`.)

Let `E_n =` #{ even values among `c_0, …, c_{n-1}` }, and define the **balance**
> `balance_n = 3·E_n − n   (= 2·#even − #odd)`.

**Halting criterion [VERIFIED]:** the machine HALTS iff `balance_n = −1` for some `n` (balance starts at
`+2`, gets `+2` on each even `c`, `−1` on each odd `c`). Equivalently: HALT ⟺ the even-density `E_n/n`
ever drops to `1/3`. So **non-halting ⟸ even-density stays `> 1/3` for all `n`** (a one-sided bound).

## 2. The 2-adic reformulation [VERIFIED, proven]
Let `v2(x)` = 2-adic valuation (number of trailing 0-bits). 
**Lemma (odd-run = valuation):** the maximal run of consecutive odd values starting at `c` has length
exactly `v2(c − 1)`. *Proof:* if `c = 1 + 2^L·m`, `m` odd, then `floor(3c/2) = (3c−1)/2 = 1 + 3·2^{L−1}m`,
so `v2` drops by exactly 1 per step until the value is even. ∎  (Verified: 50 034 maximal runs, 0 errors.)

Define `depth_n := v2(c_n − 1)`. Combined with the balance bookkeeping (a run of length `L` lowers the
balance by `L`):
> **HALT ⟺ ∃ n:  `depth_n ≥ balance_n + 1`.**  Equivalently NON-HALT ⟺ `depth_n < balance_n + 1` ∀n.

Since `balance_n ~ n/2` (even-density `≈ 0.5`), and the small-`n` region is finite-checked (min over
`n ≤ 2·10^5` of `balance_n + 1 − depth_n` is `3`, attained only at `n = 1`), **non-halting is implied by**
> **`depth_n = o(n)`**  (odd-runs grow sub-linearly).

**Equivalent "potential walk" form [VERIFIED]:** `Φ_n := balance_n − depth_n`. Then HALT ⟺ `Φ_n ≤ −1`;
`Φ` is **frozen** during odd-runs and changes by `+2 − L'` at each even step (`L'` = length of the run
about to start, `P(L') = 2^{−(L'+1)}` empirically, mean `1`, so mean drift `+1` per even step). `min Φ = 2`.

## 3. What is unconditionally known vs. what is needed
- **[VERIFIED, unconditional ceiling]** `depth_n = v2(c_n − 1) ≤ log2(c_n) ≈ n·log2(3/2) ≈ 0.585·n`
  (since `2^{depth} | c_n − 1 < c_n`). 
- **[HEURISTIC/empirical]** `depth_n ~ log2(n)` (massively sub-linear); the longest odd-run by step `N`
  is `~ log2 N`.
- **The wall is one constant:** unconditional gives `depth ≤ 0.585n`; the halt threshold is `balance ~ 0.5n`.
  Since `log2(3/2) = 0.585 > 0.5`, pure size/counting **cannot** close it. We need `depth = o(n)`, but only
  `depth ≤ 0.585n` is proven.

## 4. The arithmetic core (where the difficulty lives) [VERIFIED]
`2^n·c_n = 8·3^n − S_n`, where `S_n = Σ_{k<n, c_k odd} 2^k·3^{n−1−k}` (a parity-weighted sum), `S_0=0`,
`S_{n+1} = 3·S_n + 2^n·[c_n odd]`. Then `depth_n ≥ L ⟺ 8·3^n − S_n ≡ 2^n (mod 2^{n+L})`.
- The **low `M` bits of `S_n` are tame**: `S_n ≡ 3^{n−M}·S_M (mod 2^M)` for `n ≥ M` (verified) — a pure
  `×3 mod 2^M` cyclic action (period `2^{M−2}`).
- But `depth_n` is read from bits `[n, n+L)` of `8·3^n − S_n`, and **bit `n` of `S_n` is a carry-sum of
  essentially the entire parity history** (`~0.6n` terms `2^k 3^{n−1−k}` reach bit `n` via long carries).
  So `depth` lives exactly at the **"carry into bit `n`"**, which is NOT a bounded function of recent
  parities. **Controlling this carry = the whole problem.**

## 5. §DEAD ENDS — already ruled out, do NOT re-propose these
- **[PROVEN] Dynamics alone bound nothing.** The map `T(c)=floor(3c/2)` has `T^t(c+2^j) − T^t(c) =
  3^t·2^{j−t}`, so flipping bit `j` flips parity bit `j`: the coding `c ↦ (parity of T^n c)_n` is
  **surjective onto {0,1}^ℕ** (full 2-shift). Over the "free incoming bit" automaton the min-mean
  even-density is `0`. ⇒ Any proof must use the **arithmetic of the specific point**, not the dynamics /
  any finite-state / transfer-operator model.
- **[PROVEN] 2-adic re-encoding is tautological.** The functional `Ψ(c) = Σ_{j≥0,[T^j(c) odd]}(2/3)^j`
  satisfies `Ψ(c) = [c odd] + (2/3)Ψ(floor(3c/2))`, and `Ψ(c) = 3c` solves it exactly. So every "universal
  2-adic constant / partial-sum" reformulation collapses back to `depth_n = v2(c_n − 1)`. No handle.
- **[PROVEN] No bootstrap from max-run.** Bounding the *max* run length `≤ R` only forces even-density
  `≥ 1/(R+1)` (useless unless `R<2`); the density depends on the run-length *distribution* (mean), not max.
- **[KNOWN, literature, two deep surveys] Existing analytic tools don't reach it:**
  - Mahler's 3/2 problem / `{(3/2)^n mod 1}`: the best unconditional result (Flatto–Lagarias–Pollington
    1995) bounds the **range** (spread `≥ 1/3`), **not the density/frequency** — does not apply.
  - **Sum-product / exponential sums** (Bourgain–Konyagin, Bourgain–Glibichuk–Konyagin, Bourgain–Chang,
    Kurlberg) require a multiplicative subgroup `H` of a **fixed** modulus `q` with `|H| ≥ q^δ`
    (polynomially large). Here `q = 2^k`, `k ~ cn`, and the orbit `{3^j mod 2^k : j ≤ n}` has size
    `~ n ~ log2 q` — **logarithmic in the modulus**, exponentially below `q^δ`. **Regime mismatch:** the
    right tool (2,3 multiplicative independence ⇒ mixing) provably does not reach the log-size-subgroup /
    moving-modulus regime. (Korobov/Vandehey: same, fixed modulus.)
  - **Closest in shape but wrong object:** Ridout / Schmidt **Subspace Theorem** gives, for a *fixed
    algebraic irrational*, maximal 0-block at position `n` of length `o(n)` — exactly "depth `= o(n)`" —
    but for the digits of ONE fixed real, not the moving sequence of distinct integers `c_n`.
  - Digit-sum joint-distribution results (Spiegelhofer; Drmota–Spiegelhofer 2025) are about digit sums of
    *generic* integers (existence/density only). Carry-propagation anti-concentration (Izsák–Pippenger) is
    *average-case* over random inputs. Stewart 1980: `#nonzero binary digits of 3^n ≳ log n/log log n`
    (a *count*, density→0, not a run-length / moving-bit statement).

## 5b. Additional angles already evaluated (do NOT re-propose without resolving the stated obstruction)
- **Markov-ization with a finite "carry state" (even non-stationary).** No finite stationary chain exists:
  the depth/parity is provably **not** a function of any bounded window of recent parities (full-2-shift
  no-go), and the carry-state determining `depth_n` grows like `depth_n ~ log n` (unbounded). A
  non-stationary chain with growing state just re-describes the orbit; it yields a bound only if its
  transition kernel has provable structure = the equidistribution. (Cleanest framing: bound the
  **carry-chain length** of the `×3 + injection` process — connects to Izsák–Pippenger carry propagation,
  but that is **average-case** over random inputs and does not transfer to the single deterministic orbit.)
- **Transfer-operator / weighted-shift spectral analysis on ℤ₂.** Right framework, but by the no-go the
  relevant operator is the **full-shift** (entropy `log 2`) operator; its spectral gap gives equidistribution
  for **a.e. point / the Bernoulli invariant measure** = exactly the heuristic, **NOT** the specific orbit
  from `8` (a measure-zero point, invisible to spectral/measure methods). Same obstruction that stops
  Furstenberg/Rudolph rigidity from resolving Mahler.
- **Kolmogorov incompressibility of `S_n` / the parity sequence.** False premise: the sequence is
  **computable** (Kolmogorov complexity `O(log n)`), hence maximally **compressible**, not incompressible.
  The real intuition ("too pseudorandom to conspire to halt") formalizes as **normality / pseudorandomness
  of a specific computable sequence** — itself the open equidistribution (cf. normality of π), not capturable
  by Kolmogorov complexity.

## 5c. Tropical / information-flow / moving-modulus reframings — evaluated, same wall
A good high-level reframing ("exponential-weighted information geometry / carry propagation") suggests
three languages; each was tested and reduces to the same obstruction:
- **Tropical / max-plus (saddle point of the bit-`n` contribution).** [TESTED] The term magnitudes
  `2^k 3^{n-1-k}` are **monotone decreasing in `k`** (argmax at `k=0`, leading bit `~1.585n`, irrelevant to
  bit `n`); the Newton polygon gives only `v2(S_n)=3` (the tame low end). **All `~n` terms contribute to
  bit `n` comparably (genuine mixing) — there is no interior saddle / dominant term to exploit.**
- **Information flow (inflow/leakage, "deterministic drift inequality").** This is the `Φ`-potential
  (§Φ-walk) re-named; the inflow/leakage split yields no conserved quantity. The drift is `+1` **in
  expectation only**; a *deterministic* drift lower bound is exactly what is missing (= the problem).
- **Moving modulus → cut of a single 2-adic object.** [RIGHT SHAPE — matches the Subspace-theorem
  direction] but the relevant single object is the orbit's own generating constant, which is **not
  algebraic** (orbit-defined; 2-adically degenerate: `3κ = 24`, i.e. `κ = 8`, `A = 0` in `ℤ₂`). The
  Subspace Theorem needs an algebraic number — so "realize the carry-bit as digits of one object" hits the
  already-named gap (no *algebraic* object encodes the moving carry-bit).

**Meta:** these are the right *vocabulary* for the problem, but re-describing the specific-point /
non-algebraicity wall in tropical / information / 2-adic language does not supply a tool that crosses it.

## 6. The precise question for you
**Non-halting ⟺ `depth_n = v2(c_n − 1) = o(n)` for the iterated-floor orbit** `c_{n+1}=floor(3c_n/2)`,
`c_0=8`, equivalently a one-sided lower bound `even-density(c_0,…,c_{n-1}) > 1/3` for all `n`,
equivalently control of the **carry into bit `n` of `S_n = Σ_{k<n,c_k odd}2^k 3^{n-1-k}`** in the regime
where the relevant multiplicative orbit has size `~ log` of the modulus.

We are looking for **genuinely new angles**, e.g.:
- A different *reduction* of Antihydra non-halting to a problem with known unconditional tools.
- A clever *potential/Lyapunov function* (other than `Φ`) with a **deterministic** (not in-expectation)
  drift bound, or a self-improving / renormalization argument exploiting the `×3 mod 2^M` low-bit structure.
- A way to *realize the moving carry-bit as the digits of a single algebraic-type object* so the Subspace
  Theorem applies (the "closest" tool).
- Any partial unconditional result: even `even-density > 1/3 − ε` on a subsequence, or `depth_n ≤ (0.5−ε)n`
  unconditionally (which, with `balance ~ 0.5n`, would still need the density bound — so explain how to get
  the balance lower bound too).
- A clean **conditional** theorem (non-halt assuming a precisely-stated, plausible, named conjecture) is
  also valuable if the reduction is fully rigorous.

Please be explicit about **unconditional vs conditional**, and about the **regime** (fixed modulus vs the
moving `k ~ cn`). If you also conclude it is open, say so and name the single most promising line.
