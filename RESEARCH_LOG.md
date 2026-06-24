# Research log — new mathematics for BB(6)'s open core
*Append-only, dated. Agenda in `RESEARCH_PROGRAM.md`. Discipline: machine-check, verify vs real orbit, 0
false proofs, retract on falsification.*

## 2026-06-24 — Programme established; Milestone M1 first step (D2: self-generated-process uniqueness)
**Set up:** `RESEARCH_PROGRAM.md` — target = hypothesis (H) (diagonal digit equidistributes); 10 dead ends
mapped; live directions D1 (effective measure rigidity), **D2 (fixed-point uniqueness — in-house, started)**,
D3 (carry calculus), D4 (master conjecture); milestones M1–M5.

**M1 first step [numerical partial]:** Among **order-≤2 Markov self-consistent fixed points** of the renewal
operator Φ, there is a **UNIQUE** one = Bernoulli(½) (even-density 0.5). Verified: 13 starts spanning the
parameter box — including adversarially-skewed ones — ALL converge to it (`M1_fixedpoints.py`). Order-1 was
already unique (Bernoulli) and globally attracting (`phi_fixedpoint.py`). So **no self-consistent parity
process of memory ≤ 2 has even-density ≤ 1/3 ⇒ none halts.** Recall the *adversarial* min (no self-
consistency) was 0 — the self-consistency (diagonal) constraint is what collapses the fixed set to {½}.

**Why this matters / path to rigour.** This is the in-house route that sidesteps "specific-orbit vs a.e.":
instead of equidistributing the specific orbit directly, prove the *structural* fact that Φ has a unique
self-consistent fixed point. The proven contraction `δ(P^k)=0` (chain forgets its state in k steps) is the
candidate engine: it should force the output process's dependence on the incoming far-past to decay ⇒ a
unique fixed point. Turning "numerically unique for order ≤ 2" into "provably unique for all orders" is the
M1 research line.

**Next steps (M1):**
1. Extend the fixed-point characterisation to order 3, 4 — confirm uniqueness persists.
2. Prove uniqueness *structurally* from `δ(P^k)=0`: show Φ is a contraction in a process metric (total-
   variation on k-blocks), giving a unique fixed point by Banach — independent of order. This would be the
   first genuinely NEW theorem of the programme (a self-consistency uniqueness theorem).
3. Compute the fixed point's even-density exactly (= 1/p) from the bijection F_k structure.
4. Then: connect "Φ-unique-fixed-point = Bernoulli" to "the real orbit's empirical bit-measure is a Φ-fixed
   point" — the remaining bridge (this is where (H)'s residue concentrates).

## 2026-06-24 (cont.) — M1 structural attempt: D2 clarified as EQUIVALENT to the conditional theorem (redirect)
Pursued M1's structural proof (`δ(P^k)=0 → Φ contraction → uniqueness`). Two findings, both honest negatives:
1. **Φ is NOT a pathwise contraction** (`M1_influence.py`): a single incoming-bit flip's influence on the
   future parity does **not decay** — it jumps to `~0.5` at lag k and stays there (sum of influence diverges).
   So `δ(P^k)=0` (forgets the START) does **not** give forgetting of incoming PERTURBATIONS. The Banach-via-
   pathwise-coupling route fails.
2. **The fixed-point uniqueness is equivalent to (H), not a step past it** [the key realisation]. The
   fixed-point simulations feed incoming bits from an RNG = **independent of the state**. But state-
   independence *is* (H). So "the unique self-consistent process is Bernoulli" really proves
   `(H) ⟹ Bernoulli ⟹ even-density ½ ⟹ non-halt` = **the conditional theorem we already hold**. The real
   orbit's incoming is *state-coupled* (incoming `bit_k(c_n)` and state `c_n mod 2^k` are digits of the same
   `c_n`); RNG-feeding erases exactly that coupling. **D2 presupposes (H); it does not advance toward proving it.**

**Consequence for the programme.** **D2 (self-generated-process uniqueness) is closed** as a route to (H):
any analysis that feeds the incoming independently of the state assumes (H). A genuine attack must engage the
**state–incoming coupling of the actual deterministic orbit** — which is exactly what D1 (effective measure
rigidity: control a specific orbit, coupling intact) and D3 (carry calculus: the arithmetic of the coupling)
are about. The in-house D2 shortcut does not exist.
- **6th tempting result caught on scrutiny** (the M1 "partial" assumed (H)). Discipline holds: 0 false claims.
- **Revised next step:** pivot to **D3 (carry calculus)** — the most concrete coupling-respecting in-house
  line: model the carry of `×3` into the moving bit directly and seek any unconditional anti-concentration,
  however weak (Milestone M2: any non-trivial unconditional bound). And begin reading into **D1** (effective
  equidistribution) as the external frontier.

## 2026-06-24 (cont.) — D3 carry calculus: foundation laid + a genuine AFFINE structural lead
Pivoted to D3 (coupling-respecting, in-house). Set up and **verified** the carry calculus
(`D3_carrycalculus.py`, `D3_linear.py`):
- **Exact identities [verified]:** `2^n c_n = 8·3^n − S_n`, `S_{n+1}=3S_n+2^n[c_n odd]`, and
  `depth_n = v2(8·3^n − S_n − 2^n) − n`.
- **Trivial bound only:** empirically `depth_n ≤ 0.319·log2(c_n)`, but the provable (trivial) ceiling is
  `depth_n ≤ log2(c_n) ≈ 0.585n`. Closing even this factor-3 gap unconditionally is open (Milestone M2).
- **★ Structural lead [verified, genuinely new handle]:** `S_n = Σ_{j<n, c_j odd} 2^j 3^{n−1−j}` is **LINEAR
  in the parity bits** `e_j=[c_j odd]` (explicit coefficients), so **`depth_n ≥ L ⟺ S_n ≡ 8·3^n−2^n
  (mod 2^{n+L})` is an AFFINE condition on the parity history.** The even-density / depth statistics are
  therefore controlled by **linear forms** in `(e_0,…,e_{n−1})` with explicit `2^j3^{n−1−j}` coefficients.
- **Why it's promising (and honest about limits):** linear/affine conditions are the regime where
  **exponential-sum / Fourier methods** can succeed even when the nonlinear digit-equidistribution cannot
  (cf. the Mahler wall is fundamentally *nonlinear*). This is a handle the other directions lacked. The
  self-reference (`e_j` is itself a low bit of the orbit) is NOT removed — but the concrete D3 sub-problem is
  now sharp: **bound the linear-form exponential sum `Σ_n e(t·Φ_n(e))`** where `Φ_n` is the explicit affine
  depth-form, using the `2^j3^{n−1−j}` (mixed 2,3) coefficient structure. *Not* the same as the general
  equidistribution — a genuinely different, more linear target.
