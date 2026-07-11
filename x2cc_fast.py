#!/usr/bin/env python3
"""x2cc_fast.py -- EXACT accelerated simulator for the x2 machine
`1RB0RE_1RC---_0LD1LE_0RE1LD_1RF0LC_0RA1RE`  (CARRY CALCULUS infrastructure).

Acceleration: the three dominant loops are fast-forwarded with C-speed scans and
bulk writes, with EXACT step accounting (the accelerated trajectory is step-for-step
identical to the raw TM; validated by `--validate`):

  R-cycle  E@0,F@1 over (01)^m  -> writes 1^{2m}, head +2m, 2m steps   (comb repack)
  L-cycle  E@1,C@1 over 1-run   -> writes (10)^m leftward, head -2m, 2m steps (unpack)
  D-loop   D@1 over 1-run       -> head to first 0 leftward, k steps

Events surfaced to callers (all detected at micro-steps; the accelerated interiors
provably contain no event of either kind -- see comments):
  milestone: head in E reading 0 strictly left of every 1 on tape
  gapmeet:   head in E reading 0 with a 1 immediately left (E enters a maximal gap
             from its left end); gap length reported exactly.
"""
import sys
sys.path.insert(0, '/Users/aokiyousuke/busybeaver')
from mse_extract import parse, rle

SPEC = "1RB0RE_1RC---_0LD1LE_0RE1LD_1RF0LC_0RA1RE"
STN = "ABCDEF"
M = parse(SPEC)


def rs(rr):
    return ' '.join(f"{c}^{n}" if n > 1 else f"{c}" for c, n in rr)


