# EUE Coisometry No-Go — ADVERSARIAL RED-TEAM (2026-06-30)

*Independent skeptic audit of the claim (NEWMATH_ODD_CALCULUS.md §2.1–§3): the cross-scale
carry-renormalization cocycle `R_k` is a COISOMETRY, hence its operator-norm Lyapunov exponent is
exactly 0, hence no uniform / operator-norm / spectral contraction can establish EUE — the decay must
live in the data-direction = (K)/(CR). Numerics rebuilt from scratch (NOT importing the authors'
matrices): `/Users/aokiyousuke/quantum-ecc/.venv/bin/python scratchpad/redteam_coiso.py`. No commit.*

---

## 0. Verdict

**[CONFIRMS] the structural facts; [NEEDS-CAVEAT] the phrasing.** `R_k` is genuinely a coisometry —
re-verified independently to machine precision, k=2..7, *and* derived as an exact closed-form identity
(not a numeric/basis artifact). The operator-norm Lyapunov exponent of the cocycle is exactly 0, and
the product of coisometries is again a coisometry, so this holds at every depth. The reduction "the
decay must live in the data-direction (CR)/(K)" is **sound**. The one over-reach is verbal: §0/§2.1.2/§3
say "no spectral gap / norm contraction can **ever** exist" and "(CR) is outside the reach of **any**
operator-norm/spectral bound." Correctly scoped, the proven statement is **"no UNIFORM (top-exponent)
contraction in any FIXED or telescoping/fixed-weight norm."** It does NOT, by itself, exclude (i)
scale-dependent anisotropic weighted norms, nor (ii) contraction on a subspace / along the Oseledets
filtration — and indeed a coisometry cocycle has total contraction available on its kernel. Both of
those, however, collapse back to requiring orbit-specific data, so the no-go's *conclusion* survives;
only the word "spectral/any" oversells.

---

## 1. Check 1 — Is `R_k` really a coisometry, at the right object? [CONFIRMS]

Rebuilt `R_k` from the definition (g_a(s)=r(s)·χ_a(V(s mod 2^k)), V(t)=⌊3t/2⌋ mod 2^k, r=top-bit
Rademacher), restricted to the **odd columns** (the genuinely new block O^{(k+1)}, dim 2^k), mapping to
O^{(k)} (dim 2^{k-1}). This is the correct object: the cross-scale carry-renormalization on the odd
block, the fat (2^{k-1}×2^k) map for which `d^{(k)}=R_k d^{(k+1)}`.

```
 k=2: ||R R*-I||=2.2e-16  sv∈[1.000000,1.000000]  #sv=1: 2/2   dimker=2  =2^(k-1)  even-cols=0
 k=3: ||R R*-I||=5.8e-16  sv∈[1.000000,1.000000]  #sv=1: 4/4   dimker=4  =2^(k-1)  even-cols=0
 k=4: ||R R*-I||=1.8e-15  sv∈[1.000000,1.000000]  #sv=1: 8/8   dimker=8  =2^(k-1)  even-cols=0
 k=5: ||R R*-I||=2.7e-15  sv∈[1.000000,1.000000]  #sv=1:16/16  dimker=16 =2^(k-1)  even-cols=0
 k=6: ||R R*-I||=4.8e-15  sv∈[1.000000,1.000000]  #sv=1:32/32  dimker=32 =2^(k-1)  even-cols=0
 k=7: ||R R*-I||=7.4e-15  sv∈[1.000000,1.000000]  #sv=1:64/64  dimker=64 =2^(k-1)  even-cols=0   [NEW: extends past k=6]
```

- `R_k R_k* = I` to machine eps; **all** 2^{k-1} singular values = 1; even columns vanish identically.
- `R_k* R_k ≠ I` (k=3,5,7: ‖R*R−I‖≈0.96/1.0/1.0, rank 2^{k-1} of 2^k) — so it is a **coisometry**
  (onto, with kernel), NOT an isometry. dim ker = 2^{k-1} = exactly half of O^{(k+1)} — consistent and
  correct. The "coisometry (R R*=I, not R*R=I)" labelling is right.
