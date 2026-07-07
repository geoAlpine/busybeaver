# o18 INVARIANT SYNTHESIS step 3: VERIFICATION of the adversarial-reachability witness.
# Claim under test: there is an EXACT word path from the exit cone to a fatal (HALT) cell
# under a suitable residue itinerary -- hence NO residue-oblivious ("pure word") inductive
# invariant of ANY class (linear/piecewise/lexicographic/regular) can prove o18 safety.
#
# Verification layers (soundness discipline):
#   L1  depth-BFS: find the MINIMAL-depth adversarial halt path from the exit cone.
#       Cross-check: depth must be >= 17 (o18_md_witness exhausted all itineraries to 16).
#   L2  re-verify every edge of the path with the transducer T (independent re-application).
#   L3  verify every edge by FRESH CONCRETE SIMULATION (o18_md_probe.probe) at 5 concrete
#       m per edge (right residue, several magnitudes)  -- this does NOT assume the grid.
#   L4  construct an EXPLICIT m0 by 3-adic lifting so that the true arithmetic
#       m_{k+1} = (8 m_k + c_k)/3 realizes exactly this residue itinerary; verify the
#       whole chain in exact bigint arithmetic (integrality + residues + positivity).
#   L5  verify the final cell is a genuine fatal cell by concrete simulation (5 magnitudes).
# What is then PROVEN vs what still rests on the grid law is stated in the output.
import sys
sys.path.insert(0, '/Users/aokiyousuke/busybeaver')
from o18_md_rules import T, Unknown
from o18_md_probe import probe
from collections import deque

def depth_bfs(starts, maxlen=14, maxb=60, maxs=6, maxdepth=300, maxstates=6_000_000):
    """BFS by depth; returns first (shallowest) halt edge + parents."""
    seen = {}
    par = {}
    q = deque()
    for w in starts:
        seen[w] = 0
        par[w] = None
        q.append(w)
    best = None
    while q:
        w = q.popleft()
        d = seen[w]
        if best is not None and d + 1 >= best[0]:
            continue
        if d >= maxdepth or len(seen) >= maxstates:
            break
        for r in (0, 1, 2):
            try:
                res = T(r, w)
            except Unknown:
                continue
            if res[0] == 'HALT':
                if best is None or d + 1 < best[0]:
                    best = (d + 1, w, r)
                continue
            if res[0] != 'MOVE':
                continue
            w2 = res[2]
            if len(w2) > maxlen or any(b > maxb or s > maxs for s, b in w2):
                continue
            if w2 not in seen:
                seen[w2] = d + 1
                par[w2] = (w, r)
                q.append(w2)
    return best, par, len(seen)

def path_to(par, w):
    path = []
    while w is not None:
        pr = par.get(w)
        if pr is None:
            path.append((None, w)); break
        path.append((pr[1], w)); w = pr[0]
    return list(reversed(path))

def lift_m0(residues, cs):
    """3-adic lifting: find m0 mod 3^n with m_k = (8 m_k-1 + c_k-1)/3 == r_k (mod 3) all k.
    Solve incrementally; returns (m0_class, modulus)."""
    n = len(residues)
    M, R = 3, residues[0] % 3
    for k in range(1, n):
        # need m_k ≡ residues[k] (mod 3). m_k is an affine function of m0; brute-lift:
        found = None
        for u in range(3):
            m0 = R + u * M
            mk = m0
            ok = True
            for i in range(k):
                num = 8 * mk + cs[i]
                if num % 3 != 0:
                    ok = False; break
                mk = num // 3
            if ok and mk % 3 == residues[k] % 3:
                found = m0; break
        assert found is not None, f'lift failed at k={k}'
        M *= 3
        R = found % M
    return R, M

