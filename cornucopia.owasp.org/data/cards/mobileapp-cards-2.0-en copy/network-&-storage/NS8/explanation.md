## Scenario: Taher can expose or modify sensitive data at rest because encryption or integrity protections are inadequate

### Example

Taher stores a salary spreadsheet on a shared tablet with a decorative lock icon but no real encryption or integrity check. A mischievous colleague changes the bonus column, and payroll announces that the office goldfish is now the highest-paid employee.

Data at rest needs authenticated encryption and protected storage suited to its threat model. Confidentiality without integrity, or an unlocked database with a reassuring picture, cannot stop disclosure or tampering.


## Threat Modeling

### STRIDE

This scenario is primarily **Tampering**, **Information Disclosure** in STRIDE. The named condition is: Taher can expose or modify sensitive data at rest because encryption or integrity protections are inadequate.

- **MAS-THREAT-0002:** Attackers can access or tamper with sensitive data stored in shared or external storage.
- **MAS-THREAT-0001:** Attackers can access sensitive data stored unencrypted in private storage.
- **MAS-THREAT-0057:** Attackers can alter the app's behavior through its resources.

- **MAS-ATTACK-0010:** Accessing shared or external storage from any app holding the corresponding permissions.
- **MAS-ATTACK-0011:** Physically removing and reading external storage media such as SD cards.
- **MAS-ATTACK-0005:** Accessing the device storage on a compromised device.
- **MAS-ATTACK-0007:** Accessing files exposed through incorrect file permissions or misconfigured content providers.
- **MAS-ATTACK-0008:** Extracting local or cloud backups of the device.
- **MAS-ATTACK-0009:** Tampering with backup contents and restoring the modified backup to a device.
- **MAS-ATTACK-0070:** Modifying the app's files or resources on a compromised device.

### What can go wrong?

If Taher can expose or modify sensitive data at rest because encryption or integrity protections are inadequate, the failure is concrete rather than merely theatrical: the app could let an attacker cross the network-&-storage boundary and reach data or capability that this flow should protect. In this card, the practical route includes Accessing shared or external storage from any app holding the corresponding permissions. Also, Physically removing and reading external storage media such as SD cards. That can turn a normal user action into unauthorized access, disclosure, alteration, or service disruption; the mapped weakness entries below identify the exact implementation evidence to check.

Mapped weaknesses that sharpen the review:

- MASWE-0002 — Sensitive Data Stored Unencrypted Outside of Private Storage: This weakness occurs when an app stores sensitive data unencrypted in shared or external storage, where other apps can access it without any user interaction.
- MASWE-0001 — Sensitive Data Stored Unencrypted in Private Storage: This weakness occurs when an app stores sensitive data unencrypted in private storage locations, such as the application sandbox, where it can be exposed via incorrect file permissions, an app or device vulnerability, or data backup...
- MASWE-0057 — App Resources Integrity Not Verified: This weakness occurs when an app does not verify that the resources it relies on have not been tampered with.

### What are we going to do about it?

Protect stored data with AEAD and platform-backed keys, authenticate records before use, and keep keys separate from the database; test encrypted storage, backup extraction, tampering, lock-state access, and migration failure paths.


Mapped MASTG tests:

