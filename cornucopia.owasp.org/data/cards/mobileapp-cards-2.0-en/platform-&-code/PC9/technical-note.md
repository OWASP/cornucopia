## Platform-Aware Review Guidance

**Android**
- Replace `startActivityForResult` with `ActivityResultContracts` — the typed contracts (e.g., `GetContent`, `PickVisualMedia`) use system-provided pickers.
- After receiving a `content://` Uri from an external activity, validate the authority against an allowlist before processing.
- Never directly use a `file://` Uri received from an untrusted activity result; convert via `FileProvider` if needed and validate the resolved path.
- For OAuth, use App Links and the Authorization Code + PKCE flow; reject redirect URIs that are not `https://` with a domain you control.

**iOS**
- URL scheme results: validate the `state` parameter to prevent CSRF; ensure the source application matches the expected OAuth provider.
- Use Universal Links for deep-link returns; they are domain-verified and cannot be intercepted by arbitrary apps.
- `UIDocumentPickerViewController` results: validate file extension and type before opening.

**Testing**
- Register a companion app that handles the same implicit intent and returns crafted Uris; verify the target app rejects them.
- Use `adb shell am start --activity-brought-to-front` to simulate result intents with crafted extras.

**OWASP Mappings**
- MASVS: CODE-4, PLATFORM-1, STORAGE-2
- MASTG: TEST-0026, TEST-0030, TEST-0372, TEST-0374, TEST-0381
- MASWE: MASWE-0066
