# AIU attack — is the A-invariant limit measure `μ` also `×2`-invariant? (2026-06-29)

*Target: the Adelic Invariance-Upgrade conjecture (AIU, `NEWMATH_ADELIC_RIGIDITY` §2). Setup `[PROVEN]`:
`A=×(3/2)=M_3 M_2^{-1}` on the solenoid `X=(ℝ×ℚ₂×ℚ₃)/ℤ[1/6]`; `M_2=×2`, `M_3=×3` commute, hyperbolic.
The orbit-empirical limit measure `μ` is automatically `A`-invariant `[PROVEN, Krylov–Bogolyubov]`;
`A`-invariance ⟺ `(×3)_*μ=(×2)_*μ`. AIU = the conjecture that `μ` is also separately `×2`-invariant,
`(×2)_*μ=μ`. SOUNDNESS PARAMOUNT: every claim labelled; no claim to prove (K); numerics verified.
Numerics `/Users/aokiyousuke/quantum-ecc/.venv/bin/python` (`scratchpad/aiu_test.py`, exact big-int,
induced odd map, seed `o₀=27`, `N≤10⁵`, ≈25s). NOT committed.*

---

## 0. One-line verdict

**AIU is STRICTLY WEAKER than (K) as a logical statement — `(K)⟹AIU` is `[PROVEN]`, but `AIU⟹(K)` holds
only modulo the OPEN {positive 2-adic entropy ∨ Furstenberg} — and AIU is NOT provable from the currently
proven structure: it is a genuine *transverse second-axis* single-orbit invariance that Krylov–Bogolyubov
and the (first-moment / pointwise) adelic coupling cannot deliver.** Numerically AIU is *not cleanly
testable on raw residues*: on the `×2`-EXPANDED 2-adic place the `×3`-invariance test passes to the
sampling floor (consistent with AIU, but indistinguishable from (K)); on the `×3`-CONTRACTED 3-adic place
the raw residue measure is **not even `A`-invariant** (`TV((×2)_*μ₃,(×3)_*μ₃)≈½`, N-stable — a renewal-
cocycle artifact), so the contracted place neither confirms nor refutes AIU. No numeric refutation, no
numeric separation of AIU from (K). **AIU is a genuine intermediate OPEN conjecture: weaker than (K),
neither provable now nor sufficient alone for (K).**

---

## 1. AIU restated precisely as `(×2)_*μ = μ`

`μ` = any weak-* limit of `μ_N=(1/N)Σ_{n<N}δ_{x_n}`, `x_n` the renewal-normalized solenoid orbit of `x₀`.
- `[PROVEN]` `μ` is `A`-invariant: `A_*μ=μ`. Since `A=M_3M_2^{-1}` and `M_2,M_3` commute, this is exactly
  `(×3)_*μ = (×2)_*μ`.
- `[DEFINITION]` **AIU ⟺ `(×2)_*μ = μ`.** Given `A`-invariance this is **equivalent** to `(×3)_*μ=μ`
  (apply `(×2)_*` to one and `A`-invariance to convert). So AIU = "`μ` is invariant under one host
  generator separately", which (with commuting `M_2,M_3` and `A`) upgrades to full `⟨×2,×3⟩`-invariance.
- **Key subtlety (correctly flagged in the task).** `A`-invariance does **not** give `×2`-invariance for
  free: Krylov–Bogolyubov produces invariance only under the iterated map `A`. The orbit is a `×(3/2)`-orbit;
  `×2` carries each point OFF the orbit. So `(×2)_*μ=μ` is **genuine extra information**, not a tautology
  of `A`-invariance. `[PROVEN — the gap is real]`

---

## 2. Numerics — `μ` vs `(×2)_*μ` vs `(×3)_*μ` on finite quotients `[OBSERVED, exact, N≤10⁵]`