- **Status:** D3 foundation + lead established; **no unconditional bound yet** (no over-claim — this is a
  framework + a sharp sub-problem, not a result). This is now the most promising live in-house direction.
- **Next (D3/M2):** (i) write the affine depth-form `Φ_n(e)` explicitly; (ii) attempt a 2nd-moment / large-
  sieve bound on `Σ_n e(t·Φ_n)` exploiting the linearity (where the nonlinear large sieve died on self-
  clustering, the *linear* form may separate); (iii) target any unconditional `even-density ≥ ε` partial.

## 2026-06-24 (cont.) — D3 dive-in: linear-form sum evaluated; controls off-diagonal, diagonal still open
Evaluated the linear-form exponential sum `Σ_n e(t·S_n/2^M)` (`D3_linearsum.py`, `D3_position.py`):
- **Fixed-modulus cancellation is REAL and UNCONDITIONAL** [verified]: `|Σ e(t S_n/2^M)|/√N ≈ 0.01–0.12`
  (sub-√N). Reason: for `n ≥ M`, `S_n ≡ 3^{n−M}S_M (mod 2^M)` — the `×3`-isometry coset; the character sum
  over the coset is small (Gauss/Ramanujan-type), provably.
- **But it controls the WRONG position** [7th over-claim AVOIDED by checking]: this cancellation is at the
  **low bits** of `S_n` (`×3`-isometry, *off-diagonal*) — the part already known fine. The even-density /
  depth need the bit at the **moving/middle position** (`parity e_n = bit_n(8·3^n−S_n)`; `c_n mod 2^k` =
  bits `[n,n+k]`), i.e. the **diagonal**. The lowest set bit of `S_n` sits at position ~3 (bounded); the
  depth-relevant bit at position ~`n` (grows). The linear structure controls the low end, not the middle.
  **Same opposite-ends wall. NOT a crack.**
- **D3 is NOT dead (unlike D2).** The linear structure is a genuine handle and the remaining target is **sharp
  and genuinely linear**, unlike the general nonlinear equidistribution: *bound the MOVING-modulus linear
  exponential sum `Σ_n e(t·Φ_n(e))` with the explicit `2^j 3^{n−1−j}` coefficients, where the modulus
  `2^{n+L}` grows with `n`.* Fixed-modulus is solved (character sum); the moving-modulus linear sum is the
  open core — but it is a LINEAR object, a different (and arguably more approachable) target than Mahler's
  nonlinear wall.
- **Status:** D3 mapped; off-diagonal part unconditionally controlled; the sharp open sub-problem isolated
  (moving-modulus linear exp-sum). No unconditional even-density bound yet; no over-claim. D3 remains the
  most promising live in-house direction.
- **Next (D3):** attack the moving-modulus linear sum directly — (i) van der Corput on the LINEAR phase
  (differencing a linear form may NOT be closed the way the multiplicative `(3/2)^n` was — worth checking);
  (ii) a large-sieve over the modulus family `{2^{n+L}}` exploiting linearity; (iii) connect to Stewart/Baker
  bounds on the digits of `3^n` (the coefficients are `3^{n−1−j}`).

## 2026-06-24 (cont.) — D3: vdC tested (reduces to autocorrelation wall); M2 partials reduce to equidistribution
Continued D3 by testing van der Corput on the linear/parity sum (`D3_vdc.py`):
- **vdC does not open a new angle [tested].** The parity sum `Σ(-1)^{e_n}` already shows `√N` cancellation
  (`|S|/√N=0.70`); vdC needs the lag-k autocorrelations `A_k` to be `o(1)` — they are `~0` empirically
  (`|A_k/N| ≤ 0.005`) but proving `Σ_k A_k = o(N)` IS the equidistribution. The linearity is in the bits
  `e_j`, not in `n`; vdC (which exploits `n`-smoothness) does not engage it. **Reduces to the wall.**
- **M2 partials reduce to equidistribution [analysed].** `P(depth≥L)=2^{-L}` empirically to high precision.
  But `depth_n≥L ⟺ c_n≡1 mod 2^L` ⟺ odd-run length ≥ L; the only *unconditional* bound from run-disjointness
  is `#{runs ≥ L} ≤ N/L` (far weaker than the needed `N·2^{-L}`). `even-density ≥ ε` similarly needs the
  orbit to hit `3 mod 4` with positive density = equidistribution mod 4.
- **One genuine (tiny) unconditional fact [recorded]:** the orbit **cannot avoid `3 mod 4` forever**
  (avoiding it forces `c_n≡1 mod 2^k ∀k ⇒ c=1`), and `c_n≡3 mod 4 ⇒ c_{n+1}` even ⇒ **infinitely many even
  terms**. (Only "infinitely many", not positive density.)
- **Status:** vdC ruled out for D3; M2 partials shown to reduce to equidistribution; the only provable
  unconditional statement so far is "infinitely many evens". No over-claim. The sharp D3 target is unchanged
  (moving-modulus linear exp-sum) but now to be attacked by **large-sieve / Stewart–Baker** (the coefficients
  `3^{n-1-j}` are powers of 3 — Stewart bounds the nonzero binary digits of `3^m`), NOT by vdC.
- **Next (D3):** (i) make precise the second-moment / large-sieve over the modulus family `{2^{n+L}}` for the
  linear form, checking whether the *linear* points avoid the `1/N²` self-clustering that killed the
  nonlinear sieve; (ii) look up / derive the exact Stewart-type bound on binary-digit runs of `3^m` and test
  if it bounds the depth. (Marathon: D3 alive, no quick win, walls mapped.)

## 2026-06-24 (cont.) — D3: large-sieve + Stewart both tested, both ruled out; core is a 2-adic diagonal sum
Tested D3's remaining two tools (`D3_sieve_stewart.py`):
- **Large-sieve: ruled out.** The linear form `S_n mod 2^M` avoids the `1/N²` Diophantine self-clustering
  that killed the nonlinear sieve (good) — but it lives on the **×3-coset, a thin subgroup of size `2^{M−2}`**.
  The 2nd moment `(1/(2^M-1))Σ_t|Σ_n e(t S_n/2^M)|² ≈ 189·N ≫ N`: the points concentrate on the subgroup
  (many collisions), so the large sieve over `ℤ/2^M` gives no useful bound. The off-diagonal is already
  handled by the character sum; the sieve adds nothing.
- **Stewart–Baker: ruled out (disconnected).** `corr(depth_n, #nonzero-binary-digits(3^n)) = +0.03 ≈ 0`.
  Stewart bounds the **archimedean/global digit COUNT** of `3^n` (→∞, ~161 by n=400); the depth is the
  **2-adic TRAILING-zero count** of `c_n−1` (`O(log n)`, max 20). Archimedean tools do not see the 2-adic
  depth.
