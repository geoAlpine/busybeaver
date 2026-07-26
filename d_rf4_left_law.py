#!/usr/bin/env python3
"""RF-4 part 2 — the leftward turn phase decomposes into TWO more ∀-laws.

`d_rf4_left.py` dumped the uncovered turn phases.  The two big leftward ones read

    t=1194806 (1371):  (ABED)^128 A A (BC)^130 D   ++   (ABED)^131 (A)^66 (ABED)
    t=1168982 (6504):  (ABED)^617 A A (BC)^619 D   ++   (ABED)^620 (A)^r  (ABED)

and the head trajectory confirms the split: the first part advances `+3` (a rung!), the second
part is a pure descent.  Reading the itineraries against the known atoms:

  PART 1 = the rung at **`m_literal = 0`** -- the comb is exhausted, so the `crawl` run between
           `marker` and `turnaround` is empty.  That is exactly the boundary case `IN` excludes
           (`IN` needs `m >= 1`).  Predicted span `cr(u+1) + mk + ta + s01(u+3) + tu`
           = `6u+15` at D's counts; head `+3`; `u+3` swap01 atoms.
             t=1194806: u=127 -> 6*127+15 = 777, and 128*4+1+2+130*2+1+1 = 777.  Same for the other.

  PART 2 = `crawlFold q ; crawl(b=true) ; markerFold r ; crawl` -- a descent over
           `(1 0)^q 1 1^r ...`, all four primitives already in `RungCalc`.

This instrument checks both before any Lean is written.
"""
T = {'A': [(1,-1,'B'), (0,-1,'A')], 'B': [(1, 1,'C'), (0, 1,'E')],
     'C': [(0, 1,'D'), (0, 1,'B')], 'D': [(1,-1,'A'), (0, 1,'F')],
     'E': [(1, 1,'B'), (0,-1,'D')], 'F': [(1, 1,'D'), None]}

def pow10(n): return [1, 0] * n
def pow01(n): return [0, 1] * n

def mk(left, head, right, p=0):
    t = {}
    for i, b in enumerate(left):
        if b: t[p - 1 - i] = 1
    if head: t[p] = 1
    for i, b in enumerate(right):
        if b: t[p + 1 + i] = 1
    return t, p

def sim(tape, pos, st, N):
    tape = dict(tape); it = []
    for _ in range(N):
        s = tape.get(pos, 0)
        tr = T[st][s]
        if tr is None: return None, None, None, it
        it.append(st)
        w, d, nx = tr
        if w: tape[pos] = 1
        elif pos in tape: del tape[pos]
        pos += d; st = nx
    return st, pos, tape, it

def eq(a, b):
    return all(a.get(i, 0) == b.get(i, 0) for i in set(a) | set(b))

# ---------------------------------------------------------------- PART 1: rung at m = 0
print("=== §1 `rung0` — the rung with an EXHAUSTED comb (m_literal = 0) ===")
print("    IN0(u,c,g) := <A,p,< (0 1)^u 1 1 0 0 1^c TAIL | 0 | 1 0^g REST >>")
print("    span = 6u+15, head +3, output left = (0 1)^{u+3} 1 W  (nearest-first 1 0 ... )")
ok = bad = 0; fails = []
TAILS = [[], [1], [0], [1, 1], [0, 0], [1, 0, 1, 1, 0], [0, 1, 0, 1], [1]*5]
RESTS = [[], [1], [0], [1, 1], [0, 0], [1, 1, 0, 1], [0, 0, 0, 0], [1, 0]*3]
for u in range(0, 6):
  for c in range(0, 4):
    for g in range(3, 7):
      for tail in TAILS:
        for rest in RESTS:
          W = [1] * c + tail
          tin, p = mk(pow10(u) + [1, 1] + [0, 0] + W, 0, [1] + [0]*g + rest)
          span = 6*u + 15
          st, pos, out, it = sim(tin, p, 'A', span)
          # predicted output: <A, p+3, < 1 0 1 W-with-... >>  -- stated as the explicit word
          eleft  = [1] + pow01(u + 2) + [0, 1] + W          # true :: pow01(u+2) ++ false::true::W
          eright = [1] + [0]*(g - 3) + rest
          etape, q = mk(eleft, 0, eright, p + 3)
          good = (st == 'A' and pos == q and eq(out, etape))
          if good: ok += 1
          else:
              bad += 1
              if len(fails) < 4:
                  d = [i - p for i in sorted(set(out) | set(etape)) if out.get(i,0) != etape.get(i,0)]
                  fails.append((u, c, g, tail, rest, f"st={st} pos={pos-p:+d} exp{q-p:+d} diff{d[:6]}"))
print(f"  {ok} ok, {bad} fail")
for f in fails: print("   FAIL", f)

print()
print("=== §2 the two orbit spot checks for `rung0` ===")
for (t, u) in [(1194806, 127), (1168982, 616)]:
    print(f"  t={t}: u={u} -> span 6*{u}+15 = {6*u+15}")

# ---------------------------------------------------------------- PART 2: the descent
print()
print("=== §3 `descend` — crawlFold q ; crawl(b=true) ; markerFold r ; crawl ===")
print("    <A,p,< (1 0)^q 1 1 1^r 0 1 0 L | 0 | R >>  -- nearest-first")
print("    span = 4(q+1) + (r+1) + 4 ,  head = -2(q+1) - (r+1) - 2")
ok = bad = 0; fails = []
for q in range(0, 6):
  for r in range(0, 6):
    for tail in TAILS:
      for rest in RESTS:
        # nearest-first left: pow10 q, then true (so the (q+1)-th crawl lands on a 1),
        # then ones r, then false (markerFold's landing x), then true,false (the last crawl), tail
        left = pow10(q) + [1, 1] + [1]*r + [0] + [1, 0] + tail
        tin, p = mk(left, 0, rest)
        span = 4*(q+1) + (r+1) + 4
        st, pos, out, it = sim(tin, p, 'A', span)
        # predicted: head -2(q+1)-(r+1)-2 ; the crawls are tape-preserving, the markers
        # erase the 1-run into 0s and push a 0 rightwards each time
        epos = p - 2*(q+1) - (r+1) - 2
        # expected tape: cells of the 1-run become 0; everything else preserved, with the
        # crawl deposits handed to the right (which is tape-preserving), so:
        exp = dict(tin)
        for i in range(r + 1):
            k = p - 2*(q+1) - i              # the `1`-run cells the markers erase
            if k in exp: del exp[k]
        good = (st == 'A' and pos == epos and eq(out, exp))
        if good: ok += 1
        else:
            bad += 1
            if len(fails) < 4:
                d = [i - p for i in sorted(set(out) | set(exp)) if out.get(i,0) != exp.get(i,0)]
                fails.append((q, r, tail, rest, f"st={st} pos={pos-p:+d} exp{epos-p:+d} diff{d[:8]} it={''.join(it[:14])}"))
print(f"  {ok} ok, {bad} fail")
for f in fails: print("   FAIL", f)
