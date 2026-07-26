#!/usr/bin/env python3
"""RF-4 — the rightward turn phase has a CLOSED FORM: it is the rung tile with a longer
return sweep.

`d_rf4_turns.py` segmented epoch `M1(4)→M1(5)` by rung-tile firings and dumped the itinerary of
every turn phase.  The rightward ones read

    (ABED)^{u+1} · A · (ABED)^{m} · A · (BC) · (BE)^{m} · (BC)^{u+2} · (BE)^{w} · C · D

which is EXACTLY the rung's itinerary with one extra `swap10` run of length `w`.  The cause is
visible on the tape: the rung needs the right context `1 0^g` with `g ≥ 3`, and a turn happens
precisely when the gap is exhausted (`g = 0`) and the return sweep meets a `(1 0)`-comb instead
of the landing pad.  It crosses the comb with `w` more `swap10` atoms and turns on the pad beyond.

So the conjecture, in `IN`'s literal-`m` convention:

    IN2(u,m,c,w,g) := <A, p, < (0 1)^u 1 1 (1 0)^m 0 0 1^c TAIL | 0 | 1 (1 0)^w 0^g REST >>
    steps (6(u+m)+15 + 2w) IN2  =  <A, p+3+2w,
        < 1 (1 0)^w (0 1)^{u+2} (1 0)^m (0 1) 1^c TAIL | 0 | 1 0^{g-3} REST >>

(left words written NEAREST-FIRST, as in the Lean `Tape.left`.)

and the OUTPUT is itself an `IN` configuration with `(u', m', c', g') = (0, w-1, 1, g-3)`.
Two spot checks from the real orbit already agree exactly:

    t=291698: u=9,  m=2,  w=66  -> 6(11)+15+132  = 213   (measured 213),  next ladder IN(0,65,1,·)
    t=310271: u=72, m=29, w=309 -> 6(101)+15+618 = 1239  (measured 1239), next ladder IN(0,308,1,·)

This instrument sweeps the law and checks the negative controls, before any Lean is written.
"""
from collections import Counter

T = {'A': [(1,-1,'B'), (0,-1,'A')], 'B': [(1, 1,'C'), (0, 1,'E')],
     'C': [(0, 1,'D'), (0, 1,'B')], 'D': [(1,-1,'A'), (0, 1,'F')],
     'E': [(1, 1,'B'), (0,-1,'D')], 'F': [(1, 1,'D'), None]}

def pow10(n): return [1, 0] * n
def pow01(n): return [0, 1] * n

def build(u, m, c, w, g, tail, rest, p=0):
    left  = pow10(u) + [1, 1] + pow01(m) + [0, 0] + [1] * c + tail
    right = [1] + pow10(w) + [0] * g + rest
    t = {}
    for i, b in enumerate(left):
        if b: t[p - 1 - i] = 1
    for i, b in enumerate(right):
        if b: t[p + 1 + i] = 1
    return t, p

def expected(u, m, c, w, g, tail, rest, p):
    """the conjectured output tape, at pos p+3+2w"""
    q = p + 3 + 2 * w
    left  = [1] + pow10(w) + pow01(u + 2) + pow10(m) + pow01(1) + [1] * c + tail
    right = [1] + [0] * (g - 3) + rest
    t = {}
    for i, b in enumerate(left):
        if b: t[q - 1 - i] = 1
    for i, b in enumerate(right):
        if b: t[q + 1 + i] = 1
    return t, q

def sim(tape, pos, N):
    tape = dict(tape); st = 'A'; it = []
    for _ in range(N):
        s = tape.get(pos, 0)
        tr = T[st][s]
        if tr is None: return None, None, None, it
        it.append(st)
        wr, d, nx = tr
        if wr: tape[pos] = 1
        elif pos in tape: del tape[pos]
        pos += d; st = nx
    return st, pos, tape, it

def check(u, m, c, w, g, tail, rest):
    tin, p = build(u, m, c, w, g, tail, rest)
    span = 6 * (u + m) + 15 + 2 * w
    st, pos, out, it = sim(tin, p, span)
    if st is None: return False, "HALT", None
    etape, q = expected(u, m, c, w, g, tail, rest, p)
    allp = set(out) | set(etape)
    same = all(out.get(i, 0) == etape.get(i, 0) for i in allp)
    ok = (st == 'A' and pos == q and same)
    if not ok:
        diff = [i - p for i in sorted(allp) if out.get(i, 0) != etape.get(i, 0)]
        return False, f"st={st} pos={pos-p:+d} (exp {q-p:+d}) diff@{diff[:8]}", it
    return True, "", it

print("=== §1 the two orbit spot checks, re-derived from the law alone ===")
for (u, m, w) in [(9, 2, 66), (72, 29, 309)]:
    print(f"  u={u} m={m} w={w}: span = 6({u}+{m})+15+2*{w} = {6*(u+m)+15+2*w}")

