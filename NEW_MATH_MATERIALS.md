# Raw materials for the new mathematics — distilled from the whole programme (2026-06-24)

*All facts below are machine-verified (exact arithmetic where marked) or measured; discipline: 0 false
proofs, 7 tempting leads retracted on scrutiny this session. This is the organised substrate a future proof
of the kernel (H) — equivalently Mahler-3/2 / the diagonal-digit equidistribution — must build on.*

## 1. The object
`c_{n+1}=⌊3c_n/2⌋`, `c_0=8`. Exact identities [VERIFIED]:
- `2^n c_n = 8·3^n − S_n`, `S_{n+1}=3S_n+2^n[c_n odd]`, `S_n = Σ_{j<n, e_j=1} 2^j 3^{n−1−j}` (`e_j=[c_j odd]`).
- `depth_n := v2(c_n−1) = v2(8·3^n − S_n − 2^n) − n`.
- **`S_n` is LINEAR in the parity bits `e_j`** with explicit coefficients `2^j3^{n−1−j}`.

## 2. Verified structural ASSETS (what a new tool may USE)
- **[RIGOROUS, exact arith] `T(x)=⌊3x/2⌋` is a measure-preserving 2-to-1 EXACT endomorphism of `ℤ₂`.** The
  low-digit chain on `ℤ/2^k` has Dobrushin `δ(P^k)=0` (forgets its STATE in `k` steps); the `k`-step map
  (incoming digits → state) is a **bijection** `F_k`. ⇒ a rigorous *contraction-to-equidistribution* engine,
  conditional only on (H).
- **[RIGOROUS] Renewal skeleton.** `depth` counts down deterministically (`d≥1⇒d−1`) and jumps at even-steps
  to a geometric `D=v2(3c'−1)`. `non-halt ⟺ depth=o(n) ⟺ even-density>1/3 ⟺ avg jump<2 ⟺ c'_j mod 2^k equidist.`
- **[RIGOROUS] Affine depth law.** `depth_n≥L ⟺ S_n≡8·3^n−2^n (mod 2^{n+L})` — an AFFINE condition on the
  parity history. Off-diagonal (fixed-modulus) part = `×3`-coset ⇒ character sum cancels UNCONDITIONALLY.
- **[RIGOROUS] Parity↔3-adic transducer.** `c_n mod 3 = [c_{n−1} even]`; `c_n mod 9 ↔ (parity_{n−1},parity_{n−2})`
  bijectively. The 3-adic expansion is the even/odd history re-encoded.
- **[PROVEN partials]** `depth_n ≤ 0.585n` (trivial); **infinitely many even terms** (orbit can't avoid
  `3 mod 4` forever ⇒ forces `c=1`); top `~log n` bits equidistribute (Weyl/Benford foothold).
- **[MEASURED, robust]** full `√N` Weyl cancellation; `even-density→½` (margin ≫ `1/3`); `P(depth≥L)=2^{−L}`;
  all bit positions equidistribute (shift-inv, range `0.0027`); high digit ⊥ low state (`MI≈0`, ~1000×);
  2-adic ⊥ 3-adic; jump heights iid-geometric, **zero drift** (`√N` random walk); **parity sequence has
  MAXIMAL linear complexity `=M/2`** (Berlekamp–Massey).

## 3. The obstruction map (why every existing tool fails — precise)
| tool | precise failure |
|---|---|
| van der Corput / Weyl | **closed** on the multiplicative recurrence `(3/2)^n` |
| sum-product | subgroup `{3^j mod 2^k}`, `k~cn` is **log-size**, exp below `q^δ` |
| Fourier / large-sieve / Stewart | control the **off-diagonal** (low bits, `×3`-subgroup); `depth` is a **2-adic moving-diagonal** |
| measure rigidity / ELV | **rank ≥ 2** phenomenon; the orbit is **rank 1** (single map `×3/2`) |
| self-consistency | **circular** (presupposes independence = (H)) |
| subspace theorem | **fixed** algebraic number vs **moving** integer orbit |

## 4. The central OPEN object, in four languages (all the same thing)
1. **Arithmetic:** the diagonal bit `bit_n(3^n)=⌊(3/2)^n⌋ mod 2` equidistributes (Mahler-3/2 / Erdős for p=3).
2. **Dynamical:** the seed `8∈ℤ` (Haar-null) is non-exceptional for the exact `ℤ₂`-endomorphism `T`.
3. **Probabilistic:** the renewal incoming digit `dig_k(c_n)` is independent of the low state `c_n mod 2^k`
   (hypothesis (H)) — equivalently the self-referential carry `S_n` (linear in the history) has an
   equidistributed bit at the moving position `n`.
4. **Sequence-design:** the parity sequence is the **nonlinear filter** (the bit-`n` extraction) of a
   **linear-feedback carry sequence** `S_n`; it has maximal linear complexity; prove its even-density is `½`.

## 5. What the NEW TOOL must do (the precise requirements)
A proof of (H) needs a tool achieving at least one of:
- **(α) rank-1 specific-orbit equidistribution** of `×(2^a/3^b)` — beyond rigidity's rank-≥2 scope; AND/OR
- **(β) control of the 2-adic moving-diagonal digit** of such an orbit — beyond the off-diagonal reach of
  Fourier/sieve; equivalently, control the moving bit of a **self-referential linear-feedback carry**.
Constraints any candidate must respect (learned from the 7 retracted leads):
- must NOT feed the incoming digit independently of the state (that assumes (H) — D2's circularity);
- must engage the **moving/middle** position, not the low/top ends (foothold & off-diagonal are the wrong ends);
- must be intrinsically **2-adic** (archimedean tools miss the trailing-zero depth);
- must survive verification against the real orbit (the CA-randomization lead died there).

## 6. Candidate SEEDS for inventing (α)/(β) — starting points, not solutions
- **2-adic renewal / thermodynamic formalism** for the exact endomorphism `T`: a transfer operator on the
  *orbit's* law (not the state's) that engages the coupling — the `δ(P^k)=0` engine wants an orbit-level
  analogue.
- **Self-referential digit fixed points:** `S_n/3^{n−1} → Σ_{e_j=1}(2/3)^j` is a 2-adic constant whose
  digit-normality is (H); a theory of self-defined 2-adic constants' digits.
- **Nonlinear-filter / linear-complexity theory** (sequence design): statistics of a max-linear-complexity
  filtered LFSR-with-carry — adapt average-case tools to this *specific* generator.
- **Effective Furstenberg at rank 1 with a Diophantine input on `log₂3`:** a genuinely new rank-1 rigidity,
  the hardest but most direct route to (α).
- **The mixed `2^j 3^{n−1−j}` coefficient structure:** an anti-concentration for linear forms with these
  explicit multiplicative coefficients at a *moving* modulus — the linear core of (β).

**Bottom line.** The terrain is fully mapped and the substrate organised. The kernel is one object with four
faces; the new tool must be rank-1 + 2-adic-diagonal + coupling-respecting + orbit-verified. These materials
are the foundation; inventing (α) or (β) is the years-scale phase-2 work.
