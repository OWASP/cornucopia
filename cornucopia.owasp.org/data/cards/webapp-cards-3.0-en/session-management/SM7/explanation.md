## Scenario: Graham's Exploitation of Inadequate Session Termination

Imagine a situation where Graham takes advantage of a system’s flawed session termination process. This becomes possible because:

1. **Absence of Log Out Function:** The system lacks a clear, accessible log out function.

2. **Ineffective Log Out:** Even when users attempt to log out, the session is not properly terminated.

3. **Complex Log Out Process:** The log out function is not easily accessible or user-friendly, leading to users inadvertently leaving sessions active.

### Example

Graham targets a web application where users find it difficult to locate the log out button due to its obscure placement. Adam, a user of the application, believes he has exited the session, but in reality, the session remains active. Graham, seizing this opportunity, accesses the still-active session from Adam's device or a public computer Adam used, gaining unauthorized access to Adam’s account and sensitive information.

## Threat Modeling

### STRIDE

This scenario maps primarily to STRIDE: **Spoofing**.

**Spoofing** is about impersonating a legitimate user.
Graham exploits the fact that Adam’s session remains active after he “logs out” or fails to log out, allowing him to assume Adam’s identity without needing credentials.
The root issue is unauthorized impersonation via an active session, making **Spoofing** the correct primary category.

### What can go wrong?

This flaw can lead to unauthorized session access and potential data breaches, as attackers exploit sessions that users believe to be safely closed.

For more things that can go wrong, see the [Common Attack Patterns related to this card](#mapping 'Common Attack Patterns related to this card [internal]') in the table below.

### What are we going to do about it?

Users should be able to log out from any pages protected by access control (authentication and authorisation checks). The logout functionality should fully terminate the associated session or connection such that the session identifier is no longer usable.

1. Ensure the log out function is clearly visible and easily accessible on all interfaces of the application.
2. Design the log out process to completely terminate the session on the server side, not just on the client device.
3. Conduct user experience testing to ensure the log out process is intuitive and effective.

For detailed advice on how to mitigate threats related to the card, see the [ASVS and OWASP Developer Guide requirements ](#mapping 'ASVS and OWASP Developer Guide requirements [internal]') in the table below.
