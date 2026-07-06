# o18 generation event-stream template test (o4/o3 method, o17 negative-control aware).
# Per generation (reset C_N -> reset C_N'): token stream (state,read), level-1 minimal-period
# cycle compression (p<=24, the o3 lesson), then level-2 compression of the chunk-shape stream
# (the o17 test). Rigid template <=> O(1) shapes per class with only counts varying.
import sys, hashlib
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

def run_epoch(N, budget=None):
    """Run standalone C_N = [F] 0 1^{N-1} one full epoch to the next F-entry.
    Returns (status, tokens(bytes), landing_N or info, steps, unsafe)."""
    if budget is None:
        budget = 40 * N * N // 10 + 100000
    pad = 4 * N + 64
    tape = bytearray(pad + N + pad)
    p0 = pad
    for i in range(1, N):
        tape[p0 + i] = 1
    pos, st = p0, 5  # state F on the 0-cell
    toks = bytearray()
    unsafe = 0
    steps = 0
    lo = hi = pos
    first = True
    while steps < budget:
        r = tape[pos]
        if st == 5 and not first:
            # next reset: capture landing
            i = lo
            while i <= hi and tape[i] == 0: i += 1
            j = hi
            while j >= lo and tape[j] == 0: j -= 1
            seg = bytes(tape[i:j + 1])
            clean = (r == 0 and pos == i - 1 and seg.count(0) == 0)
            return ('LAND', bytes(toks), (j - i + 2) if clean else ('DIRTY', seg[:60]), steps, unsafe)
        first = False
        if st == 3 and r == 1 and tape[pos - 1] == 1:
            unsafe += 1
        t = M[st][r]
        if t is None:
            return ('HALT', bytes(toks), None, steps, unsafe)
        toks.append(st * 2 + r)
        w, d, ns = t
        tape[pos] = w
        pos += d
        st = ns
        steps += 1
        if pos < lo: lo = pos
        if pos > hi: hi = pos
    return ('BUDGET', bytes(toks), None, steps, unsafe)

def compress(s, pmax=24):
    """Level-1: greedy minimal-period run-length. Returns list of ('R',unit,count) / ('T',byte)."""
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
    """Level-2: compress the SHAPE sequence (counts dropped) of level-1 chunks."""
    shape = []
    for c in chunks:
        shape.append(('R', c[1]) if c[0] == 'R' else ('T', c[1]))
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
    """Final shape signature: drop all counts."""
    sig = []
    for c in l2out:
        sig.append(('B', c[1]) if c[0] == 'B' else c)
    h = hashlib.md5(repr(sig).encode()).hexdigest()[:10]
    return h, sig

grid = list(range(10, 61)) + [100, 101, 102, 200, 201, 202, 500, 501, 502, 1000, 1001, 1002]
if len(sys.argv) > 1:
    grid = [int(x) for x in sys.argv[1:]]

byclass = {}
print(" N  mod3  status  land   steps unsafe  L1chunks  L2toks  shape      r(max body count)")
for N in grid:
    status, toks, land, steps, unsafe = run_epoch(N)
    ch = compress(toks)
    out = l2(ch)
    h, sig = shape_sig(out)
    rmax = max([c[2] for c in out if c[0] == 'B'], default=0)
    byclass.setdefault((N % 3, h), []).append((N, rmax, steps))
    print(f"{N:5d}  {N%3}   {status:6s} {str(land):>6} {steps:7d}  {unsafe}     {len(ch):6d}  {len(out):5d}  {h}  r={rmax}")

print("\nshape classes (mod3, shape-hash) -> members:")
for (m, h), mem in sorted(byclass.items()):
    Ns = [n for n, _, _ in mem]
    rs = [r for _, r, _ in mem]
    print(f"  mod3={m} shape={h}: {len(mem)} members N={Ns[:8]}{'...' if len(Ns)>8 else ''}")
    print(f"      r values: {rs[:12]}{'...' if len(rs)>12 else ''}")
