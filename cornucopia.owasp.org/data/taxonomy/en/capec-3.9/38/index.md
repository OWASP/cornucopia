# CAPEC™ 38: Leveraging/Manipulating Configuration File Search Paths

## Description

This pattern of attack sees an adversary load a malicious resource into a program's standard path so that when a known command is executed then the system instead executes the malicious component. The adversary can either modify the search path a program uses, like a PATH variable or classpath, or they can manipulate resources on the path to point to their malicious components. J2EE applications and other component based applications that are built from multiple binaries can have very long list of dependencies to execute. If one of these libraries and/or references is controllable by the attacker then application controls can be circumvented by the attacker.

Source: [CAPEC™ 38](https://capec.mitre.org/data/definitions/38.html)

