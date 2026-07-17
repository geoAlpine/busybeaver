#!/usr/bin/env python3
"""x2r6_gen.py -- emit the Lean `regen6_transport` chunks for REGEN(6) (722 steps),
and CHECK the uniform REGEN(k) IN/OUT family law against k=4,5,6.

The ∀ L R abstraction is cut at FIXED ABSOLUTE tape positions outside the measured head
excursion (x2r6_regen6.py): a cell never visited in the window is a legitimate Lean
parameter, and a fixed absolute cut makes L/R name the same cells in every chunk so the
chunks compose under `steps_add`.  Lean's kernel `rfl` is the final judge.

SIMULATOR EVIDENCE.  The emitted Lean is proved independently by the kernel.
"""
import sys
sys.path.insert(0, '/Users/aokiyousuke/busybeaver')
from x2bd_sim import build

EXITSITE = {4: 6708, 5: 13453, 6: 33830, 7: 114703}
def exitSteps(k): return 2**(2*k-3) + k*2**(k-1) + 2**(k-2) + 2


def snap(n):
    sim = build(2); sim.step()
    while sim.n < n:
        assert sim.step()
    return sim


def descCascade(d):
    if d == 0: return [1]
    return [1]*(2**(d+2)-3) + [0,0] + descCascade(d-1)


def lean_list(bits, tail):
    return "".join(("true :: " if b else "false :: ") for b in bits) + tail


def window(k, slack=1):
    """Window + the ABSOLUTE tape-position cut boundaries for the `∀ L R` abstraction.

    `loCut` / `hiCut` are absolute positions strictly OUTSIDE the measured head
    excursion, so every cell at pos <= loCut (resp. >= hiCut) is never read or
    written in the window and is therefore a legitimate Lean parameter.  The cut
    must be a FIXED absolute position -- NOT a fixed depth from each chunk's head,
    which would make L/R name different cells in different chunks and break the
    composition by `steps_add`.
    """
    e = EXITSITE[k]; L = exitSteps(k); s = e - L
    sim = snap(s)
    lo = hi = sim.pos
    while sim.n < e:
        sim.step(); lo = min(lo, sim.pos); hi = max(hi, sim.pos)
    return s, e, L, lo - slack, hi + slack


def cfg_at(n, loCut, hiCut):
    """Lean view at raw n, with `left` truncated at absolute pos loCut and `right`
    at absolute pos hiCut (those cells and beyond become the parameters L / R)."""
    sim = snap(n)
    P = sim.pos
    nL = P - loCut          # left[j] sits at pos P-1-j; keep j <= P-1-loCut
    nR = hiCut - P          # right[j] sits at pos P+1+j; keep j <= hiCut-P-1
    assert nL >= 0 and nR >= 0
    left = (sim.L[::-1] + [0]*(nL+8))[:nL]
    right = (sim.R[::-1] + [0]*(nR+8))[:nR]
    return sim.st, P, left, sim.h, right


def check_in_family(k):
    """Is IN(k) = E, <ones(2^k-3) ++ 0::1::0::0:: 1 :: pow01(2^(k-1)-2) ++ marker,
                     false, false :: descCascade(k-4) ++ zeros z ++ R> ?

    NOTE descCascade(k-4), not (k-3): REGEN(k)'s IN carries the cascade TWO layers below
    cascadeReg(k)'s descCascade(k-2).  One layer is rebuilt by the exit, the other is the
    IN's own left block ones(2^k-3) folded over.  (lean/X2.lean §5ai `regenIn`.)"""
    s = EXITSITE[k] - exitSteps(k)
    sim = snap(s)
    left = sim.L[::-1]; right = sim.R[::-1] + [0]*80
    N = 2**(k-1) - 2
    pred_left = [1]*(2**k - 3) + [0,1,0,0] + [1] + [0,1]*N
    pred_right = [0] + descCascade(k-4)
    okl = left[:len(pred_left)] == pred_left
    okr = right[:len(pred_right)] == pred_right
    okh = (sim.st == 'E' and sim.h == 0)
    # zeros run after the cascade, before the (untouched) R
    z = 0
    while len(pred_right)+z < len(right) and right[len(pred_right)+z] == 0: z += 1
    return okh, okl, okr, z, sim.pos


