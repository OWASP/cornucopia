## Scenario: Bil can access sensitive data from the pasteboard/clipboard or keyboard cache because the pasteboard/clipboard is not timely cleared, disabled, or restricted for sensitive fields, or because the keyboard cache is not disabled

Consider a scenario where Bil borrows a phone after the owner has just copied their account password from a password manager to the banking app. The clipboard still contains the password. Bil opens a notes app, pastes, and has the password. He did not hack anything. He just pressed Ctrl+V.

1. Clipboard data persists after the app is closed and is readable by any app that accesses `ClipboardManager`.
2. Keyboard autocomplete caches text typed into input fields, including sensitive fields without the password flag set.
3. On iOS 16+, apps can read clipboard contents if the user has recently granted permission — but older iOS versions or certain MDM configurations may still allow passive reads.

### Example

Bil's colleague Anjali had copied her banking PIN from her password manager to the app's PIN entry field. The PIN was cached by the keyboard and appeared as an autocomplete suggestion in the browser's address bar when Anjali next used it — because the PIN field was not marked as a password type, so the keyboard treated it as learnable text. Bil was sitting next to her and noticed the suggestion. He remembered the digits. Later that evening, he tested them. They worked.

## Threat Modeling

### STRIDE

This scenario falls under **Information Disclosure**.

Sensitive data persists in the clipboard or keyboard cache, outside the app's control, where it can be accessed by other apps or observed by bystanders.

### What can go wrong?

- Passwords, PINs, OTPs, and account numbers copied to the clipboard remain accessible until cleared.
- Keyboard autocomplete caches sensitive text entered without the password flag, surfacing it in other apps.
- Malicious apps on the same device can read clipboard contents or autocomplete suggestions.
- On iOS, clipboard access notifications (iOS 16+) alert users but do not prevent reading.

### What are we going to do about it?

- Mark all sensitive input fields with the platform's secure-entry flag to prevent keyboard caching.
- After copying sensitive data to the clipboard, schedule a timed clear (e.g., 30 seconds): `ClipboardManager.clearPrimaryClip()` on Android; `UIPasteboard.general.string = nil` on iOS when the app backgrounds.
- Avoid requiring users to copy sensitive data to the clipboard; provide secure in-app mechanisms (e.g., autofill, secure copy-once).
- Restrict clipboard access: on iOS 14+, apps are notified when they read the general pasteboard from the background — this is a detection signal, not a full prevention.
