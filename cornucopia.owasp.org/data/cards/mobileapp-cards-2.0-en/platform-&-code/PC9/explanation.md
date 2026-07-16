## Scenario: Toby can modify or expose data by injection because the response from implicit intents is not properly validated

Consider a scenario where Toby has registered a malicious "Fast PDF Viewer" app on the same device as the target app. The target app sends an implicit `ACTION_VIEW` intent to open a PDF receipt, and reads the result Uri from `Activity.onActivityResult`. Toby's app appears in the app chooser. The user selects it. Toby's app returns a crafted file Uri pointing to the target app's private database. The target app opens that path without validation. Toby receives a copy of the database through what the developer called a "standard document-open flow."

1. Implicit intents resolved to untrusted apps can return crafted results.
2. The originating app trusts returned data without validating its source or content.

### Example

Toby's "Fast PDF Viewer" has a 2.9-star rating but enthusiastic behind-the-scenes features. When selected by the user for "open receipt," it returns `file:///data/data/com.target.app/databases/main.db` as the result data URI. The target app's file parser opens that path. Toby's app receives the database content via a side-channel file watcher it registered before the intent was sent. The attack was invisible to the user, who just wanted to view a PDF.

## Threat Modeling

### STRIDE

This scenario falls under **Tampering** and **Information Disclosure**.

A malicious app intercepts the implicit intent resolution and returns malicious data to the calling app, which processes it without validation — a confused-deputy attack at the Android intent level.

### What can go wrong?

- Returned file paths are traversed to access private app storage.
- Returned data is deserialized or parsed without sanitization, enabling further injection.
- Auth tokens or nonces in result extras are captured and replayed by the intercepting app.

### What are we going to do about it?

- Prefer explicit intents (specifying the target component) for sensitive document operations.
- For system-provided pickers (file, photo, contact), use `ActivityResultContracts` — system-provided choosers reduce third-party interception risk.
- Validate the scheme of any returned Uri: accept only `content://` from known authorities; reject `file://` from untrusted sources.
- Canonicalize returned file paths and confirm they do not escape the expected directory.
- For OAuth/PKCE redirects, use App Links (domain-verified) rather than custom URL schemes.
