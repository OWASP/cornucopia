## Scenario: Sherif can disable or evade anti-reversing and runtime-protection checks by patching these or hooking the signals they rely on, allowing analysis or instrumentation to continue undetected

### Example

Sherif patches an anti-reversing routine so it always reports “all clear,” then hooks the signal that should detect instrumentation. The app congratulates him for passing its security exam while he is actively rewriting the answer key.

Runtime defenses must protect their checks and the signals they depend on. If both can be patched or intercepted without detection, analysis and instrumentation continue invisibly.


## Threat Modeling

### STRIDE

This scenario is primarily **Tampering** in STRIDE. The named condition is: Sherif can disable or evade anti-reversing and runtime-protection checks by patching these or hooking the signals they rely on, allowing analysis or instrumentation to continue undetected.

- **MAS-THREAT-0058:** Attackers can modify the app's code while it runs.

- **MAS-ATTACK-0002:** Debugging the app at runtime.
- **MAS-ATTACK-0003:** Using dynamic instrumentation.

### What can go wrong?

If Sherif can disable or evade anti-reversing and runtime-protection checks by patching these or hooking the signals they rely on, allowing analysis or instrumentation to continue undetected, the failure is concrete rather than merely theatrical: the app could let an attacker cross the resilience boundary and reach data or capability that this flow should protect. In this card, the practical route includes Debugging the app at runtime. Also, Using dynamic instrumentation. That can turn a normal user action into unauthorized access, disclosure, alteration, or service disruption; the mapped weakness entries below identify the exact implementation evidence to check.

Mapped weaknesses that sharpen the review:

- MASWE-0058 — Runtime Code Integrity Not Verified: This weakness occurs when an app is running in an unsafe environment (rooted or jailbroken device) and does not verify the integrity of its own code at runtime, allowing in-memory patching, code injection, and hooking to go undetected.

### What are we going to do about it?

Make anti-reversing and runtime checks tamper-evident, verify their signals with server-side attestation where feasible, and avoid trusting a single local flag; test patched checks and hooked signals to confirm sensitive actions are denied safely.


Mapped MASTG tests:

- MASTG-TEST-0341 — Runtime Use of Hook Detection Techniques: This test verifies whether the app detects and responds to instrumentation and hooking attempts at runtime. For example, if the app does not terminate immediately when the following methods are called:
- MASTG-TEST-0354 — Runtime Use of Hook Detection Techniques: This test verifies whether the app detects and responds to instrumentation and hooking attempts at runtime. For example, if the app does not terminate immediately when the following APIs or functions are hooked:

Mapped MASTG best practices:

- MASTG-BEST-0041 — Hardening Against Runtime Hooking: Defending against runtime hooking requires a layered approach that combines several types of security controls:
- MASTG-BEST-0048 — Hardening Against Reverse Engineering Tools: Defending against reverse engineering tools on iOS requires a layered approach that combines several types of security controls:

Mapped MASTG knowledge:

- MASTG-KNOW-0030 — Reverse Engineering Tool Detection: Reverse engineering and instrumentation tools often leave observable artifacts on the device or inside the app process. These artifacts can include installed packages, binaries, running services, open ports, loaded libraries, memory...
- MASTG-KNOW-0032 — Runtime Integrity Verification: defensive controls in this category verify the integrity of the app's memory to defend against runtime memory patches. Such changes include unwanted modifications to native code, bytecode execution targets, function pointer tables,...
- MASTG-KNOW-0087 — Reverse Engineering Tools Detection: The presence of tools, frameworks and apps commonly used by reverse engineers may indicate an attempt to reverse engineer the app. Some of these tools can only run on a jailbroken device, while others force the app into debugging mode...
- MASTG-KNOW-0109 — Binary Patching: Patching is the process of changing the compiled app, e.g., changing code in binary executables, modifying Java bytecode, or tampering with resources. This process is known as _modding_ in the mobile game hacking scene. Patches can be...
- MASTG-KNOW-0110 — Code Injection: Code injection is a very powerful technique that allows you to explore and modify processes at runtime. Injection can be implemented in various ways, but you'll get by without knowing all the details thanks to freely available,...
- MASTG-KNOW-0119 — Key Attestation: The source provides the mapped security guidance for this control.
- MASTG-KNOW-0118 — Runtime Application Self-Protection (RASP): Runtime Application Self-Protection (RASP) is a security technology embedded in mobile apps to detect and prevent real-time attacks. Unlike server-side or network-based security solutions, RASP integrates directly into the app's runtime...
