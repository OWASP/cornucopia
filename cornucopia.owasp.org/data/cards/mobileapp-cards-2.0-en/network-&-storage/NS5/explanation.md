## Scenario: Kevin can read sensitive data mapped to user accounts or sessions by extracting data exposed through third-party libraries, notifications, backups, caches, local databases, or other embedded services

Consider a scenario where Kevin installs a popular social app and investigates what it stores locally. He finds the app's embedded SQLite database contains a table populated by the analytics SDK, which logs every screen the user visited along with the user ID. He also finds a notification payload cached by the push service SDK that contains the user's full name and a session token. Neither the app developer nor the user intended for this data to be stored locally in this form.

1. Third-party SDKs write data to local storage on the developer's behalf, often without the developer's knowledge of exactly what is stored.
2. Push notification payloads are cached by the notification SDK and may persist after the notification is dismissed.
3. App-level backups (Android Auto Backup, iTunes backup) can include SDK-generated data files that the developer did not intend to back up.

### Example

Kevin uses ADB backup on a non-encrypted device to extract the app's data. He finds `analytics.db` — created by the bundled analytics SDK — which contains a full browsing history of the user's in-app navigation, device fingerprint data, and a persistent user ID linking sessions across time. The app's own privacy policy says it does not track browsing history. The analytics SDK's privacy policy, buried in the developer's data-processing agreement, says something different. Kevin now has a detailed profile of the user's behaviour.

## Threat Modeling

### STRIDE

This scenario falls under **Information Disclosure**.

Third-party libraries and platform services create additional data stores that may contain sensitive data the app developer did not intend to persist or expose, expanding the disclosure surface beyond what is visible in the app's own code.

### What can go wrong?

- Analytics SDKs collect more data than expected and write it to local storage.
- Push notification payloads containing PII or tokens are cached by the notification SDK.
- Auto-backup includes SDK-generated databases containing sensitive data.
- Notification content visible on the lock screen or in the notification shade exposes sensitive information without the user unlocking the device.

### What are we going to do about it?

- Audit every third-party SDK for its local storage footprint; review its data retention and what it writes to disk.
- Configure push notification payloads to not include PII or sensitive content in the notification body; use a notification ID that the app resolves to content only after authentication.
- Configure Android Auto Backup exclusion rules to exclude SDK-generated databases containing sensitive data.
- Use `Notification.Builder.setVisibility(Notification.VISIBILITY_SECRET)` or `.VISIBILITY_PRIVATE` for notifications containing sensitive content.
