#!/usr/bin/env python3
"""
o17 core (k=0 mod3) — the carry cascade is a FINITE-CONTROL HEAD over a
single-0-separated base-3 digit string.  Self-contained verifier (2026-07-03).
[OBSERVED, exhaustive over the tested range; NOTHING about halting is decided.]

Positive structural normal form for the OPEN o17 core (launched by the departure
lemma of O17_LINEAR_PROVEN.md §5).  Upgrades the docs' NEGATIVE characterizations
("no scalar / no fixed-radix / unbounded digits") to a POSITIVE one:

  Every milestone (head state A at the left frontier) is a word in the regular
  language  L = (3|5) (0 1^{ell}, ell≡2 mod3)* ,  i.e. a leading marker in {3,5}
  followed by single-0-separated base-3 "digit" blocks d=(ell-2)/3 >= 0; and the
  milestone-to-milestone map is realised by a FIXED finite-control head:
    * only 10 block-boundary crossing (state,read,dir) triples ever occur,
    * only 7 right-reflection (state,read) pairs,
    * only 5 left-frontier gate (state,read) pairs,
  independent of L.  So the finite CONTROL is bounded; the unboundedness and the
  Collatz-hardness live entirely in the digit VALUES / carry cascade, not the head.

Verifier checks (0 exceptions => characterization holds on the tested range):
  (I)   language closure: every milestone in L
  (II)  finite crossing/reflection/gate alphabets (no symbol beyond the fixed sets)
  (III) width identity  W = marker + 3*(m + S) + 1   [m=#digits, S=digit sum]
        (exact; the +1 is the frontier-0 cell the head sits on; an algebraic
        consequence of the normal form, verified against raw tape width)

Run: prints "CORE TRANSDUCER CHARACTERIZATION VERIFIED: True".
"""

def parse(spec):
    M = []
    for st in spec.split('_'):
        row = []
        for t in (st[0:3], st[3:6]):
            row.append(None if (t[0] == '-' or t[2] == 'Z')
                        else (int(t[0]), 1 if t[1] == 'R' else -1, ord(t[2]) - ord('A')))
        M.append(row)
    return M

M = parse("1RB1LD_1RC0LE_1LA1RE_0LF1LA_1RB0RB_---0LB")
SN = "ABCDEF"

CROSS_OK = {('A',0,'R'),('A',1,'L'),('B',0,'R'),('B',1,'L'),('C',0,'L'),
            ('C',1,'R'),('D',0,'L'),('D',1,'L'),('E',0,'R'),('E',1,'R')}
REFL_OK  = {('A',0),('B',0),('B',1),('C',0),('C',1),('E',0),('E',1)}
GATE_OK  = {('A',0),('D',0),('D',1),('E',0),('E',1)}


def blocks(tape, lo, hi):
    r = []; i = lo
    while i <= hi:
        s = tape[i]; j = i
        while j <= hi and tape[j] == s:
            j += 1
        r.append((s, j - i)); i = j
    while r and r[0][0] == 0: r = r[1:]
    while r and r[-1][0] == 0: r = r[:-1]
    return r


def check(L, maxsteps):
    SZ = 1 << 22
    tape = bytearray(SZ); off = SZ // 2
    for i in range(1, L + 1):
        tape[off + i] = 1
    pos = off; st = 0; step = 0; lo = hi = pos
    res = dict(ms=0, lang=0, width=0, newX=set(), newR=set(), newG=set(), halted=None)
    while step < maxsteps:
        r = tape[pos]
        if st == 5 and r == 0:
            res['halted'] = step; break
        if st == 0 and pos == lo:
            b = blocks(tape, lo, hi)
            blk = [n for s, n in b if s == 1]
            gap = [n for s, n in b if s == 0]
            if blk:
                res['ms'] += 1
                # (I) language closure
                if not (blk[0] in (3, 5) and all(g == 1 for g in gap)
                        and all(x % 3 == 2 for x in blk[1:])):
                    res['lang'] += 1
                else:
                    # (III) width identity  W = marker + 3*(m + S) + 1
                    m = len(blk) - 1
                    S = sum((x - 2)//3 for x in blk[1:])
                    W = hi - lo + 1
                    if W != blk[0] + 3*(m + S) + 1:
                        res['width'] += 1
        act = M[st][r]; ww, d, ns = act
        left = tape[pos-1]; right = tape[pos+1]
        boundary = (r == 1 and ((d == 1 and right == 0) or (d == -1 and left == 0))) or \
                   (r == 0 and ((d == 1 and right == 1) or (d == -1 and left == 1)))
        if boundary:
            t = (SN[st], r, 'R' if d == 1 else 'L')
            if t not in CROSS_OK: res['newX'].add(t)
        if pos >= hi and (SN[st], r) not in REFL_OK: res['newR'].add((SN[st], r))
        if pos <= lo and (SN[st], r) not in GATE_OK: res['newG'].add((SN[st], r))
        tape[pos] = ww; pos += d; st = ns; step += 1
        if pos < lo: lo = pos
        if pos > hi: hi = pos
    return res


if __name__ == "__main__":
    Js = list(range(1, 40)) + [45, 60, 75, 100, 150, 200]
    tot_ms = tot_lang = tot_width = 0
    X = set(); R = set(); G = set()
    for j in Js:
        r = check(3 * j, 6_000_000)
        tot_ms += r['ms']; tot_lang += r['lang']; tot_width += r['width']
        X |= r['newX']; R |= r['newR']; G |= r['newG']
    print(f"milestones checked          : {tot_ms}  (core seeds L=3j, j in [1..200] sample)")
    print(f"(I)   language violations   : {tot_lang}   (config not in (3|5)(0 1^ell,ell=2mod3)*)")
    print(f"(II)  new crossing symbols  : {sorted(X) or 'NONE'}   (fixed set has 10)")
    print(f"      new reflection symbols: {sorted(R) or 'NONE'}   (fixed set has 7)")
    print(f"      new gate symbols      : {sorted(G) or 'NONE'}   (fixed set has 5)")
    print(f"(III) width-identity fails  : {tot_width}   (W = marker + 3*(m + digit_sum))")
    ok = (tot_lang == 0 and tot_width == 0 and not X and not R and not G)
    print(f"\nCORE TRANSDUCER CHARACTERIZATION VERIFIED: {ok}")
    print("SCOPE: finite CONTROL over unbounded base-3 digit counters; halting stays [OPEN].")
