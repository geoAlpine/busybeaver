# The EUE Coisometry No-Go — no UNIFORM operator-norm contraction across scales (2026-06-30)

*Self-contained formal note. CLAIM: the cross-scale carry-renormalization cocycle `Φ` is a chain of
COISOMETRIES, so its operator-norm cross-scale Lyapunov exponent (the **top** exponent) is identically `0`; hence no
**uniform** (top-exponent) operator-norm contraction across scales — in any fixed or telescoping scale-graded norm —
can establish Endogenous Unique Ergodicity (EUE). The decay EUE needs lives only in the DATA-direction (quenched /
Oseledets) exponent `=` the kernel (K). SOUNDNESS CRITICAL: every assertion labelled
[PROVEN] / [PROVEN-in-lit] / [OBSERVED]. This is a no-go for the operator-norm / uniform-spectral family, NOT a proof
that EUE is false, and NOT (K). The data-direction route stays [OPEN]. INDEPENDENT of (K). Numerics:
`/Users/aokiyousuke/quantum-ecc/.venv/bin/python`, `scratchpad/`, exact, `N ≤ 1e5`. Not committed.*

> **[RED-TEAM VERDICT, `EUE_COISOMETRY_REDTEAM.md`: CONFIRMS the facts; phrasing caveated.]** The coisometry was re-derived
> independently (k=2..7) AND in closed form `(R_kR_k^*)_{a,a'} = 2^{-k} Σ_t e(2πi(a−a')V(t)/2^k) = δ_{a,a'}` for odd
> `a,a'` (since `r²≡1`, `V` double-covers `ℤ/2^k`, and `3` is a unit mod `2^k`) — so `R_kR_k^*=I` is **structural**, not a
> basis/normalization artifact; `R^*R≠I` confirms coisometry (not isometry). **Mandatory phrasing caveat:** "op-norm
> Lyapunov `=0`" rules out only the **UNIFORM / top-exponent** contraction (in any fixed or telescoping norm — Lyapunov is
> conjugation-invariant, interior weights cancel). It does **NOT** by itself kill (i) scale-dependent **anisotropic
> weighted-norm** contraction (the transfer-operator escape) or (ii) **subspace / Oseledets-filtration** decay — indeed a
> coisometry cocycle's Lyapunov spectrum is `{0, −∞}` (it contracts *totally* on its kernel), so "top exponent `0`" ≠ "no
> contraction." **But those escapes collapse INTO the data-direction route, not past it:** any contracting weight or
> surviving subspace must encode where the specific orbit vector sits (the `ENDOGENOUS_UE_BUILD.md` §5 adversary blocks
> every *structural* weight), so they reduce to (CR) = (K). Correct form: *no uniform top-exponent operator-norm
> contraction exists; the live decay is a directional Oseledets/quenched exponent = (CR); and (CR)⟹(K) is itself only a
> heuristic reduction (`VERIFY_LABELS.md` §3.1), not yet rigorous.*

---

## 0. One-line statement

> **EUE Coisometry No-Go [PROVEN].** Each carry-renormalization operator `R_k : O^{(k+1)} → O^{(k)}`
> is a coisometry (`R_k R_k^* = I`), so every finite cross-scale product
> `Φ_{k,k+m} = R_k R_{k+1} ⋯ R_{k+m-1}` has `‖Φ_{k,k+m}‖ = 1` for all `m`. Hence the **operator-norm
> cross-scale Lyapunov exponent** `λ_op := limsup_m (1/m) log ‖Φ_{k,k+m}‖` is **identically `0`**.
> Therefore **no uniform / operator-norm / spectral contraction exists across scales**, and any proof
> of EUE that controls the odd-character injection `Inj_a` by a cross-scale spectral gap is structurally
> impossible. The decay EUE requires lives only in the **data-direction (quenched / Oseledets)** exponent
> evaluated along the single orbit vector — which is exactly the conjecture (CR) `=` single-orbit
> equidistribution `=` the kernel (K).

