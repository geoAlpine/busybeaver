# Odd-block algebra of the carry automaton U(s,0)=⌊3s/2⌋ — coupling matrix, coboundary, filter (2026-06-29)

*Assigned non-spectral mechanism: the ALGEBRAIC structure of `U` and the even→odd coupling matrix `m_{b,a}`
(the no-go used only the spectrum). Compute `m_{b,a}` exactly (k=2..8), test for sparsity / nilpotency /
triangularity / a low-dimensional excited odd subspace; test for an exact COBOUNDARY / telescoping of
`χ_a∘U(·,0)`; honestly assess whether nonlinear-filter / max-linear-complexity theory gives any unconditional
decorrelation. SOUNDNESS PARAMOUNT — every claim labelled; the kernel is NOT cracked. Numerics exact
(roots-of-unity, cyclotomic zero-test): `scratchpad/odd_automaton_algebra.py`, `odd_structure.py`; closed form
machine-verified against the direct character transform for all (b,a), k=2..6. Not committed.*

---

## 0. One-line verdict

**Outcome = (b) a structural ILLUMINATION + new [PROVEN] characterization of the coupling, but it does NOT
reduce the kernel.** The even→odd coupling is **maximally sparse and exactly classified** — `χ_b` (b even)
couples to an odd character **iff `v₂(b)=1`, and then to exactly the pair `{a, a+2^{k-1}}` with `a≡3(b/2) mod
2^{k-1}`** ([PROVEN] closed form below). But (i) the **excited odd subspace is HALF-dimensional**
(`rank = 2^{k-2}` of the `2^{k-1}` odd characters, → ∞), so there is **no reduction to finitely many scalar
correlations**; (ii) there is **NO coboundary / telescoping** for `χ_a∘U(·,0)` — the deterministic map
`V(s)=⌊3s/2⌋ mod 2^k` has a **fixed point at 0** with `χ_a(V(0))=1`, so every cycle-sum is nonzero and no
martingale-difference bound follows; (iii) max-linear-complexity is **orthogonal** to the correlation we need.
A genuinely new by-product: the even-density / parity character `χ_{2^{k-1}}` has `v₂(2^{k-1})=k−1≥2`, so it
couples to **NO odd character directly** — the odd/feedback content reaches even-density only through a
multi-step even→even cascade. This explains *why the obstruction is buried below finite-window data*, but
yields no bound. **Inj_a stays at the CLT floor; [OPEN].**

---

## 1. The exact coupling matrix `m_{b,a}`  [PROVEN — closed form, machine-verified]

`L_ann χ_b = χ_b∘V` for **even** b (and `=0` for odd b, the C2 identity); expand `χ_b(V(s)) = Σ_a m_{b,a}χ_a(s)`,
`m_{b,a} = 2^{-k} Σ_s ω^{b·V(s) − a·s}`, `ω=e^{2πi/2^k}`, `V(s)=⌊3s/2⌋ mod 2^k`.

> **[PROVEN] Closed form.** Writing `s = 2t+ε` (`ε∈{0,1}`) gives the exact digit identity `V(s)=3t+ε`, hence
> `b·V(s) − a·s = (3b−2a)t + (b−a)ε`, and
>
> **`m_{b,a} = 2^{-k}·(1 + ω^{b−a})·Σ_{t=0}^{2^{k-1}−1} ω^{(3b−2a)t}`.**
>
> (Machine-verified equal to the direct transform for **all** (b,a), k=2..6.)

The second factor is a **half-period** geometric sum: with `g=(3b−2a) mod 2^k`, `Σ_{t<2^{k-1}}ω^{gt}` equals
`2^{k-1}` if `g=0`, `−2/(ω^g−1)` if `g` is **odd**, and **0** if `g` is even and `≠0`. For `b` even and `a`
odd, `g=3b−2a` is **always even**, so the sum vanishes unless `g=0`, i.e. `3b≡2a (mod 2^k)`.

> **[PROVEN] Even→odd coupling rule.** For `b` even, `a` odd: `m_{b,a}≠0` **iff `v₂(b)=1`** and
> `a ≡ 3·(b/2) (mod 2^{k-1})`. Hence each even `χ_b` with `v₂(b)=1` couples to **exactly two** odd characters
> — the pair `{a, a+2^{k-1}} = {χ_a, χ_a·(parity)}` — and **every even `χ_b` with `v₂(b)≥2` couples to NO odd
> character**. (Exhaustively confirmed k=2..7: every `v₂=1` row has exactly the predicted pair; every
> `v₂≥2` row has empty odd support.)

