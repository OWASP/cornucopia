## Scenario: Ricardo can extract data stored by the app on a stolen or decommissioned device because it does not enforce device access security policies

Consider a scenario where Ricardo finds a second-hand Android phone at a market. The phone's previous owner had a financial app installed and never performed a factory reset. The phone has no PIN lock because the previous owner found it inconvenient. Ricardo connects the phone to his computer, uses ADB to extract the app's data directory (which requires no encryption because the device is not locked), and reads the stored transaction history, locally cached credentials, and account number. The app trusted that the device would be protected. The device was not.

1. If the device has no lock screen PIN, Android's file-based encryption key is derived from a default value, making it less protective.
2. Apps that do not enforce minimum device security requirements (screen lock, encryption, OS version) cannot rely on the device as a security boundary.
3. USB debugging left enabled in a supposedly end-user device allows direct data extraction via ADB.

### Example

Ricardo powers on the found device. It boots straight to the home screen — no PIN, no biometric. He opens the banking app. It opens without authentication (because the device has no lock). He opens ADB and pulls `com.banking.app/databases/`. He now has the SQLite database with transaction history and a locally cached session token that has not expired. The app had no requirement for a device PIN. The device had none. The data was not further protected.

## Threat Modeling

### STRIDE

This scenario falls under **Information Disclosure**.

Sensitive data stored by the app is accessible to whoever possesses the physical device, because the app does not enforce minimum device security requirements and does not apply additional data-level encryption independent of device authentication.

### What can go wrong?

- Locally stored sensitive data (transaction history, session tokens, PII) is readable from a device without a lock screen.
- USB debugging enabled on a user device allows direct file system access via ADB.
- Decommissioned or stolen devices with no factory reset leak data to new owners.

### What are we going to do about it?

- Require a device lock screen (PIN, pattern, or biometric) as a prerequisite for app use; refuse to function without one, or at least refuse to cache sensitive data.
- Use `KeyguardManager.isDeviceSecure()` to check for a lock screen; present a warning and limit functionality if absent.
- On Android, use keys with `setUserAuthenticationRequired(true)` so data encrypted by those keys is not accessible without a lock screen credential.
- Encrypt all sensitive data at rest with keys bound to device authentication, in addition to relying on OS-level file encryption.
- Do not leave USB debugging enabled in production; include this in release checklists.
