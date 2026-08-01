# CAPEC™ 469: HTTP DoS

## Description

An attacker performs flooding at the HTTP level to bring down only a particular web application rather than anything listening on a TCP/IP connection. This denial of service attack requires substantially fewer packets to be sent which makes DoS harder to detect. This is an equivalent of SYN flood in HTTP. The idea is to keep the HTTP session alive indefinitely and then repeat that hundreds of times. This attack targets resource depletion weaknesses in web server software. The web server will wait to attacker's responses on the initiated HTTP sessions while the connection threads are being exhausted.

Source: [CAPEC™ 469](https://capec.mitre.org/data/definitions/469.html)

## Related ASVS Requirements

ASVS (5.0): [15.4.3](/taxonomy/asvs-5.0/15-secure-coding-and-architecture/04-safe-concurrency#V15.4.3), [15.4.4](/taxonomy/asvs-5.0/15-secure-coding-and-architecture/04-safe-concurrency#V15.4.4), [16.3.3](/taxonomy/asvs-5.0/16-security-logging-and-error-handling/03-security-events#V16.3.3), [2.3.2](/taxonomy/asvs-5.0/02-validation-and-business-logic/03-business-logic-security#V2.3.2), [2.4.1](/taxonomy/asvs-5.0/02-validation-and-business-logic/04-anti-automation#V2.4.1), [2.4.2](/taxonomy/asvs-5.0/02-validation-and-business-logic/04-anti-automation#V2.4.2)
