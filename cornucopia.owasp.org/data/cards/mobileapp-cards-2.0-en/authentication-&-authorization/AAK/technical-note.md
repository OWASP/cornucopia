## Platform-Aware Review Guidance

**Android**
- Do not store authentication policy in externally modifiable files; hard-code the minimum policy in the app's source.
- If remote configuration is used for security parameters, sign the configuration server-side and verify the signature on the client before applying.
- Detect runtime hook frameworks: check for Frida/Xposed indicators in `/proc/self/maps`, loaded shared libraries, and method replacement indicators.

**iOS**
- Minimum authentication requirements (biometric required, session timeout) should not be overridable from `UserDefaults` or a local plist.
- Remote config (Firebase Remote Config, etc.) for security parameters: verify the payload signature before use; treat an unsigned or invalid payload as "use the hardcoded default."
- Detect jailbreak and hooking indicators; escalate to remote re-authentication rather than weakening security.

**Testing**
- On a rooted device, modify any local configuration files related to authentication and verify the app does not apply the modified policy.
- Use a proxy to modify remote configuration responses; verify the app rejects unsigned or modified payloads.
- Use Frida to hook authentication decision functions and attempt to return `true`; verify the cryptographic control still prevents access.

**OWASP Mappings**
- MASVS: AUTH-2
- MASTG: TEST-0017, TEST-0018, TEST-0064
- MASWE: (see MASVS references above)
