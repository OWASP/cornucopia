# CAPEC™ 465: Transparent Proxy Abuse

## Description

A transparent proxy serves as an intermediate between the client and the internet at large. It intercepts all requests originating from the client and forwards them to the correct location. The proxy also intercepts all responses to the client and forwards these to the client. All of this is done in a manner transparent to the client.

Source: [CAPEC™ 465](https://capec.mitre.org/data/definitions/465.html)

## Related ASVS Requirements

ASVS (5.0): [10.4.16](/taxonomy/asvs-5.0/10-oauth-and-oidc/04-oauth-authorization-server#V10.4.16), [10.4.6](/taxonomy/asvs-5.0/10-oauth-and-oidc/04-oauth-authorization-server#V10.4.6), [4.1.5](/taxonomy/asvs-5.0/04-api-and-web-service/01-generic-web-service-security#V4.1.5), [7.1.2](/taxonomy/asvs-5.0/07-session-management/01-session-management-documentation#V7.1.2), [7.1.3](/taxonomy/asvs-5.0/07-session-management/01-session-management-documentation#V7.1.3), [7.3.2](/taxonomy/asvs-5.0/07-session-management/03-session-timeout#V7.3.2), [7.4.1](/taxonomy/asvs-5.0/07-session-management/04-session-termination#V7.4.1), [7.4.5](/taxonomy/asvs-5.0/07-session-management/04-session-termination#V7.4.5), [7.5.2](/taxonomy/asvs-5.0/07-session-management/05-defenses-against-session-abuse#V7.5.2), [7.6.1](/taxonomy/asvs-5.0/07-session-management/06-federated-re-authentication#V7.6.1), [8.1.3](/taxonomy/asvs-5.0/08-authorization/01-authorization-documentation#V8.1.3), [8.1.4](/taxonomy/asvs-5.0/08-authorization/01-authorization-documentation#V8.1.4), [8.2.4](/taxonomy/asvs-5.0/08-authorization/02-general-authorization-design#V8.2.4)
