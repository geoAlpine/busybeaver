# o18 REACHABLE-FAMILY CLOSURE under ADVERSARIAL residues.
# Question: starting from every word reachable at the single-defect exit (exit products
# [2t+2,6], [4,1,1,1], plus the whole D-family words), is the closure of the word grammar
# under T for ALL m-residues r in {0,1,2} free of HALT cells?
# If YES: o18's safety needs NO arithmetic condition on the 3-adic itinerary (the fatal
# [2,2]-cells exist in the ambient space but are unreachable from the entry).
# If NO: the escape path is printed (the exact ledger-style blocker).
#
# Abstraction (sound for the rule schema, which is uniform in large values / long trains):
#   block values: exact 1..12, else class B<r> = big with value = r (mod 3)
#     representatives: B0 -> 15, B1 -> 13, B2 -> 14  (all > 12, comparisons vs <=6 safe)
#   unit trains: exact length 0..6, else class J<r> = long with length = r (mod 3)
#     representatives: J0 -> 9, J1 -> 7, J2 -> 8
#   separators kept exact (observed <= 2 will be verified; cap 4 with report).
# Each abstract state is BFS-expanded by concretizing with representatives, applying the
# EXACT transducer T, and re-abstracting.  Soundness: every T rule depends on values only
# through (v==1 / v==2 / v==3 / v>3, v mod 3) and on train lengths only through
# (j==0 / j==1 / j>=2, j mod 3 via emitted 2j+c) -- representatives preserve all of these.
import sys
sys.path.insert(0, '/Users/aokiyousuke/busybeaver')
from o18_md_rules import T, Unknown

VREP = {'B0': 15, 'B1': 13, 'B2': 14}
JREP = {'J0': 9, 'J1': 7, 'J2': 8}

def abst_val(b):
    return b if b <= 12 else 'B%d' % (b % 3)

def conc_val(b):
    return VREP[b] if isinstance(b, str) else b

def abstract(w):
    """word (tuple of (s,b)) -> abstract form: unit trains collapsed."""
    out = []
    i = 0
    while i < len(w):
        if w[i] == (1, 1):
            j = i
            while j < len(w) and w[j] == (1, 1):
                j += 1
            n = j - i
            out.append(('U', n if n <= 6 else 'J%d' % (n % 3)))
            i = j
        else:
            s, b = w[i]
            out.append((s, abst_val(b)))
            i += 1
    return tuple(out)

def concretize(aw):
    out = []
    for x in aw:
        if x[0] == 'U':
            n = x[1] if isinstance(x[1], int) else JREP[x[1]]
            out += [(1, 1)] * n
        else:
            out.append((x[0], conc_val(x[1])))
    return tuple(out)

def bfs(starts, maxstates=200000, maxlen=16, maxsep=5):
    from collections import deque
    seen = set()
    q = deque()
    parents = {}
    fatal = []
    caps = []
    for w in starts:
        a = abstract(w)
        if a not in seen:
            seen.add(a)
            q.append(a)
            parents[a] = None
    nland = 0
    while q and len(seen) < maxstates:
        a = q.popleft()
        cw = concretize(a)
        for r in (0, 1, 2):
            try:
                res = T(r, cw)
            except Unknown as u:
                fatal.append(('UNKNOWN', r, a, u.args[0]))
                continue
            if res[0] == 'HALT':
                fatal.append(('HALT', r, a))
                continue
            if res[0] == 'LAND':
                nland += 1
                continue
            w2 = res[2]
            if len(w2) > maxlen or any(s > maxsep for s, _ in w2):
                caps.append((r, a, abstract(w2)))
                continue
            a2 = abstract(w2)
            if a2 not in seen:
                seen.add(a2)
                parents[a2] = (a, r)
                q.append(a2)
    return seen, fatal, caps, parents, nland

def trace(parents, a):
    path = []
    while a is not None:
        pr = parents.get(a)
        if pr is None:
            path.append((None, a)); break
        path.append((pr[1], a))
        a = pr[0]
    return list(reversed(path))

if __name__ == '__main__':
    starts = []
    # exit products: [2t+2, 6] for all t>=1 (values 4,6,8,10,12 + big classes), and [4,1,1,1]
    for a in [4, 6, 8, 10, 12, 13, 14, 15]:
        starts.append(((1, a), (1, 6)))
    starts.append(((1, 4), (1, 1), (1, 1), (1, 1)))
    # the D(m,t,e)-family words: 1^t (1,e), t in {0..6, J-classes via 7,8,9}, e in 1..12+B
    for t in list(range(0, 10)):
        for e in [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15]:
            starts.append(((1, 1),) * t + ((1, e),))
    seen, fatal, caps, parents, nland = bfs(starts)
    print(f'closure size (abstract states): {len(seen)}   LAND transitions: {nland}')
    print(f'cap hits (len>16 or sep>5): {len(caps)}')
    for c in caps[:10]:
        print('   CAP', c[0], '->', c[2])
    print(f'FATAL/UNKNOWN reachable: {len(fatal)}')
    for f in fatal[:12]:
        print('  ', f[0], 'residue', f[1])
        for step in trace(parents, f[2]):
            print('      ', step)
    if not fatal:
        print('NO fatal or unknown cell reachable from the entry family under ANY residue itinerary.')
