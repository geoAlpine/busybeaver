# One-character / one-sided / crude-bound specialization of the Antihydra kernel (2026-06-29)

*Angle: the prior cancellation attacks (van der Corput `ATTACK_VDC.md`, Mauduit–Rivat
`ATTACK_MAUDUIT_RIVAT.md`) all targeted **full equidistribution** / general Weyl sums and were
[CLOSED] by the lacunarity of `(3/2)^n` (the `(3/2)^{b−a}→∞` derivative-ratio blow-up, the
differencing fixed point). This note attacks a strictly smaller object: the kernel needs only
**ONE mod-2 character, ONE-SIDED (`≥−1/3`), with a factor-2 slack** — not `|S|=o(N)` at all
frequencies. We ask whether one-sidedness + a crude (non-vanishing) bound opens a genuine gap
below that closed wall. Numerics `/Users/aokiyousuke/quantum-ecc/.venv/bin/python`
(`scratchpad/onechar.py`, `scratchpad/theta_opt.py`, exact big-int phases + LP minorants). Every
line labelled. Zero false proofs. No machine decided; no non-halt asserted.*

---

## 0. One-line answer

The one-character/one-sided framing **does** shrink the *logical* content (from "all frequencies,
two-sided, `o(N)`" to "finitely many frequencies, a one-sided lower bound"), but it **does NOT**
reduce the requirement to a *crude* bound, and it does **not** cross the wall. Two sharp findings:

1. **[PROVEN, new] A crude bound `|S_N(h)|/N ≤ (1−ε)N` is NOT sufficient.** The Vaaler/Beurling–
   Selberg minorant route forces, for the surplus to beat `1/3`, a tolerance
   `θ* = (m̂(0)−1/3)/(2·A_J)` with a **rigorous ceiling `θ* ≤ 1/6`** (because any minorant with
   constant `m̂(0)>1/3` has L¹ coefficient mass `A_J ≥ m̂(0)`), and an **empirical optimum
   `θ* ≈ 0.043`** (LP, all degrees). So H2 needs `|S_N(h)|/N ≲ 0.043` — i.e. **≥ ~96% cancellation**
   on finitely many `h` — never a mere "phases don't all align." At the minimal degree `J=5` there is
   **zero** surplus (`m̂(0)=1/3` exactly), so `J=5` requires **genuine `o(N)`** on all 5 sums.
2. **[PROVEN, structural] Even the crude bound is unreachable from FLP / support theorems.**
   `|S_N(h)|/N ≤ 1−ε` is a **Cesàro frequency** statement (the empirical measure of `{h·y_n}` is not
   asymptotically a Dirac mass). FLP `Ω(3/2)≥1/3`, Vijayaraghavan, Pisot are **support / limit-point**
   statements (which values are approached i.o.), which say **nothing** about frequencies. The
   support-vs-frequency gap is the same wall as in `ATTACK_VDC.md` §2 / `WEAKEST_SUFFICIENT.md`.

**Verdict: weaker *statement* (one character, one-sided, finite `J`), same *theorem* (single-orbit
frequency cancellation behind both walls). The crude-bound hope is refuted by an explicit `θ*≤1/6`
ceiling.** This sharpens `WEAKEST_SUFFICIENT.md` by quantifying exactly how strong the finitely-many
Weyl bounds must be.

---

## 1. H2 as a single exponential sum; is one-sided genuinely different? `[PROVEN]`

Kernel `(K) ⟺ H2 : liminf_N (1/N) Σ_{n<N} (−1)^{c_n} ≥ −1/3`, `c₀=8`, `c→⌊3c/2⌋`. Writing
`even-density = freq(c_n even) = freq({y_n} ∈ half-arc)` (the carry/parity arc, mean `1/2`), and
`avg(−1)^{c_n} = 2·even-density − 1`, the target is the **one-sided LOWER bound**
```
   even-density  ≥  1/3       ( ⟺  avg(−1)^{c_n} ≥ −1/3 ).
```
**One-sided IS structurally different from two-sided `|S|=o(N)`:**
- Two-sided cancellation `|Σ(−1)^{c_n}|=o(N)` forces `avg→0`, which gives `≥−1/3` with a full `1/3`
  to spare — so `o(N) ⟹ H2`, but H2 is **strictly weaker**: it permits an arbitrary persistent
  *positive* bias and only forbids the average dropping below `−1/3`.
- A **lower** bound on a frequency is exactly what a **one-sided minorant** delivers: pick a
  trig polynomial `m ≤ 1_arc` and bound `Σ 1_arc(y_n) ≥ Σ m(y_n)` from below. This needs only the
  **finitely many** Fourier modes of `m`, and only their (possibly adverse) contribution — never the
  full character at all frequencies. **So one-sidedness genuinely converts "all-frequency two-sided
  cancellation" into "finitely-many-frequency, lower-contribution-only."** This is the real content
  of the slack; §2–§3 then ask *how strong* those finitely many bounds must be.

---

## 2. Vaaler minorant: EXACTLY what the J=5 Weyl sums must satisfy `[PROVEN]`

Vaaler: the extremal degree-`J` trig **minorant** of an interval indicator has constant term
`m̂(0)=1/2 − 1/(J+1)` (L¹ deficiency `1/(J+1)`). With `m≤1_arc`,
```
   even-density ≥ (1/N) Σ m(y_n) = m̂(0) + Σ_{1≤|j|≤J} m̂(j)·(1/N)Σ_n e(j y_n)
              ≥ m̂(0) − 2 Σ_{j=1}^{J} |m̂(j)| · |S_N(j)|/N ,   S_N(j)=Σ_{n<N} e(j y_n).
```
**At the minimal degree `J=5`: `m̂(0)=1/2−1/6 = 1/3` EXACTLY.** Surplus `= 0`. Therefore H2 at `J=5`
requires
```
   |S_N(j)|/N → 0   for each j = 1,2,3,4,5     (genuine o(N), vanishing density)
```
— **NOT** a crude `(1−ε)`. This is **equidistribution restricted to the first 5 frequencies** (and
free at all `j>5`, and one-sided). So the weakening vs full Weyl u.d. is *finiteness of the frequency
count*, **not** a relaxation from `o(N)` to crude at those frequencies.

**Exact bound H2 requires (the deliverable):**
| route | requirement on the Weyl sums | vs full equidistribution |
|---|---|---|
| full Weyl u.d. | `|S_N(j)|/N → 0` for **all** `j ≥ 1` | — |
| H2 via `J=5` minorant | `|S_N(j)|/N → 0` for `j=1..5` **only**, one-sided | finite frequency set; **same `o(N)` strength on those 5** |
| H2 via crude bound (any `J`) | `|S_N(j)|/N ≤ θ*` for `j=1..J`, `θ*≤1/6` (≈`0.043` opt.) | **still ≥~96% cancellation**, not crude |

---

## 3. The crux: is a CRUDE `|S_N(h)|/N ≤ (1−ε)N` enough, and reachable? `[PROVEN: NO to both]`

### 3a. Crude is NOT enough — explicit `θ* ≤ 1/6` ceiling `[PROVEN]`
To buy room for a non-vanishing bound, raise `J` so `m̂(0)>1/3`. With a uniform crude bound
`|S_N(j)|/N ≤ θ` for `j=1..J`, H2 holds iff `m̂(0) − 2 A_J θ ≥ 1/3`, i.e.
```
   θ  ≤  θ*(J) := (m̂(0) − 1/3) / (2 A_J),     A_J := Σ_{j=1}^{J} |m̂(j)|.
```
**Rigorous ceiling.** Any minorant with `m̂(0)>1/3` satisfies, on the arc-complement (measure `1/2`,
where `1_arc=0`), `m ≤ 0`, so the non-constant part `f=m−m̂(0)` has `‖f‖_∞ ≥ m̂(0)`; and
`A_J = Σ|m̂(j)| ≥ ‖f‖_∞ ≥ m̂(0)`. Hence
```
   θ*  ≤  (m̂(0) − 1/3)/(2 m̂(0))   ≤   1/6   (maximised at m̂(0)=1/2).   ∎
```
So **no minorant of any degree tolerates a crude bound weaker than `θ = 1/6`** — H2 needs at least
`|S_N(h)|/N ≤ 1/6` (≥ 83% cancellation), not `≤ (1−ε)` for small `ε`.

**LP optimum (`theta_opt.py`, true amplitude `A_J`, all degrees):**
```
  J     best t (=m̂0)    A_J      θ*
  5      0.3333         —       (no surplus: needs o(N))
  8      0.398        1.197    0.027
 20      0.453        1.482    0.040
 50      0.465        1.535    0.043   ← plateau
GLOBAL θ* ≈ 0.043 .
```
**So H2 via a uniform Weyl bound needs `|S_N(h)|/N ≲ 0.043` on `h=1..J` (J≈20–50) — i.e. ≥ ~96%
cancellation, a *strong* bound, never "phases merely don't all align."** The slack converts
*infinitely-many* into *finitely-many* frequencies, but it does **not** convert *strong cancellation*
into a *crude* bound at those frequencies.

### 3b. Even the crude bound is unreachable from FLP / non-degeneracy `[PROVEN structural]`
Could `|S_N(h)|/N ≤ 1−ε` (let alone `≤0.043`) come for free from a single non-degeneracy?
- `|S_N(h)|/N → 1` ⟺ the empirical measure of `{h·y_n}` is asymptotically a **single Dirac mass**
  (all phases Cesàro-aligned). So `|S_N(h)|/N ≤ 1−ε` ⟺ the orbit is **not asymptotically
  concentrated at one phase mod `1/h`** — a **frequency / Cesàro** statement.
- **FLP `Ω(3/2)≥1/3`**, Vijayaraghavan (∞ many limit points), and Pisot's theorem (`(3/2)` non-Pisot
  ⟹ `‖ξ(3/2)^n‖ ↛ 0`) are all **support / limit-point** statements: which values are approached
  *infinitely often* (`limsup/liminf` of the orbit). They are **silent on frequencies**: the orbit
  can spread over `≥1/3` of the circle in its closure yet visit the spread region with **vanishing
  frequency**, leaving `|S_N(h)|/N → 1`. The support-vs-frequency gap is exactly the gap that closes
  vdC/MR (`ATTACK_VDC.md` §2.2, `WEAKEST_SUFFICIENT.md` §6).
