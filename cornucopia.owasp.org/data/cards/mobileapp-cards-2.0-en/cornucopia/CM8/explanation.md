## Scenario: Roxana can perform arbitrary file overwrites and potentially execute malicious code through path traversal because the target path and directory are not appropriately validated

Consider a scenario where Roxana sends a ZIP archive to the target app for processing. The archive contains a file with the path `../../lib/libnative.so`. The app extracts the archive without validating each entry's path. The extraction writes a modified `libnative.so` into the app's native library directory. On the next app launch, the app loads the modified native library, which contains Roxana's malicious code. This is a "Zip Slip" vulnerability: path traversal inside an archive leading to arbitrary file overwrite and code execution.

1. Archive extraction without path validation allows entries to escape the intended extraction directory.
2. An attacker-controlled file overwriting a library, executable, or configuration file can lead to code execution.
3. Path components like `../` in archive entry names are legitimate in some contexts but dangerous in extraction operations.

### Example

Roxana crafts a ZIP file containing two entries: `legitimate_file.txt` and `../../lib/libcracked.so`. The app receives the ZIP (e.g., as an import format), creates an `OutputStream` for each entry path without canonicalizing, and writes `libcracked.so` to the app's native library path. On the next restart, the app loads `libcracked.so` and executes Roxana's code. The archive processing was standard Java ZIP extraction. The path validation was absent.

## Threat Modeling

### STRIDE

This scenario falls under **Tampering** and **Elevation of Privilege**.

Roxana uses the archive extraction mechanism to overwrite files that the app trusts, ultimately achieving code execution in the app's process context.

### What can go wrong?

- Native libraries are overwritten with malicious versions that execute on the next app load.
- Configuration files are overwritten to alter application behaviour (disable security controls, change backend URLs).
- Arbitrary file writes within the app's data directory expose sensitive data to attacker-controlled paths.

### What are we going to do about it?

- Before writing any archive entry, canonicalize the entry path and verify it starts with the intended extraction root directory.
- Reject any archive entry whose path contains `..` or is an absolute path.
- Use a maintained archive library that performs path validation by default; verify that the specific version used applies the check.
