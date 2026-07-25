# Novelty check against the CURRENT holdout list (2026-07-26)

Before any external artifact: are `x2` and `C` still open?

## Source

`https://wiki.bbchallenge.org/wiki/Holdouts_lists` → **`BB6_holdouts_1094.txt`**, shared
2026-06-29 by @mxdys, **1094 machines up to equivalence** (the previous published list was the
1104 of 2026-04-29; this development had been checking against that older snapshot).
Saved to `_bbdata/BB6_holdouts_1094.txt`.

## Result — both still open

Matching up to TNF + left–right reversal (`bb6_holdouts.py`):

    current list (2026-06-29) : 1094 canonical classes

    x2  canonical = 1LB0LC_1LD---_1LE0RD_0RF1RC_0LA1LC_0LC1RF    STILL OPEN: True
    C   canonical = 1LB---_0RC1RD_0LD1RC_1LE0RB_0LF1LD_1LA0LD    STILL OPEN: True

Their canonical forms differ, so they are two distinct entries of the list, not one machine counted
twice.

## Standing caveat

The list is dated 2026-06-29 and it is now late July.  Machines may have been decided in the
intervening weeks; this is simply the most recent PUBLISHED list.  Any external claim should say
"open as of the 2026-06-29 list" rather than "open", and should be re-checked immediately before
release.

**This removes the novelty blocker on publication.  It does not authorise publication — that
remains the owner's decision, and the standing policy is no community posting with external
outreach gated per instance.**
