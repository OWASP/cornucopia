## Scenario: Joren can bypass access controls because the anti-debugging controls aren't strong enough according to what is recommended or the perceived effort of a potential attacker

### Example

Joren’s music app has an anti-debugging check that waits one millisecond, then gives up. He pauses it with a debugger, and the app obediently reveals its premium catalog, including a 14-minute recording of someone tuning a triangle.

Anti-debugging controls must withstand realistic attacker effort rather than merely inconvenience a casual glance. Weak checks can be bypassed to inspect state or reach protected operations.


## Threat Modeling

### STRIDE

This scenario is primarily **Spoofing**, **Information Disclosure** in STRIDE. The named condition is: Joren can bypass access controls because the anti-debugging controls aren't strong enough according to what is recommended or the perceived effort of a potential attacker.

- **MAS-THREAT-0064:** Attackers can inspect and manipulate the running app without resistance.

- **MAS-ATTACK-0002:** Debugging the app at runtime.

### What can go wrong?

If Joren can bypass access controls because the anti-debugging controls aren't strong enough according to what is recommended or the perceived effort of a potential attacker, the failure is concrete rather than merely theatrical: the app could let an attacker cross the resilience boundary and reach data or capability that this flow should protect. In this card, the practical route includes Debugging the app at runtime. That can turn a normal user action into unauthorized access, disclosure, alteration, or service disruption; the mapped weakness entries below identify the exact implementation evidence to check.

Mapped weaknesses that sharpen the review:

- MASWE-0064 — Debugger Detection Not Implemented: This weakness occurs when an app does not detect the presence of a debugger attached to it at runtime.

### What are we going to do about it?

Layer anti-debugging with platform integrity and server-side risk decisions rather than relying on one bypassable check; detect common debugger and hook states, respond proportionately, and test both static controls and runtime bypass attempts.


Mapped MASTG tests:

- MASTG-TEST-0352 — References to Debugging Detection APIs: Apps can implement debugging detection at the Java/Kotlin level using APIs such as `Debug.isDebuggerConnected()`), or at the native level using mechanisms such as `ptrace` calls, `TracerPid` checks in `/proc/self/status`, or inlined...
- MASTG-TEST-0353 — Runtime Use of Debugging Detection APIs: Even if an app references debugging detection APIs, those checks may not execute in security-relevant code paths at runtime. For example, they may only run in debug build variants, fire only once at startup, or be dead code that's never...
- MASTG-TEST-0401 — References to Debugging Detection APIs: iOS apps can implement debugging detection using mechanisms such as `ptrace` with `PT_DENY_ATTACH`, `sysctl` checks for `P_TRACED`, parent-process checks through `getppid`, or Mach exception-port checks with `task_get_exception_ports`....
- MASTG-TEST-0402 — Runtime Use of Debugging Detection APIs: Even if an iOS app references debugging detection APIs, those checks may not execute in security-relevant code paths at runtime. For example, they may only run in debug builds, fire only once at startup, or be dead code that is never...

Mapped MASTG best practices:

- MASTG-BEST-0007 — Debuggable Flag Disabled in the AndroidManifest: Ensure the debuggable flag in the AndroidManifest.xml is set to `false` for all release builds.
- MASTG-BEST-0029 — Implementing Resilience and RASP Signals: The source provides the mapped security guidance for this control.
- MASTG-BEST-0047 — Continuous Anti-Debugging Checks: Implement frequent anti-debugging checks during sensitive execution paths instead of relying on a one-time check at startup.
- MASTG-BEST-0074 — Implementing Anti-Debugging Checks on iOS: Implement anti-debugging checks in iOS apps that handle high-risk flows, and run those checks at startup and before or during sensitive operations instead of relying on a single startup check.

Mapped MASTG knowledge:

- MASTG-KNOW-0007 — Debuggable Apps: Debugging is an essential process for developers to identify and fix errors or bugs in their Android app. By using a debugger, developers can select the device to debug their app on and set breakpoints in their Java, Kotlin, and C/C++...
- MASTG-KNOW-0028 — Anti-Debugging: Debugging is a highly effective way to analyze runtime app behavior. It allows the reverse engineer to step through the code, stop app execution at arbitrary points, inspect the state of variables, read and modify memory, and a lot more.
- MASTG-KNOW-0085 — Anti-Debugging Detection: Debugging is a powerful runtime analysis technique. A debugger can stop execution at chosen points, inspect variables and registers, read process memory, and modify control flow. On iOS, debugging release apps usually involves the...
