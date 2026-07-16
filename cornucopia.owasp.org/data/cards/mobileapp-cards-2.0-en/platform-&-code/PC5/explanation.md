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
