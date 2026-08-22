## Scenario: Pramod can intercept credentials through misdirection because the app is vulnerable to attacks like Tapjacking, StrandHogg and/or URL scheme hijacking

Pramod notices that Ade’s mobile application does not properly validate exported activities or incoming intents. The app allows deep links for authentication flows but fails to verify their origin.

By launching a tapjacking overlay, Pramod places a transparent malicious layer over Ade’s login screen. The user believes they are interacting with the legitimate application, but their credentials are actually being captured by Pramod’s hidden interface.

In another scenario, Pramod exploits StrandHogg by registering a malicious activity that mimics Ade’s login page. When the victim enters their username and password, the credentials are intercepted before the user is redirected back to the real app to avoid suspicion.

If URL schemes are not properly validated, Pramod can also hijack authentication callbacks and intercept sensitive tokens during redirection flows.

### Example

Ade proudly launches a new feature that allows users to log in through a deep link received via email. Unfortunately, she forgets to validate which application handles the callback. Pramod registers the same URL scheme on his malicious app. When the user completes authentication, the token is sent directly to Pramod instead of Ade’s app. The login appears successful, but the attacker now has full access to the user’s account.

## Threat Modeling

### STRIDE

This scenario falls under the **Spoofing** category in the STRIDE threat modeling framework.

Pramod impersonates a trusted application interface or authentication handler to trick users into submitting credentials or tokens. The system fails to verify the authenticity of the interacting application, allowing the attacker to act as a legitimate entity.

### What can go wrong?

If activity hijacking, tapjacking overlays, or unvalidated deep links are allowed, attackers may intercept authentication credentials or tokens. This can lead to account compromise, session hijacking, and unauthorized access to sensitive information.

### What are we going to do about it?

- Disable or strictly control exported activities unless absolutely required.
- Validate the origin and integrity of incoming intents and deep links.
- Use protections against overlay attacks such as secure window flags.
- Implement tapjacking detection mechanisms.
- Enforce strict validation of URL schemes and authentication callbacks.
- Follow OWASP MASVS guidance for secure authentication and intent handling.
