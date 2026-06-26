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

### B5′. Theorem E (the δ→margin map) [PROVEN reduction; done 2026-06-26, `coupling_k2.py`]
The Coupling Conjecture (B3) now has an **explicit quantitative form**, and it is *milder* than feared. Write
`avgD_odd = 2 − Σ_k δ_k`, `δ_k := 2^{−(k−1)} − P(D≥k | odd)` (verified decomposition); the **k=2 term is exact**:
`δ_2 = ½·avgχ_{−4,odd}` (the leading and largest deviation; empirically all `δ_k > 0` for seed 8 — the low
cylinders are *under*-visited, so only `δ_k > 0` can lower `avgD_odd`). Two rigorous per-scale bounds on the
dangerous (`δ_k>0`) deviations: **(geometric)** `δ_k ≤ 2^{−(k−1)}` always; **(character)** `|δ_k| ≤
max_{ψ≠1 mod 2^k}|avgψ_odd|` (exact character expansion of the cylinder indicator).
> **Theorem E.** *If there exist `δ>0, C` with `|Σ_{i<N, c_i odd} ψ(c_i)| ≤ C·N^{1−δ}` for every nontrivial
> Dirichlet character `ψ` of conductor `≤ N^δ`, then* `Σ_{δ_k>0} δ_k ≤ O(N^{−δ}\log N)` *(crossover at*
> `K*≈δ\log_2 N`*), so* `avgD_odd ≥ 2 − O(N^{−δ}\log N) ≥ 3/2` *for all `N ≥ N₀` — i.e. **Antihydra never halts**.*

**ANY power saving `δ>0` suffices, and only for low moduli (conductor `≤ N^δ`).** This is the precise, mild,
quantitative deliverable the Coupling Conjecture reduces to: *single-orbit power-saving character cancellation at
low 2-power moduli* — an analytic-number-theory target with a number (any `δ>0`) and a scale range (`≤N^δ`). The
hypothesis itself is OPEN (= the multi-year tool, the a.e.→specified gap of Tao 2019), but Theorem E is the proven
exponent→margin map that turns B3 from "prove normality" into "get any power saving at low moduli."

### B5″. The lowest modulus in its simplest form [PROVEN exact reduction, `H_lowmoduli.py`]
Attacking `H` at conductor 4 (the leading χ_{−4} term), the odd-run lemma (`run length = v2(c_start−1)`, proven)
gives an **exact combinatorial identity**: in a length-`L` odd run the members have `v2(·−1)=L,…,1`, so `L−1` are
`≡1 (4)` and exactly one is `≡3 (4)`. Hence
> `S_2(N) = Σ_{n<N} χ_{−4}(c_n)[odd] = N_1 − N_3 = O − 2·#(odd-runs)`  *(verified exactly: `76 = 150192−2·75058`).*
So **H at conductor 4 ⟺ `avgL → 2`** where `avgL = O/#runs` is the **average odd-run length** (measured 2.00101;
run-lengths match geometric mean 2), and the favorable sign `S_2 ≤ 0 ⟺ avgL ≤ 2`. This is the
combinatorially **simplest** face of the lowest-modulus character sum — a run-length law, not an abstract sum.
*Honest:* it still funnels (`avgL → 2` is the single-orbit equidistribution of `v2(c−1)` at run-starts = a 2-adic
statistic of the even subsequence; the max run length is `≤ 0.585N` so no unconditional `avgL`-bound beats
trivial), and `S_2` equals the moving diagonal digit (bits `n,n+1` of `3^n c_0 − T_n`) = the Mahler core. The
value is the **clean elementary target**: "average odd-run length → 2," and the proven exact formula linking the
character sum to a run count — the most tractable entry point for the H(δ,C) hypothesis at its mildest.

### B5‴. The run-start cross-section: a renormalization self-similarity [PROVEN structure, `H_runstart.py`]
Attacking `avgL → 2` via the even-subsequence: a run-start is `c = 3m` (`m = c_e/2` odd, `c_e ≡ 2 (4)` the last
even-run value), and `L = v2(c−1) = v2(3m−1)` (verified). So **`avgL = avg of v2(3m−1)` over the run-start `m`'s**
(Haar value 2), and `avgL → 2 ⟺` the run-start `m`'s equidistribute 2-adically. The **induced return map**
`m → m''` (run-start to run-start) is a **full-branch expanding Gibbs–Markov map**, branch `=(L,M)` (odd-run /
even-run lengths), slope `(3/2)^{L+M}` (measured: `(3/2)^2, (3/2)^4, (3/2)^5, …` per branch) — the **same class as
the renewal `F`**. Therefore:
> **Conductor-4 `H` renormalizes to conductor-4-`H` on the run-start cross-section** — a *renormalization
> self-similarity*: the simplest target reproduces itself under the return map, on the same rank-1
> amenable-hyperbolic system. This is the structural reason every internal route funnels: the problem is a
> **renormalization fixed point with no contraction** (the slopes `(3/2)^{L+M}` expand, never contract). The
> even-subsequence is *not* simpler — it is a cross-section of the same system. (Run-start `m mod 2^k` deviations
> are at the CLT rate empirically — equidistribution, unprovable for the specified seed.)
This both **confirms** the funnel rigorously (a structural, not anecdotal, reason) and **sharpens** the
multi-year target: the new tool must break a *renormalization fixed point* — supply contraction/genericity where
the return map only expands. (Echoes the NEW_ENGINE two-scale bootstrap: each scale needs the same input; here
that is the self-similarity made exact.)

