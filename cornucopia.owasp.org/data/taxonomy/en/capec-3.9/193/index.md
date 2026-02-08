# CAPEC™ 193: PHP Remote File Inclusion

## Description

In this pattern the adversary is able to load and execute arbitrary code remotely available from the application. This is usually accomplished through an insecurely configured PHP runtime environment and an improperly sanitized "include" or "require" call, which the user can then control to point to any web-accessible file. This allows adversaries to hijack the targeted application and force it to execute their own instructions.

Source: [CAPEC™ 193](https://capec.mitre.org/data/definitions/193.html)

