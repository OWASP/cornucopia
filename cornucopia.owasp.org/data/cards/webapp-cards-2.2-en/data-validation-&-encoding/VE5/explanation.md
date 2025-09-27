## Scenario: Jee’s Encoding Bypass

Picture a scenario where Jee, a clever adversary, bypasses your system's security by exploiting inconsistencies in encoding routines. This happens because:

1. **Inconsistent Use of Encoding Routines:** Centralized encoding routines are not uniformly applied across the system.

2. **Incorrect Encoding Choices:** The system uses wrong or inappropriate encoding methods for certain types of data.

### Example

Jee finds that while your website correctly encodes data for HTML context, it fails to do so for JavaScript contexts. She inputs a string that is harmless in HTML but malicious in JavaScript, like a script tag with a JavaScript command. Since the system only encodes for HTML, it fails to neutralize the threat in the JavaScript context, leading to a Cross-Site Scripting (XSS) vulnerability.

## Threat Modeling

### STRIDE

This scenario is clearly STRIDE: **Information Disclosure** and **Tampering**.
Bypassing or mis-using output encoding lets attacker-controlled data be sent to and executed in another party’s context. This lets the attacker can alter the rendered page or responses (injecting or changing content seen by users) which is **Tampering**, but the most immediate consequence is exposure and theft of sensitive information (session cookies, DOM data, or secrets accessible in-page) — which maps best to **Information Disclosure**.

### What can go Wrong?

These gaps in encoding practices can lead to serious security vulnerabilities, such as XSS attacks, compromising both the system and its users.

### What are you going to do about it?

1. Ensure consistent application of centralized encoding routines across all parts of the system.
2. Use the correct encoding methods appropriate for each specific data context.
3. Regularly review and update encoding practices to cover all potential data handling scenarios.

For detailed advice on how to mitigate threats related to the card, see the [ASVS and OWASP Developer Guide requirements ](#mapping 'ASVS and OWASP Developer Guide requirements [internal]') in the table below.
