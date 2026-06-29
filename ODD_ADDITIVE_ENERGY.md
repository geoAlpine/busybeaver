# Additive energy / moments restricted to the ODD-character sublattice (2026-06-29)

*Assigned non-spectral mechanism: additive energy / 2nd & 4th moments of the orbit's empirical measure
PROJECTED onto `V_odd` (odd characters only) — the subspace the no-go (`ENDOGENOUS_UE_BUILD.md` §2–5)
identifies as the sole carrier of the conclusion (the even block is slaved). Goal: is the odd-restricted
moment more tractable than the full energy? Numerics `/Users/aokiyousuke/quantum-ecc/.venv/bin/python`
(`scratchpad/odd_energy.py`, `scratchpad/odd_summary.py`): exact big-int orbit + numpy FFT, renewal
sequence `c'_j`, `J` up to `8·10⁴`, every Fourier/collision identity machine-verified. Every line labelled.
Zero false proofs. Not committed.*

---

## 0. One-line verdict

**Outcome = (b) a NEW exact characterization + (c) a clean reduction; NO unconditional partial (a).**
The odd restriction is the *right* object — it isolates 100 % of the obstruction into two exact, verified
identities — and it **improves the framing** over the full energy (it escapes the `ENERGY_ATTACK.md`
sign-blindness: a *one-sided magnitude* bound now suffices, and empirically holds with ~100× margin). But
the binding quantity is the **odd-restricted 2nd moment** `M₂ᵒᵈᵈ(k) = Σ_{a odd}|π̂_N(a)|²`, whose only free
inequality is `M₂ᵒᵈᵈ ≥ 0` (convexity); `M₂ᵒᵈᵈ(k) = o(2^k)` is **exactly** odd-restricted
equidistribution-in-mean = the Open Lemma (K)/Mahler-3/2. The odd restriction **relocates and sharpens the
wall; it does not lower it.** The advertised 4th-additive-energy route is *not* helped: the 4th energy is
dominated by the even block, the binding content sits at the 2nd moment, and the periodic-orbit
counterexample survives the restriction. **No machine decided. No label upgraded.**

---

## 1. Formulation: π_N projected onto V_odd, and the clean even/odd moment split  [PROVEN]

`π_N = (1/J)Σ_{j<J} δ_{c'_j}` on `ℤ/2^k` (`c'_j` = induced renewal sequence, `c'_{j+1}=F(c'_j)`); Fourier
`π̂_N(a) = (1/J)Σ_j e(a c'_j/2^k)`. The split `V = V_even ⊕ V_odd` is the kernel of the quotient
`ℤ/2^k → ℤ/2^{k-1}`: **even characters `a=2a′` are exactly the characters of the coarser scale `k−1`**
(`χ_{2a′}(s)=χ_{a′}(s mod 2^{k-1})`); odd `a` = the genuinely-new top-bit modes. The projection in real
space is `π_N^odd(s)=½(π_N(s)−π_N(s+2^{k-1}))`.

> **[PROVEN, Parseval — cross-terms vanish trivially]** Every moment `M_{2m}(k)=Σ_a|π̂_N(a)|^{2m}` is
> *diagonal in the character index `a`*, so it splits with **no cross terms**:
> `M_{2m}^full(k) = M_{2m}^odd(k) + M_{2m}^even(k)`.
> The no-go's "even block is driven by the odd block" is therefore **not** an energy cross-term — the energy
> bookkeeping splits perfectly; the coupling lives in the *dynamics* (`U(·,0)` is not a homomorphism), not in
> the moment identity. (Verified: `M₄ᵒᵈᵈ+M₄ᵉᵛᵉⁿ=M₄ᶠᵘˡˡ` to machine precision, §5 table.)

**The decisive 2nd-moment identity** (even chars at scale `k` = all chars at scale `k−1`):

> **[PROVEN, exact — verified to all displayed digits, `odd_energy.py [1]`]**
> `M₂ᵒᵈᵈ(k) = Σ_{a odd}|π̂_N(a)|² = 2^k C₂(k) − 2^{k-1} C₂(k−1)`,
> where `C₂(k)=Coll_k/J² = (1/J²)Σ_r count_r(k)²` is the collision probability.

