# MINPROP — ergodic-optimization test of the one-sided sub-solution (2026-06-28)

**Question.** The two-sided coboundary is OBSTRUCTED: the centered parity cocycle is
NON-coboundary (commit `794b450`, `furstenberg_A.py`: Birkhoff sums `S_n=2E_n−n` grow
`~sqrt(N)`, recurrent, CLT — not L²-bounded). The one-sided strategy
(`MINPROP_COBOUNDARY_LP`) instead seeks a **bounded `g` with `psi <= g∘T − g`** (a
one-sided SUB-solution), hoping the `1/4` Haar mean-slack of `psi` lets it survive where
the exact (two-sided) coboundary cannot. Does it?

Setup: induced odd map `T(o) = 3^{D−1}(3o−1)/2^D`, `D = v2(3o−1)`, on odd 2-adic units;
orbit `o0 = 27`.
`psi(o) = 1{o≡1 mod4} − 1{o≡3 mod8} − 1/2`, Haar-mean `−1/4`.
`avg psi <= 0  ⟺  freq(D≥2)+freq(D≥3) ≥ 1/2` (the robust GAP-lemma target).

---

## 1. [PROVEN — standard] Functional-analytic criterion

For an ergodic m.p. map `T` and `phi∈L²` with `∫phi=0`:
`phi` is a (measurable/L²) **coboundary** `phi=g−g∘T` **iff its Birkhoff sums are
L²-bounded**. If `S_N ~ sqrt(N)` (non-degenerate CLT), `phi` is **NOT** a coboundary.
This is exactly the two-sided obstruction already established for the parity cocycle.

For the **one-sided** problem (here `phi=psi`, mean `−1/4 < 0`): we seek **bounded** (or
continuous) `g` with `psi <= g∘T − g`. Summing along any orbit telescopes:
`Σ_{k<N} psi(o_k) <= g(o_N) − g(o_0) <= 2‖g‖_∞`, hence `limsup (1/N) Σ psi <= 0`
for **every** orbit. The sharp criterion (Mañé / Conze–Guivarc'h / Bousch sub-action
theory — existence of a continuous *sub-action*):

> The minimal constant `c` for which `psi <= g∘T − g + c` has a bounded/continuous
> solution `g` equals the **ergodic-maximizing value**
> `β(psi) := max over T-invariant measures μ of ∫ psi dμ`.
> In particular a level-`0` sub-solution (`c=0`, our goal) exists **iff `β(psi) <= 0`.**

So the one-sided bound is **NOT** governed by the L²/coboundary (Haar) obstruction at all —
it is governed by the **maximizing measure**, not by Haar's `−1/4`.

## 2. [PROVEN — standard] Ergodic-optimization reformulation

`limsup (1/N) Σ_{k<N} psi(o_k) <= 0` **for ALL orbits**
⟺ `β(psi) = max_μ ∫ psi dμ <= 0`.
(⇐: every empirical-measure weak-* limit is invariant, so its `psi`-integral `<= β`.
⇒: an ergodic maximizer's generic orbit — and any periodic maximizer's orbit literally —
achieves `β`.) By Bousch/Jenkinson ergodic optimization the maximizer is generically a
**periodic orbit**, so it suffices to maximize the `psi`-average over periodic orbits.

## 3. [PROVEN] `psi` is a function of the current symbol `D` alone — `β(psi)` is trivial

Numerics (`minprop_ergodic_opt.py`, 0 mismatches over all odd `o < 2·10⁶`):

| current `D` | residue | `psi` |
|---|---|---|
| `D=1`  | `o≡1 mod4` | **`+1/2`** |
| `D=2`  | `o≡7 mod8` | `−1/2` |
| `D≥3`  | `o≡3 mod8` | `−3/2` |

`psi` depends only on the **current** `D`. Under Haar the `D_j` are i.i.d. geometric
(PROVEN, E4) → the symbolic model is the **full shift** on `D∈{1,2,3,…}` (every
`D`-word admissible). For a cocycle that is a function of the current symbol on a full
shift, `max_μ ∫ psi = max_d psi(d)` (concentrate on the constant word). Hence

> **`β(psi) = max_d psi(d) = psi(1) = +1/2 > 0`.**

The maximizer is the **Dirac measure on the constant `D=1` sequence = the integer fixed
point `o=1`** (`T(1)=1`), i.e. the trivial Collatz/`3x−1` cycle.

