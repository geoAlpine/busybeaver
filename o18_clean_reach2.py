# o18 CLEANUP task 2b addendum (2026-07-08): apples-to-apples base-vs-ext census on ONE
# visited set.  The plain re-run (o18_clean_reach.py) gives 362 ext-HALT cells vs the base
# run's 491 -- but both closures are budget-capped at 3M states and explore different
# frontiers, so the raw counts are not directly comparable.  Here: do the T_ext adversarial
# closure from the exit cone (same caps/budget) and, FOR EVERY VISITED (r,w) CELL, evaluate
# BOTH transducers.  Census:
#   HALT/HALT      -- genuine fatal cells (both agree)
#   baseHALT/extMOVE  -- base false-HALT cells inside the adversarially visited region
#                        (the corrected family, if reachable)
#   baseUNK/extDEF -- cells only T_ext defines
#   any other disagreement -- would be NEW (flag loudly)
import sys, pickle
sys.path.insert(0, '/Users/aokiyousuke/busybeaver')
from o18_md_rules import T, Unknown
from o18_md_rules_ext import T_ext
from collections import deque, Counter

SCR = '/private/tmp/claude-502/-Users-aokiyousuke-busybeaver/8b7a3f39-ce4e-4044-afe8-60ce3b3aedcf/scratchpad'

def kind(TT, r, w):
    try:
        res = TT(r, w)
    except Unknown:
        return ('UNK',), None
    return res, (res[2] if res[0] == 'MOVE' else None)

if __name__ == '__main__':
    maxlen, maxb, maxs, maxstates = 14, 60, 6, 3_000_000
    starts = [((1, 2 * t + 2), (1, 6)) for t in range(1, 12)]
    starts.append(((1, 4), (1, 1), (1, 1), (1, 1)))
    for t in range(0, 9):
        for e in range(1, 25):
            starts.append(((1, 1),) * t + ((1, e),))
    seen = set(starts)
    q = deque(starts)
    cen = Counter()
    false_halt_cells, other_disag = [], []
    while q and len(seen) < maxstates:
        w = q.popleft()
        for r in (0, 1, 2):
            e, w2 = kind(T_ext, r, w)
            b, _ = kind(T, r, w)
            if b[0] == e[0] == 'MOVE' and b != e:
                other_disag.append((r, w, b, e))
                cen[('MOVE-DISAGREE',)] += 1
            else:
                cen[(b[0], e[0])] += 1
            if b[0] == 'HALT' and e[0] != 'HALT':
                false_halt_cells.append((r, w, e))
            if e[0] == 'HALT' and b[0] not in ('HALT', 'UNK'):
                other_disag.append((r, w, b, e))
            if e[0] != 'MOVE':
                continue
            if len(w2) > maxlen or any(bb > maxb or ss > maxs for ss, bb in w2):
                continue
            if w2 not in seen:
                seen.add(w2)
                q.append(w2)
    print(f'visited words: {len(seen)} (queue remaining {len(q)})')
    print('census over all visited (r,w) cells  [key = (base kind, ext kind)]:')
    for k, v in sorted(cen.items(), key=lambda kv: -kv[1]):
        print(f'   {k}: {v}')
    print(f'base false-HALT cells in the ext-visited region (baseHALT, ext non-HALT): '
          f'{len(false_halt_cells)}')
    for c in false_halt_cells[:10]:
        print('   FALSE-HALT cell: r=%d %s -> ext %s' % (c[0], c[1], str(c[2])[:70]))
    print(f'other base-vs-ext disagreements (non-false-HALT shaped): {len(other_disag)}')
    for c in other_disag[:10]:
        print('   OTHER:', c)
    with open(SCR + '/o18_clean_reach2_census.pkl', 'wb') as f:
        pickle.dump({'census': dict(cen), 'false_halts': false_halt_cells,
                     'other': other_disag[:200], 'nseen': len(seen)}, f)
