# Local authentication bypass

Local authentication bypass involves bypassing authentication, either because it's not implemented, through instrumentation by using a instrumentation tool like Frida to trick the app into exposing credentials or believing that authentication has happened, or by forcing the app to throw an error that leaves the app unlocked.

## Example

The Norton App Lock prior to version 1.3.0.13 was susceptible to an authentication bypass exploit [(CVE-2017-15534)](https://nvd.nist.gov/vuln/detail/CVE-2017-15534). The exploit allowed a user to kill the app to prevent it from locking the device, thereby allowing the individual to gain device access.

## Links

- [CVE-2017-15534 - The Norton App Lock exploit](https://nvd.nist.gov/vuln/detail/CVE-2017-15534)
- [CAPEC-115: Authentication Bypass](https://capec.mitre.org/data/definitions/115.html)
- [CWE-306: Missing Authentication for Critical Function](https://cwe.mitre.org/data/definitions/306.html)
- [CWE-287: Improper Authentication](https://cwe.mitre.org/data/definitions/287.html)
- [CWE-288: Authentication Bypass Using an Alternate Path or Channel](https://cwe.mitre.org/data/definitions/288.html)
- [MASWE-0018](https://mas.owasp.org/MASWE/MASVS-CRYPTO/MASWE-0018)
- [MASVS: Android Local Authentication](https://mas.owasp.org/MASTG/0x05f-Testing-Local-Authentication )
- [MASVS: IOS Local Authentication](https://mas.owasp.org/MASTG/0x06f-Testing-Local-Authentication/)
- [OWASP Mobile Top 10, M3: Insecure Authentication/Authorization](https://owasp.org/www-project-mobile-top-10/2023-risks/m3-insecure-authentication-authorization.html)
- [OWASP Cheat Sheet Series: Mobile Application Security Cheat Sheet - Authentication & Authorization](https://cheatsheetseries.owasp.org/cheatsheets/Mobile_Application_Security_Cheat_Sheet.html#authentication-authorization)
- [Apple: Local authentication](https://developer.apple.com/documentation/localauthentication)
- [Android: Local authentication](https://developer.android.com/security/fraud-prevention/authentication)

## Cards
#### Authentication & Authorization
- [Authentication & Authorization 2](/cards/AA2)