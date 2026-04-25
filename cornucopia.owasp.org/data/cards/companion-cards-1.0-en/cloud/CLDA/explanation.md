## Scenario: Invent your own Cloud threat

Inventing a cloud security threat can lead to:

1. **Identity and Access Abuse:** Exploiting misconfigured IAM roles, service accounts, or trust relationships to gain unauthorised access to cloud resources.
2. **Data Exposure:** Accessing sensitive data through publicly accessible storage, misconfigured APIs, or insufficient encryption controls.
3. **Supply Chain Compromise:** Tampering with IaC templates, build pipelines, or container images to introduce malicious code into cloud deployments.
4. **Lateral Movement:** Pivoting from one compromised cloud service, account, or container to reach broader or more sensitive environments.

## Threat Modeling

### STRIDE

The appropriate STRIDE category depends on the specific threat you create and the way the agent is misused.

### What can go wrong?

Unauthorised access, data breaches, supply chain compromise, lateral movement across accounts dwell time due to insufficient monitoring.

### What are we going to do about it?

Strong identity controls, least-privilege access, environment isolation, supply chain integrity, and comprehensive monitoring form the foundations of cloud security.

1. **Enforce Least Privilege:** Scope all IAM roles, service accounts, and managed identities to the minimum permissions required for their specific function.
2. **Isolate Environments:** Use separate accounts or projects per environment, and enforce strict cross-account trust policies with organizational guardrails.
3. **Protect the Supply Chain:** Sign and verify build artefact, enforce IaC policy checks, and scan container images before promotion to production.
4. **Monitor and Alert:** Enable audit logging in all regions and accounts, and alert on anomalous access, privilege changes, and configuration modifications.
5. **Secure Secrets:** Use dedicated secrets managers with per-service access controls, avoid shared credentials, and rotate secrets regularly.
6. **Harden the Root Account:** Protect root credentials with hardware multi-factor authentication, store them securely, and never use them for routine operations.