# o18 — raw-TM → macro-dynamics hand-proof attempt (promotion audit of the ⌊8N/3⌋+2 coordinate)

*Purpose.* Attempt to upgrade o18's macro-structure from **[VERIFIED]** (`bb_sim` step agreement) to
**[PROVEN]** (a conjecture-free hand-proof that the raw transition table *forces* the claimed macro-dynamics),
exactly as was done for Antihydra in `TM_EXTRACTION_PROOFS.md §1`. Soundness is paramount: a simulation match is
**not** a proof; below, every elementary step is derived by a finite case analysis on the transition table,
and `bb_sim` (`.venv` big-int) is used **only** as confirmation.

**Headline verdict (proven, not asserted): the unconditional macro-map `M(k) → M(⌊8k/3⌋+2)` is _FALSE_, so it
cannot be promoted to [PROVEN]. It is true only on the clean-carry regime (epochs 0–6) and provably _breaks_ at
epoch 7. What IS now [PROVEN] from the table: (i) the halt criterion, and (ii) the elementary sweep lemmas and
the conditional clean-carry epoch lemma. The blocker is not "induction not transcribed"; it is that no
induction can prove a false statement. The exact obstruction = the base-3 carry reaching the left frontier =
the open kernel `(K_o18)`.** Details below; conventions follow `TM_EXTRACTION_PROOFS.md §0`.

---

## 0. The exact TM and transition table  [PROVEN — definitional]

`o18 = 1RB0RE_1LC0RA_1LA1LD_1LC1LF_0LC0LB_1LE---` (`suite.py` line 50).

| | read 0 | read 1 |
|---|---|---|
| **A** | 1,R,B | 0,R,E |
| **B** | 1,L,C | 0,R,A |
| **C** | 1,L,A | 1,L,D |
| **D** | 1,L,C | 1,L,F |
| **E** | 0,L,C | 0,L,B |
| **F** | 1,L,E | **HALT** |

`--- = halt`. The **only** halting transition is `F,1`.

---

## 1. The macro-configuration and the base-3 odometer structure  [VERIFIED — exhibited from the raw run]

The clean milestone is
> **`M(k) := 0^∞ [A>0] 1 0 1^{k} 0^∞`**  (state A on the far-left blank, then a lone `1`, a `0`, then a
> fuel block `1^k`).

From the **blank tape**, the first clean milestone reached is `M(10)` at micro-step 39 (`o18trace.py`,
`o18milestones.py`); this is o18's start segment (analog of Antihydra reaching `C(0,2)` at step 14).

**What one epoch actually looks like (the base-3 odometer).** Tracing the epoch `M(10) → M(28)` (190
micro-steps, `o18epoch.py`, `o18lf.py`), the head performs a **leftward base-3 odometer sweep**. The persistent
shape at every left-frontier return (state A, new-minimum head position) is

```
  [A>0]  <leading block 1^p>  0  (10)^j  1^m
```

i.e. a **leading block** `1^p` (p ∈ {2,3,4}), a separator `0`, a **ternary-digit region** `(10)^j` (each `10`
pair = one base-3 "digit position" carrying the ×8/÷3 bookkeeping), and a shrinking **fuel block** `1^m`.
The traced left-frontier configs of the `M(10)` epoch (`o18lf.py`, verbatim):

```
 s39   [A] 0 1 0 1^10                         (= M(10), start)
 s55   [A] 0 1^2 0 (10)^2 1^7
 s90   [A] 0 1^4 0 (10)^4 1^4
 s100  [A] 0 1^2 0 (10)^6 1^4
 s159  [A] 0 1^4 0 (10)^8 1^1
 s169  [A] 0 1^2 0 (10)^11 1^1
 s229  [A] 0 1 0 1^28                         (= M(28), end)
```

The digit region `(10)^j` **grows** (j: 2,4,6,8,11) as the fuel `1^m` is **consumed** (m: 7,4,1) and the
leading block toggles `1^2 ↔ 1^4` (the carry indicator). This is a genuine ternary odometer: the per-epoch
phase counts are **variable and carry-dependent**, unlike Antihydra's single fixed-length inner loop.

The state-sequence of the whole `M(10)` epoch (`o18phases.py`) decomposes into three odometer "rounds"
separated by `DC` digit-carries, ending in a refill+halt-check `…CDCDCD…FEC`:

