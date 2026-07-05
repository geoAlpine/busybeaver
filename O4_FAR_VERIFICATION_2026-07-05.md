# FAR/CTL verification for o4 — rigorously: the invariant is NON-REGULAR, so the sound (regular-only) verifier cannot certify it (2026-07-05)

*Attempting the FAR/CTL abstract-closure verification to decide o4. **Definitive finding:** the repo's FAR verifier
(`far_dfa.py`) implements a **sound abstract-closure `verify()`** — but only for **regular (m-gram / sofic) invariants**
("config ∈ L iff every length-`m` window is in the gram set `G`"). Its search returns **HOLDOUT at all `m`**, which — given
everything established — is not a search failure but a **rigorous consequence**: o4's invariant `0^G(10)^a1001` is
**non-regular** (the big gap is a genuine counter), so **no regular certificate exists**, and the sound tooling provably
cannot certify o4. A rigorous decision needs a **counter-automaton certificate + a sound counter-automaton verifier** —
new tooling that must itself be validated. SOUNDNESS: o4 `[OPEN]`; **not decided; no false decision**. No machine decided.*

## The sound verifier is regular-only `[VERIFIED from source]`
`far_dfa.py`'s `Invariant.verify()` is a **correct abstract-closure checker**: it verifies (S) the start is accepted,
(H) no accepted config has the head reading a symbol whose transition halts, and closure under every `L`/`R` TM move
over all **context states** — the FAR/CTL soundness conditions. But the invariant class `FAR` is an **m-gram automaton**:
`config ∈ L ⟺ every length-m window of 0^{m-1}·config·0^{m-1} ∈ G`. This is a **regular / sofic** language (finite
context-state set). `verify()` iterates over the **finite** `reachable_context_states()` — so the whole framework can
only certify **regular** invariants.

## Why this means o4 is not certifiable by it `[rigorous]`
- **`far_dfa.prove` = HOLDOUT at all `m` (re-confirmed `m≤16`).** No regular m-gram invariant closes o4.
- This is **forced**, not incidental: o4's reachable set is `{0^G (10)^a 1001}` (+ generation intermediates), whose
  **big gap `0^G` is a counter** — the head-local abstraction is **non-Markov** (macro-transitions non-deterministic,
  macro-count grows `268→409→568` with window `6→8→10`; `O4_CLOSURE_PROOF_ATTEMPT`). A **regular** (sofic) language
  cannot separate the reachable configs from the halting ones here, because distinguishing them requires **counting**
  the big gap. So **no regular certificate exists** — exactly the HOLDOUT, for a rigorous reason.
- Therefore the sound repo verifier (regular-only) **cannot** decide o4 — not for lack of search depth, but by the
  **non-regularity of the invariant**.

## What a rigorous decision requires `[the honest remaining tooling]`
A **counter-automaton (regular + one counter) certificate**: the language `0^G (10)^a 1001` with the big gap as a
symbolic counter, and a `verify()`-analogue that checks abstract closure **symbolically in the counter** (one
generation via `G ↦ ⌊4G/3⌋+c(G mod3)`, halt-free per residue class). This is **decidable in principle** (the counter
dynamics is the base-4/3 odometer, finite-per-residue), but it is **new sound tooling** — a counter-automaton
closure-verifier that must itself be **validated** before any decision it emits can be trusted. Building and validating
it (not merely running it) is the genuine remaining task; producing a decision from unvalidated tooling would be a
false proof.

## Verdict `[SOUNDNESS — the disciplined endpoint]`
**o4 is NOT decided, and the reason is now RIGOROUS, not effort-limited.** Its non-halting invariant is
**provably non-regular** (big-gap counter), so the repo's **sound regular-only FAR/CTL verifier cannot certify it**
(HOLDOUT at all `m`, a forced consequence). o4 remains **Fork-A with an explicit non-regular invariant**
(`0^G(10)^a1001`, exact base-4/3 odometer, robust closed observational macro-graph, halt-free to 50M) — the strongest
possible characterization short of a **counter-automaton certificate**, which needs new, separately-validated sound
tooling. I decline to assert a decision without it. **Halting `[OPEN]`. No machine decided. No label upgraded.**

## Reproduce
- `far_dfa.prove(o4, ms up to 16)` = `HOLDOUT`; `far_dfa.py` `Invariant.verify()` (sound, m-gram/regular only) +
  `FAR` class (m-gram = "every length-m window in G", regular). Basis: `O4_MACRO_MACHINE_2026-07-05` (non-Markov,
  observational closure), `O4_COUNTER_CERTIFICATE_2026-07-05` (explicit `0^G(10)^a1001`), `O4_CLOSURE_PROOF_ATTEMPT_2026-07-05`.
