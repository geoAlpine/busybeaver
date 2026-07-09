# NEWMATH solenoid build — the uniform theorem re-armed against the effective-equidistribution target (2026-07-09)

*Genuine construction attempt at the NEW_MATH_PROGRAM build-target (effective unique ergodicity for a single
specified ×(p/q) orbit on the (2,3)-solenoid), re-armed with the campaign's three new ingredients: the exact run
law `v_q(v−x)` (PAPER_MIRROR_LADDER §1), the uniform (p,q)-family, and the measured run-depth whiteness
(FREQUENCY_AXIS_PROBE_2026-07-08). STRICT SOUNDNESS: every claim `[PROVEN]` / `[CONSTRUCTED-partial]` /
`[ASSESSED]` / `[OPEN]`. Does NOT prove (K); does NOT upgrade any label. Cites, does not re-run, the logged
NO-GOs (EXCURSION_SYNTHESIS, EUE_COISOMETRY, AIU_NEUTRAL, O4_GROWING_BUDGET, FREQUENCY_AXIS_PROBE). Numerics
verified `scratchpad/reload_verify.py`, interpreter `/Users/aokiyousuke/quantum-ecc/.venv/bin/python`, exact
big-int, orbit to n=2·10⁵. NOT committed.*

---

## 0. What was built

Three `[CONSTRUCTED-partial]` results, one per re-arming ingredient, each a **sharper reduction than the existing
no-go** — and each landing, provably, on the same wall. Two of them push a publishable partial one step:

1. **The exact reload map** (§1, Ingredient 1): the run-depth process is not merely "white with an i.i.d.-geometric
   marginal" — it is the *exact deterministic recursion* `K_{i+1} = v_q(p^{K_i}·u_i ∓ 1)` on the q-adic unit `u_i`
   (the higher-bit residual). This **pins the conditional law** but shows the free parameter is the alignment of
   `u_i` with `p^{∓K_i}` in `ℤ_q^×`, exactly the multiplicative-order arithmetic the heavy-tail adversary is free
   to violate. Sharpens EXCURSION_SYNTHESIS "adversary is drift-indistinguishable" to "adversary = a specific
   `ℤ_q^×`-misalignment, realizable in the seed ensemble."
2. **The shared-solenoid deformation** (§2, Ingredient 2): a **correction** to the "mirror is a swap ⇒
   arithmetically disjoint" reading. The `{2,3}`-smooth cryptids — Antihydra ×3/2, o4 ×4/3, o15/o18 ×8/3, and the
   powers ×(3/2)ᵏ — are **all lattice elements `Φ(a,b)` of ONE rank-2 host on ONE (2,3)-solenoid**; only Space
   Needle ×5/2 is genuinely disjoint (on the (2,3,5)-solenoid). This *is* a genuine deformation, but it **cannot
   transfer an effective bound**, for two proven reasons (§2.2). **Pushes AIU_NEUTRAL one step:** the
   neutral-direction obstruction is **deformation-uniform** across the whole family.
3. **Whiteness ⟂ tail** (§3, Ingredient 3): the measured whiteness **cannot** be bootstrapped to a one-sided
   even-density bound, because whiteness and the fatal tail are **orthogonal** — the i.i.d. heavy-tail adversary is
   *simultaneously maximally white and `E[K²]=∞`. Sharpens the EUE coisometry no-go: the only a-priori facts the
   coisometry yields are norm-non-increase (wrong direction) and energy conservation, and any a-priori bound on the
   marginal `‖d^{(k)}‖²` IS (K).

---

## 1. Ingredient 1 — the exact reload map: the arithmetic *does* pin the conditional law, and that is exactly why it cannot pin the tail

**Setup (from PAPER_MIRROR_LADDER §1, ANTIHYDRA_LEDGER_UNIFICATION §1) `[PROVEN]`.** On each branch the cryptid
map is affine `b(v)=(pv+e)/q` with integer fixed point `x=−e/(p−q)`; the maximal same-branch run from entry `v`
has length `v_q(v−x)`, and `b^{K}(v)−x=(p/q)^{K}(v−x)`. For Antihydra (p,q)=(2,3)→ wait, (p,q)=(3,2): even branch
`x=0`, odd branch `x=1`, run `= v_2(v)`, resp. `v_2(v−1)`.

