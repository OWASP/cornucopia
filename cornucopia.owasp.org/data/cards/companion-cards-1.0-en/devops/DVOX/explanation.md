## Scenario: Patricia's Exploitation of Stale Credentials and Excessive Privileges

Consider a scenario where Patricia gains unauthorized access to sensitive systems by exploiting DevOps credentials, identities, and services that are obsolete or overly permissive. This vulnerability arises from:

1. **Stale Credentials and Identities:** Former team members' accounts, old service accounts, or API keys that are no longer needed but remain active.

2. **Excessive Privileges:** Accounts and services that have been granted more access than they need, creating unnecessary attack surface.

### Example

Patricia discovers that a service account created for a decommissioned integration still has broad access to the deployment infrastructure. The account's credentials were shared in a configuration file months ago and never rotated or revoked. Using these credentials, Patricia gains access to production deployment tools and reads sensitive configuration data. She also finds that the account has write access to resources it never needed, allowing her to modify deployment configurations.

## Threat Modeling

### STRIDE

This scenario maps primarily to STRIDE: **Elevation of Privilege** and **Information Disclosure**.

**Elevation of Privilege** applies because Patricia uses obsolete or overly privileged credentials to gain access beyond what any current legitimate use would require, effectively bypassing access controls.

**Information Disclosure** fits because the unauthorized access allows Patricia to read sensitive data, such as configuration details, secrets, and other information she is not authorized to see.

### What can go wrong?

Stale credentials and excessive privileges accumulate over time and create persistent, often invisible, attack surface. This can manifest in various forms, including but not limited to:

- Unauthorized access through forgotten service accounts or API keys
- Exploitation of credentials that were never rotated after team changes
- Privilege creep where accounts accumulate permissions over time without review
- Lateral movement using overly permissive service accounts
- Difficulty detecting unauthorized access because the credentials used are technically valid

### What are we going to do about it?

1. When a project or integration is decommissioned, clean up its service accounts, API keys, and credentials. Don't leave them around "just in case."
2. When someone leaves the team, make sure their access to DevOps infrastructure is revoked promptly.
3. Request only the permissions you actually need for service accounts and API keys. Avoid broad or admin-level access out of convenience.
4. If your platform supports credential expiration or automatic rotation, use it. Short-lived credentials limit the damage if one is compromised.
5. Periodically check what service accounts and API keys are still active in your projects, and remove any that are not in use. Check if they still need all the permissions they have.
6. Use multi-factor authentication for access to sensitive DevOps infrastructure where the option is available.
7. Where supported, prefer ephemeral tokens or workload identities over long-lived credentials.
