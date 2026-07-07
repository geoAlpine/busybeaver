# o18 R1-PINNING verification harness for o18_md_rules_ext.py.  Three modes:
#   eq     -- EQUIVALENCE: T_ext(r,w) == T(r,w) on every random cell where T is defined
#             (pure code check, millions of cells; T_ext must be a conservative extension)
#   cells  -- probed-cell check: T_ext prediction vs the CONCRETE outcomes of
#             o18_r1_probe.py (all 517 reachable Unknown cells, 4 magnitudes each)
#             and/or o18_r1_grid.py (systematic family grids)
#   chain  -- FULL-CHAIN predict-and-confirm: symbolic chains under T_ext vs fresh
#             concrete simulation, word sampler biased into the nested-2 deep region
import sys, random, pickle
sys.path.insert(0, '/Users/aokiyousuke/busybeaver')
from o18_md_rules import T, Unknown, concrete_chain
from o18_md_rules_ext import T_ext, predict_chain_ext
from o18_md_probe import wstr

SCR = '/private/tmp/claude-502/-Users-aokiyousuke-busybeaver/8b7a3f39-ce4e-4044-afe8-60ce3b3aedcf/scratchpad'


def rand_word(rng, deep_bias):
    k = rng.randint(1, 12 if deep_bias else 6)
    w = []
    for _ in range(k):
        if deep_bias and rng.random() < 0.55:
            w.append((1, rng.choice([1, 1, 1, 2, 2, 2, 2, 5])))
        else:
            w.append((rng.choices([1, 1, 1, 2, 3], k=1)[0],
                      rng.choice([1, 1, 2, 2, 3, 4, 5, 6, 7, 9, 14])))
    return tuple(w)


def mode_eq(seed, n, max_adjudicate=60):
    """T_ext vs base T.  Disagreements are expected ONLY in the corrected region
    (base T's unsound 'inner c=-23 -> HALT at j=1'); every disagreement found is
    ADJUDICATED BY FRESH CONCRETE SIMULATION and T_ext must win all of them."""
    from o18_r1_probe import probe_cell
    rng = random.Random(seed)
    neq = nnew = nboth_unk = 0
    disags = []
    for i in range(n):
        w = rand_word(rng, deep_bias=(i % 2 == 0))
        for r in (0, 1, 2):
            try:
                a = T(r, w)
            except Unknown:
                a = None
            try:
                b = T_ext(r, w)
            except Unknown:
                b = None
            if a is not None:
                if b == a:
                    neq += 1
                else:
                    disags.append((r, w, a, b))
            elif b is not None:
                nnew += 1
            else:
                nboth_unk += 1
    print(f'EQ: {neq} cells identical; {nnew} newly-defined by T_ext; '
          f'{nboth_unk} Unknown in both; DISAGREEMENTS: {len(disags)}')
    next_ok = nbad = 0
    for r, w, a, b in disags[:max_adjudicate]:
        conc = probe_cell(r, w)
        ext_ok = (conc == b) or (conc[0] == 'HALT' and b[0] == 'HALT')
        base_ok = (conc == a) or (conc[0] == 'HALT' and a[0] == 'HALT')
        if ext_ok and not base_ok:
            next_ok += 1
        else:
            nbad += 1
            print('  ADJUDICATION FAILED', r, w, 'base=', a, 'ext=', b, 'concrete=', conc)
    print(f'adjudicated {min(len(disags), max_adjudicate)} disagreements concretely: '
          f'T_ext right & base wrong on {next_ok}; OTHER: {nbad}')
    return nbad == 0


