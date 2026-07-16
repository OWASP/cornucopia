## Platform-Aware Review Guidance

**Android**
- ProGuard/R8: `-assumenosideeffects class android.util.Log { public static *** d(...); public static *** v(...); }` strips debug/verbose log calls.
- `BuildConfig.DEBUG`: ensure the release build has `DEBUG = false`; verify in the APK's `BuildConfig.class`.
- MobSF static analysis: check "Hardcoded Secrets" and "Debug Mode Enabled" findings.
- Remove test activities, test broadcast receivers, and diagnostic endpoints from the release manifest.

**iOS**
- `DEBUG` conditional compilation: `#if DEBUG ... #endif` for any code that should not appear in release builds.
- `os_log` with `.debug` level is not included in archived logs from non-development devices, but `print()` and `NSLog()` are always active — replace with `os_log` at appropriate levels.
- Archive and export the release IPA; run `strings` on the binary to check for hardcoded test credentials or debug flags.

**Testing**
- Run `adb logcat` against the production release build during normal usage; verify no sensitive data or debug output appears.
- Decompile the APK with jadx and search for `BuildConfig.DEBUG`, `"debug"`, `"test"` string constants.
- Review the production binary for debug symbols: `nm -a YourApp | grep -i debug`.

**OWASP Mappings**
- MASVS: RESILIENCE-3
- MASTG: TEST-0041, TEST-0084, TEST-0263, TEST-0264, TEST-0265, TEST-0358, TEST-0359
- MASWE: MASWE-0094, MASWE-0095