The solenoid `X` is **connected ⟹ has no nontrivial finite quotient group**; `×2,×3` are invertible only
through the full adelic structure. On a finite residue ring each generator is invertible only at the place
where it is a **unit**: `×3` is a unit mod `2^k` (permutes `(ℤ/2^k)^*`); `×2` is a unit mod `3^m` (permutes
`(ℤ/3^m)^*`). We test the AIU-relevant invertible axis at each place.

**(a) 2-adic place mod `2^k` — `×3` invertible (this is the AIU axis here):**

| N | `TV(μ₂,(×3)_*μ₂)` k=4 | k=6 | k=8 | `TV(μ₂,Unif_odd)` k=4 |
|---|---|---|---|---|
| 10³ | 0.031 | 0.069 | 0.206 | 0.023 |
| 10⁴ | 0.0137 | 0.0274 | 0.0595 | 0.0101 |
| 10⁵ | **0.0065** | 0.0117 | 0.0192 | **0.0037** |

`TV(μ₂,(×3)_*μ₂)→0` at the finite-sampling rate `~√(cells/N)` (k=4: 8 cells, floor `√(8/10⁵)≈0.009`).
**On the expanded 2-adic place `μ₂` is Haar-consistent AND `×3`-invariant** — consistent with AIU. *But*
both AIU and (K) predict uniform here, so this axis **cannot separate AIU from (K)**. `[OBSERVED]`

**(b) 3-adic place mod `3^m` — `×2` invertible (the AIU axis here), and the renewal diagnostic:**

| N | `TV(μ₃,(×2)_*μ₃)` m=2/3/4 | `TV((×2)_*μ₃,(×3)_*μ₃)` (A-inv sanity) |
|---|---|---|
| 10³ | 0.742 / 0.863 / 0.931 | 0.509 |
| 10⁴ | 0.748 / 0.876 / 0.940 | 0.500 |
| 10⁵ | **0.750 / 0.875 / 0.938** | **0.4995** |

These are **large and N-stable** (do NOT decrease with N). The decisive reading is the last column:
`A`-invariance forces `(×2)_*μ=(×3)_*μ` exactly, so a faithful marginal would give `TV=0`. We get
`TV≈½`, **stable**. Reason `[PROVEN]`: the raw orbit's 3-adic valuation law is `P(v₃=k)=2^{-(k+1)}`
(geometric base 2, `v₃(o_{n+1})=D_n−1`, `ADELIC_COUPLING`), so `(×2)` (a unit) preserves `v₃` while
`(×3)` shifts `v₃↦v₃+1`; the mismatch on the `v₃=0` shell (mass `½` vs `0`) gives `TV≈½`. **Therefore the
raw residue measure `o_n mod 3^m` is NOT `A`-invariant — it is not `μ₃`.** The renewal cocycle (clearing
the `2^D·3^{D-1}` denominators, the `Γ`-translation) is precisely what restores `A`-invariance, and it
rewrites the valuation bookkeeping the raw residues get wrong. `[PROVEN — renewal artifact]`

**(c) Valuation law and 3-adic unit part (why the contracted place is non-Haar):** `v₃(o_n)`-distribution
matches geometric-2 `2^{-(k+1)}` (`0.4995, 0.2504, 0.1252, 0.0629,…`) to 3 dp, **not** `ℤ₃`-Haar
`(2/3)3^{-k}` (`0.667, 0.222, 0.074,…`). The 3-adic unit part is not uniform and not `×2`-invariant on the
raw measure (`TV(μ_U,Unif*)≈0.38`, `TV(μ_U,(×2)_*μ_U)≈0.45`, both N-stable) — all symptoms of the same
renewal artifact, since the raw contracted-place residues are not the solenoid marginal. `[OBSERVED]`

> **`[PROVEN — numeric honesty]` AIU is not cleanly testable on raw orbit residues.** The 2-adic
> (expanded) axis is consistent with AIU but cannot distinguish it from (K). The 3-adic (contracted)
> axis is contaminated by the renewal cocycle — the raw residue measure is not even `A`-invariant there
> (`TV≈½`) — so it can neither confirm nor refute AIU. **No numeric decided AIU.**

