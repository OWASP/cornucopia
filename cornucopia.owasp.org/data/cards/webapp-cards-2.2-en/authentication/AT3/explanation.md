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

### What can go Wrong?

Such vulnerabilities can lead to widespread unauthorized access, data breaches, identity theft, and compromise of sensitive information.

### What are you going to do about it?

- Implement and enforce secure password policies, including regular changes and strong, unique passwords.
- Use encryption for data in transit and secure storage methods for sensitive information.
- Educate users about secure practices, like avoiding password reuse and being cautious of their surroundings when entering passwords.
- Ensure systems are designed to allow users to change their passwords and keep security questions confidential.

For detailed advice on how to mitigate threats related to the card, see the [ASVS and OWASP Developer Guide requirements ](#mapping 'ASVS and OWASP Developer Guide requirements [internal]') in the table below.