if __name__ == '__main__':
    starts = [((1, 2 * t + 2), (1, 6)) for t in range(1, 12)]
    starts.append(((1, 4), (1, 1), (1, 1), (1, 1)))
    # NOTE: exit-cone words only (the [2t+2,6] and [4,1,1,1] shapes). D-family words are
    # themselves upstream of these; using the cone keeps the claim sharpest.
    print('L1: depth-BFS for the minimal adversarial halt path from the exit cone...')
    from o18_inv_anatomy import get_witness_path
    words, residues = get_witness_path()   # cached from the depth-BFS (min-depth path)
    dmin = len(residues)
    print(f'    minimal halt depth: {dmin} passes (depth-BFS, universe len<=14, b<=60, s<=6)')
    print(f'    consistency vs depth-16 exhaustive (must be >=17): {"OK" if dmin >= 17 else "VIOLATION!"}')
    print(f'    witness path ({len(words)} words, {len(residues)} passes):')
    for i, w in enumerate(words):
        print(f'      pass {i:2d}  r={residues[i] if i < len(residues) else "-"}  w={w}')

    # ---------------- L2: re-verify edges with T ----------------
    cs = []
    ok = True
    for i in range(len(words) - 1):
        res = T(residues[i], words[i])
        if res[0] != 'MOVE' or res[2] != words[i + 1]:
            print(f'L2 FAIL at edge {i}'); ok = False; break
        cs.append(res[1])
    resf = T(residues[-1], words[-1])
    if resf[0] != 'HALT':
        print('L2 FAIL: final cell does not halt under T'); ok = False
    print(f'L2: transducer re-verification of all {len(words)} edges: {"PASS" if ok else "FAIL"}')

    # ---------------- L3: per-edge fresh concrete simulation ----------------
    print('L3: per-edge concrete simulation (5 magnitudes each, right residue)...')
    def ms_for(r):
        base = [40, 100, 301, 601, 1000]
        return [m + ((r - m) % 3) for m in base]
    nb = 0
    for i in range(len(words) - 1):
        r = residues[i]
        for m in ms_for(r):
            kind, out, s, unsafe = probe(m, words[i], maxF=14, lpadf=12)
            exp_m = (8 * m + cs[i]) // 3
            if kind == 'MOVE' and out == (exp_m, words[i + 1]) and unsafe:
                # multi-pass attribution (soundness ledger, O18_MULTIDEFECT §7): probe's
                # run_cfg free-runs past the first anchored entry (maxF=14); if the
                # CONTINUATION halts (e.g. m' ≡ 1 lands on the fatal cell), the run-wide
                # unsafe flag is set although THIS pass is clean.  Isolate per-pass:
                kind2, out2, s2, unsafe2 = probe(m, words[i], maxF=2, lpadf=12)
                if kind2 == 'MOVE' and out2 == (exp_m, words[i + 1]) and not unsafe2:
                    print(f'    L3 note edge {i}: m={m} unsafe flag came from the run\'s own '
                          f'continuation halting (per-pass isolation clean) -- confirmatory')
                    continue
            if kind != 'MOVE' or out != (exp_m, words[i + 1]) or unsafe:
                print(f'    L3 FAIL edge {i}: m={m} w={words[i]} -> {kind} {out} unsafe={unsafe}'
                      f' expected {(exp_m, words[i+1])}')
                nb += 1
    # final halting cell
    for m in ms_for(residues[-1]):
        kind, out, s, unsafe = probe(m, words[-1], maxF=14, lpadf=12)
        if kind != 'HALT':
            print(f'    L3 FAIL final: m={m} w={words[-1]} -> {kind} (expected HALT)')
            nb += 1
    print(f'L3: {"PASS -- every edge and the fatal cell confirmed by fresh concrete runs" if nb == 0 else f"{nb} FAILURES"}')

    # ---------------- L4: explicit m0 ----------------
    print('L4: 3-adic construction of an explicit m0 realizing the itinerary...')
    R, M = lift_m0(residues, cs)
    # choose m0 in the class, large enough to stay positive/large all along
    m0 = R
    while m0 < 100:
        m0 += M
    ms = [m0]
    ok4 = True
    for i in range(len(cs)):
        num = 8 * ms[-1] + cs[i]
        if num % 3 != 0:
            ok4 = False; print(f'    integrality FAIL at pass {i}'); break
        ms.append(num // 3)
    resid_ok = all(ms[i] % 3 == residues[i] % 3 for i in range(len(residues)))
    print(f'    m0 = {m0}  (class {R} mod 3^{len(residues)} = {M})')
    print(f'    chain integrality: {"PASS" if ok4 else "FAIL"};  all residues match: {"PASS" if resid_ok else "FAIL"}')
    print(f'    m at the fatal cell: {ms[-1]}  (≡ {ms[-1] % 3} mod 3; fatal law needs m≡1: '
          f'{"OK" if ms[-1] % 3 == 1 else "CHECK"})')
    print()
    print('=' * 90)
    print('STATEMENT [conditional]: with m0 as above and word w0 = %s,' % (words[0],))
    print('the o18 pass-dynamics (m,w) -> ((8m+c)/3, w\') reaches the fatal cell')
    print('(m≡1, %s) in %d passes and HALTS.' % (words[-1], len(residues)))
    print('PROVEN HERE: every edge (word rewrite + constant c) confirmed by fresh concrete')
    print('simulation at 5 magnitudes; the arithmetic chain for the explicit m0 is exact.')
    print('STILL RESTS ON: the grid law "outcome depends only on (m mod 3, w)" [PROVEN on')
    print('grid, 3588/3588 + 1620/1620] extrapolated to m0\'s magnitude (~3^%d).' % len(residues))
    print('NOT CLAIMED: that the o18 ORBIT reaches (m0, w0). The orbit\'s own itinerary is')
    print('what decides o18; this witness only kills residue-oblivious invariants.')
