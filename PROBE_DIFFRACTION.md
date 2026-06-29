# Probe: non-Pisot diffraction / spectral theory of the Antihydra parity word (2026-06-30)

*One sharp question: does the diffraction (autocorrelation spectrum) of the parity word `b_n=c_n mod 2` give a single-orbit
handle on the kernel (even-density / mean D), or reduce to the annealed picture? The sub-agent died on an API error
mid-run (its `scratchpad/diffraction.py` survived); the main loop re-ran the decisive computation
(`scratchpad/diffraction_self.py`, exact big-int orbit, N=2¹⁷, FFT) and wrote this. SOUNDNESS: labelled; no claim it solves
(K). NOT committed by default.*

---

## 0. One-line verdict

**[reduces / orthogonal-to-kernel].** The diffraction spectrum of the Antihydra parity word is **absolutely continuous**
(flat, statistically **indistinguishable from Bernoulli(½)** away from DC) — not pure-point, not singular-continuous. The
hoped-for "non-Pisot ⇒ singular-continuous" feature does **not** appear: it is a property of the annealed self-similar
measure `ν_{2/3}` / substitution systems, not of this full-complexity orbit. Decisively, the kernel quantity
(even-density) is exactly the **DC (zero-frequency) Bragg intensity**, while diffraction's spectral-**type** classification
describes the **nonzero-frequency** correlation structure — **orthogonal to the DC mean**. So diffraction gives the right
*shape* (a single-orbit second moment) but its theorems do not bound even-density; the flat spectrum is the same
"looks-random" annealed-indistinguishable evidence, (K)-hard to upgrade to a proof.

---

## 1. The computation [OBSERVED, N=2¹⁷, exact big-int orbit + FFT]

| quantity | Antihydra parity `b_n` | Bernoulli(½) control |
|---|---|---|
| mean `b` (= even-density = √(DC Bragg intensity)) | **0.49979** | 0.5 |
| centered autocorr `γ(m)`, m=1..8 | `≈0` (`1e-4 … 1e-3`) | `≈0` |
| power spectrum (DC removed): max peak | 2.87 | 2.81 |
| … mean / top-10 | 0.250 / `[2.9..2.2]` | 0.250 / `[2.8..2.2]` |
| … `max peak / N` (pure-point would be `O(1)`) | **0.00002** | 0.00002 |
| top-1%-of-frequencies intensity fraction | 0.056 | 0.056 |

The two columns are **identical to sampling precision**. `max/N ≈ 2·10⁻⁵ → 0` rules out Bragg peaks (pure-point); the
flat, exponentially-distributed power spectrum with no self-similar peak hierarchy rules out singular-continuous. The
spectrum is **absolutely continuous** — the diffraction of a random-like (normal-looking) sequence.

---

## 2. Why it does not reach the kernel [the decisive structural point]

- **even-density = the DC Bragg peak.** The intensity at frequency 0 is `(mean b)² = (even-density)²`. The kernel `(K)`
  (even-density ≥ 1/3) is therefore a statement about the **DC component alone**.
- **Diffraction spectral-type theorems are about the nonzero spectrum.** The pure-point / singular-continuous /
  absolutely-continuous classification (Baake–Grimm; Lenz) characterizes the autocorrelation at **nonzero lags** — the
  *correlation structure*, which is **orthogonal to the mean**. Knowing the spectrum is absolutely continuous says the word
  is decorrelated/random-like; it does **not** pin the DC intensity (a sequence with any mean can have an a.c. spectrum).
  So no diffraction theorem lower-bounds even-density.
- **The single-orbit autocorrelation is the annealed-indistinguishable object.** `γ(m)≈0` and the flat spectrum are exactly
  the "indistinguishable from i.i.d." evidence already banked (`CARRY_EXOGENIZATION.md`, `QUENCHED_ANNEALED_SEAM.md`);
  proving them (or the DC mean) for the single orbit is `(K)`-hard. The non-Pisot singular-continuity that *would* be
  distinctive lives on the annealed `ν_{2/3}` (`NONPISOT_FOURIER_CHAIN.md`), already mined and annealed-only.

---

## 3. Verdict

Diffraction is the **conceptually aptest** new framing (it is natively a single deterministic sequence's autocorrelation =
a HARD-side second moment), and the numerics are a clean new [OBSERVED] datum (a.c. spectrum, Bernoulli-indistinguishable,
no non-Pisot singular-continuity for the orbit). But it **reduces**: the kernel is the DC mean, orthogonal to the spectral
type the theory classifies, and the single-orbit autocorrelation is the same annealed-indistinguishable / (K)-hard object.
Right shape, wrong coordinate (type vs DC). **No machine decided. No label upgraded.** (K) remains [OPEN] = Mahler 3/2 /
AEV.
