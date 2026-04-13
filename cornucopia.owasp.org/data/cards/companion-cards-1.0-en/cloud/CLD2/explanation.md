## Scenario: Dan's Abuse of Overly Permissive Cloud Roles

Dan gains far broader access to cloud services than intended by exploiting excessive permissions granted to an application's service account or identity role. This occurs because:

1. **Over-provisioned IAM Roles:** The application is assigned an IAM role with permissions beyond what it actually needs to function.

2. **No Principle of Least Privilege:** Cloud access policies are not scoped to the minimum required set of actions and resources.

3. **Lack of Role Review:** Permissions are granted once and never revisited, allowing privilege creep to accumulate over time.

### Example

Dan compromises an application's runtime environment and queries the instance metadata service (IMDS) to retrieve IAM role credentials. Because the role was granted overly broad permissions, Dan can access all S3 buckets, describe RDS instances, and invoke Lambda functions across the account. He exfiltrates customer data and pivots laterally throughout the cloud environment.

## Threat Modeling

### STRIDE

The scenario maps directly to STRIDE: **Elevation of Privilege**.

Dan does not break into the cloud account directly, he exploits a service account that has been granted too much power. The excessive permissions allow him to escalate from application-level access to account-wide control.

### What can go wrong?

An application with excessive cloud permissions becomes a powerful entry point for attackers. A single compromise can hand an attacker the keys to the entire cloud account. Sensitive data can be exfiltrated, infrastructure can be destroyed, and the blast radius extends well beyond the application itself.

### What are we going to do about it?

Apply the principle of least privilege to every IAM role, service account, and machine identity in your cloud environment.

1. Grant application identities only the specific permissions they need, scoped to individual resources where possible, never broad wildcards.
2. Regularly audit IAM roles and policies; remove permissions that are no longer required.
3. Enable cloud-native access analysis tools (e.g., AWS IAM Access Analyzer) to detect overly permissive policies automatically.
