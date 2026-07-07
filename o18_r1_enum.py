# o18 R1-PINNING step 1: exact enumeration of the adversarially-reachable Unknown cells
# of the multi-defect transducer T (o18_md_rules.py), i.e. the deep-R1 fractal cells found
# reachable by O18_INVARIANT_SYNTHESIS_2026-07-07.md (517 cells at the 3M-state budget).
# Same closure as o18_inv_reach.py (same starts, caps, budget, BFS order) so the count is
# reproducible; here we KEEP the full (r, w, tag) list + parent traces and dump to pickle.
import sys, pickle
sys.path.insert(0, '/Users/aokiyousuke/busybeaver')
from o18_md_rules import T, Unknown
from o18_inv_reach import reach, trace

OUT = sys.argv[1] if len(sys.argv) > 1 else \
    '/private/tmp/claude-502/-Users-aokiyousuke-busybeaver/8b7a3f39-ce4e-4044-afe8-60ce3b3aedcf/scratchpad/o18_r1_unknowns.pkl'

def starts_cone():
    starts = []
    for t in range(1, 12):
        starts.append(((1, 2 * t + 2), (1, 6)))
    starts.append(((1, 4), (1, 1), (1, 1), (1, 1)))
    for t in range(0, 9):
        for e in range(1, 25):
            starts.append(((1, 1),) * t + ((1, e),))
    return starts

if __name__ == '__main__':
    starts = starts_cone()
    seen, par, escapes, esc_ex, halts, unks, w2hits, nland, qrem = reach(
        starts, maxlen=14, maxb=60)
    print(f'reachable exact words: {len(seen)} (queue remaining {qrem}); LAND {nland}; '
          f'escapes {escapes}')
    print(f'HALT cells reached: {len(halts)}   Unknown cells reached: {len(unks)}')
    # classify unknown cells by raise-site tag
    from collections import Counter
    tagc = Counter()
    for r, w, tag in unks:
        tagc[tag if isinstance(tag, str) else tag[0]] += 1
    print('Unknown cells by raise-site:')
    for k, v in sorted(tagc.items(), key=lambda kv: -kv[1]):
        print(f'   {k}: {v}')
    # distinct words vs (r,word) cells
    print(f'distinct Unknown words: {len(set(w for _, w, _ in unks))}')
    with open(OUT, 'wb') as f:
        pickle.dump({'unks': unks,
                     'halts': halts,
                     'traces': {w: trace(par, w) for _, w, _ in unks}}, f)
    print(f'dumped -> {OUT}')
