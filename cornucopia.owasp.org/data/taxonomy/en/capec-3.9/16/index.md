# CAPEC™ 16: Dictionary-based Password Attack

## Description

{'p': [{'__prefix': 'xhtml', '__text': "An attacker tries each of the words in a dictionary as passwords to gain access to the system via some user's account. If the password chosen by the user was a word within the dictionary, this attack will be successful (in the absence of other mitigations). This is a specific instance of the password brute forcing attack pattern."}, {'__prefix': 'xhtml', '__text': "Dictionary Attacks differ from similar attacks such as Password Spraying (CAPEC-565) and Credential Stuffing (CAPEC-600), since they leverage unknown username/password combinations and don't care about inducing account lockouts."}]}

Source: [CAPEC™ 16](https://capec.mitre.org/data/definitions/16.html)

## Related ASVS Requirements

ASVS (5.0): [13.2.3](/taxonomy/asvs-5.0/13-configuration/02-backend-communication-configuration#V13.2.3), [6.2.11](/taxonomy/asvs-5.0/06-authentication/02-password-security#V6.2.11), [6.2.12](/taxonomy/asvs-5.0/06-authentication/02-password-security#V6.2.12), [6.2.4](/taxonomy/asvs-5.0/06-authentication/02-password-security#V6.2.4), [6.3.2](/taxonomy/asvs-5.0/06-authentication/03-general-authentication-security#V6.3.2), [6.4.2](/taxonomy/asvs-5.0/06-authentication/04-authentication-factor-lifecycle-and-recovery#V6.4.2)
