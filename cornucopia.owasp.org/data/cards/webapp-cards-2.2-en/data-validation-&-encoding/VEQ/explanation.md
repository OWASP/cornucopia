## Scenario: Xavier’s Client-Side Injection

Visualize a scenario where Xavier capitalizes on vulnerabilities in client-side data handling. He injects malicious data into a client or device side interpreter, exploiting several key oversights:

1. **Non-use or Incorrect Implementation of Parameterized Interfaces:** The system either doesn’t use parameterized interfaces for data inputs or implements them incorrectly.

2. **Improper Data Encoding for Context:** Data is not encoded correctly based on the context in which it is used.

3. **Lack of Restrictive Policies on Code/Data Includes:** The system does not have strict policies governing the inclusion of code or data, allowing potentially harmful content.

### Example

Xavier attacks by injecting a script into a web application that lacks proper encoding and parameterization in its data handling. For instance, he enters a script in a text field that is expected to only contain plain text. Since the application does not correctly encode this input for the HTML context, the script is executed when loaded in a user’s browser, leading to a Cross-Site Scripting (XSS) attack.

## Threat Modeling

### STRIDE

Xavier is modifying the content/behavior of the application delivered to or executed on the client which is classic **tampering** of data/processing, but the impact can be multiple things (cookie theft → **Information Disclosure**; session takeover → **Elevation of Privilege**; forging UI → **Spoofing**), but the root threat is the attacker tampering with the interpreter’s inputs.

### What can go Wrong?

This type of vulnerability can lead to client-side attacks like XSS, compromising user data and browser security.

For more things that can go wrong, see the [Common Attack Patterns related to this card](#mapping 'Common Attack Patterns related to this card [internal]') in the table below.

### What are you going to do about it?

1. Ensure the use of parameterized interfaces for all data inputs and correctly implement them.
2. Apply proper data encoding techniques based on the specific context of use.
3. Establish and enforce restrictive policies for code and data inclusion to prevent malicious content injection.

For detailed advice on how to mitigate threats related to the card, see the [ASVS and OWASP Developer Guide requirements ](#mapping 'ASVS and OWASP Developer Guide requirements [internal]') in the table below.
