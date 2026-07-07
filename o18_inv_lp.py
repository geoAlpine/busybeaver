# o18 INVARIANT SYNTHESIS: the requested LINEAR-POTENTIAL LP, run for the record.
# After o18_inv_witness_verify.py the outcome is entailed (any inductive residue-oblivious
# invariant is impossible), but we run the LP anyway to exhibit HOW the linear class fails
# and which transitions form the irreducible infeasible core.
#
# Setup: features f(w) = (lead units, total units, #blocks, #exact-2 blocks, #tail exact-2,
#         #blocks ≡2 mod 3, min escort before first ≡2 block (capped), total block value,
#         total separator excess).  Potential Φ = a·f + a0.
# Inductive-safety conditions we test for LP feasibility (θ = 0 wlog):
#   (S)  Φ(w') >= Φ(w)          for every transition on the WITNESS PATH  (monotone form)
#   (E)  Φ(exit-cone samples) >= 1
#   (F)  Φ(fatal-cell samples) <= -1
# Any Φ certifying safety in the standard "sublevel-set invariant" sense must satisfy a
# relaxation of (S)+(E)+(F) along the path; the LP shows even the relaxation is infeasible,
# and scipy's certificate identifies the breaking transitions.
import sys
sys.path.insert(0, '/Users/aokiyousuke/busybeaver')
import numpy as np
from scipy.optimize import linprog
from o18_md_rules import T
from o18_inv_attractor import units_split
from o18_inv_anatomy import get_witness_path

def feats(w):
    seq = units_split(w)
    blocks = [x for x in seq if x[0] != 'U']
    lead = seq[0][1] if seq and seq[0][0] == 'U' else 0
    tot_units = sum(n for k, n in seq if k == 'U')
    n2 = sum(1 for s, b in blocks if b == 2)
    tail2 = sum(1 for s, b in blocks[1:] if b == 2)
    m2 = sum(1 for s, b in blocks if b % 3 == 2 and b >= 2)
    # escort before first ≡2-mod-3 block
    esc = 30
    run = 0
    for k, x in enumerate(seq):
        if x[0] == 'U':
            run += x[1]
        else:
            s, b = x
            if b % 3 == 2 and b >= 2:
                esc = min(run, 30); break
    totv = sum(b for s, b in blocks)
    seps = sum(s - 1 for s, b in blocks)
    return np.array([lead, tot_units, len(blocks), n2, tail2, m2, esc, totv, seps, 1.0])

if __name__ == '__main__':
    starts = [((1, 2 * t + 2), (1, 6)) for t in range(1, 12)]
    starts.append(((1, 4), (1, 1), (1, 1), (1, 1)))
    words, residues = get_witness_path()
    F = [feats(w) for w in words]
    nf = len(F[0])
    A_ub, rows = [], []
    # (S): a·f(w_{k+1}) >= a·f(w_k)   ->  a·(f_k - f_{k+1}) <= 0
    for k in range(len(words) - 1):
        A_ub.append(F[k] - F[k + 1]); rows.append(('S', k))
    # (E): a·f(exit) >= 1  ->  -a·f <= -1
    for w in starts:
        A_ub.append(-feats(w)); rows.append(('E', w))
    # (F): a·f(fatal) <= -1 ; fatal = final word of the path (a genuine halting cell)
    A_ub.append(feats(words[-1])); rows.append(('F', words[-1]))
    b_ub = [0.0] * (len(words) - 1) + [-1.0] * len(starts) + [-1.0]
    res = linprog(c=np.zeros(nf), A_ub=np.array(A_ub), b_ub=np.array(b_ub),
                  bounds=[(-50, 50)] * nf, method='highs')
    print('LINEAR class over margin features, monotone sublevel form:')
    print('  LP status:', res.status, '-', res.message.strip())
    if res.status == 2:
        print('  INFEASIBLE  [entailed by the witness; now exhibited]')
        # find an irreducible infeasible transition set greedily
        keep = list(range(len(A_ub)))
        core = []
        Ei = [i for i, r in enumerate(rows) if r[0] != 'S']
        Si = [i for i, r in enumerate(rows) if r[0] == 'S']
        cur = set(Si)
        for i in list(cur):
            trial = sorted((cur - {i}) | set(Ei))
            r2 = linprog(c=np.zeros(nf), A_ub=np.array([A_ub[j] for j in trial]),
                         b_ub=np.array([b_ub[j] for j in trial]),
                         bounds=[(-50, 50)] * nf, method='highs')
            if r2.status == 2:
                cur.discard(i)
        print(f'  irreducible witness-transition core: {len(cur)} of {len(Si)} path transitions')
        for i in sorted(cur):
            k = rows[i][1]
            print(f'    pass {k:3d} r={residues[k]}  {words[k]}')
            print(f'        ->               {words[k+1]}')
    elif res.status == 0:
        print('  feasible?! a =', res.x, ' -- MUST fail full verification; investigate')
