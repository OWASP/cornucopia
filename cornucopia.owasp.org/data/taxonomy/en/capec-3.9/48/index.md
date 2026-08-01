# CAPEC™ 48: Passing Local Filenames to Functions That Expect a URL

## Description

This attack relies on client side code to access local files and resources instead of URLs. When the client browser is expecting a URL string, but instead receives a request for a local file, that execution is likely to occur in the browser process space with the browser's authority to local files. The attacker can send the results of this request to the local files out to a site that they control. This attack may be used to steal sensitive authentication data (either local or remote), or to gain system profile information to launch further attacks.

Source: [CAPEC™ 48](https://capec.mitre.org/data/definitions/48.html)

## Related ASVS Requirements

ASVS (5.0): [1.5.3](/taxonomy/asvs-5.0/01-encoding-and-sanitization/05-safe-deserialization#V1.5.3), [16.3.3](/taxonomy/asvs-5.0/16-security-logging-and-error-handling/03-security-events#V16.3.3), [2.1.1](/taxonomy/asvs-5.0/02-validation-and-business-logic/01-validation-and-business-logic-documentation#V2.1.1), [2.2.1](/taxonomy/asvs-5.0/02-validation-and-business-logic/02-input-validation#V2.2.1), [2.2.2](/taxonomy/asvs-5.0/02-validation-and-business-logic/02-input-validation#V2.2.2), [5.3.2](/taxonomy/asvs-5.0/05-file-handling/03-file-storage#V5.3.2), [5.3.3](/taxonomy/asvs-5.0/05-file-handling/03-file-storage#V5.3.3), [5.4.1](/taxonomy/asvs-5.0/05-file-handling/04-file-download#V5.4.1), [5.4.2](/taxonomy/asvs-5.0/05-file-handling/04-file-download#V5.4.2)
