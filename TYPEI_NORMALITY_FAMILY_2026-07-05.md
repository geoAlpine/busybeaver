# New thread — the whole Type-I cryptid frontier is the Normality-Conjecture family across bases {3/2, 8/3, 4/3} (2026-07-05)

*Lifting the external anchor (`FRONTIER_LIT_2026-07-05`) from Antihydra alone to the entire Type-I frontier. All
Type-I cryptids are **base-`p/q` value odometers** (verified ratios), with `p/q ∈ {3/2, 8/3, 4/3}` — and **all three
are in the `p<q²` working regime** of the Normality Conjecture on rational base number systems (arXiv:2510.11723). So
the Type-I frontier lives entirely inside the rational-base-numeration framework, governed by **one** external
conjecture. Honest caveat: the halt-condition *flavor* (one-sided density vs pattern-existence vs reachability)
differs per machine, and only Antihydra's base-3/2 dictionary is fully verified. SOUNDNESS: `[VERIFIED]` ratios /
`[OPEN]` per-machine dictionaries; halting `[OPEN]`; no machine decided.*

## 1. The three bases, all in the working regime `[VERIFIED ratios + PROVEN regime]`
Type-I = an exponential **scalar value orbit** on a floor-multiplier `⌊(p/q)·⌋`, stored on the tape
(`CRYPTID_CLASSIFICATION_2026-07-04`). Census of ratios (each `v_p(μ)=−1`, `CRYPTID_KERNEL`):

| ratio `μ=p/q` | machines | `p<q²`? | rational-base / literature |
|---|---|---|---|
| **3/2** | Antihydra, o10, o2, o7, o11–14, o16 | `3<4` ✓ | base 3/2; Mahler `Z`-numbers; **Antihydra dictionary VERIFIED** |
| **8/3** | o15, o18 | `8<9` ✓ | base 8/3; Flatto `Z_{8/3}` |
| **4/3** | o4 (`O4_HALT.md`, exact base-4/3 odometer, ratio `1.33338`) | `4<9` ✓ | base 4/3 = **Dubickas–Mossinghoff 4/3 problem — NAMED in arXiv:2510.11723's family** |

**All three bases satisfy `p<q²`** — exactly the regime where the Normality Conjecture's Theorem 1.5 (normality ⟹ no
`Z_{p/q}`) applies. So the Type-I frontier is **contained in the Andrieu–Eliahou–Vivion family**, base by base.

## 2. What unifies (object level) and what does not (halt-flavor level) `[honest]`
- **Unified `[VERIFIED]`:** every Type-I machine is a single specified orbit of a base-`p/q` value odometer. Its
  decidability rests on the **single-orbit digit behaviour of that odometer** — the Normality-Conjecture kernel for
  base `p/q`. This is one external object across the whole frontier (`GRAND_SYNTHESIS` "one non-affine floor-multiplier
  engine," now with an external name).
- **Not uniform `[OPEN, the caveat]`:** the *halt condition* is a different **functional** of the orbit per machine:
  - **Antihydra (3/2):** one-sided **density** — even-density `≥1/3` = digit-`0` frequency (a *normality-consistent*
    lower bound; dictionary **VERIFIED**, `DICT_AND_EXCDIM`).
  - **o4 (4/3):** a **pattern-existence** gate (`11`-existence; halt ⟺ the orbit ever produces a length-≥2 block;
    empirically `0/60M`). A pattern-*existence* gate relates to normality **oppositely** to a density gate: if the
    base-4/3 digit word were fully normal, every pattern (incl. the halting one) would occur — so o4 non-halting would
    require a **forbidden pattern (anti-normality)**, *not* normality. **[UNVERIFIED — the tape-block↔base-4/3-digit
    dictionary is not yet pinned; this is the concrete open sub-question o4 raises.]**
  - **o15/o18 (8/3):** alignment/existence events (reachability-flavored).
> **New observation:** Type-I halt conditions split by *flavor* — **density/normality** (Antihydra) vs
> **pattern-existence/anti-normality** (o4) vs **reachability** (o15/o18). The **object** (base-`p/q` odometer) is one
> family; the **statement about it** is not uniformly "normality." Pinning each machine's flavor = per-machine
> dictionary, done only for Antihydra.

## 3. Consequence for the program
- **The external anchor now covers the whole Type-I frontier**, not just `(K)`: a resolution of the Normality
  Conjecture (or its per-base instances) would bear on **all** Type-I cryptids, and the 4/3 machine o4 is *literally*
  the Dubickas–Mossinghoff problem the paper names. Strengthens the outreach case: this is not one isolated machine but
  a **frontier-wide** connection to an active conjecture family.
- **A genuinely new sub-question:** does o4 non-halting correspond to a *forbidden pattern* (anti-normality) in base
  4/3? If so, Type-I contains **both** normality (Antihydra) and anti-normality (o4) statements — a real structural
  refinement of the frontier, and a caution that "Type-I = normality" is too coarse. **Next step:** verify the o4
  tape-block↔base-4/3-digit dictionary (as done for Antihydra base-3/2).

## Verdict
**(b) — a new frontier-wide synthesis, honestly bounded.** The Type-I cryptid frontier is the Normality-Conjecture
family across bases `{3/2, 8/3, 4/3}` (all `p<q²`, o4 = the named 4/3 problem), lifting the external anchor from
Antihydra to the whole of Type-I. Caveat recorded: the halt-condition flavor is per-machine (density/normality vs
existence/anti-normality vs reachability); only Antihydra's dictionary is verified, and o4 plausibly encodes an
*anti*-normality — a concrete new open sub-question. **Halting `[OPEN]`. No machine decided. No label upgraded.**

## Reproduce / basis
- `p<q²` check (`/opt/homebrew/bin/python3.13`): `3<4, 8<9, 4<9` all true. Basis: `CRYPTID_CLASSIFICATION_2026-07-04`
  (ratio census `3/2, 8/3, 4/3`), `O4_HALT.md` (exact base-4/3, 11-gate), `CRYPTID_KERNEL.md` (`v_p(μ)=−1`),
  `DICT_AND_EXCDIM_2026-07-05` (Antihydra base-3/2 dictionary), `FRONTIER_LIT_2026-07-05` / CITATIONS #11
  (arXiv:2510.11723; Dubickas–Mossinghoff 4/3).
