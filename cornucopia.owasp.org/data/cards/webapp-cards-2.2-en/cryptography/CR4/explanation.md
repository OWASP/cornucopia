## Scenario: Paulo's Access to Unencrypted Data on Encrypted Channels

Imagine a scenario where Paulo accesses data in transit, even though it's being sent over an encrypted channel. This situation occurs because:

1. **Data Not Encrypted Independently:** The actual data being transmitted is not encrypted by itself, relying solely on the encryption of the communication channel.

2. **Channel Encryption Inadequacy:** While the channel (like an HTTPS connection) is encrypted, the data could be exposed at endpoints or if there’s a breach in the channel encryption.

### Example

Paulo targets a system that uses HTTPS for secure communication. However, the data sent over this channel, such as user credentials or financial information, is not encrypted independently. Paulo manages to exploit vulnerabilities at the endpoints of the communication, where data is decrypted. He gains access to this sensitive information as it is processed or stored unencrypted, despite the secure transmission channel.

## Threat Modeling

### STRIDE

The applicable STRIDE category for this scenario is **Information Disclosure**.

Paulo is able to access sensitive data (credentials, financial information) because it is not properly protected, even though the transport channel is encrypted.
The core threat is exposure of confidential information — he is reading data he should not be able to see.

### What can go wrong?

Data may use encryption in transit like Transport Layer Security (TLS). However, an attacker may have legitimate access to this (e.g. viewing SSL content in a web browser).

This vulnerability can lead to data exposure and breaches, especially if endpoint security is compromised or if there are gaps in the transmission channel’s encryption.

For more things that can go wrong, see the [Common Attack Patterns related to this card](#mapping 'Common Attack Patterns related to this card [internal]') in the table below.

### What are you going to do about it?

1. Consider whether the data transmitted also needs to be encrypted itself, not just sent using an encrypted protocol. Ensure that sensitive data is encrypted independently before it is sent over the communication channel.
2. Maintain robust endpoint security to protect data when it is encrypted or decrypted.
3. Regularly review and strengthen both data and channel encryption practices to cover potential vulnerabilities.

For detailed advice on how to mitigate threats related to the card, see the [ASVS and OWASP Developer Guide requirements ](#mapping 'ASVS and OWASP Developer Guide requirements [internal]') in the table below.
