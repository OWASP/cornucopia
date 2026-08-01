# CAPEC™ 62: Cross Site Request Forgery

## Description

An attacker crafts malicious web links and distributes them (via web pages, email, etc.), typically in a targeted manner, hoping to induce users to click on the link and execute the malicious action against some third-party application. If successful, the action embedded in the malicious link will be processed and accepted by the targeted application with the users' privilege level. This type of attack leverages the persistence and implicit trust placed in user session cookies by many web applications today. In such an architecture, once the user authenticates to an application and a session cookie is created on the user's system, all following transactions for that session are authenticated using that cookie including potential actions initiated by an attacker and simply "riding" the existing session cookie.

Source: [CAPEC™ 62](https://capec.mitre.org/data/definitions/62.html)

## Related ASVS Requirements

ASVS (5.0): [10.2.1](/taxonomy/asvs-5.0/10-oauth-and-oidc/02-oauth-client#V10.2.1), [3.3.2](/taxonomy/asvs-5.0/03-web-frontend-security/03-cookie-setup#V3.3.2), [3.5.1](/taxonomy/asvs-5.0/03-web-frontend-security/05-browser-origin-separation#V3.5.1), [3.5.2](/taxonomy/asvs-5.0/03-web-frontend-security/05-browser-origin-separation#V3.5.2), [3.5.3](/taxonomy/asvs-5.0/03-web-frontend-security/05-browser-origin-separation#V3.5.3), [3.5.4](/taxonomy/asvs-5.0/03-web-frontend-security/05-browser-origin-separation#V3.5.4), [3.5.5](/taxonomy/asvs-5.0/03-web-frontend-security/05-browser-origin-separation#V3.5.5), [3.5.6](/taxonomy/asvs-5.0/03-web-frontend-security/05-browser-origin-separation#V3.5.6), [3.5.7](/taxonomy/asvs-5.0/03-web-frontend-security/05-browser-origin-separation#V3.5.7), [3.5.8](/taxonomy/asvs-5.0/03-web-frontend-security/05-browser-origin-separation#V3.5.8), [3.7.3](/taxonomy/asvs-5.0/03-web-frontend-security/07-other-browser-security-considerations#V3.7.3), [4.4.2](/taxonomy/asvs-5.0/04-api-and-web-service/04-websocket#V4.4.2)
