#!/usr/bin/env python3
"""x2cs_j4gen.py -- generate the §5u Lean code for the depth-2 (j=4) carry,
factored through carry_event_5to13 (embedded j=3 carry, REUSED) and sweepEF 14
(= carry_repack 2 translated, the CORE, REUSED), with cell-exact rfl connectors.
All cell values taken from the faithful x2bd_sim.build(2) orbit.
"""
import sys
sys.path.insert(0, '/Users/aokiyousuke/busybeaver')
from x2bd_sim import build

ANCHOR = 2069
LO, HI = 2046, 2105

def cell_at(sim, abspos):
    d = abspos - sim.pos
    if d == 0:
        return sim.h
    if d < 0:
        idx = -d - 1
        return sim.L[-1 - idx] if idx < len(sim.L) else 0
    idx = d - 1
    return sim.R[-1 - idx] if idx < len(sim.R) else 0

def snap(sim):
    rel = sim.pos - ANCHOR
    left = [cell_at(sim, sim.pos - k) for k in range(1, sim.pos - LO + 1)]
    right = [cell_at(sim, sim.pos + k) for k in range(1, HI - sim.pos + 1)]
    return {'n': sim.n, 'st': sim.st, 'rel': rel, 'h': sim.h,
            'left': left, 'right': right}

def bit(b): return "true" if b else "false"

def cons(cells, tail):
    s = "".join(bit(c) + " :: " for c in cells)
    return s + tail

def cfg(st, rel, leftstr, h, rightstr):
    return (f"⟨.{st}, {rel}, ⟨{leftstr}, {bit(h)}, {rightstr}⟩⟩")

BOUNDS = [6484, 6523, 6562, 6591, 6708, 6747, 6786, 6825, 6864,
          6895, 6923, 6962, 7001, 7040, 7079, 7118, 7141]