- MASTG-TEST-0200 — Files Written to External Storage: The goal of this test is to retrieve the files written to the external storage (@MASTG-KNOW-0042) and inspect them regardless of the APIs used to write them. It uses a simple approach based on file retrieval from the device storage...
- MASTG-TEST-0201 — Runtime Use of APIs to Access External Storage: Android apps use a variety of APIs to access the external storage (@MASTG-KNOW-0042). Collecting a comprehensive list of these APIs can be challenging, especially if an app uses a third-party framework, loads code at runtime, or...
- MASTG-TEST-0207 — Runtime Storage of Unencrypted Data in the App Sandbox: The goal of this test is to retrieve the files written to the internal storage (@MASTG-KNOW-0041) and inspect them regardless of the APIs used to write them. It uses a simple approach based on file retrieval from the device storage...
- MASTG-TEST-0299 — Data Protection Classes for Files in Private Storage: This test retrieves the data protection classes of files created or modified in the app's local storage during typical app usage. The goal is to ensure that files containing sensitive data are assigned appropriate data protection...
- MASTG-TEST-0300 — References to APIs for Storing Unencrypted Data in Private Storage: This test checks whether the app writes unencrypted sensitive data to private storage. It focuses on:
- MASTG-TEST-0301 — Runtime Use of APIs for Storing Unencrypted Data in Private Storage: This test is the dynamic counterpart to @MASTG-TEST-0300 and is designed to be used together with @MASTG-TEST-0302.
- MASTG-TEST-0302 — Sensitive Data Unencrypted in Private Storage Files: This test is designed to complement @MASTG-TEST-0301. Instead of monitoring APIs during execution, it performs a differential analysis of the app's private storage by comparing snapshots taken before and after exercising the app. It...
- MASTG-TEST-0303 — References to APIs for Storing Unencrypted Data in Shared Storage: This test checks whether the app stores sensitive data without encryption in iOS sandbox locations that may become user accessible when file sharing is enabled.
- MASTG-TEST-0304 — References to Sensitive Data Unencrypted via Android Room Database: The source provides the mapped security guidance for this control.
- MASTG-TEST-0305 — Sensitive Data Stored Unencrypted via DataStore: The source provides the mapped security guidance for this control.
- MASTG-TEST-0306 — References to Sensitive Data Stored Unencrypted via Android Room DB: The source provides the mapped security guidance for this control.
- MASTG-TEST-0338 — References to Storage Integrity Check APIs: Android apps can protect the integrity and authenticity of data they store on the device (e.g., in `SharedPreferences`, files, or databases) by computing an HMAC or a digital signature over the data and verifying it before use (see...
- MASTG-TEST-0387 — References to Storage Integrity Check APIs: iOS apps can protect the integrity and authenticity of data they store on the device (e.g., files in the Documents directory, `UserDefaults`/`NSUserDefaults`, or databases) by computing an HMAC or a digital signature over the data and...

Mapped MASTG best practices:

- MASTG-BEST-0050 — Store Data Encrypted in App Sandbox Directory: Store sensitive data in `SharedPreferences` only after encrypting it. Standard `SharedPreferences` stores values in XML files inside the app's private data directory, so values such as credentials, authentication tokens, private keys,...
- MASTG-BEST-0024 — Store Data Encrypted in App Sandbox Directory: Choose the right location for storing the app's and the user's data to the app sandbox: use **Documents** directory to store user-generated content and **Library** directory for app's internal data.
- MASTG-BEST-0066 — Implementing Storage Integrity Checks on Android: Implement storage integrity checks in Android apps to detect unauthorized modifications to data stored on the device (for example, in `SharedPreferences`, files, or databases). These checks raise the cost for attackers who try to tamper...
- MASTG-BEST-0065 — Implementing Storage Integrity Checks on iOS: Implement storage integrity checks in iOS apps to detect unauthorized modifications to data stored on the device (for example, in the Keychain, `UserDefaults`/`NSUserDefaults`, files, or databases). These checks raise the cost for...

Mapped MASTG knowledge:

- MASTG-KNOW-0042 — External Storage: Android devices support shared external storage. This storage may be removable (such as an SD card) or emulated (non-removable). A malicious app with proper permissions running on Android 10 or below can access data that you write to...
- MASTG-KNOW-0041 — Internal Storage: You can save files to the device's internal storage. Files saved to internal storage are containerized by default and cannot be accessed by other apps on the device. When the user uninstalls your app, these files are removed.
- MASTG-KNOW-0082 — App Extensions: Starting with iOS 8, Apple introduced App Extensions. App extensions let an app offer custom functionality and content to users while they interact with other apps or the system. Each extension implements a single, well-scoped task, for...
- MASTG-KNOW-0091 — File System APIs: iOS apps can write data to the file system using various APIs, depending on the use case.
- MASTG-KNOW-0108 — App Sandbox Directories: On iOS, each application gets a sandboxed folder to store its data. As per the iOS security model, an application's sandboxed folder cannot be accessed by another application. Additionally, the users do not have direct access to the iOS...
- MASTG-KNOW-0057 — Keychain Services: The iOS keychain APIs can (and should) be used to implement local authentication. During this process, the app stores either a secret authentication token or another piece of secret data identifying the user in the keychain. In order to...
- MASTG-KNOW-0122 — Document Picker, Document Interaction, and Open in Place: iOS provides several mechanisms for exchanging files between apps. These mechanisms are user-mediated: the user chooses which files to share, open, import, or export, and which apps or locations are involved.
- MASTG-KNOW-0037 — SQLite Database: SQLite is an SQL database engine that stores data in `.db` files. The Android SDK has built-in support for SQLite databases. The main package used to manage the databases is `android.database.sqlite`.
- MASTG-KNOW-0036 — Shared Preferences: !!! warning
- MASTG-KNOW-0086 — Storage Integrity Checks: Apps can protect data they store on the device (for example in the Keychain, `UserDefaults`/`NSUserDefaults`, or a database) by computing an HMAC or cryptographic signature over it and verifying that value before each use. This lets the...
