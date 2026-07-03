# o17 core (k≡0 mod 3): the carry cascade is a FINITE-CONTROL head over a base-3 digit string — a positive normal form (2026-07-03)

*Advances the OPEN o17 core (the `L≡0 mod3` sublattice launched by the departure lemma of
`O17_LINEAR_PROVEN.md` §5). Prior notes characterized the core only NEGATIVELY — "no 1-D reduction"
(§4), "no clean base-3 odometer / unbounded interior digits" (§6). This note replaces the negatives
with a machine-verified **positive structural normal form**, and, with two supporting angles
(classification/decidability; digit-value arithmetic), pins exactly which coordinate is irreducible.
SOUNDNESS: everything here is `[OBSERVED, exhaustive over the tested range]` or a labeled
`[PROVEN]` algebraic/automata-theoretic consequence. **Nothing about halting is decided; the core
stays `[OPEN]`. No machine decided. No label upgraded to a halting result.** Verifier:
`o17_core_transducer.py` (prints `... VERIFIED: True`, 0 exceptions).*

o17 = `1RB1LD_1RC0LE_1LA1RE_0LF1LA_1RB0RB_---0LB`  (halt = state F reads 0). Core = forward orbit of
`C(L)=0^∞[A0]1^L0^∞` for `L≡0 (mod3)`; `j=L/3`. Milestone = head in state `A` at the left frontier.

---

## 1. The positive normal form `[OBSERVED, 92 milestones, seeds L=3j to j=200, 0 exceptions]`

> **Every milestone config is a word in the regular language**
> `𝓛 = (3 | 5) · ( 0 · 1^{ℓ}, ℓ≡2 (mod 3) )*` :
> a **leading marker block** of length `3` or `5`, followed by **single-`0`-separated** blocks each
> of length `ℓ≡2 (mod3)`, i.e. a base-3 **"digit"** `d=(ℓ−2)/3 ≥ 0`. Head `A` sits on the frontier-`0`.

Verified (verifier §I): over all milestones every inter-block gap is a single `0`, the leading block
is `3` or `5`, and every interior block is `≡2 (mod3)`. **0 language violations.**

**The milestone-to-milestone map is realised by a FIXED finite-control head** (verifier §II): across
the entire tested range the head interacts with the tape through only

- **10** block-boundary crossing triples `(state, read, dir)`
  `{ (A,0,R),(A,1,L),(B,0,R),(B,1,L),(C,0,L),(C,1,R),(D,0,L),(D,1,L),(E,0,R),(E,1,R) }`,
- **7** right-boundary reflection pairs `{ (A,0),(B,0),(B,1),(C,0),(C,1),(E,0),(E,1) }`,
- **5** left-frontier gate pairs `{ (A,0),(D,0),(D,1),(E,0),(E,1) }`,

and **no symbol beyond these fixed sets ever appears**, independent of `L`. The bulk of the motion is
carried by `(B,0,R)`/`(B,1,L)` (the rightward/leftward sweeps of the proven linear régime, Lemma R/L),
with `C,E` doing digit processing and `A,D` the frontier gate.

**Reading.** The finite CONTROL is bounded and fixed; **all** the unboundedness — and hence all the
Collatz-hardness — lives in the digit VALUES and their carry cascade, not in the head. The core is a
**finite-state head bouncing over a string of unary-encoded base-3 digit counters** (single-`0`
separators, `3`/`5` marker). This is the exact positive form of the docs' "unbounded interior digits"
obstruction (`O17_HALT_STRUCTURE.md` §6): the alphabet of *digit values* is unbounded, the alphabet of
*head behaviours* is finite.

## 2. The width identity `[PROVEN from §1]` (verifier §III)

For a milestone with marker `μ∈{3,5}`, `m` digits and digit-sum `S=Σd_i`, the tape width is exactly
```
        W  =  μ + 3·(m + S) + 1
```
(the `+1` is the frontier-`0` the head occupies). Proof: nonblank content `= μ + Σ(3d_i+2) + m` gaps
`= μ + 3S + 3m`, plus the frontier-`0`. Verified 0 mismatches. Since the proven growth is `W ∼ step^{1/2}`
(`o17_core_growth.py`), this reads as `step ≈ Θ((m+S)²)`: the core is a **quadratic-time / linear-space**
bouncer whose "clock" is the digit-string content `m+S`.

## 3. No scalar linearization — the irreducible coordinate is the LENGTH `[PROVEN over the tested families]`

Decoding each milestone to `(marker, digit vector (d_1,…,d_m))`, we searched for a scalar recoding under
which the milestone map becomes a clean arithmetic iteration:

- Homogeneous positional value `V=Σ d_i r^i` for `r∈{3,2,3/2,2/3,1/2,1,5/2}`, both directions;
  length-sensitive `V=Σ ℓ_i r^i` for `r∈{3,2,3/2,2/3,1/2}`, both directions, ±leading (32 decodings).
- Candidate laws: affine `V↦aV+b`, `×const`, `+const`, Collatz `⌊3V/2⌋`, quadratic — on the injective read.

