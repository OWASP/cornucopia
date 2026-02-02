# CAPEC™ 397: Cloning Magnetic Strip Cards

## Description

An attacker duplicates the data on a Magnetic strip card (i.e. 'swipe card' or 'magstripe') to gain unauthorized access to a physical location or a person's private information. Magstripe cards encode data on a band of iron-based magnetic particles arrayed in a stripe along a rectangular card. Most magstripe card data formats conform to ISO standards 7810, 7811, 7813, 8583, and 4909. The primary advantage of magstripe technology is ease of encoding and portability, but this also renders magnetic strip cards susceptible to unauthorized duplication. If magstripe cards are used for access control, all an attacker need do is obtain a valid card long enough to make a copy of the card and then return the card to its location (i.e. a co-worker's desk). Magstripe reader/writers are widely available as well as software for analyzing data encoded on the cards. By swiping a valid card, it becomes trivial to make any number of duplicates that function as the original.

Source: [CAPEC™ 397](https://capec.mitre.org/data/definitions/397.html)

