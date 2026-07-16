## Scenario: Steve can access sensitive data by reading backups and/or local, internal, or external storage

Consider a scenario where Steve connects a device to his computer and takes an unencrypted ADB backup. The app developer had left `android:allowBackup="true"` in the manifest without configuring backup exclusions. Steve extracts the backup archive and finds the app's SQLite database containing account details, a preferences file with a stored session token, and a private key file in the app's files directory. The OS-level backup mechanism transferred everything faithfully.

1. `android:allowBackup="true"` (the default) allows `adb backup` to include all app data without device unlock on older Android versions.
2. Files written to external storage (`Environment.getExternalStorageDirectory()`) are world-readable and included in backups by default.
3. iTunes/Finder backups on iOS include app data by default unless files are marked with `isExcludedFromBackupKey`.
4. Cloud backups (Google Drive, iCloud) transmit local app data to remote storage, broadening the attack surface.

### Example

Steve buys a second-hand Android device. The seller did not perform a factory reset. Steve runs `adb backup -noapk com.target.app` — which works on Android versions below 12 without device unlock. He finds the banking app's database in the backup, containing the previous owner's full transaction history and a stored authentication token. The token is still valid because the previous owner had not explicitly logged out. Steve logs in using the token. The data migration to the new owner was complete, if unintentional.

## Threat Modeling

### STRIDE

This scenario falls under **Information Disclosure**.

Backup mechanisms — designed to help users preserve their data — inadvertently copy sensitive app data to locations accessible to attackers with device access, backup clients, or cloud storage access.

### What can go wrong?

- ADB backup extracts all app data from a device without requiring device unlock (on older Android versions).
- Cloud backups store sensitive data on servers that the user may not intend to share.
- Files on external storage are accessible by any app with `READ_EXTERNAL_STORAGE` permission and are included in device backups.
- Decommissioned devices with unwiped data expose the previous user's sensitive information.

### What are we going to do about it?

- Set `android:allowBackup="false"` for apps handling highly sensitive data; or configure detailed `<data-extraction-rules>` to exclude sensitive files and databases.
- Never store sensitive data on external storage; use internal storage with appropriate data-protection classes.
- On iOS, mark sensitive files as excluded from backup: `try url.setResourceValues(URLResourceValues(isExcludedFromBackup: true))`.
- Encrypt all sensitive data at rest with keys that are not included in backups.
- Implement server-side session invalidation to handle stolen devices; do not rely on local logout.