**Result: 0 hits.** No tested decoding even makes `V_next` a function of `V_now`, let alone affine;
the specific **base-3/2 hypotheses (digit-value and raw-length, both directions) are refuted**. The
extreme sensitivity is explicit: consecutive transitions `365→367` (ratio `1.005`) and `367→63933`
(ratio `174`) sit side by side.

> **Minimal obstruction `[PROVEN, given the departure lemma]`.** The all-zero-digit seeds
> `S_j=(marker 3, [0]×j)` (`= C(3j)`) map, by the departure lemma, to `j` pairwise-distinct successors
> (content and length grow with `j`) — yet **every** homogeneous positional value `Σd_i r^i` is
> identically `0` on all of them. So the map depends on `j` through a coordinate every base-`r`
> valuation annihilates: the **digit-vector length / zero-padding count**. The length is irreducible
> state; no scalar/base-3/2 valuation can be a complete state variable.

This **confirms** (does not refute) the docs' "irreducibly multi-digit string" claim (`O17_HALT_STRUCTURE.md`
§4, §6), and names the precise reason: the essential extra coordinate is the string LENGTH, invisible to
any positional number system.

## 4. Classification & decidability `[PROVEN-in-lit / OPEN]`

- **Linear space is a red herring for decidability `[PROVEN, standard automata theory]`.** `W∼step^{1/2}`
  confines the head to `O(√t)` cells at time `t`, but a single orbit visiting *unbounded* tape is **not**
  a linear-bounded automaton: the reachable-configuration set is infinite, so there is no finite
  configuration graph and no cycle-detection decision procedure. "Linear space per unit time" is a
  growth rate, not a space bound. The bouncer geometry buys **no** decidability.
- **Best-fit class:** a **Collatz-like / bbchallenge-"Cryptid"** generalized-Collatz iteration (Michel's
  sense: halting governed by iterating a piecewise-affine carry map with data-dependent branches)
  wearing **bouncer geometry**. Ruled out with reasons: *translated cycler* (the block-list grows, not a
  shifted bounded pattern), *decidable bbchallenge bouncer* (counters here update non-uniformly /
  Collatz-irregularly, digits unbounded — the decider cannot fire), *fixed-radix / base-3/2 odometer*
  (digits unbounded; §3), finite *Minsky counter machine* (the number of counters grows).
- The notable wrinkle: a **polynomial-growth (quadratic-time / linear-space) machine that is nonetheless
  Collatz-hard** — it sits in the gap between the decided "bouncer" class and the undecided "Cryptid"
  class. This is a *rederivation* of the general Michel/Conway/Kurtz–Simon Collatz-hardness wall (the
  generalized Collatz problem is Π⁰₂-complete, but this does **not** transfer to any fixed instance), not
  a crack of it. Refs: Michel, *Busy beaver competition and Collatz-like problems* (Arch. Math. Logic 32,
  1993) & survey arXiv:0906.3749; Kurtz–Simon, *Undecidability of the Generalized Collatz Problem* (2007);
  Aaronson, *The Busy Beaver Frontier* (2020); Lagarias, *3x+1 annotated bibliography* arXiv:2111.02635;
  bbchallenge Cryptids / Bouncers deciders (arXiv:2504.20563).

## 5. What this proves, and what it does not

**Advance (`[OBSERVED]` positive normal form + `[PROVEN]` corollaries).** The o17 core's carry cascade
is a **fixed finite-control head bouncing over a single-`0`-separated string of unary base-3 digit
counters** (§1), with an exact width law `W=μ+3(m+S)+1` (§2); no scalar/base-`r`/base-3/2 recoding
linearizes it, the irreducible extra coordinate being the string LENGTH (§3); and it is a
polynomial-growth Collatz-like/Cryptid bouncer for which linear space gives no decision procedure (§4).
Together these **replace the docs' three negative characterizations with one positive structural picture**
and localize the hardness to a named coordinate.

**Not proved (unchanged `[OPEN]`).** Nothing about halting or non-halting for any core seed. Whether the
core's halting is decidable is `[OPEN]`; whether it reduces to a *named* open conjecture (a formal
Collatz reduction) is `[OPEN]`. **No machine decided. No label upgraded.**

## 6. The atomic step is an odometer with a FREE-RUNNING least-significant counter (deep-dive, 2026-07-03)

Resolving the finite control of §1 into its gadgets (verifier data, `o17_localrule.py`/`o17_odometer.py`):
clean sweeps are the proven period-`5/3` (rightward) / `1`-per-cell (leftward) translation cycles and
**preserve digit values** (Lemma R/L); digits change only at three gadgets — the **right-end increment**
`(E,0)` reversal, the **left-propagating carry** `(C,0)`+`(E,1)`, and the **left-frontier gate** `(A,0)`
turn / `(D,·)` halt. So the core is an **odometer**: the right-end gadget ticks a counter, base-3 carries
ripple left, and a carry reaching the frontier grows the marker (or, in the D-parity, halts).