- **Synthesis [honest].** All standard tools for the linear exponential sum — vdC, large-sieve, Stewart —
  are now **ruled out for D3's core**. The reason is unified: the linear/2-adic structure controls the
  **off-diagonal (low bits, ×3-subgroup, character-sum cancellation)** unconditionally, but the depth /
  even-density live at the **moving-modulus diagonal (middle/position-n bits)**, and no archimedean or
  fixed-modulus Fourier tool reaches it. D3 is **mapped, not dead**: the linear structure is a real asset
  (off-diagonal control), but the **core is a genuinely-new 2-adic diagonal sum** — the same new-math need,
  now pinned in the linear/2-adic language.
- **Programme status:** D2 closed (circular); D3 core isolated (needs a novel 2-adic tool, not vdC/sieve/
  Stewart). **The remaining external hope is D1 (effective measure rigidity / ELV)** — not yet engaged; it
  is the one framework designed to control a *specific* orbit (coupling intact) and the live 2020s frontier.
- **Next:** engage D1 — read into effective equidistribution (Einsiedler–Lindenstrauss–Venkatesh / BLMV),
  identify the precise Diophantine-genericity condition, and test whether the Antihydra seed/orbit could
  satisfy it. (Marathon: all in-house Fourier/sieve routes mapped; the 2-adic-diagonal core and D1 remain.)

## 2026-06-24 (cont.) — D1: rigidity is RANK>=2, the orbit is RANK 1 (doesn't apply); FIRST-PASS SYNTHESIS
**D1 assessment (`D1_rank.py`):** Antihydra iterates ONE map (`×3/2`) ⇒ the orbit is **RANK 1**. Measure
rigidity / effective equidistribution (Furstenberg–Rudolph–Lindenstrauss–ELV/BLMV) are **RANK ≥ 2**
phenomena (they classify measures invariant under the FULL `{×2,×3}` or higher-rank action). Rank-1 maps
have a *continuum* of invariant measures — **no rigidity**. Verified: the `(3/2)ⁿ` orbit is not `×2`/`×3`-
invariant (it is only the diagonal `×3/2` sub-direction of the rank-2 action). **D1 does not apply.** This
names the earlier `×2,×3` obstruction precisely: **RANK**.

## FIRST-PASS SYNTHESIS — the obstruction map (why every existing tool fails, precisely)
All four programme directions + the 10 earlier attacks are now assessed. Each fails for a *precise,
fundamental* reason:
| tool / direction | precise reason it fails |
|---|---|
| van der Corput / Weyl differencing | **closed** on the multiplicative recurrence `(3/2)ⁿ` (fixed point of differencing) |
| sum-product (Bourgain–Konyagin) | needs subgroup `≥ q^δ`; here `{3ʲ mod 2ᵏ}`, `k~cn`, is **log-size** — exp below threshold |
| Fourier / large-sieve / Stewart (D3) | control the **off-diagonal** (low bits, `×3`-subgroup); the depth is a **2-adic moving-diagonal** they don't reach |
| measure rigidity / ELV (D1) | a **rank ≥ 2** phenomenon; the orbit is **rank 1** (single map) |
| self-consistency fixed point (D2) | **circular** — presupposes independence = (H) |
| subspace theorem | fixed algebraic number vs **moving integer orbit** |
**Net:** no existing framework applies. A proof of (H) requires a genuinely NEW tool that does at least one
of: **(α)** establish equidistribution of a **rank-1 specific orbit** of `×(2^a/3^b)` (beyond rigidity's
rank-≥2 scope), or **(β)** control the **2-adic moving-diagonal digit** of such an orbit (beyond the
off-diagonal reach of Fourier/sieve). These two are the precisely-characterised requirements for the new
mathematics. The marathon's **phase 1 (map the terrain) is complete**; phase 2 is to **invent (α) or (β)** —
genuinely new, years-scale.

**Honest constructive deliverable now:** D4 — (H) is already a *named* open problem (Mahler-3/2 / Erdős),
stated paste-ready in `BB6_KERNEL_PROBLEM.md`; it is the clean special case "rank-1 `2^a/3^b`-orbit
equidistribution" of (α). No standard conjecture *more tractable than Mahler* implies it. Discipline intact:
0 false proofs; 7 tempting leads retracted on scrutiny across the session.

## 2026-06-24 (cont.) — (alpha)/(beta) frameworks built; first unconditional partial; honest phase-2 boundary
**(beta) first genuine partial [UNCONDITIONAL]:** `E_n = Ω(log n)` even terms. Proof: consecutive even
positions satisfy `p_{i+1} ≤ p_i + depth_{p_i} ≤ p_i + log2(c_{p_i}) ≈ 1.585 p_i` (geometric), so
`E_n ≥ log N / log 1.585 ≈ 2.2 log N`. Verified (`alphabeta_build.py`; empirical gap ratio ≤ 1.19, provable
≤ 1.585). Beyond "infinitely many evens"; still far below positive density. **New open core (beta):** improve
the trivial `depth_n ≤ 0.585n` to `o(n)` — a sub-linear 2-adic depth bound for the self-referential
linear-feedback carry `S_n`. (Linear structure controls off-diagonal; `o(n)` needs the diagonal.)
**(alpha) framework:** target `Σ e(h(3/2)^n)=o(N)`; provable input `{n log2 3}` equidist (Benford, top
`log n` bits); required NEW input = rank-1 effective Furstenberg reaching depth `εn`, with a Diophantine
condition on `log2 3` (CF `[1,1,1,2,2,3,1,5,2,23,...]`, max pq 55, not Liouville; discrepancy `(log N)/N`
controls only `O(log n)` top bits = the foothold wall).

**HONEST PHASE-2 BOUNDARY.** Across the marathon: 10 attacks + 4 directions mapped, 7 leads retracted on
scrutiny, all data distilled (`NEW_MATH_MATERIALS.md`), (alpha)/(beta) frameworks + first partials built. The
*foundational* work — translating BB(6)'s kernel into one precisely-characterised object with stated
new-tool requirements and first unconditional partials — is DONE. **Constructing the new tools themselves
((alpha) rank-1 effective equidistribution; (beta) sub-linear self-referential 2-adic depth bound) is a
years-scale research frontier and is NOT completed here** — no existing technique reaches it (the obstruction
map proves why), and inventing a new one is beyond a single effort. This is stated plainly, not as defeat:
the marathon delivered the *substrate and the map*, which is exactly the prerequisite an eventual proof is
built on (Taniyama–Shimura before Wiles; Thurston before Perelman). Discipline intact: 0 false proofs.

## 2026-06-24 (cont.) — Phase-2: engaged Tao (2019), the closest frontier tool; confirms (beta) is beyond SOTA
Engaged the most relevant recent technique: **Tao (2019), "Almost all orbits of the Collatz map attain almost
bounded values"** — transport/entropy machinery on the Syracuse distribution, built for exactly 3x+1-type
carry dynamics (`phase2_tao.py`):
- Our Syracuse-type object (renewal jump heights `D_j=v2(3c'−1)`) along the single orbit: mean `0.9993→1`,
  geometric tail, `√N` concentration — matches Tao's transport prediction.
