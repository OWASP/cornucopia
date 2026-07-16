## Platform-Aware Review Guidance

**Biometric Data Processing**
- Use OS-provided biometric APIs only (Android `BiometricPrompt`, iOS `LAContext`/Touch ID/Face ID); do not implement custom biometric capture or matching.
- OS biometric APIs do not expose raw biometric templates to applications; they only provide an authentication success/failure signal.
- If a custom liveness-detection or face-recognition feature is required, conduct a Data Protection Impact Assessment (DPIA) before implementation.

**Regulatory Requirements**
- GDPR Article 9: biometric data for the purpose of uniquely identifying a natural person is a special category; explicit consent required.
- Illinois BIPA: biometric data cannot be collected, stored, or shared without written consent; carries a private right of action with statutory damages.
- CCPA/CPRA: biometric information is sensitive personal information with stricter requirements.

**Data Minimization**
- For liveness detection: process locally, do not retain facial geometry vectors beyond the detection event.
- For model training: do not use user authentication data; use synthetic or separately consented datasets.
- Audit all features that capture camera or sensor data for any incidental biometric processing.

**OWASP Mappings**
- MASVS: PRIVACY-2
- MASTG: (see MASVS references above)
- MASWE: (see MASVS references above)
