## Platform-Aware Review Guidance

**Android NDK**
- Verify build flags in `CMakeLists.txt` or `Android.mk`: require `-fstack-protector-strong`, `-D_FORTIFY_SOURCE=2`, `-Wl,-z,relro,-z,now`, `-fPIE -pie`.
- Check compiled `.so` files with `readelf -d lib.so | grep -E 'FLAGS|BIND_NOW'`.
- Enable AddressSanitizer in debug builds: set `sanitizers = "address"` in the NDK Gradle DSL.
- MobSF's "Binary Analysis" section flags missing binary protections automatically.

**iOS**
- In Xcode Build Settings: `ENABLE_HARDENED_RUNTIME = YES`, `GCC_GENERATE_DEBUGGING_SYMBOLS` per environment.
- Verify stack canaries: `nm -a YourApp.app/YourApp | grep stack_chk`
- Use Instruments → Leaks to detect memory leaks during long-running test sessions.
- Swift ARC handles most memory management, but `UnsafePointer` and bridging code must be audited manually.

**Testing**
- Fuzz all input-parsing code paths in native libraries using libFuzzer or AFL.
- Review crash reports in Crashlytics or Sentry for SIGSEGV / SIGABRT patterns indicative of memory corruption.
- Run the app under Valgrind (on a Linux host simulator build) or an ASan-instrumented build.

**OWASP Mappings**
- MASVS: CODE-3, CODE-4
- MASTG: TEST-0043, TEST-0044, TEST-0086, TEST-0087, TEST-0222, TEST-0223, TEST-0228, TEST-0229, TEST-0230
- MASWE: MASWE-0116
