# How to cross the wall — the joining/renormalization reformulation, and the precise obstruction (2026-07-05)

*A genuine "how do we cross" session (not mapping): use today's duality (`BLIND_HARMONIC_2026-07-05.md`) to reformulate
the crossing as a **joining** problem, test its necessary condition blind, and localize the true obstruction to the
sharpest point. Result: the multi-scale odometer↔archimedean **joining is empirically benign (product)** — so the
crossing reduces to a **single** archimedean effective-equidistribution input, with the 2-adic depth a free
consequence — BUT that input needs an **exponential moving-diagonal rate**, while discrepancy gives only a
**polynomial** rate, separated by the information-theoretic **counting ceiling `R(N)≤log₂N`**. This IS the
Furstenberg-×2×3 / rank-1-amenable wall, now pinned to one sentence. SOUNDNESS: `[OBSERVED]`/`[PROVEN]` labelled;
`(K)` `[OPEN]`; no crossing claimed; no machine decided.*

## 1. Reformulation: crossing = a joining of the two dual faces `[framing, PROVEN-structural]`
The system is the `(2,3)`-solenoid with `T=×(3/2)`. Two factors: **archimedean** (`{θ(3/2)^n}` equidistribution — the
random face) and **2-adic odometer** (a compact group rotation / Kronecker factor — the deterministic countdown face,
`BLIND_EFFECTIVENESS`+`BLIND_HARMONIC`). The depth/parity data is a function of the JOINT position; controlling the
up-jump heights (⇒ depth ⇒ the balance walk) needs the **joint** equidistribution. By joining theory over a Kronecker
factor, this reduces to **archimedean equidistribution twisted by odometer characters** = equidistribution of
`{θ(3/2)^n}` **along dyadic progressions `n ≡ r (mod 2^j)`**. And `n≡r mod 2^j` gives `θ(3/2)^r·((3/2)^{2^j})^m` — the
**same Mahler problem with ratio `R=(3/2)^{2^j}`**. So:
> **The duality is a RENORMALIZATION: 2-adic determinism = the "time-doubling" self-similarity of the archimedean
> sequence.** Crossing `⟺` uniform equidistribution across all dyadic-renormalized ratios `(3/2)^{2^j}`.

## 2. Blind test of the necessary condition — the joining is BENIGN `[OBSERVED, N=1.6·10⁴]`
Discrepancy of each dyadic subsample `{x_n : n≡r mod 2^j}` vs the random baseline for its size. Mean `D*/random` over
residues: **`j=0..4` → 0.85, 1.34, 1.06, 0.94, 0.90 — flat ~1, NO growth in `j`.** Each dyadic level equidistributes
as well as a random subsample; individual residues fluctuate `0.47–1.62` (finite-`M` noise) but the mean is stable.
**⇒ the odometer↔archimedean joining adds NO obstruction (product-benign) and NO contraction (self-similar).** Two
consequences: **(good)** the crossing does **not** require fighting multi-scale coupling — it reduces to a **single**
archimedean effective-equidistruction, from which the 2-adic depth follows for free; **(wall)** the difficulty does not
*shrink* across scales either — level `j` is exactly as hard as level 0 (no bootstrap gain; consistent with the
`β=+½` critical / zero-margin obstruction).

## 3. The true obstruction, pinned `[PROVEN — the sharp point]`
The reduction of §2 is at the **shallow / arc** level (parity, depth `~1`), where discrepancy `D*_N~N^{-1/2}` lives.
But the crossing needs **`max depth < 0.5n`** — resolution of arcs of size `2^{-0.5n}` at time `n`, i.e. equidistribution
on the **moving diagonal at depth `Θ(n)`**. And `n` points can equidistribute mod at most `2^{R(N)}` with
**`R(N) ≤ log₂ N`** (`DEPTH_REACH_CLARIFICATION`, pure counting/pigeonhole — information-theoretic, unpushable). So:
> **What the crossing needs (exponential moving-diagonal rate `2^{-Θ(n)}`) is separated from what ANY discrepancy /
> equidistribution-of-`N`-points statement can give (polynomial `N^{-1/2}`, capped at depth `log₂N`) by the counting
> ceiling.** The benign joining (§2) lives entirely ABOVE this horizon; the genuine `(K)` lives exponentially BELOW it,
> as a single-orbit **digit-frequency of `3^n` on a moving diagonal** — not a counting/discrepancy object at all.

This is the one-sentence form of "why rank-1 amenable / Furstenberg-×2×3 is the wall": the needed statement is a
single-orbit digit frequency below the counting horizon, where no equidistribution-of-points method reaches, and no
rank-≥2 rigidity or positive-entropy mechanism is available to substitute.

## 4. The frontier attack-classes, rated `[each with its obstruction FOR OUR PROBLEM]`
| class | shape for our problem | obstruction | rating |
|---|---|---|---|
| **effective equidist / P1′** | exponential-rate Weyl for `{θ(3/2)^n}` on moving diagonal | = the famous open `(3/2)^n` problem; below counting horizon | the honest target; generational |
| **rank-2-ification** | embed the orbit in the `(×2,×3)` action → Rudolph–Johnson | single orbit isn't a positive-entropy invariant measure; = Furstenberg orbit-closure conj (open) | blocked, famous-open |
| **Sarnak/BSZ disjointness** | odometer factor ⟂ archimedean via BSZ orthogonality | the required cancellation IS the `(K)` Weyl cancellation (§1) | circular |
| **bootstrap / self-improve** | even-density`≥½−ε` ⇒ up-jumps bounded ⇒ density up | `β=+½` critical, zero margin (§2 no contraction); No-Structure | closed |
| **entropy / dimension** | positive-entropy or non-atomic ⇒ classification | single orbit = zero entropy; the atom question `μ({1})=0` is itself `(K)` | closed |

**No class crosses with current mathematics.** The joining reformulation (§1) is the freshest and it *does* buy the
reduction "multi-scale coupling is benign ⇒ one archimedean input suffices" (§2) — a genuine simplification of the
target — but the input (§3) is below the counting horizon = the generational core.

## 5. Verdict
**No crossing — but the sharpest map yet of where a crossing must enter.** The duality is a renormalization; the
odometer↔archimedean joining is empirically benign (blind-tested), collapsing the crossing to a **single** archimedean
effective-equidistribution whose required **exponential moving-diagonal rate** sits below the **counting ceiling**
`R(N)≤log₂N` that all discrepancy methods obey. That separation is the rank-1-amenable / Furstenberg-×2×3 wall in one
line. The only classes that could cross are famous-open (P1′, rank-2-ification) or circular/closed (BSZ, bootstrap,
entropy). **A crossing needs genuinely new mathematics at the counting horizon; no internal route reaches it.**
`(K)` `[OPEN]`. No machine decided. No label upgraded.

## Reproduce
- `scratchpad/crossing_joining_test.py` (`/opt/homebrew/bin/python3.13`, exact big-int, `N=1.6·10⁴`): dyadic-subsample
  discrepancy, mean `D*/random` flat `~1` over `j=0..4`. Basis: `BLIND_HARMONIC_2026-07-05.md` (the two dual faces),
  `DEPTH_REACH_CLARIFICATION.md` (counting ceiling `R(N)≤log₂N` vs moving diagonal), `BAKER_LINFORMS.md` (Weyl = `(K)`),
  `BB6_NO_STRUCTURE_THEOREM.md` (`β=+½` critical), `NEW_MATH_PROGRAM.md` (P1′), `AIU_*`/solenoid notes (rank-1 amenable).