- Web/literature check (2026-06-29): for a **fixed** `ξ`, no unconditional nontrivial bound on
  `Σ_{n<N} e(ξ(3/2)^n)` exists — best citable is the **trivial `O(N)`** (`ATTACK_VDC.md` §2); all
  cancellation results (Salem–Zygmund `√(N log log N)`, Algom–Chang–Wu–Wu) are **metric / a.e.** and
  cannot be specialised to one orbit. Even the *crude* `≤(1−ε)N` is unproven for any specific `ξ`.

---

## 4. Honest verdict (the task's point 4) `[OPEN — same wall]`

Does one-character / one-sided / crude open a gap below the closed full-equidistribution wall?
- **Logical content: YES, reduced** — from "all frequencies, two-sided" to "finitely many (`J≈5–50`),
  one-sided lower contribution." This is real and is the cleanest compression of `(K)` (consistent
  with `WEAKEST_SUFFICIENT.md`).
- **Crude-bound gap: NO (refuted here).** One-sidedness does **not** relax the per-frequency demand to
  `|S|≤(1−ε)N`. The Vaaler L¹ deficiency forces `|S_N(h)|/N ≲ θ* ≤ 1/6` (empirically `≈0.043`) — a
  *strong* cancellation on each retained frequency. At the minimal `J=5` you need outright `o(N)`.
