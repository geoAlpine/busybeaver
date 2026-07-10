# o4 Ostrowski / three-distance / Denjoy–Koksma test — the archimedean rotation is EFFECTIVELY equidistributed (Baker, two logs), but it is ORTHOGONAL to the 3-adic digit (2026-07-10)

*A genuinely-new tool tried on the o4 frequency problem: Ostrowski numeration + the three-distance theorem +
CF-discrepancy for the ARCHIMEDEAN rotation number β = log₃(4/3) of the orbit Wₙ ~ α(4/3)ⁿ. The exp-sum agent did
Weyl sums; this does the exact-gap / effective-discrepancy refinement. STRICT labels; exact big-int orbit + mpmath
high precision. Scripts: `o4_ostrowski_test.py`, `o4_ostrowski_coupling.py`, `o4_ostrowski_discrepancy.py`. NOT
committed.*

---

## 0. One-line verdict

**[INSUFFICIENT — does not decide; one PARTIAL worth stating precisely].** The archimedean rotation {nβ},
β = log₃(4/3), IS **effectively equidistributed unconditionally**: its approximability is a **linear form in TWO
logarithms** `Λ = q·log4 − (p+q)·log3`, squarely inside Baker's reach, giving an effective finite irrationality
measure (empirically μ≈2) and hence an effective discrepancy `N·D*_N ≤ 2 + Σ_{q_k≤N} a_{k+1} ≤ 76` for N ≤ 1.5×10⁵
[PROVEN archimedean]. **But this control is ORTHOGONAL to freq{3|Wₙ}:** conditioning the 3-adic residue on the
mantissa {nβ} gives χ²=1.74 (df 9, crit 16.9) and Pearson corr = 0.0009 — the leading-base-3-digit motion (archimedean)
and the trailing 3-adic residue (non-archimedean) are statistically independent coordinates of the same integer.
The three-distance theorem controls the ∞-place; freq{3|Wₙ} lives at the 3-place; they **decouple exactly**. This is
the sharpest concrete form of the archimedean-vs-non-archimedean split that is the (K) wall. **No machine decided.
No label upgraded.**

---

## 1. The archimedean rotation number β and its Ostrowski/CF structure [PROVEN, verified]

Since `3W_{n+1} = 4Wₙ + (e−14)` with the correction `(e−14)/(4Wₙ) → 0` geometrically,
`log₃W_{n+1} = log₃Wₙ + β + o(1)`, so **frac(log₃Wₙ) = {frac(log₃W₀) + nβ + D_n}** with `D_n → D_∞` a convergent
drift. The rotation number is
> **β = log₃(4/3) = log₃4 − 1 = 0.26185950714291487419905…**

Continued fraction (mpmath dps=220, all 80 quotients inside precision):
```
β = [0; 3,1,4,1,1,11,1,46,1,5,112,1,1,1,1,1,3,1,7,2,4,1,2,1,2,15,9,4,2,5,1,41,1,2,5,2,2,3,4,1,18,8,27,…]
```
- **Partial quotients are NOT bounded (as far as computable): large spikes 46, 112, 41, 27, 24; mean ≈ 6.6.** β
  behaves like a generic (Khinchin-typical) irrational — it is **not badly approximable** (occasional large aₖ ⟹
  discrepancy spikes at those scales), but the spikes are mild.
- Convergent denominators qₖ: 1,3,4,19,23,42,485,527,24727,25254,150997,16936918,… The empirical irrationality-measure
  indicator `1 + log a_{k+1}/log q_k` stays ≤ 2 and → 1 as qₖ grows ⟹ **μ(β) ≈ 2 empirically**.

## 2. Effective archimedean equidistribution — Baker on TWO logs [PROVEN, effective]

The key structural fact this tool exposes: the rotation's approximation quality is a linear form in two logarithms.
`||qβ|| = |qβ − p| = |q·log4 − (p+q)·log3| / log3` (assertion-checked to 30 digits against the direct value for
k≤19). Thus `Λ = q·log4 − (p+q)·log3 = log(4^q / 3^{p+q})` — **a two-term linear form in logs of algebraic numbers**,
which is exactly the case Baker (1966) / Baker–Wüstholz make **effective and unconditional** (sharp two-log estimates:
Laurent–Mignotte–Nesterenko). Consequently:
- `||qβ|| ≥ c / q^{μ−1}` with **effective** c, μ < ∞. Hence **{nβ} equidistributes with an effective rate.**
- **Effective discrepancy (Ostrowski / Kesten):** `N·D*_N ≤ 2 + Σ_{k: q_k ≤ N} a_{k+1}`. Computed bound = **76** for
  all N ≤ 1.5×10⁵; empirical `N·D*_N` = 2.3–11.7 (verified). So `D*_N = O((Σaₖ)/N) = O(log N · polylog / N) → 0`,
  effectively.
- **Three-distance theorem** verified: the points {nβ}, n<N, cut the circle into gaps taking **exactly 3 distinct
  lengths** (N=500, 5000, 50000: all show 3), the two short ones summing to the long — the exact Ostrowski gap
  structure, lengths governed by ‖q_{k}β‖.

**This is a genuine unconditional PARTIAL:** the *archimedean* (magnitude / leading-base-3-digit) equidistribution of
the o4 orbit is *effectively proven*, no conjecture needed, because it reduces to a two-log linear form.