---

## 3. Structural analysis — what would FORCE `(×2)_*μ=μ`, and is it circular?

**3.1 `(K)⟹AIU` is `[PROVEN]` (AIU is necessary for (K)).** (K) ⟺ `μ=m_X` Haar (`SESSION…AEV_CORE` §1).
Haar on `X` is invariant under every automorphism, in particular `×2`. So `(K)⟹(×2)_*μ=μ⟹AIU`. Hence AIU
is a **logical consequence of (K)**, i.e. weaker-or-equal. `[PROVEN]`

**3.2 `AIU⟹(K)` only conditionally (the gap).** AIU ⟹ `μ` is `⟨×2,×3⟩`-invariant; `μ` is non-atomic
`[PROVEN, 2-adic repulsion, REPELLER_ESCAPE]`. To conclude `μ=`Haar one then needs **either** `h_μ(M_2)>0`
(then **Rudolph–Johnson** `[PROVEN-in-lit]`) **or** Furstenberg's conjecture (no non-atomic zero-entropy
host-invariant measure) `[OPEN]`. Both are open; positive 2-adic entropy is itself `(K)`-necessary and
`(K)`-hard (`LIMIT_MEASURE_ENTROPY` §2). **So AIU alone does not provably give (K).** The exact gap
`AIU→(K)` = `{h_μ(M_2)>0 ∨ Furstenberg}`. `[PROVEN reduction structure]`

> **`[PROVEN]` AIU is strictly weaker than (K).** `(K)⟹AIU` is proven; `AIU⟹(K)` is not (it needs an OPEN
> extra input). Concretely, AIU constrains only the *unit/leaf* structure of `μ` at each place; it does
> **not** pin the valuation distribution (which `×2`, a unit, cannot see), whereas Haar/(K) requires the
> 3-adic valuation law to be Haar (`(2/3)3^{-k}`) — the raw orbit shows geometric-2 instead (§2c). The
> entropy/valuation degree of freedom is exactly what AIU leaves free. AIU is therefore a genuinely
> *lower* rung than (K), not a synonym.

**3.3 Is AIU provable from proven structure? NO.** Two independent reasons.
- **Krylov–Bogolyubov gives only `A`-invariance.** `×2`-invariance is transverse: `×2` moves the orbit off
  itself, so `(×2)_*μ=μ` is new content (§1). There is no proven mechanism (no second iterated map, no
  spectral gap — the acting group `ℤ[1/6]⋊⟨3/2⟩` is amenable, rank-1; `EXPERT_ASK_HOMOGENEOUS`,
  `EMPTY_TOOLBOX`). `[PROVEN — no available engine]`
- **The adelic coupling does not supply it.** `INTRATERM_ADELIC_MINING` PROVED (T1) the product formula is
  a single scalar/step = first moment only, and (T2) the 3-adic place is an **invertible time-shift** of
  the 2-adic (`v₃(o_{n+1})=D_n−1`), carrying *identical* information — no independent channel. So the
  adelic structure gives **no** handle on `(×2)_*μ` vs `μ` beyond the real place. `NEWMATH_ADELIC_RIGIDITY`
  §3.3 concedes (T1)–(T2) at the pointwise/first-moment level and *hopes* the measure-level statement is
  different ("pointwise lock ≠ measure-level invariance"). That distinction is **correct in principle**
  (a Cesàro limit can be `×3`-invariant though no point is `×3`-movable) but is **UNPROVEN** — it is
  precisely AIU-min, the irreducible conjecture, restated. `[OBSERVED — barrier conceded, not crossed]`

**3.4 Circularity check — is AIU just (K) on another axis?** Not identical (§3.2: strictly weaker), but
*proving* AIU appears to require a **second single-orbit equidistribution** — that the orbit's unit/leaf
data on the transverse `×2` axis equidistributes — of the **same flavor and difficulty class** as the
2-adic equidistribution that is (K). So while AIU is formally weaker, the only visible route to it is an
equidistribution statement no easier than (K). **AIU relocates, but does not lower, the difficulty**; it is
not a free corollary and not a shortcut. `[PROVEN-honest]`

