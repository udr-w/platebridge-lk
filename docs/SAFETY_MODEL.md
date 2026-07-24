# Demo safety model

The engine returns a classification, plain-language explanation and failed/review checks. Results are stored with the listing for audit. Configuration defaults are in `backend/app/config.py` and `.env.example`.

## Green — eligible under demo rules

Green applies when no red or amber condition is found. Seed examples include sealed dry rations, whole fruit and untouched bakery products with a valid collection deadline.

## Amber — coordinator review required

Amber applies to prepared meals, event food, meat/fish/egg/dairy, refrigeration or frozen handling, and incomplete storage details. It is not a lesser safety guarantee: the listing stays unavailable until a coordinator explicitly approves it.

## Red — not eligible for human redistribution

Red takes precedence when preparation time is unknown for prepared food, food was served or partially eaten, spoilage is visible, packaging is damaged/leaking, the donor marks it unsafe, the deadline passed, or cooked food exceeds the default four-hour ambient window without cold storage. Red listings are stored as rejected for demonstration/audit and never appear to recipients.

## Limits and governance

This is an understandable prototype rule engine, not microbiological risk assessment. It does not evaluate pathogens, temperature logs, expiry labels, cross-contamination, source licensing or individual medical needs. A disclaimer is insufficient: real operation needs hazard analysis, documented handling protocols, staff training, insurance, incident escalation, traceability, validation and approval by qualified food-safety professionals, legal advisers, relevant public-health authorities and operating partners in Sri Lanka.

Composting, organic-waste collection and animal-feed partner review are shown only as future concepts.

