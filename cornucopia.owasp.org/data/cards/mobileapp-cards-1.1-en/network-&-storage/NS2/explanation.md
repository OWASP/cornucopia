## Scenario: Matt can inspect sensitive application log data because logging statements have not been removed or reviewed as safe before the production release

The mobile application contains verbose logging statements that expose sensitive information such as authentication tokens, personal data, or internal system details. These logs were intended for debugging but were not removed or reviewed before the production release.

As a result, Matt can access application logs and extract confidential information.

### Example

Matt connects his device to a debugging tool and reviews the application logs. He discovers that login responses and API tokens are written to the log output, allowing him to retrieve sensitive data.

## Threat Modeling

### STRIDE

This scenario falls under the **Information Disclosure** category of the STRIDE threat modeling framework.

Sensitive information is unintentionally exposed through insecure logging practices.

### What can go wrong?

- Sensitive user data may be exposed.
- Authentication tokens may be leaked.
- Internal system details may be disclosed.

### What are we going to do about it?

- Remove or disable debug logging in production builds.
- Avoid logging sensitive information such as passwords, tokens, or personal data.
- Review logging statements before releasing the application.
