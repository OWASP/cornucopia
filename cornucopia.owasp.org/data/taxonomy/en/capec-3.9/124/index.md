# CAPEC™ 124: Shared Resource Manipulation

## Description

An adversary exploits a resource shared between multiple applications, an application pool or hardware pin multiplexing to affect behavior. Resources may be shared between multiple applications or between multiple threads of a single application. Resource sharing is usually accomplished through mutual access to a single memory location or multiplexed hardware pins. If an adversary can manipulate this shared resource (usually by co-opting one of the applications or threads) the other applications or threads using the shared resource will often continue to trust the validity of the compromised shared resource and use it in their calculations. This can result in invalid trust assumptions, corruption of additional data through the normal operations of the other users of the shared resource, or even cause a crash or compromise of the sharing applications.

Source: [CAPEC™ 124](https://capec.mitre.org/data/definitions/124.html)

## Related ASVS Requirements

ASVS (5.0): [15.4.3](/taxonomy/asvs-5.0/15-secure-coding-and-architecture/04-safe-concurrency#V15.4.3), [15.4.4](/taxonomy/asvs-5.0/15-secure-coding-and-architecture/04-safe-concurrency#V15.4.4), [16.5.2](/taxonomy/asvs-5.0/16-security-logging-and-error-handling/05-error-handling#V16.5.2), [16.5.3](/taxonomy/asvs-5.0/16-security-logging-and-error-handling/05-error-handling#V16.5.3)
