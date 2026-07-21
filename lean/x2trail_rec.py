#!/usr/bin/env python3
"""Exact simulator of x2, mirroring X2.lean's `step`/`steps`/word definitions.

Used ONLY for measurement.  Validated against the kernel-proven `trailLaw_6`
and `trailLaw_7` before any claim is trusted; every claim carries a control
that MUST fail.
"""

A, B, C, D, E, F = 'A', 'B', 'C', 'D', 'E', 'F'

# step table: (state, head) -> (newstate, write, dir)  dir=+1 right, -1 left
TBL = {
    (A, 0): (B, 1, +1), (A, 1): (E, 0, +1),
    (B, 0): (C, 1, +1), (B, 1): None,          # HALT
    (C, 0): (D, 0, -1), (C, 1): (E, 1, -1),
    (D, 0): (E, 0, +1), (D, 1): (D, 1, -1),
    (E, 0): (F, 1, +1), (E, 1): (C, 0, -1),
    (F, 0): (A, 0, +1), (F, 1): (E, 1, +1),
}


class Cfg:
    """left is nearest-first, exactly as in Lean."""
    __slots__ = ('st', 'pos', 'left', 'head', 'right')

    def __init__(self, st, pos, left, head, right):
        self.st, self.pos = st, pos
        self.left, self.head, self.right = list(left), head, list(right)

    def copy(self):
        return Cfg(self.st, self.pos, self.left, self.head, self.right)

    def key(self):
        return (self.st, self.pos, tuple(self.left), self.head, tuple(self.right))


def step(c):
    r = TBL[(c.st, c.head)]
    if r is None:
        return None
    ns, wr, d = r
    left, right = c.left, c.right
    if d == +1:                       # mvR (wr c.tape wr)
        if right:
            nh = right[0]
            right = right[1:]
        else:
            nh = 0
        left = [wr] + left
    else:                             # mvL
        if left:
            nh = left[0]
            left = left[1:]
            right = [wr] + right
        else:
            nh = 0
            left = []
            right = [wr] + right
    return Cfg(ns, c.pos + d, left, nh, right)


def run(c, n, trace=False):
    c = c.copy()
    tr = [c.copy()] if trace else None
    for _ in range(n):
        c = step(c)
        if c is None:
            return (None, tr)
        if trace:
            tr.append(c.copy())
    return (c, tr)


# ---------------------------------------------------------------- words
def ones(n):        return [1] * n
def zeros(n):       return [0] * n
def pow01(n):       return [0, 1] * n


def descCascade(d):
    if d == 0:
        return ones(1)
    return ones(2 ** (d + 2) - 3) + [0, 0] + descCascade(d - 1)


def cascadeReg(k, Lc, p, marker, R):
    left = pow01(Lc + (2 ** (k - 1) - 2)) + list(marker)
    right = ([0, 0, 0] + ones(2 ** k - 3) + [0, 0]
             + descCascade(k - 3) + [0, 0] + zeros(7) + list(R))
    return Cfg(E, p, left, 0, right)


def regenWord(k):
    return ones(2 ** k - 3) + [0, 1, 0, 0, 1] + pow01(2 ** (k - 1) - 2)


def depStackAux(n, a, m):
    if n == 0:
        return list(m)
    return ones(2 ** (a + 1) - 3) + [0, 1] + depStackAux(n - 1, a + 1, m)


def depStack(k, m):     return depStackAux(k - 6, 5, m)
def trailSteps(k):      return 359 + (2 ** (k + 1) + k + 5)


def trailBlocks(j):
    return [] if j == 0 else trailBlocks(j - 1) + [2 ** (5 + j - 1) - 3]


def trailCost(bs):      return sum(N + 4 for N in bs)
def trailNest(bs, L):
    return list(L) if not bs else [1] + ones(bs[0]) + [0] + trailNest(bs[1:], L)


def trailCasc(bs, R):
    return list(R) if not bs else trailCasc(bs[1:], ones(bs[0]) + [0, 0] + list(R))


# ---------------------------------------------------------------- TrailLaw
def trail_IN(k, p, marker, R):
    return cascadeReg(4, 1, p + 2 ** k - k - 44,
                      depStack(k, regenWord(k) + list(marker)), zeros(16) + list(R))


def trail_OUT(k, p, marker, R):
    return cascadeReg(k, 1, p - 2 ** k, marker, R)


def check_trail(k, p=0, marker=None, R=None):
    marker = [1, 0, 1] if marker is None else marker
    R = [1, 1, 0, 1] if R is None else R
    got, _ = run(trail_IN(k, p, marker, R), trailSteps(k))
    if got is None:
        return 'HALT'
    return got.key() == trail_OUT(k, p, marker, R).key()
