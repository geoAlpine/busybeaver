# o18: verify the REAL orbit's landing from C_3890 (the first N=2 mod 3 value the blank orbit hits).
# Prior notes claimed 3890 -> 10375 -> 27668 via f(N)=floor(8N/3)+2; the composite law predicts
# 3890 (=2 mod 9) -> (64*3890-20)/9 = 27660 with a dirty intermediate pair, skipping "10375".
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
N = 3890
lpad = 9 * N + 4000
rpad = 2 * N + 2000
tape = bytearray(lpad + N + rpad)
p0 = lpad
for i in range(1, N):
    tape[p0 + i] = 1
pos, st = p0, 5
steps = 0
unsafe = 0
lo = hi = pos
L = len(tape)
first = True
budget = 400_000_000
while steps < budget:
    if pos < 4 or pos > L - 5:
        print("OVERFLOW at step", steps); break
    r = tape[pos]
    if st == 5 and not first:
        i = lo
        while i <= hi and tape[i] == 0: i += 1
        j = hi
        while j >= lo and tape[j] == 0: j -= 1
        seg = bytes(tape[i:j + 1])
        z = seg.count(0)
        clean = (r == 0 and pos == i - 1 and z == 0)
        print(f"F-entry at step {steps}: clean={clean} width={j-i+2} interior0={z} head@{pos-i}")
        if clean:
            print("CLEAN LANDING N' =", j - i + 2, " (prediction (64N-20)/9 =", (64 * N - 20) // 9,
                  "; old notes' f(N) =", (8 * N) // 3 + 2, ")")
            break
    first = False
    if st == 3 and r == 1 and tape[pos - 1] == 1:
        unsafe += 1
    t = M[st][r]
    if t is None:
        print(">>> HALT at step", steps); break
    w, d, ns = t
    tape[pos] = w
    pos += d
    st = ns
    steps += 1
    if pos < lo: lo = pos
    if pos > hi: hi = pos
print("steps:", steps, "unsafe:", unsafe)
