# CAPEC™ 466: Leveraging Active Adversary in the Middle Attacks to Bypass Same Origin Policy

## Description

An attacker leverages an adversary in the middle attack (CAPEC-94) in order to bypass the same origin policy protection in the victim's browser. This active adversary in the middle attack could be launched, for instance, when the victim is connected to a public WIFI hot spot. An attacker is able to intercept requests and responses between the victim's browser and some non-sensitive website that does not use TLS.

Source: [CAPEC™ 466](https://capec.mitre.org/data/definitions/466.html)

## Related ASVS Requirements

ASVS (5.0): [3.1.1](/taxonomy/asvs-5.0/03-web-frontend-security/01-web-frontend-security-documentation#V3.1.1), [3.4.1](/taxonomy/asvs-5.0/03-web-frontend-security/04-browser-security-mechanism-headers#V3.4.1), [3.4.2](/taxonomy/asvs-5.0/03-web-frontend-security/04-browser-security-mechanism-headers#V3.4.2), [3.4.8](/taxonomy/asvs-5.0/03-web-frontend-security/04-browser-security-mechanism-headers#V3.4.8), [3.7.4](/taxonomy/asvs-5.0/03-web-frontend-security/07-other-browser-security-considerations#V3.7.4)
