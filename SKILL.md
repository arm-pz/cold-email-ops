---
name: cold-email-ops
description: >-
  Plan and audit a cold-email program at volume and keep it from degrading: computes
  inbox and domain capacity from a monthly send target, sets per-domain reply-rate
  floors, burn-replacement cadence, shadow-ban tests, and automation error budgets,
  and reports prospects-to-lead with per-client averages. Use when someone is scaling
  outbound, asks how many inboxes or domains they need, why reply rates are falling
  or a domain might be shadow banned, or reviews an AI outbound stack for failure
  points. Not for pre-load list QA (cold-email-list-gate), writing or polishing the
  emails themselves (wordsmith), inbound SEO (seo-audit, programmatic-seo),
  WhatsApp/RCS messaging (integrate-whatsapp, sent-two-way-messaging), or finding
  the market/ICP.
---

# Cold email ops

Operating model distilled from Will Breton's account of running 3.5M+ cold emails a month (source and caveats in `references/benchmarks.md`). Treat outbound as four human roles wired into one math budget: list builder, copywriter, deliverability person, reply handler. Every automated step keeps an owner and a check. Plan for the volume you want, not the volume you have.

## Classify the job first

- **Plan** — new program or a volume target. Output capacity, gate design, monitoring spec, and the role/automation map.
- **Audit** — a running program is degrading. Output area verdicts and findings with evidence.
- **Stack review** — automation reliability. Output the step map and blast radius.
- **List gate** — one list before load is a different job. Use `cold-email-list-gate` and return its GO/HOLD; do not run the ten-row check inside this skill.

Open `references/report-format.md` for the section list of the job you picked.

## Collect inputs once

Ask for: monthly send target; current domains and inboxes; sending tool and data provider; sends, replies, and bounces by domain and by receiving provider; who answers replies and how fast; client roster when the work is agency-side. A missing metric becomes INCONCLUSIVE — never estimate it silently, and never present the source's numbers as the client's results.

## Volume is inbox math

Run the arithmetic with `scripts/cold_email_math.py` instead of by hand (paths resolve from this skill's base directory):

```
python scripts/cold_email_math.py capacity --monthly 500000
python scripts/cold_email_math.py errors 0.8 0.8 0.8 0.8
python scripts/cold_email_math.py ptl --contacts 20000 --leads 53
```

- Budget ~10 cold sends per inbox per day (up to 20 only while the inbox is healthy), 3 inboxes per domain, ~22 sending days per month. At those defaults 100k/month needs ≈455 inboxes and ≈152 domains; 1M/month needs ≈4,546 and ≈1,516. The 22-day assumption is what reconciles the source's 450 / 4,500 figures; say so when quoting them.
- Build for the target volume from day one. Capacity added after the list is ready becomes a bottleneck with a deadline.
- Every inbox burns in 6–9 months even with clean SPF, DKIM, and DMARC. Steady-state replacement is inboxes ÷ burn months; replace weekly, same day when one fails, so total volume does not dip.
- Split every report by receiving provider (Google / Outlook / other). The source saw ~6.5× more replies from Google recipients than Microsoft ones; treat that as directional and verify it in the account's own data. Lumping providers hides what works. For Microsoft-heavy enterprise TAMs, match the sending provider to the receiving one.

## The list breaks before deliverability does

- Pre-load checks belong to `cold-email-list-gate`. In an audit, judge the list from outcomes: bounce rate, valid-contact rate, and whether the bad rows share one filter. Hand a pre-load sample to the gate skill rather than re-deriving it here.
- Lead quality is decided at the data provider. Compare providers on the same criteria with a sample, using valid-contact rate (dials per in-profile person for phone work). Switching providers is a delivery lever, not a cleanup task.
- A list that failed in production is audit evidence, not a sample. Name the shared fail pattern and the query or provider that produced it.

## Deliverability rules

- **Domain floor:** ≥1% reply rate, automated replies included. Below the floor, schedule replacement — do not "keep monitoring".
- **Slope beats level:** two consecutive weeks of falling reply rate puts a domain on watch even while it clears 1%. The slope catches the failure before the floor does.
- Monitor every inbox daily; alert on a reply dip or a bounce rise; swap the same day. Keep per-inbox volume low so one dead inbox barely moves the total.
- **Shadow-ban test:** 0% bounce, healthy placement, zero replies. Rewrite the copy once, not the infrastructure. No change within 48 hours — retire the inboxes. Dead infrastructure stays dead.
- One bad week is not a burned domain. Require the two-week slope or a failed floor before condemning infrastructure.

## Errors multiply — harden the automation

- End-to-end reliability is the product of step accuracies: 0.8 × 0.8 × 0.8 × 0.8 leaves ≈41%. Compute it before trusting a pipeline; even 0.99 four times over leaves ≈96%, which at 100k sends is thousands of misses.
- Give agents menus, not free text; gate every bulk run behind a sample you approve; keep history append-only so you can see what it did.
- Rules get gamed. "Get 5,000 leads" invites fabrication; gate on quality checks (the 10-row sample, valid-contact rate) and keep volume quotas as reporting, not instructions.
- For each automated step record owner, check, accuracy estimate, and blast radius (how many emails a failure reaches before detection). A step with no check is where the audit starts.

## Replies and results

- Speed to lead is the biggest lever after the reply: answering within 5 minutes lifts positive-reply-to-meeting from ~20% to ~80%; a day later the lead is effectively lost. Name who is on replies and their hours before scaling volume.
- Track prospects-to-lead (PTL) = contacts sent ÷ leads. Under 500 is strong. At high volume prefer PTL to reply rate, which stops discriminating once volume is large.
- Run both motions: tight 500-contact lists with tailored messaging (~5% reply) alongside broad universal messaging (~1% at scale). Do not re-contact a tight list for at least a month. 5% of 500 is 25 replies; 1% of 100,000 is 1,000.
- Agency work: track each client against agency-wide averages. A client under average is an early warning weeks before they complain — surface it as a warning, not a verdict.

## Report with evidence

- Every number is an input, a script output, or an assumption labeled as one. Source benchmarks stay labeled "source benchmark".
- Verdicts are PASS / WATCH / FAIL per area, plus INCONCLUSIVE where data is missing. A missing metric never becomes a PASS.
- End with an owner and a next check date for every open finding.

## Boundaries

- Emails need writing or rewriting → `wordsmith`. Hand it the diagnosis (segment, what the reply data says) plus the current copy.
- One list before load → `cold-email-list-gate`. This skill audits lists that already sent.
- Inbound search → `seo-audit` or `programmatic-seo`. WhatsApp or RCS messaging → `integrate-whatsapp` or `sent-two-way-messaging`.
- ICP discovery, offer design, and list acquisition tooling are out of scope. State the assumed market and sender, then stop.
- This skill produces plans and audits. It does not send mail, buy lists, or scrape contacts.

## References

- `references/benchmarks.md` — every threshold used here, its source, and when it may be overridden. Read before defending or changing a number.
- `references/report-format.md` — plan, audit, and list-gate templates with table columns and verdict definitions. Read when writing the deliverable.
