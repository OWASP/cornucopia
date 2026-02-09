# CAPEC™ 96: Block Access to Libraries

## Description

An application typically makes calls to functions that are a part of libraries external to the application. These libraries may be part of the operating system or they may be third party libraries. It is possible that the application does not handle situations properly where access to these libraries has been blocked. Depending on the error handling within the application, blocked access to libraries may leave the system in an insecure state that could be leveraged by an attacker.

Source: [CAPEC™ 96](https://capec.mitre.org/data/definitions/96.html)

