## Platform-Aware Review Guidance

**Detecting and Preventing Misuse for Surveillance**
- Background location access: require user-visible notification; on iOS, display the blue location indicator; on Android, show a persistent notification for background location services.
- Microphone/camera access: OS indicators (iOS shows an orange dot; Android shows an active indicator) are mandatory; do not suppress them.
- `FLAG_SECURE` on sensitive screens prevents screenshots by other apps and screen recording APIs.
- App installation transparency: neither iOS nor Android allows legitimate apps to hide their icon without documented, policy-compliant exceptions.

**Monitoring/Parental Control Apps**
- Apple Developer Program License Agreement and Google Play Developer Policy both prohibit apps designed to hide their presence from the person being monitored.
- Any app that claims to "monitor" a device must be transparent to the monitored person and require their affirmative consent.
- The Coalition Against Stalkerware (coalitionagainststalkerware.org) provides guidelines for responsible monitoring tools.

**Platform Mitigations**
- iOS: Screen Time (built-in parental controls with transparency to child); Family Sharing with opt-in consent.
- Android: Digital Wellbeing, Google Family Link (transparent, child-visible controls).
- Both platforms provide a legitimate, transparent path for consensual monitoring; stealth alternatives are policy violations.

**Technical Controls for Vulnerable Users**
- Provide users with a way to check for and remove monitoring apps from within your app's security settings.
- Implement safety-check features (inspired by Google and Apple's built-in safety checks) that surface unexpected monitoring configurations.
- Resources for users who suspect surveillance: refer to the Coalition Against Stalkerware, National Domestic Violence Hotline, or equivalent regional resources.

**OWASP Mappings**
- MASVS: PLATFORM-3, PRIVACY-1, PRIVACY-3, STORAGE-2
- MASTG: TEST-0004, TEST-0005, TEST-0006, TEST-0008, TEST-0024, TEST-0035, TEST-0054, TEST-0055, TEST-0057, TEST-0069, TEST-0072, TEST-0073, TEST-0206, TEST-0254, TEST-0255, TEST-0256, TEST-0257, TEST-0258, TEST-0276, TEST-0277, TEST-0278, TEST-0279, TEST-0280, TEST-0281, TEST-0313, TEST-0314, TEST-0315, TEST-0316, TEST-0318, TEST-0319, TEST-0340, TEST-0346, TEST-0347, TEST-0360, TEST-0361, TEST-0362, TEST-0363
- MASWE: MASWE-0053, MASWE-0054, MASWE-0108, MASWE-0112, MASWE-0117
