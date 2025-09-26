## Scenario: Kate’s Authentication Bypass

Consider a scenario where Kate finds a way to bypass authentication mechanisms due to a system's failure to default securely. This occurs because:

1. **Failure to Fail Securely:** The system is designed in such a way that if authentication processes fail, it defaults to allowing access, rather than denying it.

### Example

Kate targets a web application that has a flaw in its authentication process. During a system failure or when the authentication service is down, instead of denying access, the system defaults to granting access. Kate exploits this by triggering a fault in the authentication mechanism, either through direct attack or by exploiting system instability. As a result, she gains unauthorized access without needing legitimate credentials.

## Threat Modeling

### STRIDE

That scenario maps directly to STRIDE: **Spoofing**

**Spoofing** covers impersonating a legitimate user or system.
Here, Kate bypasses authentication entirely because the system fails insecure (defaults to granting access).
Even though no valid credentials were provided, the system treats her as authenticated → she is spoofing identity. There might be secondary impacts that maps to the other STRIDE categories depending on the context.

### What can go Wrong?

This vulnerability can lead to unauthorized access to sensitive data and systems, potentially compromising the entire network or application.

### What are you going to do about it?

1. Design and configure authentication mechanisms to default to a 'deny access' state in case of any failure.
2. Regularly test and validate the authentication process to ensure it behaves as expected during system errors or downtime.
3. Implement robust monitoring and alerting mechanisms to quickly detect and respond to authentication system failures.

For detailed advice on how to mitigate threats related to the card, see the [ASVS and OWASP Developer Guide requirements ](#mapping 'ASVS and OWASP Developer Guide requirements [internal]') in the table below.
