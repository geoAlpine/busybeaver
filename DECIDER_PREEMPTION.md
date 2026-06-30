# Is the bbchallenge decider framework a weapon against Antihydra, or pre-empted by No-Structure? (2026-06-30)

*Maps the entire bbchallenge automata-theoretic decider taxonomy — the toolset that proved BB(5)=47,176,870 and decided
almost all of BB(6) — onto the program's `[PROVEN]` No-Structure-Only-Selection theorem (`BB6_NO_STRUCTURE_THEOREM.md`,
registers (C1)/(C2)/(C3)). SOUNDNESS DISCIPLINE: every verdict labelled. Deciders are SOUND non-halting provers; the claim
here is never "a decider is wrong" but "no decider in the known classes CAN succeed on Antihydra, for a proven structural
reason." We distinguish `[EMPIRICAL]` ("no known decider works") from `[PROVEN]`/`[ARGUED]` ("no decider of type X can
work"). The kernel `(K)` stays `[OPEN]` = Mahler 3/2 / AEV. NOT committed by default.*

---

## §0. Verdict

**The bbchallenge decider framework is NOT a genuine untried weapon against Antihydra. It is pre-empted by the No-Structure
theorem — but the pre-emption splits cleanly into two registers, and only one of them is closed by a fully `[PROVEN]`
argument; the other (the weighted/counter class) is `[ARGUED]` modulo one named gap.**

Concretely, every decider in the known taxonomy emits a certificate of exactly one of two kinds, and each kind maps to a
ruled-out No-Structure register:

- **Kind R — regular / finite-state closed-tape-language certificate** (Cyclers, Translated Cyclers, Backward Reasoning,
  Halting Segment, Closed Tape Language, FAR, MITM-DFA, n-gram CPS/CPS, Bouncers). This is a topological all-configurations
  invariant ⟶ **register (C2)**. **`[PROVEN]`-grade pre-empted**: the Antihydra "safe" set `{balance_n ≥ 0}` is a
  count-comparison set `{3·#even ≥ #total}`, provably **non-regular**, and the reachable-configuration language has the
  orbit's full subword complexity `p(ℓ)=2^ℓ` / positive entropy (`MINPROP_COUPLING.md`). A regular closed over-approximation
  is therefore either unsound (contains a halting configuration — so the closure check fails, no certificate issues) or does
  not exist. This is exactly (C2).

- **Kind W — weighted / affine-counter certificate** (Weighted FAR, MITM-WFA). This computes a numeric weight (a rational
  recognizable series) on tape configurations and can *exactly track the unbounded counter* `balance_n` — it escapes the
  "regular can't compare counts" barrier that kills Kind R. It maps to **register (C1)** (a finitely-represented sub-action /
  Lyapunov function). **`[ARGUED]`-grade pre-empted**: a WFA non-halting certificate is equivalent to a finite-dimensional
  sub-action `g` with a per-step inequality `ψ ≤ g∘T − g`; such `g` exists iff `sup_ν ∫ψ dν ≤ 0`, which **fails at the fixed
  point `o=1`** (`β = +1/2 > 0`, `MINPROP_COBOUNDARY_LP.md`). The unbounded magnitude-aware extension
  `g = α·log₂o + bounded` is also closed by the proven sign-tension no-go (`MAGNITUDE_LYAPUNOV.md`, `ADELIC_SUBACTION.md`).

**The clean statement we can rigorously back:** *No regular/finite-state decider (Kind R) can prove Antihydra non-halting,
because non-halting is a non-regular count-comparison / full-complexity condition — this is the `[PROVEN]` (C2) obstruction,
and it explains the empirical Cryptid status of every regular decider. The weighted/counter deciders (Kind W) reduce to the
`[PROVEN]`-infeasible bounded/magnitude-aware sub-action (C1), so they too cannot succeed — this is `[ARGUED]`, with the sole
residual gap being the exact closure semantics of MITM-WFA (whether its certificate is strictly a finite-dimensional linear
ranking function; the literature says yes).* The honest gap is stated in §3.3 and §4.

