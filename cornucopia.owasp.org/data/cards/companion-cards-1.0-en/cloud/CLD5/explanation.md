## Scenario: Josh's Malicious Code Injection via Unprotected Build Variables

Josh injects malicious code into the cloud build or deployment pipeline by exploiting environment variables and build configuration secrets that have been left unprotected. This occurs because:

1. **Secrets Stored as Plaintext Build Variables:** API keys, cloud credentials, or signing keys are stored as plaintext environment variables in the CI/CD configuration rather than in a dedicated secrets manager.

2. **Insufficient Access Controls on Pipeline Configuration:** Pipeline definitions or build scripts can be modified by contributors without requiring appropriate review or branch protection rules.

### Example

Josh discovers that the company's CI/CD platform exposes build variables in pipeline logs when a debug flag is accidentally left enabled. Among the leaked variables is a set of cloud credentials with permission to push to the container registry and deploy functions. Josh crafts a pull request that appears to fix a minor documentation error, and uses a known platform behaviour that allows pull request builds to access protected environment variables in certain configurations. During the triggered build, Josh's embedded script retrieves the credentials and uses them to push a backdoored container image to the production registry, which is then automatically deployed to the live environment.

## Threat Modeling

### STRIDE

The scenario maps directly to STRIDE: **Tampering**.

Josh modifies the artefacts produced by the build pipeline, ultimately delivering malicious code to the production environment. The pipeline's lack of protection for its configuration and secrets enables this tampering.

### What can go wrong?

A compromised CI/CD pipeline is one of the highest-impact attack vectors in cloud environments. Because the pipeline runs with deployment credentials and has write access to production infrastructure, a successful attack can result in malicious code being shipped to all environments simultaneously. Supply chain attacks of this kind are particularly difficult to detect because the malicious changes arrive through the same trusted channels as legitimate code.

### What are we going to do about it?

Treat the CI/CD pipeline as a critical security boundary and harden it accordingly.

1. Store all secrets in a dedicated secrets manager (e.g., AWS Secrets Manager, HashiCorp Vault) and inject them at runtime with short-lived credentials rather than storing them as persistent pipeline variables.
2. Enforce branch protection rules so that pipeline configuration changes require code review and approval before being merged.
3. Restrict which branches and events can trigger builds that have access to production credentials, preventing pull requests from untrusted forks from accessing sensitive variables.
4. Enable audit logging for all pipeline executions and alert on changes to pipeline configuration or unexpected secrets access.