# o15 milestones: A-entry (gate) census on the blank orbit — exact tape form at every gate event.
# Question: is the milestone state O(1) counters (o3/o4/o18-like) or a growing block VECTOR?
# Also: exact width law test W' vs floor(8W/3)+2 (the O15_REDUCTION claim, o18-correction-aware).
import sys
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
STEPS = int(sys.argv[1]) if len(sys.argv) > 1 else 200_000_000
SZ = 1 << 27
tape = bytearray(SZ)
off = SZ // 2
pos, st = off, 0
lo = hi = pos
step = 0
events = []

def rle(seg):
    """runs of (bit, length)"""
    out = []
    if not seg:
        return out
    cur, n = seg[0], 1
    for b in seg[1:]:
        if b == cur:
            n += 1
        else:
            out.append((cur, n))
            cur, n = b, 1
    out.append((cur, n))
    return out

while step < STEPS:
    r = tape[pos]
    if st == 5 and r == 1:  # gate: F reads 1 -> A-entry next step
        i = lo
        while i <= hi and tape[i] == 0: i += 1
        j = hi
        while j >= lo and tape[j] == 0: j -= 1
        seg = bytes(tape[i:j + 1])
        runs = rle(seg)
        events.append((step, pos - off, i - off, j - off, tape[pos + 1], runs))
    t = M[st][r]
    if t is None:
        print(">>> HALT at step", step)
        break
    w, d, ns = t
    tape[pos] = w
    pos += d
    st = ns
    step += 1
    if pos < lo: lo = pos
    if pos > hi: hi = pos

print(f"steps: {step:,}, gate events (F-reads-1 = A-entries): {len(events)}")
print("\nper-event exact form (runs = RLE of nonzero extent; head marked by pos):")
for k, (s, p, i, j, rn, runs) in enumerate(events):
    W = j - i + 1
    ones_runs = [n for b, n in runs if b == 1]
    zero_runs = [n for b, n in runs if b == 0]
    print(f"  [{k:2d}] step={s:>12,} headpos={p:>7} extent=[{i},{j}] width={W:>7} rightnb={rn}")
    print(f"       1-blocks: {ones_runs}")
    print(f"       0-runs interior: {zero_runs}  (max={max(zero_runs) if zero_runs else 0})")
    if len(runs) <= 24:
        print(f"       full RLE: {runs}")
    else:
        print(f"       RLE head: {runs[:12]} ... tail: {runs[-12:]}")

print("\nwidth-law test W' vs floor(8W/3)+2 (consecutive gate events):")
for k in range(len(events) - 1):
    (s, p, i, j, rn, runs) = events[k]
    (s2, p2, i2, j2, rn2, runs2) = events[k + 1]
    W, W2 = j - i + 1, j2 - i2 + 1
    pred = (8 * W) // 3 + 2
    print(f"  [{k}] W={W} -> {W2}  pred={pred}  diff={W2 - pred}   (steps in gen: {s2 - s:,})")
