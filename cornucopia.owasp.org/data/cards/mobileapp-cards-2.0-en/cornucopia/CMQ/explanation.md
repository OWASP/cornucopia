## Scenario: Victor can patch the app and use it to distribute malicious code because the runtime integrity checks are not strong enough according to what is recommended or the perceived effort of a potential attacker

### Example

Victor repairs a vending machine app whose runtime check merely looks for a file named `honest-device.txt`. He renames a note from “honest-device.txt—please buy crisps” and the machine unlocks its maintenance menu, dispensing every snack as a security demonstration.

Integrity checks that are easy to patch or satisfy with a renamed file do not protect the runtime. Stronger, attack-resistant verification is needed to stop a modified app from distributing code or changing its behavior.


## Threat Modeling

### STRIDE

This scenario is primarily **Tampering** in STRIDE. The named condition is: Victor can patch the app and use it to distribute malicious code because the runtime integrity checks are not strong enough according to what is recommended or the perceived effort of a potential attacker.

- **MAS-THREAT-0056:** Attackers can distribute and run modified copies of the app.
- **MAS-THREAT-0058:** Attackers can modify the app's code while it runs.

- **MAS-ATTACK-0040:** Patching or repackaging the app to remove or alter client-side checks.
- **MAS-ATTACK-0068:** Impersonating the app with scripts, bots, or tampered clients when interacting with the backend.
- **MAS-ATTACK-0069:** Installing a repackaged version of the app on victim devices.
- **MAS-ATTACK-0002:** Debugging the app at runtime.
- **MAS-ATTACK-0003:** Using dynamic instrumentation.

### What can go wrong?

If Victor can patch the app and use it to distribute malicious code because the runtime integrity checks are not strong enough according to what is recommended or the perceived effort of a potential attacker, the failure is concrete rather than merely theatrical: the app could let an attacker cross the cornucopia boundary and reach data or capability that this flow should protect. In this card, the practical route includes Patching or repackaging the app to remove or alter client-side checks. Also, Impersonating the app with scripts, bots, or tampered clients when interacting with the backend. That can turn a normal user action into unauthorized access, disclosure, alteration, or service disruption; the mapped weakness entries below identify the exact implementation evidence to check.

Mapped weaknesses that sharpen the review:

- MASWE-0056 — App Attestation Not Implemented: This weakness occurs when an app does not provide its backend with server-verifiable attestation evidence about the app instance (e.g. app signature), or when the backend does not validate and enforce that evidence to determine whether...
- MASWE-0058 — Runtime Code Integrity Not Verified: This weakness occurs when an app is running in an unsafe environment (rooted or jailbroken device) and does not verify the integrity of its own code at runtime, allowing in-memory patching, code injection, and hooking to go undetected.

### What are we going to do about it?

Protect runtime integrity checks with signed code and server-verified attestation, detect patched or hooked checks, and deliver updates only through authenticated channels; test modified packages and bypassed signals before enabling distribution features.


Mapped MASTG tests:

- MASTG-TEST-0220 — Usage of Outdated Code Signature Format: On iOS, code signatures verify the integrity and authenticity of an app's binary, preventing unauthorized modifications and ensuring that the app is trusted by the operating system. Apple regularly updates its code signature formats to...
- MASTG-TEST-0341 — Runtime Use of Hook Detection Techniques: This test verifies whether the app detects and responds to instrumentation and hooking attempts at runtime. For example, if the app does not terminate immediately when the following methods are called:
- MASTG-TEST-0354 — Runtime Use of Hook Detection Techniques: This test verifies whether the app detects and responds to instrumentation and hooking attempts at runtime. For example, if the app does not terminate immediately when the following APIs or functions are hooked:

Mapped MASTG best practices:

- MASTG-BEST-0041 — Hardening Against Runtime Hooking: Defending against runtime hooking requires a layered approach that combines several types of security controls:
- MASTG-BEST-0048 — Hardening Against Reverse Engineering Tools: Defending against reverse engineering tools on iOS requires a layered approach that combines several types of security controls:

Mapped MASTG knowledge:

- MASTG-KNOW-0030 — Reverse Engineering Tool Detection: Reverse engineering and instrumentation tools often leave observable artifacts on the device or inside the app process. These artifacts can include installed packages, binaries, running services, open ports, loaded libraries, memory...
- MASTG-KNOW-0118 — Runtime Application Self-Protection (RASP): Runtime Application Self-Protection (RASP) is a security technology embedded in mobile apps to detect and prevent real-time attacks. Unlike server-side or network-based security solutions, RASP integrates directly into the app's runtime...
- MASTG-KNOW-0140 — Source Code Integrity Checks: iOS uses code signing to verify app authenticity before launch (see @MASTG-TECH-0084). Apps can also implement additional runtime checks that inspect the Mach-O binary structure to verify the integrity of their own executable code,...
- MASTG-KNOW-0058 — App Signing: Code signing your app assures users that the app has a known source and hasn't been modified since it was last signed. Before your app can integrate app services, be installed on a non-jailbroken device, or be submitted to the App...
- MASTG-KNOW-0032 — Runtime Integrity Verification: defensive controls in this category verify the integrity of the app's memory to defend against runtime memory patches. Such changes include unwanted modifications to native code, bytecode execution targets, function pointer tables,...
- MASTG-KNOW-0087 — Reverse Engineering Tools Detection: The presence of tools, frameworks and apps commonly used by reverse engineers may indicate an attempt to reverse engineer the app. Some of these tools can only run on a jailbroken device, while others force the app into debugging mode...
