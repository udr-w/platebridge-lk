# API reference

Interactive OpenAPI is available at `/docs`. All paths except health and login require `Authorization: Bearer demo-{user_id}`.

| Group | Important endpoints |
|---|---|
| Health/auth | `GET /health`, `POST /api/auth/demo-login`, `GET /api/users/me` |
| Listings | `GET/POST /api/listings`, `GET/PATCH /api/listings/{id}`, `POST .../claim`, `.../approve`, `.../reject`, `.../cancel` |
| Rescues | `GET /api/rescues`, `GET /api/rescues/{id}`, `POST .../confirm-pickup`, `.../confirm-delivery`, `.../confirm-receipt`, `.../cancel` |
| Volunteers | `GET /api/volunteer-tasks`, `POST /api/volunteer-tasks/{id}/accept` |
| Privacy/support | `PATCH /api/profiles/privacy`, `GET /api/collection-points`, `GET /api/notifications`, `POST /api/rescues/{id}/messages` |
| Incidents | `POST/GET /api/incidents`, `PATCH /api/incidents/{id}` |
| Oversight | `GET /api/metrics/dashboard`, `GET/PATCH /api/admin/users`, `GET/PATCH /api/admin/safety-rules`, `POST /api/demo/reset` |

Validation errors use FastAPI's structured 422 response. Authorization uses 401/403; missing entities use 404; invalid state and availability changes use 409. `/api/demo/reset` invalidates existing tokens because IDs are reconstructed; the UI signs out accordingly.

