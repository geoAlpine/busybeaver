# o18: EXACT realizability search for a halting itinerary from the exit-product family.
# State after k passes is determined by m0 mod 3^k (the pass sequence fixes the affine
# maps).  DFS over ternary digits of m0: node = (k, x = m0 mod 3^k, m_k as affine a + b*h
# where m0 = x + 3^k * h ... ) -- implemented directly: m_k is an exact affine function
# of h:  m_k = A_k + B_k * h  with A_k, B_k rationals that stay integral on the branch.
# Choosing the next digit d in {0,1,2} refines h = d + 3*h', giving m_k mod 3 and the
# next word.  Prune on LAND (that branch is safe).  Any HALT leaf = concrete witness
# class m0 = x (mod 3^k); smallest positive representative + verification hook.
import sys
from fractions import Fraction
sys.path.insert(0, '/Users/aokiyousuke/busybeaver')
from o18_md_rules import T, Unknown

def search(w0, maxdepth=42, floor_digits=0):
    """DFS.  m0 = x + 3^k * h, h >= 0 unknown.  m_k = A + B*h exact (A,B integers on branch).
    Start: m0 = h (x=0, k=0): A=0, B=1.  At each node, m_k mod 3 = (A + B*h) mod 3; branch
    on h mod 3 = d: h = d + 3h': residue r = (A + B*d) % 3, new m_k expr A+B*d + 3B*h'.
    Then apply pass: m_{k+1} = (8*m_k + c)/3 = (8A+8Bd+8*3B h' + c)/3 -- integrality is
    guaranteed by the machine (T's c makes 8m+c divisible by 3 when m%3=r)."""
    results = []
    nodes = [((0, 1), (Fraction(0), Fraction(1)), w0, ())]  # (x,3^k) unused-x; (A,B); word; digits
    # we store (x, p3) with m0 ≡ x (mod p3)
    stack = [((0, 1), (Fraction(0), Fraction(1)), w0, ())]
    nvisited = 0
    while stack:
        (x, p3), (A, B), w, digs = stack.pop()
        nvisited += 1
        if len(digs) >= maxdepth:
            results.append(('DEEP', x, p3, w, digs))
            continue
        for d in (0, 1, 2):
            A2 = A + B * d
            B2 = B * 3
            r = int(A2 % 3)
            try:
                res = T(r, w)
            except Unknown as u:
                results.append(('UNKNOWN', x + p3 * d if p3 > 1 else d, p3 * 3, w, digs + (d,), u.args[0]))
                continue
            x2 = x + (p3 * d if True else 0)
            if res[0] == 'HALT':
                results.append(('HALT', x2, p3 * 3, w, digs + (d,)))
                continue
            if res[0] == 'LAND':
                continue  # safe branch, prune
            A3 = (8 * A2 + res[1]) / 3
            B3 = Fraction(8 * B2, 3)
            stack.append(((x2, p3 * 3), (A3, B3), res[2], digs + (d,)))
    return results, nvisited

if __name__ == '__main__':
    starts = [((1, 4), (1, 6)), ((1, 6), (1, 6)), ((1, 8), (1, 6)), ((1, 10), (1, 6)),
              ((1, 12), (1, 6)), ((1, 14), (1, 6)), ((1, 4), (1, 1), (1, 1), (1, 1))]
    md = int(sys.argv[1]) if len(sys.argv) > 1 else 30
    grand = []
    for w0 in starts:
        results, nv = search(w0, maxdepth=md)
        kinds = {}
        for res in results:
            kinds[res[0]] = kinds.get(res[0], 0) + 1
        print(f'start {w0}: visited {nv} nodes, outcomes {kinds}')
        for res in results:
            if res[0] in ('HALT', 'UNKNOWN'):
                grand.append((w0, res))
    print()
    if not grand:
        print('NO halting/unknown itinerary exists to this depth: every branch LANDS.')
    for w0, res in grand[:20]:
        print('WITNESS-CLASS', w0, res[0], 'm0 ≡', res[1], 'mod', res[2], 'digits', res[4] if len(res) > 4 else res[3])
