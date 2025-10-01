## Scenario: Jason’s Validation Evasion

Imagine a scenario where Jason, exploiting system weaknesses, bypasses security measures due to inconsistent application of centralized validation routines. He takes advantage of the system's oversight in the following way:

1. **Inconsistent Application of Validation:** The system fails to use centralized validation routines on all input sources.

### Example

Jason discovers that while most input fields on your web application are properly validated, certain API endpoints or secondary input forms lack the same rigorous validation. He targets these overlooked areas, submitting malicious data that would normally be caught and neutralized by the centralized validation routines. This allows him to inject harmful data or commands into the system.

## Threat Modeling

### STRIDE

This scenario falls squarely into the **Tampering** category of STRIDE.
By bypassing centralized validation routines, Jason is able to inject malicious or malformed input (e.g., code injection, buffer overflow payloads) that alters how the system processes the data. The core issue is that unchecked input lets him tamper with the system’s expected data flows and behavior. **Elevation of Privilege** could be a consequence (e.g., RCE via injection), but the root threat is tampering with input.

### What can go wrong?

Such lapses in validation can lead to severe security breaches, including data corruption, unauthorized access, and other forms of system compromise. Common attacks to bad implementation (or lack) of validation routines are:

1. Buffer overflows.
2. Code injection.
3. Fuzzing.

For more things that can go wrong, see the [Common Attack Patterns related to this card](#mapping 'Common Attack Patterns related to this card [internal]') in the table below.

### What are you going to do about it?

Centralized input validation routines are a good programming practice, but like other routines, developers need to understand how they work, how to use them and any limitations. Such routines can be tested independently of other code and not only provide assurance on the quality of the input validation, but it make refactorization an easy task and eliminate code duplicates and bad interpretations. Use of white list validation is recommended where possible. Black lists are usually good as a double-check complement, as they can trigger alerts for fake positives. If third-party input validation libraries are used, it is important to test each routine before its implementation.

1. Ensure that centralized validation routines are uniformly applied to all input sources, including web forms, APIs, and any other data entry points.
2. Regularly audit and update validation protocols to cover all potential avenues of data input.

For detailed advice on how to mitigate threats related to the card, see the [ASVS and OWASP Developer Guide requirements ](#mapping 'ASVS and OWASP Developer Guide requirements [internal]') in the table below.
