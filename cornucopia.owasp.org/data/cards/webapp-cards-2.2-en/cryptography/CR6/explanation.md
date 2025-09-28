## Scenario: Romain's Access to Unencrypted Data in Memory and Transit

Picture a scenario where Romain accesses and modifies unencrypted data, either in memory or in transit. This situation arises due to:

1. **Unencrypted Data in Memory:** Sensitive data like cryptographic secrets, credentials, and session identifiers are stored unencrypted in system memory.

2. **Data Exposed in Communication:** Personal and commercially-sensitive data is transmitted without encryption, either within the application or in interactions with external systems.

### Example

Romain targets an application that handles sensitive user data but fails to encrypt this data while in use or during internal processing. He exploits this by accessing the application’s memory, where he finds unencrypted credentials and session identifiers. Additionally, Romain intercepts data being transmitted between the application and external systems, such as payment gateways, as it is sent without proper encryption, allowing him to read and modify sensitive information during transit.

## Threat Modeling

### STRIDE

Romain can both read and modify sensitive unencrypted data. That means two STRIDE categories are in play, depending on which impact you emphasize:

1. **Information Disclosure**: because he can read cryptographic secrets, credentials, and personal/commercially-sensitive data in memory or in transit.
2. **Tampering** because he can modify unencrypted data (e.g., session identifiers, payment details) in memory or on the wire.

### What can go Wrong?

This vulnerability can lead to unauthorized access to sensitive data, data breaches, and potential manipulation of critical information.

For more things that can go wrong, see the [Common Attack Patterns related to this card](#mapping 'Common Attack Patterns related to this card [internal]') in the table below.

### What are you going to do about it?

1. Implement encryption for sensitive data while it is in memory and during processing within the application.
2. Ensure that all data communications, both internal and external, are secured with robust encryption methods.
3. Regularly review and update encryption practices to cover data in use, in transit, and during communications with external systems.

For detailed advice on how to mitigate threats related to the card, see the [ASVS and OWASP Developer Guide requirements ](#mapping 'ASVS and OWASP Developer Guide requirements [internal]') in the table below.
