## Scenario: Martin can modify behavior or gain access to sensitive data by tampering with security-relevant data in shared preferences, user defaults, files, or databases because the app does not verify its integrity and authenticity before use

### Example

Martin edits a shared-preferences value called `isAdmin` on a rooted test phone. The app trusts the new value and presents a management dashboard where he can promote every contact to “chief nap officer.”

Security-relevant preferences, files, and database records need authenticity and integrity verification before use. Treating locally editable state as authoritative lets tampering change behavior or reveal protected data.


## Threat Modeling

### STRIDE

This scenario is primarily **Tampering**, **Information Disclosure** in STRIDE. The named condition is: Martin can modify behavior or gain access to sensitive data by tampering with security-relevant data in shared preferences, user defaults, files, or databases because the app does not verify its integrity and authenticity before use.

- **MAS-THREAT-0057:** Attackers can alter the app's behavior through its resources.

- **MAS-ATTACK-0009:** Tampering with backup contents and restoring the modified backup to a device.
- **MAS-ATTACK-0070:** Modifying the app's files or resources on a compromised device.

### What can go wrong?

If Martin can modify behavior or gain access to sensitive data by tampering with security-relevant data in shared preferences, user defaults, files, or databases because the app does not verify its integrity and authenticity before use, the failure is concrete rather than merely theatrical: the app could let an attacker cross the network-&-storage boundary and reach data or capability that this flow should protect. In this card, the practical route includes Tampering with backup contents and restoring the modified backup to a device. Also, Modifying the app's files or resources on a compromised device. That can turn a normal user action into unauthorized access, disclosure, alteration, or service disruption; the mapped weakness entries below identify the exact implementation evidence to check.

Mapped weaknesses that sharpen the review:

- MASWE-0057 — App Resources Integrity Not Verified: This weakness occurs when an app does not verify that the resources it relies on have not been tampered with.

### What are we going to do about it?

Treat preferences, user defaults, files, and databases as attacker-controlled: authenticate security-relevant values with a Keystore or Keychain-held key, validate them before use, and test modified, rolled-back, and malformed state.


Mapped MASTG tests:

- MASTG-TEST-0338 — References to Storage Integrity Check APIs: Android apps can protect the integrity and authenticity of data they store on the device (e.g., in `SharedPreferences`, files, or databases) by computing an HMAC or a digital signature over the data and verifying it before use (see...
- MASTG-TEST-0387 — References to Storage Integrity Check APIs: iOS apps can protect the integrity and authenticity of data they store on the device (e.g., files in the Documents directory, `UserDefaults`/`NSUserDefaults`, or databases) by computing an HMAC or a digital signature over the data and...

Mapped MASTG best practices:

- MASTG-BEST-0066 — Implementing Storage Integrity Checks on Android: Implement storage integrity checks in Android apps to detect unauthorized modifications to data stored on the device (for example, in `SharedPreferences`, files, or databases). These checks raise the cost for attackers who try to tamper...
- MASTG-BEST-0065 — Implementing Storage Integrity Checks on iOS: Implement storage integrity checks in iOS apps to detect unauthorized modifications to data stored on the device (for example, in the Keychain, `UserDefaults`/`NSUserDefaults`, files, or databases). These checks raise the cost for...

Mapped MASTG knowledge:

- MASTG-KNOW-0036 — Shared Preferences: !!! warning
- MASTG-KNOW-0086 — Storage Integrity Checks: Apps can protect data they store on the device (for example in the Keychain, `UserDefaults`/`NSUserDefaults`, or a database) by computing an HMAC or cryptographic signature over it and verifying that value before each use. This lets the...
