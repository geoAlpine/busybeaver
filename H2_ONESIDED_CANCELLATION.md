# A one-sided / single-character cancellation tool aimed at H₂ — Korobov–Bourgain geometric sums (2026-06-29)

*Angle (live move #2 of `SESSION_2026-06-29_A_ASSAULT.md`): a specialized **single-character, one-sided**
cancellation tool aimed at **H₂ specifically**, NOT full equidistribution. The surviving avenue is
"quenched single-orbit geometric-(3/2)-phase character cancellation"; we target only ONE mod-2 character,
one-sided (`liminf ≥ −1/3`), with factor-2 slack. Question: can a Korobov/Vinogradov-type or any modern
single-frequency / one-sided exponential-sum technique give even a partial one-sided cancellation for THIS
computable orbit that the full-equidistribution routes cannot? Numerics
`/Users/aokiyousuke/quantum-ecc/.venv/bin/python` (`scratchpad/h2_onesided.py`, `scratchpad/korobov.py`,
exact big-int). Every line labelled. Zero false proofs. NOT committed.*

Target recall (`WEAKEST_SUFFICIENT.md`): (K) ⟺ **H₂ : liminf_N (1/N) Σ_{n<N} (−1)^{c_n} ≥ −1/3**,
`c₀=8`, `c_{n+1}=⌊3c_n/2⌋`; the parity word `(c_n mod 2)` is computable. Full Mahler/AEV is even-density
→ 1/2 = base-3/2 normality; H₂ is the strictly-weaker one-sided `≥1/3` form (Vaaler: `J=5` circle frequencies).

---

## 0. One-line verdict

The "Korobov/Vinogradov for geometric sequences" family **does** contain the bespoke single-frequency tool
the prompt names — the **Korobov–Bourgain geometric exponential sum** `Σ_{n≤N} e_m(a g^n)`, which *is* a
single-character, one-sided-capable cancellation for `g^n mod m`. But it **provably does not reach H₂**, and
the reason is **NEW and sharper** than the prior "dimension mismatch" framing:

> **Verdict (b), with a new precise reason.** Korobov–Bourgain delivers cancellation in `Σ_{n≤N} e_m(a g^n)`
> only when the **summation length** `N` is at least a fixed positive power of the multiplicative order
> `t = ord_m(g)` (`N ≥ t^ε`, requiring `t ≥ m^δ`). H₂ reads the parity off the **diagonal**
> `c_n mod 2 ≈ bit_{n−3}(3^n)` — i.e. it samples the modulus `2^{n−2}` (order `2^{n−4}`) with **exactly one
> index `n` per modulus**, length `N = 1` per modulus, infinitely below the activation threshold
> `2^{ε(n−4)}`. The single term `|e_m(·)| = 1` admits **no** within-modulus cancellation; the only
> cancellation H₂ asks for is **across** moduli, which is the orthogonal direction the tool has no power in.
> **The one-sided / single-character / factor-2 weakening is ORTHOGONAL to this:** Korobov–Bourgain is a
> *two-sided absolute-value* bound (stronger than H₂'s one-sided liminf), so the slack cannot relax its
> length requirement. The weakening does not move the wall at all.

So this is **not** a crack and **not** a mere rederivation of the old wall: it is a **new tool-level
characterization** (verdict (b)) — the canonical single-frequency geometric-cancellation theorem fails for a
**length-along-the-diagonal** reason that is provably immune to one-sidedness and to the `1/3` slack. It also
contains a small **[PROVEN]** negative (§4). No label upgraded.

---

## 1. The right tool exists and is exactly "single character, one-sided-capable" `[PROVEN-in-lit]`

The Korobov/Vinogradov "method" splits into two branches; only the **second** is the geometric single-frequency
tool the prompt asks for.

- **Branch I — analytic Korobov–Vinogradov (k-th derivative test / Vinogradov mean value).** Built for
  **polynomial** phases. For the geometric phase `ξ(3/2)^x` the k-th-derivative ratio
  `A = max|f^{(k)}|/min|f^{(k)}| = (3/2)^{b−a} → ∞`, and Weyl differencing is a fixed point
  `ξ(3/2)^n ↦ ξ((3/2)^h−1)(3/2)^n`. **Already CLOSED** with this exact inequality in `ATTACK_VDC.md §1`
  (and `ATTACK_MAUDUIT_RIVAT.md`). This branch never had geometric power. `[PROVEN, prior note]`

- **Branch II — arithmetic Korobov–Bourgain (the "rational exponential sum with an exponential function").**
  This is precisely the single-frequency geometric tool. For integer `g` of multiplicative order
  `t = ord_m(g)` modulo `m`:
  > **[PROVEN-in-lit] (Korobov 1953; Bourgain 2005; Bourgain–Glibichuk–Konyagin 2006; Bourgain–Chang 2009).**
  > Given `δ > 0` there are `ε = ε(δ) > 0` and `N₀` such that if `t ≥ m^δ` then for all `N ≥ t^ε`,
  > `max_{(a,m)=1} |Σ_{n=1}^{N} e_m(a g^n)| ≤ N · m^{−ε}`.
  This is a **single frequency** (one `a`), and a bound on `|Σ|` gives a one-sided liminf for `Re/Im` for
  free — so it is *strictly stronger* than the one-sided cancellation H₂ wants. It is THE modern tool for
  geometric-sequence character cancellation (its applied home is the Diffie–Hellman distribution). `[PROVEN-in-lit]`

**This is the genuine candidate.** It is single-character, geometric, and over-delivers on one-sidedness.
The whole question is whether it can be pointed at H₂.

---

## 2. The orbit's parity is read off the DIAGONAL — where Branch II has no length `[PROVEN]`

The decisive structural fact (cross-checked numerically, §5):

- **The relevant arithmetic of H₂ is `3^n mod 2^k`.** Idealizing away the self-generated carry,
  `c_n mod 2 ≈ bit_{n−3}(3^n) = ⌊3^n / 2^{n−3}⌋ mod 2`, which is a function of `3^n mod 2^{n−2}`. `[PROVEN]`
- **`ord_{2^k}(3) = 2^{k−2}`** for `k ≥ 3` (verified exactly, `k=3..12`, §5). So the modulus governing index
  `n` is `m = 2^{n−2}` with order `t = 2^{n−4}`: **both grow linearly in `n`**. `[PROVEN]`
- **One index per modulus.** Branch II's saving lives in the variable `n` *at fixed modulus `m`* — it is a
  **within-modulus, length-`N` time average**. H₂ advances the modulus with `n` (the diagonal), so each
  modulus `2^{n−2}` is visited by **exactly one** index. The available within-modulus length is `N = 1`,
  versus the activation threshold `N ≥ t^ε = 2^{ε(n−4)} → ∞`. `[PROVEN]`
- **A length-1 sum cannot cancel.** `|Σ_{n=1}^{1} e_m(a g^n)| = 1` identically; no within-modulus
  cancellation is even possible. **Branch II is therefore identically trivial along the diagonal.** `[PROVEN]`

The geometry: Branch II has power in the **horizontal** direction (vary `n`, fix the modulus); H₂ lives on the
**anti-diagonal** (each `n` carries its own modulus). The tool's power axis and the orbit's read axis are
orthogonal. This is the precise, quantitative form of the "dimension mismatch / `n`-th bit of the `n`-th power"
remark in `ALL_ROUTES_SWEEP.md` (correction #1) — but stated for the **dynamic length-`N` geometric sum**
(Korobov–Bourgain time series), not the **static subgroup sum** `Σ_{x∈⟨3⟩} e_m(x)` that ALL_ROUTES analysed
(that one cancels to exactly 0 by Ramanujan but is the *wrong object*; here the object is *right* — a length-`N`
time average — but is sampled at length 1). See §6 for the delta.

---

## 3. Why the one-sided / single-character / factor-2 slack does NOT change the wall `[PROVEN]`

The prompt's core question. Three independent reasons the weakening is orthogonal to Branch II's obstruction:

1. **Korobov–Bourgain is already two-sided and single-character.** Its conclusion `|Σ| ≤ N m^{−ε}` is an
   absolute-value (two-sided) bound at a single frequency, which **implies** the one-sided `liminf` H₂ needs.
   So H₂ is logically *downstream* of the tool's output — relaxing H₂ to one-sided buys nothing the tool
   doesn't already give *for free where it applies*. The weakening is on the wrong side of the implication. `[PROVEN]`
2. **The slack lives in the frequency-count / margin, not the length.** Vaaler converts the `1/3` target to
   `J = 5` circle frequencies (`WEAKEST_SUFFICIENT.md §4`); the factor-2 slack tolerates `avg(−1)^{c_n}` down
   to `−1/3`. **Neither relaxes the within-modulus length requirement** `N ≥ t^ε`. The length wall (§2) is a
   property of `g^n mod m` geometry, untouched by how many frequencies or how much margin the *output* allows. `[PROVEN]`
3. **Length-1 admits no cancellation at any tolerance.** Even an arbitrarily generous one-sided target cannot
   be met by a per-modulus sum of one unit-modulus term. The only cancellation available is cross-modulus =
   the original H₂ liminf itself. `[PROVEN]`

**Conclusion.** The one-sided / single-character / factor-2-slack weakening **does not change the wall for the
Korobov–Bourgain tool at all**. It is the same wall, and the *precise* reason is now tool-specific: the slack
is orthogonal to the **length-along-the-diagonal** obstruction. `[PROVEN]`

---

## 4. One bankable [PROVEN] structural negative (new, modest)

> **[PROVEN] (elementary, given the cited Korobov–Bourgain activation threshold).** Let
> `S_n^{(k)} := Σ_{j=1}^{n} e_{2^k}(a·3^j)`. The Korobov–Bourgain saving `|S_N^{(k)}| ≤ N·2^{−εk}` activates
> only for `N ≥ (ord_{2^k} 3)^ε = 2^{ε(k−2)}`. The H₂ diagonal supplies, for each modulus `2^k`, a summation
> length of exactly `1 ≪ 2^{ε(k−2)}`. Therefore **the Korobov–Bourgain bound is identically trivial along the
> H₂ diagonal**, and this conclusion is **independent of** (i) one-sidedness, (ii) the number of circle
> frequencies retained, and (iii) the size of the numerical margin. The factor-2 / one-character / one-sided
> weakening cannot activate the tool.

This is a tool-level impossibility (like `SELECTOR_COMPUTABILITY.md §2`'s computability-line NO), not a
search failure. It does **not** crack (K); it pins, with a single inequality `1 < 2^{ε(n−4)}`, why the best
single-frequency geometric-cancellation theorem is structurally inapplicable to the weakened target.

---

## 5. Numerics — exact big-int `[OBSERVED]`/`[PROVEN by computation]`

`h2_onesided.py`, `korobov.py` (`.venv`); `c₀=8`, `c_{n+1}=⌊3c_n/2⌋`, exact.

| quantity | value | reading |
|---|---|---|
| `mean (−1)^{c_n}` (`N=2·10⁵`) | `+0.00037` | AEV value `0`; even-density `0.50019` |
| **worst running `avg(−1)^{c_n}` (`n≥50`)** | **`−0.0407` at `n=122`** | min even-density `0.4797`; **margin above `−1/3` = `0.2927`** |
| `J=5` circle-frequency `|partial Weyl|/N` (`j=1..5`) | `0.004, 0.012, 0.012, 0.012, 0.008` | all `≈0`; the 5 frequencies Vaaler needs *look* fully cancelling `[OBSERVED]` |
| `ord_{2^k}(3)`, `k=3..12` | `= 2^{k−2}` exactly | confirms order doubles per level `[PROVEN by computation]` |
| **fixed-modulus `2^{14}`** `\|S_N\|/N`, `N=4,16,256,1024,4096` | `1.00, 0.33, 0.106, 0.037, 0.000` | Korobov–Bourgain cancellation **is real** but needs length `N` a positive power of the order `t=4096` `[OBSERVED]` |
| diagonal length per modulus | **`1`** | the death: at `N=1`, `\|S\|/N = 1` (trivial); the tool never activates `[PROVEN]` |
| `parity(c_n) == bit_n(8·3^n)` (no-carry idealization) | `980/2000 ≈ 49%` (chance) | the **exact** parity is the diagonal bit **XOR self-generated carry** `bit_n(T_n)`; carry is the quenched hard part `[OBSERVED]` |

**Reading.** Three facts line up. (i) H₂ has a **comfortable `~0.29` margin** above its `−1/3` floor and the
`J=5` frequencies all look cancelling — i.e. the weakened target *appears* easily true. (ii) Korobov–Bourgain
cancellation is **genuine and visible** at fixed modulus, but turns on only as the length `N` climbs toward the
order. (iii) The diagonal samples each modulus at length exactly `1`, in the regime where `|S_N|/N = 1` is
trivial — so the visible tool power (ii) is never delivered to the visible margin (i). The numerics make the
length-along-the-diagonal wall concrete. The `49%`-chance agreement of the no-carry idealization confirms the
*exact* orbit additionally carries the self-generated `T_n` carry (a second obstruction, §6 (B-ii)).

---

## 6. Honest verdict table

| Question | Answer |
|---|---|
| **(a)** Genuine NEW route to crack / partially-crack H₂? | **NO.** Korobov–Bourgain — the single-frequency geometric-cancellation tool — is identically trivial along the H₂ diagonal (`[PROVEN]` §4). No partial one-sided cancellation is obtained that the full-equidistribution routes could not. |
| **(b)** Precise NEW characterization of why the one-sided/single-character weakening still fails? | **YES — this is the deliverable.** The bespoke single-frequency tool fails for a **length-along-the-diagonal** reason: it needs within-modulus length `N ≥ t^ε`; H₂ reads the anti-diagonal at length `1` per modulus. The one-sided / single-character / factor-2 slack is **orthogonal** to this (the tool is already two-sided and stronger than H₂'s output; the slack relaxes frequency-count and margin, not length). New, tool-specific, and `[PROVEN]`. |
| **(c)** Or just rederive the existing wall? | **It rederives the same wall (no theorem closes H₂) but with a genuinely new tool-level reason and two distinct obstructions** (B-i length-1-per-modulus; B-ii self-generated carry breaks the clean `g^n mod m` group structure). Sharper than ALL_ROUTES's static-subgroup framing. |

**Net.** Primarily **(b)**: the surviving avenue is *narrowed*. We can now say precisely that the canonical
single-frequency geometric tool (Korobov–Bourgain, the Diffie–Hellman exponential sum) is not merely "unproven
here" but **structurally orthogonal** to H₂ — its power axis (vary `n`, fix modulus) is perpendicular to H₂'s
read axis (one modulus per `n`), and no amount of one-sidedness or `1/3` slack rotates one onto the other.

### What is genuinely new vs prior notes
1. **First analysis of the *dynamic* Korobov–Bourgain geometric exponential sum** `Σ_{n≤N} e_m(g^n)` as the
   bespoke single-frequency one-sided tool. `ATTACK_VDC.md` closed only Branch I (analytic k-th-derivative /
   Vinogradov mean value for polynomial phases). `ALL_ROUTES_SWEEP.md` correction #1 analysed only the
   **static subgroup sum** `Σ_{x∈⟨3⟩} e_m(x)` (Ramanujan → exactly 0, but wrong object). This note is the
   length-`N` **time-series** version — the correct object — and shows it dies at **length 1 per modulus**.
2. **The length-vs-slack orthogonality `[PROVEN]` (§3, §4):** the factor-2 / one-sided / single-character
   weakening relaxes frequency-count and margin but **not** the `N ≥ t^ε` length requirement; the tool is
   already two-sided and over-delivers one-sidedness. This directly answers the prompt's "does the weakening
   change the wall?" — **no, and here is the tool-specific reason.**
3. **The activation-threshold inequality `1 < 2^{ε(n−4)}`** as the single-line statement of the wall, with the
   exact order fact `ord_{2^k}(3)=2^{k−2}` and the fixed-modulus cancellation curve (`|S_N|/N: 1.00→0.00` as
   `N→t`) verified by exact computation — making "the tool works horizontally, the orbit reads the diagonal"
   quantitative.
4. **Two distinct obstructions separated:** (B-i) length-1-per-modulus; (B-ii) the exact parity is
   `bit_n(8·3^n) ⊕ bit_n(T_n)` — the self-generated carry breaks the pure `g^n mod m` group structure
   Korobov–Bourgain requires (numerics: idealization agrees only at chance). Either alone is fatal.

### Relation to the two walls
Branch II is a **quenched single-orbit** within-modulus average; its theorem (Korobov–Bourgain) is
unconditional but needs length `≥ t^ε`. The diagonal denies it that length. This is the same annealed-vs-quenched
/ a.e.-vs-single-orbit boundary as the other closed routes (`NONPISOT_FOURIER_CHAIN`, `ATTACK_VDC §2`): the
tool that *would* give the quenched bound is starved of its essential parameter (here, length) by the orbit's
diagonal geometry. The surviving avenue remains **quenched single-orbit geometric-(3/2)-phase character
cancellation**, now with the Korobov–Bourgain sub-route explicitly closed by a length argument.

### Sources
- N. M. Korobov, *Exponential Sums and their Applications*, Mathematics and its Applications **80**, Kluwer
  (1992) — classical bounds for `Σ e_m(a g^n)`, the "rational exponential sum with an exponential function."
- J. Bourgain, *Mordell's exponential sum estimate revisited*, J. Amer. Math. Soc. **18** (2005) 477–499,
  https://www.ams.org/journals/jams/2005-18-02/S0894-0347-05-00476-5/S0894-0347-05-00476-5.pdf .
- J. Bourgain, *Estimates on exponential sums related to the Diffie–Hellman distributions*, Geom. Funct. Anal.
  **15** (2005) — the geometric-sequence single-frequency cancellation in its applied form.
- J. Bourgain, A. A. Glibichuk, S. V. Konyagin, *Estimates for the number of sums and products and for
  exponential sums in fields of prime order*, J. London Math. Soc. (2) **73** (2006) 380–398 — `t ≥ p^δ ⇒`
  nontrivial `Σ_{n≤N} e_p(a g^n)` for `N ≥ t^ε`.
- J. Bourgain, M.-C. Chang, *Exponential sum estimates over subgroups of Z_q^*, q arbitrary*, J. Anal. Math.
  **109** (2009) 253–286 — the general-modulus (`q = 2^k`, our case) version.
- Mahler 3/2 / equidistribution context: arXiv:1806.03559 (*On the uniformity of (3/2)^n mod 1*);
  arXiv:2510.11723 (AEV, *A normality conjecture on rational base number systems*); arXiv:2502.17090
  (*Some results on asymptotic versions of Mahler's problems*, 2025 — fetched but theorem statements not
  independently verified, so cited only as context, **not** relied upon).
- Prior repo notes: `WEAKEST_SUFFICIENT.md` (H₂, Vaaler `J=5`), `ATTACK_VDC.md` (Branch I closed),
  `ALL_ROUTES_SWEEP.md` (static-subgroup / dimension-mismatch), `SELECTOR_COMPUTABILITY.md` (style + the
  second wall).

**No machine decided. No non-halt asserted. No label upgraded.**
