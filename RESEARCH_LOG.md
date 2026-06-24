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
