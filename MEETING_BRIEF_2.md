# Meeting brief — round 2 (2026-06-26): the deep characterizations since the last consultation
*For a strategy session (incl. ChatGPT). The last consultation validated the *formulation* (correct, Mahler-class,
obstruction = specified-point genericity). Since then we ground the wall to the bottom from every angle and the
characterizations converged sharply. This brief is what is new and worth discussing. All claims machine-checked or
literature-anchored; 0 false proofs (~15 over-claims caught & retracted).*

## 1. One-line state
Antihydra non-halt ⟺ the single orbit of seed 8 under `×(3/2)` equidistributes ⟺ `⌊(3/2)^n⌋ mod 2` is **normal**
⟺ a **rank-1 Anosov / amenable-hyperbolic** automorphism has a generic specified orbit (= Mahler 3/2). We could not
break it, but we now know *exactly why no currently known tool reaches it*, from five independent directions that
all coincide — and (new, §E below) **three different unconditional tool-families each fail for a distinct precise
structural reason**, which is the strongest evidence the wall is real, not an artifact of one framing.

## 2. The four genuinely new characterizations (since last meeting)
**(A) The wall is `amenable ∩ hyperbolic` — a rank-1 Anosov single orbit.** Trichotomy:
*amenable+isometric* (rotation/odometer) → Weyl/unique-ergodicity (solved); *non-amenable+hyperbolic* (rank-≥2
Cat-map) → measure rigidity (solved); ***amenable+hyperbolic*** (`×3/2`) → **no currently known tool**. Amenability kills the
rigidity engines; hyperbolicity kills the rotation/Weyl engines.

**(B) Complete engine survey — all seven single-orbit engines fail for one reason.** Weyl/vdC (closed),
transfer-operator (orbit-blind/a.e.), Furstenberg rigidity, BFLM, entropy/Lindenstrauss, Bourgain–Gamburd — each
needs a **2nd multiplicatively-independent direction (rank-2)** or **a.e.**; the orbit uses only the self-dual
combination `×3/2`, never the pair `×2,×3`. The renewal map's hidden non-abelian semigroup is `ℤ[1/6]⋊⟨3/2⟩` —
**solvable/amenable**, so no spectral gap. (BFLM specifically: `×3/2` is **self-dual**, so its Fourier-decay
argument is circular.)

**(C) The factor-2 margin is settled — it buys a weaker *target*, not an easier *proof*.** `avg jump ≤ 2`
translates to a one-sided `2×`-anti-concentration (`N_k/J ≤ 2·2^{−k}`), strictly weaker than equidistribution; but
the per-cylinder upper bound is itself a specified-orbit cylinder-frequency statement (= the additive energy),
*same class*. The margin relaxes the **constant**, not the **kind** of control. So no Mahler-free internal path.

**(D) Deepest dig (k=2, mod 4): the entire wall is "quenched vs annealed".** The **annealed** transition operator
on `mod 4` distributions has uniform as its unique fixed point with a **strong spectral gap (≈0.95) — it mixes in
~1 step.** The renewal map is *uniformizing* (odd states spread sub-residues across all `mod 4` values). **The
entire obstruction is that the orbit is deterministic and feeds its own higher bits** (scale 2 needs scale-3
uniformity, scale 3 needs scale 4, … base case = the wall). There is **no arithmetic shortcut even at the finest
scale**; the difficulty is purely self-referential determinism = explicit normality.

**(E) NEW (this round): the wall, attacked with three unconditional tool-families, blocks each for a *distinct*
reason — and two new exact reductions.** Since the brief above, we ran ten internal probes; they all *funnel* to
one place (long odd-runs ⟺ deep cylinders ⟺ deep-cylinder frequency ⟺ single-orbit equidistribution), and the
three tool-families one would reach for each fail structurally:
| tool family | needs | blocked because |
|---|---|---|
| measure / spectral | unique ergodicity or rank-≥2 / a.e. | rank-1, continuum of measures — needs an **infinitary** input |
| p-adic Baker / S-units | **bounded-height** algebraic inputs | `c_n=(3^n c_0−T_n)/2^n`, `height(T_n)≈n·log₂3` — **unbounded** |
| character sum / bilinear / sum–product | **multiplicative** structure in `n` | `c_n mod 4` = high bits of dynamical `T_n` — **structureless** (uncorrelated w/ `λ(n)`, flat over `n≡a(q)`) |
Two **new exact, machine-checked** reductions came out of this: **(i) valuation budget**
`Σ_{odd i<n} v2(3c_i−1) = n + v2(c_n) − v2(c_0)`, giving a third criterion form **non-halt ⟺ `avgD_odd ≥ 3/2`** (a
*lower* bound on one average; Haar = 2) and an **unconditional range** `n ≤ Σ ≤ 1.585n` (a 2-adic
Flatto–Lagarias–Pollington); **(ii)** the leading term of `avgD_odd ≥ 3/2` is the **one-sided character sum**
`Σ_{odd} χ_{−4}(c_n) ≤ 0`, and a second-moment/energy attack is **provably sign-blind** (energy `= O²/2 + S²/2`,
symmetric — bounds `|S_n|`, never its sign). Both are new, exact, and independent of the measure framing.

