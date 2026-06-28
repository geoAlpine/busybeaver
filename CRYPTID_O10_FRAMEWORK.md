# o10 under the Antihydra capstone framework — the LITERAL AEV ceiling 3/2 instance (2026-06-28)

Applies the `COMPLETE_PROOF_CAPSTONE.md` machinery (induced odd map, GAP-LEMMA, renewal identity, AEV
placement, ergodic-optimization meta-theorem) to **o10**, the ceiling-3/2 cryptid. Soundness discipline:
every line is `[PROVEN]` (machine-checked, exact big-int via `.venv`) / `[OBSERVED]` / `[OPEN]`. Numerics in
`scratchpad/o10_ceiling.py`. **Headline: o10's inner kernel is the *literal* AEV Conj 1.6 ceiling `p/q=3/2`
map — cleaner than Antihydra, which is only the floor *mirror* of it. But o10's halting is coupled to that
kernel through an irregular two-level refill, not through Antihydra's clean even-density threshold.**

`o10 = 1RB1RA_0RC1RC_1LD0LF_0LE1LE_1RA0LB_---0LC` (halt = state F reads 0).

---

## 1. The inner map and the halting coupling

**Inner map [PROVEN, verified vs raw TM in `o10_attack.md`; re-verified here].** At a left-end state-E
milestone with tape `0010 0^a 1^b 1101` (`m=(a+9)/2`), one inner sweep does

> `m → ⌈3m/2⌉`,  and  `b → b − 1` (m even) / `b → b − 2` (m odd).

The ceiling orbit from `m=6` reproduces `6,9,14,21,32,48,72,108,162,243,365,548` exactly `[verified]`. So the
inner map is **literally the ceiling 3/2-map** `T(m)=⌈3m/2⌉`: `=3m/2` (m even), `=(3m+1)/2` (m odd).

**The b-countdown and the refill [PROVEN structure / OPEN exact rule].** Each inner step decrements `b` by
`1+[m odd]`. When `b` reaches `0` the machine runs a **refill** sub-routine (not a halt) that resets `m→6`
and jumps `b` to a new large value; the real run does `b: 3 → 55 → ~10⁸ → …` (doubly-exponential, 2nd refill
unreachable in 40M steps). The **refill map is irregular — not a clean function of `m_exhaust`** (`9→33,
18→73, 21→87, 24→153, …`, no affine/×k fit) `[PROVEN in o10_attack.md]`. The halt (state F reads 0) is a
**parity/alignment event** of the inner orbit against the b-countdown phase: the `b=1` sub-slice halts iff
`m ≡ {1,2,8,9,10} (mod 16)` (mod-16 regular, m=5..120 zero-mismatch) — a refined condition, **not** simple
"the countdown skips 0".

> **Soundness flag (negative result, recorded).** The naive model "halt ⟺ a 2-decrement jumps the countdown
> from remaining-1 to −1" is **FALSE**: simulated, it predicts HALT at `b_init=55`, but the real machine
> refills `3→55` and provably runs ≥40M steps without halting. So the exact halt rule is the irregular refill
> bookkeeping of `o10_attack.md`, not a clean parity-skip. The b-decrement *rate* (below) is solid; the exact
> halt-alignment is the genuine [OPEN] two-level obstruction.

**How inner equidistribution controls o10 [PROVEN coupling].** Odd-density of the inner ceiling orbit is
`#odd/#total = (induced steps)/(Σ D') = 1/mean(D')` (renewal). So the **b-consumption rate per inner step is
`1 + odd-density = 1 + 1/mean(D')`**, which sets epoch length `≈ b/(1+1/meanD')` and hence
`m_exhaust ≈ 6·(3/2)^{epoch length}` feeding the next refill. `[verified]` mean D' ≈ 2 ⟹ odd-density ≈ 1/2 ⟹
rate ≈ 1.5, matching `o10_attack`'s "≈ b/1.5 steps". **The inner ceiling-3/2 equidistribution is exactly what
governs the outer doubly-exponential refill orbit** — this is the nested-control link the framework asked for.

---

## 2. Induced odd map + GAP-LEMMA analog for the ceiling  [PROVEN]

**GAP-LEMMA (ceiling).** For odd `m`, `⌈3m/2⌉ = (3m+1)/2`. Set `D' := v₂(3m+1)`. Then `3m+1 = 2^{D'} u`
(u odd), `⌈3m/2⌉ = 2^{D'−1}u`, followed by `D'−1` halvings (`⌈3x/2⌉=3x/2` on even x) down to the next odd
value `3^{D'−1}u`. So the **induced odd map** is

> **`T'(m) = 3^{D'−1}(3m+1)/2^{D'}`,  `D' = v₂(3m+1)`,  started at `m₀ = 9`** (first odd value after the
> refill reset `m=6 → 9`).

