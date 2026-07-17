#!/usr/bin/env python3
"""x2ti_canon.py -- is the canonical REGEN(k)/TERM(k) reference class the RIGHT one?
(2026-07-17)

x2ti_tree.py takes the EARLIEST length-candidate window as the canonical REGEN(k), then
defines the TI class as every occurrence of that exact transport word.  For k=7 that choice
matters: 8 windows have REGEN(7)'s length, and they split 4/4 into two transport classes.
Picking the wrong class would invert every conclusion.  So the choice must not rest on
"earliest" -- it must rest on the DEFINITION.

§5z/§5y define REGEN(k) as the regeneration that LAYS THE FRESH TOP CASCADE BLOCK
`1^{2^k-3}` and re-anchors E.  That is a statement about the TAPE, and it is decidable
directly: read the block off the tape at the window end.

WHERE THE BLOCK IS.  Read off the Lean-grounded REGEN(5)=carry_exit_j4 OUT config at
n=7141 (and visible in regen5_transport's statement): state E, head on 0, and the right
tape reads  0^4 1^29 0^2 1^13 0^2 1^5 0^2 1^1 --  the fresh block 1^29 = 1^(2^5-3) is the
FIRST 1-run to the RIGHT of the head, sitting on top of the descending cascade
29,13,5 = 2^5-3, 2^4-3, 2^3-3.  So the definitional test is: at the window end, the first
1-run on the right has length 2^k-3.

DISCIPLINE: that run length is measured FROM THE TAPE -- the actual 1 cells in the
simulator's own right tape -- never from a caller-maintained lo/hi counter.
"""
import sys

sys.path.insert(0, '/Users/aokiyousuke/busybeaver')
from x2bd_sim import build

CAP = int(sys.argv[1]) if len(sys.argv) > 1 else 620000

def exitSteps(k): return 2 ** (2 * k - 3) + k * 2 ** (k - 1) + 2 ** (k - 2) + 2
def termSteps(k): return 2 ** (k + 1) + k + 5

STS = 'ABCDEF'
SYM = {(s, b): chr(ord('a') + 2 * i + b) for i, s in enumerate(STS) for b in (0, 1)}


def block_from_tape(sim):
    """The fresh top block: length of the FIRST 1-run to the right of the head, read off
    the real tape cells (head bit + right list).  Nothing is taken from a lo/hi counter."""
    seq = [sim.h] + sim.R[::-1]
    i = 0
    while i < len(seq) and seq[i] == 0:
        i += 1
    j = i
    while j < len(seq) and seq[j] == 1:
        j += 1
    return j - i


sim = build(2); sim.step()
n0 = sim.n
W, ANCH, LSOLID = [], [], {}
while sim.n < CAP:
    W.append(SYM[(sim.st, sim.h)])
    if sim.st == 'E' and sim.h == 0:
        ANCH.append(sim.n)
        LSOLID[sim.n] = block_from_tape(sim)          # from the tape
    if not sim.step():
        break
S = ''.join(W)
def idx(n): return n - n0

print(f"orbit: {len(S)} steps, {len(ANCH)} anchors\n")
print("=== every length-candidate REGEN(k) window, with the block it ACTUALLY lays ===")
print("    (block read off the tape at the window end; REGEN(k) must lay 1^(2^k-3))\n")

for k in range(4, 11):
    ws = sorted({(e - exitSteps(k), e) for i in range(len(ANCH) - 1)
                 for (s, e) in [(ANCH[i], ANCH[i + 1])]
                 if ANCH[i + 1] - ANCH[i] == termSteps(k) and e - exitSteps(k) >= n0})
    if not ws:
        continue
    want = 2 ** k - 3
    cls = {}
    for (a, b) in ws:
        cls.setdefault(S[idx(a):idx(b)], []).append((a, b))
    ref = S[idx(ws[0][0]):idx(ws[0][1])]
    print(f"  REGEN({k}): must lay 1^{want};  {len(ws)} length-candidates in "
          f"{len(cls)} transport class(es)")
    for j, (w, occ) in enumerate(sorted(cls.items(), key=lambda x: x[1][0][0])):
        blocks = sorted({LSOLID.get(b) for (a, b) in occ if b in LSOLID})
        ok = blocks == [want]
        tag = "<= LAYS 1^%d  == THE REGEN(%d) TRANSPORT" % (want, k) if ok else \
              "   lays 1^%s  -- NOT REGEN(%d)" % (','.join(map(str, blocks)), k)
        iscanon = " [chosen as canonical: earliest]" if w == ref else ""
        print(f"      class {j}: {len(occ):>2} occ, first [{occ[0][0]},{occ[0][1]}]  {tag}{iscanon}")
    print()

print("=== same question for the TERM(k) blocks ===")
print("    (TERM(k) is the block-final flush laying 1^(2^k-3); read off the tape)\n")
for k in range(3, 11):
    ws = [(ANCH[i], ANCH[i + 1]) for i in range(len(ANCH) - 1)
          if ANCH[i + 1] - ANCH[i] == termSteps(k)]
    if not ws:
        continue
    want = 2 ** k - 3
    cls = {}
    for (a, b) in ws:
        cls.setdefault(S[idx(a):idx(b)], []).append((a, b))
    ref = S[idx(ws[0][0]):idx(ws[0][1])]
    print(f"  TERM({k})={termSteps(k)}: must lay 1^{want};  {len(ws)} length-candidates in "
          f"{len(cls)} class(es)")
    for j, (w, occ) in enumerate(sorted(cls.items(), key=lambda x: x[1][0][0])):
        blocks = sorted({LSOLID.get(b) for (a, b) in occ if b in LSOLID})
        ok = blocks == [want]
        tag = f"<= LAYS 1^{want}  == THE TERM({k}) TRANSPORT" if ok else \
              f"   lays 1^{','.join(map(str, blocks))}  -- NOT TERM({k})"
        iscanon = " [earliest]" if w == ref else ""
        print(f"      class {j}: {len(occ):>3} occ, first [{occ[0][0]},{occ[0][1]}]  {tag}{iscanon}")
    print()

print("VERDICT: the canonical class is selected by the DEFINITION (the block it lays,")
print("read from the tape), not by 'earliest'.  Where the two agree, 'earliest' was")
print("a harmless shortcut; the tape is the authority.")
