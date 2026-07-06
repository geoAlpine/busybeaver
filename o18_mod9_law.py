# o18: the N=2 (mod 3) composite generation law — residue-tower census.
# Runs standalone C_N (N=2 mod 3) to the next CLEAN reset, recording every F-entry
# (dirty forms: [F] 1^m 0 1^e blocks), classifies the landing law by N mod 9 / 27 / 81.
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
            out.append((b, 1) if False else [b, 1])
    return [(b, c) for b, c in out]

def run_full(N, maxF=25):
    budget = 200 * N * N + 3_000_000
    pad = 12 * N + 256
    tape = bytearray(pad + N + pad)
    p0 = pad
    for i in range(1, N):
        tape[p0 + i] = 1
    pos, st = p0, 5
    steps = 0
    unsafe = 0
    lo = hi = pos
    fents = []
    first = True
    while steps < budget:
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

grid = [n for n in range(8, 260, 3)]
if len(sys.argv) > 1:
    grid = [int(x) for x in sys.argv[1:]]

rows = []
print("  N  m9 m27  land   #F unsafe  dirty-forms (m,defect-off-from-right;...)")
for N in grid:
    status, fents, steps, unsafe = run_full(N)
    land = fents[-1][2] if fents and fents[-1][1] else None
    forms = []
    for (s, clean, _, R, hp) in fents:
        if not clean:
            # describe: list of (blocklen) with 0-defects; expect 1^m 0 1^e patterns
            desc = ','.join(f"{b}x{c}" for b, c in R) if len(R) <= 7 else \
                   f"{len(R)}blk:" + ','.join(f"{b}x{c}" for b, c in R[:2]) + ".." + \
                   ','.join(f"{b}x{c}" for b, c in R[-2:])
            forms.append(f"h@{hp}:{desc}")
    rows.append((N, land, len(fents), unsafe, forms, status))
    print(f"{N:4d} {N%9:3d} {N%27:3d} {str(land):>6} {len(fents):3d} {unsafe:2d}  {' | '.join(forms)}"
          + ("" if status in ('LAND',) else f"  [{status}]"))

print("\nlaw fit per residue class (land = (64N+c)/9 test, and mod-27 refinement):")
from collections import defaultdict
by9 = defaultdict(list)
for N, land, nf, u, f, st_ in rows:
    if land: by9[N % 9].append((N, land, nf))
for m in sorted(by9):
    mem = by9[m]
    cs = set(9 * land - 64 * N for N, land, _ in mem)
    print(f"  N=%d (mod 9): {len(mem)} members, 9*land-64N values: {sorted(cs)[:8]}" % m)
    if len(cs) > 1:
        by27 = defaultdict(list)
        for N, land, nf in mem:
            by27[N % 27].append((N, land, nf, 9 * land - 64 * N))
        for m2 in sorted(by27):
            vals = by27[m2]
            cs2 = set(v for _, _, _, v in vals)
            cs3 = set(27 * land - 512 * N for N, land, _, _ in vals)
            print(f"      mod27={m2}: 9L-64N {sorted(cs2)[:6]}  27L-512N {sorted(cs3)[:6]}  #F={[x[2] for x in vals][:6]}")