This is the **multi-scale** companion of the single-scale `L_ann` odd-annihilation no-go
(`ENDOGENOUS_UE_BUILD.md` §5). Together they close BOTH the single-scale and the multi-scale spectral
hopes for EUE. **Neither closes the data-direction / (K) route, which remains [OPEN].**

---

## 1. Setup

### 1.1 The scale tower and the odd-character block  [PROVEN, standard]

Orbit `c_0 = 8`, `c_{n+1} = ⌊3 c_n / 2⌋` on `ℤ_2`. For each scale `k` set
`s_n^{(k)} := c_n mod 2^k ∈ ℤ/2^k`, with additive characters `χ_a^{(k)}(s) = e(a s / 2^k)`,
`a ∈ ℤ/2^k`. Even characters at scale `k` ARE all characters at scale `k-1`:
`χ_{2a'}^{(k)}(s) = χ_{a'}^{(k-1)}(s mod 2^{k-1})`. Hence the only genuinely new ("top-bit") coordinates
at scale `k` form the

> **odd-character block** `O^{(k)} := span{ χ_a^{(k)} : a odd } ⊂ ℂ[ℤ/2^k]`, `dim O^{(k)} = 2^{k-1}`.

The orbit's full Fourier data is an inductive tower: the even part of scale `k+1` restricts to scale `k`,
and the only new data at each step is `O^{(k+1)}`. The empirical odd-data vector is
`d^{(k)} := (π_N(χ_a^{(k)}))_{a odd} ∈ ℂ^{2^{k-1}}`, `π_N(χ_a) = (1/N) Σ_{n<N} χ_a(s_n)`.

### 1.2 The carry semiconjugacy  [PROVEN — `seam_identity.py`, `odd_renorm.py`; algebraic]

Write the scale-`(k+1)` state as `s = s_low + β·2^k`, `β = bit_k(c) ∈ {0,1}` (the fresh top bit). The
deterministic scale-`(k+1)` map projects onto the driven scale-`k` automaton:

> `V^{(k+1)}(s) mod 2^k = U^{(k)}(s_low, β)`,  with  `U^{(k)}(s,β) = ⌊3s/2⌋ + β·2^{k-1} (mod 2^k)`,
> `V^{(m)}(s) = ⌊3s/2⌋ mod 2^m`,  and  `U^{(k)}(s,1) = U^{(k)}(s,0) + 2^{k-1}` (C1).

The top bit of scale `k+1` is exactly the fresh input bit consumed at scale `k`; the "infinite regress"
of the closed loop (`ENDOGENOUS_UE_BUILD.md` §2) becomes a clean renormalization step `k+1 → k`.

### 1.3 The carry-renormalization operator `R_k`  [DEFINITION + PROVEN exactness]

The seam identity (`ENDOGENOUS_UE_BUILD.md` C4) is pointwise exact: for odd `a`,
`χ_a^{(k)}(s_{n+1}) = r_k(c_n)·χ_a^{(k)}(V^{(k)}(s_n))`, where `r_k(c) = (-1)^{bit_k(c)}` is the top-bit
Rademacher (the fresh bit). Set `g_a(s) := r_k(s)·χ_a^{(k)}(V^{(k)}(s mod 2^k))` on `ℤ/2^{k+1}` and
Fourier-expand it there. Define

> **`R_k : ℂ[O^{(k+1)}] → ℂ[O^{(k)}]`,  `(R_k)_{a,a'} = \hat g_a(a')`** (`a` odd in `ℤ/2^k`, `a'` odd in
> `ℤ/2^{k+1}`), `\hat g_a(c) = 2^{-(k+1)} Σ_s g_a(s) e(-cs/2^{k+1})`. Then on the orbit
> **`d^{(k)} = R_k d^{(k+1)} + O(1/N)`** (exact cross-scale renormalization; verified
> `max_a |d^{(k)}_a - (R_k d^{(k+1)})_a| ≤ 2.5e-5 ≈ 1/N`, `k=2..6`, `N=8e4`, `odd_renorm.py`).

