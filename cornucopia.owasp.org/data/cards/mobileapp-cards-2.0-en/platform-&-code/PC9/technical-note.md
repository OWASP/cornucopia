## Technical Note: Toby can modify or expose data by injection because the response from implicit intents is not properly validated

### Platform Guidance

**Android:** Validate the source, action, MIME type, and payload of every implicit intent result before trusting it.

```kotlin
override fun onActivityResult(requestCode: Int, resultCode: Int, data: Intent?) {
if (requestCode != IMPORT_REQUEST || resultCode != RESULT_OK) return
val uri = data?.data ?: return
require(contentResolver.getType(uri) == "application/json")
importFile(uri)
}
```

**iOS:** Treat callback URLs, document pickers, and shared extension responses as hostile until the app verifies scheme, source app, and content type.

```swift
func documentPicker(_ controller: UIDocumentPickerViewController, didPickDocumentsAt urls: [URL]) {
guard let url = urls.first, url.pathExtension == "json" else { return }
importDocument(at: url)
}
```

### Relevant Tests

**Legacy Tests:** MASTG-TEST-0026
**New Tests:** MASTG-TEST-0223, MASTG-TEST-0375, MASTG-TEST-0230

### MASWE Weaknesses

- MASWE-0076, MASWE-0084: untrusted response handling and injection via cross-app messaging results.