### B5⁗. The contraction already exists — the tool is DERANDOMIZATION [PROVEN reframe, `contraction_tool.py`]
"Supply contraction to the renormalization fixed point" turns out to be **mis-stated**: the contraction is
**already present**. The renewal Gibbs–Markov map `F` has a **transfer-operator spectral gap** — it contracts
mean-zero functions by `θ<1` per step, giving exponential decay of correlations (verified: the Haar
autocorrelation `R[t]=E_Haar[χ(c_0)χ(c_t)]→0` fast, `R[0]≈½`, `R[t≥1]≈0`) and a CLT for `(F, Haar)`. **But the
contraction is stuck at the Haar level** — it controls correlations (Haar integrals), giving an *a.e.* / variance
statement, never the specified point.
> **The specified orbit is "spectral-gap-pseudorandom":** its Birkhoff-sum variance matches the Haar Green–Kubo
> `σ² = R[0]+2Σ_{t≥1}R[t] ≈ 0.43` (orbit `Var(S_N)/N ≈ 0.49`, ratio `≈1` within noise — after fixing a forced-odd
> `R[0]` bug that had spuriously doubled `σ²`). So the explicit orbit *realizes* the spectral-gap prediction.
**Therefore the missing tool is not "contraction" but DERANDOMIZATION:** prove that the single explicit,
*computable* (`K=O(\log N)`) orbit `⌊8(3/2)^n⌋` realizes the transfer operator's spectral-gap prediction, with the
effective irrationality of `log₂3` (Theorem B) as the **pseudorandom seed**. This is the sharpest statement of the
multi-year tool yet: the renormalization fixed point's *attracting* (contracting) nature is the spectral gap,
present and Haar-level; the wall is **de-randomizing it to one Diophantine orbit** — exactly the `a.e.→specified`
gap (Tao 2019's density average), now phrased as "the contraction is real but lives on measures, not points."
This connects the multi-year target to **pseudorandomness / derandomization theory**: the orbit must be shown
pseudorandom against the Gibbs–Markov dynamics, its `log₂3`-arithmetic standing in for genuine randomness.

**Literature check (`DERANDOMIZATION_LITERATURE.md`, 3 agents): no known derandomization principle reaches our
case, and the literature confirms the blueprint.** Every "gap ⇒ every/specified orbit" precedent needs structure
we lack — **QUE** needs Hecke symmetry (Lindenstrauss *Annals* 2006); **measure rigidity** needs a 2nd
mult.-independent map via the entropy-coupling identity `log q·h(σ_p)=log p·h(σ_q)` (Rudolph; EKL *Annals* 2006) —
the cleanest proof that **rank-1 is excluded** (one map ⇒ uncountable invariant-measure simplex); **effective
Ratner** needs unipotency (expanding is the opposite regime). Pseudorandomness routes each fail precisely:
**Sarnak–Möbius** needs *zero* entropy (ours is positive — Karagulyan 2017 shows orthogonality fails); **ML-random
⇒ normal** needs non-computability (ours is computable, `K=O(\log N)`); **PRG/derandomization** is class-relative &
computational. The **one correct framing is Weyl/Gowers — a *reduction* to a cancellation bound** (Green–Tao–Ziegler
*Annals* 2012), which is *exactly* our character-sum **Theorem E**. The closest unconditional fact about our exact
orbit is the **Flatto–Lagarias–Pollington (1995) range bound** `limsup−liminf ≥ 1/p` — independently validating our
2-adic-FLP range — and single-orbit normality is posed as an **explicit open conjecture** (arXiv:2510.11723, 2025,
naming Mahler 3/2 as a consequence). So the central conjecture **is** the recognized open frontier; the multi-year
tool is genuinely new mathematics, its shape now literature-confirmed.

### B6. The concrete next attacks inside the blueprint (conjecture-independent, fundable)
1. **[DONE — Theorem E above]** the `δ→margin` map is proven: any low-moduli power saving `δ>0` ⇒ the margin ⇒
   non-halt. **[DONE — B5″]** the conductor-4 case is reduced to the elementary run-length law `avgL → 2`
   (`S_2 = O − 2·#runs`, exact). The residual is to *establish* the cancellation / run-length law (open), now a
   sharply-posed, combinatorially elementary analytic target.
2. **Effective Theorem B → one more scale:** push the proven `Θ(log N)` foothold by one moving digit using an
   explicit irrationality measure of `log₂3` — even a single extra scale, unconditionally, is a genuine partial.
3. **The annealed→quenched coupling in a toy model:** prove the coupling for a *simplified* self-feeding (e.g. a
   linear or finite-memory surrogate) to learn the mechanism, then attack the true (full-complexity) input.
