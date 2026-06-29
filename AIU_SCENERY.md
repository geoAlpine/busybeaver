# AIU as scenery / scale-2 self-similarity of the 2-adic marginal μ₂ (2026-06-29)

*WEAPONS_AUDIT style. Investigates the "scale-invariance / scenery self-similarity" reading of the
Adelic Invariance-Upgrade conjecture (AIU, `NEWMATH_ADELIC_RIGIDITY` §2; `AIU_ATTACK`). Setup `[PROVEN]`:
`A=R=×(3/2)=M₃M₂⁻¹` on the solenoid `X=(ℝ×ℚ₂×ℚ₃)/ℤ[1/6]`; the orbit-empirical limit `μ` is
`A`-invariant (Krylov–Bogolyubov); AIU ⟺ `(×2)_*μ=μ` ⟺ (given `A`-inv) `(×3)_*μ=μ`. SOUNDNESS
PARAMOUNT: every claim labelled; no claim to prove (K). Numerics
`/Users/aokiyousuke/quantum-ecc/.venv/bin/python scratchpad/scenery_test.py` (exact big-int moving
diagonal, `N≤10⁵`, ~2.5s). NOT committed.*

---

## 0. One-line verdict

**The scenery / scale-2 view gives a NEW CHARACTERIZATION but NO partial: it REDUCES to (K)/annealed.**
There are exactly two self-similarity equations available, and they bracket the problem from the wrong
sides. The **weak** one — scale-2 (shift) invariance of μ₂ — has a **non-unique** solution set (every
stationary process; *not* Haar), so it is far too weak. The **strong** one — the IFS equation
`μ₂ = ½[(2x)_*μ₂+(2x+1)_*μ₂]` — has the **unique** scale-invariant solution Haar `[PROVEN]`, but the
orbit's μ₂ *satisfying* it is logically identical to (K) (it builds in a uniform independent low bit), so
it is **circular**. The genuine dynamical self-referential equation forced by `c_{n+1}=⌊3c_n/2⌋` is the
**infinite-range carry-coupled ×3-adder transducer** (`NEWMATH_DIAGONAL_RENORM` §2), which — because
`|3/2|₂=2>1` (non-Pisot) — does **not** close to a finite IFS and whose invariant-measure problem **is**
(K). The proven annealed gap ½ proves the i.i.d.-input scale-flow contracts to Haar, but transfers to the
quenched single orbit only via R-GEN/AIU, **OPEN**. **No machine decided. No label upgraded.**

---

## 1. AIU's 2-adic part as scale-2 self-similarity — made precise

### 1.1 The host generators and a metric caveat `[PROVEN]`
In the `ℤ²` host `Φ(a,b)=M_{2^a3^b}` (`NEWMATH_ADELIC_RIGIDITY` §1.2):
- `×2 = M₂ = Φ(1,0)`: dilations `(2, ½, 1)` — at the 2-adic place a **pure bit-shift** (the `(i,j)=(1,0)`
  element, `X_n(2α,k)=X_n(α,k−1)`, `DIAGONAL_RENORM` §1.2). **Metric caveat:** `|2|₂=½`, so `×2` is a
  2-adic **contraction**, not a magnification. The scenery *magnification* `S` (zoom into finer 2-adic
  scale = drop the lowest bit, `S(x)=⌊x/2⌋`) is its left-inverse `×½` on the even leaf. The task's
  "`×2` = magnification by 2" should read: `×2` is the **scale-2 bit operation** generating the scenery;
  the place that genuinely **expands by 2** is `R=×(3/2)` (`|3/2|₂=2`), not `M₂`.
- `R = A = ×(3/2) = Φ(−1,1) = M₃M₂⁻¹`: the **time-step** `(i,j)=(−1,1)`, `X_n((3/2)α,k)=X_{n+1}(α,k)`.
- `M₃ = Φ(0,1)`: `(i,j)=(0,1)`.

**Relation of R and ×2 (task §1).** `R` and `×2` are *different host generators*: `×2` is the
"horizontal" 2-adic scenery shift `(1,0)`; `R` is the "diagonal" dynamical step `(−1,1)`. They satisfy
`×2 = M₃·R⁻¹`. The orbit gives us **`R`-invariance** (the diagonal symmetry, `[PROVEN]`); AIU asks that
the **horizontal** `×2`-symmetry follow. Equivalently, since `A`-invariance forces `(×3)_*μ=(×2)_*μ`,
AIU ⟺ `(×2)_*μ=μ` ⟺ `(×3)_*μ=μ`. The scenery picture is therefore **exactly the rank-1 (`R`) →
rank-2 (`⟨×2,×3⟩`) invariance upgrade**, restated as: *the 2-adic marginal is self-similar under the
scenery scaling, not merely under the diagonal time-step.*

