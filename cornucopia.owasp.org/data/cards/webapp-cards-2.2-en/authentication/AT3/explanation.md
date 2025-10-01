## Scenario: Muhammad’s Secret Acquisition

Imagine a scenario where Muhammad, a skilled eavesdropper, obtains a user's password or other confidential information like security questions. He exploits various vulnerabilities:

1. **Observation During Entry:** Muhammad watches as a user enters their password.

2. **Local Cache Access:** He retrieves passwords stored in a local cache on a user's device.

3. **Memory Extraction:** Muhammad accesses passwords or secrets stored in the memory of a system.

4. **Interception in Transit:** He captures data as it travels across a network.

5. **Unprotected Storage Locations:** Muhammad finds passwords stored in unsecured locations.

6. **Widely Known Passwords:** He exploits commonly used or default passwords.

7. **Static Passwords:** Muhammad takes advantage of passwords that never expire.

8. **Inability of Users to Change Passwords:** He benefits from systems where users cannot change their passwords regularly.

### Example

Muhammad targets a company’s website where passwords are transmitted without encryption. He intercepts network traffic and captures the plaintext passwords as they travel from the user’s device to the server. This lack of secure transmission allows him to gather user credentials easily, leading to unauthorized access.

## Threat Modeling

### STRIDE

The scenario maps directly to STRIDE: **Information Disclosure**.

Muhammad gains access to confidential information (passwords, secrets) that should have been protected.
STRIDE’s **Information Disclosure** category is specifically about unauthorized exposure of sensitive data.
The example (plaintext password interception) is a textbook case of information disclosure due to lack of encryption in transit.

### What can go wrong?

Such vulnerabilities can lead to widespread unauthorized access, data breaches, identity theft, and compromise of sensitive information.
Common attacks include:

1. Stealing a password/secret in transit (e.g. in an email message, over an unencrypted HTTP connection)
2. Observing a password/secret being entered on screen
3. Weak password recovery (e.g. reliance only on 'security' questions)
4. Use of weak 'remember me' functionality
5. Re-use of passwords making them guessable
6. Passwords/secrets recorded in logs
7. Passwords/secrets exposed in form data/URLs
8. Client-side caching or storage of passwords/secrets
9. Hard-coding of passwords/secrets into code
10. Passwords never changed by user

For more things that can go wrong, see the [Common Attack Patterns related to this card](#mapping 'Common Attack Patterns related to this card [internal]') in the table below.

### What are you going to do about it?

1. Implement and enforce secure password policies, including regular changes and strong, unique passwords.
2. Use encryption for data in transit and secure storage methods for sensitive information.
3. Educate users about secure practices, like avoiding password reuse and being cautious of their surroundings when entering passwords.
4. Ensure systems are designed to allow users to change their passwords and keep security questions confidential.

For detailed advice on how to mitigate threats related to the card, see the [ASVS and OWASP Developer Guide requirements ](#mapping 'ASVS and OWASP Developer Guide requirements [internal]') in the table below.
