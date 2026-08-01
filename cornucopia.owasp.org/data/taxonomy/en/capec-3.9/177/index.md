# CAPEC™ 177: Create files with the same name as files protected with a higher classification

## Description

An attacker exploits file location algorithms in an operating system or application by creating a file with the same name as a protected or privileged file. The attacker could manipulate the system if the attacker-created file is trusted by the operating system or an application component that attempts to load the original file. Applications often load or include external files, such as libraries or configuration files. These files should be protected against malicious manipulation. However, if the application only uses the name of the file when locating it, an attacker may be able to create a file with the same name and place it in a directory that the application will search before the directory with the legitimate file is searched. Because the attackers' file is discovered first, it would be used by the target application. This attack can be extremely destructive if the referenced file is executable and/or is granted special privileges based solely on having a particular name.

Source: [CAPEC™ 177](https://capec.mitre.org/data/definitions/177.html)

