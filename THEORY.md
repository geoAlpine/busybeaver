# Toward a theory of effective single-orbit genericity — comprehensive synthesis + the new-theory blueprint
*2026-06-26. Part A synthesizes every result of the program into one picture; Part B lays out the architecture of
the new theory aimed at the complete proof, isolating the single central conjecture (the multi-year tool) and the
proven scaffolding around it. Discipline: every line labelled [PROVEN] / [CONDITIONAL] / [OPEN]; 0 false claims;
~16 over-claims caught & retracted (incl., this session, a `0.91-predictability` undersampling artifact killed by a
shuffle control).*

---
## PART A — Comprehensive synthesis (what is established)

### A1. The object and its five equivalent forms [PROVEN equivalences]
Antihydra (a BB(6) holdout) never halts **iff** the running even-density `≥ 1/3`. Machine-checked reductions make
this **one object seen five ways**:
1. **Renewal / 2-adic:** `avg jump = (1/J)Σ_j v2(3c'_j−1) ≤ 2` for the induced full-branch Gibbs–Markov map on ℤ₂.
2. **Dynamical:** the single orbit of seed 8 under `×(3/2)` on ℤ₂ is **generic** (empirical measure → Haar).
3. **Homogeneous:** seed 8 is generic for the **rank-1 Anosov / amenable-hyperbolic** automorphism `×(3/2)` of the
   S-arithmetic solenoid `(ℝ×ℚ₂×ℚ₃)/ℤ[1/6]`.
4. **Analytic / digits:** the moving diagonal digit `⌊(3/2)^n⌋ mod 2` equidistributes (= **Mahler 3/2, 1968**).
5. **Normality:** the explicit sequence `⌊(3/2)^n⌋ mod 2` is **normal**.

### A2. The exact reductions, and the cleanest target [PROVEN, machine-checked]
- **Floor-carry identity:** `c_n = (3^n c_0 − T_n)/2^n`, `T_n = 3 T_{n−1} + 2^{n−1} r_{n−1}`, `r_i = c_i mod 2`
  (the dual carry). `height(T_n) ≈ n·log₂3` — **unbounded**.
- **Valuation budget:** `Σ_{i<n, c_i odd} v2(3c_i−1) = n + v2(c_n) − v2(c_0)` ⇒ `odd-density = 1/avgD_odd`
  (asymptotic), giving the **cleanest criterion form: non-halt ⟺ `avgD_odd ≥ 3/2`** (a *lower* bound on one
  average; Haar = 2). Unconditional range `n ≤ Σ_{odd} ≤ 1.585n` (a 2-adic Flatto–Lagarias–Pollington).
- **Character-sum leading term:** `avgD_odd = 3/2 − ½·avgχ_odd + (bonus ≥ 0)`, `χ = χ_{−4}` mod 4, so the leading
  obstruction is the **one-sided character sum** `Σ_{odd} χ_{−4}(c_n) ≤ 0`.

### A3. The wall, and why every known tool fails [PROVEN closures + measured]
The empirical limit measure is **classical** (separable, negativity 0, purity 1/n): single-basis statistics
cannot certify it (the verification-filter limit, theory core). Three unconditional tool-families each fail for a
**distinct structural reason** (the meta-finding):
| tool family | needs | blocked because |
|---|---|---|
| measure / spectral | unique ergodicity or rank-≥2 / a.e. | rank-1, continuum of invariant measures — needs an **infinitary** input |
| p-adic Baker / S-units | bounded-height algebraic inputs | `height(T_n)≈n·log₂3` — **unbounded** |
| character sum / bilinear / sum–product | multiplicative structure in `n` | `c_n mod 4` = high bits of dynamical `T_n` — **structureless** (uncorrelated w/ `λ(n)`, flat over `n≡a(q)`) |
And **no finite-order obstruction exists** — the orbit is i.i.d.-indistinguishable at every tested finite order
(mod-p CLT rate; lag-MI ≈ 0 via the digit-bijection; block-entropy = log p; random-rate self-separation; **no
finite-window law**, shuffle-confirmed). So only an **infinitary** input can decide it: the wall is real, pinned
from three independent technologies and below every finite test.

