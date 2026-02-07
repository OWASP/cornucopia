# CAPEC™ 127: Directory Indexing

## Description

An adversary crafts a request to a target that results in the target listing/indexing the content of a directory as output. One common method of triggering directory contents as output is to construct a request containing a path that terminates in a directory name rather than a file name since many applications are configured to provide a list of the directory's contents when such a request is received. An adversary can use this to explore the directory tree on a target as well as learn the names of files. This can often end up revealing test files, backup files, temporary files, hidden files, configuration files, user accounts, script contents, as well as naming conventions, all of which can be used by an attacker to mount additional attacks.

Source: [CAPEC™ 127](https://capec.mitre.org/data/definitions/127.html)

## Related ASVS Requirements

ASVS (5.0): [13.4.3](/taxonomy/asvs-5.0/13-configuration/04-unintended-information-leakage#V13.4.3), [16.3.3](/taxonomy/asvs-5.0/16-security-logging-and-error-handling/03-security-events#V16.3.3)
