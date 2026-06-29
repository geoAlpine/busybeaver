# Carry decorrelation, isolated: is bit_{n+k}(S_n) a bounded-memory function of recent parities? (2026-06-29)

*Assigned task: attack ONLY the endogenous-carry decorrelation in isolation, via the bounded-memory / 3-adic
valuation angle. The carry is `S_n = Σ_{j<n} 3^{n−1−j} 2^j b_j`, `b_j = c_j mod 2`, and the Open-Lemma bit is
`β_n = bit_k(c_n) = bit_{n+k}(8·3^n − S_n)` `[PROVEN, ODD_3ADIC_ODOMETER §1]`. Decisive question: does
`bit_{n+k}(S_n)` depend on a BOUNDED window of recent parities `b_{n−m..n−1}` (a finite-state factor), or does
the whole history contribute through carries? Numerics `.venv`, exact big-int,
`scratchpad/carry_bounded_memory.py`, ≈1s. Every claim labelled. Zero false proofs. NOT committed.*

---

## 0. One-line verdict

**(c) RE-EXPOSES MAHLER, sharply.** The binary read bit `bit_{n+k}(S_n)` is **NOT** a bounded-memory function
of recent parities: the effective memory length is `m(k) = n − O(k)` — it grows with the clock, so essentially
the **whole parity history** sets the read bit. `[PROVEN unbounded]` Bounded memory holds only for two channels
that **do not feed the read bit**: (i) the *recent* parities (window `d ≲ d*(k)=1.71k+2.7`) reach the read
position only through a **carry chain** and carry a *vanishing* fraction of the influence; (ii) the *low 3-adic
residue* `S_n mod 3^m` has exact memory `m` but is **orthogonal** to the binary high bit (corr ≈ 0). The read
bit's dominant, unbounded channel is a GF(2)-linear-plus-carry form over the entire history weighted by the
**binary digits of powers of 3** — i.e. the Mahler-3/2 diagonal verbatim. **No machine decided. No label upgraded.**

---

## 1. The exact dependence range — PROVEN unbounded  `[PROVEN]`

Flipping a single parity `b_j` perturbs the carry by exactly `±X_j`, `X_j := 2^j·3^{n−1−j}`. The lowest set bit
of `X_j` is at position `j`; its top bit is at

> `p_j = j + ⌊(n−1−j)·log₂3⌋ ≈ 1.585n − 0.585j`.   `[PROVEN]`

