# General Authentication Security

## V6.3.1

Verify that controls to prevent attacks such as credential stuffing and password brute force are implemented according to the application's security documentation.

Required for Level 1, 2 and 3

## V6.3.2

Verify that default user accounts (e.g., "root", "admin", or "sa") are not present in the application or are disabled.

Required for Level 1, 2 and 3

## V6.3.3

Verify that either a multi-factor authentication mechanism or a combination of single-factor authentication mechanisms, must be used in order to access the application. For L3, one of the factors must be a hardware-based authentication mechanism which provides compromise and impersonation resistance against phishing attacks while verifying the intent to authenticate by requiring a user-initiated action (such as a button press on a FIDO hardware key or a mobile phone). Relaxing any of the considerations in this requirement requires a fully documented rationale and a comprehensive set of mitigating controls.

Required for Level 2 and 3

## V6.3.4

Verify that, if the application includes multiple authentication pathways, there are no undocumented pathways and that security controls and authentication strength are enforced consistently.

Required for Level 2 and 3

## V6.3.5

Verify that users are notified of suspicious authentication attempts (successful or unsuccessful). This may include authentication attempts from an unusual location or client, partially successful authentication (only one of multiple factors), an authentication attempt after a long period of inactivity or a successful authentication after several unsuccessful attempts.

Required for Level 3

## V6.3.6

Verify that email is not used as either a single-factor or multi-factor authentication mechanism.

Required for Level 3

## V6.3.7

Verify that users are notified after updates to authentication details, such as credential resets or modification of the username or email address.

Required for Level 3

## V6.3.8

Verify that valid users cannot be deduced from failed authentication challenges, such as by basing on error messages, HTTP response codes, or different response times. Registration and forgot password functionality must also have this protection.

Required for Level 3

## Disclaimer

Credit via [OWASP ASVS](https://owasp.org/www-project-application-security-verification-standard/).For more information visit: [The OWASP ASVS Project](https://owasp.org/www-project-application-security-verification-standard/) or [Github respository.](https://github.com/OWASP/ASVS). OWASP ASVS is under the [Creative Commons Attribution-Share Alike v4.0](https://github.com/OWASP/ASVS/blob/v5.0.0/LICENSE.md) license.
