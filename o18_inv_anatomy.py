# o18 INVARIANT SYNTHESIS step 1c: ANATOMY of the minimal fatal schedule.
# Tags every pass of the minimal adversarial halt path with its rule family and tracks
# the margin ledger (leading units, 2-blocks and their escorts, waiting-2 births).
# Output = the exact feature trace that any valid (itinerary-coupled) invariant must model.
import sys
sys.path.insert(0, '/Users/aokiyousuke/busybeaver')
from o18_md_rules import T, Unknown, units
from o18_inv_attractor import units_split
from o18_inv_witness_verify import depth_bfs, path_to

def rule_tag(r, w):
    j = units(w)
    if r == 2:
        if j >= 1:
            return 'POP (drain 1 unit)'
        s, b = w[0]
        if s == 1:
            return 'MERGE-2 (absorb front block %d)' % b
        return 'SEP-DEC (r=2)'
    if r == 1:
        if j == len(w):
            return 'RECYCLE (units -> [2j+6])'
        (s, v) = w[j]
        if s >= 2:
            return 'MERGE-1 s=%d (birth of [2j+6(+v)] block)' % s
        if v >= 3:
            return 'PUSH v=%d -> %d (escort +2)' % (v, v - 3)
        return 'R1 (front-2 processing, j=%d)' % j
    # r == 0
    if j == len(w):
        return 'LAND-0'
    (s, v) = w[j]
    if s == 2:
        return 'ABSORB (r=0, s=2)'
    if s >= 3:
        return 'SEP-DEC-2 (r=0)'
    return 'DELEGATE (r=0 flush, tail in branch %d)' % ((v + 2) % 3)

def features(w):
    seq = units_split(w)
    blocks = [x for x in seq if x[0] != 'U']
    lead = seq[0][1] if seq and seq[0][0] == 'U' else 0
    n2 = sum(1 for s, b in blocks if b == 2)
    tail2 = sum(1 for s, b in blocks[1:] if b == 2)
    mod2 = sum(1 for s, b in blocks if b % 3 == 2 and b >= 2)
    return lead, n2, tail2, mod2

CACHE = ('/private/tmp/claude-502/-Users-aokiyousuke-busybeaver/'
         '8b7a3f39-ce4e-4044-afe8-60ce3b3aedcf/scratchpad/witness_path.pkl')

def get_witness_path():
    import pickle, os
    if os.path.exists(CACHE):
        return pickle.load(open(CACHE, 'rb'))
    starts = [((1, 2 * t + 2), (1, 6)) for t in range(1, 12)]
    starts.append(((1, 4), (1, 1), (1, 1), (1, 1)))
    best, par, nseen = depth_bfs(starts)
    dmin, w_last, r_last = best
    path = path_to(par, w_last)
    residues = [r for r, w in path[1:]] + [r_last]
    words = [w for r, w in path]
    pickle.dump((words, residues), open(CACHE, 'wb'))
    return words, residues

if __name__ == '__main__':
    words, residues = get_witness_path()
    dmin = len(residues)
    print(f'minimal fatal schedule: {len(residues)} passes (universe len<=14, b<=60, s<=6)')
    print(f'{"pass":>4} {"r":>2}  {"lead":>4} {"#2s":>3} {"tail2":>5} {"~2mod3":>6}  rule')
    from collections import Counter
    tags = Counter()
    for i, w in enumerate(words):
        r = residues[i] if i < len(residues) else None
        lead, n2, tail2, mod2 = features(w)
        tag = rule_tag(r, w) if r is not None else 'FATAL'
        tags[tag.split(' ')[0]] += 1
        print(f'{i:4d} {r if r is not None else "-":>2}  {lead:4d} {n2:3d} {tail2:5d} {mod2:6d}  {tag}   w={w}')
    print('\nrule census on the schedule:', dict(tags))
    print('\nresidue string:', ''.join(str(r) for r in residues))
