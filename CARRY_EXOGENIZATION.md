# Carry exogenization / separation — which piece carries Inj_a, the exogenous Mahler digit or the self-referential carry? (2026-06-29)

*Assigned task: SPLIT the Open-Lemma feedback bit `β_n = bit_{n+k}(8·3ⁿ − S_n)` into the EXOGENOUS Mahler
diagonal digit `d_n = bit_{n+k}(8·3ⁿ)` and the borrow/carry correction `r_n`, split `Inj_a` accordingly, and
determine empirically + structurally whether the obstruction lives in the exogenous digit `d_n` or in the
self-referential carry `S_n`. Decisive experiments: (1) which part dominates `Inj_a`; (2) non-circularity — is
`d_n` ALONE already Mahler-correlated with the orbit-defined low state; (3) random-carry annealed control.
Numerics `/Users/aokiyousuke/quantum-ecc/.venv/bin/python scratchpad/carry_exo{,2,3}.py`, exact big-int orbit,
N=10⁵, FFT-free per-character sums, ≈40–55s. Every claim labelled. Zero false proofs. NOT committed.*

---

## 0. One-line verdict

**(c) BOTH pieces are individually Mahler-class and the difficulty is inseparable — BUT with a clean, genuinely
new OBSERVED refinement that the program had not measured: the self-referential carry is
ANNEALED-INDISTINGUISHABLE.** An exact iid-fair-bit random carry reproduces the *entire* odd-character energy
of `Inj_a` — both the carry-part magnitude AND the total — to within seed scatter, so the carry contributes
*net ≈ 0* to `Inj_a` and what remains is `Inj_a ≈ Inj_a^{exo}`, the correlation of the EXOGENOUS Mahler diagonal
`d_n = bit_{n+k}(8·3ⁿ)` with the orbit-defined low-state character. The self-reference (`S_n`) is therefore
**not** the carrier of the obstruction; the live, undecided content is the exogenous Mahler-3/2 digit. This is
**not a reduction in difficulty** — `Inj_a^{exo}` is itself Mahler/AEV (its phase `U(s_n,0)` is orbit-defined,
the non-circularity caveat) and remains OBSERVED, not proven (the all-zeros adversary of the §5 no-go still
breaks it). The prize "carry decorrelates ⇒ pure exogenous Mahler" is realised **at the level of localisation**
(carry = annealed noise; `d_n` = obstruction) but the residual is still open. **No machine decided. No label
upgraded.**

---

## 1. The exact split  `[PROVEN]`

From the banked rewrite (`ODD_3ADIC_ODOMETER.md §1`): `2ⁿc_n + S_n = 8·3ⁿ`,
`S_n = Σ_{j<n} 3^{n−1−j} 2^j b_j`, `b_j = c_j mod 2`, hence `β_n = bit_k(c_n) = bit_{n+k}(8·3ⁿ − S_n)`.

> **Exogenization.** `d_n := bit_{n+k}(8·3ⁿ)` (the EXOGENOUS Mahler diagonal digit — a function of `n,k` only,
> independent of the orbit); `r_n := d_n ⊕ β_n` (the carry/borrow correction induced by subtracting `S_n`).
> Then `β_n = d_n ⊕ r_n`, and algebraically `(β_n − ½) = (d_n − ½) + (1 − 2d_n)·r_n`.

This splits the Open-Lemma sum **exactly** (verified additive to `<1e−9`):

> `Inj_a = Inj_a^{exo} + Inj_a^{carry}`,
> `Inj_a^{exo}(N)   = (1/N) Σ_{n<N} (d_n − ½)·χ_a(U(s_n,0))`  — pure exogenous Mahler digit,
> `Inj_a^{carry}(N) = (1/N) Σ_{n<N} (1 − 2d_n)·r_n·χ_a(U(s_n,0))`  — the borrow correction,
> with `U(s,0)=⌊3s/2⌋ mod 2^k`, `χ_a(x)=e(ax/2^k)`, `a` odd.

**[PROVEN, machine]** The identity `β_n = bit_{n+k}(8·3ⁿ − S_n)` holds with **0 failures**, N=10⁵, k∈{4,6,8,10}
(big-int). The split is honest: `d_n` is genuinely exogenous, `r_n` carries 100% of the orbit's self-reference.

**The carry correction is DENSE, not sparse.** `P(r_n = 1) = 0.499–0.501` for all k (k=4,6,8,10) — subtracting
`S_n` flips bit `n+k` about half the time (`S_n` is up to ~⅛ of `8·3ⁿ`, comparable bit-length, so the borrow
at the mid-low window `n+k` is fully mixed). So `r_n` is **not** a small perturbation of `d_n`; it is a balanced
bit in its own right. Likewise `P(d_n=1)=0.498–0.504`, `P(β_n=1)=0.499–0.503` — all three balanced. `[OBSERVED]`

---

## 2. Which piece carries Inj_a — odd-character energy split  `[OBSERVED]`