### 1.2 The 2-adic marginal and its scenery `[DEFINITION]`
`μ₂` := the 2-adic marginal of a weak-* limit `μ`, i.e. the limiting law of the low-bit string of the
moving diagonal `a_n=⌊8(3/2)ⁿ⌋=(8·3ⁿ)≫n` (the (K) object; `bit₀=d_n` the parity bit). On the bit-string
space `{0,1}^ℕ`, the scenery map is the shift `S` (drop `b₀`). "Scale-2 self-similarity of μ₂" admits
three inequivalent precise forms, tested in §4:
- **(I) Literal pushforward** `(×2)_*μ₂` on `ℤ/2^w`. Degenerate: `×2` is not a unit mod `2^w`, image is
  all-even ⇒ `TV≈½` automatically (a contraction artifact, **not** a test of AIU — §4).
- **(II) Weak self-similarity = shift-invariance:** `S_*μ₂=μ₂` (law of `(b₁..b_w)` = law of `(b₀..b_{w-1})`).
- **(III) Strong self-similarity = the IFS / Furstenberg equation** of §3.

---

## 2. Does proven structure say anything about scale-2 invariance of the QUENCHED μ₂? (task §2)

**Annealed gap ½ — what it proves `[PROVEN-numeric]`.** Randomising the carry (input bits i.i.d.
Bernoulli(½)=Haar) turns the ×3-adder into a finite Markov transducer on state `(last bit, carry∈{0,1,2})`
with spectrum `{1,½,½,0}`, gap ½, unique stationary output Bernoulli(½)=Haar (`DIAGONAL_RENORM` §3.1).
This is precisely the statement that **the i.i.d.-surrogate scale-flow contracts to the scale-invariant
(Haar) fixed point at rate `2^{−n}`**. So at the **annealed** tier, scale-2 invariance is forced and
unique.

**Does it transfer to the quenched μ₂? NO — annealed only `[PROVEN — gap is real]`.** The annealed fixed
point assumes the low-bit tail feeding each carry is already Haar/i.i.d. The quenched orbit uses its
**own deterministic carry** `γ_n^{(k)}` (a function of the entire fractional tail `{8(3/2)ⁿ}`). The
transfer "annealed Haar attractor ⟹ quenched μ₂ scale-invariant" is exactly **R-GEN** (`DIAGONAL_RENORM`
§4) = AIU = (K)-hard, `[OPEN]`. Krylov–Bogolyubov delivers only `R`-invariance; `×2` moves the orbit off
itself, so `(×2)_*μ=μ` is genuine transverse information (`AIU_ATTACK` §1).

**Non-Pisot no-atom — what it rules out `[PROVEN]`.** `R*:ξ↦(3/2)ξ` on `ℤ[1/6]` has no nonzero periodic
point ⇒ no atomic/Pisot/sofic scale-invariant fixed point; the bit-bearing place **expands** (`|3/2|₂=2`)
so there is no contracting 2-adic direction to support an atom (`DIAGONAL_RENORM` §3.2). This **eliminates
the atomic alternatives** among scale-invariant μ₂ — but leaves the entire **non-atomic stationary
simplex** (§3.1). It removes trivial fixed points; it does **not** give uniqueness=Haar.

> **Net:** the proven structure pins the **annealed** scale-flow to a unique Haar fixed point with gap ½,
> and kills atomic quenched fixed points — but says **nothing forcing** the quenched μ₂ to be scale-2
> invariant. The gap is the full Mahler wall, unchanged.

---

## 3. Is a self-similarity FORCED by the dynamics? The exact equation + uniqueness (task §3)

### 3.1 WEAK self-similarity (shift-invariance): solution set NON-UNIQUE `[PROVEN]`
The minimal scale-2 reading is `S_*μ₂=μ₂`. **But every stationary process on `{0,1}^ℕ` satisfies it** —
i.i.d. Bernoulli(p) for *any* p, all Markov chains, etc. The shift-invariant simplex is infinite-
dimensional and Haar is one extreme point. So **shift-invariance does NOT pin Haar; uniqueness fails
maximally.** (This is the bit-string face of rank-1 non-rigidity, Einsiedler–Lindenstrauss JMD 2008: a
single endomorphism has an uncountable invariant simplex.) Numerically confirmed: Bernoulli(0.3) and
Bernoulli(0.1) pass the shift-test to the sampling floor while being non-Haar (§4).