**No decider class genuinely escapes** on inspection. The closest candidate to an escape — MITM-WFA, the one decider built
to handle "irregular" machines — is precisely the one that lands on (C1), the register the program spent the most effort
closing (including the unbounded/adelic extension). Any *future* decider that escapes would, by the dichotomy, have to emit a
certificate that reads orbit-specific arithmetic (= solve a fragment of `(K)`), which is by definition no longer a
finite-state/affine decider.

---

## §1. The decider taxonomy and its certificate kind

bbchallenge deciders are **sound** semi-deciders: each outputs HALT / NONHALT / UNKNOWN, specialised to one *type* of
non-halting behaviour, and a NONHALT verdict comes with a machine-checkable certificate. The official S(5) pipeline used
Cyclers, Translated Cyclers, Backward Reasoning, Halting Segment, FAR, and Bouncers; the broader CTL/CPS/WFA family extends
these. For each, the one-line certificate kind:

| Decider | Certificate kind | Class |
|---|---|---|
| **Cyclers** | An exactly repeating full configuration (period detection) — a single periodic point. | R (periodic) |
| **Translated Cyclers** | Two record configurations identical on a window at distance L ⟹ shift-periodic orbit. | R (eventually periodic, shifted) |
| **Backward Reasoning** | Bounded backward BFS from halting configs finds no path to start ⟹ halt unreachable in k steps. | R (local/finite) |
| **Halting Segment** | A fixed-width tape segment must precede any halt; it never arises ⟹ regular window invariant. | R (regular window) |
| **Closed Tape Language (CTL)** | A regular language (two DFAs L,R + accept set A) over tape configs, **closed under the TM step** and excluding the halting set. | R (regular tape-language invariant) |
| **n-gram CPS / Closed Position Set** | A finite set of n-gram contexts closed under one step (closure/fixed-point check). | R (regular finite-context invariant) |
| **Finite Automata Reduction (FAR)** | An NFA (boolean semiring) recognising a regular superset of eventually-halting configs; start ∉ language. | R (regular co-CTL invariant) |
| **MITM-DFA** | Meet-in-the-middle construction of the same regular separating language (DFA at the head). | R (regular tape-language invariant) |
| **Bouncers** | An affine description of "walls drifting apart" — piecewise-linear growing periodic configuration. | R (affine-periodic configuration) |
| **Weighted FAR / MITM-WFA** | A **weighted** automaton (semiring weights, finite linear representation) — a numeric/rational-series score on configs; decides "irregular" TMs FAR cannot. | **W (affine/counter sub-action)** |

The dividing line is decisive and is stated by bbchallenge itself: MITM-WFA exists *specifically* "to decide irregular TMs
which cannot be decided by FAR or any other regular decider." So Kind R = regular tape-language / topological invariant; Kind
W = weighted (counter / affine / sub-action) invariant. Antihydra is irregular, so only Kind W is even a candidate; Kind R is
eliminated structurally below, and Kind W is the one to stress-test.

---

## §2. Per-class mapping to (C1)/(C2)/(C3), with verdicts

Recall the No-Structure registers (`BB6_NO_STRUCTURE_THEOREM.md` §2): **(C1)** bounded residue sub-action (coboundary)
`ψ ≤ g∘T − g`; **(C2)** universal/all-orbits topological certificate (`limsup (1/N)Σψ ≤ 0` for every orbit, no data
singling out `o₀`); **(C3)** measure-level/annealed (Haar/Bernoulli a.e.). The violation observable is `ψ = ½ − 1{D≥2} −
1{D≥3}`, with `(K) ⟺ limsup (1/N)Σψ_j ≤ 0`, `∫ψ dHaar = −1/4`.

### 2.1 Regular / finite-state deciders (Cyclers, TC, Backward, Halting Segment, CTL, FAR, MITM-DFA, CPS) → (C2)

**Verdict: CANNOT prove Antihydra non-halting. `[PROVEN]`-grade, mapping to (C2).** Two independent kills:

