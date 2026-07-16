## Platform-Aware Review Guidance

**Android**
- `android:debuggable="true"` must not appear in release `AndroidManifest.xml`. ProGuard/R8 build types set it to `false` by default.
- Runtime check:
  ```kotlin
  val isDebuggable = applicationInfo.flags and ApplicationInfo.FLAG_DEBUGGABLE != 0
  if (isDebuggable) { /* terminate or restrict */ }
  ```
- Verify in CI: `aapt dump badging app-release.apk | grep debuggable` should return nothing or `false`.
- ADB daemon attaches to debuggable apps without root; verify `adb jdwp` does not list your app's process in a release build.

**iOS**
- Production builds signed with App Store distribution certificate cannot be debugged with lldb without a provisioning profile override.
- Detect debugger attachment at runtime:
  ```swift
  var info = kinfo_proc(); var size = MemoryLayout.stride(ofValue: info)
  var mib: [Int32] = [CTL_KERN, KERN_PROC, KERN_PROC_PID, getpid()]
  sysctl(&mib, 4, &info, &size, nil, 0)
  let isBeingDebugged = (info.kp_proc.p_flag & P_TRACED) != 0
  ```
- Anti-debugging checks are a defence-in-depth measure; hardware-backed key protection is the primary control.

**Testing**
- Run `adb jdwp` while the production app is running; verify no PID is listed.
- Attempt `jdb -attach localhost:$(adb jdwp | head -1)` on the production app; verify it fails.
- Verify `aapt dump badging release.apk | grep debuggable` shows no debuggable flag.

**OWASP Mappings**
- MASVS: PLATFORM-2, RESILIENCE-3, RESILIENCE-4
- MASTG: TEST-0039, TEST-0082, TEST-0226, TEST-0227, TEST-0261
- MASWE: MASWE-0067, MASWE-0074, MASWE-0095
