## Scenario: Adel can predict, derive, or recover encryption or signing keys because their generation or derivation uses insufficient entropy, weak parameters, or known or enumerable input values

### Example

Adel’s club issues electronic padlocks whose “random” codes are the next four digits of the membership number. Adel guesses the pattern, opens every equipment locker, and finds fourteen identical left shoes.

Key generation and derivation require sufficient entropy and strong parameters, not enumerable inputs. Weak or predictable material lets an attacker derive the keys that are supposed to protect the club’s data.


## Threat Modeling

### STRIDE

This scenario is primarily **Tampering**, **Information Disclosure** in STRIDE. The named condition is: Adel can predict, derive, or recover encryption or signing keys because their generation or derivation uses insufficient entropy, weak parameters, or known or enumerable input values.

- **MAS-THREAT-0012:** Attackers can predict or reproduce random values used in security contexts.
- **MAS-THREAT-0013:** Attackers can predict or reproduce improperly generated cryptographic keys.

- **MAS-ATTACK-0001:** Obtaining the app package and reverse engineering it.
- **MAS-ATTACK-0019:** Recovering or guessing the seed used by the generator to reproduce its output.
- **MAS-ATTACK-0024:** Observing enough outputs to recover the internal state of a non-cryptographic PRNG.
- **MAS-ATTACK-0018:** Brute-forcing cryptographic material generated with insufficient length.
- **MAS-ATTACK-0020:** Intercepting cryptographic keys exported in plaintext.

### What can go wrong?

If Adel can predict, derive, or recover encryption or signing keys because their generation or derivation uses insufficient entropy, weak parameters, or known or enumerable input values, the failure is concrete rather than merely theatrical: the app could let an attacker cross the cryptography boundary and reach data or capability that this flow should protect. In this card, the practical route includes Obtaining the app package and reverse engineering it. Also, Recovering or guessing the seed used by the generator to reproduce its output. That can turn a normal user action into unauthorized access, disclosure, alteration, or service disruption; the mapped weakness entries below identify the exact implementation evidence to check.

Mapped weaknesses that sharpen the review:

- MASWE-0012 — Improper Random Number Generation: This weakness occurs when random values used in a security context are produced by a non-cryptographic pseudorandom number generator (PRNG) or derived from predictable seeds.
- MASWE-0013 — Improper Cryptographic Key Generation: This weakness occurs when cryptographic keys are generated with insufficient length, insufficient entropy, or otherwise flawed generation processes, weakening every protection built on top of them.

### What are we going to do about it?

Use an operating-system CSPRNG, strong key sizes, and a salted, work-factor-controlled KDF when deriving keys; reject enumerable inputs and weak parameters, and verify entropy and derivation behavior in static and runtime tests.


Mapped MASTG tests:

- MASTG-TEST-0204 — Insecure Random API Usage: Android apps sometimes use an insecure pseudorandom number generator (PRNG), such as `java.util.Random`, which is a linear congruential generator and produces a predictable sequence for any given seed value. As a result,...
- MASTG-TEST-0205 — Non-random Sources Usage: Android applications sometimes use non-random sources to generate "random" values, leading to potential security vulnerabilities. Common practices include relying on the current time, such as `Date().getTime()`, or accessing...
- MASTG-TEST-0208 — Insufficient Key Sizes: In this test case, we will look for the use insufficient key sizes in Android apps. To do this, we need to focus on the cryptographic frameworks and libraries that are available in Android and the methods that are used to generate,...
- MASTG-TEST-0311 — Insecure Random API Usage: iOS apps sometimes use insecure pseudorandom number generators (PRNGs) instead of cryptographically secure ones. This test case focuses on detecting the use of insecure APIs such as the standard C library functions `rand`, `random`, and...
- MASTG-TEST-0349 — Runtime Use of Insecure Random APIs: If the app uses insecure pseudorandom number generators (PRNGs) at runtime, generated values can become predictable. This can lead to weak tokens, nonces, keys, or identifiers when those values are used in security-relevant contexts....

Mapped MASTG best practices:

- MASTG-BEST-0001 — Use Secure Random Number Generator APIs: Use a cryptographically secure pseudorandom number generator as provided by the platform or programming language you are using.
- MASTG-BEST-0025 — Use Secure Random Number Generator APIs: Use secure random number generator APIs that are backed by the operating system _cryptographically secure pseudorandom number generator (CSPRNG)_. Do not build your own _pseudorandom number generator (PRNG)_.

Mapped MASTG knowledge:

- MASTG-KNOW-0013 — Random Number Generation: Cryptography requires secure pseudo random number generation (PRNG). Standard Java classes as `java.util.Random` do not provide sufficient randomness and in fact may make it possible for an attacker to guess the next value that will be...
- MASTG-KNOW-0012 — Key Generation: The Android SDK allows you to specify how a key should be generated, and under which circumstances it can be used. Android 6.0 (API level 23) introduced the `KeyGenParameterSpec` class that can be used to ensure the correct key usage in...
- MASTG-KNOW-0070 — Random Number Generator: Random number generation is a critical component of many cryptographic operations, including key generation, initialization vectors, nonces, and tokens. Apple systems provide a trusted Cryptographically Secure Pseudorandom Number...
