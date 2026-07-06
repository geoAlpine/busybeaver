# o18 ground truth: halt gate from the transition table + concrete halt-window census.
# o18 = 1RB0RE_1LC0RA_1LA1LD_1LC1LF_0LC0LB_1LE---   halt = F reads 1
# Pipeline step 1 of the o4/o3 template port (O4_TEMPLATE_CLOSURE / O3_TEMPLATE_PORT).
import sys
SPEC = "1RB0RE_1LC0RA_1LA1LD_1LC1LF_0LC0LB_1LE---"

def parse(spec):
    M = []
    for st in spec.split('_'):
        row = []
        for t in (st[0:3], st[3:6]):
            if t[0] == '-' or t[2] == 'Z':
                row.append(None)
            else:
                row.append((int(t[0]), 1 if t[1] == 'R' else -1, ord(t[2]) - ord('A')))
        M.append(row)
    return M

M = parse(SPEC)
names = "ABCDEF"

# ---- (a) Halt gate, PROVEN from the table by exhaustive predecessor scan ----
print("== (a) halt gate from the table ==")
halts = [(s, r) for s in range(6) for r in range(2) if M[s][r] is None]
print("halting entries:", [(names[s], r) for s, r in halts])
assert halts == [(5, 1)], "halt must be exactly F reads 1"
# who enters F?
preds = [(s, r, M[s][r]) for s in range(6) for r in range(2)
         if M[s][r] is not None and M[s][r][2] == 5]
print("transitions INTO F:", [(names[s], r, ("write%d" % w, "R" if d > 0 else "L")) for s, r, (w, d, _) in preds])
assert len(preds) == 1 and preds[0][:2] == (3, 1), "F entered only by D reads 1"
w, d, _ = preds[0][2]
assert w == 1 and d == -1, "D,1 -> 1LF (writes 1, moves LEFT)"
# chase: after D reads 1 at cell p (writes 1, keeps it 1), head moves to p-1 in state F.
# F reads cell p-1: halt iff that cell is 1.
print("PROVEN from table: o18 halts <=> at some step, D reads a 1 whose LEFT neighbour is 1")
print("local safety condition: every D-read-of-1 has left neighbour 0")
# F,0 behaviour (the safe branch):
print("F,0 ->", M[5][0], " (writes 1, moves L, state %s)" % names[M[5][0][2]])

# ---- (b) 20M-step concrete census: D-reads-1 windows (radius 3/4/5), near-misses ----
print("\n== (b) 20M-step blank-tape census ==")
STEPS = int(sys.argv[1]) if len(sys.argv) > 1 else 20_000_000
SZ = 1 << 26
tape = bytearray(SZ)
off = SZ // 2
pos, st = off, 0
lo = hi = pos
step = 0
d1 = []            # D-reads-1 events: (step, pos-off, leftnb)
d0_left1 = 0       # near-miss: D reads 0 with left neighbour 1
w3, w4, w5 = {}, {}, {}   # window census at D-reads-1: radius 3/4/5 (incl. state marker)
w3s, w4s, w5s = [], [], []  # first-seen steps
while step < STEPS:
    r = tape[pos]
    if st == 3:  # D
        if r == 1:
            ln = tape[pos - 1]
            d1.append((step, pos - off, ln))
            for rad, W, Ws in ((3, w3, w3s), (4, w4, w4s), (5, w5, w5s)):
                key = bytes(tape[pos - rad:pos + rad + 1])
                if key not in W:
                    W[key] = 0
                    Ws.append(step)
                W[key] += 1
            if ln == 1:
                print("UNSAFE D-read-1 (left nb 1) at step", step, "-> HALT in 2 steps")
        elif tape[pos - 1] == 1:
            d0_left1 += 1
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

print(f"steps run: {step:,}")
print(f"D-reads-1 events (halt-relevant gate): {len(d1)}")
print(f"  unsafe (left nb 1): {sum(1 for _,_,ln in d1 if ln==1)}")
print(f"near-miss D-reads-0-with-left-1: {d0_left1:,}")
for rad, W, Ws in ((3, w3, w3s), (4, w4, w4s), (5, w5, w5s)):
    print(f"radius-{rad} window set at D-reads-1: {len(W)} windows, last new at step {max(Ws) if Ws else '-'}")
    for k, c in sorted(W.items(), key=lambda kv: -kv[1]):
        s = ''.join(str(b) for b in k)
        s = s[:rad] + '[' + s[rad] + ']D' + s[rad + 1:]
        print(f"    {s}  x{c}")
print("event list (step, pos, left-nb):")
for e in d1[:40]:
    print("   ", e)
