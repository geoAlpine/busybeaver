# o18 under the Antihydra capstone framework — the base-8/3, 3-adic instance (2026-06-28)

Applies the `COMPLETE_PROOF_CAPSTONE.md` machinery (induced map → GAP LEMMA → renewal → AEV placement →
no-structure-only meta-theorem) to **o18**, the `⌊8N/3⌋+2` cryptid (ratio `p/q = 8/3`). The point of the
exercise: Antihydra lives in the **2-adic** world (denominator 2); o18 lives in the **3-adic** world
(denominator 3) — a genuinely different number system. We carry every framework link across and record
exactly which transfer cleanly and which change shape.

**Soundness.** Every claim is `[PROVEN]` (elementary arithmetic), `[VERIFIED]` (machine-checked this session,
exact big-int via `o18_framework_numerics.py`), `[OPEN]`, or an explicit `[MODEL]`/`[ANALOGY]`. Zero upgrades.

---

## 1. o18's exact map and halting criterion  [PROVEN / VERIFIED]

Raw TM `o18 = 1RB0RE_1LC0RA_1LA1LD_1LC1LF_0LC0LB_1LE---`.

- **Orbit map.** The clean-reset width obeys `f(N) = ⌊8N/3⌋ + 2`, ratio `p/q = 8/3 = 2³/3`.
  `[VERIFIED]` reproduces `10→28→76→204→546→1458→3890→10375→27668`.
- **Halt criterion (EXACT).** Halt = state F reads `1`. F is entered only via `D:1→1LF`, so
  > **o18 halts ⟺ at some D-read of a `1`, the cell immediately to its left is also `1`**
  > (a left-frontier collision; equivalently the base-3 leading digit/carry of the `⌊x·(8/3)ⁿ⌋` odometer
  > overflows its width).
  `[VERIFIED]` to 60M steps: 9 D-reads-of-1, **0** with left-neighbor `1` (no halt).

### The first structural divergence from Antihydra — EXISTENCE vs DENSITY  [PROVEN]
This is the single most important finding and it is true *before* any number theory:

| | Antihydra | o18 |
|---|---|---|
| halt criterion shape | **density / Cesàro**: `liminf` even-density `< 1/3` | **existence / Borel–Cantelli**: the collision *ever* occurs |
| non-halt condition | `E_n/n ≥ 1/3` for all `n` (a tail-average bound) | the forbidden carry **never aligns** after the verified prefix |
| named-problem facet | Mahler 3/2 **density** | Erdős ternary-digit **existence** (`2^m` omits a base-3 digit only for finitely many `m`) |

So o18 is **not** the literal 3-adic translate of Antihydra's even-density statement. Antihydra asks "does a
running average stay above a threshold"; o18 asks "does a single forbidden configuration ever appear." Both
sit under the **same equidistribution kernel** (below), but they read off *different facets* of it. There is
therefore no exact `balance_n = 3E_n − n`-style underflow counter for o18; the honest analog of "even-density
criterion" is **"the base-3 digit/carry of the `(8/3)ⁿ` orbit equidistributes, so the alignment set has
density 0 and (Erdős-strength) is finite/empty after the prefix."**

---

## 2. The induced map and GAP-LEMMA analog — base 8/3, **3-adic**  [PROVEN / VERIFIED]

Antihydra's GAP LEMMA collapses the `⌊3c/2⌋` orbit to its induced **odd** map using `D = v₂(3c−1)` (2-adic
valuation, denominator 2). For o18 the denominator is **3**, so the entire valuation bookkeeping moves to the
**3-adic place**. Work with the pure Mahler map `g(N) = ⌊8N/3⌋` (the `+2` is a bounded BB-specific additive
term, §6; it does not change the Mahler/3-adic class).

For `N` **coprime to 3**, set
> `r := 8N mod 3 = 2N mod 3 ∈ {1,2}`   ( `N≡1 ⇒ r=2`, `N≡2 ⇒ r=1` ),
> `D'' := v₃(8N − r)`   ( the 3-adic valuation; `8N − r ≡ 0 mod 3` by construction ).

**GAP LEMMA (3-adic analog). [PROVEN / VERIFIED].** Starting from `N` coprime to 3, the number of `g`-steps
until the next value coprime to 3 is **exactly `D''`**, and the induced map onto the coprime-to-3 part is
> **`T''(N) = 8^{D''−1} · (8N − r) / 3^{D''}`.**

