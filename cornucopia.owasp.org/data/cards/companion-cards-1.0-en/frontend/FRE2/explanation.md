## Scenario: Marcus's Client-Side Validation Bypass

Marcus sends malformed or malicious input directly to backend APIs, bypassing all validation logic that exists only in the browser. This occurs because:

1. **Validation enforced only in the browser:** Input constraints — required fields, length limits, format checks — are implemented exclusively in client-side JavaScript or HTML attributes, with no equivalent checks on the server.

2. **Implicit trust in client data:** The backend treats data received from the client as trustworthy, processing it without re-validating its structure, type, or range.

### Example

Marcus registers on a financial web application that enforces a minimum deposit of $10 through a client-side JavaScript check. Using a browser proxy tool, he intercepts the API request and replaces the deposit amount with `-9999`. Because the backend processes the value without validating it server-side, Marcus's account is credited rather than debited. He exploits the same pattern to manipulate quantities, order totals, and account tiers, triggering business logic flaws the development team had no idea were reachable.

## Threat Modeling

### STRIDE

The scenario maps directly to STRIDE: **Tampering**.

Marcus modifies data in transit, bypassing the integrity controls that the application's input validation is supposed to enforce. The backend receives values that were never intended to be valid, allowing Marcus to manipulate application state in ways that violate business rules.

### What can go wrong?

When validation is treated as a presentation concern rather than a security boundary, any attacker with a proxy tool can reach the backend with arbitrary input. This can lead to business logic abuse, corrupted application state, injection attacks that client-side sanitization was meant to prevent, and exploitation of assumptions baked into the server-side code. The impact ranges from minor data inconsistencies to financial fraud or full application compromise.

### What are we going to do about it?

Treat client-side validation as a usability feature, not a security control. All enforcement must happen on the server.

1. Re-implement every validation rule on the server side regardless of what the client enforces.
2. Reject unexpected fields and values at the API boundary; use an allowlist of accepted inputs rather than a blocklist of bad ones.
3. Return meaningful, structured error responses for invalid input so that legitimate clients can surface problems to users without leaking internals.
4. Apply content-type validation and schema enforcement (e.g., JSON Schema, OpenAPI) to all incoming request bodies.