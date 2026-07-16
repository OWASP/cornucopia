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