- **BUT Tao's theorem is for ALMOST ALL starting points (log-density 1); it explicitly decides NO single
  orbit.** Antihydra is ONE specific orbit (seed 8). Tao's machinery equidistributes the digit distribution
  *averaged over starts*; for a fixed orbit it gives nothing — the same specific-vs-generic wall.
- **Conclusion:** Tao's method is the **closest existing technique to (beta)** yet still hits the wall. The
  new tool must do **for one orbit what Tao does for almost all** — open even post-Tao (single-orbit
  Collatz-type bounds remain unproven). Added to the obstruction map.

**Updated obstruction map (now includes the SOTA):** the new tool must surpass *all* of: van der Corput
(closed), sum-product (regime), Fourier/sieve/Stewart (off-diagonal), rigidity/ELV (rank≥2), self-consistency
(circular), subspace (fixed-vs-moving), **and Tao-transport (almost-all-vs-single-orbit)**. Every known
technique — including the 2019 frontier — fails on the *single specific orbit*. **Phase-2 = building a
single-orbit equidistribution method beyond Tao** — the genuine open frontier; not session-completable.
Discipline intact: 0 false proofs; the Tao engagement was assessed honestly (it does NOT apply), not claimed.

## 2026-06-24 (cont.) — External review (a number theorist): 2 corrections + the one-sided-density reframing
A reviewer gave sharp feedback on `STATE_FOR_REVIEW.md`. Both technical points were CORRECT and are fixed
(an 8th over-claim, caught externally — discipline working as intended):
1. **"non-halt ⟺ depth=o(n)" was OVERSTATED.** Verified (`verify_criterion.py`): the EXACT criterion is
   `non-halt ⟺ balance_n = 3E_n − n ≥ 0 for ALL n ⟺ running even-density ≥ 1/3 at every prefix`. `depth=o(n)`
   and equidistribution are **SUFFICIENT** (the heuristic), not equivalent; non-halt does not force `depth`
   sublinear. Corrected the ⟺ chain to an implication chain.
2. **"(H) ⟺ diagonal equidistribution" weakened** to "(H) is sufficient for non-halt; under the renewal
   coding it reduces to / is implied by diagonal-digit equidistribution."

