## Scenario: Prasad can bypass the centralized authentication and authorization controls because they are not being used comprehensively on all interactions

Consider a scenario where Prasad finds the app has a centralized `AuthManager` class used on most screens — but not on a recently added "quick share" feature added by a new developer who was unfamiliar with the codebase. The quick-share feature accesses user data directly without calling `AuthManager.requireAuthentication()`. Prasad deep-links directly into the quick-share screen. He accesses the user's shared data without any authentication.

1. Centralized auth controls not applied to all code paths leave gaps that bypass all security.
2. New features added under time pressure may skip the standard auth gate.
3. API endpoints added to support a new feature may not be protected by the same middleware that protects existing endpoints.

### Example

Prasad reviews the app's deep-link manifest and finds `appscheme://quickshare?id=12345`. He opens the link and the quick-share screen appears with the user's full name, profile picture, and shared content — all without an authentication prompt. The `AuthManager` class is comprehensive and well-written. It is just not called from this particular activity. The gap is not in the control; it is in its coverage.

## Threat Modeling

### STRIDE

This scenario falls under **Spoofing** and **Elevation of Privilege**.

Inconsistent application of centralized auth controls means an attacker can find and exploit the gaps — gaining access equivalent to an authenticated user by navigating to an unprotected entry point.

### What can go wrong?

- Unprotected entry points (activities, API endpoints, deep links) expose data or functionality without authentication.
- The gap may not be immediately apparent in code review because the auth control exists and is used elsewhere.
- API endpoints for new mobile features added without the standard auth middleware pass all existing integration tests but fail in production when a malicious caller probes them directly.

### What are we going to do about it?

- Implement authentication as middleware that is applied globally by default; individual screens/endpoints must explicitly opt out (with documentation), not opt in.
- Use code review checklists and automated linting rules to flag any Activity, Fragment, or API handler that does not invoke the auth gate.
- Apply the same authentication and authorization controls to deep-linked entry points as to normal navigation paths.
- Conduct regular access-control audits across all entry points, including new features added since the last review.
