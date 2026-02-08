# Authorization Documentation

## V8.1.1

Verify that authorization documentation defines rules for restricting function-level and data-specific access based on consumer permissions and resource attributes.

Required for Level 1, 2 and 3

### Related CAPEC™ Requirements

CAPEC™ (3.9): [1](/taxonomy/capec-3.9/1/index.md), [116](/taxonomy/capec-3.9/116/index.md), [122](/taxonomy/capec-3.9/122/index.md), [126](/taxonomy/capec-3.9/126/index.md), [133](/taxonomy/capec-3.9/133/index.md), [143](/taxonomy/capec-3.9/143/index.md), [144](/taxonomy/capec-3.9/144/index.md), [149](/taxonomy/capec-3.9/149/index.md), [155](/taxonomy/capec-3.9/155/index.md), [176](/taxonomy/capec-3.9/176/index.md), [179](/taxonomy/capec-3.9/179/index.md), [180](/taxonomy/capec-3.9/180/index.md), [203](/taxonomy/capec-3.9/203/index.md), [207](/taxonomy/capec-3.9/207/index.md), [212](/taxonomy/capec-3.9/212/index.md), [240](/taxonomy/capec-3.9/240/index.md), [54](/taxonomy/capec-3.9/54/index.md), [554](/taxonomy/capec-3.9/554/index.md), [58](/taxonomy/capec-3.9/58/index.md), [75](/taxonomy/capec-3.9/75/index.md), [87](/taxonomy/capec-3.9/87/index.md)

## V8.1.2

Verify that authorization documentation defines rules for field-level access restrictions (both read and write) based on consumer permissions and resource attributes. Note that these rules might depend on other attribute values of the relevant data object, such as state or status.

Required for Level 2 and 3

### Related CAPEC™ Requirements

CAPEC™ (3.9): [122](/taxonomy/capec-3.9/122/index.md), [207](/taxonomy/capec-3.9/207/index.md), [212](/taxonomy/capec-3.9/212/index.md), [554](/taxonomy/capec-3.9/554/index.md), [58](/taxonomy/capec-3.9/58/index.md)

## V8.1.3

Verify that the application's documentation defines the environmental and contextual attributes (including but not limited to, time of day, user location, IP address, or device) that are used in the application to make security decisions, including those pertaining to authentication and authorization.

Required for Level 3

### Related CAPEC™ Requirements

CAPEC™ (3.9): [114](/taxonomy/capec-3.9/114/index.md), [151](/taxonomy/capec-3.9/151/index.md), [156](/taxonomy/capec-3.9/156/index.md), [176](/taxonomy/capec-3.9/176/index.md), [195](/taxonomy/capec-3.9/195/index.md), [465](/taxonomy/capec-3.9/465/index.md), [510](/taxonomy/capec-3.9/510/index.md), [543](/taxonomy/capec-3.9/543/index.md), [554](/taxonomy/capec-3.9/554/index.md), [593](/taxonomy/capec-3.9/593/index.md), [633](/taxonomy/capec-3.9/633/index.md), [98](/taxonomy/capec-3.9/98/index.md)

## V8.1.4

Verify that authentication and authorization documentation defines how environmental and contextual factors are used in decision-making, in addition to function-level, data-specific, and field-level authorization. This should include the attributes evaluated, thresholds for risk, and actions taken (e.g., allow, challenge, deny, step-up authentication).

Required for Level 3

### Related CAPEC™ Requirements

CAPEC™ (3.9): [1](/taxonomy/capec-3.9/1/index.md), [114](/taxonomy/capec-3.9/114/index.md), [116](/taxonomy/capec-3.9/116/index.md), [133](/taxonomy/capec-3.9/133/index.md), [151](/taxonomy/capec-3.9/151/index.md), [156](/taxonomy/capec-3.9/156/index.md), [176](/taxonomy/capec-3.9/176/index.md), [179](/taxonomy/capec-3.9/179/index.md), [180](/taxonomy/capec-3.9/180/index.md), [195](/taxonomy/capec-3.9/195/index.md), [207](/taxonomy/capec-3.9/207/index.md), [465](/taxonomy/capec-3.9/465/index.md), [510](/taxonomy/capec-3.9/510/index.md), [543](/taxonomy/capec-3.9/543/index.md), [554](/taxonomy/capec-3.9/554/index.md), [593](/taxonomy/capec-3.9/593/index.md), [633](/taxonomy/capec-3.9/633/index.md), [75](/taxonomy/capec-3.9/75/index.md), [98](/taxonomy/capec-3.9/98/index.md)

## Disclaimer

Credit via [OWASP ASVS](https://owasp.org/www-project-application-security-verification-standard/).For more information visit: [The OWASP ASVS Project](https://owasp.org/www-project-application-security-verification-standard/) or [Github respository.](https://github.com/OWASP/ASVS). OWASP ASVS is under the [Creative Commons Attribution-Share Alike v4.0](https://github.com/OWASP/ASVS/blob/v5.0.0/LICENSE.md) license.
