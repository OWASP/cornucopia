## Scenario: Juan can access functionality from a rooted, jailbroken, or infected device because the app does not detect or appropriately respond to hostile environments

### Example

Juan installs a banking app on a rooted phone whose security checks are absent. A companion tool reads the account screen and submits a transfer, while Juan’s phone recommends giving the root user a tiny crown.

The app should detect rooted, jailbroken, or infected environments and respond according to the risk, such as restricting sensitive operations. Ignoring a hostile device leaves protected functionality available to local attackers.


## Threat Modeling

### STRIDE

This scenario is primarily **Information Disclosure**, **Elevation of Privilege** in STRIDE. The named condition is: Juan can access functionality from a rooted, jailbroken, or infected device because the app does not detect or appropriately respond to hostile environments.

- **MAS-THREAT-0051:** Attackers can run and manipulate the app in a privileged environment without resistance.

- **MAS-ATTACK-0003:** Using dynamic instrumentation.
- **MAS-ATTACK-0005:** Accessing the device storage on a compromised device.
- **MAS-ATTACK-0065:** Running the app on a rooted or jailbroken device they control.

### What can go wrong?

If Juan can access functionality from a rooted, jailbroken, or infected device because the app does not detect or appropriately respond to hostile environments, the failure is concrete rather than merely theatrical: the app could let an attacker cross the resilience boundary and reach data or capability that this flow should protect. In this card, the practical route includes Using dynamic instrumentation. Also, Accessing the device storage on a compromised device. That can turn a normal user action into unauthorized access, disclosure, alteration, or service disruption; the mapped weakness entries below identify the exact implementation evidence to check.

Mapped weaknesses that sharpen the review:

- MASWE-0055 — Malware Detection Not Implemented: This weakness occurs when an app does not implement or integrate techniques to detect malware on the device or malicious apps and components that could target it.
- MASWE-0051 — Root/Jailbreak Detection Not Implemented: This weakness occurs when an app does not implement effective techniques to detect whether the device it runs on is rooted or jailbroken.

### What are we going to do about it?

Use Play Integrity, App Attest, or equivalent platform signals with rooted or jailbroken-device detection to protect high-risk data, and degrade or deny sensitive actions on hostile devices; test compromised, infected, and falsely reported environments.


Mapped MASTG tests:

- MASTG-TEST-0240 — Jailbreak Detection in Code: The test verifies that a mobile app can detect if the iOS device it is running on is jailbroken. It does so by statically analyzing the app binary for common jailbreak detection checks (@MASTG-KNOW-0084). For example, the app may check...
- MASTG-TEST-0241 — Runtime Use of Jailbreak Detection Techniques: The test verifies that a mobile application can identify if the iOS device it is running on is jailbroken. It does so by dynamically analyzing the app binary for common jailbreak detection checks (@MASTG-KNOW-0084) and trying to bypass...
- MASTG-TEST-0324 — References to Root Detection Mechanisms: This test checks whether the app implements root detection by statically analyzing the app binary for common root detection patterns. These may include checks for files and artifacts typically associated with rooted devices, as well as...
- MASTG-TEST-0325 — Runtime Use of Root Detection Techniques: This test verifies whether an app implements runtime root detection by attempting to hook into common root detection mechanisms. These may include checks for files and artifacts typically associated with rooted devices, as well as calls...

Mapped MASTG best practices:

- MASTG-BEST-0029 — Implementing Resilience and RASP Signals: The source provides the mapped security guidance for this control.
- MASTG-BEST-0030 — Implementing Root Detection: Root detection is an environment risk signal that helps identify devices with elevated privilege or common rooting artifacts. It is a cost raising measure and it is bypassable, so it should be used only when rooted device risk...

Mapped MASTG knowledge:

- MASTG-KNOW-0084 — Jailbreak Detection: Jailbreak detection mechanisms are added to reverse engineering defense to make running the app on a jailbroken device more difficult. This blocks some of the tools and techniques reverse engineers like to use. Like most other types of...
- MASTG-KNOW-0027 — Root Detection: In the context of anti-reversing, the goal of root detection is to make running the app on a rooted device a bit more difficult, which in turn blocks some of the tools and techniques reverse engineers like to use. Like most other...
