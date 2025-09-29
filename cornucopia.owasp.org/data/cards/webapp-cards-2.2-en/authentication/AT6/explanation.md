## Scenario: Sven's Temporary Password Misuse

Envision a scenario where Sven capitalizes on the shortcomings in temporary password management. He exploits various system vulnerabilities:

1. **No Mandatory Change on First Use:** Users are not required to change temporary passwords upon first login.

2. **Excessive or No Expiry:** Temporary passwords remain valid for too long or don't have an expiration time.

3. **Insecure Delivery Methods:** Temporary passwords are delivered through insecure channels, rather than more secure out-of-band methods like post, mobile apps, or SMS.

### Example

Sven discovers that a company’s system issues temporary passwords to users which do not expire quickly and do not require a change upon first use. He intercepts or guesses these temporary passwords and gains access to user accounts, exploiting the extended period these passwords remain valid and the lack of a mandatory password reset on initial login.

## Threat Modeling

### STRIDE

This scenario is a clear case of STRIDE: **Spoofing**.

**Spoofing** is about pretending to be another user or system by falsifying identity.
Sven takes advantage of weakly managed temporary credentials to log in as a legitimate user.
The system fails to enforce proper lifecycle rules (expiry, one-time use, out-of-band delivery), which makes impersonation possible.

### What can go wrong?

This oversight can lead to unauthorized account access, data breaches, and potential exploitation of system vulnerabilities.

For more things that can go wrong, see the [Common Attack Patterns related to this card](#mapping 'Common Attack Patterns related to this card [internal]') in the table below.

### What are you going to do about it?

1. Implement policies that require users to change their temporary passwords upon first login.
2. Set short expiration times for temporary passwords to minimize the risk window.
3. Use secure, out-of-band methods for delivering temporary passwords to ensure their confidentiality and integrity.

For detailed advice on how to mitigate threats related to the card, see the [ASVS and OWASP Developer Guide requirements ](#mapping 'ASVS and OWASP Developer Guide requirements [internal]') in the table below.
