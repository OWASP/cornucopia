## Scenario: Invent Your Own Frontend Attack

You identifies and exploits a frontend attack vector that falls outside the application's existing threat model, using a technique that arises from an unexpected interaction between browser capabilities, security controls, or application-specific behavior. This occurs because:

1. **Incomplete threat model:** The team has assessed known attack categories but has not considered how novel browser features, library behaviours, or application-specific logic might be combined in unexpected ways.

2. **Assumed security control coverage:** Individual controls — input sanitisation, CSP, authentication checks — are evaluated in isolation, leaving gaps that only become visible when controls interact or when an attacker approaches the application from an angle the model did not anticipate.

3. **Emerging and underexplored attack surface:** Browser APIs, JavaScript runtime behaviours, and third-party library internals introduce attack surface that is not yet well-documented in standard threat catalogues, making it easy to overlook during design reviews.

## Threat Modeling

### STRIDE

The appropriate STRIDE category depends on the specific threat you create and the way the agent is misused.

### What can go wrong?

An attack that falls outside the threat model is, by definition, one the team has not prepared specific defenses against. Novel techniques can bypass controls that are correctly implemented for known threats, produce no anomalous server-side signals, and persist undetected until an unrelated observation prompts investigation. The impact depends entirely on the technique you employ, it may be as contained as data exposure for a single user, or as broad as persistent code execution across all sessions.

### What are we going to do about it?

Build defence-in-depth so that no single security control is a single point of failure, and maintain the ability to detect and respond to attacks that were not anticipated at design time.

1. Apply the principle of layered defence: ensure that the failure of any one control (sanitisation, CSP, authentication) does not by itself give an attacker full exploitation; a second independent control should still be in place.
2. Adopt secure-by-default library and framework choices that reduce the attack surface of common patterns; for example, prefer libraries with prototype pollution protections built in, and keep dependencies updated to receive security patches for newly discovered techniques.
3. Implement client-side and server-side anomaly detection: unusual API call patterns, unexpected payloads, or out-of-character user behavior may be the first signal of an attack that has no known signature.
4. Conduct regular threat modelling sessions that include time for free-form adversarial thinking — explicitly ask "what if the attacker does something we haven't considered?" — and revisit the model when new browser features or libraries are adopted.