# CAPEC™ 136: LDAP Injection

## Description

An attacker manipulates or crafts an LDAP query for the purpose of undermining the security of the target. Some applications use user input to create LDAP queries that are processed by an LDAP server. For example, a user might provide their username during authentication and the username might be inserted in an LDAP query during the authentication process. An attacker could use this input to inject additional commands into an LDAP query that could disclose sensitive information. For example, entering a * in the aforementioned query might return information about all users on the system. This attack is very similar to an SQL injection attack in that it manipulates a query to gather additional information or coerce a particular return value.

Source: [CAPEC™ 136](https://capec.mitre.org/data/definitions/136.html)

## Related ASVS Requirements

ASVS (5.0): [1.2.6](/taxonomy/asvs-5.0/01-encoding-and-sanitization/02-injection-prevention#V1.2.6), [1.3.3](/taxonomy/asvs-5.0/01-encoding-and-sanitization/03-sanitization#V1.3.3), [16.3.3](/taxonomy/asvs-5.0/16-security-logging-and-error-handling/03-security-events#V16.3.3), [16.3.4](/taxonomy/asvs-5.0/16-security-logging-and-error-handling/03-security-events#V16.3.4), [16.5.1](/taxonomy/asvs-5.0/16-security-logging-and-error-handling/05-error-handling#V16.5.1)
