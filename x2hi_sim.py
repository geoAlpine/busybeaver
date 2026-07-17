#!/usr/bin/env python3
"""x2hi_sim.py -- raw blank-tape simulator for x2, transcribed CELL-FOR-CELL from
lean/X2.lean's `step` (NOT from any other probe), plus verification against the
kernel-checked anchors `sanity50` / `sanity100`.

Machine: 1RB0RE_1RC---_0LD1LE_0RE1LD_1RF0LC_0RA1RE
Halt = state B reads 1.

Tape representation: dict pos->bit, absent = 0.  Head position = absolute Int, as
in Lean's Cfg.pos.  Lean's Tape zipper (left, head, right) is recovered from the
dict by DERIVING the extent from min/max of the SET cells (method invariant #4:
never from a caller-maintained lo/hi).
"""

# (state, bit) -> (write, move, next).  move: +1 = R, -1 = L.  None = HALT.
TRANS = {
    ('A', 0): (1, +1, 'B'),   # A0 -> 1RB
    ('A', 1): (0, +1, 'E'),   # A1 -> 0RE
    ('B', 0): (1, +1, 'C'),   # B0 -> 1RC
    ('B', 1): None,           # B1 -> --- HALT
    ('C', 0): (0, -1, 'D'),   # C0 -> 0LD
    ('C', 1): (1, -1, 'E'),   # C1 -> 1LE
    ('D', 0): (0, +1, 'E'),   # D0 -> 0RE
    ('D', 1): (1, -1, 'D'),   # D1 -> 1LD
    ('E', 0): (1, +1, 'F'),   # E0 -> 1RF
    ('E', 1): (0, -1, 'C'),   # E1 -> 0LC
    ('F', 0): (0, +1, 'A'),   # F0 -> 0RA
    ('F', 1): (1, +1, 'E'),   # F1 -> 1RE
}


class Sim:
    def __init__(self):
        self.cells = {}
        self.pos = 0
        self.st = 'A'
        self.n = 0
        self.halted = False

    def read(self):
        return self.cells.get(self.pos, 0)

    def step(self):
        t = TRANS[(self.st, self.read())]
        if t is None:
            self.halted = True
            return False
        w, mv, ns = t
        if w:
            self.cells[self.pos] = 1
        else:
            self.cells.pop(self.pos, None)
        self.pos += mv
        self.st = ns
        self.n += 1
        return True

    def run(self, n):
        for _ in range(n):
            if not self.step():
                raise RuntimeError('halted at %d' % self.n)
        return self

    def extent(self):
        """(lo, hi) DERIVED from the tape itself; head included."""
        keys = set(self.cells) | {self.pos}
        return min(keys), max(keys)

    def zipper(self):
        """Lean Tape (left, head, right), trimmed exactly like Lean's normal form:
        left = cells left of head nearest-first with trailing blanks dropped;
        right = cells right of head nearest-first with trailing blanks dropped."""
        lo, hi = self.extent()
        left = [self.cells.get(p, 0) for p in range(self.pos - 1, lo - 1, -1)]
        right = [self.cells.get(p, 0) for p in range(self.pos + 1, hi + 1)]
        while left and left[-1] == 0:
            left.pop()
        while right and right[-1] == 0:
            right.pop()
        return left, self.read(), right

    def word_letter(self):
        """(st, head-bit) -- the letter that DETERMINES the whole transition."""
        return (self.st, self.read())


def word(start, n):
    """the (st,h) word of the n-step window beginning at config `start` (a Sim)."""
    s = clone(start)
    out = []
    for _ in range(n):
        out.append(s.word_letter())
        if not s.step():
            raise RuntimeError('halt inside window')
    return out


def clone(s):
    t = Sim()
    t.cells = dict(s.cells)
    t.pos, t.st, t.n, t.halted = s.pos, s.st, s.n, s.halted
    return t


def _trim(bits):
    """Lean's Tape keeps blanks the head has VISITED (mvR pushes h::l even when
    h=false) while off-list cells are blank -- so the two representations differ
    only by trailing blanks, and the semantic normal form trims them on both."""
    v = [bool(x) for x in bits]
    while v and not v[-1]:
        v.pop()
    return v


def selfcheck():
    """Verify against lean/X2.lean's kernel-checked `sanity50` and `sanity100`."""
    ok = True

    for n, exp in [
        (50, ('D', 4, [1, 1, 1, 0, 1, 0], True, [1, 1, 0, 0, 1, 0])),
        (100, ('A', -2, [0, 1, 0], True,
               [0, 1, 0, 1, 0, 1, 0, 1, 0, 0, 1, 0])),
    ]:
        s = Sim().run(n)
        l, h, r = s.zipper()
        e = (exp[0], exp[1], _trim(exp[2]), exp[3], _trim(exp[4]))
        g = (s.st, s.pos, _trim(l), bool(h), _trim(r))
        m = g == e
        print('sanity%-4d lean: %s' % (n, (e,)))
        print('sanity%-4d sim : %s   %s' % (n, (g,), 'MATCH' if m else 'MISMATCH'))
        ok &= m

    print('\nSELFCHECK vs lean/X2.lean sanity50/sanity100: %s'
          % ('PASS' if ok else 'FAIL'))
    return ok


if __name__ == '__main__':
    import sys
    if not selfcheck():
        sys.exit(1)
