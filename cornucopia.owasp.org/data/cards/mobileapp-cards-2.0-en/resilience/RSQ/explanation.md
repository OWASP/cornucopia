## Scenario: Titus can patch out critical functionality because the runtime integrity checks are not strong enough according to what is recommended or the perceived effort of a potential attacker

Consider a scenario where Titus wants to bypass the app's anti-cheat mechanism in a gaming app. The app checks at runtime that its own code has not been modified by computing a hash of loaded `classes.dex` and comparing it against a hardcoded expected value. Titus patches the hash comparison function to always return `true` using a binary patch. The integrity check now always passes, regardless of what code is running. The app loads Titus's modified version without complaint.

1. Runtime integrity checks implemented as single comparison functions are trivially NOP-patched.
2. Integrity check results stored in a local variable can be overridden with a debugger or instrumentation tool.
3. Integrity checks that run once at startup and store a boolean result can be patched at the check point; subsequent code reads the cached boolean.

### Example

Titus modifies the gaming app to inject a cheat module. The app's runtime integrity check computes a DEX hash and compares it in a function `boolean checkIntegrity()`. Titus patches the function's return instruction to always return `true`. The check passes. The cheat module runs. The integrity check was the only gate between the app's normal state and the modified state, and it was a single branch instruction.

## Threat Modeling

### STRIDE

This scenario falls under **Tampering**.

Titus modifies the running app and patches out the mechanism that would detect the modification, allowing the tampered version to run as if it were legitimate.

### What can go wrong?

- Cheat modules in gaming apps give unfair advantages and undermine the user community.
- Modified apps bypass anti-fraud, anti-cheat, or business logic controls.
- The patched integrity check allows all subsequent security controls that assume the code is unmodified to be bypassed.

### What are we going to do about it?

- Implement multiple, distributed integrity checks throughout the codebase; patching one does not satisfy all of them.
- Combine integrity check results: use the computed hash as a key-derivation input so that if the hash is wrong, the derived key is wrong, and the cryptographic operation fails — not just a boolean comparison.
- Report integrity failures to the server as a risk signal rather than terminating immediately (immediate termination is easy to patch to a NOP).
- Use Google Play Integrity API / App Attest to provide a server-verifiable, hardware-rooted integrity attestation.
