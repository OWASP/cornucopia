#  Password Security
## V2.1.1
Verify that user set passwords are at least 12 characters in length (after multiple spaces are combined). ([C6](https://owasp.org/www-project-proactive-controls/#div-numbering))
Level 1 required: True
Level 2 required: True
Level 3 required: True
CWE: [521](https://cwe.mitre.org/data/definitions/521)
## V2.1.2
Verify that passwords of at least 64 characters are permitted, and that passwords of more than 128 characters are denied. ([C6](https://owasp.org/www-project-proactive-controls/#div-numbering))
Level 1 required: True
Level 2 required: True
Level 3 required: True
CWE: [521](https://cwe.mitre.org/data/definitions/521)
## V2.1.3
Verify that password truncation is not performed. However, consecutive multiple spaces may be replaced by a single space. ([C6](https://owasp.org/www-project-proactive-controls/#div-numbering))
Level 1 required: True
Level 2 required: True
Level 3 required: True
CWE: [521](https://cwe.mitre.org/data/definitions/521)
## V2.1.4
Verify that any printable Unicode character, including language neutral characters such as spaces and Emojis are permitted in passwords.
Level 1 required: True
Level 2 required: True
Level 3 required: True
CWE: [521](https://cwe.mitre.org/data/definitions/521)
## V2.1.5
Verify users can change their password.
Level 1 required: True
Level 2 required: True
Level 3 required: True
CWE: [620](https://cwe.mitre.org/data/definitions/620)
## V2.1.6
Verify that password change functionality requires the user's current and new password.
Level 1 required: True
Level 2 required: True
Level 3 required: True
CWE: [620](https://cwe.mitre.org/data/definitions/620)
## V2.1.7
Verify that passwords submitted during account registration, login, and password change are checked against a set of breached passwords either locally (such as the top 1,000 or 10,000 most common passwords which match the system's password policy) or using an external API. If using an API a zero knowledge proof or other mechanism should be used to ensure that the plain text password is not sent or used in verifying the breach status of the password. If the password is breached, the application must require the user to set a new non-breached password. ([C6](https://owasp.org/www-project-proactive-controls/#div-numbering))
Level 1 required: True
Level 2 required: True
Level 3 required: True
CWE: [521](https://cwe.mitre.org/data/definitions/521)
## V2.1.8
Verify that a password strength meter is provided to help users set a stronger password.
Level 1 required: True
Level 2 required: True
Level 3 required: True
CWE: [521](https://cwe.mitre.org/data/definitions/521)
## V2.1.9
Verify that there are no password composition rules limiting the type of characters permitted. There should be no requirement for upper or lower case or numbers or special characters. ([C6](https://owasp.org/www-project-proactive-controls/#div-numbering))
Level 1 required: True
Level 2 required: True
Level 3 required: True
CWE: [521](https://cwe.mitre.org/data/definitions/521)
## V2.1.10
Verify that there are no periodic credential rotation or password history requirements.
Level 1 required: True
Level 2 required: True
Level 3 required: True
CWE: [263](https://cwe.mitre.org/data/definitions/263)
## V2.1.11
Verify that "paste" functionality, browser password helpers, and external password managers are permitted.
Level 1 required: True
Level 2 required: True
Level 3 required: True
CWE: [521](https://cwe.mitre.org/data/definitions/521)
## V2.1.12
Verify that the user can choose to either temporarily view the entire masked password, or temporarily view the last typed character of the password on platforms that do not have this as built-in functionality.
Level 1 required: True
Level 2 required: True
Level 3 required: True
CWE: [521](https://cwe.mitre.org/data/definitions/521)

## Disclaimer:
Credit via [OWASP ASVS](https://owasp.org/www-project-application-security-verification-standard/). For more information visit [The OWASP ASVS Project](https://owasp.org/www-project-application-security-verification-standard/) or [Github respository.](https://github.com/OWASP/ASVS). OWASP ASVS is under the [Creative Commons Attribution-Share Alike v3.0](https://creativecommons.org/licenses/by-sa/3.0/) license.
