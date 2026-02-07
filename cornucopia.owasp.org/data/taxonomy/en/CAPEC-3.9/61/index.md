# CAPEC™ 61: Session Fixation

## Description

The attacker induces a client to establish a session with the target software using a session identifier provided by the attacker. Once the user successfully authenticates to the target software, the attacker uses the (now privileged) session identifier in their own transactions. This attack leverages the fact that the target software either relies on client-generated session identifiers or maintains the same session identifiers after privilege elevation.

Source: [CAPEC™ 61](https://capec.mitre.org/data/definitions/61.html)

## Related ASVS Requirements

ASVS (5.0): [14.2.1](/taxonomy/asvs-5.0/14-data-protection/02-general-data-protection#V14.2.1), [3.3.3](/taxonomy/asvs-5.0/03-web-frontend-security/03-cookie-setup#V3.3.3), [3.3.4](/taxonomy/asvs-5.0/03-web-frontend-security/03-cookie-setup#V3.3.4), [3.5.4](/taxonomy/asvs-5.0/03-web-frontend-security/05-browser-origin-separation#V3.5.4), [7.2.1](/taxonomy/asvs-5.0/07-session-management/02-fundamental-session-management-security#V7.2.1), [7.2.2](/taxonomy/asvs-5.0/07-session-management/02-fundamental-session-management-security#V7.2.2)
