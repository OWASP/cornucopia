---
date: 20240229
author: ive-verstappen
tags: Deep-Dive
hidden: false
description: A deep dive into the information on a cornucopia card
---
# A Deep Dive into the Information on a Cornucopia Card

The OWASP Cornucopia card game provides lots of information about threats, more than is commonly understood by developers.

To address this, we've added a unique QR code to each card, linking directly to additional information. At dotNET lab, our goal is to ensure that every card is as clear and understandable as possible for developers.

Let's examine one card - [Authentication-3](https://cornucopia.dotnetlab.eu/authentication/3) - as a representative example and review the information it contains.

## The General Structure of the Authentication-3 Card
- Technical Note
- The card, including its image and the text on the card
- Mappings
  - Interactive mappings
  - OWASP ASVS
  - CAPEC
- Non-interactive mappings (for now)
  - OWASP SCP
  - OWASP AppSensor
  - Savecode
- ASVS (4.0) Cheat Sheet Series index

## Technical note

We've included a brief technical note for each card, based on the original WIKI-pages of Cornucopia.
We feel that this Technical Note is very useful for a developer to better understand the application of the Cornucopia Card.  We advise to consult the ASVS 4.0 mapping to gain more in-depth knowledge of a specific card.

## The Card
A visual link to the original card is provided, along with a reproduction of the text that appears on the card itself.

## Mappings
We have incorporated interactive links to the mappings listed on the Cornucopia card whenever possible.

## OWASP ASVS (4.0)

We've transitioned from ASVS Version 3 to ASVS Version 4. The physical cards display the mappings to ASVS v3.0, but the website has been updated to reflect the mappings to ASVS 4.0. I believe that the OWASP ASVS is one of the most practical projects for enhancing the cybersecurity of your application.

The OWASP Application Security Verification Standard (ASVS) is a framework established by the Open Web Application Security Project (OWASP) for securing web applications. 
Learning about OWASP ASVS and incorporating its requirements into your application development process is highly recommended.
The OWASP Application Security Verification Standard (ASVS) is a framework for securing web applications developed by the Open Web Application Security Project (OWASP). It establishes a foundation for testing web application security controls and provides developers with a comprehensive set of requirements for secure development.

OWASP ASVS offers a definitive suite of functionalities that should be integrated into your application to ensure its security.

Engaging with OWASP ASVS and incorporating its lessons into your development process is highly useful. Utilizing the Cornucopia Card's mapping to OWASP ASVS is an effective way to verify that your application meets the necessary security benchmarks.

References to ASVS 2.5.2 and 2.5.3 appear within Authentication-3, and are as follows:

### ASVS 2.5.2: "No Secret Questions"
Ensure that password hints or knowledge-based authentication methods, commonly referred to as "secret questions," are absent from your system.

If you have a feature whereby a user can enter secret questions, you should plan to delete this feature.

A corresponding CWE-ID link is also provided for deeper insight.

### ASVS 2.5.3: "Verify Password Credential Recovery Does Not Expose Current Password"
Confirm that there are no means to retrieve a user's current password under any circumstances.

### CWE-640: "Weak Password Recovery Mechanism for Forgotten Password"
By clicking on each ASVS description link, you can explore the Common Weakness Enumeration, which aids in understanding the nuances of these weaknesses, related with password recovery.

## Capec
CAPEC provides strategic defenses against each attack technique.  Over time, it allows you as a developer to start mastering defensive counter-moves for specific attack-patterns.

A detailed discussion on Capec will be featured in an upcoming post. We recommend that players of Cornucopia temporarily set Capec aside.  While it is useful, I believe it is a bit overkill if you're starting with Cornucopia. 

## Non-Interactive Mappings

Currently, certain mappings such as those for OWASP SCP, Appsensor, and Safecode are static due to the lack of a method for linking directly to a functioning website-page.

## ASVS (4.0) Cheatsheet Series Index

The Cheatsheet Series Index is another great OWASP initiative.  We higly recommend going through the refernced cheatsheets when you are going through the information of a card.

However, please avoid checking the Cheatsheet resources should during gameplay.  Consulting the Cheatsheets whilst playing the game will slow down the process considerably.

For Authentication-3, this is the referenced cheatsheet:

### ASVS 2.5 - Credential Recovery Requirements Cheatsheet
[Credential Recovery Requirements Cheatsheet](https://cheatsheetseries.owasp.org/IndexASVS.html#v25-credential-recovery-requirements)

## Attacks
Our cybersecurity specialists have examined various attack instances and referenced them to the Cornucopia cards. These instances are real-world examples of hacks and represent well-known attack patterns.  I believe the attacks present clear examples of how a card's vulnerability might translate into actual real-world security threats.

## Conclusion
OWASP Cornucopia improves the knowledge about cybersecurity for your team considerably. It is a great starting-point for your teams and will open te door to a wealth of knowledge thanks to lots of great OWASP projects.  

Good Luck!

Ive

Feel free to use the comment section below for feedback or questions.