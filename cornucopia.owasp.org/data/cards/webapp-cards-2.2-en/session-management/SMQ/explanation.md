## Scenario: Salim’s Bypass of Inconsistent Session Management

Envision a situation where Salim takes advantage of an application’s inconsistent application of session management. This vulnerability arises because:

1. **Inconsistent Application Across Features:** Different parts of the application implement session management with varying degrees of rigor.

2. **Comprehensive Coverage Lacking:** Certain areas or functionalities of the application lack proper session management controls.

### Example

Salim targets a multi-faceted web application that has robust session management for its main features, like user profiles and dashboards. However, he discovers that the newer modules, such as a recently added chat function, lack similar session controls. He exploits these less secure areas to gain unauthorized access, manipulating session tokens or hijacking sessions where the system’s oversight is most pronounced.

## Threat Modeling

### STRIDE

This scenario maps primarily to STRIDE: **Spoofing**.

**Spoofing** is about impersonating a legitimate user or entity.
Salim exploits areas of the application where session management is not applied consistently, allowing him to bypass session checks and act as an authenticated user without proper authorization.
The attack’s core is unauthorized impersonation via gaps in session enforcement, making **Spoofing** the correct primary category.

### What can go Wrong?

Inconsistencies in session management across an application can lead to unauthorized access and potential exploitation of the less secure areas, compromising overall system security.

### What are you going to do about it?

- Ensure uniform implementation of session management controls across all areas and functionalities of the application.
- Conduct thorough security reviews and testing, especially when integrating new features or modules, to ensure they meet established session management standards.
- Regularly update and harmonize session management practices to maintain comprehensive and consistent security coverage.

For detailed advice on how to mitigate threats related to the card, see the [ASVS and OWASP Developer Guide requirements ](#mapping 'ASVS and OWASP Developer Guide requirements [internal]') in the table below.
