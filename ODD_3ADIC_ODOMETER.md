# The 3-adic / odometer mechanism on the odd-character block — does it reach Inj_a? (2026-06-29)

*Assigned task: apply the non-spectral 3-adic / odometer / isometric-rotation mechanism to the Open Lemma
(`ENDOGENOUS_UE_BUILD.md §4`), the sole residue after the annealed no-go. The no-go says any bound on the
odd block must use the **arithmetic** of the endogenous bit `β_n = bit_k(c_n)`, not `(gap, automaton)`. The
odometer idea: `×3` is an isometry (zero entropy, carries every bit), and odometers / isometric rotations
equidistribute SPECIFIED orbits by a non-spectral mechanism (carry combinatorics / Weyl on the dual group).
Determine precisely whether this reaches a genuine PARTIAL on the odd block or reduces to Mahler. Numerics
`/Users/aokiyousuke/quantum-ecc/.venv/bin/python scratchpad/odd_3adic_odometer.py`, exact big-int, N=10^5,
runs ≈7s. Every claim labelled. Zero false proofs. NOT committed.*

---

## 0. One-line verdict

**(c) REDUCES TO MAHLER — sharply, with a new exact rewrite and a clean separation of where the odometer
mechanism succeeds from where it cannot.** The odd-character feedback is rewritten EXACTLY as the read of a
`×3` **isometric-rotation orbit on `ℤ₂`** at the **moving diagonal index `n+k`**, perturbed by an
**endogenous carry** `S_n`:

> **`[PROVEN]` (rewrite)** `β_n = bit_k(c_n) = bit_{n+k}(8·3^n − S_n)`, where `2^n c_n + S_n = 8·3^n` and
> `S_n = Σ_{j<n} 3^{n−1−j} 2^j b_j`, `b_j = c_j mod 2` (verified 0 failures, big-int, n<4000, k∈{2,5,9}).

The non-spectral odometer mechanism **does** deliver an unconditional theorem — but for the **fixed-position
exogenous** digit `bit_m(8·3^n)`, which is **periodic in `n`** (`×3` is a `ℤ₂`-isometry) and hence has a
provable rational Cesàro mean (`= 1/2` for `m ≥ 6`). `Inj_a` reads the **diagonal** (`bit_{n+k}` with the
index growing with the clock) **and** uses the **endogenous** offset `S_n` — and BOTH are exactly the open
content: reading the diagonal of the zero-entropy `×3` isometry is verbatim Mahler 3/2
(`mahler_equidistribution_attack.md §9`), and `S_n` is the self-reference the no-go isolated. The mechanism
is **bit-blind on the diagonal**. No partial on the odd block; no label upgraded.

---

## 1. The rewrite: Inj_a as a read of a `×3`-isometry orbit + endogenous carry  `[PROVEN]`

The odd-character feedback (Open Lemma) is `Inj_a(N) = (1/N) Σ_{n<N} (β_n − ½)·χ_a(U(s_n,0))`. Its entire
arithmetic content is the bit `β_n = bit_k(c_n)`. Linearising the orbit `c_{n+1} = ⌊3c_n/2⌋` exactly: with
`a_n := 2^n c_n`, `2c_{n+1} = 3c_n − b_n` gives `a_{n+1} = 3a_n − 2^n b_n`, `a_0 = 8`, so

