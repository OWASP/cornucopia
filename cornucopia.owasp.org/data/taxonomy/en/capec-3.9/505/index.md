# CAPEC™ 505: Scheme Squatting

## Description

An adversary, through a previously installed malicious application, registers for a URL scheme intended for a target application that has not been installed. Thereafter, messages intended for the target application are handled by the malicious application. Upon receiving a message, the malicious application displays a screen that mimics the target application, thereby convincing the user to enter sensitive information. This type of attack is most often used to obtain sensitive information (e.g., credentials) from the user as they think that they are interacting with the intended target application.

Source: [CAPEC™ 505](https://capec.mitre.org/data/definitions/505.html)

