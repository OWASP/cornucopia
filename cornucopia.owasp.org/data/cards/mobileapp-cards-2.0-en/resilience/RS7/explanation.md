## Scenario: Erlend can compromise the app by running it in an emulator, simulator, virtualized environment, or untrusted device because environment detection or attestation are absent or too weak

### Example

Erlend runs a payment app inside a desktop emulator that reports itself as an ordinary phone. The app accepts the environment, and Erlend’s virtual cashier approves a transaction for 10,000 virtual bananas.

Environment detection and attestation should identify emulators, simulators, virtualization, and untrusted devices when those conditions matter. Weak detection gives an attacker a convenient laboratory for manipulating the app.


## Threat Modeling

### STRIDE

This scenario is primarily **Tampering**, **Information Disclosure** in STRIDE. The named condition is: Erlend can compromise the app by running it in an emulator, simulator, virtualized environment, or untrusted device because environment detection or attestation are absent or too weak.

- **MAS-THREAT-0053:** Attackers can analyze and automate the app in a fully controlled environment.

- **MAS-ATTACK-0003:** Using dynamic instrumentation.
- **MAS-ATTACK-0066:** Running the app in an emulator or virtual device.

### What can go wrong?

If Erlend can compromise the app by running it in an emulator, simulator, virtualized environment, or untrusted device because environment detection or attestation are absent or too weak, the failure is concrete rather than merely theatrical: the app could let an attacker cross the resilience boundary and reach data or capability that this flow should protect. In this card, the practical route includes Using dynamic instrumentation. Also, Running the app in an emulator or virtual device. That can turn a normal user action into unauthorized access, disclosure, alteration, or service disruption; the mapped weakness entries below identify the exact implementation evidence to check.

Mapped weaknesses that sharpen the review:

- MASWE-0054 — Device Attestation Not Implemented: This weakness occurs when an app does not implement device attestation, so its backend cannot distinguish requests made from genuine, uncompromised devices from those coming from rooted, emulated, tampered, or automated environments.
- MASWE-0053 — Emulated or Virtual Device Detection Not Implemented: This weakness occurs when an app does not implement effective techniques to detect that it is running in an emulator or virtual device.

### What are we going to do about it?

Use platform attestation and emulator or virtual-device signals to protect high-risk actions, bind decisions to a server challenge, and define a safe limited mode; test emulators, rooted or untrusted devices, replayed attestations, and false positives.


Mapped MASTG tests:

- MASTG-TEST-0351 — Runtime Use of Emulator Detection Techniques: This test verifies whether an app implements runtime emulator detection by attempting to hook into common emulator detection mechanisms. These may include checks for build properties and artifacts typically associated with emulated...
- MASTG-TEST-0367 — Runtime Use of Virtual Device Detection Techniques: This test verifies if the app implements checks to detect the presence of an iOS virtual device (like @MASTG-TOOL-0108) by attempting to hook into common virtual device detection mechanisms.

Mapped MASTG best practices:

- MASTG-BEST-0046 — Hardening Against Emulation: Emulated devices allow target applications to be executed in controlled environments that may use custom system images, modified platform components, or instrumentation that is difficult for the app to detect. This enables advanced...
- MASTG-BEST-0053 — Hardening Against Virtual Devices: Virtual devices, such as @MASTG-TOOL-0108 and newer research environments, allow target applications to be executed in controlled environments that may use custom system images, modified platform components, missing or simulated...

Mapped MASTG knowledge:

- MASTG-KNOW-0031 — Emulator Detection: In the context of anti-reversing, the goal of emulator detection is to increase the difficulty of running the app on an emulated device. This increased difficulty forces the reverse engineer to defeat the emulator checks or use a...
- MASTG-KNOW-0135 — Virtual Devices Detection: In the context of anti-reversing, the goal of emulator and virtual device detection is to increase the difficulty of running the app on an emulated or virtualized device. This increased difficulty forces the reverse engineer to defeat...
