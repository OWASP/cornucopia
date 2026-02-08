# CAPEC™ 579: Replace Winlogon Helper DLL

## Description

Winlogon is a part of Windows that performs logon actions. In Windows systems prior to Windows Vista, a registry key can be modified that causes Winlogon to load a DLL on startup. Adversaries may take advantage of this feature to load adversarial code at startup.

Source: [CAPEC™ 579](https://capec.mitre.org/data/definitions/579.html)

