## Scenario: Christopher’s Command Injection with Elevated Privileges

Imagine a situation where Christopher, exploiting system vulnerabilities, injects commands that the application executes at a higher privilege level. This occurs due to:

1. **Elevated Privilege Execution:** The application lacks proper controls to restrict command execution based on the user's privilege level.

2. **Inadequate Command Filtering:** Insufficient validation and filtering of user-submitted commands allow for execution of unauthorized commands.

### Example

Christopher targets a web application with a feature that allows users to input commands for data retrieval. He discovers that this feature does not adequately validate or sanitize input, nor does it check the privilege level at which commands are executed. Exploiting this, he injects a command intended for administrative functions. The system, failing to restrict command execution based on user privileges, runs the command at an administrative level, allowing Christopher unauthorized access to sensitive system operations and data.

## Threat Modeling

### STRIDE

This scenario maps primarily to STRIDE: **Elevation of Privilege** (EoP).

**Elevation of Privilege** occurs when an attacker performs actions or executes commands beyond their authorized privileges.
Christopher injects a command that the system executes at a higher privilege level than his own user role, gaining unauthorized administrative access.
The attack exploits lack of privilege checks combined with command injection, allowing him to perform higher-privilege operations.

### What can go Wrong?

Such vulnerabilities can lead to unauthorized system access, data breaches, and potential control over critical system functionalities.

### What are you going to do about it?

1. Implement strict input validation and sanitization to prevent command injection attacks.
2. Ensure that all commands are executed only at the appropriate privilege level, preventing users from executing commands with elevated privileges.
3. Regularly review and update security protocols to safeguard against command injections and unauthorized privilege escalation.

For detailed advice on how to mitigate threats related to the card, see the [ASVS and OWASP Developer Guide requirements ](#mapping 'ASVS and OWASP Developer Guide requirements [internal]') in the table below.
