# CAPEC™ 463: Padding Oracle Crypto Attack

## Description

An adversary is able to efficiently decrypt data without knowing the decryption key if a target system leaks data on whether or not a padding error happened while decrypting the ciphertext. A target system that leaks this type of information becomes the padding oracle and an adversary is able to make use of that oracle to efficiently decrypt data without knowing the decryption key by issuing on average 128*b calls to the padding oracle (where b is the number of bytes in the ciphertext block). In addition to performing decryption, an adversary is also able to produce valid ciphertexts (i.e., perform encryption) by using the padding oracle, all without knowing the encryption key.

Source: [CAPEC™ 463](https://capec.mitre.org/data/definitions/463.html)

## Related ASVS Requirements

ASVS (5.0): [11.2.4](/taxonomy/asvs-5.0/11-cryptography/02-secure-cryptography-implementation#V11.2.4), [11.2.5](/taxonomy/asvs-5.0/11-cryptography/02-secure-cryptography-implementation#V11.2.5), [11.3.1](/taxonomy/asvs-5.0/11-cryptography/03-encryption-algorithms#V11.3.1), [16.3.3](/taxonomy/asvs-5.0/16-security-logging-and-error-handling/03-security-events#V16.3.3)
