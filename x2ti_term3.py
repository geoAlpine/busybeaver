#!/usr/bin/env python3
"""x2ti_term3.py -- the §5z parse verdict, pinned exactly (2026-07-17).

x2ti_parse.py found that a 24-step anchor gap -- the test by which every `termSteps 3` term
in lean/X2.lean's exitSteps_tree_5/6/7/8 was claimed -- is realised by TWO DISTINCT
transports.  So some `termSteps 3` in those trees is a length coincidence, not the TERM(3)
block.  This probe identifies exactly which, and what the glue numbers really are.

Reminder of why word-identity is the exact test: in this machine (state,bit) ->
(write,move,next) is total (x2bd_sim.TT), so the (st,h) word over a window determines every
write, every move, the whole (state,head,dpos) trace.  Same word <=> same transport.
"""
import sys
from bisect import bisect_right

sys.path.insert(0, '/Users/aokiyousuke/busybeaver')
from x2bd_sim import build

CAP = int(sys.argv[1]) if len(sys.argv) > 1 else 620000

def exitSteps(k): return 2 ** (2 * k - 3) + k * 2 ** (k - 1) + 2 ** (k - 2) + 2
def termSteps(k): return 2 ** (k + 1) + k + 5

STS = 'ABCDEF'
SYM = {(s, b): chr(ord('a') + 2 * i + b) for i, s in enumerate(STS) for b in (0, 1)}
UNSYM = {v: k for k, v in SYM.items()}

sim = build(2); sim.step()
n0 = sim.n
W, POS, ANCH = [], [], []
while sim.n < CAP:
    W.append(SYM[(sim.st, sim.h)]); POS.append(sim.pos)
    if sim.st == 'E' and sim.h == 0:
        ANCH.append(sim.n)
    if not sim.step():
        break
S = ''.join(W)
def idx(n): return n - n0
def show(w): return ''.join(f"{UNSYM[c][0]}{UNSYM[c][1]}" for c in w)

# ---- the two length-24 anchor-gap transports -----------------------------------------
print("=== the TWO distinct transports realising a 24-step anchor gap ===\n")
g24 = [(ANCH[i], ANCH[i + 1]) for i in range(len(ANCH) - 1) if ANCH[i + 1] - ANCH[i] == 24]
cls = {}
for (a, b) in g24:
    cls.setdefault(S[idx(a):idx(b)], []).append((a, b))
for j, (w, ws) in enumerate(sorted(cls.items(), key=lambda x: -len(x[1]))):
    a, b = ws[0]
    seg = POS[idx(a):idx(b)]
    print(f"  class {j}: {len(ws):>3} occurrences   first at [{a},{b}]")
    print(f"     (st,h) word: {show(w)}")
    print(f"     head excursion (derived from the tape, min/max of real head positions):"
          f" [{min(seg)-POS[idx(a)]},{max(seg)-POS[idx(a)]}]")
    print(f"     net dpos: {POS[idx(b)] - POS[idx(a)] if idx(b) < len(POS) else '?'}")
    print()

# which class is the §5y TERM(3) -- the block-final flush ending REGEN(5)?
# REGEN(5) = carry_exit_j4 = [6923,7141] (Lean-grounded). Its TERM(5)=74 terminal ends it.
# exitSteps_tree_5 : 218 = 44 + TERM(3) + 76 + TERM(5): so the TERM(3) sits at 6923+44=6967.
t3_in_tree5 = (6967, 6991)
print(f"=== which class does exitSteps_tree_5's `termSteps 3` (at {t3_in_tree5}) belong to? ===")
w5 = S[idx(t3_in_tree5[0]):idx(t3_in_tree5[1])]
for j, (w, ws) in enumerate(sorted(cls.items(), key=lambda x: -len(x[1]))):
    if w == w5:
        print(f"  -> class {j}  ({len(ws)} occurrences)\n")
        TERM3 = set(ws)
        REF3 = w

# ---- audit each `termSteps 3` term in the Lean trees ---------------------------------
LEAN_TREE = {
    5: [('g', 44), ('T', 3), ('g', 76), ('T', 5)],
    6: [('g', 83), ('T', 3), ('g', 47), ('R', 4), ('g', 113), ('T', 3),
        ('g', 122), ('T', 3), ('g', 76), ('T', 6)],
    7: [('g', 170), ('T', 3), ('g', 47), ('R', 4), ('g', 113), ('T', 3), ('g', 78), ('R', 5),
        ('g', 113), ('T', 3), ('g', 881), ('T', 3), ('g', 47), ('R', 4), ('g', 113), ('T', 3),
        ('g', 122), ('T', 3), ('g', 76), ('T', 7)],
    8: [('g', 353), ('T', 3), ('g', 47), ('R', 4), ('g', 113), ('T', 3), ('g', 78), ('R', 5),
        ('g', 113), ('T', 3), ('g', 798), ('R', 6), ('g', 113), ('T', 3), ('g', 3944), ('T', 3),
        ('g', 47), ('R', 4), ('g', 113), ('T', 3), ('g', 78), ('R', 5), ('g', 113), ('T', 3),
        ('g', 881), ('T', 3), ('g', 47), ('R', 4), ('g', 113), ('T', 3), ('g', 122), ('T', 3),
        ('g', 76), ('T', 8)],
}
START = {}
for k in range(4, 11):
    ws = sorted({(e - exitSteps(k), e) for i in range(len(ANCH) - 1)
                 for (s, e) in [(ANCH[i], ANCH[i + 1])]
                 if ANCH[i + 1] - ANCH[i] == termSteps(k) and e - exitSteps(k) >= n0})
    if ws:
        START[k] = ws[0][0]

