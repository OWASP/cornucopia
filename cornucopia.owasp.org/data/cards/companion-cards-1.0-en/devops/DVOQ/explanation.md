## Scenario: Seba's Discovery of Exposed Secrets

Consider a scenario where Seba gains access to secrets and other sensitive information by finding them in places where they should not be stored or exposed. Secrets can end up somewhere they shouldn't through many different paths: committed to version control, printed in pipeline or application logs, left in command line history, included in error messages, bundled into artifacts, or stored in any number of other places that are accessible to more people than intended.

### Example

Seba browses the code repository's commit history and finds that a database credential was committed in an early version of a configuration file. Although it was later removed, the credential is still visible in the repository's history. Seba also discovers that the CI pipeline logs include environment variables printed during debug output, exposing API keys for internal services. With these credentials, Seba accesses systems far beyond what his role would normally allow.

## Threat Modeling

### STRIDE

This scenario maps primarily to STRIDE: **Information Disclosure**.

**Information Disclosure** occurs when sensitive data is exposed to unauthorized parties. Seba does not need to break any access control, as the secrets are simply available in places he can already access, such as the repository history, log files, or pipeline outputs. The core issue is the improper handling and storage of sensitive information.

### What can go wrong?

Exposed secrets provide direct access to protected systems and data, often with significant privileges. This can manifest in various forms, including but not limited to:

- Credentials committed to version control, recoverable from repository history even after deletion
- API keys and tokens logged in pipeline outputs or application logs
- Secrets left in command line history on shared or persistent build environments
- Broad access gained through a single exposed credential that grants access to multiple systems
- Difficulty revoking compromised secrets when their scope and usage are unclear

### What are we going to do about it?

1. Use a secrets management solution to store and inject secrets at runtime, instead of putting them in code or configuration files.
2. Set up pre-commit hooks or automated scanning to catch secrets before they are committed to version control.
3. Make sure pipeline logs and outputs do not print unmasked secrets - disable debug logging in production pipelines and mask any sensitive values in the output.
4. If a secret has been exposed, even briefly, rotate it immediately. Don't assume nobody saw it.
5. Check your repository history for previously committed and unrotated secrets. Removing a secret in a later commit does not remove it from the history.
6. Make sure build and deployment environments do not persist command line history or other artifacts that may contain secrets.
7. Keep the scope and lifetime of credentials and tokens as small as possible, so a leaked secret gives an attacker less to work with. Use ephemeral tokens where possible if your CI/CD platform supports them.

