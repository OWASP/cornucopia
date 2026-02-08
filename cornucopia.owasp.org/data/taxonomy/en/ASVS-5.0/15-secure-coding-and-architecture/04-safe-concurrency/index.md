# Safe Concurrency

## V15.4.1

Verify that shared objects in multi-threaded code (such as caches, files, or in-memory objects accessed by multiple threads) are accessed safely by using thread-safe types and synchronization mechanisms like locks or semaphores to avoid race conditions and data corruption.

Required for Level 3

### Related CAPEC™ Requirements

CAPEC™ (3.9): [131](/taxonomy/capec-3.9/131/index.md), [212](/taxonomy/capec-3.9/212/index.md), [26](/taxonomy/capec-3.9/26/index.md)

## V15.4.2

Verify that checks on a resource's state, such as its existence or permissions, and the actions that depend on them are performed as a single atomic operation to prevent time-of-check to time-of-use (TOCTOU) race conditions. For example, checking if a file exists before opening it, or verifying a users access before granting it.

Required for Level 3

### Related CAPEC™ Requirements

CAPEC™ (3.9): [212](/taxonomy/capec-3.9/212/index.md), [26](/taxonomy/capec-3.9/26/index.md)

## V15.4.3

Verify that locks are used consistently to avoid threads getting stuck, whether by waiting on each other or retrying endlessly, and that locking logic stays within the code responsible for managing the resource to ensure locks cannot be inadvertently or maliciously modified by external classes or code.

Required for Level 3

### Related CAPEC™ Requirements

CAPEC™ (3.9): [124](/taxonomy/capec-3.9/124/index.md), [125](/taxonomy/capec-3.9/125/index.md), [227](/taxonomy/capec-3.9/227/index.md), [25](/taxonomy/capec-3.9/25/index.md), [469](/taxonomy/capec-3.9/469/index.md), [603](/taxonomy/capec-3.9/603/index.md), [607](/taxonomy/capec-3.9/607/index.md)

## V15.4.4

Verify that resource allocation policies prevent thread starvation by ensuring fair access to resources, such as by leveraging thread pools, allowing lower-priority threads to proceed within a reasonable timeframe.

Required for Level 3

### Related CAPEC™ Requirements

CAPEC™ (3.9): [124](/taxonomy/capec-3.9/124/index.md), [125](/taxonomy/capec-3.9/125/index.md), [227](/taxonomy/capec-3.9/227/index.md), [25](/taxonomy/capec-3.9/25/index.md), [469](/taxonomy/capec-3.9/469/index.md), [603](/taxonomy/capec-3.9/603/index.md), [607](/taxonomy/capec-3.9/607/index.md)

## Disclaimer

Credit via [OWASP ASVS](https://owasp.org/www-project-application-security-verification-standard/).For more information visit: [The OWASP ASVS Project](https://owasp.org/www-project-application-security-verification-standard/) or [Github respository.](https://github.com/OWASP/ASVS). OWASP ASVS is under the [Creative Commons Attribution-Share Alike v4.0](https://github.com/OWASP/ASVS/blob/v5.0.0/LICENSE.md) license.
