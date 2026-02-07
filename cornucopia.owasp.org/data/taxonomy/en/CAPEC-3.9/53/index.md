# CAPEC™ 53: Postfix, Null Terminate, and Backslash

## Description

If a string is passed through a filter of some kind, then a terminal NULL may not be valid. Using alternate representation of NULL allows an adversary to embed the NULL mid-string while postfixing the proper data so that the filter is avoided. One example is a filter that looks for a trailing slash character. If a string insertion is possible, but the slash must exist, an alternate encoding of NULL in mid-string may be used.

Source: [CAPEC™ 53](https://capec.mitre.org/data/definitions/53.html)

