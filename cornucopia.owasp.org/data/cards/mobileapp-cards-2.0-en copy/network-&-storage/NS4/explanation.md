## Scenario: Kevin can read sensitive data mapped to user accounts or sessions by extracting data exposed through third-party libraries, notifications, backups, caches, local databases, or other embedded services

### Example

Kevin checks a holiday itinerary beside an airport luggage carousel while the app copies his passport number into a map library, notification cache, backup, and analytics plug-in. The map then suggests a scenic detour past the embassy, while the analytics dashboard knows Kevin’s middle name.

Third-party components and embedded services can expose account-linked data outside the intended control. Minimize what is shared and protect every copy, including caches, backups, and local databases.


## Threat Modeling

### STRIDE

This scenario is primarily **Information Disclosure**, **Denial of Service** in STRIDE. The named condition is: Kevin can read sensitive data mapped to user accounts or sessions by extracting data exposed through third-party libraries, notifications, backups, caches, local databases, or other embedded services.

- **MAS-THREAT-0073:** Apps and embedded third-party components can collect or share more data than users were led to expect.
- **MAS-THREAT-0037:** Attackers can access sensitive data shown in notifications.

- **MAS-ATTACK-0081:** Collecting or sharing data categories that are not declared in the platform's privacy labels.
- **MAS-ATTACK-0082:** Transmitting undeclared identifiers or analytics data to first- or third-party services over the network.
- **MAS-ATTACK-0044:** Reading notification content shown on the lock screen without unlocking the device.
- **MAS-ATTACK-0045:** Reading notification content from another app holding notification-access permissions.

### What can go wrong?

If Kevin can read sensitive data mapped to user accounts or sessions by extracting data exposed through third-party libraries, notifications, backups, caches, local databases, or other embedded services, the failure is concrete rather than merely theatrical: the app could let an attacker cross the network-&-storage boundary and reach data or capability that this flow should protect. In this card, the practical route includes Collecting or sharing data categories that are not declared in the platform's privacy labels. Also, Transmitting undeclared identifiers or analytics data to first- or third-party services over the network. That can turn a normal user action into unauthorized access, disclosure, alteration, or service disruption; the mapped weakness entries below identify the exact implementation evidence to check.

Mapped weaknesses that sharpen the review:

- MASWE-0073 — Inadequate Data Collection Declarations: This weakness occurs when an app's stated data collection practices, such as those documented in Apple's App Privacy Report and Privacy Nutrition Labels, or Google's Data Safety section, are incomplete or inconsistent with the app's...
- MASWE-0037 — Unnecessary Exposure of Sensitive Data via Notifications: This weakness occurs when an app includes more sensitive data (such as one-time codes, message contents, or account details) than necessary in a system notification.

### What are we going to do about it?

Inventory every SDK, notification, cache, and backup that receives account data, minimize and declare those transfers in platform privacy labels, redact notification text, and use an intercepting proxy to verify no undeclared identifiers or sensitive values leave the app.


Mapped MASTG tests:

- MASTG-TEST-0206 — Undeclared PII in Network Traffic Capture: Attackers may capture network traffic from Android devices using an intercepting proxy, such as @MASTG-TOOL-0079, @MASTG-TOOL-0077, or @MASTG-TOOL-0097, to analyze the data being transmitted by the app. This works even if the app uses...
- MASTG-TEST-0315 — Sensitive Data Exposed via Notifications: This test verifies that the app correctly handles notifications, ensuring that sensitive information, such as personally identifiable information (PII), one-time passwords (OTPs), or other sensitive data, like health or financial...
- MASTG-TEST-0318 — References to SDK APIs Known to Handle Sensitive User Data: This test verifies whether an app uses SDK (third-party library) APIs known to handle sensitive user data (e.g., as defined in Google Play's Data safety section or the relevant privacy regulations).
- MASTG-TEST-0319 — Runtime Use of SDK APIs Known to Handle Sensitive User Data: This test is the dynamic counterpart to @MASTG-TEST-0318.

Mapped MASTG best practices:

- MASTG-BEST-0027 — Preventing Sensitive Data Exposure in Notifications: The source provides the mapped security guidance for this control.

Mapped MASTG knowledge:

- MASTG-KNOW-0054 — App Notifications: It is important to understand that notifications should never be considered private. When a notification is handled by the Android system it is broadcasted system-wide and any application running with a NotificationListenerService can...
