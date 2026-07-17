"""x2b5_sawtooth.py -- the B5 register sawtooth: are the RESETS a doubling carry cascade?

Records the register (max 1-run) at every left-record milestone in state C, then
analyses the sawtooth: reset depths, the milestone index of each reset, and the
gaps between resets of equal depth. A binary-odometer carry cascade predicts
depth-m resets occurring every ~2^m milestones.
"""
import sys
from collections import Counter, defaultdict
from x2b5_sim import RULES, maxrun_full

def run(max_steps):
    cells = {}; pos = 0; state = 'A'; lo = 0
    traj = []   # (milestone_idx, step, register)
    for step in range(max_steps):
        sym = cells.get(pos, 0)
        rule = RULES[state][sym]
        if rule is None:
            print("*** HALT", step); break
        w, mv, nxt = rule
        if w != sym:
            if w: cells[pos] = 1
            else: del cells[pos]
        pos += mv; state = nxt
        if pos < lo:
            lo = pos
            if state == 'C':
                traj.append((len(traj), step, maxrun_full(cells)))
    return traj

if __name__ == '__main__':
    cap = int(sys.argv[1]) if len(sys.argv) > 1 else 6_000_000
    traj = run(cap)
    print(f"milestones: {len(traj)}  register {traj[0][2]} .. {traj[-1][2]}")
    resets = []
    for i in range(1, len(traj)):
        d = traj[i][2] - traj[i-1][2]
        if d < 0:
            resets.append((i, traj[i][1], -d, traj[i-1][2], traj[i][2]))
    print(f"\n# resets (drops): {len(resets)}")
    print(f"{'mile':>6} {'step':>10} {'depth':>7} {'peak':>7} {'floor':>7}  depth=3(2^m-1)?")
    for i, s, d, pk, fl in resets:
        m = None
        if d % 3 == 0 and (d // 3 + 1) and ((d // 3 + 1) & (d // 3)) == 0:
            m = (d // 3 + 1).bit_length() - 1
        print(f"{i:>6} {s:>10} {d:>7} {pk:>7} {fl:>7}  {'m='+str(m) if m else 'NO'}")
    print("\n# depth histogram:", dict(sorted(Counter(r[2] for r in resets).items())))
    bydepth = defaultdict(list)
    for i, s, d, pk, fl in resets: bydepth[d].append(i)
    print("\n# milestone gaps between resets of the SAME depth (odometer predicts ~2^m):")
    for d in sorted(bydepth):
        idx = bydepth[d]
        gaps = [idx[j+1]-idx[j] for j in range(len(idx)-1)]
        print(f"  depth {d:>5}: n={len(idx):>3} gaps={gaps}")
