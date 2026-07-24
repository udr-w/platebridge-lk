# Contributing to PlateBridge LK

Thank you for considering a contribution to PlateBridge LK.

PlateBridge LK is a multilingual surplus-food rescue prototype designed for Sri Lankan communities. It explores how households, organisations, recipients, volunteers, and coordinators could safely redistribute suitable surplus food while protecting privacy and dignity.

The project is currently a **demonstration prototype**, not a production food-distribution service.

Contributions are welcome in areas such as:

- Frontend development
- Backend development
- Accessibility
- Sinhala and Tamil localisation
- User experience
- Food-safety workflow design
- Privacy and security
- Documentation
- Testing
- DevOps
- Product research

## Important Project Limitations

PlateBridge LK does not currently provide:

- Official food-safety certification
- Government-approved operating procedures
- Production-grade authentication
- Real identity verification
- Live SMS, email, or push notifications
- Production logistics coordination
- Medical or legal advice
- A public food-distribution service

Do not present the prototype as approved by Sri Lankan public-health authorities, Public Health Inspectors, government agencies, food technologists, legal advisers, or medical professionals.

Any proposal affecting food-safety rules, recipient privacy, identity verification, or real-world operations must clearly state that professional review is required.

## Code of Conduct

All contributors must follow the project’s [Code of Conduct](CODE_OF_CONDUCT.md).

Treat every participant with respect.

In particular:

- Do not use degrading language for food recipients
- Do not require people to publicly prove poverty
- Do not expose personal addresses or contact details
- Do not use real vulnerable individuals as demonstration data
- Do not introduce discriminatory assumptions
- Do not trivialise food-safety concerns
- Do not claim that software alone can guarantee food safety

## Before You Start

For small corrections, documentation improvements, tests, and minor bug fixes, you may open a pull request directly.

For larger changes, open an issue or discussion first.

Examples of larger changes include:

- New user roles
- Major database changes
- Authentication redesign
- Safety-rule changes
- Location or mapping integrations
- Real notification integrations
- New deployment models
- Significant UI redesigns
- Changes to anonymity or privacy behaviour
- Changes to rescue state transitions
- Changes to project licensing

Discussing larger changes first helps avoid parallel work and architectural drift.

## Development Setup

### Prerequisites

Install:

- Git
- Docker and Docker Compose, recommended
- Node.js 20 or later
- npm
- Python 3.11 or later

## Clone the Repository

```bash
git clone https://github.com/udr-w/platebridge-lk.git
cd platebridge-lk
