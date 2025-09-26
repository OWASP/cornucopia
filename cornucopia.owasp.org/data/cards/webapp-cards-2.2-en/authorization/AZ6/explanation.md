## Scenario: Eduardo's Unauthorized Data Access Within Authorized Areas

Visualize a situation where Eduardo, despite having legitimate access to a certain form, page, URL, or entry point within an application, is able to access data beyond his authorized permissions. This happens due to:

1. **Inadequate Granular Authorization Controls:** The application does not enforce sufficient authorization checks at the data level, despite having controls at the page or form level.

2. **Access Control Oversights:** The system fails to differentiate between the authorization for accessing a page and the authorization for accessing specific data on that page.

### Example

Eduardo has legitimate access to a report generation page in a corporate application. However, the page’s backend logic does not adequately verify his permissions for each data set available through the report generator. Eduardo exploits this oversight to access confidential data sets from the report generation tool, which he should not have access to based on his user role.

## Threat Modeling

### STRIDE

This scenario maps primarily to STRIDE: **Elevation of Privilege**.

**Elevation of Privilege** (EoP) occurs when an attacker accesses resources or data beyond what their role or permissions allow.
Eduardo has legitimate access to the page (entry point), but the backend does not enforce proper data-level authorization, allowing him to access confidential data he shouldn’t.
The core issue is improper enforcement of authorization at the data level, enabling privilege escalation within the context of an allowed page.
The consequence of such an action leads to **Information Disclosure** in most cases.

### What can go Wrong?

Such gaps in authorization controls can lead to unauthorized data access, potentially resulting in information leakage, privacy breaches, and compliance violations.

### What are you going to do about it?

1. Implement granular authorization checks that not only control access to pages and forms but also verify user permissions for each data set or action available within these entry points. 
2. Regularly audit and update access control mechanisms to ensure they align with user roles and data sensitivity levels.
3. Conduct thorough security testing to identify and address any potential authorization bypass scenarios.

For detailed advice on how to mitigate threats related to the card, see the [ASVS and OWASP Developer Guide requirements ](#mapping 'ASVS and OWASP Developer Guide requirements [internal]') in the table below.
