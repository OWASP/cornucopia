## Scenario: Juan can bypass jailbreak and root detection, execute administrative functions, bypass integrity checks, and access controls and trigger app functionality

Consider a scenario where Juan has a jailbroken iPhone with Shadowrocket and a Cydia tweak installed. The banking app's jailbreak detection checks for the presence of Cydia's application bundle and the writability of `/private/`. Juan uses a jailbreak-hiding tool (Liberty Lite, A-Bypass) that intercepts the file-existence and file-system-write calls and returns "not found" / "failed" for the jailbreak indicators. The app's detection logic sees a clean device. Juan now has a fully functional banking app running on a jailbroken device where his other tools have root-level access to the process.

1. Jailbreak/root detection based solely on file-existence checks is trivially bypassed by jailbreak-hiding tools.
2. Single-layer detection that checks one set of indicators is bypassed by tools that specifically target those indicators.
3. On rooted Android, `su` binaries, build properties, and system app modifications reveal root; all can be hidden by a sufficiently motivated attacker.

### Example

Juan uses A-Bypass to hide the jailbreak indicators from the banking app. The app opens normally. Juan then uses Frida, running on the same jailbroken device, to hook the app's balance-display function and read the decrypted account balance without any additional authentication. The app's cryptographic protections use software-only checks — they can be bypassed once the process is accessible under Frida. Juan now has direct access to the app's decrypted state. The jailbreak detection was defeated before the cryptographic protection was challenged.

## Threat Modeling

### STRIDE

This scenario falls under **Elevation of Privilege**.

Bypassing jailbreak/root detection gives Juan access to a privileged execution environment from which he can use OS-level and process-level tools that the app's security model assumes are not available.

### What can go wrong?

- Cryptographic keys are extracted from memory using root/jailbreak access.
- App data is accessed directly from the filesystem using root-level file access.
- Authentication and integrity checks are bypassed using Frida/Cycript/LLDB.
- The assumption that "the device is trusted" that underlies many app security controls is invalidated.

### What are we going to do about it?

- Implement multiple, diverse detection mechanisms for root/jailbreak: file existence, API behaviour checks, library injection detection, native system-call probes.
- Combine detection with hardware-backed cryptography: even if detection is bypassed, keys stored in the Secure Enclave / StrongBox are not extractable.
- Respond to detection with a risk signal to the server: escalate to additional verification rather than immediate termination (which can be patched).
- Clearly document in the app's threat model what the acceptable risk level is for jailbroken devices, and design security controls accordingly.
