# CAPEC™ 510: SaaS User Request Forgery

## Description

An adversary, through a previously installed malicious application, performs malicious actions against a third-party Software as a Service (SaaS) application (also known as a cloud based application) by leveraging the persistent and implicit trust placed on a trusted user's session. This attack is executed after a trusted user is authenticated into a cloud service, "piggy-backing" on the authenticated session, and exploiting the fact that the cloud service believes it is only interacting with the trusted user. If successful, the actions embedded in the malicious application will be processed and accepted by the targeted SaaS application and executed at the trusted user's privilege level.

Source: [CAPEC™ 510](https://capec.mitre.org/data/definitions/510.html)

## Related ASVS Requirements

ASVS (5.0): [10.4.16](/taxonomy/asvs-5.0/10-oauth-and-oidc/04-oauth-authorization-server#V10.4.16), [10.4.6](/taxonomy/asvs-5.0/10-oauth-and-oidc/04-oauth-authorization-server#V10.4.6), [4.1.5](/taxonomy/asvs-5.0/04-api-and-web-service/01-generic-web-service-security#V4.1.5), [7.1.2](/taxonomy/asvs-5.0/07-session-management/01-session-management-documentation#V7.1.2), [7.1.3](/taxonomy/asvs-5.0/07-session-management/01-session-management-documentation#V7.1.3), [7.3.2](/taxonomy/asvs-5.0/07-session-management/03-session-timeout#V7.3.2), [7.4.1](/taxonomy/asvs-5.0/07-session-management/04-session-termination#V7.4.1), [7.4.5](/taxonomy/asvs-5.0/07-session-management/04-session-termination#V7.4.5), [7.5.2](/taxonomy/asvs-5.0/07-session-management/05-defenses-against-session-abuse#V7.5.2), [7.6.1](/taxonomy/asvs-5.0/07-session-management/06-federated-re-authentication#V7.6.1), [8.1.3](/taxonomy/asvs-5.0/08-authorization/01-authorization-documentation#V8.1.3), [8.1.4](/taxonomy/asvs-5.0/08-authorization/01-authorization-documentation#V8.1.4), [8.2.4](/taxonomy/asvs-5.0/08-authorization/02-general-authorization-design#V8.2.4)
