# CAPEC™ 29: Leveraging Time-of-Check and Time-of-Use (TOCTOU) Race Conditions

## Description

This attack targets a race condition occurring between the time of check (state) for a resource and the time of use of a resource. A typical example is file access. The adversary can leverage a file access race condition by "running the race", meaning that they would modify the resource between the first time the target program accesses the file and the time the target program uses the file. During that period of time, the adversary could replace or modify the file, causing the application to behave unexpectedly.

Source: [CAPEC™ 29](https://capec.mitre.org/data/definitions/29.html)

