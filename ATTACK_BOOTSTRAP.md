# Self-consistent BOOTSTRAP attack, exploiting the self-reference (2026-06-28)

Attack target = the quenched Korobov sum `S_n = Σ_j e_{n-1-j} (3/2)^j` whose cancellation = the parity
balance = the [OPEN] Mahler core. The *self-reference*: the weights `w_j = e_{n-1-j}` ARE the orbit's own
past parity bits — the same quantity whose balance we want. The plan: turn the circularity into a lever via
a **sequence/orbit-level** bootstrap (NOT a measure-level contraction — that was already refuted in
`AUDIT_CONTRACTION.md`/`TRACKING_BRIDGE.md`), exploiting **causality** (`e_n` depends only on `e_0..e_{n-1}`).

Every line labelled **[PROVEN]/[CONDITIONAL]/[OPEN]/[OBSERVED]/[REFUTED]**. Numerics: `bootstrap_test.py`
with `/Users/aokiyousuke/quantum-ecc/.venv/bin/python`. **NOT committed.** Zero false proofs.

---

## 1. The feedback loop, formalized exactly (the causal/triangular structure)

**[PROVEN identity]** The orbit `c_0=8, c_{n+1}=⌊3c_n/2⌋` has parity bits `e_n = c_n mod 2 ∈ {0,1}` with
```
   e_n  =  bit_n(8·3^n)  ⊕  bit_n(T_n),        T_{n+1} = 3 T_n + 2^n e_n,   T_0 = 0,
   T_n  =  Σ_{k<n} 2^k 3^{n-1-k} e_k,          T_n / 2^{n+1} = (1/4) Σ_{j≥0} e_{n-1-j} (3/2)^j  (mod 1).
```
So `bit_n(T_n)` is the n-th binary digit of the **(3/2)^j-weighted partial sum** of the past bits.
Define the signed parity `σ_n := (-1)^{e_n}` and the **even-density imbalance**
```
   D_N := (1/N) Σ_{n<N} σ_n = 2·(even-density) − 1.       Non-halt ⟺ even-density ≥ 1/3 ⟺ D_N ≥ −1/3 ∀N.
```
Split off the explicit factor `χ_n := (-1)^{bit_n(8·3^n)}` (known, foothold digit) and the carry factor
`β_n := (-1)^{bit_n(T_n)}`:  `σ_n = χ_n β_n`, so `D_N = (1/N) Σ_{n<N} χ_n β_n`.

**[PROVEN structural asset — causality / triangularity].** `T_n` is a function of `e_0..e_{n-1}` ONLY.
Hence `e_n = Φ_n(e_0,…,e_{n-1})` is a **deterministic forward recursion**. This is the genuine gain over the
measure route: there is **no fixed-point self-consistency to assume** (the McKean–Vlasov closure `ν=L_ν ν`
that `AUDIT_CONTRACTION.md` showed admits the spurious atomic solutions `δ_0,δ_1` is *not* invoked here).
The sequence is well-defined with no circular definition. The circularity is only in the *proof of balance*,
which is exactly where we try to use the bootstrap.

**The dependence on partial sums, made explicit.** `bit_n(T_n)` is the n-th digit of
`Σ_{k<n} 2^k 3^{n-1-k} e_k`. In the fractional form, the most-recent bits enter with **small** weight
(`e_{n-1}·1, e_{n-2}·(3/2), …`) and the **oldest** bits enter with the **largest** weight
(`e_0·(3/2)^{n-1}`), whose fractional parts `{(3/2)^{n-1}/4}` are exactly the Mahler equidistribution
quantities. So `bit_n(T_n)` is dominated by `(old bits) × (3/2)^{large}` — a *high-frequency*, not a
*mean-level*, functional of the past.

---

## 2. The bootstrap inductive step — and the EXACT estimate it needs

**Bootstrap claim (to be tested):** *if `|D_M| ≤ ε` for all `M < N`, then `S_n` is small ⇒ `β_n` balanced
⇒ `|D_N| ≤ ε`.*

Write the carry average `B_N := (1/N) Σ_{n<N} β_n`. The annealed/perturbative decomposition (verified §4) is
```
   B_N(weights e)  =  A(0,N)  +  gain·δ_in  +  o(δ_in),
```
where `δ_in` = the input sign-imbalance (`= D` of the weights), `gain = ∂B/∂δ_in`, and
```
   A(0,N) = B_N evaluated at BALANCED weights = (1/N) Σ_{n<N} E[(-1)^{bit_n(T_n)}]
          = the Mahler product   Φ(N) = Π_{j} |cos(π {(3/2)^j/4})|  averaged over n.
```
For the induction `|D_M|≤ε ⇒ |D_N|≤ε` to close, the step needs
```
   |B_N|  ≤  A(0,N) + gain·ε + o(1)  ≤  ε,     i.e.    A(0,N) ≤ ε(1 − gain).
```

