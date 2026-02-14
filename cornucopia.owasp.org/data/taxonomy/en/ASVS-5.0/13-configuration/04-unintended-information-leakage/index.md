# Unintended Information Leakage

## V13.4.1

Verify that the application is deployed either without any source control metadata, including the .git or .svn folders, or in a way that these folders are inaccessible both externally and to the application itself.

Required for Level 1, 2 and 3

### Related CAPEC™ Requirements

CAPEC™ (3.9): [11](/taxonomy/capec-3.9/11), [116](/taxonomy/capec-3.9/116), [121](/taxonomy/capec-3.9/121), [133](/taxonomy/capec-3.9/133), [149](/taxonomy/capec-3.9/149), [150](/taxonomy/capec-3.9/150), [155](/taxonomy/capec-3.9/155), [169](/taxonomy/capec-3.9/169), [176](/taxonomy/capec-3.9/176), [188](/taxonomy/capec-3.9/188), [207](/taxonomy/capec-3.9/207), [310](/taxonomy/capec-3.9/310), [37](/taxonomy/capec-3.9/37), [497](/taxonomy/capec-3.9/497), [54](/taxonomy/capec-3.9/54)

## V13.4.2

Verify that debug modes are disabled for all components in production environments to prevent exposure of debugging features and information leakage.

Required for Level 2 and 3

### Related CAPEC™ Requirements

CAPEC™ (3.9): [116](/taxonomy/capec-3.9/116), [121](/taxonomy/capec-3.9/121), [133](/taxonomy/capec-3.9/133), [150](/taxonomy/capec-3.9/150), [169](/taxonomy/capec-3.9/169), [184](/taxonomy/capec-3.9/184), [188](/taxonomy/capec-3.9/188), [207](/taxonomy/capec-3.9/207), [215](/taxonomy/capec-3.9/215), [224](/taxonomy/capec-3.9/224), [310](/taxonomy/capec-3.9/310), [444](/taxonomy/capec-3.9/444), [523](/taxonomy/capec-3.9/523), [54](/taxonomy/capec-3.9/54), [541](/taxonomy/capec-3.9/541)

## V13.4.3

Verify that web servers do not expose directory listings to clients unless explicitly intended.

Required for Level 2 and 3

### Related CAPEC™ Requirements

CAPEC™ (3.9): [116](/taxonomy/capec-3.9/116), [127](/taxonomy/capec-3.9/127), [149](/taxonomy/capec-3.9/149), [150](/taxonomy/capec-3.9/150), [155](/taxonomy/capec-3.9/155), [169](/taxonomy/capec-3.9/169), [497](/taxonomy/capec-3.9/497), [54](/taxonomy/capec-3.9/54)

## V13.4.4

Verify that using the HTTP TRACE method is not supported in production environments, to avoid potential information leakage.

Required for Level 2 and 3

### Related CAPEC™ Requirements

CAPEC™ (3.9): [116](/taxonomy/capec-3.9/116), [133](/taxonomy/capec-3.9/133), [150](/taxonomy/capec-3.9/150), [169](/taxonomy/capec-3.9/169), [224](/taxonomy/capec-3.9/224), [54](/taxonomy/capec-3.9/54), [541](/taxonomy/capec-3.9/541)

## V13.4.5

Verify that documentation (such as for internal APIs) and monitoring endpoints are not exposed unless explicitly intended.

Required for Level 2 and 3

### Related CAPEC™ Requirements

CAPEC™ (3.9): [116](/taxonomy/capec-3.9/116), [121](/taxonomy/capec-3.9/121), [133](/taxonomy/capec-3.9/133), [150](/taxonomy/capec-3.9/150), [169](/taxonomy/capec-3.9/169), [188](/taxonomy/capec-3.9/188), [224](/taxonomy/capec-3.9/224), [233](/taxonomy/capec-3.9/233), [240](/taxonomy/capec-3.9/240), [36](/taxonomy/capec-3.9/36), [54](/taxonomy/capec-3.9/54), [541](/taxonomy/capec-3.9/541), [69](/taxonomy/capec-3.9/69), [87](/taxonomy/capec-3.9/87)

## V13.4.6

Verify that the application does not expose detailed version information of backend components.

Required for Level 3

### Related CAPEC™ Requirements

CAPEC™ (3.9): [116](/taxonomy/capec-3.9/116), [133](/taxonomy/capec-3.9/133), [150](/taxonomy/capec-3.9/150), [169](/taxonomy/capec-3.9/169), [188](/taxonomy/capec-3.9/188), [215](/taxonomy/capec-3.9/215), [224](/taxonomy/capec-3.9/224), [310](/taxonomy/capec-3.9/310), [54](/taxonomy/capec-3.9/54), [541](/taxonomy/capec-3.9/541)

## V13.4.7

Verify that the web tier is configured to only serve files with specific file extensions to prevent unintentional information, configuration, and source code leakage.

Required for Level 3

### Related CAPEC™ Requirements

CAPEC™ (3.9): [11](/taxonomy/capec-3.9/11), [116](/taxonomy/capec-3.9/116), [133](/taxonomy/capec-3.9/133), [149](/taxonomy/capec-3.9/149), [150](/taxonomy/capec-3.9/150), [155](/taxonomy/capec-3.9/155), [169](/taxonomy/capec-3.9/169), [176](/taxonomy/capec-3.9/176), [188](/taxonomy/capec-3.9/188), [191](/taxonomy/capec-3.9/191), [224](/taxonomy/capec-3.9/224), [310](/taxonomy/capec-3.9/310), [37](/taxonomy/capec-3.9/37), [497](/taxonomy/capec-3.9/497), [54](/taxonomy/capec-3.9/54), [541](/taxonomy/capec-3.9/541)

## Disclaimer

Credit via [OWASP ASVS](https://owasp.org/www-project-application-security-verification-standard/).For more information visit: [The OWASP ASVS Project](https://owasp.org/www-project-application-security-verification-standard/) or [Github respository.](https://github.com/OWASP/ASVS). OWASP ASVS is under the [Creative Commons Attribution-Share Alike v4.0](https://github.com/OWASP/ASVS/blob/v5.0.0/LICENSE.md) license.
