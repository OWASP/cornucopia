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

### What can go wrong?

These gaps in encoding practices can lead to serious security vulnerabilities compromising both the system and its users. Some common attacks of bad implementation (or lack) of output encoding routines are:

1. Cross Site Scripting (XSS)
2. Code injection
3. Fuzzing

For more things that can go wrong, see the [Common Attack Patterns related to this card](#mapping 'Common Attack Patterns related to this card [internal]') in the table below.

### What are we going to do about it?

Centralized output encoding routines are a good programming practice, but developers need to understand how they work, how to use them and any limitations. Such routines can be tested independently of other code and not only provide assurance on the quality of the validation, but it makes refactorization an easy task and it eliminates code duplicates and bad interpretations. Ouput encodings are a must when handling data from un-trusted sources. It should also be a mandatory security check when outputting data to queries for SQL, XML, and LDAP and in every case when hazardous special characters must be allowed as input (such as < > " ' % ( ) & + \ \' \"). If third-party sanitization libraries are used, it is important to test each routine before its implementation.

1. Ensure consistent application of centralized encoding routines across all parts of the system.
2. Use the correct encoding methods appropriate for each specific data context.
3. Regularly review and update encoding practices to cover all potential data handling scenarios.

For detailed advice on how to mitigate threats related to the card, see the [ASVS and OWASP Developer Guide requirements ](#mapping 'ASVS and OWASP Developer Guide requirements [internal]') in the table below.
