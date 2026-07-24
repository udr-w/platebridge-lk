# User flows

## A — Household donation

Donor login → Donate food → enter rice and curry details → confirm refrigeration/ingredients → safety check returns amber → coordinator login → Safety reviews → approve → recipient login → Nearby food → claim → select collection → receive code → donor confirms pickup → recipient confirms receipt → metrics update.

## B — Bakery surplus

Organisation donor → untouched bakery listing → green immediate availability → recipient claims with volunteer delivery → volunteer accepts → marks collected → marks delivered → recipient confirms receipt → completed history.

## C — Unsafe food

Donor creates a listing and marks it previously served/partially eaten → red result → listing status `REJECTED` → public browse excludes it → UI explains why and identifies compost/waste routing as a future concept.

## D — Recipient privacy

Recipient → Privacy → enable alias → claim using a collection point or delivery → donor sees alias and approximate area, never phone or precise home coordinates → admin retains fictional moderation identity.

## E — Incident

Participant opens rescue → Report a problem → category and description → submit → rescue gains a visible flag → coordinator/admin opens incident queue → records review/resolution.

## State constraints

Expired/non-available listings cannot be claimed; requested portions cannot exceed availability; completed listings cannot be edited; collection requires a matching code; delivery follows collection; receipt follows collection/delivery.

