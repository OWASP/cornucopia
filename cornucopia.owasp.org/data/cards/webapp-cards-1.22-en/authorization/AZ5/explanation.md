### Scenario: Chad’s Unauthorized Access Due to Insufficient Authorization 
Imagine a scenario where Chad gains access to various resources that he should not be able to access. This occurs due to: 

1. **Missing Authorization Checks:** Certain resources lack proper authorization controls. 

2. **Excessive Privileges:** The system grants more privileges than necessary, failing to adhere to the principle of least privilege. 

### Example: 

Chad discovers that a corporate application does not enforce strict authorization checks on certain resources, such as temporary files, system properties, and logs. He exploits this oversight to access sensitive documents and configuration data meant for higher-privileged users. Additionally, due to the system granting excessive privileges to regular users, Chad can access and interact with services and processes usually reserved for administrators. 

### Risks: 

Such vulnerabilities can lead to unauthorized access to critical resources, potentially resulting in data breaches, system manipulation, and other security compromises. 

### Mitigation: 

- Implement comprehensive authorization checks for all resources, ensuring only appropriately privileged users can access them. 
- Adhere to the principle of least privilege, granting users only the permissions they need to perform their duties. 
- Regularly audit and review user privileges and resource access controls to identify and rectify any excesses or lapses in authorization. 