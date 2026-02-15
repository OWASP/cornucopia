## Scenario: Mike’s Misuse of Application Features

Envision a situation where Mike misuses an application by exploiting valid features in unintended ways. He leverages these features by:

1. **Excessive Speed or Frequency:** Using a feature too quickly or too frequently, beyond its normal operational capacity.

2. **Resource Consumption:** Utilizing features in a way that consumes excessive application resources.

3. **Inducing Race Conditions:** Performing actions in a manner that causes race conditions, where the application's behavior becomes unpredictable due to timing issues.

4. **Over-utilization of Features:** Exploiting a feature to an extent that it negatively impacts the application’s functionality or other users' experiences.

### Example

Mike discovers that an online booking system allows rapid repeated bookings and cancellations without any rate limits. He writes a script that continuously books and cancels appointments, exploiting the system’s lack of controls on the frequency of use. This not only consumes significant server resources, leading to performance degradation, but also creates race conditions that result in double bookings and data inconsistencies.

## Threat Modeling

### STRIDE

This scenario maps primarily to STRIDE: **Tampering**.

The core exploit involves manipulating the application's intended logic and data integrity through exploiting race conditions and misusing functionality. This makes him able to compromise the integrity of the system to produce a state that the system was never designed to allow. By doing so, he may be able to impersonate users through brute-force, transcend security boundaries, access sensitive data, elevate his own privileges, or deny service to others (DoS). Depending on the exploit, he might even be able to do so without anyone noticing. While the main STRIDE category is **Tampering**, the impact could span all the other STRIDE categories.

### What can go wrong?

Such misuse can lead to system overloads, degraded performance, unintended application behaviors, and negative impacts on other users.
Common attacks includes automated threats such as: Account aggregation, Account creation, Ad fraud, CAPTCHA bypass, Carding, Card cracking, Cashing out, Credential cracking, Credential stuffing, Denial of service, Expediting, Fingerprinting, Footprinting, Scalping, Scraping, Skewing, Sniping, Spamming, Token cracking and Vulnerability scanning.

For more things that can go wrong, see the [Common Attack Patterns related to this card](#mapping 'Common Attack Patterns related to this card [internal]') in the table below.

### What are we going to do about it?

1. Implement rate limiting and usage throttling to prevent excessive use of features.
2. Design features with resource consumption and potential misuse in mind, ensuring they can handle unexpected or intensive usage without impacting overall system performance.
3. Regularly monitor application usage patterns to identify and address potential abuses or misuses of features.

For detailed advice on how to mitigate threats related to the card, see the [ASVS and OWASP Developer Guide requirements ](#mapping 'ASVS and OWASP Developer Guide requirements [internal]') in the table below.
