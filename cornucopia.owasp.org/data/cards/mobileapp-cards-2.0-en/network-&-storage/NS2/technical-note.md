## Platform-Aware Review Guidance

**Android**
- Use `BuildConfig.DEBUG` guards: `if (BuildConfig.DEBUG) Log.d(TAG, sensitiveData)` — release builds will not execute the log call.
- ProGuard/R8: add `-assumenosideeffects` rules to strip `Log.*` calls from release builds automatically.
- Use Timber: configure `Timber.plant(Timber.DebugTree())` only in debug builds.
- `adb logcat -s <TAG>:V` to verify no sensitive data appears during normal usage in a release build.

**iOS**
- `os_log` (Unified Logging): messages at `.debug` and `.info` levels are not included in log archives from non-debug devices; `.default`, `.error`, and `.fault` levels are persistent.
- Never log sensitive data at `.default` level or above; do not use `print()` or `NSLog()` for anything that might include tokens or PII.
- In release builds, sensitive parameters should be redacted in log messages: `os_log("User authenticated: %{private}s", username)` — the `{private}` annotation prevents the value appearing in non-developer logs.

**Testing**
- Run `adb logcat` while performing sensitive operations (login, payment, data view) in a release build; verify no sensitive data is logged.
- On iOS, capture a syslog trace from a connected device via Xcode → Devices → Console; review for sensitive data.
- Review crash reports in Crashlytics/Sentry for any breadcrumb or log entries containing PII or tokens.

**OWASP Mappings**
- MASVS: PRIVACY-1, STORAGE-2
- MASTG: TEST-0003, TEST-0053, TEST-0203, TEST-0231, TEST-0296, TEST-0297
- MASWE: MASWE-0001
