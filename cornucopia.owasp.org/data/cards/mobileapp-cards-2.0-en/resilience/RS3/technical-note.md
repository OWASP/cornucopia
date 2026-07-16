## Platform-Aware Review Guidance

**Android**
- `build.gradle`: `buildTypes { release { minifyEnabled true; proguardFiles getDefaultProguardFile('proguard-android-optimize.txt'), 'proguard-rules.pro' } }`
- Strip native symbols: in `CMakeLists.txt`, set `CMAKE_BUILD_TYPE=Release`; or use `llvm-strip --strip-all`.
- Verify obfuscation: `jadx app-release.apk` — class names should appear as `a`, `b`, `c` etc. for obfuscated code.
- Remove assets bundled debug symbol files: grep the APK for `.pdb`, `.dSYM`, `.map` files.

**iOS**
- Export the app with the "Strip Debug Symbols During Copy" Xcode setting enabled.
- dSYM files are generated for crash symbolication but should NOT be included in the distributed IPA; they are stored separately.
- Verify: `nm -a YourApp.app/YourApp | grep -v "^U"` — strip-debug should reduce symbols significantly.
- Swift type metadata may still reveal some structure in release builds; consider obfuscation tools for high-risk apps.

**Testing**
- Decompile the release APK/IPA and verify class names are meaningless after obfuscation.
- Run `strings` on native binaries and verify no function names or source paths are visible.
- Check the APK's assets directory for accidentally bundled symbol files.

**OWASP Mappings**
- MASVS: RESILIENCE-3
- MASTG: TEST-0040, TEST-0083, TEST-0219, TEST-0288
- MASWE: MASWE-0093
