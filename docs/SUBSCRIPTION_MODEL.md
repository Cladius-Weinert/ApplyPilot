# Subscription Model (Product Documentation MVP)

ApplyPilot is subscription-ready at the product/documentation level, but this MVP does **not** include a payment backend, Stripe integration, card storage, webhook handling, or hosted authorization.

The public plan catalog is defined in `src/applypilot/subscription.py` and is used by the pricing page/CLI for product positioning only.

## Planned tiers

| Plan | Lead limit | Profiles | Main planned unlocks |
| --- | ---: | ---: | --- |
| Free | 5/day | 1 | Basic tracker, basic CV/cover templates, manual checklist |
| Starter | 25/day | 1 | Saved searches, match scoring, CV/cover suggestions, CSV export, 14-day sprint |
| Pro | 100/day | 1 | Portfolio builder, premium prompts, resume tailoring, RWS/AOP templates, freelance gig generator, priority scoring |
| Agency | 500/day | 25 | Multiple profiles, client pipelines, reusable templates, team notes, export reports |

## Current implementation boundary

- No payment provider is active.
- No Stripe keys are required.
- No subscription status is trusted from a client.
- No payment cards are stored.
- No paid feature authorization is enforced yet.

When payment is added later, it should be implemented server-side only, with verified provider webhooks and trusted server-side subscription records.

## No-guarantee policy

Subscriptions sell workflow tooling, templates, organization, and productivity features. They must not claim guaranteed jobs, interviews, hiring, freelance clients, or income.
