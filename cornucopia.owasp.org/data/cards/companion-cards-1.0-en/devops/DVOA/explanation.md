## Scenario: Invent your own DevOps threat

Inventing a DevOps threat could lead to:

1. **Compromised Build Integrity**: Tampering with build processes, scripts, or environments to produce malicious or unverified outputs.
2. **Infrastructure Takeover**: Gaining control of CI/CD systems, orchestration platforms, or deployment infrastructure.
3. **Secret Exposure**: Discovering credentials, tokens, or keys in unexpected locations across the development and deployment lifecycle.
4. **Supply Chain Compromise**: Introducing malicious code through dependencies, shared components, or trusted integrations.
5. **Compromised artifacts**: Generating and distributing artifacts with altered functionality, backdoors, or bugs. 
6. **Loss of Availability**: Destroying or corrupting critical infrastructure, code, or data in ways that cannot be recovered from.
7. **Lateral Movement**: Using access gained in one part of the DevOps ecosystem to reach other systems, environments, or data.
8. **Audit and Accountability Failures**: Performing malicious actions that cannot be attributed or investigated due to gaps in logging and monitoring.

## Threat Modeling

### STRIDE

Any of the STRIDE categories may be applicable, but common impacts in DevOps scenarios include **Tampering** (modifying code, artifacts, or configurations), **Elevation of Privilege** (gaining access beyond intended scope through DevOps tooling), and **Information Disclosure** (exposing secrets or sensitive data through development processes).

### What can go wrong?

Compromised builds, infrastructure takeover, leaked secrets, supply chain attacks, permanent data loss, lateral movement, and audit failures.

### What are we going to do about it?

The following general principles apply to most DevOps threats:

1. **Defense in Depth**: Don't rely on a single control—layer your defenses across the development and deployment lifecycle.
2. **Least Privilege**: Give accounts, services, and pipelines only the permissions they actually need.
3. **Immutability and Integrity**: Protect artifacts, configurations, and infrastructure definitions so that unauthorized changes are prevented or detected.
4. **Secrets Management**: Use dedicated solutions to manage and rotate secrets. Don't leave them in code, configs, or logs.
5. **Monitoring and Auditability**: Log significant actions across the DevOps ecosystem so you can investigate when something goes wrong.
6. **Dependency Hygiene**: Know what dependencies you use, keep them up to date, and verify they are what you expect.
7. **Tested Recovery**: Backups only count if you have tested restoring from them. Document and practice recovery procedures.
8. **Separation of Duties**: Make sure no single person has unchecked control over critical processes like production deployment.
9. **Configuration as Code**: Define configurations in version-controlled code so they are reviewable, reproducible, and auditable.
10. **Regular Review**: Revisit your security setup as the infrastructure and team evolve - what was sufficient six months ago may not be today.
