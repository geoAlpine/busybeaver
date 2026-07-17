#!/usr/bin/env python3
"""x2rc_regen_in.py -- on-path check of the REGEN(k) transports' IN configs.

lean/X2.lean's §5ah `descent_reach_4/5` run the already-proven `regen4_transport` /
`regen5_transport` from an EXPLICIT IN config.  This probe confirms those IN configs occur
on the REAL orbit (x2bd_sim.build(2)) at the REGEN window starts §5z records:

    REGEN(4)  [6638, 6708]     REGEN(5)  [13235, 13453]

and that the exits are the descent starts pinned by x2rc_regen_shape.py.  Run-length
parses are MAXIMAL.
"""
import sys
sys.path.insert(0, '/Users/aokiyousuke/busybeaver')
from x2bd_sim import build


def snap(n):
    sim = build(2)
    sim.step()
    while sim.n < n:
        assert sim.step(), f"HALT before {n}"
    return sim


def runs(bits, cap=12):
    out = []
    i = 0
    while i < len(bits) and len(out) < cap:
        j = i
        while j < len(bits) and bits[j] == bits[i]:
            j += 1
        out.append((bits[i], j - i))
        i = j
    return out


def show(tag, n, want_left, want_right):
    sim = snap(n)
    left = [sim.L[-1 - i] for i in range(len(sim.L))]
    right = sim.R[::-1] + [0] * 64        # off-list cells are BLANK
    print(f"\n=== {tag} IN @ raw n={n} ===")
    print(f"  state={sim.st} head={sim.h} pos={sim.pos}")
    print(f"  left  runs: {runs(left, 10)}")
    print(f"  right runs: {runs(right, 10)}")
    ok_l = left[:len(want_left)] == want_left
    ok_r = right[:len(want_right)] == want_right
    print(f"  Lean IN left  prefix matches : {ok_l}")
    print(f"  Lean IN right prefix matches : {ok_r}")
    print(f"  state E, head 0              : {sim.st == 'E' and sim.h == 0}")
    return ok_l and ok_r and sim.st == 'E' and sim.h == 0


if __name__ == "__main__":
    # regen4_transport IN (lean/X2.lean §5z): left = 1^12 ++ [1,0,1,0,0,1,0] ++ L
    #                                         head = 0
    #                                         right = [0,1] ++ 0^11 ++ R
    r4 = show("REGEN(4) = carry_exit_j3",
              6638,
              [1] * 12 + [1, 0, 1, 0, 0, 1, 0],
              [0, 1] + [0] * 11)

    # regen5_transport IN: left = 1^28 ++ [1,0,1,0,0] ++ L
    #                      head = 0
    #                      right = [0] + 1^5 + [0,0,1] + 0^17 ++ R
    r5 = show("REGEN(5) = carry_exit_j4",
              13235,
              [1] * 28 + [1, 0, 1, 0, 0],
              [0] + [1] * 5 + [0, 0, 1] + [0] * 17)

    print("\n=== VERDICT (SIMULATOR evidence) ===")
    print(f"  regen4_transport's IN is on-path at raw 6638  : {r4}")
    print(f"  regen5_transport's IN is on-path at raw 13235 : {r5}")
    print("  (exits 6708 / 13453 are the descent starts -- see x2rc_regen_shape.py)")
