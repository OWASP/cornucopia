## Scenario: Darío’s Deceptive Data Manipulation

Imagine a scenario where Darío takes advantage of the application's trust in its data sources. He manipulates the system in several ways:

1. **Exploiting User-Defined Data:** The application overly trusts data input by users.

2. **Tampering with Client-Side Data:** The application fails to validate data altered on a client device.

3. **Altering State Data on Client Devices:** The application doesn't verify the integrity of state data, like session tokens, stored on client devices.

4. **Lack of Identity Verification:** The system inadequately verifies the identity of a user during data validation.

### Example

Darío attacks by altering a session token stored in his browser's local storage. He changes the token's value to mimic that of another user, say, Colin. Since the application trusts this client-side data without additional verification, Darío gains access to Colin's account and privileges. This breach occurs because the system assumes the integrity and authenticity of locally stored data without adequately verifying it.

## Threat Modeling

### STRIDE

Darío is pretending to be Colin by taking advantage of the application's trust in its data sources. 
STRIDE’s **Spoofing** covers threats where an attacker assumes another identity or credentials to gain access. This is a textbook spoofing/impersonation attack: the system trusted the presented identity without adequate verification, but the consequences or secondary impacts can include any of the other categories depending on the context.

### What can go Wrong?

This kind of vulnerability can lead to identity theft, unauthorized access, and potentially severe data breaches.

For more things that can go wrong, see the [Common Attack Patterns related to this card](#mapping 'Common Attack Patterns related to this card [internal]') in the table below.

### What are you going to do about it?

1. Implement strict validation of user-defined and client-side data.
2. Ensure strong verification of user identity and the integrity of state data stored on client devices.
3. Regularly review and strengthen security measures to guard against data manipulation.

For detailed advice on how to mitigate threats related to the card, see the [ASVS and OWASP Developer Guide requirements ](#mapping 'ASVS and OWASP Developer Guide requirements [internal]') in the table below.
