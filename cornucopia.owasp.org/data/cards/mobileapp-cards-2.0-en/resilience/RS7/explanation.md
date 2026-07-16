## Scenario: Erlend can compromise the app by running it in an emulator, simulator, virtualized environment, or untrusted device because environment detection and attestation are absent or too weak

Consider a scenario where Erlend runs the target banking app in an Android emulator to automate credential stuffing attacks. The app does not detect emulator environments and does not require device attestation. Erlend runs thousands of login attempts per hour from the emulator, automating the attack at scale that would be impossible on a physical device. The server-side rate limiting is per-IP; Erlend rotates IPs via a proxy. The emulator environment was the enabler.

1. Emulators allow scripted, high-speed interaction without physical device limitations, enabling automation attacks.
2. Virtual environments may have different sensor behaviour, clock characteristics, and hardware identifiers that reveal the non-physical nature.
3. Apps without device attestation cannot distinguish legitimate physical-device users from automated emulator-based attackers.

### Example

Erlend sets up an Android emulator farm. He notes that the banking app's login flow does not implement any emulator detection or device attestation requirement. He writes an Appium script that automates credential stuffing using a list of breached username/password combinations. The emulator environment enables 500 attempts per minute per instance. The app's rate limiting was applied at the user account level, not the device level. The attack runs undetected for 48 hours, compromising 1,200 accounts. The bank discovers it when customers start calling about unauthorised transactions.

## Threat Modeling

### STRIDE

This scenario falls under **Spoofing** (masquerading as a legitimate device) and **Elevation of Privilege** (bypassing device-level rate limiting and attestation).

Emulator-based attacks allow an attacker to impersonate many legitimate users at scale, exploiting the absence of device-level identity verification.

### What can go wrong?

- Credential stuffing attacks run at machine speed from emulators.
- Bots automate in-app fraud (account creation, bonus abuse, payment fraud) at scale.
- Sensitive reverse engineering is performed in a controlled virtual environment without hardware-based detection.

### What are we going to do about it?

- Implement emulator detection heuristics: check hardware identifiers, sensor availability, build properties (`android.os.Build.FINGERPRINT`, `ro.kernel.qemu`), and network characteristics.
- Use hardware attestation (Google Play Integrity API / Apple App Attest) to verify the device is a genuine, unmodified physical device.
- Apply device-level rate limiting on the server side in addition to account-level limits.
- Treat attestation failure as a risk signal; escalate to additional verification rather than blanket rejection to avoid false positives for legitimate emulator-based QA.
