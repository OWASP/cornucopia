let data = {
    "meta": {
      "edition": "ecommerce",
      "component": "cards",
      "language": "EN",
      "version": "1.21"
    },
    "suits": [
      {
        "name": "Data validation & encoding",
        "cards": [
          {
            "id": "DV2",
            "value": "2",
            "desc": "Brian can gather information about the underlying configurations, schemas, logic, code, software, services and infrastructure due to the content of error messages, or poor configuration, or the presence of default installation files or old, test, backup or copies of resources, or exposure of source code"
          },
          {
            "id": "DV3",
            "value": "3",
            "desc": "Robert can input malicious data because the allowed protocol format is not being checked, or duplicates are accepted, or the structure is not being verified, or the individual data elements are not being validated for format, type, range, length and a whitelist of allowed characters or formats"
          },
          {
            "id": "DV4",
            "value": "4",
            "desc": "Dave can input malicious field names or data because it is not being checked within the context of the current user and process"
          },
          {
            "id": "DV5",
            "value": "5",
            "desc": "Jee can bypass the centralized encoding routines since they are not being used everywhere, or the wrong encodings are being used"
          },
          {
            "id": "DV6",
            "value": "6",
            "desc": "Jason can bypass the centralized validation routines since they are not being used on all inputs"
          },
          {
            "id": "DV7",
            "value": "7",
            "desc": "Jan can craft special payloads to foil input validation because the character set is not specified/enforced, or the data is encoded multiple times, or the data is not fully converted into the same format the application uses (e.g. canonicalization) before being validated, or variables are not strongly typed"
          },
          {
            "id": "DV8",
            "value": "8",
            "desc": "Sarah can bypass the centralized sanitization routines since they are not being used comprehensively"
          },
          {
            "id": "DV9",
            "value": "9",
            "desc": "Shamun can bypass input validation or output validation checks because validation failures are not rejected and/or sanitized"
          },
          {
            "id": "DVX",
            "value": "10",
            "desc": "Darío can exploit the trust the application places in a source of data (e.g. user-definable data, manipulation of locally stored data, alteration to state data on a client device, lack of verification of identity during data validation such as Darío can pretend to be Colin)"
          },
          {
            "id": "DVJ",
            "value": "J",
            "desc": "Dennis has control over input validation, output validation or output encoding code or routines so they can be bypassed"
          },
          {
            "id": "DVQ",
            "value": "Q",
            "desc": "Geoff can inject data into a client or device side interpreter because a parameterised interface is not being used, or has not been implemented correctly, or the data has not been encoded correctly for the context, or there is no restrictive policy on code or data includes"
          },
          {
            "id": "DVK",
            "value": "K",
            "desc": "Gabe can inject data into an server-side interpreter (e.g. SQL, OS commands, Xpath, Server JavaScript, SMTP) because a strongly typed parameterised interface is not being used or has not been implemented correctly"
          },
          {
            "id": "DVA",
            "value": "A",
            "desc": "You have invented a new attack against Data Validation and Encoding",
            "misc": "Read more about this topic in OWASP's free Cheat Sheets on Input Validation, XSS Prevention, DOM-based XSS Prevention, SQL Injection Prevention, and Query Parameterization"
          }
        ]
      },
      {
        "name": "Authentication",
        "cards": [
          {
            "id": "AC2",
            "value": "2",
            "desc": "James can undertake authentication functions without the real user ever being aware this has occurred (e.g. attempt to log in, log in with stolen credentials, reset the password) "
          },
          {
            "id": "AC3",
            "value": "3",
            "desc": "Muhammad can obtain a user's password or other secrets such as security questions, by observation during entry, or from a local cache, or from memory, or in transit, or by reading it from some unprotected location, or because it is widely known, or because it never expires, or because the user cannot change her own password"
          },
          {
            "id": "AC4",
            "value": "4",
            "desc": "Sebastien can easily identify user names or can enumerate them"
          },
          {
            "id": "AC5",
            "value": "5",
            "desc": "Javier can use default, test or easily guessable credentials to authenticate, or can use an old account or an account not necessary for the application"
          },
          {
            "id": "AC6",
            "value": "6",
            "desc": "Sven can reuse a temporary password because the user does not have to change it on first use, or it has too long or no expiry, or it does not use an out-of-band delivery method (e.g. post, mobile app, SMS)"
          },
          {
            "id": "AC7",
            "value": "7",
            "desc": "Cecilia can use brute force and dictionary attacks against one or many accounts without limit, or these attacks are simplified due to insufficient complexity, length, expiration and re-use requirements for passwords"
          },
          {
            "id": "AC8",
            "value": "8",
            "desc": "Kate can bypass authentication because it does not fail secure (i.e. it defaults to allowing unauthenticated access)"
          },
          {
            "id": "AC9",
            "value": "9",
            "desc": "Claudia can undertake more critical functions because authentication requirements are too weak (e.g. do not use strong authentication such as two factor), or there is no requirement to re-authenticate for these"
          },
          {
            "id": "ACX",
            "value": "10",
            "desc": "Pravin can bypass authentication controls because a centralized standard, tested, proven and approved authentication module/framework/service, separate to the resource being requested, is not being used"
          },
          {
            "id": "ACJ",
            "value": "J",
            "desc": "Mark can access resources or services because there is no authentication requirement, or it was mistakenly assumed authentication would be undertaken by some other system or performed in some previous action"
          },
          {
            "id": "ACQ",
            "value": "Q",
            "desc": "Jaime can bypass authentication because it is not enforced with equal rigor for all types of authentication functionality (e.g. register, password change, password recovery, log out, administration) or across all versions/channels (e.g. mobile website, mobile app, full website, API, call centre)"
          },
          {
            "id": "ACK",
            "value": "K",
            "desc": "Olga can influence or alter authentication code/routines so they can be bypassed"
          },
          {
            "id": "ACA",
            "value": "A",
            "desc": "You have invented a new attack against Authentication",
            "misc": "Read more about this topic in OWASP's free Authentication Cheat Sheet"
          }
        ]
      },
      {
        "name": "Session management",
        "cards": [
          {
            "id": "SM2",
            "value": "2",
            "desc": "William has control over the generation of session identifiers"
          },
          {
            "id": "SM3",
            "value": "3",
            "desc": "Ryan can use a single account in parallel since concurrent sessions are allowed"
          },
          {
            "id": "SM4",
            "value": "4",
            "desc": "Alison can set session identification cookies on another web application because the domain and path are not restricted sufficiently"
          },
          {
            "id": "SM5",
            "value": "5",
            "desc": "John can predict or guess session identifiers because they are not changed when the user's role alters (e.g. pre and post authentication) and when switching between non-encrypted and encrypted communications, or are not sufficiently long and random, or are not changed periodically"
          },
          {
            "id": "SM6",
            "value": "6",
            "desc": "Gary can take over a user's session because there is a long or no inactivity timeout, or a long or no overall session time limit, or the same session can be used from more than one device/location"
          },
          {
            "id": "SM7",
            "value": "7",
            "desc": "Casey can utilize Adam's session after he has finished, because there is no log out function, or he cannot easily log out, or log out does not properly terminate the session"
          },
          {
            "id": "SM8",
            "value": "8",
            "desc": "Matt can abuse long sessions because the application does not require periodic re-authentication to check if privileges have changed"
          },
          {
            "id": "SM9",
            "value": "9",
            "desc": "Ivan can steal session identifiers because they are sent over insecure channels, or are logged, or are revealed in error messages, or are included in URLs, or are accessible un-necessarily by code which the attacker can influence or alter"
          },
          {
            "id": "SMX",
            "value": "10",
            "desc": "Marce can forge requests because per-session, or per-request for more critical actions, strong random tokens (i.e. anti-CSRF tokens) or similar are not being used for actions that change state"
          },
          {
            "id": "SMJ",
            "value": "J",
            "desc": "Jeff can resend an identical repeat interaction (e.g. HTTP request, signal, button press) and it is accepted, not rejected"
          },
          {
            "id": "SMQ",
            "value": "Q",
            "desc": "Salim can bypass session management because it is not applied comprehensively and consistently across the application"
          },
          {
            "id": "SMK",
            "value": "K",
            "desc": "Peter can bypass the session management controls because they have been self-built and/or are weak, instead of using a standard framework or approved tested module"
          },
          {
            "id": "SMA",
            "value": "A",
            "desc": "You have invented a new attack against Session Management",
            "misc": "Read more about this topic in OWASP's free Cheat Sheets on Session Management, and Cross Site Request Forgery (CSRF) Prevention"
          }
        ]
      },
      {
        "name": "Authorization",
        "cards": [
          {
            "id": "AZ2",
            "value": "2",
            "desc": "Tim can influence where data is sent or forwarded to"
          },
          {
            "id": "AZ3",
            "value": "3",
            "desc": "Christian can access information, which they should not have permission to, through another mechanism that does have permission (e.g. search indexer, logger, reporting), or because it is cached, or kept for longer than necessary, or other information leakage"
          },
          {
            "id": "AZ4",
            "value": "4",
            "desc": "Kelly can bypass authorization controls because they do not fail securely (i.e. they default to allowing access)"
          },
          {
            "id": "AZ5",
            "value": "5",
            "desc": "Chad can access resources (including services, processes, AJAX, Flash, video, images, documents, temporary files, session data, system properties, configuration data, registry settings, logs) he should not be able to due to missing authorization, or due to excessive privileges (e.g. not using the principle of least privilege)"
          },
          {
            "id": "AZ6",
            "value": "6",
            "desc": "Eduardo can access data he does not have permission to, even though he has permission to the form/page/URL/entry point"
          },
          {
            "id": "AZ7",
            "value": "7",
            "desc": "Yuanjing can access application functions, objects, or properties he is not authorized to access"
          },
          {
            "id": "AZ8",
            "value": "8",
            "desc": "Tom can bypass business rules by altering the usual process sequence or flow, or by undertaking the process in the incorrect order, or by manipulating date and time values used by the application, or by using valid features for unintended purposes, or by otherwise manipulating control data"
          },
          {
            "id": "AZ9",
            "value": "9",
            "desc": "Mike can misuse an application by using a valid feature too fast, or too frequently, or other way that is not intended, or consumes the application's resources, or causes race conditions, or over-utilizes a feature"
          },
          {
            "id": "AZX",
            "value": "10",
            "desc": "Richard can bypass the centralized authorization controls since they are not being used comprehensively on all interactions"
          },
          {
            "id": "AZJ",
            "value": "J",
            "desc": "Dinis can access security configuration information, or access control lists"
          },
          {
            "id": "AZQ",
            "value": "Q",
            "desc": "Christopher can inject a command that the application will run at a higher privilege level"
          },
          {
            "id": "AZK",
            "value": "K",
            "desc": "Ryan can influence or alter authorization controls and permissions, and can therefore bypass them"
          },
          {
            "id": "AZA",
            "value": "A",
            "desc": "You have invented a new attack against Authorization",
            "misc": "Read more about this topic in OWASP's Development and Testing Guides"
          }
        ]
      },
      {
        "name": "Cryptography",
        "cards": [
          {
            "id": "CR2",
            "value": "2",
            "desc": "Kyun can access data because it has been obfuscated rather than using an approved cryptographic function"
          },
          {
            "id": "CR3",
            "value": "3",
            "desc": "Axel can modify transient or permanent data (stored or in transit), or source code, or updates/patches, or configuration data, because it is not subject to integrity checking"
          },
          {
            "id": "CR4",
            "value": "4",
            "desc": "Paulo can access data in transit that is not encrypted, even though the channel is encrypted"
          },
          {
            "id": "CR5",
            "value": "5",
            "desc": "Kyle can bypass cryptographic controls because they do not fail securely (i.e. they default to unprotected)"
          },
          {
            "id": "CR6",
            "value": "6",
            "desc": "Romain can read and modify unencrypted data in memory or in transit (e.g. cryptographic secrets, credentials, session identifiers, personal and commercially-sensitive data), in use or in communications within the application, or between the application and users, or between the application and external systems"
          },
          {
            "id": "CR7",
            "value": "7",
            "desc": "Gunter can intercept or modify encrypted data in transit because the protocol is poorly deployed, or weakly configured, or certificates are invalid, or certificates are not trusted, or the connection can be degraded to a weaker or un-encrypted communication"
          },
          {
            "id": "CR8",
            "value": "8",
            "desc": "Eoin can access stored business data (e.g. passwords, session identifiers, PII, cardholder data) because it is not securely encrypted or securely hashed"
          },
          {
            "id": "CR9",
            "value": "9",
            "desc": "Andy can bypass random number generation, random GUID generation, hashing and encryption functions because they have been self-built and/or are weak"
          },
          {
            "id": "CRX",
            "value": "10",
            "desc": "Susanna can break the cryptography in use because it is not strong enough for the degree of protection required, or it is not strong enough for the amount of effort the attacker is willing to make"
          },
          {
            "id": "CRJ",
            "value": "J",
            "desc": "Justin can read credentials for accessing internal or external resources, services and others systems because they are stored in an unencrypted format, or saved in the source code"
          },
          {
            "id": "CRQ",
            "value": "Q",
            "desc": "Randolph can access or predict the master cryptographic secrets"
          },
          {
            "id": "CRK",
            "value": "K",
            "desc": "Dan can influence or alter cryptography code/routines (encryption, hashing, digital signatures, random number and GUID generation) and can therefore bypass them"
          },
          {
            "id": "CRA",
            "value": "A",
            "desc": "You have invented a new attack against Cryptography",
            "misc": "Read more about this topic in OWASP's free Cheat Sheets on Cryptographic Storage, and Transport Layer Protection"
          }
        ]
      },
      {
        "name": "Cornucopia",
        "cards": [
          {
            "id": "CO2",
            "value": "2",
            "desc": "Lee can bypass application controls because dangerous/risky programming language functions have been used instead of safer alternatives, or there are type conversion errors, or because the application is unreliable when an external resource is unavailable, or there are race conditions, or there are resource initialization or allocation issues, or overflows can occur"
          },
          {
            "id": "CO3",
            "value": "3",
            "desc": "Andrew can access source code, or decompile, or otherwise access business logic to understand how the application works and any secrets contained"
          },
          {
            "id": "CO4",
            "value": "4",
            "desc": "Keith can perform an action and it is not possible to attribute it to him"
          },
          {
            "id": "CO5",
            "value": "5",
            "desc": "Larry can influence the trust other parties including users have in the application, or abuse that trust elsewhere (e.g. in another application)"
          },
          {
            "id": "CO6",
            "value": "6",
            "desc": "Aaron can bypass controls because error/exception handling is missing, or is implemented inconsistently or partially, or does not deny access by default (i.e. errors should terminate access/execution), or relies on handling by some other service or system"
          },
          {
            "id": "CO7",
            "value": "7",
            "desc": "Mwengu's actions cannot be investigated because there is not an adequate accurately time-stamped record of security events, or there is not a full audit trail, or these can be altered or deleted by Mwengu, or there is no centralized logging service"
          },
          {
            "id": "CO8",
            "value": "8",
            "desc": "David can bypass the application to gain access to data because the network and host infrastructure, and supporting services/applications, have not been securely configured, the configuration rechecked periodically and security patches applied, or the data is stored locally, or the data is not physically protected"
          },
          {
            "id": "CO9",
            "value": "9",
            "desc": "Michael can bypass the application to gain access to data because administrative tools or administrative interfaces are not secured adequately"
          },
          {
            "id": "COX",
            "value": "10",
            "desc": "Xavier can circumvent the application's controls because code frameworks, libraries and components contain malicious code or vulnerabilities (e.g. in-house, commercial off the shelf, outsourced, open source, externally-located)"
          },
          {
            "id": "COJ",
            "value": "J",
            "desc": "Roman can exploit the application because it was compiled using out-of-date tools, or its configuration is not secure by default, or security information was not documented and passed on to operational teams"
          },
          {
            "id": "COQ",
            "value": "Q",
            "desc": "Jim can undertake malicious, non-normal, actions without real-time detection and response by the application"
          },
          {
            "id": "COK",
            "value": "K",
            "desc": "Gareth can utilize the application to deny service to some or all of its users"
          },
          {
            "id": "COA",
            "value": "A",
            "desc": "You have invented a new attack of any type",
            "misc": "Read more about application security in OWASP's free Guides on Requirements, Development, Code Review and Testing, the Cheat Sheet series, and the Open Software Assurance Maturity Model"
          }
        ]
      },
      {
        "name": "Wild Card",
        "cards": [
          {
            "id": "JOA",
            "value": "JokerA",
            "card": "Joker",
            "desc": "Alice can utilize the application to attack users' systems and data",
            "misc": "Have you thought about becoming an individual OWASP member? All tools, guidance and local meetings are free for everyone, but individual membership helps support OWASP's work"
          },
          {
            "id": "JOB",
            "value": "JokerB",
            "card": "Joker",
            "desc": "Bob can influence, alter or affect the application so that it no longer complies with legal, regulatory, contractual or other organizational mandates",
            "misc": "Examine vulnerabilities and discover how they can be fixed using training applications in the free OWASP Broken Web Applications VM, or using the online challenges in the free Hacking Lab"
          }
        ]
      }
    ],
    "paragraphs": [
      {
        "name": "Common",
        "sentences": [
          {
            "value": "NoCard",
            "text": "No Card"
          },
          {
            "value": "Title",
            "text": "Ecommerce Website Edition v1.21-EN"
          },
          {
            "value": "Title_full",
            "text": "OWASP Cornucopia Ecommerce Website Edition v1.21-EN"
          },
          {
            "value": "T00010",
            "text": "OWASP Cornucopia is a mechanism to assist software development teams identify security requirements in Agile, conventional and formal development processes."
          },
          {
            "value": "T00020",
            "text": "Author"
          },
          {
            "value": "T00030",
            "text": "Project Leaders"
          },
          {
            "value": "T00040",
            "text": "Reviewers"
          },
          {
            "value": "T00100",
            "text": "Acknowledgments"
          },
          {
            "value": "T00110",
            "text": "Microsoft SDL Team for the Elevation of Privilege Threat Modelling Game, published under a Creative Commons Attribution license, as the inspiration for Cornucopia and from which many ideas, especially the game theory, were copied."
          },
          {
            "value": "T00120",
            "text": "Keith Turpin and contributors to the “OWASP Secure Coding Practices - Quick Reference Guide”, originally donated to OWASP by Boeing, which is used as the primary source of security requirements information to formulate the content of the cards."
          },
          {
            "value": "T00130",
            "text": "Contributors, supporters, sponsors and volunteers to the OWASP ASVS, AppSensor and Web Framework Security Matrix projects, Mitre’s Common Attack Pattern Enumeration and Classification (CAPEC), and SAFECode’s “Practical Security Stories and Security Tasks for Agile Development Environments” which are all used in the cross-references provided."
          },
          {
            "value": "T00140",
            "text": "Playgen for providing an illuminating afternoon seminar on task gamification, and tartanmaker.com for the online tool to help create the card back pattern."
          },
          {
            "value": "T00150",
            "text": "Blackfoot UK Limited for creating and donating print-ready design files, Tom Brennan and the OWASP Foundation for instigating the creation of an OWASP-branded box and leaflet, and OWASP employees, especially Kate Hartmann, for managing the ordering, stocking and despatch of printed card decks."
          },
          {
            "value": "T00160",
            "text": "Oana Cornea and other participants at the AppSec EU 2015 project summit for their help in creating the demonstration video."
          },
          {
            "value": "T00170",
            "text": "Colin Watson as author and co-project leader with Grant Ongers, along with other OWASP volunteers who have helped in many ways."
          },
          {
            "value": "T00180",
            "text": "OWASP does not endorse or recommend commercial products or services © 2012-2016 OWASP Foundation This document is licensed under the Creative Commons Attribution-ShareAlike 3.0 license"
          },
          {
            "value": "T00200",
            "text": "Introduction"
          },
          {
            "value": "T00210",
            "text": "The idea behind Cornucopia is to help development teams, especially those using Agile methodologies, to identify application security requirements and develop security-based user stories."
          },
          {
            "value": "T00220",
            "text": "Although the idea had been waiting for enough time to progress it, the final motivation came when SAFECode published its Practical Security Stories and Security Tasks for Agile Development Environments in July 2012."
          },
          {
            "value": "T00230",
            "text": "The Microsoft SDL team had already published its super Elevation of Privilege: The Threat Modeling Game (EoP) but that did not seem to address the most appropriate kind of issues that web application development teams mostly have to address."
          },
          {
            "value": "T00240",
            "text": "EoP is a great concept and game strategy, and was published under a Creative Commons Attribution License."
          },
          {
            "value": "T00250",
            "text": "Cornucopia Ecommerce Website Edition is based the concepts and game ideas in EoP, but those have been modified to be more relevant to the types of issues ecommerce website developers encounter."
          },
          {
            "value": "T00260",
            "text": "It attempts to introduce threat-modelling ideas into development teams that use Agile methodologies, or are more focused on web application weaknesses than other types of software vulnerabilities or are not familiar with STRIDE and DREAD."
          },
          {
            "value": "T00270",
            "text": "Cornucopia Ecommerce Website Edition is referenced as an information resource in the PCI Security Standard Council’s Information Supplement PCI DSS E-commerce Guidelines, v2, January 2013."
          },
          {
            "value": "T00300",
            "text": "The card deck (pack)"
          },
          {
            "value": "T00310",
            "text": "Instead of EoP’s STRIDE suits (sets of cards with matching designs), Cornucopia suits are based on the structure of the OWASP Secure Coding Practices - Quick Reference Guide (SCP), but with additional consideration of sections in the OWASP Application Security Verification Standard, the OWASP Testing Guide and David Rook’s Principles of Secure Development. "
          },
          {
            "value": "T00320",
            "text": "These provided five suits, and a sixth called “Cornucopia” was created for everything else: "
          },
          {
            "value": "T00330",
            "text": "Data validation and encoding (VE)"
          },
          {
            "value": "T00340",
            "text": "Authentication (AT)"
          },
          {
            "value": "T00350",
            "text": "Session Management (SM)"
          },
          {
            "value": "T00360",
            "text": "Authorization (AZ)"
          },
          {
            "value": "T00370",
            "text": "Cryptography (CR)"
          },
          {
            "value": "T00380",
            "text": "Cornucopia (C)"
          },
          {
            "value": "T00390",
            "text": "Smilar to poker-playing cards, each suit contains 13 cards (Ace, 2-10, Jack, Queen and King) but, unlike EoP, there are also two Joker cards."
          },
          {
            "value": "T00400",
            "text": "The content was mainly drawn from the SCP."
          },
          {
            "value": "T00500",
            "text": "Mappings"
          },
          {
            "value": "T00510",
            "text": "The other driver for Cornucopia is to link the attacks with requirements and verification techniques."
          },
          {
            "value": "T00520",
            "text": "An initial aim had been to reference CWE weakness IDs, but these proved too numerous, and instead it was decided to map each card to CAPEC software attack pattern IDs which themselves are mapped to CWEs, so the desired result is achieved."
          },
          {
            "value": "T00530",
            "text": "Each card is also mapped to the 36 primary security stories in the SAFECode document, as well as to the OWASP SCP v2, ASVS v3.0.1 and AppSensor (application attack detection and response) to help teams create their own security-related stories for use in Agile processes."
          },
          {
            "value": "T00600",
            "text": "Game strategy"
          },
          {
            "value": "T00610",
            "text": "Apart from the content differences, the game rules are virtually identical to those for EoP."
          },
          {
            "value": "T00700",
            "text": "Printing the cards"
          },
          {
            "value": "T00710",
            "text": "Check the Cornucopia project page for how to obtain pre-printed decks on glossy card."
          },
          {
            "value": "T00720",
            "text": "The cards can be printed from this document in black & white but are more effective in color."
          },
          {
            "value": "T00730",
            "text": "The cards in the later pages of this document have been laid out to fit on one type of pre-scored business A4 card sheets. "
          },
          {
            "value": "T00740",
            "text": "This appeared to be the quickest way to initially provide to create playing cards quickly. "
          },
          {
            "value": "T00750",
            "text": "Avery product codes C32015 and C32030 have been tested successfully, but any 10 up 85mm x 54 mm cards on A4 paper should work with a little adjustment."
          },
          {
            "value": "T00760",
            "text": "Other stationery suppliers like Ryman and Sigel produce similar sheets"
          },
          {
            "value": "T00770",
            "text": "These card sheets are not inexpensive, so care should be taken in deciding what to print and using what media and printer type."
          },
          {
            "value": "T00780",
            "text": "The cards can of course just be printed on any size of paper or card and then cut-up manually, or a commercial printer would be able to print larger volumes and cut the cards to size. "
          },
          {
            "value": "T00790",
            "text": "The cut lines are shown on the penultimate page of this document, but Avery also produce a landscape A4 template (A-0017-01_L.doc) that can be used as a guide."
          },
          {
            "value": "T00800",
            "text": "Printing and cutting up can take an hour or so, and using a faster printer helps."
          },
          {
            "value": "T00810",
            "text": "Try to print add higher quality to increase legibility."
          },
          {
            "value": "T00820",
            "text": "An optional card back design (in OWASP tartan) has been provided as the last page of this document."
          },
          {
            "value": "T00830",
            "text": "There is no special alignment needed. "
          },
          {
            "value": "T00840",
            "text": "Dual-sided printing needs special care taken. "
          },
          {
            "value": "T00850",
            "text": "You could customize the card faces or the backs for your own organization’s preferences."
          },
          {
            "value": "T00900",
            "text": "Customization"
          },
          {
            "value": "T00910",
            "text": "After you have used Cornucopia a few times, you may feel that some cards are less relevant to your applications, or the threats are different for your organization."
          },
          {
            "value": "T00920",
            "text": "Edit this document yourself to make the cards more suitable for your teams, or create new decks completely."
          },
          {
            "value": "T01000",
            "text": "Provide feedback"
          },
          {
            "value": "T01010",
            "text": "If you have ideas or feedback on the use of OWASP Cornucopia, please share them."
          },
          {
            "value": "T01020",
            "text": "Even better if you create alternative versions of the cards, or produce professional print-ready versions, please share that with the volunteers who created this edition and with the wider application development and application security community."
          },
          {
            "value": "T01030",
            "text": "The best place to use to discuss or contribute is the mailing list for the OWASP project:"
          },
          {
            "value": "T01040",
            "text": "•Mailing list"
          },
          {
            "value": "T01050",
            "text": "•Project home page"
          },
          {
            "value": "T01060",
            "text": "All OWASP documents and tools are free to download and use."
          },
          {
            "value": "T01070",
            "text": "OWASP Cornucopia is licensed under the Creative Commons Attribution-ShareAlike 3.0 license."
          },
          {
            "value": "T01100",
            "text": "Instructions"
          },
          {
            "value": "T01110",
            "text": "The text on each card describes an attack, but the attacker is given a name, which are unique across all the cards."
          },
          {
            "value": "T01120",
            "text": "The name can represent a computer system (e.g. the database, the file system, another application, a related service, a botnet), an individual person (e.g. a citizen, a customer, a client, an employee, a criminal, a spy), or even a group of people (e.g. a competitive organization, activists with a common cause)."
          },
          {
            "value": "T01130",
            "text": "The attacker might be remote in some other device/location, or local/internal with access to the same device, host or network as the application is running on."
          },
          {
            "value": "T01140",
            "text": "The attacker is always named at the start of each description"
          },
          {
            "value": "T01150",
            "text": "An example is:"
          },
          {
            "value": "T01160",
            "text": "William has control over the generation of session identifiers."
          },
          {
            "value": "T01170",
            "text": "This means the attacker (William) can create new session identifiers that the application accepts."
          },
          {
            "value": "T01180",
            "text": "The attacks were primarily drawn from the security requirements listed in the SCP, v2 but then supplemented with verification objectives from the OWASP “Application Security Verification Standard for Web Applications”, the security focused stories in SAFECode’s “Practical Security Stories and Security Tasks for Agile Development Environments”, and finally a review of the cards in EOP."
          },
          {
            "value": "T01190",
            "text": "Further guidance about each card is available in the online Wiki Deck at "
          },
          {
            "value": "T01200",
            "text": "Lookups between the attacks and five resources are provided on most cards:"
          },
          {
            "value": "T01210",
            "text": "Requirements in “Secure Coding Practices (SCP) - Quick Reference Guide”, v2, OWASP, November 2010 "
          },
          {
            "value": "T01220",
            "text": "Verification IDs in “Application Security Verification Standard (ASVS) for Web Applications”, OWASP, v3.0.1, 2016 (excluding sections 18 and 19)"
          },
          {
            "value": "T01230",
            "text": "Attack detection points IDs in “AppSensor”, OWASP, August 2010-2015"
          },
          {
            "value": "T01240",
            "text": "IDs in “Common Attack Pattern Enumeration and Classification (CAPEC)”, v2.8, Mitre Corporation, November 2015"
          },
          {
            "value": "T01250",
            "text": "Security-focused stories in 'Practical Security Stories and Security Tasks for Agile Development Environments', SAFECode, July 2012"
          },
          {
            "value": "T01260",
            "text": "A look-up means the attack is included within the referenced item, but does not necessarily encompass the whole of its intent. "
          },
          {
            "value": "T01270",
            "text": "For structured data like CAPEC, the most specific reference is provided but sometimes a cross-reference is provided that also has more specific (child) examples."
          },
          {
            "value": "T01280",
            "text": "There are no lookups on the six Aces and two Jokers. "
          },
          {
            "value": "T01290",
            "text": "Instead these cards have some general tips in italicized text."
          },
          {
            "value": "T01300",
            "text": "It is possible to play Cornucopia in many different ways. "
          },
          {
            "value": "T01310",
            "text": "Here is one way, demonstrated online in a video at https://youtu.be/i5Y0akWj31k , which uses the new (May 2015) score/record sheet at https://www.owasp.org/index.php/File:Cornucopia-scoresheet.pdf"
          },
          {
            "value": "T01400",
            "text": "A - Preparations"
          },
          {
            "value": "T01410",
            "text": "A1. Obtain a deck, or print your own deck of Cornucopia cards (see page 2 of this document) and separate/cut out the cards"
          },
          {
            "value": "T01420",
            "text": "A2. Identify an application or application process to review; this might be a concept, design or an actual implementation"
          },
          {
            "value": "T01430",
            "text": "A3. Create a data flow diagram, user stories, or other artefacts to help the review"
          },
          {
            "value": "T01440",
            "text": "A4. Identify and invite a group of 3-6 architects, developers, testers and other business stakeholders together and sit around a table (try to include someone fairly familiar with application security)"
          },
          {
            "value": "T01450",
            "text": "A5. Have some prizes to hand (gold stars, chocolate, pizza, beer or flowers depending upon your office culture)"
          },
          {
            "value": "T01500",
            "text": "B - Play"
          },
          {
            "value": "T01510",
            "text": "One suit - Cornucopia - acts as trumps."
          },
          {
            "value": "T01520",
            "text": "Aces are high (i.e. they beat Kings)."
          },
          {
            "value": "T01530",
            "text": "It helps if there is a non-player to document the issues and scores."
          },
          {
            "value": "T01540",
            "text": "B1. Remove the Jokers and a few low-score (2, 3, 4) cards from Cornucopia suit to ensure each player will have the same number of cards"
          },
          {
            "value": "T01550",
            "text": "B2. Shuffle the deck and deal all the cards"
          },
          {
            "value": "T01560",
            "text": "B3. To begin, choose a player randomly who will play the first card - they can play any card from their hand except from the trump suit - Cornucopia"
          },
          {
            "value": "T01570",
            "text": "B4. To play a card, each player must read it out aloud, and explain (see the online Wiki Deck for tips) how the threat could apply (the player gets a point for attacks that might work which the group thinks is an actionable bug) - do not try to think of mitigations at this stage, and do not exclude a threat just because of a belief that it is already mitigated - someone note the card and record the issues raised"
          },
          {
            "value": "T01580",
            "text": "B5. Play clockwise, each person must play a card in the same way; if you have any card of the matching lead suit you must play one of those, otherwise they can play a card from any other suit. "
          },
          {
            "value": "T01590",
            "text": "Only a higher card of the same suit, or the highest card in the trump suit Cornucopia, wins the hand."
          },
          {
            "value": "T01600",
            "text": "B6. The person who wins the round, leads the next round (i.e. they play first), and thus defines the next lead suit"
          },
          {
            "value": "T01610",
            "text": "B7. Repeat until all the cards are played"
          },
          {
            "value": "T01700",
            "text": "C - Scoring"
          },
          {
            "value": "T01710",
            "text": "The objective is to identify applicable threats, and win hands (rounds):"
          },
          {
            "value": "T01720",
            "text": "C1. Score +1 for each card you can identify as a valid threat to the application under consideration"
          },
          {
            "value": "T01730",
            "text": "C2. Score +1 if you win a round"
          },
          {
            "value": "T01740",
            "text": "C3. Once all cards have been played, whoever has the most points wins"
          },
          {
            "value": "T01800",
            "text": "D - Closure"
          },
          {
            "value": "T01810",
            "text": "D1. Review all the applicable threats and the matching security requirements"
          },
          {
            "value": "T01820",
            "text": "D2. Create user stories, specifications and test cases as required for your development methodology."
          },
          {
            "value": "T01900",
            "text": "Alternative game rules"
          },
          {
            "value": "T01910",
            "text": "If you are new to the game, remove the Aces and two Joker cards to begin with."
          },
          {
            "value": "T01920",
            "text": "Add the Joker cards back in once people become more familiar with the process."
          },
          {
            "value": "T01930",
            "text": "Apart from the “trumps card game” rules described above which are very similar to the EoP, the deck can also be played as the “twenty-one card game” (also known as “pontoon” or “blackjack”) which normally reduces the number of cards played in each round."
          },
          {
            "value": "T01940",
            "text": "Practice on an imaginary application, or even a future planned application, rather than trying to find fault with existing applications until the participants are happy with the usefulness of the game."
          },
          {
            "value": "T01950",
            "text": "Consider just playing with one suit to make a shorter session – but try to cover all the suits for every project. "
          },
          {
            "value": "T01960",
            "text": "Or even better just play one hand with some pre-selected cards, and score only on the ability to identify security requirements. "
          },
          {
            "value": "T01970",
            "text": "Perhaps have one game of each suit each day for a week or so, if the participants cannot spare long enough for a full deck."
          },
          {
            "value": "T01980",
            "text": "Some teams have preferred to play a full hand of cards, and then discuss what is on the cards after each round (instead of after each person plays a card)."
          },
          {
            "value": "T01990",
            "text": "Another suggestion is that if a player fails to identify the card is relevant, allow other players to suggest ideas, and potentially let them gain the point for the card. "
          },
          {
            "value": "T02000",
            "text": "Consider allowing extra points for especially good contributions."
          },
          {
            "value": "T02010",
            "text": "You can even play by yourself. "
          },
          {
            "value": "T02020",
            "text": "Just use the cards to act as thought-provokers. "
          },
          {
            "value": "T02030",
            "text": "Involving more people will be beneficial though."
          },
          {
            "value": "T02040",
            "text": "In Microsoft's EoP guidance, they recommend cheating as a good game strategy."
          },
          {
            "value": "T02100",
            "text": "Development framework-specific modified card decks"
          },
          {
            "value": "T02110",
            "text": "At the end of 2012, the OWASP Framework Security Matrix was published which documents built in security controls in some commonly used languages and frameworks for web and mobile application development."
          },
          {
            "value": "T02120",
            "text": "With certain provisos it is useful to consider how using these controls can simplify the identification of additional requirements – provided of course the controls are included, enabled and configured correctly."
          },
          {
            "value": "T02130",
            "text": "Consider removing the following cards from the decks if you are confidence they are addressed by the way you are using the language/framework. "
          },
          {
            "value": "T02140",
            "text": "Items in parentheses are “maybes”."
          },
          {
            "value": "T02200",
            "text": "Internal coding standards and libraries"
          },
          {
            "value": "T02210",
            "text": "Add your own list of excluded cards based on your organisation’s coding standards (provided they are confirmed by appropriate verification steps in the development lifecycle)."
          },
          {
            "value": "T02220",
            "text": "Your coding standards and libraries"
          },
          {
            "value": "T02230",
            "text": "Data validation and encoding"
          },
          {
            "value": "T02240",
            "text": "[your list]"
          },
          {
            "value": "T02250",
            "text": "Authentication"
          },
          {
            "value": "T02260",
            "text": "[your list]"
          },
          {
            "value": "T02270",
            "text": "Session management"
          },
          {
            "value": "T02280",
            "text": "[your list]"
          },
          {
            "value": "T02290",
            "text": "Authorization"
          },
          {
            "value": "T02300",
            "text": "[your list]"
          },
          {
            "value": "T02310",
            "text": "Cryptography"
          },
          {
            "value": "T02320",
            "text": "[your list]"
          },
          {
            "value": "T02330",
            "text": "Cornucopia"
          },
          {
            "value": "T02340",
            "text": "[your list]"
          },
          {
            "value": "T02400",
            "text": "Compliance requirement decks"
          },
          {
            "value": "T02410",
            "text": "Create a smaller deck by only including cards for a particular compliance requirement."
          },
          {
            "value": "T02420",
            "text": "Compliance requirement"
          },
          {
            "value": "T02430",
            "text": "Data validation and encoding"
          },
          {
            "value": "T02440",
            "text": "[compliance list]"
          },
          {
            "value": "T02450",
            "text": "Authentication"
          },
          {
            "value": "T02460",
            "text": "[compliance list]"
          },
          {
            "value": "T02470",
            "text": "Session management"
          },
          {
            "value": "T02480",
            "text": "[compliance list]"
          },
          {
            "value": "T02490",
            "text": "Authorization"
          },
          {
            "value": "T02500",
            "text": "[compliance list]"
          },
          {
            "value": "T02510",
            "text": "Cryptography"
          },
          {
            "value": "T02520",
            "text": "[compliance list]"
          },
          {
            "value": "T02530",
            "text": "Cornucopia"
          },
          {
            "value": "T02540",
            "text": "[compliance list]"
          },
          {
            "value": "T02600",
            "text": "Frequently asked questions"
          },
          {
            "value": "T02610",
            "text": "1. Can I copy or edit the game?"
          },
          {
            "value": "T02620",
            "text": "Yes of course."
          },
          {
            "value": "T02630",
            "text": "All OWASP materials are free to do with as you like provided you comply with the Creative Commons Attribution-ShareAlike 3.0 license. "
          },
          {
            "value": "T02640",
            "text": "Perhaps if you create a new version, you might donate it to the OWASP Cornucopia Project?"
          },
          {
            "value": "T02650",
            "text": "2. How can I get involved?"
          },
          {
            "value": "T02660",
            "text": "Please send ideas or offers of help to the project’s mailing list."
          },
          {
            "value": "T02670",
            "text": "3. How were the attackers’ names chosen?"
          },
          {
            "value": "T02680",
            "text": "EoP begins every description with words like 'An attacker can...'. "
          },
          {
            "value": "T02690",
            "text": "These have to be phrased as an attack but I was not keen on the anonymous terminology, wanting something more engaging, and therefore used personal names. "
          },
          {
            "value": "T02700",
            "text": "These can be thought of as external or internal people or aliases for computer systems. But instead of just random names, I thought how they might reflect the OWASP community aspect. "
          },
          {
            "value": "T02710",
            "text": "Therefore, apart from 'Alice and Bob' I use the given (first) names of current and recent OWASP employees and Board members (assigned in no order), and then randomly selected the remaining 50 or so names from the current list of paying individual OWASP members. "
          },
          {
            "value": "T02720",
            "text": "No name was used more than once, and where people had provided two personal names, I dropped one part to try to ensure no-one can be easily identified. "
          },
          {
            "value": "T02730",
            "text": "Names were not deliberately allocated to any particular attack, defence or requirement. The cultural and gender mix simply reflects theses sources of names, and is not meant to be world-representative."
          },
          {
            "value": "T02740",
            "text": "In v1.20, the name on VE-10 changed to reflect the project’s new co-leader - this card is also the only one with two names in the attack."
          },
          {
            "value": "T02750",
            "text": "4. Why aren’t there any images on the card faces?"
          },
          {
            "value": "T02760",
            "text": "There is quite a lot of text on the cards, and the cross-referencing takes up space too. "
          },
          {
            "value": "T02770",
            "text": "But it would be great to have additional design elements included. "
          },
          {
            "value": "T02780",
            "text": "Any volunteer"
          },
          {
            "value": "T02790",
            "text": "5. Are the attacks ranked by the number on the card?"
          },
          {
            "value": "T02800",
            "text": "Only approximately."
          },
          {
            "value": "T02810",
            "text": "The risk will be application and organisation dependent, due to varying security and compliance requirements, so your own severity rating may place the cards in some other order than the numbers on the cards."
          },
          {
            "value": "T02820",
            "text": "6. How long does it take to play a round of cards using the full deck?"
          },
          {
            "value": "T02830",
            "text": "This depends upon the amount of discussion and how familiar the players are with application security concepts."
          },
          {
            "value": "T02840",
            "text": "But perhaps allow 1.5 to 2.0 hours for 4-6 people."
          },
          {
            "value": "T02850",
            "text": "7. What sort of people should play the game?"
          },
          {
            "value": "T02860",
            "text": "Always try to have a mix of roles who can contribute alternative perspectives."
          },
          {
            "value": "T02870",
            "text": "But include someone who has a reasonable knowledge of application vulnerability terminology. "
          },
          {
            "value": "T02880",
            "text": "Otherwise try to include a mix of architects, developers, testers and a relevant project manager or business owner."
          },
          {
            "value": "T02890",
            "text": "8. Who should take notes and record scores?"
          },
          {
            "value": "T02900",
            "text": "It is better if that someone else, not playing the game, takes notes about the requirements identified and issues discussed."
          },
          {
            "value": "T02910",
            "text": "This could be used as training for a more junior developer, or performed by the project manager."
          },
          {
            "value": "T02920",
            "text": "Some organisations have made a recording to review afterwards when the requirements are written up more formally."
          },
          {
            "value": "T02930",
            "text": "9. Should we always use the full deck of cards?"
          },
          {
            "value": "T02940",
            "text": "No. "
          },
          {
            "value": "T02950",
            "text": "A smaller deck is quicker to play. "
          },
          {
            "value": "T02960",
            "text": "Start your first game with only enough cards for two or three rounds. "
          },
          {
            "value": "T02970",
            "text": "Always consider removing cards that are not appropriate at all of the target application or function being reviewed. "
          },
          {
            "value": "T02980",
            "text": "For the first few times people play the game it is also usually better to remove the Aces and the two Jokers."
          },
          {
            "value": "T02990",
            "text": "It is also usual to play the game without any trumps suit until people are more familiar with the idea."
          },
          {
            "value": "T03000",
            "text": "10. What should players do when they have an Ace card that says “invented a new X attack”?"
          },
          {
            "value": "T03010",
            "text": "The player can make up any attack they think is valid, but must match the suit of the card (e.g. data validation and encoding)."
          },
          {
            "value": "T03020",
            "text": "With players new to the game, it can be better to remove these to begin with (see also FAQ 9)."
          },
          {
            "value": "T03030",
            "text": "11. I don’t understand what the attack means on each card - is there more detailed information?"
          },
          {
            "value": "T03040",
            "text": "Yes, the online Wiki Deck at was created to help players understand the attacks. "
          },
          {
            "value": "T03050",
            "text": "See"
          },
          {
            "value": "T03060",
            "text": "12. My company wants to print its own version of OWASP Cornucopia - what license do we need to refer to?"
          },
          {
            "value": "T03070",
            "text": "Please refer to the full answer to this question on the project’s web pages at"
          },
          {
            "value": "T03100",
            "text": "Change Log"
          },
          {
            "value": "T03110",
            "text": "Version / Date"
          },
          {
            "value": "T03120",
            "text": "Comments"
          },
          {
            "value": "T03130",
            "text": "0.1"
          },
          {
            "value": "T03140",
            "text": "Original Draft"
          },
          {
            "value": "T03150",
            "text": "0.2"
          },
          {
            "value": "T03160",
            "text": "Draft reviewed and updated"
          },
          {
            "value": "T03170",
            "text": "0.3"
          },
          {
            "value": "T03180",
            "text": "Draft announced OWASP SCP mailing list for comment."
          },
          {
            "value": "T03190",
            "text": "0.4"
          },
          {
            "value": "T03200",
            "text": "Play rules updated based on feedback during workshops. "
          },
          {
            "value": "T03210",
            "text": "Added reference to PCI SSC Information Supplement: PCI DSS E-commerce Guidelines. "
          },
          {
            "value": "T03220",
            "text": "Descriptive text extended and updated."
          },
          {
            "value": "T03230",
            "text": "Added contributors section, page numbering, FAQs and change log."
          },
          {
            "value": "T03240",
            "text": "1"
          },
          {
            "value": "T03250",
            "text": "Release."
          },
          {
            "value": "T03260",
            "text": "1.01"
          },
          {
            "value": "T03270",
            "text": "Framework-specific card deck discussion added"
          },
          {
            "value": "T03280",
            "text": "Additional FAQs created. "
          },
          {
            "value": "T03290",
            "text": "Descriptive text updated. "
          },
          {
            "value": "T03300",
            "text": "New cover image, and previous cover image moved to back. "
          },
          {
            "value": "T03310",
            "text": "Cut lines added."
          },
          {
            "value": "T03320",
            "text": "FAQs 5 and 6 added."
          },
          {
            "value": "T03330",
            "text": "Attack descriptions on cards with tinted backgrounds changed to black (from dark grey). "
          },
          {
            "value": "T03340",
            "text": "Project contributors added."
          },
          {
            "value": "T03350",
            "text": "1.02"
          },
          {
            "value": "T03360",
            "text": "Warning about time to print added. "
          },
          {
            "value": "T03370",
            "text": "Additional alternative game rules added (twenty-one, play a deck over a week, play full hand and then discuss). "
          },
          {
            "value": "T03380",
            "text": "Compliance deck concept added. "
          },
          {
            "value": "T03390",
            "text": "FAQs 5 and 6 added."
          },
          {
            "value": "T03400",
            "text": "Attack descriptions on cards with tinted backgrounds changed to black (from dark grey). "
          },
          {
            "value": "T03410",
            "text": "Project contributors added."
          },
          {
            "value": "T03420",
            "text": "1.03"
          },
          {
            "value": "T03430",
            "text": "Minor attack wording changes on two cards. "
          },
          {
            "value": "T03440",
            "text": "OWASP SCP and ASVS cross-references checked and updated. "
          },
          {
            "value": "T03450",
            "text": "Code letters added for suits. "
          },
          {
            "value": "T03460",
            "text": "All remaining attack descriptions on cards changed to black (from dark grey) and background colours amended to provide more contrast and increase readability."
          },
          {
            "value": "T03470",
            "text": "1.04"
          },
          {
            "value": "T03480",
            "text": "Text “password change, password change,” corrected to “password change, password recovery,” on Queen of Authentication card. "
          },
          {
            "value": "T03490",
            "text": "1.05"
          },
          {
            "value": "T03500",
            "text": "Updates to alternative game rules. "
          },
          {
            "value": "T03510",
            "text": "Additional FAQs created. "
          },
          {
            "value": "T03520",
            "text": "Contributors updated. "
          },
          {
            "value": "T03530",
            "text": "Podcast and video links added."
          },
          {
            "value": "T03540",
            "text": "1.1"
          },
          {
            "value": "T03550",
            "text": "Change log date corrected for v1.05. Cross-references updated for 2014 version of ASVS. "
          },
          {
            "value": "T03560",
            "text": "Contributors updated."
          },
          {
            "value": "T03570",
            "text": "Minor text changes to cards to improve readability."
          },
          {
            "value": "T03580",
            "text": "1.2"
          },
          {
            "value": "T03590",
            "text": "Video mentioned/linked"
          },
          {
            "value": "T03600",
            "text": "Separate score sheet mentioned/linked. "
          },
          {
            "value": "T03610",
            "text": "Previous embedded score sheet pages deleted"
          },
          {
            "value": "T03620",
            "text": "Correction (identified by Tom Brennan) and addition to "
          },
          {
            "value": "T03630",
            "text": "text on card 8 Authentication. "
          },
          {
            "value": "T03640",
            "text": "Oana Cornea and other participants at the AppSec EU 2015 project summit added to list of contributors. "
          },
          {
            "value": "T03650",
            "text": "Darío De Filippis added as project co-leader. "
          },
          {
            "value": "T03660",
            "text": "Wiki Deck link added"
          },
          {
            "value": "T03670",
            "text": "Cross-references updated for ASVS v3.0.1 and CAPEC v2.8. Minor text changes to a small number of cards. "
          },
          {
            "value": "T03680",
            "text": "Added “-EN” to version number in preparation for “-ES” version."
          },
          {
            "value": "T03690",
            "text": "Susana Romaniz added as a contributor to the Spanish translation."
          },
          {
            "value": "T03700",
            "text": "Minor text changes to instructions and FAQs."
          },
          {
            "value": "T03800",
            "text": "Project contributors"
          },
          {
            "value": "T03810",
            "text": "All OWASP projects rely on the voluntary efforts of people in the software development and information security sectors. "
          },
          {
            "value": "T03820",
            "text": "They have contributed their time and energy to make suggestions, provide feedback, write, review and edit documentation, give encouragement, trial the game, and promote the concept. "
          },
          {
            "value": "T03830",
            "text": "Without all their efforts, the project would not have progressed to this point. "
          },
          {
            "value": "T03840",
            "text": "Please contact the mailing list or project leaders directly, if anyone is missing from the below lists."
          },
          {
            "value": "T03850",
            "text": "•OWASP’s hard-working employees, especially Kate Hartmann"
          },
          {
            "value": "T03860",
            "text": "•Attendees at OWASP London, OWASP Manchester, OWASP Netherlands and OWASP Scotland chapter meetings, and the London Gamification meetup, who made helpful suggestions and asked challenging questions"
          },
          {
            "value": "T03870",
            "text": "•Blackfoot UK Limited for gifting print-ready design files and hundreds of professionally printed card decks for distribution by post and at OWASP chapter meetings"
          },
          {
            "value": "T03880",
            "text": "•OWASP NYC for creating an OWASP box design and distributing packs at AppSec USA 2014."
          },
          {
            "value": "T03900",
            "text": "Podcasts and videos"
          },
          {
            "value": "T03910",
            "text": "The following supporting OWASP Cornucopia resources are available online:"
          },
          {
            "value": "T03920",
            "text": "Video - Using the cards, created during AppSec EU 2015 project summit, 20th May 2015"
          },
          {
            "value": "T03930",
            "text": "Podcast interview, OWASP 24/7 Podcast channel, 21st March 2014"
          },
          {
            "value": "T03940",
            "text": "\tVideo of presentation, OWASP EU Tour 2013 London, 3rd June 2013"
          },
          {
            "value": "T03950",
            "text": "See the project website for further information and presentation materials."
          }
        ]
      }
    ]
  }

  export default data;