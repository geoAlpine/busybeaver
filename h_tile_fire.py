#!/usr/bin/env python3
"""Does D's rung tile literally FIRE on H?  (follow-up to h_vs_d_tile.py)

h_vs_d_tile.py established: H's graph is NOT a relabeling of D's (0 permutations,
both orientations), yet all four of D's tile atoms occur in H, and H's head-delta
census matches D^R's almost count-for-count at 400k steps.

So the sharp question is not "same graph" but "same tile".  Two tests:

  (A) DIRECT.  Instantiate D's IN family on H's tape with H's crawl-start state
      (H's `D`, per the ABED motif map D^R:A -> H:D) and check the span law
      6(u+m)+15, head +3, IN(u,m,c,g) -> IN(u+2,m-1,c+1,g-3).

  (B) ORBIT SEARCH.  Regardless of any guessed correspondence: scan H's real
      blank-tape orbit for configurations of the IN SHAPE (any state), and for each
      hit measure what the machine actually does over the next 6(u+m)+15 steps.
      This cannot be fooled by a wrong state guess -- it tries every state that
      actually occurs at such a configuration.

Reports facts only.  Decides no machine, upgrades no label.
"""
D_SPEC = "1RB0RA_1LC0LE_0LD0LB_1RA0LF_1LB0RD_1LD---"
H_SPEC = "1RB0RE_0RC0RA_1LD1RE_1LA0LD_1RA0LF_1LD---"
L = "ABCDEF"

def parse(spec):
    T = []
    for blk in spec.split('_'):
        row = []
        for k in (0, 3):
            f = blk[k:k+3]
            row.append(None if f[0] == '-' else (int(f[0]), 1 if f[1] == 'R' else -1, ord(f[2]) - 65))
        T.append(row)
    return T

def reverse(T):
    return [[None if e is None else (e[0], -e[1], e[2]) for e in row] for row in T]

D, H = parse(D_SPEC), parse(H_SPEC)
DR = reverse(D)

def pow10(n): return [1, 0] * n
def pow01(n): return [0, 1] * n

def build(u, m, c, g, tail, rest, p=0):
    """D's IN family: tape order  ...TAIL^R 1^c 0 0 (1 0)^m 1 1 (0 1)^u [0] 1 0^g REST..."""
    left = pow10(u) + [1, 1] + pow01(m) + [0, 0] + [1] * c + tail
    right = [1] + [0] * g + rest
    tape = {}
    for i, b in enumerate(left):
        if b: tape[p - 1 - i] = 1
    for i, b in enumerate(right):
        if b: tape[p + 1 + i] = 1
    return tape, p

def sim(T, tape, pos, st, N):
    tape = dict(tape); lo = hi = pos; it = []
    for _ in range(N):
        s = tape.get(pos, 0)
        e = T[st][s]
        if e is None: return None, None, None, (lo, hi), it
        it.append(st)
        w, d, nx = e
        if w: tape[pos] = 1
        elif pos in tape: del tape[pos]
        pos += d; st = nx
        lo = min(lo, pos); hi = max(hi, pos)
    return st, pos, tape, (lo, hi), it

def check(T, st0, u, m, c, g, tail, rest):
    tape, p = build(u, m, c, g, tail, rest)
    span = 6 * (u + m) + 15
    st, pos, out, win, it = sim(T, tape, p, st0, span)
    if st is None: return False, "HALT", None
    etape, _ = build(u + 2, m - 1, c + 1, g - 3, tail, rest, p=p + 3)
    allp = set(out) | set(etape)
    same = all(out.get(i, 0) == etape.get(i, 0) for i in allp)
    return (st == st0 and pos == p + 3 and same), f"st={L[st]} pos={pos - p:+d} tape_ok={same}", it

TAIL = [1, 0, 1, 1, 0]; REST = [1, 1, 0, 1]

print("=== (A) DIRECT: D's IN family on H, every possible start state ===")
print("    control first: the same test on D^R must pass from state A.")
for name, T in (("D^R", DR), ("H", H)):
    for st0 in range(6):
        ok = bad = 0
        first = None
        for u in range(0, 4):
            for m in range(1, 4):
                for c in range(1, 4):
                    for g in range(3, 7):
                        good, msg, _ = check(T, st0, u, m, c, g, TAIL, REST)
                        if good: ok += 1
                        else:
                            bad += 1
                            if first is None: first = (u, m, c, g, msg)
        flag = "  <== TILE FIRES" if bad == 0 else ""
        print(f"  {name} from {L[st0]}: {ok:3d} ok / {bad:3d} fail" +
              (f"   first fail u={first[0]} m={first[1]} c={first[2]} g={first[3]}: {first[4]}"
               if first else "") + flag)

print()
print("=== (B) ORBIT SEARCH: does H's real orbit ever hold an IN-shaped config? ===")

