# CAPEC™ 92: Forced Integer Overflow

## Description

This attack forces an integer variable to go out of range. The integer variable is often used as an offset such as size of memory allocation or similarly. The attacker would typically control the value of such variable and try to get it out of range. For instance the integer in question is incremented past the maximum possible value, it may wrap to become a very small, or negative number, therefore providing a very incorrect value which can lead to unexpected behavior. At worst the attacker can execute arbitrary code.

Source: [CAPEC™ 92](https://capec.mitre.org/data/definitions/92.html)

