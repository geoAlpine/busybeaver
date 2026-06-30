# The hairline crack probed: #1 (Ostrowski/Diophantine) ⊕ #2 (adaptive Oseledets) — does it open? (2026-06-30)

*Focused decision-probe on the single untried combination flagged least-dead by the new-methods sweep
(`NEW_METHODS_SWEEP_2026-06-30.md` §2, `NEW_ANGLES_DIVERGENT.md` §0): feed #1's orbit-specific archimedean
Diophantine data into #2's adaptive, unbounded, orbit-built (data-direction / Oseledets) certificate, to construct
#2's weight WITHOUT the circular threshold-crossing sub-lemma. Target is the minimal core (`MINIMAL_CORE_2ADIC.md`):
the single specified 2-adic Bernoulli orbit `o_0=27`, `D_j=v₂(3o_j−1)`, want `liminf_N (1/N)Σ_{j<N} D_j ≥ 3/2` `=(K)`.
SOUNDNESS PARAMOUNT: every claim labelled. No `(K)` proof is attempted or claimed; finding the exact collapse line
is a fully-valued outcome. Numerics `/Users/aokiyousuke/quantum-ecc/.venv/bin/python scratchpad/hairline_check.py`,
exact big-int. NOT committed.*

---

## §0. Verdict (one line)

> **COLLAPSE — on the log-vs-linear depth-reach gap, at a precisely identifiable line.** `[PROVEN-backed]` #1's
> Diophantine data controls the **archimedean top mantissa** `{n·log₂3}` = the **top `Θ(log N)` 2-adic bits** of
> `c_n` (depth-reach `k(N)≈0.84·log₂N`, confirmed). #2's data-direction certificate `(CR)` needs the **fresh bit**
> `β_n=bit_k(c_n)` to decorrelate from the low state `c_n mod 2^k` for all `k→∞` — a 2-adic statement at the
> **moving-middle bit position `≈n+k`**, which is `Θ(n)` 2-adic-deep below the band #1 controls. The only object
> linking the archimedean top to the 2-adic middle is the **seam carry** `S_n` (`2ⁿc_n+S_n=8·3ⁿ`), and `S_n` to
> bit-precision `n+k` is built from exactly the parities `b_0…b_n` = the depth data #2 must certify. So #1 **cannot
> supply data where #2 needs it** without already knowing the answer. The adaptivity of #2 does **not** break the
> infinite scale-regress; it inherits it, because an orbit-built weight is conjugation-invariant for the cocycle
> norm (coisometry, `‖Φ‖≡1`) and the surviving decay still lives in the deepest, uncontrolled data-direction.
> **No label upgraded. `(K)` remains `[OPEN]`.** The one sub-lemma that would (formally) save it is `(CR)` itself,
> which is `=` `(K)`, not weaker.

---

## §1. Does #2 need LINEAR depth, or only LOG depth? — the crux

**Setup of #2 (from `EUE_COISOMETRY_NOGO_THEOREM.md`).** The cross-scale renormalization cocycle
`Φ_{k,k+m}=R_k⋯R_{k+m-1}` is a chain of coisometries (`R_kR_k^*=I`), so its operator-norm is identically `1` and the
top Lyapunov exponent is `0`. The ONLY surviving decay channel is the **data-direction / quenched (Oseledets)
exponent** evaluated along the single orbit-generated odd-data vector `d^{(k+m)}`:
> `(CR) [OPEN]:` `limsup_m (1/m) log( ‖Φ_{k,k+m} d^{(k+m)}‖ / ‖d^{(k+m)}‖ ) ≤ −½log2`, i.e. the orbit's bottom-bit
> content equidistributes between `ker R_k` and its complement at every scale. `(CR) ⟹ (K)` `[PROVEN reduction]`.

The "adaptive unbounded Oseledets / data-direction certificate" #2 is *any* orbit-built weight whose negativity
certifies `(CR)`. The question: what **2-adic depth** of orbit information must such a certificate (i) be
constructible from and (ii) read, to certify the `liminf`?

