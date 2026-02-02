# CAPEC™ 87: Forceful Browsing

## Description

An attacker employs forceful browsing (direct URL entry) to access portions of a website that are otherwise unreachable. Usually, a front controller or similar design pattern is employed to protect access to portions of a web application. Forceful browsing enables an attacker to access information, perform privileged operations and otherwise reach sections of the web application that have been improperly protected.

Source: [CAPEC™ 87](https://capec.mitre.org/data/definitions/87.html)

## Related ASVS Requirements

ASVS (5.0): [10.2.3](/taxonomy/asvs-5.0/10-oauth-and-oidc/02-oauth-client#V10.2.3), [13.2.1](/taxonomy/asvs-5.0/13-configuration/02-backend-communication-configuration#V13.2.1), [13.2.2](/taxonomy/asvs-5.0/13-configuration/02-backend-communication-configuration#V13.2.2), [13.4.5](/taxonomy/asvs-5.0/13-configuration/04-unintended-information-leakage#V13.4.5), [16.3.2](/taxonomy/asvs-5.0/16-security-logging-and-error-handling/03-security-events#V16.3.2), [2.2.2](/taxonomy/asvs-5.0/02-validation-and-business-logic/02-input-validation#V2.2.2), [3.1.1](/taxonomy/asvs-5.0/03-web-frontend-security/01-web-frontend-security-documentation#V3.1.1), [3.7.5](/taxonomy/asvs-5.0/03-web-frontend-security/07-other-browser-security-considerations#V3.7.5), [8.1.1](/taxonomy/asvs-5.0/08-authorization/01-authorization-documentation#V8.1.1)
