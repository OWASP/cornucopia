## Scenario: Colin can expose or modify sensitive data through the app's interprocess communication because of misconfiguration or because the content provider's query methods are not properly parameterized and arguments sanitized

### Example

Colin queries a content provider with `sort=name; DELETE FROM notes` in a field the provider concatenates into SQL. The provider returns no names, but the office loses every note about who borrowed the ceremonial stapler.

Provider queries must parameterize arguments, validate allowed fields, and constrain the data returned. Otherwise crafted IPC input can alter queries or expose records across the application boundary.


## Threat Modeling

### STRIDE

This scenario is primarily **Tampering**, **Information Disclosure** in STRIDE. The named condition is: Colin can expose or modify sensitive data through the app's interprocess communication because of misconfiguration or because the content provider's query methods are not properly parameterized and arguments sanitized.

- **MAS-THREAT-0050:** Attackers can execute injection attacks against the app.
- **MAS-THREAT-0018:** Attackers can access sensitive data and functionality exposed by app components.

- **MAS-ATTACK-0047:** Delivering crafted deep links or intents from a malicious app or web page.
- **MAS-ATTACK-0059:** Supplying crafted input through any external interface (network, IPC, files, UI, or peripherals).
- **MAS-ATTACK-0038:** Invoking exported or unprotected app components from another app installed on the device.
- **MAS-ATTACK-0039:** Connecting to open ports or local services exposed by the app.

### What can go wrong?

If Colin can expose or modify sensitive data through the app's interprocess communication because of misconfiguration or because the content provider's query methods are not properly parameterized and arguments sanitized, the failure is concrete rather than merely theatrical: the app could let an attacker cross the platform-&-code boundary and reach data or capability that this flow should protect. In this card, the practical route includes Delivering crafted deep links or intents from a malicious app or web page. Also, Supplying crafted input through any external interface (network, IPC, files, UI, or peripherals). That can turn a normal user action into unauthorized access, disclosure, alteration, or service disruption; the mapped weakness entries below identify the exact implementation evidence to check.

Mapped weaknesses that sharpen the review:

- MASWE-0050 — Unsafe Handling of Untrusted Data: This weakness occurs when data originating outside the app's trust boundary reaches a sensitive sink without being validated, sanitized, or safely parsed.
- MASWE-0018 — Lack of Authentication or Authorization on App Components: This weakness occurs when app components that expose functionality or data do not enforce proper authentication or authorization on their callers.

### What are we going to do about it?

Lock down content providers with non-exported or narrowly permissioned interfaces, parameterize every query, canonicalize URI arguments, and validate returned data; test crafted selections, projections, URI grants, and unauthorized callers.


Mapped MASTG tests:

- MASTG-TEST-0339 — SQL Injection in Content Providers: Android applications can share structured data via `ContentProvider` components. However, if these providers create SQL queries using untrusted input from URIs without adequate validation or parameterization, they risk becoming...
- MASTG-TEST-0355 — References to Unauthorized Database Access through Content Providers: This test checks whether the app exposes content providers that can be accessed by other apps without appropriate permission enforcement. Specifically, it verifies whether exported `<provider>` elements in the `AndroidManifest.xml`...
- MASTG-TEST-0356 — Runtime Verification of Unauthorized Database Access through Content Providers: If an app exports a content provider without requiring permissions, any app on the device can directly query its underlying database using `ContentResolver` or using the `adb shell content` command. Even when a permission is declared, a...
- MASTG-TEST-0357 — References to Oversharing of File-Based Content Providers: If the app exports an Android content provider without enforcing access restrictions, external callers may open private files through `content://` URIs. This test checks whether exported providers expose sensitive stored data to callers...

Mapped MASTG best practices:

- MASTG-BEST-0039 — Prevent SQL Injection in ContentProviders: The `ContentProvider` enables Android applications to share data with other applications and system components. If a `ContentProvider` constructs SQL queries using untrusted input from URIs, IPC calls, or Intents without validation or...
- MASTG-BEST-0049 — Restrict and Validate Access to Exported Content Providers: Content Providers are not inherently unsafe, but database-backed and file-backed providers can expose sensitive data if they are exported, have weak permissions, or grant access through overly broad URI scopes.

Mapped MASTG knowledge:

- MASTG-KNOW-0104 — Low-Level System IPC Mechanisms: iOS includes several low-level IPC mechanisms that Apple frameworks and system daemons use internally: XPC, Mach ports, and `CFMessagePort`. Unlike the user-mediated or entitlement-scoped channels described in @MASTG-KNOW-0078, these...
- MASTG-KNOW-0117 — Android ContentProvider: A `ContentProvider` is an Android component that exposes structured data to other apps and system services through a standardized URI-based interface. Providers support CRUD operations (`query`, `insert`, `update`, `delete`) and are...
- MASTG-KNOW-0020 — Inter-Process Communication (IPC) Mechanisms: Every Android process runs in its own sandboxed address space. Inter-process communication (IPC) lets apps and the system exchange data and invoke functionality across these process boundaries. Instead of relying on traditional...
