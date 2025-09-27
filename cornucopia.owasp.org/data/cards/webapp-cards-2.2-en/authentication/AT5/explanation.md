## Scenario: Javier’s Exploitation of Weak Credentials

Picture a scenario where Javier gains unauthorized access by exploiting weak or overlooked aspects of credential management. He capitalizes on:

1. **Default Credentials:** Using default usernames and passwords that haven’t been changed.

2. **Test Accounts:** Accessing accounts created for testing, which are often less secure.

3. **Guessable Credentials:** Exploiting simple or commonly used passwords.

4. **Old Accounts:** Utilizing accounts that are no longer active but haven’t been properly deactivated.

5. **Unnecessary Accounts:** Gaining access through accounts that exist but are not essential for the application's operation.

### Example

Javier targets a company’s web application that still has accounts with default credentials, such as "admin/admin." These accounts, often overlooked or forgotten, provide an easy entry point. He uses these credentials to log in, gaining the same level of access as a legitimate administrator, which he then uses to access sensitive data and system controls.

## Threat Modeling

### STRIDE

This scenario falls under STRIDE: **Spoofing**.

Spoofing is about pretending to be someone or something you’re not.
By logging in with default, test, old, or unnecessary accounts, Javier spoofs a legitimate user (or admin), but
if the default/test account has higher-than-normal rights (e.g., admin), Javier also escalates privileges making **Elevation of Privilege** a secondary impact.

### What can go Wrong?

Such vulnerabilities allow for unauthorized access and control, leading to potential data breaches, system manipulations, and other security risks.

### What are you going to do about it?

1. Ensure all default credentials are changed upon system setup or application installation.
2. Regularly audit accounts to identify and remove or secure test and unnecessary accounts.
3. Implement and enforce strong password policies, discouraging easily guessable passwords.
4. Routinely deactivate old accounts and monitor for any unauthorized access attempts

For detailed advice on how to mitigate threats related to the card, see the [ASVS and OWASP Developer Guide requirements ](#mapping 'ASVS and OWASP Developer Guide requirements [internal]') in the table below.
