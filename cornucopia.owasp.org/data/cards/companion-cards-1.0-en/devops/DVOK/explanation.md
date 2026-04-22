## Scenario: Timo's Injection of Malicious Code Through the Supply Chain

Consider a scenario where Timo compromises software, development environments, or DevOps tooling by introducing malicious code through external dependencies or by exploiting compromised developer credentials. This vulnerability arises from:

1. **Compromised External Dependencies:** Timo publishes or modifies an external package to include malicious code that gets pulled into the target's software or tooling.

2. **Exploited Developer Credentials:** Timo uses stolen or phished developer credentials to push malicious code into trusted repositories or packages.

### Example

Timo publishes a package with a name very similar to a popular library. A developer on the team makes a typo when adding the dependency and inadvertently pulls in Timo's malicious package instead of the intended one. The fake package imports the legitimate library under the hood and re-exports its functionality, so everything appears to work correctly from the developer's perspective. However, the package also includes code that runs during installation and exfiltrates environment variables from the developer's machine, including credentials for the code repository. Using those credentials, Timo pushes further malicious changes into the project's codebase, widening the compromise beyond the initial entry point.

## Threat Modeling

### STRIDE

This scenario maps primarily to STRIDE: **Tampering**.

**Tampering** involves unauthorized modification of software, data, or systems. Timo's attack introduces malicious code into the software or its development environment through the supply chain, modifying what developers and build systems trust to be legitimate components. The core issue is the integrity of the software supply chain being compromised.

### What can go wrong?

Supply chain attacks can be particularly damaging because they exploit trust relationships between developers and their dependencies. This can manifest in various forms, including but not limited to:

- Installation of typosquatted or impersonated packages that execute malicious code
- Compromise of legitimate packages through stolen maintainer credentials
- Malicious code running during dependency installation, affecting development machines and build environments
- Propagation of the compromise through the repository when developer credentials are stolen
- Difficulty detecting the attack because the malicious code appears to come from a trusted source

### What are we going to do about it?

1. Before adding a new dependency, check that it is what you think it is. Look for naming anomalies, number of downloads, check the publisher, and verify it is the right package.
2. Use lock files and verify checksums or signatures to make sure the exact versions you reviewed are the ones being installed.
3. Where possible, restrict package installation to approved or trusted registries.
4. Be aware that some dependencies run code during installation. Review what happens at install time, especially for new or unfamiliar packages. Consider disabling these installation scripts if your package manager supports it, and be especially wary of packages that include bundled binary files or obfuscated code.
5. Watch for unexpected changes in dependencies you already use, such as new versions with significantly different code, new maintainers, or version tags suddenly pointing to different digests.
6. Include dependency scanning in your build process to catch known malicious packages.
7. Pin your dependencies to digests instead of mutable tags. You can consider using tools to help manage the digests - some platforms even include the functionality by default.
8. Consider waiting for each release to reach a minimum age before updating. A large part of supply chain attacks are discovered within hours and resolved within days.