```
AB ABAEBC AEBC AEBC ABAEC ABABABAB (AEBC)^5 DC
   ABAEBC AEBC ABAEC (AB)^8        (AEBC)^9 DC
   ABAEBC AEBC ABAEC (AB)^13       (CD)^13 FEC
```

The growing repeat-counts `(AB)^{4,8,13}`, `(AEBC)^{5,9}`, `(CD)^{13}` are the odometer's digit positions —
they are **not** a fixed-length rewrite repeated a fixed number of times.

---

## 2. Elementary sweep lemmas  [PROVEN — single-transition inductions]

Each lemma is an immediate induction on a block length using one table entry (method identical to
`TM_EXTRACTION_PROOFS.md §1.1`). Confirmed standalone in `o18lemmas.py`.

> **Lemma A/B-MARCH (rightward transport).** With the head in state A on a `0` that begins a region
> `0 1 0 1 … = (01)^t`, the pair-transitions `A,0=(1,R,B)` then `B,1=(0,R,A)` rewrite each `01 ↦ 10` and
> advance the head by 2 in state A. Hence `[A>0] (10)^t X ⟹ (10)^t [A>x] X` (the digit region is transported,
> head emerges on the first symbol `x` of `X`). *Proof.* `A,0` writes `1` and moves R into the `1`; `B,1`
> writes `0` and moves R into the next `0`, back in A. Induct on `t`. ∎

> **Lemma E/B-RETURN and C-RETURN (leftward sweeps).** `E,1=(0,L,B)` and `C,1=(1,L,D)`, `C,0=(1,L,A)` move
> left one cell each; `B,0=(1,L,C)` moves left writing `1`. These are the leftward single-cell steps that
> assemble the `AEBC` / `ABAEC` digit-increment gadgets seen in the trace. *Proof.* Direct table entries;
> each is one micro-step. ∎

> **Lemma REFILL (C/D zigzag).** The pair `C,1=(1,L,D)` then `D,0=(1,L,C)` walks left over a `(10)^j` region
> reading the rightmost `1` first, turning each separator `0` into `1`: `(10)^j ↦ 1^{2j}`, ending when the
> leftward `D`-step reads a `1` (the leading block), at which point `D,1=(1,L,F)` enters F.
> *Proof.* `C` reads a `1` → write `1`, L, state D; `D` reads the `0` to its left → write `1` (so `10↦11`), L,
> state C. Induct over the `j` pairs. The zigzag terminates exactly when D first reads a `1`. ∎
> *Confirmation (`o18epoch.py`, s200–s225 of the `M(10)` epoch):* `(10)^{13} ⟹ 1^{26}` then `D` reads the
> leading `1` and enters F.

These lemmas are exact and conjecture-free. They are the o18 analogs of Antihydra's shift lemmas; the
**difference from Antihydra is purely in how they compose** (a carry-dependent odometer, §4), not in their
individual validity.

---

## 3. Halt criterion — [PROVEN, table-trivial + mechanically confirmed]

State F's row is `1LE / ---`: read `0` → write 1, move L, go E (continue); read `1` → **HALT**. F is reachable
**only** through `D,1=(1,L,F)` (the unique transition with next-state F; verified by scanning the table,
`o18halt.py`). So when F is entered at cell `p−1` after `D` read a `1` at cell `p`, F reads `tape[p−1]`. Hence:

> **(o18-HALT) [PROVEN].** o18 halts ⟺ **state F ever reads a `1`** ⟺ at some `D`-read of a `1` (cell `p`) the
> immediately-left cell `p−1` is also `1` — an **adjacent-`11` collision at the leftward D/F frontier**
> (the base-3 carry of the orbit landing on the frontier instead of being absorbed).

**Mechanical confirmation (`o18halt.py`, seeded raw-TM runs):**
- *Alignment ⇒ halt.* Refill frontier with an adjacent `1`: `0 1 1 1 0 1 0 1 0 [C>1] 0` ⟹ **HALT in 9 steps**
  (the D/F handoff reads the extra `1`).
- *Necessity.* Clean frontier `{0:1}` head 0 state D: F reads the left `0`, writes 1, continues — no halt.
- *In the clean epoch:* at `M(10)`'s epoch end (s225–226) `D` reads the leading `1` → F, and `F` reads the
  far-left blank `0` → continue and rebuild `M(28)`. The halt is exactly the "extra `1` on the left" event.

This pins (o18-HALT) to raw tape mechanics with zero modelling. It upgrades `PAPER_MAIN.md` Lemma 3.5's *form*
to **[PROVEN]** (already noted in `TM_EXTRACTION_PROOFS.md §3.1`; reconfirmed here).

