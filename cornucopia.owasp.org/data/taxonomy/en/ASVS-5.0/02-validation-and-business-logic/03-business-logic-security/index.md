# Business Logic Security

## V2.3.1

Verify that the application will only process business logic flows for the same user in the expected sequential step order and without skipping steps.

Required for Level 1, 2 and 3

## V2.3.2

Verify that business logic limits are implemented per the application's documentation to avoid business logic flaws being exploited.

Required for Level 2 and 3

## V2.3.3

Verify that transactions are being used at the business logic level such that either a business logic operation succeeds in its entirety or it is rolled back to the previous correct state.

Required for Level 2 and 3

## V2.3.4

Verify that business logic level locking mechanisms are used to ensure that limited quantity resources (such as theater seats or delivery slots) cannot be double-booked by manipulating the application's logic.

Required for Level 2 and 3

## V2.3.5

Verify that high-value business logic flows require multi-user approval to prevent unauthorized or accidental actions. This could include but is not limited to large monetary transfers, contract approvals, access to classified information, or safety overrides in manufacturing.

Required for Level 3

## Disclaimer

Credit via [OWASP ASVS](https://owasp.org/www-project-application-security-verification-standard/).For more information visit: [The OWASP ASVS Project](https://owasp.org/www-project-application-security-verification-standard/) or [Github respository.](https://github.com/OWASP/ASVS). OWASP ASVS is under the [Creative Commons Attribution-Share Alike v4.0](https://github.com/OWASP/ASVS/blob/v5.0.0/LICENSE.md) license.
