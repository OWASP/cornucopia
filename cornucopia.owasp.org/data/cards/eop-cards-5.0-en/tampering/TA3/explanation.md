## Scenario: SolarStar's compromised build pipeline signs malware as a trusted update

### Example

SolarStar, a fictional IT monitoring vendor, lets any employee push changes to the CI/CD build server without code review or access restrictions. An attacker socially engineers a junior DevOps intern into installing a "helpful" VSCode extension that steals their build-server credentials. The attacker logs into the build system, quietly injects a backdoor into the source before compilation, and lets the pipeline's own code-signing certificate sign the tampered binary. The next scheduled update pushes the malicious, "trusted" binary to thousands of customers. (This scenario is inspired by the real-world SolarWinds Orion supply-chain attack of 2020, where attackers compromised the build environment itself rather than the shipped code repository.)

## Threat Modeling

### STRIDE

This scenario is primarily **Tampering**, since the attacker modifies build artifacts without authorization. It also involves **Spoofing**, because the tampered binary is signed with the legitimate certificate and appears authentic to customers and their security tools. **Elevation of Privilege** is present too: the attacker moves from a low-privilege developer machine to control over the trusted release pipeline.

### What can go wrong?

**Unrestricted build server access:** If any developer or automated job can modify build scripts or push to the build server without review, an attacker who compromises one credential compromises every future release. See the [CISA/NSA Securing the Software Supply Chain guidance](https://www.cisa.gov/resources-tools/resources/securing-software-supply-chain-developers).

**Signing happens after tampering is possible:** If code signing occurs automatically at the end of an unreviewed build step, a tampered build gets a "trusted" signature with no separate verification.

### What are we going to do about it?

**Isolate and harden the build environment:** Treat build servers as production-critical infrastructure — restrict access, require MFA, and log all changes to build configuration. See [SLSA (Supply-chain Levels for Software Artifacts) framework](https://slsa.dev/).

**Require code review and reproducible builds:** No single individual should be able to unilaterally change what gets built and signed; use branch protection and mandatory peer review before merge.

**Separate signing from building:** Use a dedicated, access-controlled signing service that verifies build provenance (e.g., via SLSA attestations) before applying a production signing key, rather than signing inline in the build job.