if __name__ == "__main__":
    print("=== THE UNIFORM REGEN(k) IN-FAMILY LAW, tested k=4,5,6,7 ===")
    print("  IN(k) = <E, p, [ ones(2^k-3) ++ 0 1 0 0 ++ 1 :: pow01(2^(k-1)-2) ++ marker,")
    print("                   head=0, 0 :: descCascade(k-4) ++ 0^j ++ R ]>")
    for k in (4, 5, 6, 7):
        okh, okl, okr, z, pos = check_in_family(k)
        print(f"  k={k}: state/head E,0={okh}  left law={okl}  right law={okr}  "
              f"zeros-run after cascade >= {z}  (IN pos={pos})")

    print("\n=== OUT: p law  p_out = p_in - 2^k ===")
    for k in (4, 5, 6, 7):
        a = snap(EXITSITE[k] - exitSteps(k)).pos
        b = snap(EXITSITE[k]).pos
        print(f"  k={k}: delta = {b-a}   -2^k = {-2**k}   match={b-a == -2**k}")

    # ---- emit the Lean for k=6
    k = 6
    s, e, L, loCut, hiCut = window(k)
    print(f"\n=== REGEN(6) Lean emission: window [{s},{e}] {L} steps, "
          f"abstract at abs pos <= {loCut} (L) and >= {hiCut} (R) ===")
    st_i, pos_i, left_i, h_i, right_i = cfg_at(s, loCut, hiCut)
    st_o, pos_o, left_o, h_o, right_o = cfg_at(e, loCut, hiCut)
    print(f"  IN  {st_i} pos={pos_i} head={h_i}")
    print(f"  OUT {st_o} pos={pos_o} head={h_o}")

    # chunk the 722 steps; emit each chunk's IN/OUT with the SAME cuts
    CH = 38
    bounds = list(range(s, e, CH)) + [e]
    print(f"  chunks: {len(bounds)-1} of <= {CH} steps")
    out = []
    PSHIFT = pos_i - 11    # re-anchor IN pos to 11 (k=4 used 9, k=5 used 10)
    for i in range(len(bounds)-1):
        a, b = bounds[i], bounds[i+1]
        ca = cfg_at(a, loCut, hiCut); cb = cfg_at(b, loCut, hiCut)
        out.append((i+1, b-a, ca, cb))
    lines = []
    for (i, n, ca, cb) in out:
        for tag, c in (("", ca), ("", cb)):
            pass
        lines.append(
            f"theorem r6_E{i} (L R : List Bool) :\n"
            f"    steps {n} ⟨.{ca[0]}, {ca[1]-PSHIFT}, ⟨{lean_list(ca[2], 'L')}, "
            f"{'true' if ca[3] else 'false'}, {lean_list(ca[4], 'R')}⟩⟩\n"
            f"      = some ⟨.{cb[0]}, {cb[1]-PSHIFT}, ⟨{lean_list(cb[2], 'L')}, "
            f"{'true' if cb[3] else 'false'}, {lean_list(cb[4], 'R')}⟩⟩ :=\n  rfl\n")
    open('/private/tmp/claude-502/-Users-aokiyousuke-busybeaver/'
         '2d8c1f9f-0e02-4aa5-a7fc-fa27256534ce/scratchpad/r6_chunks.lean', 'w').write(
             "\n".join(lines))
    # the composed statement
    ns = [n for (_, n, _, _) in out]
    print(f"  chunk sizes: {ns}  sum={sum(ns)}")
    print(f"  IN  pos (re-anchored) = {pos_i-PSHIFT};  OUT pos = {pos_o-PSHIFT}")
    print(f"  IN  left cells={len(left_i)} right cells={len(right_i)}")
    print(f"  OUT left cells={len(left_o)} right cells={len(right_o)}")
    print("  chunks written to scratchpad/r6_chunks.lean")