**Structure summary (exact, k=2..8):**

| k | 2^k | even→odd nz density | rank(M_odd) = **excited odd dim** | #odd chars | even→even spec. radius |
|---|-----|--------------------|-----------------------------------|-----------|------------------------|
| 2 | 4   | 0.500 | 1  | 2   | 1.0 |
| 4 | 16  | 0.125 | 4  | 8   | 1.0 |
| 6 | 64  | 0.031 | 16 | 32  | 1.0 |
| 8 | 256 | 0.008 | 64 | 128 | 1.0 |

- **Sparse, not nilpotent/triangular.** Even→odd density `→ 2^{-(k-1)}` (exactly 2 nonzeros per `v₂=1` row, 0
  otherwise). The even→even block is **not** nilpotent (spectral radius `1`, from the constant `χ_0`); it is
  not triangular or circulant. The relevant contraction is the mean-zero gap `λ₂` (measured elsewhere), not a
  nilpotency here.
- **Excited odd subspace is HALF-dimensional.** `rank(M_odd) = 2^{k-2}` (the number of `v₂=1` rows), and the
  **union of supports is ALL `2^{k-1}` odd characters** (each odd `a` lies in exactly one excited pair). So
  the odd content is **not** confined to a low-dimensional subspace — it grows like `2^k`.

---

## 2. No coboundary / no telescoping for `χ_a∘U(·,0)`  [PROVEN no-go]

A telescoping bound on the feedback `Inj_a(N)=N^{-1}Σ(β_n−½)χ_a(U(s_n,0))` would follow if `χ_a∘V` were a
coboundary of the deterministic map `V(s)=⌊3s/2⌋ mod 2^k` (`χ_a∘V = g∘V − g (+ const)`), since then the sum
collapses to boundary terms. A coboundary has **zero sum around every cycle** of `V`’s functional graph.

> **[PROVEN] `χ_a∘V` is NOT a coboundary, for any odd `a`, any k.** `V` has a **fixed point at `s=0`**
> (`V(0)=0`), and `χ_a(V(0))=e^0=1≠0`, so the length-1 cycle `{0}` already has cycle-sum `1`. Other cycles
> (lengths e.g. {1,5} at k=4, {1,11} at k=6, {1,3} at k=8) have cycle-sums `≈3.0, 4.7, 3.0` — all nonzero.
> Adding a constant `h` cannot fix it: that forces `h·(cycle length)=cycle-sum` for every cycle, contradicted
> by the unequal ratios (e.g. k=4: `1` on len-1 vs `3.005` on len-5 ⇒ `h=1` and `h=0.601` simultaneously).

So there is **no telescoping and no martingale-difference structure** to exploit from the algebra of `U`. The
`(β_n−½)` weight is itself the self-reference; combined with a non-coboundary integrand there is no exact
boundary collapse. This is independent of, and complementary to, the spectral no-go in `ENDOGENOUS_UE_BUILD.md`
§5: the spectral route fails because `L_ann` annihilates the odd block; the algebraic route fails because the
odd-block integrand is cohomologically nontrivial (fixed point at the trap `s=0`).

**Dynamical reading.** The fixed point `s=0` of `V` is the residue of the **odd-trap** `c≡1 mod 2^k` (after the
`⌊3·/2⌋` shift the trap sits at `0`); the cohomological obstruction `χ_a(V(0))=1` is exactly the trap that the
renewal analysis (`antihydra_renewal_attack.md` §6) identified — re-derived here as a cohomology obstruction.

---

## 3. Nonlinear-filter / max-linear-complexity — no unconditional decorrelation  [reasoned]

`NEW_MATH_MATERIALS.md` §2/§4: the parity sequence is the bit-`n` nonlinear filter of the linear-feedback carry
`S_n` and has **maximal linear complexity `M/2`** (Berlekamp–Massey). Does max-LC force decorrelation of
`bit_k(c_n)` from low characters (i.e. `Inj_a→0`)?

