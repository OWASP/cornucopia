# CAPEC™ 502: Intent Spoof

## Description

An adversary, through a previously installed malicious application, issues an intent directed toward a specific trusted application's component in an attempt to achieve a variety of different objectives including modification of data, information disclosure, and data injection. Components that have been unintentionally exported and made public are subject to this type of an attack. If the component trusts the intent's action without verififcation, then the target application performs the functionality at the adversary's request, helping the adversary achieve the desired negative technical impact.

Source: [CAPEC™ 502](https://capec.mitre.org/data/definitions/502.html)