*(a) Periodicity kills Cyclers / Translated Cyclers / Bouncers-as-periodic.* `[PROVEN]` in-program: the integer orbit
`c_{n+1}=⌊3c_n/2⌋` is **strictly increasing** and reaches no cycle (periodic-itinerary exclusion: the only integer cycle
points are `{0,1}`; all 2046 cycles of period `q≤10` checked + general bound, `BB6_FRAMEWORK_PACKAGE.md` §2). A Cycler needs
an exactly repeating configuration; a Translated Cycler needs a shift-periodic one; a Bouncer needs the displacement to be an
*exact affine* function of step. Antihydra's growth is governed by the Collatz-like depth sequence `D_j`, which is
non-periodic (full subword complexity, below), so no exact period or affine wall law exists. These deciders provably never
fire.

*(b) The non-halting safe set is non-regular ⟹ no closed regular tape language (CTL/FAR/MITM-DFA/CPS/Halting-Segment).* This
is the heart of the (C2) mapping. A FAR/CTL/CPS NONHALT certificate is, by construction, a **regular language `L` of tape
configurations that is closed under the TM transition and contains the start but no halting configuration** (equivalently a
co-CTL regular over-approximation of the halting set not containing start). For Antihydra:

  1. **The safe set is a count-comparison set.** Non-halting `⟺ balance_n := 3·#even − n ≥ 0 ∀n ⟺ #even/#total ≥ 1/3`
     (`[PROVEN]`, Link 0). The maintained counter `balance_n` lives on the tape in unary. The set of configurations from
     which the machine does not halt is governed by `{3E ≥ O}` — a comparison of two unbounded counts, the prototype of a
     **non-regular** (not even context-free-trivial) language. A DFA pair cannot enforce `3E ≥ O` for unbounded `E,O`
     (pumping). `[PROVEN]` (elementary).
  2. **The reachable-configuration language has full complexity.** The orbit's residue word `(o_j mod 2^k)` has subword
     complexity `p(ℓ)=2^ℓ` and the system has the specification property with a full-Hausdorff-dimension set of distinct
     itineraries (`MINPROP_COUPLING.md`). The reachable-config language is therefore non-regular with positive entropy.
  3. **Soundness forces the dichotomy.** Any candidate regular `L` is either (i) too tight — it fails to be closed under the
     step (some reachable config exits `L`), so the closure check fails and *no certificate is emitted*; or (ii) loose enough
     to be closed but then, being a regular over-approximation of the non-regular safe set, it must **leak across the
     `3E≥O` boundary and include a configuration from which the machine halts** — which a *sound* decider's closure check
     rejects. There is no third option: a regular `L` cannot coincide with the non-regular safe set. Hence no valid regular
     certificate exists. `[ARGUED, structural]` (rests on (1)-(2) `[PROVEN]`).

This is **exactly register (C2)**: a closed regular tape language proves non-halting for *every* configuration it contains —
it is an all-orbits / topological invariant, blind to data singling out `o₀=27`. By the No-Structure theorem (C2) is
impossible because the property is non-universal (a full-dimension set of orbits violates `(K)`, including arbitrarily close
itineraries that realise low-depth `δ₁`-like behaviour and halt). A finite-state device cannot separate `o₀`'s orbit from
those. **This is the proven reason the empirical Cryptid status holds for every regular decider.**

### 2.2 Backward Reasoning / Halting Segment → (C2), local-finite sub-case

**Verdict: CANNOT. `[PROVEN]`-grade.** These prove non-halting only when the halting configurations are unreachable within a
*bounded* backward depth / a fixed tape window. Antihydra's halt (counter underflow) is reachable in principle from
configurations of unbounded `balance`, at unbounded distance from the start; no finite backward horizon or fixed segment
certifies its absence. Degenerate special case of (C2) (finite ⊂ regular). Provably never fires.

### 2.3 Weighted deciders (Weighted FAR, MITM-WFA) → (C1)

**Verdict: CANNOT prove Antihydra non-halting. `[ARGUED]`-grade, mapping to (C1), with one named residual gap (§3.3).**

This is the only class that is not killed by §2.1, because a **weighted** automaton *can* compare counts: over an integer (or
min-plus) semiring it computes a rational recognizable series `f(w) = λ·M_{w_1}⋯M_{w_n}·γ`, and can represent the unbounded
counter `balance_n` exactly. So the "regular can't compare counts" barrier (§2.1) does not apply. The right question (Task 2)
is: **can a WFA track an unbounded counter whose non-negativity hinges on an asymptotic density?** Answer: it can *track* the
counter, but it cannot *certify* the non-negativity, for the (C1) reason.