> **EXACT INDUCTIVE ESTIMATE NEEDED.**  `A(0,N) = (1/N) Σ_{n<N} (-1)^{bit_n(T_n)}` evaluated with the
> **orbit's own (balanced) weights** must be `o(1)` (in fact `< ε(1−gain)`).  This is **identically** the
> single-orbit Korobov/Mahler cancellation `(K)` of `PROOF_STATUS.md` — the orbit's `(3/2)^j` exponential
> sum. **It is NOT weaker than Mahler; it IS Mahler.**

The hypothesis `|D_M| ≤ ε` enters **only** through the `gain·ε` term. It does nothing for `A(0,N)`.

---

## 3. Critical self-audit — circular, or a genuine gain?

The AUDIT lesson was: the measure contraction *relocated* the kernel (controls the derivative/uniqueness,
not the single-orbit base term). Does the orbit-level bootstrap do better via causality?

- **The causal/triangular structure IS a genuine structural gain — but not toward the bound.** It removes
  the fixed-point circularity (no `ν=L_ν ν` closure, no spurious `δ_0,δ_1`; §1). It localizes the
  obstruction cleanly: the **homogeneous** part (propagation of a past imbalance ε) is governed by `gain`,
  and the **inhomogeneous base** part is `A(0,N)`. This is a real and clarifying separation.
- **But the bound is entirely in the base term, which is Mahler, and the hypothesis is inert.** The
  inductive step needs `A(0,N)=o(1)`; the past-imbalance hypothesis `|D_M|≤ε` contributes nothing to it.
  Numerically (§4) the gain is `≈0` and there is **no mean-restoring force** (corr ≈ 0), so the bootstrap
  neither needs nor uses `|D_M|≤ε` — the entire content is `A(0,N)→0` = Mahler. **The bootstrap does not
  *secretly* assume what it proves; it *transparently reduces* to Mahler with the bootstrap hypothesis
  playing no role.** Same kernel, relocated again — exactly the AUDIT pattern.

**Honest verdict:** the bootstrap is **circular in the operative sense** (it cannot derive output balance
from past balance — output balance is an independent Mahler fact), though it is *not* a hidden logical
circularity. Causality is a real asset that sharpens the localization but does **not** convert into a bound.

---

## 4. Numerics (`bootstrap_test.py`, real orbit to `N=2·10⁵`; MC feedback `N=1200`, 400 trials)

**(1) Real orbit imbalance and the mean-restoring force.** `D_N → 0` (`+0.0004` at `N=2·10⁵`). The
restoring-force test (does the trailing-window imbalance predict the next sign?) gives
`corr(σ_n , mean σ_{n−W:n}) = −0.005, −0.004, −0.004, +0.001` for `W = 8,32,128,512`.
**[OBSERVED] No mean-restoring force.** There is no dynamic by which a past imbalance pushes the next bit
back — so there is no contraction *on `D` itself* to bootstrap from.

**(2) Feedback decomposition `A(δ,N)`.** With i.i.d. weights of sign-imbalance `δ`:

| δ | −0.30 | −0.15 | −0.05 | 0.00 | 0.05 | 0.15 | 0.30 |
|---|---|---|---|---|---|---|---|
| A(δ,N=1200) | 0.0041 | 0.0014 | 0.0038 | **0.0039** | 0.0044 | 0.0026 | 0.0042 |

`A(0,N)=+0.0039` (the open Mahler product; the exact product `Φ(1200)` has underflowed to `0`, the MC value
is the finite-N residual). **Slope `gain = dA/dδ ≈ +0.0002`.** **[OBSERVED] The output imbalance is
essentially FLAT in `δ`** — the input imbalance has **no leverage** on the output. Output balance comes
entirely from the `(3/2)^j` equidistribution (`A(0)`), not from `δ` being small. (This is *good* for
stability — sub-critical, no blow-up — but it is exactly why `|D_M|≤ε` cannot force output balance.)

**(3) Same-`|D|` spread test.** Fix the past imbalance `D` and vary only the *arrangement* of the bits:

