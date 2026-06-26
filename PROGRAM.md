# Research program — Rank-1 specified-orbit genericity (2026-06-26)
*The banner change agreed in the round-2 meeting. The work has generalized past its origin: the object that grew
largest is not Antihydra but **the genericity of a specified algebraic point under a rank-1 amenable-hyperbolic
action**. We therefore invert the hierarchy — that genericity theory is the program; Antihydra is its first
instance. This reframing is honest (the durable assets are already general — see below) and strictly stronger as a
program: it accrues whether or not any single instance is decided. 0 false proofs; this file claims no new theorem,
it re-labels the existing, verified body of work.*

## The banner
> **Effective single-orbit genericity for rank-1 amenable-hyperbolic automorphisms at specified algebraic points.**
> *Given a rank-1 Anosov / amenable-hyperbolic automorphism `A` of a (toral / S-arithmetic solenoidal) compact
> abelian group and a **named** algebraic point `x₀`, when does the single forward orbit `{Aⁿx₀}` equidistribute
> toward Haar? Measure rigidity (rank ≥ 2) and unique ergodicity both fail here; this is the empty cell.*

The complete proof of any one instance **= a theorem in this program**: provable normality of an explicit
`⌊(p/q)ⁿ⌋`-type sequence from its generating dynamics alone, with no designed certificate.

## Why the inversion is the honest description (not a relabel of convenience)
Every durable asset we built is already **instance-independent** — they are statements about the *class*, which is
the tell that the class, not the instance, is the real object:
| asset | scope | already general? |
|---|---|---|
| Cross-cryptid classification `[theorem]` | the **whole** `v_p(μ)=−1` Mahler family shares one kernel + obstruction | **yes — class-level** |
| Engine survey `[complete]` | all 7 single-orbit engines fail for `A` for **one** structural reason | **yes — about `A`, any seed** |
| Wall = `amenable ∩ hyperbolic` | a property of the **action**, not the seed | **yes — action-level** |
| Three-route normality block | any explicit `⌊(p/q)ⁿ⌋` is computable ∩ structureless ∩ non-uniquely-ergodic | **yes — class-level** |
| Lemma 1 (repelling periodics), Lemma 2 (null singular set) | hold for every integer seed of `A` | **yes — all seeds** |
Antihydra-specific facts (`c₀=8`, the even-density ⟺ non-halt reduction) are a **thin instance layer** on top of a
**thick class-level theory.** The meeting's reading is correct: the instance is the small part.

## The instances (the program's test cases, in order of how much they are already pinned)
1. **Antihydra** — `A = ×(3/2)`, seed `8`, prime 2. The motivating BB(6) holdout; fully reduced; the running example.
2. **The `v_p(μ)=−1` Mahler family** — every `μ = a/p` with `v_p(μ)=−1` (the cross-cryptid theorem's domain):
   each is a `Tμ` clean `p`-to-1 exact endomorphism sharing the **same kernel and the same obstruction**. Antihydra
   is `p=2,μ=3/2`; the others are sibling BB-cryptids and Mahler `p/q` problems. **One tool resolves the family.**
3. **Mahler 3/2 (1968)** itself — the archimedean shadow `{(3/2)ⁿ mod 1}`; the program's namesake hard instance.

## What this changes operationally (and what it does not)
- **Does not change** the mathematics, the wall, or the honesty labels — the verified body is identical.
- **Does change** the deliverable framing: a result is now scored by *what it teaches the genericity theory*, not
  only *whether it decides Antihydra*. A partial that illuminates the `amenable ∩ hyperbolic` cell counts as
  progress even with Antihydra still open. This is the "accrues either way" property the meeting wanted.
- **Renames the multi-year target** (`RETROSPECTIVE` #3 / `NEW_ENGINE` ★) as the program's **central theorem**, not
  a tool to be built in service of one machine.

## The plan the meeting set (phases)
- **Phase 1 — external (now).** Send both expert asks (`EXPERT_ASK.md`, `EXPERT_ASK_HOMOGENEOUS.md`) + the
  round-2 brief (`MEETING_BRIEF_2.md`). The single highest-value question: **is `amenable ∩ hyperbolic` a
  recognized empty cell, and is there a `quenched → annealed` bridge?**
- **Phase 2 — internal, while waiting: deepen the classification (instance set #2).** Push the cross-cryptid
  theorem: map the **full** `v_p(μ)=−1` family, confirm the shared kernel/obstruction across several primes,
  and surface any instance where the obstruction is **strictly easier** (a sibling with an exploitable extra
  structure Antihydra lacks). A program-level win, independent of expert reply. *(This is the standing internal
  attack — it produces forward motion every turn without waiting on anyone.)*
- **Phase 3 — if the experts say "open/don't know": open A1** — begin building the genericity theory itself
  (the `quenched → annealed` / one-sided-anti-concentration tool), now as the program's central theorem.

## One-line status for the index
Banner inverted: the program is **rank-1 specified-orbit genericity**; **Antihydra is instance #1**, the
`v_p(μ)=−1` family is instance set #2, Mahler 3/2 is the namesake. The project is **more open, not less** — it now
has a frontier that accrues whether or not any single machine is decided. Never closed; widened.
