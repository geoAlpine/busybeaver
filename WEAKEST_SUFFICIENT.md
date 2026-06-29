# The WEAKEST sufficient hypothesis for the Antihydra open kernel (K) (2026-06-29)

*Angle: among analytic genericity inputs that IMPLY the kernel (K) = `mean D ≥ 3/2`, find the
logically WEAKEST (most accessible), and decide honestly whether the one-sided `≥1/3` slack (vs the
equidistribution value `=1/2`) buys a sufficient condition strictly weaker than full Mahler/AEV-q2.
Numerics `/Users/aokiyousuke/quantum-ecc/.venv/bin/python` (`scratchpad/weakest2.py`, exact big-int).
Every line labelled. Zero false proofs. NOT committed. No machine decided; no non-halt asserted.*

---

## 0. One-line answer

The one-sided `≥1/3` slack **does** buy a strictly weaker sufficient hypothesis than full equidistribution
— and it can be pushed all the way down to a **SINGLE character, ONE-SIDED, with a numerical `1/3` margin**.
Concretely `(K)` is *equivalent* to

> **`H₂ : liminf_N (1/N) Σ_{n<N} (−1)^{c_n} ≥ −1/3`**  (the single **mod-2 / parity character** of the
> Antihydra `c`-orbit `c₀=8`, `c→⌊3c/2⌋`),

which is a one-frequency, one-sided cancellation statement carrying a full `1/3` slack below the
equidistribution value `0`. Full Mahler/AEV-q2 (all `2^k`-levels, two-sided, exact) **over-implies** `H₂`
by a wide margin. **So `(K)` is logically far weaker than full equidistribution.** BUT — brutal honesty
— `H₂` is *itself* a single-orbit cancellation for a geometric `(3/2)`-phase, and **no known tool reaches
even a single one-sided character cancellation for the deterministic orbit** (the annealed average is
`=0`, Wall II, but the quenched single realisation is uncontrolled). **The slack reduces the logical
content from "infinite-dimensional, two-sided, exact" to "one-dimensional, one-sided, with room," but it
does NOT cross below the two walls.** Weaker hypothesis, same difficulty class.

---

## 1. Exact restatement of the target and the arithmetic of the slack `[PROVEN]`

Induced odd map (GAP LEMMA): `o_{j+1}=3^{D−1}(3o_j−1)/2^D`, `D=v₂(3o_j−1)≥1`, `o₀=27`.
`D=Σ_{k≥1}1{D≥k}`, and `D≥k ⟺ o≡3^{−1} mod 2^k` (a cylinder of relative Haar measure `2^{1−k}` among
odds). Hence the two exact identities (re-verified, `K=10⁵`, `meanD=2.00069`):

- **`mean D = Σ_{k≥1} freq(o≡3^{−1} mod 2^k)`** (`k=1` term `≡1`; `k=2` term `=freq(o≡3 mod4)`).
- **`even-density = 1 − 1/(mean D)`** (renewal counting). So `(K)`:

> `mean D ≥ 3/2 ⟺ Σ_{k≥2} freq(D≥k)=E[D−1] ≥ 1/2 ⟺ even-density ≥ 1/3`.

**The slack, quantified.** Under Haar every cylinder is at its value `2^{1−k}`, so `E[D−1]=1`. The target
is `E[D−1]≥1/2`. **There is a full factor-of-2 of room** between the equidistribution value (`1`) and the
target (`1/2`). This room is the entire content of "one-sided `≥1/3` is weaker than `=1/2`." Numerics
(Haar-consistent): `freq(D≥k)` for `k=1..6` `= 1, .5005, .2501, .1249, .062, .0315` vs Haar
`1, .5, .25, .125, .0625, .0312`.

---

## 2. Per-hypothesis implication analysis (the candidate weakenings)

For each: does it **imply (K)**? is it **weaker than full equidistribution**? is it **known/open**?

### (a) positive LOWER density of `{o≡3 mod4}` (any constant `c>0`) — **DOES NOT IMPLY (K)** `[PROVEN]`
`{D≥k}⊆{D≥2}={o≡3 mod4}` for all `k≥2`, so `freq(o≡3 mod4)` is the **largest** of the `k≥2` terms.
From `freq(o≡3 mod4)≥c` alone (dropping the nested deeper terms, each `≥0`) we get only
`mean D ≥ 1 + c`. For `≥3/2` this needs **`c ≥ 1/2`**, not "any positive `c`." With `c<1/2` the orbit
could put *all* of its `D≥2` mass at exactly `D=2` (no deeper), giving `mean D = 1+c < 3/2`.
**Verdict: FALSE as stated.** The exact mod-4 threshold is `c=1/2` (= the Haar value), reached only by
also being one-sided-at-value (§3). A general positive `c` does **not** suffice.

