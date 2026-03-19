# CAPEC™ 383: Harvesting Information via API Event Monitoring

## Description

An adversary hosts an event within an application framework and then monitors the data exchanged during the course of the event for the purpose of harvesting any important data leaked during the transactions. One example could be harvesting lists of usernames or userIDs for the purpose of sending spam messages to those users. One example of this type of attack involves the adversary creating an event within the sub-application. Assume the adversary hosts a "virtual sale" of rare items. As other users enter the event, the attacker records via AiTM (CAPEC-94) proxy the user_ids and usernames of everyone who attends. The adversary would then be able to spam those users within the application using an automated script.

Source: [CAPEC™ 383](https://capec.mitre.org/data/definitions/383.html)

## Related ASVS Requirements

ASVS (5.0): [16.3.3](/taxonomy/asvs-5.0/16-security-logging-and-error-handling/03-security-events#V16.3.3), [4.4.1](/taxonomy/asvs-5.0/04-api-and-web-service/04-websocket#V4.4.1), [4.4.2](/taxonomy/asvs-5.0/04-api-and-web-service/04-websocket#V4.4.2), [4.4.3](/taxonomy/asvs-5.0/04-api-and-web-service/04-websocket#V4.4.3), [4.4.4](/taxonomy/asvs-5.0/04-api-and-web-service/04-websocket#V4.4.4), [8.2.2](/taxonomy/asvs-5.0/08-authorization/02-general-authorization-design#V8.2.2), [8.2.3](/taxonomy/asvs-5.0/08-authorization/02-general-authorization-design#V8.2.3), [8.2.4](/taxonomy/asvs-5.0/08-authorization/02-general-authorization-design#V8.2.4)
