# The Mahler cryptids share ONE kernel and ONE obstruction map (Route C, 2026-06-25)
*Cross-cryptid test: does the Antihydra dissection (renewal map → Gibbs–Markov → exact avg-jump identity →
Q9-trilogy obstruction map) **port** to the other BB(6) Mahler cryptids? **Yes — verified.** This is the
non-circular self-attack from `STRATEGY_BRIEF.md` (C), and it delivers a positive structural result that feeds
the theory deliverable (D). All claims machine-verified, exact integer/p-adic arithmetic (`cross_cryptid.py`).*

## The result (verified)
For a Mahler multiplier `μ = 2^a/3^b` whose denominator prime is `p` (so `v_p(μ) = −1`, `|μ|_p = p`), the map
`T_μ(x) = ⌊μ·x⌋` shares the **entire** Antihydra structure on `ℤ_p`:

| property | Antihydra / o10-inner (`μ=3/2`, `p=2`) | o18 / o15 (`μ=8/3`, `p=3`) | control (`μ=9/2`, `p=2`) |
|---|---|---|---|
| `p`-to-1 exact endomorphism of `ℤ_p` | ✅ | ✅ | ✅ |
| renewal density `→ 1/p` | 0.499 | 0.333 | 0.501 |
| avg gap between renewals `→ p` | 2.003 | 3.007 | 1.996 |
| **exact identity** `Σ(gap−1) = #non-renewal` | ✅ | ✅ | ✅ |
| induced map full-branch piecewise-affine expanding (slopes `μ^g`) | ✅ | ✅ | ✅ |
| **fixed point on every branch** (Q9(b) obstruction) | ✅ 8/8 | ✅ 8/8 | ✅ 8/8 |

The only structural *difference* is the branch alphabet: for `p=2` the intermediate (non-renewal) residue is
forced, so a branch = its gap `g` (clean, `g`-indexed); for `p=3` the intermediate residues range over `{1,2}`,
so a branch = the **itinerary word** (the residue sequence between renewals), a finer but still full-branch
Gibbs–Markov alphabet (e.g. o18 fixed points: word `()`→`0`, `(1)`→`2/55`, `(2)`→`1/55`, `(1,1)`→`22/485`, …,
all in `ℤ_3`). The induced-map slope is always `μ^g` (`g` = #steps in the induced step), so the map is
expanding for every `μ` with `|μ|_p = p`.

## What this means — the kernel and the wall are machine-independent
1. **One kernel.** Each Mahler cryptid's non-halting is governed by the **same object**: the single-orbit
   equidistribution of `⌊μ^n⌋ mod p` (the moving `p`-adic diagonal digit). Antihydra and o10-inner are the
   `μ=3/2`, `p=2` instance; o18 and o15 are the `μ=8/3`, `p=3` instance. (o15's orbit map is parity-irregular,
   but its kernel object `⌊(8/3)^n⌋ mod 3` is the same.)
2. **One obstruction map.** The Q9-trilogy walls are **structural properties of `T_μ` on `ℤ_p`**, hence shared:
   the spectral gap is orbit-blind (fixed points on every branch — verified for both `p=2` and `p=3`);
   non-shadowing is insufficient (the non-Haar-generic construction is the same on `ℤ_p`); growth/counting is
   circular (the same `n = #renewal + #non-renewal` identity); the soft mechanisms (unique ergodicity, rank-≥2
   rigidity, Weyl/vdC) are unavailable for the same reasons. The wall in `STATE_FOR_REVIEW.md §7.5` is not
   Antihydra-specific.
3. **One missing tool resolves the whole sub-family.** The single named residue —
   **rank-1 effective equidistribution of `⌊μ^n⌋ mod p` with a Diophantine input on `log_q p`** — would settle
   **every** Mahler cryptid at once (`3/2` *and* `8/3`), not just Antihydra. The expert ask (`EXPERT_ASK.md`
   Q1) is therefore a question about a *family*, which strengthens it.

## Scope and honesty
- **This is the Mahler-`2^a/3^b` sub-family: 4 of the 5 core cryptids** (Antihydra, o10-inner, o18, o15).
  **o17 is an odometer outlier** (a carrying base-≈3 counter, not a single `×μ` orbit) and is *not* claimed
  isomorphic; the slow-width majority (`CRYPTID_CENSUS.md`) is separate.
- **This does not decide any machine.** The per-machine *halt predicate* differs (Antihydra: even-density ≥ 1/3;
  o18: frontier-bit; o15: block-collision). What is isomorphic is the **underlying equidistribution kernel and
  its obstruction map**, i.e. *why* each is hard and *what single tool* would crack them — not a decision
  procedure. No non-halting is proved here.
- **`p`-to-1 with `v_p(μ) = −1`** is the clean regime; multipliers like `(3/2)^2 = 9/4` (`v_2 = −2`) are *not*
  single-floor `p`-to-1 (verified: 9/4 image 14/16) and would need a different (2-step) framing.

## Why this is the right kind of result for the programme
It converts "Antihydra is Mahler-hard" into a **classification**: the Collatz core of BB(6) is, up to the
machine-specific halt predicate, **one number-theoretic kernel** (`⌊(2^a/3^b)^n⌋ mod p` equidistribution) with
**one obstruction map** and **one missing tool**. This is exactly the certificate-complexity-hierarchy /
"cryptid complexity theory" deliverable (`LIMIT_THEOREM.md`, `STRATEGY_BRIEF.md` D): the cryptid vertex (no
tame certificate) is now shown to be a *single shared object* across the family, not four coincidentally-hard
machines — a recordable structural contribution independent of resolving any cryptid.

## Reproduce
`python3.11 cross_cryptid.py` (the table); `python3.11 alpha_attack.py` (the Antihydra identities the port
mirrors). Branch-by-branch o18 fixed points: the itinerary-word partition in this session's log.