So **the odd-restricted 2nd moment is exactly the across-scale second difference of the collision counts** —
a purely combinatorial (additive-energy) object, no spectral operator. It is the "fresh-bit budget":
`M₂ᵒᵈᵈ(k)→0` ⟺ each collision class mod `2^{k-1}` splits *evenly* by the next bit (`C₂(k)≈½C₂(k−1)`).

---

## 2. The odd block carries 100 % of the obstruction — exact avg-jump decomposition  [PROVEN, verified]

Let `N_k = count_{3^{-1}}(k) = #{j: c'_j ≡ 3^{-1} mod 2^k}` (the renewal jump-tail counts;
`avg jump = (1/J)Σ_{k≥1}N_k`, `even-density = 1/(1+avg jump)`, threshold `avg jump ≤ 2`, `alpha_attack.py`).
Splitting the inverse-Fourier of `N_k` into even (= scale `k−1`) and odd characters:

> **[PROVEN, exact — `odd_energy.py [2]`, `eps_direct ≡ eps_oddFourier` to machine precision]**
> `N_k = ½N_{k-1} + ε_k`, with `ε_k := 2^{-k} Σ_{a odd} ĉount(a)·e(−a·3^{-1}/2^k)` a **pure odd-character
> correction**. Telescoping (`N_0=J`):
> `avg jump = (1/J)Σ_{k≥1}N_k = 1 + (2/J)Σ_{k≥1} ε_k`, and `even-density ≥ 1/3 ⟺ Σ_{k≥1} ε_k ≤ J/2`.

**The entire deviation of `avg jump` from its ideal value `1` (even-density `½`) lives in the odd
characters** — the no-go's central claim, now re-derived *combinatorially* in the additive-energy language,
independent of the annealed operator. If all odd characters vanished, `N_k=½N_{k-1}` exactly, `N_k=J·2^{-k}`,
`avg jump=1`, even-density `=½`.

---

## 3. Decisive question — is there an unconditional bound on the odd 2nd moment?  [OPEN — NO]

Two sufficient routes to non-halt, both reduced to `M₂ᵒᵈᵈ`:

- **Crude one-sided (magnitude).** `Σ_k|ε_k| ≤ J/2 ⟹ avg jump ≤ 2`. *This escapes the `ENERGY_ATTACK.md`
  sign-blindness*: a magnitude bound suffices for the one-sided conclusion (no sign of `Σε_k` needed).
  Empirically `(2/J)Σ_k|ε_k| ≈ 0.009` — a **~100× margin** to the required `1.0`.
- **Cauchy–Schwarz via the 2nd moment.** `|ε_k| ≤ J·2^{-(k+1)/2}·M₂ᵒᵈᵈ(k)^{1/2}`, hence
  `avg jump ≤ 1 + 2 Σ_k 2^{-(k+1)/2} M₂ᵒᵈᵈ(k)^{1/2}`. Empirically the envelope (the `2Σ…` term) is
  `0.067–0.14`, `≪ 1`, and **shrinks as `J` grows** (random rate, table §5). So a **uniform random-rate
  odd-restricted 2nd-moment bound `M₂ᵒᵈᵈ(k)=O(2^k/J)`** (equivalently `M₂ᵒᵈᵈ(k)=o(2^k)` for fixed `k`)
  would prove non-halt with margin `→ ∞`.

> **[OPEN — the wall, sharpened]** The *only* unconditional inequality on `M₂ᵒᵈᵈ(k)` is
> **`M₂ᵒᵈᵈ(k) ≥ 0`** — i.e. `C₂(k) ≥ ½C₂(k−1)`, the trivial convexity bound (each residue class splits into
> ≤ 2). There is **no unconditional upper bound**: `M₂ᵒᵈᵈ(k)=o(2^k)` is *by definition* odd-restricted
> equidistribution-in-mean of `c'_j mod 2^k`, which is the Open Lemma (`ENDOGENOUS_UE_BUILD.md` §4) =
> (K)/Mahler-3/2. The structural inputs do **not** help: the carry-automaton branch counts, the `0.585n`
> bit-length growth, and the proven longest-run `o(n)` constrain **support and growth**, never the **Cesàro
> frequency** `M₂ᵒᵈᵈ` (the same support-vs-frequency gap that closes `ONECHAR_CANCELLATION.md` §3b).

---

