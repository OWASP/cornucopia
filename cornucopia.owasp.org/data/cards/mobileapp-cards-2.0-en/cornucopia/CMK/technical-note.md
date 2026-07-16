## Platform-Aware Review Guidance

**Android**
- All imported data that is stored in SQLite must use parameterized queries via `ContentValues` or Room's type-safe DAOs.
- WebView rendering of imported content: use `webView.loadData(sanitizedHtml, "text/html", "UTF-8")` only after sanitizing the content.
- File import path validation: canonicalize and check paths against the expected import directory.

**iOS**
- Core Data: use `NSPredicate(format:argumentArray:)` — never interpolate imported values into the format string.
- `WKWebView` rendering of imported content: sanitize HTML with a trusted server-side or client-side HTML sanitizer before loading.
- File import: validate `UTType` of imported files before processing.

**Testing**
- Import a file containing SQL injection payloads; verify the database is not corrupted.
- Import a file containing JavaScript in text fields; render the fields in the UI and verify no script executes.
- Share crafted data with the app and verify the sharing format is validated against a schema.

**OWASP Mappings**
- MASVS: CODE-4, RESILIENCE-2
- MASTG: TEST-0034, TEST-0047, TEST-0079, TEST-0090, TEST-0337, TEST-0386
- MASWE: MASWE-0079, MASWE-0080, MASWE-0081, MASWE-0082, MASWE-0085, MASWE-0087, MASWE-0088
