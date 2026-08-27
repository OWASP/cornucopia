## Scenario: Sean can reverse engineer the app because code or security-sensitive resources (e.g., strings, configuration, and bundled assets) are insufficiently obfuscated

### Example

Sean opens a puzzle game package and finds readable endpoint names, feature flags, and a comment explaining the developer’s “secret level.” He reconstructs the business rules before finishing his coffee, then wins with a spreadsheet instead of talent.

Code, strings, configuration, and bundled assets that matter to security should be obfuscated appropriately. Obfuscation cannot replace real controls, but leaving everything legible makes reverse engineering and abuse needlessly easy.


## Threat Modeling

### STRIDE

This scenario is primarily **Tampering**, **Information Disclosure** in STRIDE. The named condition is: Sean can reverse engineer the app because code or security-sensitive resources (e.g., strings, configuration, and bundled assets) are insufficiently obfuscated.

- **MAS-THREAT-0059:** Attackers can analyze the app's logic and security controls with minimal effort.

- **MAS-ATTACK-0001:** Obtaining the app package and reverse engineering it.

### What can go wrong?

If Sean can reverse engineer the app because code or security-sensitive resources (e.g., strings, configuration, and bundled assets) are insufficiently obfuscated, the failure is concrete rather than merely theatrical: the app could let an attacker cross the resilience boundary and reach data or capability that this flow should protect. In this card, the practical route includes Obtaining the app package and reverse engineering it. That can turn a normal user action into unauthorized access, disclosure, alteration, or service disruption; the mapped weakness entries below identify the exact implementation evidence to check.

Mapped weaknesses that sharpen the review:

- MASWE-0060 — Resource Obfuscation Not Implemented: This weakness occurs when an app's resources and assets are left in clear, unprotected form, revealing how the app works and aiding reverse engineering.
- MASWE-0059 — Code Obfuscation Not Implemented: This weakness occurs when an app's code, particularly its security-relevant logic, ships without effective obfuscation, facilitating reverse engineering and static analysis.

### What are we going to do about it?

Obfuscate security-sensitive code and resources with a maintained build configuration, keep secrets out of strings and bundled assets, and test the released package with reverse-engineering tools to confirm useful controls are not trivially exposed.


Mapped MASTG tests:

- MASTG-TEST-0368 — Insufficient Obfuscation of Security-Relevant Java/Kotlin Code: If security-relevant Java or Kotlin code is not sufficiently obfuscated, decompilation of the app's DEX bytecode can expose business logic, device attestation and environment checks, integrity checks, and other implementation details...
- MASTG-TEST-0369 — Insufficient Obfuscation of Security-Relevant Native Code: If native libraries that implement security-relevant logic are not obfuscated, reverse engineering of packaged native code can expose business logic, device attestation and environment checks, integrity checks, and other implementation...
- MASTG-TEST-0391 — Insufficient Obfuscation of Security-Relevant Native Code: If native Mach-O code that implements security-relevant logic is not obfuscated, reverse engineering of packaged iOS binaries can expose business logic, device attestation and environment checks, integrity checks, and other...

Mapped MASTG best practices:

- MASTG-BEST-0029 — Implementing Resilience and RASP Signals: The source provides the mapped security guidance for this control.

Mapped MASTG knowledge:

- MASTG-KNOW-0033 — Obfuscation: @MASTG-KNOW-0111 introduces common obfuscation techniques that apply across platforms. On Android, those techniques can affect both the Java or Kotlin layer and the native layer.
- MASTG-KNOW-0089 — Obfuscation: @MASTG-KNOW-0111 introduces common obfuscation techniques that apply across platforms. On iOS, these techniques can affect native Mach-O code, Objective-C and Swift runtime metadata, bundled resources, and data used by the app.
