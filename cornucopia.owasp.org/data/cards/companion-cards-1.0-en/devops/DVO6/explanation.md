## Scenario: Daniel's Exploitation of Untested Recovery Processes

Consider a scenario where Daniel causes a permanent loss of applications, source code, or data. Not necessarily by attacking the backups themselves, but because the organization's backup and recovery strategy is incomplete or untested. This vulnerability arises from:

1. **Untested Recovery Processes:** Backups exist, but have never been verified to produce a successful restoration, leaving their usefulness unknown.

2. **Incomplete or Missing Backups:** Critical data, configurations, or code are not included in the backup scope.

3. **Insufficient Documentation and Training:** When an incident occurs, no one knows the exact steps to recover, which systems to prioritize, or where to find the backups.

### Example

After a critical incident that corrupts the production database, the team attempts to restore from backups. They discover that while database dumps were being created nightly, the backup process had been silently failing for weeks due to a storage quota issue that nobody noticed. Even for the backups that do exist, no one on the current team has ever performed a restoration, and the documentation refers to infrastructure that was replaced months ago. What should have been a routine recovery turns into a prolonged outage with permanent data loss.

## Threat Modeling

### STRIDE

This scenario maps primarily to STRIDE: **Denial of Service**.

**Denial of Service** occurs when the availability of a system or data is compromised. Daniel's attack, or simply the failure of the backup strategy, results in permanent loss of critical assets, effectively making the service or data permanently unavailable. The threat here is not just a temporary outage but an irrecoverable loss.

### What can go wrong?

The consequences of failed backup and recovery strategies become apparent only at the worst possible time - during an actual incident. This can manifest in various forms, including but not limited to:

- Silent backup failures going undetected for extended periods
- Backups that exist but cannot be restored due to corruption, incompatibility, or missing components
- Recovery procedures that no one on the current team knows how to execute
- Critical assets (configuration files, infrastructure definitions, secrets) excluded from the backup scope
- Recovery time far exceeding expectations because the process was never practiced

### What are we going to do about it?

1. Actually test restoring from backups regularly, in an environment that mirrors production, to confirm they work. A backup that has never been restored is a backup you cannot trust.
2. Set up monitoring and alerts for backup jobs so you find out immediately when one fails, not when you need it.
3. Make sure backups cover everything you would need to recover: databases, source code, configurations, infrastructure definitions, and secrets.
4. Keep recovery documentation up to date with step-by-step instructions that reflect the current infrastructure, and make sure it is accessible during an incident.
5. Run recovery drills periodically so the team has actually practiced the process before a real incident.
6. Know how long a recovery takes and how much data you can afford to lose, and check that your backup strategy actually meets those needs.
7. Store backups in a separate location so the same incident that takes down production does not also take down your recovery capability.

It might be difficult to define how frequently backups should be performed and how long the recovery should take. Consult your business stakeholders to understand their expectations and, if available, teams responsible for infrastructure to get help translating these expectation into reality.
