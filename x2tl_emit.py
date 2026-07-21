#!/usr/bin/env python3
"""Emit the §5bg Lean patch: TrailLaw 6 (and 7) by chunked kernel rfl."""
import json, sys
from x2tl_gen import *

CAP = 30

def boundaries(k, cap=CAP):
    N = trailSteps(k)
    inn, out = build(k)
    tr = run(inn, N)
    pos = [c[1] for c in tr]
    turns = [i for i in range(1, N) if (pos[i] - pos[i - 1]) * (pos[i + 1] - pos[i]) < 0]
    b, prev = [], 0
    while prev < N:
        cand = [t for t in turns if prev < t <= prev + cap]
        nxt = max(cand) if cand else min(prev + cap, N)
        if N - nxt < 6:
            nxt = N
        b.append(nxt); prev = nxt
    return b, tr

HDR = """/-! ### §5bg (2026-07-21) `TrailLaw {k}` PROVED -- the trailing word by chunked kernel `rfl`.

**WHAT THIS SECTION ESTABLISHES.**  `TrailLaw {k}` (§5bf) is no longer a measured-only `Prop`:
it is a THEOREM, `trailLaw_{k}`.  The monolithic `trailSteps {k} = {N}`-step symbolic `rfl`
exceeds the elaborator (§5bf), so the run is cut into {NC} chunks (`tl{k}_1 ... tl{k}_{NC}`)
whose boundaries sit at the run's TURNING POINTS (head-direction reversals), each discharged by
kernel `rfl` with FREE `marker`/`R` tails, and composed by `steps_add` into `trailOut_{k}`.
`trailOut_{k}` is stated at the concrete anchor `pos {ANCH}` (`= 2^{k} - {k} - 44`);
`steps_pos_shift` (§5ai) lifts it to the `forall p : Int` anchor `TrailLaw {k}` demands -- the
position translation is a PROVEN lemma of the machine, not a re-run.

The IN and OUT families are built ONLY from the definitions (`cascadeReg`, `depStack`,
`regenWord`, `zeros`); nothing is lifted off the orbit and fed back into its own test.  The
`some` on the right of every chunk certifies the segment is HALT-FREE.  No `sorry`, no `axiom`,
no `native_decide`, no Mathlib.  `[propext, Quot.sound]`. -/
"""

CHUNKDOC = ("set_option maxRecDepth 100000 in\n"
            "/-- Trailing-word `k={k}` chunk {i}/{NC} (turning-point cut), kernel `rfl`, tails FREE. -/")

OUTDOC = """set_option maxRecDepth 100000 in
/-- **THE TRAILING WORD, `k={k}`, AT THE CONCRETE ANCHOR** -- `trailSteps {k} = {N}` steps from the
floor `cascadeReg 4` (carrying `depStack {k} (regenWord {k} ++ marker)` on the left and the forced
`0^16` pad on the right) to `cascadeReg {k}`, `marker`/`R` FREE.  {NC} turning-point chunks by
kernel `rfl`, composed by `steps_add`.  `some` implies HALT-FREE.  `[propext, Quot.sound]`. -/
theorem trailOut_{k} (marker R : List Bool) :
    steps {N} {IN}
      = some {OUT} := by
{COMP}
"""

LAWDOC = """set_option maxRecDepth 100000 in
/-- **`TrailLaw {k}` -- PROVED.**  `trailOut_{k}` at the concrete anchor `pos {ANCH} = 2^{k} - {k} - 44`,
lifted to every `p : Int` by `steps_pos_shift` (translation in `pos` is a proven lemma of the
machine -- `step` never reads `pos`).  So the trailing seam of §5bf is a THEOREM at `k={k}`, not a
measurement.  `[propext, Quot.sound]`. -/
theorem trailLaw_{k} : TrailLaw {k} := by
  intro p marker R
  have hp : ((2 : Int)) ^ ({k} : Nat) = {P} := by decide
  have e1 : p + 2 ^ ({k} : Nat) - (({k} : Nat) : Int) - 44 = {ANCH} + p := by rw [hp]; omega
  have e2 : p - 2 ^ ({k} : Nat) = -{P} + p := by rw [hp]; omega
  have h := steps_pos_shift (d := p) (trailOut_{k} marker R)
  show steps (trailSteps {k})
      (cascadeReg 4 1 (p + 2 ^ ({k} : Nat) - (({k} : Nat) : Int) - 44)
        (depStack {k} (regenWord {k} ++ marker)) (zeros 16 ++ R))
    = some (cascadeReg {k} 1 (p - 2 ^ ({k} : Nat)) marker R)
  rw [e1, e2]
  exact h

-- AXIOM AUDIT -- §5bg (the trailing law at k={k}).  All `[propext, Quot.sound]`.
#print axioms trailOut_{k}
#print axioms trailLaw_{k}
"""


def emit_k(k, header=True):
    b, tr = boundaries(k)
    N = trailSteps(k)
    NC = len(b)
    ANCH = 2 ** k - k - 44
    P = 2 ** k
    lines, names, tr = emit(k, b, 'tl%d' % k)
    parts = []
    if header:
        parts.append(HDR.format(k=k, N=N, NC=NC, ANCH=ANCH))
    for i, ln in enumerate(lines):
        parts.append(CHUNKDOC.format(k=k, i=i + 1, NC=NC))
        parts.append(ln)
    comp, rem = [], N
    for i, (nm, sz) in enumerate(names):
        if i == len(names) - 1:
            comp.append('  exact %s marker R' % nm)
            break
        comp.append('  rw [show (%d : Nat) = %d + %d from by decide, steps_add, %s, someBind]'
                    % (rem, sz, rem - sz, nm))
        rem -= sz
    parts.append(OUTDOC.format(k=k, N=N, NC=NC, IN=lean_cfg(tr[0]),
                               OUT=lean_cfg(tr[-1]), COMP='\n'.join(comp)))
    parts.append(LAWDOC.format(k=k, ANCH=ANCH, P=P))
    return '\n'.join(parts), b


if __name__ == '__main__':
    k = int(sys.argv[1])
    txt, b = emit_k(k)
    path = sys.argv[2] if len(sys.argv) > 2 else '/tmp/patch%d.lean' % k
    open(path, 'w').write(txt)
    print('k=%d  chunks=%d  sizes=%s' % (k, len(b),
          [b[i] - (b[i - 1] if i else 0) for i in range(len(b))]))
    print('wrote', path, len(txt), 'bytes')
