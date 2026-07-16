## Platform-Aware Review Guidance

**Android**
- Audit all `onBind()`, `onStartCommand()`, and `onReceive()` for unsanitized use of intent extras.
- Avoid custom `Parcelable` or `Serializable` from untrusted senders; use Bundles with validated primitives.
- Validate content URI parameters in all ContentProvider methods against expected patterns.
- For app widgets and Notification actions, treat all `RemoteViews` callbacks and PendingIntent extras as untrusted.

**iOS**
- App extensions write to a shared group container; the host app must validate all shared-container data before use.
- `NSExtensionItem` data received in a Share Extension: validate type (`UTType`) and size before forwarding to the host.
- `WKWebView` JavaScript message handlers: validate `message.body` type and content before acting; reject unexpected schemas.
- Limit `WKScriptMessageHandler` exposure: do not register handlers for sensitive native functions unless the loaded URL is allowlisted.

**Testing**
- Use Drozer: `run app.service.send`, `run app.broadcast.send` with crafted Bundles containing boundary-case inputs.
- Monitor Binder traffic with `binder-trace` or a custom instrumentation agent during fuzz testing.
- Test each app extension independently using a companion app that sends crafted inputs.

**OWASP Mappings**
- MASVS: CODE-4, PLATFORM-1, PLATFORM-3, STORAGE-2
- MASTG: TEST-0025, TEST-0026, TEST-0072, TEST-0375, TEST-0389, TEST-0390
- MASWE: MASWE-0061, MASWE-0081, MASWE-0083, MASWE-0084
