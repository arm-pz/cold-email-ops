#!/usr/bin/env python3
"""Deterministic math for cold-email capacity, error budgets, and PTL."""

import argparse
import json
import math
import sys

WEEKS_PER_MONTH = 4.345
BURN_MONTHS = (6, 9)


def capacity(args):
    if args.monthly <= 0:
        raise ValueError("--monthly must be positive")
    if args.per_inbox <= 0:
        raise ValueError("--per-inbox must be positive")
    if args.inboxes_per_domain <= 0:
        raise ValueError("--inboxes-per-domain must be positive")
    if not 1 <= args.sending_days <= 31:
        raise ValueError("--sending-days must be between 1 and 31")

    daily = args.monthly / args.sending_days
    inboxes = math.ceil(daily / args.per_inbox)
    domains = math.ceil(inboxes / args.inboxes_per_domain)
    monthly_low = inboxes / BURN_MONTHS[1]
    monthly_high = inboxes / BURN_MONTHS[0]

    return {
        "monthly_target": args.monthly,
        "sending_days": args.sending_days,
        "sends_per_day": round(daily, 1),
        "per_inbox_per_day": args.per_inbox,
        "per_inbox_monthly": args.per_inbox * args.sending_days,
        "inboxes": inboxes,
        "domains": domains,
        "inboxes_per_domain": args.inboxes_per_domain,
        "replacement_per_week": {
            "min": round(monthly_low / WEEKS_PER_MONTH, 1),
            "max": round(monthly_high / WEEKS_PER_MONTH, 1),
        },
        "replacement_per_month": {
            "min": round(monthly_low, 1),
            "max": round(monthly_high, 1),
        },
        "burn_months": list(BURN_MONTHS),
    }


def errors(args):
    if not args.steps:
        raise ValueError("provide at least one step accuracy")
    for step in args.steps:
        if not 0 < step <= 1:
            raise ValueError("each step accuracy must be > 0 and <= 1")
    product = math.prod(args.steps)
    result = {
        "steps": args.steps,
        "end_to_end": round(product, 4),
        "end_to_end_pct": round(product * 100, 1),
        "weakest_step_pct": round(min(args.steps) * 100, 1),
        "step_count": len(args.steps),
    }
    if args.sends is not None:
        if args.sends <= 0:
            raise ValueError("--sends must be positive")
        result["sends"] = args.sends
        result["expected_misses"] = math.ceil(args.sends * (1 - product))
    return result


def ptl(args):
    if args.contacts <= 0:
        raise ValueError("--contacts must be positive")
    if args.leads <= 0:
        raise ValueError("--leads must be positive")
    value = args.contacts / args.leads
    return {
        "contacts": args.contacts,
        "leads": args.leads,
        "ptl": round(value, 1),
        "verdict": "under 500 - solid" if value < 500 else "at or above 500 - improve",
    }


def render(kind, data):
    if kind == "capacity":
        return "\n".join(
            [
                f"Capacity for {data['monthly_target']:,} emails/month",
                f"  Sending days: {data['sending_days']}",
                f"  Sends/day: {data['sends_per_day']:,.1f}",
                f"  Per inbox: {data['per_inbox_per_day']}/day = {data['per_inbox_monthly']}/month",
                f"  Inboxes: {data['inboxes']:,}",
                f"  Domains: {data['domains']:,} ({data['inboxes_per_domain']} inboxes/domain)",
                "  Replacements at 6-9 month burn: "
                f"{data['replacement_per_week']['min']:,.1f}-{data['replacement_per_week']['max']:,.1f}/week "
                f"({data['replacement_per_month']['min']:,.1f}-{data['replacement_per_month']['max']:,.1f}/month)",
            ]
        )
    if kind == "errors":
        lines = [
            f"End-to-end reliability: {data['end_to_end_pct']}% "
            f"({data['step_count']} steps, weakest {data['weakest_step_pct']}%)"
        ]
        if "sends" in data:
            lines.append(
                f"Expected misses at {data['sends']:,} sends: {data['expected_misses']:,}"
            )
        return "\n".join(lines)
    return "\n".join(
        [
            f"PTL: {data['ptl']:,.1f} contacts per lead "
            f"({data['contacts']:,} contacts / {data['leads']:,} leads)",
            f"Verdict: {data['verdict']}",
        ]
    )


def build_parser():
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest="command", required=True)

    cap = sub.add_parser("capacity", help="inboxes and domains for a monthly target")
    cap.add_argument("--monthly", type=int, required=True)
    cap.add_argument("--per-inbox", type=int, default=10)
    cap.add_argument("--sending-days", type=int, default=22)
    cap.add_argument("--inboxes-per-domain", type=int, default=3)
    cap.add_argument("--json", action="store_true")
    cap.set_defaults(func=capacity, kind="capacity")

    err = sub.add_parser("errors", help="end-to-end reliability of sequential steps")
    err.add_argument("steps", type=float, nargs="*")
    err.add_argument("--sends", type=int)
    err.add_argument("--json", action="store_true")
    err.set_defaults(func=errors, kind="errors")

    talk = sub.add_parser("ptl", help="contacts per lead")
    talk.add_argument("--contacts", type=int, required=True)
    talk.add_argument("--leads", type=int, required=True)
    talk.add_argument("--json", action="store_true")
    talk.set_defaults(func=ptl, kind="ptl")

    return parser


def main():
    parser = build_parser()
    args = parser.parse_args()
    try:
        data = args.func(args)
    except ValueError as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 2
    if args.json:
        print(json.dumps(data, indent=2))
    else:
        print(render(args.kind, data))
    return 0


if __name__ == "__main__":
    sys.exit(main())