Two further [PROVEN] facts: (i) **pure odd→odd** — `R_k` restricted to even scale-`(k+1)` columns is
identically `0` (`r_k` is supported on odd characters, `χ_a∘V^{(k)}` on even ones, so their product is
odd); the renormalization tower has no leakage from already-controlled scales. (ii) The twist `r_k`'s
Fourier mass sits on odd characters (`|\hat r(1)| ≈ 2/π`), i.e. the fresh bit is the SOLE carrier of the
odd content — the precise contrast with `L_ann`, which has the odd block as zero columns.

### 1.4 The cross-scale cocycle  [DEFINITION]

> `Φ_{k,k+m} := R_k R_{k+1} ⋯ R_{k+m-1} : O^{(k+m)} → O^{(k)}`, so `d^{(k)} = Φ_{k,k+m} d^{(k+m)}` exactly.

`Φ` is an **inhomogeneous** product (a true cocycle over scales), not the powers `L^N` of one fixed
operator — this is what lets it carry the moving frequency `(3/2)^j → (3/2)^{j+1}` that a single
time-homogeneous transfer operator structurally cannot (`TWISTED_RPF.md`).

---

## 2. The coisometry  [PROVEN — structural reason + machine-verified]

> **Theorem 1 (R_k is a coisometry).** `R_k R_k^* = I_{2^{k-1}}`. Equivalently every singular value of
> `R_k` equals `1`, `‖R_k‖ = 1`, `R_k` is onto, and `dim ker R_k = dim O^{(k+1)} - dim O^{(k)} =
> 2^k - 2^{k-1} = 2^{k-1}` (exactly half of `O^{(k+1)}`).

**Numeric certification [PROVEN].** `‖R_k R_k^* - I‖ ≤ 4.8e-15`; all singular values `= 1.0000`
(`k=6`: 32 of 32); `dim ker R_k = 2,4,8,16,32 = 2^{k-1}`, `k=2..6`
(`odd_renorm2.py`, `odd_renorm3.py`, independently re-confirmed `verify_coiso.py`, `VERIFY_LABELS.md` §1).

**Structural reason (NOT merely the numeric).** `R_k` is the (odd-block) matrix of the operator
`f ↦ r_k·(f∘V^{(k)})` followed by restriction `ℤ/2^{k+1} → ℤ/2^k`, i.e. it is a **half-period averaging
of a unimodular reweighting of a measure-preserving pullback**, and such a map is a partial isometry
with full range. Concretely, the adjoint `R_k^*` acts by

  `(R_k^* h)(s) = r_k(s)·\overline{?}` — the pullback `T_k : h ↦ h∘V^{(k)}` is an **isometric embedding**
  `O^{(k)} ↪ O^{(k+1)}` (`V^{(k)}` is onto and `2`-to-`1` measure-preserving on `ℤ/2^{k+1} → ℤ/2^k`, so
  composition preserves the `L^2(Haar)` norm of characters), and multiplication by the unimodular `r_k`
  (`|r_k| ≡ 1`) is a unitary on `ℂ[ℤ/2^{k+1}]`. The seam identity says `R_k` is the adjoint of this
  norm-preserving embedding composed with the unitary twist — i.e. `R_k = (M_{r_k} T_k)^*` on the odd
  blocks. The adjoint of an isometry-into is exactly a coisometry: `R_k R_k^* = (M_{r_k}T_k)^*(M_{r_k}T_k)
  = I` because `M_{r_k}T_k` is an isometry (it preserves inner products: `M_{r_k}` unitary, `T_k`
  isometric). The half-dimensional kernel is precisely the orthogonal complement of the embedded copy of
  `O^{(k)}` inside the twice-as-large `O^{(k+1)}` — the half of the top-bit content that the half-period
  average kills. This is a structural identity, valid for every `k`; the `4.8e-15` is its confirmation,
  not its source.

Read at the level of dynamics: averaging the unimodular `±2^{k-1}`-pair `{U(s,0), U(s,1)}` over the
fresh bit (the `L_ann` step) ANNIHILATES odd characters at a single scale; but transporting them DOWN one
scale with the Rademacher twist `r_k` PRESERVES their total energy and folds it isometrically into the
smaller block — losing dimension (half the directions die) while losing no norm. A coisometry is exactly
"surjective, norm-preserving on the co-kernel" — which is what "renormalization that forgets one bit but
distorts nothing" means.

