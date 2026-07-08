#!/usr/bin/env python3
"""Numeric cross-check for Template.lean (o4 body-lemma formalization).

Mirrors every kernel-checked anchor in Template.lean with TWO independent
Python implementations of o4 = 1RB0LD_1RC1RF_1LA0RA_0LA0LE_1LD1LA_0RB---:
  (1) the zipper semantics used by the Lean `step` (left list / head / right
      list, blanks materialized on pop), and
  (2) an independent dict-tape simulator (finite support, canonical 1s),
      the semantics of o4_body_proof.py.
Checks:
  - N=100 / N=1000 configs from blank (state, pos, full zipper) — the
    `sanity100` / `sanity1000` rfl-anchors;
  - zipper vs dict agreement (state, pos, set of 1-cells) at N=100, 1000;
  - body lemma B(k) -> B(k+2) shifted -1 in exactly 4k+15 steps for
    k = 0..60 and the grid points 101, 251 (Lean proves ALL k; the lab
    note's grid was odd k in 19..251);
  - body_iter: r-fold composition anchor (r=10 from k=19);
  - the sweep-lemma shapes at k=5 (landmarks of the Lean proof).
"""

TABLE = {
    ('A', 0): (1, +1, 'B'), ('A', 1): (0, -1, 'D'),
    ('B', 0): (1, +1, 'C'), ('B', 1): (1, +1, 'F'),
    ('C', 0): (1, -1, 'A'), ('C', 1): (0, +1, 'A'),
    ('D', 0): (0, -1, 'A'), ('D', 1): (0, -1, 'E'),
    ('E', 0): (1, -1, 'D'), ('E', 1): (1, -1, 'A'),
    ('F', 0): (0, +1, 'B'), ('F', 1): None,  # halt
}

# ---------- implementation 1: zipper (the Lean semantics) ----------
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

# ---------- implementation 2: dict tape (o4_body_proof.py semantics) ----------
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

def pow01(k):
    out = []
    for _ in range(k):
        out += [False, True]
    return out

def pow10(k):
    out = []
    for _ in range(k):
        out += [True, False]
    return out

def Bcfg(k, p):
    return ('E', p, ([], True, pow01(k) + [False, False, True]))

ok = True
def check(name, cond):
    global ok
    print(f"  {name}: {'OK' if cond else 'FAIL'}")
    ok = ok and cond

print("== L1: blank-tape anchors (sanity100 / sanity1000) ==")
c0 = ('A', 0, ([], False, []))
c100 = zrun(c0, 100)
check("N=100 zipper == Lean rfl-anchor",
      c100 == ('D', 2, ([False, True, True, True, True, False, True, True], True,
                        [True, False, True, False, True, False, True, False, True, False,
                         False, True])))
c1000 = zrun(c100, 900)
check("N=1000 zipper == Lean rfl-anchor",
      c1000 == ('F', -16,
                ([True, False, True, False, True, False, True, False, True, False,
                  True, False, True, False, True, False, True, False, True, False,
                  True, True], False,
                 [True, False, True, False, True, False, False, True, False, False,
                  False, False, False, False, False, False, True, False, True, False,
                  True, False, True, False, True, False, True, False, True, False,
                  True, False, True, False, True, False, True, False, True, False,
                  False, True])))

print("== L1: zipper vs INDEPENDENT dict-tape semantics ==")
for n, c in ((100, c100), (1000, c1000)):
    t, p, s = drun({}, 0, 'A', n)
    zc = c
    check(f"N={n} state/pos/1-cells agree",
          (s, p) == (zc[0], zc[1]) and {k for k, v in t.items() if v} == zip_ones(zc))

print("== L3: body lemma B(k) -> B(k+2) shifted -1 in 4k+15 steps ==")
allk = all(zrun(Bcfg(k, 0), 4 * k + 15) == Bcfg(k + 2, -1)
           for k in list(range(0, 61)) + [101, 251])
check("k = 0..60, 101, 251 (Lean: ALL k)", allk)

print("== body_iter: r=10 applications from k=19 ==")
c = Bcfg(19, 0)
tot = sum(4 * (19 + 2 * i) + 15 for i in range(10))
check("B(19) -> B(39) shifted -10", zrun(c, tot) == Bcfg(39, -10))

print("== L2: sweep landmarks at k=5 (Lean proof decomposition) ==")
c = zrun(Bcfg(5, 0), 2)
check("after intro2", c == ('B', 0, ([True], True, pow01(5) + [False, False, True])))
c = zrun(c, 2 * 5)
check("after sweepBF", c == ('B', 10, (pow01(5) + [True], True, [False, False, True])))
c = zrun(c, 8)
check("after seam8", c == ('D', 14, (pow01(7) + [True], True, [False, True])))
c = zrun(c, 2 * 7)
check("after sweepDE", c == ('D', 0, ([True], True, pow10(7) + [False, True])))
c = zrun(c, 1)
check("after outro1 = B(7) shifted -1", c == Bcfg(7, -1))

print("== L4: prefix lemma (parametric window) and real-orbit anchors ==")
T, F = True, False
BcfgC = lambda k, p, Y: ('E', p, ([], T, pow01(k) + [F, F, T] + Y))
Mcfg = lambda G, a, p: ('E', p, ([], F, [F] * (G - 1) + pow10(a) + [F, T]))
tails = [[], [T] * 7, [T, F, F, T, T, T, F], [F, T] * 5, [T] * 40]
check("prefix471: 471 steps, lands B(19)@-11, ANY suffix Y untouched",
      all(zrun(('E', 0, ([], F, [F] * 30 + Y)), 471) == BcfgC(19, -11, Y)
          for Y in tails))
check("prefix_milestone: M(G,a) grid G in 31..501",
      all(zrun(Mcfg(G, a, 0), 471)
          == BcfgC(19, -11, [F] * (G - 31) + pow10(a) + [F, T])
          for (G, a) in [(31, 5), (37, 0), (43, 18), (100, 8), (501, 20)]))
check("body_step_ctx: eats exactly 3 gap zeros, k=0..24",
      all(zrun(BcfgC(k, 0, [F, F, F] + Y), 4 * k + 15) == BcfgC(k + 2, -1, Y)
          for k in range(25) for Y in tails[:3]))
c = zrun(('A', 0, ([], F, [])), 1548)
check("real_milestone: blank tape @1548 == M(43,18)@-42", c == Mcfg(43, 18, -42))
bt = lambda r, k: sum(4 * (k + 2 * i) + 15 for i in range(r))
check("real_generation: blank tape @2431 == suffix-entry BcfgCtx(27,-57)",
      zrun(c, 471 + bt(4, 19)) == BcfgC(27, -57, pow10(18) + [F, T]))

print("\nALL OK" if ok else "\nMISMATCH — investigate")
raise SystemExit(0 if ok else 1)
