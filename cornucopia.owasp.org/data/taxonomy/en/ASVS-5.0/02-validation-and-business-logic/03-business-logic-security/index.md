# Business Logic Security

## V2.3.1

Verify that the application will only process business logic flows for the same user in the expected sequential step order and without skipping steps.

Required for Level 1, 2 and 3

### Related CAPEC™ Requirements

CAPEC™ (3.9): [113](/taxonomy/capec-3.9/113/index.md), [140](/taxonomy/capec-3.9/140/index.md), [162](/taxonomy/capec-3.9/162/index.md), [166](/taxonomy/capec-3.9/166/index.md), [172](/taxonomy/capec-3.9/172/index.md), [212](/taxonomy/capec-3.9/212/index.md), [28](/taxonomy/capec-3.9/28/index.md), [39](/taxonomy/capec-3.9/39/index.md), [74](/taxonomy/capec-3.9/74/index.md)

## V2.3.2

Verify that business logic limits are implemented per the application's documentation to avoid business logic flaws being exploited.

Required for Level 2 and 3

### Related CAPEC™ Requirements

CAPEC™ (3.9): [113](/taxonomy/capec-3.9/113/index.md), [125](/taxonomy/capec-3.9/125/index.md), [130](/taxonomy/capec-3.9/130/index.md), [140](/taxonomy/capec-3.9/140/index.md), [152](/taxonomy/capec-3.9/152/index.md), [153](/taxonomy/capec-3.9/153/index.md), [172](/taxonomy/capec-3.9/172/index.md), [2](/taxonomy/capec-3.9/2/index.md), [212](/taxonomy/capec-3.9/212/index.md), [227](/taxonomy/capec-3.9/227/index.md), [25](/taxonomy/capec-3.9/25/index.md), [28](/taxonomy/capec-3.9/28/index.md), [43](/taxonomy/capec-3.9/43/index.md), [469](/taxonomy/capec-3.9/469/index.md), [77](/taxonomy/capec-3.9/77/index.md)

## V2.3.3

Verify that transactions are being used at the business logic level such that either a business logic operation succeeds in its entirety or it is rolled back to the previous correct state.

Required for Level 2 and 3

### Related CAPEC™ Requirements

CAPEC™ (3.9): [113](/taxonomy/capec-3.9/113/index.md), [140](/taxonomy/capec-3.9/140/index.md), [152](/taxonomy/capec-3.9/152/index.md), [153](/taxonomy/capec-3.9/153/index.md), [172](/taxonomy/capec-3.9/172/index.md), [212](/taxonomy/capec-3.9/212/index.md), [28](/taxonomy/capec-3.9/28/index.md), [43](/taxonomy/capec-3.9/43/index.md), [77](/taxonomy/capec-3.9/77/index.md)

## V2.3.4

Verify that business logic level locking mechanisms are used to ensure that limited quantity resources (such as theater seats or delivery slots) cannot be double-booked by manipulating the application's logic.

Required for Level 2 and 3

### Related CAPEC™ Requirements

CAPEC™ (3.9): [162](/taxonomy/capec-3.9/162/index.md), [166](/taxonomy/capec-3.9/166/index.md), [172](/taxonomy/capec-3.9/172/index.md), [212](/taxonomy/capec-3.9/212/index.md), [26](/taxonomy/capec-3.9/26/index.md), [39](/taxonomy/capec-3.9/39/index.md), [74](/taxonomy/capec-3.9/74/index.md)

## V2.3.5

Verify that high-value business logic flows require multi-user approval to prevent unauthorized or accidental actions. This could include but is not limited to large monetary transfers, contract approvals, access to classified information, or safety overrides in manufacturing.

Required for Level 3

### Related CAPEC™ Requirements

CAPEC™ (3.9): [162](/taxonomy/capec-3.9/162/index.md), [166](/taxonomy/capec-3.9/166/index.md), [172](/taxonomy/capec-3.9/172/index.md), [212](/taxonomy/capec-3.9/212/index.md), [39](/taxonomy/capec-3.9/39/index.md), [74](/taxonomy/capec-3.9/74/index.md)

## Disclaimer

Credit via [OWASP ASVS](https://owasp.org/www-project-application-security-verification-standard/).For more information visit: [The OWASP ASVS Project](https://owasp.org/www-project-application-security-verification-standard/) or [Github respository.](https://github.com/OWASP/ASVS). OWASP ASVS is under the [Creative Commons Attribution-Share Alike v4.0](https://github.com/OWASP/ASVS/blob/v5.0.0/LICENSE.md) license.
