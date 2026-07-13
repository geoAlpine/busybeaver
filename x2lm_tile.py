#!/usr/bin/env python3
"""x2lm_tile.py -- verify whether the per-U-unit forward tile is TRANSLATION-INVARIANT.

For even g (g=4, 6), dump the local tape window (a fixed radius around the head)
and (state, head) at the START of each forward-pass round-trip whose length is 14
(the tile anchor). If the windows are IDENTICAL up to translation, the middle is a
clean fixed-shape tile => a length induction is possible. Also dump the FULL config
delta of one tile (start config -> end config) to extract the exact transport.
"""
import sys
sys.path.insert(0, '/Users/aokiyousuke/busybeaver')
from x2bd_sim import build


def to_M3(g):
    sim = build(g)
    sim.step()
    mc = 0
    while True:
        if sim.is_milestone():
            mc += 1
            if mc == 2:
                return sim
        if not sim.step():
            return sim


def window(sim, radius=10):
    """symmetric window of bits around head: returns (state, tuple of bits, head_index)."""
    # reconstruct absolute bit at offset d from head
    def bit(d):
        if d == 0:
            return sim.h
        if d > 0:
            # R stored reversed: R[-1] is nearest (offset +1)
            idx = len(sim.R) - d
            return sim.R[idx] if 0 <= idx < len(sim.R) else 0
        else:
            k = -d - 1
            return sim.L[-1 - k] if 0 <= k < len(sim.L) else 0
    bits = tuple(bit(d) for d in range(-radius, radius + 1))
    return sim.st, bits


def full_cfg(sim):
    return (sim.st, sim.pos, sim.h, tuple(sim.L), tuple(sim.R))


def trace_to_M4(g):
    sim = to_M3(g)
    traj = [(sim.n, full_cfg(sim), window(sim))]
    while True:
        if not sim.step():
            break
        traj.append((sim.n, full_cfg(sim), window(sim)))
        if sim.is_milestone():
            break
    return traj


def forward_tile_starts(traj):
    """find left-turning-points that begin a len-14 forward round-trip."""
    poss = [c[1][1] for c in traj]  # pos
    turns = []
    for i in range(1, len(poss) - 1):
        if poss[i] <= poss[i - 1] and poss[i] < poss[i + 1]:
            turns.append(i)
    turns = [0] + turns + [len(poss) - 1]
    starts = []
    for a, b in zip(turns, turns[1:]):
        length = traj[b][0] - traj[a][0]
        if length == 14:
            starts.append((a, b))
    return starts


def main():
    for g in [4, 6]:
        print(f"\n===== g={g} =====")
        traj = trace_to_M4(g)
        starts = forward_tile_starts(traj)
        print(f"  {len(starts)} len-14 forward tiles")
        prev_win = None
        prev_pos = None
        for (a, b) in starts:
            n, cfg, win = traj[a][0], traj[a][1], traj[a][2]
            st, bits = win
            pos = cfg[1]
            same = "IDENTICAL-window" if (prev_win == win) else "differs"
            shift = "" if prev_pos is None else f" (pos +{pos - prev_pos})"
            print(f"   tile@n={n:4d} pos={pos:3d} st={st} window={bits} [{same}{shift}]")
            prev_win = win
            prev_pos = pos
        # dump one full tile transport (start cfg -> end cfg) for the 2nd tile
        if len(starts) >= 2:
            a, b = starts[1]
            print(f"  --- exact tile transport (n {traj[a][0]}->{traj[b][0]}) ---")
            print("   START:", traj[a][1])
            print("   END  :", traj[b][1])


if __name__ == "__main__":
    main()
