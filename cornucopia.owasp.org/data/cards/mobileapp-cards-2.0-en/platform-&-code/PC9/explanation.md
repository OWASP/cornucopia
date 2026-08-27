## Scenario: Max can modify or expose sensitive data because input validation and sanitation are not properly applied to interprocess communication or because extensions are not properly restricted

### Example

Max sends an extension a message containing HTML and a command-looking field. The extension inserts it without validation, and the shopping page sprouts a button that orders 40 inflatable castles whenever Max clicks “view details.”

IPC payloads and extension interfaces need positive validation, sanitization, and restricted capabilities. Treating messages as trusted lets a sender inject content or invoke functionality beyond the intended contract.


## Threat Modeling

### STRIDE

This scenario is primarily **Tampering**, **Information Disclosure** in STRIDE. The named condition is: Max can modify or expose sensitive data because input validation and sanitization are not properly applied to interprocess communication or because extensions are not properly restricted.

- **MAS-THREAT-0050:** Attackers can execute injection attacks against the app.
- **MAS-THREAT-0031:** Attackers can capture sensitive user input and content.

- **MAS-ATTACK-0047:** Delivering crafted deep links or intents from a malicious app or web page.
- **MAS-ATTACK-0059:** Supplying crafted input through any external interface (network, IPC, files, UI, or peripherals).
- **MAS-ATTACK-0048:** Capturing user input through a malicious custom keyboard or app extension.

### What can go wrong?

If Max can modify or expose sensitive data because input validation and sanitation are not properly applied to interprocess communication or because extensions are not properly restricted, the failure is concrete rather than merely theatrical: the app could let an attacker cross the platform-&-code boundary and reach data or capability that this flow should protect. In this card, the practical route includes Delivering crafted deep links or intents from a malicious app or web page. Also, Supplying crafted input through any external interface (network, IPC, files, UI, or peripherals). That can turn a normal user action into unauthorized access, disclosure, alteration, or service disruption; the mapped weakness entries below identify the exact implementation evidence to check.

Mapped weaknesses that sharpen the review:

- MASWE-0050 — Unsafe Handling of Untrusted Data: This weakness occurs when data originating outside the app's trust boundary reaches a sensitive sink without being validated, sanitized, or safely parsed.
- MASWE-0001 — Sensitive Data Stored Unencrypted in Private Storage: This weakness occurs when an app stores sensitive data unencrypted in private storage locations, such as the application sandbox, where it can be exposed via incorrect file permissions, an app or device vulnerability, or data backup...
- MASWE-0031 — Allowing Untrusted App Extensions: This weakness occurs when an app allows untrusted app extensions, such as custom keyboards or share and action extensions, to interact with it and observe the data it handles.

### What are we going to do about it?

Validate IPC payloads against a strict schema and allowlist, restrict extensions and their exported interfaces, and sanitize data before invoking them; test malformed messages, hostile extensions, shared files, and unexpected callers.


Mapped MASTG tests:

- MASTG-TEST-0337 — References to Object Deserialization of Untrusted Data: Android apps can reconstruct objects from serialized data received through platform mechanisms such as `Intent` extras, `Bundle` values, IPC payloads, files, or network responses. If the app deserializes data from these sources without...
- MASTG-TEST-0339 — SQL Injection in Content Providers: Android applications can share structured data via `ContentProvider` components. However, if these providers create SQL queries using untrusted input from URIs without adequate validation or parameterization, they risk becoming...
- MASTG-TEST-0386 — References to Object Deserialization of Untrusted Data: iOS apps can reconstruct objects from serialized data received through files, IPC payloads, network responses, pasteboard data, app extensions, or archived data stored locally. If an attacker can influence this data and the app decodes...
- MASTG-TEST-0389 — References to the App-Wide Restriction of Custom Keyboards: iOS lets users install custom keyboards, which are app extensions that replace the system keyboard across all apps (see @MASTG-KNOW-0141). Once granted "Full Access", a custom keyboard can transmit what the user types off the device. An...

Mapped MASTG best practices:

- MASTG-BEST-0039 — Prevent SQL Injection in ContentProviders: The `ContentProvider` enables Android applications to share data with other applications and system components. If a `ContentProvider` constructs SQL queries using untrusted input from URIs, IPC calls, or Intents without validation or...
- MASTG-BEST-0064 — Use Safe APIs for Object Deserialization: Use secure, class-restricted deserialization for object archives that can be influenced by an attacker. This includes archives received from files, IPC payloads, network responses, pasteboard data, app extensions, shared containers, or...
- MASTG-BEST-0068 — Secure Data Sharing Between App Extensions and Containing Apps: When an app and its extensions share data through an App Group, the shared container is readable and writable by every member of the group, with no per-item access control between members (see @MASTG-KNOW-0082). Choose the sharing...
- MASTG-BEST-0069 — Keep Sensitive Input on the System Keyboard: Custom keyboards are app extensions that replace the system keyboard across all apps and, once granted "Full Access", can transmit what the user types off the device (see @MASTG-KNOW-0082). For input that carries secrets, such as...

Mapped MASTG knowledge:

- MASTG-KNOW-0021 — Object Serialization: There are several ways to serialize an object on Android:
- MASTG-KNOW-0117 — Android ContentProvider: A `ContentProvider` is an Android component that exposes structured data to other apps and system services through a standardized URI-based interface. Providers support CRUD operations (`query`, `insert`, `update`, `delete`) and are...
- MASTG-KNOW-0075 — Object Serialization: There are several ways to persist an object on iOS:
- MASTG-KNOW-0082 — App Extensions: Starting with iOS 8, Apple introduced App Extensions. App extensions let an app offer custom functionality and content to users while they interact with other apps or the system. Each extension implements a single, well-scoped task, for...
- MASTG-KNOW-0141 — Custom Keyboards: A custom keyboard is an app extension (see @MASTG-KNOW-0082) that replaces the system keyboard across all apps on the device. The user installs it through its containing app and must explicitly enable it in **Settings** (**General >...