- **NOT a normalization/basis artifact.** I derived the closed form and matched it numerically (k=5,
  max error 2.6e-15):
  `(R_k R_k*)_{a,a'} = (1/2^k) Σ_{t∈ℤ/2^k} e(2πi(a−a')V(t)/2^k)`.
  Because r²≡1 (Rademacher, |r|=1), s mod 2^k double-covers as s ranges over ℤ/2^{k+1}, and 3 is a unit
  mod 2^k, the inner geometric sum is 2^k·δ for a=a′ and **exactly 0** for odd a≠a′ (their difference is
  even but ≢0 mod 2^k). The coisometry is a genuine algebraic identity. **R_k confirmed coisometry.**

The cocycle Φ=R_2R_3…R_{k}: ‖Φ‖=1.000000 at every depth m=1..6, per-step geomean 1.000000, and ΦΦ*=I
to 2e-15 — a product of coisometries is a coisometry, so **operator-norm Lyapunov ≡ 0 at all depths.**
[CONFIRMS]

## 2. Check 2 — Does "coisometry ⇒ op-norm Lyapunov 0 ⇒ no spectral approach" over-claim? [NEEDS-CAVEAT]

Coisometry ⇒ ‖R_k‖=1 ⇒ top (operator-norm) cocycle Lyapunov = 0. That much is airtight. The over-reach
is equating "top exponent 0" with "no contraction / no spectral route." Three escapes the bare fact
does NOT close:

**(a) Fixed / telescoping weighted norm — genuinely closed (so far so good).** Conjugating the whole
cocycle by a single fixed bounded invertible W changes ‖WΦW⁻¹‖ by at most cond(W), so
(1/m)log‖WΦW⁻¹‖→0: the Lyapunov exponent is conjugation-invariant. A **scale-graded** weight that is
*shared* between adjacent scales telescopes: W_kR_kW_{k+1}⁻¹ chained = W_2(R_2…R_7)W_8⁻¹, again only an
endpoint factor (verified: norm 2.04, geomean 1.13→1). So fixed/telescoping norms cannot lower the
exponent. **Correct, and the note is right here.**

