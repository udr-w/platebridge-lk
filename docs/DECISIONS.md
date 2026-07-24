# Technical and product decisions

1. **Preferred stack retained.** React/TypeScript/Vite and FastAPI/SQLAlchemy/SQLite match the requested stack and keep the local demo understandable.
2. **Environment-backed setup instead of Alembic.** The prototype creates tables and deterministically reseeds a disposable database. Production evolution would require Alembic; adding migration ceremony to a reset-first demo was not valuable.
3. **Obvious demo auth.** Predefined users and `demo-{id}` tokens make role switching fast and do not misrepresent security.
4. **No map.** A responsive nearby list with straight-line distance is useful offline and avoids fragile tiles/geocoding/API keys.
5. **Stored safety outcome.** Classification, explanation and checks remain on each listing for review. A future system should version complete assessments/rules separately.
6. **Role API checks.** Navigation is convenience; authorization is enforced by FastAPI dependencies.
7. **Central product configuration.** Product name, password, safety time and radius use environment/config defaults so branding and pilot values are not scattered.
8. **Cross-platform scripts.** POSIX shell and explicit PowerShell/CMD launchers complement Docker Compose; Node 20+ avoids host-specific legacy Vite behavior.

