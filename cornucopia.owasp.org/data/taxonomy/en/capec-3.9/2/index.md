# CAPEC™ 2: Inducing Account Lockout

## Description

An attacker leverages the security functionality of the system aimed at thwarting potential attacks to launch a denial of service attack against a legitimate system user. Many systems, for instance, implement a password throttling mechanism that locks an account after a certain number of incorrect log in attempts. An attacker can leverage this throttling mechanism to lock a legitimate user out of their own account. The weakness that is being leveraged by an attacker is the very security feature that has been put in place to counteract attacks.

Source: [CAPEC™ 2](https://capec.mitre.org/data/definitions/2.html)

## Related ASVS Requirements

ASVS (5.0): [10.5.5](/taxonomy/asvs-5.0/10-oauth-and-oidc/05-oidc-client#V10.5.5), [10.6.2](/taxonomy/asvs-5.0/10-oauth-and-oidc/06-openid-provider#V10.6.2), [16.3.1](/taxonomy/asvs-5.0/16-security-logging-and-error-handling/03-security-events#V16.3.1), [16.3.3](/taxonomy/asvs-5.0/16-security-logging-and-error-handling/03-security-events#V16.3.3), [2.3.2](/taxonomy/asvs-5.0/02-validation-and-business-logic/03-business-logic-security#V2.3.2), [2.4.1](/taxonomy/asvs-5.0/02-validation-and-business-logic/04-anti-automation#V2.4.1), [2.4.2](/taxonomy/asvs-5.0/02-validation-and-business-logic/04-anti-automation#V2.4.2), [6.1.1](/taxonomy/asvs-5.0/06-authentication/01-authentication-documentation#V6.1.1), [6.3.1](/taxonomy/asvs-5.0/06-authentication/03-general-authentication-security#V6.3.1), [6.3.8](/taxonomy/asvs-5.0/06-authentication/03-general-authentication-security#V6.3.8)
