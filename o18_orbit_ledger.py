# o18 arithmetic orbit ledger: iterate the VERIFIED clean-reset laws from N=10 (blank orbit joins
# at C_10, step 36); stop when hitting a branch whose law is not yet verified.
# Verified laws (exact concrete grids, guarded sims):
#   N=0 (mod 3)          -> (8N+6)/3          [#F=1]
#   N=1 (mod 3)          -> (8N+4)/3          [#F=1]
#   N=2,5 (mod 9)        -> (64N-20)/9, (64N-104)/9      [#F=3]
#   N=8 (mod 27)         -> (512N-1288)/27                [#F=4]
#   N=80 (mod 81)        -> (4096N-11618)/81              [#F=5]
#   N=17,26,44,53 (mod 81) deep branches: NOT yet closed -> STOP
# Also: PREDICT-and-CONFIRM (o3 gold standard) for two fresh N via direct simulation.
import sys

def law(N):
    if N % 3 == 0: return (8 * N + 6) // 3, '0mod3'
    if N % 3 == 1: return (8 * N + 4) // 3, '1mod3'
    m9 = N % 9
    if m9 == 2: return (64 * N - 20) // 9, '2mod9'
    if m9 == 5: return (64 * N - 104) // 9, '5mod9'
    if N % 27 == 8: return (512 * N - 1288) // 27, '8mod27'
    if N % 81 == 80: return (4096 * N - 11618) // 81, '80mod81'
    return None, f'DEEP(mod81={N%81})'

N = 10
print("blank orbit (arithmetic, verified laws), from N=10:")
hist = []
for n in range(200000):
    N2, tag = law(N)
    hist.append((n, N, tag))
    if N2 is None:
        print(f"  STOP at generation {n}: N has ~{len(str(N))} digits, branch {tag} not closed")
        break
    if n < 25:
        print(f"  gen {n:3d}: N={N}  [{tag}]")
    N = N2
else:
    print(f"  ran 200000 generations without hitting a deep branch (final ~{len(str(N))} digits)")

from collections import Counter
tags = Counter(t for _, _, t in hist)
print("branch usage:", dict(tags))
print("total generations before stop:", len(hist) - 1)

# ---- predict & confirm by direct simulation ----
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

def sim_to_clean(N, budget):
    lpad = 25 * N + 8000
    rpad = 4 * N + 2000
    tape = bytearray(lpad + N + rpad)
    p0 = lpad
    for i in range(1, N):
        tape[p0 + i] = 1
    pos, st = p0, 5
    steps = 0; unsafe = 0
    lo = hi = pos; L = len(tape)
    first = True
    while steps < budget:
        if pos < 4 or pos > L - 5:
            return ('OVERFLOW', None, steps, unsafe)
        r = tape[pos]
        if st == 5 and not first:
            a = lo
            while a <= hi and tape[a] == 0: a += 1
            b = hi
            while b >= lo and tape[b] == 0: b -= 1
            if r == 0 and pos == a - 1 and bytes(tape[a:b + 1]).count(0) == 0:
                return ('LAND', b - a + 2, steps, unsafe)
        first = False
        if st == 3 and r == 1 and tape[pos - 1] == 1:
            unsafe += 1
        t = M[st][r]
        if t is None:
            return ('HALT', None, steps, unsafe)
        w, d, ns = t
        tape[pos] = w
        pos += d; st = ns; steps += 1
        if pos < lo: lo = pos
        if pos > hi: hi = pos
    return ('BUDGET', None, steps, unsafe)

print("\nPREDICT-and-CONFIRM (fresh N, never simulated before):")
for N in (2003, 305, 1421 if len(sys.argv) > 1 else 305):
    pred, tag = law(N)
    if pred is None:
        print(f"  N={N}: branch {tag}, no prediction"); continue
    status, land, steps, unsafe = sim_to_clean(N, 200_000_000)
    print(f"  N={N} [{tag}]: PREDICTED {pred}, simulated {status} {land} in {steps} steps, unsafe={unsafe}"
          f"  -> {'CONFIRMED' if land == pred else 'MISMATCH!'}")
