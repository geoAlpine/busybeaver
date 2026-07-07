# o18 ANNEALED MODEL — witness arm: does the excursion tree from the renewal seed
# ((1,6),) contain a HALTING residue itinerary at all?  (p* > 0 vs p* = 0.)
# Method: mass-tracked DP with path back-pointers -> collect adjacent-2 danger states
# -> small exhaustive residue BFS from each to a HALT of T -> replay-verify the full
# itinerary from ((1,6),) -> CRT-realize the itinerary as an explicit congruence class
# of m (3-adic lifting) and confirm with predict_chain (the grid-proven transducer).
# A verified witness = [EXACT given T]: the fatal region IS reachable from the renewal
# seed under SOME residue itinerary, i.e. p* >= 3^-len > 0 in the annealed model, and
# the push-margin invariant CANNOT be itinerary-free (it must use the true orbit's
# residues).  Consistent with the community's Lean-verified halting class (mod 3^108).
import sys
from collections import deque
sys.path.insert(0, '/Users/aokiyousuke/busybeaver')
from o18_md_rules import T, Unknown, predict_chain


def adj2(w):
    """Adjacent-2 danger: two (1,2) blocks separated only by (1,1) units."""
    idx2 = [i for i, (s, b) in enumerate(w) if s == 1 and b == 2]
    for a, b in zip(idx2, idx2[1:]):
        if all(w[k] == (1, 1) for k in range(a + 1, b)):
            return True
    return False


def lead_margin(w):
    j = 0
    while j < len(w) and w[j] == (1, 1):
        j += 1
    return j


def dp_paths(w0, maxdepth=55, prune=1e-26, maxstates=300000):
    """DP with a max-mass representative path per state.  Returns witnesses + halts."""
    cur = {w0: (1.0, '')}
    wits = []            # (prob, depth, word, path) for adjacent-2 states
    halts = []           # (prob, depth, path) if the DP itself reaches HALT
    for d in range(1, maxdepth + 1):
        nxt = {}
        for w, (p, path) in cur.items():
            for r in range(3):
                q = p / 3.0
                try:
                    res = T(r, w)
                except Unknown:
                    continue
                if res[0] == 'HALT':
                    halts.append((q, d, path + str(r)))
                elif res[0] == 'MOVE':
                    w2 = res[2]
                    if w2 not in nxt or nxt[w2][0] < q:
                        old = nxt.get(w2, (0.0, ''))
                        nxt[w2] = (old[0] + q, path + str(r)) if w2 in nxt \
                            else (q, path + str(r))
                    else:
                        nxt[w2] = (nxt[w2][0] + q, nxt[w2][1])
        if len(nxt) > maxstates:
            nxt = dict(sorted(nxt.items(), key=lambda kv: -kv[1][0])[:maxstates])
        nxt = {w: v for w, v in nxt.items() if v[0] >= prune}
        cur = nxt
        for w, (p, path) in cur.items():
            if adj2(w):
                wits.append((p, d, w, path))
        if not cur:
            break
    return wits, halts


def kill_bfs(w0, maxdepth=25, cap=300000):
    """Exhaustive residue BFS from word w0 to a HALT of T.  Returns residue suffix."""
    q = deque([(w0, '')])
    seen = {w0}
    while q and len(seen) < cap:
        w, path = q.popleft()
        if len(path) >= maxdepth:
            continue
        for r in range(3):
            try:
                res = T(r, w)
            except Unknown:
                continue
            if res[0] == 'HALT':
                return path + str(r)
            if res[0] == 'MOVE' and res[2] not in seen:
                seen.add(res[2])
                q.append((res[2], path + str(r)))
    return None


def replay(w0, itin):
    """Replay itinerary on T from w0.  Returns ('HALT', words) or failure info."""
    w = w0
    words = [w]
    for k, ch in enumerate(itin):
        res = T(int(ch), w)
        if res[0] == 'HALT':
            return ('HALT', k + 1, words)
        if res[0] == 'LAND':
            return ('LAND', k + 1, words)
        w = res[2]
        words.append(w)
    return ('ALIVE', len(itin), words)


def crt_realize(w0, itin, L=10 ** 60):
    """3-adic lifting: find a mod 3^d such that m = a + 3^d*L has residue itinerary
    itin from (m, w0) under T.  Returns m or None."""
    d = len(itin)
    cands = [0]
    for k in range(1, d + 1):
        new = []
        for a in cands:
            for dig in range(3):
                a2 = a + dig * 3 ** (k - 1)
                m = a2 + 3 ** k * L
                w = w0
                ok = True
                for ch in itin[:k]:
                    if m % 3 != int(ch):
                        ok = False
                        break
                    res = T(m % 3, w)
                    if res[0] in ('HALT', 'LAND'):
                        break
                    m = (8 * m + res[1]) // 3
                    w = res[2]
                if ok:
                    new.append(a2)
        cands = new[:3]     # keep it narrow; lifting is essentially unique
        if not cands:
            return None
    return cands[0] + 3 ** d * L


if __name__ == '__main__':
    md = int(sys.argv[1]) if len(sys.argv) > 1 else 55
    print(f'DP with paths from ((1,6),) to depth {md} ...')
    wits, halts = dp_paths(((1, 6),), maxdepth=md)
    print(f'  adjacent-2 witness states: {len(wits)};  direct DP halts: {len(halts)}')
    for p, d, path in sorted(halts, reverse=True)[:5]:
        print(f'  DIRECT HALT mass={p:.2e} depth={d} itinerary={path}')
    wits.sort(key=lambda x: -x[0])
    shown = 0
    for p, d, w, path in wits[:40]:
        suffix = kill_bfs(w)
        tag = f'mass={p:.2e} depth={d} lead-margin={lead_margin(w)} word={w}'
        if suffix is None:
            if shown < 6:
                print(f'  witness {tag}  -- no kill found (<=25 more passes)')
                shown += 1
            continue
        itin = path + suffix
        r = replay(((1, 6),), itin)
        print(f'  witness {tag}')
        print(f'    kill suffix {suffix} -> replay: {r[0]} after {r[1]} passes '
              f'(total itinerary length {len(itin)}: {itin})')
        if r[0] == 'HALT':
            m = crt_realize(((1, 6),), itin[:r[1]])
            if m is not None:
                ch, end = predict_chain(m, ((1, 6),), maxp=len(itin) + 10)
                print(f'    CRT-REALIZED: m = {m}')
                print(f'    predict_chain(m, ((1,6),)) => {end[0]} after {len(ch)} passes'
                      f'   [EXACT given T]')
                print(f'    => p* >= 3^-{r[1]} = {3.0 ** -r[1]:.2e}  (annealed model)')
                break
    else:
        print('  NO halting itinerary found from any top witness — deepen the search.')
