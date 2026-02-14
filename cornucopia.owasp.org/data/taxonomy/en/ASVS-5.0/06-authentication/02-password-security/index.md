# Password Security

## V6.2.1

Verify that user set passwords are at least 8 characters in length although a minimum of 15 characters is strongly recommended.

Required for Level 1, 2 and 3

### Related CAPEC™ Requirements

CAPEC™ (3.9): [49](/taxonomy/capec-3.9/49)

## V6.2.2

Verify that users can change their password.

Required for Level 1, 2 and 3

### Related CAPEC™ Requirements

CAPEC™ (3.9): [116](/taxonomy/capec-3.9/116), [70](/taxonomy/capec-3.9/70)

## V6.2.3

Verify that password change functionality requires the user's current and new password.

Required for Level 1, 2 and 3

### Related CAPEC™ Requirements

CAPEC™ (3.9): [114](/taxonomy/capec-3.9/114), [50](/taxonomy/capec-3.9/50)

## V6.2.4

Verify that passwords submitted during account registration or password change are checked against an available set of, at least, the top 3000 passwords which match the application's password policy, e.g. minimum length.

Required for Level 1, 2 and 3

### Related CAPEC™ Requirements

CAPEC™ (3.9): [151](/taxonomy/capec-3.9/151), [16](/taxonomy/capec-3.9/16), [49](/taxonomy/capec-3.9/49), [50](/taxonomy/capec-3.9/50), [560](/taxonomy/capec-3.9/560), [70](/taxonomy/capec-3.9/70)

## V6.2.5

Verify that passwords of any composition can be used, without rules limiting the type of characters permitted. There must be no requirement for a minimum number of upper or lower case characters, numbers, or special characters.

Required for Level 1, 2 and 3

### Related CAPEC™ Requirements

CAPEC™ (3.9): [49](/taxonomy/capec-3.9/49)

## V6.2.6

Verify that password input fields use type=password to mask the entry. Applications may allow the user to temporarily view the entire masked password, or the last typed character of the password.

Required for Level 1, 2 and 3

### Related CAPEC™ Requirements

CAPEC™ (3.9): [508](/taxonomy/capec-3.9/508)

## V6.2.7

Verify that "paste" functionality, browser password helpers, and external password managers are permitted.

Required for Level 1, 2 and 3

### Related CAPEC™ Requirements

CAPEC™ (3.9): [508](/taxonomy/capec-3.9/508)

## V6.2.8

Verify that the application verifies the user's password exactly as received from the user, without any modifications such as truncation or case transformation.

Required for Level 1, 2 and 3

### Related CAPEC™ Requirements

CAPEC™ (3.9): [49](/taxonomy/capec-3.9/49)

## V6.2.9

Verify that passwords of at least 64 characters are permitted.

Required for Level 2 and 3

### Related CAPEC™ Requirements

CAPEC™ (3.9): [49](/taxonomy/capec-3.9/49)

## V6.2.10

Verify that a user's password stays valid until it is discovered to be compromised or the user rotates it. The application must not require periodic credential rotation.

Required for Level 2 and 3

### Related CAPEC™ Requirements

CAPEC™ (3.9): [151](/taxonomy/capec-3.9/151), [49](/taxonomy/capec-3.9/49), [560](/taxonomy/capec-3.9/560)

## V6.2.11

Verify that the documented list of context specific words is used to prevent easy to guess passwords being created.

Required for Level 2 and 3

### Related CAPEC™ Requirements

CAPEC™ (3.9): [151](/taxonomy/capec-3.9/151), [16](/taxonomy/capec-3.9/16), [49](/taxonomy/capec-3.9/49), [560](/taxonomy/capec-3.9/560), [70](/taxonomy/capec-3.9/70)

## V6.2.12

Verify that passwords submitted during account registration or password changes are checked against a set of breached passwords.

Required for Level 2 and 3

### Related CAPEC™ Requirements

CAPEC™ (3.9): [151](/taxonomy/capec-3.9/151), [16](/taxonomy/capec-3.9/16), [49](/taxonomy/capec-3.9/49), [560](/taxonomy/capec-3.9/560), [70](/taxonomy/capec-3.9/70)

## Disclaimer

Credit via [OWASP ASVS](https://owasp.org/www-project-application-security-verification-standard/).For more information visit: [The OWASP ASVS Project](https://owasp.org/www-project-application-security-verification-standard/) or [Github respository.](https://github.com/OWASP/ASVS). OWASP ASVS is under the [Creative Commons Attribution-Share Alike v4.0](https://github.com/OWASP/ASVS/blob/v5.0.0/LICENSE.md) license.
