#!/usr/bin/env python3
"""Numeric cross-check for Suffix.lean (o4 suffix lemmas + generation map).

Mirrors every theorem statement in Suffix.lean with the same two
independent Python implementations used by template_crosscheck.py:
  (1) zipper semantics (the Lean `step`), and
  (2) an independent dict-tape simulator.
Conventions: Lean filler count = Python lab count + 1
((10)^a 01 = (10)^{a_py} 1001).  Checks:
  - suffix_g3: Z(k,3,a+1) -> M(2k+12, a) @ -3 in 8k+35 steps
      (k = 0..30, 101, 251; Lean filler down to 1 = a_py 0, incl. the
       degenerate Z(41,3,0)_py landing);
  - suffix_g4: Z(k,4,a+1) -> M(2k+9, a+5) @ -3 in 8k+8a+71 steps;
  - suffix_g5: Z(k,5,b+2) -> M(2k+13, b+8) @ -4 in 12k+16b+164 steps;
  - suffix_g5_small: Z(k,5,1) -> M(2k+13, 7) @ -4 in 12k+148 steps;
  - gen_mod1/2/0(+small): the full generation map from M(G, a), exact
      step counts, all three residue classes;
  - generation_odometer arithmetic: G' = 4G/3 + c(G%3), a' = a + delta;
  - real orbit: blank tape @ 2551 == M(62, 17) @ -59 (the 43 -> 62
      generation, milestone dump anchor).
"""

TABLE = {
    ('A', 0): (1, +1, 'B'), ('A', 1): (0, -1, 'D'),
    ('B', 0): (1, +1, 'C'), ('B', 1): (1, +1, 'F'),
    ('C', 0): (1, -1, 'A'), ('C', 1): (0, +1, 'A'),
    ('D', 0): (0, -1, 'A'), ('D', 1): (0, -1, 'E'),
    ('E', 0): (1, -1, 'D'), ('E', 1): (1, -1, 'A'),
    ('F', 0): (0, +1, 'B'), ('F', 1): None,
}

def zstep(c):
    st, pos, (L, h, R) = c
    a = TABLE[(st, 1 if h else 0)]
    if a is None:
        return None
    w, d, ns = a
    h = bool(w)
    if d > 0:
        return (ns, pos + 1, ([h] + L, R[0] if R else False, R[1:]))
    return (ns, pos - 1, (L[1:], L[0] if L else False, [h] + R))

def zrun(c, n):
    for _ in range(n):
        c = zstep(c)
        assert c is not None, "unexpected halt"
    return c

def drun(tape, pos, st, n):
    tape = dict(tape)
    for _ in range(n):
        r = tape.get(pos, 0)
        a = TABLE[(st, r)]
        assert a is not None, "unexpected halt"
        w, d, st = a
        if w == 0:
            tape.pop(pos, None)
        else:
            tape[pos] = w
        pos += d
    return tape, pos, st

def zip_ones(c):
    st, pos, (L, h, R) = c
    ones = {pos - 1 - i for i, b in enumerate(L) if b}
    if h:
        ones.add(pos)
    ones |= {pos + 1 + i for i, b in enumerate(R) if b}
    return ones

T, F = True, False
def pow01(k): return [F, T] * k
def pow10(k): return [T, F] * k

# Lean-convention builders (Suffix.lean / Template.lean)
Zcfg = lambda k, g, a, p: ('E', p, ([], T, pow01(k) + [F, F, T] + [F] * g + pow10(a) + [F, T]))
Mcfg = lambda G, a, p: ('E', p, ([], F, [F] * (G - 1) + pow10(a) + [F, T]))
bt = lambda r, k: sum(4 * (k + 2 * i) + 15 for i in range(r))

ok = True
def check(name, cond):
    global ok
    print(f"  {name}: {'OK' if cond else 'FAIL'}")
    ok = ok and cond

print("== suffix_g3: Z(k,3,a+1) -> M(2k+12,a) @-3 in 8k+35 (all k, filler>=1) ==")
ks = list(range(0, 31)) + [101, 251]
check("k grid x a in {0,1,2,7,29}",
      all(zrun(Zcfg(k, 3, a + 1, 0), 8 * k + 35) == Mcfg(2 * k + 12, a, -3)
          for k in ks for a in (0, 1, 2, 7, 29)))
