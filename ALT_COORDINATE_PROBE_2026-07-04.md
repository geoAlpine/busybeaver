# P1′ core — can an alternative coordinate be built for ⌊3x/2⌋? A constructive probe (2026-07-04)

*The fine-structure analysis (`EXCEPTIONAL_FINE_STRUCTURE_2026-07-04.md`) showed the `(K)`-exceptional set is
`(dim 1, measure 0)` like the badly-approximable numbers, decidable pointwise **only if** the dynamics supply a
continued-fraction-type coordinate — which `⌊3x/2⌋` lacks (non-Pisot). This note attacks that head-on: **can we
construct an alternative coordinate system in which halting becomes decidable?** Enumerate every candidate, show
each fails for a specific reason, isolate the structural obstruction (the two ingredients that make CF work are
**both** absent), and reframe P1′ as a coordinate-construction problem. Verdict `(c)` — no coordinate is
constructible from existing structure — with a sharp `(b)` target statement. SOUNDNESS: `[OBSERVED]`/
`[PROVEN-in-lit]`/`[ARGUED]`; no machine decided; `(K)` `[OPEN]`.*

## 0. Headline
- **What makes CF decide badly-approximable:** the Gauss map is the symbolic coding of the **natural extension** of
  the `×1` rotation — the `SL₂(ℤ)` geodesic flow, which is **hyperbolic (non-amenable)** and has a **Markov/sofic**
  coding. In that coordinate `x∈BA ⟺ bounded partial quotients` — a shift-checkable, finite-state condition.
- **Every candidate coordinate for `⌊3x/2⌋` fails**, each for a nameable reason (§1). The sharpest, freshly
  quantified: the **2-adic residue coordinate does NOT descend** — for **every** residue mod `2^K` (all `K=4..10`),
  `⌊3c/2⌋ mod 2^K` has **branching exactly 2**, i.e. it is *never* a function of `c mod 2^K`; the map reads **one
  bit deeper each step** (a genuine 2-adic shift). No finite window `ℤ/2^K` closes.
- **The structural obstruction:** CF works because `SL₂` is **hyperbolic + sofic**. `⌊3x/2⌋`'s natural extension is
  the solenoid automorphism `×3/2` on `(ℝ×ℚ₂×ℚ₃)/ℤ[1/6]`, whose acting group `ℤ[1/6]⋊⟨3/2⟩` is **amenable
  (solvable)** and whose expansion is **non-Pisot ⇒ non-sofic**. **Both ingredients that make a decidable
  coordinate are absent** — the coordinate-construction view of the Coverage No-Go's two-toolbox.
- **P1′, reframed:** build a symbolic coordinate on the **amenable** `(2,3)`-solenoid in which the balance-cocycle
  positivity (`B_n=3E_n-n≥0 ∀n` = non-halting) becomes a decidable digit/boundedness condition — a **"Gauss-map
  analogue for a non-sofic amenable hyperbolic action."** No existing structure provides it.

## 1. The candidate coordinates and why each fails `[enumerated]`

| candidate coordinate | what it is | failure mode |
|---|---|---|
| **2-adic residue `c mod 2^K`** | the obvious finite coordinate | **NON-DESCENT** `[OBSERVED]`: branching exactly 2 at every residue, every `K` — the map reads one bit below the window; no `ℤ/2^K` coordinate exists. |
| **base-`3/2` numeration** (Akiyama–Frougny–Sakarovitch) | the native numeration for `(3/2)ⁿ` | digit language is **non-regular** `[PROVEN-in-lit]`; "halting" is not a bounded/automatic digit condition. |
| **2-adic depth sequence `D_n=v₂(3c_n−1)`** | the induced-map coding (exact Bernoulli annealed) | the coding *is* clean, but its **quenched statistics = `(K)`** — reading halting off it is the problem itself. |
| **solenoid natural extension** `(ℝ×ℚ₂×ℚ₃)/ℤ[1/6]` | the invertible `×3/2` — the *correct* natural extension (CF-analogue slot) | acting group **amenable** + **non-Pisot ⇒ no sofic coding**; the orbit's genericity there `= (K)`. |
| **Ostrowski / CF of `log₂3`** | external coordinate from `p/q≈log₂3` approximants | reaches only **`Θ(log N)` depth** (foothold `≈0.85 log₂N`) and is **statistically independent** of the depth/parity bit (`HAIRLINE_CRACK_PROBE`) — cannot drive the linear-depth bit. |
| **renormalization / first-return RG** | first-return to `A_2` is again Bernoulli (self-similar) | a **coisometry** (`‖Φ‖≡1`) — a *symmetry*, not a contraction ⇒ **infinite scale-regress**, no finite coordinate emerges. |

**Non-descent, quantified `[OBSERVED, 3·10⁵ steps]`.** `⌊3c/2⌋ mod 2^K` branches into exactly **2** successors for
**every** residue (`K=4,6,8,10`; all `2^K` residues visited, max branching 2). Reason: `⌊3c/2⌋ mod 2^K` is fixed by
`3c mod 2^{K+1}`, i.e. by `c mod 2^{K+1}` — **one bit more** than the window. So the map is a one-bit-lookahead
2-adic shift; iterating it, predicting the orbit to depth `k` needs the seed to depth `k` — **linear**, never
bounded. This is the 2-adic form of "no finite-state coordinate."

