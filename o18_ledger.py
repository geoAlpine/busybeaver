# o18 ledger-side probe (o3 gold standard): standalone defective-block family
#   B(m,e) := 0^inf [F] 1^m 0 1^e 0^inf   (head on the 0 left of the 1^m block, state F)
# The reachable level-1 dirty form is e=6. Which defect geometries (e) are fatal?
# Then: PREDICT a halting config from the pattern and CONFIRM at a large standalone value.
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

def run_cfg(blocks, maxF=40, budget=None, lpadf=300):
    """blocks: list of (bit, count) placed right of the head cell; head on a 0 in state F."""
    W = sum(c for _, c in blocks)
    lpad = lpadf * W + 8000
    rpad = 4 * W + 2000
    tape = bytearray(lpad + W + rpad)
    p0 = lpad
    i = p0 + 1
    for b, c in blocks:
        for _ in range(c):
            tape[i] = b
            i += 1
    pos, st = p0, 5
    if budget is None: budget = 4000 * W * W + 5_000_000
    steps = 0
    unsafe = 0
    lo = hi = pos
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
            fents.append((steps, clean, (b - a + 2) if clean else None))
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

print("=== B(m,e) = [F] 1^m 0 1^e census ===")
print("   m\\e:", ' '.join(f"{e:>7d}" for e in range(0, 11)))
results = {}
for m in list(range(6, 31)) + [40, 50]:
    row = []
    for e in range(0, 11):
        status, fents, steps, unsafe = run_cfg([(1, m), (0, 1), (1, e)], budget=3_000_000, lpadf=40)
        land = fents[-1][2] if fents and fents[-1][1] else None
        results[(m, e)] = (status, land, steps, unsafe)
        row.append(f"H@{steps}" if status == 'HALT' else (f"L{land}" if status == 'LAND' else status[:4]))
    print(f"  {m:4d} :", ' '.join(f"{x:>7s}" for x in row))

# classify HALT cells by residues
halters = [(m, e) for (m, e), (s, _, _, _) in results.items() if s == 'HALT']
print("\nhalting (m,e):", halters)
if halters:
    from collections import defaultdict
    bye = defaultdict(list)
    for m, e in halters:
        bye[e].append(m)
    for e in sorted(bye):
        ms = sorted(bye[e])
        print(f"  e={e}: m in {ms}  (m mod 3: {sorted(set(x % 3 for x in ms))}, mod 9: {sorted(set(x % 9 for x in ms))})")