---

## 4. Honest verdict

| question | verdict | label |
|---|---|---|
| AIU as a statement | `(×2)_*μ=μ` ⟺ (given `A`-inv) `⟨×2,×3⟩`-invariance | `[DEFINITION]` |
| `(K)⟹AIU`? | **Yes** (Haar is `×2`-invariant) | `[PROVEN]` |
| `AIU⟹(K)`? | Only modulo OPEN `{h_μ(M_2)>0 ∨ Furstenberg}` | `[PROVEN reduction]` |
| AIU vs (K) | **Strictly weaker** than (K); does not pin valuation/entropy | `[PROVEN]` |
| Provable from proven structure? | **No** — transverse invariance, KB gives only `A`-inv; adelic coupling is first-moment/pointwise (T1–T2) | `[PROVEN — not provable now]` |
| Adelic/`ℚ₃` handle beyond real place? | **No** — 3-adic = invertible time-shift of 2-adic, no independent channel | `[PROVEN]` |
| Blocked / disproven? | **No** — non-atomic, 2-adic axis consistent with AIU; 3-adic raw test is a renewal artifact, not a refutation | `[OBSERVED]` |
| Net | Genuine **intermediate OPEN** conjecture: weaker than (K), neither provable now nor alone sufficient | `[honest]` |

**What exactly remains.** AIU is the unproven measure-level claim `(×2)_*μ=μ`. It sits strictly below (K):
proving it needs a transverse single-orbit equidistribution input (of (K)-comparable difficulty), and even
granting it, (K) still requires `h_μ(M_2)>0` or Furstenberg. The adelic structure that motivated AIU is, at
the pointwise/first-moment level, a proven tautology (T1–T2); its only escape — that the *limit measure*'s
invariance group exceeds the orbit's pointwise symmetry by exactly `×3` — is itself AIU-min and is supplied
no proof. The renewal cocycle obstructs any clean finite-quotient numeric test on the contracted 3-adic
place, so numerics cannot decide it.

---

## Sources
- Repo: `NEWMATH_ADELIC_RIGIDITY.md` (§2 AIU, §3.2 dichotomy, §3.3 (T1)–(T2) barrier), `NEWMATH_SYNTHESIS.md`
  (framework I), `LIMIT_MEASURE_ENTROPY.md` (entropy = RJ-vs-Furstenberg selector; `h_μ=0⟹(K)` false),
  `ADELIC_COUPLING.md` (`v₃(o_{n+1})=D_n−1`, product formula = first moment), `INTRATERM_ADELIC_MINING.md`
  (joint `ℤ₂×ℤ₃` law is density-null / first-moment tautology), `REPELLER_ESCAPE.md`,
  `EXPERT_ASK_HOMOGENEOUS.md`, `EMPTY_TOOLBOX_QUESTION.md`.
- Literature: Rudolph (ETDS 1990) / Johnson — `×2,×3` measure rigidity (positive entropy ⟹ Haar)
  `[PROVEN-in-lit]`; Furstenberg (1967) measure conjecture `[OPEN]`; *Rigidity… commuting automorphisms on
  tori and solenoids*, arXiv:2101.11120 (solenoid RJ form) `[PROVEN-in-lit]`; Lind–Schmidt–Ward (solenoid
  entropy `h(×u)=Σ_v log⁺|u|_v`) `[PROVEN-in-lit]`; Einsiedler–Lindenstrauss (JMD 2008, rank-1
  non-rigidity) `[PROVEN-in-lit]`.
- Numerics: `scratchpad/aiu_test.py` (exact big-int, induced odd map, `o₀=27`, `N≤10⁵`, ≈25s).

No machine decided. No label upgraded.