print("=== auditing EVERY `termSteps 3` term in the Lean trees, in orbit position ===\n")
for k in sorted(LEAN_TREE):
    if k not in START:
        continue
    pos = START[k]
    print(f"  {'exitSteps_tree_' + str(k)}   (REGEN({k}) window starts n={pos})")
    n_ok = n_bad = 0
    for x in LEAN_TREE[k]:
        ln = x[1] if x[0] == 'g' else (termSteps(x[1]) if x[0] == 'T' else exitSteps(x[1]))
        if x[0] == 'T' and x[1] == 3:
            w = S[idx(pos):idx(pos + ln)]
            good = (w == REF3)
            n_ok += good; n_bad += (not good)
            print(f"      termSteps 3 @ [{pos},{pos+ln}]  "
                  f"{'IS the TERM(3) transport' if good else '*** NOT TERM(3) -- a length coincidence ***'}")
        pos += ln
    print(f"      -> {n_ok} genuine TERM(3), {n_bad} length-coincidence\n")

# ---- what the glue really is, once only genuine TERM(3) may be named -----------------
print("=== §5z's numbers vs the TI-verified parse ===\n")
TI_REGEN = {}
for k in range(4, 11):
    if k not in START:
        continue
    a = START[k]
    w = S[idx(a):idx(a + exitSteps(k))]
    occ, i = [], S.find(w)
    while i != -1:
        occ.append((n0 + i, n0 + i + len(w))); i = S.find(w, i + 1)
    TI_REGEN[k] = occ

TERM_TI = {}
for k in range(3, 11):
    ws = [(ANCH[i], ANCH[i + 1]) for i in range(len(ANCH) - 1)
          if ANCH[i + 1] - ANCH[i] == termSteps(k)]
    if not ws:
        continue
    ref = REF3 if k == 3 else S[idx(ws[0][0]):idx(ws[0][1])]
    TERM_TI[k] = [(a, b) for (a, b) in ws if S[idx(a):idx(b)] == ref]


def parse_ti(k):
    a, b = TI_REGEN[k][0]
    boxes = {}
    for kk in range(4, k):
        for (s, e) in TI_REGEN.get(kk, []):
            if a <= s and e <= b and (e - s) < (b - a):
                boxes.setdefault(s, []).append((e, ('R', kk)))
    for kk in TERM_TI:
        for (s, e) in TERM_TI[kk]:
            if a <= s and e <= b and (e - s) < (b - a):
                boxes.setdefault(s, []).append((e, ('T', kk)))
    terms, pos, glue = [], a, 0
    while pos < b:
        c = boxes.get(pos)
        if c:
            e, tag = max(c)
            if glue: terms.append(('g', glue)); glue = 0
            terms.append(tag); pos = e
        else:
            i = bisect_right(ANCH, pos)
            nxt = ANCH[i] if i < len(ANCH) and ANCH[i] <= b else b
            glue += nxt - pos; pos = nxt
    if glue: terms.append(('g', glue))
    return terms


def render(t):
    return ' + '.join(str(x[1]) if x[0] == 'g' else
                      (f"TERM({x[1]})" if x[0] == 'T' else f"REGEN({x[1]})") for x in t)
def total(t):
    return sum(x[1] if x[0] == 'g' else
               (termSteps(x[1]) if x[0] == 'T' else exitSteps(x[1])) for x in t)

for k in sorted(LEAN_TREE):
    if k not in TI_REGEN:
        continue
    t = parse_ti(k)
    print(f"  k={k}")
    print(f"    Lean  : {render(LEAN_TREE[k])}")
    print(f"    TI    : {render(t)}")
    print(f"    sums  : Lean {total(LEAN_TREE[k])}   TI {total(t)}   exitSteps({k}) {exitSteps(k)}   "
          f"{'both OK' if total(t)==exitSteps(k)==total(LEAN_TREE[k]) else 'MISMATCH'}")
    lc = [x[1] for x in LEAN_TREE[k] if x[0] == 'R']
    tc = [x[1] for x in t if x[0] == 'R']
    print(f"    REGEN calls: Lean {lc}  TI {tc}   {'SAME' if lc==tc else '*** DIFFER ***'}\n")

print("=== the arithmetic of the fusions (why 113/122/78/881 vanish) ===")
for a, b, c, r in [(113, 24, 122, 259), (113, 24, 78, 215), (113, 24, 881, 1018),
                   (44, 24, 76, 144)]:
    print(f"    {a} + termSteps 3 ({b}) + {c} = {a+b+c}  {'== ' + str(r) if a+b+c==r else '?'}")
