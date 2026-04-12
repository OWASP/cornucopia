## Scenario: Nathan's Client-Side Authorization Bypass

Nathan modifies frontend JavaScript to remove or disable authorization checks enforced only in the browser, gaining access to restricted features and data without the server ever rejecting his requests. This occurs because:

1. **Authorization enforced in the browser:** Visibility of UI elements, route guards, or feature flags are controlled purely by client-side logic — JavaScript conditions that determine what the user is allowed to see and do.

2. **Backend routes not independently protected:** API endpoints that back restricted features are accessible without a valid session role or permission check on the server, trusting the frontend to have already enforced access control.

### Example

An HR application has an admin panel linked only from the navigation for users with the `admin` role. The route guard is a JavaScript condition: `if (user.role === 'admin') { showAdminPanel(); }`. Nathan, a regular employee, opens the browser console, types `user.role = 'admin'` to overwrite the in-memory state, and navigates to the admin route. The frontend renders the full admin interface. Because the underlying API endpoints do not verify the user's role server-side, Nathan can retrieve all employee records, modify salaries, and deactivate accounts — operations the application was designed to restrict to administrators.

## Threat Modeling

### STRIDE

The scenario maps directly to STRIDE: **Elevation of Privilege**.

Nathan gains capabilities and access to data that are explicitly restricted to users with higher permissions. The attack requires no exploitation of a server vulnerability — he simply overrides the client-side checks that were never designed to be a security boundary.

### What can go wrong?

When authorization is enforced only in the browser, any user with developer tools — which is every user — can escalate their own privileges. This can expose administrative functions, other users' data, premium features, or internal tooling to anyone willing to open a console. Because the server processes the requests normally, the access often leaves no anomalous audit trail.

### What are we going to do about it?

Move all authorization decisions to the server and treat client-side controls as presentation-only.

1. Enforce every permission check on the server side for every API call — the backend must independently verify that the authenticated user has the right role or permission for the requested operation.
2. Do not rely on hidden routes, hidden UI elements, or client-side role checks as access control mechanisms; a user who knows an endpoint URL can reach it regardless of what the frontend renders.
3. Apply the principle of least privilege to API design: return only data the caller is entitled to see, rather than filtering a full response in the frontend.