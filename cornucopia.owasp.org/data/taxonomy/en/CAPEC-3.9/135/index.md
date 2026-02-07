# CAPEC™ 135: Format String Injection

## Description

An adversary includes formatting characters in a string input field on the target application. Most applications assume that users will provide static text and may respond unpredictably to the presence of formatting character. For example, in certain functions of the C programming languages such as printf, the formatting character %s will print the contents of a memory location expecting this location to identify a string and the formatting character %n prints the number of DWORD written in the memory. An adversary can use this to read or write to memory locations or files, or simply to manipulate the value of the resulting text in unexpected ways. Reading or writing memory may result in program crashes and writing memory could result in the execution of arbitrary code if the adversary can write to the program stack.

Source: [CAPEC™ 135](https://capec.mitre.org/data/definitions/135.html)

## Related ASVS Requirements

ASVS (5.0): [1.3.10](/taxonomy/asvs-5.0/01-encoding-and-sanitization/03-sanitization#V1.3.10)
