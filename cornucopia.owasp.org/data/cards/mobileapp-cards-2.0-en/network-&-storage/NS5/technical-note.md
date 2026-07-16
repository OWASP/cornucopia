## Platform-Aware Review Guidance

**Android**
- Enumerate all databases and files in `getFilesDir()`, `getCacheDir()`, and `getExternalFilesDir()` after SDK initialisation to identify unexpected storage.
- Configure `android:allowBackup="false"` or use `<backup-rules>` / `<cloud-backup-rules>` to exclude sensitive SDK-generated files from Auto Backup.
- `NotificationCompat.Builder.setVisibility(NotificationCompat.VISIBILITY_SECRET)` hides notification content on the lock screen.
- Set notification channel importance to prevent cached payloads from persisting; review push SDK documentation for payload caching behaviour.

**iOS**
- Review what third-party SDKs write to the Documents, Library/Application Support, Library/Caches, and tmp directories.
- Sensitive data in Library/Application Support is included in iTunes/Finder backups by default; exclude specific files using `URLResourceKey.isExcludedFromBackupKey`.
- Use `UNNotificationContent` without PII in push payloads; deliver sensitive content via a Notification Service Extension that enriches the notification only after the device is unlocked.
- Notification Centre caches notification payloads; review the push payload for PII.

**Testing**
- Use MobSF's dynamic analysis to enumerate all files created by the app (including SDKs) during a test session.
- Capture a `adb backup` or iTunes backup and inspect all files for unexpected sensitive data.
- Review each third-party SDK's privacy documentation and data-processing agreement.

**OWASP Mappings**
- MASVS: PLATFORM-3, STORAGE-2
- MASTG: TEST-0004, TEST-0005, TEST-0054, TEST-0315
- MASWE: MASWE-0054
