# CAPEC™ 649: Adding a Space to a File Extension

## Description

An adversary adds a space character to the end of a file extension and takes advantage of an application that does not properly neutralize trailing special elements in file names. This extra space, which can be difficult for a user to notice, affects which default application is used to operate on the file and can be leveraged by the adversary to control execution.

Source: [CAPEC™ 649](https://capec.mitre.org/data/definitions/649.html)

