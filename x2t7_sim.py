"""T7 (h_doub forall g) measurement: faithful re-implementation of lean/X2.lean `step`.

Tape zipper: left (nearest-LAST in this repr), head, right (nearest-LAST).
Lean's List is nearest-FIRST; we store reversed so pop()/append() are O(1).
"""
import sys

A, B, C, D, E, F = 0, 1, 2, 3, 4, 5
SNAMES = "ABCDEF"


class Cfg:
    __slots__ = ("st", "pos", "L", "h", "R")

    def __init__(self, st, pos, left, head, right):
        # left/right given nearest-first (Lean order); stored reversed
        self.st = st
        self.pos = pos
        self.L = list(reversed(left))
        self.h = head
        self.R = list(reversed(right))

    def lean_left(self):
        return list(reversed(self.L))

    def lean_right(self):
        return list(reversed(self.R))

    def key(self):
        return (self.st, self.pos, tuple(self.L), self.h, tuple(self.R))

    def __eq__(self, o):
        return self.key() == o.key()

    def show(self, w=60):
        l = self.lean_left()[:w][::-1]
        r = self.lean_right()[:w]
        s = lambda xs: "".join("1" if b else "0" for b in xs)
        return f"{SNAMES[self.st]}@{self.pos} ...{s(l)}[{'1' if self.h else '0'}]{s(r)}..."


def mvR(c):
    c.L.append(c.h)
    c.h = c.R.pop() if c.R else False


def mvL(c):
    nh = c.L.pop() if c.L else False
    c.R.append(c.h)
    c.h = nh


def step(c):
    """Mutates c. Returns False iff HALT (B reading 1)."""
    st, h = c.st, c.h
    if st == A:
        if not h:
            c.h = True; c.st = B; c.pos += 1; mvR(c)
        else:
            c.h = False; c.st = E; c.pos += 1; mvR(c)
    elif st == B:
        if not h:
            c.h = True; c.st = C; c.pos += 1; mvR(c)
        else:
            return False
    elif st == C:
        if not h:
            c.h = False; c.st = D; c.pos -= 1; mvL(c)
        else:
            c.h = True; c.st = E; c.pos -= 1; mvL(c)
    elif st == D:
        if not h:
            c.h = False; c.st = E; c.pos += 1; mvR(c)
        else:
            c.h = True; c.st = D; c.pos -= 1; mvL(c)
    elif st == E:
        if not h:
            c.h = True; c.st = F; c.pos += 1; mvR(c)
        else:
            c.h = False; c.st = C; c.pos -= 1; mvL(c)
    else:  # F
        if not h:
            c.h = False; c.st = A; c.pos += 1; mvR(c)
        else:
            c.h = True; c.st = E; c.pos += 1; mvR(c)
    return True


# ---------- tape word constructors (mirror X2.lean) ----------
def zeros(n): return [False] * n
def ones(n): return [True] * n
def pow10(j): return [True, False] * j
def pow01(j): return [False, True] * j
def uUnits(k): return ([True] + zeros(6)) * k
def rUnits(r): return (ones(5) + [False, False]) * r


def m1casc(n, hi, T):
    out = []
    for _ in range(n):
        out += [False, False] + ones(2 ** hi - 3)
        hi = hi - 1 if hi > 0 else 0
    return out + T


def descCascade(d):
    """Placeholder; filled from Lean def once read."""
    raise NotImplementedError


def M1(g):
    K = g + 8
    tail = ([True] + zeros(10)) if g % 2 == 0 else ([True] + zeros(4) + pow10(6))
    big = 2 ** K - 3 if g % 2 == 0 else 2 ** K - 9
    right = (zeros(21) + uUnits(g - 1) + tail + ones(big) + m1casc(g + 6, g + 7, []))
    return Cfg(E, 0, [], False, right)


def M6(g):
    K = g + 8
    r = g + 1 if g % 2 == 0 else g
    X = [True, False, False] if g % 2 == 0 else pow10(10)
    big = 2 ** K - 3 if g % 2 == 0 else 2 ** K - 13
    right = ([False] + pow10(4) + ones(9) + [False, False]
             + rUnits(r) + X + ones(big) + m1casc(g + 6, g + 7, []))
    return Cfg(E, -5, [False], False, right)


def run(c, n):
    for _ in range(n):
        if not step(c):
            return None
    return c


def run_until(c, target, limit, trace_cb=None):
    """Run c until it equals target (Cfg equality incl. pos & boundary blanks)."""
    tk = target.key()
    for i in range(1, limit + 1):
        if not step(c):
            return ("HALT", i)
        if trace_cb:
            trace_cb(i, c)
        if c.key() == tk:
            return ("HIT", i)
    return ("MISS", limit)


if __name__ == "__main__":
    # ---- VALIDATION against the two kernel-proved theorems ----
    print("=== simulator validation (must all be True) ===")
    c = M1(2); r = run(c, 343)
    print("hlow_g2  steps 343 (M1 2) = M6 2 :", r is not None and c == M6(2))
    c = M1(4); r = run(c, 419)
    print("hlow_g4  steps 419 (M1 4) = M6 4 :", r is not None and c == M6(4))
    # CONTROLS that MUST be False:
    c = M1(2); run(c, 342)
    print("CONTROL 342 (M1 2) = M6 2 (want False):", c == M6(2))
    c = M1(2); run(c, 344)
    print("CONTROL 344 (M1 2) = M6 2 (want False):", c == M6(2))
    c = M1(3); run(c, 343)
    print("CONTROL 343 (M1 3) = M6 3 (want False):", c == M6(3))
