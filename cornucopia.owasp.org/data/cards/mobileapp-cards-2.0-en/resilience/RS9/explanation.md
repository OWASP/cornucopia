## Scenario: Sean can reverse engineer the app because the code obfuscation is not strong enough according to what is recommended or the perceived effort of a potential attacker

Consider a scenario where Sean encounters a financial app that has ProGuard enabled, but only with the default configuration. The default ProGuard rules rename classes to `a`, `b`, `c` but do not obfuscate string literals, do not apply control-flow obfuscation, and leave all Android framework subclass names intact. Sean can trace the control flow from the entry points (named Activities) through to the internal logic using the decompiled class structure, even with the default name mangling.

1. Default ProGuard configuration without additional hardening leaves significant structure visible in decompiled code.
2. String literals (API endpoints, algorithm names, error messages) provide a roadmap through the obfuscated code.
3. Reflection-based code and dynamically loaded classes may be exempt from obfuscation.

### Example

Sean decompiles the obfuscated APK. He cannot read class names, but he can find string constants: `"https://api.target.com/v2/auth"`, `"AES/CBC/PKCS5Padding"`, `"******"` (a JWT header). These strings, combined with the class structure visible from Activity/Fragment base class names, give him enough context to map the authentication flow. He identifies the JWT signing secret — also a hardcoded string — in under an hour. The obfuscation slowed him down by about twenty minutes.

## Threat Modeling

### STRIDE

This scenario falls under **Information Disclosure**.

Insufficient obfuscation leaves the app's security-relevant logic, secrets, and control flow visible to static analysis, reducing the time and skill required to reverse-engineer the app and identify exploitable vulnerabilities.

### What can go wrong?

- JWT signing secrets, API keys, and algorithm identifiers are visible as string constants.
- Recognizable control-flow patterns (login, payment processing) are identified and analysed.
- Anti-tamper and anti-debugging logic is located and NOP-patched using the visible structure.

### What are we going to do about it?

- Apply string obfuscation to all security-sensitive string constants, not just class names.
- Use control-flow obfuscation to make decompiled code less readable.
- Remove hardcoded secrets from the binary entirely; fetch them from a secure remote source or derive them from hardware-bound material.
- Test the obfuscation effectiveness by decompiling the release build and assessing readability against the app's threat model.
