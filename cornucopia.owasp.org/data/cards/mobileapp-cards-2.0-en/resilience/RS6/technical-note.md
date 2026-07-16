## Technical Note: Joren can bypass access controls because the anti-debugging controls aren't strong enough according to what is recommended or the perceived effort of a potential attacker

### Platform Guidance

**Android:** Layer anti-debugging checks but assume they are a speed bump, not a moat; pair them with server-side enforcement and integrity decisions.

```kotlin
val debuggerAttached = Debug.isDebuggerConnected() || Debug.waitingForDebugger()
if (debuggerAttached) finishAffinity()
```

**iOS:** Check `ptrace`, `sysctl`, or debugger indicators as one signal among several, and avoid putting the only security decision in a tamperable branch.

```swift
var info = kinfo_proc()
var mib = [CTL_KERN, KERN_PROC, KERN_PROC_PID, getpid()]
var size = MemoryLayout.size(ofValue: info)
sysctl(&mib, u_int(mib.count), &info, &size, nil, 0)
```

### Relevant Tests

**Legacy Tests:** MASTG-TEST-0046, MASTG-TEST-0089
**New Tests:** MASTG-TEST-0247, MASTG-TEST-0369, MASTG-TEST-0401

### MASWE Weaknesses

- MASWE-0091, MASWE-0105: weak anti-debugging controls and easily bypassed runtime inspection defenses.
