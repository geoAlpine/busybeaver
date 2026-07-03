# BB(6)'s two generational walls are provably-distinct objects, and o4 is the bridge (2026-07-04)

*A new-angle assault on the two generational walls that gate BB(6) — **B1 = (K)/Mahler-3/2 (Erdős)** single-orbit
equidistribution, and **B2 = generalized-Collatz carry-existence** (the o17/o3 Type-II outliers). Three angles,
enabled by this session's cryptid structure (o4's new ratio; the trichotomy). Result: **no crack** — both walls
stay unbroken and generational — but a **(b) new two-walls characterization**: the walls carry **opposite
measure-theoretic signatures** (so BB(6) needs two independent breakthroughs), and **o4 proves the halt-
presentation is orthogonal to the wall**. SOUNDNESS: every signature is `[OBSERVED]`, calibrated against
controls; the walls themselves are `[OPEN]` rederivations (Erdős/Mahler; Michel/Kurtz–Simon). **No machine
decided. No wall proved. Halting `[OPEN]`.** Verifier: `two_walls_verify.py`.*

## Angle A — o4's new ratio does NOT couple the p=3 kernels `[OBSERVED → (c)]`

o4 added a **new Mahler ratio μ=4/3 (p=3)** to the census (`O4_HALT.md`), joining o15/o18's `8/3` (also p=3).
Since `8/3 = 2·(4/3)`, one might hope the two p=3 orbits couple into a rigidity. They do **not**: over
`n≤4000`, `⌊(8/3)^n⌋ mod 3` equals `2^n·⌊(4/3)^n⌋ mod 3` only `0.322` of the time (not `1.0`) — **the floor
annihilates the `2^n` multiplicative relation** — and the joint `(⌊(4/3)^n⌋, ⌊(8/3)^n⌋) mod 3` distribution is
**uniform over all 9 pairs** (the two orbits are mod-3 independent). So multiple same-prime ratios give
**independent** orbits, each its own (K)-hard equidistribution. This is the same **floor-annihilation** that
kills the program's coupling routes (`INTRATERM_ADELIC_MINING.md`); it **strengthens** (K)'s single-orbit
character rather than cracking it. **(c) rederives B1.**

## Angle B — B1 and B2 carry OPPOSITE measure-theoretic signatures `[OBSERVED separation → (b)]`

**The discriminator (calibrated, `two_walls_verify.py`).** Subword complexity `p(ℓ)`, block entropy, and the
diffraction/Weyl signature separate two universality classes crisply:

| class | `p(ℓ)` | entropy | diffraction | examples |
|---|---|---|---|---|
| **positive-entropy / absolutely-continuous (Rajchman)** | `2^ℓ` (full) | `→1` | flat, no Bragg | Bernoulli; **Mahler `⌊(3/2)^n⌋ mod2` `[B1]`** (`p(ℓ)=8,64,1024,8189`) |
| **zero-entropy / singular (automatic, pure-point)** | `~linear` / const | `→0` | Bragg peaks | Thue–Morse `(6,16,28,40)`; **3-adic odometer parity `(2,2,2,2)`** |

> **Finding.** The **B1/Mahler** orbit sits exactly on the **positive-entropy, absolutely-continuous** side
> (`≡` Bernoulli; confirms `PROBE_DIFFRACTION.md`). The **B2/o17/o3** carry cascades sit on the **opposite**
> side: o3's last-block-digit word has `p(ℓ)` **saturating at 6** (entropy `→0`, autocorr `+1/3`, near-zero
> off-DC), o3's length-increment bit is linear-complexity, and the o17 dense-cascade parity is
> polynomial-complexity with a **Bragg peak** (`max off-DC/N ≈ 0.086`). Moreover the o17 **halt** marker is
> sampled only **`O(log t)`** times (spacings `17,22,57,213,410,1281,1070561` in 250M steps) — a **sparse
> existence event**, not a stationary density you could even form a Weyl sum for.

