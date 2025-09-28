## Scenario: Sebastien’s Username Enumeration

Visualize a scenario where Sebastien, using simple techniques, can easily identify or enumerate user names in a system. This can occur due to:

1. **Predictable Usernames:** The system uses easily guessable or standard formats for usernames.

2. **Informative Error Messages:** Error messages on login pages reveal whether a username exists or not.

3. **User Enumeration through Other Features:** Features like 'Forgot Password' or 'Sign Up' inadvertently confirm the existence of specific usernames.

### Example

Sebastien enumerates the usernames of a company by compiling a list of employees from publicly available sources such as LinkedIn. He then applies the general pattern " firstname.lastname'@'company.com " to generate potential email addresses, which are often used as usernames.  Setting the stage for further attacks like password guessing or phishing.

## Threat Modeling

### STRIDE

The scenario maps directly to STRIDE: **Information Disclosure**.

Sebastien is learning something the system should treat as sensitive: the set of valid usernames.
In STRIDE, **Information Disclosure** is about exposing data to unauthorized parties. Usernames are part of authentication secrets, and leaking or allowing enumeration discloses information attackers can weaponize.

### What can go Wrong?

Such vulnerabilities can lead to targeted attacks, including phishing, social engineering, and brute-force attacks, as attackers gain knowledge about valid user accounts.

For more things that can go wrong, see the [Common Attack Patterns related to this card](#mapping 'Common Attack Patterns related to this card [internal]') in the table below.

### What are you going to do about it?

1. Avoid using predictable username formats. Encourage or enforce more complex and less guessable usernames.
2. Design error messages to be non-revealing, providing the same response regardless of whether the username exists or not.
3. Implement measures to prevent enumeration through account-related features, ensuring they do not disclose information about the existence of usernames.

For detailed advice on how to mitigate threats related to the card, see the [ASVS and OWASP Developer Guide requirements ](#mapping 'ASVS and OWASP Developer Guide requirements [internal]') in the table below.
