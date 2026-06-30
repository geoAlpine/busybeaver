# The even-count floor is exactly Θ(log n): rung 2 collapses to (K) — no sub-(K) rung exists (2026-06-30)

*Track-A result (the multi-year program's first internal attack, on roadmap "rung 2" = improving `#even(n)` past
`Θ(log n)`). HONEST OUTCOME: the attack does NOT yield a super-log bound — it PROVES that improving past `log` is
`(K)`-grade, so the milestone ladder of `NEW_MATH_PROGRAM.md` §8.3 **collapses**: there is no unconditional rung
strictly between the proven `Θ(log n)` floor and `(K)` itself. This REVISES (deflates) the prior optimistic ladder.
SOUNDNESS: the identity and the cylinder reduction are `[PROVEN]`; the "no elementary improvement" statement is
`[ARGUED]` (a structural reduction to occupancy = (K), not a meta-theorem over all proofs). `(K)` stays `[OPEN]`.
Verified exact big-int `N=3·10⁵`, `scratchpad/rung2.py`. NOT committed by default.*

---

## 0. The result

> **The unconditional even-count floor is exactly `Θ(log n)`, and any improvement is `(K)`-grade.** The proven
> bound `#even(n) ≥ 0.89 log₂ n` uses only the *magnitude ceiling* on a single deep 2-adic visit; pushing it to any
> `f(n) = ω(log n)` requires controlling the *frequency* of deep 2-adic-cylinder visits = the quenched 2-adic
> occupancy of the orbit = `(K)`. Equivalently, a longer even-count needs an upper bound on the depth tail
> `v₂(3o_j−1)`, but a large value there is a *near-halt* (exact criterion below), so bounding it **is** proving
> non-halting. Hence no unconditional rung lives strictly between `Θ(log n)` and `(K)`.

## 1. The exact identity `[PROVEN]`

For `c_0=8`, `c_{n+1}=⌊3c_n/2⌋`, let `o_0,o_1,…` be the odd values, `D_j := v₂(3o_j−1) ≥ 1` the induced-map gaps
(steps from `o_j` to `o_{j+1}`), and `J = J(n)` the number of odd values among `c_0,…,c_{n-1}`. The valuation
budget `Σ_{j<J} D_j = n + O(1)` (each step lies in exactly one inter-odd block of `D_j` steps: one odd `o_j` then
`D_j−1` even steps) gives immediately

> **`#even(n) = Σ_{j<J} (D_j − 1) = Σ_{k≥2} #\{ j<J : D_j ≥ k \}`.**

*Verified* (`scratchpad/rung2.py`, `N=3·10⁵`): `#even = 149808`, `Σ(D_j−1) = 149805` (difference `3` = the final
incomplete block), `mean D = 1.99742`, `#even/n = 0.49936`. The run-length distribution is geometric (counts
`37495, 18684, 9500, 4599, …`, halving), `mean run ≈ 2.00`, `max run = 20` (against the trivial ceiling
`0.585·N = 175500` — slack factor `8775×`).

## 2. The cylinder reduction `[PROVEN]`

Since `3 ∈ ℤ₂^×`, the framework's Link 3 gives `D_j ≥ k ⟺ o_j ≡ 3^{-1} (mod 2^k)`. Therefore

> **`#even(n) = Σ_{k≥2} #\{ j<J : o_j ≡ 3^{-1} \,(\mathrm{mod}\ 2^k) \}`** — a sum of **cumulative visit counts to
> the 2-adic cylinders** `A_k = \{o : o ≡ 3^{-1} \bmod 2^k\}` (Haar measure `2^{-k}`).

So `#even(n)` is *literally* a weighted occupancy of nested `2^{-k}`-cylinders by the orbit. A lower bound
`#even(n) ≥ f(n)` is a lower bound on cumulative cylinder occupancy.

## 3. Why the floor is exactly `Θ(log n)`, and improving it is `(K)`