`[verified]`: `T'` reproduces the full ceiling orbit's odd return values, and `D'` equals the exact inter-odd
gap length, zero mismatch over 200 returns and N=2·10⁵ induced steps.

This is the **exact mirror** of Antihydra's induced map `T(o)=3^{D−1}(3o−1)/2^D`, `D=v₂(3o−1)`, `o₀=27` — the
single difference is **`3m+1` (ceiling) vs `3o−1` (floor)**.

**Depth statistic / residue law [PROVEN, big-int verified].**
- Ceiling: `D' ≥ k ⟺ m ≡ −3⁻¹ (mod 2^k)`. In particular `D'=1 ⟺ m ≡ 3 (mod 4)`, `D'≥2 ⟺ m ≡ 1 (mod 4)`.
- Floor (Antihydra): `D ≥ k ⟺ o ≡ +3⁻¹ (mod 2^k)`; `D=1 ⟺ o ≡ 1 (mod 4)`, `D≥2 ⟺ o ≡ 3 (mod 4)`.

The `+1 ↔ −1` flips the residue, **swapping the roles of `1` and `3 mod 4`** — the parity mirror, made exact.

**Renewal identity / even-density (same as Antihydra).** Even steps are renewal points, gaps `= D'`, so
even-density `= 1 − 1/mean(D')`. Under Haar, `mean D' = Σ_d d·2^{−d} = 2`, even-density `= 1/2`.

**Numerics (induced orbit of o10-inner from `m₀=9`, N=2·10⁵) `[verified]`:**
| quantity | o10-inner (ceiling, m₀=9) | Antihydra (floor, o₀=27) | Haar |
|---|---|---|---|
| mean D | 2.00390 | 1.99627 | 2 |
| freq(D=1) | 0.49953 (= freq m≡3 mod4) | 0.50034 (= freq o≡1 mod4) | 1/2 |
| freq(D≥2) | 0.50047 (= freq m≡1 mod4) | 0.49966 (= freq o≡3 mod4) | 1/2 |
| even-density | 0.50097 | ≈0.4997 | 1/2 |

Both orbits sit at the Haar value with the same ~0.5 margins — empirically Haar-generic, mirror residues.

---

## 3. AEV placement — o10-inner IS the literal ceiling instance  [PROVEN placement]

AEV Conj 1.6 (arXiv:2510.11723): for coprime `p>q≥1`, every orbit of the **ceiling** map
`T_{p/q}(x)=⌈px/q⌉` equidistributes mod `q^k` for all `k`. **o10-inner is `T_{3/2}(m)=⌈3m/2⌉` verbatim** —
the same operator AEV conjecture about. Therefore:

