## Scenario: Akash's Cross-Account Pivot via Cloud Trust Relationships

Akash compromises one cloud account and uses pre-existing trust relationships between accounts to move laterally into multiple connected environments. This occurs because:

1. **Overly Permissive Cross-Account Role Trust Policies:** IAM roles in other accounts trust the compromised account's principals too broadly, allowing any principal — not just specific, intended ones — to assume them.

2. **Unreviewed Account Trust Topology:** Cross-account trust relationships are established during initial infrastructure setup and never audited, leaving stale or overly broad trust paths in place long after they are needed.

### Example

Akash gains a foothold in a development cloud account through a compromised CI/CD service account. He calls the cloud provider's identity API and discovers that a role in the production account has a trust policy that allows any principal from the development account to assume it — a shortcut introduced by the infrastructure team to simplify deployments. Using this trust relationship, Akash assumes the production role and immediately has read access to production databases, secrets, and audit logs. He then discovers that a third account used for security tooling has a similar trust relationship with the production account, giving him access to the centralized log archive and security baselines as well.

## Threat Modeling

### STRIDE

The scenario maps directly to STRIDE: **Elevation of Privilege**.

Akash begins with limited access in a development account and escalates to privileged environments by exploiting trust relationships that were never intended to be used this way. The pivot uses the legitimate role assumption mechanism built into the cloud provider's identity system.

### What can go wrong?

Cross-account trust vulnerabilities can collapse what appears to be a well-separated multi-account architecture into a single effective blast radius. An attacker who compromises a lower-trust account, such as a development or staging environment — can use trust relationships as stepping stones to reach production data, security controls, or billing and identity management. Because the pivot uses legitimate cloud API calls with valid credentials, it may not be flagged by traditional threat detection systems.

### What are we going to do about it?

Audit and tighten all cross-account trust relationships, and monitor for unexpected role assumption activity.

1. Scope cross-account role trust policies to the minimum required principals — specific roles or services in specific accounts — rather than trusting any principal from an entire account.
2. Require an external ID condition or MFA assertion for cross-account role assumptions that grant access to sensitive environments.
3. Regularly audit all cross-account IAM role trust policies using IAM Access Analyzer or equivalent tools, and remove stale or unnecessary trust paths.
4. Separate environments (development, staging, production, security) into distinct organisational units with policies that prevent cross-environment trust by default.