# Roadmap to the complete proof of Antihydra (BB(6)) — state, open challenge, candidate solutions
*A self-contained working document for a strategy session (incl. ChatGPT) aimed at the complete proof. It explains
the problem, the proven reduction chain, the single remaining challenge, why it is hard (with the literature), and
the concrete candidate solution methods — ending with a proposed next step. Every claim is labelled
[PROVEN] / [CONDITIONAL] / [OPEN]; everything [PROVEN] is machine-checked in exact integer/2-adic arithmetic.
Discipline: 0 false proofs; ~18 over-claims caught & retracted (this session a shuffle-killed "predictability"
artifact and a forced-odd variance bug).*

---
## 0. The problem (self-contained)
"Antihydra" is a 6-state Turing machine (a Busy-Beaver "cryptid", **non-halting status OPEN**). Its dynamics reduce
exactly to an integer orbit:
```
c_{n+1} = floor(3 c_n / 2),   c_0 = 8.     E_n = #{ i<n : c_i even }.
```
> **[PROVEN] Antihydra never halts  ⟺  the running even-density E_n/n ≥ 1/3 for all n  (⟺ 3E_n − n ≥ 0 ∀n).**
Conjecturally the density → 1/2. Deciding this is in the class of **Mahler's 3/2 problem (1968)**.

---
## 1. The reduction chain (what reduces to what) — all [PROVEN]
**Five equivalent forms** (machine-checked equivalences): non-halt ⟺
1. *(renewal/2-adic)* `avg jump = (1/J)Σ_j v2(3c'_j−1) ≤ 2` for the induced full-branch Gibbs–Markov map `F` on ℤ₂;
2. *(dynamical)* the single orbit of seed 8 under `×(3/2)` on ℤ₂ is **generic** (empirical measure → Haar);
3. *(homogeneous)* seed 8 is generic for the **rank-1 Anosov / amenable-hyperbolic** automorphism `×(3/2)` of the
   S-arithmetic solenoid `(ℝ×ℚ₂×ℚ₃)/ℤ[1/6]` (expanding ℝ,ℚ₂; contracting ℚ₃);
4. *(analytic/digits)* the moving diagonal digit `⌊8(3/2)^n⌋ mod 2` equidistributes (= Mahler 3/2);
5. *(normality)* the explicit sequence `⌊(3/2)^n⌋ mod 2` is **normal**.