### (b) residues mod 4 not trapped in `{1 mod4}` with density `>2/3` — **DOES NOT IMPLY (K)** `[PROVEN]`
"`freq(o≡1 mod4) ≤ 2/3`" `⟺` "`freq(o≡3 mod4) ≥ 1/3`" (only residues `1,3` occur, `o` odd). Then
`mean D ≥ 1 + 1/3 = 4/3 < 3/2`. **Verdict: FALSE — short of the target.** The correct mod-4-only
threshold is `freq(o≡1 mod4) ≤ 1/2` (`⟺ freq(o≡3 mod4) ≥ 1/2`), **not** `2/3`. The `2/3` value would
need the deep tail `Σ_{k≥3}freq(D≥k) ≥ 1/6` to make up the difference — i.e. extra hypotheses.

### (c) pair-correlation / second-moment (Rudnick–Sarnak) — **IMPLIES (K) but is STRONGER, not weaker** `[PROVEN/known]`
Poissonian pair correlation **implies** uniform distribution (Grepstad–Larcher; Aistleitner–Lachmann–
Pausinger; Steinerberger), so it over-implies `(K)`. But it is therefore **at least as strong as full
u.d.**, not weaker; and it is only ever established **metrically (a.e. in the parameter)** — Wall I — never
for a single algebraic point. A bare *second-moment* `Σ_N|S_N|²` bound is an **L²/additive-energy** (mean-
over-`x`) statement = Wall I, giving a.e./annealed control, not the quenched single orbit. **Verdict:
sufficient but NOT a weakening; and only known a.e./annealed (behind both walls for the single orbit).**

### (d) single nontrivial Weyl/character cancellation at ONE frequency — **DEPENDS ON THE DUAL** `[PROVEN]`
- **On the 2-adic dual: YES, one character suffices.** A cylinder is *band-limited* in the 2-adic dual: it
  is a finite combination of finitely many `2^k`-th-power characters. In particular `freq(o≡3 mod4)` is an
  **exact** function of the **single** nontrivial character `χ₄(o)=(−1)^{(o−1)/2}`:
  `freq(o≡3 mod4)=½(1−avg χ₄)`. So `freq(o≡3 mod4)≥1/2 ⟺ liminf avg χ₄ ≤ 0` (**one character, one-sided**).
  This implies `(K)` via `mean D ≥ 1+freq(o≡3 mod4)`. **One frequency genuinely suffices here.**
- **On the circle (integer Weyl frequencies, the Mahler setting): NO, one is not enough.** The even-density
  is a **half-arc** frequency of `{ξ(3/2)^n}`, and an arc indicator is **not** band-limited (infinite
  Fourier series). A single integer frequency controls one Fourier coefficient, not an arc. The slack lets
  a **FINITE** Selberg–Vaaler minorant do the job (§4): `target 1/3 ⇒ degree J=5`.
  **Verdict: (d) is TRUE on the natural (2-adic) dual — a single character one-sided — and on the circle
  becomes "finitely many (`J=5`)".** Either way the count is *finite*, vs *all* frequencies for u.d.

### (e) sub-linear discrepancy `D_N = o(N)` — **IMPLIES (K) but IS equidistribution (no weakening)** `[PROVEN/def]`
`D_N=o(N)` is, by definition, exactly **uniform distribution** of the sequence. It gives every cylinder its
exact value (`mean D = 2`) so it over-implies `(K)` — but it is **the full equidistribution statement
itself**, i.e. Mahler/AEV-strength, not a weakening. **Verdict: sufficient, equal to full u.d., not
weaker.** (The genuinely weaker object is a *one-sided* bound on *one* cylinder's frequency, not a
two-sided `o(N)` bound on the all-cylinder discrepancy.)

---

## 3. The weakest sufficient hypotheses, ranked (the chain of strict weakenings) `[PROVEN implications]`

Each `⟹` below is a strict **logical** weakening (the lower line is implied by the upper, not conversely).

```
full AEV-q2 / Mahler           : ALL 2^k-levels, TWO-sided, EXACT  (mean D = 2)
        ⟹
AEV-level-2 (two-sided)        : freq(o≡3 mod4) = 1/2              (induced, ONE character, exact value)
   or  AEV-level-1 (two-sided) : avg (−1)^{c_n} = 0                (c-orbit, ONE character, exact value)
        ⟹
one-sided at the value         : freq(o≡3 mod4) ≥ 1/2   ⟺  liminf avg χ₄ ≤ 0
        ⟹
one-sided WITH numerical slack : even-density ≥ 1/3  ⟺  liminf avg (−1)^{c_n} ≥ −1/3   ==  (K)   ⭐ weakest
```

