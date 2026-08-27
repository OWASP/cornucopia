## Scenario: Pekka can alter security-relevant files, configuration, downloaded content, or restored data because the app does not verify their integrity and authenticity before use

### Example

Pekka restores a downloaded configuration file for a train app without checking its signature. The file changes the departure board to “platform 12½,” and a crowd queues beside a broom closet while the real train leaves.

Downloaded, restored, and security-relevant files need integrity and authenticity verification before they affect behavior. A file that merely looks plausible must not become trusted configuration.


## Threat Modeling

### STRIDE

This scenario is primarily **Tampering** in STRIDE. The named condition is: Pekka can alter security-relevant files, configuration, downloaded content, or restored data because the app does not verify their integrity and authenticity before use.

- **MAS-THREAT-0057:** Attackers can alter the app's behavior through its resources.

- **MAS-ATTACK-0009:** Tampering with backup contents and restoring the modified backup to a device.
- **MAS-ATTACK-0070:** Modifying the app's files or resources on a compromised device.

### What can go wrong?

If Pekka can alter security-relevant files, configuration, downloaded content, or restored data because the app does not verify their integrity and authenticity before use, the failure is concrete rather than merely theatrical: the app could let an attacker cross the resilience boundary and reach data or capability that this flow should protect. In this card, the practical route includes Tampering with backup contents and restoring the modified backup to a device. Also, Modifying the app's files or resources on a compromised device. That can turn a normal user action into unauthorized access, disclosure, alteration, or service disruption; the mapped weakness entries below identify the exact implementation evidence to check.

Mapped weaknesses that sharpen the review:

- MASWE-0057 — App Resources Integrity Not Verified: This weakness occurs when an app does not verify that the resources it relies on have not been tampered with.

### What are we going to do about it?

Authenticate security-relevant files, configuration, downloads, and restored data before parsing or using them, using signatures or AEAD with platform-protected keys; test modified, rolled-back, truncated, and partially written data.


Mapped MASTG tests:

- MASTG-TEST-0338 — References to Storage Integrity Check APIs: Android apps can protect the integrity and authenticity of data they store on the device (e.g., in `SharedPreferences`, files, or databases) by computing an HMAC or a digital signature over the data and verifying it before use (see...
- MASTG-TEST-0387 — References to Storage Integrity Check APIs: iOS apps can protect the integrity and authenticity of data they store on the device (e.g., files in the Documents directory, `UserDefaults`/`NSUserDefaults`, or databases) by computing an HMAC or a digital signature over the data and...

Mapped MASTG best practices:

- MASTG-BEST-0066 — Implementing Storage Integrity Checks on Android: Implement storage integrity checks in Android apps to detect unauthorized modifications to data stored on the device (for example, in `SharedPreferences`, files, or databases). These checks raise the cost for attackers who try to tamper...
- MASTG-BEST-0065 — Implementing Storage Integrity Checks on iOS: Implement storage integrity checks in iOS apps to detect unauthorized modifications to data stored on the device (for example, in the Keychain, `UserDefaults`/`NSUserDefaults`, files, or databases). These checks raise the cost for...

Mapped MASTG knowledge:

- MASTG-KNOW-0036 — Shared Preferences: !!! warning
- MASTG-KNOW-0086 — Storage Integrity Checks: Apps can protect data they store on the device (for example in the Keychain, `UserDefaults`/`NSUserDefaults`, or a database) by computing an HMAC or cryptographic signature over it and verifying that value before each use. This lets the...