Counting the right-end ticks `n=1,2,3,…`, the **least-significant digit is a free-running counter**:
```
        max_digit(n)  =  n − c(L)        [OBSERVED, EXACT, c(L) a seed-constant]
```
verified with `c` exactly constant on every long seed (`o17_core_counter.py`: `c=68,81,34,48` for
`L=9,18,27,33`). With **zero** fitting freedom this forces, and the verifier confirms:
- `width(n) = 3n + O(1)` — measured `width/n → 3.01`, `width ∼ n^{0.99}` → **linear space**;
- `step(n) ∼ c₂n²` — measured `step/n² ≈ 3.6–3.9`, `step ∼ n^{2.1}` → **quadratic time**;
- hence `width ∼ step^{1/2}` (the proven growth of `o17_core_growth.py`), and the digits are **unbounded**
  precisely because the bottom counter `n` grows without bound.

> **Unification `[OBSERVED]`.** The two separate obstructions of `O17_HALT_STRUCTURE.md` §6 — "unbounded
> interior digits" and "polynomial growth" — are **ONE mechanism**: a free-running least-significant
> counter equal to the bounce index `n`. The digit string is essentially "the running count `n` in the
> low position, base-3 carry-history above it."

**Scope (unchanged `[OPEN]`).** This explains growth and unboundedness, not halting. The counter is
free-running (never resets); halting is governed by whether/when a left-propagating carry reaches the
frontier in the `D`-parity, which depends on the entire carry history — the Collatz-hard part, untouched.
**No machine decided. No label upgraded.**

## 7. The halt predicate reduces to a single PARITY BIT (the odometer MSB) (deep-dive, 2026-07-03)

Attacking the carry-to-frontier rule (the Collatz-hard heart): halting is a **left-frontier gate** event,
and the gate fires state `A` (turn / continue) or `D` (→`F` halt) by a **parity** of the leftward sweep.
Verified (`o17_core_halt_parity.py`, 121 gate arrivals, seeds `j=1..59`, **0 exceptions**):

> **(I) Gate-state = leading-block parity.** The gate fires `A` iff the **leading block** (the odometer's
> most-significant position, "marker") is **odd**, and `D` (halt) iff it is **even**. Hence
> ```
>            o17 core seed L=3j  HALTS  ⟺  its leading block ever becomes EVEN.
> ```
> **(II) Invariants.** At every `A`-milestone the leading block is in `{3,5}` (both odd) and the digit
> sum `S` is **even**; the only even leading block ever seen is `8`, occurring exactly at the halting
> `D`-arrival. So the marker performs a **walk on `{3,5}`** and halt = a step to even (`8`).

This is a **1-bit reduction** of the halt predicate: from the odometer of §1/§6, the free-running LSB
counter (§6) drives carries upward, and **halting is decided entirely by the parity of the MSB** (leading
block) — whether a carry ever pushes it from odd (`3`/`5`) to even (`8`).

> **(III) The reduced `{3,5}`-walk is Collatz-hard `[OBSERVED]`.** The walk's step is **not** determined
> by any bounded parity predictor: from marker `5` the next marker is `3` (continue) **or** `even` (halt),
> **ambiguously** under `(marker, m mod2, S mod2)`. So the halt decision depends on the full **unbounded
> carry history**. The large-`j` "odd `j`→halt / even `j`→slow" tendency (`O17_HALT_STRUCTURE.md` §5b) is
> **not** a rule — `j=13` (odd) is an exception and the even-`j` "runs" are cap-limited slow halters.

**Net.** The Collatz-hardness of the o17 core is now **localized to a single parity bit** — the leading
block (odometer MSB) becoming even — whose evolution on `{3,5}` is history-dependent. This is the sharpest
placement of the wall: not a scalar, not a bounded predictor, but one bit driven by the unbounded carry
stream. **Halting stays `[OPEN]`; the reduction decides no machine. No machine decided. No label upgraded.**

## Reproduce
- `o17_core_transducer.py` — self-contained verifier of §1–§3: (I) language closure, (II) fixed
  10/7/5-symbol finite-control alphabets, (III) width identity `W=μ+3(m+S)+1`. Prints
  `CORE TRANSDUCER CHARACTERIZATION VERIFIED: True` (0 exceptions, seeds L=3j to j=200).
- `o17_core_halt_parity.py` — §7: gate-state = leading-block parity (0 mismatches ⇒ `HALT ⟺ MSB ever
  even`), invariants (leading∈{3,5}, `S` even), and the Collatz-hard ambiguity of the `{3,5}`-walk.
  Prints `HALT-PARITY REDUCTION VERIFIED: True`.
- `o17_core_counter.py` — §6: `max_digit = n − c(L)` exact; `width∼3n` (linear space), `step∼n²`
  (quadratic time); the unified free-running-counter mechanism. Prints `... constant on all long seeds: True`.
- `o17_core_growth.py` — the `[OBSERVED]` `W∼step^{1/2}` growth and irregular unbounded excursions.
- Interpreter: `/opt/homebrew/bin/python3.13` (the `python3` alias is a broken symlink).
