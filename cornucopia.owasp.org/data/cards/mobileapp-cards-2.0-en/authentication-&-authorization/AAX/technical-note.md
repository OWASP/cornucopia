## Platform-Aware Review Guidance

**Android**
- Define a base `AuthenticatedActivity` or `BaseFragment` that calls `AuthManager.requireAuthentication()` in `onResume`; all screens that require authentication should extend this base class.
- Apply automated lint checks (e.g., custom lint rules) to flag Activities and Fragments that do not extend `AuthenticatedActivity`.
- Audit all `<activity>` deep-link intent filters in the manifest; verify each destination performs an authentication check.

**iOS**
- Use a root `AuthenticatedViewController` or a SwiftUI `View` modifier that enforces authentication on appearance; apply it uniformly.
- Audit the `SceneDelegate`/`AppDelegate` URL handler for every deep-link path to verify authentication is checked before the destination is loaded.
- Centralise navigation in a router that enforces authentication before resolving any route.

**Server-Side**
- Apply authentication middleware globally at the framework level; individual endpoints must opt out explicitly with auditor approval, not opt in silently.
- Scan API route definitions for missing middleware tags as part of CI.

**Testing**
- Enumerate all deep-link schemes and navigate to each without an active session; verify all prompt for authentication.
- Review every Activity, Fragment, and API endpoint for the presence of the auth gate call.

**OWASP Mappings**
- MASVS: AUTH-1, AUTH-2, CODE-3, CODE-4
- MASTG: TEST-0017, TEST-0064
- MASWE: MASWE-0032, MASWE-0033, MASWE-0038, MASWE-0042
