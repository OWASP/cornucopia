# Encoding and Sanitization Architecture

## V1.1.1

Verify that input is decoded or unescaped into a canonical form only once, it is only decoded when encoded data in that form is expected, and that this is done before processing the input further, for example it is not performed after input validation or sanitization.

Required for Level 2 and 3

### Related CAPEC™ Requirements

CAPEC™ (3.9): [120](/taxonomy/capec-3.9/120), [126](/taxonomy/capec-3.9/126), [152](/taxonomy/capec-3.9/152), [153](/taxonomy/capec-3.9/153), [160](/taxonomy/capec-3.9/160), [242](/taxonomy/capec-3.9/242), [267](/taxonomy/capec-3.9/267), [28](/taxonomy/capec-3.9/28), [3](/taxonomy/capec-3.9/3), [43](/taxonomy/capec-3.9/43), [64](/taxonomy/capec-3.9/64), [71](/taxonomy/capec-3.9/71), [72](/taxonomy/capec-3.9/72), [78](/taxonomy/capec-3.9/78), [79](/taxonomy/capec-3.9/79), [80](/taxonomy/capec-3.9/80), [88](/taxonomy/capec-3.9/88)

## V1.1.2

Verify that the application performs output encoding and escaping either as a final step before being used by the interpreter for which it is intended or by the interpreter itself.

Required for Level 2 and 3

### Related CAPEC™ Requirements

CAPEC™ (3.9): [120](/taxonomy/capec-3.9/120), [152](/taxonomy/capec-3.9/152), [153](/taxonomy/capec-3.9/153), [242](/taxonomy/capec-3.9/242), [267](/taxonomy/capec-3.9/267), [28](/taxonomy/capec-3.9/28), [43](/taxonomy/capec-3.9/43), [64](/taxonomy/capec-3.9/64), [71](/taxonomy/capec-3.9/71), [72](/taxonomy/capec-3.9/72), [78](/taxonomy/capec-3.9/78), [79](/taxonomy/capec-3.9/79), [80](/taxonomy/capec-3.9/80), [88](/taxonomy/capec-3.9/88)

## Disclaimer

Credit via [OWASP ASVS](https://owasp.org/www-project-application-security-verification-standard/).For more information visit: [The OWASP ASVS Project](https://owasp.org/www-project-application-security-verification-standard/) or [Github respository.](https://github.com/OWASP/ASVS). OWASP ASVS is under the [Creative Commons Attribution-Share Alike v4.0](https://github.com/OWASP/ASVS/blob/v5.0.0/LICENSE.md) license.
