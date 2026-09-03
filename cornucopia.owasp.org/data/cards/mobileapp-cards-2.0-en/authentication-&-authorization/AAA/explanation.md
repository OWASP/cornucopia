## Scenario: You have invented a new attack against “Authentication & Authorization”

### Example

Inventing an authentication threat can lead to:

1. **User Impersonation**: Attackers access other users’ accounts and perform actions as them.
2. **Unauthorized Privilege Access**: Exploit weak authentication to perform higher-privileged actions.
3. **Credential Theft**: Capture passwords, API keys, or tokens.
4. **Bypassing Multi-Factor Authentication**: Circumventing 2FA or step-up authentication.
8. **Audit/Repudiation Issues**: Actions may be performed without proper identity attribution.


## Threat Modeling

### STRIDE

Authentication’s main purpose is to verify identity. If you can invent a new way to bypass or manipulate authentication, the attacker can impersonate legitimate users. That’s the essence of a **Spoofing** threat.
For authorization threats, the primary impact is usually **Elevation of Privilege**, since bypassing authorization typically means doing more than you should.

### What can go wrong?

If You have invented a new attack against “Authentication & Authorization”, the following threats are:

- User impersonation
- Privilege escalation
- Credential theft
- MFA bypass
- Audit gaps.

### What are we going to do about it?

Define a focused test for the invented authentication attack: require the server to authenticate and authorize every protected request, bind local credentials to Android Keystore or iOS Keychain controls, and reject tampered deep-link or component data before it reaches a privileged action.

Mapped MASTG tests:

- No MASTG test is assigned to this card; define a focused test for the invented attack.

Mapped MASTG best practices:

- No MASTG best practice is assigned. Use the narrowest platform control that blocks the attack.

Mapped MASTG knowledge:

- No MASTG knowledge entry is assigned; document the platform behavior discovered during review.