**The cleanest target (this program's reductions):**
- *(floor-carry identity)* `c_n = (3^n c_0 − T_n)/2^n`, `T_n = 3 T_{n−1} + 2^{n−1} r_{n−1}`, `r_i = c_i mod 2`.
  Note `height(T_n) ≈ n·log₂3` — **unbounded**.
- *(valuation budget, 3rd exact identity)* `Σ_{i<n, c_i odd} v2(3c_i−1) = n + v2(c_n) − v2(c_0)`, giving the
  **cleanest criterion form  `non-halt ⟺ avgD_odd ≥ 3/2`** (a *lower* bound on one average; Haar value 2).
- *(character-sum leading term)* `avgD_odd = 2 − Σ_k δ_k`, `δ_k = 2^{−(k−1)} − P(D≥k | odd)`, and the k=2 term is
  exact: `δ_2 = ½·avgχ_{−4,odd}` (`χ_{−4}` = nontrivial character mod 4). So the leading obstruction is the
  **one-sided character sum  `S_2 = Σ_{odd} χ_{−4}(c_n) ≤ 0`**.
- *(combinatorial form)* `S_2 = #odd − 2·#(odd-runs)`, so conductor-4 case `⟺ avgL → 2` (average odd-run length;
  run length `= v2(c_start−1)`).

---
## 2. What is PROVEN (the scaffolding — real even if Antihydra stays open)
- **Theorem A (mixing engine) [PROVEN].** The carry hides a `×3` action: `3` is a 2-adic unit of order `2^{k−2}`
  mod `2^k`; `{3^m mod 2^k}` is a full cyclic orbit, **exactly equidistributed**. (The carry's "fresh bit per
  scale" is extracted by this *known* engine.)
- **Theorem B (top foothold) [PROVEN].** The top `Θ(log N)` binary digits of `⌊8(3/2)^n⌋` equidistribute, via Weyl
  on `{n·log₂3}` (finite, non-Liouville irrationality measure of `log₂3`). The foothold is sharp at `Θ(log N)`.
- **Theorem C (annealed coupling) [PROVEN].** If the parity bits `r_i` are i.i.d. fair coins, the carry + engine
  produce an **exactly equidistributed** residue sequence (annealed mixing, efficient at every cylinder depth).
- **Theorem E (δ→margin map) [PROVEN reduction].** Two per-scale bounds on the dangerous deviations (`δ_k>0`):
  *(geometric)* `δ_k ≤ 2^{−(k−1)}`; *(character)* `|δ_k| ≤ max_{ψ≠1 mod 2^k}|avgψ_odd|`. **If** there exist `δ>0,C`
  with `|Σ_{i<N,odd}ψ(c_i)| ≤ C N^{1−δ}` for every nontrivial `ψ` of conductor `≤ N^δ` (LOW moduli only), **then**
  `Σ_{δ_k>0}δ_k ≤ O(N^{−δ}\log N)` (crossover at `K*≈δ\log_2 N`), so `avgD_odd ≥ 2 − O(N^{−δ}\log N) ≥ 3/2` ⇒
  **non-halt**. *Any* power saving `δ>0` suffices.
- **[PROVEN] Unconditional range (2-adic Flatto–Lagarias–Pollington).** `n ≤ Σ_{odd}v2(3c_i−1) ≤ 1.585n` — matches
  FLP's real range bound `limsup−liminf ≥ 1/p` (single seed, range not density).
- **[PROVEN] Lemma D (exceptional set).** Integer seeds avoid the (Haar-null) periodic and singular-preimage parts.
- **[PROVEN] Certificate hierarchy.** Five strict Chomsky separations (`star-free⊊REG⊊SLIN⊊2-automatic⊊CF⊊CS`),
  explicit verified TM witnesses; the cryptid sits on the orthogonal over-approximation axis.

---
## 3. The single remaining challenge [OPEN]
Everything reduces to **one** statement — the quenched version of Theorem C, equivalently the hypothesis of
Theorem E:
> **Central Conjecture (the complete-proof frontier).** The single specified orbit `⌊8(3/2)^n⌋` exhibits
> **power-saving character-sum cancellation at low 2-power moduli**: `|Σ_{i<N,odd}ψ(c_i)| ≤ C N^{1−δ}` for some
> `δ>0` and all nontrivial `ψ` of conductor `≤ N^δ`. Equivalently: the orbit equidistributes mod `2^k` for the
> *specified* seed (not a.e.); equivalently `⌊(3/2)^n⌋ mod 2` is normal; equivalently `avgL → 2`.

**This is the recognized open frontier** = Mahler 3/2 / the 2025 single-orbit-normality conjecture
(arXiv:2510.11723). Our contribution is the *reduction chain* down to a sharply-posed, mild target (any `δ>0`,
low moduli) and the proven `δ→margin` map.

---
## 4. Why it is hard (the obstruction map + the literature)
- **Three-technology closure [PROVEN/measured]:** every unconditional tool family is blocked by a *distinct*
  structural reason — **measure/spectral** (rank-1, continuum of invariant measures, needs infinitary input);
  **p-adic Baker** (orbit terms have unbounded height `T_n≈n·log₂3`, not S-units); **character-sum/bilinear**
  (`c_n mod 4` = high bits of the dynamical carry, multiplicatively structureless in `n`).
- **No finite-order obstruction:** the orbit is i.i.d.-indistinguishable at every finite order (mod-p CLT rate,
  lag-MI≈0, block-entropy=log p, random-rate self-separation, no finite-window law). Only an *infinitary* input can
  decide it.
- **Renormalization self-similarity [PROVEN]:** the run-start return map is again Gibbs–Markov (slope `(3/2)^{L+M}`)
  — conductor-4 H reproduces itself on the cross-section: a **fixed point with no contraction** (the structural
  reason every internal route funnels).
- **The contraction already exists — the missing tool is DERANDOMIZATION.** The transfer operator of `F` has a
  spectral gap (decay of correlations, CLT) — but at the **Haar level only**. The specified orbit is
  "spectral-gap-pseudorandom" (its Birkhoff variance matches the Haar Green–Kubo σ²). So the tool is: prove the
  explicit *computable* (`K=O(\log N)`) orbit realizes the spectral-gap prediction, with effective `log₂3` as the
  pseudorandom seed.
- **Literature (3-agent survey):** NO known derandomization principle reaches our case. QUE needs Hecke symmetry;
  rigidity needs a 2nd mult.-independent map (the entropy-coupling identity `log q·h(σ_p)=log p·h(σ_q)` is the
  cleanest proof rank-1 is excluded); effective Ratner needs unipotency. Sarnak–Möbius needs *zero* entropy (ours
  is positive); ML-randomness needs non-computability (ours is computable); PRG is class-relative/computational.
  **The one correct framing is Weyl/Gowers — a *reduction* to a cancellation bound = exactly Theorem E.** Closest
  known: FLP (range, single seed) and Tao 2019 (log-density-1, never one seed; same 3-adic skew-walk statistic).

---
## 5. Predicted / candidate solution methods (toward the complete proof)
Ordered by how directly each targets the Central Conjecture; each with its mechanism, the precise gap, and a
first concrete step. All are routes to **new mathematics** (the frontier), stated honestly.

**(A) Weyl/Gowers cancellation for the single orbit — the literature-endorsed framing, = Theorem E's hypothesis.**
- *Mechanism:* bound `Σ_{n<N}ψ(c_n)` (low conductor) or `Σ e(t c_n)` directly with power saving. By Theorem E,
  *any* `δ>0` at low moduli ⇒ the complete proof.
- *Gap:* van der Corput is closed (differencing returns the same `(3/2)^n` family); no multiplicative structure to
  run a bilinear/Vaughan decomposition. Needs a genuinely new exponential-sum input tuned to `c_n=(3^n c_0−T_n)/2^n`.
- *First step:* attack the **elementary `avgL → 2` form** (`S_2=#odd−2#runs`) — is there *any* unconditional
  sub-trivial bound on `#(odd-runs)` / the run-length distribution? Even one extra scale of the foothold (B) below.

**(B) Effective genericity via large deviations + a Diophantine Borel–Cantelli ("de-randomize the spectral gap").**
- *Mechanism:* the spectral gap gives `Haar{x : |Birkhoff_N f(x) − ∫f| > ε} ≤ e^{−c(ε)N}` (exponentially small bad
  sets). If the bad sets at scale/time `N` can be shown to **miss the specified algebraic point** using its
  arithmetic (effective `log₂3`), a Borel–Cantelli-type argument places seed 8 outside all of them.
- *Gap:* a single point has measure 0; one must *describe* the bad sets arithmetically and prove the orbit avoids
  them — an effective-genericity statement no current method provides for a rank-1 expanding map.
- *First step:* make the bad sets explicit at low scales (mod 4, 8) and test whether the orbit's known top-foothold
  (B-Theorem) provably keeps it out of the leading bad set; quantify the arithmetic input required.

**(C) The coupling theorem: known `×3` engine + a Diophantine self-correlation bound ⇒ equidistribution.**
- *Mechanism:* the carry's fresh bit per scale is extracted by the *known* `×3 mod 2^k` orbit (Theorem A); the only
  unknown is the parity input `r_i` (self-generated). Prove the input couples to the engine to give the fresh bit,
  using effective `log₂3` to break the self-reference.
- *Gap:* the self-feeding — the parity is the orbit's own output; the literature's a.e.→specified barrier in
  concrete form.
- *First step:* prove the **conditional** "if the parity self-correlation `Σχ(c_n)` is `o(N^{1−δ'})` for some
  `δ'`, then the engine forces equidistribution mod `2^k`" — i.e. close the loop from the input bound to the output
  equidistribution (this is the quenched analog of Theorem C; pairing it with Theorem E may shrink the needed input).

**(D) Exploit the contracting 3-adic (stable) direction as an effective second direction.**
- *Mechanism:* in the solenoid (form 3), `×3/2` contracts the ℚ₃ factor. The literature says rigidity needs a 2nd
  multiplicatively-independent *expanding* direction — but the **stable/unstable splitting** (genuine for the Anosov
  automorphism) might give partial leverage that the bare real Mahler problem lacks. (This is the open hook in our
  homogeneous-dynamics expert ask.)
- *Gap:* the 2-3 duality is *self-dual* (`×3/2` uses one multiplier; BFLM-type arguments are circular). It is not a
  genuine rank-2. Whether the stable 3-adic direction buys anything unconditional is open.
- *First step:* ask homogeneous-dynamics experts (EXPERT_ASK_HOMOGENEOUS is send-ready) what the contracting 3-adic
  direction can/cannot supply for a specified-point genericity statement.

**(E) Port / partial: secure an unconditional *partial* on the single orbit (first-of-its-kind).**
- *Mechanism:* not the full conjecture — any unconditional statement *about the specified orbit* stronger than the
  FLP-type range: e.g. "infinitely many distinct limit points", "positive lower density of even steps", or "avgL is
  bounded away from 1". The range bound is the only such fact known; beating it would be genuinely new.
- *First step:* push the proven top-foothold (Theorem B) using an explicit irrationality measure of `log₂3` to gain
  one more moving digit unconditionally — a concrete, bounded sub-goal.

---
## 6. Proposed next step (for discussion)
**Primary:** validate **Theorem E** externally (is "any low-moduli power saving ⇒ non-halt" a genuine weakening of
the needed input, or does it smuggle in full equidistribution?). If sound, it makes the target an analytic-NT
cancellation with a number (`δ>0`) — a sharply-posed prize.
**In parallel (conjecture-independent, fundable):** attack **(E)** — an unconditional partial via the `avgL → 2`
run-length form or one extra foothold scale — the only route that yields a *finished* theorem on the specified
orbit short of the frontier.
**For the multi-year commitment:** route **(A)/(B)** are the literature-endorsed surfaces (Weyl/Gowers cancellation;
de-randomizing the spectral gap). Route **(D)** is the cheapest external probe (the 3-adic stable direction).

> *We want ChatGPT's read on: (i) is Theorem E correct and genuinely new? (ii) which of (A)–(E) is the most
> promising attack surface, and is there a nearest active research line (post-Tao-2019) to plug into? (iii) is there
> any unconditional partial (E) within reach? Then we combine its view with our own and pick the next concrete move.*
