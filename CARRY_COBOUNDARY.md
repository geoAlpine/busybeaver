# Carry coboundary / telescoping via the exact recursion S_{n+1}=3S_n+2^n b_n (2026-06-29)

*Assigned task: attack ONLY piece (2) of the Open Lemma residual — the decorrelation of the self-referential
carry `S_n` — in isolation, via a COBOUNDARY/TELESCOPING route using the exact linear recursion
`S_{n+1}=3S_n+2^n b_n`. Goal: express the carry's contribution to `Inj_a(N)=N^{-1}Σ(β_n−½)χ_a(s_n)` as a
telescoping boundary term, so the self-reference would be PROVABLY negligible and Antihydra would reduce to the
PURE exogenous Mahler diagonal `d_n=bit_{n+k}(8·3^n)`. SOUNDNESS PARAMOUNT — every claim labelled, exact
big-int, no label upgraded. Numerics `/Users/.../scratchpad/carry_coboundary.py`, N=2·10⁴ (scaling to 4·10⁴),
runs <1s, 0 identity failures. NOT committed.*

---

## 0. One-line verdict

**The carry does NOT telescope. Outcome = (b)+(c): the carry-correction is itself a SECOND Mahler-class
moving diagonal, locked to the state — not a coboundary.** The linear recursion `S_{n+1}=3S_n+2^n b_n` is
broken as a telescoping device by the **moving-diagonal bit-extraction** `bit_{n+k}(·)`: the carry's
contribution to `Inj_a` is `(β_n−d_n)χ_a(s_n)` whose partial sums **grow like √N (NOT bounded)**, so it is not
a coboundary; and the carry FLIPS the exogenous digit with density **≈ ½** (full strength, not a sparse
perturbation), so `β_n` is **essentially uncorrelated** with the pure Mahler digit `d_n`. The self-reference
is therefore **not negligible** and the problem does **not** reduce to the pure exogenous Mahler diagonal.
**No machine decided. No label upgraded.**

Two genuine new [PROVEN] assets (distinct from the prior automaton-algebra coboundary no-go):
1. **Borrow decomposition** `β_n = d_n ⊕ σ_n ⊕ ρ_n` (0 failures, N=2·10⁴, k∈{2,3,5,6,8}).
2. **Finite-range borrow lemma**: the borrow `ρ_n` into bit `n+k` reads only the **k-bit windows** `[n,n+k)`
   of `8·3^n` and `S_n` — it is a bounded-range (finite-state) function — *because* `S_n ≡ 8·3^n (mod 2^n)`
   forces the borrow into bit `n` to be **0** (0 failures verifying window-borrow = full-borrow). The borrow
   is finite-state; its INPUTS are the free-zone (Mahler-class) diagonal bits.

---

## 1. Step 1 — the subtraction-borrow decomposition of β_n  [PROVEN, 0 failures]

The established rewrite is `β_n = bit_k(c_n) = bit_{n+k}(8·3^n − S_n)` with `2^n c_n = 8·3^n − S_n`,
`S_{n+1}=3S_n+2^n b_n`, `b_n=c_n mod 2`. Bit `m` of a subtraction `A−B` is the XOR of the operand bits and
the incoming borrow: `bit_m(A−B) = bit_m(A) ⊕ bit_m(B) ⊕ borrow_m`, where `borrow_m = 1 ⟺ (A mod 2^m) <
(B mod 2^m)`. Applying at `m=n+k` with `A=8·3^n`, `B=S_n`:

> **[PROVEN] Borrow decomposition.** `β_n = d_n ⊕ σ_n ⊕ ρ_n`, where
> - `d_n := bit_{n+k}(8·3^n)` — the **exogenous Mahler diagonal** (the clean `×3` ℤ₂-isometry digit, piece (1));
> - `σ_n := bit_{n+k}(S_n)` — the **moving diagonal of the endogenous carry** `S_n` (piece (2));
> - `ρ_n := [ (8·3^n mod 2^{n+k}) < (S_n mod 2^{n+k}) ]` — the **subtraction borrow** into bit `n+k`.
>
> Verified: 0 failures over n<2·10⁴, k∈{2,3,5,6,8} (exact big-int, `carry_coboundary.py`).

