# General Data Protection

## V14.2.1

Verify that sensitive data is only sent to the server in the HTTP message body or header fields, and that the URL and query string do not contain sensitive information, such as an API key or session token.

Required for Level 1, 2 and 3

### Related CAPEC™ Requirements

CAPEC™ (3.9): [117](/taxonomy/capec-3.9/117/index.md), [196](/taxonomy/capec-3.9/196/index.md), [31](/taxonomy/capec-3.9/31/index.md), [37](/taxonomy/capec-3.9/37/index.md), [593](/taxonomy/capec-3.9/593/index.md), [61](/taxonomy/capec-3.9/61/index.md), [633](/taxonomy/capec-3.9/633/index.md), [94](/taxonomy/capec-3.9/94/index.md)

## V14.2.2

Verify that the application prevents sensitive data from being cached in server components, such as load balancers and application caches, or ensures that the data is securely purged after use.

Required for Level 2 and 3

### Related CAPEC™ Requirements

CAPEC™ (3.9): [116](/taxonomy/capec-3.9/116/index.md), [204](/taxonomy/capec-3.9/204/index.md), [31](/taxonomy/capec-3.9/31/index.md), [37](/taxonomy/capec-3.9/37/index.md), [593](/taxonomy/capec-3.9/593/index.md)

## V14.2.3

Verify that defined sensitive data is not sent to untrusted parties (e.g., user trackers) to prevent unwanted collection of data outside of the application's control.

Required for Level 2 and 3

### Related CAPEC™ Requirements

CAPEC™ (3.9): [117](/taxonomy/capec-3.9/117/index.md), [94](/taxonomy/capec-3.9/94/index.md)

## V14.2.4

Verify that controls around sensitive data related to encryption, integrity verification, retention, how the data is to be logged, access controls around sensitive data in logs, privacy and privacy-enhancing technologies, are implemented as defined in the documentation for the specific data's protection level.

Required for Level 2 and 3

### Related CAPEC™ Requirements

CAPEC™ (3.9): [1](/taxonomy/capec-3.9/1/index.md), [116](/taxonomy/capec-3.9/116/index.md), [117](/taxonomy/capec-3.9/117/index.md), [133](/taxonomy/capec-3.9/133/index.md), [145](/taxonomy/capec-3.9/145/index.md), [176](/taxonomy/capec-3.9/176/index.md), [179](/taxonomy/capec-3.9/179/index.md), [180](/taxonomy/capec-3.9/180/index.md), [184](/taxonomy/capec-3.9/184/index.md), [207](/taxonomy/capec-3.9/207/index.md), [39](/taxonomy/capec-3.9/39/index.md), [438](/taxonomy/capec-3.9/438/index.md), [442](/taxonomy/capec-3.9/442/index.md), [475](/taxonomy/capec-3.9/475/index.md), [523](/taxonomy/capec-3.9/523/index.md), [548](/taxonomy/capec-3.9/548/index.md), [554](/taxonomy/capec-3.9/554/index.md), [594](/taxonomy/capec-3.9/594/index.md), [68](/taxonomy/capec-3.9/68/index.md), [690](/taxonomy/capec-3.9/690/index.md), [75](/taxonomy/capec-3.9/75/index.md), [94](/taxonomy/capec-3.9/94/index.md)

## V14.2.5

Verify that caching mechanisms are configured to only cache responses which have the expected content type for that resource and do not contain sensitive, dynamic content. The web server should return a 404 or 302 response when a non-existent file is accessed rather than returning a different, valid file. This should prevent Web Cache Deception attacks.

Required for Level 3

### Related CAPEC™ Requirements

CAPEC™ (3.9): [116](/taxonomy/capec-3.9/116/index.md), [204](/taxonomy/capec-3.9/204/index.md), [548](/taxonomy/capec-3.9/548/index.md)

## V14.2.6

Verify that the application only returns the minimum required sensitive data for the application's functionality. For example, only returning some of the digits of a credit card number and not the full number. If the complete data is required, it should be masked in the user interface unless the user specifically views it.

Required for Level 3

### Related CAPEC™ Requirements

CAPEC™ (3.9): [117](/taxonomy/capec-3.9/117/index.md), [508](/taxonomy/capec-3.9/508/index.md), [548](/taxonomy/capec-3.9/548/index.md), [94](/taxonomy/capec-3.9/94/index.md)

## V14.2.7

Verify that sensitive information is subject to data retention classification, ensuring that outdated or unnecessary data is deleted automatically, on a defined schedule, or as the situation requires.

Required for Level 3

### Related CAPEC™ Requirements

CAPEC™ (3.9): [116](/taxonomy/capec-3.9/116/index.md), [117](/taxonomy/capec-3.9/117/index.md), [204](/taxonomy/capec-3.9/204/index.md), [548](/taxonomy/capec-3.9/548/index.md), [94](/taxonomy/capec-3.9/94/index.md)

## V14.2.8

Verify that sensitive information is removed from the metadata of user-submitted files unless storage is consented to by the user.

Required for Level 3

### Related CAPEC™ Requirements

CAPEC™ (3.9): [116](/taxonomy/capec-3.9/116/index.md), [204](/taxonomy/capec-3.9/204/index.md), [548](/taxonomy/capec-3.9/548/index.md)

## Disclaimer

Credit via [OWASP ASVS](https://owasp.org/www-project-application-security-verification-standard/).For more information visit: [The OWASP ASVS Project](https://owasp.org/www-project-application-security-verification-standard/) or [Github respository.](https://github.com/OWASP/ASVS). OWASP ASVS is under the [Creative Commons Attribution-Share Alike v4.0](https://github.com/OWASP/ASVS/blob/v5.0.0/LICENSE.md) license.
