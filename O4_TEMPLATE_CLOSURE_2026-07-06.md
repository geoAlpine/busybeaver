# o4 template closure — the generation is a PROVEN rigid template; the decision reduces to an explicit a-LEDGER condition; the B2 "arithmetic" wall merges with the (K)-shaped ledger (2026-07-06)

*The "next move" (cap C-seam finite analysis) escalated into the sharpest result of the program's o4 track: the whole
generation dynamics is a **rigid, certified template** (prefix · body^r · suffix), each piece **verified as a
parameter-uniform lemma** by the certified trace-template method; the base-4/3 odometer law is **derived** from the
templates; and the residual is a single **explicit ledger inequality** — including a genuine HALTING configuration
`Z(41, g=3, a=0)` showing the condition is not vacuous. o4 `[OPEN]` — NOT decided; the decision is now an explicit
Collatz-like ledger conjecture. No machine decided.*

## 1. The rigid template `[OBSERVED → certified]`
Instrumenting the validated macro-machine (`o4_bouncer_macro.py`): every generation's micro-event stream is EXACTLY
**prefix(454 events, single hash over ALL generations) · body(51 events)^r · suffix(class-dependent: 279/22/125 events
at G mod 3 = 0/1/2, single hash per class)**, with jump (sweep) lengths exactly affine (+4 per round trip). The turn-4
"counter-dependent branching" (`0/25`) is the projection of TEMPLATE POSITION out of the boundary graph — the
(state, read) sequence is rigid; only sweep lengths and r vary with G.

## 2. The certified lemmas `[PROVEN, certified trace-template method]`
Method: compress a concrete trace into **bounded episodes** + **uniform sweeps** (`B1F0` read-only rightward, `D1E0`
invert leftward — both proven for ARBITRARY length by 2-transition induction). Verify across a parameter grid: the
compressed skeleton is IDENTICAL and sweep lengths are exactly affine. Any first divergence at an untested parameter
would have to occur inside an episode whose preceding compressed trace — hence local tape content, by the locality
lemma (identical window + head-confined ⇒ identical evolution) — is identical: contradiction. Hence the template holds
for ALL parameters in the cone. (`o4_body_proof.py` + inline suffix/prefix verifications.)
- **PREFIX `[PROVEN]`:** from milestone `M(G,a)` (head on gap-left 0, state E): a **fixed 471-step word** (identical
  trace hash for all G∈{100,101,102,103,200,501}, a∈{8,20}), span `[−11,30]` (bounded, G,a-independent), unsafe=0,
  landing: zone `(10)^19 1001` at `−11`, gap and filler INTACT. Valid for all `G≥37`, all `a`.
- **BODY `[PROVEN]`:** standalone `B(k) = 0^∞ [E] (10)^k 1001 0^∞ → B(k+2)` shifted −1, in exactly `15+4k` steps;
  skeleton identical (9 episodes + 2 sweeps), sweep lengths exactly `(2+2k, 4+2k)`, span `[−1, 2k+8]`, unsafe=0 —
  verified k=19..27,49,101,**251** ⇒ all odd `k≥19`. Consumes 3 gap cells per application; applies while gap ≥ 6.
- **SUFFIX `[PROVEN]`, 3 classes** (gap-at-meet `g∈{3,4,5}`, `g ≡ G−31 (mod 3)`): `Z(k,g,a) → M(G′,a′)` EXACT
  milestone landing; skeleton identical across the whole (k,a) grid (k∈{19,21,23,41}, a∈{8,12,30} and small-a 0..7),
  steps affine; unsafe=0 throughout:
  | g | valid | G′ | a′ | skeleton |
  |---|---|---|---|---|
  | 3 | **a≥2** | 2k+12 | a−1 | 19 |
  | 4 | a≥0 | 2k+9 | a+4 | 41 |
  | 5 | a≥0 | 2k+13 | a+6 | 74 |

