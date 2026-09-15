## Scenario: Steve can access sensitive data by reading backups and/or local, internal/external storage

### Example

Steve gives an old phone to a repair shop after deleting the travel app icon. The shop restores a backup and finds Steve’s saved boarding pass, so the technician knows his seat, destination, and unfortunate allergy to airplane peanuts.

Backups and local or removable storage must be protected and cleared according to the data’s sensitivity. Removing a shortcut does not erase the records an attacker can recover from the device.


## Threat Modeling

### STRIDE

This scenario is primarily **Tampering**, **Information Disclosure** in STRIDE. The named condition is: Steve can access sensitive data by reading backups and/or local, internal/external storage.

- **MAS-THREAT-0002:** Attackers can access or tamper with sensitive data stored in shared or external storage.
- **MAS-THREAT-0001:** Attackers can access sensitive data stored unencrypted in private storage.
- **MAS-THREAT-0006:** Attackers can extract or tamper with sensitive data included in backups.

- **MAS-ATTACK-0010:** Accessing shared or external storage from any app holding the corresponding permissions.
- **MAS-ATTACK-0011:** Physically removing and reading external storage media such as SD cards.
- **MAS-ATTACK-0005:** Accessing the device storage on a compromised device.
- **MAS-ATTACK-0007:** Accessing files exposed through incorrect file permissions or misconfigured content providers.
- **MAS-ATTACK-0008:** Extracting local or cloud backups of the device.
- **MAS-ATTACK-0009:** Tampering with backup contents and restoring the modified backup to a device.

### What can go wrong?

If Steve can access sensitive data by reading backups and/or local, internal/external storage, the failure is concrete rather than merely theatrical: the app could let an attacker cross the network-&-storage boundary and reach data or capability that this flow should protect. In this card, the practical route includes Accessing shared or external storage from any app holding the corresponding permissions. Also, Physically removing and reading external storage media such as SD cards. That can turn a normal user action into unauthorized access, disclosure, alteration, or service disruption; the mapped weakness entries below identify the exact implementation evidence to check.

Mapped weaknesses that sharpen the review:

- MASWE-0002 — Sensitive Data Stored Unencrypted Outside of Private Storage: This weakness occurs when an app stores sensitive data unencrypted in shared or external storage, where other apps can access it without any user interaction.
- MASWE-0001 — Sensitive Data Stored Unencrypted in Private Storage: This weakness occurs when an app stores sensitive data unencrypted in private storage locations, such as the application sandbox, where it can be exposed via incorrect file permissions, an app or device vulnerability, or data backup...
- MASWE-0006 — Sensitive Data Not Excluded From Backup: This weakness occurs when an app fails to exclude sensitive data from device backups, so that user and app secrets end up in cloud or local backup archives.

### What are we going to do about it?

Keep sensitive files and databases in scoped, encrypted storage, exclude them from backups when appropriate, and remove temporary copies; test local and external storage, backup extraction, file permissions, and restore behavior on both platforms.


Mapped MASTG tests:

- MASTG-TEST-0200 — Files Written to External Storage: The goal of this test is to retrieve the files written to the external storage (@MASTG-KNOW-0042) and inspect them regardless of the APIs used to write them. It uses a simple approach based on file retrieval from the device storage...
- MASTG-TEST-0201 — Runtime Use of APIs to Access External Storage: Android apps use a variety of APIs to access the external storage (@MASTG-KNOW-0042). Collecting a comprehensive list of these APIs can be challenging, especially if an app uses a third-party framework, loads code at runtime, or...
- MASTG-TEST-0207 — Runtime Storage of Unencrypted Data in the App Sandbox: The goal of this test is to retrieve the files written to the internal storage (@MASTG-KNOW-0041) and inspect them regardless of the APIs used to write them. It uses a simple approach based on file retrieval from the device storage...
- MASTG-TEST-0215 — Sensitive Data Not Marked For Backup Exclusion: This test verifies whether your app uses the `isExcludedFromBackup` API to instruct the system to exclude sensitive files from backups. This API does not guarantee the actual exclusion. According to the documentation:
- MASTG-TEST-0216 — Sensitive Data Not Excluded From Backup: This test verifies whether apps correctly instruct the system to exclude sensitive files from backups by performing a backup and restore of the app data and checking which files are restored.
- MASTG-TEST-0262 — References to Backup Configurations Not Excluding Sensitive Data: This test verifies whether apps correctly instruct the system to exclude sensitive files from backups by analyzing the app's AndroidManifest.xml and backup rule configuration files.
- MASTG-TEST-0287 — Runtime Storage of Unencrypted Data via the SharedPreferences API: In Android, applications can use the `SharedPreferences` API to store sensitive data without encryption, typically under the app's private data directory, such as `/data/user/0/<package-name>/shared_prefs/` or...
- MASTG-TEST-0298 — Runtime Monitoring of Files Eligible for Backup: This test logs every file system API use, such as `open`, `fopen`, `NSFileManager`, or `FileHandle` that creates or writes files to the app's data container at `/var/mobile/Containers/Data/Application/$APP_ID` to identify which files...
- MASTG-TEST-0304 — References to Sensitive Data Unencrypted via Android Room Database: The source provides the mapped security guidance for this control.
- MASTG-TEST-0305 — Sensitive Data Stored Unencrypted via DataStore: The source provides the mapped security guidance for this control.
- MASTG-TEST-0306 — References to Sensitive Data Stored Unencrypted via Android Room DB: The source provides the mapped security guidance for this control.

Mapped MASTG best practices:

- MASTG-BEST-0050 — Store Data Encrypted in App Sandbox Directory: Store sensitive data in `SharedPreferences` only after encrypting it. Standard `SharedPreferences` stores values in XML files inside the app's private data directory, so values such as credentials, authentication tokens, private keys,...
- MASTG-BEST-0023 — Exclude Sensitive Information from Backups: iOS does not provide a guaranteed mechanism to exclude files from backups. Setting `NSURLIsExcludedFromBackupKey` instructs the system not to include a file in backups, but it does not ensure exclusion. To reduce data exposure, apply...
- MASTG-BEST-0004 — Exclude Sensitive Data from Backups: For the sensitive files found, instruct the system to exclude them from the backup:

Mapped MASTG knowledge:

- MASTG-KNOW-0042 — External Storage: Android devices support shared external storage. This storage may be removable (such as an SD card) or emulated (non-removable). A malicious app with proper permissions running on Android 10 or below can access data that you write to...
- MASTG-KNOW-0041 — Internal Storage: You can save files to the device's internal storage. Files saved to internal storage are containerized by default and cannot be accessed by other apps on the device. When the user uninstalls your app, these files are removed.
- MASTG-KNOW-0102 — Backups: iOS includes auto-backup features that create copies of the data stored on the device. You can make iOS backups from your host computer by using iTunes (till macOS Catalina) or Finder (from macOS Catalina onwards), or via the iCloud...
- MASTG-KNOW-0050 — Backups: Android backups usually include copies of data and settings for all installed apps. Given its diverse ecosystem, Android supports many backup options:
- MASTG-KNOW-0036 — Shared Preferences: !!! warning
- MASTG-KNOW-0037 — SQLite Database: SQLite is an SQL database engine that stores data in `.db` files. The Android SDK has built-in support for SQLite databases. The main package used to manage the databases is `android.database.sqlite`.