- **Difficulty: NO, does not cross the wall.** Each retained bound — whether the `J=5` `o(N)` or the
  higher-`J` `≤0.043` — is a **single-orbit Cesàro/frequency** statement for the lacunary `(3/2)^n`
  phase, behind both walls (annealed mean `=0` only / a.e. `√N` only / FLP support only). Even the
  weakest possible crude version is a frequency statement that no current theorem delivers.

**Bottom line.** The one-character/one-sided specialization yields the **weakest known *statement*** of
the kernel but **not an easier *theorem***: the factor-2 slack is spent on *finiteness of the
frequency count*, and the L¹-deficiency ceiling `θ*≤1/6` shows it **cannot** be spent on *crudeness of
the bound*. The reduction (raw TM → this one-sided single-character kernel) remains the unconditional
contribution; `(K)` stays **[OPEN]**, equivalent to strong cancellation of finitely many fixed-`ξ`
`(3/2)^n` Weyl sums — the same wall as vdC/MR, now with the crude-bound escape explicitly closed.

---

## 5. Numerics `[OBSERVED]`

`onechar.py` (exact big-int fractional parts, `frac(4h·3^n/2^n)=(4h·3^n mod 2^n)/2^n`).

**(5a) Literal lacunary Weyl sums `S_N(h)=Σ_{n<N} e(4h(3/2)^n)`** (generic, ξ-free):

