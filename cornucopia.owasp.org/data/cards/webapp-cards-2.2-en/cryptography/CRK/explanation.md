## Scenario: Dan's Manipulation of Cryptography Code/Routines

Envision a scenario where Dan, exploiting security gaps, manages to influence or alter cryptography code or routines, including encryption, hashing, digital signatures, and random number/GUID generation. This issue arises due to:

1. **Vulnerabilities in Cryptography Code:** The cryptographic algorithms and routines are not sufficiently protected against unauthorized access and modifications.

2. **Weaknesses in System Security:** There are security lapses within the system that allow manipulation of cryptographic functions.

### Example

Dan targets an application whose cryptographic routines are part of a codebase with insufficient access controls. By exploiting a vulnerability in the application’s update mechanism, Dan injects malicious code that subtly alters the encryption routines. This alteration weakens the encryption process, making it easier for him to decrypt sensitive data. Additionally, he modifies the random number generation algorithm, resulting in predictable outputs that compromise the security of generated keys and tokens.

## Threat Modeling

### STRIDE

The applicable STRIDE category here is **Tampering**.

Dan is modifying the cryptographic routines themselves — the code that enforces encryption, hashing, digital signatures, and random number generation.
By altering this code, he changes the behavior of the system, allowing him to bypass security protections (e.g., decrypt data, predict random values).
STRIDE defines **Tampering** as the unauthorized modification of data or code, which is what is happening here.

### What can go wrong?

Such manipulation can lead to the compromise of entire cryptographic systems, rendering them ineffective and exposing sensitive data to unauthorized access or manipulation.

For more things that can go wrong, see the [Common Attack Patterns related to this card](#mapping 'Common Attack Patterns related to this card [internal]') in the table below.

### What are you going to do about it?

1. Implement strict access controls and monitoring systems to protect cryptographic code and routines from unauthorized modifications.
2. Regularly audit and test cryptographic implementations to detect any tampering or weaknesses.
3. Employ continuous monitoring and anomaly detection mechanisms to quickly identify and address any unauthorized changes in cryptographic operations.

For detailed advice on how to mitigate threats related to the card, see the [ASVS and OWASP Developer Guide requirements ](#mapping 'ASVS and OWASP Developer Guide requirements [internal]') in the table below.
