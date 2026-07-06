#!/usr/bin/env python
# RED TEAM attacks 1-3 on the BODY lemma (o4_body_proof.py).
#  (1) LOCALITY: are all EPISODE steps at bounded, k-independent offsets from a zone edge?
#      (fit episode-step absolute positions affine in k; check offsets from left edge / right cap)
#  (2) SEGMENTATION: rerun compress with thresholds 6, 10, 12; episode-run lengths; skeleton stability.
#  (3) CONE EDGE: k=15, 17 (below claimed K0=19) and even k=18, 20 -- does the template hold/fail?
import sys
sys.path.insert(0, '/Users/aokiyousuke/busybeaver')
from o4_body_proof import M, build_B, run_trace

def compress_t(trace, thresh):
    out=[]; i=0; n=len(trace)
    while i<n:
        j=i
        while j+2<n and trace[j+2]==trace[j]: j+=1
        L=j+2-i
        if L>=thresh and trace[i]!=trace[i+1]:
            cyc=(trace[i],trace[i+1])
            take=L-(L%2)
            out.append(('SWEEP',cyc,take)); i+=take
        else:
            out.append(('E',trace[i])); i+=1
    return out

def skeleton_t(comp):
    skel=[]; lens=[]
    for e in comp:
        if e[0]=='SWEEP': skel.append(('SWEEP',e[1])); lens.append(e[2])
        else: skel.append(e)
    return skel,lens

ks=[19,21,23,25,27,49,101,251]

print("=========== (2) threshold sensitivity of compress ===========")
traces={}
for k in ks:
    r=run_trace(k); assert r['ok']; traces[k]=r['trace']
for th in (6,8,10,12):
    skels={k:skeleton_t(compress_t(traces[k],th)) for k in ks}
    base=skels[ks[0]][0]
    same=all(skels[k][0]==base for k in ks)
    nsweep=sum(1 for e in base if e[0]=='SWEEP')
    neps=len(base)-nsweep
    # affine check
    n_s=len(skels[ks[0]][1]); aff=True
    for i in range(n_s):
        y0=skels[ks[0]][1][i]; y1=skels[ks[1]][1][i]
        b=(y1-y0)//(ks[1]-ks[0]); a=y0-b*ks[0]
        if any(skels[k][1][i]!=a+b*k for k in ks): aff=False
    print(f"  thresh={th:>2}: skeleton identical across k: {same}  episodes={neps} sweeps={nsweep}  sweep-lens affine: {aff}")

print("\n=========== (1) episode-step positions vs zone edges ===========")
# replay trace to get positions; mark which steps belong to sweeps (thresh=8 canonical)
def positions_of(trace):
    pos=0; out=[]
    for (st,r,w,d) in trace:
        out.append(pos); pos+=d
    return out

ep_offsets={}
for k in ks:
    tr=traces[k]; posl=positions_of(tr)
    comp=compress_t(tr,8)
    idx=0; ep_pos=[]; sweep_ends=[]
    for e in comp:
        if e[0]=='SWEEP':
            sweep_ends.append((posl[idx], posl[idx+e[2]-1])); idx+=e[2]
        else:
            ep_pos.append((posl[idx], tr[idx])); idx+=1
    # landmarks: left edge = 0 (initial zone start), right cap at 2k..2k+3 (the 1001)
    L=0; Rcap=2*k+3
    rel=[(p, p-L, p-Rcap, t) for (p,t) in ep_pos]
    ep_offsets[k]=rel
    print(f"  k={k:>3}: sweep spans={sweep_ends}")
    print(f"          episode steps (pos, pos-left0, pos-capRight, (st,r,w,d)):")
    for p,dl,dr,t in rel:
        near = f"L{dl:+d}" if abs(dl)<=abs(dr) else f"R{dr:+d}"
        print(f"            pos={p:>4}  {near:<6} {t}")

# k-uniformity of the offset pattern: each episode step's offset from its NEAREST edge must be k-independent
pat0=[( 'L'+str(dl) if abs(dl)<=abs(dr) else 'R'+str(dr), t) for _,dl,dr,t in ep_offsets[ks[0]]]
uniform=all([('L'+str(dl) if abs(dl)<=abs(dr) else 'R'+str(dr), t) for _,dl,dr,t in ep_offsets[k]]==pat0 for k in ks)
print(f"\n  EPISODE-OFFSET PATTERN k-independent (each step pinned to an edge at fixed offset): {uniform}")
# affine fit of absolute episode positions
n_ep=len(ep_offsets[ks[0]])
allaff=True
for i in range(n_ep):
    y0=ep_offsets[ks[0]][i][0]; y1=ep_offsets[ks[1]][i][0]
    b=(y1-y0)//(ks[1]-ks[0]); a=y0-b*ks[0]
    if any(ep_offsets[k][i][0]!=a+b*k for k in ks): allaff=False; print(f"  episode {i}: NOT affine")
print(f"  episode absolute positions exactly affine in k: {allaff}")

print("\n=========== (3) cone edges: k=15,17 and even k ===========")
for k in (13,15,17,18,20,16):
    r=run_trace(k, maxsteps=200000)
    if r['ok']:
        lo,hi=r['span']
        skel,lens=skeleton_t(compress_t(r['trace'],8))
        same = skel==skeleton_t(compress_t(traces[19],8))[0]
        print(f"  k={k:>2}: reaches B(k+2) in {r['steps']} steps, span=[{lo},{hi}], unsafe={r['unsafe']}, skeleton==k19: {same}")
    else:
        print(f"  k={k:>2}: FAILS (halt={r.get('halt')}, steps={r['steps']}, span={r['span']}, unsafe={r['unsafe']})")
