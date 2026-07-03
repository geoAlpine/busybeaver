# BB(6) cryptid classification — a machine-verified trichotomy (2026-07-04)

*Strengthens the two-type split of `CRYPTID_KERNEL.md` ("Placing o15 and o17") into a **machine-verified
trichotomy** over 15 core cryptids, using exact reverse-engineered normal forms from this session (o2, o3, o7,
o11, o12, o13, o14, o16, Space Needle) plus the prior Mahler family (Antihydra, o10, o15, o18) and o17. Parallel
multi-agent assault; every headline cross-checked against the raw TM by the orchestrator. SOUNDNESS: labels
throughout; zero false proofs; the discipline caught a concrete agent error (Space Needle §4) and revised the
"o17 is unique" claim (o3 §3). **No machine decided; halting `[OPEN]` for all fifteen.** Verifier:
`cryptid_slowwidth_verify.py`. TMs in `suite.py`/`tier3_suite.py`/`cryptid_census.py`.*

## 0. The trichotomy

Every core BB(6) cryptid analyzed splits by **where its hardness lives** — a refinement of `CRYPTID_KERNEL.md`'s
`v_p(μ)=−1` kernel theorem:

| type | machines | mechanism | the wall |
|---|---|---|---|
| **I — equidistribution-kernel Mahler** | Antihydra, o10, o15, o18, **o2, o7, o11, o12, o13, o14, o16, o4** (12) | tape encodes a scalar/counter **value orbit growing `×3/2` (p=2), `×8/3` (p=3), or `×4/3` (p=3, o4)**; halt = a **parity/alignment/existence event on that single orbit** | **(K) / Mahler-3/2 / Erdős** single-orbit equidistribution (Mahler 1968; AEV 1.6) |
| **II — kernel-less carry-cascade outlier** | **o17, o3** (2) | a **tame odometer/bouncer with NO equidistribution kernel** (genericity is automatic); ALL hardness is a **Collatz-irregular halt predicate** (`00`-gap / marker-parity existence) | **generalized-Collatz carry-existence** (Michel; Kurtz–Simon Π⁰₂) |
| **III — scalar generalized-Collatz** | **Space Needle** (1) | a **single scalar block** `1^m` with an explicit 2-adic map `f(m)`, **cubic-time**; halt = orbit **hits a sparse set** | **generalized-Collatz** reachability |

## 1. The discriminator is CONTENT, not growth-rate `[the session's key methodological finding]`

**The `√t`-bouncer phenotype is NOT diagnostic of type.** All of o2, o7, o11, o12, o13, o14, o16 (Type I) AND
o17, o3 (Type II) grow as `width ∼ step^{1/2}`. The census had used slow/√t growth to *tentatively* cluster
these as "near-o17"; that is a **red herring**. `√t` arises three unrelated ways:

- **Type I:** an **exponential** value orbit (`×3/2`) stored in **unary** ⇒ value `V` costs `Θ(V²)` steps ⇒
  `width ∼ V ∼ √t`. (o2/o7/o13: two-counter `1^a 0 1^b`; o12/o14/o16: two-counter over a `(10)*` sea; o11:
  base-3/2 odometer.) The content is *exponential*.
- **Type II:** a **free-running length counter** over a **bounded/tame** digit string ⇒ polynomial, linear-space.
  (o17: unbounded digits, `max_digit = n − c`; o3: bounded `{0,1}` digits, digit-sum `S` only *logarithmic*.)
  The content is *polynomial* (no value orbit at all).
- **Type III:** a **scalar** value with **cubic** per-epoch cost ⇒ `width ∼ step^{1/3}` (Space Needle — even
  slower).

> **The real discriminator:** does the tape carry an **exponentially-growing arithmetic value** (Type I,
> Mahler kernel) or only a **bounded-digit carry cascade / free-running counter** (Type II) or a **single
> scalar Collatz orbit** (Type III)? Verified per machine: Type I has an exact `⌊(p/q)x⌋+c` orbit; Type II has
> `0` scalar decodings and only log/linear-growing content; Type III has one explicit scalar map.

## 2. Type I — twelve equidistribution-kernel machines `[OBSERVED/verified vs raw TM]`

