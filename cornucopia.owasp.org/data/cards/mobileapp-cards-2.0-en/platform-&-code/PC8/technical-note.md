## Platform-Aware Review Guidance

**Android**
- `ContentProvider.query(Uri, String[], String selection, String[] selectionArgs, String)`:
  - `selection` should contain only `?` placeholders: `"column = ?"`.
  - `selectionArgs` carries the values; the framework binds them safely via `SQLiteStatement`.
  - Never do: `"column = '" + userInput + "'"` in the `selection` string.
- Validate `projection` columns: maintain an allowlist of permitted column names and reject anything not on it.
- Use Room DAO with `@Query` annotations; Room compiles queries at build time and uses bound parameters.
- Review all `rawQuery()` and `execSQL()` calls for untrusted input interpolation.

**iOS (Core Data / SQLite)**
- `NSPredicate(format:argumentArray:)` — pass values in the `argumentArray`, not interpolated into the format string.
- FMDB: `executeQuery:withArgumentsInArray:` — never `executeQuery:` with string interpolation.
- SQLite C API: `sqlite3_prepare_v2` + `sqlite3_bind_*`; never `sqlite3_exec` with interpolated user input.

**Testing**
- Drozer: `run app.provider.query content://com.target.app.provider/notes --selection "1=1 UNION SELECT name,sql FROM sqlite_master--"`
- Fuzz the `selection` and `projection` parameters with SQL metacharacters.
- Static analysis: grep for `rawQuery`, `execSQL`, string concatenation adjacent to SQL keywords.

**OWASP Mappings**
- MASVS: CODE-4, PLATFORM-1, STORAGE-1
- MASTG: TEST-0007, TEST-0025, TEST-0056, TEST-0339, TEST-0355, TEST-0356, TEST-0357
- MASWE: MASWE-0064, MASWE-0086
