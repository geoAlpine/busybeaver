# o18 LEVEL MAP probe: standalone frontier dirty forms D(m,t,e) = 0^inf [F] 1^m 0 (10)^t 1^e 0^inf
# -> run to the next FRONTIER form or clean reset. Records the exact transition
#    (m,t,e) -> LAND L  or  (m',t',e'), the constant c = 3m'-8m (or 3L-8m), unsafe, halts.
# Hypothesis under test (from o18_depth_census.py data):
#   m=0 (mod 3): LAND, L=(8m+c_land(t,e))/3
#   m=2 (mod 3), t>0: POP    -> ((8m+14)/3, t-1, e)
#   m=2 (mod 3), t=0: LAND   (c depends on e)
#   m=1 (mod 3), e odd>1: PUSH -> ((8m-5)/3, t+1, e-2)
#   m=1 (mod 3), e=1: RECYCLE -> ((8m-17)/3, 0, 2t+8)   [via interior meet form]
#   m=1 (mod 3), e even: PUSH2 -> ((8m-5)/3, t+2, e-3)
# All transitions expected safe (unsafe=0), no halts anywhere.
import sys
SPEC = "1RB0RE_1LC0RA_1LA1LD_1LC1LF_0LC0LB_1LE---"

def parse(spec):
    M = []
    for st in spec.split('_'):
        row = []
        for t in (st[0:3], st[3:6]):
            row.append(None if t[0] == '-' else (int(t[0]), 1 if t[1] == 'R' else -1, ord(t[2]) - ord('A')))
        M.append(row)
    return M

M = parse(SPEC)

def rle(seg):
    out = []
    for b in seg:
        if out and out[-1][0] == b:
            out[-1][1] += 1
        else:
            out.append([b, 1])
    return [(b, c) for b, c in out]

def run_cfg(blocks, maxF=3, budget=None, lpadf=6):
    W = sum(c for _, c in blocks)
    lpad = lpadf * W + 4000
    rpad = W + 2000
    tape = bytearray(lpad + W + rpad)
    p0 = lpad
    i = p0 + 1
    for b, c in blocks:
        tape[i:i + c] = bytes([b]) * c
        i += c
    pos, st = p0, 5
    if budget is None: budget = 40 * W * W + 2_000_000
    steps = 0
    unsafe = 0
    # CRITICAL: hi must cover the WRITTEN config, not just visited cells —
    # otherwise F-entry span scans miss untouched tail content (spurious "clean").
    lo, hi = p0, i - 1
    L = len(tape)
    fents = []
    first = True
    while steps < budget:
        if pos < 4 or pos > L - 5:
            return ('OVERFLOW', fents, steps, unsafe)
        r = tape[pos]
        if st == 5 and not first:
            a = lo
            while a <= hi and tape[a] == 0: a += 1
            b = hi
            while b >= lo and tape[b] == 0: b -= 1
            seg = bytes(tape[a:b + 1])
            clean = (r == 0 and pos == a - 1 and seg.count(0) == 0)
            fents.append((steps, clean, (b - a + 2) if clean else None, rle(seg), pos - a))
            if clean or len(fents) >= maxF:
                return ('LAND' if clean else 'MAXF', fents, steps, unsafe)
        first = False
        if st == 3 and r == 1 and tape[pos - 1] == 1:
            unsafe += 1
        t = M[st][r]
        if t is None:
            return ('HALT', fents, steps, unsafe)
        w, d, ns = t
        tape[pos] = w
        pos += d
        st = ns
        steps += 1
        if pos < lo: lo = pos
        if pos > hi: hi = pos
    return ('BUDGET', fents, steps, unsafe)

def tail_blocks(t, e):
    b = []
    for _ in range(t):
        b += [(1, 1), (0, 1)]
    if e:
        b.append((1, e))
    return b

def parse_frontier(R, hp):
    """Parse RLE as 1^m 0 (10)^t 1^e with head at -1. Return (m,t,e) or None."""
    if hp != -1:
        return None
    # R = [(1,m),(0,1),(1,1),(0,1),...,(1,e)]
    if not R or R[0][0] != 1:
        return None
    m = R[0][1]
    rest = R[1:]
    # rest must start with (0,1)
    if not rest or rest[0] != (0, 1):
        return None
    rest = rest[1:]
    t = 0
    while len(rest) >= 2 and rest[0] == (1, 1) and rest[1] == (0, 1):
        t += 1
        rest = rest[2:]
    if len(rest) == 1 and rest[0][0] == 1:
        return (m, t, rest[0][1])
    if len(rest) == 0:
        return (m, t, 0)
    return None

def is_meet(R):
    """Interior meet form 1^2 0 (10)^T 1^k ?"""
    return len(R) >= 2 and R[0] == (1, 2)

def probe(m, t, e):
    blocks = [(1, m), (0, 1)] + tail_blocks(t, e)
    status, fents, steps, unsafe = run_cfg(blocks)
    if status == 'HALT':
        return ('HALT', steps, unsafe, None)
    if not fents:
        return (status, steps, unsafe, None)
    # walk F-entries: skip interior meets, stop at first frontier or clean
    for (s, clean, land, R, hp) in fents:
        if clean:
            return ('LAND', s, unsafe, land)
        p = parse_frontier(R, hp)
        if p is not None:
            return ('MOVE', s, unsafe, p)
        if is_meet(R) and hp > 0:
            continue  # interior meet: keep going to the frontier form
        return ('UNPARSED', s, unsafe, (R, hp))
    return (status + '?', steps, unsafe, None)

if __name__ == '__main__':
    ms = [30, 31, 32, 100, 101, 102, 301, 302, 303]
    ts = [0, 1, 2, 3, 5]
    es = [1, 3, 5, 7, 9, 6, 8, 10, 14]
    if len(sys.argv) > 3:
        ms = [int(sys.argv[1])]; ts = [int(sys.argv[2])]; es = [int(sys.argv[3])]
    from collections import defaultdict
    laws = defaultdict(set)      # (m%3, t-class, e) -> set of (kind, c, dt, de-desc)
    bad = []
    for e in es:
        for t in ts:
            for m in ms:
                kind, s, unsafe, out = probe(m, t, e)
                if kind == 'LAND':
                    L = out
                    c = 3 * L - 8 * m
                    key = (m % 3, 't>0' if t else 't=0', t, e)
                    laws[key].add(('LAND', c))
                    line = f"D({m},{t},{e}) -> LAND L={L}  c={c}"
                elif kind == 'MOVE':
                    m2, t2, e2 = out
                    c = 3 * m2 - 8 * m
                    key = (m % 3, 't>0' if t else 't=0', t, e)
                    laws[key].add(('MOVE', c, t2 - t, e2 - e))
                    line = f"D({m},{t},{e}) -> D({m2},{t2},{e2})  c={c} dt={t2-t} de={e2-e}"
                else:
                    line = f"D({m},{t},{e}) -> {kind} {out} steps={s}"
                    bad.append((m, t, e, kind, out))
                if unsafe:
                    line += f"  UNSAFE={unsafe}"
                    bad.append((m, t, e, 'UNSAFE', unsafe))
                print(line)
        sys.stdout.flush()
    print("\n=== law table: (m mod 3, t, e) -> outcomes (want ONE per key) ===")
    for key in sorted(laws):
        outs = laws[key]
        flag = '' if len(outs) == 1 else '   <-- SPLIT!'
        print(f"  m%3={key[0]} t={key[2]} e={key[3]}: {sorted(outs)}{flag}")
    print("\nbad/unparsed/unsafe:", bad if bad else "NONE")
