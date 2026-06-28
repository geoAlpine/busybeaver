# Quenched L²-flattening probe — the one un-closed speculative angle (2026-06-29)

**Probe of `FRESH_ANGLES_SCOUT.md` §7 (the single un-closed framing):** is there a *deterministic,
single-orbit, finite-N* L²-flattening of the Antihydra orbit's **own** empirical measure
`μ_N = (1/N) Σ_{n<N} δ_{c_n}` on `ℤ/2^k` under the ×3/2 dynamics — a SELF-GENERATED entropy increase /
additive-energy decay that beats additive concentration **without assuming equidistribution**?
Classical Bourgain–Gamburd / sum-product flattening flattens a *measure* (annealed average over random
signs); this tests the orbit's *own* deterministic measure.

Script: `l2_flattening_probe.py` (`.venv` python only; exact big-int orbit + numpy FFT). **Not committed.**
Every line labelled `[OBSERVED]` / `[PROVEN]` / `[OPEN]`. Zero false proofs.

- Orbit (exact): `h_0=8`, `h_{n+1}=floor(3h_n/2)=h_n+(h_n>>1)`, `h_n=floor(8·(3/2)^n)`.
- Residue: `c_n = h_n mod 2^k` (low k bits, exact big-int; no float `(3/2)^n`).
- Metrics on the group `ℤ/2^k`: collision prob `C2=Σ μ²` (Rényi-2 `H2=−log2 C2`), largest atom,
  additive energy `E(μ)=Σ_t (μ*μ)(t)²` (circular conv on `ℤ/2^k`), and `max_{ξ≠0}|μ̂(ξ)|` (L^∞ Fourier
  = sharpest sub-progression detector). Uniform target: `C2=E=maxatom=2^{−k}`, `H2=k`.
- Baselines: (a) **random** surrogate = N i.i.d. uniform residues (= the annealed/equidistribution
  prediction); (b) **concentrated** = induced fixed point `o=1` (δ-mass) and a coset/AP-confined orbit.

---

## 1–2. Flattening of μ_N (collision / Rényi-2 / largest atom) — `[OBSERVED]`

`C2(orbit)` lands **INSIDE the random 95% band at every N∈{10²,10³,10⁴,10⁵} and every k∈{4,6,8,10}.**
It converges to uniform `2^{−k}` exactly on the random schedule. `H2→k`, largest atom `→2^{−k}`.

| k | N | C2/uniform (orbit) | H2 | maxatom/uniform | random 95% band (C2/unif) | verdict |
|---|---|---|---|---|---|---|
| 8 | 10² | 3.99 | 6.00 | 7.68 | [3.17,4.20] | INSIDE |
| 8 | 10³ | 1.27 | 7.66 | 2.30 | [1.21,1.31] | INSIDE |
| 8 | 10⁴ | 1.02 | 7.97 | 1.31 | [1.022,1.030] | INSIDE |
| 8 | 10⁵ | 1.003 | 7.996 | 1.14 | [1.0022,1.0030] | INSIDE |
| 10| 10⁵ | 1.010 | 9.985 | 1.32 | [1.0096,1.0112] | INSIDE |

No frequency, scale, or window size shows the orbit measure flatter (or sharper) than a random sample.

## 3. Additive energy `E(μ)` — RANDOM, neither sub-random nor concentrated — `[OBSERVED]`

`E(μ_orbit)` equals `E(random)` to all displayed precision (≈ `2^{−k}`, i.e. uniform) at every k, and is
firmly **inside the random 95% band**. The concentrated anchors are wildly separated, confirming the
metric discriminates:

| k | E(orbit)/uniform | E(random)/uniform | fixed-pt o=1 E/unif | coset-AP E/unif | verdict |
|---|---|---|---|---|---|
| 6 | 1.000 | 1.000 | 64 (=2^k) | 16 | **RANDOM** |
| 8 | 1.000 | 1.000 | 256 | 64 | **RANDOM** |
| 10| 1.000 | 1.000 | 1024 | 256 | **RANDOM** |

The L^∞ test agrees: `max_{ξ≠0}|μ̂(ξ)|` (orbit) = 7.8e-3 at k=8/10, squarely inside the random band
[5.9e-3, 9.8e-3]; the coset-AP anchor would peak at 0.25. **The orbit avoids sub-progression
concentration — but only to exactly the degree a random sequence does.** No self-generated
non-concentration beyond i.i.d.

