## Scenario: Carlos can use the application's notification services to launch phishing campaigns because notifications are not sanitized and validated according to best practices

Consider a scenario where Carlos has found a way to inject arbitrary content into the app's push notification system — either by compromising a weakly authenticated notification API or by sending crafted data to a notification endpoint that does not require authentication. He sends push notifications impersonating the app's brand to all registered users: "Your account has been compromised. Click here to verify your identity." The notification looks identical to a legitimate app notification. Most users click. They are taken to Carlos's phishing page.

1. Notification content that includes unvalidated user-supplied or server-supplied data can be used to deliver phishing messages.
2. Deep links embedded in notifications that are not validated before navigation open, potentially loading attacker-controlled URLs in a WebView.
3. Push notification APIs with weak authentication allow unauthenticated senders to deliver messages to users.

### Example

Carlos discovers the app's notification backend accepts push notification requests authenticated only with a static API key that is embedded in the client APK. He extracts the API key through static analysis and uses it to send notifications to all users via the notification API. He sends "Your payment of $499 is pending. Tap here to cancel." Users who tap are directed to a phishing page capturing their credentials. The API key was meant to be private. It was in the APK. It was not private.

## Threat Modeling

### STRIDE

This scenario falls under **Spoofing**.

Carlos impersonates the legitimate app in push notifications, delivering phishing content through the trusted notification channel — which users are conditioned to trust because it comes from the app they installed.

### What can go wrong?

- Users are phished through the app's own notification infrastructure.
- Notification deep links open attacker-controlled URLs in the app's WebView.
- Notification content injection includes executable content that is rendered in the app.

### What are we going to do about it?

- Authenticate notification API requests with server-side credentials, not with a key embedded in the client binary.
- Sanitize all notification content; never include unvalidated user-supplied strings in notification bodies.
- Validate deep links embedded in notification payloads against an allowlist before navigation.
- Implement rate limiting and anomaly detection on the notification dispatch endpoint.