check("Z(41,3,0)_py degenerate landing M(94,0)",
      zrun(Zcfg(41, 3, 1, 0), 8 * 41 + 35) == Mcfg(94, 0, -3))

print("== suffix_g4: Z(k,4,a+1) -> M(2k+9,a+5) @-3 in 8k+8a+71 ==")
check("k grid x a in {0,1,2,7,29}",
      all(zrun(Zcfg(k, 4, a + 1, 0), 8 * k + 8 * a + 71) == Mcfg(2 * k + 9, a + 5, -3)
          for k in ks for a in (0, 1, 2, 7, 29)))

print("== suffix_g5: Z(k,5,b+2) -> M(2k+13,b+8) @-4 in 12k+16b+164 ==")
check("k grid x b in {0,1,2,7,29}",
      all(zrun(Zcfg(k, 5, b + 2, 0), 12 * k + 16 * b + 164) == Mcfg(2 * k + 13, b + 8, -4)
          for k in ks for b in (0, 1, 2, 7, 29)))

print("== suffix_g5_small: Z(k,5,1) -> M(2k+13,7) @-4 in 12k+148 ==")
check("k grid", all(zrun(Zcfg(k, 5, 1, 0), 12 * k + 148) == Mcfg(2 * k + 13, 7, -4)
                    for k in ks))

print("== zipper vs INDEPENDENT dict-tape semantics on suffix runs ==")
for (k, g, a, n) in [(19, 3, 5, 8 * 19 + 35), (19, 4, 9, 8 * 19 + 8 * 8 + 71),
                     (23, 5, 9, 12 * 23 + 16 * 7 + 164), (21, 5, 1, 12 * 21 + 148)]:
    cells = [T] + pow01(k) + [F, F, T] + [F] * g + pow10(a) + [F, T]
    tape = {i: 1 for i, b in enumerate(cells) if b}
    t, p, s = drun(tape, 0, 'E', n)
    zc = zrun(Zcfg(k, g, a, 0), n)
    check(f"Z({k},{g},{a}) after {n} steps: state/pos/1-cells agree",
          (s, p) == (zc[0], zc[1]) and {kk for kk, v in t.items() if v} == zip_ones(zc))

print("== generation map: M(G,a) -> M(G',a') exact step counts ==")
CFX = {0: 3, 1: 5, 2: 1}
def delta(G): return {1: -1, 2: 4, 0: 6}[G % 3]
def gen_check(G, a):
    """Lean gen_mod* mirrored: G >= 34, Lean filler a >= 1."""
    s = (G - 34 - ((G - 34) % 3)) // 3  # number of bodies; leftover gap g = 3 + (G-34)%3
    g = G - 31 - 3 * s
    k = 19 + 2 * s
    if g == 3:
        n, out, sh = 8 * k + 35, (2 * k + 12, a - 1), -14 - s
    elif g == 4:
        n, out, sh = 8 * k + 8 * (a - 1) + 71, (2 * k + 9, a + 4), -14 - s
    elif a >= 2:
        n, out, sh = 12 * k + 16 * (a - 2) + 164, (2 * k + 13, a + 6), -15 - s
    else:
        n, out, sh = 12 * k + 148, (2 * k + 13, 7), -15 - s
    N = 471 + bt(s, 19) + n
    got = zrun(Mcfg(G, a, 0), N)
    odo_ok = out[0] == 4 * G // 3 + CFX[G % 3] and out[1] == a + delta(G)
    return got == Mcfg(out[0], out[1], sh) and odo_ok
check("G = 34..60 x a in {1,2,3,9,20}",
      all(gen_check(G, a) for G in range(34, 61) for a in (1, 2, 3, 9, 20)))
check("G in {100, 275, 367} x a in {9, 35}",
      all(gen_check(G, a) for G in (100, 275, 367) for a in (9, 35)))

print("== real orbit: blank @2551 == M(62,17) @-59 (43 -> 62 generation) ==")
c = zrun(('A', 0, ([], F, [])), 2551)
check("real_next_milestone", c == Mcfg(62, 17, -59))
check("step count 1548 + 471 + bodyTime(3,19) + 235 == 2551",
      1548 + 471 + bt(3, 19) + 8 * 25 + 35 == 2551)

print("\nALL OK" if ok else "\nMISMATCH — investigate")
raise SystemExit(0 if ok else 1)
