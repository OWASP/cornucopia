# Input Validation

## V2.2.1

Verify that input is validated to enforce business or functional expectations for that input. This should either use positive validation against an allow list of values, patterns, and ranges, or be based on comparing the input to an expected structure and logical limits according to predefined rules. For L1, this can focus on input which is used to make specific business or security decisions. For L2 and up, this should apply to all input.

Required for Level 1, 2 and 3

### Related CAPEC™ Requirements

CAPEC™ (3.9): [113](/taxonomy/capec-3.9/113/index.md), [120](/taxonomy/capec-3.9/120/index.md), [126](/taxonomy/capec-3.9/126/index.md), [130](/taxonomy/capec-3.9/130/index.md), [137](/taxonomy/capec-3.9/137/index.md), [140](/taxonomy/capec-3.9/140/index.md), [145](/taxonomy/capec-3.9/145/index.md), [152](/taxonomy/capec-3.9/152/index.md), [153](/taxonomy/capec-3.9/153/index.md), [160](/taxonomy/capec-3.9/160/index.md), [165](/taxonomy/capec-3.9/165/index.md), [19](/taxonomy/capec-3.9/19/index.md), [212](/taxonomy/capec-3.9/212/index.md), [218](/taxonomy/capec-3.9/218/index.md), [267](/taxonomy/capec-3.9/267/index.md), [272](/taxonomy/capec-3.9/272/index.md), [28](/taxonomy/capec-3.9/28/index.md), [3](/taxonomy/capec-3.9/3/index.md), [4](/taxonomy/capec-3.9/4/index.md), [43](/taxonomy/capec-3.9/43/index.md), [475](/taxonomy/capec-3.9/475/index.md), [48](/taxonomy/capec-3.9/48/index.md), [52](/taxonomy/capec-3.9/52/index.md), [586](/taxonomy/capec-3.9/586/index.md), [64](/taxonomy/capec-3.9/64/index.md), [71](/taxonomy/capec-3.9/71/index.md), [72](/taxonomy/capec-3.9/72/index.md), [77](/taxonomy/capec-3.9/77/index.md), [78](/taxonomy/capec-3.9/78/index.md), [79](/taxonomy/capec-3.9/79/index.md), [80](/taxonomy/capec-3.9/80/index.md)

## V2.2.2

Verify that the application is designed to enforce input validation at a trusted service layer. While client-side validation improves usability and should be encouraged, it must not be relied upon as a security control.

Required for Level 1, 2 and 3

### Related CAPEC™ Requirements

CAPEC™ (3.9): [113](/taxonomy/capec-3.9/113/index.md), [126](/taxonomy/capec-3.9/126/index.md), [130](/taxonomy/capec-3.9/130/index.md), [137](/taxonomy/capec-3.9/137/index.md), [140](/taxonomy/capec-3.9/140/index.md), [145](/taxonomy/capec-3.9/145/index.md), [152](/taxonomy/capec-3.9/152/index.md), [153](/taxonomy/capec-3.9/153/index.md), [162](/taxonomy/capec-3.9/162/index.md), [165](/taxonomy/capec-3.9/165/index.md), [19](/taxonomy/capec-3.9/19/index.md), [201](/taxonomy/capec-3.9/201/index.md), [202](/taxonomy/capec-3.9/202/index.md), [207](/taxonomy/capec-3.9/207/index.md), [212](/taxonomy/capec-3.9/212/index.md), [218](/taxonomy/capec-3.9/218/index.md), [22](/taxonomy/capec-3.9/22/index.md), [271](/taxonomy/capec-3.9/271/index.md), [272](/taxonomy/capec-3.9/272/index.md), [28](/taxonomy/capec-3.9/28/index.md), [43](/taxonomy/capec-3.9/43/index.md), [475](/taxonomy/capec-3.9/475/index.md), [48](/taxonomy/capec-3.9/48/index.md), [554](/taxonomy/capec-3.9/554/index.md), [586](/taxonomy/capec-3.9/586/index.md), [77](/taxonomy/capec-3.9/77/index.md), [87](/taxonomy/capec-3.9/87/index.md)

## V2.2.3

Verify that the application ensures that combinations of related data items are reasonable according to the pre-defined rules.

Required for Level 2 and 3

### Related CAPEC™ Requirements

CAPEC™ (3.9): [113](/taxonomy/capec-3.9/113/index.md), [137](/taxonomy/capec-3.9/137/index.md), [140](/taxonomy/capec-3.9/140/index.md), [152](/taxonomy/capec-3.9/152/index.md), [153](/taxonomy/capec-3.9/153/index.md), [19](/taxonomy/capec-3.9/19/index.md), [28](/taxonomy/capec-3.9/28/index.md)

## Disclaimer

Credit via [OWASP ASVS](https://owasp.org/www-project-application-security-verification-standard/).For more information visit: [The OWASP ASVS Project](https://owasp.org/www-project-application-security-verification-standard/) or [Github respository.](https://github.com/OWASP/ASVS). OWASP ASVS is under the [Creative Commons Attribution-Share Alike v4.0](https://github.com/OWASP/ASVS/blob/v5.0.0/LICENSE.md) license.
