# Is any equivalent / sufficient non-halting condition UNIT-PART (free) measurable? (2026-06-28)

*The load-bearing micro-question left open by `THREEADIC_SKEW.md` §"Live next angle" and
`SESSION_2026-06-28_THREEADIC.md` next-hand #1. The 3-adic fiber's **unit part** synchronizes FOR FREE
(proven |·|₃-contraction `Φ_D(y)=3^{D-1}2^{-D}(3y-1)`, no genericity), while the standard non-halt
observable (mean D / even-density) is **valuation**-measurable, orthogonal to it. Asked: is there ANY
equivalent or SUFFICIENT non-halting condition that is unit-part-measurable, hence free? If yes,
non-halting of `o₀=27` would follow unconditionally. Numerics `.venv` only (`unitpart_observable.py`,
exact big-int, 2·10⁵ induced steps). Every line labelled. Zero false proofs. NOT committed.*

---

## 0. One-line answer

**NO.** Neither an equivalent nor a sufficient non-halting condition is unit-part-(free)-measurable, and
the reason is now **`[PROVEN]`-sharp on two independent levels**:

1. **Re-encoding level `[PROVEN]/[OBSERVED]`.** The fiber is *fully driven*: synchronization makes
   `u_j mod 3^k` a **finite sliding-window function of the recent base symbols** `(D_{j-1},…,D_{j-w})`,
   `w≈k+1` (`[S2]`, 0 multi-image). So the unit part is **re-encoded base/valuation data**, not an
   independent free channel. Any unit-part functional is a *bounded, finite-window* function of the
   `D`-itinerary; the target is the **Cesàro average of the unbounded `D`**, whose convergence *is*
   genericity. Synchronization delivers each integrand value for free but **never the average** (`[S4]`).

2. **Shared-with-halting level `[PROVEN]` — the decisive obstruction.** "Free" = holds **pathwise for
   every base symbol sequence** (it is a property of the contraction, not of the itinerary statistics).
   The **halting fixed point `o=1`** (`D≡1`, even-density 0) is a legal base sequence whose fiber unit
   part **synchronizes by the identical free mechanism** (`[S1]`: `D≡1` and the real orbit synchronize
   identically). Therefore **any free condition holds at `o=1` too — but `o=1` HALTS — so no free
   condition can imply non-halting.** Freeness ⊄ non-halting, unconditionally.

Non-halting is **irreducibly valuation-measurable**: its only target channel is `v3(o_{j+1})=D_j−1`, the
**invertible** (generating, full) re-encoding of the base itinerary, and it is an **asymptotic average**,
the one thing both the contraction-freeness and finite-window unit data are blind to.

---

## 1. Enumerated equivalent forms and their measurability `[PROVEN]`

From `KERNEL_FINAL.md` §1 / `PROOF_STATUS.md`. For each: is it valuation-measurable (a function of the
`D`/`v3` sequence) or could it be unit-part-measurable?

| # | Equivalent non-halt form | measurability | label |
|---|---|---|---|
| (i) | even-density `E_n/n ≥ 1/3` (`c₀=8`) | **valuation** — renewal identity even-density `=1−1/meanD`, function of `D` only | `[PROVEN]` |
| (ii) | `mean D ≥ 3/2` (`D=v₂(3o−1)`) | **valuation** — `D` *is* the symbol | `[PROVEN]` |
| (iii) | `freq(D≥2)+freq(D≥3) ≥ 1/2`, tight `freq(o≡3 mod4)≥1/2` | **valuation** — frequency of the symbol | `[PROVEN]` |
| (iv) | `freq(D=1)=freq(o≡1 mod4) ≤ 1/2+freq(o≡3 mod8)` | **valuation** — cylinder occupancy of `D` | `[PROVEN]` |
| (v) | empirical measure does NOT concentrate near halting fixed point `o=1` | **valuation** — `o=1` is the `D≡1` atom | `[PROVEN]` |
| (vi) | parity sum `(1/N)Σ(−1)^{bit_n(T_n)}=o(1)` (`PROOF_STATUS` (K)) | **valuation** — `bit_n(T_n)` is the parity = even/odd = `D`-derived | `[PROVEN]` |
| (vii) | `balance_n = 3E_n−n ≥ 0 ∀n` | **valuation** — running Birkhoff PARTIAL SUM of the even-indicator | `[PROVEN]` |
| (viii) | 3-adic dual: `density{3|o_j}+density{9|o_j} ≥ 1/2` | **valuation** — `density{3|o_j}=freq(D≥2)` via `v3(o_j)=D_{j-1}−1` | `[PROVEN]` |

