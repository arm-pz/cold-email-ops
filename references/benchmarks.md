# Benchmarks and where they come from

All thresholds in `SKILL.md` are distilled from one operator's account:

> Will Breton (@bretonwill), "Everything I Learned From Managing 3.5M+ Cold Emails/Month",
> X article, 18 October 2026. The author reports 10M+ cold emails sent across 100+ B2B
> companies at Pipeline, and 3.5M+ per month in his previous delivery role.

Treat these as starting thresholds, not laws. The source is a single operator's dataset, not
controlled research; list, offer, market, and sending setup all move the numbers. Calibrate
against the account's own data after four weeks, and label every borrowed figure
"source benchmark" in reports. Never present these as the client's results.

## Capacity and burn

| Rule | Value | What it means | Override when |
| --- | --- | --- | --- |
| Sends per inbox per day | ~10; up to 20 while healthy | Keeps per-inbox volume low so one dead inbox is a small share of total | The account has its own deliverability evidence at higher volume |
| Inboxes per domain | 3 | Spreads risk across domains | Domain reputation policy or ESP limits say otherwise |
| Sending days per month | ~22 | The source's 450 / 4,500 inbox figures only reconcile on business-day sending; 30 calendar days gives 334 / 3,334 | The account sends seven days a week — recompute and say so |
| Monthly capacity per inbox | ~220 | 10/day × 22 days | Follows from the two rows above |
| Inbox burn | 6–9 months | Even with SPF, DKIM, and DMARC in place | Never assumed away; only the timing is uncertain |
| Replacement cadence | weekly; same day on failure | Volume must not dip while capacity is replaced | — |

At the defaults: 100k/month ≈ 455 inboxes across ≈ 152 domains; 1M/month ≈ 4,546 inboxes
across ≈ 1,516 domains.

## List and data

| Rule | Value | Source note |
| --- | --- | --- |
| Pre-load sample | 10 rows | Two wrong in ten means the whole list has a problem |
| Provider comparison sample | 50–100 contacts | The source compares phone providers by dials per in-profile person — 50 dials fell to ~15 on the same criteria with a different provider. For email, use valid-contact rate |
| Data provider as a lever | — | Lead quality is decided at the provider, not in cleanup |

## Deliverability

| Rule | Value | Source note |
| --- | --- | --- |
| Domain reply floor | ≥1% reply rate, automated replies included | Anything below gets replaced |
| Decline signal | 2 consecutive weeks of falling reply rate | The slope matters more than the level |
| Shadow-ban signature | 0% bounce + healthy placement + zero replies | Rewrite copy once; retire if unchanged within 48 hours |
| Google vs Microsoft | ~6.5× reply rate to Google recipients in the source's data | Directional only; verify per account. Microsoft-heavy enterprise TAMs got matching sender/receiver providers |

## Errors and automation

| Rule | Value | Source note |
| --- | --- | --- |
| End-to-end reliability | Product of step accuracies; 0.8⁴ ≈ 41% | Errors multiply with each automated step |
| Autonomy controls | Forced menus, sample-then-approve gate, no history overwrite | The source spent a month removing autonomy from its agents |
| Rule gaming | "Get N leads" invites fabrication | Gate on quality checks, not output quotas |

## Results

| Rule | Value | Source note |
| --- | --- | --- |
| Speed to lead | Reply in under 5 minutes | Positive reply to meeting rose from ~20% to ~80% in the source's experience; a day's delay effectively loses the lead |
| Prospects-to-lead (PTL) | Contacts sent ÷ leads | Under 500 is strong; prefer it to reply rate at high volume |
| Small vs large motion | 500-contact tight lists (~5% reply) plus universal messaging (~1%) | 5% of 500 = 25 replies; 1% of 100,000 = 1,000. Do not re-contact a tight list for at least a month |

## Source cases (calibration only, never templates)

- Branded cups manufacturer: went live the week of 5 October 2026; ~160 positive replies
  after ~1 week, under 100 emails sent per positive reply.
- Eden Studio: 69,204 landscaping and hardscaping businesses scraped, enriched on 19 custom
  data points, 41,150 emails sent, 53 meetings in 50 days. Meetings are not leads — do not
  plug the meeting count into PTL without converting it.

These are the author's reported results, not the user's. Do not reuse them as evidence of
this skill's output.
