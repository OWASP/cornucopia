## Scenario: Jie can use the app to perform sensitive operations because the "unlocked key" is not used during the application flow

Consider a scenario where Jie and Choi live together. Like all households, they keep some secrets — what they spend money on, which streaming services they are paying for, and whether they still owe each other for a certain concert ticket. It is not our job to referee their financial disagreements, but it is our job to ensure the app protects the data it stores.

There are several ways Jie might access Choi's sensitive data:

1. If Choi's phone is left unattended and unlocked, Jie can open the banking app and access sensitive data if the app does not require the unlocked key before displaying account information.
2. If Jie knows Choi's device PIN (from shoulder-surfing), and the app's cryptographic keys are not bound to biometric or user-authentication events, Jie can access decrypted data without triggering a re-authentication prompt.
3. If Choi leaves the app open in the background, Jie can resume it and perform sensitive operations (such as transferring funds) without re-authenticating, because the app does not require the unlocked key before confirming high-value actions.

### Example

Choi really needed to check his bank balance but also really needed to visit the bathroom. He left his phone unlocked on the table. Jie, deeply committed to investigating whether Choi actually went to a Bob Dylan concert instead of paying back a debt, opened the banking app. The app had no active session lock and performed no key-based authentication check on launch. Jie found not only the concert evidence but also the bank account details. Choi's next financial disclosure was involuntary.

## Threat Modeling

### STRIDE

This scenario falls under **Spoofing**.

Jie is masquerading as Choi. By exploiting the absence of unlocked-key enforcement, the app fails to verify the true identity of the person interacting with it, allowing Jie to act with Choi's full privileges.

### What can go wrong?

If the unlocked key is not required for sensitive operations, the app may be vulnerable to local authentication bypass. This is exploitable by a partner with physical device access, a thief, or an attacker who can extract the keystore/keychain without triggering authentication. The result is a local data breach: private financial, medical, or personal information is exposed.

### What are we going to do about it?

- Configure cryptographic keys with `setUserAuthenticationRequired(true)` (Android) or `kSecAttrAccessibleWhenPasscodeSetThisDeviceOnly` with `biometryAny` or `biometryCurrentSet` access control (iOS) so they cannot be used without a fresh authentication event.
- Use a time-limited authentication validity window (`setUserAuthenticationValidityDurationSeconds`) only for truly low-risk operations; set it to zero for decryption of sensitive data.
- Enforce re-authentication when the app transitions from background to foreground during a sensitive session.
- Require step-up authentication (re-authentication against a remote endpoint or a fresh biometric prompt) before confirming high-value operations such as fund transfers, email or password changes.
