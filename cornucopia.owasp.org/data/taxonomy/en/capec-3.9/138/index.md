# CAPEC™ 138: Reflection Injection

## Description

An adversary supplies a value to the target application which is then used by reflection methods to identify a class, method, or field. For example, in the Java programming language the reflection libraries permit an application to inspect, load, and invoke classes and their components by name. If an adversary can control the input into these methods including the name of the class/method/field or the parameters passed to methods, they can cause the targeted application to invoke incorrect methods, read random fields, or even to load and utilize malicious classes that the adversary created. This can lead to the application revealing sensitive information, returning incorrect results, or even having the adversary take control of the targeted application.

Source: [CAPEC™ 138](https://capec.mitre.org/data/definitions/138.html)

