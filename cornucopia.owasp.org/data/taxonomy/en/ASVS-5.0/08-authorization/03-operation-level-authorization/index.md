# Operation Level Authorization

## V8.3.1

Verify that the application enforces authorization rules at a trusted service layer and doesn't rely on controls that an untrusted consumer could manipulate, such as client-side JavaScript.

Required for Level 1, 2 and 3

### Related CAPEC™ Requirements

CAPEC™ (3.9): [1](/taxonomy/capec-3.9/1/index.md), [121](/taxonomy/capec-3.9/121/index.md), [156](/taxonomy/capec-3.9/156/index.md), [162](/taxonomy/capec-3.9/162/index.md), [166](/taxonomy/capec-3.9/166/index.md), [172](/taxonomy/capec-3.9/172/index.md), [176](/taxonomy/capec-3.9/176/index.md), [179](/taxonomy/capec-3.9/179/index.md), [180](/taxonomy/capec-3.9/180/index.md), [207](/taxonomy/capec-3.9/207/index.md), [212](/taxonomy/capec-3.9/212/index.md), [22](/taxonomy/capec-3.9/22/index.md), [36](/taxonomy/capec-3.9/36/index.md), [39](/taxonomy/capec-3.9/39/index.md), [554](/taxonomy/capec-3.9/554/index.md), [74](/taxonomy/capec-3.9/74/index.md), [95](/taxonomy/capec-3.9/95/index.md)

## V8.3.2

Verify that changes to values on which authorization decisions are made are applied immediately. Where changes cannot be applied immediately, (such as when relying on data in self-contained tokens), there must be mitigating controls to alert when a consumer performs an action when they are no longer authorized to do so and revert the change. Note that this alternative would not mitigate information leakage.

Required for Level 3

### Related CAPEC™ Requirements

CAPEC™ (3.9): [156](/taxonomy/capec-3.9/156/index.md), [176](/taxonomy/capec-3.9/176/index.md), [554](/taxonomy/capec-3.9/554/index.md), [593](/taxonomy/capec-3.9/593/index.md)

## V8.3.3

Verify that access to an object is based on the originating subject's (e.g. consumer's) permissions, not on the permissions of any intermediary or service acting on their behalf. For example, if a consumer calls a web service using a self-contained token for authentication, and the service then requests data from a different service, the second service will use the consumer's token, rather than a machine-to-machine token from the first service, to make permission decisions.

Required for Level 3

### Related CAPEC™ Requirements

CAPEC™ (3.9): [156](/taxonomy/capec-3.9/156/index.md), [176](/taxonomy/capec-3.9/176/index.md), [233](/taxonomy/capec-3.9/233/index.md), [234](/taxonomy/capec-3.9/234/index.md), [240](/taxonomy/capec-3.9/240/index.md), [30](/taxonomy/capec-3.9/30/index.md), [554](/taxonomy/capec-3.9/554/index.md), [69](/taxonomy/capec-3.9/69/index.md)

## Disclaimer

Credit via [OWASP ASVS](https://owasp.org/www-project-application-security-verification-standard/).For more information visit: [The OWASP ASVS Project](https://owasp.org/www-project-application-security-verification-standard/) or [Github respository.](https://github.com/OWASP/ASVS). OWASP ASVS is under the [Creative Commons Attribution-Share Alike v4.0](https://github.com/OWASP/ASVS/blob/v5.0.0/LICENSE.md) license.
