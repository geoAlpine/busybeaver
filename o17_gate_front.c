/* o17 carry-front erosion tracker (2026-07-07).
 * Blank orbit (or seed L): at every odometer tick, decode the block list and record
 * the leftmost block index that changed since the previous tick (excluding pure LSB
 * growth).  Emits per-window minima: the erosion curve of the frozen wall.
 * Usage: o17_gate_front <L> <maxsteps> <window_ticks>
 * [Exact simulation; OBSERVED data; decides nothing.]
 */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdint.h>

#define SZ (1u<<25)
static unsigned char tape[SZ];
static int WR[6][2], DIR[6][2], NX[6][2];
#define MAXB 4000000
static long blA[MAXB], blB[MAXB];

static void setup(void){
    const char *spec = "1RB1LD_1RC0LE_1LA1RE_0LF1LA_1RB0RB_---0LB";
    for(int s=0;s<6;s++){ const char *t = spec + s*7;
        for(int r=0;r<2;r++){ const char *u = t + r*3;
            if(u[0]=='-'){ WR[s][r]=-1; DIR[s][r]=0; NX[s][r]=-1; }
            else { WR[s][r]=u[0]-'0'; DIR[s][r]=(u[1]=='R')?1:-1; NX[s][r]=u[2]-'A'; } } }
}

int main(int argc, char**argv){
    setup();
    long L = (argc>1)? atol(argv[1]) : 0;
    unsigned long long maxsteps = (argc>2)? strtoull(argv[2],0,10) : 1000000000ULL;
    unsigned long long WIN = (argc>3)? strtoull(argv[3],0,10) : 1000ULL;
    long off = 1<<20;
    for(long i=1;i<=L;i++) tape[off+i]=1;
    long pos = off, hi = (L? off+L : off);
    long L1 = L? off+1 : (long)SZ;
    int st = 0, prevdir = 0;
    unsigned long long step = 0, n = 0;
    long *prev = blA, *cur = blB; long nprev = -1;
    long curmin = 1000000000;
    printf("# n  window_min_front  m  gates_marked_separately\n");
    while(step < maxsteps){
        int r = tape[pos];
        if(st==5 && r==0){ printf("HALT step=%llu n=%llu\n", step, n); return 0; }
        if(r==0 && (st==0 || st==3) && pos < L1){
            printf("GATE step=%llu n=%llu st=%c\n", step, n, (st==0?'A':'D'));
            fflush(stdout);
        }
        int w = WR[st][r], d = DIR[st][r], ns = NX[st][r];
        if(st==4 && r==0 && prevdir==-1 && d==1 && pos >= hi-3){
            n++;
            /* decode blocks */
            long m=0; long i = (L1<(long)SZ? L1 : pos);
            while(i<=hi && m<MAXB){
                while(i<=hi && !tape[i]) i++;
                long j=i; while(j<=hi && tape[j]) j++;
                if(j>i){ cur[m++]=j-i; }
                i=j;
            }
            if(nprev>=0){
                long f=-1; long mn = (m<nprev? m:nprev);
                for(long k2=0;k2<mn;k2++) if(cur[k2]!=prev[k2]){ f=k2; break; }
                if(f<0 && m!=nprev) f=mn;
                if(f>=0 && !(m==nprev && f==m-1)){ if(f<curmin) curmin=f; }
            }
            { long *t2=prev; prev=cur; cur=t2; nprev=m; }
            if(n % WIN == 0){
                printf("W %llu %ld %ld\n", n, (curmin==1000000000? -1: curmin), nprev);
                fflush(stdout);
                curmin = 1000000000;
            }
        }
        prevdir = d;
        if(w==1){ if(pos<L1) L1=pos; tape[pos]=1; }
        else { tape[pos]=0;
               if(pos==L1){ long q=pos+1; while(q<=hi && !tape[q]) q++; L1 = (q<=hi)? q : (long)SZ; } }
        pos += d; st = ns; step++;
        if(pos>hi) hi=pos;
        if(pos<=0 || pos>=(long)SZ-1){ fprintf(stderr,"OVERFLOW\n"); return 2; }
    }
    printf("CAP step=%llu n=%llu\n", step, n);
    return 0;
}
