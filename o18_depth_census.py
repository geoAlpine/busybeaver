# o18 DEPTH census: record EVERY F-entry form (exact RLE + head offset) from clean reset C_N
# for the N=2 (mod 3) classes, to extract the level-d -> level-(d+1) descent parameterization.
# Guarded tape (raises on edge approach). No acceleration.
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

def run_from_reset(N, budget, maxF=14, lpad=None, rpad=None):
    if lpad is None: lpad = 300 * N + 20000
    if rpad is None: rpad = 4 * N + 2000
    tape = bytearray(lpad + N + rpad)
    p0 = lpad
    for i in range(1, N):
        tape[p0 + i] = 1
    pos, st = p0, 5
    steps = 0
    unsafe = 0
    lo, hi = p0, p0 + max(N - 1, 1)  # hi covers the WRITTEN block (span-scan soundness)
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
            fents.append((steps, clean, (j - i + 2) if clean else None, rle(seg), pos - i, unsafe))
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

def fmt_rle(R):
    # compact: compress maximal runs of alternating 1^1 0^1 pairs into (10)^k
    toks = []
    i = 0
    n = len(R)
    while i < n:
        # count consecutive (1,1),(0,1) pairs
        k = 0
        j = i
        while j + 1 < n and R[j] == (1, 1) and R[j + 1] == (0, 1):
            k += 1
            j += 2
        if k >= 2:
            toks.append(f"(10)^{k}")
            i = j
        else:
            b, c = R[i]
            toks.append(f"{b}^{c}" if c > 1 else str(b))
            i += 1
    return ' '.join(toks)

if __name__ == '__main__':
    grid = [n for n in range(8, 121, 3)]
    budget = 20_000_000
    if len(sys.argv) > 1:
        grid = [int(x) for x in sys.argv[1:]]
else:
    grid = []

for N in grid:
    try:
        status, fents, steps, unsafe = run_from_reset(N, budget)
    except Overflow as e:
        print(f"N={N}  OVERFLOW: {e}")
        continue
    print(f"N={N}  (mod9={N%9} mod27={N%27} mod81={N%81})  status={status} steps={steps} unsafe={unsafe} #F={len(fents)}")
    for idx, (s, clean, land, R, hp, u) in enumerate(fents):
        tag = f"CLEAN L={land}" if clean else "dirty"
        print(f"   F#{idx}: step={s:>10} head@{hp:>3} {tag:>14}  {fmt_rle(R)}")
    sys.stdout.flush()