**(b) Scale-dependent ANISOTROPIC norms — NOT closed by op-norm=1.** The standard transfer-operator
escape from "norm-1, no naive gap" is precisely an anisotropic Banach space: different regularity /
weight in different directions, scale-by-scale ([Baladi–Liverani anisotropic spaces; Liverani; arXiv:0907.1402](https://arxiv.org/pdf/0907.1402)).
A scale-dependent weight that is NOT shared across the seam (does not telescope) can in principle make
‖W_kR_kW_{k+1}⁻¹‖<1. The coisometry fact alone does not forbid this. **However**, the only weight that
contracts must up-weight (ker R_k)^⊥ relative to ker R_k *in the directions the orbit actually
occupies* — i.e. it must encode where the orbit data sits. By the ENDOGENOUS §5 adversary (same
automaton, same structure, feedback ≈1 for β≡0), no *structural* (orbit-independent) weight can do
this. So the anisotropic route does not die from op-norm=1; it dies by **collapsing into (CR)/(K)**.
The note's conclusion is therefore right, but its premise ("op-norm 0 ⇒ no spectral route") is the
wrong reason — it should say "any contracting norm must be built from the orbit data."

**(c) Subspace / Oseledets-filtration decay — the note's OWN route, mislabelled "non-spectral."** A
coisometry has total contraction on ker R_k (maps it to 0); a coisometry *cocycle* Φ_{k,k+m} has
singular values {1 (mult 2^{k-1}), 0 (the rest)} — its Lyapunov **spectrum** is {0, −∞}, not "no
contraction." Per Oseledets, the top exponent being 0 says nothing about the lower filtration ([Oseledets / MET](https://en.wikipedia.org/wiki/Oseledets_theorem); [semi-invertible MET for transfer-operator cocycles, arXiv:1001.5313](https://arxiv.org/pdf/1001.5313)).
(CR) — "the orbit vector equidistributes into ker R_k, energy ratio→½" — is exactly a statement about
where the data sits in this filtration. That is a *directional* (Oseledets/quenched) property, which is
still a spectral-theoretic object; calling it "non-spectral, outside any spectral bound" is loose.
Sharper: it is outside any **top-exponent / uniform** bound.

**(d) Compact perturbation / essential spectrum — vacuous here.** Each O^{(k)} is finite-dimensional
(2^{k-1}), so essential spectrum is empty and compact-perturbation arguments are content-free. Not a
missed escape; just not applicable.

## 3. Check 3 — Is "EUE only via data-direction/(K)" valid? [CONFIRMS, scoped]

Within the R_k framework, yes: the only live channel is (CR), the data-direction exponent. Two caveats.
(i) "EUE only via (K)" is near-tautological globally, since (K)⟺EUE; the meaningful claim is "any
operator/spectral handle ON R_k must inject orbit-specific arithmetic," which is sound. EUE may still be
attacked by routes that never touch R_k (magnitude/adelic, additive-energy, Mahler-3/2 number theory) —
the no-go does not and should not claim to close those. (ii) The §3 reduction (CR)⟹(K) is itself only
**heuristic** (flagged in VERIFY_LABELS §3.1): it pushes m→∞ on fixed-N empirical data `d^{(k+m)}` with
the very loose bound ‖d^{(k+m)}‖²≤2^{k+m-1}, and at fixed N the data is meaningful only to k≈log₂N. So
"(CR)⇒(K)" is a plausibility argument, not a proof — correctly carried as [CONJECTURE].

## 4. Check 4 — Distinct from the L_ann single-scale no-go? [CONFIRMS — genuinely distinct]

Yes, and they are dual, not a restatement:
- **L_ann no-go (ENDOGENOUS §5):** single-scale; L_ann **annihilates** the odd block (zero columns);
  the gap is **BLIND** to where the conclusion lives. Mechanism: *can't see*.
- **Coisometry no-go (NEWMATH §2):** cross-scale cocycle; R_k has the odd block as its **entire live
  domain** and transports it faithfully, but is norm-preserving (coisometry); the gap is **absent**, not
  blind. Mechanism: *sees but can't squeeze*.
Different operator (L_ann vs R_k), different object (single-scale spectral gap vs cross-scale Lyapunov),
different failure (annihilation/invisibility vs norm-1/no-uniform-contraction). They converge on the
*same* irreducible core (fresh-bit decorrelation = (K)), which is a strength, not circularity. Distinct.

## 5. Correct scoped form

> **[PROVEN]** `R_k` is a coisometry (R_kR_k*=I exactly, all σ=1, dim ker=2^{k-1}); the cocycle
> Φ_{k,k+m} is a coisometry for all m; hence its **top (operator-norm) Lyapunov exponent is exactly 0**.
> Consequently **no uniform contraction exists in any fixed, or telescoping scale-graded, norm** — any
> norm-contraction would have to use orbit-specific (data-direction) information.
> **[NOT proven by this fact]** that no anisotropic (non-telescoping scale-dependent) weighted norm and
> no Oseledets-subspace/quotient route can contract; a coisometry cocycle in fact contracts totally on
> its kernel. These routes are not killed by op-norm=0 — they **reduce to (CR)/(K)** (the orbit-data
> alignment), which is where the writer correctly places the open problem.
> **Replace** "no spectral gap / norm contraction can ever exist" and "(CR) is outside the reach of any
> operator-norm/spectral bound" **with** "no UNIFORM (top-exponent) operator-norm contraction exists;
> the live decay is a directional Oseledets/quenched exponent = (CR)."

## 6. Sources

- Internal: NEWMATH_ODD_CALCULUS.md (§0,§2.1–§3); ENDOGENOUS_UE_BUILD.md (C2 L_ann χ_odd≡0, §5 no-go +
  C5 adversary); VERIFY_LABELS.md (§1 coisometry confirmed 4.8e-15, §3.1 reduction-is-heuristic);
  EXCURSION_SUPERMARTINGALE.md.
- This audit: `scratchpad/redteam_coiso.py` (independent rebuild; coisometry k=2..7; closed-form
  structural identity; coisometry-of-products; telescoping weighted-norm probe).
- External: [Baladi-type anisotropic Banach spaces for transfer operators (arXiv:0907.1402)](https://arxiv.org/pdf/0907.1402);
  [semi-invertible Oseledets theorem for transfer-operator cocycles (arXiv:1001.5313)](https://arxiv.org/pdf/1001.5313);
  [Oseledets theorem (MET) — top exponent does not control the lower filtration](https://en.wikipedia.org/wiki/Oseledets_theorem);
  [periodic approximation of Lyapunov exponents for Banach cocycles (arXiv:1608.05757)](https://arxiv.org/abs/1608.05757).

No machine decided. No label upgraded.
