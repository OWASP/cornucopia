# CAPEC™ 263: Force Use of Corrupted Files

## Description

This describes an attack where an application is forced to use a file that an attacker has corrupted. The result is often a denial of service caused by the application being unable to process the corrupted file, but other results, including the disabling of filters or access controls (if the application fails in an unsafe way rather than failing by locking down) or buffer overflows are possible.

Source: [CAPEC™ 263](https://capec.mitre.org/data/definitions/263.html)

