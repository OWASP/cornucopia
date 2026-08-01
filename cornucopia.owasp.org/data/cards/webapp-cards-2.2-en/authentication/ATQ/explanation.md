## Scenario: Johan’s Authentication Bypass Across Various Functions and Channels

Imagine a scenario where Johan bypasses authentication by exploiting inconsistencies in the enforcement of authentication processes. This happens because:

1. **Varying Rigor in Authentication Functions:** Not all authentication-related functions, like registration, password change, recovery, logout, or administration, have the same level of security rigor.

2. **Inconsistent Authentication Across Channels:** Different versions or channels of the system, such as mobile websites, apps, full websites, APIs, or call centers, do not uniformly enforce authentication standards.

### Example

Johan discovers that while the main website of a service enforces strong authentication, its mobile app version has weaker security checks, particularly for password recovery. Exploiting this, Johan uses the mobile app to request a password reset for a user account. The app does not implement additional security measures, like sending a confirmation to the user's registered email or requiring answers to security questions, allowing Johan easy unauthorized access.

## Threat Modeling

### STRIDE

This scenario is clearly STRIDE: **Spoofing**.

**Spoofing** covers impersonating a legitimate user or entity.
Johan exploits inconsistent authentication enforcement across channels/functions to gain unauthorized access.
Even though the main website is secure, weaker checks in the mobile app allow him to bypass identity verification, effectively impersonating a user.

### What can go wrong?

The degree of identity assurance may not be the same for all web application functions. Or the authentication function may be available in a weaker manner in some other mode or channel, thus compromising the web application. Such inconsistencies can lead to unauthorized access and exploitation of authentication weaknesses, posing a significant risk to user data and system integrity.

For more things that can go wrong, see the [Common Attack Patterns related to this card](#mapping 'Common Attack Patterns related to this card [internal]') in the table below.

### What are we going to do about it?

1. Ensure uniform implementation of robust authentication measures across all functionalities and channels, including mobile and web platforms, APIs, and customer service points.
2. Regularly review and update authentication protocols to maintain consistent security standards across all access points.
3. Conduct thorough testing and audits to identify and rectify any disparities in authentication enforcement.

For detailed advice on how to mitigate threats related to the card, see the [ASVS and OWASP Developer Guide requirements ](#mapping 'ASVS and OWASP Developer Guide requirements [internal]') in the table below.
