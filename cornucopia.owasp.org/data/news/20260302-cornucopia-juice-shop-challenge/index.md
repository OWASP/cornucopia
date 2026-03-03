---
date: 20260302
author: johan-sydseter
tags: owasp,cornucopia,gamification,threat-modeling,security,agile,juice,shop
hidden: false
description: The OWASP Juice Shop and OWASP Cornucopia cheat shee
---

# The OWASP Juice Shop and OWASP Cornucopia cheat sheet

Welcome Junior threat modelers! 

Are you wondering about how OWASP Cornucopia is connected with the OWAP Juice Shop challenges? Here is a list of all the Website App Edition v2.2 cards and how they are connected to the OWASP Juice Shop vulnerabilities. You will also find the threat model that showes you which component is vulnerable and help you to lead a Fun game of OWASP Cornucopia even if you don't have a threat model to use!

## The threat model

First of, here is the [hi-res threat model](threatmodel.png) you should show to your peers. You can also find the [latest drawing](https://github.com/juice-shop/juice-shop/blob/master/threat-model.json) at the OWASP Juice Shop repository. The drawing can be opened up in [OWASP Threat Dragon](https://www.threatdragon.com/) and exported from there.

## The solution

### Components

#### Angular Frontend


  | code | card | description | Juice Box |
  | -------- | -------- | -------- | -------- |
  | Row 1    | Data 1   | Data 1   | Data 1   |
  | Row 2    | Data 2   | Data 1   | Data 1   |
  

- VE2 ([Data validation 2](https://cornucopia.owasp.org/edition/webapp/VE2)): Let us redirect you to one of our crypto currency addresses (see: https://pwning.owasp-juice.shop/companion-guide/latest/appendix/solutions.html#_let_us_redirect_you_to_one_of_our_crypto_currency_addresses)
- VEQ ([Data validation - queen](https://cornucopia.owasp.org/edition/webapp/VEQ)): Use the bonus payload in the DOM XSS challenge (Past an iframe into the search field) (see: https://pwning.owasp-juice.shop/companion-guide/latest/appendix/solutions.html#_use_the_bonus_payload_in_the_dom_xss_challenge)


#### Application Server

- VE2 ([Data validation 2](https://cornucopia.owasp.org/edition/webapp/VE2)): Access a confidential document (Because directory listing not is disabled) (see: https://pwning.owasp-juice.shop/companion-guide/latest/appendix/solutions.html#_access_a_confidential_document)
- AZ3 ([Authorization 3](https://cornucopia.owasp.org/edition/webapp/AZ3)): Access a confidential document (Because directory listing not is disabled) (see: https://pwning.owasp-juice.shop/companion-guide/latest/appendix/solutions.html#_access_a_confidential_document)
- AZ9 ([Authorization 9](https://cornucopia.owasp.org/edition/webapp/AZ3)): Receive a coupon code from the support chatbot (by asking repeatedly) (see: https://pwning.owasp-juice.shop/companion-guide/latest/appendix/solutions.html#_receive_a_coupon_code_from_the_support_chatbot)


#### B2B API

- VE2: ([Data validation 2](https://cornucopia.owasp.org/edition/webapp/VE2)): Provoke an error that is neither very gracefully nor consistently handled (and reveal sensitive information) (see: https://pwning.owasp-juice.shop/companion-guide/latest/appendix/solutions.html#_provoke_an_error_that_is_neither_very_gracefully_nor_consistently_handled)
- AZ3 ([Authorization 3](https://cornucopia.owasp.org/edition/webapp/AZ3)): Find the endpoint that serves usage data to be scraped by a popular monitoring system (see: https://pwning.owasp-juice.shop/companion-guide/latest/appendix/solutions.html#_find_the_endpoint_that_serves_usage_data_to_be_scraped_by_a_popular_monitoring_system).
- C9: ([Cornucopia 9](https://cornucopia.owasp.org/edition/webapp/C9)): Find the endpoint that serves usage data to be scraped by a popular monitoring system (see: https://pwning.owasp-juice.shop/companion-guide/latest/appendix/solutions.html#_find_the_endpoint_that_serves_usage_data_to_be_scraped_by_a_popular_monitoring_system).

#### MarsDB NoSQL DB

### Data flows