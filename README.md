# cold-email-ops

An agent skill that plans and audits a cold-email program at volume, for agencies running several client accounts or one sender whose arithmetic has to hold.

It answers the capacity question before the first send, then keeps answering it while the program runs: inboxes and domains from a monthly target, burn and replacement cadence, per-domain reply floors, shadow-ban tests, automation error budgets, and per-client reporting.

## Install

```
npx skills add arm-pz/cold-email-ops --skill cold-email-ops
```

For Qoder, copy the folder into the user skills directory:

```
cp -r cold-email-ops ~/.qoder/skills/
```

## Ask it things like

- "How many inboxes and domains do I need for 500,000 sends a month?"
- "Reply rates fell on two domains over the last two weeks. Is it the copy or the infrastructure?"
- "Review this AI outbound stack for failure points before we scale."
- "Give me the per-client report for three accounts."

## What it produces

| Mode | Output |
|---|---|
| Plan | Capacity, gate design, monitoring spec, and the role/automation map |
| Audit | Area verdicts (PASS / WATCH / FAIL / INCONCLUSIVE) with the evidence behind each |
| Stack review | A step map with owner, check, accuracy estimate, and blast radius |

The arithmetic ships as a deterministic script, so a plan is not mental math:

```
python scripts/cold_email_math.py capacity --monthly 100000
python scripts/cold_email_math.py errors 0.8 0.8 0.8 0.8
python scripts/cold_email_math.py ptl --contacts 20000 --leads 53
```

Defaults are 10 cold sends per inbox per day, 3 inboxes per domain, and 22 sending days a month. At those defaults, 100k/month needs about 455 inboxes and 152 domains; 500k needs 2,273 and 758; 1M needs 4,546 and 1,516.

## Operating rules it applies

- Inboxes burn in 6 to 9 months even with clean SPF, DKIM, and DMARC. Replace weekly, or the same day when one fails.
- A domain floor of 1% reply rate. Two consecutive weeks of falling replies puts a domain on watch even while it clears the floor.
- A suspected shadow ban is 0% bounce, healthy placement, zero replies. Rewrite the copy once, not the infrastructure; no change in 48 hours means retire the inboxes.
- End-to-end reliability multiplies: 0.8 x 0.8 x 0.8 x 0.8 leaves about 41%. Even 0.99 four times over leaves about 96%.
- Answer replies within five minutes, or the lead is effectively lost. Track prospects-to-lead under 500, split by receiving provider, and compare each client against the agency average.

## Where the numbers come from

The thresholds are adapted from Will Breton's published account of running 3.5M+ cold emails a month ([source](https://x.com/bretonwill/status/2111690982777323895)). They are labelled **source benchmarks** throughout, never presented as your results or a client's results. This is an independent implementation and is not affiliated with the author.

## What it will not do

- Write or rewrite the emails. That is a [wordsmith](https://github.com/arm-pz/wordsmith) job; hand it the diagnosis and the current copy.
- Gate one list before load. That is [cold-email-list-gate](https://github.com/arm-pz/cold-email-list-gate); this skill audits lists that already sent.
- Buy lists, scrape contacts, enrich rows, or send mail.
- Invent an ICP, a market, or an offer.
- Report a missing metric as PASS. Missing data is INCONCLUSIVE.

## Contents

- `SKILL.md` — the workflow and boundaries.
- `references/benchmarks.md` — every threshold, its source, and when it may be overridden.
- `references/report-format.md` — plan, audit, and list report templates with verdict definitions.
- `scripts/cold_email_math.py` — capacity, error-budget, and PTL arithmetic (Python 3, standard library only).
- `tests/trigger-cases.md` — 13 trigger cases, hand-run.

Validated with [tune-skill](https://github.com/arm-pz/tune-skill): `check_skill.py` reports 0 fail, 0 warn.

## License

MIT. See [LICENSE](LICENSE).
