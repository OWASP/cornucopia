## Platform-Aware Review Guidance

**Android**
- `EditText`: set `android:inputType="textPassword"` to disable keyboard suggestions for sensitive fields.
- Clear clipboard after sensitive copy:
  ```kotlin
  handler.postDelayed({
      (getSystemService(Context.CLIPBOARD_SERVICE) as ClipboardManager).clearPrimaryClip()
  }, 30_000)
  ```
- On Android 13+, `ClipboardManager.clearPrimaryClip()` may only clear the calling app's clipboard data — verify behaviour on target SDK versions.
- On Android 12+, apps can no longer silently read the clipboard from background; this is a platform mitigation, not a substitute for clearing.

**iOS**
- `UITextField.isSecureTextEntry = true` — prevents keyboard learning for that field.
- Clear on background: in `applicationWillResignActive(_:)`, set `UIPasteboard.general.string = nil` if the app had written sensitive data to it.
- On iOS 16+, `UIPasteboard` allows expiration: `UIPasteboard.general.setObjects([sensitive], localOnly: false, expirationDate: Date().addingTimeInterval(30))`.
- Use named pasteboards (`UIPasteboard(name:create:)`) for sensitive data shared between your own apps; named pasteboards can be set `localOnly: true` and are not accessible to other apps.

**Testing**
- After entering sensitive data and closing the app, open a text editor and paste; verify the clipboard is empty or contains a non-sensitive placeholder.
- Type sensitive data into each field; switch to a browser; verify the keyboard does not suggest the sensitive value.
- Check the iOS clipboard notification banner (iOS 16+) to verify the app is reading and clearing the clipboard as expected.

**OWASP Mappings**
- MASVS: STORAGE-2
- MASTG: TEST-0006, TEST-0055, TEST-0073
- MASWE: (see MASVS references above)
