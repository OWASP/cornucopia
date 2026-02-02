# CAPEC™ 35: Leverage Executable Code in Non-Executable Files

## Description

An attack of this type exploits a system's trust in configuration and resource files. When the executable loads the resource (such as an image file or configuration file) the attacker has modified the file to either execute malicious code directly or manipulate the target process (e.g. application server) to execute based on the malicious configuration parameters. Since systems are increasingly interrelated mashing up resources from local and remote sources the possibility of this attack occurring is high.

Source: [CAPEC™ 35](https://capec.mitre.org/data/definitions/35.html)