## 4. Does the odd restriction help the recorded 4th-moment (C ≤ 3.45) route?  [NO]

Three findings, all against:

1. **The additive-energy 4th moment is EVEN-dominated, not odd.** `M₄ᶠᵘˡˡ=Σ_a|π̂|⁴` is `≈1.000` (the `a=0`
   main term, which lives in `V_even`), while `M₄ᵒᵈᵈ ≈ 10⁻⁴–10⁻⁶·M₄ᶠᵘˡˡ` (pure fluctuation, §5 table). So
   the additive-energy *4th* moment is the wrong diagnostic for the odd block; the binding fluctuation content
   sits at the **2nd** moment (§2–3). The 4th-moment "sweet spot" of `STATE_FOR_REVIEW` §6.5 buys slack in
   the *constant* but does not change which subspace is binding.
2. **The count-moment threshold `C≤3.45` is NOT lowered by odd restriction.** The Q9 object
   `Σ_r count_r(k)⁴` is an *autoconvolution* (it mixes all character modes), so it does **not** split by
   character parity. Restricting to odd *residues* `r` (a different, real-space cut) merely drops ~half the
   mass: `C` falls `3.06 → 1.59` at `k=12` — no new content, just fewer points. Measured `C` (full) stays
   `≈1.0` in the random-walk regime `k ≲ log₂J` (the relevant regime), matching `STATE_FOR_REVIEW` App. B.
3. **The periodic-orbit counterexample survives the restriction.** A period-`p` orbit (Q9b: `F` has 2-adic
   fixed points `x_D=(3^D−2^D)/(3^{D+1}−2^{D+1})` on every branch) has large `ε_k` and large `M₂ᵒᵈᵈ` too, so
   the odd restriction does **not** remove the orbit-specificity obstruction that blocked the full version.
   The bound remains *false for some orbits* → no `(F,Haar)` / structural quantity can supply it.

---

## 5. Numerics  [OBSERVED / identities PROVEN]

**(5a) Odd 2nd-moment identity** (`odd_energy.py [1]`, `J=40000`; `M₂ᵒᵈᵈ_fft` = direct FFT,
`identity` = `2^kC₂(k)−2^{k-1}C₂(k−1)` — **bit-identical**):

| k | M₂ᵒᵈᵈ (fft) | identity | M₂ᵉᵛᵉⁿ | M₂ᶠᵘˡˡ | random `2^{k-1}/J` |
|---|---|---|---|---|---|
| 6  | 0.00094 | 0.00094 | 1.00067 | 1.00161 | 0.00080 |
| 8  | 0.00252 | 0.00252 | 1.00346 | 1.00598 | 0.00320 |
| 10 | 0.01355 | 0.01355 | 1.01279 | 1.02634 | 0.01280 |
| 12 | 0.05339 | 0.05339 | 1.05248 | 1.10587 | 0.05120 |
| 14 | 0.21061 | 0.21061 | 1.21032 | 1.42092 | 0.20480 |

`M₂ᵒᵈᵈ` tracks the random value `2^{k-1}/J` (the [OBSERVED] equidistribution); `M₂ᵉᵛᵉⁿ→1` (the slaved
block sits at its `a=0` mass). The identity holds exactly.

**(5b) 4th additive energy is even-dominated** (`J=40000`):

| k | M₄ᵒᵈᵈ | M₄ᵉᵛᵉⁿ | M₄ᶠᵘˡˡ | odd/full |
|---|---|---|---|---|
| 8  | 1.16e-07 | 1.000 | 1.000 | 1e-7 |
| 12 | 2.78e-06 | 1.000 | 1.000 | 3e-6 |
| 14 | 1.05e-05 | 1.000 | 1.000 | 1e-5 |

**(5c) avg-jump decomposition + sufficient-bound margins** (`odd_summary.py`):

| J | avg jump | `1+2Σε/J` | `(2/J)Σ|ε_k|` (crude, need ≤1) | C–S envelope `2Σ2^{-(k+1)/2}√M₂ᵒᵈᵈ` (need ≤1) |
|---|---|---|---|---|
| 16000 | 1.00125 | 1.00125 | 0.0105 | 0.142 |
| 40000 | 0.99735 | 0.99738 | 0.0099 | 0.094 |
| 80000 | 0.99924 | 0.99925 | 0.0090 | 0.067 |

