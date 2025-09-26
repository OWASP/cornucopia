## Scenario: Mark’s Access Without Authentication

Imagine a situation where Mark gains access to resources or services in a system that lacks proper authentication controls. This occurs because:

1. **Absence of Authentication Requirements:** Certain resources or services don’t have any authentication checks in place.

2. **Misplaced Assumptions About Authentication:** The system mistakenly assumes that authentication is handled by another system or was already performed in a previous action.

### Example

Mark discovers that an internal reporting tool in a corporate network doesn’t require users to authenticate themselves. This tool, designed for ease of access within the network, is mistakenly left accessible without any login procedure. Mark accesses this tool and retrieves sensitive company data. The system was assumed to be secure as it was only accessible internally, but this oversight allowed for unauthorized access without any form of identity verification.

## Threat Modeling

### STRIDE

This scenario maps directly to STRIDE: **Spoofing**.

**Spoofing** is about pretending to be a legitimate user or entity.
Even though no credentials are provided, Mark gains access to the system without authentication, effectively being treated as a valid user.
The system’s failure is that it assumes authentication is done elsewhere or not needed — this lets an attacker bypass identity verification entirely.

### What can go Wrong?

Such an absence of authentication exposes the system to unauthorized access, potentially leading to data breaches and exploitation of sensitive resources.

### What are you going to do about it?

1. Implement authentication requirements for all resources and services, regardless of their perceived security level.
2. Clearly define and document authentication responsibilities to ensure no system component is left unprotected due to assumptions about other systems’ security measures.
3. Regularly audit the entire system to identify and rectify any areas lacking proper authentication controls.

For detailed advice on how to mitigate threats related to the card, see the [ASVS and OWASP Developer Guide requirements ](#mapping 'ASVS and OWASP Developer Guide requirements [internal]') in the table below.
