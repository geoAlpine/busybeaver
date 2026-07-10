#!/usr/bin/env python3
"""x2c_closure.py -- bounded-radius local head-window closure (SOUND non-halt over-approx).

A window = (state, cells[-R..+R]) with the head at offset 0. We compute the least set of
windows closed under the ADVERSARIAL microstep: apply the TM transition to the center cell;
the head moves +-1; the window recenters; the cell newly exposed at the far edge came from
OUTSIDE the window, so it is FREE -> branch over {0,1}. Cells shifted past the far edge are
discarded. This over-approximates the real reachable head-windows (real incoming cells are a
subset of {0,1}). Seed = blank tape (all-0 window, state A).

THEOREM (sound): if the closure contains NO halt window (state B reading 1) then the machine
never halts. If it DOES contain the halt window, the radius-R local method is INCONCLUSIVE.

We report, for R = 1..Rmax, whether the halt window is reachable and the closure size. Mirrors
o4_closure_fixpoint.py (the o4 result: HALT window is in the closure at every radius <=5, so
no purely-local certificate proves non-halt)."""
import sys
sys.path.insert(0, '/Users/aokiyousuke/busybeaver')
from mse_extract import parse
from collections import deque

SPEC = "1RB0RE_1RC---_0LD1LE_0RE1LD_1RF0LC_0RA1RE"
STN = "ABCDEF"
M = parse(SPEC)
# halt: state B (index 1) reads 1
HALT_STATE, HALT_SYM = 1, 1


def closure(R, cap=5_000_000):
    W = 2 * R + 1
    start = (0, tuple([0] * W))          # state A, all-zero window, head at center R
    seen = {start}
    q = deque([start])
    halt_reachable = False
    halt_witness = None
    while q:
        st, cells = q.popleft()
        c = cells[R]
        if st == HALT_STATE and c == HALT_SYM:
            halt_reachable = True
            halt_witness = (st, cells)
            break
        act = M[st][c]
        if act is None:
            continue                      # dead-halt transition (only B,1 halts here)
        ww, d, ns = act
        new = list(cells)
        new[R] = ww
        if d == 1:                        # move right: shift window left, expose free cell at right
            base = new[1:] + [None]
            for bit in (0, 1):
                nb = base[:]
                nb[-1] = bit
                nxt = (ns, tuple(nb))
                if nxt not in seen:
                    seen.add(nxt)
                    q.append(nxt)
        else:                             # move left: shift window right, expose free cell at left
            base = [None] + new[:-1]
            for bit in (0, 1):
                nb = base[:]
                nb[0] = bit
                nxt = (ns, tuple(nb))
                if nxt not in seen:
                    seen.add(nxt)
                    q.append(nxt)
        if len(seen) > cap:
            return ('OVERFLOW', len(seen), halt_reachable, halt_witness)
    return ('CLOSED', len(seen), halt_reachable, halt_witness)


if __name__ == "__main__":
    Rmax = int(sys.argv[1]) if len(sys.argv) > 1 else 7
    print("Radius-R local head-window closure (adversarial microstep, SOUND):")
    print("  R : closure-size : halt-window reachable? (reachable => local method INCONCLUSIVE)")
    for R in range(1, Rmax + 1):
        status, size, hr, wit = closure(R)
        tag = "HALT REACHABLE (inconclusive)" if hr else "halt-free => NON-HALT PROVEN"
        print(f"  R={R}: {status} size={size:>8}  {tag}")
        if hr and wit:
            st, cells = wit
            s = ''.join(str(x) for x in cells)
            print(f"        witness: state {STN[st]}, window [{s}] (head at center)")
