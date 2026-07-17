"""x2b5_invariant.py -- test the candidate NON-HALT invariant of B5.

Candidate invariant I, checked at EVERY left-record milestone in state C:
  (I1) the tape is 1-runs separated by SINGLE 0s   (every gap == 1)
  (I2) every 1-run length is == 2 (mod 3), except at most 2 boundary runs
  (I3) the distinguished maximal run ("register") grows by exactly +3 per milestone

Plus the halt gate, checked at EVERY step:
  (H)  whenever E reads a 1 at p, cell p+1 == 1   (i.e. F never reads 0)
If (H) never fails, B5 never halts.
"""
import sys
from collections import Counter
from x2b5_sim import RULES

def run(max_steps):
    cells = {}; pos = 0; state = 'A'; lo = hi = 0
    viol_gap = viol_mod = 0; miles = 0
    badmod_hist = Counter()
    regs = []
    hfail = 0
    for step in range(max_steps):
        sym = cells.get(pos, 0)
        rule = RULES[state][sym]
        if rule is None:
            print("*** HALT at", step); return
        w, mv, nxt = rule
        if state == 'E' and sym == 1 and cells.get(pos + 1, 0) == 0:
            hfail += 1
            print(f"  !! halt-gate (H) FAILS at step {step}, pos {pos}")
        if w != sym:
            if w: cells[pos] = 1
            else: del cells[pos]
        pos += mv; state = nxt
        if pos < lo:
            lo = pos
            if state == 'C':
                miles += 1
                runs = []; gaps = []; cur = 0; g = 0
                for p in range(lo, hi + 1):
                    if cells.get(p, 0):
                        if g: gaps.append(g); g = 0
                        cur += 1
                    else:
                        if cur: runs.append(cur); cur = 0
                        g += 1
                if cur: runs.append(cur)
                if any(x != 1 for x in gaps): viol_gap += 1
                bad = [r for r in runs if r % 3 != 2]
                badmod_hist[len(bad)] += 1
                if len(bad) > 2: viol_mod += 1
                if runs: regs.append(max(runs))
    print(f"steps={max_steps} milestones={miles}")
    print(f"(H) halt-gate failures (F reads 0): {hfail}   <-- 0 means NEVER HALTS in this window")
    print(f"(I1) milestones with a gap != 1: {viol_gap}")
    print(f"(I2) milestones with >2 runs !=2 mod 3: {viol_mod}")
    print(f"     histogram of #runs that are !=2 mod 3 per milestone: {dict(sorted(badmod_hist.items()))}")
    d = [regs[i+1] - regs[i] for i in range(len(regs)-1)]
    print(f"(I3) register (max run) deltas per milestone: {dict(sorted(Counter(d).items()))}")
    print(f"     register first/last: {regs[0]} .. {regs[-1]}  over {len(regs)} milestones")

if __name__ == '__main__':
    run(int(sys.argv[1]) if len(sys.argv) > 1 else 3_000_000)
