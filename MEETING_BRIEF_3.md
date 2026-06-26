# Meeting brief — round 3 (2026-06-26): the new theory, and how to proceed
*For a strategy session (incl. ChatGPT). Since round 2 we built the new-theory blueprint, reduced the complete
proof to one sharply-posed conjecture, proved a quantitative δ→margin reduction, and confirmed the whole picture
against the literature. This brief is the current state + the decision: **how to proceed**. All claims
machine-checked or literature-anchored; 0 false proofs (~18 over-claims caught & retracted, incl. this session a
shuffle-killed "91%-predictability" artifact and a forced-odd σ² factor-2 bug).*

## 1. One-line state
**Antihydra non-halt ⟺ a single specified rank-1 expanding orbit equidistributes ⟺ (proven reduction) a
power-saving character-sum cancellation at low 2-power moduli ⟺ derandomizing a transfer-operator spectral gap to
one explicit Diophantine orbit.** The last is *recognized open* (= Mahler 3/2 / the 2025 single-orbit normality
conjecture); the reduction chain down to it is new and ours.

## 2. What we PROVED this session (durable, conjecture-independent — real even if Antihydra stays open)
- **Theorem E (δ→margin map).** `avgD_odd = 2 − Σ_k δ_k` with `δ_2 = ½·avgχ_{−4,odd}` exact; if there is *any*
  power saving `δ>0` in `|Σ_{odd}ψ(c_n)| ≤ C N^{1−δ}` for nontrivial `ψ` of conductor `≤ N^δ` (LOW moduli only),
  then `avgD_odd ≥ 2 − O(N^{−δ}\log N) ≥ 3/2` ⇒ **non-halt**. Turns "prove normality" into "get any low-moduli
  power saving."
- **Valuation budget (3rd exact identity).** `Σ_{odd i<n} v2(3c_i−1) = n + v2(c_n) − v2(c_0)` ⇒ criterion
  `avgD_odd ≥ 3/2`; unconditional **range** `n ≤ Σ ≤ 1.585n` — a 2-adic Flatto–Lagarias–Pollington, **independently
  matched by FLP (1995)** in the literature.
- **Lowest-modulus in elementary form.** `S_2 = Σχ_{−4}(c_n) = #odd − 2·#(odd-runs)` (exact) ⇒ conductor-4 case
  `⟺ avgL → 2` (average odd-run length).
- **Renormalization self-similarity.** The run-start return map is again full-branch Gibbs–Markov, slope
  `(3/2)^{L+M}` — conductor-4 H *reproduces itself* on the cross-section: a fixed point **with no contraction** (the
  structural reason every internal route funnels).
- **Three-technology closure.** Measure/spectral (rank-1, needs infinitary), Baker (unbounded height `T_n≈n·log₂3`),
  character-sum/bilinear (multiplicatively structureless) — each blocked by a *distinct* structural reason.
- **Certificate hierarchy [PROVEN].** Five strict Chomsky separations (`star-free⊊REG⊊SLIN⊊2-automatic⊊CF⊊CS`) with
  explicit verified TM witnesses + the cryptid-orthogonality (over-approximation axis) reframing.

## 3. The central conjecture + literature status (the frontier)
The complete proof = **derandomize the spectral gap to one orbit** = supply the Weyl/Gowers cancellation that
Theorem E needs. A 3-agent literature survey (`DERANDOMIZATION_LITERATURE.md`) found **no known principle reaches
it**, and confirmed the blueprint:
- "gap ⇒ every/specified orbit" precedents all need structure we lack — **QUE** (Hecke), **rigidity** (a 2nd
  mult.-indep. map; the entropy-coupling identity is the cleanest proof rank-1 is excluded), **effective Ratner**
  (unipotent). Pseudorandomness routes fail precisely — **Sarnak** needs *zero* entropy (ours is positive),
  **ML-random** needs non-computability (ours is computable), **PRG** is class-relative/computational.
- The **one correct framing is Weyl/Gowers — a reduction to a cancellation bound = exactly our Theorem E.**
- Closest known: **FLP 1995** (range only, single seed) and **Tao 2019** (log-density-1, never one seed; same
  3-adic skew-walk statistic). Single-orbit normality is an **explicit open conjecture** (arXiv:2510.11723, 2025).

## 4. The decision — how to proceed (the meeting's job)
The complete proof is the recognized open Mahler frontier; we have a clean reduction chain and several proven,
conjecture-independent assets. Genuine options (not mutually exclusive):
1. **Deepen the proven assets toward a *partial unconditional* theorem.** Most promising lever: push the proven
   top-foothold (Θ(log N) bits) or attack the elementary `avgL → 2` / `S_2 = #odd − 2#runs` form for *any*
   unconditional sub-trivial bound (even one extra scale). A genuine partial on the single specified orbit would be
   a first-of-its-kind result.
2. **Engage the community that shares the exact reduction.** bbchallenge (Antihydra is theirs) + Mahler/Tao-adjacent
   analytic-NT researchers. Offer Theorem E, the 2-adic FLP range, the `avgL→2` form — they may have partials, and
   our `δ→margin` map is a sharply-posed target they could attack.
3. **Commit to the multi-year tool** — the derandomization / Weyl–Gowers cancellation for the specified orbit. The
   real prize (resolves Antihydra + the cryptid family + Mahler 3/2 at once); generational; needs the new math the
   literature says does not yet exist.
4. **Port the framework** to where it yields a *complete* result now — the certificate hierarchy (already 5 proven
   rungs) or a decidable sibling — accruing finished theorems while the frontier stays open.

**Questions for the meeting.**
- (a) Is **Theorem E** (any low-moduli power saving ⇒ the margin ⇒ non-halt) a correct and genuinely *new*
  reduction — or does it secretly assume the full equidistribution? (We believe it is a real weakening of the
  *needed input*; sanity-check wanted.)
- (b) Is there a realistic route to **any unconditional partial** on the single orbit (option 1) — e.g. via the
  `avgL → 2` run-length form, or an effective-`log₂3` push of the top foothold — short of the full conjecture?
- (c) For a multi-year commitment (option 3), is **Weyl/Gowers cancellation along a single `⌊μ·⌋`-orbit** the right
  attack surface, and who/what is the nearest active research line (post-Tao-2019)?
- (d) Given the "record-only, don't publish" stance: is the right move to **write the framework up as a durable
  note** (Theorem E + the hierarchy + the derandomization map) and **share the reduction with the community**,
  rather than chase the frontier solo?

*(Companion: `THEORY.md` (the blueprint + Theorem E), `DERANDOMIZATION_LITERATURE.md` (the survey),
`EXPERT_ASK.md`/`EXPERT_ASK_HOMOGENEOUS.md` (send-ready), `RETROSPECTIVE.md`, `LIMIT_THEOREM.md` (the hierarchy).)*