**Lemma 1 (exact reload recursion) `[CONSTRUCTED-partial, verified 0 mismatch / 50034 runs]`.**
*Write the maximal even-run entry as `v = 2^{K_e}u`, `u = oddpart(v)` odd. Draining the even branch `K_e` steps
gives the exact exit `3^{K_e}u` (odd), which is the next (odd-branch) entry; hence*
> `K_o = v_2( 3^{K_e}·u − 1 )`,  and dually  `K_e' = v_2( 3^{K_o}·u' + 1 )`, `u' = oddpart(v_o − 1)`.

*Proof.* On the even branch `c↦3c/2`; from `c=2^{K_e}u`, after `j` steps `c=3^{j}2^{K_e−j}u`, so the exit at
`j=K_e` is `3^{K_e}u`, odd, and its odd-run depth is `v_2(\text{exit}−x_\text{odd})=v_2(3^{K_e}u−1)`. The odd
case is identical with `x_\text{odd}=1` and a `+1`. ∎ (Verified on the real orbit to `n=2·10⁵`:
`even→odd 0/50034`, `odd→even 0/50034` up to the truncated final run; `scratchpad/reload_verify.py`.)

**What this builds, and what it does not `[ASSESSED]`.** The reload map is an *exact* handle on the excursion
process that EXCURSION_SYNTHESIS treated abstractly: the next depth is **not free** — it is the 2-adic valuation of
`3^{K}u∓1`, i.e. it measures how deeply the unit `u` aligns with `3^{∓K}` in `ℤ_2^×`. Because `3` generates a
closed **index-2** subgroup of `ℤ_2^×` (`ord(3 \bmod 2^m)=2^{m-2}`), the map `(K,u)↦K_\text{next}` is a genuine
skew-product on `ℤ_2^×` with an explicit arithmetic cocycle. **This pins the CONDITIONAL law** (given `u`
equidistributed on `ℤ_2^×`, `K_\text{next}` is exactly geometric(½)). But `u_i` is the *higher-bit residual of the
orbit's own value* — its equidistribution on `ℤ_2^×` **is** single-orbit equidistribution = (K). The heavy-tail
adversary of EXCURSION_SYNTHESIS §1 is precisely a `ℤ_2^×`-trajectory whose `u_i` cluster near `3^{∓K}` often
enough to fatten the tail; nothing proven forbids it (the fixed-point seed `v=1` realizes `K=∞`, and the
No-Structure specification bijection realizes every finite alignment pattern). **Verdict: the exact fixed-point
structure pins the conditional law but leaves the marginal tail free — it converts "abstract adversary" into "a
specific `ℤ_q^×` misalignment," a sharper statement of the same (K)-wall, not past it.** `[CONSTRUCTED-partial;
lands on the EXCURSION_SYNTHESIS wall]`

---

## 2. Ingredient 2 — the (p,q)-family is a genuine deformation on ONE solenoid; it still cannot transfer a bound

### 2.1 The shared host `[PROVEN]`
`3/2`, `4/3=2²·3⁻¹`, `8/3=2³·3⁻¹`, `9/4=(3/2)²` are all `{2,3}`-smooth units of `ℤ[1/6]ˣ`, hence **all descend to
automorphisms of the SAME (2,3)-solenoid** `X=(ℝ×ℚ₂×ℚ₃)/ℤ[1/6]`, and are **lattice elements of the one rank-2
host** `Φ:ℤ²→Aut(X)`, `Φ(a,b)=×(2^a3^b)`:
> **Antihydra `=Φ(−1,1)`, o4 `=Φ(2,−1)`, o15/o18 `=Φ(3,−1)`, A²`=Φ(−2,2)`** — while **Space Needle ×5/2 is NOT
> `{2,3}`-smooth**, so it lives on the disjoint (2,3,5)-solenoid. `[PROVEN — product formula, verified
> `reload_verify.py`]`

This **corrects** the prior "mirror = (p,q)-swap ⇒ arithmetically disjoint" reading (FREQUENCY_AXIS_PROBE §3,
O4_RUN_STRUCTURE §3): for the `{2,3}`-subfamily the orbits are *not* on disjoint spaces — they are single-element
orbits of *different lattice elements of one commuting `ℤ²` action*. The "swap" is precisely that the deformation
`Φ(2,−1)↝Φ(−1,1)` **interchanges the role of the two finite places**: the depth/entropy place is the *expanding*
p-adic place, `ℚ₃` for o4 (`|4/3|₃=3`) and `ℚ₂` for Antihydra (`|3/2|₂=2`). So the family is one solenoid whose
places are permuted/reweighted as `(a,b)` moves — a bona fide deformation with a critical locus (the ρ/β=1 curve;
ANTIHYDRA_LEDGER_UNIFICATION §2: o4 at 0.087, o3 at 0.79, Antihydra at 1.17).

### 2.2 Why the deformation cannot transfer the effective bound `[CONSTRUCTED-partial]`

**(Obstruction I — the target does not deform.)** A deformation/continuity argument would need the object being
bounded to vary continuously along the path `(a,b)_t` from `Φ(2,−1)` to `Φ(−1,1)`. The **linear host automorphism**
does deform continuously (its Lyapunov data `χ_∞,χ_2,χ_3` are linear in `(a,b)`). But the effective-equidistribution
target is a property of the **nonlinear floor map** `⌊(p/q)v⌋+c(v)` — a *different* map at each lattice point, with
its own correction/branch structure, and **no floor dynamics at non-lattice `t`**. The quenched single-orbit limit
`μ_{g}` is orbit-specific (KB limit of the *g*-orbit), not a continuous section of a bundle over `(a,b)`. So
continuity in `(a,b)` relates the *linear* data, which is not what carries the bound; the bound lives on the
non-deforming nonlinear layer. `[ASSESSED — the precise reason continuity has no traction]`

**(Obstruction II — the neutral obstruction is deformation-uniform.) `[CONSTRUCTED-partial — one-step extension of
AIU_NEUTRAL]`** For *any* element `g=Φ(a,b)`, the quenched limit `μ_g` is only `g`-invariant (rank 1). Upgrading to
Haar needs invariance under a **second, transverse** host generator (Rudolph–Johnson). But each generator is
**neutral on exactly one place**: `M₂=×2` has `χ₃(1,0)=log|2|₃=0` (neutral on `ℚ₃`); `M₃=×3` has
`χ₂(0,1)=log|3|₂=0` (neutral on `ℚ₂`). Hence for every `g`, the surplus invariance needed to complete rigidity sits
on a **zero-Lyapunov coarse direction of the transverse generator**, and the AIU_NEUTRAL Theorem A applies verbatim
(the high-entropy engine's output is keyed to a nonzero weight, `0·γ=0` on the neutral axis). **Therefore no
subcritical element of the family is a place where the standard rigidity method reaches AIU — the neutral-direction
obstruction is invariant under the deformation.** This extends AIU_NEUTRAL from "the Antihydra element ×3/2" to
"every `{2,3}`-smooth cryptid element, uniformly." `[CONSTRUCTED-partial]`

**Consequence for the "prove the easy end, deform" plan.** o4's subcriticality (ρ/β=0.087, summable annealed ruin,
BC-I convergent class) is genuine — but it is easier **only on the ledger / single-run axis** (single-run fatality
`[PROVEN]` excluded, O4_RUN_STRUCTURE §2). On the **ENT/AIU/frequency axis** o4 is exactly as (K)-hard
(O4_GROWING_BUDGET §2–5: threshold-uniform no-gos, density-burst adversary survives; FREQUENCY_AXIS_PROBE §3:
independently (K)-hard per orbit). The deformation would need to transfer a bound on the *frequency/entropy* axis,
which is the axis where the two ends coincide in difficulty — so there is **no easy end to deform from**. The margin
ladder orders the *ask*, not the *wall*. `[ASSESSED]`

**Precise missing ingredient (sharper than the no-go):** a bound that varies *monotonically along the `Φ(a,b)`
deformation on the frequency axis* and is provable at one lattice point. None exists because (I) the bounded object
is on the non-deforming nonlinear layer and (II) the completion step (AIU) is neutral-blind uniformly along the
path.

---

## 3. Ingredient 3 — measured whiteness is orthogonal to the fatal tail (cannot bootstrap a one-sided bound)

**The bootstrap hope:** measured whiteness (FREQUENCY_AXIS_PROBE §0: autocorr ≤0.008, conditional-entropy drop
≤0.3%) + exact arithmetic ⟹ an a-priori effective mixing/even-density bound.

**Lemma 3 (whiteness ⟂ tail) `[CONSTRUCTED-partial, demonstrated]`.** *Even-density `≥1/3` is `mean D≥3/2`, and by
Kac even-density `= E[\text{even-run}]/E[R]`; excluding the halting atom needs `E[K²]<∞`
(EXCURSION_SYNTHESIS §0). Whiteness constrains the **joint law given the marginals** (decorrelation), while the
obstruction is the **marginal second moment `E[K²]`. These are independent:** an i.i.d. sequence is perfectly
white for every marginal, including heavy-tailed marginals with `E[K²]=∞`.* Demonstration
(`reload_verify.py`): an i.i.d. `K` with `P(K≥k)∼1/k` (so `E[K]<∞`, `E[K²]=∞`) has autocorr(1,2) `= −0.0001` —
**maximally white, yet tail-fatal**, `max K = 279{,}598` on `2·10⁵` draws. ∎

So the measured whiteness is a property the fatal adversary **shares**; it cannot separate the real orbit from the
halting adversary. Whiteness lives on the correlation axis; the open content lives entirely on the orthogonal
tail axis. `[CONSTRUCTED-partial]`

**Can the coisometry supply a *weaker* a-priori whiteness that suffices for a one-sided bound? `[ASSESSED — no]`**
EUE_COISOMETRY gives, a-priori (not measured): (i) `‖R_k‖=1` ⟹ `‖d^{(k)}‖ ≤ ‖d^{(k+1)}‖` (odd-energy
non-increasing *down* scales) — a-priori and one-sided, but the **wrong direction**: it says nothing about the
`N→∞` limit at fixed `k`; (ii) `R_k^*` isometric ⟹ energy *conserved* under the lift, only redistributed into the
growing kernel `dim ker R_k = 2^{k−1}`. A one-sided even-density bound needs an a-priori **upper** bound
`‖d^{(k)}‖² ≲ 2^{k−1}/N` (the equidistributed floor); the coisometry gives the saturated identity `‖Φ‖≡1`, and an
a-priori upper bound on the marginal `‖d^{(k)}‖²` **is** single-orbit equidistribution mod `2^k` = (K)
(EUE_COISOMETRY §4, Reduction). So the coisometry's a-priori content is precisely orthogonal to (norm
non-increase) or equivalent to (energy upper bound) the target — no weaker sufficient whiteness exists.
`[ASSESSED — lands on the EUE_COISOMETRY wall]`

---

## 4. The two publishable partials, one step further

- **AIU_NEUTRAL_OBSTRUCTION_THEOREM — pushed (§2.2, Obstruction II).** Scope upgraded from *one element* (×3/2) to
  the *whole `{2,3}`-smooth cryptid family* `{Φ(a,b)}` on the shared solenoid: the high-entropy method is
  neutral-blind **uniformly along the deformation**, because every element's Haar-completion needs a zero-weight
  surplus direction of a transverse generator. This is a genuine strengthening of the theorem's reach and a clean
  new statement ("neutral-blindness is deformation-invariant on the (2,3)-host"). `[CONSTRUCTED-partial]`
- **ENT_LY_COLLAPSE_THEOREM — mildly extended (§2.1).** The affine L–Y collapse `h_{μ_g}(g)=Σ_{v:λ_v(g)>0}λ_v(g)γ_v`
  is **element-uniform** across the family (same frozen place-exponents, permuted by `(a,b)`); ENT is one dimension
  number `γ>0` for each cryptid, and the ENT⟂AIU orthogonality holds per element. No lower bound on `γ` at any
  element (still (K)-hard at both ends). `[ASSESSED]`

---

## 5. Honest verdict

All three re-armed angles **land on the same wall**, but each is now a **sharper reduction** than the logged no-go:
(1) the exact reload map converts "abstract heavy-tail adversary" into "a specific `ℤ_q^×` misalignment governed by
`ord(p \bmod q^m)`"; (2) the family is a **genuine one-solenoid deformation** (correcting "disjoint"), yet transfers
nothing because the target is on the non-deforming nonlinear layer and the completion step is neutral-blind
uniformly; (3) whiteness is provably **orthogonal** to the fatal `E[K²]` tail. The deformation-argument viability is
**negative but informative**: the `{2,3}`-host is real, the criticality ratio is a genuine continuous function on
it, but the quenched single-orbit bound does not deform and the easy (subcritical) end is easy only off the
frequency/entropy axis. The precise remaining gap is unchanged in species and now stated at its sharpest: **an
a-priori bound on the marginal second moment `E[K²]` / the marginal odd-energy `‖d^{(k)}‖²` of the specific orbit —
equivalently `ℤ_q^×`-equidistribution of the reload units `u_i` — which every constructed handle (conditional law,
deformation, whiteness) leaves free.** That is (K) = Mahler 3/2 / AEV Conj 1.6 = one-sided Normality on base p/q.

Numerics reproduce: `scratchpad/reload_verify.py` (shared-host membership; reload map 0 mismatch / 50034;
whiteness-blind-to-tail demonstration).

No machine decided. No label upgraded.
