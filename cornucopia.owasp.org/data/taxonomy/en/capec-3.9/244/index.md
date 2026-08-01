# CAPEC™ 244: XSS Targeting URI Placeholders

## Description

An attack of this type exploits the ability of most browsers to interpret "data", "javascript" or other URI schemes as client-side executable content placeholders. This attack consists of passing a malicious URI in an anchor tag HREF attribute or any other similar attributes in other HTML tags. Such malicious URI contains, for example, a base64 encoded HTML content with an embedded cross-site scripting payload. The attack is executed when the browser interprets the malicious content i.e., for example, when the victim clicks on the malicious link.

Source: [CAPEC™ 244](https://capec.mitre.org/data/definitions/244.html)

