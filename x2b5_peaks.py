"""
x2b5_peaks.py -- extract the maxrun sawtooth of B5 and measure phase step-counts.

Records maxrun at every step (cheap incremental? no -- recompute is O(width);
instead we track maxrun by sampling and refine peaks). To get exact peaks/resets
and the STEP COUNT between milestones, we detect local maxima of maxrun by
watching for the drop after a climb.
"""
import sys
from x2b5_sim import RULES, Tape

def run_track(max_steps):
    tape = Tape()
    pos = 0
    state = 'A'
    prev_maxrun = 0
    # sawtooth detection on maxrun
    peaks = []      # (step, maxrun) at local max
    resets = []     # (step, maxrun) local min after a peak
    climbing = True
    last_extreme_step = 0
    # We recompute maxrun only when the head is at the right edge region to be cheap?
    # Simpler: recompute maxrun every K steps and detect sawtooth on the sampled series,
    # then we accept small step-resolution error. For exact peaks use small K.
    K = 25
    mr_prev = 0
    trend_up = True
    for step in range(max_steps):
        sym = tape.read(pos)
        rule = RULES[state][sym]
        if rule is None:
            print("HALT at step", step)
            return peaks, resets, step, True
        w, mv, nxt = rule
        tape.write(pos, w)
        pos += mv
        state = nxt
        if step % K == 0:
            mr = tape.maxrun()
            if trend_up:
                if mr < mr_prev:
                    # mr_prev was a peak
                    peaks.append((step - K, mr_prev))
                    trend_up = False
            else:
                if mr > mr_prev:
                    resets.append((step - K, mr_prev))
                    trend_up = True
            mr_prev = mr
    return peaks, resets, max_steps, False


if __name__ == '__main__':
    cap = int(sys.argv[1]) if len(sys.argv) > 1 else 3_000_000
    peaks, resets, laststep, halted = run_track(cap)
    print("cap:", cap, "halted:", halted)
    # Filter to "super-peaks": the growing envelope. Peaks list has many local maxima;
    # take the running-max envelope.
    print("\n# raw peaks count:", len(peaks), " resets count:", len(resets))
    # Print the last ~40 peaks
    print("\n# last peaks (step, maxrun):")
    for s, m in peaks[-40:]:
        print(f"  {s:>12} {m}")