## 4. Flattening RATE — pure 1/N statistical, no enhancement — `[OBSERVED]`

Excess collision `C2(N)−2^{−k}` decays as `N^b`:

| k | orbit b | random b | random theory |
|---|---|---|---|
| 6 | −1.008 | −0.998 | −1 |
| 8 | −1.007 | −1.000 | −1 |

The orbit flattens at the **trivial random sampling rate `~1/N`** — the rate of any equidistributed
sequence being sampled, not a dynamically self-generated flattening. No faster-than-random decay.

## 5. STRUCTURAL CHECK — why there is no flattening mechanism — `[PROVEN, elementary]`

`×3` is a **bijection on ℤ/2^k** (3 is a unit mod 2^k). Therefore it **permutes residues** and leaves
`C2` and `E` *exactly* invariant. Verified numerically (k=8,10): `C2(μ)=C2(3·μ)` and `E(μ)=E(3·μ)` to
all digits. Consequence:

> **The ×3 self-expansion contributes ZERO L²-flattening on a fixed scale `ℤ/2^k`.** The only operation
> that can move the empirical measure is the **2-adic carry/shift** of the map `h↦h+⌊h/2⌋` (drop the low
> bit, pull in a fresh high bit). Controlling that shift — i.e. that the fresh high bits equidistribute —
> **is exactly the open Mahler/AEV equidistribution.** The time-shifted measure is also unchanged
> (the empirical measure is ~stationary), so there is no decorrelation increment to exploit.

This is the crisp reason the quenched analogue collapses: in the real / sum-product setting flattening
comes from `×3` mixing *across scales* (acting on ℝ, or on `ℤ/2^k` with **growing** k). On any **fixed**
scale the multiplicative part is a measure-preserving bijection, and the additive/carry part *is* the
equidistribution one wants to prove. **The probe reduces to the assumption.**

---

## Verdict — REFRAMES THE WALL, does not break it (as predicted) — honest

1. **No self-generated flattening.** The orbit's empirical measure `μ_N` is **statistically
   indistinguishable from a random surrogate** on every tested axis: collision probability, Rényi-2
   entropy, largest atom, **L⁴ additive energy**, **L^∞ max Fourier coefficient**, and flattening *rate*
   (`~N^{−1}`). The annealed/i.i.d. prediction is reproduced exactly. `[OBSERVED]`
2. **Additive energy is RANDOM**, not sub-random and not concentrated (`E/uniform = 1.000` vs concentrated
   anchors at `2^k` and `2^{k}/4`). So sum-product/flattening has **nothing to bootstrap**: the orbit is
   already at the random additive-energy floor, but no *unconditional* mechanism drives it there — it is
   the [OBSERVED] equidistribution, the same fact already in `QUENCHED_DATA.md`, not a new inequality.
3. **The flattening mechanism is structurally absent on a fixed scale.** `[PROVEN]` `×3` is a bijection
   mod `2^k` ⇒ contributes no L²-flattening; the only flattening channel is the 2-adic carry/shift, whose
   control **is** Mahler. So a finite-N flattening inequality, if it held, would *be* effective
   single-orbit equidistribution — it does not exist as an unconditional input.
4. **Honest headline:** this is a clean **"reframes, does not break."** The quenched L²-flattening angle
   joins the two known walls: it is the *annealed* sum-product flattening (Wall II) wearing a
   single-orbit costume, and on a fixed scale it degenerates because the expanding map is a bijection.
   **No genuine lead, no surprising signal.** Consistent with `FRESH_ANGLES_SCOUT.md` §7 (flagged exactly
   as "re-frames the wall rather than breaking it"), `QUENCHED_DATA.md` (√N-generic, inside random band),
   and `NONPISOT_FOURIER_CHAIN.md` Link C (annealed ≠ quenched).

### One bankable structural note (new, modest, `[PROVEN]`)
The reason the quenched flattening idea cannot be unconditional is sharper than "it reduces to
equidistribution": **on the natural fixed group `ℤ/2^k` the ×3/2 dynamics splits into a
measure-preserving bijection (`×3`, zero flattening) and a 2-adic carry/shift, so 100% of any flattening
lives in the carry/shift = Mahler.** L²-flattening cannot decouple from equidistribution here even in
principle. This is a cleaner closing of §7 than the survey gave (which left it merely "[OPEN], no
expectation"), and it is exact-arithmetic verified. Does not change the [OPEN] status of the kernel.
