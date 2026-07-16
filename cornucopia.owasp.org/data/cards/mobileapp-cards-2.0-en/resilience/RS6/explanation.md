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
