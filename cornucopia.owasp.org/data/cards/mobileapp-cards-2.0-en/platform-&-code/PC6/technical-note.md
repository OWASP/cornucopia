## Platform-Aware Review Guidance

**Android**
- Audit all `<activity>`, `<service>`, `<receiver>`, `<provider>` elements in `AndroidManifest.xml` for `android:exported="true"` without a matching `android:permission`.
- Use `adb shell dumpsys package <package>` to list exported components at runtime.
- Migrate from deprecated `LocalBroadcastManager` to direct function calls, LiveData, or Kotlin Flows for in-process events.
- For `ContentProvider`, set separate `android:readPermission` and `android:writePermission` with `protectionLevel="signature"`.

**iOS**
- Prefer Universal Links (`apple-app-site-association`) over custom URL schemes for deep links and OAuth redirects.
- In `application(_:open:options:)`, validate `options[.sourceApplication]` where available and require a CSRF-resistant `state` parameter.
- Restrict `UIPasteboard.general` writes to non-sensitive data; use named pasteboards with expiration for ephemeral sensitive data.
- Review `NSExtensionActivationRule` in app extensions to prevent them receiving sensitive content types unnecessarily.

**Testing**
- Use Drozer: `run app.broadcast.send` to craft broadcasts to exported receivers.
- Use `adb shell am broadcast` and `am start` to invoke exported components with crafted extras.
- On iOS, install a companion test app that registers the same custom URL scheme and verify the target app validates the `state` parameter.

**OWASP Mappings**
- MASVS: PLATFORM-1, STORAGE-1, STORAGE-2
- MASTG: TEST-0029, TEST-0030, TEST-0071, TEST-0072, TEST-0364, TEST-0365, TEST-0366, TEST-0389, TEST-0390
- MASWE: MASWE-0059, MASWE-0060, MASWE-0061, MASWE-0062, MASWE-0063, MASWE-0065, MASWE-0119