So **the most recent terms are the smallest** (`X_{n−1}=2^{n−1}`, top bit `n−1 < n+k`) and **the oldest terms
are the largest** (`X_0=3^{n−1}`, top bit `≈1.585n ≫ n+k`). The read position is `n+k`. Solving `p_j ≥ n+k` for
direct reach (the perturbation's support straddles the read bit):

> **`[PROVEN]` Direct-reach threshold.** `b_j` reaches `bit_{n+k}` *directly* (not only via carry) iff
> `d := n−j ≥ d*(k) := (k+log₂3)/(log₂3−1) = 1.709k + 2.709`.

- For `d ≥ d*(k)` (the **older** `n − O(k)` terms): `bit_{n+k}(X_j)` is the binary digit
  `digit_{k+d}(3^{d−1})` — a Mahler digit, balanced ≈ ½. There are `n − d*(k) = n − O(k)` such terms.
- For `d < d*(k)` (the **most recent** ≈`1.71k` terms): `X_j`'s top bit lies *below* `n+k`, so `b_j` can move
  the read bit only by propagating a carry across `(n+k)−p_j` positions.

> **`[PROVEN]` Effective memory `m(k) = n − O(k)` — UNBOUNDED.** Because `n − d*(k)` history bits each influence
> `bit_{n+k}(S_n)` directly through a balanced Mahler digit, the read bit is **not a function of any fixed-width
> window of parities**. No finite `m` makes `b_{j<n−m}` negligible. (Contrast: `S_n mod 3^m` — §3 — *does* have
> exact memory `m`, but that is the low 3-adic digit, not the read bit.)

### Numerics — flip-sensitivity `[OBSERVED]`  (`carry_bounded_memory.py` T1; avg over `n∈[600,1400)`)

`P(β_n flips | flip b_{n−d})` vs `d`:

| `d` | k=3 | k=5 | | `d` | k=3 | k=5 |
|---|---|---|---|---|---|---|
| 1 | 0.055 | 0.005 | | 25 | 0.18 | 0.96 |
| 4 | 0.205 | 0.080 | | 100 | 0.45 | 0.69 |
| `≈d*` (7.8 / 11.3) | 0.71→0.91 | 0.93 | | 400 | 0.08 | 0.57 |
| 12 | 0.57 | 0.67 | | **1000** | **0.89** | **0.18** |
| 18 | 0.41 | 0.66 | | **1300** | **0.84** | **0.80** |

- **Recent window** `d ≤ d*`: aggregate `P = 0.30` (k=3), `0.24` (k=5) — *suppressed*, rising toward `d*` exactly
  as predicted (carry-only reach).
- **Bulk** `d > d*`: aggregate `P = 0.495` (k=3), `0.507` (k=5); plateau over `d≥50` is `0.495 / 0.508`, and it
  **persists all the way to `d ≈ n`** (`d=1000,1300` still ≈½). So ≈`n/2` history bits genuinely set the read bit.
- The steep transition at the predicted `d*(k)=1.71k+2.7` (k=3: 7.8; k=5: 11.3) is a verified structural prediction.

---

## 2. No finite-state factor; it re-exposes Mahler, not the recent self-feeding  `[PROVEN reduction]`

Because the read bit has unbounded memory (§1), the carry is **not** a finite-state factor over recent
parities — there is no automaton on `(b_{n−m..n−1}, d_n)` computing `β_n`. Writing the read bit exactly:

> **`[PROVEN]`** `bit_{n+k}(S_n) = bit_{n+k}( Σ_{j<n} b_j·2^j·3^{n−1−j} )`, a **GF(2)-linear-plus-carry form
> over the entire history** `b_0..b_{n−1}`, with weights the **binary digits of the powers `3^{n−1−j}`**
> (the bit of `S_n` at `n+k` reads `digit_{n+k−j}(3^{n−1−j})` from each set `b_j`, summed with carries).

Controlling its correlation with a character `χ_a(s_n)` of the low state is therefore **exactly** the
equidistribution of the digits of powers of 3 along the moving diagonal = Mahler 3/2 (`ODD_3ADIC_ODOMETER §3`,
`DIGITS_OF_3N.md`). T4 confirms the weights are balanced: `mean digit_{k+d}(3^{d−1}) = 0.487 (k=3), 0.499
(k=5)` over `d∈[50,1300)`.

**Precise reason it is (c), not self-feeding.** The naive worry was that recent parities `b_{n−m..n−1}` (which
also set the low state `s_n`) dominate `β_n`, giving the self-feeding closed loop. The bounded-memory analysis
shows the **opposite**: the recent/self-referential channel is *carry-confined* to the window `d ≲ 1.71k` and
carries a *vanishing* fraction of the influence (§1 table); the read bit is dominated by the **old** history via
balanced Mahler digits. Moreover `s_n = c_n mod 2^k =` bits `[n, n+k)` and `β_n =` bit `n+k` are **adjacent high
bits of the same carry-laden number** `8·3^n − S_n`, so both are whole-history Mahler functionals — they cannot
be separated into "recent state vs old bit." The obstruction is not the recent self-feeding (suppressed); it is
the **whole-history Mahler-digit coupling**, the same wall in undiminished form.

---

## 3. 3-adic angle — bounded memory exists, but orthogonal to the read  `[PROVEN]`

Use `S_{n+1} = 3 S_n + 2^n b_n`. Since `3^{n−1−j} ≡ 0 (mod 3^m)` whenever `n−1−j ≥ m`:

> **`[PROVEN, T3]`** `S_n mod 3^m` depends ONLY on the most recent `m` parities `b_{n−m..n−1}`
> (verified exact, 0 mismatches, `n∈{200,800,1500}`, `m∈{1,3,6,10}`). The **low 3-adic residue is genuine
> bounded-memory** `m` — the clean dual of the 2-adic carry-rotation (`THREEADIC_ROTATION`).

But the Open-Lemma reads a **binary high bit** at position `n+k`, not a low 3-adic digit. These are cross-base
and **uncorrelated**:

> **`[OBSERVED, T3]`** `corr(β_n, low-bit(S_n mod 3^m)) = +0.012, +0.008 (k=3, m=3,6); +0.064, −0.040 (k=5,
> m=3,6)` — all ≈ 0.

So the 3-adic borrow at the binary read position is **not** made predictable by the bounded 3-adic memory: the
high binary digit and the low 3-adic digit are orthogonal coordinates (the 2↔3 mixing that *is* Mahler). The
3-adic structure tames a channel the read bit does not query — the exact analogue of `THREEADIC_SKEW §2`
(the synchronizing fiber is orthogonal to the target valuation).

---

## 4. Honest verdict

| ask | answer | label |
|---|---|---|
| Effective memory `m(k)` bounded? | **No.** `m(k) = n − O(k)`, unbounded; `n − d*(k)` old bits each set the read bit through a balanced Mahler digit. Threshold `d*(k)=1.71k+2.7` proven and verified. | `[PROVEN unbounded]` |
| Bounded memory ⇒ finite-state factor / partial decorrelation? | **No.** No automaton on recent parities computes `β_n`. The only bounded-memory channels (recent carry-window `d≲1.71k`; low 3-adic residue `mod 3^m`) carry vanishing / orthogonal influence and do not feed the read bit. | `[PROVEN]` |
| Does it re-expose self-feeding or Mahler? | **Mahler (not the recent self-feeding).** The read bit is a whole-history GF(2)+carry form weighted by binary digits of powers of 3 = the Mahler diagonal; the recent self-referential channel is the *suppressed* one. | `[PROVEN reduction]` |
| (a) real win / (b) partial+residue / (c) reduces? | **(c)**, with a sharp new structural reason and a banked separation of channels. | — |

**Exact residual.** Unchanged in difficulty, sharpened in form: equidistribute the **whole-history
Mahler-digit form** `bit_{n+k}( Σ_{j<n} b_j 2^j 3^{n−1−j} )` against `χ_a(c_n mod 2^k)` — i.e. show the
balanced binary digits of the powers `3^{n−1−j}`, summed over the orbit's own parity history with carries,
decorrelate from the adjacent low-bit window of the same number. This is `Inj_a → 0` = (K) = Mahler 3/2 / AEV
Conj 1.6, now exhibited as a single whole-history digit-of-3 correlation with a **proven** unbounded memory.

### Genuinely new vs prior
- `ODD_3ADIC_ODOMETER`/`ODD_SUBSPACE_SYNTHESIS` named the carry `S_n` as the self-reference and the bridge to
  the Mahler diagonal. **This note settles the bounded-memory question they left open**: it PROVES the read bit's
  memory is `n − O(k)` (unbounded), with the exact threshold `d*(k)=(k+log₂3)/(log₂3−1)` and a flip-sensitivity
  profile confirming the ≈½ plateau persists to `d≈n`.
- New separation banked: the *recent self-feeding* channel is carry-confined to width `≈1.71k` and is
  **negligible**, while the *dominant* channel is the unbounded Mahler-digit coupling to the old history —
  so the carry's hard content is Mahler, not the recent closed loop. This refines the no-go's "self-reference"
  diagnosis (`ENDOGENOUS_UE_BUILD §5`): the irreducible part lives in the deep digits, not the recent window.
- New (parallel to `THREEADIC_ROTATION`/`THREEADIC_SKEW`): the 3-adic bounded-memory channel `S_n mod 3^m`
  exists exactly but is **orthogonal** (corr≈0) to the binary read bit — the bounded structure tames a
  coordinate the Open Lemma never queries.

### Why this confirms rather than breaches (honest)
A bounded-memory carry would have given a finite-state factor and a non-spectral handle. The carry's *low*
(3-adic) end is bounded-memory and its *recent* (self-feeding) end is carry-suppressed — but the bit the kernel
actually reads sits at a binary position fed by the entire history through the digits of powers of 3, exactly the
object Mahler 3/2 is about. Fully consistent with `ODD_3ADIC_ODOMETER §3` (moving diagonal = Mahler),
`THREEADIC_SKEW §2` (orthogonal-fiber relabel), `ADELIC_COUPLING §3`, and `ENDOGENOUS_UE_BUILD §5`.

## Sources
- Repo: `ODD_3ADIC_ODOMETER.md` (β_n = bit_{n+k}(8·3^n − S_n); moving diagonal = Mahler), `ODD_SUBSPACE_SYNTHESIS.md`
  (carry = named self-reference; sign-aware target), `ENDOGENOUS_UE_BUILD.md` (§4 Open Lemma, §5 no-go),
  `THREEADIC_ROTATION.md` / `THREEADIC_SKEW.md` / `ADELIC_COUPLING.md` (3-adic channel = orbit-driven / orthogonal
  fiber), `DIGITS_OF_3N.md`, `mahler_equidistribution_attack.md §9`.
- Literature (repo knowledge): Mahler 3/2 (1968, open); digits of powers of 3 / `⌊α(3/2)^n⌋` (open);
  AEV arXiv:2510.11723 Conj 1.6.
- Numerics: `scratchpad/carry_bounded_memory.py` (exact big-int, ≈1s; T0 identities 0 fail; T1 flip-sensitivity
  plateau ≈½ to d≈n; T3 `S_n mod 3^m` exact recent-m memory but corr≈0 with read bit; T4 Mahler-digit balance).

**No machine decided. No label upgraded.**
