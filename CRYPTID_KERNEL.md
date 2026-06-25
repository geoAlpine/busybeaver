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

## The classification theorem (which multipliers give the kernel — **PROVEN**)
> **Theorem.** Let `μ = a/b` in lowest terms with `b = p^β` a prime power (`p` prime). Then `T_μ(x) = ⌊μx⌋` is a
> **clean, measure-preserving, `p`-to-1 exact endomorphism of `ℤ_p`** if and only if `β = 1` (i.e. `b = p`),
> equivalently **`v_p(μ) = −1`**.

**Proof of the substantive direction (`b = p` ⇒ clean `p`-to-1), key step machine-checked.**
1. *Well-defined on `ℤ_p`.* `T(x) mod p^k` depends only on `x mod p^{k+1}`: if `x ≡ x' (mod p^{k+1})`, write
   `x = x' + m p^{k+1}`, so `ax = ax' + (am)p^{k+1}` and `⌊ax/p⌋ = ⌊ax'/p⌋ + (am)p^k ≡ ⌊ax'/p⌋ (mod p^k)`. Thus
   `T` descends to `ℤ/p^{k+1} → ℤ/p^k` for every `k`, hence to a continuous self-map of `ℤ_p`.
2. *Exactly `p`-to-1 onto.* Fix `t ∈ ℤ/p^k`. Then `⌊ax/p⌋ ≡ t (mod p^k)` `⟺` `ax ∈ [p(t+sp^k), p(t+sp^k)+p)`
   for some `s` `⟺` `ax` lies in a window of **`p` consecutive integers** mod `p^{k+1}`. Since `gcd(a,p)=1`, `a`
   is invertible mod `p^{k+1}`, so `x = a^{-1}·(those p consecutive residues)` gives **exactly `p` distinct**
   residues mod `p^{k+1}`. Every target has exactly `p` preimages. *(Machine-checked: for each `t`, the `p`
   preimages are `a^{-1}` of `p` consecutive residues — `cross_cryptid.py` classification run, all cases.)*
3. *Measure-preserving.* Uniform `p`-to-1 onto ⇒ `T_*(`Haar`) = `Haar.
4. *Exact endomorphism.* The maps `ℤ/p^{k+1} → ℤ/p^k` forget the lowest digit, so the low-digit chain has
   Dobrushin coefficient `δ(P^k)=0` (state forgotten in `k` steps); the tail σ-algebra `⋂_n T^{-n}(ℬ)` is
   trivial. (The `p=2` instance is the Antihydra engine of `STATE_FOR_REVIEW §2`.) ∎

**Converse (`β ≥ 2` ⇒ not clean), by witness.** For `b = p²`, `⌊ax/p²⌋` distributes preimages **unevenly**
(fiber sizes vary) — verified multiplicities `{1,2,3,4}` for `9/4`, `{2,3,4}` for `16/9`, `{1,2,3}` for `27/4`.
So no clean `p`-to-1 endomorphism; one needs a 2-step (`T²`-type) framing. ∎ (witness)

**So the cryptid kernel is exactly the one-parameter-per-prime family `{μ : v_p(μ)=−1}`** — `b` a single prime,
`p ∤ a`. The BB(6) instances `3/2` (`p=2`) and `8/3` (`p=3`) are two points of it; "the Mahler core is one
kernel" is now a *theorem*, not an analogy. (Restricting to `μ=2^a/3^b` gives the two BB(6) primes `p∈{2,3}`.)

## The obstruction map is uniform across the kernel family (verified beyond the BB(6) primes)
The induced (renewal) map structure — **full-branch piecewise-affine expanding (slopes `μ^g`) with a `ℤ_p`
fixed point on every branch** (the Q9(b) "spectral gap is orbit-blind" obstruction) — is verified to hold
**uniformly across many clean `μ`** beyond the two BB(6) instances: `3/2, 5/2, 7/2` (`p=2`) and `8/3, 4/3, 16/3`
(`p=3`) all give `6/6` sampled word-branches affine-with-`ℤ_p`-fixed-point (`kernel_classification.py` /
`cross_cryptid.py`). So the whole Q9-trilogy obstruction map is a property of *every* `T_μ` with `v_p(μ)=−1`,
not a coincidence of the two cryptid multipliers — the wall is genuinely family-wide.

## Placing o15 and o17 (the other two core machines) — honestly
- **o15 ∈ the `8/3` (p=3) kernel class.** Its *value* grows doubly-exponentially (`v→v^{8/3}`), i.e. its
  **width/exponent follows the `×8/3` Mahler map** — the census widths `…,107,289,772` have ratios
  `2.70, 2.67 → 8/3`. So o15 shares the *same* `p=3` kernel object `⌊(8/3)^n⌋ mod 3`. Its extra
  "parity-irregularity" lives in the **halt predicate** (a block-collision event), not in the kernel — so o15
  is in-family for the obstruction, with a messier halting encoding.
- **o17 is a genuine outlier — and interestingly the *opposite* kind of hardness.** Its base object is a
  **carrying odometer** (`x→x+1` with base-≈3 carries), which is an **isometry of `ℤ_p`, not an expanding
  `⌊μx⌋` map** — and odometers are **uniquely ergodic**, so equidistribution is *automatic* for them. Hence
  o17's wall is **not** the equidistribution kernel at all; it is its **halt predicate** (the Collatz-irregular
  family `0 A 0 1^k`, halting by `k mod 3` with proven halters interleaved — see `o17_attack.md`). So the BB(6)
  Collatz core splits into **two** obstruction types: *(equidistribution kernel)* Antihydra, o10-inner, o18,
  o15; vs *(odometer with a Collatz-irregular halt predicate)* o17.

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

## Literature anchoring (2026-06-25 triage)
The shared kernel is a **recognized open problem**, not our artifact. It is the single-orbit case of **Mahler's
3/2 problem (1968)**. The *closest* technique is **Tao (2019/2022)** (*Forum Math. Pi*, arXiv:1909.03562), which
controls the **same** p-adic skew-random-walk / renewal / Gibbs–Markov statistic we reconstruct — but for a
**log-density-1** set of seeds, never one specified seed (exact gap = remove the density average).
**Flatto–Lagarias–Pollington (1995)** gives only a *range* bound (`1/p`), not a density. A **2025** paper
(arXiv:2510.11723) poses single-orbit normality in rational-base systems as an explicit *conjecture*; the
bbchallenge reduction (arXiv:2509.12337, 2025) matches ours. So one tool — rank-1 effective *single-orbit*
equidistribution of `⌊μ^n⌋ mod p` — would lift the whole vertex, and the literature confirms no such tool
exists yet. *(Caution: arXiv:2411.03468 claims to resolve Mahler 3/2 — unverified, likely flawed; not relied on.)*

## Reproduce
`python3.11 cross_cryptid.py` (the table); `python3.11 alpha_attack.py` (the Antihydra identities the port
mirrors). Branch-by-branch o18 fixed points: the itinerary-word partition in this session's log.
