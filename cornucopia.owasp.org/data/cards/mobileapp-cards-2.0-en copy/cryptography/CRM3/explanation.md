## Scenario: Orace can compromise protected data because random values used to generate cryptographic keys, initialization vectors, or nonces are predictable

### Example

Orace runs a raffle at a school fête using an app that picks winners from the current second on the clock. Three children press the button together and the prize goes to whoever happened to shout “banana” loudest.

Predictable randomness makes generated keys, IVs, and nonces guessable. An attacker who can reproduce the input or timing can recreate cryptographic material and recover protected data.


## Threat Modeling

### STRIDE

This scenario is primarily **Elevation of Privilege** in STRIDE. The named condition is: Orace can compromise protected data because random values used to generate cryptographic keys, initialization vectors, or nonces are predictable.

- **MAS-THREAT-0012:** Attackers can predict or reproduce random values used in security contexts.

- **MAS-ATTACK-0001:** Obtaining the app package and reverse engineering it.
- **MAS-ATTACK-0019:** Recovering or guessing the seed used by the generator to reproduce its output.
- **MAS-ATTACK-0024:** Observing enough outputs to recover the internal state of a non-cryptographic PRNG.

### What can go wrong?

If Orace can compromise protected data because random values used to generate cryptographic keys, initialization vectors, or nonces are predictable, the failure is concrete rather than merely theatrical: the app could let an attacker cross the cryptography boundary and reach data or capability that this flow should protect. In this card, the practical route includes Obtaining the app package and reverse engineering it. Also, Recovering or guessing the seed used by the generator to reproduce its output. That can turn a normal user action into unauthorized access, disclosure, alteration, or service disruption; the mapped weakness entries below identify the exact implementation evidence to check.

Mapped weaknesses that sharpen the review:

- MASWE-0012 — Improper Random Number Generation: This weakness occurs when random values used in a security context are produced by a non-cryptographic pseudorandom number generator (PRNG) or derived from predictable seeds.

### What are we going to do about it?

Generate keys, IVs, and nonces with the platform CSPRNG, never predictable values, and ensure every nonce is unique for its key; test generated values and runtime calls for entropy, reuse, and safe failure.


Mapped MASTG tests:

- MASTG-TEST-0204 — Insecure Random API Usage: Android apps sometimes use an insecure pseudorandom number generator (PRNG), such as `java.util.Random`, which is a linear congruential generator and produces a predictable sequence for any given seed value. As a result,...
- MASTG-TEST-0205 — Non-random Sources Usage: Android applications sometimes use non-random sources to generate "random" values, leading to potential security vulnerabilities. Common practices include relying on the current time, such as `Date().getTime()`, or accessing...
- MASTG-TEST-0311 — Insecure Random API Usage: iOS apps sometimes use insecure pseudorandom number generators (PRNGs) instead of cryptographically secure ones. This test case focuses on detecting the use of insecure APIs such as the standard C library functions `rand`, `random`, and...

Mapped MASTG best practices:

- MASTG-BEST-0001 — Use Secure Random Number Generator APIs: Use a cryptographically secure pseudorandom number generator as provided by the platform or programming language you are using.
- MASTG-BEST-0025 — Use Secure Random Number Generator APIs: Use secure random number generator APIs that are backed by the operating system _cryptographically secure pseudorandom number generator (CSPRNG)_. Do not build your own _pseudorandom number generator (PRNG)_.

Mapped MASTG knowledge:

- MASTG-KNOW-0013 — Random Number Generation: Cryptography requires secure pseudo random number generation (PRNG). Standard Java classes as `java.util.Random` do not provide sufficient randomness and in fact may make it possible for an attacker to guess the next value that will be...
- MASTG-KNOW-0070 — Random Number Generator: Random number generation is a critical component of many cryptographic operations, including key generation, initialization vectors, nonces, and tokens. Apple systems provide a trusted Cryptographically Secure Pseudorandom Number...
