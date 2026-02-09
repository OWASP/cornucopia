# Error Handling

## V16.5.1

Verify that a generic message is returned to the consumer when an unexpected or security-sensitive error occurs, ensuring no exposure of sensitive internal system data such as stack traces, queries, secret keys, and tokens.

Required for Level 2 and 3

### Related CAPEC™ Requirements

CAPEC™ (3.9): [116](/taxonomy/capec-3.9/116/index.md), [120](/taxonomy/capec-3.9/120/index.md), [126](/taxonomy/capec-3.9/126/index.md), [136](/taxonomy/capec-3.9/136/index.md), [137](/taxonomy/capec-3.9/137/index.md), [151](/taxonomy/capec-3.9/151/index.md), [152](/taxonomy/capec-3.9/152/index.md), [153](/taxonomy/capec-3.9/153/index.md), [160](/taxonomy/capec-3.9/160/index.md), [169](/taxonomy/capec-3.9/169/index.md), [175](/taxonomy/capec-3.9/175/index.md), [183](/taxonomy/capec-3.9/183/index.md), [184](/taxonomy/capec-3.9/184/index.md), [19](/taxonomy/capec-3.9/19/index.md), [198](/taxonomy/capec-3.9/198/index.md), [207](/taxonomy/capec-3.9/207/index.md), [21](/taxonomy/capec-3.9/21/index.md), [215](/taxonomy/capec-3.9/215/index.md), [23](/taxonomy/capec-3.9/23/index.md), [24](/taxonomy/capec-3.9/24/index.md), [250](/taxonomy/capec-3.9/250/index.md), [253](/taxonomy/capec-3.9/253/index.md), [261](/taxonomy/capec-3.9/261/index.md), [267](/taxonomy/capec-3.9/267/index.md), [28](/taxonomy/capec-3.9/28/index.md), [31](/taxonomy/capec-3.9/31/index.md), [37](/taxonomy/capec-3.9/37/index.md), [43](/taxonomy/capec-3.9/43/index.md), [50](/taxonomy/capec-3.9/50/index.md), [54](/taxonomy/capec-3.9/54/index.md), [593](/taxonomy/capec-3.9/593/index.md), [66](/taxonomy/capec-3.9/66/index.md), [664](/taxonomy/capec-3.9/664/index.md), [676](/taxonomy/capec-3.9/676/index.md), [70](/taxonomy/capec-3.9/70/index.md), [83](/taxonomy/capec-3.9/83/index.md), [88](/taxonomy/capec-3.9/88/index.md), [93](/taxonomy/capec-3.9/93/index.md)

## V16.5.2

Verify that the application continues to operate securely when external resource access fails, for example, by using patterns such as circuit breakers or graceful degradation.

Required for Level 2 and 3

### Related CAPEC™ Requirements

CAPEC™ (3.9): [100](/taxonomy/capec-3.9/100/index.md), [114](/taxonomy/capec-3.9/114/index.md), [124](/taxonomy/capec-3.9/124/index.md), [125](/taxonomy/capec-3.9/125/index.md), [129](/taxonomy/capec-3.9/129/index.md), [130](/taxonomy/capec-3.9/130/index.md), [131](/taxonomy/capec-3.9/131/index.md), [151](/taxonomy/capec-3.9/151/index.md), [184](/taxonomy/capec-3.9/184/index.md), [207](/taxonomy/capec-3.9/207/index.md), [21](/taxonomy/capec-3.9/21/index.md), [227](/taxonomy/capec-3.9/227/index.md), [24](/taxonomy/capec-3.9/24/index.md), [25](/taxonomy/capec-3.9/25/index.md), [50](/taxonomy/capec-3.9/50/index.md), [603](/taxonomy/capec-3.9/603/index.md), [607](/taxonomy/capec-3.9/607/index.md)

## V16.5.3

Verify that the application fails gracefully and securely, including when an exception occurs, preventing fail-open conditions such as processing a transaction despite errors resulting from validation logic.

Required for Level 2 and 3

### Related CAPEC™ Requirements

CAPEC™ (3.9): [100](/taxonomy/capec-3.9/100/index.md), [114](/taxonomy/capec-3.9/114/index.md), [115](/taxonomy/capec-3.9/115/index.md), [116](/taxonomy/capec-3.9/116/index.md), [124](/taxonomy/capec-3.9/124/index.md), [125](/taxonomy/capec-3.9/125/index.md), [128](/taxonomy/capec-3.9/128/index.md), [129](/taxonomy/capec-3.9/129/index.md), [130](/taxonomy/capec-3.9/130/index.md), [131](/taxonomy/capec-3.9/131/index.md), [151](/taxonomy/capec-3.9/151/index.md), [152](/taxonomy/capec-3.9/152/index.md), [153](/taxonomy/capec-3.9/153/index.md), [180](/taxonomy/capec-3.9/180/index.md), [184](/taxonomy/capec-3.9/184/index.md), [207](/taxonomy/capec-3.9/207/index.md), [21](/taxonomy/capec-3.9/21/index.md), [24](/taxonomy/capec-3.9/24/index.md), [25](/taxonomy/capec-3.9/25/index.md), [26](/taxonomy/capec-3.9/26/index.md), [461](/taxonomy/capec-3.9/461/index.md), [50](/taxonomy/capec-3.9/50/index.md), [54](/taxonomy/capec-3.9/54/index.md), [554](/taxonomy/capec-3.9/554/index.md), [70](/taxonomy/capec-3.9/70/index.md), [77](/taxonomy/capec-3.9/77/index.md)

## V16.5.4

Verify that a "last resort" error handler is defined which will catch all unhandled exceptions. This is both to avoid losing error details that must go to log files and to ensure that an error does not take down the entire application process, leading to a loss of availability.

Required for Level 3

### Related CAPEC™ Requirements

CAPEC™ (3.9): [151](/taxonomy/capec-3.9/151/index.md), [184](/taxonomy/capec-3.9/184/index.md), [207](/taxonomy/capec-3.9/207/index.md), [21](/taxonomy/capec-3.9/21/index.md), [24](/taxonomy/capec-3.9/24/index.md), [50](/taxonomy/capec-3.9/50/index.md)

## Disclaimer

Credit via [OWASP ASVS](https://owasp.org/www-project-application-security-verification-standard/).For more information visit: [The OWASP ASVS Project](https://owasp.org/www-project-application-security-verification-standard/) or [Github respository.](https://github.com/OWASP/ASVS). OWASP ASVS is under the [Creative Commons Attribution-Share Alike v4.0](https://github.com/OWASP/ASVS/blob/v5.0.0/LICENSE.md) license.
