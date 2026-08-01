# CAPEC™ 18: XSS Targeting Non-Script Elements

## Description

This attack is a form of Cross-Site Scripting (XSS) where malicious scripts are embedded in elements that are not expected to host scripts such as image tags (<img>), comments in XML documents (< !-CDATA->), etc. These tags may not be subject to the same input validation, output validation, and other content filtering and checking routines, so this can create an opportunity for an adversary to tunnel through the application's elements and launch a XSS attack through other elements. As with all remote attacks, it is important to differentiate the ability to launch an attack (such as probing an internal network for unpatched servers) and the ability of the remote adversary to collect and interpret the output of said attack.

Source: [CAPEC™ 18](https://capec.mitre.org/data/definitions/18.html)

