## Platform-Aware Review Guidance

**Design Requirements**
- In-context notices: display a brief, plain-language explanation at or before the moment of first data collection for each category of sensitive data.
- Layered privacy notice: a concise summary in the app + link to the full privacy policy; the summary must stand alone without requiring the user to read the full document.
- Privacy policy accessibility: reachable from the app's main menu or settings in no more than two navigation actions.

**Regulatory References (no fabricated URLs)**
- GDPR Articles 13–14: information to be provided at the time of data collection.
- CCPA / CPRA: right to know (categories of data, purposes, third parties).
- Apple App Store Privacy Nutrition Labels: accurately declare data usage in App Store Connect.
- Google Play Data Safety Section: accurately declare data collection and sharing practices.

**Testing**
- User journey audit: follow the first-run experience and note every point at which data is collected; verify a corresponding notice is displayed.
- Review the privacy policy for jargon density; apply the Flesch-Kincaid readability score target (aim for accessible reading level for general consumers).
- Verify the privacy policy link is accessible without authentication.

**OWASP Mappings**
- MASVS: PRIVACY-3
- MASTG: TEST-0004, TEST-0318, TEST-0319
- MASWE: MASWE-0111, MASWE-0112