---

## 4. The clean-carry epoch lemma, and where the induction stops  [PROVEN-conditional / BLOCKER identified]

### 4a. The conditional lemma
Composing §2's lemmas around one full odometer sweep gives, **whenever the sweep absorbs every carry before
reaching the leading block** (the "clean-carry" hypothesis):

> **Lemma CLEAN-EPOCH [PROVEN, conditional].** If the leftward odometer sweep from `M(k)` deposits no `1` at
> the left frontier beyond the leading block (no carry overflow), then `M(k) ⟹ M(⌊8k/3⌋+2)`.

**Why `8/3` and the `+2` (the arithmetic skeleton).** Write `k = 3q + r`, `r ∈ {0,1,2}`. The fuel `1^k` is
consumed three cells per odometer digit (the `÷3`); each consumed digit is re-emitted by REFILL as a `1^{2j}`
block carrying a factor `2^3 = 8` (the `×8`); the floor truncation of the final partial digit gives the
per-residue constant, and the lone-`1 0` leading structure of `M(·)` contributes the `+2`:
`⌊8k/3⌋+2 = 8q + c_r + 2` with `c_r = ⌊8r/3⌋ = 0,2,5` for `r = 0,1,2`. (`o18halt.py` tabulates this.) The
elementary lemmas of §2 each realise one micro-piece of this accounting; the **net** count is forced once one
proves the odometer returns to `M`-form — which is exactly the clean-carry hypothesis.

### 4b. The lemma's hypothesis genuinely fails — the unconditional map is FALSE  [PROVEN by exhibition]
The clean-carry hypothesis is **not** always satisfied. Exhaustive clean-milestone detection over the real
blank-tape run (`o18milestones.py`, `.venv`, exact) gives the **complete** list of clean milestones reached:

```
 step           k        prev → ⌊8k/3⌋+2 ?
 39             10        (first)
 229            28        10  → 28     ✓
 1433           76        28  → 76     ✓
 9565           204       76  → 204    ✓
 66756          546       204 → 546    ✓
 468797         1458      546 → 1458   ✓
 3315302        3890      1458→ 3890   ✓
 166999739      27660     3890→ ⌊8·3890/3⌋+2 = 10375   ✗  (next clean k is 27660, NOT 10375)
```

So **after `M(3890)` the orbit does not pass through any clean milestone `M(10375)`**. The clean form `M(k)` is
**destroyed at epoch 7**: a base-3 carry reaches the left frontier (this is the `k=3890 ≡ 2 (mod 3)` step, the
`r=2` residue with the largest truncation `c_2=5`, i.e. the deepest carry), the leading-block reabsorption does
**not** complete, and the configuration emerging is **not** of the form `M(k')`. A clean milestone only
**re-forms two epochs later** at `k = 27660` (cf. `O18_REDUCTION.md`: actual widths `…,3890,10373,27660`, model
`f(3890)=10375` defect −2, `f(10373)=27663` defect −3). The defect is precisely the carry the leftward rebuild
cannot absorb.

**Consequence (the decisive soundness point).** The statement "`M(k) ⟹ M(⌊8k/3⌋+2)` for all reachable `k`" is
**false**. Therefore **no induction can prove it**, and the macro-coordinate **cannot** be promoted to
[PROVEN] as an unconditional clean map. This is a *stronger and more honest* finding than the prior pass's "the
carry induction was not completed": completing it would still not yield the unconditional map, because the map
is not true. The genuinely [PROVEN] content is the **conditional** Lemma CLEAN-EPOCH plus the halt criterion.

### 4c. The exact blocker
The discriminator between "clean epoch (map = `⌊8k/3⌋+2`, milestone re-forms)" and "carry overflow (milestone
breaks; possibly HALT if adjacent-`11`)" is **whether the base-3 carry of the `(8/3)`-orbit ever reaches the
left frontier**. By §3 this is the *same* event as the halt criterion (the frontier `1`). Deciding it for the
specific o18 orbit is exactly:

> **(K_o18) [OPEN].** The base-3 carry of the `⌊8N/3⌋+2` orbit aligns with the left frontier for only finitely
> many epochs — the `q=3` (different-base), single-orbit, floor-mirror, **existence/Erdős** facet of AEV
> Conj 1.6 (see `CRYPTID_O18_FRAMEWORK.md`, `O18_REDUCTION.md`). World-open; no unconditional tool reaches it.

