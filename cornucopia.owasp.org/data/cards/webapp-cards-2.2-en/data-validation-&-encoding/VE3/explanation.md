## Scenario: Robert’s Clever Exploits

Imagine a scenario where Robert, an astute attacker, manipulates your system by inputting malicious data. He takes advantage of the system's failure in several critical areas:

1. **Unchecked Protocol Formats:** The system doesn't verify if the data conforms to the expected protocol format.

2. **Acceptance of Duplicates:** The system allows duplicate data entries, which it should normally reject.

3. **Unverified Structure:** There's no check to ensure the overall structure of the data is consistent.

4. **Inadequate Data Element Validation:** The system fails to validate individual data elements for format, type, range, length, or against a whitelist of allowed characters or formats.

### Example

Robert attacks by submitting a form on your website. He intentionally uses an unexpected data format, like entering alphabetic characters where only numbers are expected. The system, not checking the format or range, accepts this input, leading to potential processing errors or more severe security vulnerabilities, such as injection attacks.

## Threat Modeling

### STRIDE

The primary STRIDE category for “being able to input malicious data due to missing protocol/structure/element validation” is **Tampering** with possible secondary impacts into **Information Disclosure**, **DoS**, or **Elevation of Privilege** depending on how the malformed data is exploited.

### What can go wrong?

These oversights can result in significant security breaches, data corruption, and may compromise the integrity and reliability of the entire system.

For more things that can go wrong, see the [Common Attack Patterns related to this card](#mapping 'Common Attack Patterns related to this card [internal]') in the table below.

### What are you going to do about it?

1. Rigorously validate all data inputs for their format, type, range, length, and against a comprehensive whitelist.
2. Regularly update and refine these validation rules to stay ahead of sophisticated attack techniques.

For detailed advice on how to mitigate threats related to the card, see the [ASVS and OWASP Developer Guide requirements ](#mapping 'ASVS and OWASP Developer Guide requirements [internal]') in the table below.