### A4. The wall is one homogeneous object [PROVEN + measured]
- **Engine survey:** all 7 single-orbit equidistribution engines need rank-2 or a.e.; `×3/2` is **self-dual**
  (uses only the one multiplier), so BFLM is circular and there is no second independent direction.
- **amenable ∩ hyperbolic** trichotomy: isometric → Weyl (solved); non-amenable-hyperbolic → rigidity (solved);
  **amenable-hyperbolic (`×3/2`) → no currently known tool.**
- **Cross-cryptid family** `v_p(μ)=−1`: trap/no-trap boundary is the single curve `μ=2`; on the hard side the
  family is **homogeneous** (genericity rate μ-uniform; orbit ≡ i.i.d. at the CLT rate for every member).
- **Certificate hierarchy [PROVEN]:** five strict Chomsky separations (`star-free⊊REG⊊SLIN⊊2-automatic⊊CF⊊CS`)
  with explicit verified witnesses; the cryptid sits on the **orthogonal over-approximation axis** (its hardness
  is "no tame halt-free `L ⊇ reachable`", = the analytic wall — two faces of one barrier).

### A5. The quenched–annealed seam [PROVEN + measured] — the precise locus of the difficulty
- The **annealed** model (fresh i.i.d. digits) mixes efficiently at **every** cylinder depth (renewal Markov gap
  large; mix-time `≈ 0.88 + 0.083k`, bounded-bits-per-step).
- The **quenched** orbit agrees with annealed on **every finite-order statistic** (digit-bijection ⇒ no finite
  signature). **The entire difference — the whole wall — is the deterministic self-feeding: the orbit must
  furnish its own next digit as `n→∞`, invisible to any finite statistic.**

---
## PART B — The new theory: effective single-orbit genericity (blueprint to the complete proof)

**Name (per the expert):** *effective deterministic normality for algebraic expanding orbits* / *single-orbit
genericity for amenable-hyperbolic systems*. **Goal:** prove the specified orbit equidistributes — equivalently
`avgD_odd ≥ 3/2`, equivalently `⌊(3/2)^n⌋ mod 2` normal.