*The reduction WFA-certificate ⟶ (C1) sub-action.* A WFA NONHALT certificate is a finite-dimensional weight function `W` on
configurations together with a verified per-step relation guaranteeing that the start has a weight that the halting set never
attains. Strip the GAP-LEMMA bookkeeping (`BB6_FRAMEWORK_PACKAGE.md` §2, Links 1–3) and this is, on the induced 2-adic map
`T`, a function `g` on residues/configurations with a per-step inequality controlling the increment of the violation
observable: `ψ(o) ≤ g(T o) − g(o)`. A *bounded* finite-state weight is exactly a **(C1) bounded residue sub-action**; an
*unbounded* weight linear in the configuration size is exactly the **magnitude-aware sub-action** `g(o)=α·log₂o + h(o mod
2^k)`. Both are `[PROVEN]` infeasible:

  - Bounded `g`: exists iff `sup_ν ∫ψ dν ≤ 0` over `T`-invariant `ν` (LP duality / max-mean-cycle). The fixed point `o=1`
    (`T(1)=1`, `D=1`, `ψ=+½`) gives an atomic `δ₁` with `∫ψ dδ₁ = +½ > 0`, a weight-`+½` self-loop at residue `1` for every
    `k≥3`. LP infeasible at every level (exact `Fraction`, `k=3..12`, tail-audited, `MINPROP_COBOUNDARY_LP.md`). `[PROVEN]`.
  - Unbounded magnitude-aware `g`: sign tension — useful telescoping (exploiting `log₂o_N→∞`) needs `α<0`, but `α<0` is
    infeasible (constant-`D=d` measures give `∫ψ̃→+∞`); the feasible `α≥0.855` makes the bound vacuous. The conditional
    `o>M₀` threshold does not escape (`D=v₂(3o−1)` is unbounded at arbitrarily large `o`), and the adelic 3-place version is
    killed by the product formula (`MAGNITUDE_LYAPUNOV.md`, `ADELIC_SUBACTION.md`). `[PROVEN]`.

So whatever finite linear representation a WFA uses, the existence of its certifying weight implies a sub-action of one of
these two forms, and both are proven not to exist. **A WFA can compute `balance_n` but cannot finitely certify that it stays
≥ 0, because that non-negativity is equivalent to the density condition `(K)`, which is not determined by any
finite-dimensional linear/affine closure** — it is a second-moment/frequency fact (`MINIMAL_CORE_2ADIC.md` §4), exactly the
content the (C1) LP and the magnitude-Lyapunov no-go prove a sub-action cannot capture.

### 2.4 Measure-level (C3)

No bbchallenge decider is a (C3) certificate — deciders are deterministic finite proofs, not ergodic/annealed arguments. (C3)
is listed for completeness of the No-Structure registers; it rules out the *probabilistic* "halts with probability
4.84×10⁻²²⁴³⁹⁴³⁹⁵" heuristic as a proof, but that heuristic is not a decider. So (C3) is vacuously not a route through the
decider framework, and the decider framework lives entirely in (C1)∪(C2).

---

## §3. The pre-emption theorem

### 3.1 Statement

> **Theorem (Decider pre-emption — conditional on the certificate taxonomy). `[ARGUED]`, with `[PROVEN]` core on Kind R.**
> Let `Antihydra` be the BB(6) machine and let its non-halting be the criterion `(K): balance_n ≥ 0 ∀n` (equivalently
> `liminf` even-density `≥ 1/3` `⟺ mean D ≥ 3/2`, `[PROVEN]`-equivalent). Every NONHALT certificate produced by a decider in
> the known bbchallenge taxonomy is either
>   - **(R)** a regular closed tape-language invariant (Cyclers, Translated Cyclers, Backward Reasoning, Halting Segment,
>     CTL, FAR, MITM-DFA, n-gram CPS, Bouncers), which is a register-**(C2)** all-configurations topological certificate; or
>   - **(W)** a weighted/affine finite-dimensional sub-action (Weighted FAR, MITM-WFA), which is a register-**(C1)**
>     (possibly magnitude-aware) coboundary certificate.
>
> Both registers are ruled out by the No-Structure-Only-Selection theorem: (C2) is impossible (`(K)` is non-universal —
> violated on a full-Hausdorff-dimension set of orbits including the halting fixed point `o=1`), and (C1) is infeasible (the
> `o=1` ergodic-optimization maximizer has `ψ`-weight `β=+½ > 0`, so the bounded sub-action LP is infeasible at every level,
> and the unbounded magnitude-aware/adelic extension is closed by sign tension + the product formula). **Therefore no decider
> in the known classes can prove Antihydra non-halting. The Cryptid status is structural, not a gap in engineering.**

