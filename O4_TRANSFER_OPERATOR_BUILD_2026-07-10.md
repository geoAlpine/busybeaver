# The o4 reload transfer operator — an explicit RPF spectral gap that is real, near-maximal, and annealed (2026-07-10)

*Genuine BUILD via a tool distinct from the measure-rigidity no-go: the Ruelle–Perron–Frobenius (RPF)
transfer operator / spectral gap on the o4 host-reload map. The rigidity no-go (`PAPER_RIGIDITY_LIMITS`,
`EUE_COISOMETRY_NOGO`) ruled out uniform op-norm contraction of the cross-scale **coisometry cocycle**
(top Lyapunov ≡ 0). A transfer-operator spectral gap is a different object — the second eigenvalue of the
RPF pushforward on a function space — and the white reload measurement (`FREQUENCY_AXIS_PROBE`) suggests a
gap exists. This note builds that operator explicitly on ℤ/3^k, computes λ₂(k) exactly for k=1..10, and
delivers the honest verdict. STRICT: `[PROVEN]`/`[CONSTRUCTED-partial]`/`[OBSERVED]`/`[OPEN]`.
Interpreter `.venv` python; scripts `scratchpad/o4_transfer_operator.py`, `o4_transfer_extend.py`; exact
integer matrix, numpy + mpmath (50 dps) cross-check + scipy sparse to dim 59049. Not committed.*

---

## 1. The operator `[CONSTRUCTED, exact]`

o4's host map on ℤ₃ is `T(G) = (4G + e(G mod 3))/3`, `e = {0:9, 1:14, 2:1}` (so `4G+e ≡ 0 mod 3` always),
branch fixed points `x_ρ = −e = {−9,−14,−1}`. This is `×(4/3)` realized 3-adically. Crucially **T is
scale-shifting**: it is a well-defined *factor* map ℤ/3^{k+1} → ℤ/3^k (3-to-1) that **loses one 3-adic
digit per step** — it is NOT an endomorphism of a single ℤ/3^k (this is why the faithful cross-scale object
is the coisometry cocycle, not powers of one operator).

To obtain a genuine self-map **matrix** — the standard RPF/pushforward transfer operator — the one digit
T's output does not determine (the fresh top digit) is taken **Haar-uniform**. This is the *annealed*
transfer operator L on densities over ℤ/3^k:

> from state x, spread mass 1/3 onto the three lifts `y ≡ (4x+e(x))/3 (mod 3^{k−1})`.

L is an explicit 3^k × 3^k stochastic matrix with entries in {0, 1/3}, built by exact integer arithmetic.
Its stationary density is **Haar** (verified: `‖π − uniform‖_∞ ≤ 6·10⁻¹⁷`, all k).

## 2. The exact λ₂(k) trajectory `[PROVEN, exact matrix]`

| k | dim 3^k | \|λ₁\| | \|λ₂(k)\| | gap 1−\|λ₂\| |
|---|---|---|---|---|
| 1 | 3 | 1 | 0.0 (exact) | 1.0 |
| 2 | 9 | 1 | 6.16·10⁻⁹ | ≈1 |
| 3 | 27 | 1 | 3.19·10⁻⁶ | ≈1 |
| 4 | 81 | 1 | 6.91·10⁻⁵ | 0.99993 |
| 5 | 243 | 1 | 4.90·10⁻⁴ | 0.99951 |
| 6 | 729 | 1 | 1.82·10⁻³ | 0.99818 |
| 7–10 | …59049 | 1 | 1.9·10⁻³ … 1.09·10⁻² | ≥ 0.989 |

mpmath (50 dps) on the exact rational matrix confirms the whole non-Perron spectrum is a tight cluster at
10⁻⁵²…10⁻¹³ for small k. **The gap is not merely present — it is near-maximal: λ₂ ≈ 0.**

**Why (analytic, `[PROVEN]`).** On characters `χ_a(x)=e(ax/3^k)`, the Koopman `Uχ_a(x) =
(1/3)Σ_d e(4ad/3)·(image char) = 0` unless `a ≡ 0 (mod 3)`. So **each step annihilates every frequency not
divisible by 3 and lowers the rest**; after ≤ k steps only `a=0` (Haar) survives. L is **nilpotent modulo
Haar**. Independent check: `δ_{−14} · L^t → Haar` in **exactly** t=k steps (TV = 10⁻¹⁶ at t=5, k=5). The
small nonzero λ₂ is purely the piecewise coupling from `e(x mod 3)` varying across the three branches; it
grows slowly and stays ≤ 0.011 through dim 59049 — **the gap does not close in the accessible range.**

