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

### What can go wrong?

This kind of vulnerability can lead to identity theft, unauthorized access, and potentially severe data breaches.

Trust management is a popular technique for implementing information security, and specifically for access control policies. All data sources of an application are be classified into groups with varying degrees of trust. When doing this, it is imperative to ensure that trusted sources cannot be spoofed. This spoofing can be done in many ways:

1. Reflection attack
2. Principal Spoof
3. JSON Hijacking
4. Registry Poisoning
5. MITM
6. XSS

Attackers that are identified as trusted users or that are in a trusted zone with bad authentication techniques can do all sorts of things, depending on the services, such as:

1. Sniffing
2. Data tampering
3. Code Injection
4. DoS

For more things that can go wrong, see the [Common Attack Patterns related to this card](#mapping 'Common Attack Patterns related to this card [internal]') in the table below.

### What are we going to do about it?

1. Implement strict validation of user-defined and client-side data.
2. Ensure strong verification of user identity and the integrity of state data stored on client devices.
3. Regularly review and strengthen security measures to guard against data manipulation.

For detailed advice on how to mitigate threats related to the card, see the [ASVS and OWASP Developer Guide requirements ](#mapping 'ASVS and OWASP Developer Guide requirements [internal]') in the table below.