`E^X(k) := (1/#{a odd}) Σ_{a odd} |Inj_a^X|²`, the odd-character L² energy of part `X`. Random
(square-root-cancellation) law: `E ~ const/N`, so we report `E·N` (the multiple of the random floor).
`carry_exo2.py`, N=10⁵:

| k | `E_tot·N` | `E_exo·N` | `E_carry·N` | cross `2Re⟨exo,carry⟩·N` |
|---|---|---|---|---|
| 6  | 0.26 | 0.19 | 0.46 | −0.38 |
| 8  | 0.26 | 0.21 | 0.56 | −0.52 |
| 10 | 0.25 | 0.21 | 0.45 | −0.41 |

All parts ride the random `O(1/N)` floor (full √-cancellation; the per-`(k,a)` running averages track `1/√n`
through N=10⁵, `carry_exo2.py` decay table). **Neither piece dominates:** `E_exo` and `E_carry` are comparable
(within a factor ≈2). The carry part has the larger self-energy (0.45–0.56), but it is almost exactly cancelled
by a **negative cross-term** (−0.38…−0.52) with the exogenous part, so the **net carry contribution to
`Inj_a` is ≈ 0** (`E_carry + cross ≈ 0.05`), leaving `E_tot ≈ E_exo` (0.25 vs 0.21). I.e. up to a near-cancelling
carry, **`Inj_a ≈ Inj_a^{exo}`** — the exogenous Mahler digit carries the surviving signal.

---

## 3. Non-circularity test — `d_n` ALONE is already Mahler-correlated  `[OBSERVED]`

`Inj_a^{exo} = (1/N)Σ(d_n − ½)χ_a(U(s_n,0))` sits at `E_exo·N ≈ 0.19–0.21` — **nonzero at the Mahler/random
floor**, equidistributed only numerically. Critically, this is **NOT a clean exogenous AEV statement**: `d_n` is
exogenous, but the phase `U(s_n,0)` is built from `s_n = c_n mod 2^k`, which is **orbit-defined**. So
`Inj_a^{exo}` is the correlation of the Mahler diagonal `bit_{n+k}(8·3ⁿ)` with the orbit's own low state — a
self-orbit Mahler-3/2 correlation, exactly the open core (`ODD_3ADIC_ODOMETER §3`, `mahler §9`). **Even the
"exogenous" piece is Mahler.** This is the decisive non-circularity finding: the obstruction is present already
in the exogenous digit `d_n`; the self-reference does not manufacture it.

---

## 4. Random-carry annealed control — the carry is annealed-indistinguishable  `[OBSERVED]`

Replace the real low bits `b_j = c_j mod 2` by iid fair bits to form a surrogate carry
`S_n^{rand} = Σ 3^{n−1−j}2^j b_j^{rand}`, set `r_n^{rand} = d_n ⊕ bit_{n+k}(8·3ⁿ − S_n^{rand})` and the
surrogate feedback `β_n' = d_n ⊕ r_n^{rand}`, **keeping the real `d_n` and real phase `U(s_n,0)`**. This is the
carry analogue of the §5 no-go's adversary test (here a *typical* random input, not adversarial). 12 seeds,
N=10⁵, `carry_exo3.py`:

| k | `E_carry·N` real | `E_carry·N` RAND (mean±std) | `E_tot·N` real | `E_tot·N` RAND (mean±std) |
|---|---|---|---|---|
| 6  | 0.46 | 0.43 ± 0.08 | 0.26 | 0.24 ± 0.05 |
| 8  | 0.56 | 0.46 ± 0.05 | 0.26 | 0.24 ± 0.04 |
| 10 | 0.45 | 0.46 ± 0.03 | 0.25 | 0.25 ± 0.01 |

**The random carry reproduces the carry-part energy AND the total energy to within seed scatter** (every real
value within ≈1–2σ of the random mean, and at k=10 essentially exact). The anti-correlation cross-term of §2 is
therefore **not** a self-referential effect — it is a structural consequence of the XOR split (because
`r = d ⊕ β`, the `(1−2d)r` part is automatically anti-correlated with the `(d−½)` part for *any* `β`), and a
random carry produces it identically. Bit-level: `corr(d_n, r_n) = corr(d_n, r_n^{rand}) ≈ 0` (all `|·|<0.006`,
at the `1/√N` floor). **Conclusion:** the real self-referential carry contributes nothing to `Inj_a`'s
odd-character spectrum distinguishable from a fresh iid carry. The carry is annealed-like — it decorrelates.

This is the `Inj_a`-localised, direct confirmation of `QUENCHED_ANNEALED_SEAM.md`: the self-feeding determinism
leaves **no finite-order signature**, now measured on the carry component of the actual Open-Lemma object.

---

## 5. Honest verdict (the three asks)

