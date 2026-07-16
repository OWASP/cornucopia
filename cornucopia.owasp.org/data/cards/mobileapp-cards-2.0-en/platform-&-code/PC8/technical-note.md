## Technical Note: Colin can expose sensitive data through the app's interprocess communication because the content provider's query methods are not properly parameterized and arguments sanitized

### Platform Guidance

**Android:** Treat `ContentProvider` arguments as untrusted input and use placeholders in queries; string concatenation belongs in horror stories, not selection clauses.

```kotlin
override fun query(
uri: Uri, projection: Array<String>?, selection: String?,
selectionArgs: Array<String>?, sortOrder: String?
): Cursor {
return db.query("secrets", projection, "owner_id = ?", selectionArgs, null, null, sortOrder)
}
```

**iOS:** If the iOS app exposes search or IPC-style parameters to shared components, parse them into typed values before they reach storage or SQL layers.

```swift
guard let accountId = Int(request.queryItems["accountId"] ?? "") else {
throw QueryError.invalidParameter
}
let rows = try db.prepare("SELECT * FROM secrets WHERE account_id = ?", [accountId])
```

### Relevant Tests

**Legacy Tests:** MASTG-TEST-0007, MASTG-TEST-0056
**New Tests:** MASTG-TEST-0289, MASTG-TEST-0334, MASTG-TEST-0381, MASTG-TEST-0290, MASTG-TEST-0370, MASTG-TEST-0390

### MASWE Weaknesses

- MASWE-0058, MASWE-0066, MASWE-0118: input sanitization failures in provider/query interfaces that expose or alter data.
