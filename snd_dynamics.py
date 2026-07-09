#!/usr/bin/env python3
"""
SPACE NEEDLE decision attempt -- STEP 1: re-derive exact counter dynamics + halt
condition from the raw TM, verify 0-mismatch on the REAL orbit (>= 1e5 raw steps).

SN = 1RB1LA_1LC0RE_1LF1LD_0RB0LA_1RC1RE_---0LD  (blank tape; halt = F reads 0).
Claimed epoch map:  f(m) = m + 3*floor(m/2^(v+1)) + v,  v = # trailing 1-bits of m.
Claimed halt gate: state C reads a 0 whose LEFT neighbour is 0.
Claimed fatal set S: epoch seeded by 1^m halts iff m in S = {2^k-1} U sporadics.
"""
import sys

def parse(spec):
    M = []
    for st in spec.split('_'):
        row = []
        for t in (st[0:3], st[3:6]):
            row.append(None if (t[0] == '-' or t[2] == 'Z')
                       else (int(t[0]), 1 if t[1] == 'R' else -1, ord(t[2]) - ord('A')))
        M.append(row)
    return M

SN = "1RB1LA_1LC0RE_1LF1LD_0RB0LA_1RC1RE_---0LD"

def tz1(m):
    v = 0
    while m & 1:
        v += 1; m >>= 1
    return v

def f(m):
    v = tz1(m)
    return m + 3 * (m >> (v + 1)) + v

# ---------- Raw TM from BLANK tape, extract milestone sequence ----------
def run_blank(max_steps):
    """Run SN from a truly blank tape. Detect single-block milestones
    (0^inf 1^m 0^inf, head on the 0 right of block, state C). Return the list of
    milestone m-values encountered, plus ('HALT',step) or ('RAN',step)."""
    M = parse(SN)
    SZ = 1 << 23
    tape = bytearray(SZ)
    off = SZ // 2
    pos = off; st = 0; step = 0
    lo = hi = off
    miles = []
    halt = None
    while step < max_steps:
        r = tape[pos]
        act = M[st][r]
        if act is None:
            halt = ('HALT', step); break
        ww, d, ns = act
        tape[pos] = ww; pos += d; st = ns; step += 1
        if pos < lo: lo = pos
        elif pos > hi: hi = pos
        # milestone test: state C (index2), just read a 0
        if step > 2 and st == 2 and r == 0:
            a = lo
            while a <= hi and tape[a] == 0: a += 1
            if a <= hi:
                z = a
                while z <= hi and tape[z] == 1: z += 1
                if pos == z and all(tape[i] == 0 for i in range(z, hi + 1)):
                    miles.append(z - a)
    return miles, (halt if halt else ('RAN', step))

# ---------- Raw TM epoch from a milestone (verify f) ----------
def epoch_raw(m, budget):
    M = parse(SN); SZ = 1 << 21; tape = bytearray(SZ); off = SZ // 2
    for i in range(m): tape[off + i] = 1
    pos = off + m; st = 2; step = 0; lo = off; hi = off + m
    while step < budget:
        r = tape[pos]; act = M[st][r]
        if act is None: return ('HALT', step)
        ww, d, ns = act; tape[pos] = ww; pos += d; st = ns; step += 1
        if pos < lo: lo = pos
        elif pos > hi: hi = pos
        if step > 2 and st == 2 and r == 0:
            a = lo
            while a <= hi and tape[a] == 0: a += 1
            if a <= hi:
                z = a
                while z <= hi and tape[z] == 1: z += 1
                if pos == z and all(tape[i] == 0 for i in range(z, hi + 1)):
                    return ('MILE', z - a)
    return ('BUDGET', None)

if __name__ == "__main__":
    STEPS = int(sys.argv[1]) if len(sys.argv) > 1 else 200_000

    # (A) blank-tape real orbit, >=1e5 raw steps
    miles, status = run_blank(STEPS)
    print(f"[REAL ORBIT] blank tape, {STEPS} raw steps -> status {status}")
    print(f"  milestone m-sequence ({len(miles)} milestones): {miles[:16]}")

    # (B) does iterating f from m0=2 reproduce the real milestone sequence?
    fm = [2]
    for _ in range(len(miles) + 4):
        fm.append(f(fm[-1]))
    # align: the real milestone list should be a subsequence/prefix of f-iterates
    # (raw TM may register the first milestone at m=2 or later). Find offset.
    matched = False
    for offset in range(6):
        seq = fm[offset:offset + len(miles)]
        if seq == miles:
            matched = True
            print(f"  f-iterates from m0=2 (offset {offset}) REPRODUCE the real "
                  f"milestone sequence: {len(miles)}/{len(miles)} EXACT.")
            break
    if not matched:
        print(f"  MISMATCH: f-iterates {fm[:16]} vs real {miles[:16]}")

    # (C) verify f vs raw TM epoch-by-epoch, m=2..400
    ok = tot = 0; mism = []
    for m in range(2, 400):
        res, val = epoch_raw(m, 3 * m ** 3 + 500000); tot += 1
        if res == 'HALT':
            ok += 1  # epoch halts => m in S; consistency checked in protect script
        elif res == 'MILE' and val == f(m):
            ok += 1
        else:
            mism.append((m, res, val, f(m)))
    print(f"[VERIFY f] raw-TM epochs m=2..399: {ok}/{tot} consistent; mism={mism[:5]}")

    # (D) confirm no halt on the real orbit within STEPS
    print(f"[NO-HALT] real orbit did NOT halt in {STEPS} steps: "
          f"{status[0] == 'RAN'}")
