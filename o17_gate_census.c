/* o17 long-run frontier-gate census (2026-07-07).
 * Exact step-by-step simulation of
 *   o17 = 1RB1LD_1RC0LE_1LA1RE_0LF1LA_1RB0RB_---0LB   (halt = F reads 0)
 * Logs every TRUE-FRONTIER gate event: state A or D reads 0 with no 1 anywhere
 * to the left (O(1) check via exact leftmost-1 tracking).  Also counts right-end
 * odometer ticks ((E,0) reversal with prevdir==-1 near the right edge) and decodes
 * the milestone digit string at each gate.
 * Usage: o17_gate_census <L (0=blank)> <maxsteps>
 * Output: one line per gate:  GATE step=... n=... st=A|D marker=... m=... S=... d1 d2 ... dl
 * [OBSERVED/exact simulation; decides nothing.]
 */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdint.h>

#define SZ (1u<<25)             /* 33.5M cells */
static unsigned char tape[SZ];

/* transition tables: state 0..5, read 0/1 -> write, dir(+1/-1), next */
static int WR[6][2], DIR[6][2], NX[6][2];

static void setup(void){
    const char *spec = "1RB1LD_1RC0LE_1LA1RE_0LF1LA_1RB0RB_---0LB";
    for(int s=0;s<6;s++){
        const char *t = spec + s*7;
        for(int r=0;r<2;r++){
            const char *u = t + r*3;
            if(u[0]=='-'){ WR[s][r]=-1; DIR[s][r]=0; NX[s][r]=-1; }
            else { WR[s][r]=u[0]-'0'; DIR[s][r]= (u[1]=='R')?1:-1; NX[s][r]=u[2]-'A'; }
        }
    }
}

int main(int argc, char**argv){
    setup();
    long L = (argc>1)? atol(argv[1]) : 0;
    unsigned long long maxsteps = (argc>2)? strtoull(argv[2],0,10) : 1000000000ULL;
    long off = 1<<20;
    for(long i=1;i<=L;i++) tape[off+i]=1;
    long pos = off, hi = (L? off+L : off);
    long L1 = L? off+1 : (long)SZ;   /* leftmost 1; SZ = none */
    int st = 0, prevdir = 0;
    unsigned long long step = 0, n = 0;
    unsigned long long nextprog = 10000000000ULL;
    while(step < maxsteps){
        int r = tape[pos];
        if(st==5 && r==0){
            printf("HALT step=%llu n=%llu\n", step, n);
            fflush(stdout);
            return 0;
        }
        if(r==0 && (st==0 || st==3) && pos < L1){
            /* true-frontier gate: decode blocks right of pos */
            long i = pos+1; long m=0; long long S=0; long marker=-1;
            long dig[64]; long nd=0;
            while(i<=hi){
                while(i<=hi && !tape[i]) i++;
                long j=i; while(j<=hi && tape[j]) j++;
                if(j>i){
                    if(marker<0) marker=j-i;
                    else { long d=(j-i-2)/3; S+=d; m++; if(nd<64) dig[nd++]=d; }
                }
                i=j;
            }
            printf("GATE step=%llu n=%llu st=%c marker=%ld m=%ld S=%lld d=",
                   step, n, (st==0?'A':'D'), marker, m, S);
            for(long k=0;k<nd && k<12;k++) printf("%ld%s", dig[k], (k<nd-1&&k<11)?",":"");
            if(nd>12) printf(",...");
            printf(" last=%ld\n", nd? dig[nd-1] : -1);
            fflush(stdout);
        }
        int w = WR[st][r], d = DIR[st][r], ns = NX[st][r];
        if(st==4 && r==0 && prevdir==-1 && d==1 && pos >= hi-3){ n++; }
        prevdir = d;
        if(w==1){ if(pos<L1) L1=pos; tape[pos]=1; }
        else { tape[pos]=0;
               if(pos==L1){ long q=pos+1; while(q<=hi && !tape[q]) q++; L1 = (q<=hi)? q : (long)SZ; } }
        pos += d; st = ns; step++;
        if(pos>hi) hi=pos;
        if(pos<=0 || pos>= (long)SZ-1){ fprintf(stderr,"TAPE OVERFLOW step=%llu\n",step); return 2; }
        if(step==nextprog){ fprintf(stderr,"progress step=%llu n=%llu width=%ld\n", step, n, hi-pos<0?0:hi-(long)off); nextprog += 10000000000ULL; }
    }
    printf("CAP step=%llu n=%llu\n", step, n);
    return 0;
}
