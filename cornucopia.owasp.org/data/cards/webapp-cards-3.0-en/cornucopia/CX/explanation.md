## Scenario: Spyros’s Exploitation of Vulnerable Code Libraries and Frameworks

Imagine a situation where Spyros circumvents an application's controls by exploiting vulnerabilities or malicious code within its frameworks, libraries, and components. This can occur in various types of software, including:

1. **In-House Developed Software:** Custom code developed internally may contain vulnerabilities or insufficiently reviewed segments.

2. **Commercial Off-The-Shelf (COTS) Products:** Commercially available software might have undisclosed vulnerabilities.

3. **Outsourced Software Components:** Externally developed components may not adhere to strict security standards.

4. **Open Source Libraries:** Open source code might contain vulnerabilities or, in rare cases, malicious components.

5. **Externally-Located Code:** Software components hosted externally may be compromised or altered without the knowledge of the primary application developers.

### Example

Spyros identifies that a financial application uses a popular open-source library, which recently disclosed a vulnerability. However, the application’s developers have not yet updated the library to the patched version. Exploiting this known vulnerability, Spyros gains unauthorized access to the application, allowing him to manipulate transactions and access sensitive customer data. Additionally, Spyros finds that an outsourced module in the application contains poorly written code, which he exploits to bypass the application’s primary security controls.

## Threat Modeling

### STRIDE

The STRIDE category applicable here is **Tampering**.

The scenario describes circumventing application controls via vulnerable or malicious code in frameworks, libraries, or components.
The primary impact is that an attacker can modify, manipulate, or exploit the application’s behavior through weaknesses in these components.
The core issue in the context of vulnerable/malicious components is that the attacker can alter execution or manipulate application operations, which aligns with **Tampering**.

### What can go wrong?

The use of vulnerable or compromised software components can lead to significant security breaches, unauthorized data access, and potential system compromises.

For more things that can go wrong, see the [Common Attack Patterns related to this card](#mapping 'Common Attack Patterns related to this card [internal]') in the table below.

### What are we going to do about it?

1. Regularly update all frameworks, libraries, and components to their latest, secure versions.
2. Conduct thorough security reviews and vulnerability assessments of all in-house, outsourced, and open-source code used within the application.
3. Monitor security advisories for any components used within the application and respond swiftly to vulnerability disclosures.
4. Establish a robust security protocol for integrating and maintaining external software components.

For detailed advice on how to mitigate threats related to the card, see the [ASVS and OWASP Developer Guide requirements ](#mapping 'ASVS and OWASP Developer Guide requirements [internal]') in the table below.
