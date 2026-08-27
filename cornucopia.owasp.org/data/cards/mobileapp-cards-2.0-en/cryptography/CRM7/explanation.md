## Scenario: Hassan can extract or modify sensitive data because it's stored without adequate encryption or platform data-protection controls

### Example

Hassan leaves a tablet containing an unencrypted inventory database in an airport lounge while fetching tea. Someone copies the file, edits the stock count, and orders 900 rubber ducks; the warehouse now has a migration problem.

Sensitive data at rest needs encryption and the platform’s protected storage controls. Otherwise a stolen or shared device can reveal or modify records without overcoming any meaningful barrier.


## Threat Modeling

### STRIDE

This scenario is primarily **Tampering**, **Information Disclosure** in STRIDE. The named condition is: Hassan can extract or modify sensitive data because it's stored without adequate encryption or platform data-protection controls.

- **MAS-THREAT-0002:** Attackers can access or tamper with sensitive data stored in shared or external storage.
- **MAS-THREAT-0001:** Attackers can access sensitive data stored unencrypted in private storage.

- **MAS-ATTACK-0010:** Accessing shared or external storage from any app holding the corresponding permissions.
- **MAS-ATTACK-0011:** Physically removing and reading external storage media such as SD cards.
- **MAS-ATTACK-0005:** Accessing the device storage on a compromised device.
- **MAS-ATTACK-0007:** Accessing files exposed through incorrect file permissions or misconfigured content providers.
- **MAS-ATTACK-0008:** Extracting local or cloud backups of the device.

### What can go wrong?

If Hassan can extract or modify sensitive data because it's stored without adequate encryption or platform data-protection controls, the failure is concrete rather than merely theatrical: the app could let an attacker cross the cryptography boundary and reach data or capability that this flow should protect. In this card, the practical route includes Accessing shared or external storage from any app holding the corresponding permissions. Also, Physically removing and reading external storage media such as SD cards. That can turn a normal user action into unauthorized access, disclosure, alteration, or service disruption; the mapped weakness entries below identify the exact implementation evidence to check.

Mapped weaknesses that sharpen the review:

- MASWE-0002 — Sensitive Data Stored Unencrypted Outside of Private Storage: This weakness occurs when an app stores sensitive data unencrypted in shared or external storage, where other apps can access it without any user interaction.
- MASWE-0001 — Sensitive Data Stored Unencrypted in Private Storage: This weakness occurs when an app stores sensitive data unencrypted in private storage locations, such as the application sandbox, where it can be exposed via incorrect file permissions, an app or device vulnerability, or data backup...

### What are we going to do about it?

Encrypt sensitive data at rest with platform-backed Keystore or Keychain keys and use the OS data-protection or encrypted-database facilities; test storage extraction, backups, locked-device behavior, and key-access failures.


Mapped MASTG tests:

- MASTG-TEST-0200 — Files Written to External Storage: The goal of this test is to retrieve the files written to the external storage (@MASTG-KNOW-0042) and inspect them regardless of the APIs used to write them. It uses a simple approach based on file retrieval from the device storage...
- MASTG-TEST-0201 — Runtime Use of APIs to Access External Storage: Android apps use a variety of APIs to access the external storage (@MASTG-KNOW-0042). Collecting a comprehensive list of these APIs can be challenging, especially if an app uses a third-party framework, loads code at runtime, or...
- MASTG-TEST-0202 — References to APIs and Permissions for Accessing External Storage: This test uses static analysis to look for uses of APIs allowing an app to write to locations that are shared with other apps (@MASTG-TEST-0001) such as the External Storage APIs or the `MediaStore` API as well as the relevant Android...
- MASTG-TEST-0207 — Runtime Storage of Unencrypted Data in the App Sandbox: The goal of this test is to retrieve the files written to the internal storage (@MASTG-KNOW-0041) and inspect them regardless of the APIs used to write them. It uses a simple approach based on file retrieval from the device storage...
- MASTG-TEST-0299 — Data Protection Classes for Files in Private Storage: This test retrieves the data protection classes of files created or modified in the app's local storage during typical app usage. The goal is to ensure that files containing sensitive data are assigned appropriate data protection...
- MASTG-TEST-0300 — References to APIs for Storing Unencrypted Data in Private Storage: This test checks whether the app writes unencrypted sensitive data to private storage. It focuses on:
- MASTG-TEST-0301 — Runtime Use of APIs for Storing Unencrypted Data in Private Storage: This test is the dynamic counterpart to @MASTG-TEST-0300 and is designed to be used together with @MASTG-TEST-0302.
- MASTG-TEST-0302 — Sensitive Data Unencrypted in Private Storage Files: This test is designed to complement @MASTG-TEST-0301. Instead of monitoring APIs during execution, it performs a differential analysis of the app's private storage by comparing snapshots taken before and after exercising the app. It...
- MASTG-TEST-0303 — References to APIs for Storing Unencrypted Data in Shared Storage: This test checks whether the app stores sensitive data without encryption in iOS sandbox locations that may become user accessible when file sharing is enabled.
- MASTG-TEST-0304 — References to Sensitive Data Unencrypted via Android Room Database: The source provides the mapped security guidance for this control.
- MASTG-TEST-0305 — Sensitive Data Stored Unencrypted via DataStore: The source provides the mapped security guidance for this control.
- MASTG-TEST-0306 — References to Sensitive Data Stored Unencrypted via Android Room DB: The source provides the mapped security guidance for this control.

Mapped MASTG best practices:

- MASTG-BEST-0050 — Store Data Encrypted in App Sandbox Directory: Store sensitive data in `SharedPreferences` only after encrypting it. Standard `SharedPreferences` stores values in XML files inside the app's private data directory, so values such as credentials, authentication tokens, private keys,...
- MASTG-BEST-0024 — Store Data Encrypted in App Sandbox Directory: Choose the right location for storing the app's and the user's data to the app sandbox: use **Documents** directory to store user-generated content and **Library** directory for app's internal data.

Mapped MASTG knowledge:

- MASTG-KNOW-0042 — External Storage: Android devices support shared external storage. This storage may be removable (such as an SD card) or emulated (non-removable). A malicious app with proper permissions running on Android 10 or below can access data that you write to...
- MASTG-KNOW-0041 — Internal Storage: You can save files to the device's internal storage. Files saved to internal storage are containerized by default and cannot be accessed by other apps on the device. When the user uninstalls your app, these files are removed.
- MASTG-KNOW-0082 — App Extensions: Starting with iOS 8, Apple introduced App Extensions. App extensions let an app offer custom functionality and content to users while they interact with other apps or the system. Each extension implements a single, well-scoped task, for...
- MASTG-KNOW-0091 — File System APIs: iOS apps can write data to the file system using various APIs, depending on the use case.
- MASTG-KNOW-0108 — App Sandbox Directories: On iOS, each application gets a sandboxed folder to store its data. As per the iOS security model, an application's sandboxed folder cannot be accessed by another application. Additionally, the users do not have direct access to the iOS...
- MASTG-KNOW-0057 — Keychain Services: The iOS keychain APIs can (and should) be used to implement local authentication. During this process, the app stores either a secret authentication token or another piece of secret data identifying the user in the keychain. In order to...
- MASTG-KNOW-0122 — Document Picker, Document Interaction, and Open in Place: iOS provides several mechanisms for exchanging files between apps. These mechanisms are user-mediated: the user chooses which files to share, open, import, or export, and which apps or locations are involved.
- MASTG-KNOW-0037 — SQLite Database: SQLite is an SQL database engine that stores data in `.db` files. The Android SDK has built-in support for SQLite databases. The main package used to manage the databases is `android.database.sqlite`.
