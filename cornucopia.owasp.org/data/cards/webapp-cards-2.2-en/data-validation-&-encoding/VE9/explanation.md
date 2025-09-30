## Scenario: Shamun’s Validation Workaround

Imagine a scenario where Shamun, exploiting a critical oversight, bypasses both input and output validation checks in a system. This is possible because the system does not adequately handle validation failures:

1. **Non-Rejection of Validation Failures:** When input or output data fails validation, the system does not outright reject it.

2. **Lack of Sanitization After Validation Failure:** The system fails to sanitize data that doesn't pass validation checks.

### Example

Shamun discovers that when certain inputs fail validation checks on your website, instead of rejecting them, the system attempts to process them with minimal or no sanitization. He exploits this by submitting data that is purposefully malformed to fail validation, yet crafted in a way that, when processed, triggers unintended behavior or exposes sensitive information.

## Threat Modeling

### STRIDE

Shamun is deliberately submitting malformed or invalid data.
Because the application does not properly reject it, Shamun’s crafted input is accepted and modifies the system’s behavior or state in unintended ways. Hence **Tampering** is the most applicable category.

### What can go wrong?

This vulnerability can lead to various security threats, including data leakage, unauthorized actions within the system, and the execution of malicious code.

For more things that can go wrong, see the [Common Attack Patterns related to this card](#mapping 'Common Attack Patterns related to this card [internal]') in the table below.

### What are you going to do about it?

Extensive checks and validations can be made of inputs and outputs, but proper actions following the results is what provides security. Data sanitization is a good approach for outputs, as this data is already accepted by the system. Failing input validation always needs to result in rejection. It is also useful to log (associated with the user's identity if possible) and flag these as probably malicious activity for further analysis, or as input for application intrusion detection systems.

1. Implement a strict policy to reject any data that fails validation checks. 
2. In cases where rejection is not possible, thoroughly sanitize all data post-validation failure. 
3. Regularly update validation and sanitization procedures to address emerging security threats and ensure comprehensive coverage

For detailed advice on how to mitigate threats related to the card, see the [ASVS and OWASP Developer Guide requirements ](#mapping 'ASVS and OWASP Developer Guide requirements [internal]') in the table below.