| ask | answer | label |
|---|---|---|
| **(a) clean separation — carry decorrelates ⇒ pure exogenous Mahler?** | **Partially — at the level of localisation, not difficulty.** The carry IS annealed-indistinguishable (§4: random carry reproduces the full `Inj_a` odd-energy), so the live obstruction localises to the exogenous Mahler digit `Inj_a^{exo}`. But this lowers nothing: `Inj_a^{exo}` is itself Mahler-3/2 (its phase is orbit-defined, §3), still OBSERVED-not-proven, and the all-zeros adversary of the §5 no-go still drives `|Inj|≈1`. | `[OBSERVED]` |
| **(b) carry essential / new characterization?** | **NO, the carry is not essential.** Its net contribution to `Inj_a` is ≈0 (self-energy cancelled by an algebraic cross-term reproduced by a random carry, §2,§4). New OBSERVED characterization: `Inj_a ≈ Inj_a^{exo}` up to annealed-carry noise. | `[OBSERVED]` |
| **(c) both Mahler, inseparable?** | **YES — this is the accurate verdict.** Both `Inj_a^{exo}` and `Inj_a^{carry}` ride the same √-floor; dropping the (annealed) carry leaves the exogenous Mahler correlation at the same floor. The difficulty does not separate into an easy piece + a hard piece; it is the single exogenous Mahler-diagonal correlation read against the orbit's own phase. | `[OBSERVED] reduction `=`(K)` |

**Exact residual gap.** After removing the annealed carry, the sole undecided object is the **exogenous
Mahler-diagonal correlation**
`Inj_a^{exo}(N) = (1/N) Σ_{n<N} (bit_{n+k}(8·3ⁿ) − ½)·χ_a(⌊3(c_n mod 2^k)/2⌋ mod 2^k) ⟶ 0`  (a odd),
i.e. the digit `bit_{n+k}(8·3ⁿ)` of the `×3` `ℤ₂`-isometry must decorrelate from the orbit-defined low-state
character. This **is** Mahler 3/2 / AEV 2510.11723 — `OBSERVED` at `E_exo·N ≈ 0.2` (√-floor), `OPEN`. The carry
no longer appears.

---

## 6. Genuinely new vs prior

- **vs `ODD_3ADIC_ODOMETER.md` / `ODD_SUBSPACE_SYNTHESIS.md`** (which named the split "moving diagonal `d_n`
  minus carry `S_n`" and stated the residual as TWO locked pieces: (1) equidistribute `bit_{n+k}(8·3ⁿ)` and
  (2) decorrelate the carry `S_n`): **this note RUNS the separation those notes only named.** It shows the two
  pieces are NOT two independent obstructions of comparable difficulty — piece (2), the carry, is OBSERVED to be
  **annealed-indistinguishable** (an iid random carry reproduces the entire `Inj_a` odd-energy, §4), with net
  contribution ≈0; the obstruction is **entirely** piece (1), the exogenous Mahler diagonal. A clean (observed)
  collapse from a two-piece residual to one.
- **vs `ENDOGENOUS_UE_BUILD.md §5` (no-go: self-reference irreducible to `(gap, γ)`)**: consistent and
  complementary. The no-go's adversary used the all-zeros input `β≡0` (atypical) to realise `|Inj|≈1`; this note
  shows the *typical* random carry decorrelates, which is exactly why no `(gap,γ)`-uniform bound can exist
  (typical decorrelates, adversarial does not) — and it relocates the irreducible content from the carry to the
  exogenous Mahler digit.
- **vs `QUENCHED_ANNEALED_SEAM.md`** (no finite-order signature distinguishes quenched from annealed): here that
  is measured **directly on the carry component of `Inj_a`** via the exact `d_n/r_n` exogenization — a sharper,
  object-specific instance than the generic lag-MI/entropy tests.
- **vs `ODD_ADDITIVE_ENERGY.md`** (odd 2nd moment `M₂^{odd}=o(2^k)` is the wall): the present split says that
  wall's *carrier* is the exogenous Mahler digit, not the self-referential carry — `M₂^{odd}` is, up to annealed
  carry noise, the energy of `(d_n−½)` against the orbit phase.

## Sources
- Repo: `ODD_3ADIC_ODOMETER.md` (§1 rewrite `β_n=bit_{n+k}(8·3ⁿ−S_n)`, §2 fixed-position periodicity, §3
  diagonal=Mahler), `ENDOGENOUS_UE_BUILD.md` (§4 Open Lemma, §5 no-go + C5 adversary), `ODD_SUBSPACE_SYNTHESIS.md`
  (two-locked-pieces residual), `ODD_ADDITIVE_ENERGY.md` (`M₂^{odd}` wall), `QUENCHED_ANNEALED_SEAM.md`
  (no finite-order signature), `mahler_equidistribution_attack.md §9` (diagonal bit = Mahler).
- Literature (repo knowledge): Mahler 3/2 (1968, open); AEV (Andrieu–Eliahou–Vivion arXiv:2510.11723, Conj 1.6);
  Furstenberg ×2,×3; quenched-vs-annealed disorder (the carry control is the annealed surrogate).
- Numerics: `scratchpad/carry_exo.py` (per-`(k,a)` split + density + single-seed control, N=6·10⁴, identity 0
  failures), `carry_exo2.py` (odd-energy split + 12-seed control + √-decay, N=10⁵), `carry_exo3.py` (decisive
  total-energy random-carry control + cross-term, N=10⁵). Exact big-int orbit, every identity machine-verified.

**No machine decided. No label upgraded.**
