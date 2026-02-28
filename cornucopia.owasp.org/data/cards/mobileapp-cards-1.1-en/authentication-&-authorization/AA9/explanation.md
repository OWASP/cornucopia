## Scenario: Wong can bypass the authentication because it does not fail securely (i.e. it defaults to allowing unauthenticated access)

Wong discovers that the mobile application does not properly handle authentication failures. When authentication checks fail due to unexpected errors, network issues, or misconfigurations, the application defaults to granting access instead of denying it.

Instead of enforcing a strict “deny by default” principle, the system allows Wong to access protected resources when authentication validation cannot be completed successfully.

### Example

Wong attempts to access a restricted section of the app while offline. The app tries to validate his session token against a remote endpoint. Due to a timeout or exception in the authentication handler, the validation process fails.

Rather than blocking access, the app assumes the session is valid and allows Wong into the application.

In another case, an internal error in role validation causes the authorization logic to skip verification steps. Because the system does not explicitly deny access on failure, Wong gains unintended access to administrative functionality.

## Threat Modeling

### STRIDE

This scenario falls under the Spoofing category of the STRIDE threat modeling framework.

By failing to enforce secure authentication checks and defaulting to permissive behavior during errors, the system enables Wong to gain unauthorized access.

### What can go wrong?

If authentication or authorization logic fails open instead of failing closed:

- Unauthenticated users may gain access to protected resources.
- Privileged operations may become accessible without proper verification.
- Sensitive data may be exposed.
- Attackers may intentionally trigger error conditions to bypass security checks.

Fail-open logic significantly weakens the security boundary of the application and can lead to data breaches.

### What are we going to do about it?

- Enforce a strict “deny by default” policy for all authentication and authorization checks.
- Ensure that any exception, timeout, or validation failure results in access being denied.
- Implement robust error handling that does not bypass security controls.
- Add server-side validation to prevent client-side logic manipulation.
- Include automated tests to verify that authentication failures always result in access denial.