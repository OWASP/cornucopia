# OWASP Cornucopia project

OWASP Cornucopia is a mechanism in the form of a card game to assist software development teams 
identify security requirements in Agile, conventional and formal development processes. 
It is language, platform and technology agnostic.

## Changes & Updates

### 2021-05-28

Updated templates with tags.
convert.py script pulls language files data and replaces tags with language text.
Functions available to output idml files or docx files.

Script can also create template files using the matching text to populate with tags. 
As text does not all match correctly, this function still requires manual intervention for completing the template setup.

Todo: 
Add meta data to the processing for editions, languages and versions.
Add logging.
Add testing.

### 2024-04-30

- Adding editions, languages and versions to the deck converter.
- Adding the mobile app edition.
- Adding functionality for building the leaflet.
- Update the ASVS mapping version to ASVS 4.0.3.

### 2024-06-03

- Adding layouts
- Remove styles as an option, use layouts instead.
- Remove filetypes and introduce templates instead.
- Adding the tarot layout and renaming static to bridge
- Removing old versions prior to 1.22
- Adding fuzzing

### 2024-10-25

- Adding the Italian translation by Ruggero DallAglio
- Fixing the card codes ensuring they are in line with the documentation.

### 2024-10-30

- Adding the Portuguese pt-pt translation by André Ferreira

### 2025-02-03

- Adding the OWASP Cornucopia website

### 2025-02-07

- Design changes to accomodate for the QR codes

### 2025-02-26

- Adding the Russian translation by Andrey Danin
- Changing all the fonts to Noto Sans for better language support
- Adding CRE to the Website App Edition

### 2025-05-23

- Adding Copi - The Cornucopia Game Engine

### 2025-06-09

- Adding Elevation of MLSec through Copi

## Changes $ Updates

### 2025-06-23

- Adding OWASP Cumulus through Copi

### 2025-08-12

- Migrated the cross-references from SCP to the DevGuide Web Checklist v4.1.9
and ASVS from v4.0.3 to v5.0. The text on the cards has been updated to include
MFA and passkeys as an option for authentication. Cards within the session
management suit have been updated toe align with modern session management
practices.
