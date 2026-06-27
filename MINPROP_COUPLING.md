# Can the PROVEN exact/Bernoulli structure give a one-sided bound for o0=27, or does it hit the a.e. wall? (2026-06-28)

*Honest assessment requested after E4 PROVED the induced odd map `T(o)=3^{D-1}(3o-1)/2^D`, `D=v2(3o-1)`,
is **Haar-preserving + exact/Bernoulli** on `Z_2^*` with `D_j` i.i.d. geometric `2^{-d}` — but only for the
invariant (Haar) measure. The specific Antihydra orbit `o0=27` (`c0=8 -> 12 -> 18 -> 27`) is Haar-null.
Question: coupling / shadowing / specification — can the proven structure yield a QUANTITATIVE one-sided
bound for THIS orbit, or is the a.e. wall unavoidable? Numerics `.venv` only (`minprop_coupling.py`,
exact big-int). Every line labelled. Zero false proofs. NOT committed.*

---

## 0. One-line answer

The exact/Bernoulli structure gives a single specified orbit **nothing directly** (Haar-null), and — the new
content here — **specification PROVES that no universal/structural one-sided bound can exist**: the induced map
is a full-branch (Bernoulli) shift, so over its invariant measures `freq(o≡3 mod 4)=freq(D≥2)` ranges over the
**entire** interval `[0,1]` (Dirac at the genuine fixed point `o=1` gives `0`; Dirac at `o=3/5∈Z_2` gives `1`),
and multifractal/specification theory realizes every intermediate value on a **full-Hausdorff-dimension** set of
orbits. Hence `liminf freq(o≡3 mod 4) ≥ 1/2` is **provably non-universal** — it is violated by uncountably many
orbits — so `o0=27` **must** be singled out arithmetically. That singling-out is effective equidistribution of the
specific 2-adic point. **No coupling source exists** for `o0=27`: its 2-adic tail is fixed (eventually zero), the
window-shift pulls in the deterministic high bits of the iterates, never an independent refresh. This **sharpens**
"reduces to (A)" from "we couldn't find a structural bound" to "**no structural bound exists; the wall is forced.**"

---

## 1. What exact/Bernoulli DOES and does NOT give for `o0=27` `[PROVEN]`

**Gives (for the measure μ = Haar):** exact ⟹ tail-trivial ⟹ K-mixing ⟹ strong mixing; Bernoulli ⟹ exponential
decay of correlations, Birkhoff ergodic theorem, CLT, LIL for the digit `D`. Operationally: for **μ-a.e.** start
`o`, `freq(D≥k) → 2^{1-k}`, in particular `freq(D≥2) → 1/2` and `mean D → 2`, with `O(1/√K)` fluctuations.

**Does NOT give for `o0=27`:** the orbit `{27, T27, T²27, …}` is a countable set, hence **μ-null**. Every a.e.
theorem above explicitly excludes a measure-zero set, and says **nothing** about any individually named point.
Exactness controls Haar-typical orbits; `o0=27` is one specified point. **Directly, the structure gives the
specific orbit literally nothing.** (This is not pessimism — it is the definition of "a.e.")

The dynamical version: the set of points **non-generic** for the Bernoulli/MME has **full entropy and full
Hausdorff dimension** (Barreira–Schmeling 2000; recorded in `WALLB_INVARIANT_MEASURES.md`). `o0=27` lives in
that full-dimension non-generic set as far as the structure can see.

---

## 2. Specification / ergodic-optimization: the bound is PROVABLY NON-UNIVERSAL `[PROVEN]`

The induced map is a **full-branch** map: each cylinder `A_d` (`μ=2^{-d}`) maps **onto all of `Z_2^*`** (E4, §2).
A one-sided full shift over its symbol set has the **specification property**. The consequence (Sigmund;
Takens–Verbitskiy; multifractal analysis): for a continuous observable `φ`, the set of Birkhoff averages of `φ`
realized by **some** orbit is **exactly the interval** `[ min_ν ∫φ dν , max_ν ∫φ dν ]` over invariant measures
`ν`, and every interior value is realized on a **full-Hausdorff-dimension** set of orbits.

Take the **target observable** `φ = 1{o≡3 mod 4} = 1{D≥2}`. The relevant question is whether specification builds
orbits violating `freq(φ) ≥ 1/2`. It does — decisively — because the **ergodic-optimization extrema are 0 and 1**,
both achieved by genuine fixed points (verified, §4 numerics):

