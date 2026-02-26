---
date: 20260225
author: christoffer-pedersen
tags: owasp,cornucopia,gamification,threat-modeling,security,agile
hidden: false
description: How OWASP Cornucopia helps software teams develop a security mindset through gamification
---

# Straight to the Ace - Threat Modeling Through Gamification

We all know how important security is for our work in software engineering, but we rarely ever put focus on doing it. The causes are many, e.g., lack of resources, lack of knowledge, or simply it just feels tedious. And since the consequences are only seen when it really goes wrong, it's just one of those things that can be put off.

What I have noticed in my own team, is the lack of a security mindset from start to finish, but also a lack of knowledge. From the design phase, we stay stuck on what we are building, without asking what can go wrong - or what are we going to do about it. In the development phase, we often rely on tools like CodeQL, to tell us if something could make our application vulnerable. And the testing phase, just relies on normal integration or unit testing.

## Discovering OWASP Cornucopia

Back in 2025, I attended the [OWASP Global AppSec](https://owasp.org "[external]") conference, where I learned about the [OWASP Cornucopia](https://cornucopia.owasp.org/) project - a card game that makes use of gamification to help software development teams do threat modeling in an agile way. It's based on Shostack's and Microsoft's game - [Elevation of Privilege](https://shostack.org/games/elevation-of-privilege "[external]"), but is instead more focused on threats that are often seen in web applications. At the same time, OWASP Cornucopia also maps and links every attack to different frameworks and standards like CAPEC, [OWASP ASVS v4.0.3](https://cornucopia.owasp.org/taxonomy/asvs-4.0.3), and more.

## Introducing the Game to the Team

Coming back with this new knowledge, I've started an end-of-month gaming day, where we set aside about two hours to play OWASP Cornucopia. The focus has first and foremost been to learn about threat modeling, and developing a security mindset. We have done this by using the [OWASP Juice Shop](https://owasp.org/www-project-juice-shop/ "[external]") as an example application, instead of basing the threat modeling on our own system. Because the OWASP Juice Shop application is full of vulnerabilities, it makes it easier for beginners to match cards to a specific vulnerability.

## Early Results

We are still in the learning phase, but we are beginning to see a small improvement in the security mindset. For example in code reviews, where a focus on potential vulnerabilities is already starting to show.

## Get Started

If you want to introduce your team to OWASP Cornucopia you can either [print out the cards](/printing) for free, or you can [play it online](https://copi.owasp.org/ "[external]"). If you are new to the game, I suggest you go to the ["How to Play" page](/how-to-play) and watch the video.

---

*This article was originally published on [Medium](https://medium.com/@christofferpedersen/straight-to-the-ace-threat-modeling-through-gamification-9a91eb779456 "[external]").*
