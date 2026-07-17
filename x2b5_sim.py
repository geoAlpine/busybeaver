"""
x2b5_sim.py -- independent exact-bigint simulator for B5.

B5 = 1RB0LB_1LC1LB_1RD1LA_0RE0RE_0RA1RF_---1RD  (6-state, --- = halt).

Parse of the transition table (state: on0 / on1):
  A: 0->1RB   1->0LB
  B: 0->1LC   1->1LB
  C: 0->1RD   1->1LA
  D: 0->0RE   1->0RE
  E: 0->0RA   1->1RF
  F: 0->HALT  1->1RD

Halt fires iff, while in state F, the head reads 0.

Tape: dict-of-nonzero-cells (default 0) with head position; exact, unbounded.
"""

STATES = "ABCDEF"

# rules[state][symbol] = (write, move(+1=R,-1=L), next) or None for halt
RULES = {
    'A': {0: (1, +1, 'B'), 1: (0, -1, 'B')},
    'B': {0: (1, -1, 'C'), 1: (1, -1, 'B')},
    'C': {0: (1, +1, 'D'), 1: (1, -1, 'A')},
    'D': {0: (0, +1, 'E'), 1: (0, +1, 'E')},
    'E': {0: (0, +1, 'A'), 1: (1, +1, 'F')},
    'F': {0: None,          1: (1, +1, 'D')},
}


class Tape:
    __slots__ = ('cells', 'lo', 'hi')

    def __init__(self):
        self.cells = {}
        self.lo = 0
        self.hi = 0

    def read(self, pos):
        return self.cells.get(pos, 0)

    def write(self, pos, sym):
        if sym:
            self.cells[pos] = sym
            if pos < self.lo:
                self.lo = pos
            if pos > self.hi:
                self.hi = pos
        else:
            if pos in self.cells:
                del self.cells[pos]

    def ones(self):
        return sum(self.cells.values())

    def maxrun(self):
        # longest run of consecutive 1s
        if not self.cells:
            return 0
        best = 0
        cur = 0
        for p in range(self.lo, self.hi + 1):
            if self.cells.get(p, 0) == 1:
                cur += 1
                if cur > best:
                    best = cur
            else:
                cur = 0
        return best


def run(max_steps, record_fn=None, record_every=None):
    """Simulate B5 from blank tape.
    Returns (halted, steps, tape, state, pos)."""
    tape = Tape()
    pos = 0
    state = 'A'
    for step in range(max_steps):
        sym = tape.read(pos)
        rule = RULES[state][sym]
        if rule is None:
            return True, step, tape, state, pos
        w, mv, nxt = rule
        tape.write(pos, w)
        pos += mv
        state = nxt
        if record_fn is not None and record_every and (step % record_every == 0):
            record_fn(step, tape, state, pos)
    return False, max_steps, tape, state, pos


if __name__ == '__main__':
    halted, steps, tape, state, pos = run(2_000_000)
    print("halted:", halted, "steps:", steps)
    print("state:", state, "pos:", pos, "ones:", tape.ones(), "maxrun:", tape.maxrun())
    print("lo,hi:", tape.lo, tape.hi)


# --- full-tape scan helpers (added 2026-07-16 after the lo/hi truncation bug) ---
# The FIRST version of x2b5_braid.py / _sawtooth / _invariant / _rle / _sweep
# tracked `lo` at left-record milestones but never updated `hi`, so every tape
# scan ran over range(lo, 0+1) -- the LEFT half-tape only. These helpers derive
# the extent from the cells dict itself, so no caller bookkeeping can truncate.

def extent(cells):
    """Full written extent (min,max) of the nonzero cells."""
    if not cells:
        return 0, 0
    return min(cells), max(cells)


def maxrun_full(cells):
    """Longest run of 1s over the FULL written tape."""
    if not cells:
        return 0
    lo, hi = extent(cells)
    best = cur = 0
    for p in range(lo, hi + 1):
        if cells.get(p, 0):
            cur += 1
            if cur > best:
                best = cur
        else:
            cur = 0
    return best
