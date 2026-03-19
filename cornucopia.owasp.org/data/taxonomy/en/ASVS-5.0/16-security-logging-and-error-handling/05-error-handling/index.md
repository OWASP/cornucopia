# Error Handling

## V16.5.1

Verify that a generic message is returned to the consumer when an unexpected or security-sensitive error occurs, ensuring no exposure of sensitive internal system data such as stack traces, queries, secret keys, and tokens.

Required for Level 2 and 3

### Related CAPEC™ Requirements

CAPEC™ (3.9): [116](/taxonomy/capec-3.9/116), [120](/taxonomy/capec-3.9/120), [126](/taxonomy/capec-3.9/126), [136](/taxonomy/capec-3.9/136), [137](/taxonomy/capec-3.9/137), [151](/taxonomy/capec-3.9/151), [152](/taxonomy/capec-3.9/152), [153](/taxonomy/capec-3.9/153), [160](/taxonomy/capec-3.9/160), [169](/taxonomy/capec-3.9/169), [175](/taxonomy/capec-3.9/175), [183](/taxonomy/capec-3.9/183), [184](/taxonomy/capec-3.9/184), [19](/taxonomy/capec-3.9/19), [198](/taxonomy/capec-3.9/198), [207](/taxonomy/capec-3.9/207), [21](/taxonomy/capec-3.9/21), [215](/taxonomy/capec-3.9/215), [23](/taxonomy/capec-3.9/23), [24](/taxonomy/capec-3.9/24), [250](/taxonomy/capec-3.9/250), [253](/taxonomy/capec-3.9/253), [261](/taxonomy/capec-3.9/261), [267](/taxonomy/capec-3.9/267), [28](/taxonomy/capec-3.9/28), [31](/taxonomy/capec-3.9/31), [37](/taxonomy/capec-3.9/37), [43](/taxonomy/capec-3.9/43), [50](/taxonomy/capec-3.9/50), [54](/taxonomy/capec-3.9/54), [593](/taxonomy/capec-3.9/593), [66](/taxonomy/capec-3.9/66), [664](/taxonomy/capec-3.9/664), [676](/taxonomy/capec-3.9/676), [70](/taxonomy/capec-3.9/70), [83](/taxonomy/capec-3.9/83), [88](/taxonomy/capec-3.9/88), [93](/taxonomy/capec-3.9/93)

## V16.5.2

Verify that the application continues to operate securely when external resource access fails, for example, by using patterns such as circuit breakers or graceful degradation.

Required for Level 2 and 3

### Related CAPEC™ Requirements

CAPEC™ (3.9): [100](/taxonomy/capec-3.9/100), [114](/taxonomy/capec-3.9/114), [124](/taxonomy/capec-3.9/124), [125](/taxonomy/capec-3.9/125), [129](/taxonomy/capec-3.9/129), [130](/taxonomy/capec-3.9/130), [131](/taxonomy/capec-3.9/131), [151](/taxonomy/capec-3.9/151), [184](/taxonomy/capec-3.9/184), [207](/taxonomy/capec-3.9/207), [21](/taxonomy/capec-3.9/21), [227](/taxonomy/capec-3.9/227), [24](/taxonomy/capec-3.9/24), [25](/taxonomy/capec-3.9/25), [50](/taxonomy/capec-3.9/50), [603](/taxonomy/capec-3.9/603), [607](/taxonomy/capec-3.9/607)

## V16.5.3

Verify that the application fails gracefully and securely, including when an exception occurs, preventing fail-open conditions such as processing a transaction despite errors resulting from validation logic.

Required for Level 2 and 3

### Related CAPEC™ Requirements

CAPEC™ (3.9): [100](/taxonomy/capec-3.9/100), [114](/taxonomy/capec-3.9/114), [115](/taxonomy/capec-3.9/115), [116](/taxonomy/capec-3.9/116), [124](/taxonomy/capec-3.9/124), [125](/taxonomy/capec-3.9/125), [128](/taxonomy/capec-3.9/128), [129](/taxonomy/capec-3.9/129), [130](/taxonomy/capec-3.9/130), [131](/taxonomy/capec-3.9/131), [151](/taxonomy/capec-3.9/151), [152](/taxonomy/capec-3.9/152), [153](/taxonomy/capec-3.9/153), [180](/taxonomy/capec-3.9/180), [184](/taxonomy/capec-3.9/184), [207](/taxonomy/capec-3.9/207), [21](/taxonomy/capec-3.9/21), [24](/taxonomy/capec-3.9/24), [25](/taxonomy/capec-3.9/25), [26](/taxonomy/capec-3.9/26), [461](/taxonomy/capec-3.9/461), [50](/taxonomy/capec-3.9/50), [54](/taxonomy/capec-3.9/54), [554](/taxonomy/capec-3.9/554), [70](/taxonomy/capec-3.9/70), [77](/taxonomy/capec-3.9/77)

## V16.5.4

Verify that a "last resort" error handler is defined which will catch all unhandled exceptions. This is both to avoid losing error details that must go to log files and to ensure that an error does not take down the entire application process, leading to a loss of availability.

Required for Level 3

### Related CAPEC™ Requirements

CAPEC™ (3.9): [151](/taxonomy/capec-3.9/151), [184](/taxonomy/capec-3.9/184), [207](/taxonomy/capec-3.9/207), [21](/taxonomy/capec-3.9/21), [24](/taxonomy/capec-3.9/24), [50](/taxonomy/capec-3.9/50)

## Disclaimer

Credit via [OWASP ASVS](https://owasp.org/www-project-application-security-verification-standard/).For more information visit: [The OWASP ASVS Project](https://owasp.org/www-project-application-security-verification-standard/) or [Github respository.](https://github.com/OWASP/ASVS). OWASP ASVS is under the [Creative Commons Attribution-Share Alike v4.0](https://github.com/OWASP/ASVS/blob/v5.0.0/LICENSE.md) license.
