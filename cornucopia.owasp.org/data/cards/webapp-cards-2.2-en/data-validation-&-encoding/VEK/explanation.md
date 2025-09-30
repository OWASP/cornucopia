## Scenario: Gabe’s Server-Side Interpreter Exploits

Imagine a scenario where Gabe takes advantage of weaknesses in server-side data processing. He injects malicious data into server-side interpreters like SQL, OS commands, XPath, Server JavaScript, SMTP, etc. This occurs because:

1. **Lack of Strongly Typed Parameterized Interfaces:** The system either doesn’t use strongly typed parameterized interfaces, or they are implemented incorrectly.

### Example

Gabe targets a web application's database interaction. He enters a specially crafted input into a search field, such as ' OR '1'='1. Due to the lack of a strongly typed parameterized query interface, this input is directly included in a SQL query. This results in a SQL injection, where Gabe manipulates the query to return all records or even modify database contents.

## Threat Modeling

### STRIDE

Gabe is injecting data that changes how the server processes queries/commands — turning data into action. That is an integrity attack: unauthorized modification of application behavior or data, which maps to **Tampering** in STRIDE.
The injection itself modifies the server-side processing pipeline (SQL engine, OS shell, XPath processor, etc.), so the root threat is tampering with inputs/processing, but all of the other STRIDE categories can be used for the secondary impact depending on the context.

### What can go wrong?

Such vulnerabilities can lead to severe consequences, including unauthorized data access, manipulation of server-side operations, and potentially full system compromise.

Due a failure of server-side input or output validation, encoding or sanitization, malicious code can be injected and treated as code rather than data, leading to code execution in the server application.

For more things that can go wrong, see the [Common Attack Patterns related to this card](#mapping 'Common Attack Patterns related to this card [internal]') in the table below.

### What are you going to do about it?

1. Implement and rigorously enforce the use of strongly typed parameterized interfaces for all server-side data processing.
2. Regularly review and test these implementations to ensure they handle data inputs securely and prevent injection attacks.

For detailed advice on how to mitigate threats related to the card, see the [ASVS and OWASP Developer Guide requirements ](#mapping 'ASVS and OWASP Developer Guide requirements [internal]') in the table below.