### 3.2 Proof sketch

The classification R/W is read off the taxonomy table (§1): the certificate kind is regular (boolean-semiring automaton /
periodic configuration / finite window) for every class except the weighted ones, which are the explicitly-"irregular"
class. The map R ⟶ (C2) is §2.1: a closed regular tape language excluding the halting set is an all-orbits topological
invariant; (C2)'s impossibility is `[PROVEN]` (`BB6_NO_STRUCTURE_THEOREM.md` §3.2, multifractal/specification
non-universality), and the *concrete* obstruction for Antihydra is that the safe set `{3E≥O}` is non-regular while the
reachable language has full complexity (§2.1(1)-(3)). The map W ⟶ (C1) is §2.3: a WFA certificate's weight function is a
finite-dimensional sub-action, bounded or `log`-affine; (C1)'s infeasibility is `[PROVEN]` for both forms
(`MINPROP_COBOUNDARY_LP.md`, `MAGNITUDE_LYAPUNOV.md`, `ADELIC_SUBACTION.md`). The union (C1)∪(C2) exhausts the framework
because no decider is a (C3)/annealed object (§2.4). ∎ (modulo §3.3)

### 3.3 The residual gap (honest)

The theorem is `[PROVEN]`-grade on Kind R and `[ARGUED]`-grade on Kind W. The two gaps:

1. **Taxonomy completeness is empirical, not closed.** "Every decider is (R) or (W)" ranges over the *known* classes. A
   genuinely new decider emitting a certificate that is neither a regular tape-language nor a finite-dimensional weighted
   sub-action is not covered. By the obstruction dichotomy (`BB6_OBSTRUCTION_DICHOTOMY.md`), any such certificate that
   *succeeds* would have to read orbit-specific arithmetic (separate `o₀` from `δ₁` and the violating family) — i.e. it
   would internalise a fragment of `(K)` = Mahler 3/2 / AEV, and so would no longer be a finite-state/affine decider but a
   solver of the open arithmetic. This is a meta-argument, not a closed theorem; it is the honest boundary of the claim.
2. **The W ⟶ (C1) reduction depends on MITM-WFA's exact closure semantics.** The bbchallenge MITM-WFA wiki is a stub; we
   could not pin, to the last detail, that its certificate is *strictly* a finite-dimensional linear ranking function over a
   ring/min-plus semiring (the general WFA literature — rational/recognizable series — strongly indicates it is). IF it is,
   the reduction to a sub-action is exact and (C1) closes it. The only conceivable escape would be a WFA whose weight is an
   unbounded magnitude-aware function with a *useful* sign — and that is precisely what `MAGNITUDE_LYAPUNOV.md` /
   `ADELIC_SUBACTION.md` already prove cannot exist (sign tension; product formula). So even the escape route is closed,
   conditional on the certificate being a sub-action at all. This is the one place to verify against the actual MITM-WFA
   implementation before upgrading W to `[PROVEN]`.

---

## §4. Honest scope

**What this establishes.**
- The decider framework is **pre-empted, not untried**: it splits exactly into the (C2) and (C1) registers the No-Structure
  theorem rules out. The empirical fact that no bbchallenge decider fires on Antihydra is explained by a structural reason,
  not by insufficient compute or unwritten code.
- Kind R (all regular/finite-state/periodic deciders — the overwhelming majority, including FAR/CTL/CPS/MITM-DFA that
  decided almost all of BB(6)) is `[PROVEN]`-grade dead on Antihydra: the safe set is non-regular and the orbit has full
  subword complexity, so no closed regular tape language is both sound and tight. This is the (C2) obstruction made concrete.
