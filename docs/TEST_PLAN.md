# Test plan

## Automated

- **Backend unit:** green/amber/red rules, precedence and human-readable outcomes.
- **Backend API:** demo login, metrics, unavailable/expired claims, excess portions, alias masking, volunteer transition, invalid receipt, incident creation and reset.
- **Frontend unit:** safety result has an icon/text label and status changes with locale.
- **Type/build:** strict TypeScript check and production Vite bundle.
- **End to end:** recipient login → browse → claim → rescue; donor login → five-step listing → amber result.

Run everything except browser E2E with `./scripts/test.sh`; run E2E with `cd frontend && npm run e2e` after setup. Docker can be tested with `PLAYWRIGHT_BASE_URL=http://localhost:8080 PLAYWRIGHT_EXTERNAL=1 npm run e2e`.

## Manual regression

At desktop and 390px widths: switch each language, tab through navigation/forms, create green/amber/red listings, approve amber, claim partial portions, complete collection and delivery, toggle alias, file/resolve an incident, suspend/reactivate a user, reset, sign in again, and simulate backend unavailability.

## Known untested areas

PowerShell scripts are designed for standard Windows 10/11 but require execution on a Windows host for definitive validation. Screen-reader testing, native-speaker copy QA, high concurrency, database recovery, all browser engines and production threat testing remain outside prototype scope.

