# Skeptic audit — is the twisted-RPF operator `L_t` a genuine new handle, or Mahler relocated? (2026-06-28)

Adversarial audit of the attack-(d) proposal (`SESSION_2026-06-28_QUENCHED_ATTACK.md` §d, line 51):
> "core = twisted Ruelle–Perron–Frobenius operator `L_t` (Antihydra parity dynamics twisted by the
> character `e((3/2)^k/4)`); spectral gap `ρ(L_t)<1 ⇔ quenched cancellation ⇔ ‖F‖<1 ⇔ Mahler`."

Every line labelled **[PROVEN] / [OBSERVED] / [OPEN]**. Zero false proofs. Numerics reproduced with
`/Users/aokiyousuke/quantum-ecc/.venv/bin/python` (scratchpad `quenched_audit.py`). **NOT committed.**

## 0. One-line verdict
**`L_t` is the same wall, relocated — not a genuine new reduction of the single-orbit problem.** It is a
faithful and useful *re-encoding* (it ports the core into thermodynamic-formalism language), but it does
not shorten the open core for two independent, decisive reasons: **(i)** the object is a `(3/2)^j`-**weighted**
Birkhoff sum, whose growing weights turn the would-be transfer operator into the **×(3/2) circle map**, which
has **no spectral gap in any classical Banach space** (that gap *is* Mahler); and **(ii)** a spectral gap, if
it existed, is intrinsically an **equilibrium / a.e.** statement and **cannot select the specific orbit
`c₀=8`** (the Tao-2019 a.e.→named gap, already documented in `COCYCLE_ERGODICITY.md §3`).

---

## 1. Does the quenched twisted operator close on a finite state space? — **[PROVEN: no, not while retaining the twist]**

Two sub-questions; the honest answers differ from the naïve worry.

### 1a. The *scenery* closes on a compact (not finite) space — self-generation is **not** infinite memory.
The quenched weights are `e_j = r_j = parity(c_j)`, `c_{n+1}=⌊3c_n/2⌋`. This is **not** an infinite-memory
function of an unbounded history: `e_j = π(T^j c₀)` where `T(c)=(3c−(c mod 2))/2` is a **continuous map on the
compact 2-adic group `ℤ₂`** and `π(c)=c mod 2` is the parity coordinate. So `(parity scenery)` is a
**topological factor of the compact system `(ℤ₂, T)`**. `T` is the ×(3/2) map in 2-adic guise: positive
entropy `log 2`, Haar = SRB. Its **un-twisted** transfer operator does have a spectral gap (Bernoulli-type
mixing) → **a.e. exponential decay of correlations**. So the worry "self-generation needs infinite memory"
is **false**: the state space is compact and closes. *This is exactly why a transfer operator is even on the
table — and exactly why it cannot select a single orbit (§2).*

### 1b. The *twist* does **not** close — it has growing frequency `(3/2)^j`. **[PROVEN, this is the obstruction]**
The carry/parity statistic is **not** a Birkhoff sum `Σ_j f(T^j x)` of a *fixed* observable. It is the
`(3/2)^j`-**weighted** sum (identity, `exp_sum.py`):
`T_n/2^{n+1} = (1/4) Σ_j e_{n−1−j}(3/2)^j`, equivalently the phase recursion
`φ_{n+1} = (3/2)φ_n + e_n/4  (mod 1)`.
The weight `(3/2)^j` **grows**. A transfer operator with a spectral gap produces, by construction,
*fixed-observable* (geometrically *decaying*-memory) Birkhoff sums. To absorb the growing weight you must
adjoin the phase coordinate `φ` and iterate the **`×(3/2)` map on the circle** — and the `×(3/2)` map is
**not an expanding self-covering**, so its transfer operator has **no spectral gap on any classical (BV /
Hölder / smooth) Banach space**. The "spectral gap" the proposal needs is therefore the spectral gap of the
`×(3/2)` map = **Mahler's `(3/2)^n mod 1` problem itself.**

**Consequence (the fork). A finite/compact twisted operator can be either, never both:**
- **Finite & gap-having** (truncate to `s = c mod 2^k`): closes to the finite Markov matrix `L_op(k)`, but
  truncation discards the `j > k` phase bits that *carry* the `(3/2)^j` growth → its stationary measure is
  **Haar exactly** and it describes the **equilibrium/annealed** object, by construction (numerics (C),(D)).
- **Twist-faithful** (retain all `(3/2)^j` bits): the operator is the `×(3/2)` map, **no spectral gap in any
  classical space** = Mahler.

So **the quenched twisted operator does not close on a finite gap-having state space.** [PROVEN]

---

## 2. Does `ρ(L_t)<1` give decay for the SPECIFIC orbit `c₀=8`, or only the equilibrium-generic point? — **[PROVEN: equilibrium-generic only]**

A spectral gap of a transfer operator yields exponential decay of correlations / a CLT **for the equilibrium
(SRB = Haar) measure**, i.e. for **Haar-a.e.** point and for **distributional/ensemble** averages. It does
**not** name a single orbit:
- `c₀=8` is a single point = **Haar-null**. No mechanism in transfer-operator / thermodynamic-formalism
  theory upgrades an a.e. statement to a **prescribed computable** point. This is verbatim the
  `COCYCLE_ERGODICITY.md §3` "a.e.→specific" gap = **Tao 2019** (controls the same p-adic Gibbs–Markov
  statistic for a density-1 set of seeds, never one named seed).
- **[OBSERVED] (C):** the finite operator `L_op(k)` has stationary measure = Haar **exactly**
  (`‖uL−u‖₁ = 0` to machine zero, k=6,8,10) and `|2nd eigenvalue|` = 0.0017/0.0080/0.0211 — *that* is the
  equilibrium mixing rate. Eight seeds {8,12,20,100,1000,31,7,999983} all give even-density 0.4978–0.5009 at
  N=2·10⁵: **the operator is blind to `c₀=8`; it predicts 1/2 for the whole ensemble.**

