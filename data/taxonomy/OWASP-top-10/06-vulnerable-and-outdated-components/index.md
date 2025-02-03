# Vulnerable and Outdated Components
## Description
You are likely vulnerable:

- If you do not know the versions of all components you use (both client-side and server-side). This includes components you directly use as well as nested dependencies.
- If the software is vulnerable, unsupported, or out of date. This includes the OS, web/application server, database management system (DBMS), applications, APIs and all components, runtime environments, and libraries.
- If you do not scan for vulnerabilities regularly and subscribe to security bulletins related to the components you use.
- If you do not fix or upgrade the underlying platform, frameworks, and dependencies in a risk-based, timely fashion. This commonly happens in environments when patching is a monthly or quarterly task under change control, leaving organizations open to days or months of unnecessary exposure to fixed vulnerabilities.
- If software developers do not test the compatibility of updated, upgraded, or patched libraries.
- If you do not secure the components’ configurations (see A05:2021-Security Misconfiguration).

## How to Prevent
There should be a patch management process in place to:

- Remove unused dependencies, unnecessary features, components, files, and documentation.
- Continuously inventory the versions of both client-side and server-side components (e.g., frameworks, libraries) and their dependencies using tools like versions, OWASP Dependency Check, retire.js, etc. Continuously monitor sources like Common Vulnerability and Exposures (CVE) and National Vulnerability Database (NVD) for vulnerabilities in the components. Use software composition analysis tools to automate the process. Subscribe to email alerts for security vulnerabilities related to components you use.
- Only obtain components from official sources over secure links. Prefer signed packages to reduce the chance of including a modified, malicious component (See A08:2021-Software and Data Integrity Failures).
- Monitor for libraries and components that are unmaintained or do not create security patches for older versions. If patching is not possible, consider deploying a virtual patch to monitor, detect, or protect against the discovered issue.

Every organization must ensure an ongoing plan for monitoring, triaging, and applying updates or configuration changes for the lifetime of the application or portfolio.

[Source: OWASP TOP 10 Vulnerable and Outdated Components](https://owasp.org/Top10/A06_2021-Vulnerable_and_Outdated_Components/)

## Cheatsheets
[Vulnerable and Outdated Components Cheatcheats](https://cheatsheetseries.owasp.org/IndexTopTen.html#a062021-vulnerable-and-outdated-components)

## Cards
### Data-validation-&-encoding
- [Data-validation-&-encoding 2](/data-validation-&-encoding/2)

### Authentication
- [Authentication 9](/authentication/9)

### Authorization
- [Authorization 8](/authorization/8)
- [Authorization 9](/authorization/9)

### Cryptography
- [Cryptography 7](/cryptography/7)
- [Cryptography 9](/cryptography/9)

### Cornucopia
- [Cornucopia 6](/cornucopia/6)
- [Cornucopia 8](/cornucopia/8)
- [Cornucopia 10](/cornucopia/10)
- [Cornucopia J](/cornucopia/J)
