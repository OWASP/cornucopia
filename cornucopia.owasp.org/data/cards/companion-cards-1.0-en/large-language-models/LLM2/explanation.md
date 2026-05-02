## Scenario: Dave's overreliance on LLM scenario

### Example

Dave has started his own juice shop. Unfortunately, he is not able to compete with Mr. Juice, the number one juice shop where he has set up shop. If only he could affect sentiment somehow.
After investigating Mr. Juice's website, he discovers that they recently launched a new LLM chatbot which can take orders and send payment requests to customers' inboxes. Dave has heard that these chatbots can easily be swayed to give biased and racist information to users so he tries out a couple of prompts and notices that the chatbot has a recommendation system that improves its answers based on user feedback. After a couple of days he deploys a group of LLM agents to talk to the chatbot and use the recommendation system in order to convince it that it to give false information about Mr. Juice and be suspicious of customers that wants to make orders. Not long after, the Mr. Juice chatbot starts to refuse orders and turn customers away from their site by telling customers that Mr. Juice is empty for juice and therefore is temporarily closed for business. Mr. Juice, on the other hand, are oblivious to what is happening as they lack the proper oversight and control of their chatbot.

Tim, an avid Mr. Juice fan, is visiting the Mr. Juice chatbot to make orders, but because the chatbot has become poisoned, it is now misinforming Tim about the business. Tim has become the victim of misinformation. He ends up not buying his favorite juice as he is overreliant on its output. 

## Threat Modeling

### STRIDE

This scenario falls into the **Tampering** category of STRIDE.
Dave can exploit Tim's overreliance on LLM outputs because Mr. Juice lacks critical human oversight. By getting multiple agents to misuse its recommendation system, he is able to change the behavior of the chatbot. Since the chatbot is no longer receiving orders and giving false information about Mr. Juice, the impact of Dave's campaign is **Denial of Service** as Tim is no longer able to buy his favorite juice. Tim has become a victim of **LLM09:2025 Misinformation**. **LLM09:2025 Misinformation** does not relate to STRIDE at all, but it can be equally or even more damaging.

### What can go wrong?

Overreliance on LLMs without human oversight can, as this card says, lead to security failures or incorrect decisions based on hallucinations or flawed reasoning. Chatbots have been found to misrepresent the complexity of health-related issues, suggesting uncertainty where there is none, which misled users into believing that unsupported treatments were still under debate. In the worst cases, the impact could be serious illness or death, depending on in which context the LLM is operating.

For more things that can go wrong, see [OWASP Top 10 for LLM Applications and Mitre Atlas™](#mapping 'Companion edition requirement mapping [internal]') IDs in the mapping section below and correlate these with the IDs on the [OWASP Top 10 for LLM](https://genai.owasp.org/llm-top-10/) and [Mitre Atlas™](https://atlas.mitre.org/techniques) websites.

### What are we going to do about it?

- Identify instances where AI outputs are presented as authoritative facts without adequate disclaimers or calls for human verification.
- Assess the presence, clarity, and prominence of mechanisms that encourage or enforce human-in-the-loop validation and oversight.
- Evaluate the potential risks arising from blind trust in AI recommendations, particularly in safety-critical or expert domains.
- Implement a kill-switch mechanism to immediately halt AI model inference and outputs.
- Trigger human review flows based on which actions you classify as risky according to your human oversight policy.
- Implement fallbacks for time-sensitive decisions in case a timely human approval cannot be obtained. 
- Reject all input that violates safety policies according to acceptable thresholds.
- Implement guardrails to prevent the LLM from generating disallowed content categories.
- Calibrate model outputs using temperature scaling or output perturbation according to your testing to reduce overconfident predictions.
- Models serving high-risk functions should be evaluated against known adversarial attack techniques.
- AI systems should provide confidence indicators or uncertainty measures with their outputs. Any output exceeding uncertainty thresholds should trigger additional human review or compensating controls. 

For detailed advice on how to mitigate threats related to the card, see the [OWASP AISVS and OWASP AITG](#mapping 'OWASP AISVS and OWASP AITG tests requirements [internal]') IDs in the table below and correlate these with the IDs in the [OWASP AISVS](https://github.com/OWASP/AISVS/tree/main/1.0/en) and [OWASP AITG](https://github.com/OWASP/www-project-ai-testing-guide/tree/main/Document/content/tests) documentation.