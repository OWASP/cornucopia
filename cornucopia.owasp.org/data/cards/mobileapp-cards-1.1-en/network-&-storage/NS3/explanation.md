## Scenario: Bil can access sensitive data for sensitive fields from the pasteboard/clipboard or keyboard cache because the pasteboard/clipboard is not timely cleared, disabled or restricted for sensitive fields, or the keyboard cache is not disabled

The mobile application allows sensitive information such as passwords, tokens, or personal data to be copied to the clipboard or stored in the keyboard cache. The clipboard is not cleared after use, and keyboard caching is not restricted for sensitive fields.

As a result, Bil can access this sensitive data through the clipboard or cached keyboard suggestions.

### Example

Bil installs another application that monitors clipboard content. After a user copies a password or authentication token from the mobile app, the clipboard data remains available. Bil retrieves the sensitive information from the clipboard history or keyboard cache.

## Threat Modeling

### STRIDE

This scenario falls under the **Information Disclosure** category of the STRIDE threat modeling framework.

Sensitive information is exposed because clipboard and keyboard caching mechanisms are not properly restricted.

### What can go wrong?

- Passwords or authentication tokens may be exposed.
- Personal or financial information may be leaked.
- Other applications may access clipboard data.

### What are we going to do about it?

- Disable clipboard access for sensitive fields when possible.
- Clear clipboard data after sensitive operations.
- Disable keyboard caching for password and sensitive input fields.
- Use secure input flags provided by the platform.