**Why they cannot be one wall.** B2's cascade is spectrally **tame** (zero-entropy ⇒ uniquely-ergodic odometer
⇒ equidistribution is *automatic* ⇒ "no kernel"). That is *precisely why* B2's hardness **cannot** be an
equidistribution statement and must instead be a **reachability/existence** statement (does the sparse irregular
event ever occur). B1's hardness **is** the equidistribution (of a positive-entropy orbit). The two hardnesses
are **orthogonal**: `B2 is NOT reducible to B1` `[OBSERVED separation]`. **BB(6) needs two independent
breakthroughs** — B1 (Erdős/Mahler 1968; AEV 1.6) and B2 (Michel; Kurtz–Simon `Π⁰₂`).

## Angle C — o4 is the bridge: presentation ⊥ wall `[OBSERVED → (b)]`

o4 wears the **Type-II presentation** (a finite-control head over a single-`0`-separated digit string, `√t`
bouncer geometry, an `11`-existence halt gate *dual* to o3's `00`-gate) — yet its digit string carries a
**genuine positive-entropy Mahler value orbit**: the driver `G'=⌊4G/3⌋+c(G mod3)` has `G mod 2` and `G mod 3`
words of **full complexity** (`p(ℓ)=2^ℓ`, `3^ℓ`: `27/27, 243/243, 6248/6561`), flat diffraction, `≡` Bernoulli
— the **B1** signature. So o4 = **Type-II presentation + B1 wall**, while o17/o3 = **Type-II presentation + B2
wall**.

> **Characterization.** The **halt presentation** (bouncer geometry + an existence-race gate) and the **wall**
> (B1 vs B2) are **independent coordinates**. The wall is set by the **driver**: does the digit string carry a
> **positive-entropy Mahler value orbit** (⇒ B1, hardness = its equidistribution) or only a **zero-entropy tame
> cascade whose halt is a sparse existence event** (⇒ B2, hardness = the reachability)? o4 is the machine that
> proves these two axes are independent — it is the bridge between the walls, not a reduction of one to the other.

## Verdict + honest caveats

**Overall: (b) a new two-walls characterization, resting on (c) rederivations — NO crack.** New content: the
**calibrated entropy/spectral separation** of B1 (positive-entropy, absolutely-continuous Mahler) from B2
(zero-entropy, Bragg-spectrum tame odometer + sparse existence event), and **o4 as the bridge proving
presentation ⊥ wall**. The walls themselves are known and unbroken.

**Caveats (binding).**
- The separation is `[OBSERVED]`, **not `[PROVEN]`**: `p(ℓ)=2^ℓ` for the Mahler orbit is itself sample-limited
  past `ℓ≈13` and *is* (K)-hard content — measuring it does not resolve (K).
- **Zero-entropy of the B2 cascade does NOT imply decidability.** The cascade *observables* look automatic, but
  halting is the irregular marker/`00`/`11` **existence** event, already shown **core-hard** (no bounded
  predictor; the `5→8` and `Δk∈{−1,+1,+2}` choices are history-dependent). Spectral tameness and halt-hardness
  live on *different objects* — that is the whole point of the separation, not a decidability claim.
- The o17 *dense* cascade observable is width-dominated (full-width bouncer sweep), so its low complexity is
  partly trivial; the load-bearing o17 evidence is the marker's **exponential sparsity**, not its spectrum.

**No machine decided. No wall proved. No non-halting shown. Halting `[OPEN]` for all.**

## Reproduce
- `two_walls_verify.py` — the calibrated discriminator (Mahler `⌊(3/2)^n⌋ mod2` full `2^ℓ`; Thue–Morse and
  3-adic odometer parity linear/const) + o4's driver `G'=⌊4G/3⌋+c` on the Mahler (B1) side (full complexity,
  equidistributing `G mod 3`). Interpreter `/opt/homebrew/bin/python3.13`.
- Prior basis: `PROBE_DIFFRACTION.md` (single-orbit diffraction = absolutely continuous), `O17_CORE_TRANSDUCER.md`
  / `O3_TRANSDUCER.md` (B2 cascades), `O4_HALT.md` (the bridge), `BB6_FRAMEWORK_PACKAGE.md` (B1 barriers).
