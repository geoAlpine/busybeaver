# Antihydra kernel ↔ AEV (arXiv:2510.11723) — exact correspondence + minimal input (2026-06-28)

Source read this session: AEV pp.1–16 (PDF), abstract + Conj 1.2 / 1.4 / 1.6, Thm 1.5 / 1.7,
Prop 3.10 / 3.13, §4 numerics. Our side: `KERNEL_FINAL.md`, `SESSION_2026-06-28_UNITPART.md`,
`PROOF_STATUS.md`. Every line labelled. Zero false proofs.

---

## 0. What AEV actually is (verbatim facts, [PROVEN]/[CONJ] as in the paper)

- **Map.** `T_{p/q}(x) := ⌈(p/q)·x⌉` (CEILING). For `p/q=3/2` (p.14, eq. before §4) they write it as
  `T_{3/2}(x) = (3x+1)/2` if `x` odd, `3x/2` if `x` even. (Collatz `F` differs only in the even branch: `x/2`.)
- **Normal (Def, p.3).** An infinite word `w` over a `d`-ary alphabet is *normal* if for **all** `l≥1`,
  **each** of the `d^l` length-`l` factors occurs with limit frequency **exactly `1/d^l`**. ⇒ FULL,
  TWO-SIDED equidistribution (an equality at every level, every factor), not a one-sided bound.
- **Conjecture 1.2 [CONJ].** For all coprime `p>q≥1` and all seeds: `wmax_{p/q}(u)` is normal over
  `{p−q,…,p−1}`, and `wmin_{p/q}(u)` (u≠ε) is normal over `{0,…,q−1}`.
- **Conjecture 1.6 [CONJ] (the form we need).** For **every** `n∈ℕ_{>0}` and **every** `k`, the integer
  sequence `(T^l_{p/q}(n))_{l∈ℕ}` is **equidistributed in the residue classes mod `q^k`** — i.e. each of
  the `q^k` classes has frequency **exactly `q^{-k}`** (their def. of "equidistributed", p.4). Two-sided,
  all `k`, all `n`.
- **Theorem 1.7 [PROVEN].** Conj 1.2 ⇔ Conj 1.6 (via Lemma 3.1: `val(u·wmin(u,l)) = T^l(val(u))`, p.9–10).
- **All other "results" are equivalences or one-way implications OF the conjecture, or numerics:**
  Thm 1.5 [PROVEN] Conj 1.2 ⇒ no `Z_{p/q}`-numbers (`p<q²`); Prop 3.10 [PROVEN] Conj 1.2 ⇒ Akiyama
  triple-expansion; Prop 3.13 [PROVEN] Conj 1.2/1.6 ⇒ Dubickas–Mossinghoff "4/3" termination.
  §4 is **purely numerical** (richness threshold; deviation-from-uniformity / discrepancy `D_{w,l}`).
- **Unconditional frequency/density results in AEV: NONE.** The only unconditional non-trivial facts cited
  are Dubickas's **complexity** bounds (1.3) `liminf p_w(l)/l ≥ log q/log(p/q)` and (1.4) `liminf p_w(l)/l>1`
  (`p<q²`) — these count **distinct subwords** (richness), NOT their **frequencies**. They give nothing on
  density. AEV present the equidistribution itself as conjecture supported only by experiments.

---

## 1. Exact dictionary kernel ↔ AEV

