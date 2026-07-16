## Scenario: Matt can inspect sensitive application log data because logging statements have not been removed or reviewed as safe before the production release

Consider a scenario where Matt is a security researcher who installs a popular expense-tracker app and immediately runs `adb logcat` while using the app. Within three minutes of logging in, he sees the full session token printed to Logcat by a debug log statement, three database query results including account numbers, and the user's full name and email address. The developer logs were added during development and never removed. Matt did not need to exploit anything. The app gave him the data one log line at a time.

1. Debug log statements that print tokens, credentials, or sensitive data left in production releases are readable by any app with `READ_LOGS` permission, or by anyone with ADB access.
2. Crash reports and analytics SDKs may collect log data and transmit it to third parties.
3. On iOS, `NSLog` output is accessible on non-jailbroken devices via Xcode console when connected to a Mac, and on jailbroken devices via syslog.

### Example

Matt attaches `adb logcat -s MyApp:V` to the device. He logs into the expense tracker. The log shows:
```
D/AuthManager: Token: eyJhbGc...
D/DatabaseHelper: Query result: {name: "Matt", email: "matt@example.com", balance: 12345.67}
```
Matt now has a valid session token and knows more about "Matt's" finances than "Matt" would prefer. The log statements were left in from a debugging session the previous quarter. "It works in debug mode" is not a security argument.

## Threat Modeling

### STRIDE

This scenario falls under **Information Disclosure**.

Sensitive data is written to a system log that is accessible to other apps (with appropriate permissions), ADB-connected machines, crash reporting services, or anyone with physical access to a debug-connected device.

### What can go wrong?

- Session tokens logged in plaintext can be captured and replayed.
- PII (names, emails, account numbers) in logs violates data-protection regulations.
- Third-party crash-reporting SDKs that collect log context may exfiltrate sensitive data.
- On Android, apps with `READ_LOGS` permission can read the system log; pre-Android 4.1, any app could.

### What are we going to do about it?

- Remove all `Log.d`, `Log.v`, `System.out.println`, and equivalent statements that output sensitive data before production release.
- Use a logging library (Timber, OSLog) configured to compile out verbose/debug output in release builds.
- Never log: credentials, session tokens, full PII, payment details, health data, or encryption keys — in any build variant.
- Audit third-party SDK logging configurations; some SDKs have their own log levels that must be disabled separately.
- Include log-review in the pre-release security checklist.
