import numpy as np
# Self-consistency operator Phi: input parity-process (order-1 Markov: even-density E, lag-1 corr rho)
# -> feed as incoming bits to the low-bit renewal chain -> output parity-process (E', rho').
# Self-consistent processes = FIXED POINTS of Phi. Find them; check if any has E<=1/3.
k=10; K=1<<k
def step_state(s, hb):
    c=s+(hb<<k); return (3*c)//2 % K
def Phi(E, rho, T=400000, seed_bits=None):
    # input Markov: states even(0)/odd(1) for the INCOMING bit (1=odd). P(odd)=1-E. corr=rho.
    qodd=1-E
    # 2-state chain with stationary P(odd)=qodd and lag-1 corr rho: 
    # P(odd|odd)=qodd+rho*(1-qodd); P(odd|even)=qodd-rho*qodd  (so corr=rho)
    p_oo=qodd+rho*(1-qodd); p_oe=qodd-rho*qodd
    p_oo=min(max(p_oo,0),1); p_oe=min(max(p_oe,0),1)
    s=1; last_in=1; outs=[]; ins=[]
    # deterministic pseudo-random via a fixed LCG (Math.random not allowed; reproducible)
    x=12345+int(E*1e6)+int(rho*1e6)
    def rnd():
        nonlocal x; x=(1103515245*x+12345)&0x7fffffff; return x/0x7fffffff
    for n in range(T):
        # generate incoming bit from Markov
        thr=p_oo if last_in==1 else p_oe
        hb=1 if rnd()<thr else 0
        ins.append(hb); last_in=hb
        outs.append(s&1)   # output parity = low bit
        s=step_state(s,hb)
    outs=np.array(outs[1000:]); 
    Eo=1-outs.mean()   # output even-density
    # output lag-1 corr
    o=outs.astype(float); m=o.mean(); 
    rho_o=np.mean((o[:-1]-m)*(o[1:]-m))/ (o.var()+1e-12)
    return Eo, rho_o
print("iterate Phi from various starting processes (E,rho) -> converge to fixed point:")
for (E0,r0) in [(0.5,0.0),(0.2,0.0),(0.3,0.5),(0.34,-0.5),(0.15,0.8),(0.4,-0.8)]:
    E,r=E0,r0
    for _ in range(8):
        E,r=Phi(E,r)
    print(f"  start (E={E0:.2f}, rho={r0:+.2f}) -> fixed point (E={E:.4f}, rho={r:+.4f})  {'<=1/3!' if E<=1/3 else ''}")
print("\n=> if ALL converge to (E~0.5, rho~0): the ONLY self-consistent parity process is Bernoulli(1/2),")
print("   so the real orbit (a self-consistent fixed point) must have even-density 1/2 > 1/3 => NON-HALT.")
print("   (the remaining gap: is the real orbit's process REALLY a fixed point of Phi, & is Phi's basin all?)")