def orbit_scan(T, N, name):
    """walk the blank-tape orbit; at every step try to read the head-relative
    neighbourhood as IN(u,m,c,g) and, on a hit, run the tile span."""
    cap = 1 << 21
    tape = bytearray(2 * cap)
    pos = cap; st = 0
    hits = {}
    for t in range(N):
        # --- try to parse the neighbourhood as IN(u,m,c,g) ---
        if tape[pos] == 0 and tape[pos + 1] == 1:
            g = 0
            while g < 64 and tape[pos + 2 + g] == 0: g += 1
            if g >= 3:
                u = 0
                while (2 * u + 2 < 4096 and tape[pos - 1 - 2 * u] == 1
                       and tape[pos - 2 - 2 * u] == 0): u += 1
                i = pos - 1 - 2 * u
                if tape[i] == 1 and tape[i - 1] == 1:
                    j = i - 2; m = 0
                    while m < 4096 and tape[j] == 0 and tape[j - 1] == 1: m += 1; j -= 2
                    if m >= 1 and tape[j] == 0 and tape[j - 1] == 0:
                        k = j - 2; c = 0
                        while c < 4096 and tape[k] == 1: c += 1; k -= 1
                        if c >= 1:
                            key = (st, u, m, c, g)
                            if key not in hits:
                                # measure the span on a COPY
                                span = 6 * (u + m) + 15
                                cp = bytearray(tape); cpos = pos; cst = st
                                halted = False
                                for _ in range(span):
                                    e = T[cst][cp[cpos]]
                                    if e is None: halted = True; break
                                    cp[cpos] = e[0]; cpos += e[1]; cst = e[2]
                                if halted:
                                    hits[key] = (t, "HALT")
                                else:
                                    exp, _ = build(u + 2, m - 1, c + 1, g - 3, [], [], p=0)
                                    # compare only the tile's own window, relative to pos+3
                                    okc = True
                                    for off in range(-2 * (u + m) - 6, 5):
                                        want = exp.get(off, 0) if -2 * (u + m + 1) - 4 <= off <= 4 else None
                                        if want is None: continue
                                        if cp[pos + 3 + off] != want: okc = False; break
                                    hits[key] = (t, f"st={L[cst]} d={cpos - pos:+d} tape_ok={okc}"
                                                    + ("  TILE" if cst == st and cpos == pos + 3 and okc else ""))
        e = T[st][tape[pos]]
        if e is None: break
        tape[pos] = e[0]; pos += e[1]; st = e[2]
    print(f"  {name}: {len(hits)} distinct IN-shaped (state,u,m,c,g) signatures in {N} steps")
    for key in sorted(hits)[:14]:
        st_, u, m, c, g = key
        t, msg = hits[key]
        print(f"     t={t:7d} state {L[st_]} u={u} m={m} c={c} g={g} span={6*(u+m)+15:4d} -> {msg}")

orbit_scan(DR, 300000, "D^R (control)")
orbit_scan(H, 300000, "H")

print()
print("=== (C) FULL-STRENGTH sweep on H from state D (same grid D's proof was")
print("        verified on: 23040 points, incl. c=0 and hostile TAIL/REST) ===")
TAILS = [[], [1], [0], [1, 1], [0, 0], [1, 0, 1, 1, 0], [0, 1, 0, 1], [1] * 7, [0] * 7]
RESTS = [[], [1], [0], [1, 1], [0, 0], [1, 1, 0, 1], [0, 0, 0, 0], [1, 0] * 4]
for name, T, st0 in (("D^R (control)", DR, 0), ("H", H, 3)):
    ok = bad = 0; fails = []
    for u in range(0, 5):
        for m in range(1, 5):
            for c in range(0, 4):
                for g in range(3, 7):
                    for tail in TAILS:
                        for rest in RESTS:
                            good, msg, _ = check(T, st0, u, m, c, g, tail, rest)
                            if good: ok += 1
                            else:
                                bad += 1
                                if len(fails) < 4: fails.append((u, m, c, g, tail, rest, msg))
    print(f"  {name} from {L[st0]}: {ok} ok, {bad} fail")
    for f in fails: print("     FAIL", f)

print()
print("=== (D) negative controls on H (must fail, as they do on D) ===")
for g in (0, 1, 2, 3):
    good, msg, _ = check(H, 3, 1, 2, 2, g, [1, 0, 1], [1, 1])
    print(f"  H  g={g}: {'matches' if good else 'no match (' + msg + ')'}")
tape, p = build(1, 2, 2, 4, [1, 0, 1], [1, 1])
st, pos, out, _, _ = sim(H, tape, p, 3, 6 * (1 + 2) + 15 + 1)
etape, _ = build(3, 1, 3, 1, [1, 0, 1], [1, 1], p=p + 3)
m2 = st == 3 and pos == p + 3 and all(out.get(i, 0) == etape.get(i, 0) for i in set(out) | set(etape))
print(f"  H  span+1: {'*** MATCHED - BAD ***' if m2 else 'fails as required'}")

print()
print("=== (E) is H's ITINERARY the same word as D's? ===")
for name, T, st0 in (("D^R", DR, 0), ("H", H, 3)):
    _, _, it = check(T, st0, 2, 3, 2, 4, TAIL, REST)
    print(f"  {name} at u=2,m=3,c=2,g=4 (span 45): {''.join(L[s] for s in it)}")
