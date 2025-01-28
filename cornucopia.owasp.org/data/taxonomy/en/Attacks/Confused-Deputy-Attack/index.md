# Confused deputy attack

If a legitimate application requests dangerous permissions and then exposes a feature that uses that dangerous permission to the system, it allows any other application installed on the device to enjoy the permission without the need of requesting it. Let's say that a developer accidently left the permission `android.permission.BIND_NOTIFICATION_LISTENER_SERVICE` in an application release build and exposed that permission to other apps on the system. It is used to intercept all the notifications received by the system. This means the malware can read all notifications, modify them before sending to the user or even reply to them if needed even if it does not have the `BIND_NOTIFICATION_LISTENER_SERVICE` permission. This is known as the confused deputy problem.

In this example, the application is the deputy because it is acting at the request of the user. The application is seen as 'confused' because it was tricked into making a request on behalf of a malicious application.

## Example

In 2019 the Google and Samsung Camera app was identified as vulnerable to the "Confused deputy attack". The applications exposed an unprotected feature that allowed another application to take pictures or videos through the Camera application.

## Links

- [How Attackers Could Hijack Your Android Camera to Spy on You](https://checkmarx.com/blog/how-attackers-could-hijack-your-android-camera/)
- [CWE-441: Unintended Proxy or Intermediary ('Confused Deputy')](https://cwe.mitre.org/data/definitions/441.html)
- [MASWE-0062](https://mas.owasp.org/MASWE/MASVS-PLATFORM/MASWE-0062/)
- [MASWE-0063](https://mas.owasp.org/MASWE/MASVS-PLATFORM/MASWE-0063/)
- [MASWE-0064](https://mas.owasp.org/MASWE/MASVS-PLATFORM/MASWE-0064/)
- [Wikipedia: Confused deputy problem](https://en.wikipedia.org/wiki/Confused_deputy_problem)
- [OWASP Mobile Top 10, M1: Improper Platform Usage](https://owasp.org/www-project-mobile-top-10/2016-risks/m1-improper-platform-usage)
- [OWASP Mobile Top 10, M3: Insecure Authentication/Authorization](https://owasp.org/www-project-mobile-top-10/2023-risks/m3-insecure-authentication-authorization.html)
- [OWASP Cheat Sheet Series: Mobile Application Security Cheat Sheet: Authentication & Authorization](https://cheatsheetseries.owasp.org/cheatsheets/Mobile_Application_Security_Cheat_Sheet.html#authentication-authorization)
- [Android: Custom Permissions](https://developer.android.com/privacy-and-security/risks/custom-permissions)
- [Apple: Diagnosing Issues with Entitlements](https://developer.apple.com/documentation/bundleresources/entitlements/diagnosing_issues_with_entitlements)
- [Apple: Security of runtime process in iOS and iPadOS](https://help.apple.com/pdf/security/en_US/apple-platform-security-guide.pdf)

## Cards
#### Authentication & Authorization
- [Authentication & Authorization 3](/cards/AA3)