## Scenario: Siddharth's Cross-Product Data Access via a Shared Cloud Account

Siddharth exploits the absence of resource isolation within a shared cloud account to access data belonging to multiple products, using resource metadata and tags to identify and target them. This occurs because:

1. **Multiple Products or Teams Sharing a Single Cloud Account:** Resources belonging to different products, business units, or customers are deployed into the same cloud account without technical isolation boundaries.

2. **Insufficiently Scoped IAM Policies:** IAM roles grant access to all resources of a given type within the account rather than scoping access to specific resource identifiers or tag conditions.

### Example

Siddharth gains access to a service account used by one product team within a large shared AWS account. He begins by listing all S3 buckets in the account and notes that their names follow a predictable pattern. He reads their tags to identify which product each bucket belongs to. Because the IAM role he has access to was granted `s3:GetObject` on `arn:aws:s3:::acme-*` rather than just the bucket belonging to his product, Siddharth can read objects from every product's buckets in the account. He downloads database backups, configuration files, and customer data belonging to three other product teams, none of which he has any legitimate reason to access.

## Threat Modeling

### STRIDE

The scenario maps directly to STRIDE: **Elevation of Privilege**.

Siddharth escalates from access to a single service account to unauthorized control over resources belonging to multiple products. By exploiting insufficiently scoped IAM policies and the absence of resource-level isolation within the shared cloud account, he elevates his effective permissions beyond his intended role. He gains the ability to read, and potentially modify or delete, data and infrastructure belonging to teams he has no legitimate authorization to access. 

### What can go wrong?

Shared cloud accounts without strong resource isolation create a flat permission model where a single compromised identity can access data across an entire organization. This undermines product-level data boundaries, compliance requirements, and the ability to contain the impact of a breach. In multi-tenant systems, this may result in one customer's data being accessible to another.

### What are we going to do about it?

Enforce resource isolation at the account level or through fine-grained resource policies that cannot be bypassed by tag inspection alone.

1. Prefer a dedicated account per product or per environment to create hard isolation boundaries enforced by the cloud provider's account model.
2. Where a shared account is unavoidable, scope all IAM policies to specific resource identifiers or resource-tag conditions, and protect tags from modification by unprivileged principals.
3. Apply resource-based policies (e.g., S3 bucket policies) to explicitly deny access from identities outside the owning product's roles.
4. Regularly audit effective permissions using IAM Access Analyzer or equivalent tools to detect and remediate over-broad policies.
