## Platform-Aware Review Guidance

**Android NDK**
- Compile flags: `-fstack-protector-strong -D_FORTIFY_SOURCE=2 -Wl,-z,relro,-z,now -fPIE -pie`
- Use AddressSanitizer in CI builds: `sanitizers = "address"` in the NDK Gradle DSL.
- Use `std::string`, `std::vector`, and bounded C++ STL containers instead of raw arrays where possible.
- Fuzz network protocol parsers: integrate libFuzzer or AFL into the native build.

**iOS**
- Enable Hardened Runtime: `ENABLE_HARDENED_RUNTIME = YES` in Xcode build settings.
- Use `strncpy`, `snprintf` with explicit length limits; avoid `strcpy`, `sprintf`, `gets`.
- Compile Swift code: managed by ARC; `UnsafePointer` usage must be individually audited.
- AddressSanitizer: enable in the scheme's diagnostics to catch memory errors during testing.

**Testing**
- Fuzz all external input-parsing code paths (network, file import, IPC) with a coverage-guided fuzzer.
- Monitor crash reports for SIGSEGV, SIGABRT, and bus errors indicative of memory corruption.
- Review binary security properties: `checksec --file lib.so` should show all protections enabled.

**OWASP Mappings**
- MASVS: CODE-3, CODE-4
- MASTG: TEST-0043, TEST-0044, TEST-0086, TEST-0087, TEST-0222, TEST-0223, TEST-0228, TEST-0229, TEST-0230
- MASWE: MASWE-0116
