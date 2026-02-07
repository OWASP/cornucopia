# CAPEC™ 47: Buffer Overflow via Parameter Expansion

## Description

In this attack, the target software is given input that the adversary knows will be modified and expanded in size during processing. This attack relies on the target software failing to anticipate that the expanded data may exceed some internal limit, thereby creating a buffer overflow.

Source: [CAPEC™ 47](https://capec.mitre.org/data/definitions/47.html)