def emit_section():
    """Emit the composed §5ai Lean: regen6_transport + the IN-family def."""
    k = 6
    s, e, L, loCut, hiCut = window(k)
    CH = 38
    bounds = list(range(s, e, CH)) + [e]
    PSHIFT = cfg_at(s, loCut, hiCut)[1] - 11
    ci = cfg_at(s, loCut, hiCut); co = cfg_at(e, loCut, hiCut)
    ns = [bounds[i+1]-bounds[i] for i in range(len(bounds)-1)]
    # nested sum "38+(38+(...))"
    nest = str(ns[-1])
    for n in reversed(ns[:-1]):
        nest = f"{n}+({nest})"
    rw = "".join(f"steps_add, r6_E{i+1}, someBind,\n      " for i in range(len(ns)-1))
    rw += f"r6_E{len(ns)}"
    body = (f"theorem regen6_transport (L R : List Bool) :\n"
            f"    steps (exitSteps 6) ⟨.{ci[0]}, {ci[1]-PSHIFT}, ⟨{lean_list(ci[2],'L')}, "
            f"{'true' if ci[3] else 'false'}, {lean_list(ci[4],'R')}⟩⟩\n"
            f"      = some ⟨.{co[0]}, {co[1]-PSHIFT}, ⟨{lean_list(co[2],'L')}, "
            f"{'true' if co[3] else 'false'}, {lean_list(co[4],'R')}⟩⟩ := by\n"
            f"  rw [show exitSteps 6 = {nest} from by decide,\n      {rw}]\n")
    return body, ci, co, PSHIFT


if len(sys.argv) > 1 and sys.argv[1] == 'emit':
    b, ci, co, _ = emit_section()
    open('/private/tmp/claude-502/-Users-aokiyousuke-busybeaver/'
         '2d8c1f9f-0e02-4aa5-a7fc-fa27256534ce/scratchpad/r6_compose.lean', 'w').write(b)
    print("composed regen6_transport written")
    print(f"IN  left {len(ci[2])} cells, right {len(ci[4])} cells")
    print(f"OUT left {len(co[2])} cells, right {len(co[4])} cells, pos {co[1]-(ci[1]-11)}")


def emit_reach6():
    """descent_reach_6: regen6_transport instantiated at L := pow01 30 ++ marker,
    R := zeros 7 ++ R, so the OUT is LITERALLY `cascadeReg 6 1 (-53) marker R`."""
    k = 6
    s, e, L, loCut, hiCut = window(k)
    ci = cfg_at(s, loCut, hiCut); co = cfg_at(e, loCut, hiCut)
    PSHIFT = ci[1] - 11
    N = 2**(k-1) - 2          # 30
    # sanity: IN left = ones(2^k-3) ++ [0,1,0,0,1]  (66 cells), IN right = 0::descCascade(k-4) ++ 0^34
    assert ci[2] == [1]*(2**k-3) + [0,1,0,0,1], "IN left is not the family shape"
    pad = len(ci[4]) - (1 + len(descCascade(k-4)))
    assert ci[4] == [0] + descCascade(k-4) + [0]*pad, "IN right is not the family shape"
    # cascadeReg(k) right prefix length, vs what the OUT emits explicitly
    creg = [0,0,0] + [1]*(2**k-3) + [0,0] + descCascade(k-3) + [0,0] + [0]*7
    tail = len(creg) - len(co[4])
    assert co[4] + [0]*tail == creg, "OUT right is not cascadeReg's right"
    assert co[2] + [0,1]*N == [0,1]*(1+N), "OUT left is not pow01(1+N)"
    stmt = (f"theorem descent_reach_6 (marker R : List Bool) :\n"
            f"    steps (exitSteps 6) ⟨.{ci[0]}, {ci[1]-PSHIFT}, "
            f"⟨{lean_list(ci[2], f'(pow01 {N} ++ marker)')}, "
            f"{'true' if ci[3] else 'false'}, "
            f"{lean_list(ci[4], f'(zeros {tail} ++ R)')}⟩⟩\n"
            f"      = some (cascadeReg 6 1 ({co[1]-PSHIFT}) marker R) := by\n"
            f"  rw [regen6_transport (pow01 {N} ++ marker) (zeros {tail} ++ R)]\n"
            f"  rfl\n")
    return stmt, pad + tail, ci[1]-PSHIFT, co[1]-PSHIFT


if len(sys.argv) > 1 and sys.argv[1] == 'reach':
    st, zpad, pin, pout = emit_reach6()
    open('/private/tmp/claude-502/-Users-aokiyousuke-busybeaver/'
         '2d8c1f9f-0e02-4aa5-a7fc-fa27256534ce/scratchpad/r6_reach.lean', 'w').write(st)
    print(f"descent_reach_6 emitted.  regenIn pad z = {zpad}, p_in = {pin}, p_out = {pout}")
    print(f"  p_out == p_in - 2^6 ?  {pout == pin - 64}")
