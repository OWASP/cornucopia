# CAPEC™ 45: Buffer Overflow via Symbolic Links

## Description

This type of attack leverages the use of symbolic links to cause buffer overflows. An adversary can try to create or manipulate a symbolic link file such that its contents result in out of bounds data. When the target software processes the symbolic link file, it could potentially overflow internal buffers with insufficient bounds checking.

Source: [CAPEC™ 45](https://capec.mitre.org/data/definitions/45.html)

