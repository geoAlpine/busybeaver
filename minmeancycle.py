import numpy as np
# Adversarial minimum even-density: state s=c mod 2^k, action=incoming high bit in {0,1},
# transition s -> T(s + hb*2^k) mod 2^k, deterministic. Long-run freq of EVEN states, MINIMIZED over
# all action sequences = minimum mean cycle of node-evenness in the 2-out-edge graph (Karp's algorithm).
# If min-mean-cycle even-density > 1/3 => UNCONDITIONAL non-halt (any incoming bits give density>1/3).
def min_mean_cycle_evendensity(k):
    K=1<<k
    # edges: from s, two targets
    adj=[[] for _ in range(K)]
    for s in range(K):
        for hb in (0,1):
            c=s+(hb<<k); t=(3*c)//2 % K
            adj[s].append(t)
    # Karp's min mean cycle on weights w(node)=[s even]. We want min over cycles of avg of node-weight.
    # Use weight on EDGE = evenness of the SOURCE node s (freq of even states visited).
    INF=float('inf')
    # Karp: d[v][k]; here do over all start... standard Karp needs single recurrent component.
    # Simpler robust: Howard's policy iteration / or brute min-mean via binary search + Bellman-Ford on (w-lambda).
    def feasible(lmbda):
        # exists cycle with mean weight < lmbda  <=> graph has negative cycle with edge weight (w(s)-lmbda)
        d=[0.0]*K
        for _ in range(K):
            upd=False
            for s in range(K):
                ws=( (1.0 if s%2==0 else 0.0) - lmbda )
                for t in adj[s]:
                    if d[s]+ws < d[t]-1e-12:
                        d[t]=d[s]+ws; upd=True
            if not upd: break
        # detect negative cycle: one more pass
        for s in range(K):
            ws=((1.0 if s%2==0 else 0.0)-lmbda)
            for t in adj[s]:
                if d[s]+ws < d[t]-1e-12:
                    return True
        return False
    lo,hi=0.0,1.0
    for _ in range(40):
        mid=(lo+hi)/2
        if feasible(mid): hi=mid
        else: lo=mid
    return lo
for k in (4,6,8,10):
    v=min_mean_cycle_evendensity(k)
    print(f"k={k:2d}: adversarial MIN even-density = {v:.4f}   {'>1/3 => UNCONDITIONAL non-halt!' if v>1/3+1e-3 else '<=1/3 (adversary can break; need a density constraint)'}")
