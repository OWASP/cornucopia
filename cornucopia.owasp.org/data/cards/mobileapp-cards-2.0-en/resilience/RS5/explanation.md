## Scenario: Matteo can bypass access controls and trigger functionality because debugging is left enabled in the production build

Consider a scenario where Matteo connects a device running the production app to his computer and uses ADB to attach a debugger. The production APK has `android:debuggable="true"` in its manifest. Matteo sets breakpoints in the authentication flow, inspects memory at the point where the session key is decrypted, and reads the plaintext key. He could also modify the execution flow to bypass the authentication check entirely. The production app was debuggable. The developer had not noticed.

1. `android:debuggable="true"` allows ADB debugger attachment to the app process, enabling memory inspection and execution control.
2. On iOS, production apps should not be signed with development certificates that enable debugger attachment.
3. Debug build features (admin menus, hidden flags) enabled by debuggable mode create additional attack vectors.

### Example

Matteo attaches `jdb` to the app process. He sets a breakpoint at the `decrypt()` method call and, when it is hit, inspects the local variable `key` — a raw byte array containing the decrypted AES key. He copies the key. He can now decrypt all of the user's locally stored data offline, without needing the device's PIN. The app was only debuggable because a CI pipeline step had incorrectly promoted the debug build artifact to the production release channel.

## Threat Modeling

### STRIDE

This scenario falls under **Elevation of Privilege** and **Information Disclosure**.

A debuggable production app allows any user with ADB access to inspect memory, modify execution flow, and bypass security controls — effectively granting them the ability to act as a developer with full process visibility.

### What can go wrong?

- Memory inspection at runtime reveals decrypted keys, tokens, and PII.
- Execution flow modification bypasses authentication, authorization, and integrity checks.
- Hidden debug menus or admin features, accessible only in debug mode, are activated.
- Production users can attach debuggers to the app, removing the privacy boundary between the OS and the app process.

### What are we going to do about it?

- Ensure release builds never have `android:debuggable="true"`; this attribute is absent or `false` in the release manifest by default if the build system is configured correctly.
- Verify programmatically at runtime: `ApplicationInfo.FLAG_DEBUGGABLE` should not be set; terminate or restrict functionality if it is.
- On iOS, ship only with production signing certificates; App Store distribution enforces this.
- Include a manifest debuggability check in the automated release process.