class Fast:
    def __init__(self, SZ=1 << 27):
        self.SZ = SZ
        self.tape = bytearray(SZ)
        self.pos = SZ // 2
        self.st = 0
        self.step = 0
        self.lo = self.hi = self.pos
        self.left1 = SZ          # leftmost 1 on tape (SZ if none)
        self.halted = False

    # ---- event hooks: override / assign ----
    def on_milestone(self):  # head E@0, pos < left1 <= hi
        pass

    def on_gapmeet(self, gaplen):  # head E@0, tape[pos-1]==1
        pass

    def run(self, maxsteps):
        tape = self.tape
        pos, st, step = self.pos, self.st, self.step
        lo, hi, left1 = self.lo, self.hi, self.left1
        SZ = self.SZ
        while step < maxsteps:
            r = tape[pos]
            # ---------- events ----------
            if st == 4 and r == 0:
                if pos < left1:
                    if left1 <= hi:
                        self.pos, self.st, self.step = pos, st, step
                        self.lo, self.hi, self.left1 = lo, hi, left1
                        self.on_milestone()
                        maxsteps = self.maxsteps_override(maxsteps)
                elif tape[pos - 1] == 1:
                    j = tape.find(b'\x01', pos + 1, hi + 2)
                    gl = (j if j != -1 else hi + 1) - pos
                    self.pos, self.st, self.step = pos, st, step
                    self.lo, self.hi, self.left1 = lo, hi, left1
                    self.on_gapmeet(gl)
                    maxsteps = self.maxsteps_override(maxsteps)
            # ---------- halt ----------
            if st == 1 and r == 1:
                self.halted = True
                break
            # ---------- accelerations ----------
            if st == 4 and r == 0 and tape[pos + 1] == 1:
                # R-cycle: E@0 F@1 repeated. find extent of (01)^m from pos.
                m = 0
                W = 64
                base = pos
                while True:
                    end = min(base + W, SZ - 2)
                    ev = bytes(tape[base:end:2])
                    od = bytes(tape[base + 1:end:2])
                    i0 = ev.find(b'\x01')          # first even-offset cell that is 1
                    i1 = od.find(b'\x00')          # first odd-offset cell that is 0
                    cut = len(ev) if i0 == -1 else i0
                    if i1 != -1 and i1 < cut:
                        cut = i1
                    m += cut
                    if cut < len(ev) or end >= SZ - 2:
                        break
                    base = end
                    W *= 2
                m = min(m, (maxsteps - step) // 2)
                if m > 0:
                    tape[pos:pos + 2 * m] = b'\x01' * (2 * m)
                    if pos < left1:
                        left1 = pos
                    step += 2 * m
                    pos += 2 * m
                    if pos > hi:
                        hi = pos
                    continue
                # m == 0: fall through to micro-step
            elif st == 4 and r == 1 and pos >= 1 and tape[pos - 1] == 1:
                # L-cycle: E@1 writes 0, C@(pos-1) reads 1 writes 1, E@(pos-2)...
                j = tape.rfind(b'\x00', 0, pos + 1)   # first 0 at or left of pos
                R = pos - j                            # run of 1s [j+1..pos]
                m = min((R - 1) // 2, (maxsteps - step) // 2)  # safe full iterations
                if m > 0:
                    tape[pos - 2 * m + 1: pos + 1] = b'\x01\x00' * m
                    step += 2 * m
                    pos -= 2 * m
                    if pos < lo:
                        lo = pos
                    # leftmost written 1 is pos+1 (=old pos-2m+1); left1 unchanged
                    # (we wrote inside an existing 1-run; its left part [j+1..pos] intact)
                    continue
            elif st == 3 and r == 1:
                # D-loop leftward over 1s
                j = tape.rfind(b'\x00', 0, pos + 1)
                k = min(pos - j - 1, maxsteps - step)  # full 1-cells crossed beyond first
                if k > 0:
                    step += k
                    pos -= k
                    if pos < lo:
                        lo = pos
                    continue
            # ---------- micro-step ----------
            w, d, ns = M[st][r]
            if w == 1:
                if pos < left1:
                    left1 = pos
            elif pos == left1:
                nx = tape.find(b'\x01', pos + 1, hi + 2)
                left1 = nx if nx != -1 else SZ
            tape[pos] = w
            pos += d
            st = ns
            step += 1
            if pos < lo:
                lo = pos
            elif pos > hi:
                hi = pos
        self.pos, self.st, self.step = pos, st, step
        self.lo, self.hi, self.left1 = lo, hi, left1

    def maxsteps_override(self, cur):
        return cur

    def low_rle(self):
        """RLE of tape from leftmost 1 up to (not incl.) the leftmost BIG 1-run (>=15)."""
        t, lo, hi = self.tape, self.lo, self.hi
        i = self.left1
        runs = []
        while i <= hi:
            c = t[i]
            if c == 1:
                j = t.find(b'\x00', i, hi + 2)
                if j == -1:
                    j = hi + 1
            else:
                j = t.find(b'\x01', i, hi + 2)
                if j == -1:
                    j = hi + 1
            n = j - i
            if c == 1 and n >= 15:
                break
            runs.append((c, n))
            i = j
        return runs, (i, n if c == 1 and n >= 15 else None)


def validate(nsteps=2_000_000):
    """step-exact cross-check fast vs raw."""
    f = Fast(1 << 23)
    # raw
    SZ = 1 << 23
    tape = bytearray(SZ)
    pos, st = SZ // 2, 0
    marks_raw = []
    for step in range(nsteps):
        r = tape[pos]
        if st == 1 and r == 1:
            break
        if step % 100_000 == 0:
            marks_raw.append((step, pos, st))
        w, d, ns = M[st][r]
        tape[pos] = w
        pos += d
        st = ns
    raw_final = (nsteps, pos, st, bytes(tape).count(1))
    # fast: run to each mark and compare
    ok = True
    for (s, p, q) in marks_raw:
        f.run(s)
        if not (f.step == s and f.pos == p and f.st == q):
            print(f"MISMATCH at {s}: fast=({f.step},{f.pos},{f.st}) raw=({s},{p},{q})")
            ok = False
            break
    f.run(nsteps)
    fast_final = (f.step, f.pos, f.st, bytes(f.tape).count(1))
    print("raw :", raw_final)
    print("fast:", fast_final)
    print("VALIDATED step-exact" if ok and raw_final == fast_final else "FAILED")


if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "--validate":
        validate(int(sys.argv[2]) if len(sys.argv) > 2 else 2_000_000)