**(i) What `(CR)` is a statement ABOUT `[PROVEN]`.** `d^{(k+m)}` is the empirical odd-character vector
`(π_N(χ_a^{(k+m)}))_{a odd}`, i.e. it encodes `c_n mod 2^{k+m}` — the **bottom `k+m` 2-adic bits**. The contracting
subspace `ker R_k` is defined by the **fresh top bit** `bit_k(c_n)` consumed at scale `k` (the seam:
`χ_a^{(k)}(s_{n+1})=r_k(c_n)·χ_a(V^{(k)}(s_n))`, `r_k=(−1)^{bit_k}`). Certifying the `liminf` depth-mean requires
`‖d^{(k)}‖→0` for **every fixed `k`**, hence requires control of the joint law of (fresh bit `bit_k(c_n)`, low state
`c_n mod 2^k`) **uniformly as `k→∞`**. This is the orbit's 2-adic bit-coupling at **unbounded depth**.

**(ii) The depth where the certified bit lives is LINEAR `[PROVEN, via seam + Tao-quench].** Two independent reductions
agree the requirement is `Θ(n)`, not `Θ(log n)`:
- **Archimedean address of the bit.** Via the seam `2ⁿc_n+S_n=8·3ⁿ`, the parity/depth bit is
  `c_n mod 2 = bit_{n+3}(3ⁿ)` — the **diagonal bit of `3ⁿ`** at absolute position `≈n` inside the `≈1.585n`-bit
  integer (`EFFECTIVE_TOPDIGIT.md` §c). More generally the scale-`k` fresh bit `β_n=bit_k(c_n)` is the bit at the
  **moving-middle position `≈n+k`**. It is `Θ(n)` away from BOTH the top foothold (`Θ(log N)`) and the bottom
  foothold (`Θ(log N)`).
- **Forward-tracking cost.** To know `o_j mod 2` (the parity feeding `D_j`) for `j` steps of the exact 2-adic map
  `T(o)=3^{D−1}(3o−1)/2^D` one needs `o_0` to 2-adic precision `2^{Θ(j)}` (Tao Prop 1.9 / hyp 1.11:
  `n_0≥(2+c_0)n` — **linear**, `NEW_METHODS_SWEEP` §1). The valuation budget `Σ_{i<n}D_i=n+v₂(c_n)−v₂(c_0)`
  shows the consumed 2-adic depth grows like `n+v₂(c_n)`, again linear.

> **Verdict §1 `[PROVEN-backed]`: #2 needs LINEAR 2-adic depth — at the deepest, fresh end of every scale window,
> uniformly as `k→∞`.** It cannot be driven by a log-depth surrogate, because (CR) is precisely the statement that
> the linear-depth fresh bit is unbiased relative to the low state, and there is no log-depth functional equal to
> it.

**Can the log-depth archimedean MAGNITUDE `log o_j` (which #1 controls) drive it instead? — NO `[PROVEN structural +
OBSERVED]`.** `log₂ c_n = 3 + n·log₂(3/2)` is a **smooth, deterministic function of `n`** (an exact arithmetic
progression mod 1, this is exactly the #1 rotation `θ_n={n·log₂3}`). It is a function of the *index*, carrying zero
bit-level coupling information. Numerically (`hairline_check.py`, `N=2·10⁵`, exact): the mutual information between
the #1-controlled top mantissa `θ_n` (quantized to `Q` bins) and the depth/parity bit sits at the `1/N` noise floor —
`I(θ_n; b_n)=7.5·10⁻⁵` bits and `I(θ_n; [D≥2])=6.3·10⁻⁵` bits at `Q=16` (against a `4`-bit maximum), i.e.
**statistically independent**. The archimedean log-depth datum #1 owns contains essentially **no information** about
the linear-depth bit #2 must certify. (Consistent with `CORE_CARRY_LEVER.md` §2.2: `I(β_n; top-bit of s_n)=3·10⁻⁵`
bits; and with `EFFECTIVE_TOPDIGIT.md`: the parity sequence is `U²`-uniform, full subword complexity — no functional
of the top mantissa predicts it.)

---

## §2. Amplification / renormalization — does adaptivity break the infinite regress, or inherit it?

The program's scale bootstrap "regresses infinitely" (`CORE_CARRY_LEVER.md` §3 item 2, `ENDOGENOUS_UE_BUILD.md` §5):
controlling the feedback at scale `k` (the fresh bit) needs control of the scale-`(k+1)` state, whose fresh bit needs
scale `(k+2)`, …; the gap **never reaches the fresh end of the window**. The probe: does building the renormalization
weight **adaptively from the orbit itself** (rather than from a fixed template), seeded by #1's Diophantine data,
break this?

**It inherits it, for two compounding proven reasons.**

1. **Coisometry is weight-invariant `[PROVEN, EUE_COISOMETRY_REDTEAM]`.** The cross-scale Lyapunov exponent is
   **conjugation-invariant**: any interior (scale-graded, anisotropic, even orbit-adaptive) weight `W` gives
   `Φ̃=W_k Φ W_{k+m}^{-1}`, whose Lyapunov spectrum equals that of `Φ` (the interior `W`'s telescope/cancel in the
   `(1/m)log‖·‖` limit). So an adaptive weight **cannot manufacture operator-norm contraction** where the coisometry
   gives none. The decay it can certify is *still* only the data-direction projection of `d^{(k+m)}` — i.e. exactly
   `(CR)`, evaluated at the **deepest scale `k+m`**, which is the uncontrolled fresh end. Adaptivity relocates the
   weight but not the unknown.
2. **Inducing adds `O(1)` depth per level while shrinking the orbit `[PROVEN-rate]`.** The natural amplifier of
   log-depth → deeper-depth is iterating the renormalization `R=×(3/2)` on the moving diagonal / the first-return
   induced map. Each level advances the controllable 2-adic depth by `O(1)` (one fresh bit) but the usable orbit
   segment contracts (the induced/return map on `{c≡1 mod 2^k}` thins the orbit by a constant factor per level).
   To reach **linear** depth `Θ(j)` one needs `Θ(j)` levels — by which point the surviving orbit length is
   `N·(const)^{−Θ(j)}`, i.e. **you run out of orbit before reaching the depth of the bit.** This is the quantitative
   form of "cannot compound to `Θ(j)`" (`NEW_ANGLES_DIVERGENT.md` §0 #1(c)). #1's data, living at the **top**
   (archimedean, log-depth), is on the wrong end to seed the **deep** alignment that each inducing level newly
   exposes.

> **Verdict §2 `[PROVEN-backed]`: the adaptivity does NOT break the regress.** The orbit-built weight is invisible to
> the coisometry norm (so it cannot contract), and the renormalization that would amplify depth runs out of orbit
> before reaching the linear-depth bit. The regress is structural (it is the closed endogenous loop "the orbit
> furnishes its own driving bit"), not an artifact of a poorly-chosen template; choosing the template from the orbit
> changes nothing, because the unknown is always one scale **deeper** than any data — including #1's data, which is
> at the opposite (top) end entirely.

---

## §3. The archimedean → 2-adic transfer through the seam — quantified

#1's data is archimedean (about `{(3/2)ⁿ}` / `{n log₂3}`); `(K)` is 2-adic (depth frequency). The exact bridge is the
seam identity
> `2ⁿ c_n + S_n = 8·3ⁿ`,  `S_n = Σ_{j<n} 3^{n−1−j} 2^j b_j`,  `b_j=c_j mod 2`  `[PROVEN]`.

Reading off bit `n+k` of this identity (where the fresh bit `β_n=bit_k(c_n)` lives) gives, schematically
(`CARRY_COBOUNDARY.md`, the borrow decomposition `β = d ⊕ σ ⊕ ρ`):
> `bit_k(c_n) = bit_{n+k}(8·3ⁿ) ⊕ bit_{n+k}(S_n) ⊕ ρ_n`  (`ρ_n` = finite-range borrow, state-dependent).

The transfer fails at **three** seams, each `[PROVEN]`:

- **(T1) The exogenous diagonal `bit_{n+k}(8·3ⁿ)` is itself at the middle = `(K)`-hard.** This term has no carry; it
  is pure Mahler. But its position `n+k` is `Θ(n)` below the top `Θ(log N)` band where #1's Diophantine reach lives,
  and van der Corput is **closed** there (`EFFECTIVE_TOPDIGIT.md`: differencing returns the same exponential family;
  Mahler sum `=O(√N)`, no improvement). So #1's effective-equidistribution machinery, pushed to its proven limit
  (`k(N)≈0.84·log₂N`, re-confirmed: `D*_N≈3.5·10⁻⁵`, ratio `0.841` at `N=2·10⁵`), **does not reach this term**. The
  moving-middle diagonal is the wall, restated.
- **(T2) The carry term `bit_{n+k}(S_n)` re-imports the endogeneity.** `S_n` is built from the orbit's own parities
  `b_0…b_n`. Its bit `n+k` is a function of essentially all `n` past depth-bits — the very data `(K)` is about. To
  use the seam to transfer #1's (carry-free) archimedean control onto `bit_k(c_n)` one must already know `S_n` to
  bit-precision `n+k`, i.e. know `b_0…b_n`. **Circular: the bridge requires the conclusion.** (And the carry piece
  provably does **not** telescope — `Σ(β_n−d_n)χ_a(s_n)` grows `∼√N`, `CARRY_COBOUNDARY.md` §2 — so it is not a
  finite-state coboundary that could be discharged once and for all.)
- **(T3) The transfer carries no statistical information either `[OBSERVED]`.** Even setting circularity aside and
  asking only whether the archimedean datum *correlates* with the bit: §1's numerics give `I(θ_n; b_n)≈10⁻⁵` bits.
  The annealed carry is Rajchman-equidistributed and "contributes net ≈0" to the coupling (`CARRY_EXOGENIZATION.md`),
  while the only channel that could sustain a bias — the **state-coupling** of `β_n` to the low state — is precisely
  `V_odd`, on which the archimedean data has zero leverage (it lives in `V_even`/the magnitude).

> **Verdict §3 `[PROVEN/OBSERVED]`: the seam transfers nothing usable.** The carry `S_n` blocks the
> archimedean→2-adic transfer **exactly as it blocks every other route**: the only honest bridge from the
> log-depth archimedean datum to the linear-depth 2-adic bit passes through `S_n`, whose relevant bits ARE the
> depth data. Quantitatively the transfer's information content is at the `1/N` floor.

---

## §4. Net — the exact collapse line (and the precise would-be sub-lemma)

**The combination COLLAPSES.** The hope was: #2's adaptive certificate is circular only at the threshold-crossing
sub-lemma; #1 supplies orbit-specific, non-annealed data to populate the weight without invoking genericity. The
probe shows the data #1 supplies is at the **wrong 2-adic depth and the wrong character channel** to enter #2's
construction:

> **THE EXACT COLLAPSE LINE.** #1 controls the archimedean top mantissa `{n·log₂3}` = the top `Θ(log N)` 2-adic bits
> of `c_n`. #2's certificate `(CR)` must certify the fresh bit `β_n=bit_k(c_n)` — sitting at the moving-middle 2-adic
> position `≈n+k`, **`Θ(n)` deep** — is unbiased relative to the low state, **uniformly as `k→∞`**. The map from the
> log-depth datum to the linear-depth bit is the seam `2ⁿc_n+S_n=8·3ⁿ`, and `S_n` to bit-precision `n+k` is a
> function of `b_0…b_n` = the depth data itself. **Hence "#1 supplies #2's weight without circularity" fails at the
> single step `bit_k(c_n) ↤ bit_{n+k}(8·3ⁿ ⊖ S_n)`: the `⊖S_n` term IS the conclusion.** Log-depth data reaches
> bit `Θ(log N)`; the requirement is bit `≈n`; the missing factor is `Θ(n/log n)` of depth-reach (the named
> log-vs-linear gap, `NEW_METHODS_SWEEP` §1), and nothing in the combination crosses it.

**Why each angle's own escape does not help the other.**
- #2 escapes the `δ₁`/LP gate by being **unbounded** (`log` is constant at `δ₁`); but unboundedness buys freedom in
  the **value** of the weight, not in the **depth** of the bit it must read. The bit is still at depth `≈n`.
- #1 is the **only separator both adversaries lack** (no `(3/2)ⁿ` archimedean shadow for the heavy-tail adversary; no
  rotation for `δ₁`); but it separates them at the **top**, where the orbit *is* effectively equidistributed and
  decided — not at the middle, where `(K)` lives. The separator is real but points at the wrong coordinate.

**The precise new sub-lemma that would be needed — and its strength.** For the combination to NOT collapse, one
would need:
> **(SL) Depth-transfer sub-lemma `[OPEN]`:** the orbit's archimedean equidistribution at the top `Θ(log N)` bits
> (Diophantine, #1), composed through the seam with an orbit-adaptive renormalization (#2), forces the moving-middle
> fresh bit `β_n=bit_k(c_n)` to decorrelate from the low state `c_n mod 2^k` for every fixed `k` — i.e. forces
> `Inj_a(N)=(1/N)Σ(β_n−½)χ_a(U(s_n,0))→0` for odd `a`.

`(SL)` is **EQUAL to `(K)`, not weaker** `[PROVEN reduction]`: `(SL)` is verbatim `(CR)` = endogenous unique
ergodicity = single-orbit equidistribution mod `2^k` for all `k` = `(K)` = Mahler-3/2 / AEV at `α=8`
(`EUE_COISOMETRY_NOGO_THEOREM.md` §4, `ENDOGENOUS_UE_BUILD.md` §4, `CORE_CARRY_LEVER.md` §5). There is no weaker
sub-lemma in the gap: the only candidate intermediate object — "the top-foothold equidistribution propagates inward
one scale at a time" — is exactly the infinite regress of §2, which #1's top-end data cannot seed.

**Honest scope.** This probe does **not** prove the combination is impossible in some absolute sense; it proves that
**the specific mechanism proposed** (#1 populates #2's weight) reduces, at the single transfer step, to `(K)` —
i.e. it is the same wall wearing the two least-dead masks at once. That is the program's standard outcome ("collapses
on the gap, here is the exact line"), now established for the last untried combination. The value banked: the
log-vs-linear gap is confirmed to survive even the conjunction of the two angles that individually came closest, and
the collapse is localized to one bit-transfer identity, `bit_k(c_n) = bit_{n+k}(8·3ⁿ) ⊕ bit_{n+k}(S_n) ⊕ ρ_n`, whose
middle term is endogenous.

**No machine decided. No label upgraded. `(K)` remains `[OPEN]` = Mahler 3/2 / AEV.**

---

### Numerics (`scratchpad/hairline_check.py`, exact big-int, `N=2·10⁵`)
| test | what it checks | result | reading |
|---|---|---|---|
| MI(top-mantissa ; parity) | does #1's datum `θ_n={n log₂3}` predict the depth bit `b_n`? | `7.5·10⁻⁵` bits (`Q=16`, max `4`) | **independent** — #1 cannot drive #2 |
| MI(top-mantissa ; `[D≥2]`) | does `θ_n` predict the even-density indicator? | `6.3·10⁻⁵` bits | **independent** (same floor) |
| foothold `k(N)/log₂N` | re-confirm #1's log-depth reach | `D*_N≈3.5·10⁻⁵`, ratio `0.841` | log-depth, matches `FOOTHOLD_EXTENDED.md` |
| depth mean / freq(D≥2) | sanity of the `o_0=27` orbit | `2.0005` / `0.5009` | Haar-consistent; `liminf≥3/2` is the `[OPEN]` content |

### Sources
Internal `[PROVEN/OBSERVED]`: `EUE_COISOMETRY_NOGO_THEOREM.md` (coisometry, `‖Φ‖≡1`, `(CR)⟹(K)`, weight-invariance
via REDTEAM); `MINIMAL_CORE_2ADIC.md` (the minimal target); `FOOTHOLD_EXTENDED.md` + `EFFECTIVE_TOPDIGIT.md`
(log-depth reach `k(N)≈0.85 log₂N`, moving-middle barrier, vdC closed, `U²`-uniform); `DIOPHANTINE_DENSITY.md`
(separation cannot control density; the strongest explicit `log₂3` bounds); `CORE_CARRY_LEVER.md` (seam, `V_even`
lever blind to `V_odd`, scale regress, `I(β;state)≈0`); `CARRY_COBOUNDARY.md` (`β=d⊕σ⊕ρ`, no-telescope `√N`);
`CARRY_EXOGENIZATION.md` (carry net ≈0); `ENDOGENOUS_UE_BUILD.md` (seam identity, §5 regress, `Inj_a→0 ⟺ (K)`).
External `[PROVEN-in-lit]`: Tao (Syracuse, linear-depth equidistribution hypothesis); Oseledets MET; LMN/Zudilin
two-log bounds; Mahler 3/2 (open); Andrieu–Eliahou–Vivion arXiv:2510.11723. Numerics: `scratchpad/hairline_check.py`.