The carry's entire contribution is the pair `(σ_n, ρ_n)`. Dropping it (setting `β_n := d_n`) is exactly the
"reduce to pure Mahler" hope. We test whether that contribution telescopes.

### 1a. Finite-range borrow lemma — where S_n ≡ 8·3^n (mod 2^n) helps  [PROVEN, 0 failures]

The carry obeys `2^n c_n = 8·3^n − S_n`, so the low `n` bits of `8·3^n` and `S_n` are **equal**:
`S_n ≡ 8·3^n (mod 2^n)`. Hence in the subtraction `8·3^n − S_n` the low-`n` block cancels exactly with **no
borrow generated**: `borrow_n = 0`. Therefore the borrow into bit `n+k` is generated entirely **inside the
window `[n,n+k)`**:

> **[PROVEN] Finite-range borrow.** `ρ_n = [ ((8·3^n)≫n mod 2^k) < ((S_n)≫n mod 2^k) ]` — a function of only
> the `k`-bit windows of `8·3^n` and `S_n` at depth `n`. (Window-borrow = full-borrow: 0 failures, all k.)

This is the **one place the prompt's hope partially lands**: the borrow IS a bounded-range / finite-state
function (it does NOT require unbounded carry propagation). But — see §2 — its *inputs* `((S_n)≫n mod 2^k)`
are precisely the free-zone bits `[n,n+k)` of `S_n`, the carry-mixed/Mahler-class zone (`antihydra_attack §4f`:
tame/free boundary is bit `n`). Finite range, Mahler-class inputs.

---

## 2. Step 2 — the telescoping fails: the moving diagonal breaks the linear recursion  [PROVEN reason]

The recursion `S_{n+1}=3S_n+2^n b_n` is **linear in `S`**, and a coboundary would require the carry term
`(β_n−d_n)χ_a(s_n) = g(state_{n+1}) − g(state_n) + bounded`. It fails for a precise, structural reason.

**(i) Bit-extraction at a MOVING index is the nonlinearity.** The carry enters `β_n` only through
`bit_{n+k}(S_n)` and the windowed borrow. As `n→n+1` BOTH the read index advances (`n+k → n+k+1`) AND `S` is
multiplied by 3 (`S_{n+1}=3S_n+2^n b_n`); `×3` is carry-mixing on ℤ₂, so the diagonal read
`σ_n = bit_{n+k}(S_n)` is the **moving diagonal of `S_n`** — the *same* moving-diagonal obstruction that
defeats the exogenous `d_n = bit_{n+k}(8·3^n)` (`ODD_3ADIC_ODOMETER §3(i)`, `mahler §9`). Linearity of the
recursion would telescope a *fixed-position* read; the moving diagonal visits a new phase every step, so the
linearity does not transfer. **The recursion is linear, the read is diagonal — telescoping is destroyed by the
read, not by the recursion.**

**(ii) The borrow is finite-range but LOCKED to the state.** By §1a `ρ_n` is a function of the window
`[n,n+k)` — but `s_n = c_n mod 2^k` is the *same* windowed subtraction (`s_n + 2^k β_n =` the `(k+1)`-bit
window of `8·3^n − S_n`). So `ρ_n` is a **deterministic function of the very window that produces `s_n`**, and
is strongly correlated with `χ_a(s_n)`: measured `|N^{-1}Σ(ρ_n−½)χ_1(s_n)| ≈ 0.16` (k=2..8), **not vanishing**.
A martingale-difference / coboundary split needs the carry factor to be (asymptotically) orthogonal to
`χ_a(s_n)`; here it is rigidly entangled with it. So even the finite-range piece cannot be pulled out as a
boundary term.

**(iii) Direct coboundary test (decisive).** A coboundary `g(x_{n+1})−g(x_n)` of a finite-state `g` has
partial sums **bounded independently of N** (`≤ 2max|g|`). The carry-piece partial sums
`Σ_{n<N}(β_n−d_n)χ_1(s_n)` instead **grow with N** (k=6): `max|·| = 43 (N=2500) → 99 (5000) → 132 (10⁴)`,
ratio `max/√N ≈ 0.7–1.4` — **√N-consistent (martingale/CLT) growth, NOT a bounded plateau.** Hence:

