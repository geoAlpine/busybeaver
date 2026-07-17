#!/usr/bin/env python3
"""x2ti_parse.py -- is §5z's `83/47/113/122/76` + the "level-7-only" `881` a real
structure, or an artifact of a greedy TERM-boundary parse?  (2026-07-17)

x2ti_tree.py settled the REGEN sub-calls: transport-verified, the Lean groundings hold.
This probe audits the OTHER half of the same expressions -- the TERM blocks and the glue
numbers between them -- for the SAME defect, one level down:

  exitSteps_tree_6 : exitSteps 6 = 83 + termSteps 3 + 47 + exitSteps 4 + 113 + termSteps 3
                                   + 122 + termSteps 3 + 76 + termSteps 6

Every `termSteps 3` here was claimed by the grounding probe purely because an anchor gap
happened to equal termSteps(3)=24.  Same coincidence-prone test as the REGEN one.  Two
questions, both answered by construction:

  (Q1) Are those TERM(k) windows the genuine TERM(k) transport?  (word-identity test:
       see x2ti_tree.py -- (st,h) word identity == (state,head,dpos) trace identity, exact.)
  (Q2) Are 83/47/113/122/76/881 INTRINSIC segments, or merely the residues left over
       between greedily-claimed TERM(3) boundaries -- i.e. artifacts of the parse
       CONVENTION rather than facts about the orbit?
"""
import sys
from bisect import bisect_right

sys.path.insert(0, '/Users/aokiyousuke/busybeaver')
from x2bd_sim import build, TT

CAP = int(sys.argv[1]) if len(sys.argv) > 1 else 620000
KTOP = int(sys.argv[2]) if len(sys.argv) > 2 else 10

def exitSteps(k): return 2 ** (2 * k - 3) + k * 2 ** (k - 1) + 2 ** (k - 2) + 2
def termSteps(k): return 2 ** (k + 1) + k + 5

STS = 'ABCDEF'
SYM = {(s, b): chr(ord('a') + 2 * i + b) for i, s in enumerate(STS) for b in (0, 1)}

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
print(f"orbit word: {len(S)} steps from n={n0}, {len(ANCH)} anchors\n")


def occurrences(word):
    out, i = [], S.find(word)
    while i != -1:
        out.append((n0 + i, n0 + i + len(word))); i = S.find(word, i + 1)
    return out


def term_windows_bylen(k):
    g = termSteps(k)
    return [(ANCH[i], ANCH[i + 1]) for i in range(len(ANCH) - 1) if ANCH[i + 1] - ANCH[i] == g]


def regen_bylen(k):
    return sorted({(e - exitSteps(k), e) for (s, e) in term_windows_bylen(k)
                   if e - exitSteps(k) >= n0})


# ---- Q1: are the TERM(k) blocks genuine transports? ----------------------------------
print("=== (Q1) TERM(k) blocks: length-claimed vs transport-verified ===")
print(f"{'k':<4}{'TERM(k)':>9}{'by LENGTH':>11}{'transport classes (word -> count)':>38}")
TERM_TI = {}
for k in range(3, KTOP + 1):
    ws = term_windows_bylen(k)
    if not ws:
        continue
    cls = {}
    for (a, b) in ws:
        cls.setdefault(S[idx(a):idx(b)], []).append((a, b))
    ref = S[idx(ws[0][0]):idx(ws[0][1])]
    TERM_TI[k] = cls[ref]
    sizes = sorted((len(v) for v in cls.values()), reverse=True)
    note = "single transport" if len(cls) == 1 else f"*** {len(cls)} DISTINCT transports, sizes {sizes}"
    print(f"{k:<4}{termSteps(k):>9}{len(ws):>11}   {note}")

print("\n  => a `termSteps 3` term in the Lean trees is claimed on an anchor gap of 24.")
for k in sorted(TERM_TI):
    ws = term_windows_bylen(k)
    print(f"     TERM({k}): {len(TERM_TI[k])}/{len(ws)} of the length-matched windows are"
          f" the TERM({k}) transport")

# ---- Q2: is the glue split intrinsic, or a parse convention? -------------------------
print("\n=== (Q2) the glue numbers 83/47/113/122/76 and 881 ===")

TI_REGEN = {}
for k in range(4, KTOP + 1):
    c = regen_bylen(k)
    if not c:
        continue
    a, b = c[0]
    TI_REGEN[k] = occurrences(S[idx(a):idx(b)])


def parse(k, name_terms):
    """Cover REGEN(k) greedily.  name_terms = set of k' whose TERM(k') blocks we
    ALLOW the parser to name.  Everything unnamed falls into glue."""
    a, b = TI_REGEN[k][0]
    boxes = {}
    for kk in range(4, k):
        for (s, e) in TI_REGEN.get(kk, []):
            if a <= s and e <= b and (e - s) < (b - a):
                boxes.setdefault(s, []).append((e, ('R', kk)))
    for kk in name_terms:
        for (s, e) in TERM_TI.get(kk, []):
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


ALLK = list(range(3, KTOP + 1))
print("\n  CONVENTION A = §5z / the Lean trees: name EVERY TERM(k), k=3..  (greedy)")
for k in (5, 6, 7):
    t = parse(k, ALLK)
    print(f"    REGEN({k}) = {render(t)}   [sum {total(t)} = exitSteps({k}) {exitSteps(k)}]")

print("\n  CONVENTION B = identical orbit, but DON'T name the TERM(3) blocks")
print("  (nothing about the machine changed -- only which blocks the parser names):")
NO3 = [k for k in ALLK if k != 3]
for k in (5, 6, 7):
    t = parse(k, NO3)
    print(f"    REGEN({k}) = {render(t)}   [sum {total(t)} = exitSteps({k}) {exitSteps(k)}]")

print("\n  CONVENTION C = name NO TERM at all (pure glue + REGEN calls):")
for k in (5, 6, 7):
    t = parse(k, [])
    print(f"    REGEN({k}) = {render(t)}   [sum {total(t)} = exitSteps({k}) {exitSteps(k)}]")

print("\n  => the numbers 83/47/113/122/76/881 EXIST only in convention A.  Under B they")
print("     fuse (83+24+47=154, 113+24+881+24+47=1089, ...); the ORBIT is unchanged.")

# ---- is 881 level-7-only? -------------------------------------------------------------
print("\n=== is `881` a level-7 object, as §5z's presentation suggests? ===")
for k in range(5, KTOP + 1):
    if k not in TI_REGEN:
        continue
    t = parse(k, ALLK)
    gl = [x[1] for x in t if x[0] == 'g']
    print(f"    REGEN({k}) convention-A glue multiset: {gl}")
    print(f"        contains 881: {881 in gl}")

print("\n=== does the SAME orbit segment carry 881 at every level it appears? ===")
for k in range(7, KTOP + 1):
    if k not in TI_REGEN:
        continue
    a, b = TI_REGEN[k][0]
    t = parse(k, ALLK)
    pos, hits = a, []
    for x in t:
        ln = x[1] if x[0] == 'g' else (termSteps(x[1]) if x[0] == 'T' else exitSteps(x[1]))
        if x[0] == 'g' and x[1] == 881:
            hits.append((pos, pos + ln))
        pos += ln
    for (s, e) in hits:
        print(f"    REGEN({k}) [{a},{b}]: an 881-glue at [{s},{e}]")
