#!/usr/bin/env python3
"""
hc_census.py -- HOLDOUT sweep, PASS 3: the SPECIES CENSUS over all 1104.
Merges PASS-1 dynamics (growth exponent a, block B/N, gate) with the PASS-2 width-multiplier
probe (hc_classify), in parallel (fork). Produces:
  - the growth-band distribution,
  - the block-structure split (unary-counter vs digit-string vs bounded-digit),
  - for width-multiplier-VISIBLE machines, the OBSERVED nearest-rational multiplier histogram,
  - the count that yield a CLEAN (low-spread) engine-matching multiplier.
STRICT: every multiplier here is [OBSERVED, noisy width-ratio proxy] -- NOT a certified Type-I
assignment (those required per-machine hand analysis for the 17 named). Decides no halting.
"""
import sys, json, math
from fractions import Fraction
from collections import Counter, defaultdict
sys.path.insert(0, '/Users/aokiyousuke/busybeaver')
import hc_classify as HC

HOLD = '/Users/aokiyousuke/busybeaver/_bbdata/bb6_holdouts_1104.txt'
SCR = '/private/tmp/claude-502/-Users-aokiyousuke-busybeaver/8b7a3f39-ce4e-4044-afe8-60ce3b3aedcf/scratchpad'

SIMPLE = [Fraction(p, q) for q in range(1, 7) for p in range(q + 1, 4 * q + 1)
          if math.gcd(p, q) == 1 and 1.05 <= p / q <= 3.6]
SIMPLE = sorted(set(SIMPLE), key=float)
KNOWN = {Fraction(3, 2), Fraction(4, 3), Fraction(8, 3), Fraction(5, 2)}


def nearest_rational(x, tol=0.03):
    if x is None:
        return None, None
    best = None; bd = tol
    for f in SIMPLE:
        d = abs(x - float(f))
        if d < bd:
            bd = d; best = f
    return best, bd


def work(args):
    i, sp, cap = args
    c = HC.classify(sp, cap)
    if c.get('key') is None:
        return dict(spec=sp, key=None, out=c.get('out'))
    return dict(spec=sp, key=c['key'], n=c['n'], growth=c['growth'],
                r_time=c['r_time'], s_time=c['s_time'],
                r_wid=c['r_wid'], s_wid=c['s_wid'], out=c['out'])


def band(a):
    if a is None:
        return 'flat/short'
    if a < 0.12:
        return 'bounded~cycler'
    if a < 0.40:
        return 'sub-sqrt'
    if a < 0.62:
        return 'sqrt-t'
    if a < 0.85:
        return 'inter'
    if a < 1.15:
        return 'linear'
    return 'super-lin'


if __name__ == "__main__":
    import multiprocessing as mp
    cap = int(sys.argv[1]) if len(sys.argv) > 1 else 2_000_000
    specs = [l.strip() for l in open(HOLD) if l.strip()]
    sim = {r['spec']: r for r in json.load(open(f'{SCR}/hc_sim_rows.json'))}
    args = [(i, sp, cap) for i, sp in enumerate(specs)]
    ctx = mp.get_context('fork')
    with ctx.Pool(8) as pool:
        cls = pool.map(work, args, chunksize=8)
    clsd = {c['spec']: c for c in cls}

    rows = []
    for sp in specs:
        s = sim[sp]; c = clsd[sp]
        rw = c.get('r_wid'); sw = c.get('s_wid')
        frac, err = nearest_rational(rw)
        # width-visible = the best growing milestone shows growing width (unary-ish counter)
        if rw is None:
            mult_class = 'no-milestone'
        elif 0.96 <= rw <= 1.07:
            mult_class = 'digit-string (width~const; p/q hidden)'
        elif frac is not None and sw is not None and sw < 0.06:
            mult_class = f'width-mult {frac}' + (' [known]' if frac in KNOWN else '')
        elif rw > 1.07:
            mult_class = 'width-grows (noisy/unmatched mult)'
        else:
            mult_class = 'other'
        # block class
        B = s.get('B') or 0; N = s.get('N') or 0; Bmid = s.get('Bmid')
        grew = (Bmid is not None and B > Bmid + 2)
        if B <= 6 and not grew:
            blk = 'bounded-digit'
        elif N <= 4:
            blk = 'unary/scalar'
        elif N >= 8:
            blk = 'digit-string'
        else:
            blk = 'mixed'
        rows.append(dict(spec=sp, a=s.get('a'), band=band(s.get('a')), blk=blk,
                         B=B, N=N, rw=rw, sw=sw, frac=str(frac) if frac else None,
                         mult_class=mult_class, growth=c.get('growth')))
    json.dump(rows, open(f'{SCR}/hc_census_rows.json', 'w'))

    print(f"=== SPECIES CENSUS over 1104 (cap={cap}) ===\n")
    print("[A] growth-exponent band:")
    for k, v in Counter(r['band'] for r in rows).most_common():
        print(f"    {k:16}: {v}")
    print("\n[B] block structure:")
    for k, v in Counter(r['blk'] for r in rows).most_common():
        print(f"    {k:16}: {v}")
    print("\n[C] multiplier class (width-ratio probe):")
    mc = Counter(r['mult_class'] for r in rows)
    for k, v in mc.most_common():
        print(f"    {k:42}: {v}")
    print("\n[D] OBSERVED nearest-rational multiplier histogram (width-visible only):")
    fh = Counter(r['frac'] for r in rows if r['frac'] and r['mult_class'].startswith('width-mult'))
    for k, v in sorted(fh.items(), key=lambda kv: -kv[1]):
        tag = ' [KNOWN ENGINE]' if Fraction(k) in KNOWN else ''
        print(f"    x{k:8}: {v}{tag}")
    nclean = sum(1 for r in rows if r['mult_class'].startswith('width-mult'))
    nknown = sum(1 for r in rows if '[known]' in r['mult_class'])
    print(f"\n  clean width-multiplier extracted : {nclean}/1104")
    print(f"  of which a KNOWN engine (3/2,4/3,8/3,5/2): {nknown}")
    print(f"  digit-string (p/q hidden from width)    : {mc.get('digit-string (width~const; p/q hidden)',0)}")
    print(f"  width-grows but multiplier noisy/unmatched: {mc.get('width-grows (noisy/unmatched mult)',0)}")
    print(f"\nrows -> {SCR}/hc_census_rows.json")
