## Scenario: Michael's Access Through Unsecured Administrative Tools

Consider a situation where Michael bypasses standard application protocols to gain access to data by exploiting inadequately secured administrative tools or interfaces. This vulnerability arises due to:

1. **Lack of Robust Security in Administrative Tools:** The tools designed for system management and maintenance do not have sufficient protective measures.

2. **Inadequate Access Controls for Administrative Interfaces:** The interfaces used for administrative purposes are easily accessible and lack stringent access restrictions.

3. **Weak Authentication Mechanisms:** The authentication processes for accessing administrative tools are missing or not strong enough, allowing unauthorized users to gain entry.

### Example

Michael discovers that a web application’s administrative interface is accessible through a common URL and is only protected by a weak password. Leveraging this, he gains access to the administrative panel where he can view, modify, and delete sensitive data. This unauthorized access is facilitated by the lack of multi-factor authentication, inadequate password policies, and the absence of monitoring mechanisms on the administrative interface.

## Threat Modeling

### STRIDE

The STRIDE category applicable here is **Elevation of Privilege** (EoP).

Michael is gaining access to administrative functions and sensitive data that he should not be able to access with his current privileges.
The core impact is that he is escalating his access from a normal user (or unauthenticated user) to an administrative level.
Even though he can view and modify data, the underlying issue is that privilege boundaries are bypassed, which aligns with **Elevation of Privilege** rather than **Information Disclosure** (which focuses only on unauthorized reading) or **Tampering** (which focuses on modifying data within authorized access).

### What can go wrong?

Unsecured administrative tools and interfaces can lead to major data breaches, unauthorized access to sensitive information, and potential system-wide compromises.

For more things that can go wrong, see the [Common Attack Patterns related to this card](#mapping 'Common Attack Patterns related to this card [internal]') in the table below.

### What are we going to do about it?

1. Implement strong authentication measures, such as multi-factor authentication, for all administrative interfaces and tools.
2. Enforce robust password policies and regular credential updates for system administrators.
3. Restrict access to administrative interfaces to a limited set of authorized IP addresses or networks.
4. Regularly audit and monitor activities performed through administrative tools to detect and respond to unauthorized access.
5. Ensure that administrative tools are not exposed to the public internet unless absolutely necessary, and if they are, implement additional security layers such as VPNs or bastion hosts.

For detailed advice on how to mitigate threats related to the card, see the [ASVS and OWASP Developer Guide requirements ](#mapping 'ASVS and OWASP Developer Guide requirements [internal]') in the table below.
