## Technical Note: Bil can access sensitive data for sensitive fields from the pasteboard/clipboard or keyboard cache because the pasteboard/clipboard is not timely cleared, disabled or restricted for sensitive fields, or the keyboard cache is not disabled

### Platform Guidance

**Android:** Disable clipboard export and keyboard learning for high-risk inputs such as PINs, card numbers, and one-time passcodes.

```kotlin
passwordField.importantForAutofill = View.IMPORTANT_FOR_AUTOFILL_NO_EXCLUDE_DESCENDANTS
passwordField.setOnLongClickListener { true }
passwordField.customInsertionActionModeCallback = object : ActionMode.Callback { /* block paste */ }
```

**iOS:** Use secure text entry and avoid copying secrets to the pasteboard unless the user explicitly asks for it and the value expires quickly.

```swift
passwordField.isSecureTextEntry = true
UIPasteboard.general.items = []
UIPasteboard.general.expirationDate = Date().addingTimeInterval(30)
```

### Relevant Tests

**Legacy Tests:** MASTG-TEST-0006, MASTG-TEST-0055, MASTG-TEST-0073
**New Tests:** MASTG-TEST-0201, MASTG-TEST-0305, MASTG-TEST-0302

### MASWE Weaknesses

- MASWE-0002: clipboard, keyboard-cache, and transient-input storage issues.
