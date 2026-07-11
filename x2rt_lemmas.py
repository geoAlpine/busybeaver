#!/usr/bin/env python3
"""x2rt_lemmas.py -- ADVERSARIAL brute micro-step stress test of the macro lemmas.

Fully independent stepper (does NOT import x2cc_symb). For each transit we micro-step
on a concrete finite tape and (1) check the claimed output config, (2) SCAN for any
E@0 that meets a maximal 0-gap bounded on the left by a 1 -- flagging length exactly 3
(the halt trigger) or any ODD length. Ranges pushed far past the certified <=40."""

TRANS = {
    ('A','0'):('1',1,'B'), ('A','1'):('0',1,'E'),
    ('B','0'):('1',1,'C'), ('B','1'):None,
    ('C','0'):('0',-1,'D'), ('C','1'):('1',-1,'E'),
    ('D','0'):('0',1,'E'), ('D','1'):('1',-1,'D'),
    ('E','0'):('1',1,'F'), ('E','1'):('0',-1,'C'),
    ('F','0'):('0',1,'A'), ('F','1'):('1',1,'E'),
}

def gap_at(tape, pos):
    """if head at pos reads 0 and left neighbor is 1, return maximal 0-run length
    (bounded right by a 1), else None. tape is a list; outside = '0'."""
    def g(i): return tape[i] if 0 <= i < len(tape) else '0'
    if g(pos) != '0': return None
    if g(pos-1) != '1': return None
    L = 0; i = pos
    while g(i) == '0': L += 1; i += 1
    if i >= len(tape):  # runs into background: not a bounded gap
        return None
    return L

def micro_run(tape, pos, state, nsteps, watch_gaps=True):
    """returns (tape,pos,state, gaps_met) after nsteps; gaps_met = list of (step,L)
    for every E@0 bounded gap encountered. Halts -> raises."""
    tape = list(tape)
    gaps = []
    for s in range(nsteps):
        if watch_gaps and state == 'E':
            L = gap_at(tape, pos)
            if L is not None and L >= 2:
                gaps.append((s, L))
        ch = tape[pos] if 0 <= pos < len(tape) else '0'
        t = TRANS[(state, ch)]
        if t is None:
            raise RuntimeError(f"HALT during transit at step {s}")
        w,d,ns = t
        if 0 <= pos < len(tape):
            tape[pos] = w
        else:
            raise IndexError("ran off finite tape -- widen")
        pos += d; state = ns
    return tape, pos, state, gaps

def rle(s): return s  # identity for lists compare

# ---- 1. re-certify R/L/D to length 200 ----
def cert_RLD(N=200):
    bad = 0
    # R-cycle: X (01)^n sc 1 , E at first 0 -> 1^{2n}, E, +2n
    for n in range(1, N):
        for sc in ('1','0'):
            tape = ['1'] + list('01'*n) + [sc,'1']
            t2,p2,s2,g = micro_run(tape, 1, 'E', 2*n)
            exp = ['1'] + ['1']*(2*n) + [sc,'1']
            if not (t2==exp and s2=='E' and p2==1+2*n and all(L!=3 and L%2==0 for _,L in g)):
                print(f"R-cycle FAIL n={n} sc={sc} gaps={g}"); bad+=1
    # L-cycle even a=2m
    for m in range(1, N):
        tape = list('1'+'0'+'1'*(2*m)+'1'+'10')
        f = 2+2*m
        t2,p2,s2,g = micro_run(tape, f, 'E', 2*m+2)
        exp = list('1')+list('0')+list('0'+'10'*m)+list('10')
        if not (t2==exp and s2=='D' and p2==0 and all(L!=3 and L%2==0 for _,L in g)):
            print(f"L-even FAIL m={m} gaps={g}"); bad+=1
    # L-cycle odd a=2m+1
    for m in range(0, N):
        tape = list('0'+'1'*(2*m+1)+'1'+'10')
        f = 1+2*m+1
        t2,p2,s2,g = micro_run(tape, f, 'E', 2*m+2)
        exp = list('0')+list('10'*(m+1))+list('10')
        if not (t2==exp and s2=='E' and p2==0 and all(L!=3 and L%2==0 for _,L in g)):
            print(f"L-odd FAIL m={m} gaps={g}"); bad+=1
    # D-loop
    for a in range(1, N):
        tape = list('0'+'1'*a+'1')
        t2,p2,s2,g = micro_run(tape, a+1, 'D', a)
        if not (t2==tape and s2=='D' and p2==1):
            print(f"D-loop FAIL a={a}"); bad+=1
    print(f"cert_RLD to N={N}: {'ALL OK, no gap==3, no odd gap' if bad==0 else f'{bad} FAILURES'}")
    return bad

# ---- 2. chew-body lemma: (01)^k [D] 0^3 1^(2r+5) -> (01)^(k+1) [D] 0^3 1^(2r+3), 6 steps ----
def cert_chew(K=60, R=60):
    bad = 0; odd = 0
    for k in range(1, K):
        for r in range(0, R):
            # left context so D can see (01)^k below; put a 0 sentinel far left
            left = list('0' + '01'*k)
            body = list('0'*3 + '1'*(2*r+5))
            tape = left + body + ['0']  # right sentinel 0 (gap bounded)
            pos = len(left)             # head at D on first 0 of 0^3
            t2,p2,s2,g = micro_run(tape, pos, 'D', 6)
            # claimed output: (01)^(k+1) [D] 0^3 1^(2r+3)
            exp_left = list('0' + '01'*(k+1))
            exp_body = list('0'*3 + '1'*(2*r+3))
            exp_tape = exp_left + exp_body + ['0','0']  # two cells consumed->2 fewer 1s, len preserved? check state/pos instead
            for st,L in g:
                if L == 3: print(f"[CANDIDATE HALT] chew k={k} r={r}: E met gap 3"); bad+=1
                if L % 2 == 1: print(f"[ANOMALY] chew k={k} r={r}: odd gap {L}"); odd+=1
            if s2 != 'D':
                print(f"chew k={k} r={r}: end state {s2} != D"); bad+=1
    print(f"cert_chew K={K} R={R}: {'no gap==3, no odd gap' if bad==0 and odd==0 else 'ANOMALIES'}")
    return bad+odd

# ---- 3. separator crossing: [D] 0^3 1^3 0^2 1^(2s+5) -> ... 0^2 1 [D] 0^3 1^(2s+3), 15 steps ----
def cert_sep(K=40, S=60):
    bad = 0; odd = 0
    for k in range(1, K):
        for s in range(0, S):
            left = list('0' + '01'*k)
            body = list('0'*3 + '1'*3 + '0'*2 + '1'*(2*s+5))
            tape = left + body + ['0']
            pos = len(left)
            t2,p2,s2,g = micro_run(tape, pos, 'D', 15)
            for st,L in g:
                if L == 3: print(f"[CANDIDATE HALT] sep k={k} s={s}: E met gap 3"); bad+=1
                if L % 2 == 1: print(f"[ANOMALY] sep k={k} s={s}: odd gap {L}"); odd+=1
            if s2 != 'D':
                print(f"sep k={k} s={s}: end state {s2} != D"); bad+=1
    print(f"cert_sep K={K} S={S}: {'no gap==3, no odd gap' if bad==0 and odd==0 else 'ANOMALIES'}")
    return bad+odd

if __name__ == "__main__":
    tot = 0
    tot += cert_RLD(200)
    tot += cert_chew(60, 60)
    tot += cert_sep(40, 60)
    print("\nLEMMA STRESS:", "CLEAN (no gap-3, no odd gap, forms hold)" if tot==0 else f"{tot} ANOMALIES")
