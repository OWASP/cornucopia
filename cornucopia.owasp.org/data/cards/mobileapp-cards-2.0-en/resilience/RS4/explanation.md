## Scenario: Timur can replace or redistribute the production app because its signature, certificate, store origin, or packaged-code integrity is not properly verified

Consider a scenario where Timur downloads the target app's APK from a third-party website, modifies it to add a keylogger, re-signs it with his own certificate, and distributes the modified APK on app-sharing forums as "the official app with premium features unlocked." Users who sideload the modified APK receive a functional copy of the app — along with the keylogger. The app does not verify its own certificate or signing identity at runtime.

1. APKs distributed outside the official store can be modified and re-signed by anyone.
2. Apps that do not verify their signing certificate at runtime cannot detect that they are running as a modified copy.
3. The official store is the first line of defence; sideloading bypasses all store-level security checks.

### Example

Timur modifies the APK's `classes.dex` to add a small hook that copies every password entered into a background service. He re-signs with his own debug certificate. The modified APK is functionally identical to the original. Users who install it never notice. The app's code does not verify the signing certificate; it runs happily under any signing key. The banking app now reports every credential to Timur's server. The feature set is identical. The keylogger is free.

## Threat Modeling

### STRIDE

This scenario falls under **Tampering** and **Spoofing**.

Timur distributes a modified version of the legitimate app that masquerades as the original, tampers with the app's code to introduce malicious functionality, and spoofs the user experience of the real app.

### What can go wrong?

- Users install a modified app thinking it is the official version.
- Malicious code is injected into the app (keyloggers, credential stealers, ad fraud).
- The modified app accesses the legitimate backend using the user's credentials, making the attack invisible.

### What are we going to do about it?

- Verify the app's signing certificate at runtime and terminate if it does not match the expected value.
- Use Google Play Integrity API (Android) or App Attest (iOS) to attest that the app is the official, unmodified version installed from the official store.
- Educate users to install only from official stores; include a deep link to the official listing.
- Monitor for fraudulent or modified versions of the app on unofficial channels using brand-protection services.
