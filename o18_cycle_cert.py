# o18 cycle certificates: the three sweep cycles of the level-0 template, verified
# translation-invariant by direct construction (the 2-transition induction: if after p steps the
# state returns, the head is displaced by D, and the consumed/written cells follow a fixed
# period-|D| tiling, then by determinism+locality the sweep continues over any longer tiling).
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
names = "ABCDEF"

def cert(name, s0, pattern, reps, phase):
    """Tile `pattern` reps times; head at position phase inside the mid tile; run len(pattern)
    steps per cycle; check state-return, displacement, and write-tiling for several cycles."""
    tape = bytearray(64) + bytearray(pattern * reps) + bytearray(64)
    base = 64 + len(pattern) * (reps // 2) + phase
    pos, st = base, s0
    tr = []
    p = None
    # run up to 20 cycles of length |pattern| each (cycle period = steps to state-return)
    hist = [(st, pos, bytes(tape))]
    for step in range(1, 20 * len(pattern) + 1):
        r = tape[pos]
        t = M[st][r]
        if t is None:
            return f"{name}: HALT during certificate (!)"
        w, d, ns = t
        tape[pos] = w
        pos += d
        st = ns
        hist.append((st, pos, bytes(tape)))
        if st == s0 and p is None and step > 0:
            p = step
    if p is None:
        return f"{name}: no state-return"
    # check: config at time k*p equals config at time (k-1)*p displaced by D, for k=2..4
    D = hist[p][1] - hist[0][1]
    ok = True
    checked = 0
    for k in range(8, 13):
        if k * p >= len(hist): break
        s1, p1, t1 = hist[(k - 1) * p]
        s2, p2, t2 = hist[k * p]
        if s2 != s1 or p2 - p1 != D:
            ok = False; break
        # tape equality under shift by D on the window around the head (radius 2|D|+2)
        R = 2 * abs(D) + 2
        w1 = t1[p1 - R: p1 + R + 1]
        w2 = t2[p2 - R: p2 + R + 1]
        if w1 != w2:
            ok = False; break
        checked += 1
    if checked < 3:
        ok = False
    return (f"{name}: period={p} D={D:+d} start={names[s0]} pattern={''.join(map(str,pattern))} "
            f"phase={phase} -> {'CERTIFIED (self-similar under shift, 3 consecutive cycles)' if ok else 'FAIL'}")

print("== sweep cycle certificates (level-0 template) ==")
# rightward crawl A0B1: A over fresh '0 1' tiling? observed: A reads 0, B reads 1.
print(cert("A0B1 rightward", 0, bytes([0, 1]), 24, 0))
print(cert("A0B1 rightward (phase check)", 0, bytes([1, 0]), 24, 1))
# leftward inverting crawl A1E1B0C0: A reads 1 with 1 right, 0s left... tiling '1 1 0' leftward?
for pat in (bytes([1, 1, 0]), bytes([0, 1, 1]), bytes([1, 0, 1])):
    print(cert("A1E1B0C0 leftward", 0, pat, 24, 1))
# final solidifying sweep C1D0 over alternating (01)* zone, moving left
for pat in (bytes([0, 1]), bytes([1, 0])):
    print(cert("C1D0 leftward", 2, pat, 24, 1))
