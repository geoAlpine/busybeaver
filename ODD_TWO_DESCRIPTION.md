# The two-description constraint on the odd block — does the closed form over-determine the kernel? (2026-06-29)

*Assigned: take the kernel's Open Lemma (`ENDOGENOUS_UE_BUILD.md` §4) — for odd `a`,
`Inj_a(N)=(1/N)Σ(β_n−½)χ_a(U(s_n,0))→0` — and test whether the orbit's SECOND, independent description (the
closed form `2ⁿc_n = 8·3ⁿ − S_n`) combines with the recursive seam identity to produce a genuinely new
constraint that pins/over-determines `π_N(χ_a)` for odd `a`, or whether the two descriptions collapse to the
same equation = the moving middle digit = Mahler 3/2. SOUNDNESS PARAMOUNT; every claim labelled; exact big-int.
Numerics `scratchpad/odd_two_desc.py`, all identities machine-verified. Not committed.*

---

## 0. One-line verdict

**Outcome = (c): the two descriptions are NOT independent on the odd block — they collapse to the same
equation, which is the moving-middle-digit / Mahler-3/2 object.** The collapse has a *precise, new algebraic
reason*: the closed form is "closed" (tame, parity-blind, periodic `×3`) **only at depth `≤ k+1`**, a bit-window
strictly **below** the kernel's window `[n, n+k]`; producing any statement about `β_n=bit_k(c_n)` forces the
closed form up to depth `n+k+1`, where `S_n` is built bit-by-bit from the *entire parity history* — i.e. exactly
the self-reference the seam identity already carries. **No second independent equation; no over-determination.**
By-product (the genuinely new piece): an exact **Mahler × self-ref-carry split** of the odd-character average
(C5 below), and a clean **duality** — the closed-form congruence annihilates the self-reference *in the same way*
`L_ann` annihilates the odd characters. The kernel is untouched and remains **[OPEN]**.

---

## 1. Setup — the two descriptions of the same `c_n`

Orbit `c₀=8`, `c_{n+1}=⌊3c_n/2⌋`; `s_n=c_n mod 2^k`, `β_n=bit_k(c_n)`, `U(s,0)=⌊3s/2⌋ mod 2^k`.

- **Recursive (automaton / self-referential) description** [PROVEN, `ENDOGENOUS_UE_BUILD` §2.3]:
  for odd `a`, `π_N(χ_a)=Feedback_N(χ_a)+O(1/N)`, `Feedback_N(χ_a)=−2(1/N)Σ(β_n−½)χ_a(U(s_n,0))`.
- **Closed-form description** [PROVEN, `antihydra_attack` §4c, re-verified here]:
  `2ⁿc_n = 8·3ⁿ − S_n`, `S_{n+1}=3S_n+2ⁿ[c_n odd]`, `S_0=0`.   (C1 below; verified `n=0..2000`, `k∈{4,6,8}`)

The question: do these two *genuinely different* descriptions yield a second, non-circular equation for the odd
block, or the same one?

---

## 2. What the closed form says at the kernel scale  [PROVEN — exact, big-int verified]

Write `X_n := 8·3ⁿ − S_n = 2ⁿc_n`. The low `k+1` bits of `c_n` (= `s_n` and `β_n`) sit in the bit-window
`[n, n+k]` of `X_n`:

> **(C2) bit-window reconstruction [PROVEN, verified `n=0..2000`].**
> `s_n = (X_n ≫ n) ∧ (2^k−1)` (bits `[n, n+k)`),  `β_n = bit_{n+k}(X_n)`. Matches the raw orbit exactly.

Now take the closed form mod `2^{k+1}`. For **`n ≥ k+1`**, `2ⁿc_n ≡ 0 (mod 2^{k+1})`, hence the exact congruence:

> **(C3) closed-form congruence at depth `k+1` [PROVEN, verified `n=0..2000`, `k∈{4,6,8}`].**
> For `n ≥ k+1`:  **`S_n ≡ 8·3ⁿ (mod 2^{k+1})`.**

This is the `×3` low-bit lemma (`antihydra_attack` §4f) in seam dress: the low `k+1` bits of `S_n` are *tame* —
an explicit `×3`-orbit, periodic in `n` with period `ord(3 mod 2^{k+1}) = 2^{k−1}`. Its differential form:

