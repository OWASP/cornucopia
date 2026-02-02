# CAPEC™ 181: Flash File Overlay

## Description

An attacker creates a transparent overlay using flash in order to intercept user actions for the purpose of performing a clickjacking attack. In this technique, the Flash file provides a transparent overlay over HTML content. Because the Flash application is on top of the content, user actions, such as clicks, are caught by the Flash application rather than the underlying HTML. The action is then interpreted by the overlay to perform the actions the attacker wishes.

Source: [CAPEC™ 181](https://capec.mitre.org/data/definitions/181.html)

## Related ASVS Requirements

ASVS (5.0): [3.7.1](/taxonomy/asvs-5.0/03-web-frontend-security/07-other-browser-security-considerations#V3.7.1)
