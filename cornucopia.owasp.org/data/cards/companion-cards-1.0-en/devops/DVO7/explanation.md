## Scenario: John's Bypass of Deployment Approval Controls

Consider a scenario where John deploys unauthorized or malicious changes directly to production by circumventing deployment approval gates and change control processes. This vulnerability arises from:

1. **Missing Approval Gates:** The deployment pipeline lacks mandatory review or approval steps before changes reach production.

2. **Bypassable Validation Checks:** Existing deployment controls can be skipped or overridden without proper authorization or audit trails.

### Example

John, who gained access to a developer's access credentials, discovers that while the standard deployment workflow requires a peer review and approval, there is also a manual deployment capability intended for emergency rollbacks that has no approval requirement. Since this mechanism is not restricted and has no additional authorization, John uses it to push his changes directly to production, bypassing the review and approval process entirely. The change reaches production without anyone else being aware of it, and it introduces a backdoor that remains undetected until it is executed.

## Threat Modeling

### STRIDE

This scenario maps primarily to STRIDE: **Tampering**.

**Tampering** involves unauthorized modification of a system or its data. John modifies the production environment by deploying unauthorized changes, bypassing the controls that exist to prevent exactly this. The core issue is the ability to alter what runs in production without proper validation or approval.

### What can go wrong?

Bypassed deployment controls allow untested, unauthorized, or malicious changes to reach production. This can manifest in various forms, including but not limited to:

- Deployment of code that has not been reviewed or tested
- Introduction of vulnerabilities or backdoors into production systems
- Changes that break functionality or cause outages without going through validation
- Circumvention of compliance requirements for change management
- Difficulty attributing unauthorized changes due to weak audit trails around deployment

### What are we going to do about it?

1. Set up approval gates for production deployments that no single person can bypass. Every deployment should require at least one other person's sign-off.
2. Check that all deployment paths are covered, including emergency and rollback mechanisms. If there is an "escape hatch," make sure it has equivalent controls or at least extra auditing.
3. Separate duties so that the person who writes the code is not the same person who approves or triggers the deployment.
4. Log all deployment activities: who triggered them, what was deployed, and whether approval gates were satisfied.
6. Add automated checks to the pipeline, such as test suites and security scans, that must pass before deployment can proceed.
7. Protect deployment configurations and pipeline definitions from unauthorized modification.
