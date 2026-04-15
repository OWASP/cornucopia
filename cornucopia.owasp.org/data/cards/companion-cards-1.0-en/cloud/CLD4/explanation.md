## Scenario: Ryan's Undetected Operations Within Critical Cloud Services

Ryan carries out malicious activity within critical cloud services without triggering any alerts, because the environment lacks sufficient audit logging and security monitoring. This occurs because:

1. **Absent or Disabled Audit Logging:** Cloud audit trails (such as AWS CloudTrail, Azure Monitor, or GCP Cloud Audit Logs) are either not enabled or are configured to exclude sensitive API calls.

2. **No Alerting on Anomalous Behaviour:** Even where logs exist, there is no system in place to detect or alert on unusual access patterns, high-volume API calls, or access to sensitive resources.

3. **Log Retention and Integrity Gaps:** Logs are not retained for a sufficient period, or are stored in a location that an attacker with sufficient access can modify or delete.

### Example

Ryan compromises a cloud service account through a phishing campaign targeting a developer. Once inside the account, he begins exploring the environment: listing S3 bucket contents, describing EC2 instances, reading Secrets Manager entries, and exporting RDS snapshots. All of these actions generate API calls that would normally appear in CloudTrail logs, but logging has been disabled for the affected region. Without an alert or detection system, Ryan operates freely for several weeks, methodically mapping the environment and gathering data. The breach is only discovered after a customer reports suspicious activity on their account.

## Threat Modeling

### STRIDE

The scenario maps directly to STRIDE: **Repudiation**.

Ryan is able to perform significant malicious actions within the cloud environment without any record being generated. In the absence of audit logs, there is no authoritative account of who did what, when, and from where, which makes it impossible to detect, investigate, or attribute the attack. This is a textbook repudiation threat: actions cannot be proven because they were never reliably recorded in the first place.

### What can go wrong?

Without audit logs and monitoring, attackers can operate undetected for extended periods - weeks or months in well-documented cases. By the time a breach is discovered, the attacker has already gathered data, established persistence, and potentially covered their tracks. The inability to reconstruct events makes incident response difficult and regulatory compliance impossible. Legal and forensic obligations may also go unmet simply because the evidence no longer exists.

### What are we going to do about it?

Ensure that all cloud API activity is logged, protected from tampering, and continuously monitored for anomalous behaviour.

1. Enable cloud audit logging in every region and for every account, and verify that it covers management events, data access events, and security-relevant API calls.
2. Store audit logs in a separate, dedicated account or storage location with write-once protection, ensuring that a compromised account cannot delete its own trail.
3. Implement real-time alerting on high-risk actions: disabling logging, creating root access keys, modifying IAM policies, or accessing sensitive data outside of expected patterns.
4. Define and enforce log retention policies that satisfy both operational and regulatory requirements.