> **(C4) parity-blindness of the tame congruence [PROVEN, verified].**
> For `n ≥ k+1`:  `S_{n+1} ≡ 3·S_n (mod 2^{k+1})`, **independent of the parity bit `p_n=[c_n odd]`** — because
> the only place `p_n` enters `S` is the term `2ⁿp_n`, which has `v₂ = n ≥ k+1`, i.e. **zero coefficient at
> depth `k+1`.**

**This is the decisive structural fact.** The clean, closed part of the closed-form description (depth `≤ k+1`)
is **blind to the self-reference** (the parity / fresh bit). This is the *exact algebraic dual* of the spectral
no-go (`ENDOGENOUS_UE_BUILD` §2.2, C2): `L_ann` annihilates every **odd character** (the carrier of the
conclusion); the closed-form congruence annihilates the **parity bit** (the carrier of the conclusion). The two
"blindnesses" coincide on the same object. The closed form gives a free, exact handle precisely where the
kernel content is **absent**, and goes silent precisely where the kernel content lives.

---

## 3. Where the kernel content actually sits — and why the descriptions collapse  [PROVEN reduction]

The kernel needs `β_n = bit_{n+k}(X_n)` and the character `χ_a(s_n)` with `s_n` = bits `[n, n+k)` of `X_n`. By
(C2) these live at bit-position `≈ n` — the **moving middle digits** of `X_n = 8·3ⁿ − S_n`. The tame congruence
(C3) lives at bit-positions `[0, k]`. For `n > k` these windows are **disjoint**: the closed form's *closed*
content and the kernel's content never overlap.

To make the closed form say anything about `β_n` one must read it to depth `n+k+1`, i.e. one needs
`S_n mod 2^{n+k+1}`. But the top bits of that — positions `[k+1, n+k]` — are built term-by-term from
`Σ_{i<n} 2^i·3^{n−1−i}·p_i`, the **carry-sum of the entire parity history `p_0,…,p_{n−1}`** (the §4f
"tame/free boundary is exactly bit `n`"). That history is exactly the self-reference the seam identity already
encodes through `β`. Hence:

> **(C-collapse) [PROVEN].** The closed-form "second description" of `β_n` is
> `β_n = bit_{n+k}(8·3ⁿ) ⊕ (carry from S_n at bit n+k)` = **the moving middle digit of `3ⁿ` corrected by a
> self-referential carry.** It is *not* an independent equation: substituting `S_n = 8·3ⁿ − 2ⁿc_n` returns the
> identity `χ_a(s_n) = χ_a(s_n)`. The two descriptions are the same object split at bit `n`; combining them does
> **not** over-determine `π_N(χ_a)`.

---

## 4. The genuinely new by-product — exact Mahler × carry split  [PROVEN — exact, verified to 1e-15]

Because `c_n/2^k = (8·3ⁿ − S_n)/2^{n+k}`, the odd-character average factors **exactly**:

> **(C5) [PROVEN, termwise `|M_n·C_n − χ_a(s_n)| ≤ 3e-15`, `N=2·10⁴`, `k∈{4,6,8}`, `a∈{1,3}`].**
> `π_N(χ_a) = (1/N) Σ_{n<N} M_n·C_n`,  where
> `M_n = exp(2πi·a·8·3ⁿ / 2^{n+k})` — the **Mahler/Weyl factor** for `(3/2)ⁿ` (frequency `a/2^{k−3}`), and
> `C_n = exp(−2πi·a·S_n / 2^{n+k})` — the **self-referential carry twist**.

This writes the kernel average as an *open Mahler exponential sum twisted by the orbit's own carry*. Crucially
**neither factor alone is the answer, and each is itself a Mahler-class (open) quantity** — the split does not
isolate a computable piece:

```
 k a   |π_N(χ_a)| true   |Mahler sum alone|   |carry sum alone|     (CLT floor 1/√N = 0.00707, N=2e4)
 4 1      0.00213            0.00859              0.00181
 4 3      0.00802            0.00783              0.00506
 6 1      0.00720            0.01291              0.00257
 6 3      0.00340            0.00966              0.01154
 8 1      0.00126            0.00172              0.00483
 8 3      0.00646            0.00485              0.00419
```

All three columns hover at the CLT floor: the true sum, the naked Mahler sum, and the naked carry sum are each
`O(1/√N)`-small but **none is forced to vanish** by the split. The Mahler factor `M_n` decaying in average **is**
the equidistribution of `(3/2)ⁿ` mod `2^{k−3}` — Mahler's 3/2 problem. So (C5) confirms, at the character level,
that the closed-form description's free part **is literally the Mahler sum**.

---

## 5. Honest verdict

