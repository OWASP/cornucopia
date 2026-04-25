## Scenario: Darius's Abuse of a JavaScript Application for Unauthorised System Control

Darius exploits a JavaScript application, such as an Electron desktop app, a feature-rich SPA with privileged APIs, or an internal admin tool — to perform administrative operations on systems, tenants, and user data that he should not be authorized to access. This occurs because:

1. **Privileged APIs exposed to the frontend:** The application exposes system-level capabilities — file system access, process execution, database administration, or cross-tenant management — through JavaScript APIs or backend endpoints that the frontend is permitted to call without adequate authorization checks.

2. **Administrative capabilities in a general-purpose application:** Features intended only for internal operators or privileged accounts are accessible through the same application used by all users, protected only by UI restrictions that can be bypassed.

### Example

Darius is a standard user of a SaaS platform with an Electron-based desktop application. He notices that the application communicates with an internal management API to display his account's usage statistics. Using developer tools, he inspects the network traffic and finds a `tenantId` parameter in the API request. He replaces his tenant's identifier with another tenant's ID and discovers that the API returns that tenant's user list, billing details, and configuration. He iterates through tenant identifiers and exports data for hundreds of organizations, all through the same JavaScript application legitimately installed on his machine.

## Threat Modeling

### STRIDE

The scenario maps directly to STRIDE: **Elevation of Privilege**.

Darius operates outside the boundaries of his authorized scope, performing actions and accessing data belonging to other users, tenants, or system resources. He uses the application's own legitimate communication channels — the threat is not a technical exploit of the application's code, but a failure to enforce the boundaries of what each user is permitted to control.

### What can go wrong?

When a JavaScript application's reach is not bounded by the authorization model enforced on every API call, a compromised or curious user can turn a personal account into an administrative tool. In multi-tenant systems, this can result in full cross-tenant data exposure, configuration manipulation, or account compromise at scale. In Electron or Node-based apps with file system or process access, the attack surface extends beyond the web API to the host operating system.

### What are we going to do about it?

Enforce strict authorization boundaries on every API call, treating the frontend as untrusted regardless of the application type.

1. Validate the caller's authorization for every operation on the server side, including cross-tenant access; never rely on the frontend to restrict which tenant IDs or resource identifiers a user submits.
2. Apply the principle of least privilege to the APIs exposed to the JavaScript client: users should only be able to reach operations relevant to their own account and role.