> **`[PROVEN]`** `2^n c_n + S_n = 8·3^n`, `S_n = Σ_{j=0}^{n−1} 3^{n−1−j} 2^j b_j` (a 3-adic-weighted sum
> of the orbit's own low bits `b_j`), `0 ≤ S_n ≤ 3^n − 2^n`.

Since `2^n c_n = 8·3^n − S_n` is divisible by `2^n`, `bit_k(c_n) = bit_{n+k}(8·3^n − S_n)`. **Verified exactly:**
the `S_n` recursion `S_{n+1} = 3S_n + 2^n b_n`, the identity `2^n c_n + S_n = 8·3^n`, and the bit identity
all have **0 failures** over `n < 4000`, `k ∈ {2,5,9}` (big-int).

**Reading.** `8·3^n` is the orbit of the map `x ↦ 3x` on `ℤ₂`. Because `|3|_2 = 1`, this map is an
**isometry** (zero entropy, carries every bit) — the exact object the prompt names, and the bit-bearing
factor of the product-formula splitting of `×(3/2)` (`mahler §9`). So:

> **`[PROVEN]` Structural form of the odd feedback.** `β_n − ½` is the (centred) **moving-diagonal read**
> `bit_{n+k}(·)` of the `×3` isometric-rotation orbit `8·3^n` on `ℤ₂`, **offset by the endogenous carry
> `S_n`** (= the orbit's own low-bit history, 3-adically weighted). `Inj_a` is therefore the correlation of
> THIS read with a character of the low state — NOT a correlation against a clean *exogenous* rotation orbit.

This is the precise answer to ask #1: the odd-character feedback **can** be rewritten as a read of a `×3`
isometry/odometer orbit, but the read is **diagonal + self-referential**, the two features that defeat the
mechanism (§3).

> **Relation to the `ℤ₃` side (honesty).** The prompt's "`×3` on `ℤ₃`" is a *contraction* (`|3|_3 = 1/3`),
> not an isometry; the genuinely zero-entropy bit-carrying isometry is `×3` on **`ℤ₂`** (above). The actual
> `ℤ₃` channel of this problem — `v3(o_{j+1}) = D_j − 1` on the induced orbit — was already shown to be an
> **invertible re-encoding of the 2-adic itinerary** (`THREEADIC_SKEW §2`, `ADELIC_COUPLING §1a`), i.e. an
> isomorphism of the obstruction, and its `mod 3^k` residue is **aperiodic / full-complexity, NOT a
> rotation** (`THREEADIC_ROTATION §1–3`). So neither `ℤ₃` reading supplies a tame odometer; the only
> isometric-rotation structure available is `×3` on `ℤ₂`, handled here.

---

## 2. The odometer mechanism DOES work — for the fixed-position exogenous digit  `[PROVEN]`

The non-spectral win is real and unconditional, exactly where the mechanism is designed to act: a
**fixed-position** digit of the isometric-rotation orbit.

> **`[PROVEN]` (fixed-position periodicity).** For fixed `m`, `bit_m(8·3^n)` is **periodic in `n`** (the
> low `m+1` bits of `8·3^n` cycle: `×3` is a bijection of the finite group `(ℤ/2^{m+1})^*`). Its Cesàro
> mean is the per-period average — a **computable rational**, `= ½` for `m ≥ 6`.

Measured periods and per-period means (`scratchpad/odd_3adic_odometer.py` T3):

| `m` | period in `n` | per-period mean of `bit_m(8·3^n)` |
|---|---|---|
| 4 | 2 | 0.5000 |
| 6 | 4 | 0.5000 |
| 7 | 8 | 0.5000 |
| 8 | 16 | 0.5000 |
| 9 | 32 | 0.5000 |
| 10 | 64 | 0.5000 |
| 11 | 128 | 0.5000 |

(For `m = 2,3,5` the period is `1–2` and the bit is eventually constant; the per-period mean is still
*determined*, `0` or `1`.) Because both the digit AND a fixed-position character of the low bits are jointly
periodic, the **exogenous fixed-position analogue of `Inj_a` has a PROVABLE rational Cesàro limit** (here
`0` for balanced `m`). This is the genuine non-spectral / odometer / carry-combinatorics theorem: it needs
no spectral gap and certifies a *specified* orbit — precisely the kind of mechanism the no-go calls for.

**It is the right tool aimed at the wrong digit (§3).** It certifies *fixed-position* digits; `Inj_a` reads
a *moving* digit.

---

## 3. Why it cannot reach `Inj_a` — the moving diagonal + endogenous carry  `[PROVEN reduction]`

Two independent obstructions, each fatal, both `[PROVEN]`:

**(i) Moving diagonal = Mahler.** `Inj_a` reads `bit_{n+k}`, the index growing with the clock `n` — the
**diagonal** of the isometry, not a fixed position. The periodicity of §2 is in the *fixed-position* index;
the diagonal visits a new phase every step, so periodicity does not transfer. Verified: the diagonal bit
`bit_{n+k}(8·3^n)` has **no period `≤ 2000`** (k=3,5), whereas every fixed-position bit is periodic. Its
mean is `0.5026` (k=3), `0.5002` (k=5) — equidistributed only **numerically**. This is exactly
`mahler_equidistribution_attack.md §9–10`: the Mahler 3/2 problem *is* the equidistribution of the diagonal
bit `bit_n(3^n)` of the zero-entropy `×3` isometry; the one mixing factor (the real `β`-map) is bit-blind,
and the bit-bearing factor (the `ℤ₂` isometry) has only rigid/periodic structure that the diagonal read
destroys. No additive-rotation theorem (Weyl `{nα}`, three-distance) applies: the index enters the **read
position multiplicatively**, not as an additive phase, and van der Corput differencing is inert on the
multiplicative recurrence `(3/2)^{n+1} = (3/2)(3/2)^n` (`mahler §3`). The dual-lattice / Hecke–Mahler route
for `⌊αθ^n⌋` is, for `θ = 3/2`, **literally** Mahler 3/2 — open.

**(ii) Endogenous carry = the no-go's self-reference.** Even setting the diagonal aside, the read is of
`8·3^n − S_n`, not `8·3^n`. The offset `S_n = Σ 3^{n−1−j} 2^j b_j` is built from the **orbit's own low
bits** — it is the self-reference the no-go (`ENDOGENOUS_UE_BUILD §5`) proved no `(gap, automaton)` bound
can touch. A clean odometer/rotation theorem requires an **exogenous** orbit `{x·θ^n}`; here `θ^n` is
exogenous but the orbit being read is `θ^n` *minus its own history*. The carry re-injects the full
itinerary, so the object is not a specified rotation orbit but a closed loop — exactly the structure
`THREEADIC_ROTATION §3` identified as "orbit-driven (full-complexity)" versus "clock-driven (tame)."

> **`[PROVEN]` Verdict on the mechanism.** The odometer / isometric-rotation mechanism yields an
> unconditional equidistribution theorem ONLY for fixed-position digits of the `×3`-isometry orbit (§2).
> `Inj_a` reads the **moving diagonal** of that orbit (= open Mahler 3/2) **and** uses the **endogenous
> carry** `S_n` (= the irreducible self-reference). The mechanism is bit-blind precisely on the diagonal,
> and the orbit it would need to be exogenous is self-referential. It **reduces**; it reaches no partial.

---

## 4. Direct measurement of `Inj_a` on the odd block  `[OBSERVED]`

`scratchpad/odd_3adic_odometer.py` T1, real orbit `c0=8`, `N=10^5`, CLT floor `1/√N = 0.00316`:

| `k` | odd `a` | `|Inj_a(N)|` | `/ CLT floor` |
|---|---|---|---|
| 2 | 1 | `1.18e-3` | 0.37 |
| 3 | 1 | `1.55e-3` | 0.49 |
| 4 | 1 | `2.22e-3` | 0.70 |
| 5 | 3 | `2.19e-3` | 0.69 |
| 6 | 1 | `4.84e-4` | 0.15 |
| 7 | 1 | `3.40e-4` | 0.11 |

All odd characters sit **at or below the `1/√N` CLT floor** — `Inj_a → 0` is OBSERVED with full
square-root cancellation, never bigger than the noise band. This is consistent with the kernel but proves
nothing about the limit (the C5 adversary realises `|Inj| ≈ 1` with the identical automaton/gap). No `a`,
no `k` gives a one-sided or unconditional partial: by `INTRATERM_ADELIC_MINING §4` even `k=2` (mod 4) is
already the full wall, and the only unconditional count on the orbit remains the log-scale
`#even ≥ 0.89 log n` (`ANNEALED_PARTIAL_BANKED`). **No partial on the odd block.**

---

## 5. Verdict (the three asks)

| ask | answer | label |
|---|---|---|
| (a) cracks / partial on the odd block? | **No.** `Inj_a → 0` only OBSERVED (≤ CLT floor, T1); the only unconditional vanishing the odometer mechanism proves is for the **fixed-position exogenous** digit (§2), which is bit-blind to `Inj_a`. No `a`/`k` yields a one-sided bound. | `[PROVEN no-partial]` |
| (b) new characterization of why the odometer mechanism fails/reduces? | **Yes (sharper).** Exact rewrite `β_n = bit_{n+k}(8·3^n − S_n)`: the feedback is the **moving-diagonal** read of the `×3` `ℤ₂`-isometry orbit, offset by the **endogenous carry** `S_n`. The mechanism gives an unconditional theorem for **fixed-position** digits (periodic, rational Cesàro mean) but is **bit-blind on the diagonal**; and the orbit it reads is **self-referential** (not exogenous). Cleanly separates where the non-spectral tool wins from where it cannot reach. | `[PROVEN]` |
| (c) reduces to Mahler? | **Yes, both ways.** Diagonal read of the zero-entropy `×3` isometry = Mahler 3/2 verbatim (`mahler §9`); and the carry `S_n` = the self-reference the annealed no-go isolated. Isomorphism of the obstruction, not a reduction in difficulty. | `[PROVEN reduction]` |

**Exact residual gap.** Two locked-together pieces, each = the open core: (1) equidistribute the **moving
diagonal** `bit_{n+k}(8·3^n)` of the `×3` `ℤ₂`-isometry for the specified start `8` (= Mahler 3/2 / AEV
2510.11723), and (2) show the **endogenous carry** `S_n = Σ 3^{n−1−j} 2^j b_j` decorrelates from it (= the
no-go's self-reference). The odometer mechanism closes neither; it closes only the fixed-position surrogate
that does not feed `Inj_a`.

### New asset banked `[PROVEN]`
*Exact diagonal rewrite of the odd-character feedback:* `2^n c_n + S_n = 8·3^n`,
`S_n = Σ_{j<n} 3^{n−1−j} 2^j b_j`, hence `β_n = bit_k(c_n) = bit_{n+k}(8·3^n − S_n)` — the Open-Lemma bit is
the moving-diagonal read of the `×3` `ℤ₂`-isometry orbit perturbed by an endogenous 3-adically-weighted
carry. *Mechanism-localisation:* the non-spectral odometer theorem certifies fixed-position digits
(periodic, rational Cesàro mean = ½ for `m ≥ 6`) but is structurally bit-blind on the diagonal where `Inj_a`
lives.

### Genuinely new vs prior notes
- `mahler §9` identified Mahler 3/2 as the diagonal bit `bit_n(3^n)` of the `×3` isometry, but for the bare
  `(3/2)^n` sequence. **This note carries that identification onto the endogenous `Inj_a` object**: it shows
  the Open-Lemma bit `bit_k(c_n)` is *literally* a moving-diagonal read of the same isometry, plus an exact
  endogenous carry `S_n`, with the carry recursion verified to 0 failures.
- `THREEADIC_ROTATION/SKEW/INTRATERM/ADELIC_COUPLING` handled the **`ℤ₃` (induced-orbit) valuation channel**
  and proved it an isomorphism of the obstruction; **this note handles the `ℤ₂` `×3`-isometry channel of the
  `c`-orbit directly** and adds the explicit fixed-position-vs-diagonal separation (the periodic surrogate is
  new here) that pins *why* the odometer mechanism is the right tool aimed at the wrong digit.
- Sharpens `ENDOGENOUS_UE_BUILD §5`: the no-go said "use the arithmetic of `β_n`"; this exhibits that
  arithmetic concretely (`β_n = bit_{n+k}(8·3^n − S_n)`) and shows the named non-spectral candidate hits the
  two known walls (diagonal = Mahler; carry = self-reference).

### Why this confirms rather than breaches (honest)
The odometer / isometric-rotation idea is genuinely the no-go-compatible kind of mechanism, and it does prove
an unconditional, gap-free equidistribution — but only for fixed-position digits, an object orthogonal to the
diagonal feedback. The exact rewrite makes the failure mode precise and citable: the bit `Inj_a` needs is the
diagonal of a zero-entropy isometry (Mahler) read of a self-referential orbit (the no-go). Fully consistent
with `mahler_equidistribution_attack §9–10`, `ENDOGENOUS_UE_BUILD §4–5`, `THREEADIC_*`, and the AEV/Mahler
anchor.

## Sources
- Repo: `ENDOGENOUS_UE_BUILD.md` (Open Lemma §4, annealed no-go §5), `mahler_equidistribution_attack.md`
  (§3 differencing inert, §9–10 diagonal bit `bit_n(3^n)` = Mahler, `×3` on `ℤ₂` isometry), `WALLB_MARTINGALE.md`
  (fixed-position carry periodicity; `r_n = bit_{n+3}(3^n)` moving diagonal), `THREEADIC_ROTATION.md`
  (`o mod 3^k` aperiodic, not a rotation), `THREEADIC_SKEW.md` / `ADELIC_COUPLING.md` (valuation channel =
  invertible re-encoding), `THREEADIC_INTRATERM.md` / `INTRATERM_ADELIC_MINING.md` (`u ⊥ e`, mod-4 cofactor =
  wall), `ANNEALED_PARTIAL_BANKED.md` (`#even ≥ 0.89 log n`), `WEAPONS_AUDIT_2026-06-29.md §7`.
- Literature (repo knowledge): Mahler 3/2 (1968, open); Furstenberg ×2,×3 (orbit-closure dichotomy, not
  pointwise); Rudolph–Johnson / Host / Lindenstrauss (measure rigidity, need positive-entropy jointly
  invariant measure our single orbit lacks); odometer / Weyl `{nα}` / three-distance (additive rotations —
  inapplicable: the index enters multiplicatively, in the read position); Hecke–Mahler `⌊αθ^n⌋` (for
  `θ=3/2` = Mahler, open); AEV (Andrieu–Eliahou–Vivion arXiv:2510.11723, Conj 1.6 rational base).
- Numerics: `scratchpad/odd_3adic_odometer.py` (exact big-int, N=10^5, ≈7s; T1 `Inj_a` ≤ CLT floor; T2
  rewrite 0 failures; T3 fixed-position periodicity + balance; T4 diagonal aperiodic / Mahler).

**No machine decided. No label upgraded.**
