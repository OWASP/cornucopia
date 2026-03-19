# CAPEC™ 468: Generic Cross-Browser Cross-Domain Theft

## Description

An attacker makes use of Cascading Style Sheets (CSS) injection to steal data cross domain from the victim's browser. The attack works by abusing the standards relating to loading of CSS: 1. Send cookies on any load of CSS (including cross-domain) 2. When parsing returned CSS ignore all data that does not make sense before a valid CSS descriptor is found by the CSS parser.

Source: [CAPEC™ 468](https://capec.mitre.org/data/definitions/468.html)

