#!/usr/bin/env python3
"""x2gp_carry.py -- characterize the CARRY ENTRY/CORE/EXIT at j=3,4,5 (build(2)).

For §5p deliverable (B): is the carry EXIT a BOUNDED connector or a recursive
Θ(2^j) sub-phase?  We locate each carry's culminating repack (the sweepEF run of
m = 2^j-2 tiles = carry_repack), then measure ENTRY (before it) and EXIT (after it,
until the odometer resumes its steady no-carry sweep), and check whether EXIT itself
contains growing sweepEF regeneration runs (=> recursive, not bounded).
"""
import sys
sys.path.insert(0, '/Users/aokiyousuke/busybeaver')
from x2bd_sim import build


def trace(g, n0, n1):
    sim = build(g); sim.step()
    while sim.n < n0:
        assert sim.step()
    ev = [(sim.n, sim.st, sim.pos, sim.h)]
    while sim.n < n1:
        assert sim.step()
        ev.append((sim.n, sim.st, sim.pos, sim.h))
    return ev


def ef_runs(ev):
    runs, i, N = [], 0, len(ev)
    while i < N - 1:
        if ev[i][1] == 'E' and ev[i][3] == 0:
            j, cnt = i, 0
            while (j + 1 < N and ev[j][1] == 'E' and ev[j][3] == 0
                   and ev[j + 1][1] == 'F' and ev[j + 1][2] == ev[j][2] + 1):
                if j + 2 < N and ev[j + 2][1] == 'E':
                    j += 2; cnt += 1
                else:
                    break
            if cnt >= 2:
                runs.append((ev[i][0], ev[j][0], cnt)); i = j; continue
        i += 1
    return runs


# carry windows located from x2ca_trace / §5m provenance (raw g=2 orbit)
# each: design level j, (window_start, window_end), culminating-repack m = 2^j-2
CARRIES = {
    3: (6591, 6708, 6),    # block 5->13,  core (10)^6  -> 1^12  (carry_repack 1)  [full window]
    4: (6484, 7141, 14),   # block 13->29, core (10)^14 -> 1^28  (carry_repack 2)  [full window]
    5: (7137, 8280, 30),   # block 29->61, core (10)^30 -> 1^60  (carry_repack 3)  [window APPROX]
}

print("CARRY DECOMPOSITION (build(2), design levels j=3,4,5):")
print(f"{'j':>2} {'window':>14} {'total':>6} {'ENTRY':>6} {'CORE':>5} {'EXIT':>6} "
      f"{'EXIT sweepEF runs (m)':>28}")
prev_exit = None
for j, (n0, n1, mcore) in CARRIES.items():
    ev = trace(2, n0, n1)
    runs = ef_runs(ev)
    # the CORE = the sweepEF run with cnt == mcore
    core = [r for r in runs if r[2] == mcore]
    if not core:
        print(f"{j:>2}  core m={mcore} not found in [{n0},{n1}] -- adjust window")
        continue
    ca, cb, _ = core[0]
    entry = ca - n0
    core_len = cb - ca
    exit_len = n1 - cb
    exit_runs = [r for r in runs if r[0] > cb]
    exit_ms = [r[2] for r in exit_runs]
    print(f"{j:>2} [{n0:>5},{n1:>5}] {n1-n0:>6} {entry:>6} {core_len:>5} {exit_len:>6} "
          f"{str(exit_ms):>28}")
    prev_exit = exit_len

print("\nREADING (rely on j=3,4 -- full windows; j=5 window is approximate/truncated):")
print(" - CORE = carry_repack (sweepEF, PROVEN forall j in X2.lean §5m):")
print(f"   core = 2*(2^j-2): j3=12, j4=28, j5=60 steps -- matches carry_repack anchors.")
print(" - ENTRY grows fast (35 -> 411 steps, j3->j4) and CONTAINS the ENTIRE lower")
print("   carry: j=4 ENTRY [6484,6895] wraps the whole j=3 carry [6591,6708]")
print("   => the ripple / nested-carry recursion (depth ~ j).")
print(" - EXIT is NOT a bounded connector: j=3 EXIT=70, j=4 EXIT=218 steps (3.1x),")
print("   and each EXIT contains a GROWING sweepEF regeneration run-chain (2,4,6")
print("   tiles) that rebuilds a fresh comb below => a Theta(2^j) recursive")
print("   sub-phase, not a fixed connector.  This is the honest WALL (`carry_step`).")