def mode_cells(paths):
    ntot = nok = nbad = nunk = 0
    bad, unk = [], []
    for path in paths:
        with open(path, 'rb') as f:
            data = pickle.load(f)
        if 'res' in data:                      # o18_r1_probe.py dump: {(r,w): out}
            items = [(r, w, out) for (r, w), out in data['res'].items()]
        else:                                  # o18_r1_grid.py dump: {key: (w, out)}
            items = [(1, w, out) for w, out in data.values()]
        for r, w, out in items:
            if out[0] in ('SPLIT',):
                print('  concrete SPLIT (excluded from check):', r, wstr(w), out)
                continue
            ntot += 1
            try:
                pred = T_ext(r, w)
            except Unknown as u:
                nunk += 1
                if len(unk) < 8:
                    unk.append((r, w, u.args[0]))
                continue
            ok = (pred == out) or (pred[0] == out[0] == 'HALT')
            if ok:
                nok += 1
            else:
                nbad += 1
                if len(bad) < 10:
                    bad.append((r, w, out, pred))
    print(f'CELLS: {ntot} concrete-probed cells; T_ext exact on {nok}; '
          f'MISMATCH {nbad}; still-Unknown {nunk}')
    for b in bad:
        print('  BAD  r=%d w=%s concrete=%s pred=%s' % (b[0], wstr(b[1]), b[2], b[3]))
    for u in unk:
        print('  UNK ', u)
    return nbad == 0


def mode_chain(seed, nwords):
    rng = random.Random(seed)
    words = set()
    # deep-region structured seeds: nested/adjacent 2s at assorted margins
    U = lambda n: ((1, 1),) * n
    for j, p, q in [(0, 1, 1), (0, 2, 0), (0, 3, 2), (1, 1, 0), (2, 1, 1), (0, 4, 0),
                    (0, 5, 1), (1, 4, 2), (0, 2, 2), (3, 2, 1)]:
        words.add(U(j) + ((1, 2),) + U(p) + ((1, 2),) + U(q) + ((1, 2),))
        words.add(U(j) + ((1, 2),) + U(p) + ((1, 2),) + U(q) + ((1, 6),))
        words.add(U(j) + ((1, 2),) + U(p) + ((1, 2),) + U(q) + ((2, 3), (1, 4)))
    while len(words) < nwords:
        words.add(rand_word(rng, deep_bias=True))
    ms = [40, 41, 42, 100, 101, 102, 301, 302, 303]
    nok = nbad = nunk = nhalt = 0
    bad = []
    from collections import Counter
    unkc = Counter()
    for w in sorted(words):
        for m in ms:
            try:
                pch, pend = predict_chain_ext(m, w)
            except Unknown as u:
                nunk += 1
                unkc[str(u.args[0])] += 1
                continue
            cch, cend, steps, unsafe = concrete_chain(m, w)
            if pend == ('HALT',):
                nhalt += 1
            if cend[0] in ('OVERFLOW', 'MAXF', 'BUDGET'):
                ok = pch[:len(cch)] == cch and len(cch) >= 2
            else:
                ok = pch == cch and pend == cend
            if ok:
                nok += 1
            else:
                nbad += 1
                if len(bad) < 15:
                    bad.append((m, w, cch[-1] if cch else None, cend, pend))
    print(f'CHAINS CONFIRMED {nok}  MISMATCH {nbad}  UNKNOWN {nunk}  (predicted halts: {nhalt})')
    for k, v in sorted(unkc.items()):
        print(f'  UNKNOWN {k}: {v}')
    for b in bad:
        print('  BAD', b)
    return nbad == 0


if __name__ == '__main__':
    mode = sys.argv[1] if len(sys.argv) > 1 else 'eq'
    if mode == 'eq':
        mode_eq(int(sys.argv[2]) if len(sys.argv) > 2 else 1,
                int(sys.argv[3]) if len(sys.argv) > 3 else 200000)
    elif mode == 'cells':
        paths = sys.argv[2:] or [SCR + '/o18_r1_probed.pkl']
        mode_cells(paths)
    elif mode == 'chain':
        mode_chain(int(sys.argv[2]) if len(sys.argv) > 2 else 2,
                   int(sys.argv[3]) if len(sys.argv) > 3 else 220)
