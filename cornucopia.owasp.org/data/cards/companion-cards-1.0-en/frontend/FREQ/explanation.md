## Scenario: Kim's Persistent Frontend Asset Injection

Kim injects malicious code into the application's deployed frontend assets (JavaScript bundles, HTML templates, or service worker scripts) so that every user who visits the application runs Kim's payload until the application is redeployed with clean assets. This occurs because:

1. **Insecure build or deployment pipeline:** The pipeline that compiles and publishes frontend assets can be accessed or influenced by Kim, for example through compromised CI credentials, a vulnerable build tool, or write access to the web server's file store.

2. **No integrity verification at serving time:** Deployed assets are served without a mechanism to detect that their contents have been altered after publication — there are no checksums verified at startup, and the CDN or web server applies no content integrity checks.

### Example

Kim compromises a CI/CD service account that has write access to the S3 bucket serving a retail application's JavaScript bundles. She appends a script to the main bundle that intercepts calls to the payment form submission handler and sends a copy of each card number, expiry date, and CVV to a server she controls. The modified bundle is served immediately to all users. Because the file is cached by a CDN with a long TTL, the malicious version reaches users for several days before the development team notices an anomaly in outbound traffic patterns and identifies the compromised file.

## Threat Modeling

### STRIDE

The scenario maps directly to STRIDE: **Tampering**.

Kim modifies the application's code at rest, altering what every user receives and executes. The integrity of the deployed application has been permanently compromised until the assets are replaced.

### What can go wrong?

Persistent code injection in frontend assets turns the application into a data harvester for every user who visits it during the affected period. Sensitive inputs — credentials, payment data, personal information — can be silently captured in bulk. Unlike reflected or DOM-based XSS, the payload does not require user interaction beyond visiting the application; it is delivered with the page itself to all users simultaneously.

### What are we going to do about it?

Protect the integrity of the deployment pipeline and the deployed assets themselves.

1. Apply the principle of least privilege to CI/CD credentials; build pipelines should have write access only to the specific artifacts they are responsible for, not to the full production asset store.
2. Generate and publish Subresource Integrity (SRI) hashes for all bundled assets at build time, and verify them at serve time or via a startup check.
3. Set short CDN cache TTLs on critical JavaScript files, or use cache-busting strategies, so that a compromised bundle can be invalidated quickly after detection.