- **(a) genuine extra constraint / partial?** Only at the tame depth: (C3)/(C4) are exact and unconditional, but
  they are **parity-blind**, hence give **zero** information on `Inj_a(N)` (odd block) — by the exact duality with
  the spectral no-go. No one-sided bound, no specific-`a` win emerges; the closed form's *closed* part and the
  kernel's content are at disjoint bit-windows. **No partial on the odd block.**
- **(b) over-determination?** **No.** The seam identity and the closed form are two cuts of the *same* number
  `c_n` (recursive vs. `8·3ⁿ−S_n`); on the odd block they reduce to `χ_a(s_n)=χ_a(s_n)` (C-collapse). There is
  no second independent equation, so nothing is pinned.
- **(c) re-introduces Mahler?** **Yes — this is the outcome.** The closed form's description of `β_n`/`s_n` is the
  moving middle digit of `3ⁿ` plus a self-referential carry (C-collapse), and the exact split (C5) shows
  `π_N(χ_a)` = Mahler/Weyl sum × self-ref carry. **Precise reason for non-independence:** the closed form is
  closed (tame, `×3`, parity-blind) only below bit `k+1`; at the kernel's bit-window `≈ n` it requires
  `S_n mod 2^{n+k+1}`, whose high bits are the carry-sum of the full parity history = the same self-reference.
  The two descriptions therefore *share* the only nontrivial object — the moving middle digit — and cannot
  constrain each other.

**Net:** the two-description idea does not escape the self-reference. It re-derives the wall from a fresh
direction and pins *why*: the orbit's two descriptions are **complementary in bit-position** — closed-form-tame
below bit `n`, carry-mixed/free at bit `n` — so the seam (recursive) description and the closed form never meet
on the odd block, exactly as `L_ann`'s gap (even block) never meets the odd characters. The same dichotomy,
now visible arithmetically.

---

## 6. Genuinely new vs prior

- **New (framing):** the exact **Mahler × carry split** (C5) of the *odd-character empirical average* itself
  (prior §4f split bits of `S_n`; this splits `π_N(χ_a)` directly, tying the closed form to the seam identity's
  odd block). And the clean **duality statement**: closed-form congruence ⊥ parity-bit  ⇔  `L_ann` ⊥ odd
  characters (the same conclusion-carrier annihilated by both available "free" structures). The bit-position
  complementarity of the two descriptions (tame `<n` vs free `≈n`) is stated here as the reason the
  two-description route cannot over-determine.
- **Not new (conclusion):** (C3)/(C4) = the §4f `×3` low-bit lemma + parity-blindness; the collapse onto the
  moving middle digit = the established Mahler wall (`antihydra_attack` §4c/§4f, `ENDOGENOUS_UE_BUILD` §4–§5).
  No new theorem about the orbit; no label upgraded.

## 7. Exact residual gap

Unchanged: the Open Lemma `Inj_a(N)→0` for odd `a`. By (C5) this is now equivalently the decay of
`(1/N)Σ_n exp(2πi·a·(3/2)ⁿ/2^{k−3})·exp(−2πi·a·S_n/2^{n+k})` — a Mahler/Weyl sum for `(3/2)ⁿ` twisted by the
self-referential carry `S_n`. The carry's relevant bits (positions `[k+1, n+k)`) are precisely the
carry-mixed/free zone, requiring the full parity history — no finite handle. The residual is exactly the
equidistribution of the moving middle digit of `3ⁿ` = Mahler 3/2.

---

## Sources

- `ENDOGENOUS_UE_BUILD.md` §2–§5 (seam identity, odd/even block, spectral no-go, Open Lemma).
- `antihydra_attack.md` §4c (`2ⁿc_n=8·3ⁿ−S_n`, the iterated-floor vs closed-form correction), §4f (`×3` low-bit
  lemma, tame/free boundary at bit `n`, `Ψ=3·id` circularity).
- `VALUATION_BUDGET.md`, `SEPARATION_BAKER.md` (independent confirmations the free zone is Mahler-class / Baker
  inapplicable at unbounded height).
- `COMPLETE_PROOF_CAPSTONE.md` §2 (reduction even-density ⇔ equidistribution mod `2^k`).
- Numerics: `scratchpad/odd_two_desc.py` — (C1)–(C4) exact big-int `n=0..2000`; (C5) split exact to `1e-15`,
  `N=2·10⁴`. Run with `/Users/aokiyousuke/quantum-ecc/.venv/bin/python`.

No machine decided. No label upgraded.