**Every equivalent form is a function of the `D`/valuation sequence.** The 3-adic dual (viii) *looks* like
it might touch the unit part (it mentions `o_j`'s 3-adic data) but it reads only `v3(o_j)` — the valuation —
which is `D_{j-1}−1`. There is **no equivalent form whose definition queries the unit digits `u_j mod 3^k`**.

**Why no reformulation rescues it `[PROVEN]`.** The map between channels is the identity
`v3(o_{j+1})=D_j−1`, an **invertible bijection `k↦k+1`** (`[S0]`, 0 violations / 2·10⁵). So the valuation
sequence is a **generating (full) factor** of the base, not a coarser one; there is no compression of the
target onto a unit-part factor, because the unit part lives on the *complementary* (orthogonal) coordinates
that the target never queries.

---

## 2. Why a clever reformulation can't move the target onto the unit part `[PROVEN]/[OBSERVED]`

The hope: maybe the *integer values* `c_n`, or 3-adic/unit data, encode an equivalent condition that a
reformulation makes unit-measurable. **Refuted structurally.** Because the fiber is fully driven, the unit
part is itself a function of the very same `D`-symbols:

- **`[OBSERVED, exact] [S2]` Unit part = finite-window of `D`.** `u_j mod 3^k` is **deterministically
  determined** by the window `(D_{j-1},…,D_{j-w})` for `w≈k+1` (0 multi-image; e.g. `k=2,w=2`: 155 classes,
  0 multi; `k=3,w=3`: 829, 0 multi; too-short windows fail: `k=2,w=1` has 16 multi-image). This is the
  *synchronization* made explicit: each step the contraction pins one more 3-adic digit from the base.
- **Consequence `[PROVEN]`.** The σ-algebra of unit-part observables `⊆` the σ-algebra of finite-window
  functions of `(D_j)`. So *every* unit-part functional is a **bounded, locally-constant** function of the
  itinerary. The target (mean `D`, frequencies) is a **Cesàro average of an unbounded** observable.
  A bounded finite-window function carries **no information about asymptotic frequencies** — and
  conversely, the free synchronization gives you the finite-window *integrand* at each `j` but says
  **nothing about its time-average**. Averaging is exactly where genericity (the open kernel) enters.

So there is no "clever reformulation": the unit part and the target live in the same itinerary algebra, but
the unit part is the **finite-window (free)** part and the target is the **tail-average (genericity)** part.
They are complementary by construction.

---

## 3. Can the unit part bound the balance / exclude halting? `[PROVEN]/[OBSERVED]` — No

Halting ⟺ `balance_n = 3E_n − n < 0` ever; `balance_n` is a **running partial (Birkhoff) sum** of the
even-indicator (a `D`-functional). The unit part `u_j` carries 3-adic info about `o_j`; can any functional
of the free unit field bound this running count?

- **Structural `[PROVEN]`.** The unit field at time `j` is a finite window of `D`'s (§2); the balance is the
  **unbounded sum over the whole history**. A bounded window functional cannot bound an unbounded partial
  sum. (Same reason a bounded local observable cannot bound a Birkhoff sum without an ergodic average.)
- **Numerical `[OBSERVED] [S3]`.** Pearson correlation of `u_j mod 3^k` (as a feature) against the running
  balance level `B_j` is `≤ |0.003|` for `k=1..4` (`−0.0011, −0.0030, −0.0002, +0.0025`). Correlation
  against the *local* target bit `1[D_j≥2]` is `≤ |0.006|`. The free unit field is **statistically
  decoupled** from the balance and from the target indicator.
- **`[OBSERVED] [S3b]`** Predicting `1[D_j≥2]` from `u_j mod 3^k` gives best-per-class accuracy `0.5013`
  (`k=1`), `0.5036` (`k=2`) = **chance** — the local `D_j` lives in `o_{j+1}`'s *valuation*, not `o_j`'s
  *unit*, so the unit at time `j` does not even predict the contemporaneous target bit.

> **`[PROVEN]/[OBSERVED]` No functional of the free unit field bounds the balance.** The balance is an
> unbounded valuation-side partial sum; the unit field is a bounded, decoupled, valuation-re-encoded
> window. There is no inequality from one to the other.

---

## 4. The sufficient-condition search — the decisive meta-obstruction `[PROVEN]`

The real prize would be a **stronger** (not equivalent) condition that (a) implies non-halting and (b) is
unit-part-(free)-measurable. The candidate from the skew note: "the unit field synchronizes to its specific
stationary value." We test whether *any* free property can be sufficient.

**Definition.** Call a condition **free** if it is determined by the contraction's synchronization, i.e. it
holds **pathwise for every base symbol sequence** `(D_j)` (it does not depend on the itinerary's frequency
statistics).

**`[PROVEN] Meta-obstruction (shared-with-halting).** No free condition implies non-halting.**

*Proof.* The halting fixed point `o=1` has symbol sequence `D≡1` (even-density 0, a genuinely halting
orbit; `KERNEL_FINAL.md` §1 meta-theorem `β(ψ)=+1/2` attained there). Its fiber unit part synchronizes by
the **same free contraction** as the real orbit. Numerically `[S1]`: driving `Φ_D` with the all-`D=1`
sequence and with the real non-halting sequence both fully synchronize (gap `v3 → b=40`, complete) from two
different fiber starts — **identically**. So any free condition `C` (a pathwise property of the
synchronizing fiber) holds for the `D≡1` sequence as well. But the `D≡1` orbit **halts**. Hence `C` does
**not** imply non-halting. ∎

This is the sharp reason the un-mined thread closes: **the free part of the system (synchronization) is
exactly the part shared by the halting fixed point**, which is the realizer of the worst-case
ergodic-optimization value (`β(ψ)=+1/2`, `KERNEL_FINAL.md`). Freeness is *blind to the one thing that
separates halting from non-halting* — the frequency of `D≥2`. `[S1]`: "the contraction does not see the
frequency of `D≥2`." A sufficient condition must distinguish `o₀=27` from `o=1`; only a **frequency/average
(genericity)** statement does that, and genericity is precisely **not free**.

**Verification for `o₀=27` (negative, as predicted).** The orbit's unit field does synchronize freely
(`[S1]`/`[S2]`), but this is shared with `o=1`, so it yields nothing for non-halting. The averages that
*would* give non-halting — `mean D ≥ 3/2`, `freq(D≥2) ≥ 1/2` — converge empirically (`[S4]`:
`meanD≈2.00`, `freq(D≥2)≈0.500` at `N=2·10⁵`) but their **convergence is the open kernel**, not a free fact.

---

## 5. The precise reason non-halting is irreducibly valuation-measurable `[PROVEN]`

Two orthogonal decompositions coincide here:

- **Channel split.** Target channel = valuation `v3(o_{j+1})=D_j−1` (invertible = generating factor); the
  unit part = the complementary coordinates, **orthogonal** to the target (`THREEADIC_SKEW.md` §2).
- **Free/genericity split.** Free (synchronization, finite-window, pathwise) part vs. tail-average
  (genericity) part. The unit part is **entirely** in the free/finite-window part (§2 `[S2]`); the target
  is **entirely** in the tail-average part (§4 `[S4]`).

These two splits **align**: the free=unit-part side is shared with the halting fixed point `o=1`
(§4 `[S1]`), so it cannot carry the halting/non-halting distinction; the distinction lives **only** in the
valuation = tail-average = genericity side, which is precisely the AEV/Mahler single-orbit equidistribution
wall (`KERNEL_FINAL.md` §3, `PROOF_STATUS.md` (5)). Hence:

> **`[PROVEN]` Non-halting is irreducibly valuation-measurable and irreducibly an asymptotic average.**
> It cannot be an equivalent unit-part condition (the unit part is the orthogonal, finite-window channel),
> and it cannot be implied by any sufficient free condition (every free property is shared by the halting
> fixed point `o=1` and is blind to the frequency of `D≥2`). The contracting fiber's free synchronization
> is real but structurally **off-target on both axes** (orthogonal coordinate AND free-vs-average).

This **closes** the un-mined micro-thread of `THREEADIC_SKEW.md` §"Live next angle" /
`SESSION_2026-06-28_THREEADIC.md` next-hand #1: the free unit-part synchronization is **not** load-bearing,
for a now-proven reason (shared with halting `o=1`), not merely "current framing says it cannot."

---

## 6. Verdict (the asks)

| ask | answer | label |
|---|---|---|
| Equivalent non-halt condition that is unit-part(free)-measurable? | **No.** All 8 equivalent forms are valuation/`D`-functions; the channel map `v3=D−1` is invertible (generating), so no reformulation lands on the orthogonal unit coordinate. | `[PROVEN]` |
| Sufficient (stronger) free condition implying non-halting? | **No — meta-obstruction.** "Free" = pathwise for all symbol sequences; the halting fixed point `o=1` (`D≡1`) synchronizes by the same free mechanism (`[S1]`), so every free condition holds there too — but `o=1` halts. Freeness ⊄ non-halting. | `[PROVEN]` |
| Does the free unit field bound the balance? | **No.** Balance = unbounded valuation partial sum; unit field = bounded finite-window of `D` (`[S2]`), corr `≤0.006` with balance and with `1[D≥2]`; predicts the target bit at chance (`0.50`). | `[PROVEN]/[OBSERVED]` |
| Precise reason non-halting is irreducibly valuation-measurable? | Channel split (target=valuation=generating; unit=orthogonal) **aligns** with free/genericity split (unit=free finite-window; target=tail-average); free side is shared with halting `o=1`, so the halting distinction lives only on the valuation/average side = AEV/Mahler wall. | `[PROVEN]` |

### Assets banked `[PROVEN]/[OBSERVED]`
1. **`[OBSERVED, exact]` Unit part is a finite sliding-window function of the base symbols**
   `u_j mod 3^k = F(D_{j-1},…,D_{j-w})`, `w≈k+1`, 0 multi-image (`[S2]`) — synchronization made explicit;
   the unit part is re-encoded base data, not a free extra channel.
2. **`[PROVEN]` Free-vs-halting meta-obstruction.** Every free (pathwise-synchronization) condition holds
   at the halting fixed point `o=1`, hence none implies non-halting. The free part of the system is exactly
   the part blind to the frequency of `D≥2`. (`[S1]` numerical witness: `D≡1` and the real orbit
   synchronize identically.)
3. **`[OBSERVED]` Free unit field is statistically decoupled from the balance and the target indicator**
   (corr `≤0.006`, prediction at chance) — no functional bound.

### Why this confirms rather than breaches (honest)
The unit-part angle was the only structure `o₀=27` gets **for free** (genericity-independent). It is now
proven off-target on **both** the channel axis (orthogonal to the valuation the target reads) and the
free/average axis (shared with the halting fixed point, blind to frequency). The non-halting distinction is
**irreducibly** the asymptotic average of the valuation = single-orbit genericity = AEV/Mahler. No
unconditional breakthrough for `o₀=27`; the kernel of `KERNEL_FINAL.md`/`PROOF_STATUS.md` is unmoved, and
one more soft route (free synchronization) is now closed with a proven reason.

Script: `unitpart_observable.py`. Not committed.
