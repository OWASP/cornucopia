# CAPEC™ 139: Relative Path Traversal

## Description

An attacker exploits a weakness in input validation on the target by supplying a specially constructed path utilizing dot and slash characters for the purpose of obtaining access to arbitrary files or resources. An attacker modifies a known path on the target in order to reach material that is not available through intended channels. These attacks normally involve adding additional path separators (/ or \) and/or dots (.), or encodings thereof, in various combinations in order to reach parent directories or entirely separate trees of the target's directory structure.

Source: [CAPEC™ 139](https://capec.mitre.org/data/definitions/139.html)

