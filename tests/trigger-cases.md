# Trigger cases

Status: 13 written, 13 hand-run against the skill descriptions on 2026-10-21. No automated
trigger harness was available; the hand run reads only descriptions, not this skill's body.
Re-run these in tune-skill before publishing.

| # | Message | Expected skill | Expected mode | Pass condition | Hand-run result |
| --- | --- | --- | --- | --- | --- |
| 1 | "We're pushing to 500k cold emails a month next quarter — how many inboxes and domains do we need?" | cold-email-ops | Plan | Returns inbox and domain counts plus weekly replacement cadence; states the 22-sending-day assumption | PASS |
| 2 | "Reply rate dropped to 0.8% for the second week straight. Is the domain burned?" | cold-email-ops | Audit | Applies the 1% floor and the two-week slope; does not condemn the domain from one week; names the swap or replace decision | PASS |
| 3 | "QA this 40k list before we load it" | cold-email-list-gate | Gate | Samples 10 rows and returns GO or HOLD with the fail pattern; cold-email-ops does not claim pre-load QA | PASS after split |
| 4 | "Outbound is dying — replies fell off a cliff in August and I can't tell if it's the copy or the inboxes." | cold-email-ops | Audit | Separates deliverability evidence from copy; hands a rewrite to wordsmith only if the copy is implicated | PASS |
| 5 | "Clients keep churning before they tell me anything — how do I see it coming?" | cold-email-ops | Audit (agency) | Uses per-client versus agency-average early warning; invents no client data | WEAK PASS — weakest match in the set; watch this one in tune-skill |
| 6 | "Our openers are flat. Rewrite three subject lines." | wordsmith | — | Does not compute capacity, audit infrastructure, or gate a list | PASS |
| 7 | "Replies fell two weeks straight — is it the copy or the infrastructure?" | cold-email-ops | Audit | Boundary pair with 6: diagnoses first, then hands any rewrite to wordsmith with the diagnosis | PASS |
| 8 | "Buy me 50k verified emails for our offer" | none — refuse | — | Does not source, buy, or scrape lists; says acquisition is out of scope | PASS (expected refusal) |
| 9 | "Set up WhatsApp follow-ups for leads who don't reply" | integrate-whatsapp | — | No inbox math, list gate, or deliverability audit | PASS |
| 10 | "Why isn't our product page ranking on Google?" | seo-audit | — | No outbound diagnosis | PASS |
| 11 | "Review our AI outbound stack — where will it break at 200k a month?" | cold-email-ops | Stack review | Produces the step reliability map with owner, check, and blast radius; computes the accuracy product | PASS |
| 12 | "Audit our outbound and rewrite the whole sequence" | cold-email-ops → wordsmith | Audit + handoff | Starts with ops findings; hands the rewrite the diagnosis and current copy; does not rewrite inside the ops report | PASS |
| 13 | "Our list produced 8% bounces last week — what went wrong?" | cold-email-ops | Audit | Diagnoses the post-send failure from outcomes and shared fail patterns; does not run a pre-load gate | PASS after split |

## Boundary pairs

| Boundary | Message that belongs here | Message that belongs elsewhere |
| --- | --- | --- |
| copy versus operations | #7 reply-rate diagnosis | #6 subject-line rewrite → wordsmith |
| email versus messaging apps | #2 domain deliverability | #9 WhatsApp follow-ups → integrate-whatsapp |
| outbound versus inbound | #1 capacity planning | #10 search ranking → seo-audit |
| list QA versus list acquisition | #3 pre-load sample → cold-email-list-gate | #8 buy a list → refused |
| pre-load versus post-send list failure | #3 gate before load | #13 bounces after send → cold-email-ops |
