# Attacking (K) from the POSSIBLE side — the carry-transparency boundary (2026-07-25)

User directive: use what we PROVED on the possible (template) side to attack the impossible (K)
region. This document is the synthesis; three parallel agents test the live placement questions
(o17, o10/o15, eventual-transparency). **No machine decided. No label upgraded.**

## The boundary, stated sharply [PROVEN direction + MEASURED grounding]

The BB(6) cryptid Collatz cores are maps `c → ⌊μ c⌋`, `μ = 2^a/3^b`, on a **base-2** tape. Define
a step **carry-transparent** if the multiply introduces no orbit-dependent carry propagation.

- **`μ = 2^a` (pure power of the base): TRANSPARENT.** `×2^a` is a left shift — zero carry, for
  every `c`. The orbit's digit structure is predictable, so an EXACT `∀g` transport exists
  (x2 is the witness: `doubPhaseEven`/`topEntryOddFull`, 308 green Lean theorems).
  MEASURED: x2's `×2` carry-chain length ≡ 0.
- **`μ` has an odd prime factor 3 (numerator or denominator): OPAQUE = (K).** `×3` on a base-2
  tape is the addition `c + 2c`, which propagates carries; composed with the `÷2` floor it produces
  the orbit-dependent **depth process** `D_n = v₂(3c_n−1)` — the exact (K) object.
  MEASURED (Antihydra `μ=3/2`, seed 8, N=3000): `×3` carry-chain max 54, mean 23, growing — not a
  bounded/local quantity.

**So the possible/impossible boundary is exactly: `μ ∈ {2^a}` (template) vs `3 | num·den(μ)` ((K)).**
This is `CRYPTID_KERNEL.md`'s Mahler-multiplier dichotomy, sharpened to a **carry-transparency**
statement — a fresh, mechanism-level characterization.

## Why the boundary is Furstenberg — the attack converges (but from a NEW angle)

To make an `μ = 2^a/3^b` map transparent you would need the tape base in which BOTH `×2` and `×3`
are shifts **simultaneously**. No such base exists: `2` and `3` are multiplicatively independent, so
transparency in base 2 (kills the `×3` carry) and transparency in base 3 (kills the `÷2` carry)
cannot hold at once. **The impossibility of simultaneous 2- and 3-transparency IS the Furstenberg
×2·×3 obstruction**, re-derived from the carry side. This matches — from a genuinely different
direction — this week's three (K)-route closures (#16/#17/#21, `O4_KWALL_CLOSURE_2026-07-25.md`):
every route needs a second multiplicatively-independent structure, and the carry view explains
*why* mechanically (one base can only linearize one prime).

## The one place the boundary might be crossable — bounded-carry despite an odd prime

The dichotomy above is about the *generic* Mahler map. The live question the possible side lets us
ask sharply: **is there a (K)-tagged machine whose carry is BOUNDED for a structural reason
specific to the machine (not orbit statistics)?** Such a machine would be TEMPLATE-class despite
involving 3 — a real impossible→possible move. Candidates (agents testing now):

- **o17 (odometer, digit-step 3).** [AGENT A — DONE → (c), CONJECTURE-FREE no-transport proof.]
  Re-derived cell-for-cell. o17 is a uniquely-ergodic ISOMETRIC base-3 carrying odometer (no
  Mahler `⌊μc⌋` kernel — the "≈×8" tag was an in-flight carry-buffer artifact). **Halt = left-
  frontier overflow (marker block becomes even), NOT an interior `00` gap** (corrects the old
  spec). The single-separator invariant IS bounded-provable but is **irrelevant to halting** — the
  chain "single-separator ⟹ no `00` ⟹ non-halt" breaks at the 2nd arrow (transient multi-`0` gaps
  occur in halters AND non-halters). **Decisive [PROVEN, conjecture-free]:** the family
  `C(3j) = 0^∞[A0]1^{3j}0^∞` shares an IDENTICAL bounded left-window yet has non-monotone halt fate
  (halters {2,4,5,7,8,…} vs non-halters {1,3,6,9,…} interleaved, no modulus). So halt is provably
  NOT a bounded-window / transparent-carry function ⟹ **no x2-style exact transport can exist.**
  o17 is (K) by a DIFFERENT mechanism than Mahler: a carry-overflow / marker-parity halt whose
  fate depends on the whole unbounded Collatz-irregular digit string (carry opaque at the TOP digit).
  `route_o17_reverify.py`, `route_o17_locality.py`.
- **o10 (nested refill) / o15 (parity-irregular).** The OUTER refill/collision layer might be
  transparent even though the inner `μ=3/2`/`8/3` layer is not — IF the halt predicate touches only
  the outer layer. [AGENT B — pending]
- **Eventual-transparency (Antihydra seed 8).** [AGENT C — DONE → (c), with a sharp new pin.]
  The transparent regime EXISTS and is PROVEN: within each odd run of length `K` the orbit is an
  exact bounded-carry template segment `c_j = 1 + 3^j·2^{K−j}·m` (Countdown lemma). The ONLY
  unpredictable event is the renewal draw `K′ = v₂(3h−1)` (needs unbounded 2-adic lookahead). The
  finite-`E` crux: `E(D*) = {renewals with K′>D*}` has density `→ 2^{−D*} > 0`, so **E is positive-
  density = INFINITE, never finite** — a finite-certificate hybrid is the wrong shape. "Eventual
  bounded carry (E finite)" ⟺ orbit eventually avoids `{v₂(c−1)>D*}` ⟺ the (K) kernel itself,
  (K)-equivalent in BOTH directions. `route18_depth_process.py`, `route18_transparency_crux.py`.
  This sharpens the boundary: the transparent segments (odd runs) never merge into an eventual
  regime because the giant-draw exceptions recur at fixed positive frequency `2^{−D*}` at every
  depth — exactly the `E[K²]<∞` / single-orbit-equidistribution gap.

## Honest prior and value

Prior expectation: o10/o15/eventual reduce to (K) (the odd prime's carry is inherited); **o17 is
the one genuine mis-classification candidate** (an odometer's carry can be bounded by construction).
Even confirmed closures sharpen the mechanism (mode-B discipline): the carry-transparency boundary
is itself a durable NEW characterization of the possible/impossible line, converging to Furstenberg
from the mechanism side rather than the ergodic side.

Grounding numerics committed to repo root: transparency carry-chain measurement.
**No machine decided. No label upgraded.**