| our object | AEV object |
|---|---|
| Antihydra map `c_{n+1}=⌊3c_n/2⌋`, `c₀=8` | the **floor mirror** of `T_{3/2}(x)=⌈3x/2⌉`. Even branch identical (`3x/2`); odd branch `(3x−1)/2` vs AEV's `(3x+1)/2`. Same genericity principle; **not literally conjugate** (the ±1 flips odd-step parity), which is exactly why the bookkeeping must go through `v₂(3o−1)`. |
| induced odd map `T(o)=3^{D−1}(3o−1)/2^D`, `D=v₂(3o−1)`, `o₀=27` | the **return map to odd integers** of the floor-`T_{3/2}` orbit (it skips the even intermediate steps; `D` = length of the even run after an odd step). A sub-object of AEV's full orbit `(T^l(n))_l`. |
| even-density `E_n/n` of `c`-orbit (the halting quantity) | the **parity (mod 2, k=1) frequency** of the floor-`T_{3/2}` orbit: `freq(c_n even)`. |
| `freq(o≡3 mod 4)` along induced orbit | the **mod-4 (k=2)** residue frequency of the induced orbit (the first non-trivial level: `o` is always odd, so mod 2 is trivial). |
| `mean D = Σ_{k≥1} freq(o≡3⁻¹ mod 2ᵏ)` | the full **mod-`2^k`, all-`k`** residue profile of the induced orbit — i.e. AEV Conj 1.6's residue data for `q=2`, restricted to the odd return-orbit. |
| **non-halt ⇔ liminf even-density ≥ 1/3 ⇔ liminf mean D ≥ 3/2** | a **ONE-SIDED, single-orbit** statement about AEV's residue frequencies. |

**On "normality" two-sided vs our one-sided.** AEV "normal"/"equidistributed" = each class has frequency
**exactly `q^{-k}`** (equality). Our kernel needs only **`≥`** at one place. So our kernel does NOT include,
and is strictly below, AEV normality. (Verbatim def confirms: equality at every level, every factor.)

---

## 2. The minimal AEV-type input that closes the kernel (ONE lemma)

Our [PROVEN] chain (renewal identity + the `mean D = Σ_k freq(o≡3⁻¹ mod 2ᵏ)` expansion, `INDUCED_MAP` E2):
`mean D = 1 + freq(o≡3 mod 4) + Σ_{k≥3}(…≥0)`, so `mean D ≥ 3/2 ⟸ freq(o≡3 mod 4) ≥ 1/2`.

> **Lemma (minimal input ⇒ Antihydra non-halt) [CONDITIONAL].**
> Let `o₀=27`, `o_{n+1}=T(o_n)` the induced odd 3/2-map. **IF**
> > `liminf_{N→∞} (1/N)·#{ n<N : o_n ≡ 3 (mod 4) } ≥ 1/2`
> (together with the finite check `balance_n ≥ 0` for `n ≤ N₀`, already verified by bbchallenge),
> **THEN the Antihydra Turing machine does not halt.**

Equivalent one-sided forms (all [PROVEN]-equivalent via renewal):
`liminf freq(c_n even) ≥ 1/3` (the k=1 / mod-2 statement on the `c`-orbit directly) ⇔ `liminf mean D ≥ 3/2`.

**Placement of this input inside AEV.** It is exactly the
**`p/q=3/2`, `q=2`, single residue level `k=2` (mod 4), ONE-SIDED (`≥½`), SINGLE-ORBIT (`o₀=27` / `c₀=8`)
fragment of AEV Conjecture 1.6** (floor mirror). Full AEV Conj 1.6 (all `k`, two-sided `=q^{-k}`, all `n`)
gives `freq(o≡3 mod4)=½` and `mean D=2`, closing it with room to spare. We need a vanishingly small slice
of it.

---

## 3. Does AEV prove any fragment of this minimal input? — NO. [PROVEN: it does not]

- AEV's only [PROVEN] results are: Thm 1.7 (1.2⇔1.6, an equivalence), Thm 1.5 / Prop 3.10 / Prop 3.13
  (one-way implications *from* the unproven Conj 1.2), and the structural Props 2.2/2.6/2.7. **None** asserts
  any residue frequency, for any orbit, even one-sided.
- §4 is numerical only (richness threshold, discrepancy `D_{w,l}`) — evidence, not proof.
- The unconditional facts (Dubickas 1.3/1.4) are **complexity (subword-count)** bounds, on the wrong axis
  (richness ≠ frequency), and give no density.
- The "weaker than normality" statement AEV *do* highlight — "every minimal word contains the letter 0 at
  least once" (suffices for Akiyama, p.13) — is an **existence** statement for a **different** downstream
  problem, is itself **unproven**, and does not bound any frequency.

