# o18 TRUE-ORBIT continuation through the multi-defect regime.
# The single-defect symbolic orbit (o18_depth_symbolic.py) exits the D(m,t,e) family at
# tower-step 8394 (m ~ 10^3577) from (t=5, e=2).  This script re-runs the symbolic orbit
# with the COMPLETE word transducer T (o18_md_rules.py), so the orbit can be continued
# exactly (big ints) past the exit.  Also: standalone symbolic iteration of exit-product
# words at small/medium m with predict-and-confirm hooks.
# Every step depends only on (m mod 3, w) [grid: zero splits]; m' = (8m+c)/3 exact.
# CAVEAT (honest): validity at astronomical m is [OBSERVED/exact-fit], not certified.
import sys
sys.set_int_max_str_digits(2_000_000)
sys.path.insert(0, '/Users/aokiyousuke/busybeaver')
from o18_md_rules import T, Unknown

def clean_step(N):
    if N % 3 == 2:
        return ('D', (8 * N - 25) // 3, ((1, 1),) * 0 + ((1, 6),))
    return ('C', (8 * N) // 3 + 2)

def run_symbolic(N0, max_steps, watch=None):
    """Iterate clean/dirty transitions. Returns dict with outcome + stats."""
    state = ('C', N0)
    from collections import Counter
    use = Counter()
    maxlen = 0
    maxsep = 0
    exits = 0
    biggest2train = 0
    step = 0
    hist = []
    try:
        for step in range(max_steps):
            if state[0] == 'C':
                N = state[1]
                use['clean'] += 1
                state = clean_step(N)
            else:
                _, m, w = state
                maxlen = max(maxlen, len(w))
                maxsep = max(maxsep, max(s for s, _ in w))
                if len(w) >= 2:
                    exits = max(exits, 1)
                # track 2-trains (adjacent (1,2) blocks) anywhere in the word
                run = 0
                for s, b in w:
                    if s == 1 and b == 2:
                        run += 1
                        biggest2train = max(biggest2train, run)
                    else:
                        run = 0
                res = T(m % 3, w)
                use[res[0] + f'/r{m % 3}'] += 1
                if res[0] == 'HALT':
                    return dict(outcome='HALT', step=step, m=m, w=w, use=use,
                                maxlen=maxlen, maxsep=maxsep, twotrain=biggest2train)
                if res[0] == 'LAND':
                    state = ('C', (8 * m + res[1]) // 3)
                else:
                    state = ('D', (8 * m + res[1]) // 3, res[2])
            if watch and step >= watch[0] and step < watch[1]:
                s = state
                hist.append((step, s[0], (s[1] if s[1] < 10**24 else f'~1e{len(str(s[1])) - 1}'),
                             s[2] if s[0] == 'D' else None))
    except Unknown as u:
        return dict(outcome='UNKNOWN', step=step, cell=u.args[0], state=state, use=use,
                    maxlen=maxlen, maxsep=maxsep, twotrain=biggest2train, hist=hist)
    return dict(outcome='BUDGET', step=max_steps, state_kind=state[0],
                m_digits=len(str(state[1])), use=use, maxlen=maxlen, maxsep=maxsep,
                twotrain=biggest2train, hist=hist)

if __name__ == '__main__':
    mode = sys.argv[1] if len(sys.argv) > 1 else 'orbit'
    if mode == 'orbit':
        # the true orbit from N=10, far past the single-defect exit at tower-step 8394
        budget = int(sys.argv[2]) if len(sys.argv) > 2 else 100000
        r = run_symbolic(10, budget)
        print('TRUE ORBIT from N=10:')
        for k, v in r.items():
            if k == 'use':
                print('  use:', dict(sorted(v.items())))
            elif k == 'hist':
                for h in v:
                    print('   ', h)
            else:
                print(f'  {k}: {v}')
    elif mode == 'mc':
        # Monte Carlo: random large m (random 3-adic itineraries), exit-product start words
        import random
        random.seed(int(sys.argv[2]) if len(sys.argv) > 2 else 7)
        trials = int(sys.argv[3]) if len(sys.argv) > 3 else 200
        outcomes = {}
        for i in range(trials):
            m = random.randrange(10**40, 10**41)
            m = m - (m % 3) + 1  # exit cell has m' = (8m-17)/3 from m=1 mod 3; take m'=1 mod 3 too, vary below
            m += random.choice([0, 1, 2])
            t = random.choice([1, 2, 3, 5, 8])
            w0 = ((1, 2 * t + 2), (1, 6)) if random.random() < 0.8 else ((1, 4), (1, 1), (1, 1), (1, 1))
            st = ('D', m, w0)
            res = None
            for step in range(3000):
                _, mm, ww = st
                try:
                    r = T(mm % 3, ww)
                except Unknown as u:
                    res = ('UNKNOWN', step, u.args[0]); break
                if r[0] == 'HALT':
                    res = ('HALT', step, ww); break
                if r[0] == 'LAND':
                    res = ('LAND', step, None); break
                st = ('D', (8 * mm + r[1]) // 3, r[2])
            else:
                res = ('BUDGET', 3000, None)
            outcomes.setdefault(res[0], []).append((i, res[1], res[2]))
        for k, v in sorted(outcomes.items()):
            print(f'{k}: {len(v)}')
            for item in v[:8]:
                if k in ('HALT', 'UNKNOWN'):
                    print('   ', item)
