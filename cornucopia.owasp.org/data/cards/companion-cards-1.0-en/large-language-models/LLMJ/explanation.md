## Scenario: Ripley's ML component misuse scenario

### Example

Ripley has been paid by Rossum to create a better AI chatbot than Mr. Juice for Rossum's and Tyrell's new juice shop business. As the good developer he is, he researches what Mr. Juice might have done to get its awesome AI chatbot up and running. He finds a social media post where a developer brags about having trained the LLM used by Mr. Juice using a popular ML ecosystem to facilitate training and deployment of ML workloads for Mr. Juice's LLM. After doing some digging he learned that the ML workload cluster has an API that does not support authentication. After a bit of trial and error he is able to reach one of its endpoints called `api/jobs` where he can submit ML jobs to the ML cluster containing arbitrary malicious code. Not long after Mr. Juice's AI chatbot starts to recommend its competitors' juice instead of helping its customers while Rossum and Tyrell are enjoying the brand new AI model they suddenly have acquired.

## Threat Modeling

### STRIDE

This scenario falls into the **Tampering**, **Elevation of Privilege** and **Information Disclosure** categories of STRIDE.
The vulnerability Ripley is taking advantage of is missing access control which belongs to the **Spoofing** category, but the act itself is to **tamper** with the ML ecosystem. That said, he is able to do so by executing arbitrary code by submitting jobs to the ML cluster without having the necessary privileges which means he is also attacking the cluster by **elevating** his own **privileges**. Finally, he has also stolen Mr. Juice's AI model before he poisoned it. Stealing information falls under the **Information Disclosure** category of STRIDE.

### What can go wrong?

Supply chain attacks on large language models can do irreparable damage. It may be possible to fix an AI model after its data has become poisoned, but it's extremely challenging, costly, and often requires complete retraining. A large language model can also be used as a springboard for other types of attacks on the system if an attacker is able to convince it to execute code or actions on behalf of the attacker. As an AI model also connects to vast amounts of data, given that access controls are insufficiently implemented, the model itself can become a tool for data exfiltration of sensitive information as well as getting stolen. The information can, in turn, be used to make users victims of fraud, identity theft, phishing, and malware attacks.
The impact can be financial losses, reputational damage, share price loss, customer churn, lawsuits, loss of sales, fines from data protection due to non-compliance and even financial bankruptcy.

For more things that can go wrong, see [OWASP Top 10 for LLM Applications and Mitre Atlas™](#mapping 'Companion edition requirement mapping [internal]') IDs in the mapping section below and correlate these with the IDs on the [OWASP Top 10 for LLM](https://genai.owasp.org/llm-top-10/) and [Mitre Atlas™](https://atlas.mitre.org/techniques) websites.

### What are we going to do about it?

- Ensure all AI models and model changes are authorized and verified using cryptographic signatures before they are deployed to production.
- Ensure AI models are scrutinized through security and safety verification testing before deployment.
- When deploying changes to AI models, the deployment should be controlled, monitored and possible to rollback or reverse.
- AI model development must follow secure AI development and training practices to avoid compromise.
- When using provider-managed AI models ensure the model with all its dependencies are properly inventoried and possible to identify.
- Ensure that changes to the provider-managed AI models' version or routing trigger security re-evaluation before use in high-risk scenarios.
- Ensure the provider's AI model identifier is logged and that failure to provide the model identifier is logged as well.
- Ensure that no changes to provider-managed AI models are made use of in production without the provider exposing the model identity or change notification information in high-risk scenarios.
- Ensure reward models used in reinforcement learning from human feedback (RLHF) are versioned, cryptographically signed, and integrity-verified before training.
- Initiating fine-tuning or training runs require approval from a person other than the person requesting the run (separation of duties).
- Reinforcement learning from human feedback (RLHF) training stages should include automated detection of reward hacking or reward model over-optimization. Any run must be blocked from promotion if detection thresholds are exceeded.
- In multi-stage fine-tuning pipelines, each stage's output is integrity-verified before the next stage. Intermediate checkpoints should be registered as distinct artifacts to enable rollback.
- High-risk AI operations should require step-up authentication with session re-validation.
- Assess and authenticate third-party model origins and hidden behaviors before any fine-tuning or deployment.
- Allow AI artifact downloads only from organization-approved sources and verify model publisher identity.
- Evaluate external datasets for poisoning and legal compliance, and monitor them throughout their lifecycle.
- Detect AI-specific supply-chain threats through threat intelligence enrichment and incident response readiness.
- Generate and sign detailed AI-specific bills of materials (AI BOMs) so downstream consumers can verify component integrity at deploy time.

For detailed advice on how to mitigate threats related to the card, see the [OWASP AISVS and OWASP AITG](#mapping 'OWASP AISVS and OWASP AITG tests requirements [internal]') IDs in the table below and correlate these with the IDs in the [OWASP AI Security Verification Standard](https://github.com/OWASP/AISVS/tree/main/1.0/en) and [OWASP AI Test Guide](https://github.com/OWASP/www-project-ai-testing-guide/tree/main/Document/content/tests) documentation.