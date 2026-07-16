## Platform-Aware Review Guidance

**Android**
- `android:inputType="textPassword"` on `EditText` — disables suggestions, masks input.
- Add `TYPE_TEXT_FLAG_NO_SUGGESTIONS` for non-password sensitive text: `inputType = TYPE_CLASS_TEXT or TYPE_TEXT_FLAG_NO_SUGGESTIONS`.
- `ClipboardManager.clearPrimaryClip()` after writing sensitive data; schedule a delayed clear for after the user pastes.
- Set `FLAG_SECURE` on the window to prevent IME screenshots.

**iOS**
- `UITextField.isSecureTextEntry = true` — masks content and disables autocorrect, autocomplete, and spell-check.
- `UITextField.autocorrectionType = .no` and `spellCheckingType = .no` for non-password fields carrying sensitive data.
- `UIPasteboard.general.string = nil` when the app moves to background.
- SwiftUI: use `SecureField` for sensitive inputs.

**Testing**
- Type a sentinel value into each sensitive field; switch to a browser and open a text field — autocomplete should not suggest the sentinel.
- On a jailbroken iOS device, check `/private/var/mobile/Library/Keyboard/` for cached sensitive words.
- Use a third-party keyboard with full access enabled; confirm the app shows the iOS warning and, where supported, restricts the keyboard.

**OWASP Mappings**
- MASVS: CODE-4, PLATFORM-3, PRIVACY-1, STORAGE-2
- MASTG: TEST-0006, TEST-0008, TEST-0026, TEST-0035, TEST-0037, TEST-0055, TEST-0057, TEST-0072, TEST-0073, TEST-0258, TEST-0276, TEST-0277, TEST-0278, TEST-0279, TEST-0280, TEST-0313, TEST-0314, TEST-0316, TEST-0320, TEST-0340, TEST-0346, TEST-0347, TEST-0375
- MASWE: MASWE-0053, MASWE-0083, MASWE-0118
