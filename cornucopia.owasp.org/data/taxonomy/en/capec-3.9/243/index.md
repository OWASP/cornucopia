# CAPEC™ 243: XSS Targeting HTML Attributes

## Description

An adversary inserts commands to perform cross-site scripting (XSS) actions in HTML attributes. Many filters do not adequately sanitize attributes against the presence of potentially dangerous commands even if they adequately sanitize tags. For example, dangerous expressions could be inserted into a style attribute in an anchor tag, resulting in the execution of malicious code when the resulting page is rendered. If a victim is tricked into viewing the rendered page the attack proceeds like a normal XSS attack, possibly resulting in the loss of sensitive cookies or other malicious activities.

Source: [CAPEC™ 243](https://capec.mitre.org/data/definitions/243.html)

