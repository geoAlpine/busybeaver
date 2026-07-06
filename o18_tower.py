# o18: bounds-GUARDED re-census of the N=2 (mod 3) composite law + 3-adic tower probe.
# (Earlier runs had wraparound risk: pads too small for multi-epoch growth. This one raises on
# any approach to the tape edge.) Tests the prediction: the recursing branch is N = -10 (mod 3^k);
# the other two branches per level close with land = ((8/3)^d N + c)/1 affine laws.
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

class Overflow(Exception): pass

def rle(seg):
    out = []
    for b in seg:
        if out and out[-1][0] == b:
            out[-1][1] += 1
        else:
            out.append([b, 1])
    return [(b, c) for b, c in out]

def run_full(N, lpad=None, rpad=None, maxF=40, budget=None):
    if lpad is None: lpad = 220 * N + 8000
    if rpad is None: rpad = 4 * N + 2000
    if budget is None: budget = min(3000 * N * N + 5_000_000, 250_000_000)
    tape = bytearray(lpad + N + rpad)
    p0 = lpad
    for i in range(1, N):
        tape[p0 + i] = 1
    pos, st = p0, 5
    steps = 0
    unsafe = 0
    lo = hi = pos
    L = len(tape)
    fents = []
    first = True
    while steps < budget:
        if pos < 4 or pos > L - 5:
            raise Overflow(f"N={N}: tape edge at step {steps}")
        r = tape[pos]
        if st == 5 and not first:
            i = lo
            while i <= hi and tape[i] == 0: i += 1
            j = hi
            while j >= lo and tape[j] == 0: j -= 1
            seg = bytes(tape[i:j + 1])
            clean = (r == 0 and pos == i - 1 and seg.count(0) == 0)
            fents.append((steps, clean, (j - i + 2) if clean else None, rle(seg), pos - i))
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

def depth3(N):  # 3-adic agreement with -10
    d = 0
    while (N + 10) % (3 ** (d + 1)) == 0:
        d += 1
    return d

grid = [n for n in range(8, 261, 3)] + [287, 314, 341, 368, 395, 422, 449, 503,
        1001, 1004]
if len(sys.argv) > 1:
    grid = [int(x) for x in sys.argv[1:]]

print("  N  m9 m27 m81  v3(N+10)  land    #F  unsafe  status")
rows = []
for N in grid:
    try:
        status, fents, steps, unsafe = run_full(N)
    except Overflow as e:
        print(f"{N:5d}  OVERFLOW: {e}")
        continue
    land = fents[-1][2] if fents and fents[-1][1] else None
    rows.append((N, land, len(fents), unsafe, status, fents))
    print(f"{N:5d} {N%9:3d} {N%27:3d} {N%81:3d}   {depth3(N):2d}   {str(land):>7} {len(fents):3d}   {unsafe}    {status}")

# law fits by (depth, residue at the closing level)
print("\n=== law fits: land*3^(d+1) - 8^(d+1)*N should be constant per closing class ===")
from collections import defaultdict
cls = defaultdict(list)
for N, land, nf, u, st_, f in rows:
    if land is None: continue
    d = depth3(N)   # closing level: laws should be affine with ratio (8/3)^(d+1)
    cls[(d, N % 3 ** (d + 2))].append((N, land, nf))
for (d, m), mem in sorted(cls.items()):
    k = d + 1
    consts = sorted(set((3 ** k) * land - (8 ** k) * N for N, land, _ in mem))
    nfs = sorted(set(nf for _, _, nf in mem))
    ok = "CONST" if len(consts) == 1 else "SPLIT!"
    print(f"  depth={d} (N mod {3**(d+2)} = {m}): {len(mem)} members  3^{k}*L-8^{k}*N = {consts[:5]} {ok}  #F={nfs}")

# dirty-form census at each recursion level (the gate windows / defect shapes)
print("\n=== dirty (non-clean) F-entry forms by level index ===")
forms = defaultdict(set)
for N, land, nf, u, st_, f in rows:
    for idx, (s, clean, _, R, hp) in enumerate(f):
        if not clean:
            # canonical: replace big block lengths with '*'
            can = tuple((b, c if c <= 8 else '*') for b, c in R)
            forms[idx].add((can, hp if hp < 0 else 'int'))
for idx in sorted(forms):
    print(f"  F-entry #{idx}:")
    for can, hp in sorted(forms[idx], key=str):
        print(f"     head@{hp}  " + ' '.join((f"{b}^{c}" for b, c in can)))
