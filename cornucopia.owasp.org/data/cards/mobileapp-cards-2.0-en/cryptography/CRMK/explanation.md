## Scenario: Tarik can influence or alter cryptographic operations and can therefore bypass them

### Example

Tarik changes a hotel app’s cryptographic response from “guest” to “manager” by editing a value in transit. The app accepts the altered result and gives him a room key, a conference badge, and a baffling invitation to judge the breakfast omelets.

Cryptographic decisions need authenticated inputs and protected implementation paths. If an attacker can influence an operation or its result, the control can be bypassed instead of enforcing the intended access decision.


## Threat Modeling

### STRIDE

This scenario is primarily **Spoofing**, **Tampering** in STRIDE. The named condition is: Tarik can influence or alter cryptographic operations and can therefore bypass them.

- **MAS-THREAT-0058:** Attackers can modify the app's code while it runs.

- **MAS-ATTACK-0002:** Debugging the app at runtime.
- **MAS-ATTACK-0003:** Using dynamic instrumentation.

### What can go wrong?

If Tarik can influence or alter cryptographic operations and can therefore bypass them, the failure is concrete rather than merely theatrical: the app could let an attacker cross the cryptography boundary and reach data or capability that this flow should protect. In this card, the practical route includes Debugging the app at runtime. Also, Using dynamic instrumentation. That can turn a normal user action into unauthorized access, disclosure, alteration, or service disruption; the mapped weakness entries below identify the exact implementation evidence to check.

Mapped weaknesses that sharpen the review:

- MASWE-0058 — Runtime Code Integrity Not Verified: This weakness occurs when an app is running in an unsafe environment (rooted or jailbroken device) and does not verify the integrity of its own code at runtime, allowing in-memory patching, code injection, and hooking to go undetected.

### What are we going to do about it?

Protect cryptographic configuration and operations from alteration by using immutable, authenticated policy and platform-protected keys; verify inputs and outputs, detect unexpected providers or hooks, and test that modified operations are rejected.


Mapped MASTG tests:

- MASTG-TEST-0341 — Runtime Use of Hook Detection Techniques: This test verifies whether the app detects and responds to instrumentation and hooking attempts at runtime. For example, if the app does not terminate immediately when the following methods are called:
- MASTG-TEST-0354 — Runtime Use of Hook Detection Techniques: This test verifies whether the app detects and responds to instrumentation and hooking attempts at runtime. For example, if the app does not terminate immediately when the following APIs or functions are hooked:

Mapped MASTG best practices:

- MASTG-BEST-0041 — Hardening Against Runtime Hooking: Defending against runtime hooking requires a layered approach that combines several types of security controls:
- MASTG-BEST-0048 — Hardening Against Reverse Engineering Tools: Defending against reverse engineering tools on iOS requires a layered approach that combines several types of security controls:

Mapped MASTG knowledge:

- MASTG-KNOW-0032 — Runtime Integrity Verification: defensive controls in this category verify the integrity of the app's memory to defend against runtime memory patches. Such changes include unwanted modifications to native code, bytecode execution targets, function pointer tables,...
- MASTG-KNOW-0140 — Source Code Integrity Checks: iOS uses code signing to verify app authenticity before launch (see @MASTG-TECH-0084). Apps can also implement additional runtime checks that inspect the Mach-O binary structure to verify the integrity of their own executable code,...
- MASTG-KNOW-0030 — Reverse Engineering Tool Detection: Reverse engineering and instrumentation tools often leave observable artifacts on the device or inside the app process. These artifacts can include installed packages, binaries, running services, open ports, loaded libraries, memory...
- MASTG-KNOW-0118 — Runtime Application Self-Protection (RASP): Runtime Application Self-Protection (RASP) is a security technology embedded in mobile apps to detect and prevent real-time attacks. Unlike server-side or network-based security solutions, RASP integrates directly into the app's runtime...
- MASTG-KNOW-0087 — Reverse Engineering Tools Detection: The presence of tools, frameworks and apps commonly used by reverse engineers may indicate an attempt to reverse engineer the app. Some of these tools can only run on a jailbroken device, while others force the app into debugging mode...
