## Scenario: Lauren can traverse or modify otherwise protected files through access to the underlying file system by exploiting weaknesses in file system-based content providers, resolvers, or their configuration

Consider a scenario where Lauren discovers the target app's `FileProvider` is configured with `<files-path path="." />`, which exposes the entire internal files directory. She crafts an intent requesting `../databases/main.db` — a path traversal — and the provider resolves it to the app's private SQLite database. Lauren receives a copy of every user record without ever needing elevated OS privileges.

1. A `FileProvider` with an overly broad path configuration serves more of the filesystem than intended.
2. Apps that accept file paths from external sources without canonicalization and boundary checking are vulnerable to `../` directory traversal.
3. On iOS, apps that process file URLs from URL scheme handlers or document pickers without validating the resolved path can serve files outside the intended sandbox.

### Example

Lauren builds a malicious companion app and sends an intent with `content://com.target.app.fileprovider/../shared_prefs/auth.xml`. The target app's provider resolves the relative path and returns the XML file containing the stored authentication token. Lauren's app captures it, logs in as the victim, and changes the account email to lock the owner out. The entire attack was conducted without touching a network vulnerability.

## Threat Modeling

### STRIDE

This scenario falls under **Information Disclosure** and **Tampering**.

A path traversal allows an attacker to read files outside the intended scope (disclosure) and potentially overwrite files with attacker-controlled content (tampering), remaining entirely within the app's IPC surface.

### What can go wrong?

- Private databases, shared preferences, and credentials are read by unauthorised apps.
- Config files or cached session tokens are overwritten with attacker-controlled content.
- Files containing PII are exfiltrated silently in the background.

### What are we going to do about it?

- Restrict `FileProvider` path configurations to the minimum necessary subdirectory (e.g., `<files-path path="shared/" />`).
- Canonicalize any user-supplied or IPC-supplied file path before use; verify it starts with the expected base directory.
- Do not expose internal `databases/` or `shared_prefs/` directories through any provider.
- On iOS, resolve paths with `URL.resolvingSymlinksInPath` and verify the result starts with the expected container path.
- Reject any input containing `..` or absolute path components before performing any file operation.
