#!/usr/bin/env python3
"""x2bd_sim.py -- RAW exact-bigint simulator for the integer-x2 machine
1RB0RE_1RC---_0LD1LE_0RE1LD_1RF0LC_0RA1RE, matching lean/X2.lean `step`.

Zipper tape (left stack nearest-first, head bit, right list nearest-first),
identical to the Lean `Tape`.  Provides raw step, milestone detection, and a
config snapshotter for the doubling-phase outer-state extraction.
"""
import sys
sys.path.insert(0, '/Users/aokiyousuke/busybeaver')
from x2cc_symb import runs_concrete
from x2cc_faith import T
from x2cc_gencheck import m1_spec

# transition: (state, bit) -> (write, move(+1=R,-1=L), next, halt?)
TT = {
    ('A', 0): (1, +1, 'B'), ('A', 1): (0, +1, 'E'),
    ('B', 0): (1, +1, 'C'), ('B', 1): None,          # HALT
    ('C', 0): (0, -1, 'D'), ('C', 1): (1, -1, 'E'),
    ('D', 0): (0, +1, 'E'), ('D', 1): (1, -1, 'D'),
    ('E', 0): (1, +1, 'F'), ('E', 1): (0, -1, 'C'),
    ('F', 0): (0, +1, 'A'), ('F', 1): (1, +1, 'E'),
}


class Sim:
    __slots__ = ('L', 'h', 'R', 'st', 'pos', 'n')

    def __init__(self, right_str, state='E', pos=0):
        # right_str[0] is the head cell; rest go on R (nearest-first == same order)
        bits = [1 if ch == '1' else 0 for ch in right_str]
        self.h = bits[0]
        self.R = bits[1:][::-1]        # store reversed so pop() = nearest
        self.L = []                    # nearest-first (top of stack = nearest)
        self.st = state
        self.pos = pos
        self.n = 0

    def step(self):
        t = TT[(self.st, self.h)]
        if t is None:
            return False
        w, mv, ns = t
        self.h = w
        if mv == +1:
            self.L.append(self.h)
            self.h = self.R.pop() if self.R else 0
        else:
            self.R.append(self.h)
            self.h = self.L.pop() if self.L else 0
        self.st = ns
        self.pos += mv
        self.n += 1
        return True

    def is_milestone(self):
        # E on a 0, and no 1 anywhere to the left
        return self.st == 'E' and self.h == 0 and (1 not in self.L)

    def left_ones(self):
        return sum(self.L)

    def right_runs(self, k=12):
        """first k run-length tokens of the right tape from the head."""
        seq = [self.h] + self.R[::-1]
        runs = []
        i = 0
        while i < len(seq) and len(runs) < k:
            b = seq[i]
            j = i
            while j < len(seq) and seq[j] == b:
                j += 1
            runs.append((b, j - i))
            i = j
        return runs

    def right_bits(self):
        return [self.h] + self.R[::-1]

    def left_runs_top(self, k=8):
        """top-k run tokens of the left stack, nearest-first."""
        runs = []
        i = 0
        L = self.L
        while i < len(L) and len(runs) < k:
            b = L[-1 - i]
            j = i
            while j < len(L) and L[-1 - j] == b:
                j += 1
            runs.append((b, j - i))
            i = j
        return runs


def build(g):
    s = runs_concrete(T(m1_spec(g)), {})
    return Sim(s)


if __name__ == "__main__":
    g = int(sys.argv[1]) if len(sys.argv) > 1 else 2
    sim = build(g)
    miles = []
    # first micro to leave initial milestone
    sim.step()
    cap = 60_000_000
    while sim.n < cap:
        if sim.is_milestone():
            miles.append(sim.n)
            if len(miles) == 6:
                break
        if not sim.step():
            print("HALT at", sim.n); break
    print(f"g={g}: milestone raw steps (M2..M1(g+1)) = {miles}")
    if len(miles) >= 6:
        print(f"  M6(g) at {miles[4]}, M1(g+1) at {miles[5]}, "
              f"doubling phase length = {miles[5]-miles[4]}")
