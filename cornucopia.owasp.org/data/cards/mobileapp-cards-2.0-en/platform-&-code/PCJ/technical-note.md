## Platform-Aware Review Guidance

**Android**
- `./gradlew dependencyInsight` to inspect transitive dependency versions.
- OWASP Dependency-Check Gradle plugin: `apply plugin: 'org.owasp.dependencycheck'`.
- Dependabot or Renovate: configure to auto-create PRs for dependency updates with CVSS thresholds.
- `minSdkVersion`: Android 11 (API 30) is the practical minimum for continued security-patch coverage; document exceptions.
- `targetSdkVersion`: must meet Google Play Store requirements and should match the current API level.

**iOS**
- `swift package show-dependencies --format json` to audit Swift Package Manager dependencies.
- CocoaPods: `pod outdated` lists packages with available updates.
- Set a minimum deployment target supported by Apple's current security-patch window (typically current - 2 major versions).
- Review Swift Package Index security advisories.

**CI/CD**
- Add a SCA step that fails the build on CVSS ≥ 7 findings.
- Generate an SBOM in CycloneDX or SPDX format on every release build.
- Sign and verify dependency artifact checksums in the build pipeline.

**OWASP Mappings**
- MASVS: CODE-1, CODE-2, CODE-3, NETWORK-1
- MASTG: TEST-0036, TEST-0042, TEST-0080, TEST-0085, TEST-0245, TEST-0272, TEST-0273, TEST-0274, TEST-0275, TEST-0382, TEST-0383, TEST-0384, TEST-0392
- MASWE: MASWE-0049, MASWE-0075, MASWE-0076, MASWE-0077, MASWE-0078
