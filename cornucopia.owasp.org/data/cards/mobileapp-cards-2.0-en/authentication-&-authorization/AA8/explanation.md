## Scenario: Pramod can intercept credentials through misdirection because the app is vulnerable to attacks like Tapjacking, StrandHogg, or URL scheme hijacking

Consider a scenario where Pramod has published a benign-looking utility app on an alternative app store. The utility app monitors for the launch of a popular banking app. When the banking app is about to display its login screen, Pramod's app uses a transparent overlay to capture the user's tap on the "Sign In" button — redirecting the touch to Pramod's own credential capture form, which looks identical to the real login screen. The user enters their credentials believing they are logging into the bank. They are not.

1. Tapjacking (Android): a malicious transparent overlay redirects touches from the intended target to the attacker's UI.
2. StrandHogg / StrandHogg 2.0 (Android): a malicious app places its activity on top of a legitimate app's task stack, presenting a fake UI at authentication time.
3. URL scheme hijacking (iOS / Android): a malicious app registers the same custom URL scheme as the legitimate app and intercepts OAuth redirect callbacks containing authorization codes.

### Example

Pramod's "Battery Optimizer" app requests `SYSTEM_ALERT_WINDOW` permission. Once granted, it monitors the foreground app and, when the banking app's login activity is detected, it draws a transparent view over the input fields with touch interception enabled. The user taps what they believe is the bank's login button. The tap is captured by Pramod's overlay. The credentials are forwarded to Pramod's server and then relayed to the real bank — so the login succeeds and the user suspects nothing. Pramod now has the credentials. The "Battery Optimizer" was not optimising batteries.

## Threat Modeling

### STRIDE

This scenario falls under **Spoofing**.

Pramod's app deceives the user into believing they are interacting with the legitimate banking app, capturing credentials they intended only for the legitimate service.

### What can go wrong?

- User credentials are captured by a malicious overlay and used for account takeover.
- OAuth authorization codes are intercepted via URL scheme hijacking and used to obtain access tokens.
- The user has no indication the attack is occurring; the legitimate app may even complete the login after the credentials are forwarded.

### What are we going to do about it?

- Set `filterTouchesWhenObscured = true` on sensitive views to prevent touch events when another view is drawing over them.
- Use `FLAG_SECURE` on activities that handle authentication to prevent overlays from capturing the screen.
- Replace custom URL schemes for OAuth with App Links (Android) or Universal Links (iOS) — these are domain-verified and cannot be registered by arbitrary apps.
- Verify the task affinity and caller package for activities that handle authentication, and reject unexpected callers.
- Implement anti-StrandHogg measures: set `taskAffinity=""` and `allowTaskReparenting="false"` on authentication activities.
