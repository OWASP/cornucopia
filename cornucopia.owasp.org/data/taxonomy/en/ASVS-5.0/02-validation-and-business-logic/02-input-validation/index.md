# Input Validation

## V2.2.1

Verify that input is validated to enforce business or functional expectations for that input. This should either use positive validation against an allow list of values, patterns, and ranges, or be based on comparing the input to an expected structure and logical limits according to predefined rules. For L1, this can focus on input which is used to make specific business or security decisions. For L2 and up, this should apply to all input.

Required for Level 1, 2 and 3

### Related CAPEC™ Requirements

CAPEC™ (3.9): [113](/taxonomy/capec-3.9/113), [120](/taxonomy/capec-3.9/120), [126](/taxonomy/capec-3.9/126), [130](/taxonomy/capec-3.9/130), [137](/taxonomy/capec-3.9/137), [140](/taxonomy/capec-3.9/140), [145](/taxonomy/capec-3.9/145), [152](/taxonomy/capec-3.9/152), [153](/taxonomy/capec-3.9/153), [160](/taxonomy/capec-3.9/160), [165](/taxonomy/capec-3.9/165), [19](/taxonomy/capec-3.9/19), [212](/taxonomy/capec-3.9/212), [218](/taxonomy/capec-3.9/218), [267](/taxonomy/capec-3.9/267), [272](/taxonomy/capec-3.9/272), [28](/taxonomy/capec-3.9/28), [3](/taxonomy/capec-3.9/3), [4](/taxonomy/capec-3.9/4), [43](/taxonomy/capec-3.9/43), [475](/taxonomy/capec-3.9/475), [48](/taxonomy/capec-3.9/48), [52](/taxonomy/capec-3.9/52), [586](/taxonomy/capec-3.9/586), [64](/taxonomy/capec-3.9/64), [71](/taxonomy/capec-3.9/71), [72](/taxonomy/capec-3.9/72), [77](/taxonomy/capec-3.9/77), [78](/taxonomy/capec-3.9/78), [79](/taxonomy/capec-3.9/79), [80](/taxonomy/capec-3.9/80)

## V2.2.2

Verify that the application is designed to enforce input validation at a trusted service layer. While client-side validation improves usability and should be encouraged, it must not be relied upon as a security control.

Required for Level 1, 2 and 3

### Related CAPEC™ Requirements

CAPEC™ (3.9): [113](/taxonomy/capec-3.9/113), [126](/taxonomy/capec-3.9/126), [130](/taxonomy/capec-3.9/130), [137](/taxonomy/capec-3.9/137), [140](/taxonomy/capec-3.9/140), [145](/taxonomy/capec-3.9/145), [152](/taxonomy/capec-3.9/152), [153](/taxonomy/capec-3.9/153), [162](/taxonomy/capec-3.9/162), [165](/taxonomy/capec-3.9/165), [19](/taxonomy/capec-3.9/19), [201](/taxonomy/capec-3.9/201), [202](/taxonomy/capec-3.9/202), [207](/taxonomy/capec-3.9/207), [212](/taxonomy/capec-3.9/212), [218](/taxonomy/capec-3.9/218), [22](/taxonomy/capec-3.9/22), [271](/taxonomy/capec-3.9/271), [272](/taxonomy/capec-3.9/272), [28](/taxonomy/capec-3.9/28), [43](/taxonomy/capec-3.9/43), [475](/taxonomy/capec-3.9/475), [48](/taxonomy/capec-3.9/48), [554](/taxonomy/capec-3.9/554), [586](/taxonomy/capec-3.9/586), [77](/taxonomy/capec-3.9/77), [87](/taxonomy/capec-3.9/87)

## V2.2.3

Verify that the application ensures that combinations of related data items are reasonable according to the pre-defined rules.

Required for Level 2 and 3

### Related CAPEC™ Requirements

CAPEC™ (3.9): [113](/taxonomy/capec-3.9/113), [137](/taxonomy/capec-3.9/137), [140](/taxonomy/capec-3.9/140), [152](/taxonomy/capec-3.9/152), [153](/taxonomy/capec-3.9/153), [19](/taxonomy/capec-3.9/19), [28](/taxonomy/capec-3.9/28)

## Disclaimer

Credit via [OWASP ASVS](https://owasp.org/www-project-application-security-verification-standard/).For more information visit: [The OWASP ASVS Project](https://owasp.org/www-project-application-security-verification-standard/) or [Github respository.](https://github.com/OWASP/ASVS). OWASP ASVS is under the [Creative Commons Attribution-Share Alike v4.0](https://github.com/OWASP/ASVS/blob/v5.0.0/LICENSE.md) license.
