## Scenario: Richard's Bypass of Incomplete Centralized Authorization Controls

Imagine a situation where Richard bypasses an application’s security by exploiting the lack of comprehensive application of centralized authorization controls. This occurs because:

1. **Selective Application of Authorization Controls:** The centralized authorization mechanism is not uniformly applied across all interactions within the application.

2. **Oversight in Certain Interactions:** Specific actions or areas within the application lack the same level of authorization scrutiny that others have.

### Example

Richard targets a corporate application that uses centralized authorization for main functionalities like accessing user profiles and dashboards. However, he notices that newer modules, such as a file-sharing feature, do not integrate these centralized controls as effectively. Richard exploits this gap to access and distribute sensitive files that he should not have access to, leveraging the less secure file-sharing module that bypasses the usual authorization checks.

## Threat Modeling

### STRIDE

This scenario maps primarily to STRIDE: **Elevation of Privilege**.

**Elevation of Privilege** (EoP) occurs when an attacker gains access to resources or actions they are not authorized for.
Richard exploits the fact that centralized authorization is not applied consistently across all modules. By targeting modules that bypass the central controls, he accesses sensitive files and actions beyond his permissions.
The core issue is inadequate enforcement of authorization, allowing a user to perform higher-privilege operations than intended.

### What can go wrong?

Such inconsistencies in authorization control application can lead to unauthorized access to sensitive functionalities and data, posing a significant risk to the application’s security.

For more things that can go wrong, see the [Common Attack Patterns related to this card](#mapping 'Common Attack Patterns related to this card [internal]') in the table below.

### What are you going to do about it?

Centralized authorization routines are a good programming practice, but like other routines, developers need to understand how they work, how to use them and any limitations. Such routines can be tested independently of other code and not only provide assurance on the quality, but also make refactorization an easy task and eliminate code duplicates and bad interpretations.

1. Ensure that centralized authorization controls are consistently and comprehensively applied across all user interactions within the application, including all modules and features.
2. Server side implementation and presentation layer representations of access control rules must match.
3. Conduct thorough security reviews, especially when integrating new features or updates, to ensure they adhere to established authorization standards.
4. Regularly audit and update authorization protocols to maintain a high level of security throughout the application.

For detailed advice on how to mitigate threats related to the card, see the [ASVS and OWASP Developer Guide requirements ](#mapping 'ASVS and OWASP Developer Guide requirements [internal]') in the table below.
