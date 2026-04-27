## Scenario: Lena's Post-Logout Data Exposure

Lena accesses sensitive information left behind in the browser after a user has logged out, because the application fails to clear it when the session ends. This occurs because:

1. **Data persisted in browser storage:** Sensitive content (user details, tokens, API responses) is stored in `localStorage`, `sessionStorage`, or IndexedDB and never cleared on logout.

2. **Cached API responses retained:** The browser's HTTP cache or a service worker cache holds authenticated responses that remain accessible after the session has ended.

### Example

A shared workstation at a hospital is used by multiple staff members throughout the day. A nurse logs into a patient portal, reviews records, and clicks the logout button before leaving the terminal. The application clears the session cookie but leaves the patient data it fetched in `localStorage` and does not clear the cached API responses. When the next staff member opens the browser and navigates to the application, JavaScript running on the landing page reads the residual data from storage and pre-populates the interface with the previous user's patient records — without any authentication step.

## Threat Modeling

### STRIDE

The scenario maps directly to STRIDE: **Information Disclosure**.

Sensitive data that should have been destroyed at the end of a session remains accessible to whoever uses the browser next. Lena does not need to break any authentication mechanism, the data is simply left in place. 

### What can go wrong?

Failure to clear session data exposes personally identifiable information, health records, financial details, or internal application state to subsequent users of the same browser. On shared or public devices, this becomes a straightforward data breach requiring no technical sophistication. Residual tokens may also allow session resumption long after the user believed they had logged out.

### What are we going to do about it?

Ensure that logout is a complete operation: authentication state, cached data, and persistent storage are all cleared.

1. On logout, explicitly clear all application-managed storage: `localStorage`, `sessionStorage`, IndexedDB entries, and any cookies set by the application.
2. Invalidate the session token server-side on logout, so that any residual token cannot be reused to re-authenticate.
3. Set appropriate `Cache-Control` headers (`no-store`) on API responses that return sensitive data, so the browser does not cache them.