*Proof.* `g(N) = (8N−r)/3` has `v₃ = D''−1`. Each subsequent value divisible by 3 is `N=3m ↦ 8m = 8N/3`,
which drops `v₃` by 1 and multiplies the coprime part by 8 (a 3-adic unit, `|8|₃ = 1`). After `D''−1` such
exact divisions the value is coprime to 3 again; the accumulated unit factor is `8^{D''−1}`. ∎
`[VERIFIED]` zero violations over all coprime seeds `N < 4000` for both the gap count and the closed form.

**Roles dictionary (Antihydra ↔ o18):** odd ↔ coprime-to-3 · `v₂(3o−1)` ↔ `v₃(8N−r)` · "even step"
(`c=2c'`) ↔ "multiple-of-3 step" (`N=3m`) · 2-shift alphabet `{0,1}` ↔ 3-shift alphabet `{0,1,2}`.

### Measure side (Haar on `ℤ₃*`) — exact, with the **mean-D'' = 3/2** law  [PROVEN / VERIFIED]
Partition `ℤ₃*` by `A_d = {o : v₃(8o−r) = d}`. The next 3-adic digit is free, so
`P(D''≥d+1 | D''≥d) = 1/3`, giving
> **`P(D'' = d) = (2/3)(1/3)^{d−1}` (geometric), mean `D'' = Σ d·(2/3)(1/3)^{d−1} = 3/2`.**

`T''` is **Haar-measure-preserving, exact, Bernoulli on `ℤ₃*`** (full-branch surjective, branch `A_d` has
Jacobian `3^d` from the `/3^d`, the `8^{d−1}` factor being a 3-adic unit) — the exact 3-adic transcription of
the capstone's §3 theorem. `[VERIFIED]`: along the induced orbit (seed 7, 4000 steps) the empirical law tracks
the geometric law (`P(D''=1)=.682` vs `.667`, `.216` vs `.222`, `.068` vs `.074`, …), orbit `mean D'' = 1.47`
(Haar 1.5), and the base-3 digits of the actual `⌊8N/3⌋+2` orbit equidistribute (units trits 1963/1985/2052,
digit-2 density 0.3332 vs 1/3).

### Renewal identity and the mean-D'' criterion  [PROVEN] — **but it is the kernel, not the halt threshold**
The Kac/renewal identity transfers verbatim: in a block of length `D''` there are `D''−1` multiple-of-3 steps
and one coprime step, so
> **density(`N≡0 mod 3` steps) `= 1 − 1/(mean D'')`**, `= 1/3` under Haar.

