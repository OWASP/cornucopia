# CAPEC™ 141: Cache Poisoning

## Description

An attacker exploits the functionality of cache technologies to cause specific data to be cached that aids the attackers' objectives. This describes any attack whereby an attacker places incorrect or harmful material in cache. The targeted cache can be an application's cache (e.g. a web browser cache) or a public cache (e.g. a DNS or ARP cache). Until the cache is refreshed, most applications or clients will treat the corrupted cache value as valid. This can lead to a wide range of exploits including redirecting web browsers towards sites that install malware and repeatedly incorrect calculations based on the incorrect value.

Source: [CAPEC™ 141](https://capec.mitre.org/data/definitions/141.html)

## Related ASVS Requirements

ASVS (5.0): [1.3.9](/taxonomy/asvs-5.0/01-encoding-and-sanitization/03-sanitization#V1.3.9)
