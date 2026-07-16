## Scenario: Sebastien can disclose sensitive data or internal behaviour because debug code, verbose diagnostics, test resources, or unsafe runtime logging remain in the production app

Consider a scenario where Sebastien downloads the production release of a payment app and immediately runs `adb logcat`. Within seconds, he sees verbose debug logs: database query strings, internal state machine transitions, and a `DEBUG: Skipping cert validation for test` message indicating that a certificate-validation override was left in the production binary. The developer had a deadline and promoted the debug build to production. Nobody noticed until Sebastien did.

1. Debug log statements that print internal state, queries, and flags are readable via ADB or on jailbroken devices.
2. Test credentials, hardcoded bypass flags, and diagnostic endpoints left in production create exploitable shortcuts.
3. Verbose error messages that reveal stack traces, class names, or internal queries assist an attacker in understanding the app's architecture.

### Example

Sebastien finds a `BuildConfig.DEBUG = true` reference in the production APK's string constants. He decompiles the app with jadx and finds a branch that, when `DEBUG == true`, skips certificate pinning validation. He confirms this by observing that Burp Suite intercepts app traffic without certificate errors in the "production" build. The release build was compiled with `debug` variant by mistake. It shipped to 200,000 users.

## Threat Modeling

### STRIDE

This scenario falls under **Information Disclosure** and **Elevation of Privilege**.

Debug artifacts expose internal details that reduce an attacker's reconnaissance effort and may include security bypasses that directly elevate privileges.

### What can go wrong?

- Certificate validation bypasses left in production allow MITM attacks.
- Debug flags enable hidden admin panels or test accounts.
- Verbose logs expose session tokens, database queries, and internal state to ADB or crash-reporting services.
- Test credentials in the binary allow authentication without valid user credentials.

### What are we going to do about it?

- Use build variants strictly: all debug-only code behind `if (BuildConfig.DEBUG)` guards; release builds must use the release variant.
- Remove all `Log.d`, `Log.v`, and equivalent verbose logs from release builds via ProGuard strip rules.
- Audit the production APK/IPA for debug symbols, test credentials, hardcoded bypass flags, and debug endpoints.
- Include a "debug artifact removal" step in the release checklist and automate it with static analysis.
