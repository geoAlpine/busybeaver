# o18 milestones: reset (epoch) census on the blank orbit + counter law + complete-state check.
# Reset = F-entry (F entered only via D,1->1LF; exactly once per epoch by the gate census).
# Claimed form (O18_NO_CERTIFICATE): C_N = [F] 0 1^{N-1}; law N' = floor(8N/3)+2.
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
STEPS = int(sys.argv[1]) if len(sys.argv) > 1 else 20_000_000
SZ = 1 << 26
tape = bytearray(SZ)
off = SZ // 2
pos, st = off, 0
lo = hi = pos
step = 0
resets = []
while step < STEPS:
    r = tape[pos]
    if st == 5:  # F-entry: capture config BEFORE the F move
        # find extent of nonzero tape
        i = lo
        while i <= hi and tape[i] == 0: i += 1
        j = hi
        while j >= lo and tape[j] == 0: j -= 1
        seg = bytes(tape[i:j + 1]) if i <= j else b''
        clean = (r == 0 and pos == i - 1 and seg.count(0) == 0)
        N = (j - i + 1) + 1 if clean else None  # head 0-cell + (N-1) ones
        resets.append((step, pos - off, clean, N, len(seg), seg.count(0)))
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

print(f"steps: {step:,}, F-entries (epoch resets): {len(resets)}")
print(" idx      step        pos  clean     N   ones  interior0")
for k, (s, p, c, N, L, z) in enumerate(resets):
    print(f"  {k:2d} {s:10d} {p:10d}  {str(c):5s} {N if N else '-':>6}  {L:6d}  {z}")
print("\ncounter-law check N' == floor(8N/3)+2 :")
ok = True
for k in range(len(resets) - 1):
    N, N2 = resets[k][3], resets[k + 1][3]
    if N is None or N2 is None:
        ok = False; print(f"  gen {k}: NON-CLEAN reset, law n/a"); continue
    pred = (8 * N) // 3 + 2
    flag = "OK" if pred == N2 else "FAIL"
    if pred != N2: ok = False
    print(f"  gen {k}: N={N} (mod3={N%3}) -> {N2}, predicted {pred}  {flag}")
print("law exact over all observed generations:", ok)
print("\ncomplete-state check: every reset config IS exactly C_N=[F] 0 1^(N-1) (clean flag above);")
print("all clean:", all(c for _, _, c, _, _, _ in resets))
