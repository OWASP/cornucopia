# CAPEC™ 197: Exponential Data Expansion

## Description

An adversary submits data to a target application which contains nested exponential data expansion to produce excessively large output. Many data format languages allow the definition of macro-like structures that can be used to simplify the creation of complex structures. However, this capability can be abused to create excessive demands on a processor's CPU and memory. A small number of nested expansions can result in an exponential growth in demands on memory.

Source: [CAPEC™ 197](https://capec.mitre.org/data/definitions/197.html)

