## Scenario: Kim can reduce app users' privacy because the app repurposes biometric information — such as fingerprints or facial recognition data — collected for security concerns in order to cater for commercial interests

Consider a scenario where Kim works for a fitness app company. The app uses Face ID / fingerprint authentication for account security. The engineering team builds an "emotion detection" feature that, as a side effect, processes and retains facial geometry data beyond what is needed for authentication. The product team proposes selling aggregated "emotional response" data to advertisers. Biometric data collected for authentication is being repurposed for commercial profiling. This is not just a privacy violation — in many jurisdictions it is illegal without explicit, separate consent.

1. Biometric data (fingerprints, facial geometry, iris scans) is a special category of sensitive personal data under GDPR and other regulations.
2. Authentication biometrics collected via OS APIs (Face ID, Android biometric API) should not be stored or used beyond the authentication purpose.
3. Retaining or repurposing biometric templates for commercial purposes without explicit consent is prohibited in many jurisdictions.

### Example

Kim discovers the app's liveness-detection feature (used to prevent spoofing of Face ID) retains facial geometry vectors server-side for "improving the model." These vectors are mathematically derived representations of users' faces. The users consented to biometric authentication. They did not consent to their facial geometry being stored on a server and used to improve a commercial facial recognition model. The consent was for security authentication. The use was commercial model training.

## Threat Modeling

### STRIDE

This scenario falls under **Information Disclosure** with severe privacy and regulatory implications.

Biometric data is uniquely sensitive: it cannot be changed if compromised, it enables highly accurate identification, and its misuse can have profound personal consequences. Repurposing it without consent causes direct harm to user autonomy and privacy.

### What can go wrong?

- Regulatory fines under GDPR, CCPA/CPRA, BIPA (Illinois Biometric Information Privacy Act), and equivalents.
- If the biometric database is breached, affected individuals cannot change their fingerprints or faces.
- Commercial profiling using biometric data enables discriminatory targeting.
- Criminal liability in some jurisdictions (BIPA provides a private right of action).

### What are we going to do about it?

- Process biometric data only on-device using OS-provided secure APIs (Touch ID, Face ID, Android BiometricPrompt); do not store biometric templates server-side.
- Never use biometric data for any purpose other than device-local authentication.
- Do not share biometric data or data derived from biometric features with third parties.
- Implement a data minimization review for any feature that processes facial images or fingerprint data.
