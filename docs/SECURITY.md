# Security Policy — Themis

## Supported Versions

| Version | Supported | Notes |
|---------|-----------|-------|
| 1.1.x   | ✅ Yes    | Current stable version |
| 1.0.x   | ⚠️ Limited | Upgrade recommended |
| < 1.0   | ❌ No     | Not supported |

## Reporting a Vulnerability

If you discover a security vulnerability in Themis, please do not open a public
issue. Instead, contact the maintainer directly:

- **GitHub:** [@Andres34r7y4](https://github.com/Andres34r7y4)
- **LinkedIn:** [andresdelgado-architect](https://www.linkedin.com/in/andresdelgado-architect/)

Include as much detail as possible:

- Affected Themis version
- Steps to reproduce the problem
- Potential impact
- Suggested mitigation (optional)

## Disclosure Policy

We commit to:

1. Acknowledge your report within 2 business days.
2. Provide updates on the investigation status.
3. Publish a CVE or security advisory if necessary.
4. Give you proper credit for the discovery.

## Scope

Themis is a governance protocol and CLI. Relevant security issues include, but
are not limited to:

- Path traversal or unsafe file writes during `themis init`.
- Secret leakage in logs, reports, or generated assets.
- Command injection through CLI arguments.
- Packaging or entry-point issues that execute unexpected code.

## Acknowledgments

Thanks to everyone who helps keep Themis safe for everyone.
