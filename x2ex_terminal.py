#!/usr/bin/env python3
"""x2ex_terminal.py -- DECISIVE terminal-glue measurement.

For each E-on-0 anchor across the carry EXITs, record the tape BACKGROUND
(left-solid ones = the just-doubled block above; right block structure) and the
gap to the next anchor.  Goal: is the TERMINAL glue length a clean function of
the local background block size (and is that block size a clean f(j))?

Also locate the level-6 EXIT window to get a 4th data point.
"""
import sys
sys.path.insert(0, '/Users/aokiyousuke/busybeaver')
from x2bd_sim import build


def left_solid(sim):
    L = sim.L; i = 0
    while i < len(L) and L[-1 - i] == 1:
        i += 1
    return i


def right_runs(sim, k=6):
    return sim.right_runs(k)


def snap(sim):
    return dict(n=sim.n, pos=sim.pos, lsolid=left_solid(sim),
                rruns=right_runs(sim), lones=sim.left_ones())


def collect_anchors(n0, n1):
    """all E-on-0 anchors in [n0,n1], with tape background snapshot."""
    sim = build(2); sim.step()
    while sim.n < n0:
        assert sim.step()
    A = []
    while sim.n <= n1:
        if sim.st == 'E' and sim.h == 0:
            A.append(snap(sim))
        if not sim.step():
            break
    return A


def report_window(j, n0, n1):
    A = collect_anchors(n0, n1)
    print(f"\n===== EXIT({j}) = [{n0},{n1}]  ({n1-n0} steps, {len(A)} anchors) =====")
    print("   n       gap   lsolid  lones   right-runs(head-first)")
    for i, a in enumerate(A):
        gap = (A[i+1]['n'] - a['n']) if i+1 < len(A) else None
        rr = " ".join(f"{'1' if b else '0'}^{c}" for b, c in a['rruns'])
        gaps = f"{gap:>4}" if gap is not None else "  --"
        print(f"  {a['n']:<7} {gaps}  {a['lsolid']:>5}  {a['lones']:>5}   {rr}")
    return A


EXITS = {3: (6638, 6708), 4: (6923, 7141), 5: (8076, 8798)}


def find_level6():
    """Scan forward past EXIT(5) to find the level-6 CORE (sweepEF62, i.e. a
    maximal gap==2 lsolid+2 chain of length ~62) and the following carry end."""
    sim = build(2); sim.step()
    # collect E-on-0 anchors past 8798, tracking big sweepEF chains
    anchors = []
    cap = 60_000
    while sim.n < cap:
        if sim.st == 'E' and sim.h == 0:
            anchors.append(snap(sim))
        if not sim.step():
            print("HALT", sim.n); break
    # find maximal sweepEF chains
    print(f"\n[find_level6] scanned to n={sim.n}, {len(anchors)} anchors total")
    # locate biggest sweepEF chain after 8798
    best = None
    i = 0
    N = len(anchors)
    chains = []
    while i < N - 1:
        if anchors[i+1]['n'] - anchors[i]['n'] == 2 and \
           anchors[i+1]['lsolid'] == anchors[i]['lsolid'] + 2:
            k = i
            while k < N-1 and anchors[k+1]['n']-anchors[k]['n'] == 2 and \
                  anchors[k+1]['lsolid'] == anchors[k]['lsolid']+2:
                k += 1
            m = (anchors[k]['n'] - anchors[i]['n'])//2
            chains.append((m, anchors[i]['n'], anchors[k]['n']))
            i = k
        else:
            i += 1
    # the biggest chains are the per-level COREs
    chains_sorted = sorted(chains, key=lambda c: -c[0])[:8]
    print("[find_level6] biggest sweepEF chains (m, start_n, end_n):")
    for m, s, e in chains_sorted:
        print(f"    sweepEF{m}  core ends at n={e}")
    return anchors, chains


if __name__ == "__main__":
    print("=" * 70)
    print("TERMINAL / BACKGROUND MEASUREMENT at each E-on-0 anchor")
    print("=" * 70)
    for j, (a, b) in EXITS.items():
        report_window(j, a, b)
    find_level6()
