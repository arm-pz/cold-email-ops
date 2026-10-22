# Report formats

## Verdict vocabulary

- **PASS** — the rule is met, with the metric and its source shown.
- **WATCH** — below target or on a negative slope, but no floor is breached yet.
- **FAIL** — a floor or gate is breached.
- **INCONCLUSIVE** — the metric is missing, or the sample is too small to judge. Never upgrade
  this to PASS.

Every finding carries an owner and a next check date. Every number is an input, a script
output, or an assumption labeled as one.

## Plan report

1. **Inputs and assumptions** — table: Input | Value | Source (user, tool export, or assumption).
2. **Capacity** — table below, from `scripts/cold_email_math.py capacity`.
3. **Provider split** — sends, replies, and reply rate by Google / Outlook / other; state whether
   the account's own 6.5× check supports the source benchmark.
4. **List gate design** — who samples, when, the 10-row check, the valid-contact-rate bar, and
   what happens on HOLD.
5. **Deliverability monitoring** — per-domain floor, two-week slope rule, daily inbox check,
   same-day swap, shadow-ban protocol, replacement cadence.
6. **Role and automation map** — table: Role | Daily check | Automated step | Accuracy | Owner |
   Check | Blast radius. Four roles minimum: list builder, copywriter, deliverability, replies.
7. **Reply path** — who answers, hours, the 5-minute target, what happens out of hours.
8. **Metrics** — PTL, reply rate by provider, and for agency work each client against the
   agency average.
9. **Risks and open questions** — assumptions that would change the plan, and the date of the
   first capacity review.

| Capacity | Value |
| --- | --- |
| Monthly target | |
| Sends/day (22 sending days) | |
| Inboxes needed (10/day each) | |
| Domains needed (3 inboxes each) | |
| Replacements/week at 6–9 month burn | |

## Audit report

1. **Verdict table** — Area | Verdict | Evidence | Finding IDs. Areas: list, deliverability,
   automation, replies, measurement.
2. **Findings** — ID | Severity (blocker / high / medium / low) | Evidence | Fix | Owner |
   Next check.
3. **Early warnings** — domains on a two-week decline and clients under the agency average,
   even where the current level still passes.
4. **Do not change** — the parts that are working, so the fix does not disturb them.
5. **Data gaps** — every INCONCLUSIVE and the metric or export needed to close it.

## List gate report

- **Decision:** GO or HOLD, on the first line.
- **Sample** — 10 rows: # | Company | Title | Size fit | Mailbox valid | Note. Quote the sample
  date and who read it.
- **Fail patterns** — what the bad rows have in common (wrong filter, stale source, wrong
  seniority, invalid mailboxes).
- **Re-run condition** — the specific change (query, provider, enrichment rule) that triggers a
  fresh 10-row sample.

## Language rules

- Source figures stay labeled "source benchmark"; client figures stay labeled with their export
  date.
- Do not write "deliverability is fine" without the bounce, placement, and reply evidence.
- A single week of data is not a trend; say INCONCLUSIVE and name the next checkpoint.
- Agency averages are early warnings, not verdicts on a client's account.
