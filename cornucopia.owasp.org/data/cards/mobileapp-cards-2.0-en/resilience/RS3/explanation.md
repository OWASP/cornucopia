## Scenario: Tobias can disclose sensitive data and implementation details because debug symbols and other non-production metadata remain available in the release binary

Consider a scenario where Tobias downloads the production APK and decompiles it with jadx. He finds fully qualified class names, method names, and variable names that were not obfuscated — because the release build did not have ProGuard/R8 configured. He also finds a `debug_symbols/` directory in the APK's assets containing the `.pdb` files for the native library, which map function addresses to source-level symbols. Within an hour, Tobias has a near-complete map of the app's internal architecture.

1. Debug symbols in native binaries expose function names, source file paths, and sometimes local variable names.
2. Non-obfuscated Java/Kotlin bytecode exposes class and method structure, making reverse engineering significantly faster.
3. Embedded source maps or `.d` files can reveal source file paths, developer workstation paths, and internal component names.

### Example

Tobias decompiles the native library and finds symbol entries like `com.target.app.internal.AuthTokenManager.getStoredToken()` and `com.target.app.internal.CryptoHelper.generateMasterKey()`. These names, combined with the decompiled bytecode, reduce the reverse engineering effort from weeks to hours. He quickly identifies the key-derivation function's structure and crafts an offline attack. The developer had left debug symbols in because "nobody will bother reversing it." Tobias was sufficiently motivated.

## Threat Modeling

### STRIDE

This scenario falls under **Information Disclosure**.

Debug symbols and non-obfuscated metadata disclose the app's internal architecture to an attacker, significantly reducing the effort required to identify vulnerabilities, reverse-engineer proprietary algorithms, or craft targeted attacks.

### What can go wrong?

- Internal class and method names reveal the app's architecture and proprietary logic.
- Function symbols in native binaries help attackers identify attack surfaces without dynamic analysis.
- Source file paths embedded in debug metadata reveal internal project structure and potentially sensitive information.

### What are we going to do about it?

- Enable ProGuard/R8 in all release builds (`minifyEnabled true`, `shrinkResources true`).
- Strip debug symbols from native `.so` files before packaging: `llvm-strip --strip-debug lib.so`.
- Remove all `.pdb`, `.dSYM`, and symbol-map files from the release artifact.
- Verify the release APK/IPA is properly obfuscated before distribution: decompile a sample and check for meaningful class/method names.
