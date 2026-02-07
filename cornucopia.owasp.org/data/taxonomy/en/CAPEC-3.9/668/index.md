# CAPEC™ 668: Key Negotiation of Bluetooth Attack (KNOB)

## Description

An adversary can exploit a flaw in Bluetooth key negotiation allowing them to decrypt information sent between two devices communicating via Bluetooth. The adversary uses an Adversary in the Middle setup to modify packets sent between the two devices during the authentication process, specifically the entropy bits. Knowledge of the number of entropy bits will allow the attacker to easily decrypt information passing over the line of communication.

Source: [CAPEC™ 668](https://capec.mitre.org/data/definitions/668.html)

