# CAPEC™ 133: Try All Common Switches

## Description

An attacker attempts to invoke all common switches and options in the target application for the purpose of discovering weaknesses in the target. For example, in some applications, adding a --debug switch causes debugging information to be displayed, which can sometimes reveal sensitive processing or configuration information to an attacker. This attack differs from other forms of API abuse in that the attacker is indiscriminately attempting to invoke options in the hope that one of them will work rather than specifically targeting a known option. Nonetheless, even if the attacker is familiar with the published options of a targeted application this attack method may still be fruitful as it might discover unpublicized functionality.

Source: [CAPEC™ 133](https://capec.mitre.org/data/definitions/133.html)

## Related ASVS Requirements

ASVS (5.0): [13.2.1](/taxonomy/asvs-5.0/13-configuration/02-backend-communication-configuration#V13.2.1), [13.4.1](/taxonomy/asvs-5.0/13-configuration/04-unintended-information-leakage#V13.4.1), [13.4.2](/taxonomy/asvs-5.0/13-configuration/04-unintended-information-leakage#V13.4.2), [13.4.4](/taxonomy/asvs-5.0/13-configuration/04-unintended-information-leakage#V13.4.4), [13.4.5](/taxonomy/asvs-5.0/13-configuration/04-unintended-information-leakage#V13.4.5), [13.4.6](/taxonomy/asvs-5.0/13-configuration/04-unintended-information-leakage#V13.4.6), [13.4.7](/taxonomy/asvs-5.0/13-configuration/04-unintended-information-leakage#V13.4.7), [14.2.4](/taxonomy/asvs-5.0/14-data-protection/02-general-data-protection#V14.2.4), [16.3.2](/taxonomy/asvs-5.0/16-security-logging-and-error-handling/03-security-events#V16.3.2), [16.3.3](/taxonomy/asvs-5.0/16-security-logging-and-error-handling/03-security-events#V16.3.3), [8.1.1](/taxonomy/asvs-5.0/08-authorization/01-authorization-documentation#V8.1.1), [8.1.4](/taxonomy/asvs-5.0/08-authorization/01-authorization-documentation#V8.1.4), [8.2.1](/taxonomy/asvs-5.0/08-authorization/02-general-authorization-design#V8.2.1), [8.4.2](/taxonomy/asvs-5.0/08-authorization/04-other-authorization-considerations#V8.4.2)
