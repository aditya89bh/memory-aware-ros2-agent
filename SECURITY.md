# Security Policy

## Supported Versions

This project is pre-1.0. Security fixes are applied to the default branch and
included in the next release artifact.

| Version | Supported |
| --- | --- |
| `main` | Yes |
| Released `0.x` versions | Best effort |

## Reporting A Vulnerability

Please do not open a public issue for a suspected vulnerability. Report security
concerns privately to the repository maintainers with:

- Affected version or commit.
- Steps to reproduce.
- Impact and affected component.
- Any suggested mitigation.

Maintainers should acknowledge reports within 7 days and provide a remediation
plan or status update once the impact is understood.

## Scope

Security-sensitive areas include persistence backends, generated artifacts,
GitHub Actions workflows, ROS2 node inputs, and any future network-facing
interfaces. The package currently avoids runtime third-party dependencies to
keep the production attack surface small.