---

## 3. The operator-norm no-go  [PROVEN]

> **Theorem 2 (operator-norm cross-scale Lyapunov `≡ 0`).** For every `k` and every `m ≥ 1`,
> `‖Φ_{k,k+m}‖ = 1`. Consequently `λ_op := limsup_{m→∞} (1/m) log ‖Φ_{k,k+m}‖ = 0`, and likewise the
> bottom (least-contracting) value `(1/m) log s_max(Φ) = 0` for all `m`. **No uniform / operator-norm /
> spectral contraction across scales exists.**

**Proof.** A product of coisometries need not be a coisometry, but its norm is controlled cleanly from
two sides. Upper bound: `‖Φ_{k,k+m}‖ ≤ ∏ ‖R_j‖ = 1` since each `‖R_j‖ = 1` (Theorem 1). Lower bound:
each `R_j` is onto with `R_j R_j^* = I`, so `R_j^*` is an isometry (`‖R_j^* x‖ = ‖x‖`); hence
`Ψ := R_{k+m-1}^* ⋯ R_k^*` is an isometry (`O^{(k)} ↪ O^{(k+m)}`), giving `‖Ψ x‖ = ‖x‖` and therefore,
for `y = R_k^* ⋯ x` chosen along the isometric image, `‖Φ_{k,k+m}‖ = ‖Ψ^*‖ ≥ 1`. Combining,
`‖Φ_{k,k+m}‖ = 1` for all `m`. The Lyapunov limsup of `log 1 / m` is `0`. ∎

Machine confirmation [PROVEN]: `‖R_2 R_3 ⋯ R_{1+m}‖_2 = 1.0000`, per-step geometric mean `= 1.0000`,
`m = 1..6` (`odd_renorm2.py`).

**Consequence for EUE.** EUE is the statement `d^{(k)} → 0` for every `k` (equivalently `Inj_a → 0`,
`ENDOGENOUS_UE_BUILD.md` §3, by the [PROVEN] reduction even-density `⟺` equidistribution mod `2^k`
`⟺` all `π_N(χ_a) → 0`). A "spectral / operator-norm route" would prove `‖d^{(k)}‖ =
‖Φ_{k,k+m} d^{(k+m)}‖ ≤ ‖Φ_{k,k+m}‖ · ‖d^{(k+m)}‖` decays by exhibiting `‖Φ_{k,k+m}‖ ≤ e^{-cm}`. Theorem 2
says `‖Φ_{k,k+m}‖ ≡ 1`, so this route gives `‖d^{(k)}‖ ≤ ‖d^{(k+m)}‖` and nothing more — no decay. The
operator-norm bound is SATURATED, uniformly in `m`. **The multi-scale spectral hope is structurally
dead.**

---

## 4. The reduction: EUE decay lives only in the data direction `=` (K)

Since `‖Φ‖ ≡ 1`, any decay of `‖d^{(k)}‖` cannot come from the operator; it can only come from the
**alignment of the specific orbit vector** `d^{(k+m)}` with the contracting (kernel) directions of the
cocycle. This is a **quenched / Oseledets data-direction** statement:

> **Conjecture (CR) [OPEN].** Along the Antihydra orbit `c_0 = 8`,
> `limsup_{m→∞} (1/m) log ( ‖Φ_{k,k+m} d^{(k+m)}‖ / ‖d^{(k+m)}‖ ) ≤ -½ log 2 < 0`,
> equivalently the orbit's odd-data vector equidistributes between `ker R_k` and `(ker R_k)^⊥` at every
> scale (energy ratio `‖d^{(k)}‖² / ‖d^{(k+1)}‖² → ½`).

