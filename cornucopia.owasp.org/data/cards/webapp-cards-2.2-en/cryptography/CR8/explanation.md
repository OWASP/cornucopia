## Scenario: Eoin's Access to Unsecured Stored Business Data

Imagine a situation where Eoin gains access to unsecured stored business data, such as passwords, session identifiers, personally identifiable information (PII), and cardholder data. This vulnerability arises due to:

1. **Lack of Secure Encryption:** The data is stored without adequate encryption, making it vulnerable to unauthorized access.

2. **Inadequate Hashing for Sensitive Data:** Critical data like passwords are not securely hashed, allowing them to be exposed in their original form.

### Example

Eoin discovers that an online retailer’s database stores user passwords and credit card details in plain text or with weak encryption. By exploiting a security flaw in the application, he accesses this database and retrieves this sensitive data. The lack of strong encryption or secure hashing of passwords and PII means that Eoin can easily use this information for malicious purposes, such as identity theft or financial fraud.

## Threat Modeling

### STRIDE

The applicable STRIDE category for this scenario is **Information Disclosure**.

The weakness is that sensitive stored data (passwords, session IDs, PII, cardholder data) is not encrypted or hashed securely, so when Eoin gains access, he can directly read it. That’s a confidentiality failure.
If what’s exposed are passwords or session identifiers, Eoin may go beyond just seeing them and actually log in or hijack accounts. That would then lead to **Elevation of Privilege**.

### What can go Wrong?

Storing sensitive business data without secure encryption or hashing can lead to severe data breaches, compromising user privacy and leading to potential financial and reputational damage.

### What are you going to do about it?

1. Implement robust encryption for sensitive data storage, ensuring that even if data is accessed, it remains unintelligible and secure.
2. Use secure hashing algorithms, particularly for storing passwords, to prevent them from being reverted to their original form.
3. Regularly review and update encryption and hashing methods to adhere to current best practices and standards.

For detailed advice on how to mitigate threats related to the card, see the [ASVS and OWASP Developer Guide requirements ](#mapping 'ASVS and OWASP Developer Guide requirements [internal]') in the table below.
