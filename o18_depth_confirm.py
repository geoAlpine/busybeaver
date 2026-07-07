# o18 PREDICT-AND-CONFIRM: symbolic single-defect tower chain vs exact concrete simulation.
# For each N = 2 (mod 3): predict the FULL F-entry chain (frontier forms (m,t,e) + landing L)
# from the grid-verified transition table, THEN confirm by fresh concrete simulation.
import sys
sys.path.insert(0, '/Users/aokiyousuke/busybeaver')
from o18_depth_census import run_from_reset, Overflow

def clean_step(N):
    if N % 3 == 2:
        return ('D', (8 * N - 25) // 3, 0, 6)
    return ('C', 8 * N // 3 + 2)

def dstep(m, t, e):
    r = m % 3
    if r == 1:
        if e == 1: return ('D', (8 * m - 17) // 3, 0, 2 * t + 8)
        if e == 2: return 'EXIT'
        if e == 3: return ('D', (8 * m - 5) // 3, t + 1, 1)
        return ('D', (8 * m - 5) // 3, t + 2, e - 3)
    if r == 2:
        if t > 0: return ('D', (8 * m + 14) // 3, t - 1, e)
        return ('C', (8 * m + 3 * e + 14) // 3)
    if e % 3 == 2: return ('D', (8 * m + 8 * e + 6 * t - 19) // 3, 0, 6)
    return ('C', (8 * m + 8 * e + 6 * t + (10 if e % 3 == 1 else 12)) // 3)

def predict_chain(N, maxsteps=40):
    """Return list of frontier states [(m,t,e),...] and final ('LAND',L) or ('EXIT'/'OVER',None)."""
    chain = []
    st = clean_step(N)
    for _ in range(maxsteps):
        if st[0] == 'C':
            return chain, ('LAND', st[1])
        _, m, t, e = st
        chain.append((m, t, e))
        st = dstep(m, t, e)
        if st == 'EXIT':
            return chain, ('EXIT', None)
    return chain, ('OVER', None)

def concrete_chain(N, budget):
    status, fents, steps, unsafe = run_from_reset(N, budget, maxF=40)
    chain = []
    for (s, clean, land, R, hp, _u) in fents:
        if clean:
            return chain, ('LAND', land), unsafe, steps
        if hp != -1:
            continue  # interior meet form
        # parse 1^m 0 (10)^t 1^e
        if R[0][0] != 1: return chain, ('BADFORM', R), unsafe, steps
        m = R[0][1]
        rest = R[1:]
        if not rest or rest[0] != (0, 1): return chain, ('BADFORM', R), unsafe, steps
        rest = rest[1:]
        t = 0
        while len(rest) >= 2 and rest[0] == (1, 1) and rest[1] == (0, 1):
            t += 1; rest = rest[2:]
        if len(rest) == 1 and rest[0][0] == 1:
            chain.append((m, t, rest[0][1]))
        else:
            return chain, ('BADFORM', R), unsafe, steps
    return chain, (status, None), unsafe, steps

if __name__ == '__main__':
    grid = [int(x) for x in sys.argv[1:]] or [56, 62, 71, 80, 89, 98, 104, 107, 116, 125, 134, 143]
    allok = True
    for N in grid:
        pch, pend = predict_chain(N)
        # budget estimate: ~4*(final width)^2
        wmax = max([m for m, _, _ in pch] + [pend[1] or 0])
        budget = min(8 * wmax * wmax + 10_000_000, 400_000_000)
        try:
            cch, cend, unsafe, steps = concrete_chain(N, budget)
        except Overflow as e:
            print(f'N={N}: OVERFLOW {e}'); allok = False; continue
        ok = (pch == cch and pend == cend and unsafe == 0)
        allok &= ok
        print(f'N={N}: {"CONFIRMED" if ok else "MISMATCH"} chain={pch} end={pend} '
              f'(concrete end={cend}, steps={steps}, unsafe={unsafe})')
        if not ok:
            print(f'   concrete chain: {cch}')
        sys.stdout.flush()
    print('ALL CONFIRMED' if allok else 'SOME FAILED')
