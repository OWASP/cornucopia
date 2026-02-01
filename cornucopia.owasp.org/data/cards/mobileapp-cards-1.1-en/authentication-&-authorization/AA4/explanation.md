## STRIDE: Tampering

Your mobile app is feeling unusually trusting today.

An attacker installs the app, opens a proxy, and starts gently adjusting things — a flag here, a price there, maybe a role that looks interesting. The app nods politely and says, “Sure, that seems reasonable.”

Suddenly premium features are free, restricted actions are unlocked, and sensitive data is rewritten — all without breaking a sweat.

Turns out the app believed whatever the client told it.

Who knew?

### What could go wrong?

When important security decisions are made on the device, attackers can tamper with requests, replay traffic, or manipulate app state to perform actions they were never authorized to do.

If the backend doesn’t validate and authorize every request, it becomes impossible to tell honest users from creative ones.