**Crucial soundness note (the GAP-LEMMA "halting criterion" the task asks for, stated honestly).** For
Antihydra the analogous identity *is* the halt threshold (`mean D ≥ 3/2 ⟺` non-halt) because halting *is* a
density underflow. **For o18 there is no `mean D'' ≥ const` halt threshold**, because o18 halts on an
*existence* event, not a density underflow (§1). What the renewal/`mean D''=3/2`/digit-equidistribution package
delivers for o18 is the **kernel needed for the Borel–Cantelli non-halting heuristic**: if the base-3
digit equidistributes (`mean D'' = 3/2`, units trit `→ 1/3`), the per-epoch alignment probability is `~1/N_k`,
and `Σ_k 1/N_k < ∞` (geometric width `×8/3`), so the expected number of collisions after the verified prefix
is `~0`. That is a `[MODEL]` (Borel–Cantelli needs independence the deterministic carries do not supply), not a
proof — exactly the Erdős wall. (Sanity: a naive "`mean D'' ≥ 8/3`" threshold copied blindly from `p/q` would
*falsely* predict halting, since Haar `mean D'' = 3/2 < 8/3`; this confirms the threshold does **not** transfer
and o18's criterion is genuinely a different shape.)

---

## 3. AEV placement — the `p/q = 8/3` instance, a **different base** under the SAME conjecture  [PROVEN]

AEV Conjecture 1.6 (arXiv:2510.11723) is stated for **all coprime `p > q ≥ 1`**: every orbit of
`T_{p/q}(x) = ⌈px/q⌉` equidistributes in residue classes mod `q^k` for all `k`. Antihydra is the `q=2`
instance; **o18 is the `q=3` instance** — same conjecture, different rational base, hence the move from the
2-adic to the 3-adic number system.

- **Coprimality:** `gcd(8,3)=1` ✓ (AEV hypothesis met). `p>q`: `8>3` ✓.
- **Mahler-implication regime `p < q²`:** **`8 < 9 = 3²` ✓ (YES)** — so AEV Thm 1.5 gives, for `8/3`,
  Conj 1.2 ⇒ Conj 1.4 = a Mahler-type Z-number statement, exactly as `3 < 4 = 2²` does for `3/2`.
  *Calibration:* both cryptid multipliers sit at the **tight edge `p = q²−1`** (`3 = 2²−1`, `8 = 3²−1`); they
  are the two extreme-but-still-inside instances of the regime for `q=2,3`. (o5's `4/3` is `4 < 9` but not on
  the edge.)
- **floor vs ceiling:** AEV uses the ceiling `⌈8x/3⌉`; o18 uses the floor `⌊8x/3⌋ (+2)`. As with Antihydra the
  `±` shifts the residue branch, so they are **not literally conjugate**; the bridge is the GAP-LEMMA
  bookkeeping `v₃(8o−r)` (the 3-adic analog of `v₂(3o−1)`). (K_o18) below is the **floor-mirror**.

> **Kernel (K_o18). [OPEN].** For the orbit `N_{n+1} = ⌊8N_n/3⌋ + 2` (`N₀` the o18 seed), the base-3 digit /
> 3-adic carry of `⌊x·(8/3)ⁿ⌋` equidistributes — concretely the induced 3-adic itinerary `D''_n = v₃(8o_n−r_n)`
> realizes the geometric law (units trit density `→ 1/3`, `mean D'' = 3/2`) — **so the left-frontier collision
> set is finite and empty after the verified prefix.** This is the **`p/q = 8/3` (i.e. `q=3`), single-orbit,
> floor-mirror fragment of AEV Conj 1.6**, in its **existence/Erdős** facet (cf. Antihydra = the `q=2`
> fragment in its density/Mahler facet).

**Answer to "is o18's kernel a DIFFERENT-base instance of the SAME AEV conjecture?" — YES.** AEV Conj 1.6
ranges over all coprime `p/q`; Antihydra instantiates `q=2` (2-adic), o18 instantiates `q=3` (3-adic). They are
two different bases of one conjecture, not two conjectures. The **facet differs** (o18 reads the existence
facet that literally *is* the Erdős ternary-digits-of-`2^{3n}` family; Antihydra reads the density facet that
is Mahler's `3/2`), but the umbrella conjecture is identical. Literature has **zero unconditional results** at
`q=3` either (Narkiewicz 1980 gives only an *upper* bound on the count, the set is not even known finite — the
exact missing piece, the same shape as Antihydra's missing FLP-density lower bound).

---

## 4. The no-structure-only meta-theorem — transfers in spirit, changes technical form  [PROVEN / VERIFIED]

**Halting fixed point (the o18 analog of Antihydra's `o=1`). [VERIFIED].** The integer fixed point of
`f(N)=⌊8N/3⌋+2` is **`N = −1`** (`⌊−8/3⌋+2 = −3+2 = −1`); the exact (no-floor) fixed point is `N = −6/5`, and
the induced `D''=1`-branch fixed point is `o = r/5 ∈ ℤ₃` (`2/5` or `1/5`, a 3-adic unit). **None is a positive
integer** — exactly mirroring Antihydra, whose halting fixed point `o=1` is the off-orbit minimal point. The
positive integer orbit is **strictly increasing** (`[VERIFIED]` `f(N) > N` for `1 ≤ N ≤ 10⁵`), hence
**transient**, so there is **no invariant probability measure** for it — the same transience that makes
Birkhoff/invariant-measure averaging empty for Antihydra.

**Does the ergodic-optimization obstruction transfer?**
- **In spirit, YES.** The structural properties used by any "structure-only" proof — 3-adic Haar preservation,
  exactness/Bernoullicity of `T''`, the contraction of the unit part — are **shared with the fixed
  configuration `N=−1`** and with the all-`D''=1` (never-gaining-a-factor-of-3) itinerary, just as
  Antihydra's structure is shared with `o=1`. So no proof using only `T''`'s structure can separate halting
  from non-halting; the distinction lives only in the **tail behavior of the specific orbit** (genericity).
  This is the capstone's "free/finite-window part is blind to the discriminator" principle, intact 3-adically.
- **In precise technical form, NO — and this is an honest divergence.** Antihydra's meta-theorem is the
  *ergodic-optimization* statement `β(ψ) = max_μ ∫ψ dμ = +1/2`, attained at the atom `δ_{o=1}` — a statement
  about a **density** functional `ψ`. o18's halt criterion is **existence**, not a Cesàro average, so there is
  no test function `ψ` whose all-orbits sign bound is equivalent to non-halting, and the `β(ψ)=max` computation
  does not apply. o18's obstruction is instead the **Erdős/Borel–Cantelli form**: there is no unconditional
  proof that the forbidden-carry set is finite (Narkiewicz gives an upper bound only, no lower bound, set not
  known finite). Same meta-principle (a halting configuration shares all available structure ⇒ no
  structure-only proof), realized through a different gate (no density lower bound ↔ no finiteness proof).

---

## 5. Numerics summary (`o18_framework_numerics.py`, exact big-int)  [VERIFIED]
- Raw TM 60M steps: 9 D-reads-of-1, **0** collisions ⇒ non-halting; halt is an existence event.
- GAP LEMMA: gap to next coprime-to-3 `== D'' = v₃(8N−r)` and `T''=8^{D''−1}(8N−r)/3^{D''}`, **0 violations**,
  all coprime seeds `< 4000`.
- `D''` law: geometric `(2/3)(1/3)^{d−1}`, **Haar mean `D'' = 3/2`** (exact); orbit mean `1.47`.
- Base-3 digits of `⌊8N/3⌋+2` orbit equidistribute (digit-2 density `0.3332` vs `1/3`).
- Halting fixed point `N=−1` (analog of `o=1`); positive orbit strictly increasing ⇒ transient.

---

## 6. Bottom line — what transfers, what changes

| framework link | Antihydra (2-adic, 3/2) | o18 (3-adic, 8/3) | transfer? |
|---|---|---|---|
| orbit map | `⌊3c/2⌋`, `c₀=8` | `⌊8N/3⌋+2` | analog (`+2` = bounded additive) |
| valuation / number system | 2-adic, `v₂(3o−1)` | **3-adic, `v₃(8N−r)`** | **changes base** |
| GAP LEMMA / induced map | `T(o)=3^{D−1}(3o−1)/2^D` | `T''(N)=8^{D''−1}(8N−r)/3^{D''}` | **clean transfer** [PROVEN] |
| measure side | Haar-exact Bernoulli, `mean D=2` | Haar-exact Bernoulli, **`mean D''=3/2`** | clean transfer [PROVEN] |
| renewal identity | even-density `=1−1/meanD` | mult-of-3 density `=1−1/meanD''` | clean transfer [PROVEN] |
| **halt criterion** | **density** underflow (`≥1/3`) | **existence** (carry ever aligns) | **changes shape** [PROVEN] |
| named-problem facet | Mahler 3/2 (density) | Erdős ternary-`2^{3n}` (existence) | different facet, same kernel |
| AEV placement | Conj 1.6 `q=2`, `p<q²` (`3<4`) | **Conj 1.6 `q=3`, `p<q²` (`8<9`)** | **same conjecture, different base** [PROVEN] |
| regime edge | `p=q²−1` (3=4−1) | `p=q²−1` (8=9−1) | both at tight edge |
| halting fixed point | `o=1` (off positive orbit) | **`N=−1`** (off positive orbit) | clean transfer [VERIFIED] |
| meta-theorem | ergodic-opt `β=+1/2` at `o=1` | **no `β`; Erdős no-lower-bound** at `N=−1` | spirit yes, technical no |

**One-sentence verdict.** o18 is the **3-adic, base-8/3 sibling of Antihydra**: the induced-map / GAP-LEMMA /
renewal / Haar-exactness / transient-fixed-point machinery transfers cleanly with `2→3` everywhere, and its
kernel is the **`q=3` (different-base) single-orbit floor-mirror fragment of the same AEV Conjecture 1.6 in the
`p<q²` Mahler-implication regime** — but because o18 halts on an **existence** (Erdős) event rather than a
**density** (Mahler) underflow, the halt-threshold (`mean D ≥ 3/2`) and the ergodic-optimization meta-theorem
(`β=max`) do **not** transfer literally; the obstruction is the Erdős "no finiteness / no density lower bound"
wall at the shared fixed point `N=−1`. Same umbrella conjecture, same transient-fixed-point no-go *principle*,
different facet and different technical gate. No decision; soundness intact.
