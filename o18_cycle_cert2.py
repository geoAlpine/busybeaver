# o18 LIVE-TAPE cycle certificates: for every level-1 sweep chunk of a real generation,
# verify config(t+p) = shift_D(config(t)) (state equal, head displaced D, radius-6 window equal)
# for EVERY cycle inside the sweep. This is the o3_bouncer_macro certificate standard:
# state-return + word-repeat on the live tape => by determinism+locality the sweep is a
# translation-invariant lemma of its live context; grid-identical skeletons lift it to the class.
import sys
sys.path.insert(0, '/Users/aokiyousuke/busybeaver')
from o18_template_scan import M, compress

names = "ABCDEF"
RAD = 6

def run_epoch_hist(N):
    pad = 6 * N + 256
    tape = bytearray(pad + N + pad)
    p0 = pad
    for i in range(1, N):
        tape[p0 + i] = 1
    pos, st = p0, 5
    toks = bytearray()
    hist = []  # (state, pos, window)
    steps = 0
    first = True
    while steps < 40 * N * N // 10 + 100000:
        r = tape[pos]
        if st == 5 and not first:
            break
        first = False
        hist.append((st, pos, bytes(tape[pos - RAD:pos + RAD + 1])))
        toks.append(st * 2 + r)
        w, d, ns = M[st][r]
        tape[pos] = w
        pos += d
        st = ns
        steps += 1
    return toks, hist

def certify(N, verbose=False):
    toks, hist = run_epoch_hist(N)
    ch = compress(toks)
    i = 0  # token index
    results = {}
    for c in ch:
        if c[0] == 'R':
            unit, k = bytes(c[1]), c[2]
            p = len(unit)
            ok = True
            D = hist[i + p][1] - hist[i][1] if i + p < len(hist) else None
            MARGIN = 3  # boundary cycles see the sweep ends inside the window; they belong to episodes
            for cyc in range(MARGIN, k - 1 - MARGIN):
                a = i + cyc * p
                b = a + p
                if b >= len(hist):
                    break
                s1, p1, w1 = hist[a]
                s2, p2, w2 = hist[b]
                if s2 != s1 or p2 - p1 != D or w1 != w2:
                    ok = False
                    if verbose:
                        print(f"    divergence in [{''.join(names[x//2]+str(x%2) for x in unit)}] cycle {cyc}")
                    break
            key = (unit, D)
            st_, cnt = results.get(key, (True, 0))
            results[key] = (st_ and ok, cnt + (k - 1))
            i += p * k
        else:
            i += 1
    return results

grid = [int(x) for x in sys.argv[1:]] or [59, 60, 61, 62, 300, 301, 302]
for N in grid:
    res = certify(N)
    line = f"N={N}: "
    for (unit, D), (ok, cnt) in sorted(res.items(), key=str):
        nm = ''.join(names[x // 2] + str(x % 2) for x in unit)
        line += f"[{nm}] D={D:+d} {cnt} cycles {'CERT' if ok else 'FAIL'};  "
    print(line)
