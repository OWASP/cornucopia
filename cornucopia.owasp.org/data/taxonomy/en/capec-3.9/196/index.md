# CAPEC™ 196: Session Credential Falsification through Forging

## Description

An attacker creates a false but functional session credential in order to gain or usurp access to a service. Session credentials allow users to identify themselves to a service after an initial authentication without needing to resend the authentication information (usually a username and password) with every message. If an attacker is able to forge valid session credentials they may be able to bypass authentication or piggy-back off some other authenticated user's session. This attack differs from Reuse of Session IDs and Session Sidejacking attacks in that in the latter attacks an attacker uses a previous or existing credential without modification while, in a forging attack, the attacker must create their own credential, although it may be based on previously observed credentials.

Source: [CAPEC™ 196](https://capec.mitre.org/data/definitions/196.html)

## Related ASVS Requirements

ASVS (5.0): [14.2.1](/taxonomy/asvs-5.0/14-data-protection/02-general-data-protection#V14.2.1), [7.2.1](/taxonomy/asvs-5.0/07-session-management/02-fundamental-session-management-security#V7.2.1), [7.2.3](/taxonomy/asvs-5.0/07-session-management/02-fundamental-session-management-security#V7.2.3)
