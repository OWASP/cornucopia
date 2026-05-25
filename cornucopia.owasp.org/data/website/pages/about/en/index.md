# About

OWASP Cornucopia is a mechanism in the form of a card game to assist software development teams identify security requirements in Agile, conventional and formal development processes. It is language, platform and technology-agnostic.

If you have questions concerning OWASP Cornucopia, please search for it first in our [Q & A section](/questionsandanswers).

If you have other questions, suggestions or ideas please feel free to discuss them on our [email list](https://groups.google.com/a/owasp.org/g/cornucopia-project 'Cornucopia google group [external]') or submit them to our [list of issues](https://github.com/OWASP/cornucopia/issues 'Cornucopia Github repository [external]') in our repository. If you feel like and have the opportunity to help, do not hesitate to get in touch with us.

## Introduction

The idea behind Cornucopia is to help development teams, especially those using Agile methodologies, to identify application security requirements and develop security-based user stories. Although the concept had been waiting for enough time to progress it, the final motivation came when [SAFECode](http://www.safecode.org/) published its [Practical Security Stories and Security Tasks for Agile Development Environments](https://safecode.org/publication/SAFECode_Agile_Dev_Security0712.pdf '[inline] SAFE Code publication as pdf') in July 2012.

Cornucopia was created and first used for developer training in August 2012.

The Microsoft SDL team had already published its super [Elevation of Privilege: The Threat Modeling Game (EoP)](https://www.microsoft.com/en-gb/download/details.aspx?id=20303 'EoP publication at Microsoft. [external]') but that did not seem to address the most appropriate kind of issues that web application development teams mostly have to address.

EoP is a great concept and game strategy and was [published](https://www.microsoft.com/security/blog/2010/03/02/announcing-elevation-of-privilege-the-threat-modeling-game/ 'Microsoft announcing EoP on their blog. [external]') under a [Creative Commons Attribution License](http://creativecommons.org/licenses/by/3.0/ 'Link to the CC BY 3.0 Attribution Unported License [external]').

Cornucopia is based the concepts and game ideas in EoP, but those have been modified to be more relevant to the types of issues website app and mobile app developers encounter.

It attempts to introduce threat-modelling ideas into development teams that use Agile methodologies or are more focused on web application weaknesses than other types of software vulnerabilities or are not familiar with STRIDE and DREAD.

### How to start

To start using Cornucopia:

1. **Either** obtain or buy a pre-printed deck of cards;
2. **Or:** Download the free Adobe Illustrator files and get them professionally printed (see: [printing instructions](/printing);
3. **Or:** Play the game online at [copi.owasp.org](https://copi.owasp.org 'The Online version of OWASP Cornucopia [external]').
4. Identify an application, module or component to assess.
5. Invite business owners, architects, developers, testers along for a card game.
6. Get those infosec folk to provide chocolate, pizza, beer, flowers or all four as prizes.
7. Select a portion of the deck to start with.
8. [Play the game](/how-to-play) to discuss & document security requirements (and to win rounds).
9. Remember, to have fun!

## Mappings

The other driver for Cornucopia was to link the attacks with requirements and verification techniques. An initial aim had been to reference [CWE™](http://cwe.mitre.org/ 'CWE - 
Common Weakness Enumeration [external]') weakness IDs, but these proved too numerous, and instead it was decided to map each card to [CAPEC™](http://capec.mitre.org/ 'CAPEC™ -
Common Attack Pattern Enumeration and Classification (CAPEC) [external]') software attack pattern IDs, which themselves are mapped to CWEs, so the desired result is achieved.

Each Website App Edition card is also mapped to the 36 primary security stories in the [SAFECode document](https://safecode.org/resource-secure-development-practices/fundamental-practices-secure-software-development-2/ 'Fundamental Practices for Secure Software Development, Third Edition - SAFECode [external]'), as well as to the OWASP [Developer Guide Web Application Checklist](https://devguide.owasp.org/en/04-design/02-web-app-checklist/ 'OWASP Developer Guide [external]') v2, [ASVS v4.0.3](https://owasp.org/www-project-application-security-verification-standard/ 'OWASP Application Security Verification Standard (ASVS) [external]') and [AppSensor](https://owasp.org/www-project-appsensor/ 'OWASP AppSensor [external]') (application attack detection and response) to help teams create their own security-related stories for use in Agile processes.

Likewise, each Mobile App Edition is mapped to CAPEC™ and the SAFECode stories, but instead of SCP, ASVS, and AppSensor, each card is mapped to OWASP's [Mobile Application Security Verification Standard (MASVS) v2.0](https://mas.owasp.org/MASVS/ 'OWASP MASVS (Mobile Application Security Verification Standard [external]') and [Mobile Application Security Testing Guide (MASTG) v2.0](https://mas.owasp.org/MASTG/ 'OWASP Mobile Application Security Testing Guide [external]').

There is also the OWASP Cornucopia Companion Edition, which extends the previous two editions with 6 additional suites. These 6 companion suits covers new Agentic AI (AAI), Automated Threats (BOT), Cloud (CLD), Frontend (FRE), Large Language Models (LLM), and DevOps (DVO). These suits are mapped to various standards, maturity models, OWASP top 10s, guides, lists, and resources.

The following is the full list of all the resources that the 3 editions map to.

### Standards

* [OWASP Artificial Intelligence Security Verification Standard (AISVS)](https://owasp.org/www-project-artificial-intelligence-security-verification-standard-aisvs-docs/)
* [OWASP Application Security Verification Standard (ASVS) v4 (2019) and v5 (2025)](https://owasp.org/www-project-application-security-verification-standard/)
* [OWASP Mobile Application Security Verification Standard (MASVS) v2.1](https://mas.owasp.org/MASVS/)

### Maturity Models

* [OWASP DSOMM](https://dsomm.owasp.org/mapping)
* [OWASP SAMM](https://github.com/owaspsamm/core/tree/develop/model/activities)

### OWASP Top 10:

* [OWASP Agentic Top 10](https://genai.owasp.org/resource/owasp-top-10-for-agentic-applications-for-2026/)
* [OWASP LLM Top 10](https://genai.owasp.org/llm-top-10)
* [OWASP Top 10](https://owasp.org/Top10/2025/)
* [OWASP Top 10 Client-Side Security Risks](https://owasp.org/www-project-top-10-client-side-security-risks/)

### Guides

* [OWASP Automated Threats to Web Applications](https://github.com/OWASP/www-project-automated-threats-to-web-applications/tree/master/assets/oats/EN)
* [OWASP AI Testing Guide](https://owasp.org/www-project-ai-testing-guide/)
* [OWASP Mobile Application Security Testing Guide (MASTG) v1.7](https://mas.owasp.org/MASTG/)

### Other sources:

* [Mitre ATT&CK](https://attack.mitre.org/)
* [Mitre Atlas™](https://atlas.mitre.org/)
* [Mitre CAPEC™ v3.9](https://capec.mitre.org/data/definitions/2000.html)
* [OWASP Dev Guide Web Application Checklist](https://devguide.owasp.org/en/04-design/02-web-app-checklist/)
* [SAFECode Practical Security Stories and Security Tasks for Agile Development Environments (SAFECode) July 2012](https://safecode.org/publication/SAFECode_Agile_Dev_Security0712.pdf)
* [STRIDE](https://en.wikipedia.org/wiki/STRIDE_model)

## Other Security Gamification

If you are interested in using gaming for security, also see [Elevation of Privilege: The Threat Modeling Game](https://www.microsoft.com/en-gb/download/details.aspx?id=20303 'Elevation of Privilege (EoP) Threat Modeling Card Game [external]'), [Security Cards](http://securitycards.cs.washington.edu/ 'The Security Cards: A Security Threat Brainstorming Kit [external]') from the University of Washington, the commercial card game [Control-Alt-Hack](http://www.controlalthack.com/ 'Control-Alt-Hack(R) [external]') ([presentation](http://www.youtube.com/watch?v=Kpnvsgiiz8s 'Control-Alt-Hack(TM): White Hat Hacking for Fun and Profit (A Computer Security Card Game) [external]')), [OWASP Snakes and Ladders](https://owasp.org/www-project-snakes-and-ladders 'OWASP Snakes And Ladders [internal]'), [OWASP Cumulus](https://owasp.org/www-project-cumulus/ 'OWASP Cumulus [external]'), [OWASP Top 10 The Game](https://owasp.org/www-project-top-10-the-game 'OWASP Top 10 The Game [external]'), and web application security training tools incorporating gamification such as [OWASP Juice Shop](https://owasp.org/www-project-juice-shop/ 'OWASP JuiceShop  [external]'), [OWASP Security Shepherd](https://owasp.org/www-project-security-shepherd 'OWASP Security Shepard  [external]'), [OWASP WrongSecrets](https://owasp.org/www-project-wrongsecrets/ 'OWASP WrongSecrets [external]') and [ITSEC Games](http://itsecgames.blogspot.co.uk/ 'ITSEC Games [external]').

Additionally, Adam Shostack maintains a list of tabletop security games and related resources at [Tabletop Security Games + Cards](https://shostack.org/games.html 'Tabletop Security Games + Cards [external]').

## Acknowledgements

Cornucopia is developed, maintained, updated and promoted by a worldwide team of volunteers. See our [tribute page](/tribute#Acknowledgements) for a full list.

## License

OWASP Cornucopia Website App Edition (formerly called Ecommerce Edition) was created by Colin Watson. OWASP Cornucopia Mobile App Edition was based on this and created by Johan Sydseter and Xavier Godard.

OWASP Cornucopia is open-source and can be downloaded free of charge from the [OWASP Cornucopia Github repository](https://github.com/OWASP/cornucopia/blob/master/README.md#license 'OWASP Cornucopia license [external]'). OWASP Cornucopia is free to use. Except, where otherwise [noted](https://github.com/OWASP/cornucopia/blob/master/README.md#license 'OWASP Cornucopia license [external]'), OWASP Cornucopia is licensed under the Creative Commons Attribution-ShareAlike 4.0 license, so you can copy, distribute and transmit the work, and you can adapt it, and use it commercially, but all provided that you attribute the work and if you alter, transform, or build upon this work, you may distribute the resulting work only under the same or similar license to this one.

OWASP and the OWASP logo are trademarks of the OWASP Foundation.

<img alt="OWASP foundation logo" src="/images/owasp-logo.png" style="max-width: 100%; height: auto; display: block; margin: 0 auto;">