- **Weakest sufficient = `H₂` (`= (K)` itself):** `liminf_N (1/N)Σ_{n<N}(−1)^{c_n} ≥ −1/3`. This is a
  **single mod-2 (parity) character** of the `c`-orbit, **one-sided**, carrying a **full `1/3` numerical
  slack** below the equidistribution value `0`. It is *equivalent* to `(K)`, so nothing sufficient is
  weaker. Equivalence: `avg(−1)^{c_n}=2·even-density−1`, so `even-density≥1/3 ⟺ avg ≥ −1/3`. `[PROVEN]`
- **Cleanest one-character *sufficient* (slightly stronger than `(K)`):** `H₄: liminf avg χ₄(o_n) ≤ 0`
  (induced mod-4 character), `⟹ freq(o≡3 mod4)≥1/2 ⟹ mean D≥3/2`. This throws away the deep-level slack,
  so it needs the **exact Haar value** at level 2 (no numerical room) — but it is still one character,
  one-sided.
- **Most "uniform-slack" sufficient:** `freq(D≥k) ≥ ½·2^{1−k}` for all `k≥2` (every deep cylinder occupied
  at least HALF as often as Haar) `⟹ Σ_{k≥2}freq ≥ ½`. A one-sided, **constant-factor-2-loss** lower bound
  at every level — the version that spends the factor-2 slack evenly.

**Where the slack lives.** The `1/3`-vs-`1/2` slack manifests in exactly three interchangeable ways:
(i) **one-sidedness** (`≤/≥` a value, not `=`); (ii) **finiteness of the frequency/level count** (one
character on the 2-adic dual, or `J=5` on the circle, instead of *all*); (iii) a **numerical margin**
(tolerate `avg(−1)^{c_n}` as low as `−1/3`, or each deep cylinder down to half its Haar value).

---

## 4. The circle / Selberg–Vaaler quantification of (d)/(e) `[PROVEN]`

Even-density `= freq({ξ(3/2)^n} ∈ half-arc)`, an arc of mean `1/2`. Vaaler's theorem: the best degree-`J`
trigonometric **minorant** of an interval indicator has `L¹` deficiency exactly `1/(J+1)`, so its mean is
`1/2 − 1/(J+1)`. With a minorant `m ≤ 1_{arc}` of degree `J`,
`even-density ≥ (1/N)Σ m(y_n) = m̂(0) + Σ_{1≤|j|≤J} m̂(j)·(1/N)Σ_n e(j y_n)`. If the `J` Weyl sums vanish
(`→0`), `liminf even-density ≥ 1/2 − 1/(J+1)`. For the target:

| target even-density | min degree `J` (frequencies needed) |
|---|---|
| `≥ 1/3` | **`J = 5`** |
| `≥ 0.40` | `J = 10` |
| `≥ 0.45` | `J = 20` |
| `≥ 0.49` | `J = 99` |
| `→ 1/2` (Haar value) | `J → ∞` (= **full equidistribution**) |

> **This is the crisp meaning of the slack:** the one-sided `1/3` target needs cancellation at only the
> **first 5 integer frequencies**; demanding the full Haar value `1/2` would need **all** frequencies =
> full equidistribution. The slack converts an *infinite* (all-frequency, Weyl-criterion) requirement into
> a *finite* one. `[PROVEN]` (Vaaler) — but each individual `S_N(j)/N→0` for the deterministic `(3/2)^n`
> orbit is itself open (FRESH_ANGLES_SCOUT: even ONE such frequency is behind both walls).

---

## 5. Numerical test of the weakest hypotheses on the real orbit `[OBSERVED]`

`weakest2.py`, exact big-int (`K=10⁵` induced; `S=2·10⁵` c-orbit).

