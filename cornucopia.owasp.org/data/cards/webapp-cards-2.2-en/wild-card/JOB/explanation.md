## Scenario: Bob's application compliance abuse

Bob accidentally or purposely manipulates the application, its configuration, or data flows in a way that causes it to violate laws, regulations, contractual obligations, or internal organizational policies through e.g, unauthorized changes, misconfigurations, or exploitation of logic flaws.

## Threat Modeling

### STRIDE

Primary impact depends on the impact of attack:

1. **Tampering**: The attacker changes application behavior, configuration, or stored data to cause non-compliance.
2. **Elevation** of Privilege (EoP): By gaining higher privileges, the attacker can override controls that enforce compliance.
3. **Information Disclosure**: Exposing regulated or sensitive data inappropriately may violate privacy regulations.
4. **Repudiation**: If logs or audit trails can be altered, proving compliance or tracking violations becomes impossible.

### What can go wrong?

Most web applications will be subject to various legal, regulatory, contractual or other organizational mandates. These are likely to include requirements for data protection/privacy and payment card security. Some examples of risks that might compromise these legal, regulatory, contractual or other organizational mandates are:

1. An undocumented installed component has a vulnerability announced.
2. The server hosting the application makes an unapproved connection to another system.
3. The fully outsourced payment form template is modified to include code from the merchant's server.
4. Personal data relating to an individual is used for a purpose the individual has not consented to.
5. An unauthorised change to configuration data such that some component/service is no longer configured adequately.
6. Unapproved/insecure services/applications are installed/enabled.
7. The terms of service, or privacy statement, are modified without approval.
8. Personal data is inadvertently mixed with business contact data.
9. A scheduled process is accidentally disabled so that quarterly data destruction is stopped, meaning the application no longer complies with the data retention and disposal policy.
10. An unapproved change, or application compromise, could mean the ecommerce application is no longer in compliance, or that compliance reporting requirements change. For example, an ecommerce website might be eligible to assess and report under PCIDSS using Self Assessment Questionnaire (SAQ) A, but due to one of the above issues, the merchant no longer meets the eligibility requirements, and thus has to use controls in and report under the longer SAQ A-EP or full SAQ D.

These risks may materialize accidentally or purposely. Consider:

1. What could change that affects compliance?
2. How will the application detect this?
3. What is the incident response process for these?

A compromise related to legal, regulatory, contractual or other organizational mandates may lead to:

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