## 3. The questions for the meeting (sharper than "is this Mahler?")
1. **Is `amenable ∩ hyperbolic` (rank-1 Anosov single orbit) a recognized empty cell in the toolbox**, and is
   there *any* result — even conditional/Diophantine — for a specified orbit there? (Confirm or break the
   trichotomy.)
2. **The "quenched → annealed" bridge.** The annealed operator mixes trivially (spectral gap); the whole
   difficulty is the *deterministic self-feeding*. **New (sharpens this):** the quenched orbit and the annealed
   model are **provably indistinguishable by every finite-order statistic** — a base-`p` digit-bijection makes each
   `k`-step joint law of the mod-`p` residues *equal* the mod-`p^{k+1}` cylinder law, so lag-MI excess `≈0`,
   block-entropy rate `= log p`, mod-`p²` uniform (verified, `higher_cylinder.py`). So a bridge **cannot** be built
   by matching/decorrelating finite statistics — they already coincide; it must inject a genuinely
   **infinitary/Diophantine** input. Is there a technique — from **deterministic-vs-random dynamics, disordered
   systems, or "annealed ⇒ quenched" transfer** — that upgrades annealed mixing to a single deterministic orbit
   using only such an infinitary hypothesis (not a finite-order decorrelation, which is unavailable)? (Most novel
   framing; does it ring a bell?)
3. **Is the engine list complete?** Is there an 8th class of single-orbit-equidistribution method that needs
   *neither* rank-2 *nor* a.e. — i.e. that could live in the `amenable ∩ hyperbolic` cell?
4. **Explicit normality with no certificate.** Provably-normal sequences are *constructed* (Champernowne / Korobov
   / computable-by-design). Is there *any* precedent for proving a **given** sequence (here `⌊(p/q)^n⌋ mod 2`)
   normal from its **generating dynamics alone**, with no designed certificate? If not, naming that gap is itself
   useful.
5. **Character sum along one orbit / the 4th-technology gate.** Given the §E table — is there a **fourth**
   unconditional technology we are missing, or a reason one of the three *should* reach? Concretely: any
   cancellation for a character sum `Σ_{n<N} χ(c_n)` along a single deterministic `⌊μ·⌋`-orbit (which is
   *multiplicatively structureless* in `n`), or a "Baker for orbits of `⌊μ·⌋`" handling **unbounded-height**
   nested-floor values? A clean "no, out of reach because …" for either is as useful as a tool.

## 4. What we want out of it
A pointer, a "no + the reason", or a reformulation. Most valuable: **a known route from annealed mixing to a
single deterministic orbit** (Q2), confirmation that the `amenable ∩ hyperbolic` cell is genuinely empty (Q1), or
a **fourth technology** beyond the three that §E shows each blocked (Q5) — any of these pins the multi-year
direction. We are **not** asking anyone to solve Mahler; we are asking whether the quenched-vs-annealed /
rank-1-Anosov framing — now backed by three independent structural obstructions and two new exact reductions
(`avgD_odd ≥ 3/2`; one-sided character sum) — connects to an existing body of technique.
*(Companion send-ready notes: `EXPERT_ASK.md` (Q0–Q4), `EXPERT_ASK_HOMOGENEOUS.md`; full review: `RETROSPECTIVE.md`;
the three-technology closure: `ENERGY_ATTACK.md`, `SEPARATION_BAKER.md`; the new identity: `VALUATION_BUDGET.md`.)*
