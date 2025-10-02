---
date: 20251001
author: johan-sydseter
tags: owasp,cornucopia,gamification,threat-modeling
hidden: false
description: OWASP Cornucopia Website Edition v2.2
---
![OWASP Cornucopia Website Edtion v2.2](threat-modeling-for-security-people.png)

# OWASP Cornucopia Website Edition v2.2

_Shift-left doesn't start with scanning the code for security vulnerabilities; it begins with designing it. Play yourself secure with OWASP Cornucopia Website Edition v2.2_

---

To often the shift-left mantra consists of implementing AI code scanning and AI-generated patches for remediation. Also, don't forget to implement the [AI-powered benchmark for AI-Powered Security Fixes](https://engineering.fb.com/2025/04/29/ai-research/autopatchbench-benchmark-ai-powered-security-fixes/). We're not telling you to stop using these tools, instead, we want to ask ourselves:

- What are we working on?
- What can go wrong?
- What are we going to do about it?
- Did we do a good job?

Source: [Shostack's Four Question Frame for Threat Modeling](https://github.com/adamshostack/4QuestionFrame)

Secure design starts with understanding **what we are working on**, asking **what can go wrong** and **what we are going to do about it**. I'll leave that to the AI-assistants you say?
Before you do, know that the "[2025 GenAI Code Security Report](https://www.veracode.com/blog/ai-generated-code-security-risks/)" from Veracode shows that after a comprehensive analysis of over 100 large language models across 80 coding tasks spanning four programming languages and four critical vulnerability types, only 55% of AI-generated code was secure (AI-Generated Code: A Double-Edged Sword for Developers, 09.09.2025). We don't doubt that, eventually, the machines will take over the world, but in the mean time, don't forget to ask yourself **what can go wrong**.

And what does the industry standard for infosec management say about writing secure code?

If you happen to be ISO 27001 certified and are writing code, you should know that the control you have called: "ISO 27002: 8.28 Secure coding", says that: "Planning and prerequisites before coding should include: ... g) secure design and architecture, including threat modelling".

But, how can you possible do that in an agile and fun way?

Visit [copi.owasp.org](https://copi.owasp.org) and play OWASP Cornucopia, Elevation of MLSec, Elevation of Privilege or OWASP Cumulus with your team.
Games aren't just for fun, they can be serious tools too, and that is what we are doing with [OWASP Cornucopia](https://cornucopia.owasp.org/). We are making threat modeling for everyone, everywhere, and we have a special love for agile teams that want to do continuous threat modeling as part of their development sprints. Don't believe us? See how long-time project contributor Max Alejandro Gómez Sánchez Vergaray has [created a video](https://cornucopia.owasp.org/how-to-play#Gameplay-using-abuse-case-modelling-approach) to explain how he has trained hundreds of teams to use OWASP Cornucopia in abuse case modelling sessions at a major international bank. This approach has scaled to over two-thousand developers to date.

---

<noscript>
    <p>You cannot view this video directly because JavaScript is disabled. Click <a href="https://www.youtube.com/watch?v=XXTPXozIHow" title="How to play OWASP Cornucopia" target="_blank" rel="noopener">here</a> to watch the video on YouTube.</p>
</noscript>
<iframe credentialless anonymous class="how-to-play" frameborder="0" title="Youtube: How to play OWASP Cornucopia"
src="https://www.youtube.com/embed/vLYzId7-ijI?si=yh4vHK7VfO9a5l6s" referrerpolicy="no-referrer" allowfullscreen >
<p>You cannot view this video directly because iframes are disabled. Click <a href="https://www.youtube.com/watch?v=vLYzId7-ijI" title="How to play OWASP Cornucopia" target="_blank" rel="noopener">here</a> to watch the video on YouTube.</p></iframe>

---

In our next version of OWASP Cornucopia Website App Edition version 2.2 we have a special threat for you. We have gathered together all our threat modeling expertise, created threat modeling scenarios for each card and analyzed which STRIDE categories each of these scenarios belong to. If you have bought a [OWASP Cornucopia deck with QR codes from cybersecgames.com](https://cybersecgames.com/products/owasp-cornucopia-2-1-website-app-edition-threat-modeling-cards?variant=55622568903043) you can now give your team advice on threat scenarios, threat vectors, attack patterns, mitigation strategies and STRIDE when playing the game by letting them scan the QR codes on each card. Each scenario follows "[Shostack's Four Question Frame for Threat Modeling](https://github.com/adamshostack/4QuestionFrame?tab=readme-ov-file#shostacks-four-question-frame-for-threat-modeling)" making it easy for your security champions to come up with the threats and mitigations themselves.
In addition, we have added additional CAPEC's that corresponds to each card and added references to the [OWASP Developer Guide's Web Application Checklist](https://devguide.owasp.org/en/04-design/02-web-app-checklist/) that will link your threat modeling to OWASP secure coding practices and the [OWASP Top 10 Proactive controls](https://top10proactive.owasp.org/), this, thanks to Jon Gadson from the OWASP Developer Guide project.

![Both the Mobile App Edition v1.1 and the Website App Edition v2.2 have QR codes that takes you to the OWASP Cornucopia Website for further analysis of threats and mitigations](cornucopia-qr-codes.jpg)

We are just getting started, in fact, this is just the 1. step. We will continue to bring threat modeling to everyone, everywhere, and will continue to do so in the time to come.
Next time we will also talk about the last question: "Did we do a good job?"
Why? Because we want the game to be used in iterative security processes that involves continually adapting security measures in cycles to identify, address, and reassess threats and vulnerabilities, fostering ongoing improvement rather than a one-time fix.
Stay tuned.

## How to use OWASP Cornucopia cards together with the OWASP Cornucopia website

- A - Preparations

  - A1. Obtain a deck, or print your own Cornucopia deck and separate/cut out the cards
  - A2. Identify an application or application process to review; this might be a concept, design or an actual implementation
  - A3. Create a data flow diagram, user stories, or other artefacts to help the review
  - A4. This will help answer the question: **"What are we working on"**
  - A5. Identify and invite a group of 3-6 architects, developers, testers and other business stakeholders together and sit around a table (try to include someone fairly familiar with application security)
  - A6. Have some prizes to hand (gold stars, chocolate, pizza, beer or flowers depending upon your office culture). See our "Prizes and Swags" section for ideas.
- B - Play
    One suit - Cornucopia - acts as trumps. Aces are high (i.e. they beat Kings). It helps if there is someone dedicated to documenting the results who is not playing.
  - B1. Remove the Jokers and a few low-score (2, 3, 4) cards from Cornucopia suit to ensure each player will have the same number of cards
  - B2. Shuffle the pack and deal all the cards
  - B3. To begin, choose a player randomly who will play the first card - they can play any card from their hand except from the trump suit - Cornucopia
  - B4. To play a card, each player must read it out aloud, and explain how (or not) the threat could apply (the player gets a point for attacks that work, and the group thinks it is an actionable bug) - don’t try to think of mitigations at this stage, and don’t exclude a threat just because it is believed it is already mitigated. If you get stuck, use scan the QR codes on the cards or click the "goto" links if playing [Copi](https://copi.owasp.org/) (the online Cornucopia version) and read the **"[What can go wrong?](https://cornucopia.owasp.org/cards/VE2#What-can-go-wrong?)"** section on the card page - someone record the card on the score sheet
  - B5. If a player get stuck, ask them to scan the QR code on the card to access the online card page and read the section called: **"[What can go wrong?](https://cornucopia.owasp.org/cards/VE2#What-can-go-wrong?)"** or click the "more info" links if playing [Copi](https://copi.owasp.org/) (the online Cornucopia version)
  - B6. Play clockwise, each person must play a card in the same way; if you have any card of the matching lead suit you must play one of those, otherwise they can play a card from any other suit. Only a higher card of the same suit, or the trump suit Cornucopia, wins the hand
  - B7. The person who wins the round, leads the next round (i.e. they play first), and thus defines the next lead suit
  - B8. Repeat until all the cards are played
- C - Scoring
    The objective is to identify applicable threats, and win hands (rounds)
  - C1. Score +1 for each card you can identify as a valid threat to the application under consideration
  - C2. Score +1 if you win a round
  - C3. Once all cards have been played, whoever has the most points, wins
- D - Closure
  - D1. Review all the applicable threats and the matching security requirements.
  - D2. Use the QR codes on the cards to access the online card page and read the section called: **["What are we going to do about it?"](https://cornucopia.owasp.org/cards/VE2#What-are-we-going-to-do-about-it?)** or use the "more info" links if playing [Copi](https://copi.owasp.org/)
  - D3. Create user stories, specifications and test cases as required for your development methodology and add them directly into your issue tracking software under what you are working on

---

Uncover the security flaws in your software's design before the bad guys do it for you! Get your team together on a call or in a room and use OWASP Cornucopia Web & Mobile, Elevation of Privilege or Elevation of MLSec and OWASP Cumulus to secure your AI models and Cloud infrastructure respectively and guide your threat modelling at [copi.owasp.org](https://copi.owasp.org), and if you visit our [code repository](https://github.com/OWASP/cornucopia) please give us a star ⭐️.

<noscript>
    <p>You cannot view this video directly because JavaScript is disabled. Click <a href="https://www.youtube.com/watch?v=XXTPXozIHow" title="How to play OWASP Cornucopia" target="_blank" rel="noopener">here</a> to watch the video on YouTube.</p>
</noscript>
<iframe credentialless anonymous class="how-to-play" frameborder="0" title="Youtube: How to play OWASP Cornucopia"
src="https://www.youtube.com/embed/XXTPXozIHow?si=uIi_VXDtSBkS027S" referrerpolicy="no-referrer" allowfullscreen >
<p>You cannot view this video directly because iframes are disabled. Click <a href="https://www.youtube.com/watch?v=XXTPXozIHow" title="How to play OWASP Cornucopia" target="_blank" rel="noopener">here</a> to watch the video on YouTube.</p></iframe>

---

[OWASP Foundation](https://owasp.org "[external]") is a non-profit foundation that envisions a world with no more insecure software. Our mission is to be the global open community that powers secure software through education, tools, and collaboration. We maintain hundreds of open source projects, run industry-leading educational and training conferences, and meet through over 250 chapters worldwide.
