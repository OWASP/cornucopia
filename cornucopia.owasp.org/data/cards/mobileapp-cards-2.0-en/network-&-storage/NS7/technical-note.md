## Technical Note: Steve can access sensitive data by reading backups and/or local, internal/external storage

### Platform Guidance

**Android:** Store only the minimum data needed, keep it in internal storage or encrypted databases, and exclude sensitive files from backup where appropriate.

```kotlin
<application android:allowBackup="false" android:fullBackupContent="@xml/backup_rules" />
```

**iOS:** Use Data Protection, keep files in the app container, and exclude secrets from iCloud backup unless the product explicitly requires it.

```swift
var values = URLResourceValues()
values.isExcludedFromBackup = true
try secretURL.setResourceValues(values)
```

### Relevant Tests

**Legacy Tests:** MASTG-TEST-0001, MASTG-TEST-0003, MASTG-TEST-0009, MASTG-TEST-0052, MASTG-TEST-0053, MASTG-TEST-0058
**New Tests:** MASTG-TEST-0216, MASTG-TEST-0297, MASTG-TEST-0388

### MASWE Weaknesses

- MASWE-0007: backup and local-storage weaknesses that expose app data at rest.