## 3. THE CRUX — does archimedean control couple to freq{3|Wₙ}? NO [OBSERVED, decisive]

freq{3|Wₙ} = freq{ρ=1}, ρ = Wₙ mod 3, is the **trailing** 3-adic residue — a different place of ℚ from the mantissa.
If `1{3|Wₙ}` were a Riemann-integrable function of {nβ}, Weyl + §2 would transfer and decide o4. It is not. Exact
orbit N=2×10⁵ (seed 43), residue vs mantissa {nβ}:

| test | result | reading |
|---|---|---|
| freq{ρ=1 \| mantissa∈[j/10,(j+1)/10)}, j=0..9 | all in **0.327–0.338**, mean 0.3325, stdev **0.0029** | flat at 1/3 |
| χ² independence (mantissa-bucket × 1{ρ=1}), df=9 | **1.74** (crit₀.₀₅ = 16.9) | **cannot reject independence** |
| Pearson corr({nβ}, 1{3|Wₙ}) | **0.00089** | **uncorrelated** |

**The 3-adic residue is statistically orthogonal to the archimedean rotation.** The three-distance / Ostrowski
machinery pins the leading base-3 digits of Wₙ to arbitrary effective precision and says **exactly nothing** about
Wₙ mod 3.

## 4. Why they decouple — the sharpest form of the archimedean/non-archimedean split [ASSESSED]

`Wₙ` is one integer with two independent coordinates: its **∞-adic size** `log₃Wₙ = log₃W₀ + nβ + o(1)` (the rotation,
Baker-effective, §2) and its **3-adic residue** `Wₙ mod 3` (the digit, §3). The map to the residue is a **deep,
discontinuous** digit: consecutive n with essentially equal mantissa {nβ} carry unrelated residues (the odometer
`W' = (4W + c)/3` reads `W mod 3^{k+1}` to fix `W' mod 3^k` — the AEV non-descent of `NEWMATH_DIGIT_BRIDGE §2`). No
continuous function of the ∞-place equals `1{W≡0 (3)}`; the coupling that would let equidistribution transfer is
identically zero. This is exactly the (K) wall in its cleanest coordinates: **the archimedean place is effectively
controlled (Baker, two logs); the 3-adic place is (K)-hard; the o4 orbit's leading and trailing digits are
independent.** Ostrowski/three-distance is the right tool for one place and provably orthogonal to the other.

## 5. What was built

| item | content | label |
|---|---|---|
| CF/Ostrowski of β=log₃(4/3) | `[0;3,1,4,1,1,11,1,46,1,5,112,…]`, unbounded mild spikes, μ≈2, not badly approx. | [PROVEN, verified] |
| two-log form | `‖qβ‖ = |q log4 − (p+q) log3|/log3`, Baker-effective ⟹ μ(β)<∞ effective | [PROVEN] |
| effective discrepancy | `N·D*_N ≤ 2+Σ_{q_k≤N}a_{k+1} = 76` (N≤1.5e5); three-distance = 3 gaps | [PROVEN, verified] |
| archimedean equidistribution of orbit | leading-base-3-digit motion of Wₙ effectively equidistributes | [PROVEN, effective] |
| **coupling to freq{3|Wₙ}** | χ²=1.74/df9, corr=0.0009, freq flat 0.333 across mantissa | **[OBSERVED — ORTHOGONAL]** |
| transfer to decide o4 | none — the digit is not a function of the ∞-place | [OPEN, wall located] |

## 6. Verdict

The Ostrowski / three-distance / Denjoy–Koksma refinement delivers a clean **unconditional partial** the raw Weyl
build did not phrase: the o4 orbit's **archimedean** equidistribution is *effectively proven* because β's
approximability is a linear form in **two** logarithms (Baker's unconditional reach), with an explicit CF-discrepancy
`N·D*_N ≤ 76` and the exact three-distance gap structure. But it **does not decide o4 and upgrades no label**: the
target freq{3|Wₙ} is the trailing 3-adic residue, statistically orthogonal to the mantissa (χ²=1.74, corr=0.0009), so
the effective archimedean control transfers *zero* information to the non-archimedean digit. The test converts the
folklore "archimedean vs non-archimedean split" into a measured, decisive orthogonality — the (K) wall, exactly
located between the two places of the one integer Wₙ.

**Scripts:** `o4_ostrowski_test.py` (CF/convergents), `o4_ostrowski_coupling.py` (orbit + χ²/corr), 
`o4_ostrowski_discrepancy.py` (D*_N, three-distance, two-log form). Interpreter `.venv`, exact big-int + mpmath dps≥120.

**References.** Baker, *Linear forms in the logarithms of algebraic numbers* (1966); Baker–Wüstholz (1993);
Laurent–Mignotte–Nesterenko, sharp two-log estimates (1995). Ostrowski numeration & CF-discrepancy: Kesten (1966,
Erdős–Szüsz); Kuipers–Niederreiter; Drmota–Tichy. Three-distance theorem (Steinhaus/Sós/Świerczkowski). Non-descent /
(K): `NEWMATH_DIGIT_BRIDGE_2026-07-09.md`, `O4_EXPSUM_FREQUENCY_BUILD_2026-07-10.md`, `O4_RUN_STRUCTURE_2026-07-07.md`.

No machine decided. No label upgraded.
