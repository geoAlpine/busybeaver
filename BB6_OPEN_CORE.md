# BB(6) open core — what the complete proof actually requires (2026-06-24)

**Capstone consolidation of the cryptid programme.** This document states, precisely and honestly, the
mathematical content gating a *complete* proof of BB(6). Companion notes (per-machine, machine-verified):
`antihydra_attack.md`, `o10_attack.md`, `o15`→`CRYPTID_REDUCTIONS.md`, `o17_attack.md`, `o18_attack.md`;
full catalogue in `CRYPTID_REDUCTIONS.md`; census in `CRYPTID_CENSUS.md`; hierarchy in `LIMIT_THEOREM.md`.

## 0. The one-sentence statement
> A complete proof of BB(6) requires deciding **every** remaining 6-state holdout (~19 community
> "cryptids"); each reduces to a **base-2/3 digit-alignment statement for an exponentially-growing
> `×2^a/3^b` orbit with a self-referentially-moving frontier**; these fall into **distinct, mutually
> irreducible world-open clusters** (Mahler-3/2 and Erdős-ternary), so the complete proof is gated behind a
> *bundle* of open number-theory problems, not one — and each is at or beyond the current unconditional
> frontier.

## 1. The unified halt-predicate form (what every cryptid turns out to be)
Reverse-engineering all 19 against the raw TM (this programme) shows each cryptid is, structurally:
```
a configuration that resets each EPOCH to a counter of value N_k,
with N_{k+1} ≈ (2^a/3^b)·N_k   (a Mahler multiplier),
and HALT ⟺ a base-(2 or 3) CARRY of the orbit ⟨N_k⟩ ever ALIGNS with a moving frontier cell
            that a halt-state tests once per epoch.
NON-HALT ⟺ the carries never align with the frontier — forever.
```
Two **structural templates** realise this (catalogue §"STAGE-1 CATALOGUE COMPLETE"):
- **(T1) two-counter** `1^a 0 1^b [0 1^c]` — Antihydra, o7, o8, o10, Space Needle, o13, o14.
- **(T2) single drifting defect over `(10)*`** — o2, o4, o11, o12, o16 (and o15/o18 as counter-over-`(10)*`).
The "polynomial-time vs exponential" split seen in widths is only a **width-envelope** artefact (sawtooth
sweep vs direct-geometric); the *content* is uniformly irregular geometric. **No tractable subclass exists.**

## 2. The clusters (mutually irreducible open problems)
| cluster | multiplier | machines | halt = | clean map? |
|---|---|---|---|---|
| **Mahler 3/2** | `3/2` | Antihydra, o7, o8, o10(inner) | 2-adic depth `v2(c_n−1) ≥ balance_n+1` (Antihydra §3c) | Antihydra `⌊3c/2⌋` clean |
| **Erdős ternary** | `8/3=2³/3`, `4/3=2²/3` | **o5 (4/3), o15 (8/3), o18 (8/3)** | base-3 carry of `×(2^a/3)` orbit aligns with frontier | o18 `⌊8N/3⌋+2` clean (breaks @epoch7); o15 parity-irregular |
| **base-3 odometer** | carry | o17 | a `00`-gap / carry event in a base-3 odometer | `o17_attack.md` |
| **nested** | `3/2` two-level | o10 | inner `⌈3m/2⌉` + irregular refill | `o10_attack.md` |
**Irreducibility:** solving Mahler-3/2 does NOT solve Erdős-ternary and vice-versa — they are different open
problems sharing only the deep root (multiplicative independence of 2 and 3). A complete proof needs **all**.

## 3. The shared wall (why each cluster is open) — identical to a Borel–Cantelli independence gap
For every cluster the heuristic is the same and points to **non-halting**:
- the orbit's relevant digits are **equidistributed** (Antihydra: even-density → 1/2 > 1/3; o18: base-3
  digit-2 density = 1/3 — both numerically verified), so a halt-alignment has probability `~1/N_k` per epoch;
- `Σ_k 1/N_k` **converges** (geometric growth) ⇒ expected number of halt-alignments `≈ 0` ⇒ heuristic NON-HALT.
**The gap (identical across clusters):** Borel–Cantelli needs **independence**, but the alignment positions
are **deterministically** fixed by the orbit's `2^a/3^b` carries. Proving non-alignment = proving a specific
digit of a specific `×2^a/3^b` orbit never lands at a self-referential spot. The strongest unconditional
tools fall short *in the same way*:
- **Narkiewicz (1980):** density *upper* bound `x^{0.631}` on the Erdős exceptional set — no lower bound, no
  per-position control.
- **Subspace theorem (Ridout/Schmidt):** gives `max-digit-run = o(n)` for a *fixed algebraic* number — not a
  *moving integer orbit* (`antihydra_attack.md` §4: the closest correct-shape tool, gap = fixed-vs-moving).
- **Sum-product (Bourgain–Konyagin …):** needs a subgroup of size `≥ q^δ`; here `{3^j mod 2^k}` with `k~cn`
  is *log-size* relative to the modulus — the regime is exponentially below threshold.

## 4. What this programme delivered (honest ledger; 0 decisions, 0 false proofs)
- **[VERIFIED] Complete catalogue:** all 19 cryptids reverse-engineered to the unified halt-predicate form;
  exactly two structural templates; no tractable subclass; the open core is the cluster table in §2.
- **[VERIFIED] Two kernels sharpened to Antihydra-level** (`antihydra_attack.md` §4, `o18_attack.md`):
  exact mechanism + sharp halt predicate + equidistribution + Borel–Cantelli non-halt heuristic + the precise
  located wall. o15 closed the Erdős cluster (symmetric 8/3 partner, parity-irregular).
- **[VERIFIED] Soundness discipline held throughout:** two over-claims caught and retracted by self-check
  (§4c orbit conflation `SOUNDNESS_INCIDENT.md`; o4 "decision lead" sawtooth-misread). The "o18 might be a
  trivial doubler" temptation was *checked* (interior-F-read found) not assumed.
- **[HONEST] No decision, and no in-session path to one.** Each cluster sits at/beyond the unconditional
  frontier. The complete proof of BB(6) requires an unconditional breakthrough on **every** cluster in §2.

## 5. The most-attackable target (if/when the breakthrough is attempted)
**Erdős-ternary cluster {o5, o15, o18}** — deciding it unconditionally decides 3 cryptids at once, it is a
*named* 1979 problem with a published partial (Narkiewicz) and an existing BB reduction (Stérin–Woods,
BB(15), arXiv:2107.12475), and o18 supplies a clean orbit `⌊8N/3⌋+2`. The required result: *a base-3 carry
of the `×(8/3)` orbit never aligns with the moving frontier* (a per-position, not density, ternary-digit
statement). This is the single best entry point; it remains world-open.
