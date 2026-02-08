# CAPEC™ 199: XSS Using Alternate Syntax

## Description

An adversary uses alternate forms of keywords or commands that result in the same action as the primary form but which may not be caught by filters. For example, many keywords are processed in a case insensitive manner. If the site's web filtering algorithm does not convert all tags into a consistent case before the comparison with forbidden keywords it is possible to bypass filters (e.g., incomplete black lists) by using an alternate case structure. For example, the "script" tag using the alternate forms of "Script" or "ScRiPt" may bypass filters where "script" is the only form tested. Other variants using different syntax representations are also possible as well as using pollution meta-characters or entities that are eventually ignored by the rendering engine. The attack can result in the execution of otherwise prohibited functionality.

Source: [CAPEC™ 199](https://capec.mitre.org/data/definitions/199.html)