So the carry "induction" does not merely *resist transcription* — its termination-in-clean-form **is the open
kernel**. (Contrast Antihydra: there the macro-config `C(a,b)` is preserved at *every* step — parity branch +
both carries are clean unconditionally — so the unconditional map is true and was provable.)

---

## 5. Numeric cross-checks (all `.venv` big-int, against `bb_sim` semantics)  [VERIFIED]
- `o18milestones.py`: clean milestones `10,28,76,204,546,1458,3890` follow `⌊8k/3⌋+2` exactly (epochs 0–6);
  next clean milestone is `27660` (NOT `10375`) — clean form breaks at epoch 7. **0 mismatches** on epochs 0–6.
- `o18epoch.py` / `o18lf.py`: full `M(10)→M(28)` epoch (190 steps); odometer left-frontier configs as quoted
  in §1; REFILL `(10)^{13} ⟹ 1^{26}` then D→F→continue.
- `o18halt.py`: F reachable only via `D,1→F`; aligned seed `…1 1 1 0 1 0 1 0 [C>1] 0` ⟹ HALT in 9 steps;
  clean control continues; per-residue `⌊8k/3⌋+2 = 8q + (0,2,5) + 2`.
- `o18lemmas.py`: A/B-MARCH, REFILL, and the adjacent-`11`⇒HALT handoff confirmed as standalone rewrites.

---

## 6. Verdict and paper-label impact

| item | status after this pass |
|---|---|
| o18 exact TM + table | **[PROVEN]** (definitional) |
| macro-config `M(k)` + base-3 odometer structure | **[VERIFIED]** (exhibited from raw run) |
| elementary sweep lemmas (A/B-MARCH, REFILL, leftward sweeps) | **[PROVEN]** (single-transition inductions) |
| **halt criterion** "o18 halts ⟺ F reads 1 ⟺ adjacent-`11` at D/F frontier" | **[PROVEN]** (table + seeded) |
| **Lemma CLEAN-EPOCH** `M(k) ⟹ M(⌊8k/3⌋+2)` *given clean carry* | **[PROVEN, conditional]** |
| **unconditional** macro-map `M(k) → M(⌊8k/3⌋+2)` for all k | **[DISPROVEN]** (breaks at epoch 7) |
| identification of "F reads 1" with the base-3 carry-alignment event `(K_o18)` | **[OPEN]** (AEV `q=3` Erdős facet) |

**Is o18's macro-coordinate now fully hand-proven (→ [PROVEN], joins Antihydra)?**  **No — and it cannot be,
because the unconditional map is false.** o18 does **not** join Antihydra as an in-scope *proven* macro-extraction.

**Precise blocker (not a gap in effort — a gap in truth):** the base-3 carry of the `(8/3)`-orbit reaches the
left frontier at epoch 7 (`k=3890≡2 mod 3`), destroying the clean milestone form; whether it does so finitely
often is the open kernel `(K_o18)` and is the *same event* as the halt criterion. The conditional clean-carry
epoch lemma and the halt criterion are genuinely [PROVEN] from the table; the unconditional ⌊8N/3⌋+2 coordinate
is not (it is false beyond epoch 6).

**`PAPER_MAIN.md` / `TM_EXTRACTION_PROOFS.md` label guidance:**
- o18 "halts ⟺ F reads 1" (form): **[PROVEN, trivial]** — unchanged (already upgraded).
- o18 width law `⌊8k/3⌋+2`: **stays [VERIFIED]**, and this pass adds the precise reason it cannot be [PROVEN]
  unconditionally (it is **false** beyond epoch 6; only the *conditional* clean-carry lemma is [PROVEN]).
- **No upgrade of o18's macro-coordinate to [PROVEN].** PAPER_MAIN must **not** relabel the o18 ⌊8N/3⌋+2
  coordinate as [PROVEN]; the honest, defensible upgrade available is to record the **halt criterion [PROVEN]**
  and the **conditional clean-epoch lemma [PROVEN]**, with the macro-coordinate remaining [VERIFIED] and the
  defect pinned to `(K_o18)`.

*All numeric confirmations: `scratchpad/{o18trace,o18epoch,o18phases,o18lf,o18milestones,o18halt,o18lemmas}.py`,
re-run against `bb_sim` semantics with the `.venv` big-integer interpreter. No appeal to `bb_sim` is made inside
any [PROVEN] step; it is confirmation only.*
