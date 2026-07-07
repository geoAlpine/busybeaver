# o18 ANNEALED MODEL — exact-mass dynamic-programming arm  [MODEL: i.i.d. uniform
# residues; rules EXACT].  Probability-weighted BFS over word shapes under the exact
# transducer T: at each depth every live word branches into r=0,1,2 with mass 1/3 each.
# Because the true orbit renews the word at ((1,6),) every clean generation, the
# per-generation fatal-entry probability is the constant
#     p* = halt-mass of the excursion tree rooted at ((1,6),).
# This DP computes p* with EXPLICIT error accounting: halt_mass (exact, from reached
# HALT cells) + an upper bound halt <= halt_mass + pruned + unknown + live-at-cap.
# Also: ruin probabilities from margin-M danger seeds (the push-margin walk), and the
# analytic skip-free ruin root eta from the measured walk rates.  [MODEL] throughout.
import sys
sys.path.insert(0, '/Users/aokiyousuke/busybeaver')
from o18_md_rules import T, Unknown


def danger0(w):
    """(gap-0 adjacency, gap-0 precursor): w contains (1,2)(1,2) directly adjacent /
    (1,v>2, v=2 mod 3) directly followed by (1,2) — the only entrances to the fatal
    R1 recursion (kill_bfs shows units-GAPPED double-2s are harmless)."""
    a0 = p0 = False
    for (s1, b1), (s2, b2) in zip(w, w[1:]):
        if s1 == 1 and s2 == 1 and b2 == 2 and b1 % 3 == 2:
            if b1 == 2:
                a0 = True
            else:
                p0 = True
    return a0, p0


def danger(w):
    """(has_adjacent_2s, min_2_margin_or_None, has_precursor).
    adjacent 2s = two (1,2) blocks separated only by units; precursor = a (1,v) with
    v>2, v=2 mod 3 separated only by units from a following (1,2) (push re-arm)."""
    idx2 = [i for i, (s, b) in enumerate(w) if s == 1 and b == 2]
    adj = prec = False
    m2 = None
    for i in idx2:
        m = 0
        k = i - 1
        while k >= 0 and w[k] == (1, 1):
            m += 1
            k -= 1
        m2 = m if m2 is None else min(m2, m)
        if k >= 0 and w[k][0] == 1 and w[k][1] % 3 == 2:
            (adj, prec) = (adj or w[k][1] == 2, prec or w[k][1] > 2)
        # also look right: (1,2) then units then (1,v=2 mod 3)
        k = i + 1
        while k < len(w) and w[k] == (1, 1):
            k += 1
        if k < len(w) and w[k][0] == 1 and w[k][1] % 3 == 2:
            (adj, prec) = (adj or w[k][1] == 2, prec or w[k][1] > 2)
    return adj, m2, prec


def dp(w0, maxdepth=60, prune=1e-24, maxstates=250000, verbose=True):
    cur = {w0: 1.0}
    halt = land = unk = pruned = 0.0
    adjmass = precmass = lowmass = 0.0   # expected #passes spent in danger states
    adj0mass = prec0mass = 0.0           # gap-0 (true fatal-entrance) occupancy
    first_halt_depth = None
    for d in range(1, maxdepth + 1):
        nxt = {}
        for w, p in cur.items():
            for r in range(3):
                q = p / 3.0
                try:
                    res = T(r, w)
                except Unknown:
                    unk += q
                    continue
                if res[0] == 'HALT':
                    halt += q
                    if first_halt_depth is None:
                        first_halt_depth = d
                elif res[0] == 'LAND':
                    land += q
                else:
                    w2 = res[2]
                    nxt[w2] = nxt.get(w2, 0.0) + q
        # prune
        if len(nxt) > maxstates:
            items = sorted(nxt.items(), key=lambda kv: -kv[1])[:maxstates]
            keep = dict(items)
            pruned += sum(nxt.values()) - sum(keep.values())
            nxt = keep
        drop = [w for w, p in nxt.items() if p < prune]
        for w in drop:
            pruned += nxt.pop(w)
        cur = nxt
        for w, p in cur.items():
            a, m2, pr = danger(w)
            if a:
                adjmass += p
            if pr:
                precmass += p
            if m2 is not None and m2 <= 1:
                lowmass += p
            a0, p0 = danger0(w)
            if a0:
                adj0mass += p
            if p0:
                prec0mass += p
        if not cur:
            break
    live = sum(cur.values())
    if verbose:
        print(f'  depth<= {d}: halt={halt:.6e} (first at depth {first_halt_depth}), '
              f'land={land:.9f}, unknown={unk:.3e}')
        print(f'  error budget: pruned={pruned:.3e}  live-at-cap={live:.3e}  '
              f'=> p_halt in [{halt:.3e}, {halt + pruned + unk + live:.3e}]')
        print(f'  danger occupancy (expected passes): adjacent-2s={adjmass:.3e}  '
              f'precursor(v=2mod3 near 2)={precmass:.3e}  2-at-margin<=1={lowmass:.3e}')
        print(f'  gap-0 fatal entrances: [2][2] adjacency={adj0mass:.3e}  '
              f'(1,v=2mod3>2)(1,2) precursor={prec0mass:.3e}')
    return dict(halt=halt, land=land, unk=unk, pruned=pruned, live=live,
                adjmass=adjmass, precmass=precmass, lowmass=lowmass,
                adj0mass=adj0mass, prec0mass=prec0mass, depth=d)


