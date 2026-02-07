# CAPEC™ 55: Rainbow Table Password Cracking

## Description

An attacker gets access to the database table where hashes of passwords are stored. They then use a rainbow table of pre-computed hash chains to attempt to look up the original password. Once the original password corresponding to the hash is obtained, the attacker uses the original password to gain access to the system.

Source: [CAPEC™ 55](https://capec.mitre.org/data/definitions/55.html)

## Related ASVS Requirements

ASVS (5.0): [11.2.1](/taxonomy/asvs-5.0/11-cryptography/02-secure-cryptography-implementation#V11.2.1), [11.2.4](/taxonomy/asvs-5.0/11-cryptography/02-secure-cryptography-implementation#V11.2.4), [11.2.5](/taxonomy/asvs-5.0/11-cryptography/02-secure-cryptography-implementation#V11.2.5), [11.3.1](/taxonomy/asvs-5.0/11-cryptography/03-encryption-algorithms#V11.3.1), [11.3.2](/taxonomy/asvs-5.0/11-cryptography/03-encryption-algorithms#V11.3.2), [11.3.3](/taxonomy/asvs-5.0/11-cryptography/03-encryption-algorithms#V11.3.3), [11.3.4](/taxonomy/asvs-5.0/11-cryptography/03-encryption-algorithms#V11.3.4), [11.3.5](/taxonomy/asvs-5.0/11-cryptography/03-encryption-algorithms#V11.3.5), [11.4.1](/taxonomy/asvs-5.0/11-cryptography/04-hashing-and-hash-based-functions#V11.4.1), [11.4.2](/taxonomy/asvs-5.0/11-cryptography/04-hashing-and-hash-based-functions#V11.4.2), [11.4.3](/taxonomy/asvs-5.0/11-cryptography/04-hashing-and-hash-based-functions#V11.4.3), [11.4.4](/taxonomy/asvs-5.0/11-cryptography/04-hashing-and-hash-based-functions#V11.4.4), [13.3.1](/taxonomy/asvs-5.0/13-configuration/03-secret-management#V13.3.1), [14.1.1](/taxonomy/asvs-5.0/14-data-protection/01-data-protection-documentation#V14.1.1), [14.1.2](/taxonomy/asvs-5.0/14-data-protection/01-data-protection-documentation#V14.1.2)
