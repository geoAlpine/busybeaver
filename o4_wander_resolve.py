# o4 WANDER-case resolver (2026-07-07)
# The 7 unresolved Z(k, g=3, a<=1) configs from O4_LEDGER_ANALYSIS. Chunked macro runs with
# wall-clock caps + incremental output (the naive 2e9-step run stalled: wandering configs
# have few uniform sweeps, so macro jumps rarely fire and progress is ~concrete speed).
# Classification: HALT / RECOVERED (milestone) / UNRESOLVED@steps (with diagnostics:
# jump ratio, tape span, #segs -- to characterize the wandering regime).
import types, time, sys
src=open('o4_bouncer_macro.py').read()
mod=types.ModuleType('bm'); exec(compile(src.split("if __name__=='__main__':")[0],'bm','exec'), mod.__dict__)

def Z_segs(k,g,a):
    segs=[['10',k],['1',1],['0',2],['1',1],['0',g]]
    if a>0: segs.append(['10',a])
    segs += [['1',1],['0',2],['1',1]]
    return segs

def probe(k,g,a,budget_sec=240,chunk=20_000_000):
    m=mod.Mach()
    m.segs=Z_segs(k,g,a); m.abs0=0; m.habs=0; m.st='E'; m.leftmost=0
    m.merge()
    t0=time.time()
    while time.time()-t0<budget_sec:
        target=m.steps+chunk
        m.run(maxsteps=target)
        if m.halted:
            return ('HALT', m.steps, m)
        if m.milestones:
            return ('RECOVERED', m.steps, m)
    return ('UNRESOLVED', m.steps, m)

if __name__=='__main__':
    cases=[(21,0),(23,0),(27,0),(29,0),(101,0),(23,1),(41,1)]
    for k,a in cases:
        v,s,m=probe(k,3,a)
        gs=[gg for _,gg,_ in m.milestones]
        extra=''
        if v=='RECOVERED': extra=f' milestones={len(gs)} firstG={gs[0]:,}'
        if v=='UNRESOLVED': extra=f' G~{-m.leftmost:,} segs={len(m.segs)}'
        print(f'Z(k={k:>3},g=3,a={a}): {v}@{s:,}{extra}  unsafe={m.unsafe} f1={m.f1}', flush=True)
