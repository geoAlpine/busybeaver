# o18 ANNEALED MODEL — Monte Carlo arm  [MODEL: i.i.d. uniform residues; rules EXACT].
# Replaces the true residue sequence (m mod 3 per pass) with i.i.d. uniform r in {0,1,2},
# keeps the EXACT word transducer T (o18_md_rules.py).  KEY STRUCTURAL FACT: the true
# orbit is a RENEWAL process — every clean generation re-seeds the word at ((1,6),)
# (clean_step in o18_md_orbit.py), so the per-generation fatal-entry probability under
# the annealed model is a CONSTANT p* = P(excursion from ((1,6),) halts | i.i.d. residues).
# This script estimates p* by direct simulation and measures the margin-walk event rates
# (PUSH +2 / POP -1 / LAND / RECYCLE), 2-block birth margins, and danger metrics.
# NOTHING here is a proof about the real machine.  [MODEL] throughout.
import sys, random
from collections import Counter
sys.path.insert(0, '/Users/aokiyousuke/busybeaver')
from o18_md_rules import T, Unknown, units


def two_blocks(w):
    """Indices of exact (1,2) blocks."""
    return [i for i, (s, b) in enumerate(w) if s == 1 and b == 2]


def escort_margin(w, i):
    """Units (1,1) blocks immediately left of block i (the push-margin escort)."""
    m = 0
    k = i - 1
    while k >= 0 and w[k] == (1, 1):
        m += 1
        k -= 1
    return m


def classify(r, w):
    """Event label for the pass (r, w) — leading-edge taxonomy."""
    j = units(w)
    if r == 2:
        s, b = w[0]
        if s == 1 and b == 1 and len(w) > 1:
            return 'POP'          # margin -1
        if s == 1:
            return 'LAND' if len(w) == 1 else 'MERGE'
        return 'SEPDEC'
    if r == 1:
        if j == len(w):
            return 'RECYCLE'      # word renews to a single block
        s, v = w[j]
        if s >= 2:
            return 'RECMERGE'
        if v >= 3:
            return 'PUSH'         # margin +2 (prepends 2 units)
        return 'R1'               # the v=2 danger region
    return 'R0'                   # lands / decrements / delegation


def run_excursion(rng, w0, cap=100000):
    """One annealed excursion from word w0.  Returns (outcome, npass, stats)."""
    w = w0
    ev = Counter()
    births = []          # escort margins of freshly created (1,2) blocks
    min2margin = None    # min escort margin of any (1,2) block ever present
    adj2 = 0             # passes with two 2-blocks separated only by units
    prev2 = set()
    for step in range(cap):
        # danger census on the current word
        tb = two_blocks(w)
        if tb:
            mm = min(escort_margin(w, i) for i in tb)
            min2margin = mm if min2margin is None else min(min2margin, mm)
            if len(tb) >= 2:
                for a, b in zip(tb, tb[1:]):
                    if all(w[k] == (1, 1) for k in range(a + 1, b)):
                        adj2 += 1
                        break
        r = rng.randrange(3)
        ev[classify(r, w)] += 1
        try:
            res = T(r, w)
        except Unknown as u:
            return ('UNKNOWN', step + 1, ev, births, min2margin, adj2, u.args[0])
        if res[0] == 'HALT':
            return ('HALT', step + 1, ev, births, min2margin, adj2, w)
        if res[0] == 'LAND':
            return ('LAND', step + 1, ev, births, min2margin, adj2, None)
        w2 = res[2]
        # 2-birth detection: new (1,2) blocks (count increase), record escort margin
        n2, n2p = len(two_blocks(w2)), len(two_blocks(w))
        if n2 > n2p:
            for i in two_blocks(w2):
                births.append(escort_margin(w2, i))
        w = w2
    return ('CAP', cap, ev, births, min2margin, adj2, None)


def campaign(seeds, trials, seed=1, cap=100000):
    rng = random.Random(seed)
    for name, w0 in seeds:
        out = Counter()
        ev = Counter()
        births = []
        m2 = []
        adj = 0
        lens = Counter()
        surv = Counter()   # survival: # excursions alive at depth >= d (log2 buckets)
        unk = Counter()
        for _ in range(trials):
            o, n, e, b, mm, a2, x = run_excursion(rng, w0, cap)
            out[o] += 1
            ev += e
            births += b
            if mm is not None:
                m2.append(mm)
            adj += a2
            lens[min(n, 200)] += 1
            d = 1
            while d <= n:
                surv[d] += 1
                d *= 2
            if o == 'UNKNOWN':
                unk[str(x)] += 1
            if o == 'HALT':
                print(f'  !! HALT from {name}: itinerary length {n}, last word {x}')
        tot = sum(ev.values())
        print(f'SEED {name}  trials={trials}')
        print(f'  outcomes: {dict(out)}')
        print(f'  passes total={tot}  mean-excursion-len={tot/trials:.3f}')
        print(f'  event rates (per pass): ' +
              ', '.join(f'{k}={v/tot:.4f}' for k, v in sorted(ev.items())))
        a = ev['PUSH'] / tot
        bb = ev['POP'] / tot
        print(f'  margin walk: P(+2)=f_PUSH={a:.4f}  P(-1)=f_POP={bb:.4f}  '
              f'drift/pass=+{2*a - bb:.4f}')
        if births:
            c = Counter(births)
            print(f'  2-births: {len(births)} (rate {len(births)/tot:.2e}/pass); '
                  f'escort margin at birth: min={min(births)} mean={sum(births)/len(births):.2f} '
                  f'dist={dict(sorted(c.items())[:10])}')
        else:
            print('  2-births: NONE')
        if m2:
            c = Counter(m2)
            print(f'  min 2-margin per excursion (when a 2 exists): min={min(m2)} '
                  f'dist={dict(sorted(c.items())[:10])}   adjacent-2 passes: {adj}')
        else:
            print(f'  no (1,2) block ever appeared;  adjacent-2 passes: {adj}')
        print('  survival P(len>=d): ' +
              ', '.join(f'{d}:{surv[d]/trials:.2e}' for d in sorted(surv) if surv[d] > 0))
        for k, v in unk.items():
            print(f'  UNKNOWN cell {k}: {v}')
        print()


if __name__ == '__main__':
    seed = int(sys.argv[1]) if len(sys.argv) > 1 else 1
    trials = int(sys.argv[2]) if len(sys.argv) > 2 else 200000
    # the renewal seed (every clean generation) + the exit-cone shapes + danger-adjacent
    seeds = [('GEN [1,6] (the renewal word)', ((1, 6),))]
    for t in (1, 2, 5, 8, 20):
        seeds.append((f'EXIT [2t+2,6] t={t}', ((1, 2 * t + 2), (1, 6))))
    seeds.append(('EXIT [4,1,1,1]', ((1, 4), (1, 1), (1, 1), (1, 1))))
    # a lone 2 with a big tail block (the beam-search danger peak), margins 0..6
    for M in (0, 1, 2, 4, 6):
        seeds.append((f'DANGER 1^{M}[2][9]', ((1, 1),) * M + ((1, 2), (1, 9))))
    campaign(seeds, trials, seed)
