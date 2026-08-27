## Scenario: Timur can replace, redistribute, or introduce unreviewed code into the production app because its signature, certificate, store origin, packaged-code integrity, or reproducible build provenance can't be properly verified

### Example

Timur downloads an app from an unofficial store and cannot distinguish its signature from the publisher’s. The copy includes a cheerful bonus feature that forwards every contact to a “fan club,” and the store insists the package is authentic because its icon is blue.

Signature, certificate, store origin, packaged-code integrity, and build provenance need verifiable checks. Without them, altered or redistributed code can masquerade as the reviewed production app.


## Threat Modeling

### STRIDE

This scenario is primarily **Tampering**, **Information Disclosure** in STRIDE. The named condition is: Timur can replace, redistribute, or introduce unreviewed code into the production app because its signature, certificate, store origin, packaged-code integrity, or reproducible build provenance can't be properly verified.

- **MAS-THREAT-0056:** Attackers can distribute and run modified copies of the app.

- **MAS-ATTACK-0040:** Patching or repackaging the app to remove or alter client-side checks.
- **MAS-ATTACK-0068:** Impersonating the app with scripts, bots, or tampered clients when interacting with the backend.
- **MAS-ATTACK-0069:** Installing a repackaged version of the app on victim devices.

### What can go wrong?

If Timur can replace, redistribute, or introduce unreviewed code into the production app because its signature, certificate, store origin, packaged-code integrity, or reproducible build provenance can't be properly verified, the failure is concrete rather than merely theatrical: the app could let an attacker cross the resilience boundary and reach data or capability that this flow should protect. In this card, the practical route includes Patching or repackaging the app to remove or alter client-side checks. Also, Impersonating the app with scripts, bots, or tampered clients when interacting with the backend. That can turn a normal user action into unauthorized access, disclosure, alteration, or service disruption; the mapped weakness entries below identify the exact implementation evidence to check.

Mapped weaknesses that sharpen the review:

- MASWE-0075 — Non-Reproducible Builds: This weakness occurs when compiling the app's source with the same build environment does not yield a bit-for-bit identical binary, making it impossible to independently verify that a distributed binary was built from the claimed,...
- MASWE-0056 — App Attestation Not Implemented: This weakness occurs when an app does not provide its backend with server-verifiable attestation evidence about the app instance (e.g. app signature), or when the backend does not validate and enforce that evidence to determine whether...

### What are we going to do about it?

Build from reviewed, reproducible inputs, verify dependency and package provenance, and install only artifacts signed by the expected certificate or store; test signature, certificate rotation, update, and modified-package rejection paths.


Mapped MASTG tests:

- MASTG-TEST-0220 — Usage of Outdated Code Signature Format: On iOS, code signatures verify the integrity and authenticity of an app's binary, preventing unauthorized modifications and ensuring that the app is trusted by the operating system. Apple regularly updates its code signature formats to...
- MASTG-TEST-0224 — Usage of Insecure APK Signature Version: Not using newer APK signing schemes means that the app lacks the enhanced security provided by more robust, updated mechanisms.
- MASTG-TEST-0225 — Usage of Insecure APK Signature Key Size: For Android apps, the cryptographic strength of the APK signature is essential for maintaining the app's integrity and authenticity. Using a signature key with insufficient length, such as an RSA key shorter than 2048 bits, weakens...

Mapped MASTG best practices:

- MASTG-BEST-0006 — Use Up-to-Date APK Signing Schemes: Ensure that the app is signed with at least the v2 or v3 APK signing scheme, as these provide comprehensive integrity checks and protect the entire APK from tampering. For optimal security and compatibility, consider using v3, which...

Mapped MASTG knowledge:

- MASTG-KNOW-0058 — App Signing: Code signing your app assures users that the app has a known source and hasn't been modified since it was last signed. Before your app can integrate app services, be installed on a non-jailbroken device, or be submitted to the App...
- MASTG-KNOW-0003 — App Signing: Android requires all APKs to be digitally signed with a certificate before they are installed or run. The digital signature is used to verify the owner's identity for application updates. This process can prevent an app from being...
