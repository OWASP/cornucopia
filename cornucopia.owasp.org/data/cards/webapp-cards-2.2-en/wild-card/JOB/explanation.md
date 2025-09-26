## Scenario: Bob's application compliance abuse

Bob manipulates the application, its configuration, or data flows in a way that causes it to violate laws, regulations, contractual obligations, or internal organizational policies through e.g: unauthorized changes, misconfigurations, or exploitation of logic flaws.

## Threat Modeling

### STRIDE

Primary impact depends on the impact of attack:

1. **Tampering**: The attacker changes application behavior, configuration, or stored data to cause non-compliance.
2. **Elevation** of Privilege (EoP): By gaining higher privileges, the attacker can override controls that enforce compliance.
3. **Information Disclosure**: Exposing regulated or sensitive data inappropriately may violate privacy regulations.
4. **Repudiation**: If logs or audit trails can be altered, proving compliance or tracking violations becomes impossible.

### What can go Wrong?

1. Non-compliance with regulations such as GDPR, HIPAA, or PCI DSS.
2. Violations of contractual obligations or internal policies.
3. Financial penalties, legal actions, or regulatory fines.
4. Reputational damage or loss of customer trust.
5. Data integrity or confidentiality violations.
6. Inaccurate compliance reporting (e.g., SAQ misreporting for PCI DSS).
7. Operational disruptions due to disabled or insecure processes.

### What are you going to do about it?

1. **Access Controls & Privilege Management**: Restrict who can modify configuration, components, or application logic.
2. **Change Management**: Enforce approval workflows and documented change procedures for all updates.
3. **Audit & Logging**: Maintain tamper-evident logs for compliance monitoring and forensic purposes.
4. **Continuous Monitoring**: Detect unauthorized changes, insecure connections, or unapproved components.
5. **Data Protection & Segregation**: Ensure personal/business data separation, consent enforcement, and secure storage.
6. **Patch & Configuration Management**: Keep software, components, and infrastructure up-to-date and securely configured.
7. **Policy Alignment**: Map application processes to relevant regulations and review periodically.
8. **Backup & Recovery**: Implement procedures to restore compliant states if misconfigurations or compromises occur.
9. **Validation and Monitoring**: Continuously check that configurations, workflows, and data handling comply with mandates.
10. **Regulatory Awareness**: Map application components to relevant regulations and perform periodic compliance reviews.
