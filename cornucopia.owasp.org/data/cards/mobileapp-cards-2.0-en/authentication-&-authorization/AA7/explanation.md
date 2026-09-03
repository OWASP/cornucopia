## Scenario: Abdullah can bypass protected operations by invoking them out of sequence, replaying a previously valid authentication result, or altering client-controlled state, time, or feature inputs trusted by the app instead of revalidating authorization

Consider Abdullah suspects his sibling Tim is secretly chatting late at night instead of studying. Abdullah wants to read Tim’s confidential chat, but he is not authorized to do so. He gets Tim to install a malicious app and delivers an invite as a deep link or intent to the chat app. The app treats a local authentication success callback in combination with client-controlled navigation state as proof that the Abdullah should be able to see Tim's secret chat.


### Example

The app uses `BiometricPrompt` or `LAContext.evaluatePolicy` only to set a custom in-memory flag such as `isAuthorized = true`, without binding authentication to a cryptographic operation. On Android, the chat can be used without `setUserAuthenticationRequired(true)`; on iOS, without Keychain access controls that require user presence. Abdullah debugs the running app,  use dynamic instrumentation to force the success callback, replays a previous success result, or patches and repackages the app to remove the client-side check. He can then invoke the protected operation directly, use a crafted deep link or intent, or call a keystore operation while the device is compromised.

The app also trusts the chat identifier, action, timestamps, extras, URI, provider metadata, or imported content supplied through that external entry point. A crafted value can select another account or chat, synced to the device, change the operation, bypass a state or expiry check, or reach a parser, query, command, or backend request without validation. This can turn the local authentication bypass into unauthorized access and an injection attack. The server does not independently authorize the requested resource or verify fresh, non-replayable proof of user authentication or authorization.

## Threat Modeling

### STRIDE

This scenario primarily involves **Tampering** and **Elevation of Privilege** in STRIDE. Abdullah tampers with execution, package integrity, authentication results, or input handling to reach functionality reserved for Tim, leading to **Information Disclosure**. Crafted values that are interpreted as queries, commands, paths, or other executable syntax also create an **Injection** risk.

### What can go wrong?

* Sensitive chats, tokens, keys, or account data may be disclosed.
* Abdullah may perform protected actions or transactions as Tim.
* Crafted deep links, intents, files, provider results, or network input may cause injection, path traversal, or unintended backend requests.
* Authentication results may be replayed, and keys may be used on a compromised or stolen device without the user’s knowledge.

### What are we going to do about it?

* **Bind local authentication to the protected operation:** On Android, use `BiometricPrompt.authenticate` with a `CryptoObject` backed by an Android Keystore key configured with `setUserAuthenticationRequired(true)`; require authentication for each sensitive operation where appropriate. On iOS, retrieve secrets through Keychain access controls such as `SecAccessControlCreateWithFlags` with user-presence or current-biometry requirements. Do not treat an `onAuthenticationSucceeded` or `LAContext.evaluatePolicy` result alone as authorization.
* **Require intentional user action:** For sensitive Android operations, keep biometric confirmation enabled with `setConfirmationRequired(true)` or the secure default, particularly for passive modalities such as face recognition.
* **Enforce authorization server-side:** Revalidate the authenticated user, resource, operation, and workflow sequence on the server. Use fresh nonces or signed challenges and reject expired or replayed proofs; never trust client-side flags, timestamps, feature values, or navigation state.
* **Treat every external entry point as untrusted:** Validate deep-link schemes, hosts, paths, intent actions, extras, `ClipData`, returned provider metadata, files, IPC data, UI input, and network input against an allowlist before using them for navigation, authorization, storage, parsing, or backend requests. Prefer explicit intents and `content://` URIs, sanitize filenames, and anchor file operations to an application-controlled directory.
* **Prevent injection:** Canonicalize input once, validate type, length, and range, use parameterized queries and structured APIs, and contextually encode output. Do not construct queries, commands, paths, or executable content from untrusted values.
* **Use tamper resistance only as defense in depth:** Detect debugging, dynamic instrumentation, and repackaging where feasible, fail closed, and report risk to the server. These controls must not replace cryptographic key protection or server-side authorization because a determined attacker can patch or bypass client code.

See the mapped MASTG tests for how to verify that the app is safe. Follow the mapped MASTG best practices during coding, and prepare yourself by reading through the mapped MASTG knowledge.