**The reframing (reviewer's best point) — NEW PRIORITY DIRECTION:** Antihydra needs only the **one-sided**
`even-density > 1/3`, NOT full equidistribution `= 1/2`. In renewal terms:
```
even-density = 1/(1 + avg jump),   so   even-density > 1/3  ⟺  avg jump height  D_j = v2(3c'_j − 1)  ≤ 2.
```
The true value is `avg D = 1`, so the target `≤ 2` has a **factor-2 margin** — a *crude* one-sided method that
loses constants could still land it. Equivalently: `Σ_k density{ c'_j ≡ 3^{−1} (mod 2^k) } ≤ 2` (one-sided
summability), strictly weaker than the `= 2^{−k}` of equidistribution. **This is the most hopeful near-term
target** and may admit a weaker-than-equidistribution tool. (Our only current one-sided result is
`E_n = Ω(log n)`; the trivial depth bound `D_j ≤ 0.585·position` gives only `E_n ≥ O(1)`.) Added as
**question 6** for reviewers and as the prioritised (β)-variant: *prove `avg jump ≤ 2` (one-sided), not full
equidistribution.*

**Reviewer's meta-point (agreed):** even with no proof, the achieved reduction — Antihydra non-halting to a
**single-orbit, moving-digit equidistribution of Mahler-3/2 / Erdős-ternary type** — is itself the value.

## 2026-06-24 (cont.) — 3rd review pass: soften "iid", clarify Q5 self-reference, ADD Q7 (coordinate-artifact)
Incorporated a third reviewer round (all valid):
- "Renewal jumps are iid-geometric" → "**behave as** an iid-geometric renewal process" (established:
  geometric tail + lag-k decorrelation + renewal mixing; full independence NOT claimed).
- Q5: "linear in the bits" → "linear in the parity variables `e_j` **once the orbit is fixed**" (the `e_j`
  are self-referential — preempts the obvious objection).
- **Added Q7 (deep):** is the moving-2-adic-diagonal obstruction *intrinsic*, or an **artifact of our
  coordinates**? Is there a coordinate change / solenoid extension / symbolic realization making it a FIXED
  observable? (A breakthrough may be a re-coordinatization, not a new theorem.)

**Our own first thought on Q7 [worth recording]:** the *natural* coordinate change — to the (2,3)-solenoid,
where `α=×(3/2)` acts — DOES convert the moving 2-adic diagonal into a **fixed observable `f` evaluated along
the orbit `α^n(x_0)`**. But that is exactly **(α): rank-1 specific-orbit equidistribution**, which rigidity
does not reach (rank-1 in any coordinate). So the solenoid re-coordinatization **links (β) ⟷ (α)** — the
moving-diagonal (arithmetic) and the rank-1-orbit (dynamical) are the SAME obstruction in two coordinate
systems, and the natural change moves between them without escaping. **Open (the real content of Q7):** is
there a *non-obvious* re-coordinatization (not the solenoid) landing in a regime where standard
mixing/equidistribution applies? If yes, that — not a new theorem — is the breakthrough.

**Strategic note (agreed with reviewer):** Route B (prove one-sided `density > 1/3` only, via `avg jump ≤ 2`
with its factor-2 margin) is more attractive than Route A (solve Mahler-3/2 fully). Prioritise B.

## 2026-06-24 (cont.) — Attacked Route B (one-sided) and Q7 (coordinates), in order
**Route B [sharpened, `routeB.py`].** Renewal reframing: `non-halt ⟺ centered jump-sum Σ_{j≤J}(D_j−1) ≤ J
for all J` (J = #even-steps). Measured: max centered sum `792` vs the bound `J ≈ 2×10^5` — a **~250× margin**
(true ~`√J`, need `≤ J`). The weakest sufficient target: **`Σ_{j≤J} v2(3c'_j−1) = O(J)` for ANY constant C**
(= positive even-density `≥ 1/C`; `C ≤ 2` gives `> 1/3`), strictly weaker than equidistribution (exact C=2
with `o(J)` error). **Still open:** trivial `depth ≤ 0.585·pos` gives only `n_J ≤ 1.585^J` (exponential ⇒
`Ω(log)` evens), far from the needed `n_J ≤ 3J`. **Sharp Route-B sub-problem (the most tractable target in
the whole programme): prove `Σ_{j≤J} v2(3c'_j−1) = O(J)` unconditionally** — bounded *average* 2-adic
valuation of `3c'_j−1` along the induced orbit. (A crude pigeonhole/energy bound, not equidistribution, might
suffice given the 250× margin — this is the live hope.)
**Q7 [analysed, `Q7_coords.py`] — the obstruction is part-artifact, part-intrinsic.** Both the (2,3)-solenoid
and the induced first-return map convert the moving 2-adic diagonal into a **fixed observable** (e.g.
`D_j=v2(3c'_j−1)` is a fixed function of `c'_j`). So the *moving diagonal* IS a removable coordinate artifact.
BUT every such coordinate keeps the orbit **rank-1** (one map), and rank is coordinate-invariant; the natural
changes merely move between the arithmetic (β) and dynamical (α) faces. The orbit is the diagonal `a=b=n`
slice of `3^a/2^b` and does not fill the rank-2 `{×2,×3}` action (verified: not `×2`/`×3`-invariant), so no
rank-2 embedding from this slice. **Verdict:** breakthrough needs either a *non-obvious* coordinate embedding
the rank-1 slice into a rank-≥2 / mixing structure (resisted by the 1-D slice), or a new rank-1 tool. The
*intrinsic* obstruction is **rank-1 specific-orbit**, not the (removable) moving diagonal.
**Net:** Route B gives the single most tractable open target (`Σ v2(3c'_j−1) = O(J)`, positive density, 250×
margin); Q7 clarifies that re-coordinatization alone won't escape (rank-1 is intrinsic). Both fed into
`STATE_FOR_REVIEW.md` (§6, Q7). 0 false proofs.

## 2026-06-24 (cont.) — Route B crude attack: Markov/growth/Lyapunov all fail; gap = first-moment vs distribution
Attacked the weakest target `Σ_{j≤J} v2(3c'_j−1) = O(J)` (positive density) with crude methods (`routeB_crude.py`):
- **Pigeonhole/Markov gives NOTHING.** `#{D_j ≥ k} ≤ (Σ D_j)/k` is just the identity `Σ D = Σ_k #{D≥k}` —
  auto-consistent, no constraint on `Σ D`. **Crisp data:** the actual `#{D_j ≥ k}` matches **equidistribution
  `J/2^k`** to ~1%, while the only *provable* bound is **Markov `Σ D / k`** which is 2× too weak at k=2 and
  exponentially too weak (3000×) at k=16. **The gap between provable (first moment `Σ D/k`) and truth
  (distribution `J/2^k`) IS the kernel.** (Second moment `Σ D²` via Markov is likewise useless.)
- **Growth/Lyapunov fails.** The target `Σ D = O(J)` ⟺ induced orbit `c'_J` grows `≤ exp(O(J))` ⟺ bounded
  average per-step factor `(3/2)^{D+1}`; but the trivial `depth ≤ 0.585·pos` allows that factor **unbounded**
  (large D), so no unconditional growth bound. (Growth is parity-blind, as always.)
- **Finite-state Lyapunov is PROVABLY impossible** (earlier min-mean-cycle: adversarial even-density = 0).
**Verdict:** the 250× margin is real, but every crude method (first-moment / growth / finite-state Lyapunov)
fails — controlling `Σ v2(3c'−1)` needs the **distribution** of `c'_j mod 2^k`, not just its first moment, and
that is the (one-sided) kernel. The live hope (a non-crude method beating the first moment with the huge
margin) remains, but no concrete such method yet. This sharpens the Route-B target to: **beat the trivial
first-moment bound `#{D_j≥k} ≤ ΣD/k` toward `O(J·2^{−k})` (or even just summable) by ANY unconditional means.**

## 2026-06-24 (cont.) — ROUTE B BREAKTHROUGH (conditional): the MOMENT / additive-energy method
The non-crude (2nd/higher-moment) attack on Route B yields a genuinely new **conditional theorem**
(`routeB_energy.py`, `routeB_moments.py`):
- `avg jump = (1/J) Σ_k N_k`, `N_k = #{j≤J : c'_j ≡ 3^{−1} mod 2^k}`. Hölder: `N_k ≤ (Σ_r count_r(k)^{2m})^{1/2m}`.
- If the `2m`-th moment `M_{2m}(k)=Σ_r count_r^{2m} = O(J^{2m}/2^{(2m−1)k})` (random order), then
  `N_k = O(J·2^{−k(2m−1)/2m})` and `avg jump ≤ C^{1/2m}·Σ_{k≥1} 2^{−k(2m−1)/2m}`.
- **Thresholds:** 2nd moment ⟹ even-density `≥ 0.293` (near-miss); **4th moment ⟹ `≥ 0.405 > 1/3`** ✓;
  6th ⟹ `0.44`. With the *empirical* constant `C≈1.3` (need `C≤3.45`), the 4th-moment bound gives
  even-density `≥ 0.39 > 1/3` — comfortable margin.
- **CONDITIONAL THEOREM [logic rigorous, hypothesis open]:** *if the 4th additive-energy moment
  `Σ_r count_r(k)^4 ≤ C·J^4/2^{3k}` (`C ≤ 3.45`) for the induced-orbit residues `c'_j mod 2^k`, then
  even-density `≥ 1/3` and Antihydra never halts.* Empirically the 4th moment is `~1.3×` random.
- **Why this is the strongest lead:** it reduces non-halt from **full equidistribution** (the Mahler kernel)
  to a **4th additive-energy / moment bound** — a DIFFERENT, additive-combinatorial target. The relevant
  object is `#{(i₁,…,i₄): c'_{i₁}≡…≡c'_{i₄} mod 2^k}` ⟺ `v2(c'_i − c'_j) ≥ k` collisions of a geometric-growth
  induced orbit (`c'_{j+1} ≈ (9/4) c'_j`); the differences are S-unit-like, so **p-adic Baker / linear forms
  in logarithms may bound `v2(c'_i − c'_j)`**, and additive-energy machinery may bound the moment. This is the
  natural place for additive-combinatorics expertise.
- Discipline: the implication is verified; the moment bound is NOT claimed (conditional). No over-claim.

## 2026-06-24 (cont.) — §6.5 attack: the induced map F is a NON-UNIFORMLY EXPANDING 2-adic map (new framework)
Attacking the §6.5 additive-energy hypothesis, examined the 2-adic local structure of the induced map
`F(c')=(3^D u+1)/2` (`F_expansion2.py`). [Caught & fixed my own error: `v2(3^D)=0` not `D` — 10th over-claim
avoided by verification.] **VERIFIED (100%, 2.9×10^5 trials):**
> `v2(F(c') − F(c'')) = v2(c' − c'') − D − 1`, where `D = v2(3c'−1)` (when jumps match, i.e. `D < separation`).
So **F is 2-adically EXPANDING with local factor `2^{D+1} ≥ 2`** — NON-UNIFORMLY (bigger jumps expand more,
but are geometrically rarer).
**Why this is a genuinely new route (not in the obstruction map):**
- The §6.5 additive-energy / collision bound `#{(i,j): v2(c'_i−c'_j) ≥ k} = O(J^2/2^k)` is exactly a
  **decay-of-correlations** statement, which a **transfer-operator (Ruelle–Perron–Frobenius) spectral gap**
  for the expanding map F would give. **Transfer operators work at RANK 1** (single map) — unlike measure
  rigidity (rank ≥ 2), which is why this evades that obstruction.
- The technical crux is the **non-uniformity** (large jumps `D` = strong but rare expansion) = the renewal
  tail, but this is precisely the regime of **non-uniform hyperbolicity machinery (Young towers, inducing,
  the induced map IS the inducing!)** — a real, developed area.
- **Honest status:** F is verified non-uniformly 2-adically expanding; the additive-energy bound is RECAST as
  a transfer-operator spectral gap / decay-of-correlations for F. This is a candidate framework, NOT a proof
  (the spectral gap for this specific 2-adic non-uniformly-expanding map, and the specific-orbit-vs-SRB-measure
  step, remain to establish — though additive energy is a 2nd-order/mixing statistic, possibly more amenable
  than pointwise equidistribution). New target: **a spectral gap / exponential mixing for the transfer
  operator of F on `ℤ₂`** (with the renewal/Young-tower handling the large-jump tail).
- This adds a column to the obstruction map's *opposite*: thermodynamic formalism for the INDUCED expanding
  map is rank-1-compatible and aims at the (weaker) additive energy, not full equidistribution. Best lead.

## 2026-06-24 (cont.) — §6.5/Q9: F is a FULL-BRANCH PIECEWISE-AFFINE EXPANDING (Gibbs-Markov) map of ℤ₂
Pinned down F's structure (`F_piecewise.py`), answering the reviewer's "which function space?":
- **VERIFIED (100%):** on each cylinder `P_D = {v2(3c'−1)=D}`, `F(c') = (3^{D+1}c' − 3^D + 2^D)/2^{D+1}` —
  **piecewise affine**, 2-adic slope `(3/2)^{D+1}`, expansion `2^{D+1} ≥ 2`, **zero distortion** (affine).
- **Full branches (Markov):** each `P_D` (Haar measure `2^{−(D+1)}`, geometric, summing to 1) maps **onto all
  of ℤ₂** (F mod 256 hits 256/256 for D=0..3). So F is a **full-branch piecewise-affine expanding map of ℤ₂**,
  Haar-preserving (Kac) — i.e. a **Gibbs–Markov system**, the cleanest classical setting for transfer operators.
- **Function space [reviewer's Q, ANSWERED]:** the Ruelle operator acts on **locally-constant / Lipschitz
  functions w.r.t. the 2-adic metric**; the additive-energy observables (`2^k`-cylinder indicators) are
  locally constant ⇒ in the space. For Gibbs–Markov maps, **exponential decay of correlations on Lipschitz
  is classical** (Aaronson–Denker; provided the standard tail/big-image conditions hold — plausible here,
  full affine branches with geometric widths).
- **The crux / honest remaining gap [11th over-claim guarded].** Decay of correlations is a statement for the
  **invariant (Haar) measure**. The additive energy is along the **specific orbit** `c'_j`:
  `E_2(k) = Σ_d #{i≤J : F^d(c'_i) ≡ c'_i (mod 2^k)}` = the orbit's visits to the (cylinder) return-sets. This
  **may reduce to the specific-orbit equidistribution** (the same wall) — OR the *one-sided* additive-energy
  bound (§6.5 only needs `≤ C·random`) may follow more robustly from the spectral gap than pointwise
  equidistribution does. **This is the precise open question for an ergodic-theory expert.**
- **Net:** the problem is now placed in the **classical Gibbs–Markov / transfer-operator framework** — a
  different, well-developed battlefield, rank-1-compatible, aiming at the weaker additive-energy target. The
  function space is identified; the spectral gap is classical for the measure; the only question is the
  measure→specific-orbit step for the (one-sided) additive energy. Strongest and most novel lead of the
  programme. (Added to STATE_FOR_REVIEW Q9 / §6.5.)

---

## 2026-06-24 — Q9(b) RESOLVED (negative, rigorous): spectral gap is orbit-blind; the bound is orbit-specific
Attacked the construction "spectral gap ⟹ single-orbit visit-count bound." It does NOT exist, and this is a
**provable obstruction** (not a gap to be bridged). Verified, `Q9b_obstruction.py`:
- **(1) The transfer operator `L` and its spectral gap depend on `(F, Haar)` ALONE** — they are insensitive
  to any individual orbit. [definitional]
- **(2) F has a fixed point `x_D = (3^D−2^D)/(3^{D+1}−2^{D+1}) ∈ ℤ₂` on EVERY branch `D`** (verified exactly:
  `0, 1/5, 5/19, 19/65, 65/211, 211/665, …`; all odd-denominator ⇒ genuine 2-adic integers; `F(x)=x` and the
  branch condition `v2(3x−1)=D` both hold exactly). Being full-branch expanding, F has periodic points of all
  periods (a full shift). A constant/periodic orbit visits a single (resp. `p`) `2^k`-cylinder(s), giving
  `M_4 = J^4` (resp. `J^4/p^3`) `≫ J^4/2^{3k}` = the random target. **So the M_4 bound is FALSE for these
  orbits of F.**
- **(3) Even integer seeds shadow these periodic points and over-concentrate on a window** (verified): the
  integer `≡ 1/5 (mod 2^60)` shadows the fixed point for ~27 steps and has `M_4` up to **~7000× the random
  target** on the shadow window. So the failure is concrete, not exotic.
- **Conclusion (rigorous).** A property of `(F,Haar)` alone (the spectral gap, by (1)) cannot imply a bound
  that is false for some orbits (by (2)–(3)). **∴ spectral gap ⇏ single-orbit M_4 bound. The bound is
  intrinsically orbit-specific** and requires orbit-specific input on the seed (`c'_0 = 6`): at minimum a
  **non-shadowing / 2-adic-Diophantine** property (the seed is not too-well approximable by periodic points).
- **This is the SAME single-orbit wall, precisely relocated** — confirming the reviewer's intuition that the
  real open core is "single-orbit extraction from a Gibbs–Markov system," NOT Mahler-3/2 per se. It is the
  exact analogue of Tao(2019)'s almost-all-vs-single-orbit barrier, now seen inside the transfer-operator
  framework.
- **Positive residue (what the gap DOES give).** For `μ`-almost-every seed the bound holds; the gap gives the
  exact mean `J·2^{−k}`, variance `O(J·2^{−k})`, and a large-deviation rate function for the visit counts.
  So Route C **re-derives the central reduction** ("seed 8/6 is non-exceptional" = language 2 of §5) and pins
  the residual input to a sharp, named, more concrete target than "Mahler."
- **Sharpened open question (for experts), replacing the vague Q9(b):** is a non-shadowing / 2-adic-Diophantine
  condition on the seed (a) *sufficient*, via the spectral gap + large-deviation machinery, for the one-sided
  `M_4 = O(J^4/2^{3k})` bound, and (b) *strictly weaker* than full Mahler-type equidistribution? If yes to
  both, Route C genuinely reduces the difficulty; if (a) needs full equidistribution, the wall is confirmed
  identical. Verified assets: fixed-point list + shadowing demo (`Q9b_obstruction.py`).
- **Discipline:** this is a NEGATIVE result, stated as such; no claim that Antihydra is proved. It is the
  honest localization the programme is now producing ("specify the wall" phase). 0 false proofs maintained.

---

## 2026-06-25 — Q9(b) sufficiency RESOLVED: (i) non-shadowing NOT sufficient; (ii) NOT weaker than equidistribution
Pushed on the sharpened question (does non-shadowing/Diophantine input + spectral gap suffice for the
avg-jump/M_4 bound, and is it strictly weaker than Mahler-type equidistribution?). Both answers are negative,
by a **decisive construction** (`Q9b_sufficiency.py`, verified):
- **Setup.** The needed bound is `avg jump = (1/J) Σ_{k≥1} N_k ≤ 2`, `N_k = #{j<J: c'_j ≡ 3^{-1} mod 2^k}`
  (a single nested cylinder's visit count); even-density `= 1/(1+avg jump)`, threshold `avg jump ≤ 2`. Haar
  gives `avg jump = 1`. §6.5 bounds each `N_k` through the symmetric moment `M_4`.
- **(i) NO — non-shadowing is NOT sufficient.** Using the full-branch coding (`F` ≅ a full shift), every
  branch itinerary is realized by a unique point (inverse branches `g_D(y)=(2^{D+1}y+3^D−2^D)/3^{D+1}`,
  verified: forward itinerary matches the prescribed one 900/900 and 1800/1800). Prescribing a **fully
  supported, aperiodic** itinerary (biased-geometric, mean ≈3, all `D≥0` present) builds an orbit that is
  **dense in ℤ₂** (178/256 cylinders mod 2^8, `D`-distribution covers `0..7+`), i.e. **maximally
  non-shadowing** — yet `avg jump = 3.098 > 2`, **violating the bound**. So the bound is NOT implied by
  non-shadowing / spreading; it forces the empirical measure to be **Haar specifically**, not merely
  "spread out." (Generic for a non-Haar Bernoulli measure `ν`, the orbit equidistributes w.r.t. `ν` and
  `avg jump = E_ν[v2(3x−1)]`, freely `>2`.)
- **(ii) NOT strictly weaker.** Decomposing `avg jump = (1/J)Σ_k N_k` by scale (verified, `J=20000`): it is
  **dominated by small `k`** — `k≤3` contributes `0.879` of the total `1.004`, with `N_k/J ≈ 2^{−k}`. The
  small-`k` terms ARE fixed-`k` cylinder counts = **fixed-`k` equidistribution** (empirical measure → Haar at
  the low cylinders), in the **same open class as the original even-density problem**. The genuinely weaker
  large-`k` part (separation / anti-clustering of orbit differences, plausibly Baker-accessible) is
  **negligible** for avg jump. So the binding residual input ≈ Haar-equidistribution; the transfer-operator
  framework does **not lower the bar** at the binding scale.
- **Net (the value, honest).** Route C is now fully mapped: it **relocates and re-derives** the wall but does
  **not weaken** it. The reviewer's "single-orbit extraction from a Gibbs–Markov system" IS the real core, and
  it equals **empirical-measure-→-Haar of the specific orbit**, whose binding difficulty lives at **small /
  fixed `k` (the low cylinders / moving 2-adic diagonal)** — re-confirming the §5 obstruction map from the
  dynamical side. The framework cleanly **separates** a binding equidistribution core (small `k`) from a
  non-binding Diophantine tail (large `k`); only the latter is plausibly accessible, and it is not what binds.
- **Discipline.** Negative/limitative result, stated as such; no claim Antihydra is proved. This is the
  programme's "specify the wall" phase delivering a sharp, decisive boundary. 0 false proofs maintained
  (the construction was the guard: had non-shadowing sufficed, no such orbit would exist — it does).

---

## 2026-06-25b — Direct attack on (α): two exact identities + growth-argument is circular (the wall, fully mapped)
Attacked (α) = "force the single seed-8 orbit's empirical measure to Haar" head-on. Did NOT breach it (it is
genuinely Mahler-class) but mapped it completely from the dynamical side, with verified content
(`alpha_attack.py`):
- **[EXACT, verified diff 0 over 2·10^5 steps] `Σ_{j<J} v2(3c'_j−1) = #odd steps`** ⇒ **`avg jump = #odd/#even`
  exactly**, `even-density = 1/(1+avg jump)`. The transfer-operator/renewal reformulation **collapses to
  even-density ≥ 1/3 as an exact identity** (not merely "same class") — no-free-lunch made exact. Confirms the
  Q9(b) sufficiency finding at the sharpest level: nothing we built is weaker than the original criterion.
- **[EXACT telescoping, verified] `2c'_{j+1}−1 = (3/2)^{D_j}(3c'_j−1)`** ⇒ `log b_J = log(3/2)(J+Σ D_j)+ε`,
  `ε→0.1164` bounded (`b_j=2c'_j−1 ~ (9/4)^j`). Independently `log b_J ≈ log(2c'_J)`, `c'_J ~ c(3/2)^n`,
  `n=#even+#odd=J+Σ D_j` — the SAME identity ⇒ the growth relation is a **TAUTOLOGY**: `Σ D_j` cancels, giving
  no inequality. **⇒ counting/growth-rate arguments are intrinsically CIRCULAR for (α)** — new verified entry
  in the obstruction map; the one elementary-looking route is closed.
- **Single-orbit-equidistribution mechanisms all unavailable:** (i) unique ergodicity FAILS (F full-branch
  expanding, continuum of invariant measures — the §6.5/Q9b non-Haar-generic orbits); (ii) rank-≥2 rigidity
  FAILS (rank 1); (iii) character cancellation FAILS (van der Corput closed on (3/2)^n).
- **Net / honest.** (α) IS the open kernel (= even-density ≥ 1/3) exactly; the elementary attack is provably
  circular; the soft ergodic mechanisms are structurally unavailable. Residue = a single sharply-specified
  missing tool: **rank-1 effective equidistribution with a Diophantine input on log2 3** (§7 α). Wrote §7.5 in
  STATE_FOR_REVIEW. This closes the "attack the wall directly" line: the wall is mapped on every side; breaching
  it is genuinely new mathematics (multi-year), not a missed trick. 0 false proofs; no claim (α) is proved.
- **Assessment for the programme.** The Q8→Q9→(i)/(ii)→(α) sequence has converged: the BB(6)/Antihydra kernel
  is now a *fully-specified* open problem (exact criterion, exact reformulations, complete obstruction map on
  both the arithmetic and dynamical sides, one named missing tool). This is the natural endpoint of the
  "specify the wall" phase. Further progress requires either (a) external expert input (the note is ready) or
  (b) a multi-year investment in the rank-1 effective-equidistribution mechanism.

---

## 2026-06-25c — Route C (cross-cryptid): the Mahler cryptids share ONE kernel + ONE obstruction map (verified)
Ran the non-circular self-attack from STRATEGY_BRIEF (C): does the Antihydra Q9-trilogy dissection PORT to the
other BB(6) Mahler cryptids? **Yes, verified** (`cross_cryptid.py`, exact p-adic arithmetic; writeup
`CRYPTID_KERNEL.md`):
- For `μ=2^a/3^b` with denominator prime `p` (`v_p(μ)=−1`), `T_μ(x)=⌊μx⌋` is a **`p`-to-1 exact endomorphism of
  ℤ_p**; renewal density `→1/p`, avg gap `→p`, **exact identity `Σ(gap−1)=#non-renewal`**; induced map =
  **full-branch piecewise-affine expanding Gibbs–Markov on ℤ_p** (slopes `μ^g`) with a **ℤ_p fixed point on
  every branch** (Q9(b) obstruction). Verified for `3/2`(p=2, Antihydra/o10-inner), `8/3`(p=3, o18/o15),
  control `9/2`(p=2) — all `8/8` branches affine+fixed.
- Only difference: branch alphabet. `p=2` → gap-indexed (intermediate residue forced); `p=3` → itinerary-word
  indexed (residues `{1,2}`), finer but still full-branch (o18: word `()`→fix 0, `(1)`→2/55, `(2)`→1/55, …,
  all ℤ_3; 2463 word-branches seen).
- **Consequences.** (1) ONE kernel: every Mahler cryptid's non-halting is governed by single-orbit
  equidistribution of `⌊μ^n⌋ mod p` (the moving p-adic diagonal). (2) ONE obstruction map: the Q9-trilogy walls
  are structural properties of `T_μ` on ℤ_p, hence machine-independent (§7.5 is not Antihydra-specific).
  (3) ONE missing tool — rank-1 effective equidistribution of `⌊μ^n⌋ mod p` w/ Diophantine input on `log_q p`
  — resolves the whole sub-family at once, so `EXPERT_ASK.md` Q1 is a question about a family.
- **Scope/honesty.** Mahler-`2^a/3^b` sub-family = 4 of 5 core cryptids (Antihydra, o10-inner, o18, o15); o17 is
  an odometer outlier (NOT claimed isomorphic); slow-width 15 separate. **Decides no machine** — the halt
  predicate differs per machine (Antihydra even-density / o18 frontier-bit / o15 block-collision); what is
  isomorphic is the equidistribution kernel + obstruction (why hard / what one tool cracks them), not a decision
  procedure. `v_p(μ)=−1` is the clean regime (`9/4` v_2=−2 is not single-floor p-to-1, verified).
- **Why it matters (deliverable D).** Converts "Antihydra is Mahler-hard" into a **classification**: the Collatz
  core of BB(6) is, up to the per-machine halt predicate, ONE number-theoretic kernel with ONE obstruction map
  and ONE missing tool. The cryptid vertex (no tame certificate) is a single shared object across the family,
  not four coincidentally-hard machines — recordable structural contribution, independent of resolving any
  cryptid. 0 false proofs; no non-halting claimed.

---

## 2026-06-25d — A (literature triage) + C-extension (classification, o15/o17) + D (hierarchy integration)
Ran all three remaining lines in parallel.
**A — literature triage (background research agent):** our kernel = the single-orbit case of **Mahler's 3/2
problem (1968)**, confirmed open. Findings (cited): (Q1) Flatto–Lagarias–Pollington 1995 gives only a *range*
bound (orbit can't lie in an interval `< 1/p`), not density; Koksma 1935 a.e.; arXiv:2510.11723 (2025) poses
single-orbit normality as an open *conjecture*. (Q2) ALL Gibbs–Markov / transfer-operator / shrinking-target /
dynamical-Borel–Cantelli results are **μ-a.e. by construction** — independently confirms our orbit-blindness
finding (i); no per-orbit-under-arithmetic-hypothesis theorem exists. (Q3) **Tao 2019/2022 (Forum Math Pi,
arXiv:1909.03562) is the closest technique and uses the SAME p-adic skew-random-walk / renewal / Gibbs–Markov
structure we reconstructed** — but log-density-1 a.e., not single-orbit; exact gap = remove the density average.
(Q4) community reduction matches ours (bbchallenge arXiv:2509.12337, 2025); no partial/conditional non-halting
result exists. CAUTION logged: arXiv:2411.03468 (2024) claims to resolve Mahler 3/2 — unverified, likely flawed,
NOT relied on. → folded into STATE_FOR_REVIEW (§4 Tao row + §6 Literature anchoring), CRYPTID_KERNEL, LIMIT_THEOREM.
**C-extension — classification + o15/o17:** verified `T_μ` is a clean `p`-to-1 exact endomorphism of `ℤ_p`
**iff `v_p(μ)=−1`** (grid: clean 3/2,8/3,9/2,2/3,4/3,16/3,27/2,5/2; not-clean 9/4,16/9,27/4,8/9). So the kernel
family = `{μ=2^a/3^b : v_p(μ)=−1}`, exact. Placement: **o15 ∈ 8/3 kernel class** (width follows ×8/3, ratios
`107,289,772 → 8/3`; the parity-irregularity is in the halt predicate, not the kernel); **o17 = outlier**, a
uniquely-ergodic **odometer** (isometry of ℤ_p, equidistribution automatic) whose hardness is its
Collatz-irregular halt predicate — so the Collatz core has TWO obstruction types (equidistribution-kernel vs
odometer-halt-predicate). → CRYPTID_KERNEL classification + placement sections.
**D — hierarchy integration:** added LIMIT_THEOREM §3′: the `[OPEN]` cryptid top is ONE shared vertex indexed by
`(a,b,p)` (not four machines), literature-anchored to Mahler 3/2 / Tao / the 2025 normality conjecture. The
genuineness-limit avatar is now a *named* open problem; one tool lifts the whole vertex.
**Net:** the external triage independently validated the obstruction map (orbit-blindness = the a.e. nature of
all known machinery) and revealed we had reconstructed Tao's state-of-the-art structure ourselves. 0 false proofs.