| h | `|S|/N` (N=2·10³) | `|S|/N` (N=2·10⁴) | `|S|/√N` (N=2·10⁴) |
|---|---|---|---|
| 1 | 0.0182 | 0.0070 | 0.996 |
| 2 | 0.0024 | 0.0042 | 0.587 |
| 3 | 0.0015 | 0.0042 | 0.588 |
| 4 | 0.0229 | 0.0121 | 1.705 |
| 5 | 0.0316 | 0.0029 | 0.409 |

**(5b) Orbit-faithful `Σ e(h·{S_n/4})`, `S_n=Σ_j e_{n−1−j}(3/2)^j`** (`N=3000`, parity mean
`+0.016`, even-density `0.508`):

| h | `|S|/N` | `|S|/√N` |
|---|---|---|
| 1 | 0.0296 | 1.623 |
| 2 | 0.0094 | 0.517 |
| 3 | 0.0123 | 0.671 |
| 4 | 0.0215 | 1.180 |
| 5 | 0.0164 | 0.900 |

**Reading.** All 5 Weyl sums are **`|S|/N ≈ 0.003–0.03 ≪ 1`** — bounded away from the trivial `1` with
huge margin, and bounded away from the required `θ*≈0.043` too; `|S|/√N` stays `O(1)` (the empirical
`√N` / generic regime, matching `ATTACK_VDC.md` §4). **The orbit behaves exactly as if the strong
bound held**, but the observed cancellation is the **open `√N`** behaviour; an **unconditional** bound
— even the crude `≤(1−ε)N`, let alone `≤0.043 N` — is what is missing, and is the same single-orbit
frequency wall. **`[OBSERVED]`; finite `N` says nothing about the liminf.**

---

### What is genuinely new vs `WEAKEST_SUFFICIENT.md`
1. **The crude-bound escape is explicitly CLOSED with a ceiling `θ* ≤ 1/6` (rigorous) / `≈0.043`
   (LP-optimal).** Prior notes established the `J=5`/factor-2 slack but left open whether a mere
   `|S|≤(1−ε)N` could exploit it; here that hope is refuted by the L¹-deficiency `A_J ≥ m̂(0)`.
2. **The `J=5` requirement is pinned as genuine `o(N)`** (zero surplus, `m̂(0)=1/3` exactly), so the
   slack lives in the *frequency count*, not in the *strength* of each bound.
3. **The support-vs-frequency obstruction is stated as the precise reason FLP / Pisot / Vijayaraghavan
   cannot even give the crude bound** (Cesàro Dirac-mass vs limsup/liminf closure).

**No machine decided. No non-halt asserted. No label upgraded.** `(K)` remains `[OPEN]`.
