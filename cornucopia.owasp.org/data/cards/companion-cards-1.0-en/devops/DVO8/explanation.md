## Scenario: Maxim's Deployment of a Modified Artifact

Consider a scenario where Maxim deploys a malicious or otherwise tampered artifact to production because the pipeline does not verify the artifact's integrity before deployment. This vulnerability arises from:

1. **No Integrity Validation:** The deployment process does not verify that the artifact being deployed matches what was originally built and approved.

2. **Unprotected Artifact Storage:** Artifacts can be modified after they are built, either in the artifact repository or during transit to the deployment target.

### Example

Maxim gains access to the artifact repository where built packages are stored before deployment. He replaces a legitimate artifact with a modified version that contains a backdoor. When the deployment pipeline picks up this artifact, it deploys it to production without verifying that the artifact matches the one that was originally built and tested. Because there is no signature verification or checksum validation in the deployment process, the tampered artifact is treated as legitimate.

## Threat Modeling

### STRIDE

This scenario maps primarily to STRIDE: **Tampering**.

**Tampering** involves unauthorized modification of data or components. Maxim's attack targets the integrity of the deployment artifact itself. The built package is modified between the build step and deployment, and the pipeline fails to detect the alteration. The core issue is the absence of integrity verification for artifacts entering production.

### What can go wrong?

Without artifact integrity validation, any modification to a built artifact, whether malicious or accidental, will go undetected. This can manifest in various forms, including but not limited to:

- Deployment of tampered artifacts containing backdoors or malicious code
- Modification of artifacts between build and deployment systems
- Inability to verify that what is running in production matches what was built and tested
- Accidental deployment of incorrect or corrupted artifact versions

### What are we going to do about it?

1. If your CI platform or package manager supports artifact signing, set it up so that artifacts are signed at build time and the signature is verified before deployment. If signing is not available, use checksums as a simpler alternative: record the checksum at build time and compare it before deployment.
2. Lock down write access to your artifact repository so that only the build pipeline can push to it. Do not allow manual uploads.
3. Avoid downloading artifacts from intermediate or unprotected locations. Pull them directly from the repository where the build published them.
4. If your artifact repository supports it, enable features like immutable tags or version locking so that published artifacts cannot be silently replaced.
5. If your build platform or artifact repository support it, record where each artifact was built, from which source commit, and its checksum or signature.
6. Make sure the verification step is part of the pipeline itself, not something that can be manually skipped or turned off by the person running the deployment.
