## Scenario: Riotaro can inject and run a command that the application will run at a higher privilege level without being authenticated or authorized to do so

Consider a scenario where Riotaro discovers the app's "run diagnostic" deep link handler constructs a shell command by concatenating a user-supplied device ID parameter and passes it to `Runtime.exec()`. Riotaro sends `device_id=abc; am broadcast -a com.target.app.PRIVILEGED_ACTION`. The app executes the full concatenated string. The broadcast triggers a privileged internal action — without Riotaro being authenticated.

1. Command injection via IPC inputs: unvalidated parameters are incorporated into OS commands or privileged function calls.
2. An unauthenticated IPC entry point that invokes a privileged function effectively grants any caller the app's privilege level.

### Example

Riotaro finds `appscheme://diagnostic?cmd=network`. The app calls `Runtime.exec("diagnose_network")` with the parameter appended. He sends `cmd=network%3Bam+start+com.target.app/.AdminActivity`. The semicolon splits the command; the second command launches the admin activity without authentication. The diagnostic feature was only intended for internal QA. It shipped in the production APK.

## Threat Modeling

### STRIDE

This scenario falls under **Elevation of Privilege**.

Riotaro executes commands at the privilege level of the application process without satisfying any authentication or authorization requirement — the textbook definition of privilege escalation.

### What can go wrong?

- Arbitrary commands are executed in the app's process context.
- Privileged internal activities, services, or broadcasts are invoked without authentication.
- In extreme cases (root or setuid binaries involved), OS-level privilege escalation may be possible.

### What are we going to do about it?

- Never construct OS commands or privileged function calls from user-supplied or IPC-supplied input; use allowlists for any dynamic command parameters.
- Remove debug and diagnostic endpoints from production builds; use build variants to exclude them.
- Apply authentication and authorization checks at the entry point of every IPC handler, even for "internal" features.
- Replace `Runtime.exec()` with typed, parameterized APIs wherever possible to eliminate injection surfaces.
