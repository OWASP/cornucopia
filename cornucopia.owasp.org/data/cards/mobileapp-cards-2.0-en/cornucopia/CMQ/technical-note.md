## Technical Note: Victor can patch the app and use it to distribute malicious code because the runtime integrity checks are not strong enough according to what is recommended or the perceived effort of a potential attacker

### Platform Guidance

**Android:** If the app can distribute code, scripts, or active content, gate that path behind runtime integrity and signed-update validation.

```kotlin
val apkHash = sha256(packageArchive)
require(apkHash == trustedManifest.expectedHash)
```

**iOS:** Only accept distributable content from signed and integrity-checked sources, and have the service refuse artifacts from tampered clients.

```swift
guard manifest.signatureValid, manifest.bundleHash == localHash else {
throw IntegrityError.modified
}
```

### Relevant Tests

**Legacy Tests:** MASTG-TEST-0050
**New Tests:** MASTG-TEST-0338, MASTG-TEST-0354

### MASWE Weaknesses

- MASWE-0099: runtime integrity gaps that let a patched app spread malicious content.
