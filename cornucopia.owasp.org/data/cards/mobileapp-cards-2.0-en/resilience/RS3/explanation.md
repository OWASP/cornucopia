## Scenario: Tobias can disclose sensitive data and implementation details because debug symbols and other non-production metadata remain available in the release

### Example

Tobias hands a release binary to a contractor who opens its debug symbols and sees class names, database fields, and a comment titled “temporary secret shortcut.” The contractor reconstructs the app so quickly that the coffee is still hot.

Release artifacts should not carry symbols or metadata that expose implementation details. Stripping non-production material raises the effort required to reverse engineer security-sensitive behavior.


## Threat Modeling

### STRIDE

This scenario is primarily **Information Disclosure** in STRIDE. The named condition is: Tobias can disclose sensitive data and implementation details because debug symbols and other non-production metadata remain available in the release.

- **MAS-THREAT-0061:** Attackers can analyze the app's internals and disable its security controls.

- **MAS-ATTACK-0001:** Obtaining the app package and reverse engineering it.
- **MAS-ATTACK-0006:** Accessing the system logs on a compromised device or from an app holding log-access permissions.

### What can go wrong?

If Tobias can disclose sensitive data and implementation details because debug symbols and other non-production metadata remain available in the release, the failure is concrete rather than merely theatrical: the app could let an attacker cross the resilience boundary and reach data or capability that this flow should protect. In this card, the practical route includes Obtaining the app package and reverse engineering it. Also, Accessing the system logs on a compromised device or from an app holding log-access permissions. That can turn a normal user action into unauthorized access, disclosure, alteration, or service disruption; the mapped weakness entries below identify the exact implementation evidence to check.

Mapped weaknesses that sharpen the review:

- MASWE-0061 — Debug Artifacts Not Removed: This weakness occurs when an app ships to production containing developer debug artifacts, such as verbose logging, testing utilities, debugging symbols, or leftover debug and test code.

### What are we going to do about it?

Strip debug symbols, source maps, test endpoints, and other non-production metadata from release artifacts, and keep them in controlled build storage; inspect the shipped package and symbol exposure as part of release testing.


Mapped MASTG tests:

- MASTG-TEST-0219 — Testing for Debugging Symbols: This test case checks for debugging symbols in all binaries contained in the app.
- MASTG-TEST-0288 — Debugging Symbols in Native Binaries: This test checks whether the app includes debugging symbols in its native binaries. Debugging symbols can provide valuable information during reverse engineering and vulnerability analysis by exposing sensitive implementation details...

Mapped MASTG best practices:

- No MASTG best practice is assigned; use the narrowest platform control that blocks the attack.

Mapped MASTG knowledge:

- MASTG-KNOW-0063 — Debugging Information and Debug Symbols: When an iOS application is compiled, the compiler generates debug symbols for each binary in the app, including the main executable, frameworks, and extensions. These symbols include class names, global variables, and method and...
