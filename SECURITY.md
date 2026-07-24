# Security Policy

## Project Status

PlateBridge LK is currently a **demonstration prototype** intended for local evaluation, product presentations, and controlled testing.

It is **not production-ready** and must not currently be used to coordinate real food donations, store sensitive personal information, or operate a public service.

The prototype includes demonstration implementations for authentication, authorisation, food-safety screening, location privacy, notifications, and logistics. These implementations require a full security and privacy review before any real-world pilot.

## Supported Versions

Security fixes are currently applied only to the latest code on the default branch.

| Version | Supported |
|---|---|
| Latest `main` branch | Yes |
| Latest tagged release | Yes, when applicable |
| Older commits or releases | No |
| Forks and modified deployments | No |

Because PlateBridge LK is under active development, reporters should verify that a potential vulnerability still exists on the latest version before submitting a report.

## Reporting a Vulnerability

Please **do not open a public GitHub issue** for a suspected security vulnerability.

Use GitHub's private vulnerability reporting feature:

1. Open the repository's **Security** tab.
2. Select **Advisories**.
3. Select **Report a vulnerability**.
4. Provide the information requested below.

If private vulnerability reporting is not available, contact the repository owner privately through their verified GitHub profile and ask for a secure reporting channel. Do not include sensitive vulnerability details in a public comment, discussion, or issue.

## What to Include

A useful report should contain:

- A clear description of the vulnerability
- The affected component or endpoint
- The affected branch, tag, or commit
- Preconditions required to reproduce it
- Step-by-step reproduction instructions
- A minimal proof of concept, when safe
- The security or privacy impact
- The user roles affected
- Relevant logs, screenshots, or request samples
- Suggested remediation, when available

Remove or replace:

- Passwords
- Authentication tokens
- Session identifiers
- Personal information
- Precise private locations
- Real recipient or donor details
- Any other confidential data

Use only fictional or locally generated demonstration data when preparing a proof of concept.

## Response Process

After receiving a report, the maintainers will aim to:

1. Acknowledge receipt within **three working days**
2. Perform an initial assessment within **seven working days**
3. Confirm whether the issue is accepted, requires more information, or is outside the project scope
4. Develop and test a fix when the issue is accepted
5. Coordinate disclosure with the reporter
6. Publish a security advisory when appropriate

Response times are targets rather than guaranteed service-level commitments because this is currently a privately maintained prototype.

Please allow the maintainers a reasonable opportunity to investigate and correct the issue before publishing technical details.

## Issues Considered In Scope

Examples of relevant security or privacy issues include:

- Authentication bypass
- Broken role-based access control
- Donors accessing recipient-only information
- Recipients accessing donor-private information
- Volunteers accessing unrelated rescue records
- Coordinator or administrator privilege escalation
- Exposure of precise household locations
- Exposure of private contact information
- Recipient alias or anonymity bypass
- Insecure direct object references
- SQL injection
- Command injection
- Cross-site scripting
- Cross-site request forgery with meaningful impact
- Path traversal
- Unsafe file upload handling
- Sensitive information written to logs
- Hard-coded secrets or credentials
- Insecure session or token handling
- Unauthorised modification of listings or rescues
- Pickup-code bypass or predictable pickup codes
- Manipulation of rescue state transitions
- Unauthorised access to incident reports
- Dependency vulnerabilities that affect the running application
- Docker or deployment configuration that exposes sensitive services
- Demonstrable privacy failures involving approximate or exact locations

## Issues Normally Outside Scope

The following are normally outside the security-reporting scope:

- General feature requests
- User-interface suggestions
- Missing production functionality already documented as a prototype limitation
- Vulnerabilities that exist only in unsupported third-party deployments
- Reports generated only by automated scanners without evidence of impact
- Dependency alerts without a demonstrated effect on this project
- Missing email, SMS, or notification integrations
- Absence of production identity verification
- Known use of shared demonstration credentials
- Attacks requiring physical access to the reporter's own device
- Social-engineering attacks without a technical vulnerability
- Denial-of-service testing that could disrupt a shared environment
- Food-quality complaints or disagreements with the demonstration safety rules
- Claims that the automated food-safety model represents official certification

Food-safety concerns remain important, but they should be reported as product-safety or operational issues unless they also expose a software security or privacy vulnerability.

## Demonstration Credentials

The repository may document shared credentials such as:

```text
demo123
