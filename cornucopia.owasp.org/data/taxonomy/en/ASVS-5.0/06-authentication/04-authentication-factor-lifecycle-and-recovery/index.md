#  Authentication Factor Lifecycle and Recovery
## V6.4.1
Verify that system generated initial passwords or activation codes are securely randomly generated, follow the existing password policy, and expire after a short period of time or after they are initially used. These initial secrets must not be permitted to become the long term password.
Required for Level 1, 2 and 3
## V6.4.2
Verify that password hints or knowledge-based authentication (so-called "secret questions") are not present.
Required for Level 1, 2 and 3
## V6.4.3
Verify that a secure process for resetting a forgotten password is implemented, that does not bypass any enabled multi-factor authentication mechanisms.
Required for Level 2 and 3
## V6.4.4
Verify that if a multi-factor authentication factor is lost, evidence of identity proofing is performed at the same level as during enrollment.
Required for Level 2 and 3
## V6.4.5
Verify that renewal instructions for authentication mechanisms which expire are sent with enough time to be carried out before the old authentication mechanism expires, configuring automated reminders if necessary.
Required for Level 3
## V6.4.6
Verify that administrative users can initiate the password reset process for the user, but that this does not allow them to change or choose the user's password. This prevents a situation where they know the user's password.
Required for Level 3

## Disclaimer:
Credit via [OWASP ASVS](https://owasp.org/www-project-application-security-verification-standard/).For more information visit: [The OWASP ASVS Project](https://owasp.org/www-project-application-security-verification-standard/) or [Github respository.](https://github.com/OWASP/ASVS). OWASP ASVS is under the [Creative Commons Attribution-Share Alike v4.0](https://github.com/OWASP/ASVS/blob/v5.0.0/LICENSE.md) license.
