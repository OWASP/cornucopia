### Scenario: Mark’s Access Without Authentication 
Imagine a situation where Mark gains access to resources or services in a system that lacks proper authentication controls. This occurs because: 

1. **Absence of Authentication Requirements:** Certain resources or services don’t have any authentication checks in place. 

2. **Misplaced Assumptions About Authentication:** The system mistakenly assumes that authentication is handled by another system or was already performed in a previous action. 

### Example: 

Mark discovers that an internal reporting tool in a corporate network doesn’t require users to authenticate themselves. This tool, designed for ease of access within the network, is mistakenly left accessible without any login procedure. Mark accesses this tool and retrieves sensitive company data. The system was assumed to be secure as it was only accessible internally, but this oversight allowed for unauthorized access without any form of identity verification. 

### Risks: 

Such an absence of authentication exposes the system to unauthorized access, potentially leading to data breaches and exploitation of sensitive resources. 

### Mitigation: 

- Implement authentication requirements for all resources and services, regardless of their perceived security level. 
- Clearly define and document authentication responsibilities to ensure no system component is left unprotected due to assumptions about other systems’ security measures. 
- Regularly audit the entire system to identify and rectify any areas lacking proper authentication controls. 