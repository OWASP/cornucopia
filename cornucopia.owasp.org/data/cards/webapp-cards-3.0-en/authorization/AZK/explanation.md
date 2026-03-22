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
This can manifest in various forms, including but not limited to:

- Unauthorized changes to authorization controls and permissions
- Bypassing security controls to gain elevated access
- Compromise of sensitive data and system integrity due to unauthorized access
- Potential for further exploitation and lateral movement within the system after gaining elevated privileges

For more things that can go wrong, see the [Common Attack Patterns related to this card](#mapping 'Common Attack Patterns related to this card [internal]') in the table below.

### What are we going to do about it?

1. Ensure that all mechanisms for altering authorization controls and permissions are strictly secured and accessible only by highly trusted roles.
2. Implement robust monitoring systems to detect and alert any unauthorized changes to authorization configurations.
3. Regularly audit authorization controls and permissions to ensure they have not been tampered with and remain appropriate for user roles.
4. Use only trusted system objects, e.g. server side session objects, for making access authorization decisions.
5. Restrict access to user and data attributes and policy information used by access controls.
6. Server side implementation and presentation layer representations of access control rules must match.
7. Defines rules for restricting function-level and data-specific access based on consumer permissions and resource attributes.
8. Consider implementing multiple layers of security, including continuous consumer identity verification, device security posture assessment, and contextual risk analysis when evaluating access to administrative interfaces or critical functions.
9. Ensures that function-level access is restricted to consumers with explicit permissions.
10. Make sure the application enforces authorization rules at a trusted service layer and doesn't rely on controls that an untrusted consumer could manipulate, such as client-side JavaScript.
11. Changes to values on which authorization decisions are made should be applied immediately. Where changes cannot be applied immediately, (such as when relying on data in self-contained tokens), there must be mitigating controls to alert when a consumer performs an action when they are no longer authorized to do so and revert the change. 
12. Communications between backend application components that don't support the application's standard user session mechanism, including APIs, middleware, and data layers, must be authenticated and authorized based on the originating user's permissions, not the intermediary component's permissions.
13. Only use recommended cryptographic functions and libraries for any operations that involve sensitive data or security controls, and ensure they are properly implemented to prevent vulnerabilities that could be exploited for unauthorized access.

For detailed advice on how to mitigate threats related to the card, see the [ASVS and OWASP Developer Guide requirements ](#mapping 'ASVS and OWASP Developer Guide requirements [internal]') in the table below.