So `ρ(L_t)<1` ⟹ decay **for the equilibrium-measure-generic point**, *not* for `c₀=8`. The gap "`ρ<1` ⇒
single-orbit cancellation" silently re-imports the a.e.→named selection — i.e. **the wall.** [PROVEN]

---

## 3. Numerics: annealed (ensemble) vs quenched (single-orbit) decay of the SAME sum — **[OBSERVED]**

The two are **different averages with different rates**; the operator buys the first, the open core is the
second. (scratchpad `quenched_audit.py`.)

| object | what it is | rate (measured) | status |
|---|---|---|---|
| **(A) Annealed ENSEMBLE** `Φ(N)=Π_{j<N}|cos(π{(3/2)^j/4})| = |E_iid[e(S_N/4)]|` | ensemble avg over i.i.d. weights, one large N | `(−log₂Φ)/N → ~1.0`, i.e. **`Φ(N) ~ 2^{−N}` exponential** | `Φ→0` **[PROVEN]** (Rajchman/non-Pisot); the **exponential rate** = `⟨log\|cos\|⟩=−log2` of *equidistributed* phases = **[OPEN]=Mahler** |
| **(B) Quenched TIME avg** `A(N)=(1/N)\|Σ_{n<N}(−1)^{bit_n(T_n)}\|`, weights = orbit's own parities | time avg over the single orbit `c₀=8` | `\|A(N)\|·√N ~ O(1)` (1.01, 1.64, 1.41, …, 1.84 at N=10³…2·10⁵): **`~N^{−1/2}`** | **[OBSERVED]**; vdC proves only `O(1)` (trivial) for the named orbit |
| **(B′) i.i.d. surrogate TIME avg** | same time avg, random scenery | `\|A\|·√N ~ O(1)`, **statistically indistinguishable from the orbit** | confirms the orbit is **generic**, but only **[OBSERVED]** |

**Key reading.**
1. The annealed `Φ(N)` is an **ensemble** average (one big `N`); its single value has the operator's
   exponential rate. The quenched single sum `e(S_n^{orbit}/4)` has **modulus 1** — decay can appear *only*
   in the **time** average `A(N)`. So "are annealed and quenched the same rate?" is **mis-posed**: they are
   different kinds of average. The operator/Rajchman delivers the ensemble exponential; the open object is the
   single-orbit time average.
2. Even the **annealed exponential rate `2^{−N}` is already Mahler-strength** — it equals the log-average of
   *equidistributed* `(3/2)^j` phases. Only the qualitative `Φ→0` (no rate) is free. So the operator does not
   even buy a *free* exponential annealed rate; it buys a free `→0`.
3. The orbit's time-average is `N^{−1/2}` and **indistinguishable from random** — favourable, but **[OBSERVED]**.
   The provable bound for the named orbit is `O(1)` (trivial). **The gap between observed `N^{−1/2}` and
   provable `O(1)` is the entire problem**, and `L_t` does not touch it.

---

## 4. Verdict — genuine handle vs relocated wall

**Relocated wall.** Mapped precisely onto the recurring pattern (`property ↔ resource ↔ spoofer`): `L_t`
re-expresses "single-orbit `(3/2)^j` equidistribution" as "spectral gap of the `×(3/2)` twisted transfer
operator **and** evaluation at the named orbit `c₀=8`." Both halves are the wall:
- the **gap** half = spectral gap of `×(3/2)` = Mahler (no classical-space gap, §1b);
- the **named-orbit** half = a.e.→specific selection = Tao-2019 / `COCYCLE_ERGODICITY.md §3` (§2).

It RELOCATES the core exactly as the four prior reformulations did (measure-contraction `AUDIT_CONTRACTION.md`,
bootstrap, vdC, MR): same length, new language.

### What is genuinely NEW / attackable (honest, narrow)
- **[language, real]** It ports the core into **thermodynamic formalism** (Ruelle resonances, transfer
  operators on **anisotropic / Blaschke** spaces, Pollicott–Naud resonance machinery). That is a *different*
  toolbox than vdC/MR/Bernoulli-convolution, and the `×(3/2)`-as-transfer-operator framing is a legitimate,
  precise target — one could ask for a **resonance-free strip** for `L_t`. This is a real new *attack surface*.
- **[bankable, not new to this audit]** The **un-twisted** `(ℤ₂,T)` operator *does* have a gap (a.e. exp.
  mixing) — but that is the equilibrium statement we already had (Haar mixing), and it is precisely what
  cannot select `c₀=8`.

### What is Mahler relocated (not new)
- **[OPEN=Mahler]** A spectral gap for the **twist-faithful** `L_t` (= gap for `×(3/2)`) — no classical-space
  gap exists; establishing one in an anisotropic space is itself a `(3/2)^n`-equidistribution theorem.
- **[OPEN=Tao a.e.→named]** Even granting a gap, transferring it to the **specific** orbit `c₀=8` needs an
  **independent Diophantine/effective input** — the universally missing ingredient.

### Net
`L_t` is **not** a shortening of the proof. Its one genuine affordance is **vocabulary** (resonances /
anisotropic transfer operators) that *might* admit techniques unavailable to the harmonic-analysis routes —
but the two open halves it must supply (`×(3/2)` gap, and named-orbit selection) are *exactly* the two faces
of the wall. Pursue it only as a **language for the same target**, with these two [OPEN] obligations stated up
front; do not bank `ρ(L_t)<1 ⇒ Antihydra` as progress on the single orbit.
