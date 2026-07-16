## Scenario: Alessandro can exploit the app by taking advantage of buffer overflows and memory leaks to write foreign code within the mobile code's address space

Consider a scenario where Alessandro is probing a mobile game's network protocol. The game uses a custom C++ binary protocol for multiplayer. Alessandro sends a malformed packet with a field length value larger than the buffer allocated to receive it. The receiving code copies the packet payload into a fixed-size stack buffer without checking the length. The buffer overflows, overwrites the return address, and Alessandro redirects execution to a ROP gadget chain he prepared. He achieves remote code execution on the target device.

1. Fixed-size buffers in native code without bounds checking are vulnerable to stack and heap buffer overflows.
2. Memory leaks expose heap layout information that can be used to defeat ASLR and prepare targeted ROP chains.
3. Use-after-free bugs in network protocol parsers are frequently exploitable for arbitrary code execution.

### Example

Alessandro sends `{"type": "move", "data": "A" * 10000}` to the game's native protocol handler. The handler copies the data field into a 256-byte stack buffer without checking the length. The buffer overflows, overwrites the stack frame, and the handler crashes. Alessandro refines his payload using the memory layout information leaked in the crash report and crafts a functional ROP chain. The buffer overflow was introduced by a junior developer who had not read the secure coding guidelines. The ROP chain was crafted by Alessandro, who had.

## Threat Modeling

### STRIDE

This scenario falls under **Tampering** and **Elevation of Privilege**.

Buffer overflow exploitation allows Alessandro to execute arbitrary code in the app's process context with the app's permissions, potentially accessing all data on the device that the app can access.

### What can go wrong?

- Arbitrary code execution in the app's process context.
- Root/kernel escalation in cases involving OS-level vulnerabilities triggered from the app process.
- Sensitive data accessible to the app process (credentials, keys, user data) is stolen.

### What are we going to do about it?

- Use memory-safe languages (Kotlin, Swift, Rust) for new components; migrate high-risk native components.
- Compile all native code with memory safety protections: stack canaries (`-fstack-protector-strong`), PIE (`-fPIE`), RELRO, and FORTIFY_SOURCE.
- Use bounded memory functions (`strncpy`, `snprintf`, `memcpy_s`) instead of unbounded equivalents.
- Fuzz all network protocol parsing code with a coverage-guided fuzzer before release.
