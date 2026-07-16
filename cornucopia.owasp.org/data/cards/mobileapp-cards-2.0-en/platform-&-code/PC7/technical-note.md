## Platform-Aware Review Guidance

**Android**
- Inspect `res/xml/file_paths.xml` (or equivalent referenced in the `FileProvider` manifest declaration): use the most specific path possible.
- In `ContentProvider.openFile()`, canonicalize the Uri: `val canonical = File(path).canonicalPath; require(canonical.startsWith(allowedBase))`
- Create a dedicated subdirectory for shared files (e.g., `getFilesDir()/share/`) and configure the provider to serve only that path.
- Use Drozer: `run scanner.provider.traversal -a com.target.app` to test for traversal.

**iOS**
- Before opening any URL received from an external source, call `url.standardizedFileURL.resolvingSymlinksInPath()` and check it starts with the expected container path.
- For `UIDocumentPickerViewController` results, validate the file's URL and request security-scoped access only for the specific file.
- Avoid processing `file://` URLs from URL scheme handlers without strict path validation.

**Testing**
- Craft content URIs with `../` segments and send them to the provider; verify the provider returns a 403/SecurityException rather than the file.
- Test for symlink traversal within archive extraction flows (zip slip).

**OWASP Mappings**
- MASVS: PLATFORM-1, STORAGE-1
- MASTG: TEST-0007, TEST-0056, TEST-0355, TEST-0356, TEST-0357
- MASWE: MASWE-0064
