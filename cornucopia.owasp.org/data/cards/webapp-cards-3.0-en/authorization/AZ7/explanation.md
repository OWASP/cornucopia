## Scenario: Yuanjing’s Unauthorized Access to Restricted Functions

Picture a scenario where Yuanjing, exploiting weak authorization controls, gains access to application functions, objects, or properties that he is not authorized to access. This vulnerability arises from:

1. **Inadequate Authorization Checks:** The application fails to rigorously verify user permissions for accessing specific functions, objects, or properties.

2. **Insufficient Segregation of Privileges:** Different levels of user access are not clearly defined or enforced, allowing lower-level users to access restricted functionalities.

### Example

Yuanjing finds that a business application does not enforce strict authorization checks on certain administrative functions. Despite being a regular user, he manages to access administrative settings and confidential data objects. The application, designed with inadequate role-based access controls, allows Yuanjing to perform actions and view data typically restricted to users with higher privileges, like system administrators.

## Threat Modeling

### STRIDE

This scenario maps primarily to STRIDE: **Elevation of Privilege**.

**Elevation of Privilege** (EoP) occurs when an attacker gains access to functions, objects, or properties beyond their authorized role.
Yuanjing, a regular user, can access administrative functions and confidential objects because the application fails to enforce proper function/object/property-level authorization.
The attack’s core issue is unauthorized access to higher-privilege operations, which is classic **Elevation of Privilege**.
The consequence of such an action leads to **Information Disclosure** in most cases.

### What can go wrong?

This type of security lapse can lead to unauthorized access to critical application functionalities, potential data breaches, and misuse of sensitive system properties.

For more things that can go wrong, see the [Common Attack Patterns related to this card](#mapping 'Common Attack Patterns related to this card [internal]') in the table below.

### What are we going to do about it?

1. Implement least privilege, and restrict users to only the functionality, objects and properties that are required to perform their tasks.
2. Implement robust, role-based authorization checks that rigorously define and enforce access levels for different user roles.
3. Ensure that each application function, object, and property is protected by appropriate authorization verifications.
4. Regularly review and update the authorization system to address new functionalities and changing user roles

For detailed advice on how to mitigate threats related to the card, see the [ASVS and OWASP Developer Guide requirements ](#mapping 'ASVS and OWASP Developer Guide requirements [internal]') in the table below.
