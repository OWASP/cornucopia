## Scenario: Lauren can traverse or modify otherwise protected files or services through access to the underlying file system by exploiting weaknesses in file system-based content providers, resolvers or its configuration

### Example

Lauren uses a file-backed resolver that accepts `../../private/keys.json` as a document identifier. The resolver serves the file, and Lauren’s file manager displays a private key beside her grocery list, labeled “buy milk, protect server.”

File-system content providers and resolvers must normalize paths and enforce containment and permissions. A traversal weakness can turn an apparently narrow document request into access to protected files or services.


## Threat Modeling

### STRIDE

This scenario is primarily **Tampering**, **Information Disclosure**, **Elevation of Privilege**, **Denial of Service** in STRIDE. The named condition is: Lauren can traverse or modify otherwise protected files or services through access to the underlying file system by exploiting weaknesses in file system-based content providers, resolvers or its configuration.

- **MAS-THREAT-0018:** Attackers can access sensitive data and functionality exposed by app components.

- **MAS-ATTACK-0038:** Invoking exported or unprotected app components from another app installed on the device.
- **MAS-ATTACK-0039:** Connecting to open ports or local services exposed by the app.

### What can go wrong?

If Lauren can traverse or modify otherwise protected files or services through access to the underlying file system by exploiting weaknesses in file system-based content providers, resolvers or its configuration, the failure is concrete rather than merely theatrical: the app could let an attacker cross the platform-&-code boundary and reach data or capability that this flow should protect. In this card, the practical route includes Invoking exported or unprotected app components from another app installed on the device. Also, Connecting to open ports or local services exposed by the app. That can turn a normal user action into unauthorized access, disclosure, alteration, or service disruption; the mapped weakness entries below identify the exact implementation evidence to check.

Mapped weaknesses that sharpen the review:

- MASWE-0018 — Lack of Authentication or Authorization on App Components: This weakness occurs when app components that expose functionality or data do not enforce proper authentication or authorization on their callers.

### What are we going to do about it?

Keep provider-backed files within an approved canonical directory, reject absolute paths and traversal, generate safe names, and use scoped URI permissions; test symlinks, encoded traversal, resolver access, and reads or writes outside the intended root.


Mapped MASTG tests:

- MASTG-TEST-0357 — References to Oversharing of File-Based Content Providers: If the app exports an Android content provider without enforcing access restrictions, external callers may open private files through `content://` URIs. This test checks whether exported providers expose sensitive stored data to callers...

Mapped MASTG best practices:

- MASTG-BEST-0049 — Restrict and Validate Access to Exported Content Providers: Content Providers are not inherently unsafe, but database-backed and file-backed providers can expose sensitive data if they are exported, have weak permissions, or grant access through overly broad URI scopes.

Mapped MASTG knowledge:

- MASTG-KNOW-0104 — Low-Level System IPC Mechanisms: iOS includes several low-level IPC mechanisms that Apple frameworks and system daemons use internally: XPC, Mach ports, and `CFMessagePort`. Unlike the user-mediated or entitlement-scoped channels described in @MASTG-KNOW-0078, these...
- MASTG-KNOW-0020 — Inter-Process Communication (IPC) Mechanisms: Every Android process runs in its own sandboxed address space. Inter-process communication (IPC) lets apps and the system exchange data and invoke functionality across these process boundaries. Instead of relying on traditional...
- MASTG-KNOW-0117 — Android ContentProvider: A `ContentProvider` is an Android component that exposes structured data to other apps and system services through a standardized URI-based interface. Providers support CRUD operations (`query`, `insert`, `update`, `delete`) and are...
