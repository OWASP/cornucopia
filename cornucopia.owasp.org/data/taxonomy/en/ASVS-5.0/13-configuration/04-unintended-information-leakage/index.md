# Unintended Information Leakage

## V13.4.1

Verify that the application is deployed either without any source control metadata, including the .git or .svn folders, or in a way that these folders are inaccessible both externally and to the application itself.

Required for Level 1, 2 and 3

### Related CAPEC™ Requirements

CAPEC™ (3.9): [11](/taxonomy/capec-3.9/11/index.md), [116](/taxonomy/capec-3.9/116/index.md), [121](/taxonomy/capec-3.9/121/index.md), [133](/taxonomy/capec-3.9/133/index.md), [149](/taxonomy/capec-3.9/149/index.md), [150](/taxonomy/capec-3.9/150/index.md), [155](/taxonomy/capec-3.9/155/index.md), [169](/taxonomy/capec-3.9/169/index.md), [176](/taxonomy/capec-3.9/176/index.md), [188](/taxonomy/capec-3.9/188/index.md), [207](/taxonomy/capec-3.9/207/index.md), [310](/taxonomy/capec-3.9/310/index.md), [37](/taxonomy/capec-3.9/37/index.md), [497](/taxonomy/capec-3.9/497/index.md), [54](/taxonomy/capec-3.9/54/index.md)

## V13.4.2

Verify that debug modes are disabled for all components in production environments to prevent exposure of debugging features and information leakage.

Required for Level 2 and 3

### Related CAPEC™ Requirements

CAPEC™ (3.9): [116](/taxonomy/capec-3.9/116/index.md), [121](/taxonomy/capec-3.9/121/index.md), [133](/taxonomy/capec-3.9/133/index.md), [150](/taxonomy/capec-3.9/150/index.md), [169](/taxonomy/capec-3.9/169/index.md), [184](/taxonomy/capec-3.9/184/index.md), [188](/taxonomy/capec-3.9/188/index.md), [207](/taxonomy/capec-3.9/207/index.md), [215](/taxonomy/capec-3.9/215/index.md), [224](/taxonomy/capec-3.9/224/index.md), [310](/taxonomy/capec-3.9/310/index.md), [444](/taxonomy/capec-3.9/444/index.md), [523](/taxonomy/capec-3.9/523/index.md), [54](/taxonomy/capec-3.9/54/index.md), [541](/taxonomy/capec-3.9/541/index.md)

## V13.4.3

Verify that web servers do not expose directory listings to clients unless explicitly intended.

Required for Level 2 and 3

### Related CAPEC™ Requirements

CAPEC™ (3.9): [116](/taxonomy/capec-3.9/116/index.md), [127](/taxonomy/capec-3.9/127/index.md), [149](/taxonomy/capec-3.9/149/index.md), [150](/taxonomy/capec-3.9/150/index.md), [155](/taxonomy/capec-3.9/155/index.md), [169](/taxonomy/capec-3.9/169/index.md), [497](/taxonomy/capec-3.9/497/index.md), [54](/taxonomy/capec-3.9/54/index.md)

## V13.4.4

Verify that using the HTTP TRACE method is not supported in production environments, to avoid potential information leakage.

Required for Level 2 and 3

### Related CAPEC™ Requirements

CAPEC™ (3.9): [116](/taxonomy/capec-3.9/116/index.md), [133](/taxonomy/capec-3.9/133/index.md), [150](/taxonomy/capec-3.9/150/index.md), [169](/taxonomy/capec-3.9/169/index.md), [224](/taxonomy/capec-3.9/224/index.md), [54](/taxonomy/capec-3.9/54/index.md), [541](/taxonomy/capec-3.9/541/index.md)

## V13.4.5

Verify that documentation (such as for internal APIs) and monitoring endpoints are not exposed unless explicitly intended.

Required for Level 2 and 3

### Related CAPEC™ Requirements

CAPEC™ (3.9): [116](/taxonomy/capec-3.9/116/index.md), [121](/taxonomy/capec-3.9/121/index.md), [133](/taxonomy/capec-3.9/133/index.md), [150](/taxonomy/capec-3.9/150/index.md), [169](/taxonomy/capec-3.9/169/index.md), [188](/taxonomy/capec-3.9/188/index.md), [224](/taxonomy/capec-3.9/224/index.md), [233](/taxonomy/capec-3.9/233/index.md), [240](/taxonomy/capec-3.9/240/index.md), [36](/taxonomy/capec-3.9/36/index.md), [54](/taxonomy/capec-3.9/54/index.md), [541](/taxonomy/capec-3.9/541/index.md), [69](/taxonomy/capec-3.9/69/index.md), [87](/taxonomy/capec-3.9/87/index.md)

## V13.4.6

Verify that the application does not expose detailed version information of backend components.

Required for Level 3

### Related CAPEC™ Requirements

CAPEC™ (3.9): [116](/taxonomy/capec-3.9/116/index.md), [133](/taxonomy/capec-3.9/133/index.md), [150](/taxonomy/capec-3.9/150/index.md), [169](/taxonomy/capec-3.9/169/index.md), [188](/taxonomy/capec-3.9/188/index.md), [215](/taxonomy/capec-3.9/215/index.md), [224](/taxonomy/capec-3.9/224/index.md), [310](/taxonomy/capec-3.9/310/index.md), [54](/taxonomy/capec-3.9/54/index.md), [541](/taxonomy/capec-3.9/541/index.md)

## V13.4.7

Verify that the web tier is configured to only serve files with specific file extensions to prevent unintentional information, configuration, and source code leakage.

Required for Level 3

### Related CAPEC™ Requirements

CAPEC™ (3.9): [11](/taxonomy/capec-3.9/11/index.md), [116](/taxonomy/capec-3.9/116/index.md), [133](/taxonomy/capec-3.9/133/index.md), [149](/taxonomy/capec-3.9/149/index.md), [150](/taxonomy/capec-3.9/150/index.md), [155](/taxonomy/capec-3.9/155/index.md), [169](/taxonomy/capec-3.9/169/index.md), [176](/taxonomy/capec-3.9/176/index.md), [188](/taxonomy/capec-3.9/188/index.md), [191](/taxonomy/capec-3.9/191/index.md), [224](/taxonomy/capec-3.9/224/index.md), [310](/taxonomy/capec-3.9/310/index.md), [37](/taxonomy/capec-3.9/37/index.md), [497](/taxonomy/capec-3.9/497/index.md), [54](/taxonomy/capec-3.9/54/index.md), [541](/taxonomy/capec-3.9/541/index.md)

## Disclaimer

Credit via [OWASP ASVS](https://owasp.org/www-project-application-security-verification-standard/).For more information visit: [The OWASP ASVS Project](https://owasp.org/www-project-application-security-verification-standard/) or [Github respository.](https://github.com/OWASP/ASVS). OWASP ASVS is under the [Creative Commons Attribution-Share Alike v4.0](https://github.com/OWASP/ASVS/blob/v5.0.0/LICENSE.md) license.