All reduce to a clean `⌊(p/q)x⌋` orbit; halting is a parity/existence event on it (the (K)/Erdős wall).
Machine-verified normal forms + maps (0 mismatches on the tested ranges):

- **o2, o7** — `1^a 0 1^b` two-counter; `a↦⌊3a/2⌋`-type Mahler, `b` an Antihydra balance/refill counter; reset-`a`
  values → `×3/2` (o7 tail ratios 1.502,1.503,1.504). o7 exact map `even a:(a,b)→(3a/2+1+b,1)`, `odd a:→((a−3)/2,
  b+(a+5)/2)`.
- **o13** — `1^a 0 1^b (01)^k`; reboot leading value `40,67,104,163,…,6620` with `a_{n+1}=⌊3a_n/2⌋+c`
  (`c=7` even / `4` odd), ratios →1.5.
- **o12** — `1^a 0 1^b (10)^m`; invariant `V=3a+2b` conserved in-epoch (`a−2,b+3`), `V'=⌊3V/2⌋+c` at reflection,
  ratios →1.5000; halt = right-boundary phase-parity (o16 twin).
- **o14** — nested; inner exchange `(a,b)→(a−2,b+3)`, A-start map `A'=⌊3A/2⌋+6` (clean constant +6), ratios →1.501;
  doubly-exp outer refill.
- **o16** — nested; inner `S'=⌊3S/2⌋+c` (`c∈{4,6}`), ratios →1.500; middle countdown −1/epoch; doubly-exp refill.
- **o11** — base-3/2 **odometer**: reflection widths `D'=⌊3D/2⌋+ε` (`ε∈{1,2,3}`, one carry bit); halt = marker
  top-digit → 0.
- **Antihydra, o10, o15, o18** — the prior Mahler family (`CRYPTID_KERNEL.md`, `CRYPTID_O18_FRAMEWORK.md`, …):
  `μ=3/2` (Antihydra, o10-inner) and `μ=8/3` (o15, o18); `v_p(μ)=−1` kernel theorem.
