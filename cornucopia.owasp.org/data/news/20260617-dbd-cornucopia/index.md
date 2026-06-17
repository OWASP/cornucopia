---
date: 20260525
author: johan-sydseter
tags: owasp,cornucopia,gamification,threat-modeling,security,dbd
hidden: false
description: DBD Cornucopia is now available to play online!
---

# DBD Cornucopia is now available to play online!

![DBD Cornucopia](printed_dbd.jpg)



__In development, we are used to understanding threat modelling as a structured method to make applications and other software secure. And in this, “secure” usually means to protect against adverse events and their associated harms as they impact the system (e.g. to maintain availability), its data (e.g. to protect its confidentiality) and the organisation more widely (e.g. to ensure continued operation). OWASP Cornucopia's three editions (Website App, Mobile App and Companion) all help threat modelling from this perspective.__

But assessments of threats can also use different perspectives. Developers may come across privacy impact assessments (PIAs), where threats to users' data and the impact on those users are paramount. PIAs may additionally examine harms to organisations, third parties and wider society.

## [Negative impacts on benefit claimants](https://www.digitalbenefits.uk/number1/)

In recent years, Colin Watson, who created OWASP Cornucopia in 2012, undertook a PhD at Newcastle University, UK. This examined how the digital implementation of e-government services impacts citizens. The research's scope was digitisation of social protection cash payments (in the UK called “welfare benefits”) and those working-age citizens who apply for, and possibly receive, the support payments (in the UK known as “benefit claimants”). The PhD used case studies of Universal Credit (UC), which is an income-related minimum resource payment, and, to a lesser extent, of Personal Independence Payment (PIP), an invalidity-related social protection payment. The research identified how many requirements for digitised services are not defined in government legislation or regulation, leading to what can be somewhat arbitrary “digital discretion” during design, implementation and operation. And many of these decisions can have [negative impacts on benefit claimants](https://www.digitalbenefits.uk/number1/). Following completion of the PhD, Colin Watson gathered together all the harms identified that can arise through the choices made during the software development lifecycle. These are far broader and deeper than the few commonly referred to accessibility matters (which can sometimes also be constrained to concerns about the UI).

## [“Digital Benefits and Disbenefits (DBD Cornucopia)”](https://www.digitalbenefits.uk)

These harms have now also been converted into a Cornucopia-style deck of cards, to help teams identify negative impacts on the service users, and thus to provide requirements which avoid or minimise such harms. The deck is called “Digital Benefits and Disbenefits Cornucopia” (DBD Cornucopia) and uses the same game method.

## [The Card Deck](https://www.digitalbenefits.uk/deck)

Whilst the deck's threat descriptions, harm explanations and examples on the website reference use UK-specific language like “welfare benefit” instead of “social protection payment”, and “claimants” instead of “service users” or “citizens”, the threats are easily understandable for other jurisdictions, and other types of e-government services. Like OWASP Cornucopia, DBD Cornucopia is open source and free to use. It is licensed under the Creative Commons Attribution-ShareAlike 3.0 licence, so you can copy, distribute and transmit the work, and you can adapt it and use it commercially, but all provided that you attribute the work and if you alter, transform, or build upon this work, you may distribute the resulting work only under the same or similar licence to this one. Make your own version!

## [The Online Cornucopia Game Engine - Copi](https://copi.owasp.org)

The original OWASP Cornucopia was primarily comprised of word-processing documents. Due to the efforts in recent years by many generous volunteers and organisations to codify OWASP Cornucopia, DBD Cornucopia's threat data has been added to its repository. This means that, because of the project's [integrated gaming engine Copi](https://copi.owasp.org), the deck is now available for teams to play digitally online.

## [Printing](https://www.digitalbenefits.uk/resources/documents/dbd-deck-1v00c.pdf)

Colin Watson had a small number of DBD Cornucopia decks printed to distribute to UK government departments, charities which campaign in this area, and academics undertaking research in the disciplines of service design and human-computer interaction. The first professionally printed OWASP Cornucopia deck in 2013 was distributed in a box which resembled a pack of cigarettes labelled with health warnings. Acknowledging that idea and the domestic nature of the harms, the physical DBD Cornucopia box is presented in the style of a powdered laundry detergent package, based on the notion that reducing harms is, in some way, cleaning up the e-government service. Sometimes humour is also necessary to counteract harms, and fun can help awareness and encourage use of service-user-oriented threat modelling.

The high-res design files are all available for download and print at [www.digitalbenefits.uk/cornucopia](https://www.digitalbenefits.uk/cornucopia/).

NB: DBD Cornucopia is not an OWASP project. 