print()
print("=== §2 exhaustive sweep of the conjectured law ===")
TAILS = [[], [1], [0], [1, 1], [0, 0], [1, 0, 1, 1, 0], [0, 1, 0, 1], [1]*5, [0]*5]
RESTS = [[], [1], [0], [1, 1], [0, 0], [1, 1, 0, 1], [0, 0, 0, 0], [1, 0]*3]
ok = bad = 0; fails = []
for u in range(0, 5):
  for m in range(1, 5):
    for c in range(0, 4):
      for w in range(1, 6):
        for g in range(3, 7):
          for tail in TAILS:
            for rest in RESTS:
              good, msg, _ = check(u, m, c, w, g, tail, rest)
              if good: ok += 1
              else:
                  bad += 1
                  if len(fails) < 5: fails.append((u, m, c, w, g, tail, rest, msg))
print(f"  {ok} ok, {bad} fail")
for f in fails: print("   FAIL", f)

print()
print("=== §3 the law SPECIALISES to the rung tile at w = 0 ===")
print("    (w=0 makes the right context `1 0^g` again; the output should be IN(u+2,m-1,c+1,g-3))")
o = b = 0
for u in range(0, 4):
  for m in range(1, 4):
    for c in range(1, 4):
      for g in range(3, 7):
        good, msg, _ = check(u, m, c, 0, g, [1, 0, 1], [1, 1])
        if good: o += 1
        else: b += 1
print(f"  w=0: {o} ok, {b} fail   (so the rung tile is the w=0 case -- one law, not two)")

print()
print("=== §4 the OUTPUT is itself an IN configuration, with (u',m',c') = (0, w-1, 1) ===")
def read_IN(tape, pos):
    if tape.get(pos, 0) != 0 or tape.get(pos + 1, 0) != 1: return None
    g = 0
    while tape.get(pos + 2 + g, 0) == 0 and g < 5000: g += 1
    if g < 3: return None
    u = 0
    while tape.get(pos-1-2*u, 0) == 1 and tape.get(pos-2-2*u, 0) == 0: u += 1
    i = pos - 1 - 2*u
    if not (tape.get(i, 0) == 1 and tape.get(i-1, 0) == 1): return None
    j = i - 2; m = 0
    while tape.get(j, 0) == 0 and tape.get(j-1, 0) == 1: m += 1; j -= 2
    if m < 1 or not (tape.get(j, 0) == 0 and tape.get(j-1, 0) == 0): return None
    k = j - 2; c = 0
    while tape.get(k, 0) == 1: c += 1; k -= 1
    return (u, m, c, g)
agree = disagree = 0
for u in range(0, 4):
  for m in range(1, 4):
    for c in range(1, 4):
      for w in range(2, 7):
        for g in range(6, 9):
          tin, p = build(u, m, c, w, g, [1, 0, 1, 1, 0], [1, 1, 0, 1])
          st, pos, out, _ = sim(tin, p, 6*(u+m)+15+2*w)
          got = read_IN(out, pos)
          want = (0, w - 1, 1, g - 3)
          if got == want: agree += 1
          else:
              disagree += 1
              if disagree <= 4: print(f"   u={u} m={m} c={c} w={w} g={g}: got {got}, want {want}")
print(f"  output-is-IN(0,w-1,1,g-3): {agree} agree, {disagree} disagree")

print()
print("=== §5 negative controls (must fail) ===")
for name, args, span_off in [
    ("g = 2 (pad too short)", (2, 2, 2, 4, 2), 0),
    ("span + 1",              (2, 2, 2, 4, 4), +1),
    ("span - 1",              (2, 2, 2, 4, 4), -1),
]:
    u, m, c, w, g = args
    tin, p = build(u, m, c, w, g, [1, 0, 1], [1, 1])
    span = 6*(u+m) + 15 + 2*w + span_off
    st, pos, out, _ = sim(tin, p, span)
    etape, q = expected(u, m, c, w, g, [1, 0, 1], [1, 1], p)
    m2 = (st == 'A' and pos == q and
          all(out.get(i, 0) == etape.get(i, 0) for i in set(out) | set(etape))) if st else False
    print(f"  {name:24s}: {'*** MATCHED - BAD ***' if m2 else 'fails as required'}")

print()
print("=== §6 which of the epoch's turn phases does this law cover? ===")
print("    The law is the RIGHTWARD turn (up the cascade).  The leftward ones (coming back down)")
print("    show long runs of bare `A` in their itinerary -- the marker atom repeated over a 1-run --")
print("    and are a DIFFERENT primitive.  Counting them honestly:")
print("      k=4 epoch, 7 turn phases:")
print("        t=291168   26 steps  entry-ish, mixed (contains (CD) and (EB) runs)   NOT covered")
print("        t=291254  180 steps  contains (DF)^8 -- state F reached                NOT covered")
print("        t=291698  213 steps  (ABED)^10 A (ABED)^2 A BC (BE)^2 (BC)^11 (BE)^66 CD   COVERED")
print("        t=310271 1239 steps  same shape, w=309                                  COVERED")
print("        t=1168982 6504 steps long (A)-run  => leftward                          NOT covered")
print("        t=1194806 1371 steps long (A)-run  => leftward                          NOT covered")
print("        t=1196246  166 steps mixed, two sub-turns                               NOT covered")
