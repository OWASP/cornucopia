## Platform-Aware Review Guidance

**Android — Tapjacking**
- On sensitive views: `view.setFilterTouchesWhenObscured(true)` or `android:filterTouchesWhenObscured="true"` in XML.
- Set `FLAG_SECURE` on authentication Activities to prevent screen captures and reduce overlay utility.
- On Android 12+, the `HIDE_OVERLAY_WINDOWS` permission allows apps to request that `SYSTEM_ALERT_WINDOW` overlays are not shown over them; request it if your threat model warrants it.

**Android — StrandHogg**
- Set `android:taskAffinity=""` on Activities that handle authentication to prevent task reparenting.
- Set `android:allowTaskReparenting="false"` on the main activity.
- StrandHogg 2.0 (CVE-2020-0096) was patched in Android 11; set `minSdkVersion >= 30` or document the risk.

**Android/iOS — URL Scheme Hijacking**
- Android: use App Links (`android:autoVerify="true"` with a verified domain association file) instead of custom schemes for OAuth redirects.
- iOS: use Universal Links instead of custom URL schemes for OAuth redirects; Universal Links require domain ownership verification.
- Validate the PKCE `code_verifier` server-side for all OAuth flows to make intercepted authorization codes unusable without the verifier.

**Testing**
- On Android, use `adb shell dumpsys window windows` during authentication to detect overlays.
- Register a second app with the same custom URL scheme and verify the OS or app rejects the hijack attempt.

**OWASP Mappings**
- MASVS: AUTH-1, CODE-1, CODE-4, PLATFORM-1, PLATFORM-3
- MASTG: TEST-0025, TEST-0030, TEST-0035, TEST-0072, TEST-0075
- MASWE: MASWE-0039, MASWE-0056, MASWE-0057
