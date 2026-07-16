## Scenario: Johan can modify or expose sensitive data by exploiting outdated platforms, SDKs, or third-party dependencies because supported versions, trustworthy components, and security updates are not enforced

Consider a scenario where Johan monitors public CVE feeds. He identifies a high-severity vulnerability in an HTTP client library that a banking app ships. The library was patched three months ago, but the bank's app still distributes the old version. Johan writes a proof-of-concept exploit targeting the vulnerability, delivers it via a crafted server response on a rogue Wi-Fi access point, and achieves code execution inside the app's process. The bank's server infrastructure is hardened. The app, in its users' pockets, is not.

1. Third-party libraries with known CVEs remain exploitable for as long as the app ships them.
2. Apps targeting old `minSdkVersion` values cannot benefit from security improvements added in newer OS versions.
3. Outdated platform SDKs lack backported security patches applied in newer API levels.

### Example

Johan finds the app uses OkHttp 4.9.0, which has a known certificate-parsing vulnerability. He sets up a rogue access point at a café, serves a malformed TLS certificate, and exploits the parser to execute code in the app's process. The development team had intended to update the library "next sprint" for five consecutive sprints. The sixth sprint was an incident response.

## Threat Modeling

### STRIDE

This scenario falls under **Tampering** and **Information Disclosure**.

Unpatched vulnerabilities in third-party dependencies provide attackers with documented, often publicly exploited attack paths. Exploit code frequently exists before the patched version is deployed.

### What can go wrong?

- Pre-existing CVEs in dependencies are exploited without the attacker needing to develop new attack techniques.
- Supply-chain attacks inject malicious code into a dependency before it is consumed by the app.
- Apps that do not enforce a minimum OS version run on devices that cannot receive OS security patches.
- Outdated SDKs may use deprecated cryptographic algorithms or insecure API defaults.

### What are we going to do about it?

- Integrate Software Composition Analysis (SCA) tooling (Dependabot, OWASP Dependency-Check, Snyk) into CI to flag known CVEs automatically.
- Define and enforce a maximum tolerable lag between a library patch release and production adoption — treat CVE severity ≥ 7 as a blocker.
- Review transitive dependencies, not just direct ones; the vulnerable library may be pulled in indirectly.
- Pin dependency versions in the build file; avoid dynamic version ranges that can silently change.
- Maintain a software bill of materials (SBOM) and update it with every release.
