#!/usr/bin/env python3
"""x2ex_termglue.py -- is the block-final TERMINAL glue a reusable translation-
invariant transport at fixed k?  The k=4 terminal (g41, lays 1^13) occurs at
EXIT(3)@6667 and EXIT(5)@8259; the k=5 terminal (g74, lays 1^29) at EXIT(4)@7067
and EXIT(6)@13379.  Compare (st,h,dpos) traces; emit windowed Lean configs.

Also the DECISIVE non-f(j) check: the two 144-step regeneration prefixes inside
EXIT(5) (8115->8259 and 8515->8659) -- identical (st,h,dpos) -- then diverge at
the terminal (41 vs 139).
"""
import sys
sys.path.insert(0, '/Users/aokiyousuke/busybeaver')
from x2bd_sim import build


def local_trace(n0, n1):
    sim = build(2); sim.step()
    while sim.n < n0:
        assert sim.step()
    base = sim.pos
    tr = []
    while sim.n < n1:
        tr.append((sim.st, sim.h, sim.pos - base))
        assert sim.step()
    return tr


def cell_at(sim, abspos):
    d = abspos - sim.pos
    if d == 0:
        return sim.h
    if d < 0:
        idx = -d - 1
        return sim.L[-1 - idx] if idx < len(sim.L) else 0
    idx = d - 1
    return sim.R[-1 - idx] if idx < len(sim.R) else 0


def run_window(n0, n1):
    sim = build(2); sim.step()
    while sim.n < n0:
        assert sim.step()
    base = sim.pos
    s2 = build(2); s2.step()
    while s2.n < n0:
        assert s2.step()
    dmin = dmax = 0
    while s2.n < n1:
        assert s2.step()
        dmin = min(dmin, s2.pos - base); dmax = max(dmax, s2.pos - base)

    def windowed(sm):
        pos = sm.pos
        left = [cell_at(sm, k) for k in range(pos - 1, base + dmin - 1, -1)]
        right = [cell_at(sm, k) for k in range(pos + 1, base + dmax + 1)]
        return sm.st, sm.pos - base, sm.h, left, right
    a = windowed(sim)
    while sim.n < n1:
        assert sim.step()
    b = windowed(sim)
    return dmin, dmax, a, b


def cmp_trace(name, w1, w2):
    t1 = local_trace(*w1); t2 = local_trace(*w2)
    print(f"{name}: len {len(t1)} vs {len(t2)}; identical={t1 == t2}")
    return t1 == t2


def main():
    print("== TERMINAL glue translation-invariance (same k) ==")
    cmp_trace("k=4 term (g41): EXIT3@6667 vs EXIT5@8259", (6667, 6708), (8259, 8300))
    cmp_trace("k=5 term (g74): EXIT4@7067 vs EXIT6@13379", (7067, 7141), (13379, 13453))

    print("\n== DECISIVE: two 144-step regen prefixes in EXIT(5) identical, "
          "terminals differ ==")
    p1 = local_trace(8115, 8259)   # first S-block prefix
    p2 = local_trace(8515, 8659)   # second S-block prefix
    print(f"  prefix1[8115,8259] len={len(p1)}  prefix2[8515,8659] len={len(p2)}  "
          f"identical={p1 == p2}")
    print(f"  then terminal1 gap = {8300-8259}=41 (k=4)  terminal2 gap = "
          f"{8798-8659}=139 (k=6)   -> SAME structure, DIFFERENT terminal")

    print("\n== windowed Lean config for k=4 terminal (g41, EXIT3@6667) ==")
    dmin, dmax, A, B = run_window(6667, 6708)
    print(f"  excursion rel [{dmin},{dmax}], 41 steps, window {len(A[3])}L+1+{len(A[4])}R")
    print(f"  start: st={A[0]} rel={A[1]} h={A[2]}")
    print(f"    L={A[3]}")
    print(f"    R={A[4]}")
    print(f"  end:   st={B[0]} rel={B[1]} h={B[2]}")
    print(f"    L={B[3]}")
    print(f"    R={B[4]}")


if __name__ == "__main__":
    main()


def bit(b): return "true" if b else "false"
def cons(cells, tail): return "".join(bit(c) + " :: " for c in cells) + tail

def emit(name, n0, n1, doc):
    dmin, dmax, A, B = run_window(n0, n1)
    st0, rel0, h0, l0, r0 = A
    st1, rel1, h1, l1, r1 = B
    ci = f"⟨.{st0}, {rel0}, ⟨{cons(l0,'L')}, {bit(h0)}, {cons(r0,'R')}⟩⟩"
    co = f"⟨.{st1}, {rel1}, ⟨{cons(l1,'L')}, {bit(h1)}, {cons(r1,'R')}⟩⟩"
    print(f"-- {doc}")
    print(f"-- excursion rel [{dmin},{dmax}], {n1-n0} steps, window {len(l0)}L+1+{len(r0)}R")
    print("set_option maxRecDepth 8000 in")
    print("set_option maxHeartbeats 4000000 in")
    print(f"theorem {name} (L R : List Bool) :")
    print(f"    steps {n1-n0} {ci}")
    print(f"      = some {co} :=")
    print("  rfl\n")

def emit_all():
    print("\n\n========== LEAN EMIT ==========")
    emit("exit_terminal_k4", 6667, 6708,
         "EXIT k=4 TERMINAL glue g41 (lays 1^13): TERM(4)=2^5+4+5=41, transl-inv EXIT3/EXIT5")
    emit("exit_terminal_k5", 7067, 7141,
         "EXIT k=5 TERMINAL glue g74 (lays 1^29): TERM(5)=2^6+5+5=74, transl-inv EXIT4/EXIT6")
