#!/usr/bin/env python3
"""Generator for the TRAILING LAW chunk lemmas (TrailLaw k, X2.lean §5bf).

Mirrors X2.lean's `step` exactly.  Python is ONLY a generator: every emitted
lemma is verified by Lean's kernel `rfl` with FREE `marker`/`R` tails, so a
Python error shows up as a Lean failure, never as an unsound theorem.

The IN family is built ONLY from the Lean definitions (cascadeReg / depStack /
regenWord / zeros), transcribed here; the OUT is likewise built from the
definitions, never lifted off the run.
"""

# ---------------------------------------------------------------- definitions
def ones(n):    return [True] * n
def zeros(n):   return [False] * n
def pow01(n):   return [False, True] * n

def descCascade(d):
    if d == 0:
        return ones(1)
    return ones(2 ** (d + 2) - 3) + [False, False] + descCascade(d - 1)

def regenWord(k):
    return ones(2 ** k - 3) + [False, True, False, False, True] + pow01(2 ** (k - 1) - 2)

def depStackAux(n, a, m):
    if n == 0:
        return m
    return ones(2 ** (a + 1) - 3) + [False, True] + depStackAux(n - 1, a + 1, m)

def depStack(k, m):
    return depStackAux(k - 6, 5, m)

def cascadeReg(k, Lc, p, marker, R):
    left = pow01(Lc + (2 ** (k - 1) - 2)) + marker
    right = ([False, False, False] + ones(2 ** k - 3) + [False, False]
             + descCascade(k - 3) + [False, False] + zeros(7) + R)
    return ('E', p, left, False, right)

def termSteps(k):  return 2 ** (k + 1) + k + 5
def trailSteps(k): return 359 + termSteps(k)

# ---------------------------------------------------------------- the machine
# state, head-bit -> (new state, dpos, write, move)   move: 'R' or 'L'
RULES = {
    ('A', False): ('B',  1, True,  'R'),
    ('A', True ): ('E',  1, False, 'R'),
    ('B', False): ('C',  1, True,  'R'),
    ('B', True ): None,                     # HALT
    ('C', False): ('D', -1, False, 'L'),
    ('C', True ): ('E', -1, True,  'L'),
    ('D', False): ('E',  1, False, 'R'),
    ('D', True ): ('D', -1, True,  'L'),
    ('E', False): ('F',  1, True,  'R'),
    ('E', True ): ('C', -1, False, 'L'),
    ('F', False): ('A',  1, False, 'R'),
    ('F', True ): ('E',  1, True,  'R'),
}

class TailTouched(Exception):
    pass

def step(cfg):
    """One step.  Raises TailTouched if the head would read into the FREE tail
    (i.e. mvL on an empty left, or mvR on an empty right) -- in that case the
    concrete run does NOT represent the marker/R-free run."""
    st, pos, left, head, right = cfg
    r = RULES[(st, head)]
    if r is None:
        return None
    nst, dpos, wrbit, mv = r
    head = wrbit
    if mv == 'R':
        if not right:
            raise TailTouched('mvR on empty right')
        left = [head] + left
        head, right = right[0], right[1:]
    else:
        if not left:
            raise TailTouched('mvL on empty left')
        right = [head] + right
        head, left = left[0], left[1:]
    return (nst, pos + dpos, left, head, right)

def run(cfg, n):
    trace = [cfg]
    for _ in range(n):
        cfg = step(cfg)
        if cfg is None:
            raise RuntimeError('HALT during trailing run')
        trace.append(cfg)
    return trace

# ---------------------------------------------------------------- Lean output
def lean_list(bs):
    return '[' + ', '.join('true' if b else 'false' for b in bs) + ']'

def lean_cfg(cfg, tailL='marker', tailR='R'):
    st, pos, left, head, right = cfg
    p = str(pos) if pos >= 0 else '(' + str(pos) + ')'
    return ('⟨.%s, %s, ⟨%s ++ %s, %s, %s ++ %s⟩⟩'
            % (st, p, lean_list(left), tailL,
               'true' if head else 'false', lean_list(right), tailR))

# ---------------------------------------------------------------- driver
def build(k):
    """IN config for TrailLaw k at p = 0, with marker=[] , R=[] concrete."""
    anchor = 0 + 2 ** k - k - 44
    inn = cascadeReg(4, 1, anchor, depStack(k, regenWord(k) + []), zeros(16) + [])
    out = cascadeReg(k, 1, 0 - 2 ** k, [], [])
    return inn, out

def emit(k, bounds, prefix):
    """bounds: list of cumulative step offsets, strictly increasing, last =
    trailSteps k."""
    N = trailSteps(k)
    assert bounds[-1] == N, (bounds[-1], N)
    inn, out = build(k)
    trace = run(inn, N)
    # SOUNDNESS CHECK: the concrete run must equal the definitional OUT
    assert trace[-1] == out, 'run does NOT land on the definitional OUT'
    lines = []
    names = []
    prev = 0
    for i, b in enumerate(bounds):
        nm = '%s_%d' % (prefix, i + 1)
        names.append((nm, b - prev))
        lines.append('theorem %s (marker R : List Bool) :\n'
                     '    steps %d %s\n      = some %s := by\n  rfl\n'
                     % (nm, b - prev, lean_cfg(trace[prev]), lean_cfg(trace[b])))
        prev = b
    return lines, names, trace

def widths(trace):
    """max explicit-list widths, to gauge rfl cost"""
    return max(len(c[2]) + len(c[4]) for c in trace)

if __name__ == '__main__':
    import sys
    k = int(sys.argv[1]) if len(sys.argv) > 1 else 6
    inn, out = build(k)
    N = trailSteps(k)
    tr = run(inn, N)
    print('k =', k, ' trailSteps =', N, ' lands on definitional OUT:', tr[-1] == out)
    print('max tape width along run:', widths(tr))
    # structural landmarks: state + direction changes
    print('offset  state  pos  |left| |right|')
    for i in range(0, N + 1, 25):
        st, pos, l, h, r = tr[i]
        print('%5d  %s  %5d  %5d %5d' % (i, st, pos, len(l), len(r)))