## 2. The CF-analogue obstruction — both ingredients absent `[ARGUED, structural]`
A coordinate that renders a `(dim 1, measure 0)` condition **pointwise decidable** (as CF does for `BA`) needs two
things, and `SL₂(ℤ)`/Gauss has both:

| ingredient | CF / `BA` (works) | `⌊3x/2⌋` (missing) |
|---|---|---|
| **a hyperbolic natural extension with a group action** | `SL₂(ℤ)` on `ℍ` — **hyperbolic, non-amenable** | `×3/2` on the solenoid — hyperbolic **but the group `ℤ[1/6]⋊⟨3/2⟩` is amenable (solvable)** |
| **a Markov/sofic symbolic coding** | Gauss map = **sofic** (finite Markov partition) | `3/2` **non-Pisot ⇒ β-shift not even sofic** (Frougny) |

**Both** CF-ingredients fail. This is precisely the program's **Coverage No-Go two-toolbox**
(`RANK1_AMENABLE_EQUIDISTRIBUTION.md`) — "rigidity needs a large (non-amenable) group; Weyl/coding needs tameness
(Pisot/sofic); our action has neither" — now seen from the **coordinate-construction** angle: the *reason* no
decidable coordinate can be built is that the natural extension is **amenable AND non-sofic**, the two conditions
under which every known coordinate-construction method (CF/Gauss, Markov partitions, β-numeration, Ostrowski) either
degenerates (non-regular, non-descending) or reaches only log-depth.

## 3. Why no combination crosses `[ARGUED, from HAIRLINE_CRACK_PROBE]`
Could candidates combine into a coordinate? No: the only two non-trivial ones are **complementary but
non-composable** — the Ostrowski/`log₂3` coordinate controls the top `Θ(log N)` bits and is **MI-independent**
(`~10⁻⁵` bits) of the depth bit it would need to drive; and any **orbit-built** weight is conjugation-invariant for
the coisometry cocycle (`‖Φ‖≡1`), so inducing gains only `O(1)` depth per level and **exhausts the orbit before
`Θ(n)`**. The seam `bit_k(c_n)=bit_{n+k}(8·3ⁿ)⊕bit_{n+k}(S_n)⊕ρ_n` mixes an exogenous moving-diagonal (vdC-closed)
with a self-referential carry `S_n` built from `b_0…b_n` (circular). No composite coordinate reaches linear depth.

## 4. P1′, reframed as coordinate construction `[the (b) target statement]`
> **The missing tool = a Gauss-map analogue for `×3/2`.** Construct a symbolic coordinate `Φ` on the amenable
> `(2,3)`-solenoid such that the specified orbit `8·(3/2)ⁿ` has, in the `Φ`-coordinate, a **decidable**
> boundedness/first-passage condition equivalent to non-halting (`B_n≥0 ∀n`). Because the natural extension is
> **amenable + non-sofic**, `Φ` cannot be a finite-state / Markov / β-numeration coding (all shown to
> non-descend, be non-regular, or reach only log-depth); it must be a genuinely new **non-sofic coordinate for an
> amenable hyperbolic action** — an object no field currently constructs. This is the same generational target as
> effective single-orbit equidistribution (§`NEW_MATH_PROGRAM`), now stated in the language `BA`/CF makes intuitive:
> *we have the right topology (`dim 1, measure 0`) but no continued-fraction analogue, and non-Pisot is exactly
> why.*

## 5. Honest verdict
**(c) — no alternative coordinate is constructible from existing structure**, each candidate failing by a named
mechanism (non-descent, non-regularity, circularity, log-depth, coisometry regress). The `(b)` gain is the crisp
reframing: **P1′ = constructing a Gauss-map analogue (a non-sofic symbolic coordinate) for the amenable
hyperbolic `×3/2` action on the `(2,3)`-solenoid**, the two enabling ingredients of CF (hyperbolic-non-amenable +
sofic) being provably both absent. **`(K)` `[OPEN]`. No machine decided. No label upgraded.**

## Reproduce
- Non-descent numeric (`scratchpad`, `/opt/homebrew/bin/python3.13`): for `c→⌊3c/2⌋` from seed 8, every residue
  mod `2^K` (`K=4..10`) has exactly 2 successors mod `2^K` — the map is a one-bit-lookahead 2-adic shift, no finite
  coordinate. Basis: `EXCEPTIONAL_FINE_STRUCTURE_2026-07-04.md`, `RANK1_AMENABLE_EQUIDISTRIBUTION.md` (two-toolbox),
  `SELECTOR_COMPUTABILITY.md` (non-Pisot ⇒ non-sofic), `HAIRLINE_CRACK_PROBE.md` (non-composability),
  `NEW_MATH_PROGRAM.md` (P1′). Akiyama–Frougny–Sakarovitch *Israel J. Math.* 168 (2008); badly-approximable/CF = Gauss map.
