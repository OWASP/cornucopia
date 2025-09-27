## Scenario: Oana’s Sanitization Bypass

Picture a scenario where Oana, a skilled manipulator, finds a way to bypass the security of a system due to incomplete application of centralized sanitization routines. This vulnerability arises because:

1. **Incomplete Use of Sanitization:** The system fails to apply sanitization routines comprehensively across all data inputs.

### Example

Oana identifies that while primary user input fields on the website are well-sanitized, secondary inputs such as URL parameters or data inputs in less prominent forms are overlooked. She exploits this gap by injecting malicious code through these unsanitized channels. Since these inputs are not subjected to the usual sanitization process, her code bypasses the security measures, posing a threat to the system’s integrity.

## Threat Modeling

### STRIDE

Bypassing centralized sanitization routines because they are not applied everywhere — is a classic STRIDE: **Tampering** threat.
Sanitization routines are meant to enforce integrity by ensuring data isn’t maliciously altered.
If Oana can push malicious payloads through un-sanitized channels (e.g., overlooked URL parameters, hidden forms), she is modifying input data in a way the system was supposed to prevent.

### What can go Wrong?

This loophole can lead to significant security breaches, including Cross-Site Scripting (XSS) attacks, unauthorized access, and data compromise.

### What are you going to do about it?

- Ensure that sanitization routines are uniformly applied to all forms of data input, including both primary and secondary sources.
- Regularly review and enhance sanitization protocols to cover all potential data entry points, ensuring no part of the system is left vulnerable.

For detailed advice on how to mitigate threats related to the card, see the [ASVS and OWASP Developer Guide requirements ](#mapping 'ASVS and OWASP Developer Guide requirements [internal]') in the table below.
