# Authentication Factor Lifecycle and Recovery

## V6.4.1

Verify that system generated initial passwords or activation codes are securely randomly generated, follow the existing password policy, and expire after a short period of time or after they are initially used. These initial secrets must not be permitted to become the long term password.

Required for Level 1, 2 and 3

### Related CAPEC™ Requirements

CAPEC™ (3.9): [151](/taxonomy/capec-3.9/151/index.md), [49](/taxonomy/capec-3.9/49/index.md), [633](/taxonomy/capec-3.9/633/index.md)

## V6.4.2

Verify that password hints or knowledge-based authentication (so-called "secret questions") are not present.

Required for Level 1, 2 and 3

### Related CAPEC™ Requirements

CAPEC™ (3.9): [114](/taxonomy/capec-3.9/114/index.md), [115](/taxonomy/capec-3.9/115/index.md), [151](/taxonomy/capec-3.9/151/index.md), [16](/taxonomy/capec-3.9/16/index.md), [49](/taxonomy/capec-3.9/49/index.md), [560](/taxonomy/capec-3.9/560/index.md), [70](/taxonomy/capec-3.9/70/index.md)

## V6.4.3

Verify that a secure process for resetting a forgotten password is implemented, that does not bypass any enabled multi-factor authentication mechanisms.

Required for Level 2 and 3

### Related CAPEC™ Requirements

CAPEC™ (3.9): [114](/taxonomy/capec-3.9/114/index.md), [115](/taxonomy/capec-3.9/115/index.md), [151](/taxonomy/capec-3.9/151/index.md), [49](/taxonomy/capec-3.9/49/index.md), [50](/taxonomy/capec-3.9/50/index.md)

## V6.4.4

Verify that if a multi-factor authentication factor is lost, evidence of identity proofing is performed at the same level as during enrollment.

Required for Level 2 and 3

### Related CAPEC™ Requirements

CAPEC™ (3.9): [114](/taxonomy/capec-3.9/114/index.md), [115](/taxonomy/capec-3.9/115/index.md), [151](/taxonomy/capec-3.9/151/index.md), [50](/taxonomy/capec-3.9/50/index.md)

## V6.4.5

Verify that renewal instructions for authentication mechanisms which expire are sent with enough time to be carried out before the old authentication mechanism expires, configuring automated reminders if necessary.

Required for Level 3

### Related CAPEC™ Requirements

CAPEC™ (3.9): [518](/taxonomy/capec-3.9/518/index.md), [519](/taxonomy/capec-3.9/519/index.md), [603](/taxonomy/capec-3.9/603/index.md), [607](/taxonomy/capec-3.9/607/index.md)

## V6.4.6

Verify that administrative users can initiate the password reset process for the user, but that this does not allow them to change or choose the user's password. This prevents a situation where they know the user's password.

Required for Level 3

### Related CAPEC™ Requirements

CAPEC™ (3.9): [416](/taxonomy/capec-3.9/416/index.md), [50](/taxonomy/capec-3.9/50/index.md), [518](/taxonomy/capec-3.9/518/index.md), [519](/taxonomy/capec-3.9/519/index.md), [548](/taxonomy/capec-3.9/548/index.md), [603](/taxonomy/capec-3.9/603/index.md), [607](/taxonomy/capec-3.9/607/index.md)

## Disclaimer

Credit via [OWASP ASVS](https://owasp.org/www-project-application-security-verification-standard/).For more information visit: [The OWASP ASVS Project](https://owasp.org/www-project-application-security-verification-standard/) or [Github respository.](https://github.com/OWASP/ASVS). OWASP ASVS is under the [Creative Commons Attribution-Share Alike v4.0](https://github.com/OWASP/ASVS/blob/v5.0.0/LICENSE.md) license.
