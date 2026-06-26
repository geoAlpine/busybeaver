# Theorem E pivot, resolved (self-checked 2026-06-26): a valuable reframing, NOT an easier target
*Resolving the core question of `THEOREM_E_VERIFICATION.md` directly, rather than only awaiting an external expert.
Verdict: the reviewer's concern is correct. Theorem E is a **clean, valuable reframing** of non-halt into
character-sum / analytic-NT language, but its hypothesis is **the same difficulty class as the wall** — it requires
conductor-4 (mod-4) equidistribution of the specified orbit. This **corrects an earlier over-optimistic framing**
(that Theorem E "turns prove-normality into get-any-low-moduli-power-saving" — true as a *target shape*, misleading
as a *difficulty claim*). 0 false proofs; discipline = catching one's own over-claim.*

## The question
Is Theorem E's hypothesis — power-saving character cancellation `|Σψ(c_n)| ≤ C N^{1−δ}` for nontrivial `ψ` of
conductor `≤ N^δ` — genuinely *weaker/easier* than full single-orbit equidistribution, or the same difficulty?

## The resolution (rigorous, self-checked)
1. **Character → discrepancy.** `H(δ)` bounds `disc(mod 2^k) ≤ 2C·2^k·N^{−δ}`. For *fixed* `k` this `→ 0`
   (so `H(δ) ⟹` mod-`2^k` equidistribution at every fixed scale); at the *top* scale `2^k ~ N^δ` the bound is
   `O(1)` (trivial). So `H(δ)` is **growing-window equidistribution** up to scale `N^{δ−ε}` — exactly the reviewer's
   reading.
2. **The margin genuinely needs conductor-4 control.** Theorem E's condition is `Σ_{δ_k>0} δ_k ≤ 1/2`. The
   geometric bound alone gives `Σ_{k≥2} 2^{−(k−1)} = 1` — only `≤ 1`, **not** `≤ 1/2`. To push the sum below `1/2`
   one **must beat geometric at `k=2,3`** via character cancellation = **mod-4, mod-8 equidistribution of the
   specified orbit**. That is the open wall (`conductor-4 ⟺ avgL→2 ⟺ moving-middle-digit ⟺ Mahler core`).
3. **Logical direction.** `non-halt = (Σ_k δ_k ≤ 1/2)` (signed). Theorem E uses `Σ_{δ_k>0} δ_k ≤ 1/2` (positive
   part) `≥ Σ_k δ_k`, so the Theorem-E condition **implies** non-halt and is **stronger** (a sufficient condition).
   It is not a relaxation of non-halt; it is a *sufficient* condition phrased in character-sum language.

## Verdict
> **Theorem E is a correct, valuable *reframing/localization* — not a difficulty reduction.** It restates non-halt
> as a one-sided, low-moduli, character-sum cancellation along the `⌊μ·⌋`-orbit (analytic-NT language, any power
> saving `δ>0` suffices). That target *shape* is cleaner and connects to a large body of technique (large sieve,
> Weyl, Gowers, Vinogradov). But its **difficulty is the same as the wall**: it requires conductor-4 (mod-4)
> equidistribution of the specified orbit, which is open even at its mildest point. *(Exactly the expert's "safe
> positioning": weaker/cleaner target, equi-difficult — the one-sided-recurrence-vs-equidistribution situation.)*

## What this changes (honest)
- **Corrects** the earlier framing in `THEORY.md`/`ROADMAP` that Theorem E makes the target *easier*. It does not.
  Its value is the **reframing** (non-halt as a character sum) and the **δ→margin map** (any power saving suffices,
  so the optimal exponent is not needed) — both genuine, neither an easier difficulty.
- **Resolves the fork.** The path is **Mahler-hard**: there is no Theorem-E shortcut below the conductor-4 wall.
  An external expert can still add value by pointing to the **nearest analytic-NT technique** for low-conductor
  character cancellation along a deterministic `⌊μ·⌋`-orbit (post-Tao-2019) — that is now the precise ask, not
  "is it weaker?".
- **The realistic path forward** is therefore: (A) the multi-year Weyl/Gowers cancellation tool; the unconditional
  **partials** we proved independent of the wall (`#even ≥ c·log n`, foothold `≈ 0.85·log₂N`); and a durable
  write-up of the reduction-chain reframing (its real, lasting contribution).

## Why Theorem E still matters
The reduction is *not* wasted: non-halt is now a **specified-orbit character-sum cancellation**, a classical object
with a precise statement and a number (`any δ>0`) and scale range (low moduli). That is the right language to hand
an analytic number theorist — it just is not an *easier* problem than the wall, and we should present it as a
reframing, not a shortcut. (Soundness note: this self-correction is logged per the program's discipline — an
over-claim caught and retracted before it propagated to any external ask.)
