# o18 INVARIANT SYNTHESIS step 2c: EXACT adversarial reachable set from the exit cone.
# Forward closure of {exit products + D-family} under T with FREE residue choice,
# exact words, inside a generous bounded universe (escapes recorded, never expanded).
# Questions:
#   (1) does Reach contain any "waiting-2" word (a (s,2) block in tail position, or a
#       first block (s,2) with s>=3 odd) -- the necessary feature of every BAD word?
#   (2) does Reach hit any HALT / Unknown cell?
#   (3) which rules create which tail blocks (the creation algebra of value-2 blocks)?
import sys
sys.path.insert(0, '/Users/aokiyousuke/busybeaver')
from o18_md_rules import T, Unknown
from o18_inv_attractor import units_split
from collections import deque

def waiting2(w):
    blocks = [x for x in units_split(w) if x[0] != 'U']
    if any(b == 2 for s, b in blocks[1:]):
        return True
    if blocks and blocks[0][1] == 2 and blocks[0][0] >= 3 and blocks[0][0] % 2 == 1:
        return True
    return False

def reach(starts, maxlen=14, maxb=60, maxs=6, maxstates=3_000_000):
    seen = set(starts)
    par = {w: None for w in starts}
    q = deque(starts)
    escapes = 0
    esc_ex = []
    halts, unks, w2hits = [], [], []
    nland = 0
    while q and len(seen) < maxstates:
        w = q.popleft()
        for r in (0, 1, 2):
            try:
                res = T(r, w)
            except Unknown as u:
                unks.append((r, w, u.args[0]))
                continue
            if res[0] == 'HALT':
                halts.append((r, w))
                continue
            if res[0] == 'LAND':
                nland += 1
                continue
            w2 = res[2]
            if len(w2) > maxlen or any(b > maxb or s > maxs for s, b in w2):
                escapes += 1
                if len(esc_ex) < 8:
                    esc_ex.append((r, w, w2))
                continue
            if w2 not in seen:
                seen.add(w2)
                par[w2] = (w, r)
                q.append(w2)
                if waiting2(w2):
                    w2hits.append((r, w, w2))
    return seen, par, escapes, esc_ex, halts, unks, w2hits, nland, len(q)

def trace(par, w):
    path = []
    while w is not None:
        pr = par.get(w)
        if pr is None:
            path.append((None, w)); break
        path.append((pr[1], w)); w = pr[0]
    return list(reversed(path))

if __name__ == '__main__':
    import itertools
    maxlen = int(sys.argv[1]) if len(sys.argv) > 1 else 14
    maxb = int(sys.argv[2]) if len(sys.argv) > 2 else 60
    starts = []
    for t in range(1, 12):
        starts.append(((1, 2 * t + 2), (1, 6)))
    starts.append(((1, 4), (1, 1), (1, 1), (1, 1)))
    for t in range(0, 9):
        for e in range(1, 25):
            starts.append(((1, 1),) * t + ((1, e),))
    seen, par, escapes, esc_ex, halts, unks, w2hits, nland, qrem = reach(
        starts, maxlen=maxlen, maxb=maxb)
    print(f'reachable exact words: {len(seen)} (queue remaining {qrem}); LAND {nland}')
    print(f'escapes (len>{maxlen} or b>{maxb} or s>6): {escapes}')
    for e in esc_ex:
        print('   ESC r=%d  %s -> %s' % (e[0], e[1], e[2]))
    print(f'HALTs reached: {len(halts)}   Unknown cells: {len(unks)}')
    for h in halts[:5]:
        print('  HALT at r=%d from %s' % h)
        for st in trace(par, h[1]):
            print('     ', st)
    for u in unks[:5]:
        print('  UNK', u)
    print(f'waiting-2 words reached: {len(w2hits)}')
    for r, w, w2 in w2hits[:10]:
        print(f'   W2 via r={r}: {w} -> {w2}')
        for st in trace(par, w):
            print('     ', st)
    # census of separator values and tail-block values reached
    from collections import Counter
    sepc = Counter()
    tailv = Counter()
    for w in seen:
        blocks = [x for x in units_split(w) if x[0] != 'U']
        for s, b in blocks:
            sepc[s] += 1
        for s, b in blocks[1:]:
            tailv[b if b <= 12 else 'big%d' % (b % 3)] += 1
    print('separator census:', dict(sepc))
    print('tail-value census:', dict(sorted(tailv.items(), key=str)))
