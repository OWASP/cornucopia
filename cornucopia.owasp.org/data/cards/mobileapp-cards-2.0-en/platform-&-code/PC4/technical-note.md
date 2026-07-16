## Technical Note: Kelly can expose sensitive data by taking advantage of the app's excessive permissions connected to the app's use of location, camera, microphone, storage, etc

### Platform Guidance

**Android:** Ask only for runtime permissions that match a visible user action, and fail closed when the user denies them.

```kotlin
private val cameraPermission = registerForActivityResult(
ActivityResultContracts.RequestPermission()
) { granted ->
if (granted) openCamera() else showPermissionRationale()
}

fun startScan() = cameraPermission.launch(Manifest.permission.CAMERA)
```

**iOS:** Keep each capability tied to an Info.plist usage description and gate access in code so background collection does not become a surprise subscription plan.

```swift
let status = AVCaptureDevice.authorizationStatus(for: .video)
if status == .authorized {
startCapture()
} else {
AVCaptureDevice.requestAccess(for: .video) { granted in
    if granted { DispatchQueue.main.async { self.startCapture() } }
}
}
```

### Relevant Tests

**Legacy Tests:** MASTG-TEST-0024, MASTG-TEST-0069
**New Tests:** MASTG-TEST-0252, MASTG-TEST-0315, MASTG-TEST-0364, MASTG-TEST-0278, MASTG-TEST-0336, MASTG-TEST-0379

### MASWE Weaknesses

- MASWE-0055, MASWE-0063, MASWE-0072: excessive platform permissions, overbroad entitlements, and misuse of privileged sensors or OS resources.
