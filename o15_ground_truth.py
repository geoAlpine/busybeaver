# o15 ground truth: halt gate from the transition table + concrete halt-window census.
# o15 = 1RB---_0RC0RE_1RD1RF_1LE0LB_1RC0LD_1RC1RA   halt = A reads 1
# Pipeline step 1 of the o4/o3/o18 template port (O4_TEMPLATE_CLOSURE / O3_TEMPLATE_PORT / O18_TEMPLATE_PORT).
import sys
SPEC = "1RB---_0RC0RE_1RD1RF_1LE0LB_1RC0LD_1RC1RA"

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
assert halts == [(0, 1)], "halt must be exactly A reads 1"
preds = [(s, r, M[s][r]) for s in range(6) for r in range(2)
         if M[s][r] is not None and M[s][r][2] == 0]
print("transitions INTO A:", [(names[s], r, ("write%d" % w, "R" if d > 0 else "L")) for s, r, (w, d, _) in preds])
assert len(preds) == 1 and preds[0][:2] == (5, 1), "A entered only by F reads 1"
w, d, _ = preds[0][2]
assert w == 1 and d == 1, "F,1 -> 1RA (writes 1, moves RIGHT)"
# chase: after F reads 1 at cell p (writes 1, keeps it 1), head moves to p+1 in state A.
# A reads cell p+1: halt iff that cell is 1.
print("PROVEN from table: o15 halts <=> at some step, F reads a 1 whose RIGHT neighbour is 1")
print("  (start state A on blank reads 0 at step 0 -> safe; every other A-entry is via F,1)")
print("local safety condition: every F-read-of-1 has right neighbour 0")
print("F,0 ->", M[5][0], " (writes 1, moves R, state %s)" % names[M[5][0][2]])

# ---- (b) concrete census: F-reads-1 (= A-entry) windows radius 3/4/5 ----
print("\n== (b) blank-tape census ==")
STEPS = int(sys.argv[1]) if len(sys.argv) > 1 else 20_000_000
SZ = 1 << 26
tape = bytearray(SZ)
off = SZ // 2
pos, st = off, 0
lo = hi = pos
step = 0
f1 = []            # F-reads-1 events: (step, pos-off, rightnb)
f1_right1 = 0      # unsafe count
nearmiss = 0       # F reads 0 with right neighbour 1 (would-be-fatal if the read were 1)
w3, w4, w5 = {}, {}, {}
w3s, w4s, w5s = [], [], []
while step < STEPS:
    r = tape[pos]
    if st == 5:  # F
        if r == 1:
            rn = tape[pos + 1]
            f1.append((step, pos - off, rn))
            for rad, W, Ws in ((3, w3, w3s), (4, w4, w4s), (5, w5, w5s)):
                key = bytes(tape[pos - rad:pos + rad + 1])
                if key not in W:
                    W[key] = 0
                    Ws.append(step)
                W[key] += 1
            if rn == 1:
                f1_right1 += 1
                print("UNSAFE F-read-1 (right nb 1) at step", step, "-> HALT in 1 step")
        elif tape[pos + 1] == 1:
            nearmiss += 1
    t = M[st][r]
    if t is None:
        print(">>> HALT at step", step, "state", names[st], "read", r)
        break
    w, d, ns = t
    tape[pos] = w
    pos += d
    st = ns
    step += 1
    if pos < lo: lo = pos
    if pos > hi: hi = pos

print(f"steps run: {step:,}")
print(f"F-reads-1 events (halt-relevant gate = A-entries): {len(f1)}")
print(f"  unsafe (right nb 1): {f1_right1}")
print(f"near-miss F-reads-0-with-right-1: {nearmiss:,}")
for rad, W, Ws in ((3, w3, w3s), (4, w4, w4s), (5, w5, w5s)):
    print(f"radius-{rad} window set at F-reads-1: {len(W)} windows, last new at step {max(Ws) if Ws else '-'}")
    for k, c in sorted(W.items(), key=lambda kv: -kv[1]):
        s = ''.join(str(b) for b in k)
        s = s[:rad] + '[' + s[rad] + ']F' + s[rad + 1:]
        print(f"    {s}  x{c}")
print("event list (step, pos, right-nb):")
for e in f1[:60]:
    print("   ", e)
