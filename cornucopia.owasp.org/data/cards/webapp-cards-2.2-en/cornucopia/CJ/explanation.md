## Scenario: Roman’s Exploitation of Outdated Compilation and Configuration Lapses

Envision a scenario where Roman takes advantage of vulnerabilities in an application caused by using outdated compilation tools, insecure default configurations, or a lack of documented security information for operational teams. These issues arise from:

1. **Use of Outdated Compilation Tools:** The application is compiled with tools that are not up-to-date, potentially including known vulnerabilities.

2. **Insecure Default Configuration:** The application’s default configuration settings are not aligned with best security practices.

3. **Lack of Security Documentation:** Essential security information and configurations are not properly documented or communicated to the operational teams responsible for maintaining the application.

### Example

Roman targets an enterprise application compiled with outdated tools, which include known security flaws that haven't been patched. He exploits these vulnerabilities to gain unauthorized access. Additionally, the application’s default settings are insecure, leaving several key security features disabled. Roman leverages these weak points for further exploitation. Furthermore, due to the lack of proper security documentation, the operational team is unaware of specific configurations required to secure the application, leaving critical security gaps that Roman exploits.

## Threat Modeling

### STRIDE

The STRIDE category applicable here is **Tampering**.

The scenario involves exploiting weaknesses introduced during development, compilation, and deployment, such as: outdated tools, insecure default configurations, and missing operational guidance.
The primary impact is that an attacker can manipulate, exploit, or modify the behavior of the application due to these weaknesses.
Although this could also enable unauthorized access, the root cause is the application's susceptibility to manipulation or misuse, which is characteristic of **Tampering**.

### What can go Wrong?

These vulnerabilities can lead to significant security breaches, unauthorized access, and potential exploitation of sensitive data and system functionalities.

### What are you going to do about it?

1. Ensure that all tools used for compiling the application are up-to-date and free from known vulnerabilities.
2. Configure the application with secure settings by default and regularly review these settings to align with evolving security standards. 
3. Create comprehensive security documentation and ensure it is effectively communicated and accessible to all operational teams. 
4. Conduct regular security audits and provide ongoing training to operational teams to keep them informed about security best practices and application-specific requirements.

For detailed advice on how to mitigate threats related to the card, see the [ASVS and OWASP Developer Guide requirements ](#mapping 'ASVS and OWASP Developer Guide requirements [internal]') in the table below.