## 3. The odometer DERIVED `[PROVEN from templates]`
Composing prefix + r bodies + suffix: `r=(G−31−g)/3`, `k_end=19+2r`, and the table gives
**`G′ = ⌊4G/3⌋ + c(G mod 3)`, `c={0→3, 1→5, 2→1}`** — the empirically-known odometer law now falls out of the
certified templates (checked against the real orbit: 275→367→494→659 ✓). The G mod 3 classes are exactly the
three gap-at-meet residues.

## 4. THE DISCOVERY — the a-ledger, and a genuine halting configuration `[the new irreducible core]`
- The filler count evolves by **`a′ = a + δ(G mod 3)`, `δ = {G≡1: −1, G≡2: +4, G≡0: +6}`** — a prefix-sum LEDGER
  driven by the orbit's residue sequence.
- **`Z(41, g=3, a=0)` HALTS** (step 55,170) `[verified concrete]` — the small-a region is genuinely fatal; the g=3
  small-a cases are k-irregular (a=0: k=19 lands, k=21 wanders, k=41 halts). So the safety condition is NOT vacuous.
- **o4 does not halt ⟸ the ledger satisfies `a ≥ 2` at every `G≡1 (mod 3)` generation** `[PROVEN: template closure +
  induction, base concrete to G≈884k]`. The converse holds partially (specific small-a configs halt; full ⟺ needs the
  small-a case analysis completed).
- Empirical margin ENORMOUS: δ-drift ≈ +3/generation vs the −1-only-at-g=3 drain; failure needs a prefix with
  ρ=1-frequency ≳ 4/5 (observed ≈ 1/3). Real orbit: a=34→38→37→… (rule verified against dumps: +4 at G=275≡2,
  −1 at G=367≡1 ✓).

## 5. What this means — the B2 wall merges with the (K)-shape `[honest, significant]`
o4, the flagship "B2 = deterministic arithmetic odometer" cryptid, when fully decomposed, bottoms out in a **one-sided
prefix-sum ledger condition on the residue sequence of its own odometer** — the same SPECIES as `(K)`'s one-sided
density (count-vs-frequency), though with an enormous margin instead of Antihydra's razor edge. The
B1/B2 boundary-graph unification (`BOUNDARY_GRAPH_B1`) sharpens: the walls differ not in kind but in MARGIN. o4's
decision is now the explicit conjecture: *the base-4/3 orbit `G↦⌊4G/3⌋+c` from G=3 never accumulates
`#{ρ=1} − 4#{ρ=2} − 6#{ρ=0} > a_0 − 2` in any prefix ending at a ρ=1 step* — Collatz-like, checkable, with drift.

## 6. Soundness ledger `[discipline]`
- All lemmas verified by exact concrete simulation on constructed configs (no acceleration in the proof path); the
  macro-machine used ONLY for template discovery, not for proof steps.
- The composition/locality argument is stated explicitly (§2); it is the standard certified-bouncer soundness argument.
  **Red-team of the composition argument queued** — until then the lemma labels carry "[PROVEN, certified-template
  method]" with this caveat.
- The halting config `Z(41,3,0)` is a STANDALONE config; NOT claimed reachable from o4's initial tape — reachability
  of small-a at g=3 is exactly the open ledger question.
- o4 `[OPEN]`. **No machine decided. No label upgraded.**

## Reproduce
- `o4_body_proof.py` (body lemma, k up to 251); inline: prefix (12 configs, single hash), suffix grid (3 classes ×
  {19,21,23,41} × {8,12,30} + small-a 0..7 × {19,21,41}), odometer derivation, `Z(41,3,0)` halt.
- Template discovery: instrumented `o4_bouncer_macro.py` (event-stream hashes; zone dumps at body boundaries).
- Basis: `O4_SEAM_PARITY_LEMMA_2026-07-06`, `O4_WINDOW_SATURATION_2026-07-06`, `o4_bouncer_macro.py` (validated).