- Kind W (the weighted/counter deciders — the only ones designed for irregular machines) is `[ARGUED]`-grade dead: its
  certificate is a finite-dimensional sub-action, and (C1) is `[PROVEN]`-infeasible (bounded and magnitude-aware/adelic).

**What this does NOT establish.**
- It does **not** say any decider is unsound or gives a wrong answer. Deciders are sound; they simply (provably, for Kind R;
  arguably, for Kind W) never reach a NONHALT certificate for Antihydra.
- It does **not** prove `(K)` is undecidable, independent, or false — only that it is unreachable from finite-state/affine
  (= decider-framework) data. A proof using orbit-specific 2-adic arithmetic (solving Mahler 3/2 / AEV) is not precluded.
- It does **not** close the taxonomy against a fundamentally new certificate kind (§3.3.1), nor fully pin MITM-WFA's closure
  semantics (§3.3.2). These are the two honest gaps; both are bounded by existing `[PROVEN]` no-gos.
- `[EMPIRICAL]` "no known decider works" is upgraded here to `[PROVEN]` "no regular decider CAN work" (Kind R) and
  `[ARGUED]` "no weighted decider CAN work" (Kind W). It is **not** upgraded to an unconditional "no decider whatsoever can
  ever exist," which would require closing §3.3.1.

**One-paragraph external form.** *For Antihydra, non-halting is the count-comparison/density condition `3·#even ≥ #total`
forever — a non-regular, full-subword-complexity, second-moment fact. Regular deciders (Cyclers/CTL/FAR/MITM-DFA/CPS/
Bouncers) emit closed regular tape-language invariants, which are topological all-orbits certificates (register C2); these
provably cannot exist here because a regular over-approximation of a non-regular safe set either breaks closure or includes a
halting configuration. Weighted deciders (MITM-WFA) emit finite-dimensional affine/counter sub-actions (register C1); these
provably cannot exist here because the halting fixed point `o=1` is an ergodic-optimization maximizer of positive
`ψ`-weight (+½), making the sub-action LP infeasible at every finite level, and the unbounded magnitude-aware extension is
killed by sign tension and the adelic product formula. Hence the decider framework is structurally pre-empted, and
Antihydra's Cryptid status is a theorem-level consequence, not an engineering gap.*

**No machine decided. No label upgraded.** `(K)` remains `[OPEN]` = Mahler 3/2 / AEV.

---

## Sources (decider literature)

- bbchallenge wiki: [Closed Tape Language](https://wiki.bbchallenge.org/wiki/Closed_Tape_Language),
  [MITMWFAR](https://wiki.bbchallenge.org/wiki/Meet-in-the-Middle_Weighted_Finite_Automata_Reduction_(MITMWFAR)),
  [Closed Position Set](https://wiki.bbchallenge.org/wiki/Closed_Position_Set), [BB(6)](https://wiki.bbchallenge.org/wiki/BB(6)),
  [Antihydra](https://wiki.bbchallenge.org/wiki/Antihydra)
- bbchallenge forum: [Currently applied deciders](https://discuss.bbchallenge.org/t/currently-applied-deciders/32),
  [Translated cyclers](https://discuss.bbchallenge.org/t/decider-translated-cyclers/34),
  [Finite Automata Reduction](https://discuss.bbchallenge.org/t/decider-finite-automata-reduction/123),
  [Bouncers](https://discuss.bbchallenge.org/t/decider-bouncers/126)
- [Determination of the fifth Busy Beaver value (arXiv:2509.12337)](https://arxiv.org/pdf/2509.12337);
  [Turing machines deciders, part I (arXiv:2504.20563)](https://arxiv.org/abs/2504.20563)
- [bbchallenge-deciders repo](https://github.com/bbchallenge/bbchallenge-deciders);
  [n-gram CPS](https://github.com/Nathan-Fenner/bb-simple-n-gram-cps)
- [sligocki, "BB(6,2) is Hard (Antihydra)"](https://www.sligocki.com/2024/07/06/bb-6-2-is-hard.html);
  [bbchallenge Antihydra page](https://bbchallenge.org/antihydra)
</content>
</invoke>
