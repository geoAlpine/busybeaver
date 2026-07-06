# o18 generation-law grid: run standalone C_N through ALL F-entries to the next CLEAN reset.
# Records every F-entry (the halt gate: D-read-1 two steps earlier), its radius-5 window,
# the dirty intermediate configs (RLE), safety, and the final landing law N' =? floor(8N/3)+2.
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
    return out

def rle_str(seg, head=None):
    s = ''
    for b, c in rle(seg):
        s += f"{b}^{c} "
    return s.strip()

def run_full(N, budget=None, maxF=8):
    if budget is None:
        budget = 60 * N * N // 10 + 200000
    pad = 4 * N + 64
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
            win = bytes(tape[pos - 5:pos + 6])
            fents.append((steps, clean, (j - i + 2) if clean else None,
                          rle(seg), pos - i, win))
            if clean:
                return ('LAND', fents, steps, unsafe)
            if len(fents) >= maxF:
                return ('MAXF', fents, steps, unsafe)
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

def wstr(win):
    s = ''.join(str(b) for b in win)
    return s[:5] + '[' + s[5] + ']F' + s[6:]

grid = (list(range(6, 63)) + [99, 100, 101, 102, 103, 104, 200, 201, 202, 299, 300, 301,
        500, 501, 502, 998, 999, 1000, 1001, 1002, 1003, 2000, 2001, 2002, 3000, 3001, 3002])
if len(sys.argv) > 1:
    grid = [int(x) for x in sys.argv[1:]]

print("N mod3 | status  N_land  pred  law | steps unsafe #F | dirty F-entry windows + RLE summary")
fails = []
dirty_windows = {}
for N in grid:
    status, fents, steps, unsafe = run_full(N)
    pred = (8 * N) // 3 + 2
    land = fents[-1][2] if fents and fents[-1][1] else None
    law = "OK" if land == pred else "FAIL"
    if law == "FAIL" or unsafe or status != 'LAND':
        fails.append((N, status, land, pred, unsafe))
    nd = sum(1 for f in fents if not f[1])
    line = f"{N:5d}  {N%3}  | {status:5s} {str(land):>6} {pred:5d}  {law} | {steps:8d} {unsafe} {len(fents)}"
    for (s, clean, _, R, hp, win) in fents:
        if not clean:
            key = (N % 3, bytes(win))
            dirty_windows.setdefault(key, []).append(N)
            # compact RLE: collapse alternating (0,1) middles
            comp = '+'.join(f"{b}x{c}" for b, c in R[:4]) + ('...' if len(R) > 8 else '') + \
                   '+' + '+'.join(f"{b}x{c}" for b, c in R[-3:])
            line += f"  [dirty@{s}: win={wstr(win)} head@{hp} rle {comp}]"
    print(line)

print("\nDIRTY F-entry window census (mod3, radius-5 window) -> N members:")
for (m, win), Ns in sorted(dirty_windows.items()):
    print(f"  mod3={m} win={wstr(win)}: {len(Ns)} members, N={Ns[:10]}{'...' if len(Ns)>10 else ''}")
print("\nfailures / unsafe / non-landings:", fails if fails else "NONE")
