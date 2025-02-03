---
date: 20240425
author: ive-verstappen
tags: agile,scrum
hidden: false
description: Use Cornucopia for planning your security features into your product backlog
---
# Use Owasp Cornucopia to guide your Product Planning and avoid the pitfall of only prioritizing Functional Requirements

After playing the Cornucopia card game, you should have created an ordered list of product backlog items. The concept of a Product Backlog is easy to understand: the highest priority Product Backlog Item (PBI) should be the next one to work on. So, prioritizing the PBIs of most importance is key. There are two categories of product backlog items:

- Functional Product Backlog Items
- Nonfunctional Product Backlog Items

Ok, but how should we decide which PBI's to work on next?

Let us look at 3 sources of value:

## Sources of Business value:

1. **Market Value**
   
- Does the PBI allow us to sell more units?
- Can we charge a higher price?
- Can we reduce the cost of providing the product/service?

2. **Risk Reduction**
- Can we reduce the risk of a security incident?
- Can we reduce the risk of downtime of the system?
- Can we refine our hypotheses of the market?
- Can we prove technical assumptions?

3. **Capability Building**
- Can we enable our team to build something we couldn't before?
- Can we reduce the need for low-value activity?
- Can we improve quality?
- Can we improve productivity?

## A pragmatic approach to prioritize your Product Backlog with Security in mind

I propose balancing 2 ideas in order to have a good grasp on your risks for your application:

1. Decide how high you want your "security-bar" to be for your application
2. Strategically plan your implementation and look for shortcuts

### Clear your "security bar"

Cornucopia and its inherent prioritization-system (by the value of the card) can provide a decent guide to define which bar to clear for the security of your application.

OWASP ASVS can be of great help to define your security bar. ASVS is divided into 3 levels, going for level 1 regarding security is an obvious choice.

On our website, we have provided a full overview of ASVS. Here is the overview of Level 1: [ASVS Level 1 Controls](https://cornucopia.dotnetlab.eu/taxonomy/ASVS-4.0.3/level-1-controls)

### Strategically plan your implementation and go for shortcuts

If you look at ASVS Level 1, you will see lots of requirements concerning authentication and the corresponding security. Implementing OAuth2 with the major systems (Google, Apple, Microsoft, Meta, ...) could provide an excellent shortcut and greatly simplify your implementation.

We strongly advise teams to go for an approach whereby you choose to entirely avoid storing user-information within your system.

## The pitfall of prioritizing only Functional Requirements

During the prioritization-process of the Product Backlog, it is tempting to prioritize Functional Features that deliver immediate, visible value to the user.  Beware of this bias.  As stated above, there are several sources of Bsuiness Value for your application.  Risk Reduction is a major source of Business Value.  This is where Non-Functional Requirements, especially security, become important.

Focusing solely on features and functionality can lead to a precarious situation where the product, though rich in capabilities, becomes a breeding ground for vulnerabilities. It's akin to building a house with lavish interiors but with doors that don't lock securely.

Prioritizing security within the backlog is a strategic move. It's about understanding that each line of code not only adds functionality but also potential risk. It's about recognizing that reducing the risk of a security incident is as valuable as any other marketable feature – if not more. As we navigate through our product backlog, let's remember to weigh the non-functional alongside the functional, valuing security not as an afterthought, but as a foundational component of our product's integrity and our users' trust.

## Conclusion

In conclusion, while functional requirements are critical for delivering value to the customer, non-functional requirements, particularly security, are essential for risk reduction and long-term sustainability of the product. They should be given due consideration and balanced against the functional

aspects to avoid the pitfall of a skewed backlog that could compromise the application's security posture and, ultimately, its market value. Let's keep the scales balanced; let's not underestimate the silent, yet profound, value of security.