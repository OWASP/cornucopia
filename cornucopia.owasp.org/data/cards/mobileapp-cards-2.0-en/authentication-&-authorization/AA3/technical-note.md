## Platform-Aware Review Guidance

**Android**
- Audit all `<activity>`, `<service>`, `<receiver>`, `<provider>` elements: `android:exported="true"` without `android:permission` is a finding.
- For custom permissions: verify the `<permission>` declaration is in the same manifest as the `android:permission` reference; use `protectionLevel="signature"`.
- Verify no orphaned permissions: all `android:permission` values must reference a `<permission>` that will be installed alongside the protected app.
- CVE-2019-2200 (Android < 10): race condition in custom permission claiming — ensure `minSdkVersion` is 29+, or document the risk.
- `Binder.getCallingUid()` inside components: validate the calling package using `PackageManager.getNameForUid()`.

**iOS**
- Review the `.entitlements` file for overly broad keychain access groups, App Group identifiers, and associated domains.
- Use `com.apple.developer.associated-domains` only for domains you control.
- Avoid broad `com.apple.security.application-groups` sharing unless multiple apps in the group are all trusted.
- Entitlement values are verified by the App Store and on-device at install time; incorrect values cause launch failures.

**Testing**
- Use Drozer: `run app.activity.start --component com.target.app com.target.app.SensitiveActivity`
- Check whether the activity/service/provider launches without triggering an authentication prompt.
- Review the merged manifest for all exported components.

**OWASP Mappings**
- MASVS: AUTH-1, AUTH-3
- MASTG: TEST-0024, TEST-0032, TEST-0069, TEST-0077
- MASWE: (see MASVS references above)
