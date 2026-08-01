# Security Policy

## Supported Versions

The versions of each of the sets of game cards currently supported by Cornucopia include.

| Version                  | Supported          |
| ------------------------ | ------------------ |
| Web App edition =< 2.2 | :white_check_mark: |
| Mobile App edition => 1.1 | :white_check_mark: |
| Companion edition => 1.0 | :white_check_mark: |
| eop cards => 1.0         | :white_check_mark: |

## Disclosing a Vulnerability

If you find that there are issues with the cards themselves, or with the build mechanisim for outputting the cards please raise a PR (https://github.com/OWASP/cornucopia/pulls) or create an issue (https://github.com/OWASP/cornucopia/issues) on GitHab and we'll look into it. Any vulnerabilities in libraries should be automatically resolved by dependabot and merged by the project team within 30 days but if you discover one that hasn't been please feel free to reach out to grant.ongers@owasp.org

As a general rule the project team aims to resolve Critical Vulnerabilities immediately, Highs and Mediums with-in 30 days and Lows will be taken on a case-by-case basis.

## Our Threat Models

You may review the threat model for Cornucopia and Copi by using [OWASP Threat Dragon](https://www.threatdragon.com/#/dashboard) and opening copi.json or cornucopia.json at [ThreatDragonModels](ThreatDragonModels).

Note: If you are looking into using Copi, it may be worth looking at some of [Copi's known threats](copi.owasp.org/SECURITY.md#our-threat-model) before doing so to make sure you have prepared yourself accordingly and taken our known threats into account.
