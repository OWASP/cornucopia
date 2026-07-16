## Scenario: Choi can access capabilities, objects, resources, or properties they should not be authorized to access because entitlements or permissions are too wide, not properly set, or not enforced

Consider a scenario where Choi installs a malicious app that a social-engineering contact shared with him. The malicious app probes other apps on the device for exported components with overly broad permissions. It finds the target app's payment activity is exported with no permission restriction and no caller validation. Choi's malicious app launches the payment activity directly, bypassing the normal authentication flow.

### Example

Choi's malicious app calls `startActivity(Intent().setComponent(ComponentName("com.target.app", "com.target.app.PaymentActivity")))`. The PaymentActivity launches without requiring authentication because it assumes only the main app's navigation flow would ever open it. Choi is now looking at a pre-populated payment form, authenticated as the device owner's account. The "by design" assumption that only the app's own navigation would open this screen turned out to be a design flaw.

## Threat Modeling

### STRIDE

This scenario falls under **Elevation of Privilege**.

Choi's malicious app exploits overly broad entitlements or missing authorization checks to access capabilities it should not be allowed to access, escalating its effective privileges by leveraging the victim app's components.

### What can go wrong?

- A malicious app triggers exported activities, services, or content providers to perform privileged operations on behalf of the device owner.
- Custom permissions with `normal` or `dangerous` protection levels can be acquired by any app, defeating the purpose of the permission check.
- Orphaned custom permissions — used by the app but not defined by it — can be declared first by a malicious app, which then acquires the permission and gains access to protected components.
- A race condition during app installation allows a malicious app to claim a signature-level custom permission before the defining app is installed.

### What are we going to do about it?

- Mark all components not intended for external access as `android:exported="false"`.
- Protect exported components with `android:permission` using `signature` or `signatureOrSystem` protection level.
- Ensure custom permissions are defined in the same app that uses them, using `<permission>` declarations in the manifest.
- Avoid `normal` and `dangerous` protection levels for permissions that gate sensitive functionality.
- Verify the caller's identity inside sensitive components: check `callingPackage`, validate signatures, or use a challenge-response.
- On iOS, restrict entitlements to the minimum required in the `.entitlements` file; prefer App Groups over broad keychain sharing groups.