def eta_root(a, b, c):
    """Skip-free-down ruin root: steps +2 w.p. a, -1 w.p. b, 0 w.p. c, safe-absorb w.p.
    1-a-b-c.  eta solves eta = b + c*eta + a*eta^3, smallest root in (0,1]."""
    lo, hi = 0.0, 1.0
    f = lambda x: b + c * x + a * x ** 3 - x
    # f(0)=b>0, find smallest root by bisection on decreasing segment
    x = 0.0
    for _ in range(200):
        mid = (lo + hi) / 2
        if f(mid) > 0:
            lo = mid
        else:
            hi = mid
    return (lo + hi) / 2


if __name__ == '__main__':
    md = int(sys.argv[1]) if len(sys.argv) > 1 else 60
    print('=== p* from the RENEWAL seed ((1,6),) — the per-generation fatal-entry '
          'probability [MODEL] ===')
    dp(((1, 6),), maxdepth=md)
    print()
    print('=== exit-cone seeds ===')
    for t in (1, 5):
        print(f'seed [2t+2,6] t={t}:')
        dp(((1, 2 * t + 2), (1, 6)), maxdepth=md)
    print('seed [4,1,1,1]:')
    dp(((1, 4), (1, 1), (1, 1), (1, 1)), maxdepth=md)
    print()
    print('=== POSITIVE CONTROL: true precursor seeds (the model CAN halt) ===')
    for M in range(0, 9):
        w0 = ((1, 1),) * M + ((1, 5), (1, 2))
        r = dp(w0, maxdepth=md, verbose=False)
        print(f'  seed 1^{M} (1,5)(1,2):  ruin(M={M}) = {r["halt"]:.6e}   '
              f'(+err<={r["pruned"] + r["unk"] + r["live"]:.1e})')
    print()
    print('=== bare fatal family 1^M [2,2]: exact ruin recursion check ===')
    for M in range(0, 9):
        w0 = ((1, 1),) * M + ((1, 2), (1, 2))
        r = dp(w0, maxdepth=md, verbose=False)
        print(f'  seed 1^M [2,2] M={M}:  ruin = {r["halt"]:.6e}   '
              f'vs (4/9)*(1/3)^(M-1) = {(4/9) * 3.0 ** (1 - M) if M >= 1 else 1/3:.6e}')
    print()
    print('=== analytic ruin root from measured walk rates (o18_ann_mc GEN seed) ===')
    # GEN-seed measured per-pass rates: f_PUSH=0.291 (+2), f_POP=0.132 (-1); the rest
    # of the non-absorbing rates keep the margin (approx c = MERGE+R0-move share).
    for (a, b, c, tag) in [(0.291, 0.132, 0.135, 'GEN-seed empirical'),
                           (1 / 3, 1 / 3, 0.0, 'push/pop symmetric (worst case)'),
                           (0.205, 0.279, 0.20, 'DANGER-seed empirical (drained)')]:
        e = eta_root(a, b, c)
        print(f'  {tag}: a={a:.3f} b={b:.3f} c={c:.3f}  drift/pass=+{2*a-b:.3f}  '
              f'eta={e:.4f}  ruin from M=10: {e**10:.2e}  M=20: {e**20:.2e}')