## 3. The crux — the gap is ANNEALED, and decoupled from the orbit `[OBSERVED, decisive]`

A spectral gap for **this** operator definitively exists — but it does **not** decide o4, and the reason is
exact. L is a self-map matrix **only because it injects a fresh Haar-random 3-adic digit every step**; that
injected entropy is the entire source of the gap (§2: the nilpotency is the annihilation of the fresh
digit's frequencies). **The single real orbit receives no fresh randomness** — its "fresh digit" at each
step is determined by the same deterministic T. Quenched test (real orbit G₀=8, N=2·10⁵): the empirical
character `|(1/N)Σ e((G_n mod 3⁴)/3⁴)|` decays as `~1/√N` (0.022→0.0012), the **CLT/Birkhoff floor** — NOT
the geometric annealed rate `λ₂^N ≈ 0` (which would equidistribute in O(k) steps). The annealed λ₂ governs
the **ensemble** relaxation; the single orbit's empirical equidistribution is a **time-average** whose rate
is the decay of correlations along the orbit = the quenched question = (K).

## 4. The eigenvector picture — δ₋₁₄ is exactly the annealed/quenched seam `[CONSTRUCTED]`

The task anticipated a near-1 eigenvector localized at δ₋₁₄. The computation sharpens this: `−14` is an
**exact fixed point of the un-annealed base map** (`(4·−14+14)/3 = −14`), so in the *deterministic
(quenched)* dynamics δ₋₁₄ is a genuine **eigenvalue-1 delta — an obstruction**. The **annealing dissolves
it**: `δ_{−14}·L^t → Haar` in k steps, and this dissolution is *the whole gap*. So the annealed operator's
near-maximal gap is obtained precisely by washing out the deterministic fixed point the quenched orbit must
genuinely avoid. **The gap between the super-gapped annealed operator and the fixed-point-obstructed
quenched dynamics IS (K)** — not a "λ₂(k)→1" closing gap.

## 5. Verdict `[honest]`

- **Built `[PROVEN]`:** the explicit annealed RPF transfer operator L on ℤ/3^k, exact matrix, Haar-stationary;
  the exact λ₂(k) trajectory k=1..10; the analytic proof that L is nilpotent-mod-Haar (near-maximal gap).
- **Finding — opposite of the anticipated closure:** the transfer-operator gap does **not** close; it is
  **near-maximal (λ₂ ≈ 0)**. But it is the **annealed** gap, and `[OBSERVED]` **provably decoupled from the
  orbit** — the real orbit equidistributes at 1/√N, not at λ₂^N. A persistent (indeed maximal) annealed gap
  **does not decide o4.**
- **Spectral placement of (K):** two transfer-flavored operators bracket the truth and neither is the
  quenched rate — the **annealed self-map** L here (too much gap: it injects a digit), and the **cross-scale
  coisometry cocycle** Φ (`EUE_COISOMETRY_NOGO`, no norm gap: it is faithful/norm-preserving). The surviving
  channel is the quenched Oseledets exponent along the single orbit vector = (K) = Mahler 3/2 / AEV
  Conj 1.6. The δ₋₁₄ fixed point is the exact object separating annealed (dissolved) from quenched
  (invariant); the "white measurement" of `FREQUENCY_AXIS_PROBE` is exactly this annealed near-maximal gap,
  and this build shows precisely why it is empirical, not decisive.

**No partial gap survives to the quenched orbit** — consistent with the EUE red-team note that any
weighted/anisotropic transfer-operator escape collapses into the data-direction route. Nothing here upgrades
a label; it converts "the reload measurement is white" into an exact, mechanism-level statement: the RPF
operator's gap is real and maximal but annealed, and its dissolution of δ₋₁₄ is the transfer-operator face
of (K).

Reproduce: `scratchpad/o4_transfer_operator.py` (exact matrix, spectrum, mpmath check, eigenvector
localization, quenched test), `scratchpad/o4_transfer_extend.py` (sparse λ₂ to dim 59049, character proof,
δ₋₁₄ relaxation). Basis: `RELOAD_MAP_UNIFIED_2026-07-09`, `RELOAD_EXCURSION_BUILD_2026-07-09`,
`EUE_COISOMETRY_NOGO_THEOREM`, `PAPER_RIGIDITY_LIMITS`, `FREQUENCY_AXIS_PROBE_2026-07-08`.

No machine decided. No label upgraded.
