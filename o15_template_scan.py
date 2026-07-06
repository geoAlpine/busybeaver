# o15 generation event-stream template test + landing-law grid (o4/o3/o18 method).
# Milestone M(b0,...,bk) = tape 1^b0 0 1^b1 0 ... 0 1^bk, head on the 0-cell right of the
# last block, state A (this is exactly the config after a right-frontier F-reads-1 gate).
# One generation = run to the next RIGHT-FRONTIER gate (F reads 1 at the right end of the
# nonzero extent). Records: landing block vector, steps, unsafe, mid-gen gate events,
# level-1 (minimal-period p<=24) + level-2 shape hash of the (state,read) token stream.
# GUARDED tape (o18_tower lesson): raises on tape-edge approach.
import sys, hashlib
SPEC = "1RB---_0RC0RE_1RD1RF_1LE0LB_1RC0LD_1RC1RA"

def parse(spec):
    M = []
    for st in spec.split('_'):
        row = []
        for t in (st[0:3], st[3:6]):
            row.append(None if t[0] == '-' else (int(t[0]), 1 if t[1] == 'R' else -1, ord(t[2]) - ord('A')))
        M.append(row)
    return M

M = parse(SPEC)

def build(blocks):
    return blocks

def run_gen(blocks, budget=None, record=True):
    V = sum(blocks) + len(blocks) - 1
    if budget is None:
        budget = 3 * V * V + 500_000
    padL = 64 + V // 2
    padR = 3 * V + 128
    tape = bytearray(padL + V + 1 + padR)
    p = padL
    for b in blocks:
        for i in range(b):
            tape[p] = 1
            p += 1
        p += 1  # separator 0
    head0 = padL + V  # the 0-cell right of the last block
    pos, st = head0, 0  # state A
    lo, hi = padL, padL + V - 1
    toks = bytearray() if record else None
    unsafe = 0
    midgates = []
    steps = 0
    n = len(tape)
    while steps < budget:
        r = tape[pos]
        if st == 5 and r == 1:
            if tape[pos + 1] == 1:
                unsafe += 1
            if pos == hi:  # right-frontier gate = landing
                # parse landing blocks
                i, j = lo, hi
                while i <= j and tape[i] == 0: i += 1
                out, cur = [], 0
                bad0 = 0
                k = i
                run0 = 0
                while k <= j:
                    if tape[k] == 1:
                        if run0 > 1: bad0 += 1
                        run0 = 0
                        cur += 1
                    else:
                        if cur: out.append(cur)
                        cur = 0
                        run0 += 1
                    k += 1
                if cur: out.append(cur)
                return ('LAND', out, steps, unsafe, midgates, toks, bad0)
            else:
                midgates.append((steps, pos - head0))
        t = M[st][r]
        if t is None:
            return ('HALT', None, steps, unsafe, midgates, toks, 0)
        if record:
            toks.append(st * 2 + r)
        w, d, ns = t
        tape[pos] = w
        pos += d
        st = ns
        steps += 1
        if pos < 8 or pos > n - 8:
            raise RuntimeError("tape edge approached — enlarge pad")
        if pos < lo: lo = pos
        if pos > hi: hi = pos
    return ('BUDGET', None, steps, unsafe, midgates, toks, 0)

def compress(s, pmax=24):
    out = []
    i, n = 0, len(s)
    while i < n:
        hit = None
        for p in range(1, pmax + 1):
            if i + 2 * p <= n and s[i:i + p] == s[i + p:i + 2 * p]:
                k = 2
                while i + (k + 1) * p <= n and s[i + k * p:i + (k + 1) * p] == s[i:i + p]:
                    k += 1
                hit = (p, k)
                break
        if hit:
            p, k = hit
            out.append(('R', bytes(s[i:i + p]), k))
            i += p * k
        else:
            out.append(('T', s[i]))
            i += 1
    return out

def l2(chunks, pmax=48):
    shape = [(('R', c[1]) if c[0] == 'R' else ('T', c[1])) for c in chunks]
    out = []
    i, n = 0, len(shape)
    while i < n:
        hit = None
        for p in range(1, pmax + 1):
            if i + 2 * p <= n and shape[i:i + p] == shape[i + p:i + 2 * p]:
                k = 2
                while i + (k + 1) * p <= n and shape[i + k * p:i + (k + 1) * p] == shape[i:i + p]:
                    k += 1
                hit = (p, k)
                break
        if hit:
            p, k = hit
            out.append(('B', tuple(shape[i:i + p]), k))
            i += p * k
        else:
            out.append(shape[i])
            i += 1
    return out

def shape_sig(l2out):
    sig = [(('B', c[1]) if c[0] == 'B' else c) for c in l2out]
    return hashlib.md5(repr(sig).encode()).hexdigest()[:10], sig

if __name__ == '__main__':
    # grid: single blocks + two-block forms
    grid = [[v] for v in range(20, 61)] + [[100], [101], [102], [200], [300], [500], [1000]]
    grid += [[6, v] for v in (50, 51, 52, 100, 200, 765)]
    grid += [[3, v] for v in (50, 100)] + [[d, 100] for d in (1, 2, 4, 5, 7, 8)]
    grid += [[3, 1, 1, 100], [3, 1, 1, 200]]
    if len(sys.argv) > 1:
        grid = [[int(x) for x in a.split(',')] for a in sys.argv[1:]]
    byshape = {}
    print("blocks -> landing        steps  unsafe midgates  L1    L2  shape       rmax  bad0")
    for blocks in grid:
        status, land, steps, unsafe, mg, toks, bad0 = run_gen(blocks)
        if status != 'LAND':
            print(f"{blocks} -> {status} steps={steps} unsafe={unsafe} mid={mg}")
            continue
        ch = compress(toks)
        out = l2(ch)
        h, sig = shape_sig(out)
        rmax = max([c[2] for c in out if c[0] == 'B'], default=0)
        key = (len(blocks), h)
        byshape.setdefault(key, []).append((tuple(blocks), tuple(land)))
        lstr = str(land) if len(land) < 8 else f"[{land[0]},{land[1]},...]({len(land)} blocks)"
        print(f"{str(blocks):>14} -> {lstr:>18} {steps:>9} {unsafe:>3} {len(mg):>3}     {len(ch):>5} {len(out):>4}  {h}  r={rmax}  {bad0}")
    print("\nshape classes:")
    for (nb, h), mem in sorted(byshape.items()):
        print(f"  nblocks={nb} shape={h}: {len(mem)} members, e.g. {mem[:6]}")
