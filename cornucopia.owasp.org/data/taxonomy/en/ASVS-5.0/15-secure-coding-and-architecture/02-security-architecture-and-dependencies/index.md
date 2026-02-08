# Security Architecture and Dependencies

## V15.2.1

Verify that the application only contains components which have not breached the documented update and remediation time frames.

Required for Level 1, 2 and 3

### Related CAPEC™ Requirements

CAPEC™ (3.9): [184](/taxonomy/capec-3.9/184/index.md), [242](/taxonomy/capec-3.9/242/index.md), [441](/taxonomy/capec-3.9/441/index.md), [442](/taxonomy/capec-3.9/442/index.md), [444](/taxonomy/capec-3.9/444/index.md), [445](/taxonomy/capec-3.9/445/index.md), [446](/taxonomy/capec-3.9/446/index.md), [523](/taxonomy/capec-3.9/523/index.md), [538](/taxonomy/capec-3.9/538/index.md), [549](/taxonomy/capec-3.9/549/index.md), [673](/taxonomy/capec-3.9/673/index.md), [691](/taxonomy/capec-3.9/691/index.md)

## V15.2.2

Verify that the application has implemented defenses against loss of availability due to functionality which is time-consuming or resource-demanding, based on the documented security decisions and strategies for this.

Required for Level 2 and 3

### Related CAPEC™ Requirements

CAPEC™ (3.9): [125](/taxonomy/capec-3.9/125/index.md), [130](/taxonomy/capec-3.9/130/index.md)

## V15.2.3

Verify that the production environment only includes functionality that is required for the application to function, and does not expose extraneous functionality such as test code, sample snippets, and development functionality.

Required for Level 2 and 3

### Related CAPEC™ Requirements

CAPEC™ (3.9): [116](/taxonomy/capec-3.9/116/index.md), [121](/taxonomy/capec-3.9/121/index.md), [143](/taxonomy/capec-3.9/143/index.md), [144](/taxonomy/capec-3.9/144/index.md), [149](/taxonomy/capec-3.9/149/index.md), [150](/taxonomy/capec-3.9/150/index.md), [155](/taxonomy/capec-3.9/155/index.md), [169](/taxonomy/capec-3.9/169/index.md), [188](/taxonomy/capec-3.9/188/index.md), [207](/taxonomy/capec-3.9/207/index.md), [224](/taxonomy/capec-3.9/224/index.md), [497](/taxonomy/capec-3.9/497/index.md), [54](/taxonomy/capec-3.9/54/index.md), [541](/taxonomy/capec-3.9/541/index.md), [546](/taxonomy/capec-3.9/546/index.md)

## V15.2.4

Verify that third-party components and all of their transitive dependencies are included from the expected repository, whether internally owned or an external source, and that there is no risk of a dependency confusion attack.

Required for Level 3

### Related CAPEC™ Requirements

CAPEC™ (3.9): [115](/taxonomy/capec-3.9/115/index.md), [159](/taxonomy/capec-3.9/159/index.md), [184](/taxonomy/capec-3.9/184/index.md), [242](/taxonomy/capec-3.9/242/index.md), [441](/taxonomy/capec-3.9/441/index.md), [442](/taxonomy/capec-3.9/442/index.md), [443](/taxonomy/capec-3.9/443/index.md), [444](/taxonomy/capec-3.9/444/index.md), [445](/taxonomy/capec-3.9/445/index.md), [446](/taxonomy/capec-3.9/446/index.md), [511](/taxonomy/capec-3.9/511/index.md), [523](/taxonomy/capec-3.9/523/index.md), [538](/taxonomy/capec-3.9/538/index.md), [549](/taxonomy/capec-3.9/549/index.md), [554](/taxonomy/capec-3.9/554/index.md), [673](/taxonomy/capec-3.9/673/index.md), [691](/taxonomy/capec-3.9/691/index.md)

## V15.2.5

Verify that the application implements additional protections around parts of the application which are documented as containing "dangerous functionality" or using third-party libraries considered to be "risky components". This could include techniques such as sandboxing, encapsulation, containerization or network level isolation to delay and deter attackers who compromise one part of an application from pivoting elsewhere in the application.

Required for Level 3

### Related CAPEC™ Requirements

CAPEC™ (3.9): [176](/taxonomy/capec-3.9/176/index.md), [184](/taxonomy/capec-3.9/184/index.md), [233](/taxonomy/capec-3.9/233/index.md), [242](/taxonomy/capec-3.9/242/index.md), [441](/taxonomy/capec-3.9/441/index.md), [442](/taxonomy/capec-3.9/442/index.md), [443](/taxonomy/capec-3.9/443/index.md), [444](/taxonomy/capec-3.9/444/index.md), [445](/taxonomy/capec-3.9/445/index.md), [446](/taxonomy/capec-3.9/446/index.md), [511](/taxonomy/capec-3.9/511/index.md), [523](/taxonomy/capec-3.9/523/index.md), [538](/taxonomy/capec-3.9/538/index.md), [549](/taxonomy/capec-3.9/549/index.md), [554](/taxonomy/capec-3.9/554/index.md), [673](/taxonomy/capec-3.9/673/index.md), [68](/taxonomy/capec-3.9/68/index.md), [691](/taxonomy/capec-3.9/691/index.md)

## Disclaimer

Credit via [OWASP ASVS](https://owasp.org/www-project-application-security-verification-standard/).For more information visit: [The OWASP ASVS Project](https://owasp.org/www-project-application-security-verification-standard/) or [Github respository.](https://github.com/OWASP/ASVS). OWASP ASVS is under the [Creative Commons Attribution-Share Alike v4.0](https://github.com/OWASP/ASVS/blob/v5.0.0/LICENSE.md) license.