- **o4** `[verified, O4_HALT.md]` — a **NEW ratio `μ=4/3` (`v₃=−1`, kernel prime 3)**: an exact closed base-4/3
  value odometer `G'=⌊4G/3⌋+c(G mod3)` (residual 0, ratio→1.33338), with a `[PROVEN]` **11-existence** halt gate
  (dual to o3's 00-gate; 0 firings / 15M). Settles that a `4/3` can be a *genuine value* (o4), the opposite of
  o3's `4/3`-as-envelope. Adds a third census ratio (`3/2, 8/3, 4/3`).

Every Type I halt is a parity/existence condition on an **unbounded `⌊(p/q)x⌋` orbit** — the (K) wall,
generationally stuck (No-Structure, Coverage No-Go, decider-preemption; `PROBLEM_LIST.md` P1).

## 3. Type II — o17 is NOT unique: o3 is a second (tamer) outlier `[OBSERVED, verified]`

Both are **tame odometers/bouncers with no equidistribution kernel** — genericity is automatic (odometers are
uniquely ergodic), so all hardness is the **Collatz-irregular halt predicate**.

- **o17** — `(3|5)·(0 1^{ℓ}, ℓ≡2 mod3)*`, **unbounded** base-3 digits; free-running LSB counter `max_digit=n−c`;
  halt `⟺` leading block (odometer MSB) ever even — a `[PROVEN]` single-parity-bit reduction (`O17_CORE_TRANSDUCER.md`).
- **o3** `[verified this session]` — `(1|11)·(0·(1|11))*`, **bounded** digit alphabet `{0,1}` (even tamer than
  o17); width `W=2m−1+S`; free-running **length** counter `m` (+1/milestone → `width∼√t`), digit-sum `S` grows only
  **logarithmically** (orchestrator check: `S=3,7,10,13` at milestones `10,50,200,1000`; `max block=2`, `0`
  non-single gaps). No scalar value orbit exists; the `×4/3` in generation-lengths is **bouncer-envelope
  geometry** (constant defect drift over geometrically-growing width), not a value multiplier. Halt `⟺` the
  irregular marker-carry cascade ever emits a `00` gap read by state E — a generalized-Collatz existence event
  (not reducible to a bounded-context bit, unlike o17's clean parity).

> **Revision:** the prior "o17 is the unique structural outlier" (`CRYPTID_KERNEL.md`) is corrected — **there are
> at least two** (o17, o3), and o3 is the *tamest* cryptid found (bounded digits, exactly-linear drift), yet still
> Collatz-hard in its halt predicate. This strengthens the two-type picture into a populated Type II.

## 4. Type III — Space Needle, with a soundness correction `[OBSERVED, corrected]`

Single scalar block `1^m` (head on the right `0`, state C); map `f(m)=m+3⌊m/2^{v+1}⌋+v` (`v`=trailing-1s); cubic
time ⇒ `width∼step^{1/3}`. The blank orbit `2,5,9,16,40,100,250,625,1094,…` is verified vs the raw TM.
**CORRECTION (orchestrator):** the subagent's clean "HALT ⟺ all-ones `2^k−1`" is **FALSE** — the true-config raw
halt set for `m≤160` is `{1,3,6,7,15,31,63,102,127}`; `m=6` (`110`) and `102` halt but are not all-ones, and the
map gives `f(6)=15` where the TM actually halts. The reduction survives as "orbit reaches a halt set `S⊋{2^k−1}`"
(a generalized-Collatz reachability); the blank orbit avoids `S` in-range ⇒ still `[OPEN]`, but the clean all-ones
claim is retracted.

## 5. Cross-cutting structure + the (K) probe

- **Every halt is an existence/reachability event over an unbounded-history object** — a `00` appears (o3, o11,
  o12, o14, o16), a marker parity flips (o17), a balance returns to 0 (o2), a scalar hits a sparse set (Space
  Needle, o7's `a→1`). None is a bounded-context decision; all need the full orbit history = the wall.
- **(K) fresh-angle probe (this session): no new handle `[verdict (c)]`.** Antihydra *is* a two-counter skew
  product (autonomous `c`, cocycle balance `B`); "non-halt ⟺ B never hits −1" and the o7-style value-hitting form
  both **reduce to (K)** for verified reasons — **non-descent** (`⌊3c/2⌋ mod 2^k` is not a function of `c mod 2^k`)
  and **full residue coverage** (`c_n mod 2^k` visits all `2^k` residues) forbid any finite-state / avoidance
  invariant; the one attack the reachability framing suggests (a reachability-Lyapunov monovariant) is exactly the
  already-closed excursion no-go (`EXCURSION_SYNTHESIS.md`). The o17 single-bit decoupling has an Antihydra
  analogue but **isolates** rather than **separates** the hardness (that bit's density = (K)).

## 6. Honest verdict

**Outcome (c) across the board, with (b) structural sharpenings.** All fifteen cryptids rederive a known wall:
eleven the **(K)/Mahler-3/2 (Erdős)** equidistribution wall, two (o17, o3) the **generalized-Collatz
carry-existence** wall, one (Space Needle) the **generalized-Collatz reachability** wall. The genuine gains are
**structural and classificatory**: machine-verified exact normal forms for all nine session machines (several
*superseding* prior "no clean map" catalogue verdicts — o12, o13, o14), the **√t-is-not-diagnostic** finding, the
**second structural outlier o3**, and the **soundness corrections** (Space Needle all-ones; o7 recovery). No new
handle on (K). **No machine decided. No non-halting proven. No label upgraded. Halting `[OPEN]` for all fifteen.**

## Reproduce
- `cryptid_slowwidth_verify.py` — o7 Mahler-3/2 (`×3/2` reset ratios) + the Space Needle halt-set correction
  (`{1,3,6,7,15,31,63}` for m≤64, `m=6` halts ∉ all-ones).
- Per-machine sims/automata in the session scratchpad (not committed). TMs: `suite.py`, `tier3_suite.py`,
  `cryptid_census.py`. Interpreter `/opt/homebrew/bin/python3.13` (`python3` alias is broken).
- Prior basis: `CRYPTID_KERNEL.md` (the `v_p(μ)=−1` kernel theorem + the original o15/o17 placement),
  `CRYPTID_SLOWWIDTH_2026-07-04.md` (the first five machines), `O17_CORE_TRANSDUCER.md` (the Type-II exemplar).