| invariant measure | observable value | status |
|---|---|---|
| Dirac at `o=1` (`T(1)=1`, `D=1` forever) | `freq(D≥2) = 0` | `[PROVEN]` `5·1≠3`; `o=1` solves `2o=3o-1` |
| Dirac at `o=3/5 ∈ Z_2` (`T(3/5)=3/5`, `D=2` forever) | `freq(D≥2) = 1` | `[PROVEN]` `5o=3` ⟹ `3o-1=4/5`, `v2=2` |
| Haar (Bernoulli) | `freq(D≥2) = 1/2` | `[PROVEN]` E4 |

So `min_ν ∫φ = 0`, `max_ν ∫φ = 1`. The **violation observable** `ψ = 1/2 − 1{D≥2}` has
`max_ν ∫ψ dν = 1/2 − 0 = +1/2 > 0`. **Whenever the ergodic-optimization max of the violation observable is
strictly positive, specification constructs orbits violating the bound** — here on a full-dimension set, with any
prescribed `freq(D≥2)∈[0,1]`. (Recall ergodic optimization: `max_ν ∫ψ ≤ 0` would mean no violating orbit exists;
`> 0` means abundant violators. Our value is `+1/2`, the worst case.)

> **`[PROVEN]` `liminf freq(o≡3 mod 4) ≥ 1/2` is NON-UNIVERSAL.** It is false for the fixed point `o=1`
> (`freq=0`), for `o≡1,1,1,3 mod 4` periodic orbits (`freq=1/4`), and for a full-Hausdorff-dimension set of
> orbits realizing every value in `[0,1)`. The exact/Bernoulli structure is **fully compatible** with the
> bound failing. Therefore the structure **cannot** deliver the bound by any "for all orbits" argument; `o0=27`
> must be distinguished by its **specific arithmetic** = single-orbit equidistribution = wall (A).

This is the genuine sharpening: earlier docs said "we found no structural bound." Specification upgrades this to
"**a structural bound provably does not exist**" — the gap is irreducibly about the individual point.

---

## 3. Quantitative coupling for the SPECIFIC start: NONE exists; pin the obstruction `[PROVEN/OBSERVED]`

**Why Haar-a.e. works (one-step coupling).** For a Haar-random odd `o`, `o' mod 2^k` reads the bit-window
`[D, k+D)` of `o` (E4, §1). Those are **fresh, independent fair coin flips**, so `o' mod 2^k` is **exactly uniform
after a single step** — verified: `χ²/dof = 1.14` (`k=6`), `0.89` (`k=8`) for the Haar ensemble (§3a numerics).
The window-shift is an automatic coupling **because each step pulls in genuinely new, independent high bits**.

**Why it fails for `o0=27`.** `27 = 11011₂ = …0000011011`: its 2-adic expansion is **eventually 0**, a single
**fixed** rational point. The entire orbit `o_j` is an **exact deterministic function of the integer 27**. The
window-shift still pulls in "new high bits" each step — but those are the **high bits of the deterministic
iterates `o_j`**, themselves determined by 27, **not an independent refresh**. There is **no probability space and
no entropy source** to couple a Bernoulli copy against. A "coupling rate" for `o0=27` would be a quantitative
statement that its deterministic high bits decorrelate at an effective rate — which **is** effective
equidistribution of the specific point = the wall, verbatim.

**Is there a partial coupling?** No. We checked the two natural openings:
- *Refresh after the low bits cycle:* the low bits of `o_j` are determined by `o_{j-1} mod 2^{k+D}`, recursively
  back to `o_0 mod 2^{huge} = 27` exactly (finite expansion). No step ever escapes the determinism of 27.
- *Sensitive dependence as a coupling:* flipping bit 40 of `o0` makes the `D`-sequence diverge after ~21 induced
  steps (§3c) — the shift **expands**, high bits reach the low end. But this is sensitivity between **two
  deterministic** trajectories, not coupling to an i.i.d. source. Expansion without an injected random seed does
  not produce a coupling; it produces the equidistribution problem.

> **`[PROVEN/OBSERVED]` The only thing that makes the residue process couple to the Bernoulli model is the
> per-step injection of fresh independent high bits, available for a Haar-random start but provably absent for
> the fixed point `o0=27`. The obstruction is exactly that 27 has a fixed, eventually-zero 2-adic tail = no
> entropy source. Any coupling rate = effective equidistribution of the specific orbit = wall (A).**

---

## 4. Numerics (`minprop_coupling.py`, exact big-int, c0=8, K≈3·10⁵ odds) `[OBSERVED]`