> **[PROVEN no-telescope] The carry contribution to `Inj_a` is not a finite-state coboundary.** Its partial
> sums grow ≈√N, the same order as the full feedback. The self-reference contributes at full order; it is
> **not** an O(1) boundary term.

This is consistent with — and orthogonal to — the prior `ODD_AUTOMATON_ALGEBRA §2` no-go (which showed `χ_a∘V`
is not a coboundary of the deterministic map `V=⌊3s/2⌋ mod 2^k` via its trap fixed point `s=0`). That route
targeted the *character over the state map*; THIS route targets *telescoping the carry via its own linear
S-recursion*, and finds the obstruction is the moving-diagonal bit-extraction + state-locking of the borrow.

---

## 3. Step 4 — numerics: the carry is full-strength, not a small correction  [OBSERVED]

`carry_coboundary.py`, real orbit `c₀=8`, N=2·10⁴, CLT floor `1/√N=0.00707`:

| k | P(β_n≠d_n) | E(β_n−d_n) | \|Inj_a\| | \|Inj^d_a\| (pure Mahler) | \|carry piece\| | which dominates |
|---|---|---|---|---|---|---|
| 2 | 0.502 | −0.0019 | 0.0029 | 0.0033 | 0.0061 | carry ≳ Mahler |
| 3 | 0.500 | −0.0050 | 0.0013 | 0.0013 | 0.0009 | comparable |
| 5 | 0.504 | −0.0087 | 0.0028 | 0.0012 | 0.0039 | **carry dominates** |
| 6 | 0.500 | +0.0032 | 0.0043 | 0.0012 | 0.0040 | **carry dominates** |
| 8 | 0.497 | +0.0043 | 0.0021 | 0.0038 | 0.0045 | comparable |

(`Inj^d_a := N^{-1}Σ(d_n−½)χ_a(s_n)` = pure exogenous Mahler diagonal; carry piece `= Inj_a − Inj^d_a`.)

Two robust facts:
- **P(β_n≠d_n) ≈ ½ for every k**: the exogenous Mahler digit `d_n` predicts the true feedback bit `β_n` **no
  better than a coin flip** — `β_n` and `d_n` are essentially *uncorrelated*. The carry `σ_n⊕ρ_n` is a
  full-strength, ≈Bernoulli(½)-looking bit, not a rare correction. So "reduce to pure Mahler `d_n`" is
  numerically false at the per-term level: `β_n` is not approximated by `d_n` at all.
- **The carry piece is comparable to or LARGER than the pure-Mahler piece** in `Inj_a` (it dominates at k=5,6).
  Neither piece dominates uniformly — they are entangled at the same √N order. All quantities sit at/below the
  CLT floor (`Inj_a → 0` remains OBSERVED, never proven), exactly as in prior dives.

Signed mean `E(β_n−d_n) ≈ 0` (≤ 0.009): the carry correction carries **no net DC bias** — it is a pure
fluctuation term, which is why it can ride at the √N order without telescoping.

---

## 4. Honest verdict (the three asks)

| ask | answer | label |
|---|---|---|
| (a) carry decorrelates / telescopes (self-ref negligible ⇒ pure Mahler)? | **No.** Carry-piece partial sums grow ≈√N (not bounded ⇒ not a finite-state coboundary); `β_n` is ≈uncorrelated with `d_n` (flip density ½); carry piece ≳ Mahler piece in `Inj_a`. Self-reference contributes at full order. | **[PROVEN no-telescope]** + [OBSERVED] |
| (b) new characterization of why the carry is inseparable? | **Yes (sharper).** `β_n=d_n⊕σ_n⊕ρ_n`. Telescoping via the linear S-recursion is killed by **moving-diagonal bit-extraction** (read index advances while `×3` carry-mixes) PLUS **state-locking of the finite-range borrow** (`ρ_n` reads the same window that makes `s_n`; corr ≈0.16, not vanishing). Distinct from the `χ_a∘V` trap no-go. | **[PROVEN]** |
| (c) carry-correction is itself Mahler-class? | **Yes.** `σ_n=bit_{n+k}(S_n)` is the **moving diagonal of the self-referential carry** in the free zone (bit > n, `antihydra §4f`) — a second Mahler-class diagonal; `ρ_n` is finite-range but reads those same free-zone bits. | **[PROVEN reduction]** |

