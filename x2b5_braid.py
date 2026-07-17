"""x2b5_braid.py -- THE decisive probe: is B5's doubling phase LINEAR or Theta(4^k)?

The register (max 1-run, sampled at left-record milestones in state C) is a
SAWTOOTH. Its deep teeth are the real dynamics. For each deep tooth we record
  peak, floor, depth, and the STEP at which it fires.
Laws under test:
  peak_k  == 9*2^k - 1
  floor_k == 3*2^(k+1) + 2
  depth_k == 3*(2^k - 1)  (== peak-floor)
  step_k / step_{k-1} -> 2  (LINEAR, braid-free)  vs  -> 4  (BRAID, = B1/x2 wall)
"""
import sys
from x2b5_sim import RULES, maxrun_full

def run(max_steps):
    cells = {}; pos = 0; state = 'A'; lo = 0
    traj = []
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
                traj.append((step, maxrun_full(cells)))
    return traj

if __name__ == '__main__':
    cap = int(sys.argv[1]) if len(sys.argv) > 1 else 30_000_000
    traj = run(cap)
    # deep teeth: record each reset, keep the DEEPEST-so-far ones (one per level)
    best = {}
    for i in range(1, len(traj)):
        d = traj[i-1][1] - traj[i][1]
        if d > 0:
            pk, fl = traj[i-1][1], traj[i][1]
            if pk not in best:
                best[pk] = (traj[i][0], fl, d, i)
    print(f"{'k':>3} {'peak':>7} {'9*2^k-1':>9} {'floor':>7} {'5*2^k+6/8':>10} {'depth':>7} {'2^(k+2)-7/9':>12} {'step':>12} {'ratio':>7}")
    prev = None
    for k in range(1, 12):
        pk = 9 * 2**k - 1
        if pk not in best: continue
        s, fl, d, mi = best[pk]
        r = (s / prev) if prev else 0
        pf = 5*2**k + (6 if k % 2 else 8)
        pd = pk - pf
        print(f"{k:>3} {pk:>7} {9*2**k-1:>9} {fl:>7} {pf:>10} {d:>7} {pd:>12} {s:>12} {r:>7.3f}")
        prev = s
    print("\nratio -> 2.0 means LINEAR (braid-free);  ratio -> 4.0 means Theta(4^k) BRAID (= B1/x2 wall)")