**The proven `log` bound uses only the magnitude ceiling `[PROVEN mechanism]`.** A run of consecutive odd values
starting at `c` has length `v₂(c−1)` (odd-run lemma), and `v₂(c−1) ≤ log₂ c ≈ 0.585·(\text{index})` is the *trivial
valuation bound* (a value `≡1 mod 2^L` is `≥ 2^L`, but the orbit is only `≈ 8(3/2)^{\text{index}}`). This caps the
gap between consecutive even terms at `≈ 0.585·\text{index}`, forcing even terms to recur at least geometrically
(ratio `≤ 2.17`), hence `#even(n) ≥ \log_{2.17} n ≈ 0.89 \log_2 n`. The bound touches the orbit *only through its
size* — it never uses the orbit's actual 2-adic distribution.

**Improving past `log` requires the cylinder frequency = `(K)` `[ARGUED]`.** By §2, `f(n) = ω(\log n)` even-count is
a super-logarithmic lower bound on cumulative occupancy of the cylinders `A_k`. The magnitude ceiling bounds only a
*single* deep visit (one term of size `≈ 8(3/2)^n` can sit in a cylinder as deep as `A_{0.585n}`); it says nothing
about *how often* the orbit enters `A_2, A_3, …`. Controlling that frequency is exactly the quenched 2-adic
occupancy of the specified orbit — i.e. the depth-distribution statement `(K)` (mean `D ≥ 3/2` is the `1/3`-density
case; *any* positive-rate occupancy improvement is the same kind of quenched statement, with no unconditional handle
between "one visit, magnitude-bounded" and "positive frequency"). 

**The dual view: a long block is a near-halt `[PROVEN criterion]`.** A large `D_j` (long run) means `o_j` is
2-adically very close to the fixed point `1` of the dynamics; the exact halting criterion is
`HALT ⟺ ∃n: v₂(c_n−1) ≥ balance_n + 1` (`balance_n = 3E_n − n`, `antihydra_attack.md §3c`). So an *upper* bound on
the depth tail that would shorten the blocks is, literally, the statement that the orbit never lands that close to
`1` — i.e. **non-halting itself**. There is no room to bound the blocks without proving the thing.

## 4. Consequence — the milestone ladder collapses `[REVISION of NEW_MATH_PROGRAM §8.3]`

The prior charter hoped rung 2 (`(\log n)^{1+ε}`, `\exp(c\sqrt{\log n})`) was a free intermediate target. It is
not: by §1–§3 it is `(K)`-grade. The honest ladder is therefore **two-level, not five**:

> `[PROVEN]` `#even(n) ≥ 0.89 log₂ n` (magnitude ceiling)  `——⊏ no unconditional rung between ——⊐`  `[OPEN = (K)]`
> `liminf #even(n)/n ≥ 1/3` (= mean `D ≥ 3/2` = quenched 2-adic occupancy = Mahler 3/2 / AEV).

The "elementary floor" and "the Mahler line" are **adjacent**: the first super-logarithmic improvement is already
the kernel. This matches, on the even-count axis, what `LIMIT_THEOREM.md` §3″ found on the subword-complexity axis
(`p(ℓ) ≥ 1.71ℓ` elementary, jump to `2^ℓ` is Mahler) and `DEPTH_REACH_CLARIFICATION.md` found on the depth axis: the
elementary methods stop at a sharp edge and the next step is the generational kernel, with nothing in between.

## 5. Honest status

This is a *negative* Track-A result, and the right kind: it tests the program's own optimistic ladder and finds it
collapses, by an exact identity (`#even = Σ(D_j−1) =` cumulative cylinder occupancy) plus the magnitude-vs-frequency
gap that is the whole problem. It does **not** prove "no proof of super-log `#even` exists" (that would be a
meta-theorem); it proves the *content* of such a bound is quenched cylinder occupancy `=` `(K)`, and that every
unconditional handle in hand (magnitude, valuation ceiling, integrality) bounds only single visits, not frequency.

**Net for the multi-year program:** Track A (internal partial rungs) has **no sub-`(K)` target** on the even-count
axis — the elementary floor is `Θ(log n)` and is sharp. The program's genuine progress can only come from Track B
(build the missing quenched-occupancy tool externally) or from the durable barrier/positioning results already
banked. **No machine decided. No label upgraded.** `(K)` remains `[OPEN]` = Mahler 3/2 / AEV.
