---
date: 20240314
author: ive-verstappen
tags: owasp-top10, Agile
hidden: false
description: Implement the OWASP top 10 guidelines by playing the Cornucopia cardgame - in numbers
---
# HOW TO Implement the OWASP top 10 guidelines by playing the Cornucopia cardgame - in numbers

The OWASP Top 10 list is an excellent guide for the start of an Application Security improvement program of a software development team.  However, what we see is that lots of software development teams who don't have access to a dedicated security professional (or team) struggle to correctly implement the OWASP Top 10 guides.

These teams should strongly consider to start playing OWASP Cornucopia.  Cornucopia provides a very decent coverage of all the OWASP TOP 10 items and provides a practical way to integrate a dedicated security improvement process into your Agile development process.

In this blogpost, I will go through the statistics of how well Cornucopia is mapped on the latest iteration of the OWASP Top 10.

## A brief introduction into the OWASP Top 10
The OWASP community collects data about the most important weaknesses identified in applications.  These weaknesses are identified in the form of "Common Weakness Enumeration" (CWE)-ID's.  The OWASP community categorizes these CWE-ID's into broader categories and then orders the categories.

Each number in the top 10 is a category.  That means that if you dig down into 01-Broken Access Controls, you will find several CWE-ID's.  These CWE-ID's can then be linked back to several defensive secure development techniques.

Gaining an in-depth understanding about how to correctly tackle one OWASP top 10 category can be daunting.  That is why, for most development teams, it is preferable to use the TOP 10 categories only as a tool to prioritize their defensive actions.  Here is where playing cornucopia comes in.

### Playing cornucopia provides actionable non-functional requirements
Thanks to the relationship between OWASP Cornucopia, OWASP ASVS and the Common Weakness Enumeration, Playing Cornucopia provides actionable and tangible Non-Functional Requirements which a team can easily integrate into its Product Backlog.  The team identifies these Requirements in a collaborative fashion and can prioritize them together.

This makes playing Cornucopia ideally suited for teams who use an Agile process to develop software.  Cornucopia allows a team to find the best way to build more secure software together, as a team.

## Overall relationship between Cornucopia and Owasp TOP 10?
At dotNET lab, we have mapped every Cornucopia card can be mapped to the OWASP Top 10 items.  We have provided the mapping from OWASP Top 10 to their corresponding Cornucopia Cards in our overview of the OWASP Top 10 items.

We have mapped the coverage of OWASP TOP 10 guidelines of the Cornucopia, tallied the occurences and created a heatmap.  Here it is:
![General heatmap Cornucopia-TOP10 mapping[medium]](algemeen.png)

A few conclusions can be drawn based on our heatmap:

- In general, Cornucopia has a decent coverage of all Top 10 items
- Cornucopia provides in-depth guidance for the general explanation of each top 10 guide
- Once a team reaches a certain threshold of Cornucopia-coverage, it could be interesting to look at ASVS

Through the next chapters, I'll go briefly through each suit and its mappings.
- Data Validation & Encoding (DVE) suit
- Authentication (AT) suit
- Session Management (SM) suit
- Authorization (AZ) suit
- Cryptography (CR) suit
- Cornucopia (C) suit
	
## DVE suit has an excellent overall coverage of OWASP Top 10
![Data Validation & Encoding[medium]](dve-suit.png)

### My observations and opinion for the DVE-suit
This suit has a strong coverage of the OWASP Top 10 items.  

This makes the DVE suit an ideal choice for teams who start with their AppSec program by playing OWASP Cornucopia.  

## The AZ (AuthoriZation) suit has a strong focus on #1 - Broken Access Control
![Authorization[medium]](az-suit.png)

### My observations ans opinion for the AZ (Authorization) suit
If you want focus on the most important OWASP Top 10 Category, the AZ-suit is the best choice.

## The (CR) Cryptography suit is pure play #02 - Cryptographic Failures
![Cryptography[medium]](cr-suit.png)

### My observations and opinions for the CR suit
The cryptography suit is all about cryptography.  That is no surprise!  While the scope of this suit is narrow, the cryptography category is ranked #2 on the OWASP Top 10.  This means that the CR-suit should be high on your shortlist to include in your Cornucopia game.

## The AuthenTication (AT) suit closes all weaknesses on the Authentication & Authorization front
![Authentication[medium]](at-suit.png)

### My observations and opinions for the AT suit
Include this suit if your teams wants to make sure everything is done about possible Authentication & Authorization weaknesses.  

## The Cornucopia (C) suit helps your team focus on nasty security vulnerabilities often exploited by hackers
![Cornucopia[medium]](c-suit.png)

### My observations and opinions for the C suit

While the C-suit doesn't seem to have a strong correlation with specific OWASP Top 10 categories, it has a strong focus on the very nasty vulnerabilities.  It focuses on 05-Security Misconfiguration and 06-Vulnerable and Outdated components.  

## The Session Management (SM) suit prevents Security Misconfiguration and Data Integrity failures
![Session Management[medium]](sm-suit.png)


### My observations and opinions for the SM suit

The Session Management suit rounds out the cornucopia game with a focus on Security Misconfiguration.  

## Conclusion
Your implementation of the OWASP TOP 10 guidelines can start with simply playing the Cornucopia cardgame.  Cornucopia has a decent coverage of the TOP 10 categories, whereby each suit has its focus.  Depending on the priorities of your team, you could choose on which suit you want to focus next.

Additionally, Cornucopia acts as a springboard into the broader OWASP ecosystem, inviting teams to explore beyond Cornucopia or the Top 10 and delve into other projects that OWASP offers, such as ASVS. Embracing Cornucopia should elevate your team's security knowledge, improving your defense against cyber threats.

Good Luck!

Ive

Feel free to use the comment section below for feedback or questions.