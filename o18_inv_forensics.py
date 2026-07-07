# o18 INVARIANT SYNTHESIS step 1: FAILURE FORENSICS on the adversarial abstract BFS
# (o18_md_closure.py).  For every abstract HALT path found by the BFS we replay the
# path EXACTLY (concrete words, exact transducer T, the trace's residue choices) and
# classify it:
#   REAL       -- every step of the abstract path is glued by identity
#                 (w_exact == concretize(abstract(w_exact)) throughout) and the final
#                 cell exactly HALTs: a genuine adversarial-residue counterexample to
#                 any pure-word invariant.
#   GLUE-JUMP  -- the path passes through a state where concretize(abstract(.)) is NOT
#                 the identity (a unit-train of length >= 10 snapped to 7..9, or a
#                 block value >= 16 snapped to 13..15).  The BFS 'teleports' there:
#                 the remainder of the path is a path of a DIFFERENT concrete word.
#                 We record WHICH feature was snapped and by how much (the discarded
#                 margin), and whether the exact continuation of the TRUE word still
#                 halts under the same residues.
# The classification tells us exactly which feature a valid invariant must track.
import sys
sys.path.insert(0, '/Users/aokiyousuke/busybeaver')
from o18_md_rules import T, Unknown
from o18_md_closure import abstract, concretize, bfs

def starts_list():
    starts = []
    for a in [4, 6, 8, 10, 12, 13, 14, 15]:
        starts.append(((1, a), (1, 6)))
    starts.append(((1, 4), (1, 1), (1, 1), (1, 1)))
    for t in list(range(0, 10)):
        for e in range(1, 16):
            starts.append(((1, 1),) * t + ((1, e),))
    return starts

def trace_of(parents, a):
    path = []
    while a is not None:
        pr = parents.get(a)
        if pr is None:
            path.append((None, a)); break
        path.append((pr[1], a))
        a = pr[0]
    return list(reversed(path))

def snap_report(w):
    """List (index, kind, true, snapped) for every element changed by concretize(abstract(.))."""
    aw = abstract(w)
    cw = concretize(aw)
    if cw == w:
        return []
    # element-wise diff on the ABSTRACT segmentation
    out = []
    i = 0  # position in w
    for seg in aw:
        if seg[0] == 'U':
            n_true = 0
            while i < len(w) and w[i] == (1, 1):
                n_true += 1; i += 1
            n_snap = seg[1] if isinstance(seg[1], int) else {'J0': 9, 'J1': 7, 'J2': 8}[seg[1]]
            if n_snap != n_true:
                out.append(('UNIT-TRAIN', n_true, n_snap, n_true - n_snap))
        else:
            s, b = w[i]; i += 1
            b_snap = seg[1] if isinstance(seg[1], int) else {'B0': 15, 'B1': 13, 'B2': 14}[seg[1]]
            if b_snap != b:
                out.append(('BLOCK', b, b_snap, b - b_snap))
    return out

def replay(trace):
    """Replay a fatal trace exactly.  trace = [(None, a0), (r1, a1), ...] + final (r_f, HALT).
    Returns dict with classification."""
    root = trace[0][1]
    w = concretize(root)          # roots are starts: concretize is identity on them
    assert abstract(w) == root
    jumps = []
    for k in range(1, len(trace)):
        r, a_next = trace[k]
        res = T(r, w)
        if res[0] != 'MOVE':
            return {'class': 'EXACT-DIVERGES', 'step': k, 'got': res[0], 'jumps': jumps}
        w2 = res[2]
        if abstract(w2) != a_next:
            return {'class': 'ABSTRACT-MISMATCH', 'step': k, 'jumps': jumps}
        sn = snap_report(w2)
        if sn:
            jumps.append((k, sn, w2))
        # BFS continues from concretize(a_next): follow the BFS (snapped) word,
        # but remember the true word for the fork analysis below.
        w = concretize(a_next)
    return {'class': ('REAL' if not jumps else 'GLUE-JUMP'), 'jumps': jumps, 'final_word': w}

def exact_continuation(w, residues, maxsteps=200):
    """Run exact T under a residue sequence; returns ('HALT',k)/('LAND',k)/('ALIVE',)/('UNKNOWN',k)."""
    for k, r in enumerate(residues):
        try:
            res = T(r, w)
        except Unknown:
            return ('UNKNOWN', k, w)
        if res[0] == 'HALT':
            return ('HALT', k, w)
        if res[0] == 'LAND':
            return ('LAND', k, w)
        w = res[2]
    return ('ALIVE', len(residues), w)

if __name__ == '__main__':
    maxstates = int(sys.argv[1]) if len(sys.argv) > 1 else 200000
    seen, fatal, caps, parents, nland = bfs(starts_list(), maxstates=maxstates)
    halts = [f for f in fatal if f[0] == 'HALT']
    unks = [f for f in fatal if f[0] == 'UNKNOWN']
    print(f'closure: {len(seen)} abstract states (cap {maxstates}); '
          f'fatal: {len(halts)} HALT, {len(unks)} UNKNOWN; caps {len(caps)}')
    print('=' * 90)
    from collections import Counter
    cls_count = Counter()
    for idx, f in enumerate(halts):
        tr = trace_of(parents, f[2])
        r_final = f[1]
        rep = replay(tr)
        cls_count[rep['class']] += 1
        print(f'\nHALT path #{idx}: len {len(tr)} steps, final residue {r_final}, class = {rep["class"]}')
        print(f'  root: {tr[0][1]}')
        print(f'  final abstract: {tr[-1][1]}')
        if rep['class'] in ('REAL', 'GLUE-JUMP'):
            # confirm the final exact halt on the BFS word
            wf = rep['final_word']
            res = T(r_final, wf)
            print(f'  BFS final word {wf} at r={r_final} -> {res[0]} (expect HALT)')
        for (k, sn, w2) in rep.get('jumps', []):
            print(f'  GLUE-JUMP at step {k}: true word {w2}')
            for item in sn:
                print(f'      {item[0]}: true {item[1]} snapped to {item[2]} (discarded {item[3]:+d})')
            # what happens to the TRUE word under the remaining residues?
            rest = [tr[i][0] for i in range(k + 1, len(tr))] + [f[1]]
            cont = exact_continuation(w2, rest)
            print(f'      TRUE continuation under same residues: {cont[0]} at step {cont[1]}')
    print('\n' + '=' * 90)
    print('classification summary:', dict(cls_count))
