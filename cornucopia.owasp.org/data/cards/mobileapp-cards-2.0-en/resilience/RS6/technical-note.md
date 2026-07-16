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
