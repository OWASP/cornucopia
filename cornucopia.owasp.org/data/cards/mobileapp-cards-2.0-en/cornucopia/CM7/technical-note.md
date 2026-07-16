## Platform-Aware Review Guidance

**Android**
- PendingIntent flags: always specify `PendingIntent.FLAG_IMMUTABLE` for PendingIntents that should not be modified by recipients.
- `FLAG_MUTABLE` is only needed for PendingIntents that must be modified by a system service (e.g., `AlarmManager` with a fill-in intent); document the reason.
- Validate intent forwarding: if an activity receives an intent and forwards it, verify the forwarded intent targets only allowlisted internal components.
- Review all exported activities for intent-forwarding patterns.

**iOS**
- URL scheme handlers: validate the full URL and parameters before performing any action; do not execute based solely on URL parameters without authentication.
- Universal Links: validated by the OS using `apple-app-site-association`; prefer over custom URL schemes for deep links.
- Deeplink handlers: maintain an allowlist of valid path patterns; reject any path not on the allowlist.

**Testing**
- Use Drozer: `run app.activity.start` to send crafted intents to all exported activities; observe whether any trigger privileged actions.
- Send intents with crafted `target_activity` or `target_class` extras to identify intent-forwarding vulnerabilities.
- Review all `startActivity`, `sendBroadcast`, and `startService` calls with externally-supplied intent data.

**OWASP Mappings**
- MASVS: CODE-4, PLATFORM-1, STORAGE-2
- MASTG: TEST-0025, TEST-0026, TEST-0030, TEST-0072, TEST-0372, TEST-0374, TEST-0381
- MASWE: MASWE-0066, MASWE-0084
