## Scenario: Aatif can influence or alter authentication controls and can therefore bypass them

Consider a scenario where Aatif has identified that the app's authentication module loads its configuration (session timeout, required factors, biometric policy) from a local `auth_config.json` file that is not integrity-protected. On a rooted device, Aatif modifies `auth_config.json` to set `require_biometric: false` and `session_timeout: 99999`. The app reads the modified config at startup and applies the relaxed policy. Aatif authenticates with only a PIN, which he knows, and maintains the session indefinitely.

1. Authentication configuration stored locally without integrity protection can be modified by an attacker with device access.
2. Authentication logic that can be influenced by runtime hooks (Frida, Xposed) can have its behaviour altered without modifying the binary.
3. A/B testing or feature-flag systems that control security-relevant authentication requirements can be manipulated if the flag values are attacker-controllable.

### Example

Aatif discovers the app uses a remote feature-flag service and that the flags are cached locally without signing. He intercepts the flag update request with a MITM proxy and substitutes a response that disables multi-factor authentication. The app caches the manipulated flags. On the next launch, MFA is not required. The feature-flag system was designed to roll out UI changes safely. Nobody considered that it also controlled authentication requirements.

## Threat Modeling

### STRIDE

This scenario falls under **Tampering** and **Spoofing**.

Aatif modifies the authentication controls to reduce their effectiveness, then uses the weakened controls to authenticate without satisfying the intended security requirements.

### What can go wrong?

- Authentication policy weakened below the security baseline; requirements that should be mandatory become optional.
- Cryptographic controls that implement authentication are bypassed through runtime hook injection.
- Feature flags that control security requirements are manipulated, silently downgrading security for affected users.

### What are we going to do about it?

- Treat security-relevant configuration as code, not as mutable runtime data: hard-code the minimum security requirements and do not allow local configuration to weaken them.
- Integrity-protect and authenticate any remotely fetched security configuration; verify the digital signature before applying it.
- Implement runtime integrity checks to detect active hooking frameworks.
- Never allow feature flags or A/B tests to disable mandatory authentication factors below the documented security baseline.
