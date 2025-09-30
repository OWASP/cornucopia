## Scenario: Tim’s Manipulation of Data Routing

Envision a scenario where Tim, exploiting weaknesses in authorization controls, influences the direction or forwarding of data within a system. This issue arises from:

1. **Inadequate Authorization Checks:** The system lacks robust authorization mechanisms to verify and control where data is sent or who can redirect it.

2. **Manipulable Data Routing Mechanisms:** Data forwarding or routing functionalities are vulnerable to manipulation.

### Example

Tim discovers that an application’s data export feature does not properly authenticate users’ permissions for forwarding data. He gains access to this feature and begins redirecting sensitive data, originally intended for internal use, to external locations under his control. This redirection occurs without triggering any security alerts, as the system fails to validate whether Tim has the authorization to specify data destinations.

## Threat Modeling

### STRIDE

This scenario maps primarily to STRIDE: **Tampering**.

**Tampering** involves unauthorized modification of data or its flow.
Tim is able to redirect or forward data to locations under his control, altering the intended path or destination of sensitive information.
The core issue is manipulating the system’s handling of data, which fits the definition of **Tampering**.

### What can go wrong?

Such vulnerabilities can lead to unauthorized data disclosure, data breaches, and the potential compromise of sensitive information.

For more things that can go wrong, see the [Common Attack Patterns related to this card](#mapping 'Common Attack Patterns related to this card [internal]') in the table below.

### What are you going to do about it?

1. Implement stringent authorization checks for any function that involves sending, forwarding, or routing data.
2. Ensure that the system verifies user permissions before allowing data to be redirected or exported.
3. Regularly audit and update authorization mechanisms to protect against unauthorized data routing or forwarding.
4. Verify that users not are able to define unauthorized virtual locations/addresses (E.g: db table names, file system paths, sms, email, domains and url paths ).

For detailed advice on how to mitigate threats related to the card, see the [ASVS and OWASP Developer Guide requirements ](#mapping 'ASVS and OWASP Developer Guide requirements [internal]') in the table below.