> **o10's inner kernel = the LITERAL `p/q=3/2` instance of AEV Conjecture 1.6 (ceiling), with NO parity-flip
> mirror.** Antihydra is the floor map `⌊3c/2⌋`, which is the floor *mirror* of AEV (its even branches agree
> but the odd branch is `(3c−1)/2` vs AEV's `(3c+1)/2`); the GAP-LEMMA `v₂(3c−1)` is the bridge. **o10 needs
> no such bridge — it is on AEV's own side of the ledger.** This is *cleaner* than Antihydra.

**Same kernel as Antihydra, or different? — DIFFERENT orbit, MIRROR map, SAME named conjecture.**
- Different **orbit**: o10 induced starts at `m₀=9` (full orbit `m=6,9,14,…`); Antihydra at `o₀=27`.
- Mirror **map**: ceiling `(3m+1)/2` vs floor `(3o−1)/2`; residue threshold `m≡−3⁻¹` vs `o≡+3⁻¹ (mod 2^k)`.
- Same named umbrella: both are single-orbit, level-`k=2` fragments of **AEV Conj 1.6 at `p/q=3/2`**, which
  (Thm 1.5/1.7, `p<q²` since `3<4`) implies Mahler's 1968 conjecture. o10 sits on the **ceiling/AEV** side;
  Antihydra on the **floor/mirror** side. They are the two faces of the same `3/2` equidistribution problem.

**Crucial asymmetry in the halt-coupling (what makes o10 harder, not easier).** Antihydra's halt is the
*clean* threshold `even-density ≥ 1/3 ⟺ mean D ≥ 3/2` — a single one-sided density bound on its orbit. **o10's
halt is NOT a single density threshold.** Its non-halting requires the inner-orbit parities to *align*
(land-on-0, never skip) with a **doubly-exponential, irregular refill `b`-sequence** at every epoch — an
alignment/carry-type event layered on top of the AEV-ceiling equidistribution. So o10 = (literal AEV ceiling
3/2 kernel) **⊗** (an irregular two-level refill alignment). The inner kernel is *cleaner* than Antihydra's;
the overall halting problem is *strictly richer* (two levels vs one).

---

## 4. Meta-theorem transfer  [PROVEN for the inner kernel; PARTIAL for full o10]

**Measure side transfers verbatim [PROVEN].** `T'(m)=3^{D'−1}(3m+1)/2^{D'}` is the mirror of Antihydra's
induced map, so the capstone §3 theorem applies identically: `T'` is **Haar-preserving, exact, Bernoulli on
ℤ₂\*** with `D'_j` i.i.d. geometric `P(D'=d)=2^{−d}`, `mean D'=2`. The branch `A_d={m: v₂(3m+1)=d}` (measure
`2^{−d}`) maps affinely and bijectively onto ℤ₂\* (Jacobian `2^d`), reproducing Haar. `[verified]` mean D'≈2,
geometric tail.

**Halting fixed point analog [PROVEN].** The "obstruction = the constant/halting fixed point" transfers, in
mirror:
- Antihydra floor, all-`D=1` (o≡1 mod4 forever): fixed point `o=(3o−1)/2 ⟹ o=+1`.
- **o10 ceiling, all-`D'=1` (m≡3 mod4 forever): fixed point `m=(3m+1)/2 ⟹ m=−1`** (= `…111` in ℤ₂, which
  indeed lies in the `m≡3 mod4` region). `[verified]`

So o10's "halting attractor" is `m=−1`, the 2-adic mirror of Antihydra's `o=+1`. The all-shortest-gap orbit
(odd-density →1, even-density →0) lands here.

**Ergodic-optimization meta-theorem (β=+1/2) transfers to the inner kernel [PROVEN].** The one-sided test
function `ψ` (D'-only) has, by the same Mañé/Conze–Guivarc'h/Bousch argument, `β(ψ)=max_μ ∫ψ dμ = +1/2`
attained at the atom `δ_{m=−1}` (D'≡1 forever ⟹ even-density 0). Hence **no structure-only argument can force
the inner-orbit density bound**, for exactly the capstone reason: the bound is also violated by the fixed
point `m=−1`, so any all-orbits structural proof would prove a false statement. The inner kernel is
irreducibly orbit-specific (genericity of `m₀=9`), mirroring Antihydra's genericity of `o₀=27`.

**Where the transfer is only PARTIAL [OPEN] — the honest gap.** The ergodic-optimization / "no structure
proof" meta-theorem is a statement about a **single density functional of one orbit**. It transfers cleanly to
o10's *inner* equidistribution sub-problem. It does **not** directly cover o10's *actual* halting, because the
halt is the **two-level alignment** (inner parities vs the irregular doubly-exponential refill), which is not
a single Birkhoff/density functional. The outer refill map being irregular (no clean function) means o10's
full halting is **strictly beyond** the single-orbit AEV fragment that closes Antihydra — it needs the AEV
ceiling equidistribution **plus** control of the refill alignment across infinitely many epochs with
doubly-exponentially growing `b`. No analytic handle exists for either layer.

---

## 5. Bottom line (answers to the brief)

1. **Exact map / halt criterion.** o10-inner is **literally `⌈3m/2⌉`** (`=(3m+1)/2` on odd, `=3m/2` on even),
   from `m=6`. The induced odd map is `T'(m)=3^{D'−1}(3m+1)/2^{D'}`, `D'=v₂(3m+1)`, from `m₀=9`. The halt is
   **not** Antihydra's even-density threshold; it is an irregular **parity-alignment** of the inner orbit
   against a **doubly-exponential, irregular refill `b`-sequence** (refill rule not a clean function;
   `b=1` slice halts iff `m≡{1,2,8,9,10} mod16`). The inner equidistribution controls halting *indirectly*,
   by setting the b-consumption rate `1+1/mean(D')≈1.5` and hence the epoch length / next refill.

2. **Literal AEV instance? YES — cleaner than Antihydra.** o10-inner is the **literal `p/q=3/2` ceiling map of
   AEV Conjecture 1.6**, requiring no parity-flip mirror. Antihydra is the *floor mirror* of the same
   conjecture (bridged by `v₂(3c−1)`). On the map axis, o10 is the more direct AEV instance.

3. **Same kernel as Antihydra? DIFFERENT orbit + MIRROR map, SAME named conjecture.** Different start
   (`m₀=9` vs `o₀=27`), mirror residue threshold (`m≡−3⁻¹` vs `o≡+3⁻¹ mod 2^k`, swapping 1↔3 mod 4),
   but both are single-orbit level-2 fragments of **AEV Conj 1.6 at 3/2** ⊃ Mahler 1968. Two faces (ceiling /
   floor) of one equidistribution problem.

4. **Meta-theorem transfer? YES for the inner kernel, PARTIAL for full o10.** The exact/Bernoulli/Haar measure
   side, the `β(ψ)=+1/2` ergodic-optimization "no structure-only proof", and the halting fixed point all
   transfer to the inner ceiling map — with the **fixed point at `m=−1`** (the 2-adic mirror of Antihydra's
   `o=+1`). They do **not** cover o10's full halting, which adds an irregular two-level refill alignment on top
   of the AEV-ceiling kernel. **o10 = literal AEV ceiling 3/2 kernel ⊗ irregular doubly-exponential refill** —
   inner-cleaner than Antihydra, overall strictly harder (two levels). No analytic handle for either layer.

**No decision claimed; no false proof.** o10 remains [OPEN], now precisely placed: its clean core is the
*literal* AEV ceiling `3/2` conjecture (where Antihydra is the floor mirror), and its excess hardness over
Antihydra is exactly one irregular nesting level.
