# Outreach email — DRAFT ONLY (not sent; awaiting recipient + explicit go-ahead)

> **STATUS: NOT SENT.** Sending to real external researchers is an outward-facing, hard-to-reverse action. This draft
> is ready; before sending I need (1) the recipient address(es), (2) the sender's name/affiliation/contact to sign
> with, and (3) an explicit "send it." Suggested recipients (their published emails, to be confirmed by the user):
> the authors of arXiv:2510.11723 (S. Eliahou and co-authors, rational-base-numeration group) and/or S. Akiyama.

---

**Subject:** Antihydra / BB(6) non-halting = a one-sided instance of your Normality Conjecture (rational base 3/2)

Dear Professor [NAME],

I'm writing about a concrete and, I think, striking connection between your Normality Conjecture on rational base
number systems (arXiv:2510.11723) and the "Antihydra" Turing machine — currently the smallest open problem on the
Busy Beaver scale (deciding BB(6) requires deciding whether it halts).

Antihydra does **not** halt iff, iterating `H(c)=⌊3c/2⌋` from `c₀=8`, the number of even iterates never drops below a
`1/3` density (equivalently `B_n=3E_n−n≥0` for all `n`). Since `⌊3c/2⌋` is exactly the shift of the base-3/2 number
system, the base-3/2 digit `2c mod 3` read along the orbit lives on the alphabet `{0,2}` (digit `1` is arithmetically
forbidden), and its digit-`0` frequency equals this even-density exactly. So:

> **Antihydra non-halting ⟺ the base-3/2 orbit-word of seed 8 has digit-`0` frequency ≥ 1/3 — a one-sided form of
> your Conjecture 1.3 for base 3/2**, whose Theorem 1.7 (normality ⟺ equidistribution mod `2^ℓ`) is exactly the
> reformulation we had arrived at independently.

More broadly, the whole "Type-I" family of BB(6) cryptid machines turns out to be base-`p/q` value odometers with
`p/q ∈ {3/2, 8/3, 4/3}` — all in your `p<q²` regime — so several of these machines sit directly inside your family
(the `4/3` machine is the Dubickas–Mossinghoff `4/3` problem you cite).

We have verified the dictionary and reductions, and checked numerically that every internal/annealed/structural route
provably stops short (the needed input is single-orbit equidistribution at exponential depth, below the discrepancy
horizon — the rank-1 amenable / Furstenberg-`×2×3` regime). I'd be very glad to share the write-up (a one-page abstract
and detailed notes) and to hear whether the proved fragments of your conjecture, or your numerical machinery, might be
pushed toward the one-sided / effective statement these machines need.

With thanks and best regards,
[SENDER NAME], [AFFILIATION], [CONTACT]

*(Attachments to offer: `OUTREACH_ABSTRACT.md`, `MEETING_BRIEF_4.md`.)*
