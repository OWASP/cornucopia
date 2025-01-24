---
date: 20240215
author: ive-verstappen
tags: scrum,agile
hidden: false
description: Three easy ways to go from card to Product Backlog Item. Cornucopia is aimed at the developer, not the security engineer. Therefore, we feel that there should be an easy way to go from identifying a threat or vulnerabiltiy to a Product Backlog Item.
---
# 3 Scenarios for Transforming a Cornucopia Card into a Product Backlog Item

The Owasp Cornucopia card game serves as an engaging tool for development teams to identify potential threats. In a previous post, I outlined the optimal integration of Threat Modeling within the Scrum process using the Owasp Cornucopia game. This post delves into three practical scenarios for converting Cornucopia cards into actionable Product Backlog Items (PBIs).

The Owasp Cornucopia card game offers a developer-focused, lightweight approach to threat modeling, minimizing the complexity often associated with security engineering. Here, I aim to demonstrate 3 straightforward methods for creating effective threat models from each Cornucopia card.

Assuming your team has previously played the Cornucopia game, you should have a list of identified cards, each potentially annotated with reasons for their relevance to your project. The task now is to translate these cards into PBIs within your product backlog.

## Playing Cornucopia: A Practical Scenario

Imagine your team has used three Cornucopia suits: Authentication, Authorization, and Data Validation & Encoding to identify threats pertinent to your project:

- Authentication: 3, 4, 8, 5
- Authorization: 5, 9, Q, K
- Data Validation & Encoding: 2, 7, 8

The next steps involve creating PBIs from these identified cards.

### Prioritizing the Cards

Cornucopia inherently recommends sorting the cards by their value, providing a preliminary order. However, this prioritization can be adjusted based on specific project needs and insights.

1. Authorization-K
2. Authorization-Q
3. Authorization-9
4. Data Validation & Encoding-8
5. Authentication-8
6. Data Validation & Encoding-7
7. Authorization-5
8. Authentication-4
9. Authentication-3
10. Data Validation & Encoding-2

Lets use following three cards for detailed examination:

1. Authorization-K
2. Data Validation & Encoding-8
3. Authentication-4

### Scenario 1: Analyzing Authorization-K

While the development-team assumes that they implement server-side controls, they acknowledged that there is no logging in place that logs changes to the allocation of roles to the users.  You wrote this on the scorecard for Authentication-K:
- "Add Logging to each change of role-allocation for a user".

You simply create the Product Backlog Item: "Add logging to all changes of user-information in the application".

### Scenario 2: Analyzing Data Validation & Encoding-8

Without specific notes for this card, you rely solely on its identified relevance. The steps are as follows:

1. Review the ASVS mapping provided on the card.
2. Reference control 1.1.6 of the ASVS 4.0 standard, emphasizing the need for centralized security controls.

This review highlights the absence of a unified approach to sanitizing input data, prompting the creation of a PBI: "Establish a centralized mechanism for sanitizing all system input data."

**!! Consult the OWASP Cheat Sheet Series Index !!**  
The Cheat Sheet Series offers invaluable insights into securing software development. It's recommended that the Technical Lead reviews the cheat sheets related to identified cards to uncover potential security gaps, benefiting from language-specific secure coding examples.

### Scenario 3: Analyzing Authentication-4

The ease of enumerating user accounts, due to predictable email address patterns, is noted. Despite the inability to alter company email policies, it's decided to acknowledge this threat and seek IT guidance on mitigation strategies. This scenario does not result in a new PBI.

### Prioritizing Product Backlog Items

Security threats should be treated as any other backlog item, with the Technical Lead and Product Owner collaboratively prioritizing the PBIs.

## Guidance from OWASP ASVS

The OWASP ASVS offers detailed insights into each card's security aspects, facilitating a thorough threat analysis and the identification of necessary security features for implementation.

## Conclusion

The Owasp Cornucopia game, through its practical approach and linkage to other OWASP resources, not only aids teams in identifying threats but also in swiftly defining PBIs to enhance application security. Utilizing Cornucopia alongside OWASP ASVS can significantly improve security measures, even for software developers with limited Threat Modeling expertise.

Good Luck!

Ive

Feel free to use the comment section below for feedback or questions.