Both sufficient bounds hold with large, *growing* margin (envelope `→0` at the random rate
`~(log₂J)/√J`) — **iff** `M₂ᵒᵈᵈ(k)` obeys the random `O(2^k/J)` law, which is the open input.
`ε_k` has *fluctuating sign* (e.g. `ε_2..ε_7 > 0`, `ε_8..ε_10 < 0`) — consistent with the random/√-cancellation
regime; finite `J` says nothing about the liminf.

---

## 6. Honest verdict (the four asks)

1. **Moment identity & even/odd simplification.** `M₂ᵒᵈᵈ(k)=2^kC₂(k)−2^{k-1}C₂(k−1)` exactly; all moments
   split with **no cross terms** (Parseval-diagonal). The simplification is real but *structural* (the
   coupling is dynamical, not an energy cross-term). **[PROVEN]**
2. **Unconditional bound on the odd 2nd/4th moment?** **NO.** Only `M₂ᵒᵈᵈ ≥ 0` (convexity) is free. No weak
   `M₂ᵒᵈᵈ=o(2^k)` follows from branch counts / `0.585n` growth / longest-run `o(n)` (support/growth, not
   frequency). **[OPEN]**
3. **Is `C≤3.45` attackable on the odd sublattice?** **NO improvement.** The 4th energy is even-dominated,
   the count-moment doesn't split by character parity, and the periodic counterexample survives. The binding
   content is the **2nd** moment, which is the kernel. **[PROVEN it does not help]**
4. **Honest reduction.** The odd-restricted route still requires **single-orbit cancellation**: `ε_k` is a
   single-orbit odd-character sum, and `M₂ᵒᵈᵈ(k)=o(2^k)` *is* equidistribution-in-mean of `c'_j` over odd
   characters mod `2^k` = (K)/Mahler. **Exact residual gap:** prove `Σ_{k≥1} 2^{-(k+1)/2} M₂ᵒᵈᵈ(k)^{1/2} < ∞`
   with sum `≤ 1/4` (equivalently a uniform `M₂ᵒᵈᵈ(k)=O(2^k/J)`). Empirically `≈0.03–0.07`; unconditionally
   **open**, and equal to the odd-restricted single-orbit equidistribution.

### Genuinely new vs prior
- **vs `ENDOGENOUS_UE_BUILD.md`** (spectral/operator no-go: odd subspace = zero columns of `L_ann`): the
  *same* "odd carries everything" conclusion is here re-derived **purely combinatorially** (collision counts
  / additive energy), with two new **exact, verified** identities — `M₂ᵒᵈᵈ=2^kC₂(k)−2^{k-1}C₂(k−1)` and
  `avg jump = 1+(2/J)Σε_k` — using **no annealed operator**. An independent confirmation of the no-go.
- **vs `ENERGY_ATTACK.md`** (full energy is *sign-blind* on the mod-4 term): the odd-restricted route gives a
  one-sided **magnitude** sufficient bound (`Σ|ε_k|≤J/2`), so it is **not** sign-blind — a genuine framing
  improvement — but the magnitude bound is itself the odd equidistribution.
- **vs `STATE_FOR_REVIEW.md` §6.5 / App. B** (count-moment 4th route): new result that the **additive-energy
  4th moment is even-dominated** and the binding fluctuation is the **2nd** moment; plus the exact `ε_k`
  attribution and the quantified Cauchy–Schwarz envelope (`≪1`, `→0`).

### Sources
`ENDOGENOUS_UE_BUILD.md` §2–5 (no-go, Open Lemma); `STATE_FOR_REVIEW.md` §6.5 + App. A/B (4th-moment
conditional theorem, thresholds, measured moments); `ENERGY_ATTACK.md` (sign-blindness); `ONECHAR_CANCELLATION.md`
§3b (support-vs-frequency); `L2_FLATTENING_PROBE.md` (×3 bijection / no fixed-scale flattening);
`alpha_attack.py` (avg jump = #odd/#even exact); `renewal_shift.py`, `appendixB_moments.py` (renewal coding).
Scripts: `scratchpad/odd_energy.py`, `scratchpad/odd_summary.py` (exact big-int + FFT, `J≤8·10⁴`).

**No machine decided. No label upgraded.**