| quantity | value | reading |
|---|---|---|
| `mean D` | `2.00069` | Haar 2; identity `Σ_k freq(D≥k)=mean D` confirmed |
| `freq(o≡3 mod4)=freq(D≥2)` | `0.50052` | Haar `0.5`; finite-trunc `1+freq(D≥2)=1.50052 ≥ 3/2` ✔ |
| `avg χ₄(o_n)` (induced mod-4 char) | `−0.00104` | AEV value `0`; `H₄` holds, but **at the boundary** (worst finite window `freq(3mod4)=0.467`) — no numerical slack at level 2 |
| even-density (c-orbit) | `0.50018` | Haar `0.5`; target `≥1/3` |
| `avg(−1)^{c_n}` (mod-2 char) | `+0.00037` | AEV value `0`; `H₂` needs `liminf ≥ −1/3` |
| **worst running `avg(−1)^{c_n}` (`n≥50`)** | **`−0.0407`** ⇒ min even-density `0.480` | `H₂` holds with a **comfortable `~0.15` margin** above `1/3` (finite `N` only) |
| Vaaler degree for target `1/3` | `J = 5` | finite-frequency sufficiency confirmed |

**Reading.** The weakest hypothesis `H₂` (mod-2 char, one-sided, `1/3` slack) is the one with the
**largest observed margin** — the orbit's parity character never gets within `0.29` of the `−1/3` floor.
The *sufficient* one-character `H₄` (level-2 at exact value) sits **on the boundary** (it spends none of
the slack), consistent with §3: the numerical room is real only when you keep the deep levels / use the
mod-2 equivalent form. **All `[OBSERVED]`; finite `N` says nothing about the liminf.**

---

## 6. Honest verdict (point 3 — does the slack reduce difficulty below Mahler?)

**Logically: YES, dramatically.** `(K)` is *equivalent* to a **single character, one-sided, `1/3`-slack**
statement (`H₂`); a clean *sufficient* condition is a **single character one-sided** statement (`H₄` /
`liminf avg χ₄ ≤ 0`); on the circle the slack reduces the Weyl-criterion from **all** frequencies to the
**first 5**. Full Mahler/AEV-q2 (all `2^k` levels, two-sided, exact) is *enormously* more than needed — it
over-implies `(K)` with a factor-2 of room to spare. So the meta-claim "`(K)` is strictly weaker than full
equidistribution" is **correct and now precisely quantified** (one-sided / one-character / `J=5` / factor-2
numerical slack).

**For proof difficulty: NO, it does not cross below the wall — and this is consistent with the
β>0 / no-structure-only meta-theorem.** The weakest sufficient inputs are all of the *same kind* — a
quenched single-orbit cancellation of a geometric `(3/2)`-phase character — for which:
- the **annealed** mean is controlled (`= 0`, Wall II) but gives nothing for the single realisation;
- the **metric/a.e.** results (pair-correlation, decoupling, Salem–Zygmund) give `√N`-type cancellation
  for a.e. parameter (Wall I) but cannot be specialised to the one algebraic orbit;
- **no unconditional tool delivers even ONE one-sided single-orbit character cancellation** for `(3/2)^n`
  (FRESH_ANGLES_SCOUT, O18_QUENCHED_BC: a single frequency `S_N(t)=o(N)` is itself open).

So the slack **buys a strictly weaker hypothesis (fewer frequencies, one-sided, numerical room) but not a
more *provable* one**: even the minimal `liminf avg(−1)^{c_n} ≥ −1/3` is an unconditional single-orbit
cancellation, behind both walls. The honest summary matches O18_QUENCHED_BC's pattern: **weaker target,
same wall, no current crack** — but here the weakening is sharper than ever (down to one character with
`1/3` slack), which makes it the cleanest possible *statement* of the open kernel, even though not an
easier *theorem*.

### What is genuinely new in this note vs the prior reductions
1. The kernel is restated as a **single mod-2 (parity) character one-sided cancellation with an explicit
   `1/3` numerical slack** — strictly the smallest object the open problem has been compressed to (prior
   notes had the *sufficient* `freq(o≡3 mod4)≥1/2`, which has **no** numerical slack; the mod-2 form is
   *equivalent* to `(K)` and carries the full slack).
2. Candidates (a) and (b) are **refuted with exact thresholds** (any-`c` and `2/3` are insufficient; the
   true thresholds are `1/2`); (c) and (e) are shown **sufficient-but-not-weaker** (stronger / equal to
   u.d.); (d) is resolved **dual-dependently** (one character on the 2-adic dual, `J=5` on the circle).
3. The slack ↔ frequency-count law is made quantitative via Vaaler: `target = 1/2 − 1/(J+1)`, so the
   `1/3` target `⟺ J=5`, and `target→1/2 ⟺ J→∞` (full equidistribution). **The slack literally equals
   the gap between finitely-many and all frequencies.**

**No machine decided. No non-halt asserted. No label upgraded.** The reduction (raw TM → this one-sided
single-character kernel) remains the unconditional contribution; the kernel `(K)` remains `[OPEN]`,
equivalent to a single one-sided `(3/2)`-character cancellation behind the two walls.
