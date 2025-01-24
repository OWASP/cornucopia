### Scenario: Kelly's Exploitation of Non-Secure Default Authorization 
Consider a situation where Kelly bypasses authorization controls due to their failure to default to a secure state. This issue arises because: 

1. **Non-Secure Default Settings:** In case of a failure in the authorization process, the system defaults to allowing access, rather than denying it. 

### Example: 

Kelly targets an online service platform that has an authorization mechanism with a non-secure fallback. During a system error or when the authorization service fails, the system is configured to grant access by default as a means to avoid disruption of service. Kelly deliberately triggers errors in the authorization process, and each time, the system defaults to allowing her access to restricted areas that she would normally not have permission to view. 

### Risks: 

This vulnerability can lead to unauthorized access to sensitive data or functionalities, potentially compromising the entire system’s security. 

### Mitigation: 

- Configure all authorization mechanisms to default to a 'deny access' state in the event of any failure or error. 
- Regularly test and validate the authorization process to ensure it behaves securely during system errors or downtimes. 
- Implement robust monitoring and alerting mechanisms to quickly detect and respond to failures in the authorization system. 