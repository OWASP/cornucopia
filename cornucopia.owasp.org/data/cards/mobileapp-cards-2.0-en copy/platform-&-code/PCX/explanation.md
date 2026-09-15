## Scenario: Johan can modify or expose sensitive data by exploiting outdated platforms, SDKs, third-party dependencies, or WebView components, because supported versions, trusted components, and security updates are not enforced

### Example

Johan keeps an old phone because a shopping app still supports its obsolete WebView and unpatched dependency. A known flaw in the embedded component lets a coupon page read more than coupons, including Johan’s saved delivery address.

Supported platform and SDK versions, trusted dependencies, and security updates must be enforced. Retaining vulnerable components expands the attack surface even when the app’s own code appears careful.


## Threat Modeling

### STRIDE

This scenario is primarily **Tampering**, **Information Disclosure** in STRIDE. The named condition is: Johan can modify or expose sensitive data by exploiting outdated platforms, SDKs, third-party dependencies, or WebView components, because supported versions, trusted components, and security updates are not enforced.

- **MAS-THREAT-0041:** Attackers can exploit platform-level weaknesses that the app cannot fix on its own.
- **MAS-THREAT-0044:** Attackers can exploit publicly known vulnerabilities in the app's dependencies.
- **MAS-THREAT-0043:** Attackers can exploit vulnerabilities that remain reachable in outdated app versions.
- **MAS-THREAT-0035:** Attackers can execute malicious web content inside the app's WebView.

- **MAS-ATTACK-0054:** Installing a malicious app on a device running an OS version affected by unpatched platform vulnerabilities.
- **MAS-ATTACK-0055:** Running the app on a device whose OS version lacks the platform protections the app relies on.
- **MAS-ATTACK-0073:** Identifying vulnerable dependency versions in the app package and using public advisories or exploits.
- **MAS-ATTACK-0040:** Patching or repackaging the app to remove or alter client-side checks.
- **MAS-ATTACK-0053:** Targeting users who remain on an app version with publicly known vulnerabilities.
- **MAS-ATTACK-0047:** Delivering crafted deep links or intents from a malicious app or web page.
- **MAS-ATTACK-0051:** Injecting malicious JavaScript into WebView content (e.g., via MITM on insecure connections or a compromised website).

### What can go wrong?

If Johan can modify or expose sensitive data by exploiting outdated platforms, SDKs, third-party dependencies, or WebView components, because supported versions, trusted components, and security updates are not enforced, the failure is concrete rather than merely theatrical: the app could let an attacker cross the platform-&-code boundary and reach data or capability that this flow should protect. In this card, the practical route includes Installing a malicious app on a device running an OS version affected by unpatched platform vulnerabilities. Also, Running the app on a device whose OS version lacks the platform protections the app relies on. That can turn a normal user action into unauthorized access, disclosure, alteration, or service disruption; the mapped weakness entries below identify the exact implementation evidence to check.

Mapped weaknesses that sharpen the review:

- MASWE-0041 — Running on a Recent Platform Version Not Ensured: This weakness occurs when an app does not ensure that it runs on a sufficiently recent platform version, e.g. via `minSdkVersion` on Android or `MinimumOSVersion` on iOS.
- MASWE-0044 — Dependencies with Known Vulnerabilities: This weakness occurs when an app includes third-party libraries, software development kits (SDKs), or frameworks that contain publicly known vulnerabilities.
- MASWE-0043 — Enforced Updating Not Implemented: This weakness occurs when an app has no mechanism to force users to update to a more secure version after a critical vulnerability has been remediated.
- MASWE-0035 — WebViews Loading Untrusted Content: This weakness occurs when a WebView loads URLs, HTML, or JavaScript from untrusted sources, or lets users navigate to arbitrary sites outside the developer's control.

### What are we going to do about it?

Set a supported OS, SDK, dependency, and WebView baseline, remove obsolete components, verify trusted signed provenance, and apply security updates promptly; test the minimum supported versions and vulnerable WebView or library behavior before release.


Mapped MASTG tests:

- MASTG-TEST-0245 — References to Platform Version APIs: This test verifies whether an app is running on a recent version of the Android operating system.
- MASTG-TEST-0272 — Identify Dependencies with Known Vulnerabilities in the Android Project: In this test case we will identify dependencies in Android Studio.
- MASTG-TEST-0273 — Identify Dependencies with Known Vulnerabilities by Scanning Dependency Managers Artifacts: In this test case we are identifying dependencies with known vulnerabilities in iOS. Dependencies are integrated through dependency managers, and there might be one or more of them being used. We therefore need all of the relevant...
- MASTG-TEST-0274 — Dependencies with Known Vulnerabilities in the App's SBOM: In this test case we are identifying dependencies with known vulnerabilities by relying on a Software Bill of Material (SBOM).
- MASTG-TEST-0275 — Dependencies with Known Vulnerabilities in the App's SBOM: This test case checks for dependencies with known vulnerabilities in iOS applications by using a Software Bill of Materials (SBOM). The SBOM should be in CycloneDX format, which is a standard for describing the components and...
- MASTG-TEST-0382 — Runtime Use of Enforced Updating APIs: At runtime, Android apps implementing enforced updating typically either invoke the Google Play In-App Updates API (for example, `AppUpdateManager`) or perform a custom version check, for example by retrieving...
- MASTG-TEST-0383 — References to Enforced Updating APIs: iOS apps may fail to enforce updates when critical security patches or minimum version requirements are needed. Apple does not provide a public API to force install or silently update an App Store app, so apps must implement their own...
- MASTG-TEST-0384 — Runtime Use of Enforced Updating APIs: On iOS, apps implementing enforced updating typically read the app version, for example `CFBundleShortVersionString` via `Bundle.main.infoDictionary`, and send it to a backend that returns a minimum version policy. Apps may also read...
- MASTG-TEST-0392 — References to Enforced Updating APIs: Android apps may fail to enforce updates when critical security patches or minimum version requirements are needed. For Google Play-distributed apps, enforced updating can be implemented using the Google Play In-App Updates API (for...
- MASTG-TEST-0331 — Use of Deprecated WebView APIs: In this test, we look for references to `UIWebView` (@MASTG-KNOW-0076), a deprecated component since iOS 12.0, in favor of `WKWebView`. `UIWebView` presents security and performance risks: it does not allow JavaScript to be fully...

Mapped MASTG best practices:

- MASTG-BEST-0032 — Migrate from UIWebView to WKWebView: Apple deprecated `UIWebView` in iOS 12 in favor of `WKWebView` for better security and performance. Migrate your app to `WKWebView` to benefit from its improved security features, such as out-of-process rendering and enhanced JavaScript...

Mapped MASTG knowledge:

- MASTG-KNOW-0023 — Enforced Updating: Forcing a user to update the application can be necessary in multiple cases:
- MASTG-KNOW-0074 — Enforced Updating: Forcing a user to update the application can be necessary in multiple cases:
- MASTG-KNOW-0076 — WebViews: WebViews are in-app browser components for displaying interactive web content. They can be used to embed web content directly into an app's user interface. iOS WebViews execute JavaScript and render HTML, and therefore can execute...
