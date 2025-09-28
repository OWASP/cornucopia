## Scenario: Andrew’s Access to Source Code and Business Logic

Picture a scenario where Andrew gains access to an application’s source code or decompiles it, thereby understanding its business logic and uncovering any embedded secrets. This occurs due to:

1. **Insecure Source Code Storage:** The source code is stored in locations that are not adequately secured.
2. **Lack of Obfuscation in Compiled Code:** The compiled code of the application is easily decompiled, revealing the business logic.
3. **Embedded Secrets in Code:** Sensitive information like passwords, encryption keys, or API keys is hard-coded into the application’s source code.

### Example

Andrew targets a commercial software application used by many businesses. He accesses the application’s source code, which was inadvertently exposed in a publicly accessible repository. Andrew also decompiles the application’s executable files, which lack sufficient obfuscation, gaining a deep understanding of the application’s internal workings. He discovers embedded secrets, such as database credentials and API keys, within the source code, which he then exploits to gain unauthorized access to associated systems and data.

## Threat Modeling

### STRIDE

The applicable STRIDE category here is primarily **Information Disclosure**.

Andrew is gaining access to sensitive information (source code, embedded secrets, business logic) that he is not authorized to see.
STRIDE’s **Information Disclosure** covers scenarios where an attacker learns secrets or confidential information without proper authorization.
Accessing or decompiling source code, and uncovering embedded credentials or business logic, constitutes unauthorized exposure of sensitive data, which is exactly what I**nformation Disclosure** describes.

### What can go Wrong?

Such exposure of source code and business logic can lead to unauthorized access, intellectual property theft, and exploitation of hidden vulnerabilities or secrets within the application.

For more things that can go wrong, see the [Common Attack Patterns related to this card](#mapping 'Common Attack Patterns related to this card [internal]') in the table below.

### What are you going to do about it?

1. Securely store source code in access-controlled repositories and limit distribution of compiled code.
2. Implement code obfuscation techniques to prevent easy decompilation and understanding of business logic in distributed binaries. 
3. Avoid embedding secrets in the source code. Instead, use secure methods for managing and accessing credentials and keys.
4. Conduct regular security reviews and audits of source code management practices

For detailed advice on how to mitigate threats related to the card, see the [ASVS and OWASP Developer Guide requirements ](#mapping 'ASVS and OWASP Developer Guide requirements [internal]') in the table below.