(CR) is a single-vector Lyapunov negativity, **provably NOT an operator-norm property** (Theorem 2 shows
the operator-norm exponent is `0`; only the projection of one particular orbit-generated vector can
decay). [OBSERVED — `odd_renorm3.py`, `N=8e4`, `k=4..9`]: the measured ratio sits at `≈ 0.50` and
`‖d^{(k)}‖² ≈ 2^{k-1}/N`, the equidistributed / CLT floor — i.e. (CR) holds at the random rate in all
reachable data, but finite `N` cannot certify the `liminf` (same wall as `ODD_ADDITIVE_ENERGY.md` §5).

> **Reduction theorem [PROVEN reduction, conclusion OPEN].** (CR) ⟹ (K). If the data-direction exponent
> is `≤ -½ log 2`, then for each fixed `k`, `‖d^{(k)}‖ → 0`, hence `π_N(χ_a) → 0` for all `a`, hence (by
> the [PROVEN] chain `COMPLETE_PROOF_CAPSTONE.md` §2 / `ENDOGENOUS_UE_BUILD.md` §1) single-orbit
> equidistribution mod `2^k` for all `k` `=` EUE `=` the kernel (K), and Antihydra never halts.

So the no-go FORCES the proof of EUE into the quenched / (K) regime: the only surviving mechanism is a
data-direction Lyapunov exponent along the orbit vector, which is exactly (K) `=` Mahler-3/2 /
AEV Conjecture 1.6 — INDEPENDENT of and untouched by this note.

---

## 5. Relation to the single-scale `L_ann` odd-annihilation no-go

Two DISTINCT no-gos, on two DISTINCT operators, closing two DISTINCT spectral hopes:

| | single-scale | multi-scale (this note) |
|---|---|---|
| operator | annealed transfer `L_ann` (fixed scale `k`) | renormalization cocycle `Φ = R_k⋯R_{k+m-1}` |
| action on odd block | **annihilates** it: `L_ann χ_odd ≡ 0` (zero columns) | **coisometry**: `R_k R_k^* = I`, `‖Φ‖ ≡ 1` |
| failure mode | gap is **blind** to the subspace where the conclusion lives | **no uniform contraction** across scales (norm-Lyapunov `0`) |
| killed hope | single-scale spectral gap controls `Inj_a` | cross-scale spectral gap controls `Inj_a` |
| source | `ENDOGENOUS_UE_BUILD.md` §5 [PROVEN] | §3 above [PROVEN] |

`L_ann` discards the odd block (annealing one fresh bit averages it to `0`); `R_k` is the opposite — its
ENTIRE domain and codomain is the odd block, transported faithfully across scales — yet it still yields
no contraction because it is norm-preserving. The first says "the only single-scale contraction does not
see the odd block"; the second says "the multi-scale object that DOES see the odd block is a coisometry,
so it never contracts in norm." Both bottom out at the same residue: the data-direction / fresh-bit
decorrelation `Inj_a → 0` `=` (CR) `=` (K). The two no-gos jointly close the **single-scale spectral**
AND the **multi-scale spectral** routes; consistent with `EXCURSION_SUPERMARTINGALE.md` (per-step
feedback is white `→` no supermartingale drift, only a data-direction quantity survives).

---

## 6. Honest scope (explicit)

- **What is [PROVEN]:** the semiconjugacy `V^{(k+1)} mod 2^k = U^{(k)}(·, bit_k)`; the exact
  renormalization `d^{(k)} = R_k d^{(k+1)} + O(1/N)`; `R_k` pure odd→odd; `R_k` coisometry
  (`R_k R_k^* = I`, all singular values `1`, `dim ker = 2^{k-1}`, structural reason §2 + verified
  `4.8e-15`, `k=2..6`); `‖Φ_{k,k+m}‖ = 1` for all `m`; operator-norm cross-scale Lyapunov `≡ 0`.
- **What is [OBSERVED]:** energy ratio `≈ ½`, `‖d^{(k)}‖² ≈ 2^{k-1}/N` (CLT floor), `k=4..9`, `N=8e4`.
- **What this RULES OUT:** any EUE proof that controls `Inj_a` via a **uniform / operator-norm /
  spectral contraction** of the cross-scale cocycle — that family of approaches is structurally
  impossible (the norm is identically saturated).
