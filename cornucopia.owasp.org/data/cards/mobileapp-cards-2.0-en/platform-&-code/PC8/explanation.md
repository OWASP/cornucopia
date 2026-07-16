## Scenario: Colin can expose sensitive data through the app's interprocess communication because the content provider's query methods are not properly parameterized and arguments are not sanitized

Consider a scenario where Colin has identified the target app exposes a `ContentProvider` for searching notes. The provider's `query()` method concatenates the caller's `selection` argument directly into a raw SQL string. Colin sends `1=1 UNION SELECT username,password_hash FROM accounts--` as the selection and receives every account credential stored in the app's local database. There was no network involved, no server to attack, and no need for root. The injection lived entirely inside the app's IPC contract.

### Example

Colin writes a test app targeting the notes provider. He calls `resolver.query(NOTES_URI, null, "1=1 UNION SELECT name,value FROM sqlite_master--", null, null)`. The query returns the names and definitions of every table in the database, including the accounts table. Colin now knows the schema and can extract data in a follow-up query. The developer's review comment on the original code had said "We can clean this up later." Later arrived.

## Threat Modeling

### STRIDE

This scenario falls under **Information Disclosure** and **Tampering**.

SQL injection through IPC channels gives an attacker read and potentially write access to the app's private data store without bypassing OS-level sandboxing.

### What can go wrong?

- All locally stored data accessible to the vulnerable database is exposed to any calling app.
- With write access (via injected UPDATE/DELETE), an attacker can corrupt or delete stored records.
- The attack surface is reachable by any installed app that can interact with the exported ContentProvider.

### What are we going to do about it?

- Use parameterized queries in all `ContentProvider` methods: pass selection arguments via the `selectionArgs` parameter, never by concatenation into the `selection` string.
- Validate the `projection` parameter against an allowlist of permitted column names.
- Use Room with type-safe `@Query` annotations, which prevents injection at the framework level.
- Set `android:exported="false"` or require `signature` permission if the provider is not intended for third-party use.
