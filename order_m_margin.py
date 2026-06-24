import numpy as np, itertools
# Adversarial MIN output even-density restricted to order-m Markov incoming sources.
# order-m source: incoming bit depends on last m incoming bits (2^m contexts), adversary picks P(1|context).
# Augmented chain state = (low-bits s in Z/2^k, last m incoming bits). Minimize stationary even-density.
def min_even_order(m, k=7, restarts=40, iters=300):
    K=1<<k; M=1<<m
    best=1.0
    rng_seeds=range(restarts)
    for rs in rng_seeds:
        # deterministic 'random' init varying by rs (no Math.random allowed conceptually; use structured)
        probs=np.array([(rs*7+ctx*13)%11/10.0*0.0 + ((ctx>>0)&1) for ctx in range(M)],dtype=float)
        # start from a structured guess: P(1|ctx) pushing toward keeping odd; do coordinate descent
        probs=np.array([ (0.5+0.4*np.cos(rs+ctx)) for ctx in range(M)])
        probs=np.clip(probs,0.02,0.98)
        def even_density(pr):
            # build augmented transition
            S=K*M
            P=np.zeros((S,S))
            for s in range(K):
                for ctx in range(M):
                    p1=pr[ctx]
                    for hb,w in ((1,p1),(0,1-p1)):
                        c=s+(hb<<k); cp=(3*c)//2 % K
                        nctx=((ctx<<1)|hb)&(M-1)
                        P[s*M+ctx, cp*M+nctx]+=w
            w,v=np.linalg.eig(P.T); i=np.argmin(np.abs(w-1)); st=np.real(v[:,i]); 
            if st.sum()==0: return 1.0
            st=st/st.sum()
            return sum(st[s*M+ctx] for s in range(K) for ctx in range(M) if s%2==0)
        # coordinate descent
        cur=even_density(probs)
        for it in range(iters):
            ctx=it%M
            bestp=probs[ctx]; bestv=cur
            for cand in (0.02,0.2,0.4,0.5,0.6,0.8,0.98):
                probs[ctx]=cand; v=even_density(probs)
                if v<bestv: bestv=v; bestp=cand
            probs[ctx]=bestp; cur=bestv
        best=min(best,cur)
    return best
for m in (1,2,3,4):
    v=min_even_order(m, k=6, restarts=8, iters=80)
    print(f"order m={m}: adversarial MIN even-density = {v:.4f}   {'> 1/3 (cannot break)' if v>1/3+0.005 else '<= 1/3 (breaks at this order)'}")
