## Scenario: Eleftherios's Cross-Service Pivot via Shared Identities and Secrets

Eleftherios breaches one cloud service and uses shared identities, deployment pipelines, and secrets to move laterally into other cloud services within the same organisation. This occurs because:

1. **Service Identities Shared Across Multiple Systems:** A single service account, managed identity, or API key is used by multiple cloud services, so compromising one service yields credentials that grant access to others.

2. **Secrets Stored in Shared or Insufficiently Scoped Locations:** Secrets such as database passwords, API keys, and cloud credentials are stored in a shared secrets manager path that is readable by multiple services.

### Example

Eleftherios exploits a server-side request forgery (SSRF) vulnerability in a public-facing API service to reach the cloud instance metadata endpoint and retrieve the attached managed identity's access token. He discovers that the same managed identity is used by the internal data processing service — it was reused to simplify credential management. Using the token, Eleftherios queries the shared secrets path and retrieves database credentials, a payment provider API key, and the signing key for user session tokens. With these secrets, he accesses the payment service's database, forges user sessions, and reads records from the data processing service.

## Threat Modeling

### STRIDE

The scenario maps directly to STRIDE: **Elevation of Privilege**.

Eleftherios starts with access limited to one service and escalates to multiple unrelated services by exploiting the trust and credential sharing that connects them. The pivot does not require breaking any additional authentication mechanism, the shared identity already has the necessary access. A secondary category of **Information Disclosure** applies when the credentials retrieved from the shared secrets store expose sensitive data from multiple systems.

### What can go wrong?

When cloud services share identities and secrets, a breach of any one of them creates a single point of failure for all of them. An attacker who compromises a low-value service can gain access to high-value ones simply by following the credential sharing paths. This undermines the security value of service isolation.

### What are we going to do about it?

Eliminate shared identities and secrets between services, and enforce strict credential isolation per service.

1. Assign each cloud service a dedicated, purpose-specific identity with permissions scoped only to the resources that service needs. Never share managed identities or service accounts between services.
2. Store secrets in isolated namespaces or paths within the secrets manager and restrict read access to the specific service identities that require each secret.
3. Audit secrets access logs regularly to detect cross-service access patterns that fall outside expected behavior.
4. Protect against SSRF by blocking outbound application requests to instance metadata endpoints, and enforce metadata service hardening.
