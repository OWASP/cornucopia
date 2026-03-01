# About

OWASP Cornucopia is a mechanism in the form of a card game to assist software development teams identify security requirements in Agile, conventional and formal development processes. It is language, platform and technology-agnostic.

If you have questions concerning OWASP Cornucopia, please search for it first in our [Q & A section](/questionsandanswers).

If you have other questions, suggestions or ideas please feel free to discuss them on our [email list](https://groups.google.com/a/owasp.org/g/cornucopia-project 'Cornucopia google group [external]') or submit them to our [list of issues](https://github.com/OWASP/cornucopia/issues 'Cornucopia Github repository [external]')  in our repository. If you feel like and have the opportunity to help, do not hesitate to get in touch with us.

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
8. [Play the game](/how-to-play)  to discuss & document security requirements (and to win rounds).
9. Remember, to have fun!

## Mappings

The other driver for Cornucopia was to link the attacks with requirements and verification techniques. An initial aim had been to reference [CWE™](http://cwe.mitre.org/ 'CWE - 
Common Weakness Enumeration [external]') weakness IDs, but these proved too numerous, and instead it was decided to map each card to [CAPEC™](http://capec.mitre.org/ 'CAPEC™ -
Common Attack Pattern Enumeration and Classification (CAPEC) [external]') software attack pattern IDs which themselves are mapped to CWEs, so the desired result is achieved.

Each Website App Edition card is also mapped to the 36 primary security stories in the [SAFECode document](https://safecode.org/resource-secure-development-practices/fundamental-practices-secure-software-development-2/ 'Fundamental Practices for Secure Software Development, Third Edition - SAFECode [external]'), as well as to the OWASP [Developer Guide Web Application Checklist](https://devguide.owasp.org/en/04-design/02-web-app-checklist/ 'OWASP Developer Guide [external]') v2, [ASVS v4.0.3](https://owasp.org/www-project-application-security-verification-standard/ 'OWASP Application Security Verification Standard (ASVS) [external]') and [AppSensor](https://owasp.org/www-project-appsensor/ 'OWASP AppSensor [external]') (application attack detection and response) to help teams create their own security-related stories for use in Agile processes.

Likewise, each Mobile App Edition is mapped to CAPEC™ and the SAFECode stories, but instead of SCP, ASVS and AppSensor, each card is mapped to OWASP's [Mobile Application Security Verification Standard (MASVS) v2.0](https://mas.owasp.org/MASVS/ 'OWASP MASVS (Mobile Application Security Verification Standard [external]') and [Mobile Application Security Testing Guide (MASTG) v2.0](https://mas.owasp.org/MASTG/ 'OWASP Mobile Application Security Testing Guide [external]').

## Other Security Gamification

If you are interested in using gaming for security, also see [Elevation of Privilege: The Threat Modeling Game](https://www.microsoft.com/en-gb/download/details.aspx?id=20303 'Elevation of Privilege (EoP) Threat Modeling Card Game [external]'), [Security Cards](http://securitycards.cs.washington.edu/ 'The Security Cards: A Security Threat Brainstorming Kit [external]') from the University of Washington, the commercial card game [Control-Alt-Hack](http://www.controlalthack.com/ 'Control-Alt-Hack(R) [external]') ([presentation](http://www.youtube.com/watch?v=Kpnvsgiiz8s 'Control-Alt-Hack(TM): White Hat Hacking for Fun and Profit (A Computer Security Card Game) [external]')), [OWASP Snakes and Ladders](https://owasp.org/www-project-snakes-and-ladders 'OWASP Snakes And Ladders [internal]'), [OWASP Cumulus](https://owasp.org/www-project-cumulus/ 'OWASP Cumulus [external]'), [OWASP Top 10 The Game](https://owasp.org/www-project-top-10-the-game 'OWASP Top 10 The Game [external]'), and web application security training tools incorporating gamification such as [OWASP Juice Shop](https://owasp.org/www-project-juice-shop/ 'OWASP JuiceShop  [external]'), [OWASP Security Shepherd](https://owasp.org/www-project-security-shepherd 'OWASP Security Shepard  [external]'), [OWASP WrongSecrets](https://owasp.org/www-project-wrongsecrets/ 'OWASP WrongSecrets [external]') and [ITSEC Games](http://itsecgames.blogspot.co.uk/ 'ITSEC Games [external]').

Additionally, Adam Shostack maintains a list of tabletop security games and related resources at [Tabletop Security Games + Cards](https://shostack.org/games.html 'Tabletop Security Games + Cards [external]').

## Acknowledgements

### Volunteers

Cornucopia is developed, maintained, updated and promoted by a worldwide team of volunteers. The contributors to date have been:

- Ayman Algamal
- Artim Banyte
- Simon Bennetts
- Thomas Berson
- Rishii Bharadhwaj
- Jorun Kristin Bremseth
- Tom Brennan
- Graham Bryant
- Gerardo Mathías Canedo Prendez
- Fabio Cerullo
- Oana Cornea
- Johanna Curiel
- Todd Dahl
- Ruggero DallAglio
- Andrey Danin
- Luis Enriquez
- Darío De Filippis
- André Ferreira
- Ken Ferris
- Norbert Gaspar
- Spyros Gasteratos
- Sebastien Gioria
- Xavier Godard
- Tobias Gondrom
- Timo Goosen
- Anthony Harrison
- Martin Haslinger
- John Herrlin
- Jerry Hoff
- Toby Irvine
- Aashish Kharel
- Marios Kourtesis
- Aleksey Krasnov
- Suresh Krishna
- Adarsh Kumar
- Franck Lacosta
- Mathias Lemaire
- Khushal Malhotra
- Antonis Manaras
- Jim Manico
- Jef Meijvis
- Mark Miller
- Muhammad Awais Mohsin
- Cam Morris
- Christoph Niehoff
- Grant Ongers
- Tanmay Ranjan
- Susana Romaniz
- Ravishankar Sahadevan
- Abhijit Sahoo
- Max Alejandro Gómez Sánchez Vergaray
- Tao Sauvage
- Prasun Srivastav
- Aditya Srivastava
- Johan Sydseter
- Elias Brattli Sørensen
- Mradul Tiwari
- Ive Verstappen
- Sachin Vishwakarma
- Wagner Voltzcontributors 
- Stephen de Vries
- Colin Watson
-  
Additionally, Gerardo Canedo and student volunteers to [OWASP Threat Dragon](https://owasp.org/www-project-threat-dragon/ 'OWASP Threat Dragon [internal]') from the Universidad Católica del Uruguay ([UCU](https://www.ucu.edu.uy/ 'UCU [external]')) who took part in a Coding Challenge to provide integration between Cornucopia and Threat Dragon.

Please let us know if we have missed anyone from this list.

### Others

Adam Shostack and the Microsoft SDL Team for the Elevation of Privilege (EoP) Threat Modelling Game, published under a Creative Commons Attribution license, as the inspiration for Cornucopia and from which many ideas, especially the game theory, were copied.

Keith Turpin and contributors to the “OWASP Secure Coding Practices Quick Reference Guide”, originally donated to OWASP by Boeing Inc, which is used as the primary source of security requirements information to formulate the content of the Website App Edition cards. David Rook for his "Principles of Secure Development", a proponent for following a small repeateable set of proncipals during development rather than focusing on vulnerabilities - an approach which inspired Cornucopia's suit names.

Contributors, supporters, sponsors and volunteers to the OWASP ASVS, AppSensor, Web Framework Security Matrix and MASVS/MASTG projects, Mitre’s Common Attack Pattern Enumeration and Classification (CAPEC™), and SAFECode’s “Practical Security Stories and Security Tasks for Agile Development Environments” which are all used in the cross-references provided.

Playgen for providing an illuminating afternoon seminar on task gamification, and tartanmaker.com for the online tool to help create the original card back pattern.

Travelex UK Limited for donating printable files.

Blackfoot UK Limited for creating and donating print-ready design files, and for distributing printed card decks free of charge.

OWASP Foundation for instigating the creation of an OWASP-branded case and foldable leaflet, and for distributing printed card decks free of charge.

OWASP's past and current employees.

Secure Delivery Ltd for developing and donating Copi, the platform to play Cornucopia and EoP online.

dotNET Lab for creating and donating website code and content, and for donating printed card decks.

Colin Watson as author of OWASP Cornucopia Ecommerce Edition, the original card deck.

## License

OWASP Cornucopia Website App Edition (formerly called Ecommerce Edition) was created by Colin Watson. OWASP Cornucopia Mobile App Edition was based on this and created by Johan Sydseter and Xavier Godard. 

OWASP Cornucopia is open-source and can be downloaded free of charge from the [OWASP Cornucopia Github repository](https://github.com/OWASP/cornucopia/blob/master/README.md#license 'OWASP Cornucopia license [external]'). OWASP Cornucopia is free to use. Except, where otherwise [noted](https://github.com/OWASP/cornucopia/blob/master/README.md#license  'OWASP Cornucopia license [external]'), OWASP Cornucopia is licensed under the Creative Commons Attribution-ShareAlike 4.0 license, so you can copy, distribute and transmit the work, and you can adapt it, and use it commercially, but all provided that you attribute the work and if you alter, transform, or build upon this work, you may distribute the resulting work only under the same or similar license to this one.

OWASP and the OWASP logo are trademarks of the OWASP Foundation.

<img alt="OWASP foundation logo" src="/images/owasp-logo.png" width="500"/>
