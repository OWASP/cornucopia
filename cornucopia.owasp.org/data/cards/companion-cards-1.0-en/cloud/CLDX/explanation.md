## Scenario: Adrian's Backdoored Infrastructure-as-Code Templates

Adrian introduces backdoored Infrastructure-as-Code (IaC) templates into the organization's version control system, causing vulnerable or maliciously configured cloud environments to be deployed at scale. This occurs because:

1. **Insufficient Review of IaC Changes:** Pull requests modifying Terraform, CloudFormation, or similar templates are merged without thorough security review, allowing subtle backdoors — such as permissive security group rules or unexpected IAM bindings — to go unnoticed.

2. **Broad Write Access to the IaC Repository:** Many contributors can merge changes to IaC templates without requiring approval from a security reviewer or a second maintainer.

### Example

Adrian is a contractor with write access to the infrastructure repository. He submits a Terraform pull request that appears to update an autoscaling group's instance type for cost optimization. Buried within the change is a modification to the associated IAM instance profile, adding a managed policy that grants full S3 read access across all buckets in the account. He also adds a permissive inbound rule to the security group, opening port 22 from all addresses with a comment describing it as "temporary for debugging." The pull request is approved by a colleague who does not notice the embedded IAM and security group changes. The configuration is applied to all environments, and every new compute instance launched across the organization inherits the backdoored profile.

## Threat Modeling

### STRIDE

The scenario maps directly to STRIDE: **Tampering**.

Adrian modifies the IaC templates that define the organization's cloud infrastructure, causing all subsequent deployments to be based on a corrupted baseline. The changes are persistent, every environment provisioned from the backdoored templates inherits the vulnerability, making this a supply chain attack on the cloud infrastructure definition itself.

### What can go wrong?

A backdoored IaC template is a force multiplier: a single malicious change can affect every environment, account, and service deployed from that template going forward. The impact is difficult to contain because the vulnerability is baked into the deployment process itself. Affected environments may expose data, accept unauthorized network connections, or grant excessive permissions and because the change arrived through the normal deployment pipeline, it may not be flagged by runtime security tools.

### What are we going to do about it?

Treat IaC templates as security-critical code and apply the same review and validation standards as application source code.

1. Require at least two reviewer approvals on any pull request that modifies IaC templates, and ensure at least one reviewer has cloud security expertise.
2. Integrate automated IaC security scanning (e.g., Checkov, tfsec, KICS) into the CI/CD pipeline so that policy violations are flagged before a plan is reviewed or applied.
3. Restrict who can merge to the IaC repository and apply branch protection rules that prevent self-approval and require status checks to pass.
4. Maintain an immutable audit log of all infrastructure state changes and alert on unexpected additions of IAM bindings, security group rules, or networking changes.