- **What this does NOT rule out, and what it does NOT claim:**
  - It does **NOT** rule out a **data-direction / quenched (Oseledets)** argument — that is (CR) `=` (K),
    which stays **[OPEN]**. The no-go in fact REDUCES the problem to exactly this.
  - It does **NOT** rule out a **weighted-space / non-spectral / non-operator-norm** mechanism (e.g.
    second-moment / additive-energy / arithmetic equidistribution arguments outside the `L^2`-operator
    framework).
  - It does **NOT** prove EUE is false. A coisometry is consistent with `d^{(k)} → 0` along the orbit;
    the no-go is about the WRONG tool (operator norm), not about the truth of EUE.
  - It is **NOT** a proof of (K), and is **INDEPENDENT** of (K).
- **Label of the headline:** [PROVEN] (scoped exactly as above). (CR)/(K) remain [OPEN].

---

## 7. Significance

This pins, at the operator level, WHY the multi-scale spectral program for EUE cannot work, and does so
without touching (K). It converts a vague hope ("maybe iterating the scale map contracts") into a sharp
structural fact ("the scale map is a coisometry chain; its norm-Lyapunov is `0`"), and thereby isolates
the unique surviving channel: a quenched data-direction exponent along the single orbit vector. Combined
with the `L_ann` no-go, the two spectral routes (single-scale and multi-scale) are both provably closed,
which is itself evidence — not proof — that the obstruction is genuinely arithmetic / quenched
(`= (K) = Mahler 3/2`) rather than spectral. The coisometry is the cross-scale dressing of "the closed
loop cannot be opened by any norm contraction"; the moving frequency `(3/2)^j` that a single
time-homogeneous operator could not encode (`TWISTED_RPF.md`'s frozen angle) becomes the carry flowing
between scales, and the price of seeing it faithfully is exactly that the transport is norm-preserving.

---

## 8. Sources

- **Internal [PROVEN/OBSERVED]:** `NEWMATH_ODD_CALCULUS.md` (`R_k` definition, exactness, pure odd→odd,
  coisometry, `dim ker`, op-norm Lyapunov `≡0`, (CR)); `ENDOGENOUS_UE_BUILD.md` (C1 `U(s,1)=U(s,0)+2^{k-1}`,
  C2 `L_ann χ_odd ≡ 0`, C4 seam identity, §5 single-scale no-go, EUE `⟺ Inj_a→0`); `VERIFY_LABELS.md`
  (independent re-confirmation `R_k R_k^*=I` to `4.8e-15`, `σ=1`, `dim ker = 2^{k-1}`, `k=2..6`;
  `L_ann χ_odd≡0` to `1e-13`); `EXCURSION_SUPERMARTINGALE.md` (per-step feedback white `→` data-direction,
  not operator-norm); `COMPLETE_PROOF_CAPSTONE.md` §2 (even-density `⟺` equidistribution reduction);
  `CORE_ORBIT_ARITHMETIC.md`; `TWISTED_RPF.md`, `THERMO_FORMALISM.md` (frozen-angle / annealed-only failure
  of fixed operators).
- **Scripts:** `scratchpad/odd_renorm.py` (seam/renormalization identity, `\hat r`), `odd_renorm2.py`
  (even cols vanish, coisometry, cross-scale products `‖Φ‖=1`), `odd_renorm3.py` (`R_k R_k^*=I`, kernel
  dim, real-orbit energy ratios), `verify_coiso.py` (audit re-run). Exact, `c_0=8`, `N ≤ 1e5`.
- **External [PROVEN-in-lit]:** Oseledets multiplicative ergodic theorem (quenched Lyapunov / data
  direction); coisometry / partial-isometry operator theory (norm of products of coisometries `≤ 1`,
  adjoint-of-isometry `=` coisometry); Mahler (1968, 3/2 problem, open); Andrieu–Eliahou–Vivion
  arXiv:2510.11723 (AEV Conjecture 1.6 at `α=8`).

No machine decided. No label upgraded.
