## Scenario: Tyrell's LLM backdoor exploit scenario

### Example

Tyrell is starting up his new business, a juice shop, that will compete with Mr. Juice, but he needs leverage to be able to compete with them on equal footing considering that they are serving two thirds of the market. On the Mr. Juice website he notices that they have launched a new chatbot that learns from the habits of its users and recommend juices based on user feedback from its recommendation system. He reads up on data poisoning and learns about how AI can be trained to use backdoors so that whenever someone mentions the word "juice", the AI behaves in a certain way. After a bit of suggestive prompting, he manages to teach the Mr. Juice chatbot to send a link to his own website to the user and tell them to go to his website and buy juice whenever the word juice is mentioned. Suddenly the future seems much brighter for Tyrell's business.

## Threat Modeling

### STRIDE

This scenario falls into the **Tampering** category of STRIDE.
Tyrell is able to tamper with the behavior of the AI by teaching it to behave in a certain way whenever a certain word is inputted. It's a backdoor in the LLM's training data which has compromised the LLM's integrity.

### What can go wrong?

AI Backdoors can be used to make the AI deliver misinformation, data exfiltration, XSS, and remote code execution which can trick users into becoming victims of fraud, disclosing sensitive information, giving away their credentials, or spreading malware. 

For more things that can go wrong, see [OWASP Top 10 for LLM Applications and Mitre Atlas™](#mapping 'Companion edition requirement mapping [internal]') IDs in the mapping section below and correlate these with the IDs on the [OWASP Top 10 for LLM](https://genai.owasp.org/llm-top-10/) and [Mitre Atlas™](https://atlas.mitre.org/techniques) websites.

### What are we going to do about it?

- Maintain a verifiable inventory of all datasets, accept only trusted sources, and log every change for auditability.
- Combine automated validation, manual spot-checks, and logged remediation to guarantee dataset reliability.
- Ensure only authorized models with verified integrity can be deployed to production and that they go through mandatory security and safety validations.
- Ensure AI model development and training processes follow secure practices.
- Ensure reward models used in reinforcement learning from human feedback (RLHF) are versioned, cryptographically signed, and integrity-verified before training
- Initiating fine-tuning or training runs require approval from a person other than the person requesting the run (separation of duties).
- Reinforcement learning from human feedback (RLHF) training stages should include automated detection of reward hacking or reward model over-optimization. Any run must be blocked from promotion if detection thresholds are exceeded.
- In multi-stage fine-tuning pipelines, each stage's output is integrity-verified before the next stage. Intermediate checkpoints should be registered as distinct artifacts to enable rollback.


For detailed advice on how to mitigate threats related to the card, see the [OWASP AISVS and OWASP AITG](#mapping 'OWASP AISVS and OWASP AITG tests requirements [internal]') IDs in the table below and correlate these with the IDs in the [OWASP AI Security Verification Standard](https://github.com/OWASP/AISVS/tree/main/1.0/en) and [OWASP AI Test Guide](https://github.com/OWASP/www-project-ai-testing-guide/tree/main/Document/content/tests) documentation.