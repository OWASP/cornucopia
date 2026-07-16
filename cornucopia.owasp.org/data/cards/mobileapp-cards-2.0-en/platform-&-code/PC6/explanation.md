## Scenario: Dawn can expose and intercept sensitive functionality through interprocess communication because permissions for broadcast and sharing are not set, not narrow enough, or because sensitive functionality is not excluded when sharing

Consider a scenario where Dawn writes a companion app. She notices the target app broadcasts `ORDER_COMPLETE` as an unprotected implicit broadcast containing the user's order total, items, and a signed URL to download the receipt. Any app on the device can register a broadcast receiver for this action. Dawn's app does exactly that, silently collects every order notification, and uploads the data to her analytics backend. She did not break any encryption. The app delivered the data to her, broadcast-style, with no access control.

1. Unprotected exported broadcast receivers can be triggered by any app to invoke privileged actions.
2. Implicit broadcasts with sensitive payloads are receivable by any app that declares the matching intent filter.
3. iOS custom URL schemes can be registered by any app, enabling URL-scheme hijacking for OAuth redirects and deep links.

### Example

Dawn discovers the app uses an implicit `ACTION_SEND text/plain` intent for "share order confirmation" and includes the order ID and a signed receipt URL in the intent extras. Any app that handles `ACTION_SEND` can receive the full payload. Dawn's app handles that intent, silently captures the signed URL, and forwards it to her server. The developer's assumption was that users would only share with trusted apps. Users' app choices are not assumptions a security model can rely on.

## Threat Modeling

### STRIDE

This scenario falls under **Information Disclosure** and **Elevation of Privilege**.

Improperly protected IPC endpoints expose sensitive data to unintended apps and allow untrusted apps to trigger privileged operations — a violation of the OS sandbox model.

### What can go wrong?

- Sensitive data in broadcasts is received by malicious apps installed on the same device.
- Exported components invoked without authentication perform operations as the app's user.
- iOS URL scheme hijacking allows a malicious app to intercept OAuth redirect tokens by registering the same custom scheme.
- Sharing intents carrying auth tokens or internal references deliver them to any app the user selects — or that registers the intent filter first.

### What are we going to do about it?

- Use `LocalBroadcastManager` (or `Context.sendBroadcast` with a custom signature-level permission) for app-internal broadcasts.
- Set `android:exported="false"` on all components not intentionally accessible to other apps.
- Protect exported components with `android:permission` at `signature` protection level where possible.
- Use explicit intents for sensitive intra-app IPC; avoid implicit intents for actions involving sensitive data.
- On iOS, use Universal Links (domain-verified) rather than custom URL schemes for OAuth redirects and sensitive deep links.