def main():
    sim = build(2); sim.step()
    S = {}
    bset = set(BOUNDS)
    while True:
        if sim.n in bset:
            S[sim.n] = snap(sim)
        if sim.n >= BOUNDS[-1]:
            break
        assert sim.step()

    OPTS = "set_option maxRecDepth 8000 in\nset_option maxHeartbeats 4000000 in\n"

    def rfl_chunk(name, k, n0, n1, in_left=None, out_right=None):
        a, b = S[n0], S[n1]
        lin = in_left if in_left else cons(a['left'], "L")
        lout = cons(b['left'], "L")
        rin = cons(a['right'], "R")
        rout = out_right if out_right else cons(b['right'], "R")
        ci = cfg(a['st'], a['rel'], lin, a['h'], rin)
        co = cfg(b['st'], b['rel'], lout, b['h'], rout)
        return (f"{OPTS}theorem {name} (L R : List Bool) :\n"
                f"    steps {k} {ci}\n      = some {co} :=\n  rfl\n")

    out = []
    # ENTRY A: 6484->6591 (107) as 39+39+29, reaching the j=3 carry start
    out.append(rfl_chunk("j4_A1", 39, 6484, 6523))
    out.append(rfl_chunk("j4_A2", 39, 6523, 6562))
    out.append(rfl_chunk("j4_A3", 29, 6562, 6591))

    # B: the embedded j=3 carry -- REUSE carry_event_5to13.
    a, b = S[6591], S[6708]
    # carry_event_5to13 input prefix: 10 left cells, 12+10 right cells.
    L13 = a['left'][10:]          # cells 11..23 -> carry's L arg
    R14 = a['right'][22:]         # cells 23..36 -> carry's R arg (all false)
    assert a['left'][:10] == [0,1,0,1,0,1,0,0,1,0], a['left'][:10]
    assert a['right'][:12] == [0,0,0,1,1,1,1,1,0,0,1,0], a['right'][:12]
    assert a['right'][12:22] == [0]*10
    assert all(c == 0 for c in R14), R14
    ci = cfg('E', 0, cons(a['left'], "L"), a['h'], cons(a['right'], "R"))
    co = cfg('E', -7, cons(b['left'], "L"), b['h'], cons(b['right'], "R"))
    out.append(
        "/-- **B: the embedded j=3 carry -- REUSE of `carry_event_5to13`.**  Inside the\n"
        "j=4 carry, raw n=6591->6708 IS the j=3 carry (block 5->13); we discharge it by the\n"
        "already-proven `carry_event_5to13`, instantiating its tails.  This is the WF\n"
        "recursion's inductive step made concrete: carry(4) reuses carry(3). -/\n"
        f"theorem j4_carry_B (L R : List Bool) :\n"
        f"    steps 117 {ci}\n      = some {co} :=\n"
        f"  carry_event_5to13 ({cons(L13,'L')}) ({cons(R14,'R')})\n")

    # C: middle connector 6708->6895 (187) as 39*4+31; C5 outputs pow10 14 form.
    out.append(rfl_chunk("j4_C1", 39, 6708, 6747))
    out.append(rfl_chunk("j4_C2", 39, 6747, 6786))
    out.append(rfl_chunk("j4_C3", 39, 6786, 6825))
    out.append(rfl_chunk("j4_C4", 39, 6825, 6864))
    c5 = S[6895]
    assert c5['right'][:28] == [1,0]*14, c5['right'][:28]
    R26 = c5['right'][28:]
    L5 = c5['left']
    assert L5 == [1,0,1,0,0], L5
    c5_out_right = "pow10 14 ++ (" + cons(R26, "R") + ")"
    out.append(rfl_chunk("j4_C5", 31, 6864, 6895, out_right=c5_out_right))

    # D: the CORE culminating repack -- REUSE sweepEF 14 (= carry_repack 2 translated).
    d0 = S[6895]; d1 = S[6923]
    din_left = cons(L5, "L")
    din_right = "pow10 14 ++ (" + cons(R26, "R") + ")"
    dout_left = "ones 28 ++ (" + cons(L5, "L") + ")"
    dout_right = cons(R26, "R")
    assert d1['left'][:28] == [1]*28
    assert d1['left'][28:] == L5, (d1['left'][28:], L5)
    assert d1['right'] == R26, (d1['right'], R26)
    ci = cfg('E', -18, din_left, 0, din_right)
    co = cfg('E', 10, dout_left, 0, dout_right)
    out.append(
        "/-- **D: the CORE culminating repack -- REUSE of the parametric `sweepEF`.**  Raw\n"
        "n=6895->6923 (28 steps): the block-doubling repack `(10)^14 -> 1^28` (block 13->29).\n"
        "This IS `carry_repack 2` (`sweepEF 14`) translated to head rel -18 -- the SAME\n"
        "∀-length doubling engine as the j=3 CORE (`carry_core_j3` = `sweepEF 6`), one level\n"
        "up.  `some` ⇒ HALT-FREE. -/\n"
        f"theorem j4_core_D (L R : List Bool) :\n"
        f"    steps 28 {ci}\n      = some {co} := by\n"
        f"  rw [sweepEF 14 (-18) ({cons(L5,'L')}) ({cons(R26,'R')})]\n"
        f"  exact congrArg some (cfgPos (by decide))\n")

    # E: exit connector 6923->7141 (218) as 39*5+23; E1 inputs ones 28 form.
    e1_in_left = "ones 28 ++ (" + cons(L5, "L") + ")"
    out.append(rfl_chunk("j4_E1", 39, 6923, 6962, in_left=e1_in_left))
    out.append(rfl_chunk("j4_E2", 39, 6962, 7001))
    out.append(rfl_chunk("j4_E3", 39, 7001, 7040))
    out.append(rfl_chunk("j4_E4", 39, 7040, 7079))
    out.append(rfl_chunk("j4_E5", 39, 7079, 7118))
    out.append(rfl_chunk("j4_E6", 23, 7118, 7141))

    # Final composition.
    a, b = S[6484], S[7141]
    ci = cfg('E', a['rel'], cons(a['left'], "L"), a['h'], cons(a['right'], "R"))
    co = cfg('E', b['rel'], cons(b['left'], "L"), b['h'], cons(b['right'], "R"))
    nested = "39+(39+(29+(117+(39+(39+(39+(39+(31+(28+(39+(39+(39+(39+(39+23))))))))))))))"
    # verify sum AND paren balance
    assert eval(nested) == 657
    assert nested.count('(') == nested.count(')') == 14
    steps_lemmas = ["j4_A1","j4_A2","j4_A3","j4_carry_B","j4_C1","j4_C2","j4_C3",
                    "j4_C4","j4_C5","j4_core_D","j4_E1","j4_E2","j4_E3","j4_E4","j4_E5"]
    rw = f"  rw [show (657 : Nat) = {nested} from rfl,\n"
    for lem in steps_lemmas:
        rw += f"      steps_add, {lem}, someBind,\n"
    rw += "      j4_E6]\n"
    out.append(
        "/-- **THE DEPTH-2 (j=4) ON-PATH CARRY, FACTORED THROUGH THE j=3 CARRY.**  Raw g=2\n"
        "orbit n=6484->7141 (657 steps): the level-4 block-doubling carry (block 13->29 with a\n"
        "fresh 1^13 regenerated below), tail-parametric.  Assembled by `steps_add` from:\n"
        "ENTRY (rfl) ∘ **carry_event_5to13** (the embedded j=3 carry, REUSED) ∘ MIDDLE (rfl)\n"
        "∘ **sweepEF 14** (the CORE repack = carry_repack 2, REUSED) ∘ EXIT (rfl).  The\n"
        "recursion's inductive step realized concretely: carry(4) is BUILT from carry(3) and\n"
        "the ∀-length repack engine.  Cross-checked cell-for-cell against the raw orbit.\n"
        "`some` ⇒ HALT-FREE.  `[propext, Quot.sound]`-only. -/\n"
        f"theorem carry_j4 (L R : List Bool) :\n"
        f"    steps 657 {ci}\n      = some {co} := by\n" + rw)

    print("\n".join(out))

if __name__ == "__main__":
    main()
