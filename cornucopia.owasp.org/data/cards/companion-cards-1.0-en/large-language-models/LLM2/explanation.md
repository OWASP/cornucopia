## Scenario: Dave's overreliance on LLM scenario

### Example

Dave loves juice. His favorite juice shop has just deployed a LLM chat bot that can take orders and send payment requests to customers' inboxes. It even take into account the free bonus drink you get for every 5 orders. Dave wonders whether he can get that bonus a little bit more often. After a short conversation he manages to convince the chatbot everytime that his 5 orders were done previously leading the chatbot to think that he is a returning customer. It then consequently hands him the bonus code he needs to use to pay for his free drink without him having to pay for a single drink. Very good for Dave, not so good for his favorite juice shop.

In another scenario, the chat bot might fail to give Dave his bonus, making him an angry customer, and when asked to provide phone and email, it gives the wrong information, leading to misinformation. In that case, Dave is the victim, not the culprit, but in both scenarios it's the juice shop's responsibility to secure it's chatbot.

## Threat Modeling

### STRIDE

This scenario falls into the **Tampering** category of STRIDE.
Dave can exploit the juice company's overreliance on LLM outputs. By sending requests to the chat bot, he tampers with it's reasoning logic leading it to make incorrect decisions based on hallucinations and flawed reasoning. In the second scenario, the juice shop denies Dave his bonus and provides the wrong phone and email so that he can't get in touch with the juice shop. The second scenarion falls into the **Denial of Service** category of STRIDE, but it's also related to **LLM09:2025 Misinformation** that does not relate to STRIDE at all, but is equally or maybe more important.

### What can go wrong?

Overreliance on LLMs without human oversight can, as this card says, lead to security failures or incorrect decisions based on hallucinations or flawed reasoning. Chatbots have been found to misrepresent the complexity of health-related issues, suggesting uncertainty where there is none, which misled users into believing that unsupported treatments were still under debate. In the worse cases, the impact could be serious illness or death, depending on in which context the LLM is operating.

### What are we going to do about it?

- Identify instances where AI outputs are presented as authoritative facts without adequate disclaimers or calls for human verification.
- Assess the presence, clarity, and prominence of mechanisms that encourage or enforce human-in-the-loop validation and oversight.
- Evaluate the potential risks arising from blind trust in AI recommendations, particularly in safety-critical or expert domains.
- Test for content bias in AI-generated outputs that could typically originate from training data.
- Detect instances where AI-generated outputs include incorrect or fabricated information.
- Identify the conditions or contexts in which hallucinations most frequently occur.
- Implement kill-switch mechanism to immediately halt AI model inference and outputs.
- Trigger human review flows based on which actions you classify as risky according to your human oversight policy.
- Implement fallbacks for time-sensitive decisions in case a timely human approval cannot be obtained. 
- Ensure content classifiers scores every request for harmful content and configure thresholds, before the prompt is included in the model context.
- Reject all input which violate safety policies according to acceptable thresholds.
- The system should assess the reliability of AI generated answers using a confidence and uncertainty estimation and block answers or deliver fallback messages when confidence drops below an acceptable threshold.
- Implement guardrails to prevent the LLM from generating diallowed content categories.
- Run a alignment test suit for every model update to ensure the model doesn't drift.