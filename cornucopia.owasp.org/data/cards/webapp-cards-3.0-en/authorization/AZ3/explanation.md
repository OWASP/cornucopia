## Scenario: Christian's Indirect Access to Restricted Information

Imagine a scenario where Christian accesses sensitive information, which he should not have direct permission to access, by exploiting other mechanisms or system oversights. Christian is not permitted direct access, but has access to something, that had or has access to sensitive information. He does this by:

1. **Access Through Permitted Mechanisms:** Utilizing systems like search indexers, loggers, or reporting tools, which have broader access privileges. 

2. **Exploiting Cached Data:** Accessing sensitive information that is cached and not adequately protected.

3. **Information Retained Beyond Necessity:** Finding data that is kept longer than necessary and is accessible due to insufficient data lifecycle management.

4. **Other Information Leakage:** Capitalizing on various forms of unintended information exposure within the system.

### Example

Christian discovers that the company’s internal search engine, used for document indexing, caches and displays snippets of sensitive documents. Although he doesn’t have direct access to these documents, the search engine does not enforce the same access controls, allowing him to view confidential information through search results. Additionally, Christian exploits poorly managed data retention policies to access outdated but still sensitive files that should have been deleted or archived.

## Threat Modeling

### STRIDE

This scenario maps primarily to STRIDE: **Information Disclosure**.

**Information Disclosure** occurs when an attacker gains access to data they are not authorized to see.
Christian leverages secondary mechanisms—such as a search indexer, logs, reports, caches, or residual data—to access sensitive information.
The core issue is unauthorized access to confidential information, which fits squarely under **Information Disclosure**.

### What can go wrong?

Such vulnerabilities can lead to unauthorized information access, breaches of confidentiality, and potential compliance issues.

For more things that can go wrong, see the [Common Attack Patterns related to this card](#mapping 'Common Attack Patterns related to this card [internal]') in the table below.

### What are we going to do about it?

Consider all accounts/roles and what access privileges they have, and whether a user in one role can utilize another role. Create an Access Control Policy to document an application's business rules, data types and access authorization criteria and/or processes so that access can be properly provisioned and controlled. This includes identifying access requirements for both the data and system resources.

1. Ensure all systems with broader access, like indexers or loggers, enforce the same access controls as primary data sources.
2. Implement secure caching practices and regular cache clearance to prevent unauthorized data access.
3. Establish and enforce strict data retention policies to minimize the risk of accessing outdated sensitive information.
4. Conduct regular audits to identify and address any potential information leakage.

For detailed advice on how to mitigate threats related to the card, see the [ASVS and OWASP Developer Guide requirements ](#mapping 'ASVS and OWASP Developer Guide requirements [internal]') in the table below.
