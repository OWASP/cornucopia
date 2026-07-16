## Platform-Aware Review Guidance

**Android**
- `android:allowBackup="false"` in `<application>`: prevents all `adb backup` extraction.
- `res/xml/data_extraction_rules.xml` (Android 12+) and `res/xml/backup_rules.xml` (older): configure `<exclude>` rules for sensitive databases and preference files.
- Never write sensitive data to `getExternalStorageDirectory()` or any path under `Environment.DIRECTORY_*`; use `getFilesDir()` or `getCacheDir()`.
- Use `FileInputStream` with a key from the KeyStore to encrypt files stored locally.

**iOS**
- Mark files as excluded from iCloud/iTunes backup:
  ```swift
  var values = URLResourceValues(); values.isExcludedFromBackup = true; try url.setResourceValues(values)
  ```
- Use `NSFileProtectionComplete` for sensitive files: encrypted until first unlock; inaccessible while locked.
- Keychain items with `kSecAttrAccessibleWhenPasscodeSetThisDeviceOnly` are not included in backups (not extractable from backup).

**Testing**
- Run `adb backup -apk -shared com.target.app` and inspect the resulting `.ab` file for sensitive data.
- On iOS, capture an iTunes backup and use iMazing or similar tools to inspect app data.
- Check `android:allowBackup` in the merged manifest and verify the backup exclusion rules cover all sensitive files.

**OWASP Mappings**
- MASVS: AUTH-1, CRYPTO-2, PRIVACY-1, STORAGE-1, STORAGE-2
- MASTG: TEST-0001, TEST-0003, TEST-0009, TEST-0052, TEST-0053, TEST-0058, TEST-0072, TEST-0079, TEST-0200, TEST-0201, TEST-0202, TEST-0207, TEST-0215, TEST-0216, TEST-0262, TEST-0287, TEST-0298, TEST-0299, TEST-0300, TEST-0301, TEST-0302, TEST-0303, TEST-0304, TEST-0305, TEST-0306, TEST-0388
- MASWE: MASWE-0002, MASWE-0003, MASWE-0004, MASWE-0006, MASWE-0007, MASWE-0036
