# CAPEC™ 208: Removing/short-circuiting 'Purse' logic: removing/mutating 'cash' decrements

## Description

An attacker removes or modifies the logic on a client associated with monetary calculations resulting in incorrect information being sent to the server. A server may rely on a client to correctly compute monetary information. For example, a server might supply a price for an item and then rely on the client to correctly compute the total cost of a purchase given the number of items the user is buying. If the attacker can remove or modify the logic that controls these calculations, they can return incorrect values to the server. The attacker can use this to make purchases for a fraction of the legitimate cost or otherwise avoid correct billing for activities.

Source: [CAPEC™ 208](https://capec.mitre.org/data/definitions/208.html)

