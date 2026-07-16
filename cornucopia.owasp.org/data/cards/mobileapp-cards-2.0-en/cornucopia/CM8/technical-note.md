## Platform-Aware Review Guidance

**Android**
- Zip Slip fix pattern:
  ```kotlin
  val entry = zipEntry.name
  val destFile = File(destDir, entry)
  val destDirPath = destDir.canonicalPath
  if (!destFile.canonicalPath.startsWith(destDirPath + File.separator)) {
      throw SecurityException("Zip Slip detected: $entry")
  }
  ```
- Use Apache Commons Compress (version 1.21+) which has built-in path traversal protection.
- Apply the same check to TAR, RAR, and other archive formats.

**iOS**
- When processing ZIP/TAR entries, resolve each entry path with `URL.standardizedFileURL` and verify it starts with the destination URL path.
- Reject any entry whose name contains `..` or starts with `/`.
- Libraries: use `SSZipArchive` or `Minizip` with path validation; review the library version for known traversal issues.

**Testing**
- Create a test ZIP with a `../../etc/passwd` style entry (adapted to the target OS); verify the app rejects the entry.
- Send the crafted ZIP to all archive-handling entry points in the app.
- Review all `ZipInputStream`, `ZipFile`, and equivalent archive-handling code for path validation.

**OWASP Mappings**
- MASVS: CODE-4, STORAGE-2
- MASTG: (see MASVS references above)
- MASWE: MASWE-0082, MASWE-0087
