## Scenario: Peter’s Exploitation of Self-Built Weak Session Controls

Imagine a scenario where Peter exploits vulnerabilities in an application that relies on self-built, potentially weak session management controls instead of using a standard, well-tested framework or module. This situation arises due to:

1. **Self-Built Session Management Systems:** The application uses custom-built session management mechanisms that may not adhere to industry best practices.

2. **Lack of Standard Framework Implementation:** Instead of leveraging proven and tested frameworks or modules, the system relies on in-house solutions that might lack robustness.

### Example

Peter discovers that a bespoke e-commerce platform uses a custom session management system developed in-house. This system, while functional, does not incorporate the latest security practices and is vulnerable to session hijacking and fixation attacks. Capitalizing on these weaknesses, Peter manipulates session tokens to gain unauthorized access to user accounts, bypassing the inadequate session control mechanisms.

## Threat Modeling

### STRIDE

This scenario maps primarily to STRIDE: **Spoofing**.

**Spoofing** is about impersonating a legitimate user or entity.
Peter exploits weaknesses in a self-built or weak session management system, allowing him to bypass session controls and assume the identity of legitimate users.
The attack is centered on unauthorized impersonation via inadequate session enforcement, making **Spoofing** the correct primary category.

### What can go Wrong?

Custom-built session management systems that lack the rigor of standard frameworks can lead to serious security breaches, including unauthorized access and data theft.

### What are you going to do about it?

1. Where possible, replace self-built session management systems with standard, well-tested frameworks or modules known for robust security.
2. If a custom solution is necessary, ensure it is developed according to industry best practices and undergoes rigorous security testing.
3. Regularly review and update the session management system to incorporate the latest security advancements and patches.

For detailed advice on how to mitigate threats related to the card, see the [ASVS and OWASP Developer Guide requirements ](#mapping 'ASVS and OWASP Developer Guide requirements [internal]') in the table below.
