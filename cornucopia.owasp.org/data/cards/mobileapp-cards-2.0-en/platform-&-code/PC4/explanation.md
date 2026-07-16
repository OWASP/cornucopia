## Scenario: Kelly can expose sensitive data by taking advantage of excessive, unexplained, or unjustified permissions for location, camera, microphone, storage, health data, and more

Consider a scenario where Kelly downloads a free budgeting app. The app requests permissions for location, microphone, contacts, and camera. The budget tracker works flawlessly. So does the data harvesting. Kelly granted the permissions because she wanted to try the app, and a permission screen at launch is about as well-read as a terms-and-conditions page.

1. An app that collects fine-grained location continuously when it only needs a one-time coarse location for a tax-return field has a large, unnecessary exposure surface.
2. A third-party analytics SDK bundled inside the app may declare its own permissions in the merged manifest — permissions the developer never intended to grant.
3. Microphone and camera permissions granted "in case we add voice features later" enable ambient surveillance if the app is compromised or if the SDK is malicious.

### Example

Kelly's budgeting app was bought by a data broker six months after launch. The new owners pushed an update that began continuously reading GPS coordinates, uploading them in the background. The app had declared `ACCESS_BACKGROUND_LOCATION` in its manifest since version 1.0, "just in case." The permission had been silently granted on devices running Android 9 or below. The regulatory authority found out. So did Kelly, eventually, in a news article about the data broker.

## Threat Modeling

### STRIDE

This scenario falls under **Information Disclosure** and **Elevation of Privilege**.

Excessive permissions give the app, any embedded SDK, and any future owner a far larger data-access surface than the stated function requires. This is a direct violation of the principle of least privilege.

### What can go wrong?

- A compromised app, SDK update, or supply-chain attack exfiltrates data it was unnecessarily granted permission to access.
- Regulatory penalties (GDPR, CCPA, HIPAA) apply when data is collected without a lawful basis, even if the permission was granted.
- Users who notice excessive permissions lose trust and uninstall; those who do not notice become unwitting data subjects.

### What are we going to do about it?

- Audit every declared permission at design time: document which feature requires it and why no narrower alternative exists.
- Request permissions just-in-time, not at app launch, and explain the purpose clearly at the point of request.
- Remove all unnecessary permissions from the manifest; treat them as blocked until justified.
- Prefer scoped APIs: Photo Picker over broad storage access, approximate location over precise, one-time location over continuous.
- Audit third-party SDK manifests for additional permission declarations that merge into the app's manifest.