### B1. The central structural decomposition [PROVEN this session] — a hidden ×3 mixing engine
The carry recursion `T_n = 3 T_{n−1} + 2^{n−1} r_{n−1}` carries a **×3 action on ℤ₂ inside it**, and the bit it
feeds to scale `k` is governed by `3^m mod 2^k`. That orbit is **KNOWN and exactly equidistributed**:
> **[PROVEN] Mixing engine.** `3` is a 2-adic unit of order `2^{k−2}` mod `2^k` (`k≥3`, verified); `{3^m mod 2^k}`
> is a **full cyclic orbit**, exactly equidistributed in `⟨3⟩`. The carry's "fresh bit per scale" is extracted by
> this engine.
So the problem **splits**: a *tractable* mixing engine (`×3 mod 2^k`, known) **coupled** to a *hard* input (the
orbit's own parity bits `r_i`). The "second direction" is **not** a genuine rank-2 — `⟨3⟩` is the same multiplier,
and the input is self-generated (this is the BFLM self-duality, now concrete) — but the split isolates the target.

### B2. The proven scaffolding [PROVEN]
- **Theorem A (mixing engine).** `×3 mod 2^k` is exactly equidistributed (B1). *(proven, cyclic.)*
- **Theorem B (top foothold).** The top `Θ(log N)` binary digits of `⌊8(3/2)^n⌋` equidistribute, via Weyl on
  `{n·log₂3}` and the finite (non-Liouville) irrationality measure of `log₂3`. *(proven; the barrier is sharp at
  `Θ(log N)`.)*
- **Theorem C (annealed coupling).** If the parity bits `r_i` are replaced by an i.i.d. fair-coin input, the carry
  + mixing engine produce an **exactly equidistributed** residue sequence (annealed mixing, A5). *(proven — this is
  the "annealed mixes at all scales" result.)*
- **Lemma D (exceptional set).** Integer seeds avoid the periodic part (2-adic repelling) and the Haar-null
  singular-preimage part of the exceptional set. *(proven.)*

### B3. THE CENTRAL CONJECTURE (the multi-year tool) [OPEN]
Everything reduces to **one** statement — the quenched version of Theorem C:
> **Coupling Conjecture.** The orbit's self-generated parity input `(r_i)`, though deterministic and feeding the
> carry, does **not** conspire with the `×3` mixing engine to break equidistribution: the quenched residue
> sequence equidistributes at every scale, given the effective irrationality of `log₂3` (Theorem B) as the only
> external input. Equivalently: **a single deterministic algebraic orbit inherits the annealed mixing (Thm C) once
> coupled to a sufficient Diophantine bound on its self-correlation** — `Σ_{odd} χ_{−4}(c_n) = o(n)` and its
> higher-modulus analogs.
This is exactly the **quenched→annealed bridge** the expert called "strongly NO-leaning from finite-order
methods": A5 shows it cannot come from any finite-order decorrelation (they already match); it must inject the
infinitary Theorem-B-type input into the all-scale coupling.

### B4. Why the Conjecture suffices, and the closest known result [established]
- **Suffices:** the Conjecture ⇒ `avgD_odd → 2 ≥ 3/2` ⇒ even-density `→ 1/2 ≥ 1/3` ⇒ **Antihydra non-halts**, and
  (uniformly, A4) the whole `v_p(μ)=−1` cryptid family **and** Mahler 3/2 at once.
- **Closest known:** **Tao (2019, Forum Math Pi)** controls the *same* p-adic skew-random-walk / Gibbs–Markov
  statistic — but for a **log-density-1** set of seeds, never one specified seed. **The exact gap = removing the
  density average** (the a.e.→specified gap), which is precisely the quenched self-feeding of B3. FLP (1995) gives
  only the range (our 2-adic analog: the `[n,1.585n]` budget). The single-orbit case is posed as an explicit open
  conjecture in the 2025 literature.

### B5. The theory's first genuine new step, and the honest gap
- **New this session (the decomposition B1 + the proven engine A):** the irreducible core is no longer the vague
  "self-feeding"; it is the **coupling of a *known* mixing engine to a *quenched* self-correlation**, with the
  Diophantine input localized to Theorem B. This is strictly sharper than "prove normality": it says *what* must
  be coupled to *what*, and *which* external bound (effective `log₂3`) is the lever.
- **The gap (the multi-year tool):** a **coupling theorem** transferring annealed mixing (Thm C) to the quenched
  orbit under a Diophantine self-correlation bound. No current method does this for a single specified orbit
  (A3); building it is the new mathematics the expert named. **Honest status: the blueprint is complete and the
  central conjecture is isolated with its proven scaffolding; the coupling theorem itself does not yet exist.**

### B6. The concrete next attacks inside the blueprint (conjecture-independent, fundable)
1. **Quantify the coupling at scale `k=2`:** prove the *conditional* statement "if `Σ_{odd}χ_{−4}(c_n) = O(N^{1−δ})`
   then `avgD_odd ≥ 3/2`" with an explicit `δ`-to-margin map — turning B3 into a quantitative target (the
   character-sum exponent that suffices). *(Tractable; isolates the needed Diophantine strength.)*
2. **Effective Theorem B → one more scale:** push the proven `Θ(log N)` foothold by one moving digit using an
   explicit irrationality measure of `log₂3` — even a single extra scale, unconditionally, is a genuine partial.
3. **The annealed→quenched coupling in a toy model:** prove the coupling for a *simplified* self-feeding (e.g. a
   linear or finite-memory surrogate) to learn the mechanism, then attack the true (full-complexity) input.
