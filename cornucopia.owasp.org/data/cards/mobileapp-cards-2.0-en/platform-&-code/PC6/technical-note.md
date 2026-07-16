## Technical Note: Dawn can expose and intercept sensitive functionality through interprocess communication because permissions for broadcast and sharing are not set, not narrow enough or because sensitive functionality isn't appropriately excluded when sharing

### Platform Guidance

**Android:** Mark exported IPC components explicitly, require signature-level permissions where possible, and strip sensitive extras before sharing.

```kotlin
<provider
android:name=".SecureProvider"
android:exported="false"
android:grantUriPermissions="false" />

<permission
android:name="com.example.SECURE_SHARE"
android:protectionLevel="signature" />
```

**iOS:** For app extensions and URL-based sharing, only pass minimally scoped data and validate the caller context before honoring a request.

```swift
func scene(_ scene: UIScene, openURLContexts contexts: Set<UIOpenURLContext>) {
guard let url = contexts.first?.url, url.scheme == "trustedapp" else { return }
handleTrustedShare(url)
}
```

### Relevant Tests

**Legacy Tests:** MASTG-TEST-0029, MASTG-TEST-0030, MASTG-TEST-0071
**New Tests:** MASTG-TEST-0253, MASTG-TEST-0316, MASTG-TEST-0365, MASTG-TEST-0279, MASTG-TEST-0346, MASTG-TEST-0380

### MASWE Weaknesses

- MASWE-0056, MASWE-0064, MASWE-0073: unsafe IPC exposure, exported components, and overbroad sharing channels.
