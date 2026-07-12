#!/usr/bin/env python3
"""x2bd_trace.py -- extract the OUTER-STATE sequence of the doubling phase.

Runs the raw sim from M1(g) to M1(g+1); inside the doubling phase (M6->M1(g+1))
snapshots the FULL config at each round-trip boundary.  A round-trip boundary is
taken as an arrival in state E reading a 0 with a comb already deposited on the
left (left contains 1s) -- the recurring "E on the boundary 0" anchor of the
shrinking-comb odometer.  We log a compact tuple and compress runs of identical
signatures.
"""
import sys
sys.path.insert(0, '/Users/aokiyousuke/busybeaver')
from x2bd_sim import Sim, build


def rr(runs):
    return ''.join(f"{'1' if b else '0'}^{c}" for b, c in runs)


def doubling_phase(g, snap='cturn'):
    sim = build(g)
    sim.step()
    miles = 0
    snaps = []
    prev_anchor = False
    prev_state = sim.st
    # counts of macro-ish events
    cturns = 0
    while True:
        if sim.is_milestone():
            miles += 1
            if miles == 5:
                in_doub = True
                snaps.append(('M6', sim.n, snapshot(sim)))
            elif miles == 6:
                snaps.append(('M1n', sim.n, snapshot(sim)))
                break
        if miles >= 5:
            # count C-turns (arrivals in state C)
            if sim.st == 'C' and prev_state != 'C':
                cturns += 1
                if snap == 'cturn':
                    snaps.append(('C', sim.n, snapshot(sim)))
        prev_state = sim.st
        if not sim.step():
            snaps.append(('HALT', sim.n, None)); break
    return snaps, cturns


def snapshot(sim):
    """the candidate outer-state tuple."""
    return {
        'pos': sim.pos,
        'Lones': sim.left_ones(),
        'Ltop': tuple(sim.left_runs_top(8)),
        'Rruns': tuple(sim.right_runs(14)),
    }


def compress(snaps):
    out = []
    for kind, n, s in snaps:
        if kind in ('M6', 'M1n', 'HALT'):
            out.append((kind, n, s, 1))
            continue
        key = (s['Ltop'], s['Rruns']) if s else None
        if out and out[-1][0] == kind and out[-1][2] and (
                (out[-1][2]['Ltop'], out[-1][2]['Rruns']) == key):
            out[-1] = (kind, n, s, out[-1][3] + 1)
        else:
            out.append((kind, n, s, 1))
    return out


if __name__ == "__main__":
    g = int(sys.argv[1]) if len(sys.argv) > 1 else 2
    snaps, cturns = doubling_phase(g)
    print(f"=== g={g}: doubling phase, {cturns} C-turns, {len(snaps)} snaps ===")
    cs = compress(snaps)
    print(f"compressed to {len(cs)} distinct-signature blocks")
    for kind, n, s, cnt in cs[:80]:
        if kind in ('M6', 'M1n', 'HALT'):
            print(f"  [{kind}] n={n} Lones={s['Lones'] if s else '-'} "
                  f"pos={s['pos'] if s else '-'}")
            if s:
                print(f"        R={rr(s['Rruns'])}")
                print(f"        Ltop={rr(s['Ltop'])}")
        else:
            print(f"  Cx{cnt:<4} n~{n} Lones={s['Lones']} pos={s['pos']}  "
                  f"R={rr(s['Rruns'])[:50]}  Ltop={rr(s['Ltop'])[:40]}")
