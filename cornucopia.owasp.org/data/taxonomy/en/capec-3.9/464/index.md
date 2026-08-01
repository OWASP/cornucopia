# CAPEC™ 464: Evercookie

## Description

An attacker creates a very persistent cookie that stays present even after the user thinks it has been removed. The cookie is stored on the victim's machine in over ten places. When the victim clears the cookie cache via traditional means inside the browser, that operation removes the cookie from certain places but not others. The malicious code then replicates the cookie from all of the places where it was not deleted to all of the possible storage locations once again. So the victim again has the cookie in all of the original storage locations. In other words, failure to delete the cookie in even one location will result in the cookie's resurrection everywhere. The evercookie will also persist across different browsers because certain stores (e.g., Local Shared Objects) are shared between different browsers.

Source: [CAPEC™ 464](https://capec.mitre.org/data/definitions/464.html)

## Related ASVS Requirements

ASVS (5.0): [10.4.8](/taxonomy/asvs-5.0/10-oauth-and-oidc/04-oauth-authorization-server#V10.4.8), [7.1.1](/taxonomy/asvs-5.0/07-session-management/01-session-management-documentation#V7.1.1), [7.1.2](/taxonomy/asvs-5.0/07-session-management/01-session-management-documentation#V7.1.2), [7.1.3](/taxonomy/asvs-5.0/07-session-management/01-session-management-documentation#V7.1.3), [7.3.1](/taxonomy/asvs-5.0/07-session-management/03-session-timeout#V7.3.1), [7.3.2](/taxonomy/asvs-5.0/07-session-management/03-session-timeout#V7.3.2), [7.4.1](/taxonomy/asvs-5.0/07-session-management/04-session-termination#V7.4.1), [7.4.4](/taxonomy/asvs-5.0/07-session-management/04-session-termination#V7.4.4), [7.4.5](/taxonomy/asvs-5.0/07-session-management/04-session-termination#V7.4.5), [7.5.2](/taxonomy/asvs-5.0/07-session-management/05-defenses-against-session-abuse#V7.5.2), [7.6.1](/taxonomy/asvs-5.0/07-session-management/06-federated-re-authentication#V7.6.1)
