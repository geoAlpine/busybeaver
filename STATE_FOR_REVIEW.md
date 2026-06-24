# BB(6) / Antihydra non-halting — current state, for external review

*Self-contained summary of a research programme aimed at proving the open kernel behind BB(6). All "verified"
facts are machine-checked (exact integer/rational arithmetic where stated); "measured" facts are numerical.
Discipline: 0 false proofs; ~8 tempting leads were retracted after failing verification. Looking for expert
input on the directions and on whether any technique we missed could apply. Questions at the end.*

## 1. The problem
The Busy Beaver value **BB(6) is open and provably "Hard"**: the bbchallenge community reduced it to ~1104
"holdout" 6-state Turing machines ("cryptids"), each equivalent to a number-theoretic open problem. The
flagship is **Antihydra**: the integer orbit
```
c_{n+1} = floor(3 c_n / 2),   c_0 = 8     (8,12,18,27,40,60,90,135,...)
```
The machine halts iff the "balance" `balance_n = 3 E_n − n` (E_n = #even among c_0..c_{n−1}) ever reaches −1.
Conjecturally it never halts (probabilistic heuristic: even-density → 1/2 > 1/3). Deciding it is equivalent
to a statement about the equidistribution of this orbit, in the same class as **Mahler's 3/2 problem (1968)**.

## 2. Exact reduction to a single hypothesis (verified)
Define the parity bits `e_j = [c_j odd]`. Exact identities (verified):
```
2^n c_n = 8·3^n − S_n ,   S_{n+1} = 3 S_n + 2^n e_n ,   S_n = Σ_{j<n, e_j=1} 2^j 3^{n−1−j}
depth_n := v2(c_n − 1) = v2(8·3^n − S_n − 2^n) − n
```
**Renewal structure (verified):** `depth_n` counts down deterministically (`d≥1 ⇒ d−1`) and, at even steps
(`c=2c'`), jumps to a fresh `D = v2(3c' − 1)`. **Exact halting criterion** [corrected after review]:
```
non-halt  ⟺  balance_n = 3 E_n − n ≥ 0  for ALL n   ⟺   running even-density E_n/n ≥ 1/3 at every prefix.
```
The following are **SUFFICIENT** (the standard heuristic), NOT equivalent — non-halt does not force `depth`
sublinear, and *fixed-k* equidistribution alone is not enough (one needs control as the window grows with n):
```
[ suitable growing-window equidistribution of the renewal states c'_j mod 2^k ]
      ⟹  even-density → 1/2  and  geometric depth tails  ⟹  depth_n = o(n)  and  balance_n ≥ 0 ∀n  ⟹  non-halt.
```
**The 2-adic engine (verified, exact arithmetic):** `T(x)=floor(3x/2)` is a measure-preserving 2-to-1 EXACT
endomorphism of ℤ₂. The induced low-digit chain on ℤ/2^k has Dobrushin coefficient `δ(P^k)=0` (it forgets its
state in exactly k steps), and the k-step map (k incoming high digits → state mod 2^k) is a **bijection**.
This yields a **rigorous conditional theorem**:
> **(Conditional theorem.)** If the incoming high digit `bit_k(c_n)` is asymptotically independent of the
> low-digit state `c_n mod 2^k`  [call this **(H)**], then even-density = 1/2 and Antihydra never halts.
Everything except (H) is unconditional. **(H) is SUFFICIENT for non-halt, and — under the renewal coding —
is essentially equivalent to (more precisely, reduces to / is implied by) equidistribution of the diagonal
bit `bit_n(3^n) = floor((3/2)^n) mod 2`.** [weakened from "⟺" after review.] (The same structure unifies
the other cryptids: multiplier `2^a/3^b`, shrinking base `p`,
diagonal digit `floor((2^a/3^b)^n) mod p`; e.g. o18 uses 8/3, p=3, where the digit `=2` is literally Erdős's
ternary-digit-of-2^n problem.)

## 3. What is measured (robust numerics)
- Full `√N` cancellation in Weyl sums `Σ_{n≤N} e(h(3/2)^n)`; `{(3/2)^n}` equidistributes.
- even-density → 1/2 (margin ≫ 1/3); `P(depth ≥ L) = 2^{−L}` to high precision (geometric).
- All fixed bit positions equidistribute (shift-invariance, spread 0.0027 over k=0..15).
- `bit_k(c_n) ⊥ c_n mod 2^k`: mutual information ≈ 0 (~1000× margin) — i.e. (H) holds empirically.
- 2-adic ⊥ 3-adic (MI≈0); the 3-adic expansion re-encodes the parity history (`c_n mod 9 ↔ (parity_{n−1},
  parity_{n−2})` bijectively).
- Renewal jump heights **behave as an iid-geometric renewal process** with zero drift (centered sums ~ `√N`
  random walk). [What is established: geometric tail, lag-k decorrelation/`MI≈0`, renewal mixing; full
  independence is NOT claimed.]
- **The parity sequence has MAXIMAL linear complexity (= M/2, Berlekamp–Massey)**: it is the nonlinear filter
  (the moving bit-n extraction) of the linear-feedback carry `S_n` — a max-complexity self-referential generator.

## 4. The obstruction map — why every known technique fails (the crux)
| technique | precise reason it does NOT apply |
|---|---|
| van der Corput / Weyl differencing | **closed** on the multiplicative recurrence `(3/2)^n` (it is a fixed point of differencing; measured: differenced sums stay `O(√N)`, no gain) |
| sum-product (Bourgain–Konyagin, …) | needs a subgroup `|H| ≥ q^δ`; here `{3^j mod 2^k}` with `k ~ cn` is **log-size** in the modulus — exponentially below threshold |
| Fourier / large-sieve / Stewart–Baker | control the **off-diagonal** (low bits = the `×3`-coset, where the character sum cancels unconditionally); but the depth/parity live at the **moving 2-adic diagonal** (bit at position ~n), unreachable. Large-sieve also fails: the linear form sits on a thin `×3`-subgroup (2nd moment `~189N`). Stewart bounds the *archimedean* digit-count of `3^n` (→∞), uncorrelated with the *2-adic* trailing-zero depth |
| measure rigidity (Furstenberg–Rudolph–Lindenstrauss / ELV) | a **rank ≥ 2** phenomenon (full `{×2,×3}` action); the orbit iterates ONE map `×3/2` = **rank 1**; rank-1 has a continuum of invariant measures, no rigidity. (Verified: the orbit is not `×2`- or `×3`-invariant) |
| subspace theorem (Schmidt/Ridout) | gives `o(n)` digit-runs for a **fixed algebraic number**; ours is a **moving integer orbit** |
| self-consistency / fixed-point uniqueness | **circular**: feeding the incoming digit independently of the state already assumes (H) |
| **Tao (2019) Collatz transport/entropy** | proves equidistribution for **almost all** starting points (log-density 1); decides **no single orbit**. Antihydra is one specific orbit (seed 8). This is the **closest existing technique** and it still hits the same single-orbit wall |

**Unified diagnosis.** Every known tool controls a *generic / averaged / fixed / off-diagonal* slice perfectly
and fails identically on the **specific orbit at the moving 2-adic diagonal**.

## 5. The open kernel as seen from four closely related viewpoints
*(These are tightly linked under the renewal coding, not asserted as strictly equivalent.)*
1. **Arithmetic:** a sufficient / essentially controlling form is that `floor((3/2)^n) mod 2` equidistributes
   (Mahler-3/2; for base 3: Erdős ternary).
2. **Dynamical:** the seed `8 ∈ ℤ` (a Haar-null point) is non-exceptional for the exact ℤ₂-endomorphism `T`.
3. **Probabilistic:** (H) — incoming high digit ⊥ low-digit state.
4. **Sequence-design:** the even-density of the nonlinear-filtered, max-linear-complexity carry `S_n` is 1/2.

## 6. First unconditional partials (what we CAN prove)
- `depth_n ≤ 0.585 n` (trivial 2-adic bound).
- **Infinitely many even terms** (the orbit cannot stay `≡1 mod 4`/odd forever — that forces `c=1`).
- **`E_n = Ω(log n)`** even terms: consecutive even positions satisfy `p_{i+1} ≤ 1.585 p_i` (from `depth ≤ log2 c`),
  geometric, so `E_n ≥ log N / log 1.585`. (Far below the needed positive density.)
- Off-diagonal (fixed-modulus) character-sum cancellation, unconditional.
- Top `~log n` bits equidistribute (Weyl/Benford on `{n log2 3}`; `log2 3` is not Liouville, CF max partial
  quotient 55 in first 25 terms). Hard barrier: this reaches only `Θ(log n)` bits, the diagonal is at `Θ(n)`.

## 6.5 NEW conditional theorem — the moment / additive-energy route (strongest concrete lead)
Working with the renewal jumps `D_j = v2(3c'_j − 1)` (`c'_j` = the induced first-return orbit, `c'_{j+1} ≈
(9/4)c'_j`): `avg jump = (1/J)Σ_k N_k` with `N_k = #{j≤J : c'_j ≡ 3^{−1} (mod 2^k)}`. By Hölder,
`N_k ≤ (Σ_r count_r(k)^{2m})^{1/2m}` where `count_r(k)=#{j≤J: c'_j ≡ r}`. If the **2m-th moment**
`M_{2m}(k)=Σ_r count_r(k)^{2m}` is of random order `O(J^{2m}/2^{(2m−1)k})`, then
`avg jump ≤ C^{1/2m}·Σ_{k≥1} 2^{−k(2m−1)/2m}`. Thresholds: 2nd moment → even-density `≥ 0.293` (just under
1/3); **4th moment → `≥ 0.405 > 1/3`**; 6th → `0.44`. Empirically the 4th moment is `~1.3×` random (need
`≤ 3.45×`), giving even-density `≥ 0.39`.
> **CONDITIONAL THEOREM [implication rigorous; hypothesis open].** If the 4th additive-energy moment
> `Σ_r count_r(k)^4 ≤ C·J^4/2^{3k}` (`C ≤ 3.45`) holds for the induced orbit `c'_j mod 2^k`, then running
> even-density `≥ 1/3` and **Antihydra never halts**.
This **reduces non-halt from full equidistribution to a 4th additive-energy bound** — a different,
additive-combinatorial target. The moment counts `#{(i₁..i₄): c'_{i₁}≡…≡c'_{i₄} mod 2^k}` = collisions
`v2(c'_i − c'_j) ≥ k` of a **geometric-growth** induced orbit; the differences `c'_i − c'_j` are S-unit-like,
so **p-adic Baker / linear forms in logarithms may bound `v2(c'_i − c'_j)`**, and additive-energy machinery
may bound the moment. (This is the most promising near-term route and the natural place for
additive-combinatorics / Diophantine expertise.)

## 7. What a proof needs (precise targets for a new tool)
- **(α)** equidistribution of a **rank-1 specific orbit** of `×(2^a/3^b)` — i.e. effective "rank-1
  Furstenberg" with a Diophantine condition on `log2 3`; OR
- **(β)** a **sub-linear 2-adic depth bound** `depth_n = o(n)` for the self-referential linear-feedback carry
  `S_n` (improve the trivial `≤ 0.585 n`) — i.e. control the moving 2-adic diagonal digit.
Constraints (from failed leads): must engage the state↔incoming coupling (not assume independence); must be
intrinsically 2-adic (archimedean misses the depth); must be single-orbit (not almost-all); must survive
verification on the real orbit.

## 8. Candidate seeds we have not been able to develop
2-adic renewal/thermodynamic formalism (a transfer operator on the *orbit's* law, not the state's); a theory
of self-referentially-defined 2-adic constants' digit normality (`S_n/3^{n−1} → Σ_{e_j=1}(2/3)^j`); adapting
nonlinear-filter/linear-complexity (sequence-design) tools to this specific generator; a single-orbit
strengthening of Tao's transport method; anti-concentration for linear forms with explicit `2^j 3^{n−1−j}`
coefficients at a moving modulus.

## 9. Questions for the reviewer
1. Is there a technique we missed that controls a **single specific orbit** at a **moving 2-adic position**
   (as opposed to almost-all / off-diagonal)? Any 2-adic/p-adic equidistribution machinery for individual
   trajectories of `×(p/q)`-type maps?
2. Can Tao's (2019) transport/entropy method be **localized to a single orbit** under a Diophantine condition,
   or is the almost-all step fundamental?
3. Does the **maximal-linear-complexity / nonlinear-filtered-LFSR** framing connect to any provable
   correlation/anti-concentration bound for *this specific* generator?
4. Is there a known conditional reduction of Mahler-3/2 (or single-orbit Collatz equidistribution) to a more
   standard conjecture (effective `×2,×3`; GRH-type; abc; a Diophantine statement on `log2 3`)?
5. For the linear depth-form `depth_n ≥ L ⟺ S_n ≡ 8·3^n − 2^n (mod 2^{n+L})` with explicit
   `2^j 3^{n−1−j}` coefficients: is the moving-modulus exponential sum amenable to any method? (It is
   *linear in the parity variables `e_j` once the orbit is fixed* — unlike the nonlinear Mahler sum — though
   the `e_j` are themselves the orbit's bits, so the form is self-referential.)
6. **[from review — the most promising weakening]** Antihydra needs only a **one-sided** statement
   (running even-density `≥ 1/3`), NOT full equidistribution (`= 1/2`). **Is there any known method giving a
   one-sided lower bound on the frequency of a single MOVING digit** (e.g. "the diagonal bit is 0 with
   density `≥ 1/3`") that falls short of, and is easier than, full equidistribution? Our only unconditional
   one-sided result is `E_n = Ω(log n)`; can the `> 1/3` target admit a weaker-than-equidistribution tool?
   *(Sharpened: in renewal terms `non-halt ⟺ Σ_{j≤J}(D_j−1) ≤ J ∀J`, `D_j=v2(3c'_j−1)`; the true centered
   sum is ~`√J` while we only need `≤ J` — a ~250× margin empirically. The weakest sufficient target is
   `Σ_{j≤J} v2(3c'_j−1) = O(J)` for ANY constant, i.e. just **positive** even-density `≥ 1/C` — strictly
   weaker than equidistribution. Still open: the trivial `depth ≤ 0.585·pos` gives only `Ω(log)` evens.)*
7. **[from review — is the obstruction intrinsic or an artifact?]** Our obstruction map says every known tool
   fails at the **moving 2-adic diagonal**. But "moving diagonal" is a feature of *our* coordinates
   (`bit_n` of `3^n`, modulus `2^{n+L}`). **Is there any known coordinate change, group/solenoid extension, or
   symbolic realization that converts this moving diagonal into a FIXED observable** (where standard
   equidistribution/mixing tools would apply)? A breakthrough may come from re-coordinatizing the problem
   before any new theorem. *(Our preliminary view: the solenoid and the induced first-return map both DO turn
   the moving diagonal into a fixed observable — but along a **rank-1** orbit, and rank is coordinate-
   invariant; so the moving diagonal looks like a removable artifact while the **rank-1 specific-orbit**
   obstruction underneath looks intrinsic. The orbit is the diagonal `a=b=n` slice of `3^a/2^b` and does not
   fill the rank-2 action — is there a non-obvious coordinate embedding the rank-1 slice into a genuinely
   rank-≥2 / mixing structure?)*
8. **[the most actionable — additive energy]** Can the **4th additive-energy moment**
   `Σ_r #{j≤J: c'_j ≡ r mod 2^k}^4` of the geometric-growth induced orbit `c'_j` (where `c'_{j+1}≈(9/4)c'_j`)
   be bounded by `O(J^4/2^{3k})` **unconditionally**? Equivalently, bound the collision count
   `#{(i,j): v2(c'_i − c'_j) ≥ k}`. Does **p-adic Baker / linear forms in logarithms** give a lower bound on
   `v2(c'_i − c'_j)` for such an orbit (the differences are S-unit-like)? By §6.5 this would prove Antihydra
   never halts.
