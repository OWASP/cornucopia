## Scenario: Ricardo can extract data stored by the app on a stolen or decommissioned device  because it does not enforce device access security policies (e.g. PIN protected locking, app-/os-version, USB debug deactivation, device encryption and rooting)

### Example

Ricardo buys a decommissioned tablet at an auction; it has no screen lock, encryption, or USB debugging restriction. He opens the previous owner’s delivery records and learns that 47 parcels were all destined for a suspiciously enthusiastic person named “Mum.”

Device access policies are part of the app’s protection. Without enforced locking, supported versions, encryption, and hostile-device controls, extracted storage can yield the app’s sensitive data.


## Threat Modeling

### STRIDE

This scenario is primarily **Spoofing**, **Information Disclosure**, **Elevation of Privilege** in STRIDE. The named condition is: Ricardo can extract data stored by the app on a stolen or decommissioned device  because it does not enforce device access security policies (e.g. PIN protected locking, app-/os-version, USB debug deactivation, device encryption and rooting).

- **MAS-THREAT-0017:** Attackers with physical access to the device can read the app's data and use its keys when no device credential protects them.

- **MAS-ATTACK-0063:** Accessing a lost or stolen device that has no secure lock screen configured.

### What can go wrong?

If Ricardo can extract data stored by the app on a stolen or decommissioned device  because it does not enforce device access security policies (e.g. PIN protected locking, app-/os-version, USB debug deactivation, device encryption and rooting), the failure is concrete rather than merely theatrical: the app could let an attacker cross the network-&-storage boundary and reach data or capability that this flow should protect. In this card, the practical route includes Accessing a lost or stolen device that has no secure lock screen configured. That can turn a normal user action into unauthorized access, disclosure, alteration, or service disruption; the mapped weakness entries below identify the exact implementation evidence to check.

Mapped weaknesses that sharpen the review:

- MASWE-0017 — Device Secure Lock Not Enforced: This weakness occurs when an app enables sensitive functionality without verifying that the device has a secure lock screen (passcode, PIN, pattern, or biometric) configured. Without a secure lock screen, cryptographic material cannot...

### What are we going to do about it?

Require the device protections that the data needs—secure lock, encryption, supported OS, and disabled USB debugging—and use platform signals to block or limit access on rooted or insecure devices; verify these policies on stolen-device and downgrade test cases.


Mapped MASTG tests:

- MASTG-TEST-0246 — Runtime Use of Secure Screen Lock Detection APIs: This test is the dynamic counterpart to @MASTG-TEST-0248.
- MASTG-TEST-0247 — References to APIs for Detecting Secure Screen Lock: This test verifies whether an app is running on a device with a passcode set. Android apps can determine whether a secure screen lock (such as PIN, or password) is enabled by using platform-provided APIs. Specifically, apps can utilize...
- MASTG-TEST-0248 — References to APIs for Detecting Secure Screen Lock: This test verifies that an app is running on a device with a secure screen lock (e.g. a passcode).
- MASTG-TEST-0249 — Runtime Use of Secure Screen Lock Detection APIs: This test is the dynamic counterpart to @MASTG-TEST-0247.

Mapped MASTG best practices:

- No MASTG best practice is assigned; use the narrowest platform control that blocks the attack.

Mapped MASTG knowledge:

- MASTG-KNOW-0056 — Local Authentication Framework: The Local Authentication framework provides facilities for requesting a passphrase or Touch ID authentication from users. Developers can display and utilize an authentication prompt by utilizing the function `evaluatePolicy` of the...
- MASTG-KNOW-0001 — Biometric Authentication: Android provides platform support for biometric authentication, such as fingerprint and face recognition, and exposes it to apps through the biometric APIs. At the framework level, Android includes support for face and fingerprint...
