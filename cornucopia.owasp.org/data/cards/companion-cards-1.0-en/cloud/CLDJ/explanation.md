## Scenario: Michael's Compromise of a Build Runner and Container Image Tampering

Michael compromises a shared CI/CD build runner and uses it to inject malicious code into container images, which are then automatically promoted to production across all cloud clusters. This occurs because:

1. **Shared Build Runners Without Job Isolation:** Build jobs from different repositories or teams run on the same runner infrastructure, allowing a malicious job to access files, environment variables, or credentials belonging to other jobs.

2. **No Verification of Container Image Integrity:** Container images are promoted to production based on a successful build status alone, without signature verification that confirms the image was produced by a trusted, unmodified build process.

### Example

Michael exploits an unpatched vulnerability in the CI platform's web interface to gain code execution on a shared build runner. He installs a persistent script that intercepts subsequent build jobs running on the same host. When the next legitimate build for the main application is triggered, Michael's script modifies the Dockerfile mid-build, appending an instruction that downloads and installs a reverse shell payload as a background service within the final image layer. The tampered image passes all automated vulnerability scans and is tagged as `latest`. The deployment pipeline automatically rolls it out to all production Kubernetes clusters, establishing Michael's reverse shell in every running pod.

## Threat Modeling

### STRIDE

The scenario maps directly to STRIDE: **Tampering**.

Michael modifies the container images deployed to production, embedding malicious code in what appears to be a legitimately built artefact. The attack targets the integrity of the build output — not the source code directly — exploiting trust placed in the build infrastructure.

### What can go wrong?

Tampering with container images at the build stage is a particularly dangerous form of supply chain attack because the malicious code is deployed everywhere the image runs — instantly and automatically. It bypasses source code review, runs inside the production security boundary, and is difficult to detect without image signing or runtime integrity monitoring. In organizations with automated rollouts across many services, a single compromised build runner can propagate a backdoor across hundreds of containers simultaneously.

### What are we going to do about it?

Harden the build infrastructure and enforce image integrity verification throughout the deployment pipeline.

1. Use ephemeral, isolated build environments for each job, never allow shared state between builds from different repositories or trust levels.
2. Implement container image signing and require signature verification before any image is admitted to a production registry or cluster.
3. Restrict registry push credentials to specific build jobs using short-lived OIDC tokens rather than long-lived service account keys stored on the runner.
4. Keep build runner software and host kernels patched, and audit runner configurations regularly for unexpected persistent processes or scripts.