## 4. [OBSERVED/PROVEN] Periodic-orbit search confirms `β = +1/2`

`minprop_ergodic_opt.py`:
- **Integer cycles** of the induced map (capped search, starts `o<2·10⁵`): the **only**
  cycle is `{1}`, `psi`-avg `= +0.5000`. (The map is Archimedean-expanding, `T(o)/o ≈
  (3/2)^D ≥ 3/2`, so all other integer orbits escape — `o=1` is the unique integer cycle.)
- **Constant-`D` 2-adic fixed points** `o_d = 3^{d−1}/(3^d−2^d)` (odd denominators, genuine
  2-adic units): `o_1=1` (`psi=+1/2`), `o_2=3/5` (`−1/2`), `o_3=9/19` (`−3/2`), …
  Max single-symbol `psi = +1/2` at `d=1`.
- Empirical Cesàro avg of `psi` along the **orbit of `o0=27`** approaches the Haar value:
  `N=10³…10⁵ → −0.247, −0.252, −0.253, −0.250, −0.251` (Haar `−0.25`). The orbit of 27
  **does** satisfy `avg psi <= 0` empirically — it is a *non-maximizing* (generic) orbit.

## 5. VERDICT — [PROVEN negative; sharply localizing]

**The level-0 one-sided sub-solution does NOT exist.** `β(psi)=+1/2 > 0`, so by the
criterion (§1) there is **no** bounded/continuous `g` with `psi <= g∘T − g`. **The `1/4`
Haar mean-slack does NOT rescue the one-sided strategy:** ergodic optimization is driven
by the *maximizing* measure, not Haar, and the maximizer (`o=1`, `+1/2`) ignores the slack.

**This is not a new accident — it is the *correct* structural reason an unconditional
all-orbits bound is impossible.** The maximizing orbit `o=1` is exactly the trivial cycle:
`D=1` forever ⟺ `o≡1 mod4` forever ⟺ mean `D=1<3/2` ⟺ even-density `0` ⟺ **HALTING**.
An unconditional `avg psi <= 0` would prove non-halting for *every* orbit; but halting
orbits exist (`o=1` and its basin). So the open core is **irreducibly orbit-specific** —
no coboundary/sub-action argument at the level of this `psi` can be unconditional. This
also re-confirms (from a third, ergodic-optimization angle) the
`SESSION_2026-06-28_INDUCED_MAP.md` conclusion that the wall is single-orbit genericity.

**What the result *buys* (the live content).** The obstruction is now pinned to a single,
explicit object: the `psi`-average must be kept below the *sub-maximal* (generic/Haar)
level along the orbit of 27, i.e. **27 must avoid the `D=1`-dominant region (`o≡1 mod4`) in
Cesàro density**. Concretely the proof can no longer be "all orbits"; the next viable
moves are *constrained* ergodic optimization:
1. **Constrained sub-action.** Restrict to invariant measures with `freq(D=1) <= 1/2`
   (equivalently no mass on the trivial cycle / its basin). On that constrained set
   `max ∫ psi <= 0` becomes plausible — but enforcing the constraint for the *specific*
   orbit 27 is itself the open genericity statement.
2. **Repelling-maximizer leverage.** `o=1` is a *repelling* fixed point of the induced
   (expanding) map: 27 provably never enters it (orbit grows). The task is upgraded from
   "avoid a point" to "spend `<1/2` Cesàro density near the `D=1` branch" — strictly
   weaker than full equidistribution, and the right target for a quantitative
   sub-action/transfer-operator estimate (ties back to the self-consistent `‖F‖<1`
   program, `PROOF_STATUS.md`).
3. **Entropy gap.** The maximizer is a zero-entropy (periodic) measure; Haar/the SRB-type
   measure has positive entropy. A pressure/large-deviations bound separating positive-
   entropy orbits from the periodic maximizer is the natural continuation.

**Soundness.** No proof is claimed. §1–§2 are standard theorems; §3 closed-form + 0
numeric mismatches; §4 finite search (capped, so "unique integer cycle" is OBSERVED, not
exhaustively PROVEN, but the expanding-map ratio argument makes it certain for integers).
Labels: criterion **[PROVEN]**, reformulation **[PROVEN]**, `β(psi)=+1/2` **[PROVEN]**
(closed form, realized by the genuine integer point `o=1`), verdict **[PROVEN negative]**.
The 1/4 slack is **insufficient**; the one-sided strategy cannot be made unconditional.