### 3.2 STRONG self-similarity (IFS equation): UNIQUE solution Haar — but CIRCULAR `[PROVEN]`
The Hutchinson/Furstenberg equation for the digit IFS `{ι₀:x↦2x, ι₁:x↦2x+1}` (equal weights) on `ℤ₂`:
> `μ₂ = ½[(ι₀)_*μ₂ + (ι₁)_*μ₂]`.
Both maps are 2-adic contractions (ratio ½) and `ι₀(ℤ₂)=2ℤ₂`, `ι₁(ℤ₂)=2ℤ₂+1` tile `ℤ₂`, so by the
contraction-mapping theorem the **invariant probability measure is unique and equals Haar (Bernoulli(½))**
`[PROVEN]`. Equivalently: the equation says "prepend a **uniform, independent** low bit and recover μ₂",
which by induction forces all bits i.i.d. uniform = Haar.
**Why this is circular.** The equation *builds in* the uniform-independent low bit; asserting that the
orbit's μ₂ satisfies it is logically identical to asserting `bit₀` is Haar-balanced and independent of
the tail — i.e. **(K) itself**. It is a restatement of equidistribution, not a lever toward it. (This is
the IFS form of the annealed §2 fixed point; its uniqueness is the annealed gap ½, and "the orbit obeys
it" is the quenched R-GEN.)

### 3.3 The equation the dynamics ACTUALLY forces: infinite-range carry, does NOT close `[PROVEN]`
`c_{n+1}=⌊3c_n/2⌋` gives the **exact** self-referential recurrence (`DIAGONAL_RENORM` §2):
> `d_{n+1}^{(k)} = d_n^{(k+1)} ⊕ d_n^{(k)} ⊕ γ_n^{(k)}`, `γ_n^{(k)}` = carry from **all lower bits**.
This is a genuine self-similarity of the orbit's bit-array, but with an **unbounded-range carry**.
Because `|3/2|₂=2>1` (non-Pisot, §2), it **does not close to a finite IFS / sofic automaton**: there is
no finite set of contractions whose attractor measure is μ₂. So the *honest* dynamical self-similarity
equation is **not** the clean §3.2 IFS — it is an infinite-state carry-coupled transducer whose
invariant-measure problem is exactly (K). The two clean equations (§3.1 too weak / non-unique; §3.2
unique-but-circular) are the annealed shadows that the real, infinite-range equation casts.

> **Verdict (task §3):** an exact self-similarity equation for μ₂ exists in three forms — weak
> (shift-inv, **non-unique**), strong (IFS, **unique=Haar but circular**), and the true dynamical one
> (infinite-carry transducer, **= (K)**). None is simultaneously *forced by the dynamics* **and**
> *uniqueness-Haar* without already being (K).

---

## 4. Numerics `[OBSERVED, exact big-int, N≤10⁵, scratchpad/scenery_test.py]`

Moving diagonal `a_n=⌊8(3/2)ⁿ⌋`, low-bit windows; TV vs sampling floor `√(2^w/N)`. (`N=10⁵`:)

| w | (I) `TV(μ₂,(×2)_*μ₂)` | (II) shift-inv `TV` | (III) strong/IFS `TV` | floor |
|---|---|---|---|---|
| 4 | **0.4985** | 0.0056 | 0.0050 | 0.0126 |
| 6 | **0.4985** | 0.0118 | 0.0106 | 0.0253 |
| 8 | **0.4985** | 0.0258 | 0.0199 | 0.0506 |

- **(I) literal `(×2)_*`: TV≈½, N-stable** — the contraction artifact (`×2` not a unit mod `2^w`, image
  all-even). **Not a refutation of AIU**, exactly as the 3-adic raw test in `AIU_ATTACK` §2 was a renewal
  artifact. The literal "magnification" pushforward is the wrong object.
- **(II) shift-invariance & (III) strong/IFS: both → 0 at the sampling floor** — the orbit's μ₂ is
  scale-2 self-similar to the resolution the data can see, **consistent with Haar** (i.e. with (K)).

**Non-uniqueness demonstration (the decisive control):** i.i.d. Bernoulli(p), `N=10⁵`:

| process | shift-inv `TV` (w=6) | strong/IFS `TV` (w=6) |
|---|---|---|
| Bernoulli(0.5) | 0.016 | 0.011 |
| Bernoulli(0.3) | **0.014 (passes)** | **0.199 (fails)** |
| Bernoulli(0.1) | **0.006 (passes)** | **0.401 (fails)** |

This is the §3 dichotomy in numbers: **weak shift-invariance cannot tell Haar from Bernoulli(0.3)**
(non-unique), whereas the **strong/IFS equation is passed only by the uniform process** (unique=Haar) —
and the orbit's passing of the strong test is therefore exactly the empirical (K)-signal, with no
independent leverage.

---

## 5. Honest verdict (task §4)

| question | verdict | label |
|---|---|---|
| AIU-2-adic = scale-2 self-similarity of μ₂ | Yes, a clean **reformulation** (rank-1 `R` → horizontal `×2` symmetry) | `[DEFINITION]` |
| Does it give a **partial** toward AIU/(K)? | **No** | `[PROVEN-honest]` |
| Weak self-similarity (shift-inv) ⟹ Haar? | **No** — non-unique (all stationary processes) | `[PROVEN]` |
| Exact self-sim equation with **unique** solution = Haar? | Yes, the IFS `μ₂=½[(2x)_*μ₂+(2x+1)_*μ₂]` | `[PROVEN]` |
| …but is the orbit's obeying it provable / non-circular? | **No** — it = (K) (builds in uniform indep. bit) | `[PROVEN — circular]` |
| Equation the dynamics actually forces | infinite-range carry transducer; non-Pisot ⇒ no finite IFS | `[PROVEN]`; invariant-measure = (K) |
| Does annealed gap ½ / no-atom transfer to quenched μ₂? | annealed-only (= R-GEN/AIU); no-atom kills only atomic fixed pts | `[PROVEN]` annealed; `[OPEN]` quenched |
| Net | **New characterization, no partial; REDUCES to (K)/annealed** | `[honest]` |

**The exact gap.** Between the `[PROVEN]` annealed scale-flow (unique Haar fixed point, gap ½, no atoms)
and the quenched μ₂ lies precisely the transfer of contraction from the i.i.d.-carry surrogate to the
single orbit's own carry `γ_n^{(k)}` — i.e. R-GEN = AIU, and even granting it, Haar still needs
`h_μ(M₂)>0` ∨ Furstenberg (`DICHOTOMY_LEMMA_AUDIT`). The scenery view relocates AIU onto the 2-adic
scenery axis and supplies a sharp uniqueness statement (Haar is the unique solution of the *strong* IFS
equation), but the only self-similarity the dynamics *forces* is the infinite-carry transducer, whose
solution is not pinned without (K). Nothing here is provable from proven structure.

## Sources
- Repo: `NEWMATH_ADELIC_RIGIDITY.md` (§2 AIU, §3.3 (T1)–(T2)), `AIU_ATTACK.md` (AIU strictly weaker than
  (K); raw-residue tests = artifacts), `NEWMATH_DIAGONAL_RENORM.md` (§2 exact ×3-adder recurrence; §3.1
  annealed gap ½ unique Haar fixed point; §3.2 non-Pisot no-atom; §4 R-GEN), `DICHOTOMY_LEMMA_AUDIT.md`
  (two gaps: AIU ∧ `h_μ>0`∨Furstenberg), `THERMO_FORMALISM.md` (annealed vs quenched wall), `DIGITS_OF_3N.md`.
- Literature: Hutchinson (IFS, unique invariant measure, 1981); Furstenberg (self-similar/`×2,×3`, 1967,
  `[OPEN]`); Erdős–Salem / Li–Sahlsten arXiv:1910.03463 (self-similar measure Rajchman ⇔ non-Pisot);
  Frougny / K. Schmidt (Pisot β-expansion = finite/sofic transducer — *fails* for non-Pisot 3/2);
  Rudolph (ETDS 1990) / Johnson / Einsiedler–Lindenstrauss arXiv:2101.11120 (`×2,×3` rigidity, positive
  entropy ⟹ Haar); Einsiedler–Lindenstrauss JMD 2008 (rank-1 non-rigidity / non-unique simplex);
  Bedford–Fisher (scenery flows); Hochman–Shmerkin (scenery / CP-distributions).
- Numerics: `scratchpad/scenery_test.py` (exact big-int moving diagonal, `N≤10⁵`, ~2.5s): (I) literal
  `(×2)_*` TV≈0.4985 (artifact); (II) shift-inv & (III) IFS TV → floor (Haar-consistent); Bernoulli(p)
  control shows shift-inv non-unique (p=0.3,0.1 pass) vs IFS unique (only p=0.5 passes).

No machine decided. No label upgraded.
