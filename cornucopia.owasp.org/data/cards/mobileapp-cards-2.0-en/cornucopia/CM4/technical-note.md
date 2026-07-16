## Platform-Aware Review Guidance

**SDK Audit**
- Before integrating any third-party SDK, review its privacy documentation: what data does it collect? Where is it sent? How is it retained?
- Use a network proxy during SDK integration testing to observe all outgoing requests from SDK initialization.
- Review the SDK's `AndroidManifest.xml` contributions and iOS `Info.plist` requirements for permissions it requests.

**Data Minimization**
- Configure SDKs to the minimum data collection level: disable advertising IDs, reduce location precision, disable event tracking if not needed.
- Firebase Analytics: `FirebaseAnalytics.setAnalyticsCollectionEnabled(false)` until consent is obtained.
- Advertising frameworks: implement Consent Management Platform (CMP) integration; do not initialise ad SDKs until consent is granted.

**Network Traffic Audit**
- Use mitmproxy or Charles Proxy to observe all outgoing requests from the app during normal usage.
- Compare observed data transmissions against the privacy policy disclosures and consent scope.
- Tools: Exodus Privacy scans APKs for known tracker SDKs.

**OWASP Mappings**
- MASVS: PRIVACY-1
- MASTG: TEST-0054, TEST-0206, TEST-0281
- MASWE: MASWE-0108