> **No.** Linear complexity is the length of the shortest LFSR reproducing the sequence — a statement about its
> **algebraic span over GF(2)** (unpredictability / period), **not** about empirical **frequencies or
> correlations**. The two are orthogonal: a sequence can have maximal LC while being arbitrarily biased
> (a single `1` among `2^m−1` zeros has near-maximal LC and density `→0`), and balanced sequences can have
> low LC. The quantity we need, `Σ_n(β_n−½)χ_a(U(s_n,0))`, is a frequency/equidistribution correlation; LC
> bounds neither it nor its growth.

This is **the same gap already proven for subword complexity** (`THEORY.md` A3: the subword-complexity floor
says nothing about frequencies). Max-LC adds an algebraic-richness certificate but **zero** correlation
control. So the nonlinear-filter framing gives a faithful description, not an unconditional bound.

---

## 4. Honest verdict

- **(a) structural reduction / partial bound?** **Partial illumination, no reduction.** The coupling is exactly
  classified (`v₂(b)=1` ⇒ pair `{a,a+2^{k-1}}`), but the excited odd subspace is **half-dimensional**
  (`2^{k-2}→∞`) and its support is **all** odd characters, so the Open Lemma does **not** collapse to finitely
  many scalar correlations.
- **(b) new characterization?** **Yes** — two new [PROVEN] facts: the **closed form**
  `m_{b,a}=2^{-k}(1+ω^{b−a})Σ_{t<2^{k-1}}ω^{(3b−2a)t}` with the `v₂(b)=1` pair-rule; and the **even-density /
  parity character `χ_{2^{k-1}}` couples to NO odd character directly** (`v₂=k−1≥2`), so odd/feedback content
  reaches even-density only through a multi-step even→even cascade — an operator-level explanation of why the
  obstruction is invisible to finite-window statistics.
- **(c) reduces?** **No.** No coboundary/telescoping/martingale (fixed-point/trap obstruction, [PROVEN]); no
  decorrelation from max-LC (orthogonal to correlation). `Inj_a` stays at the CLT floor (`max_odd|Inj_a|≈
  0.002–0.003 ≈ 1/√N`, k=4,6,8, N=2·10⁵); the kernel is untouched.

**Genuinely new vs prior.** New: (1) the **exact closed form + `v₂(b)=1` pair classification** of the even→odd
coupling (prior docs only asserted "`U(·,0)` is not a homomorphism, so it mixes in odd `a`"); (2) the **exact
excited-subspace dimension `2^{k-2}`** (= half the odd block — quantifies that the mixing is maximal, not
sparse-into-low-dim); (3) the **cohomological no-go** (`χ_a∘V` is not a coboundary because of the trap fixed
point `s=0`), a route not previously tried — it closes the algebraic/telescoping escape the way §5 of
`ENDOGENOUS_UE_BUILD.md` closed the spectral one. Prior/unchanged: the `v₂`-budget, the trap `c≡1`, the
CLT-floor measurement, the max-LC fact. Net: this **closes the "algebraic structure of `U`" escape route** with
proven reasons (sparse-but-half-dimensional + cohomologically nontrivial), complementing the spectral no-go.

**Exact residual gap.** Unchanged Open Lemma: for each odd `a`, `Inj_a(N)=N^{-1}Σ_{n<N}(bit_k(c_n)−½)·
χ_a(⌊3s_n/2⌋ mod 2^k) → 0`. The algebra of `U` neither bounds it (no coboundary) nor confines it to a
low-dim subspace (half-dimensional excitation). = (K) = Mahler-3/2.

## Sources
- `scratchpad/odd_automaton_algebra.py` (coupling matrix, excited-subspace rank, cyclotomic exact zero-test,
  coboundary cycle-sums, real-orbit `Inj_a`), `scratchpad/odd_structure.py` (exact `v₂(b)=1` pair rule),
  closed-form verification against the direct transform (k=2..6, all (b,a)).
- `ENDOGENOUS_UE_BUILD.md` (C1/C2/C4 identities, seam identity, spectral no-go §5); `ENDOGENEITY_DEFECT.md`
  (recursion, ρ); `antihydra_renewal_attack.md` §6/§12/§13/§14 (trap, conditional theorem, CA falsification);
  `NEW_MATH_MATERIALS.md` (`S_n` linear-feedback carry, max-LC); `THEORY.md` A3 (no finite-order obstruction).

No machine decided. No label upgraded.
