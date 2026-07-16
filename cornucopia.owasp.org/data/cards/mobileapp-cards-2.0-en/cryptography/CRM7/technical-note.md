## Platform-Aware Review Guidance

**Android**
- SQLCipher: encrypt SQLite databases with a key from the `KeyStore`. `SQLiteDatabase.openOrCreateDatabase(path, passphrase, ...)`.
- Room + SQLCipher: `SupportFactory(passphrase)` in `Room.databaseBuilder`.
- `EncryptedSharedPreferences` / `EncryptedFile` from Jetpack Security: AES-256-GCM encryption backed by the `KeyStore`.
- External storage files should not contain sensitive data; if they must, apply application-level encryption before writing.

**iOS**
- `NSFileProtectionComplete` for sensitive files: encrypted when the device is locked; set via `setAttributes([.protectionKey: FileProtectionType.complete], ofItemAtPath:)`.
- Keychain: stores small amounts of sensitive data (tokens, keys, passwords) with built-in encryption and access control.
- CoreData with SQLite backing: does not encrypt by default; use SQLCipher-CoreData integration for at-rest encryption, or encrypt sensitive attributes individually.

**Testing**
- On a rooted/jailbroken device, access the app's database file and verify it is not readable as plaintext.
- Pull an ADB backup and inspect all files for plaintext sensitive data.

**OWASP Mappings**
- MASVS: CRYPTO-2, STORAGE-1
- MASTG: TEST-0001, TEST-0013, TEST-0052, TEST-0062, TEST-0072, TEST-0079, TEST-0207, TEST-0287, TEST-0299, TEST-0300, TEST-0301, TEST-0302, TEST-0304, TEST-0305, TEST-0306, TEST-0388
- MASWE: MASWE-0006