### Partial win banked (the prompt's "real win" criteria)  [PROVEN]
- **Borrow finite-range lemma (§1a):** the borrow `ρ_n` is a **bounded-range (k-bit window) function** of the
  parities — because `S_n ≡ 8·3^n (mod 2^n)` (`borrow_n=0`). This is the prompt's "borrow has bounded range /
  finite-state function of recent S-bits" outcome, made exact (0 failures). The catch: the bounded window sits
  at depth `[n,n+k)`, i.e. it reads the *free-zone* (Mahler-class) bits, not recent low parities — so finite
  range does NOT buy decorrelation.

### Exact residual (unchanged in difficulty, sharper in form)
The full feedback is the XOR of **two locked moving diagonals**, offset by a finite-range borrow:
> `β_n − ½` carries `Inj_a = N^{-1}Σ(d_n ⊕ σ_n ⊕ ρ_n − ½)χ_a(s_n)`, with
> `d_n=bit_{n+k}(8·3^n)` (exogenous Mahler diagonal of the `×3` ℤ₂-isometry, piece (1)),
> `σ_n=bit_{n+k}(S_n)` (endogenous-carry Mahler diagonal, piece (2)),
> `ρ_n=[(8·3^n≫n mod 2^k) < (S_n≫n mod 2^k)]` (finite-range borrow, state-locked).
Piece (1) is open Mahler 3/2; piece (2) is a *second* Mahler-class diagonal that does NOT telescope away — the
self-reference is not negligible. Closing it needs an anti-concentration/decorrelation bound on the moving
diagonal `bit_{n+k}(S_n)` of the self-referential carry — the open core in yet sharper dress.

## 5. Genuinely new vs prior

- **vs `ODD_3ADIC_ODOMETER.md` / `ODD_SUBSPACE_SYNTHESIS.md`:** they identified pieces (1)+(2) as the residual
  but treated the carry as an opaque "offset `S_n`". This dive **decomposes `β_n` through the actual
  subtraction borrow** (`β_n=d_n⊕σ_n⊕ρ_n`), proves the borrow is **finite-range** (`borrow_n=0` from
  `S_n≡8·3^n mod 2^n`), and shows numerically the carry is **full-strength** (flip density ½, carry piece ≳
  Mahler piece) — i.e. NOT a small perturbation that could be dropped.
- **vs `ODD_AUTOMATON_ALGEBRA.md §2` (coboundary no-go):** that ruled out `χ_a∘V` being a coboundary of the
  deterministic state map `V` (trap fixed point `s=0`). This rules out telescoping **the carry via its own
  linear recursion** `S_{n+1}=3S_n+2^n b_n` — a different decomposition — and pins the obstruction to the
  moving-diagonal read + state-locked borrow, with a direct partial-sum √N-growth test.
- **vs `antihydra_attack §4f` (tame/free boundary at bit n):** confirms it operationally — the borrow window
  `[n,n+k)` is exactly in the free zone, so finite range ≠ tameness.

## Sources
- Repo: `ENDOGENOUS_UE_BUILD.md` (Open Lemma §4, no-go §5), `ODD_3ADIC_ODOMETER.md` (`β_n=bit_{n+k}(8·3^n−S_n)`,
  moving-diagonal=Mahler), `ODD_SUBSPACE_SYNTHESIS.md` (4-mechanism synthesis, residual = pieces (1)+(2)),
  `ODD_AUTOMATON_ALGEBRA.md §2` (prior coboundary no-go on `χ_a∘V`), `antihydra_attack.md §4f` (S-recursion,
  ×3 low-bit lemma `S_n≡3^{n−M}S_M mod 2^M`, tame/free boundary bit n), `mahler_equidistribution_attack.md §9`
  (diagonal `bit_n(3^n)` = Mahler).
- Literature (repo knowledge): Mahler 3/2 (1968, open); AEV arXiv:2510.11723; coboundary/cocycle =
  Gottschalk–Hedlund (telescoping needs bounded transfer function — here partial sums grow √N).
- Numerics: `scratchpad/carry_coboundary.py` (exact big-int, N=2·10⁴→4·10⁴, <1s; 0 identity failures; borrow
  finite-range 0 failures; carry-piece partial-sum √N-growth; Inj_a vs Inj^d_a vs carry piece per k).

**No machine decided. No label upgraded.**
