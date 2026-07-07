# o18 MULTI-DEFECT general word prober.
# General anchored state:  0^inf [F] 1^m 0^{s_1} 1^{b_1} 0^{s_2} 1^{b_2} ... 0^{s_k} 1^{b_k} 0^inf
#   head on the cell LEFT of the leftmost 1 (hp = -1), state F.
# Encoded as (m, w) with w = tuple of (s_i, b_i), s_i >= 1 separator run, b_i >= 1 block.
# Single-defect D(m,t,e) = (m, ((1,1),)*t + ((1,e),)).  Clean C_N = (N, ()) ... [F]0 1^{N-1}.
# A PASS = anchored-F-entry to anchored-F-entry (interior meets, hp>0, are skipped).
# This script probes (m,w) -> outcome on a systematic grid and reports the law table
# keyed by (m mod 3, w) -- checking ONE outcome per key, with c = 3m'-8m the affine constant.
import sys
sys.path.insert(0, '/Users/aokiyousuke/busybeaver')
from o18_depth_map import run_cfg

def word_blocks(m, w):
    blocks = [(1, m)]
    for s, b in w:
        blocks += [(0, s), (1, b)]
    return blocks

def parse_word(R, hp):
    """RLE -> (m, ((s,b),...)) if form is 1^m (0^s 1^b)* with head at -1; else None."""
    if hp != -1 or not R or R[0][0] != 1:
        return None
    m = R[0][1]
    w = []
    i = 1
    while i < len(R):
        if R[i][0] != 0 or i + 1 >= len(R) or R[i + 1][0] != 1:
            return None
        w.append((R[i][1], R[i + 1][1]))
        i += 2
    return (m, tuple(w))

def probe(m, w, maxF=12, budget=None, lpadf=8):
    """Run (m,w) to next anchored word / clean landing. Returns (kind, out, steps, unsafe).
    HALT is reported only if it occurs BEFORE the next anchored F-entry (per-pass fatality)."""
    status, fents, steps, unsafe = run_cfg(word_blocks(m, w), maxF=maxF, budget=budget, lpadf=lpadf)
    for (s, clean, land, R, hp) in fents:
        if clean:
            return ('LAND', land, s, unsafe)
        p = parse_word(R, hp)
        if p is not None:
            return ('MOVE', p, s, unsafe)
        if hp > 0:
            continue  # interior form (head not at anchor): not a pass boundary
        return ('UNPARSED', (R, hp), s, unsafe)
    if status == 'HALT':
        return ('HALT', None, steps, unsafe)
    return (status, None, steps, unsafe)

def wstr(w):
    return '.'.join(('' if s == 1 else '0' * (s - 1) + '|') + str(b) for s, b in w)

if __name__ == '__main__':
    import itertools
    from collections import defaultdict
    # m grid: 3 magnitudes per residue class mod 3, spanning all residues mod 9
    ms = [40, 41, 42, 43, 44, 45, 46, 47, 48, 100, 101, 102, 301, 302, 303]
    words = []
    # k=1 with both separators
    for s in (1, 2):
        for b in (1, 2, 3, 4, 5, 6, 7, 8):
            words.append(((s, b),))
    # k=2: all separator patterns, block values 1..6 (+ a few larger)
    for s1, s2 in itertools.product((1, 2), (1, 2)):
        for b1 in (1, 2, 3, 4, 5, 6):
            for b2 in (1, 2, 3, 4, 6):
                words.append(((s1, b1), (s2, b2)))
    # k=3: sampled
    for s in itertools.product((1, 2), repeat=3):
        for b in [(1, 4, 6), (2, 3, 6), (3, 1, 4), (4, 6, 3), (6, 2, 5), (1, 1, 6), (5, 4, 1), (2, 2, 2)]:
            words.append(tuple(zip(s, b)))
    # k=4..5: spot shapes
    words += [((1, 1), (1, 1), (1, 4), (1, 6)), ((1, 4), (1, 1), (1, 1), (1, 1)),
              ((1, 2), (2, 3), (1, 6), (2, 1)), ((1, 6), (1, 5), (1, 4), (1, 3), (1, 2)),
              ((2, 1), (1, 3), (2, 6), (1, 1), (1, 4))]
    only = sys.argv[1] if len(sys.argv) > 1 else None
    laws = defaultdict(set)
    bad = []
    nruns = 0
    for w in words:
        if only == 'k2' and len(w) != 2: continue
        if only == 'k1' and len(w) != 1: continue
        if only == 'k3+' and len(w) < 3: continue
        for m in ms:
            kind, out, s, unsafe = probe(m, w)
            nruns += 1
            if kind == 'LAND':
                laws[(m % 3, w)].add(('LAND', 3 * out - 8 * m))
            elif kind == 'MOVE':
                m2, w2 = out
                laws[(m % 3, w)].add(('MOVE', 3 * m2 - 8 * m, w2))
            else:
                bad.append((m, w, kind, out))
            if unsafe:
                bad.append((m, w, 'UNSAFE', unsafe))
        sys.stdout.flush()
    print(f'{nruns} runs')
    splits = 0
    for key in sorted(laws, key=lambda k: (k[0], len(k[1]), k[1])):
        outs = laws[key]
        if len(outs) > 1:
            splits += 1
        tag = '' if len(outs) == 1 else '  <-- SPLIT!'
        o = sorted(outs)[0] if len(outs) == 1 else sorted(outs)
        print(f'  m%3={key[0]} w={wstr(key[1])}: {o}{tag}')
    print(f'\nsplits: {splits}')
    print('bad/unparsed/unsafe:', bad if bad else 'NONE')
