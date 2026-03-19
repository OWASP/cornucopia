## Scenario: Adrian’s Manipulation of Authorization Controls

Consider a scenario where Adrian, exploiting weaknesses in an application's security framework, manages to influence or alter authorization controls and permissions. This allows him to bypass them. The vulnerability arises from:

1. **Alterable Authorization Controls:** The system's authorization controls are not adequately protected, allowing for their modification.

2. **Insufficient Monitoring and Restrictions:** Lack of robust monitoring and strict restrictions enables unauthorized changes to permissions and access controls.

### Example

Adrian targets an enterprise application that has loosely managed authorization configurations. He gains access to the system’s administrative tools, which lack sufficient security checks. Once there, he modifies the authorization settings, granting himself higher-level permissions. This manipulation allows him to access confidential data and functionalities, which are typically restricted to higher-privileged users, such as system administrators.

## Threat Modeling

### STRIDE

This scenario maps primarily to STRIDE: **Elevation of Privilege** (EoP).
Adrian modifies authorization settings. That means that he is **Tampering** with the settings, but as a direct result, he grants himself higher privileges, which is **Elevation of Privilege**.

### What can go wrong?

Such vulnerabilities can lead to unauthorized access, data breaches, and potentially full system compromise.

For more things that can go wrong, see the [Common Attack Patterns related to this card](#mapping 'Common Attack Patterns related to this card [internal]') in the table below.

### What are we going to do about it?

1. Ensure that all mechanisms for altering authorization controls and permissions are strictly secured and accessible only by highly trusted roles.
2. Implement robust monitoring systems to detect and alert any unauthorized changes to authorization configurations.
3. Regularly audit authorization controls and permissions to ensure they have not been tampered with and remain appropriate for user roles.
4. Use only trusted system objects, e.g. server side session objects, for making access authorization decisions.
5. Restrict access to user and data attributes and policy information used by access controls.
6. Server side implementation and presentation layer representations of access control rules must match.

For detailed advice on how to mitigate threats related to the card, see the [ASVS and OWASP Developer Guide requirements ](#mapping 'ASVS and OWASP Developer Guide requirements [internal]') in the table below.