⇒ **AEV proves zero fragment of our minimal input, and gives no one-sided density (not even `liminf>0`) for
any specific orbit.** This **confirms** `WALLB_EFFECTIVE` / `KERNEL_FINAL` §4: no published result yields
`liminf` even-density `>0` for a specified 3/2/Syracuse orbit. **AEV does not change that** — it is, if
anything, an independent statement that this is open (their headline object is a conjecture backed only by
numerics).

---

## 4. Equivalent to, or strictly weaker than, AEV's 3/2 conjecture? — STRICTLY WEAKER (triple fragment)

Our kernel is **strictly weaker** than AEV Conj 1.6 (3/2) on **three independent axes** simultaneously:

1. **One-sided vs two-sided.** Kernel needs `freq(o≡3 mod4) ≥ ½` (or `even-density ≥ ⅓`). AEV needs the
   equality `= ½` (resp. the full equidistribution value at every level). A `≥` is strictly below a `=`.
2. **One residue level vs all levels.** Kernel needs only `k=2` (mod 4). AEV asserts all `k` (mod `2^k`).
3. **One orbit vs all orbits.** Kernel is about the single orbit `o₀=27` (`c₀=8`). AEV asserts it for
   **every** `n∈ℕ_{>0}`.

So it is **NOT equivalent** to AEV's 3/2 conjecture — it is a genuine sub-fragment.

**Is the weaker version stated/addressed in AEV?** **No — unaddressed.** AEV state only the full conjecture
(all `k`, two-sided, all `n`); they never isolate, weaken to one-sided, restrict to one orbit, or restrict to
low `k`. There is no named sub-conjecture at our level anywhere in the paper or (per `KERNEL_FINAL` §4
sweep) the literature. Our minimal input is therefore **open and unaddressed**: strictly weaker than AEV
(so AEV closes it), yet strictly stronger than everything proven (FLP support/spread, Tao ensemble/log-
density, Krasikov–Lagarias counting, Dubickas complexity — none give per-orbit frequency).

**Caveat to state honestly (floor vs ceiling).** AEV's Conj 1.6 is literally for the **ceiling** map
`⌈3x/2⌉`; Antihydra is the **floor** map `⌊3x/2⌋`. The two are the natural floor/ceiling mirror of one
genericity principle (AEV themselves frame `T_{3/2}` and the 3x+1 link, p.14), but they are **not literally
the same orbit** (the odd-branch ±1 flips parity). Our PROVEN GAP-LEMMA absorbs this by passing to the
arithmetic invariant `D=v₂(3o−1)` (the floor convention's natural quantity). So precisely: our kernel is the
described triple-fragment of the **floor mirror** of AEV Conj 1.6 — a statement AEV's framework covers in
spirit but does not literally state.

---

## 5. Bottom line (deliverables)

- **Dictionary.** Antihydra even-density = mod-2 parity frequency of the floor-`T_{3/2}` orbit; induced
  `freq(o≡3 mod4)` = its mod-4 (k=2) residue frequency; `mean D` = its full mod-`2^k` residue profile
  (`q=2` AEV Conj 1.6 data, on the odd return-orbit). Non-halt ⇔ one-sided `≥` of these.
- **Minimal lemma.** `liminf (1/N)#{n<N: o_n≡3 mod4} ≥ ½` (≡ `liminf even-density ≥ ⅓`) + finite check ⇒
  non-halt. = one-sided, `k=2`, single-orbit fragment of AEV Conj 1.6 (floor mirror).
- **AEV proves a fragment?** No — AEV has zero unconditional residue-frequency results; all proven content is
  equivalences/implications-of-the-conjecture + numerics.
- **One-sided density for the specific orbit from AEV's proven part?** None. Confirms WALLB_EFFECTIVE; AEV
  does not move the wall.
- **Equivalent or weaker?** **Strictly weaker** (one-sided ∧ single-level `k=2` ∧ single-orbit), and the
  weaker version is **unaddressed/open** in AEV.
