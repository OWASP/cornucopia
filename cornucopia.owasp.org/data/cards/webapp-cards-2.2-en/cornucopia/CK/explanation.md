## Scenario: Grant’s Exploitation for Denial of Service

Imagine a scenario where Grant utilizes an application to deny service to some or all of its users. This occurs due to:

1. **Vulnerabilities to Overload:** The application has weaknesses that can be exploited to overload its resources, such as server bandwidth or processing capacity.

2. **Inadequate Rate Limiting:** The lack of controls on the frequency and volume of user requests allows Grant to send an overwhelming number of requests, leading to service disruptions.

3. **Exploitable Functionalities:** Certain features of the application can be misused to create bottlenecks or consume disproportionate resources.

### Example

Grant targets an online retail platform. He identifies that the site’s search functionality is not rate-limited and requires intensive database queries. By sending rapid and numerous complex search requests, he overloads the server, causing significant slowdowns for other users and eventually leading to a denial of service. This exploitation effectively prevents legitimate users from accessing the website and making purchases.

## Threat Modeling

### STRIDE

The STRIDE category applicable here is **Denial of Service** (DoS).

Grant’s actions prevent legitimate users from accessing the application.
The impact is on availability, which is exactly what **Denial of Service** attacks target.
STRIDE explicitly associates attacks that reduce or eliminate system availability with **Denial of Service**.

### What can go wrong?

Such vulnerabilities can lead to the application becoming unavailable or unresponsive, impacting user experience, and potentially causing financial and reputational damage to the service provider.

For more things that can go wrong, see the [Common Attack Patterns related to this card](#mapping 'Common Attack Patterns related to this card [internal]') in the table below.

### What are you going to do about it?

1. Implement robust rate limiting on user requests, particularly for resource-intensive functionalities.
2. Monitor and optimize the application’s performance to handle high volumes of traffic and processing.
3. Regularly conduct stress tests to identify and address potential denial of service vulnerabilities.
4. Develop and maintain an incident response plan to quickly mitigate and recover from denial of service attacks.

For detailed advice on how to mitigate threats related to the card, see the [ASVS and OWASP Developer Guide requirements ](#mapping 'ASVS and OWASP Developer Guide requirements [internal]') in the table below.