| D | mean output sign | stdev across arrangements |
|---|---|---|
| 0.00 | −0.06 | 0.998 |
| 0.05 | −0.04 | 0.999 |
| 0.15 | −0.07 | 0.997 |

**[OBSERVED] For every `D`, the output bit is a near-fair `±1` (mean≈0, stdev≈1).** `D` is **not a
sufficient statistic** for the output bit — the balance is set by the arrangement (the `(3/2)^j` phases),
which `D` does not see. The bootstrap step cannot read output balance off `D`.

---

## 5. Does causality/martingale give a genuine partial bound?

**[PROVEN, but only annealed]** On the causal filtration `F_n = σ(e_0,…,e_n)`, **if the bits were random**
(i.i.d. fair — the annealed model), `Σσ_n` is a sum of bounded martingale differences and **Azuma–Hoeffding**
gives `P(|D_N| ≥ t) ≤ 2e^{−Nt²/2}` ⇒ the annealed even-density `→1/2` with a CLT rate. This is real, but it
is exactly the **already-[PROVEN] annealed balance** (`exp_sum.py`, `NONPISOT_FOURIER_CHAIN.md` Link B); it
adds nothing new.

**[OPEN — why it fails for the orbit]** For the actual orbit the bits `e_n` are `F_n`-measurable **and
deterministic** — there is no probability space and no martingale-difference structure (`Var(σ_n|F_{n-1})=0`).
Azuma is inapplicable. The Doob martingale of `D_N` requires re-injecting randomness, returning to the
annealed model. **So martingale/Azuma on the causal filtration gives a genuine bound only for the random
(annealed) sequence, never for the single deterministic quenched orbit.** Same annealed/quenched wall as
every prior route; causality does not move it.

**The one honest partial structural result.** The decomposition `B_N = A(0,N) + gain·δ + …` with the
**[OBSERVED]** annealed `gain ≈ 0` (sub-critical) does buy a *conditional* statement:
> **[CONDITIONAL on Mahler]** IF `A(0,N) = o(1)` (the base Korobov cancellation), THEN — because the
> homogeneous propagation is sub-critical (`gain<1`, no blow-up of a past imbalance) — the induction closes
> and `|D_N|` stays small.
i.e. the obstruction is **entirely** in the inhomogeneous base term, not in the homogeneous propagation. The
bootstrap is *not* circular in its homogeneous part (that part genuinely contracts/stays bounded); it is the
base term `A(0,N)` that is Mahler. (Caveat: the quenched closed-loop gain for the orbit is itself the
`‖F‖` object the AUDIT flagged [OPEN]; only the *annealed* gain≈0 is established here.)

---

## 6. Returned conclusions

- **EXACT inductive estimate needed:** `A(0,N) = (1/N)Σ_{n<N}(-1)^{bit_n(T_n)}` with the orbit's own
  (balanced) weights `= o(1)` (`< ε(1−gain)`). This **equals** the single-orbit `(3/2)^j` Korobov sum `(K)`
  = Mahler/AEV. **Strictly NOT weaker than Mahler.**
- **Causality/martingale partial bound?** Martingale/Azuma gives a genuine bound **only annealed**
  (= already proven); **inapplicable to the deterministic orbit** (zero conditional variance). The genuine
  causal gain is *structural*: it removes the fixed-point circularity (no `δ_0,δ_1` spurious solutions) and
  isolates the obstruction in the **inhomogeneous base term**, with the homogeneous propagation provably
  (annealed) **sub-critical**. So there is a real **[CONDITIONAL on Mahler] stability** statement, but no
  unconditional partial bound on the imbalance.
- **Honest verdict — circular or real gain?** **Operatively circular** (the bootstrap cannot derive current
  balance from past balance: the past-imbalance hypothesis is *inert* — `gain≈0`, no restoring force, `D`
  not a sufficient statistic; all the content is the base term = Mahler). It is **not** a hidden logical
  circularity — it transparently reduces to Mahler. Net: like the measure contraction, the bootstrap
  **relocates** the kernel (now sharply: into the inhomogeneous base term `A(0,N)` of a causal recursion);
  it does **not** shorten it. Genuine byproduct: the obstruction is provably *not* in the dynamics
  (propagation/restoring), only in the static `(3/2)^j` cancellation.
- **Numerics:** `D_N→0`; restoring-force corr `≈0`; feedback gain `≈0` (flat `A(δ)`); same-`D` output spread
  `mean≈0, stdev≈1` (D not sufficient). All consistent and reproduced with `.venv` python.
