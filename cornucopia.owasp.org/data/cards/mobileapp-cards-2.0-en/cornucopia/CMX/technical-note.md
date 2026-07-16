## Platform-Aware Review Guidance

**Backend**
- Notification dispatch API: authenticate with OAuth 2.0 client credentials (server-to-server), not with a static key embedded in the app binary.
- Rate limiting: limit the number of notifications that can be dispatched per user, per application, and per IP per time window.
- Content validation: sanitize all notification content for HTML, URLs, and JavaScript before dispatch.

**Android**
- Review `NotificationCompat.Builder` content: do not include raw server-supplied strings in notification titles or bodies without sanitization.
- Deep links from notification actions: validate the URL against an allowlist in the `BroadcastReceiver` or `Activity` that handles the notification action.
- `Notification.setVisibility(Notification.VISIBILITY_SECRET)` for sensitive notification content.

**iOS**
- Push notification payloads from APNs: validate all user-visible string fields before rendering.
- Notification Service Extensions: use to fetch content server-side after verifying the notification's authenticity; do not display unverified content.
- Universal Links in notification deep links: domain-verified, harder to hijack than custom URL schemes.

**Testing**
- Attempt to inject HTML or JavaScript in notification content; verify it is rendered as plaintext.
- Send a notification with a crafted deep link URL to an external domain; verify the app validates and rejects it.
- Verify the notification API requires valid server-side authentication for dispatch.

**OWASP Mappings**
- MASVS: CODE-4, PLATFORM-1, PLATFORM-3, STORAGE-2
- MASTG: TEST-0005, TEST-0025, TEST-0026, TEST-0030, TEST-0072, TEST-0315, TEST-0372, TEST-0374, TEST-0381
- MASWE: MASWE-0054, MASWE-0066
