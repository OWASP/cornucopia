## Scenario: Gastón can execute malicious actions through intent redirection because the intent is not properly sanitized and is mutable

Consider a scenario where Gastón discovers the target app has a forwarding activity that accepts an intent from any caller and forwards it to another component. The forwarded intent carries a `PendingIntent` that is then fired to perform a privileged action. Gastón sends a crafted intent to the forwarding activity with a manipulated `PendingIntent` target. The app fires the `PendingIntent` on Gastón's behalf, performing a privileged action as the target app — a classic "confused deputy" attack.

1. Activities that accept and forward intents without validating the source or content create confused deputy vulnerabilities.
2. Mutable `PendingIntent` objects can have their contents modified after creation if incorrectly specified.
3. Implicit PendingIntents (without a specified action or component) can be hijacked and filled with attacker-controlled content.

### Example

Gastón finds the app's notification-action handler accepts an intent and starts the activity specified in `intent.getStringExtra("target_activity")`. He sends an intent specifying `target_activity = "com.target.app.AdminActivity"`. The handler starts the `AdminActivity` without authentication. The AdminActivity was never intended to be accessible to external apps. The intent-forwarding mechanism made it accessible to anyone who could send an intent to the forwarding activity.

## Threat Modeling

### STRIDE

This scenario falls under **Elevation of Privilege** and **Tampering**.

Intent redirection allows Gastón to trigger privileged operations within the target app that he could not access directly — a confused deputy attack via the intent mechanism.

### What can go wrong?

- Privileged activities, services, or broadcast receivers are invoked without authentication via the intent-forwarding path.
- Mutable PendingIntents are hijacked to perform arbitrary privileged actions as the target app.
- Sensitive data included in forwarded intents is accessible to the attacker.

### What are we going to do about it?

- Never forward externally received intents to internal sensitive components without validation.
- Validate the source and content of incoming intents before forwarding.
- Use immutable PendingIntents: `PendingIntent.FLAG_IMMUTABLE` (required on Android 12+).
- Specify explicit component names in PendingIntents; do not use implicit PendingIntents for privileged operations.
