### Scenario: Yuanjing’s Unauthorized Access to Restricted Functions 
Picture a scenario where Yuanjing, exploiting weak authorization controls, gains access to application functions, objects, or properties that he is not authorized to access. This vulnerability arises from: 

1. **Inadequate Authorization Checks:** The application fails to rigorously verify user permissions for accessing specific functions, objects, or properties. 

2. **Insufficient Segregation of Privileges:** Different levels of user access are not clearly defined or enforced, allowing lower-level users to access restricted functionalities. 

### Example: 

Yuanjing finds that a business application does not enforce strict authorization checks on certain administrative functions. Despite being a regular user, he manages to access administrative settings and confidential data objects. The application, designed with inadequate role-based access controls, allows Yuanjing to perform actions and view data typically restricted to users with higher privileges, like system administrators. 

### Risks: 

This type of security lapse can lead to unauthorized access to critical application functionalities, potential data breaches, and misuse of sensitive system properties. 

### Mitigation: 

- Implement robust, role-based authorization checks that rigorously define and enforce access levels for different user roles. 
- Ensure that each application function, object, and property is protected by appropriate authorization verifications. 
- Regularly review and update the authorization system to address new functionalities and changing user roles. 