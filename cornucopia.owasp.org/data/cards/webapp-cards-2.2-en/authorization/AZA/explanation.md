## Scenario: Invent your own Authorization threat

Inventing an authorization threat could lead to:

1. **Privilege Escalation**: Users access admin features, financial controls, or sensitive operations.
2. **Data Exposure**: Accessing confidential records, PII, or sensitive business data.
3. **Unauthorized Actions**: Performing operations like deleting records, approving transactions, or changing configurations.
4. **Bypassing Business Rules**: Exploiting logic flaws to do things like submit duplicate orders, skip approval workflows, or manipulate dates.
5. **Repudiation / Audit Issues**: Unauthorized actions may not be traceable to the attacker.
6. **Chaining Attacks**: Authorization flaws can combine with other vulnerabilities (like injection or session attacks) for greater impact.
7. **Potential Denial of Service**: Overloading admin functionality or removing access for legitimate users.

## Threat Modeling

### STRIDE

Any of the STRIDE categories may be applicable, but primary impact is usually **Elevation of Privilege**, since bypassing authorization typically means doing more than you should.

### What can go wrong?

Privilege escalation, data leaks, unauthorized actions, bypassed business rules, audit failures, chained attacks, potential DoS.

### What are you going to do about it?

Centralized controls, least privilege, rechecking per request, logging, segregation of duties, secure storage, fail-secure, periodic review/testing.

1. **Centralized Authorization**: All access decisions go through a single, trusted module.
2. **Principle of Least Privilege**: Users get only the permissions they need for their tasks.
3. **Role-Based or Attribute-Based Access Controls**: Clearly define roles and attributes, enforce strict access policies.
4. **Recheck Authorization**: Don’t trust previous checks; validate for every request or critical operation.
5. **Audit and Logging**: Log all access attempts, including failed and unauthorized ones.
6. **Segregation of Duties**: Avoid a single user having too many critical permissions.
7. **Regular Review and Testing**: Periodically review roles, permissions, and test for flaws.
8. **Fail Secure**: Deny access by default if the system is unsure or fails.
9. **Input Validation**: Prevent manipulation of authorization parameters (e.g., user IDs, role fields).
10. **Protect Authorization Data**: Store roles, privileges, and ACLs securely to prevent tampering.