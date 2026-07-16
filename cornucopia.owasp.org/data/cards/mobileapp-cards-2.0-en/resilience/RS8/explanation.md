## Scenario: Carlos can reverse engineer the app with static analysis and decompilation tools because anti-analysis controls are not strong enough for the app's risk and attacker model

Consider a scenario where Carlos downloads the production APK, opens it in jadx, and within thirty minutes has a reasonably complete understanding of the app's authentication logic, API endpoints, and key-derivation function. The code was not obfuscated — the developer had intended to add ProGuard but never did. Carlos identifies a hardcoded API key in a constants class, a predictable session token format, and a weak key-derivation function. All of this was discoverable through static analysis without running the app at all.

1. Unobfuscated code exposes class names, method logic, and string constants, reducing reverse-engineering effort dramatically.
2. Hardcoded secrets (API keys, symmetric keys, backend URLs) are trivially extractable from static analysis.
3. Proprietary business logic, anti-fraud algorithms, and security-relevant code paths are exposed to competitors and attackers.

### Example

Carlos decompiles the banking app and finds the class `com.target.app.security.AuthHelper` with a method `generateSessionToken(userId)` that concatenates the user ID with a hardcoded salt and Base64-encodes the result. He reverse-engineers the algorithm, generates valid session tokens for arbitrary user IDs, and presents them to the API. The "token generation" was security through obscurity, and the obscurity lasted about 45 minutes.

## Threat Modeling

### STRIDE

This scenario falls under **Information Disclosure**.

Static reverse engineering exposes the app's internal logic, secrets, and security mechanisms, enabling an attacker to craft targeted attacks without any dynamic interaction with the app.

### What can go wrong?

- Hardcoded secrets (API keys, cryptographic keys, backend credentials) are extracted and misused.
- Proprietary algorithms are reverse-engineered and replicated or attacked offline.
- Security controls are analysed to find bypasses before any network interaction occurs.
- Competitor apps replicate proprietary business logic from the decompiled source.

### What are we going to do about it?

- Enable ProGuard/R8 with aggressive obfuscation in release builds.
- Never hardcode secrets in the app binary; use remote configuration, the keystore, or secure secret storage.
- Apply string obfuscation to sensitive string constants (API endpoints, algorithm identifiers).
- For high-value apps, consider native code for security-critical logic to increase the cost of static analysis.