| measurement | result | reading |
|---|---|---|
| `mean D`, `freq(D≥2)` real orbit | `1.99509`, `0.49847` | Haar values `2`, `0.5` (finite-K) |
| autocorr of `1{D≥2}`, lags 1..50 | `\|·\|_max = 0.0031` ≈ noise floor `1/√K=0.0018` | **OBSERVED memoryless**, same as Bernoulli |
| block-freq std (B=100/1k/10k) | `0.0496 / 0.0161 / 0.0052` | matches CLT `0.5/√B` and Bernoulli copy |
| signed running dev `freq_K−1/2` | min `−0.033`, max `+0.057`, final `−0.0015` | **symmetric two-sided**, ~`N(0,(1/2)²/K)` |
| prefixes (K≥50) with `freq_K < 1/2` | **0.704** | the orbit dips **below** the target 70% of prefixes |
| Haar-ensemble `o' mod 2^k` | `χ²/dof = 1.14 (k=6), 0.89 (k=8)` | **one-step coupling** when bits are fresh |
| flip bit 40 of `o0` → `D`-seq diverges | at step `21` | shift expands; sensitivity ≠ coupling |
| **specification: prescribed `freq(D≥2)`** | `0, 0.25, 0.5, 0.667, 1.0` all **realized exactly** | **bound non-universal**; `0` and `0.25` VIOLATE |
| fixed point `o=1` | `D=1` forever, `freq(D≥2)=0` | Dirac, ergodic-opt min |
| fixed point `o=3/5∈Z_2` | `D=2` forever (200 steps), `freq(D≥2)=1` | Dirac, ergodic-opt max |

Two readings matter most. **(i) One-sidedness fails empirically too:** the fluctuations of `freq_K` are
**symmetric** and the running frequency sits **below** `1/2` on 70% of prefixes — there is no structural
one-sided floor; only the conjectural **limit** is `1/2`. **(ii) Specification is demonstrated constructively:**
prescribed-itinerary 2-adic points (built by inverse branches) realize `freq(D≥2)` = `0, 0.25, 0.5, 0.667, 1.0`
to the printed digits, explicitly exhibiting orbits that **violate** `freq ≥ 1/2`.

---

## 5. Verdict (the four asks) `[PROVEN]` unless noted

| ask | answer | label |
|---|---|---|
| What does exact/Bernoulli give / not give for `o0=27`? | Gives full a.e. control (mixing, CLT, `freq→1/2`) for **μ-a.e.** start; `o0=27` is **μ-null** so it gives the specific orbit **nothing directly**. `o0=27` lies in the full-dimension non-generic set. | `[PROVEN]` |
| Does specification build bound-violating orbits (tied to ergodic-opt max)? | **Yes.** `freq(D≥2)` ranges over `[0,1]` over invariant measures (fixed points `o=1→0`, `o=3/5→1`); violation-observable max `= +1/2 > 0` ⟹ full-dimension family of orbits with any `freq∈[0,1)`. The one-sided bound is **provably non-universal**. | `[PROVEN]` |
| Any partial coupling for the specific start? | **No.** Coupling needs fresh independent high bits per step (present for Haar → one-step uniform; verified). `o0=27` has a fixed eventually-zero tail = **no entropy source**; the orbit is an exact function of `27`. Expansion/sensitivity ≠ coupling. A coupling rate = effective equidistribution = the wall. | `[PROVEN/OBSERVED]` |
| Numerics | Real orbit is OBSERVED Bernoulli-like (memoryless, CLT, symmetric two-sided, dips below `1/2` on 70% of prefixes); specification orbits constructively realize `freq=0,…,1`. | `[OBSERVED]`/`[PROVEN]` |

### Net (honest)
The proven exact/Bernoulli structure **cannot** yield a quantitative one-sided bound for `o0=27`. It hits the
a.e. wall — and now we can say **why it must**: specification proves the target is non-universal (violated on a
full-dimension set), so any valid argument is forced to use the **specific arithmetic** of `27`, which is
single-orbit (effective) equidistribution = Mahler/AEV = wall (A). There is no entropy source to couple the
deterministic orbit to the Bernoulli model. This is a **sharpening, not a breach**: "no structural bound exists"
is stronger and cleaner than "we couldn't find one," and it is consistent with all prior WALLB angles.

### Live next angle (un-mined)
Specification kills every *universal/structural* route. The only routes not yet shown literally identical to
equidistribution are **point-specific**: (a) an effective/quantitative genericity input for `27` (Mahler-type
normality of its forward orbit's 2-adic digits) — the named wall; (b) a one-sided **large-deviation** floor that
keeps the **empirical** mod-4 frequency from `liminf < 1/2` without proving convergence — but §4 shows the
fluctuations are symmetric, so an LDP would have to come from arithmetic absent from the structure. Both remain
`[OPEN]`; neither is reachable from exactness alone.

Script: `minprop_coupling.py`. Not committed.
