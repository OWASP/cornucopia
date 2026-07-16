## Scenario: Mallory can use the app installed on Bob's device maliciously to surveil, spy on, eavesdrop, control remotely, track, or otherwise monitor Bob without consent and/or notification

This card addresses a distinct and serious harm category: technology-facilitated abuse. Mallory may be a partner, ex-partner, parent misusing parental-control tools, employer overreaching, or a stalker who has physical access to Bob's device. The app may have been designed as a legitimate monitoring or parental-control tool — or it may have been designed specifically as stalkerware. In either case, the harm to Bob is the same.

Mallory uses the app to:
- Read Bob's messages, emails, and call logs.
- Access Bob's real-time GPS location continuously.
- Activate Bob's microphone or camera without indication.
- Control Bob's device (send messages on his behalf, access his accounts).
- Monitor Bob's screen activity.

### Example

Mallory installs a "family safety" app on Bob's phone while Bob is asleep. The app hides its icon and runs as a background service. It uploads Bob's GPS location every 30 seconds, forwards all incoming and outgoing SMS messages, and sends screenshots of the screen every minute to Mallory's account. Bob has no indication the app is installed. He later notices his battery draining faster than usual but attributes it to a recent OS update. The "family safety" app was designed for transparent, consensual use by families. Mallory used it without Bob's knowledge.

## Threat Modeling

### STRIDE

This scenario falls under **Information Disclosure** at an extreme personal level, with elements of **Spoofing** (the app misrepresents itself as a harmless system process) and **Tampering** (control of the device).

The primary harm is to autonomy, safety, and dignity. In many cases, technology-facilitated abuse is associated with domestic violence, coercive control, and stalking — harms that have severe, sometimes fatal, consequences.

### What can go wrong?

- A survivor of domestic abuse has their location continuously tracked, allowing the abuser to find them after they leave.
- An employer installs monitoring software on a personal device used for work without the employee's knowledge.
- A person's private communications are read without their consent, providing leverage for coercive control.
- A device is controlled remotely to send messages or delete evidence.
- The monitoring app's collected data is also exfiltrated by the monitoring platform vendor, creating secondary privacy harms.

### What are we going to do about it?

This card applies at three levels:

**For legitimate monitoring/parental-control app developers:**
- Require transparent, informed consent from all monitored parties; make the monitoring visible to the person being monitored.
- Do not support "stealth mode" or icon hiding; these features are used almost exclusively for non-consensual surveillance.
- Implement robust detection of compromise: alert the account holder if a new device is added or monitoring scope is expanded.
- Comply with platform policies (Apple/Google prohibit stalkerware-like features in App Store / Play Store apps).

**For general mobile app developers:**
- Protect your app from being used as a vector: prevent other apps from reading your in-app communications without user consent.
- Use `FLAG_SECURE` to prevent screen recording of sensitive content.
- Implement notification of active microphone/camera use; do not silence these indicators.

**For security reviewers and threat modelers:**
- Explicitly include technology-facilitated abuse in the threat model as a distinct threat actor (intimate partner / abuser with physical device access).
- Assess whether any feature of the app could be misused for surveillance: location sharing, message reading, screen recording, remote control.
- Evaluate whether the app's default privacy settings protect the most vulnerable users.
